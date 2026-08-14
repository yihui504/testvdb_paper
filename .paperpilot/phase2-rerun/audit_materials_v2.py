#!/usr/bin/env python3
"""v2 材料包（tvdb_sessions）深入审核 — 确定性检查。

检查维度：
  1. 结构完整性：71 session 三方一致（cases_index scored ↔ defect_id_map ↔ 文件系统）
  2. stage2_aggregation 形态真实性（4-key 集合、中性 summary/aggregator、单 confirmed、无多余字段）
  3. 19 处标签修正生效（对照 fix_stage2_labels_v2.py）
  4. 匿名一致性（confirmed key = 目录名；output log 名匹配；.srcdir 指向存在）
  5. 泄漏扫描：全材料文件（含 output log）扫实验元话语词 + 样本 issue 号
  6. stage2 related_issue_numbers 样本号泄露
  7. intelligence 清洗零残留（样本号）
  8. 版本级契约文件齐全（15 版本 × {api_templates.md, structured_contract.json}）
  9. 三树 ↔ v2 一致性（endpoint/defect_type/severity_level 值一致，防 drift）
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
V2 = r'C:/Users/11428/Desktop/tvdb_sessions'
TREES = ('run', 'run2', 'run3')

CASES = json.load(open(os.path.join(ROOT, 'cases_index.json'), encoding='utf-8'))
SCORED = [c for c in CASES if c['group'] in ('A', 'B', 'C')]
ID_MAP = json.load(open(os.path.join(ROOT, 'defect_id_map.json'), encoding='utf-8'))

# 敏感号：A/B/C 样本号（GT 保护范围）+ D 组号（dup 链可能引向样本 GT）
SAMPLE_NUMS = {c['num'] for c in SCORED}
ALL_NUMS = {c['num'] for c in CASES}

# 实验元话语词（材料侧不该出现的）
LEAK_WORDS = [
    'rerun', 'phase2', 'run1', 'run2', 'run3', 'curated',
    '重审', '重判', '排雷', '实验', '判词', '裁决方向', '修正', '别判', '无污染',
]

# 19 处修正的预期新值（来自 fix_stage2_labels_v2.py，逐字对齐）
EXPECT_ENDPOINT = {
    'milvus_47767': 'entities+search', 'milvus_49823': 'entities+search',
    'milvus_49843': 'collections+create', 'milvus_49844': 'entities+query',
    'milvus_49889': 'collections+list', 'milvus_49890': 'collections+list',
    'milvus_49929': 'indexes+create', 'milvus_49930': 'entities+search',
    'milvus_50193': 'collections+get_stats', 'milvus_50194': 'entities+search',
    'milvus_50323': 'entities+delete', 'milvus_50325': 'collections+create',
    'milvus_51085': 'collections+create', 'milvus_52309': 'entities+search',
    'milvus_52312': 'entities+upsert',
    'qdrant_9373': 'collections+{collection_name}+points+scroll',
    'weaviate_11399': 'POST /schema', 'weaviate_11400': 'POST /schema',
}
EXPECT_DEFECT_TYPE = {'milvus_49059': 'behavior'}

fails = []
warns = []


def fail(msg: str) -> None:
    fails.append(msg)


def warn(msg: str) -> None:
    warns.append(msg)


def anon_of(vendor: str, num: int) -> str:
    return next(d for d, r in ID_MAP.items() if r['orig'] == '%s_%d' % (vendor, num))


def num_in_text(text: str, nums) -> list:
    """返回文本中出现的敏感 issue 号（#NNN 或裸 4-6 位数字均可疑，只报 #NNN 与 word 边界裸号）。"""
    found = []
    for m in re.finditer(r'#(\d{4,6})', text):
        n = int(m.group(1))
        if n in nums and n not in found:
            found.append(n)
    return found


def walk_text_files(root: str) -> list:
    """返回 root 下所有文本文件路径（log/md/json/txt，无扩展名的 .srcdir 也含）。"""
    out = []
    for dirpath, _, fns in os.walk(root):
        for fn in fns:
            p = os.path.join(dirpath, fn)
            try:
                open(p, encoding='utf-8').read(4096)
                out.append(p)
            except (UnicodeDecodeError, OSError):
                pass
    return out


def main() -> None:
    # ---- 1. 结构完整性 ----
    n_session_dirs = 0
    for c in SCORED:
        did = anon_of(c['vendor'], c['num'])
        d = os.path.join(V2, 'sessions', c['vendor'], c['version'], did)
        if not os.path.isdir(d):
            fail('missing dir: %s' % d)
            continue
        n_session_dirs += 1
        for req in ('.srcdir', 'output_%s.log' % did, os.path.join('debate_logs', 'stage2_aggregation.json')):
            if not os.path.isfile(os.path.join(d, req)):
                fail('missing file: %s/%s' % (d, req))
        extra = [f for f in os.listdir(d) if f not in ('.srcdir', 'output_%s.log' % did, 'debate_logs')]
        if extra:
            warn('extra files in %s: %s' % (did, extra))
    if n_session_dirs != 71:
        fail('session dirs = %d, expect 71' % n_session_dirs)

    # ---- 2/3/4/6. stage2 形态 + 修正生效 + 匿名一致 + related_issue_numbers ----
    for c in SCORED:
        vendor, num, ver = c['vendor'], c['num'], c['version']
        did = anon_of(vendor, num)
        p = os.path.join(V2, 'sessions', vendor, ver, did, 'debate_logs', 'stage2_aggregation.json')
        if not os.path.isfile(p):
            continue
        agg = json.load(open(p, encoding='utf-8'))
        if set(agg.keys()) != {'summary', 'aggregator', 'confirmed', 'rejected'}:
            fail('%s stage2 keys=%s' % (did, sorted(agg.keys())))
        if agg.get('summary') != '1 candidate confirmed by quartet debate':
            fail('%s summary=%r' % (did, agg.get('summary')))
        if agg.get('aggregator') != 'aggregate_votes.py':
            fail('%s aggregator=%r' % (did, agg.get('aggregator')))
        conf = agg.get('confirmed', {})
        if len(conf) != 1 or did not in conf:
            fail('%s confirmed keys=%s' % (did, list(conf)))
            continue
        c0 = conf[did]
        expect_fields = {'defect_id', 'endpoint', 'defect_type', 'severity_level', 'confirmed', 'related_issue_numbers'}
        if set(c0.keys()) != expect_fields:
            fail('%s confirmed fields=%s' % (did, sorted(c0.keys())))
        if c0.get('defect_id') != did:
            fail('%s confirmed.defect_id=%r' % (did, c0.get('defect_id')))
        if agg.get('rejected') != {}:
            fail('%s rejected non-empty' % did)
        # 19 处修正生效
        orig = '%s_%d' % (vendor, num)
        if orig in EXPECT_ENDPOINT and c0.get('endpoint') != EXPECT_ENDPOINT[orig]:
            fail('%s endpoint=%r expect %r' % (did, c0.get('endpoint'), EXPECT_ENDPOINT[orig]))
        if orig in EXPECT_DEFECT_TYPE and c0.get('defect_type') != EXPECT_DEFECT_TYPE[orig]:
            fail('%s defect_type=%r expect %r' % (did, c0.get('defect_type'), EXPECT_DEFECT_TYPE[orig]))
        # related_issue_numbers：样本号 = GT 泄露通道（SOP 解禁 github.com，匿名 did 挡不住 related 号）
        rels = c0.get('related_issue_numbers', [])
        for n in rels:
            if n in SAMPLE_NUMS:
                fail('%s related_issue_numbers 含样本号 %d（GT 泄露）' % (did, n))
            elif n in ALL_NUMS:
                warn('%s related_issue_numbers 含 D 组号 %d' % (did, n))

    # ---- 5. 泄漏词 + 样本号扫描（全材料文本文件） ----
    files = walk_text_files(os.path.join(V2, 'sessions'))
    files += walk_text_files(os.path.join(V2, 'intelligence'))
    for p in files:
        rel = os.path.relpath(p, V2)
        text = open(p, encoding='utf-8').read()
        for w in LEAK_WORDS:
            if w in text:
                fail('泄漏词 %r in %s' % (w, rel))
        nums = num_in_text(text, SAMPLE_NUMS)
        if nums:
            warn('样本号 %s in %s' % (nums, rel))

    # ---- 5b. 裸号扫描：探针命名（test_47763 等无 # 前缀）查全部样本号 ----
    for c in SCORED:
        did = anon_of(c['vendor'], c['num'])
        lp = os.path.join(V2, 'sessions', c['vendor'], c['version'], did, 'output_%s.log' % did)
        if not os.path.isfile(lp):
            continue
        text = open(lp, encoding='utf-8').read()
        hit = sorted(n for n in SAMPLE_NUMS if re.search(r'(?<![0-9])%d(?![0-9])' % n, text))
        if hit:
            warn('%s output log 含裸样本号 %s' % (did, hit))

    # ---- 7. intelligence 零残留 ----
    for vendor in ('milvus', 'qdrant', 'weaviate'):
        for fn in ('developer_cognition.json', 'bug_shapes.json'):
            p = os.path.join(V2, 'intelligence', vendor, fn)
            d = json.load(open(p, encoding='utf-8'))

            def scan(node):
                if isinstance(node, dict):
                    for k, v in node.items():
                        if k in ('known_instances', 'historical_instances', 'example_issues', 'source_issues') and isinstance(v, list):
                            for it in v:
                                n = it.get('issue_number') if isinstance(it, dict) else it
                                if isinstance(n, int) and n in SAMPLE_NUMS:
                                    fail('intelligence %s/%s 样本号残留: %s=%s' % (vendor, fn, k, n))
                        else:
                            scan(v)
                elif isinstance(node, list):
                    for it in node:
                        scan(it)
                elif isinstance(node, str):
                    for m in re.finditer(r'#(\d{4,6})', node):
                        if int(m.group(1)) in SAMPLE_NUMS:
                            fail('intelligence %s/%s 文本残留 #%s' % (vendor, fn, m.group(1)))
            scan(d)

    # ---- 8. 版本级契约 ----
    versions = {(c['vendor'], c['version']) for c in SCORED}
    for vendor, ver in sorted(versions):
        vdir = os.path.join(V2, 'sessions', vendor, ver)
        for fn in ('api_templates.md', 'structured_contract.json'):
            if not os.path.isfile(os.path.join(vdir, fn)):
                fail('missing %s/%s/%s' % (vendor, ver, fn))

    # ---- 9. 三树 ↔ v2 一致性 ----
    for c in SCORED:
        vendor, num, ver = c['vendor'], c['num'], c['version']
        did = anon_of(vendor, num)
        p2 = os.path.join(V2, 'sessions', vendor, ver, did, 'debate_logs', 'stage2_aggregation.json')
        if not os.path.isfile(p2):
            continue
        c2 = json.load(open(p2, encoding='utf-8'))['confirmed'][did]
        for tree in TREES:
            pt = os.path.join(ROOT, tree, 'results', vendor, ver, str(num), 'debate_logs', 'stage2_aggregation.json')
            if not os.path.isfile(pt):
                fail('%s 三树 %s 缺 stage2_aggregation' % (did, tree))
                continue
            ct = json.load(open(pt, encoding='utf-8'))
            tconf = ct.get('confirmed', {})
            key = '%s_%d' % (vendor, num)
            if key not in tconf:
                fail('%s 三树 %s confirmed 无 key %s' % (did, tree, key))
                continue
            for field in ('endpoint', 'defect_type', 'severity_level'):
                if tconf[key].get(field) != c2.get(field):
                    fail('%s %s 三树 %s 不一致: %r vs v2 %r' % (did, field, tree, tconf[key].get(field), c2.get(field)))

    # ---- 10. 空日志 ----
    for c in SCORED:
        did = anon_of(c['vendor'], c['num'])
        lp = os.path.join(V2, 'sessions', c['vendor'], c['version'], did, 'output_%s.log' % did)
        if os.path.isfile(lp) and os.path.getsize(lp) < 30 and did != 'milvus_001':
            fail('%s 空 output log（milvus_001 例外）' % did)

    print('FAIL %d | WARN %d' % (len(fails), len(warns)))
    for m in fails:
        print('  [FAIL]', m)
    for m in warns:
        print('  [WARN]', m)


if __name__ == '__main__':
    main()

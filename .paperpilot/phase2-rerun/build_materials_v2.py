#!/usr/bin/env python3
"""构建 v2 材料包（tvdb_sessions）：把审计发现的形态偏差/泄露全部在材料层修复。

从 run/（排雷后的材料树）+ intel/ 源生成包，修复（见 docs/phase2-audit-report.md §5）：
  1. 中性路径 tvdb_sessions/sessions/{target}/{version}/{seq}/（无 phase2/rerun/run 字样）
  2. 匿名 defect_id {vendor}_{seq}（seq 按 vendor 编号）；映射存 defect_id_map.json（实验侧，不进材料树）
  3. 真实形态 stage2_aggregation（aggregator=aggregate_votes.py，summary 中性，无 rerun/GT note）
  4. 清洗 intelligence（剔除与样本重叠的 issue number，保留抽象模式）
  5. output_*.log 重命名匿名带入（空日志 case 由 fill_raw_v2.py 另行补 raw）
产物: C:/Users/11428/Desktop/tvdb_sessions/ + defect_id_map.json
构建顺序: build_materials_v2.py（重建包）→ fill_raw_v2.py <ver>（补空日志 raw）
"""
import json
import os
import re
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
CASES = json.load(open(os.path.join(ROOT, 'cases_index.json'), encoding='utf-8'))
SCORED = [c for c in CASES if c['group'] in ('A', 'B', 'C')]

OUT = r'C:/Users/11428/Desktop/tvdb_sessions'
MAP_PATH = os.path.join(ROOT, 'defect_id_map.json')


def seq_defect_ids():
    """vendor -> 按 (version, num) 稳定排序的 seq 编号。"""
    by_vendor = {}
    for c in SCORED:
        by_vendor.setdefault(c['vendor'], []).append(c)
    mapping = {}
    for v, cs in by_vendor.items():
        for i, c in enumerate(sorted(cs, key=lambda x: (x['version'], x['num'])), 1):
            mapping['%s_%s' % (v, c['num'])] = '%s_%03d' % (v, i)
    return mapping


def clean_intelligence(src_dir, dst_dir, sample_nums):
    """复制 intelligence，剔除 known_instances/example_issues 里与样本重叠的 issue number。"""
    os.makedirs(dst_dir, exist_ok=True)
    for fn in ('developer_cognition.json', 'bug_shapes.json'):
        d = json.load(open(os.path.join(src_dir, fn), encoding='utf-8'))
        _strip_issue_refs(d, sample_nums)
        json.dump(d, open(os.path.join(dst_dir, fn), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def _strip_issue_refs(node, sample_nums):
    if isinstance(node, dict):
        for k, v in list(node.items()):
            if k in ('known_instances', 'historical_instances', 'example_issues', 'examples', 'source_issues'):
                if isinstance(v, list):
                    filtered = []
                    for it in v:
                        if isinstance(it, dict) and it.get('issue_number') in sample_nums:
                            continue
                        if isinstance(it, (int, float)) and int(it) in sample_nums:
                            continue
                        filtered.append(it)
                    node[k] = filtered
            elif isinstance(v, (dict, list, str)):
                node[k] = _strip_issue_refs(v, sample_nums)
    elif isinstance(node, list):
        return [_strip_issue_refs(it, sample_nums) for it in node]
    elif isinstance(node, str):
        return re.sub(r'#(\d{4,6})', lambda m: '#<tracked>' if int(m.group(1)) in sample_nums else m.group(0), node)
    return node


def real_form_aggregation(did, old_agg):
    """真实形态 stage2_aggregation（模拟 aggregate_votes.py 输出，去实验元话语）。"""
    old_c = list(old_agg['confirmed'].values())[0]
    return {
        'summary': '1 candidate confirmed by quartet debate',
        'aggregator': 'aggregate_votes.py',
        'confirmed': {
            did: {
                'defect_id': did,
                'endpoint': old_c.get('endpoint', ''),
                'defect_type': old_c.get('defect_type', 'unknown'),
                'severity_level': old_c.get('severity_level', 'High'),
                'confirmed': True,
                'related_issue_numbers': old_c.get('related_issue_numbers', []),
            }
        },
        'rejected': {},
    }


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    id_map = seq_defect_ids()
    sample_nums = {c['num'] for c in SCORED}

    # intelligence（版本级不区分 vendor，源在 intel/）
    for v in ('milvus', 'qdrant', 'weaviate'):
        clean_intelligence(os.path.join(ROOT, 'intel', v), os.path.join(OUT, 'intelligence', v), sample_nums)

    # 每样本 session
    records = {}
    for c in SCORED:
        v, num, ver = c['vendor'], c['num'], c['version']
        did = id_map['%s_%s' % (v, num)]
        src = os.path.join(ROOT, 'run', 'results', v, ver, str(num))
        dst = os.path.join(OUT, 'sessions', v, ver, did)
        os.makedirs(os.path.join(dst, 'debate_logs'), exist_ok=True)

        # .srcdir 原样；output log 重命名为匿名 output_{did}.log
        shutil.copy(os.path.join(src, '.srcdir'), os.path.join(dst, '.srcdir'))
        for fn in os.listdir(src):
            if fn.startswith('output_') and fn.endswith('.log'):
                shutil.copy(os.path.join(src, fn), os.path.join(dst, 'output_%s.log' % did))
        # stage2_aggregation 真实形态
        old_agg = json.load(open(os.path.join(src, 'debate_logs', 'stage2_aggregation.json'), encoding='utf-8'))
        json.dump(real_form_aggregation(did, old_agg),
                  open(os.path.join(dst, 'debate_logs', 'stage2_aggregation.json'), 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)
        records[did] = {'vendor': v, 'version': ver, 'orig': '%s_%d' % (v, num)}

    # 版本级契约 + api_templates
    for c in SCORED:
        v, ver = c['vendor'], c['version']
        vdir = os.path.join(OUT, 'sessions', v, ver)
        if os.path.isdir(vdir) and not os.path.isfile(os.path.join(vdir, 'structured_contract.json')):
            shutil.copy(os.path.join(ROOT, 'run', 'results', v, ver, 'structured_contract.json'),
                        os.path.join(vdir, 'structured_contract.json'))
            shutil.copy(os.path.join(ROOT, 'run', 'results', v, ver, 'api_templates.md'),
                        os.path.join(vdir, 'api_templates.md'))

    json.dump(records, open(MAP_PATH, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    n_logs = 0
    empty = []
    for did, r in records.items():
        d = os.path.join(OUT, 'sessions', r['vendor'], r['version'], did)
        for f in os.listdir(d):
            if f.startswith('output_') and f.endswith('.log'):
                n_logs += 1
                if os.path.getsize(os.path.join(d, f)) < 30:
                    empty.append(did)
    print('materials_v2: %d sessions | %d output logs | map -> %s' % (len(records), n_logs, os.path.relpath(MAP_PATH, ROOT)))
    print('empty-log cases (需补 raw):', empty)


if __name__ == '__main__':
    main()

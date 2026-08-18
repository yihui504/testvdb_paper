#!/usr/bin/env python3
"""gen_dispatch_v7 — RQ2 v7 完整复测派发器（2026-08-18）。

基于 gen_dispatch_v4.py（RQ2_V4_RULES.md 纪律全继承：原生 agent 任务参数 only /
claim 锚原文引用 / R2 泄漏扫描硬门禁）。与 v4 的差异仅三处：
1. auditor 判词输出 → chain_verdicts_v7.json（不覆盖 v1-v4/e6）
2. rework 模式读 chain_verdicts_v7.json 工单
3. claim 锚兜底：packet raw_observation 为空时用 cases_index.json 该 issue 的
   title 原文（任务书口径），不再留"自定主观测"

用法:
  python gen_dispatch_v7.py <vendor> <version> <did[,did...]> [--builders|--auditor] [--rework <did>]
"""
import json
import os
import re
import sys

V2 = r'C:/Users/11428/Desktop/tvdb_sessions'
VDB_SRC = r'C:/Users/11428/Desktop/vdb_src'
PLUGIN = r'C:/Users/11428/.claude/plugins/cache/testvdb/testvdb/2.3.0'
BUILDER_SOP = PLUGIN + r'/agents/evidence-builder.md'
AUDITOR_SOP = PLUGIN + r'/agents/chain-auditor.md'
INTEL = r'C:/Users/11428/Desktop/tvdb_sessions/intelligence'
HERE = os.path.dirname(os.path.abspath(__file__))
PACKETS = os.path.join(HERE, 'packets')
DMAP = os.path.join(HERE, 'defect_id_map.json')
CASES_INDEX = os.path.join(HERE, 'cases_index.json')

VENDOR_CFG = {
    'milvus': {'live': 'milvus gRPC localhost:19530 (pymilvus) + REST v2 http://localhost:19530/v2/vectordb', 'env': ''},
    'qdrant': {'live': 'qdrant REST http://localhost:6333', 'env': ''},
    'weaviate': {'live': 'weaviate REST http://localhost:18080/v1', 'env': '环境变量 WEAVIATE_BASE=http://localhost:18080/v1'},
}

# ── R2 泄漏扫描（硬门禁，同 v4）──────────────────────────────
LEAK_PATTERNS = [
    (r'你是 TestVDB', '角色声明（原生 agent 禁）'),
    (r'GT 参考|gt_label|翻正|预期.*正|上轮判错|上一轮|复判|主验证点', '实验元话语'),
    (r'REQ ?\d+ ?是主|主违规观测 ?=|次观测，记入|应记入', '主审人定位语'),
    (r'\bCONFIRMED\b(?!.{0,20}by)', 'GT 标签词（builder/auditor prompt 禁现）'),
    (r'FALSE_POSITIVE(?!_BY)', 'GT 标签词'),
]
# 候选材料原文行豁免：raw_observation / issue title / rework 工单引 claim 原文
WHITELIST = [r'raw_observation', r'候选现象声称', r'"claim"']


def leak_scan(text: str) -> list:
    """返回 [(pattern, why, hit_line)]。白名单行（候选材料原文引用）跳过。"""
    hits = []
    for line in text.splitlines():
        if any(re.search(w, line) for w in WHITELIST):
            continue
        for pat, why in LEAK_PATTERNS:
            if re.search(pat, line):
                hits.append((pat, why, line.strip()[:80]))
    return hits


def claim_anchor(did: str) -> str:
    """claim 对照锚 = packet raw_observation 原文；空则 cases_index title 原文。"""
    dmap = json.load(open(DMAP, encoding='utf-8'))
    orig = dmap[did]['orig']
    p = os.path.join(PACKETS, orig + '.json')
    if os.path.exists(p):
        ro = json.load(open(p, encoding='utf-8')).get('raw_observation')
        if ro and str(ro).strip() not in ('', 'null', 'None'):
            return '候选现象声称（packet raw_observation 原文）：\n%s' % ro
    # title 兜底（v7：18 个 raw_observation=null 的 case）
    num = int(orig.split('_')[1])
    ci = json.load(open(CASES_INDEX, encoding='utf-8'))
    e = next((x for x in ci if x.get('num') == num), None)
    if e and e.get('title'):
        return '候选现象声称（packet raw_observation 为空，用该 issue 标题原文）：\n%s' % e['title']
    return '候选现象声称：（无 packet raw_observation，按 log 全文自定主观测）'


# ── 模板（原生 agent：任务参数 only，同 v4）─────────────────
BUILDER_TMPL = """【任务】按你的 agent 规范（SOP）处理以下单个候选。

SOP 文件（你的 agent 定义同源，可 Read 交叉核对）: {sop}

## 材料
- SESSION_DIR: {sess}（output_*.log、debate_logs/、.srcdir）
- 契约: {contract}
- 源码 clone: {clone}

## 候选
defect_id={did}
{anchor}

## 产出
Write {sess}/evidence_chain/{did}.json 后 Bash touch {sess}/evidence_chain/{did}.json.done
（若已存在，覆盖写入并保持 .done）

## 汇报
一行：{did} done=<y/n>"""

BUILDER_REWORK_TMPL = """【任务】按你的 agent 规范（SOP）处理以下单个候选（重做工单轮）。

SOP 文件（你的 agent 定义同源，可 Read 交叉核对）: {sop}

## 材料
- SESSION_DIR: {sess}
- 契约: {contract}
- 源码 clone: {clone}

## 候选
defect_id={did}
{anchor}

## 打回工单（auditor 产出，按工单针对性重做）
{rework_order}

## 产出
Write {sess}/evidence_chain/{did}.json 后 Bash touch {sess}/evidence_chain/{did}.json.done

## 汇报
一行：{did} done=<y/n> rework_applied=<y/n>"""

AUDITOR_TMPL = """【任务】按你的 agent 规范（SOP）审计以下候选的全部证据链并产出组级判词。

SOP 文件（你的 agent 定义同源，可 Read 交叉核对）: {sop}

## 材料
- 版本组前缀: {sess_root}（各 case 子目录 evidence_chain/）
- 契约: {contract}
- 认知材料（视角 D）: {intel}

## 审计对象（每 case 的 {sess_root}/{{did}}/evidence_chain/{{did}}.json）
{did_lines}

## 候选现象声称对照材料（第 4 查用，packet raw_observation/title 原文）
{anchors}

## 产出
Write {out} + touch {out}.done（不覆盖其他版本判词文件）

## 汇报
一行/case：{did_list_fmt}"""


def tag_for(vendor, version):
    if vendor == 'milvus':
        return 'v2.3.22' if version == '2.3' else 'v' + version
    return 'v' + version


def main():
    argv = sys.argv[1:]
    mode = 'auditor' if '--auditor' in argv else 'builders'
    rework_did = None
    if '--rework' in argv:
        i = argv.index('--rework')
        rework_did = argv[i + 1]
        mode = 'rework'
        argv = argv[:i] + argv[i + 2:]
        pos = [a for a in argv if not a.startswith('--')]
        vendor, version, dids_s = pos[0], pos[1], '%s' % rework_did
        dids = [rework_did]
    else:
        pos = [a for a in argv if not a.startswith('--')]
        vendor, version, dids_s = pos[0], pos[1], pos[2]
        dids = dids_s.split(',')
    cfg = VENDOR_CFG[vendor]
    sess_root = '%s/sessions/%s/%s' % (V2, vendor, version)
    contract = '%s/structured_contract.json' % sess_root
    clone = '%s/%s/%s' % (VDB_SRC, vendor, tag_for(vendor, version))
    intel = '%s/%s/developer_cognition.json' % (INTEL, vendor)

    outs = []
    if mode in ('builders', 'rework'):
        for did in dids:
            if mode == 'rework':
                assert did == rework_did, '--rework 模式单 case'
                # 工单原文从 auditor v7 判词读取（主进程只搬运不解读）
                v7p = os.path.join(sess_root, 'debate_logs', 'chain_verdicts_v7.json')
                cv = json.load(open(v7p, encoding='utf-8'))
                e = next(x for x in cv['verdicts'] if x['defect_id'] == did)
                ro = e.get('rework_order') or {}
                ro_txt = json.dumps(ro, ensure_ascii=False, indent=1)
                outs.append(BUILDER_REWORK_TMPL.format(
                    sop=BUILDER_SOP, sess='%s/%s' % (sess_root, did), contract=contract,
                    clone=clone, did=did, anchor=claim_anchor(did), rework_order=ro_txt))
            else:
                outs.append(BUILDER_TMPL.format(
                    sop=BUILDER_SOP, sess='%s/%s' % (sess_root, did), contract=contract,
                    clone=clone, did=did, anchor=claim_anchor(did)))
    else:
        out = '%s/debate_logs/chain_verdicts_v7.json' % sess_root
        did_lines = '\n'.join('  - %s' % d for d in dids)
        anchors = '\n'.join('  %s: %s' % (d, claim_anchor(d).replace('\n', ' | ')) for d in dids)
        outs.append(AUDITOR_TMPL.format(
            sop=AUDITOR_SOP, sess_root=sess_root, contract=contract, intel=intel,
            did_lines=did_lines, anchors=anchors, out=out,
            did_list_fmt='<defect_id> verdict=… fp_src=… root_cause=… rework=y/n'))
        tail = '\n【目标 DB 容器】\n  ' + cfg['live']
        if cfg['env']:
            tail += '\n  ' + cfg['env']
        outs[-1] += tail

    full = ('\n' + '═' * 60 + '\n').join(outs)
    # R2 泄漏扫描（硬门禁）
    hits = leak_scan(full)
    if hits:
        print('LEAK_SCAN FAIL — 拒发：', file=sys.stderr)
        for pat, why, line in hits:
            print('  [%s] %s ← %s' % (why, pat, line), file=sys.stderr)
        sys.exit(2)
    print(full)
    print('\n[leak_scan] PASS (0 hits)', file=sys.stderr)


if __name__ == '__main__':
    main()

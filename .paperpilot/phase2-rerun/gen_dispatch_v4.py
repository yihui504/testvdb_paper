#!/usr/bin/env python3
"""gen_dispatch_v4 — RQ2 v4 派发器（RQ2_V4_RULES.md 的实现，2026-08-18）。

与 v3 生成器的差异（两条 v3 教训的修正）：
1. 原生 agent 派发：prompt 只含任务参数（case/材料路径/产出/汇报格式），
   无角色声明（"你是 TestVDB 的…"）、无 SOP 复述——SOP 由 subagent_type 自带
2. claim 对照锚：仅 packet raw_observation 原文引用，无主审人解读
3. 内置泄漏扫描（R2 硬门禁）：命中即拒发 exit 2

用法:
  python gen_dispatch_v4.py <vendor> <version> <did[,did...]> [--builders|--auditor] [--rework <did>]
  --builders   生成单 case builder prompt × N（默认）
  --auditor    生成组收口 auditor prompt
  --rework     生成 rework 重派 builder prompt（携带 auditor 工单原文）
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
PACKETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'packets')
DMAP = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'defect_id_map.json')

VENDOR_CFG = {
    'milvus': {'live': 'milvus gRPC localhost:19530 (pymilvus) + REST v2 http://localhost:19530/v2/vectordb', 'env': ''},
    'qdrant': {'live': 'qdrant REST http://localhost:6333', 'env': ''},
    'weaviate': {'live': 'weaviate REST http://localhost:18080/v1', 'env': '环境变量 WEAVIATE_BASE=http://localhost:18080/v1'},
}

# ── R2 泄漏扫描（硬门禁）──────────────────────────────────────
LEAK_PATTERNS = [
    (r'你是 TestVDB', '角色声明（原生 agent 禁）'),
    (r'GT 参考|gt_label|翻正|预期.*正|上轮判错|上一轮|复判|主验证点', '实验元话语'),
    (r'REQ ?\d+ ?是主|主违规观测 ?=|次观测，记入|应记入', '主审人定位语'),
    (r'\bCONFIRMED\b(?!.{0,20}by)', 'GT 标签词（builder/auditor prompt 禁现）'),
    (r'FALSE_POSITIVE(?!_BY)', 'GT 标签词'),
]
WHITELIST = [r'raw_observation']


def leak_scan(text: str) -> list:
    """返回 [(pattern, why, hit_line)]。白名单行（含 raw_observation 引用原文）跳过。"""
    hits = []
    for line in text.splitlines():
        if any(re.search(w, line) for w in WHITELIST):
            continue
        for pat, why in LEAK_PATTERNS:
            if re.search(pat, line):
                hits.append((pat, why, line.strip()[:80]))
    return hits


def claim_anchor(did: str) -> str:
    """R3: claim 对照锚 = packet raw_observation 原文（无解读）。"""
    dmap = json.load(open(DMAP, encoding='utf-8'))
    orig = dmap[did]['orig']
    p = os.path.join(PACKETS, orig + '.json')
    if os.path.exists(p):
        ro = json.load(open(p, encoding='utf-8')).get('raw_observation')
        if ro and str(ro).strip() not in ('', 'null', 'None'):
            return '候选现象声称（packet raw_observation 原文）：\n%s' % ro
    return '候选现象声称：（无 packet raw_observation，按 log 全文自定主观测）'


# ── 模板（原生 agent：任务参数 only）─────────────────────────
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

SOP 文件（你的 agent 定义同源）: {sop}

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

## 候选现象声称对照材料（第 4 查用，packet raw_observation 原文）
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
        argv = [a for a in argv if a not in ('--rework', rework_did)]
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
                # 工单原文从 auditor v4 判词读取（主进程只搬运不解读）
                v4p = os.path.join(sess_root, 'debate_logs', 'chain_verdicts_v4.json')
                cv = json.load(open(v4p, encoding='utf-8'))
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
        out = '%s/debate_logs/chain_verdicts_v4.json' % sess_root
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

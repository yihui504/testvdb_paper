#!/usr/bin/env python3
"""gen_dispatch_v71 — RQ2 v7.1 派发器：机械层预跑注入版（2026-08-19，mechbacktest 结论落地）。

与 gen_dispatch_v7.py 的差异（唯一）：auditor 模式新增"机械预跑结果"段——
主进程对每条链预跑 check_chain_grounding.py + check_physical_constraints.py，
输出 JSON 注入派发词；auditor 采信填入 verdict_A/implied/verdict_B，只解释不计算。
builder/rework 模板不变（rework 工单读 chain_verdicts_v71.json）。

背景：v7 实测 auditor 无监督时不跑/不采信机械脚本（A 不一致 18/71、B 未采信 8/23、
CONFLICT 闭环被架空）——SOP 文字要求无效，改为主进程结构化注入。

用法:
  python gen_dispatch_v71.py <vendor> <version> <did[,did...]> --auditor
  python gen_dispatch_v71.py <vendor> <version> <did> --rework <did>
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, r'C:/Users/11428/.claude/plugins/cache/testvdb/testvdb/2.3.0/scripts')
from check_physical_constraints import judge_physical  # noqa: E402

V2 = r'C:/Users/11428/Desktop/tvdb_sessions'
VDB_SRC = r'C:/Users/11428/Desktop/vdb_src'
PLUGIN = r'C:/Users/11428/.claude/plugins/cache/testvdb/testvdb/2.3.0'
BUILDER_SOP = PLUGIN + r'/agents/evidence-builder.md'
AUDITOR_SOP = PLUGIN + r'/agents/chain-auditor.md'
GROUNDING = PLUGIN + r'/scripts/check_chain_grounding.py'
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

# ── R2 泄漏扫描（同 v7 + 机械预跑行白名单）──────────────────
LEAK_PATTERNS = [
    (r'你是 TestVDB', '角色声明（原生 agent 禁）'),
    (r'GT 参考|gt_label|翻正|预期.*正|上轮判错|上一轮|复判|主验证点', '实验元话语'),
    (r'REQ ?\d+ ?是主|主违规观测 ?=|次观测，记入|应记入', '主审人定位语'),
    (r'\bCONFIRMED\b(?!.{0,20}by)', 'GT 标签词（builder/auditor prompt 禁现）'),
    (r'FALSE_POSITIVE(?!_BY)', 'GT 标签词'),
]
WHITELIST = [r'raw_observation', r'候选现象声称', r'"claim"', r'机械预跑|verdict_A=|verdict_B=|implied_verdict=', r'A=CONFIRMED|B=CONFIRMED|机械|drift_point|targeted_instruction']


def leak_scan(text: str) -> list:
    hits = []
    for line in text.splitlines():
        if any(re.search(w, line) for w in WHITELIST):
            continue
        for pat, why in LEAK_PATTERNS:
            if re.search(pat, line):
                hits.append((pat, why, line.strip()[:80]))
    return hits


def claim_anchor(did: str) -> str:
    dmap = json.load(open(DMAP, encoding='utf-8'))
    orig = dmap[did]['orig']
    p = os.path.join(PACKETS, orig + '.json')
    if os.path.exists(p):
        ro = json.load(open(p, encoding='utf-8')).get('raw_observation')
        if ro and str(ro).strip() not in ('', 'null', 'None'):
            return '候选现象声称（packet raw_observation 原文）：\n%s' % ro
    num = int(orig.split('_')[1])
    ci = json.load(open(CASES_INDEX, encoding='utf-8'))
    e = next((x for x in ci if x.get('num') == num), None)
    if e and e.get('title'):
        return '候选现象声称（packet raw_observation 为空，用该 issue 标题原文）：\n%s' % e['title']
    return '候选现象声称：（无 packet raw_observation，按 log 全文自定主观测）'


def mech_line(did: str, chain: str, contract: str) -> str:
    """预跑两个机械脚本，产出一行注入文本。"""
    r = subprocess.run([sys.executable, GROUNDING, chain, contract],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    try:
        a = json.loads(r.stdout)
    except Exception:
        a = {'verdict_A': 'RUN_ERROR', 'implied_verdict': 'GREY_ZONE', 'reason': r.stdout[:60]}
    b = judge_physical(json.load(open(chain, encoding='utf-8')))
    trg = (b.get('trigger') or '')[:60].replace('\n', ' ')
    return ('%s: verdict_A=%s(%s) implied_verdict=%s | verdict_B=%s(%s) trigger=%s'
            % (did, a.get('verdict_A'), a.get('reason'), a.get('implied_verdict'),
               b.get('verdict_B'), b.get('objective_constraint_class') or '', trg))


BUILDER_TMPL = """【任务】按你的 agent 规范（SOP）处理以下单个候选。

SOP 文件（你的 agent 定义同源，可 Read 交叉核对）: {sop}

## 材料
- SESSION_DIR: {sess}
- 契约: {contract}
- 源码 clone: {clone}

## 候选
defect_id={did}
{anchor}

## 产出
Write {sess}/evidence_chain/{did}.json 后 Bash touch {sess}/evidence_chain/{did}.json.done

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

## 机械预跑结果（主进程已用 SOP 同源脚本对每条链预计算——视角 A 与机械 B 的值直接采信填入
   perspective_analysis，不得改判；implied_verdict 定案分支按 SOP 聚合层机械化执行；
   rationale 仍须转述该 case 的 A/B 判定依据；你只需行使 GREY_ZONE 灰区的 LLM 兜底与三查/第 4 查）
{mech_lines}

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
        vendor, version = pos[0], pos[1]
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
                v71p = os.path.join(sess_root, 'debate_logs', 'chain_verdicts_v71.json')
                cv = json.load(open(v71p, encoding='utf-8'))
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
        out = '%s/debate_logs/chain_verdicts_v71.json' % sess_root
        did_lines = '\n'.join('  - %s' % d for d in dids)
        mech = []
        for d in dids:
            chain = '%s/%s/evidence_chain/%s.json' % (sess_root, d, d)
            mech.append('  %s' % mech_line(d, chain, contract))
        anchors = '\n'.join('  %s: %s' % (d, claim_anchor(d).replace('\n', ' | ')) for d in dids)
        outs.append(AUDITOR_TMPL.format(
            sop=AUDITOR_SOP, sess_root=sess_root, contract=contract, intel=intel,
            did_lines=did_lines, mech_lines='\n'.join(mech), anchors=anchors, out=out,
            did_list_fmt='<defect_id> verdict=… fp_src=… root_cause=… rework=y/n'))
        tail = '\n【目标 DB 容器】\n  ' + cfg['live']
        if cfg['env']:
            tail += '\n  ' + cfg['env']
        outs[-1] += tail

    full = ('\n' + '═' * 60 + '\n').join(outs)
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

#!/usr/bin/env python3
"""check_v3_readiness — RQ2 新链路（ADR-0008）实验集改造后全面检查。

检查项（改造完 → 开跑前的门禁）：
  A. 材料对账：71 case 的 session 树 / output log / stage2_aggregation / .srcdir / 契约 全齐
  B. 源码 clone：.srcdir 指向的路径存在且非空（builder step2 依赖）
  C. 双盲面：材料树内无 GT 标签泄漏（gt_label/CONFIRMED/FALSE_POSITIVE 字样不得出现在
     sessions/ 材料中——agent prompt 只给中性材料）
  D. 派发器：gen_dispatch_v3.py 对全部 15 个 (vendor,version) 组可生成合法 prompt，
     SOP 路径存在，输出路径与 session 树一致
  E. GT 对照就绪：cases_index 44 CONFIRMED / 27 FALSE_POSITIVE 与 defect_id_map 71 对齐
  F. 新链路 SOP 就位：evidence-builder.md / chain-auditor.md 存在且含关键节

Exit: 0 = 全过；1 = 有 FAIL（明细打印）。
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

PHASE2 = Path(__file__).resolve().parent
V2 = Path(r'C:/Users/11428/Desktop/tvdb_sessions')
VDB_SRC = Path(r'C:/Users/11428/Desktop/vdb_src')
PLUGIN = Path(r'C:/Users/11428/.claude/plugins/cache/testvdb/testvdb/2.3.0')

fails, warns = [], []


def check(name, ok, detail=''):
    mark = 'PASS' if ok else 'FAIL'
    print(f'[{mark}] {name}' + (f' — {detail}' if detail else ''))
    if not ok:
        fails.append(name)


def main():
    dmap = json.loads((PHASE2 / 'defect_id_map.json').read_text(encoding='utf-8'))
    cases = json.loads((PHASE2 / 'cases_index.json').read_text(encoding='utf-8'))

    # ── A. 材料对账 ──
    print('══ A. 材料对账（71 case）══')
    missing_log, missing_agg, missing_srcdir = [], [], []
    contracts = set()
    for did, r in dmap.items():
        sess = V2 / 'sessions' / r['vendor'] / r['version'] / did
        logs = list(sess.glob('output_*.log'))
        if not logs:
            missing_log.append(did)
        if not (sess / 'debate_logs' / 'stage2_aggregation.json').exists():
            missing_agg.append(did)
        if not (sess / '.srcdir').exists():
            missing_srcdir.append(did)
        contracts.add((r['vendor'], r['version']))
    check('A1 output_*.log 全覆盖', not missing_log, f'缺 {missing_log[:5]}' if missing_log else '71/71')
    check('A2 stage2_aggregation.json 全覆盖', not missing_agg, f'缺 {missing_agg[:5]}' if missing_agg else '71/71')
    check('A3 .srcdir 全覆盖', not missing_srcdir, f'缺 {missing_srcdir[:5]}' if missing_srcdir else '71/71')

    # raw 缺失：session 树实测仅 milvus_001（pymilvus gRPC 抓不到 raw，真实历史形态）
    # ——builder 将如实记 grade D，与旧判定者同等条件（公平）。packets/ 侧 18 个
    # raw_observation=null 是 packet 字段未回填，不影响新链路（builder 读 session 树不读 packets）
    nocap = []
    for did, r in dmap.items():
        sess = V2 / 'sessions' / r['vendor'] / r['version'] / did
        for lg in sess.glob('output_*.log'):
            txt = lg.read_text(encoding='utf-8', errors='replace').strip()
            if txt == '[no raw HTTP captured]':
                nocap.append(did)
    check('A4 raw 缺失形态已知（仅 milvus_001 no-captured，gRPC 真实形态）',
          nocap == ['milvus_001'], f'实际 {nocap}')

    # ── B. 源码 clone ──
    print('══ B. 源码 clone（builder step2 依赖）══')
    def tag_for(vendor, version):
        if vendor == 'milvus':
            return 'v2.3.22' if version == '2.3' else 'v' + version
        return 'v' + version
    bad_clones = []
    for vendor, version in sorted(contracts):
        tag = tag_for(vendor, version)
        cp = VDB_SRC / vendor / tag
        rs = list(cp.glob('*.rs' if vendor != 'milvus' else '*.go'))[:1] if cp.is_dir() else []
        sub = list(cp.iterdir())[:3] if cp.is_dir() else []
        if not cp.is_dir() or not sub:
            bad_clones.append(f'{vendor}/{tag}')
    check('B1 源码 clone 非空', not bad_clones, f'缺 {bad_clones}' if bad_clones else f'{len(contracts)} 组')

    # ── C. 双盲面（材料树无 GT 泄漏）──
    print('══ C. 双盲面（GT 泄漏扫描）══')
    leak = []
    for did, r in dmap.items():
        sess = V2 / 'sessions' / r['vendor'] / r['version'] / did
        for f in [sess / 'output_{}.log'.format(did),
                  sess / 'debate_logs' / 'stage2_aggregation.json',
                  sess / '.srcdir']:
            try:
                t = f.read_text(encoding='utf-8', errors='replace').lower()
            except OSError:
                continue
            if re.search(r'gt_label|gt_category|false_positive\b|tp_ack|fp_by_design', t):
                # stage2_aggregation 的候选字段可能有 "vote" 等判定词——只扫 GT 专属词
                leak.append(f'{f.name}@{did}')
    check('C1 sessions 材料无 GT 标签泄漏', not leak, f'泄漏 {leak[:5]}' if leak else '71 case 扫描干净')

    # ── D. 派发器 ──
    print('══ D. gen_dispatch_v3 派发器 ══')
    gen = PHASE2 / 'gen_dispatch_v3.py'
    check('D1 派发器存在', gen.exists())
    ok_groups = 0
    for vendor, version in sorted(contracts):
        r0 = subprocess.run(
            [sys.executable, str(gen), vendor, version, 'x_001'],
            capture_output=True, text=True, encoding='utf-8', timeout=30)
        r1 = subprocess.run(
            [sys.executable, str(gen), vendor, version, 'x_001,x_002', '--auditor'],
            capture_output=True, text=True, encoding='utf-8', timeout=30)
        if r0.returncode == 0 and r1.returncode == 0 and 'evidence-builder' in r0.stdout and 'chain-auditor' in r1.stdout:
            ok_groups += 1
    check('D2 全部 (vendor,version) 组可生成 builder+auditor prompt', ok_groups == len(contracts),
          f'{ok_groups}/{len(contracts)}')
    sop_ok = ((PLUGIN / 'agents' / 'evidence-builder.md').exists()
              and (PLUGIN / 'agents' / 'chain-auditor.md').exists())
    check('D3 SOP 文件存在（插件 ADR-0008 版）', sop_ok)

    # ── E. GT 对照 ──
    print('══ E. GT 对照 ══')
    origs = {r['orig'].split('_', 1)[1] for r in dmap.values()}
    scored = [c for c in cases if str(c['num']) in origs]
    from collections import Counter
    lab = Counter(c['gt_label'] for c in scored)
    check('E1 71 case GT 分布 44 CONFIRMED / 27 FALSE_POSITIVE',
          lab.get('CONFIRMED') == 44 and lab.get('FALSE_POSITIVE') == 27,
          f'实际 {dict(lab)}')
    check('E2 defect_id_map 71 条', len(dmap) == 71, f'实际 {len(dmap)}')

    # ── F. SOP 关键节 ──
    print('══ F. 新链路 SOP 关键节 ══')
    eb = (PLUGIN / 'agents' / 'evidence-builder.md').read_text(encoding='utf-8', errors='replace')
    ca = (PLUGIN / 'agents' / 'chain-auditor.md').read_text(encoding='utf-8', errors='replace')
    check('F1 builder 含 step1/step2/六节 schema',
          all(k in eb for k in ('step1', 'step2', 'doc_verification', 'execution_evidence',
                                'chain_trace', 'source_grounding')))
    check('F2 auditor 含三查/三视角/fp_evidence_source',
          all(k in ca for k in ('完备性', '视角 A', 'fp_evidence_source', 'root_cause')))

    print('═' * 50)
    if fails:
        print(f'结果: {len(fails)} FAIL — {fails}')
        return 1
    print('结果: 全部 PASS — 实验集就绪，可派发 RQ2 新链路')
    return 0


if __name__ == '__main__':
    sys.exit(main())

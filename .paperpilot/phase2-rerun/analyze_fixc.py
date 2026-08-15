#!/usr/bin/env python3
"""fixC 分析（按 FIXC_PLAN §4 预注册判据）：SPLIT 32 κ vs fixA 三轮 + 对错 vs 21/32 + 对照 6。"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
MAP = json.load(open(os.path.join(ROOT, 'defect_id_map.json'), encoding='utf-8'))
CASES = {(x['vendor'], x['num']): x for x in json.load(open(os.path.join(ROOT, 'cases_index.json'), encoding='utf-8'))}
GT = {}
for did, rr in MAP.items():
    e = CASES.get((rr['vendor'], int(rr['orig'].split('_')[1])))
    if e and e['group'] in ('A', 'B', 'C'):
        GT[did] = e['group']

r3 = json.load(open(os.path.join(ROOT, 'clean_run_fixes', 'fixA_run3', 'RUN_RESULTS.json'), encoding='utf-8'))
r2 = json.load(open(os.path.join(ROOT, 'clean_run_fixes', 'fixA_run2', 'RUN_RESULTS.json'), encoding='utf-8'))
t3 = {r['did']: r for r in r3['case_table']}
t2 = {r['did']: r for r in r2['case_table']}
SPLIT = [d for d in t3 if d in t2 and not (t3[d]['fixa1'] == t2[d]['fixA_run2'] == t3[d]['fixA_run3'])]
CTRL = ['milvus_022', 'milvus_035', 'milvus_043', 'qdrant_002', 'qdrant_017', 'weaviate_001']

fixc = {}
vd = os.path.join(ROOT, 'clean_run_fixes', 'fixC', 'verdicts')
for fn in os.listdir(vd):
    if fn.endswith('.json'):
        fixc[fn[:-5]] = json.load(open(os.path.join(vd, fn), encoding='utf-8'))['verdicts'][0].get('verdict')


def kappa(a, b):
    n = len(a)
    if not n:
        return None
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    pe = sum((a.count(l) / n) * (b.count(l) / n) for l in ('CONFIRMED', 'FALSE_POSITIVE'))
    return None if pe == 1 else round((po - pe) / (1 - pe), 3)


def correct(vc, did):
    want = 'CONFIRMED' if GT[did] in 'AB' else 'FALSE_POSITIVE'
    return vc == want


def main():
    out = sys.stdout
    # 主指标：SPLIT 32 κ
    ks = {}
    for name, key in (('fixA_r1', 'fixa1'), ('fixA_r2', 'fixA_run2'), ('fixA_r3', 'fixA_run3')):
        a = [fixc[d] for d in SPLIT]
        b = [t3[d][key] if key in t3[d] else t2[d][key] for d in SPLIT]
        ks[name] = kappa(a, b)
    kmed = sorted(ks.values())[1]
    # 次指标：对错
    fixc_ok = sum(1 for d in SPLIT if correct(fixc[d], d))
    maj_ok = 0
    for d in SPLIT:
        v = [t3[d]['fixa1'], t2[d]['fixA_run2'], t3[d]['fixA_run3']]
        maj = max(set(v), key=v.count)
        maj_ok += correct(maj, d)
    r1_ok = sum(1 for d in SPLIT if correct(t3[d]['fixa1'], d))
    r2_ok = sum(1 for d in SPLIT if correct(t2[d]['fixA_run2'], d))
    r3_ok = sum(1 for d in SPLIT if correct(t3[d]['fixA_run3'], d))
    # 对照
    ctrl_res = {d: (fixc[d], correct(fixc[d], d)) for d in CTRL}
    ctrl_ok = sum(1 for _, ok in ctrl_res.values() if ok)
    # fixC 与三轮各自在 SPLIT 的 agreement
    print('=== fixC 预注册判据分析 ===')
    print('SPLIT n=%d  κ(fixC vs %s)' % (len(SPLIT), ks))
    print('κ 中位 = %.3f  (判据线 0.60: %s)' % (kmed, 'PASS' if kmed >= 0.60 else 'FAIL'))
    print('SPLIT 对错: fixC %d/%d | 三轮多数 %d/%d | 单轮 r1 %d r2 %d r3 %d' %
          (fixc_ok, len(SPLIT), maj_ok, len(SPLIT), r1_ok, r2_ok, r3_ok))
    print('对照: %d/6 %s' % (ctrl_ok, {d: v[0][0] for d, v in ctrl_res.items()}))
    verdict = ('采纳' if kmed >= 0.60 and fixc_ok >= maj_ok and ctrl_ok == 6 else
               '负结果(κ升但对错降)' if kmed >= 0.60 and fixc_ok < maj_ok else '无效(κ未达标)')
    print('判据结论: %s' % verdict)
    # 逐 case 表
    rows = []
    for d in SPLIT + CTRL:
        v = [t3[d]['fixa1'], t2[d]['fixA_run2'], t3[d]['fixA_run3']]
        rows.append({'did': d, 'gt': GT[d], 'r1': v[0], 'r2': v[1], 'r3': v[2],
                     'fixC': fixc[d], 'fixC_ok': correct(fixc[d], d)})
    json.dump({'kappa': ks, 'k_median': kmed, 'split_fixc_correct': fixc_ok,
               'split_majority_correct': maj_ok, 'split_single': [r1_ok, r2_ok, r3_ok],
               'ctrl_ok': ctrl_ok, 'ctrl': ctrl_res, 'case_table': rows},
              open(os.path.join(ROOT, 'clean_run_fixes', 'fixC', 'FIXC_RESULTS.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print('-> fixC/FIXC_RESULTS.json')


if __name__ == '__main__':
    main()

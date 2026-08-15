#!/usr/bin/env python3
"""fixA 复跑轮分析：run2/run3 判词 vs GT + 与 clean/fixA-run1 对照（指标、κ、flip）。

判词源: clean_run_fixes/fixA_run{N}/verdicts/{did}.json（N=2,3）+ milvus_001 沿用 clean（例外）
对照源: clean（CLEAN_RUN_RESULTS.json case_table）、fixA-run1（clean_run_fixes/fixA/verdicts/ + 沿用）
输出: clean_run_fixes/fixA_run{N}/RUN_RESULTS.json
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
MAP = json.load(open(os.path.join(ROOT, 'defect_id_map.json'), encoding='utf-8'))
CASES = {(x['vendor'], x['num']): x for x in json.load(open(os.path.join(ROOT, 'cases_index.json'), encoding='utf-8'))}
GT = {}
for did, r in MAP.items():
    e = CASES.get((r['vendor'], int(r['orig'].split('_')[1])))
    if e and e['group'] in ('A', 'B', 'C'):
        GT[did] = e['group']


def load_run_dir(rd):
    """读 fixA_run{N}/verdicts/*.json；milvus_001 缺失时沿用 clean。"""
    out = {}
    vd = os.path.join(ROOT, 'clean_run_fixes', rd, 'verdicts')
    for fn in os.listdir(vd):
        if fn.endswith('.json'):
            try:
                d = json.load(open(os.path.join(vd, fn), encoding='utf-8'))
                out[fn[:-5]] = d['verdicts'][0].get('verdict')
            except Exception:  # noqa: BLE001
                out[fn[:-5]] = None
    return out


CLEAN = {}
for row in json.load(open(os.path.join(ROOT, 'clean_run', 'CLEAN_RUN_RESULTS.json'), encoding='utf-8'))['case_table']:
    CLEAN[row['did']] = row.get('clean')


def load_fixa_r1():
    """fixA-run1 = fixA/verdicts/(42 milvus 重判) + 其余沿用 clean。"""
    out = dict(CLEAN)
    vd = os.path.join(ROOT, 'clean_run_fixes', 'fixA', 'verdicts')
    if not os.path.isdir(vd):
        return out
    for fn in os.listdir(vd):
        if fn.endswith('.json'):
            try:
                d = json.load(open(os.path.join(vd, fn), encoding='utf-8'))
                out[fn[:-5]] = d['verdicts'][0].get('verdict')
            except Exception:  # noqa: BLE001
                pass
    return out


FIXA1 = load_fixa_r1()


def metrics(vd_map):
    rows = [(did, v, GT[did]) for did, v in vd_map.items() if did in GT and v]
    AB = [r for r in rows if r[2] in ('A', 'B')]
    C = [r for r in rows if r[2] == 'C']
    tp = sum(1 for _, v, _ in AB if v == 'CONFIRMED')
    fp = sum(1 for _, v, _ in C if v == 'CONFIRMED')
    n = len(rows)
    correct = sum(1 for d, v, g in rows if (g in 'AB') == (v == 'CONFIRMED'))
    return {'n': n, 'TP': tp, 'FN': len(AB) - tp, 'FP': fp, 'TN': len(C) - fp,
            'recall': round(tp / len(AB), 3), 'precision': round(tp / (tp + fp), 3) if tp + fp else None,
            'fp_suppression': round((len(C) - fp) / len(C), 3), 'accuracy': round(correct / n, 3)}


def kappa(a, b):
    n = len(a)
    if not n:
        return None
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    pe = sum((a.count(l) / n) * (b.count(l) / n) for l in ('CONFIRMED', 'FALSE_POSITIVE'))
    return None if pe == 1 else round((po - pe) / (1 - pe), 3)


def main():
    rd = sys.argv[1]
    cur = load_run_dir(rd)
    run2 = {}
    for did in GT:
        run2[did] = cur.get(did, CLEAN.get(did))  # milvus_001 沿用 clean
    res = {'run': rd, 'metrics': metrics(run2),
           'vs_clean': metrics({k: v for k, v in CLEAN.items()}),
           'vs_fixa1': metrics(FIXA1)}
    for name, other in (('clean', CLEAN), ('fixa1', FIXA1)):
        pair = [(run2[d], other[d]) for d in GT if run2.get(d) and other.get(d)]
        res['kappa_vs_%s' % name] = {
            'n': len(pair), 'agreement': round(sum(1 for a, b in pair if a == b) / len(pair), 3),
            'kappa': kappa([a for a, _ in pair], [b for _, b in pair]),
            'flip': [d for d in GT if run2.get(d) and other.get(d) and run2[d] != other[d]]}
    table = [{'did': d, 'group': GT[d], 'clean': CLEAN.get(d), 'fixa1': FIXA1.get(d), rd: run2.get(d)} for d in sorted(GT)]
    res['case_table'] = table
    out = os.path.join(ROOT, 'clean_run_fixes', rd, 'RUN_RESULTS.json')
    json.dump(res, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in res.items() if k != 'case_table'}, ensure_ascii=False, indent=1))
    print('-> %s' % out)


if __name__ == '__main__':
    main()

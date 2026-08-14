#!/usr/bin/env python3
"""多 run 一致性分析：对 run(=首次curated) / run2 / run3 各算 metrics，再算 run 间一致性与 κ。

每个 run 树: {ROOT}/run{,2,3}/results/{vendor}/{ver}/{num}/debate_logs/dev_review.json
输出: VARIANCE_RESULTS.json (per-run metrics + 逐 case 三 run verdict + agreement/κ + flip sets)
"""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
CASES = {(x['vendor'], x['num']): x for x in json.load(open(os.path.join(ROOT, 'cases_index.json'), encoding='utf-8'))}
RUN_TREES = {'run1': 'run', 'run2': 'run2', 'run3': 'run3'}


def load_run(tree_sub):
    """{did: verdict} for one run tree."""
    base = os.path.join(ROOT, tree_sub, 'results')
    out = {}
    if not os.path.isdir(base):
        return out
    for v in os.listdir(base):
        vd = os.path.join(base, v)
        if not os.path.isdir(vd):
            continue
        for ver in os.listdir(vd):
            nd = os.path.join(vd, ver)
            if not os.path.isdir(nd):
                continue
            for num in os.listdir(nd):
                dr = os.path.join(nd, num, 'debate_logs', 'dev_review.json')
                if not os.path.isfile(dr):
                    continue
                try:
                    d = json.load(open(dr, encoding='utf-8'))
                    vd0 = d['verdicts'][0]
                    out['%s_%s' % (v, num)] = {
                        'verdict': vd0.get('verdict'),
                        'conf': vd0.get('confidence'),
                    }
                except Exception as e:  # noqa: BLE001
                    out['%s_%s' % (v, num)] = {'verdict': None, 'err': str(e)}
    return out


def metrics(verdicts):
    """verdicts: {did: {...}}. 仅计 A∪B∪C 中有的."""
    rows = []
    for did, v in verdicts.items():
        vendor, num = did.rsplit('_', 1)
        e = CASES.get((vendor, int(num)))
        if not e or e['group'] not in ('A', 'B', 'C'):
            continue
        rows.append((did, v.get('verdict'), e['group']))
    AB = [r for r in rows if r[2] in ('A', 'B')]
    C = [r for r in rows if r[2] == 'C']
    tp = sum(1 for _, vd, _ in AB if vd == 'CONFIRMED')
    fn = sum(1 for _, vd, _ in AB if vd == 'FALSE_POSITIVE')
    fp = sum(1 for _, vd, _ in C if vd == 'CONFIRMED')
    tn = sum(1 for _, vd, _ in C if vd == 'FALSE_POSITIVE')
    return {
        'n': len(rows), 'TP': tp, 'FN': fn, 'FP': fp, 'TN': tn,
        'recall': round(tp / len(AB), 3) if AB else None,
        'precision': round(tp / (tp + fp), 3) if (tp + fp) else None,
        'fp_suppression': round(tn / len(C), 3) if C else None,
    }


def cohen_kappa(a, b):
    """a,b: aligned verdict lists (binary CONFIRMED vs not)."""
    n = len(a)
    if n == 0:
        return None
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    labels = ['CONFIRMED', 'FALSE_POSITIVE']
    pe = 0
    for la in labels:
        pa = sum(1 for x in a if x == la) / n
        pb = sum(1 for y in b if y == la) / n
        pe += pa * pb
    return None if pe == 1 else round((po - pe) / (1 - pe), 3)


def main():
    runs = {name: load_run(sub) for name, sub in RUN_TREES.items()}
    per_run = {name: metrics(v) for name, v in runs.items()}

    # 逐 case 三 run verdict（仅 A∪B∪C）
    dids = sorted({did for v in runs.values() for did in v}
                  | {'%s_%s' % (e_vendor, n) for (e_vendor, n), e in CASES.items() if e['group'] in 'ABC'})
    case_table = []
    for did in dids:
        vendor, num = did.rsplit('_', 1)
        e = CASES.get((vendor, int(num)))
        if not e or e['group'] not in ('A', 'B', 'C'):
            continue
        row = {'did': did, 'group': e['group'], 'gt': e['gt_label']}
        for name in RUN_TREES:
            row[name] = (runs[name].get(did) or {}).get('verdict')
        case_table.append(row)

    # 一致性：run2 vs run3（两个 clean pass）；以及各对 vs run1
    common23 = [r for r in case_table if r['run2'] and r['run3']]
    a23 = [r['run2'] for r in common23]
    b23 = [r['run3'] for r in common23]
    agree23 = sum(1 for x, y in zip(a23, b23) if x == y)
    disagree23 = [r['did'] for r in common23 if r['run2'] != r['run3']]

    def pair_agree(colx, coly):
        c = [r for r in case_table if r.get(colx) and r.get(coly)]
        ax = [r[colx] for r in c]
        ay = [r[coly] for r in c]
        ag = sum(1 for x, y in zip(ax, ay) if x == y)
        return ag, len(c), cohen_kappa(ax, ay)

    res = {
        'per_run_metrics': per_run,
        'run2_vs_run3': {
            'agree': agree23, 'n': len(common23),
            'agreement_rate': round(agree23 / len(common23), 3) if common23 else None,
            'kappa': cohen_kappa(a23, b23),
            'disagree_cases': disagree23,
        },
        'pairwise': {
            'run1_vs_run2': pair_agree('run1', 'run2'),
            'run1_vs_run3': pair_agree('run1', 'run3'),
            'run2_vs_run3': pair_agree('run2', 'run3'),
        },
        'case_table': case_table,
    }
    out = os.path.join(ROOT, 'VARIANCE_RESULTS.json')
    json.dump(res, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    print('=== per-run metrics ===')
    for name, m in per_run.items():
        print('  %s: %s' % (name, m))
    print('\n=== run2 vs run3 (两个 clean pass) ===')
    p = res['run2_vs_run3']
    ar = p['agreement_rate']
    print('  agree %d/%d = %s | κ=%s' % (p['agree'], p['n'], ('%.3f' % ar) if ar is not None else 'N/A', p['kappa']))
    print('  disagree(%d): %s' % (len(p['disagree_cases']), p['disagree_cases']))
    print('\n=== pairwise (agree, n, κ) ===')
    for k, (ag, n, kx) in res['pairwise'].items():
        print('  %s: %d/%d κ=%s' % (k, ag, n, kx))
    print('\n→ VARIANCE_RESULTS.json')


if __name__ == '__main__':
    main()

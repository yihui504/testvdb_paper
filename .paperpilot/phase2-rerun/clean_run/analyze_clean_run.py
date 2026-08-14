#!/usr/bin/env python3
"""clean_run 分析：判词 vs GT（A/B recall、C 组 fp_suppression、precision）+ 与 run1/2/3 逐 case κ。

判词源: tvdb_sessions/sessions/{vendor}/{version}/{did}/debate_logs/dev_review.json（本轮写入）
输出: clean_run/CLEAN_RUN_RESULTS.json
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V2 = r'C:/Users/11428/Desktop/tvdb_sessions'
MAP = json.load(open(os.path.join(ROOT, 'defect_id_map.json'), encoding='utf-8'))
CASES = {(x['vendor'], x['num']): x for x in json.load(open(os.path.join(ROOT, 'cases_index.json'), encoding='utf-8'))}


def load_clean():
    out = {}
    for did, r in MAP.items():
        vj = os.path.join(V2, 'sessions', r['vendor'], r['version'], did, 'debate_logs', 'dev_review.json')
        if not os.path.isfile(vj):
            continue
        try:
            d = json.load(open(vj, encoding='utf-8'))
            out[did] = {'verdict': d['verdicts'][0].get('verdict'), 'conf': d['verdicts'][0].get('confidence')}
        except Exception as e:  # noqa: BLE001
            out[did] = {'verdict': None, 'err': str(e)}
    return out


def load_tree(sub):
    base = os.path.join(ROOT, sub, 'results')
    out = {}
    if not os.path.isdir(base):
        return out
    for v in os.listdir(base):
        for ver in os.listdir(os.path.join(base, v)):
            nd = os.path.join(base, v, ver)
            if not os.path.isdir(nd):
                continue
            for num in os.listdir(nd):
                dr = os.path.join(nd, num, 'debate_logs', 'dev_review.json')
                if os.path.isfile(dr):
                    try:
                        out['%s_%s' % (v, num)] = json.load(open(dr, encoding='utf-8'))['verdicts'][0].get('verdict')
                    except Exception:  # noqa: BLE001
                        pass
    return out


def metrics(rows):
    AB = [r for r in rows if r[2] in ('A', 'B')]
    C = [r for r in rows if r[2] == 'C']
    tp = sum(1 for _, vd, _ in AB if vd == 'CONFIRMED')
    fn = len(AB) - tp
    fp = sum(1 for _, vd, _ in C if vd == 'CONFIRMED')
    tn = len(C) - fp
    return {'n': len(rows), 'TP': tp, 'FN': fn, 'FP': fp, 'TN': tn,
            'recall': round(tp / len(AB), 3) if AB else None,
            'precision': round(tp / (tp + fp), 3) if (tp + fp) else None,
            'fp_suppression': round(tn / len(C), 3) if C else None}


def kappa(a, b):
    n = len(a)
    if not n:
        return None
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    pe = sum((a.count(l) / n) * (b.count(l) / n) for l in ('CONFIRMED', 'FALSE_POSITIVE'))
    return None if pe == 1 else round((po - pe) / (1 - pe), 3)


def main():
    clean = load_clean()
    rows = []
    for did, v in clean.items():
        r = MAP[did]
        e = CASES.get((r['vendor'], int(r['orig'].split('_')[1])))
        if e and e['group'] in ('A', 'B', 'C'):
            rows.append((did, v['verdict'], e['group']))
    res = {'clean_metrics': metrics(rows), 'n_judged': len(clean)}
    hist = {'run1': load_tree('run'), 'run2': load_tree('run2'), 'run3': load_tree('run3')}
    for name, hv in hist.items():
        # 历史 did = orig issue 号（milvus_47635），clean did = 匿名（milvus_001）→ 反查对齐
        pair = [(did, clean[did]['verdict'], hv.get(MAP[did]['orig']))
                for did in clean if clean[did]['verdict'] and hv.get(MAP[did]['orig'])]
        res['kappa_vs_%s' % name] = {
            'n': len(pair),
            'agreement': round(sum(1 for _, a, b in pair if a == b) / len(pair), 3) if pair else None,
            'kappa': kappa([a for _, a, _ in pair], [b for _, _, b in pair]),
            'flip_cases': [d for d, a, b in pair if a != b],
        }
    # 逐 case 表（含 GT 与历史四轮 verdict）
    table = []
    for did in sorted(MAP):
        r = MAP[did]
        e = CASES.get((r['vendor'], int(r['orig'].split('_')[1])))
        if not e or e['group'] not in ('A', 'B', 'C'):
            continue
        table.append({'did': did, 'group': e['group'], 'gt': e['gt_label'],
                      'clean': (clean.get(did) or {}).get('verdict'),
                      **{n: hv.get(r['orig']) for n, hv in hist.items()}})
    res['case_table'] = table
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'CLEAN_RUN_RESULTS.json')
    json.dump(res, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in res.items() if k != 'case_table'}, ensure_ascii=False, indent=1))
    print('-> %s' % out)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Phase 2 rerun — 汇总 71 dev_review.json vs GT，算 metrics，列 flips/错配/噪声/弱判。"""
import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
CASES = {(x['vendor'], x['num']): x for x in json.load(open(os.path.join(ROOT, 'cases_index.json'), encoding='utf-8'))}
RUN = os.path.join(ROOT, 'run')


def load_all():
    rows = []
    for v in ('milvus', 'qdrant', 'weaviate'):
        base = os.path.join(RUN, 'results', v)
        if not os.path.isdir(base):
            continue
        for ver in os.listdir(base):
            nd = os.path.join(base, ver)
            if not os.path.isdir(nd):
                continue
            for num in os.listdir(nd):
                dr = os.path.join(nd, num, 'debate_logs', 'dev_review.json')
                if not os.path.isfile(dr):
                    continue
                try:
                    d = json.load(open(dr, encoding='utf-8'))
                    vd = d['verdicts'][0]
                    sg = vd.get('steps', {}).get('source_grounding', {}) or vd.get('source_grounding', {})
                    rows.append({
                        'did': vd.get('defect_id') or '%s_%s' % (v, num),
                        'vendor': v, 'num': int(num),
                        'verdict': vd.get('verdict'),
                        'conf': vd.get('confidence'),
                        'root': vd.get('root_cause_if_fp') or vd.get('root_cause'),
                        'rationale': (vd.get('rationale') or '')[:200],
                        'files': sg.get('files_examined') or [],
                        'excerpt': bool(sg.get('source_excerpt')),
                    })
                except Exception as e:
                    rows.append({'did': '%s_%s' % (v, num), 'vendor': v, 'num': int(num), 'err': str(e)})
    return rows


def main():
    rows = load_all()
    # join GT
    for r in rows:
        e = CASES.get((r['vendor'], r['num']))
        r['gt'] = e['gt_label'] if e else None
        r['group'] = e['group'] if e else None
    n = len(rows)
    done = [r for r in rows if r.get('verdict')]
    print('=== dev_review 收集 ===')
    print('total rows:', n, '| with verdict:', len(done))

    # metrics: recall = TP_found / (A∪B); precision = TP / (TP+FP); FP-suppression = C correctly FP
    AB = [r for r in done if r['group'] in ('A', 'B')]  # GT CONFIRMED (45)
    C = [r for r in done if r['group'] == 'C']           # GT FALSE_POSITIVE (26)
    tp = sum(1 for r in AB if r['verdict'] == 'CONFIRMED')        # 真bug 召回
    fn = sum(1 for r in AB if r['verdict'] == 'FALSE_POSITIVE')    # 漏判
    fp = sum(1 for r in C if r['verdict'] == 'CONFIRMED')          # 误报
    tn = sum(1 for r in C if r['verdict'] == 'FALSE_POSITIVE')     # 正确识破 FP
    recall = tp / len(AB) if AB else 0
    precision = tp / (tp + fp) if (tp + fp) else 0
    fp_supp = tn / len(C) if C else 0
    print('\n=== GLM-5.2 dev-reviewer vs GT (n=%d, A∪B=%d, C=%d) ===' % (len(done), len(AB), len(C)))
    print('TP=%d FN=%d | FP=%d TN=%d' % (tp, fn, fp, tn))
    print('recall=%.3f  precision=%.3f  FP-suppression=%.3f' % (recall, precision, fp_supp))
    print('对比: 旧精简 oracle 0.933/0.792/0.577 | cleaned 0.911/0.872/0.769')

    flips = [r for r in done if r['gt'] and r['verdict'] != r['gt']]
    print('\n=== flips (dev != GT): %d ===' % len(flips))
    for r in flips:
        print('  %-16s dev=%-13s GT=%s | %s' % (r['did'], r['verdict'], r['gt'], r['root']))

    # 数据质量问题
    mismatch = [r for r in done if re.search(r'mismatch|mapping_error|infrastructure|no raw|missing_raw|未提取|零流量|ZERO', r['rationale'] + ' ' + (r['root'] or ''), re.I)]
    envnoise = [r for r in done if re.search(r'env_noise|timeout|408|resource', r['root'] or '', re.I)]
    weak = [r for r in done if (r.get('conf') or 1) < 0.9 or not r['excerpt']]
    print('\n=== 数据质量待复核 ===')
    print('endpoint/metadata 错配:', [r['did'] for r in mismatch])
    print('env_noise(超时/资源):', [r['did'] for r in envnoise])
    print('弱判(conf<0.9 或无源码excerpt):', [r['did'] for r in weak])

    json.dump(rows, open(os.path.join(ROOT, 'analysis_rows.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('\n→ analysis_rows.json 写入')


if __name__ == '__main__':
    main()

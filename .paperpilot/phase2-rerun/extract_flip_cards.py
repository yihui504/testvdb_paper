#!/usr/bin/env python3
"""抽 21 flips 的复核卡，供逐个定性审查。"""
import json, os, re
ROOT = os.path.dirname(os.path.abspath(__file__))
CI = {(x['vendor'], x['num']): x for x in json.load(open(os.path.join(ROOT, 'cases_index.json'), encoding='utf-8'))}
FLIPS = json.load(open(os.path.join(ROOT, 'FINAL_RESULTS.json'), encoding='utf-8'))['flips']


def load(did):
    v, num = did.split('_')
    e = CI[(v, int(num))]
    sess = os.path.join(ROOT, 'run', 'results', v, e['version'], num)
    d = json.load(open(os.path.join(sess, 'debate_logs', 'dev_review.json'), encoding='utf-8'))
    return d['verdicts'][0], e, sess


def card(did):
    vd, e, sess = load(did)
    pa = vd.get('perspective_analysis', {}) or {}
    sg = vd.get('steps', {}).get('source_grounding', {}) or vd.get('source_grounding', {})
    cr = vd.get('steps', {}).get('clean_repro', {}) or {}
    A = (pa.get('contract', {}) or {}).get('verdict_A', '?')
    B = (pa.get('physical', {}) or {}).get('verdict_B', '?')
    C = (pa.get('behavioral', {}) or {}).get('verdict_C', '?')
    agg = pa.get('aggregation') or pa.get('aggregation_applied') or ''
    print('=' * 80)
    print('%s  | dev=%s conf=%s | GT=%s/%s | %s' % (did, vd['verdict'], vd.get('confidence'), e['group'], e['gt_label'], e.get('defect_type') or '?'))
    print('  三视角 A=%s B=%s C=%s | agg: %s' % (A, B, C, (agg[:90] if agg else '?')))
    print('  root_cause: %s' % (vd.get('root_cause_if_fp') or vd.get('root_cause') or '?'))
    print('  clean_repro.pass: %s | observed: %s' % (cr.get('pass'), (cr.get('observed') or '')[:100]))
    fe = sg.get('files_examined') or []
    print('  files(%d): %s' % (len(fe), ', '.join(fe[:4])))
    exc = (sg.get('source_excerpt') or '')[:280].replace('\n', ' ')
    print('  excerpt: %s' % exc)
    print('  rationale: %s' % (vd.get('rationale') or '')[:300].replace('\n', ' '))


for did in FLIPS:
    try:
        card(did)
    except Exception as ex:
        print(did, 'ERR', ex)

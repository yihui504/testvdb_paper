#!/usr/bin/env python3
"""clean_run 判词校验（纪律 §7.2）：JSON 合法 + judge + verdict 二值 + source_excerpt 非空 + files_examined 非空 + .done。

用法: python check_verdicts.py [did ...]   # 无参 = 校验全部已有判词
"""
import json
import os
import sys

V2 = r'C:/Users/11428/Desktop/tvdb_sessions'
MAP = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'defect_id_map.json'), encoding='utf-8'))


def check(did):
    r = MAP[did]
    sess = os.path.join(V2, 'sessions', r['vendor'], r['version'], did)
    vj = os.path.join(sess, 'debate_logs', 'dev_review.json')
    errs = []
    if not os.path.isfile(vj):
        return did, ['missing dev_review.json']
    if not os.path.isfile(vj + '.done'):
        errs.append('missing .done')
    try:
        d = json.load(open(vj, encoding='utf-8'))
    except Exception as e:  # noqa: BLE001
        return did, ['invalid JSON: %s' % str(e)[:80]]
    if d.get('judge') != 'dev-review':
        errs.append('judge != dev-review')
    vs = d.get('verdicts') or []
    if not vs:
        return did, errs + ['verdicts empty']
    v = vs[0]
    if v.get('defect_id') != did:
        errs.append('defect_id mismatch: %s' % v.get('defect_id'))
    if v.get('verdict') not in ('CONFIRMED', 'FALSE_POSITIVE'):
        errs.append('verdict not binary: %r' % v.get('verdict'))
    sg = v.get('steps', {}).get('source_grounding', {}) or {}
    if len((sg.get('source_excerpt') or '').strip()) < 50:
        errs.append('source_excerpt missing/too short')
    if not sg.get('files_examined'):
        errs.append('files_examined empty')
    return did, errs


def main():
    dids = sys.argv[1:] or list(MAP)
    n_ok = n_bad = n_miss = 0
    for did in dids:
        _, errs = check(did)
        if not errs:
            n_ok += 1
        elif errs == ['missing dev_review.json']:
            n_miss += 1
        else:
            n_bad += 1
            print('FAIL %s: %s' % (did, '; '.join(errs)))
    print('PASS %d | FAIL %d | PENDING %d' % (n_ok, n_bad, n_miss))


if __name__ == '__main__':
    main()

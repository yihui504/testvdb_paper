# -*- coding: utf-8 -*-
"""清理作废链对应的 defect 报告（defects/ 中 defect_id 不在有效 chain_verdicts DEFECT 集的移 voided/defects/）"""
import json, os, re, shutil, sys
sys.stdout.reconfigure(encoding='utf-8')
CACHE = r'C:/Users/11428/.claude/plugins/cache/testvdb/testvdb/2.3.0/results/milvus'

for ver, sess in [('v2.3.22', '2026-08-21T18-44-26Z'), ('v2.6.10', '2026-08-21T20-31-04Z'),
                  ('v2.6.12', '2026-08-21T22-15-23Z'), ('v2.6.16', '2026-08-21T23-37-54Z')]:
    cvp = os.path.join(CACHE, ver, sess, 'debate_logs', 'chain_verdicts.json')
    ddir = os.path.join(CACHE, ver, sess, 'defects')
    if not os.path.exists(cvp) or not os.path.isdir(ddir):
        print(ver, 'skip'); continue
    cv = json.load(open(cvp, encoding='utf-8'))
    valid = {v['defect_id'] for v in cv['verdicts'] if v['verdict'] == 'DEFECT'}
    vd = os.path.join(CACHE, ver, 'voided', 'defects')
    os.makedirs(vd, exist_ok=True)
    removed = 0
    for fn in os.listdir(ddir):
        if not fn.endswith('.md'): continue
        content = open(os.path.join(ddir, fn), encoding='utf-8', errors='replace').read()
        m = re.search(r'defect_id["\s:]*`?([A-Za-z0-9_.\-]+)`?', content)
        did = m.group(1) if m else None
        if did and did not in valid:
            shutil.move(os.path.join(ddir, fn), os.path.join(vd, fn)); removed += 1
    print(ver, 'kept', len(os.listdir(ddir)), 'removed', removed)

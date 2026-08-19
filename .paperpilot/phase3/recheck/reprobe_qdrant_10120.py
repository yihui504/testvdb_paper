"""probe for qdrant/qdrant#10120  count exact=false on is_empty under-counts ~35% at steady state
version: 1.18.3 | gt: TP_FIXED_PR | class: semantics
"""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready

import os as _os; BASE = _os.environ.get("QDRANT_BASE", "http://localhost:6333")
COL = 'c'
N = 200  # is_empty matches the ~20% missing-kw points (i%5==0 -> no kw)

def count(exact, kind):
    return http('POST', BASE + '/collections/' + COL + '/points/count',
                {"exact": exact, "filter": {"must": [{kind: {"key": "kw"}}]}})

def main():
    if not wait_ready(BASE + '/'):
        emit('setup', observation='server not ready')
        return
    http('DELETE', BASE + '/collections/' + COL)
    http('PUT', BASE + '/collections/' + COL,
         {"vectors": {"size": 2, "distance": "Cosine"}, "optimizer_config": {"indexing_threshold": 1}})
    pts = []
    for i in range(N):
        p = {"id": i + 1, "vector": [1.0, 0.0]}
        if i % 5 != 0:
            p["payload"] = {"kw": "red"}
        pts.append(p)
    http('PUT', BASE + '/collections/' + COL + '/points?wait=true', {"points": pts})
    http('PUT', BASE + '/collections/' + COL + '/index',
         {"field_name": "kw", "field_schema": "keyword"})
    time.sleep(3)  # 稳态, 避开 indexing 窗口

    # c1 ground truth exact=true on is_empty
    s, b, _ = count(True, 'is_empty')
    exact = (b or {}).get('result', {}).get('count')
    emit('c1', http_status=s, observation=('count exact=true is_empty -> %s (ground truth)' % exact))

    # c2 the defect
    s, b, _ = count(False, 'is_empty')
    approx = (b or {}).get('result', {}).get('count')
    pct = (approx - exact) / float(exact) * 100 if exact else 0
    emit('c2', http_status=s, observation=(
        'count exact=false is_empty -> %s vs exact=%s (%+.0f%%%s)' % (
          approx, exact, pct, ' undercount, BUG' if approx < exact * 0.9 else '')))

    # c3 control is_null (expect correct 0 on both)
    s, b, _ = count(False, 'is_null')
    isn = (b or {}).get('result', {}).get('count')
    emit('c3', http_status=s, observation=('count exact=false is_null -> %s (control, expect 0)' % isn))
    print('probe_qdrant_10120 done')

if __name__ == '__main__':
    main()

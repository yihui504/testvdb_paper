"""probe for qdrant/qdrant#10127  count exact=false on match_any under-counts (independent-OR)
version: 1.18.3 | gt: PENDING_SELF_LABELED | class: semantics
"""
import os, sys, time, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready

BASE = 'http://localhost:6333'
COL = 'c'
N = 500
KWS = ['red', 'blue', 'green', 'yellow', 'purple']

def count(exact, vals):
    return http('POST', BASE + '/collections/' + COL + '/points/count',
                {"exact": exact, "filter": {"must": [{"key": "kw", "match": {"any": vals}}]}})

def main():
    if not wait_ready(BASE + '/'):
        emit('setup', observation='server not ready')
        return
    http('DELETE', BASE + '/collections/' + COL)
    http('PUT', BASE + '/collections/' + COL,
         {"vectors": {"size": 2, "distance": "Cosine"}, "optimizer_config": {"indexing_threshold": 1}})
    r = random.Random(42)
    pts = [{"id": i + 1, "vector": [1.0, 0.0], "payload": {"kw": r.choice(KWS)}} for i in range(N)]
    http('PUT', BASE + '/collections/' + COL + '/points?wait=true', {"points": pts})
    http('PUT', BASE + '/collections/' + COL + '/index', {"field_name": "kw", "field_schema": "keyword"})
    time.sleep(3)

    # c1 control single value [red]
    s, b, _ = count(False, ["red"])
    c1 = (b or {}).get('result', {}).get('count')
    emit('c1', http_status=s, observation=('match_any [red] exact=false -> %s (single value, should be exact)' % c1))

    # c2 two values
    s, b, _ = count(False, ["red", "blue"])
    c2 = (b or {}).get('result', {}).get('count')
    emit('c2', http_status=s, observation=('match_any [red,blue] exact=false -> %s (undercount grows?)' % c2))

    # c3 all five values (covers entire field, should equal total=N)
    s, b, _ = count(False, KWS)
    c3 = (b or {}).get('result', {}).get('count')
    emit('c3', http_status=s, observation=(
        'match_any all 5 values exact=false -> %s vs total=%d (undercount=%d, BUG: should equal total)' % (
          c3, N, N - c3)))
    print('probe_qdrant_10127 done')

if __name__ == '__main__':
    main()

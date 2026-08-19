"""probe for qdrant/qdrant#10124  count exact=false on numeric range -> bidirectional histogram error
version: 1.18.3 | gt: PENDING_SELF_LABELED | class: semantics
"""
import os, sys, time, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready

BASE = 'http://localhost:6333'
COL = 'c'
N = 500

def count(exact, rng):
    return http('POST', BASE + '/collections/' + COL + '/points/count',
                {"exact": exact, "filter": {"must": [{"key": "n", "range": rng}]}})

def main():
    if not wait_ready(BASE + '/'):
        emit('setup', observation='server not ready')
        return
    http('DELETE', BASE + '/collections/' + COL)
    http('PUT', BASE + '/collections/' + COL,
         {"vectors": {"size": 2, "distance": "Cosine"}, "optimizer_config": {"indexing_threshold": 1}})
    r = random.Random(42)
    pts = [{"id": i + 1, "vector": [1.0, 0.0], "payload": {"n": r.randint(0, 1000)}} for i in range(N)]
    http('PUT', BASE + '/collections/' + COL + '/points?wait=true', {"points": pts})
    http('PUT', BASE + '/collections/' + COL + '/index', {"field_name": "n", "field_schema": "integer"})
    time.sleep(3)

    # c1 ground truth exact=true
    s, b, _ = count(True, {"gte": 100, "lte": 200})
    g = (b or {}).get('result', {}).get('count')
    emit('c1', http_status=s, observation=('count exact=true range 100..200 -> %s (ground truth)' % g))

    # c2 the defect: exact=false same range
    s, b, _ = count(False, {"gte": 100, "lte": 200})
    a = (b or {}).get('result', {}).get('count')
    emit('c2', http_status=s, observation=(
        'count exact=false range 100..200 -> %s vs exact=%s (%+.1f%%)' % (
          a, g, (a - g) / float(g) * 100 if g else 0)))

    # c3 exact=false range gte:500
    s, b, _ = count(False, {"gte": 500})
    c3 = (b or {}).get('result', {}).get('count')
    emit('c3', http_status=s, observation=('count exact=false gte:500 -> %s (observe over/undercount)' % c3))

    # c4 exact=false range lte:300
    s, b, _ = count(False, {"lte": 300})
    c4 = (b or {}).get('result', {}).get('count')
    emit('c4', http_status=s, observation=('count exact=false lte:300 -> %s (bidirectional?)' % c4))
    print('probe_qdrant_10124 done')

if __name__ == '__main__':
    main()

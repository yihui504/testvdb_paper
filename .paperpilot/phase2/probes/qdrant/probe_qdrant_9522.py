"""probe for qdrant/qdrant#9522  Query API returns 200 when lookup_from references non-existent collection
version: 1.18.2 | gt: TP_FIXED_PR | class: behavior
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready

BASE = 'http://localhost:6333'
SRC = 'test_lookup_source'
DST = 'test_lookup_target'

def mkcol(name):
    http('DELETE', BASE + '/collections/' + name)
    http('PUT', BASE + '/collections/' + name, {"vectors": {"size": 4, "distance": "Cosine"}})

def main():
    if not wait_ready(BASE + '/'):
        emit('setup', observation='server not ready')
        return
    mkcol(SRC)
    http('PUT', BASE + '/collections/' + SRC + '/points?wait=true',
         {"points": [{"id": i, "vector": [0.1, 0.2, 0.3, 0.4], "payload": {"tag": "t%d" % i}} for i in range(5)]})
    mkcol(DST)
    http('PUT', BASE + '/collections/' + DST + '/points?wait=true',
         {"points": [{"id": i, "vector": [0.1, 0.2, 0.3, 0.4]} for i in range(5)]})

    # c1: lookup_from -> non-existent collection
    s, b, t = http('POST', BASE + '/collections/' + SRC + '/points/query',
                   {"query": [0.3, 0.3, 0.3, 0.3], "limit": 3,
                    "lookup_from": {"collection": "nonexistent_collection_xyz", "vector": "default"}})
    n = len((b or {}).get('result', {}).get('points', [])) if b else None
    emit('c1', http_status=s, observation=(
        'lookup non-existent coll -> status=%s, %d results%s' % (
          s, n, ' (silent 200, invalid lookup ignored, BUG)' if s == 200 else ' (404/400, FIX)')))

    # c2: control valid lookup
    s, b, t = http('POST', BASE + '/collections/' + SRC + '/points/query',
                   {"query": [0.3, 0.3, 0.3, 0.3], "limit": 3,
                    "lookup_from": {"collection": DST, "vector": "default"}})
    emit('c2', http_status=s, observation=('lookup valid coll -> status=%s (control OK)' % s))
    print('probe_qdrant_9522 done')

if __name__ == '__main__':
    main()

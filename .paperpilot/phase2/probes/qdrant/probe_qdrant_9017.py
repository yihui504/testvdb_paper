"""probe for qdrant/qdrant#9017  hnsw_ef accepts 0
version: 1.18.0 | gt: TP_FIXED_PR | class: param_validation
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready

BASE = 'http://localhost:6333'
COL = 'test_hnsw_bug'

def main():
    if not wait_ready(BASE + '/'):
        emit('setup', observation='server not ready')
        return
    http('DELETE', BASE + '/collections/' + COL)
    http('PUT', BASE + '/collections/' + COL, {"vectors": {"size": 4, "distance": "Cosine"}})
    http('PUT', BASE + '/collections/' + COL + '/points', {"points": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4]}]})

    s, b, t = http('POST', BASE + '/collections/' + COL + '/points/search',
                   {"vector": [0.1, 0.2, 0.3, 0.4], "limit": 3, "params": {"hnsw_ef": 0}})
    n = len(b.get('result', [])) if b else None
    emit('c1', http_status=s, resp_code=(b or {}).get('status.code'), observation=(
        'hnsw_ef=0 search -> status=%s, %d results%s' % (s, n,
          ' (accepted, BUG)' if s == 200 else ' (rejected, FIX)')))
    print('probe_qdrant_9017 done')

if __name__ == '__main__':
    main()

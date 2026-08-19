"""probe for qdrant/qdrant#9420  query=null silently accepted -> returns all points
version: 1.18.2 | gt: FP_BY_DESIGN | class: param_validation
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready

BASE = 'http://localhost:6333'
COL = 'test_qnull'

def main():
    if not wait_ready(BASE + '/'):
        emit('setup', observation='server not ready')
        return
    http('DELETE', BASE + '/collections/' + COL)
    http('PUT', BASE + '/collections/' + COL, {"vectors": {"size": 4, "distance": "Cosine"}})
    http('PUT', BASE + '/collections/' + COL + '/points',
         {"points": [{"id": 10, "vector": [0.5, 0.5, 0.5, 0.5]},
                     {"id": 1, "vector": [0.1, 0.2, 0.3, 0.4]},
                     {"id": 5, "vector": [0.3, 0.3, 0.3, 0.3]}]})

    s, b, t = http('POST', BASE + '/collections/' + COL + '/points/query',
                   {"query": None, "limit": 5})
    res = (b or {}).get('result', {}).get('points', [])
    ids = [p.get('id') for p in res]
    emit('c1', http_status=s, observation=(
        'query=null -> status=%s, ids=%s%s' % (
          s, ids, ' (null accepted, returns all by ID, BUG)' if s == 200 and len(res) == 3 else ' (rejected/excluded, OK)')))
    print('probe_qdrant_9420 done')

if __name__ == '__main__':
    main()

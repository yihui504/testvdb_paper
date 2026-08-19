"""probe for qdrant/qdrant#9418  filter.should=null silently accepted and ignored
version: 1.18.2 | gt: FP_BY_DESIGN | class: param_validation
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready

BASE = 'http://localhost:6333'
COL = 'test_filter_null'

def main():
    if not wait_ready(BASE + '/'):
        emit('setup', observation='server not ready')
        return
    http('DELETE', BASE + '/collections/' + COL)
    http('PUT', BASE + '/collections/' + COL, {"vectors": {"size": 4, "distance": "Cosine"}})
    http('PUT', BASE + '/collections/' + COL + '/points',
         {"points": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4], "payload": {"tag": "A"}},
                     {"id": 2, "vector": [0.1, 0.2, 0.3, 0.4], "payload": {"tag": "B"}}]})

    s, b, t = http('POST', BASE + '/collections/' + COL + '/points/query',
                   {"query": [0.1, 0.2, 0.3, 0.4], "limit": 5, "filter": {"should": None}})
    res = (b or {}).get('result', {}).get('points', [])
    emit('c1', http_status=s, observation=(
        'filter.should=null query -> status=%s, %d points%s' % (
          s, len(res), ' (null ignored, no filtering, BUG)' if s == 200 and len(res) == 2 else ' (ok)')))
    print('probe_qdrant_9418 done')

if __name__ == '__main__':
    main()

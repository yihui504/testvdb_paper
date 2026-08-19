"""probe for qdrant/qdrant#9419  filter.must_not accepts object instead of array — silently ignored
version: 1.18.2 | gt: FP_BY_DESIGN | class: param_validation
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready

BASE = 'http://localhost:6333'
COL = 'test_mustnot'

def main():
    if not wait_ready(BASE + '/'):
        emit('setup', observation='server not ready')
        return
    http('DELETE', BASE + '/collections/' + COL)
    http('PUT', BASE + '/collections/' + COL, {"vectors": {"size": 4, "distance": "Cosine"}})
    http('PUT', BASE + '/collections/' + COL + '/points',
         {"points": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4], "payload": {"tag": "x"}},
                     {"id": 2, "vector": [0.1, 0.2, 0.3, 0.4], "payload": {"tag": "y"}}]})

    s, b, t = http('POST', BASE + '/collections/' + COL + '/points/query',
                   {"query": [0.1, 0.2, 0.3, 0.4], "limit": 5,
                    "filter": {"must_not": {"key": "tag", "match": {"value": "x"}}}})
    res = (b or {}).get('result', {}).get('points', [])
    emit('c1', http_status=s, observation=(
        'must_not as object -> status=%s, %d points returned%s' % (
          s, len(res), ' (object silently ignored, exclusion not applied, BUG)' if s == 200 and len(res) == 2 else ' (excluded, expect 1)')))
    print('probe_qdrant_9419 done')

if __name__ == '__main__':
    main()

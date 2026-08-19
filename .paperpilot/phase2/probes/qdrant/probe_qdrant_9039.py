"""probe for qdrant/qdrant#9039  Async upsert silently discards dimension-mismatched vectors
version: 1.18.0 | gt: TP_FIXED_PR | class: type_coercion
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready

BASE = 'http://localhost:6333'
COL = 'test'

def count():
    _, b, _ = http('GET', BASE + '/collections/' + COL)
    return (b or {}).get('result', {}).get('points_count')

def main():
    if not wait_ready(BASE + '/'):
        emit('setup', observation='server not ready')
        return
    http('DELETE', BASE + '/collections/' + COL)
    http('PUT', BASE + '/collections/' + COL, {"vectors": {"size": 4, "distance": "Cosine"}})

    # c1: async (wait omitted) 3-dim into 4-dim collection
    s, b, t = http('PUT', BASE + '/collections/' + COL + '/points',
                   {"points": [{"id": 2, "vector": [0.1, 0.2, 0.3]}]})
    emit('c1', http_status=s, resp_code=(b or {}).get('status.code'), observation=(
        'async 3-dim upsert -> status=%s body=%s count_after=%s' % (s, t, count())))

    # c2: sync (wait=true) comparison
    s, b, t = http('PUT', BASE + '/collections/' + COL + '/points?wait=true',
                   {"points": [{"id": 1, "vector": [0.1, 0.2, 0.3]}]})
    emit('c2', http_status=s, resp_code=(b or {}).get('status.code'), observation=(
        'sync(wait=true) 3-dim upsert -> status=%s body=%r' % (s, t)))
    print('probe_qdrant_9039 done')

if __name__ == '__main__':
    main()

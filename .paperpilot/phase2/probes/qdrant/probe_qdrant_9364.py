"""probe for qdrant/qdrant#9364  Batch operations partially apply despite HTTP 400 (atomicity)
version: 1.18.2 | gt: SELF_CLOSED | class: behavior
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready

BASE = 'http://localhost:6333'
COL = 'test_batch'

def count():
    _, b, _ = http('POST', BASE + '/collections/' + COL + '/points/count', {"exact": True})
    return (b or {}).get('result', {}).get('count')

def main():
    if not wait_ready(BASE + '/'):
        emit('setup', observation='server not ready')
        return
    http('DELETE', BASE + '/collections/' + COL)
    http('PUT', BASE + '/collections/' + COL, {"vectors": {"size": 4, "distance": "Cosine"}})
    http('PUT', BASE + '/collections/' + COL + '/points?wait=true',
         {"points": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4]},
                     {"id": 2, "vector": [0.5, 0.6, 0.7, 0.8]},
                     {"id": 3, "vector": [0.9, 0.9, 0.9, 0.9]}]})
    base = count()

    s, b, t = http('POST', BASE + '/collections/' + COL + '/points/batch',
                   {"operations": [{"upsert": {"points": [
                       {"id": 4, "vector": [0.1, 0.2, 0.3, 0.4]},
                       {"id": 5, "vector": [0.5, 0.6, 0.7, 0.8]},
                       {"id": 6, "vector": [0.1, 0.2, 0.3]}]}}]})
    after = count()
    emit('c1', http_status=s, observation=(
        'mixed batch(2 valid+1 invalid) -> status=%s, count %s->%s%s' % (
          s, base, after, ' (atomic, OK)' if s != 200 and after == base else ' (partial-apply, BUG)')))
    print('probe_qdrant_9364 done')

if __name__ == '__main__':
    main()

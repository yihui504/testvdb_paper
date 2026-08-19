"""probe for qdrant/qdrant#9521  Named vector upsert in single-vector collection returns 200 but discarded
version: 1.18.2 | gt: PENDING_SELF_LABELED | class: type_coercion
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready

BASE = 'http://localhost:6333'
COL = 'test_named_vec'

def count():
    _, b, _ = http('POST', BASE + '/collections/' + COL + '/points/count', {"exact": True})
    return (b or {}).get('result', {}).get('count')

def main():
    if not wait_ready(BASE + '/'):
        emit('setup', observation='server not ready')
        return
    http('DELETE', BASE + '/collections/' + COL)
    http('PUT', BASE + '/collections/' + COL, {"vectors": {"size": 4, "distance": "Cosine"}})

    # c1: named-vector format into single-vector collection
    s, b, t = http('PUT', BASE + '/collections/' + COL + '/points?wait=true',
                   {"points": [{"id": 102, "vector": {"name": [0.1, 0.2, 0.3, 0.4]}}]})
    c = count()
    emit('c1', http_status=s, resp_code=(b or {}).get('status.code'), observation=(
        'named-vector upsert into single-vec coll -> status=%s, count=%s%s' % (
          s, c, ' (silent data loss, BUG)' if s == 200 and c == 0 else ' (stored/rejected, OK)')))

    # c2: control wrong-dimension
    s, b, t = http('PUT', BASE + '/collections/' + COL + '/points?wait=true',
                   {"points": [{"id": 103, "vector": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]}]})
    emit('c2', http_status=s, observation=('wrong-dim(6) upsert -> status=%s body=%r' % (s, t)))
    print('probe_qdrant_9521 done')

if __name__ == '__main__':
    main()

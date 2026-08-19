"""probe for qdrant/qdrant#9524  Invalid filter conditions silently accepted (200 OK) with poor diagnostics
version: 1.18.2 | gt: OPEN_NO_LABEL | class: param_validation
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready

BASE = 'http://localhost:6333'
COL = 'test_filter_validation'

def search(filt):
    return http('POST', BASE + '/collections/' + COL + '/points/search',
                {"vector": [0.1, 0.1, 0.1, 0.1], "limit": 5, "filter": filt})

def main():
    if not wait_ready(BASE + '/'):
        emit('setup', observation='server not ready')
        return
    http('DELETE', BASE + '/collections/' + COL)
    http('PUT', BASE + '/collections/' + COL, {"vectors": {"size": 4, "distance": "Cosine"}})
    http('PUT', BASE + '/collections/' + COL + '/points',
         {"points": [{"id": 1, "vector": [0.1, 0.1, 0.1, 0.1], "payload": {"category": "A", "score": 10}},
                     {"id": 2, "vector": [0.2, 0.2, 0.2, 0.2], "payload": {"category": "B", "score": 20}}]})

    s, b, t = search({"must": []})
    emit('c1', http_status=s, observation=('empty must [] -> status=%s (accepted 200 = BUG)' % s))

    s, b, t = search({"must": [{"key": "nonexistent_field_xyz", "match": {"value": "A"}}]})
    emit('c2', http_status=s, observation=('non-existent field -> status=%s (accepted 200 = BUG)' % s))

    s, b, t = search({"must": [{"key": "score", "range": {"gt": 50, "lt": 10}}]})
    emit('c3', http_status=s, observation=('contradictory range gt>lt -> status=%s (accepted 200 = BUG)' % s))

    # c4 diagnostics: null key already rejected,观察错误文案质量
    s, b, t = search({"must": [{"key": None, "match": {"value": "A"}}]})
    msg = (t or '')[:160]
    emit('c4', http_status=s, observation=('null key -> status=%s msg=%r%s' % (
        s, msg, ' (poor: serde, no param name)' if s == 400 and 'column' in msg else ' (ok)')))
    print('probe_qdrant_9524 done')

if __name__ == '__main__':
    main()

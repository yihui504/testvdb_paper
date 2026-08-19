"""probe for qdrant/qdrant#9027  score_threshold_range_issue
version: 1.18.0 | gt: BY_DESIGN | class: behavior
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready

BASE = 'http://localhost:6333'
COL = 'test_score_threshold_bug'

def main():
    if not wait_ready(BASE + '/'):
        emit('setup', observation='server not ready')
        return
    http('DELETE', BASE + '/collections/' + COL)
    http('PUT', BASE + '/collections/' + COL, {"vectors": {"size": 4, "distance": "Cosine"}})
    http('PUT', BASE + '/collections/' + COL + '/points', {"points": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4]}]})

    s, b, t = http('POST', BASE + '/collections/' + COL + '/points/search',
                   {"vector": [0.1, 0.2, 0.3, 0.4], "limit": 5, "score_threshold": 2.0})
    n = len(b.get('result', [])) if b else None
    emit('c1', http_status=s, observation=('threshold=2.0 (above Cosine max) -> status=%s, %d results' % (s, n)))

    s, b, t = http('POST', BASE + '/collections/' + COL + '/points/search',
                   {"vector": [0.1, 0.2, 0.3, 0.4], "limit": 5, "score_threshold": -0.5})
    n = len(b.get('result', [])) if b else None
    emit('c2', http_status=s, observation=('threshold=-0.5 (below min score) -> status=%s, %d results' % (s, n)))
    print('probe_qdrant_9027 done')

if __name__ == '__main__':
    main()

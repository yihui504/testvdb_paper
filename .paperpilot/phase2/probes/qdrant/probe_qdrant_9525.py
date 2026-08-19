"""probe for qdrant/qdrant#9525  Serde errors expose Rust internal types, lack parameter names
version: 1.18.2 | gt: PENDING_SELF_LABELED | class: doc_mismatch
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready

BASE = 'http://localhost:6333'
COL = 'test_serde_errors'

def main():
    if not wait_ready(BASE + '/'):
        emit('setup', observation='server not ready')
        return
    http('DELETE', BASE + '/collections/' + COL)
    http('PUT', BASE + '/collections/' + COL, {"vectors": {"size": 4, "distance": "Cosine"}})
    http('PUT', BASE + '/collections/' + COL + '/points',
         {"points": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4], "payload": {"group": "A", "score": 10}}]})

    s, b, t = http('POST', BASE + '/collections/' + COL + '/points/search',
                   {"vector": [0.1, 0.2, 0.3, 0.4], "limit": -1})
    emit('c1', http_status=s, msg=(t or '')[:140], observation=('search limit=-1 -> status=%s msg=%r (leaks usize?)' % (s, (t or '')[:140])))

    s, b, t = http('POST', BASE + '/collections/' + COL + '/points/search',
                   {"vector": [0.1, 0.2, 0.3, 0.4], "limit": 5, "score_threshold": "not_a_number"})
    emit('c2', http_status=s, observation=('search score_threshold="x" -> status=%s msg=%r' % (s, (t or '')[:140])))

    s, b, t = http('POST', BASE + '/collections/' + COL + '/points/recommend',
                   {"positive": [1], "limit": 5, "strategy": 123})
    emit('c3', http_status=s, observation=('recommend strategy=123 -> status=%s msg=%r' % (s, (t or '')[:140])))

    s, b, t = http('POST', BASE + '/collections/' + COL + '/points/scroll', {"limit": -1})
    emit('c4', http_status=s, observation=('scroll limit=-1 -> status=%s msg=%r' % (s, (t or '')[:140])))

    s, b, t = http('POST', BASE + '/collections/' + COL + '/points/query',
                   {"query": {"nearest": [0.1, 0.2, 0.3, 0.4]}, "limit": -1})
    emit('c5', http_status=s, observation=('query limit=-1 -> status=%s msg=%r' % (s, (t or '')[:140])))
    print('probe_qdrant_9525 done')

if __name__ == '__main__':
    main()

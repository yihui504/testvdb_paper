"""probe for qdrant/qdrant#9523  Search offset pagination returns duplicate IDs (HNSW approximation)
version: 1.18.2 | gt: BY_DESIGN | class: behavior
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready

BASE = 'http://localhost:6333'
COL = 'test_pagination_dedup'

def search(offset, limit=10):
    s, b, t = http('POST', BASE + '/collections/' + COL + '/points/search',
                   {"vector": [0.5, 0.5, 0.5, 0.5], "limit": limit, "offset": offset,
                    "with_payload": False})
    return s, [r.get('id') for r in (b or {}).get('result', [])]

def main():
    if not wait_ready(BASE + '/'):
        emit('setup', observation='server not ready')
        return
    http('DELETE', BASE + '/collections/' + COL)
    http('PUT', BASE + '/collections/' + COL, {"vectors": {"size": 4, "distance": "Cosine"}})
    http('PUT', BASE + '/collections/' + COL + '/points?wait=true',
         {"points": [{"id": i, "vector": [0.1 + i * 0.01, 0.1 + i * 0.01, 0.1, 0.1]} for i in range(25)]})

    s1, p1 = search(0)
    emit('c1', http_status=s1, observation=('page1 offset=0 ids=%s' % p1))
    s2, p2 = search(10)
    overlap = sorted(set(p1) & set(p2))
    emit('c2', http_status=s2, observation=('page2 offset=10 ids=%s overlap_with_p1=%s' % (p2, overlap)))
    s3, p3 = search(20)
    union = sorted(set(p1 + p2 + p3))
    emit('c3', http_status=s3, observation=(
        'page3 offset=20 ids=%s unique_union=%d duplicate_sets=%s' % (p3, len(union),
          sorted(set([x for x in p1 + p2 + p3 if (p1 + p2 + p3).count(x) > 1])))))

    # c4 control via scroll
    s, b, t = http('POST', BASE + '/collections/' + COL + '/points/scroll', {"limit": 10})
    sp = [pt.get('id') for pt in (b or {}).get('result', {}).get('points', [])]
    emit('c4', http_status=s, observation=('scroll control ids=%s (non-overlapping cursor)' % sp))
    print('probe_qdrant_9523 done')

if __name__ == '__main__':
    main()

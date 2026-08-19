"""probe for qdrant/qdrant#9366  Named vector lifecycle (update+delete) corrupts search -> 400
version: 1.18.2 | gt: SELF_CLOSED | class: behavior
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready

BASE = 'http://localhost:6333'
COL = 'test_named'

def main():
    if not wait_ready(BASE + '/'):
        emit('setup', observation='server not ready')
        return
    http('DELETE', BASE + '/collections/' + COL)
    http('PUT', BASE + '/collections/' + COL,
         {"vectors": {"image_vector": {"size": 4, "distance": "Cosine"}}})
    pts = []
    for i in range(1, 21):
        pts.append({"id": i, "vector": {"image_vector": [0.1, 0.2, 0.3, 0.4]}})
    http('PUT', BASE + '/collections/' + COL + '/points?wait=true', {"points": pts})

    s, b, t = http('POST', BASE + '/collections/' + COL + '/points/search',
                   {"vector": {"name": "image_vector", "vector": [0.1, 0.2, 0.3, 0.4]}, "limit": 5})
    n = len(b.get('result', [])) if b else None
    emit('c1', http_status=s, observation=('baseline named search -> status=%s, %d results' % (s, n)))

    s, b, t = http('PUT', BASE + '/collections/' + COL + '/points?wait=true',
                   {"points": [{"id": 3, "vector": {"image_vector": [0.2, 0.3, 0.4, 0.5]}}]})
    emit('c2', http_status=s, observation=('update id=3 image_vector -> status=%s' % s))

    s, b, t = http('POST', BASE + '/collections/' + COL + '/points/delete',
                   {"points": [1, 2], "vectors": ["image_vector"]})
    _, cb, _ = http('POST', BASE + '/collections/' + COL + '/points/count', {"exact": True})
    c = (cb or {}).get('result', {}).get('count')
    emit('c3', http_status=s, observation=('delete named vectors ids 1,2 -> status=%s, count=%s' % (s, c)))

    s, b, t = http('POST', BASE + '/collections/' + COL + '/points/search',
                   {"vector": {"name": "image_vector", "vector": [0.1, 0.2, 0.3, 0.4]}, "limit": 5})
    n = len(b.get('result', [])) if b else None
    emit('c4', http_status=s, observation=(
        'search after lifecycle -> status=%s, %d results%s' % (
          s, n, ' (broken, BUG)' if s == 400 else ' (OK)')))
    print('probe_qdrant_9366 done')

if __name__ == '__main__':
    main()

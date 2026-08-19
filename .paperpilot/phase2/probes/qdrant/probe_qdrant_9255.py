"""probe for qdrant/qdrant#9255  Payload filter returns points with missing payload field
version: 1.18.1 | gt: FP_NOT_REPRO | class: semantics
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready

BASE = 'http://localhost:6333'
COL = 'test_payload_filter'

def main():
    if not wait_ready(BASE + '/'):
        emit('setup', observation='server not ready')
        return
    http('DELETE', BASE + '/collections/' + COL)
    http('PUT', BASE + '/collections/' + COL, {"vectors": {"size": 4, "distance": "Cosine"}})
    # 10 points: even red, odd blue; ids 3,6 have NO color payload
    pts = []
    for i in range(1, 11):
        p = {"id": i, "vector": [0.1, 0.2, 0.3, 0.4]}
        if i not in (3, 6):
            p["payload"] = {"color": "red" if i % 2 == 0 else "blue"}
        pts.append(p)
    http('PUT', BASE + '/collections/' + COL + '/points?wait=true', {"points": pts})

    s, b, t = http('POST', BASE + '/collections/' + COL + '/points/search',
                   {"vector": [0.1, 0.2, 0.3, 0.4], "limit": 10, "with_payload": True,
                    "filter": {"must": [{"key": "color", "match": {"value": "red"}}]}})
    res = (b or {}).get('result', [])
    ids = [r.get('id') for r in res]
    missing = [r.get('id') for r in res if not r.get('payload')]
    emit('c1', http_status=s, observation=(
        'filter color=red -> %d results ids=%s missing_payload_ids=%s%s' % (
          len(res), ids, missing, ' (BUG)' if missing else ' (expected 4 red, seems OK)')))
    print('probe_qdrant_9255 done')

if __name__ == '__main__':
    main()

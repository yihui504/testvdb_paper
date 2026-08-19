"""probe for qdrant/qdrant#9373  Payload index silently returns 2/25 after wait:true
version: 1.18.2 | gt: FP_NOT_REPRO | class: behavior
"""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready

BASE = 'http://localhost:6333'
COL = 'test_idx2'

def main():
    if not wait_ready(BASE + '/'):
        emit('setup', observation='server not ready')
        return
    http('DELETE', BASE + '/collections/' + COL)
    http('PUT', BASE + '/collections/' + COL, {"vectors": {"size": 4, "distance": "Cosine"}})
    pts = [{"id": i, "vector": [0.1, 0.2, 0.3, 0.4],
            "payload": {"category_id": "cat_a" if i <= 25 else "cat_b"}} for i in range(1, 51)]
    http('PUT', BASE + '/collections/' + COL + '/points?wait=true', {"points": pts})
    http('PUT', BASE + '/collections/' + COL + '/index',
         {"field_name": "category_id", "field_schema": {"type": "keyword"}, "wait": True})
    time.sleep(2)

    _, b, _ = http('GET', BASE + '/collections/' + COL)
    total = (b or {}).get('result', {}).get('points_count')

    s, b, t = http('POST', BASE + '/collections/' + COL + '/points/scroll',
                   {"filter": {"must": [{"key": "category_id", "match": {"value": "cat_a"}}]}, "limit": 100})
    res = (b or {}).get('result', {}).get('points', [])
    emit('c1', http_status=s, observation=(
        'indexed filter cat_a -> %d collected (total=%s)%s' % (
          len(res), total, ' (severely incomplete, BUG)' if len(res) < 25 else ' (25/25 expected, OK; fresh ctl repro unlikely)')))
    print('probe_qdrant_9373 done')

if __name__ == '__main__':
    main()

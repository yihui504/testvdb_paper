"""probe for qdrant/qdrant#8688  Cosine similarity score strictly exceeds upper bound of 1.0
version: 1.17.1 | gt: PENDING_SELF_LABELED | class: semantics
"""
import os, sys, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready

BASE = 'http://localhost:6333'
COL = 'test_cosine_bound'
DIM = 128

def main():
    if not wait_ready(BASE + '/'):
        emit('setup', observation='server not ready')
        return
    http('DELETE', BASE + '/collections/' + COL)
    http('PUT', BASE + '/collections/' + COL, {"vectors": {"size": DIM, "distance": "Cosine"}})

    r = random.Random(42)
    v = [round(r.uniform(-1, 1), 6) for _ in range(DIM)]
    http('PUT', BASE + '/collections/' + COL + '/points', {"points": [{"id": 1, "vector": v}]})

    s, b, t = http('POST', BASE + '/collections/' + COL + '/points/search',
                   {"vector": v, "limit": 1, "with_payload": False})
    res = (b or {}).get('result', [])
    score = res[0].get('score') if res else None
    emit('c1', http_status=s, resp_code=(b or {}).get('status.code'), observation=(
        'identical self-match cosine score=%s%s' % (score,
          ' (exceeds 1.0, BUG)' if score and score > 1.0 else ' (<=1.0, OK)')))
    print('probe_qdrant_8688 done')

if __name__ == '__main__':
    main()

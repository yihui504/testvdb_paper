"""probe for qdrant/qdrant#9869  Write ops accept timeout=0 despite OpenAPI minimum:1
version: 1.18.2 | gt: PENDING_SELF_LABELED | class: doc_mismatch
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready

BASE = 'http://localhost:6333'
COL = 'test_timeout'

def main():
    if not wait_ready(BASE + '/'):
        emit('setup', observation='server not ready')
        return
    http('DELETE', BASE + '/collections/' + COL)
    http('PUT', BASE + '/collections/' + COL, {"vectors": {"size": 4, "distance": "Cosine"}})
    http('PUT', BASE + '/collections/' + COL + '/points',
         {"points": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4]}]})

    s, b, t = http('POST', BASE + '/collections/' + COL + '/points/payload?timeout=0',
                   {"payload": {"x": 1}, "points": [1]})
    emit('c1', http_status=s, resp_code=(b or {}).get('status.code'), observation=(
        'set payload timeout=0 -> status=%s body=%r%s' % (
          s, t, ' (accepted, schema minimum:1 not enforced, BUG)' if s == 200 else ' (rejected 422, OK)')))

    s, b, t = http('POST', BASE + '/collections/' + COL + '/points/payload?timeout=1',
                   {"payload": {"x": 2}, "points": [1]})
    emit('c2', http_status=s, observation=('set payload timeout=1 -> status=%s (control)' % s))
    print('probe_qdrant_9869 done')

if __name__ == '__main__':
    main()

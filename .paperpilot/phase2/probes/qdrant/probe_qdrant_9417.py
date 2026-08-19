"""probe for qdrant/qdrant#9417  Missing vectors field accepted -> unusable collection
version: 1.18.2 | gt: FP_BY_DESIGN | class: param_validation
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready

BASE = 'http://localhost:6333'
COL = 'broken2'

def main():
    if not wait_ready(BASE + '/'):
        emit('setup', observation='server not ready')
        return
    http('DELETE', BASE + '/collections/' + COL)
    s, b, t = http('PUT', BASE + '/collections/' + COL, {"shard_number": 1})
    _, gb, _ = http('GET', BASE + '/collections/' + COL)
    exists = (gb or {}).get('result') is not None
    emit('c1', http_status=s, observation=(
        'create without vectors field -> status=%s, collection_exists=%s' % (s, exists)))

    s, b, t = http('PUT', BASE + '/collections/' + COL + '/points?wait=true',
                   {"points": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4]}]})
    emit('c1b', http_status=s, observation=(
        'upsert into it -> status=%s body=%r (vector op fails)' % (s, t)))
    print('probe_qdrant_9417 done')

if __name__ == '__main__':
    main()

"""probe for qdrant/qdrant#9416  vectors={} silently accepted -> unusable collection
version: 1.18.2 | gt: FP_BY_DESIGN | class: param_validation
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready

BASE = 'http://localhost:6333'
COL = 'broken'

def main():
    if not wait_ready(BASE + '/'):
        emit('setup', observation='server not ready')
        return
    http('DELETE', BASE + '/collections/' + COL)
    s, b, t = http('PUT', BASE + '/collections/' + COL, {"vectors": {}})
    _, gb, _ = http('GET', BASE + '/collections/' + COL)
    exists = (gb or {}).get('result') is not None
    emit('c1', http_status=s, observation=(
        'vectors={} create -> status=%s, collection_exists=%s' % (s, exists)))

    s, b, t = http('PUT', BASE + '/collections/' + COL + '/points?wait=true',
                   {"points": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4]}]})
    emit('c2', http_status=s, observation=(
        'upsert into vectorless collection -> status=%s body=%r (no default vector config -> unusable)' % (s, t)))
    print('probe_qdrant_9416 done')

if __name__ == '__main__':
    main()

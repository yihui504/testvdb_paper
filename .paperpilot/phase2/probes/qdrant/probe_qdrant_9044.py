"""probe for qdrant/qdrant#9044  Collection creation accepts size=65536 despite FAQ max 65535
version: 1.12.1 | gt: PENDING_SELF_LABELED | class: doc_mismatch
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready

BASE = 'http://localhost:6333'

def main():
    if not wait_ready(BASE + '/'):
        emit('setup', observation='server not ready')
        return
    for name, size in [('test_65536', 65536), ('test_65537', 65537), ('test_65535', 65535)]:
        http('DELETE', BASE + '/collections/' + name)
        s, b, t = http('PUT', BASE + '/collections/' + name,
                       {"vectors": {"size": size, "distance": "Cosine"}})
        emit('c%d' % {65536: 1, 65537: 2, 65535: 3}[size], http_status=s, observation=(
            'size=%s create -> status=%s' % (size, s)))
    print('probe_qdrant_9044 done')

if __name__ == '__main__':
    main()

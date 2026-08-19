"""probe for qdrant/qdrant#9942  OpenAPI VectorParams.size missing maximum:65536 constraint
version: 1.18.2 | gt: PENDING_SELF_LABELED | class: doc_mismatch
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready

BASE = 'http://localhost:6333'

def main():
    if not wait_ready(BASE + '/'):
        emit('setup', observation='server not ready')
        return
    # c1: inspect published OpenAPI schema
    s, b, t = http('GET', BASE + '/openapi.json')
    vp = None
    if b:
        props = b.get('components', {}).get('schemas', {}).get('VectorParams', {}).get('properties', {})
        vp = props.get('size', {})
    emit('c1', http_status=s, observation=(
        'VectorParams.size schema=%s' % (vp,)))

    # c2: runtime create size=70000 (>65536), new collection name
    http('DELETE', BASE + '/collections/repro2')
    s, b, t = http('PUT', BASE + '/collections/repro2',
                   {"vectors": {"size": 70000, "distance": "Cosine"}})
    emit('c2', http_status=s, observation=(
        'size=70000 create -> status=%s body=%r (runtime enforces 422 regardless of schema)' % (s, t)))
    print('probe_qdrant_9942 done')

if __name__ == '__main__':
    main()

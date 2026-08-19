"""probe for weaviate/weaviate#11742  PQ bitCompression accepts string "true" instead of boolean true
version: 1.38.0 | gt: PENDING_SELF_LABELED | class: type_coercion
NOTE needs_manual: result may depend on JSON decoding library coercion behavior; ambiguous whether
coercion to true is intended. Follow-up: also pass "false" to confirm truthiness-based coercion.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready

BASE = os.environ.get('WEAVIATE_BASE', 'http://localhost:8080/v1')

def main():
    wait_ready(BASE + '/.well-known/ready')
    http('DELETE', BASE + '/schema/TestClass')
    payload = {
        'class': 'TestClass', 'vectorizer': 'none',
        'vectorIndexConfig': {
            'vectorIndexType': 'hnsw',
            'pq': {'enabled': True, 'bitCompression': 'true', 'segments': 96, 'centroids': 256},
        },
    }
    st, body, _ = http('POST', BASE + '/schema', payload)
    stored = None
    if st == 200:
        _, stored, _ = http('GET', BASE + '/schema/TestClass')
    pq = (stored or {}).get('vectorIndexConfig', {}).get('pq', {})
    emit('c1', http_status=st, stored_bitCompression=pq.get('bitCompression'),
         obs='POST schema pq.bitCompression="true" (string): got HTTP %s; stored bitCompression=%s (bug: 200 coerced to boolean true; correct: 422)' % (
             st, pq.get('bitCompression')))
    print('probe_weaviate_11742 done')

if __name__ == '__main__':
    main()

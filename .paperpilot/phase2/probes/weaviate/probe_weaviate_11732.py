"""probe for weaviate/weaviate#11732  vectorIndexConfig.distance silently accepts null and defaults to cosine
version: 1.38.0 | gt: TP_FIXED_PR | class: type_coercion
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
        'vectorIndexConfig': {'distance': None},
    }
    st, body, _ = http('POST', BASE + '/schema', payload)
    stored = None
    if st == 200:
        _, stored, _ = http('GET', BASE + '/schema/TestClass')
    cfg = (stored or {}).get('vectorIndexConfig', {})
    emit('c1', http_status=st, stored_distance=cfg.get('distance'),
         obs='POST schema distance=null: got HTTP %s; stored distance=%s (bug: 200 silently defaulted to cosine; correct: 422)' % (
             st, cfg.get('distance')))
    print('probe_weaviate_11732 done')

if __name__ == '__main__':
    main()

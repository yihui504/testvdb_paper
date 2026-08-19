"""probe for weaviate/weaviate#11395  dynamicEfMin > dynamicEfMax accepted (no validation)
version: 1.37.4 | gt: SELF_CLOSED | class: param_validation
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready

BASE = os.environ.get('WEAVIATE_BASE', 'http://localhost:8080/v1')

def main():
    wait_ready(BASE + '/.well-known/ready')
    http('DELETE', BASE + '/schema/TestEfBad')  # idempotent cleanup, ignore 404
    payload = {
        'class': 'TestEfBad', 'vectorizer': 'none',
        'vectorIndexConfig': {'distance': 'cosine', 'dynamicEfMin': 500,
                             'dynamicEfMax': 10, 'dynamicEfFactor': 8},
        'properties': [{'name': 'text', 'dataType': ['text']}],
    }
    st, body, _ = http('POST', BASE + '/schema', payload)
    stored = None
    if st == 200:
        _, stored, _ = http('GET', BASE + '/schema/TestEfBad')
    cfg = (stored or {}).get('vectorIndexConfig', {})
    emit('c1', http_status=st, dynamicEfMin=cfg.get('dynamicEfMin'),
         dynamicEfMax=cfg.get('dynamicEfMax'),
         obs='POST schema with dynamicEfMin=500 > dynamicEfMax=10: got HTTP %s; stored min=%s max=%s' % (
             st, cfg.get('dynamicEfMin'), cfg.get('dynamicEfMax')))
    print('probe_weaviate_11395 done')

if __name__ == '__main__':
    main()

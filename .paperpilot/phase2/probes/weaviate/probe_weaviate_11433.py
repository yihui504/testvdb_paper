"""probe for weaviate/weaviate#11433  Negative ef=-1 accepted in vectorIndexConfig without validation
version: 1.37.4 | gt: SELF_CLOSED | class: param_validation
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready

BASE = os.environ.get('WEAVIATE_BASE', 'http://localhost:8080/v1')

def main():
    wait_ready(BASE + '/.well-known/ready')
    http('DELETE', BASE + '/schema/TestEfneg')
    payload = {
        'class': 'TestEfneg', 'vectorizer': 'none',
        'vectorIndexConfig': {'distance': 'cosine', 'ef': -1},
        'properties': [{'name': 'text', 'dataType': ['text']}],
    }
    st, body, _ = http('POST', BASE + '/schema', payload)
    stored = None
    if st == 200:
        _, stored, _ = http('GET', BASE + '/schema/TestEfneg')
    cfg = (stored or {}).get('vectorIndexConfig', {})
    emit('c1', http_status=st, ef=cfg.get('ef'),
         obs='POST schema with HNSW ef=-1: got HTTP %s; stored ef=%s' % (st, cfg.get('ef')))
    print('probe_weaviate_11433 done')

if __name__ == '__main__':
    main()

"""probe for weaviate/weaviate#11436  Negative ef=-1 accepted in vectorIndexConfig
version: 1.37.4 | class: param_validation
NOTE: probe records actual server behavior, asserts no fix.
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
    emit('c1', http_status=st,
         obs='POST schema with HNSW ef=-1: got HTTP %s' % st)
    print('probe_weaviate_11436 done')

if __name__ == '__main__':
    main()

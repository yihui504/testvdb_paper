"""probe for weaviate/weaviate#11401  replicationFactor=-1 accepted and silently normalized to 1
version: 1.37.4 | gt: TP_FIXED_PR | class: param_validation
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready

BASE = os.environ.get('WEAVIATE_BASE', 'http://localhost:8080/v1')

def main():
    wait_ready(BASE + '/.well-known/ready')
    http('DELETE', BASE + '/schema/TestRep')
    payload = {
        'class': 'TestRep', 'vectorizer': 'none',
        'replicationConfig': {'factor': -1},
        'vectorIndexConfig': {'distance': 'cosine'},
        'properties': [{'name': 'text', 'dataType': ['text']}],
    }
    st, body, _ = http('POST', BASE + '/schema', payload)
    stored = None
    if st == 200:
        _, stored, _ = http('GET', BASE + '/schema/TestRep')
    rep = (stored or {}).get('replicationConfig', {})
    emit('c1', http_status=st, factor=rep.get('factor'),
         obs='POST schema replicationConfig.factor=-1: got HTTP %s; stored factor=%s' % (
             st, rep.get('factor')))
    print('probe_weaviate_11401 done')

if __name__ == '__main__':
    main()

"""probe for weaviate/weaviate#11398  bq.rescoreLimit=-1 accepted and silently discarded
version: 1.37.4 | gt: SELF_CLOSED | class: param_validation
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready

BASE = os.environ.get('WEAVIATE_BASE', 'http://localhost:8080/v1')

def main():
    wait_ready(BASE + '/.well-known/ready')
    http('DELETE', BASE + '/schema/TestBQ')
    payload = {
        'class': 'TestBQ', 'vectorizer': 'none',
        'vectorIndexConfig': {'distance': 'cosine', 'bq': {'enabled': True, 'rescoreLimit': -1}},
        'properties': [{'name': 'text', 'dataType': ['text']}],
    }
    st, body, _ = http('POST', BASE + '/schema', payload)
    stored = None
    if st == 200:
        _, stored, _ = http('GET', BASE + '/schema/TestBQ')
    cfg = (stored or {}).get('vectorIndexConfig', {})
    bq = cfg.get('bq', {})
    emit('c1', http_status=st, bq=bq,
         obs='POST schema with bq.rescoreLimit=-1: got HTTP %s; stored bq=%s (rescoreLimit present=%s)' % (
             st, bq, 'rescoreLimit' in bq))
    print('probe_weaviate_11398 done')

if __name__ == '__main__':
    main()

"""probe for weaviate/weaviate#11400  flatSearchCutoff accepts negative values (no validation)
version: 1.37.4 | gt: TP_FIXED_PR | class: param_validation
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready

BASE = os.environ.get('WEAVIATE_BASE', 'http://localhost:8080/v1')

def main():
    wait_ready(BASE + '/.well-known/ready')
    http('DELETE', BASE + '/schema/TestFC')
    payload = {
        'class': 'TestFC', 'vectorizer': 'none',
        'vectorIndexConfig': {'distance': 'cosine', 'flatSearchCutoff': -100},
        'properties': [{'name': 'text', 'dataType': ['text']}],
    }
    st, body, _ = http('POST', BASE + '/schema', payload)
    stored = None
    if st == 200:
        _, stored, _ = http('GET', BASE + '/schema/TestFC')
    cfg = (stored or {}).get('vectorIndexConfig', {})
    emit('c1', http_status=st, flatSearchCutoff=cfg.get('flatSearchCutoff'),
         obs='POST schema flatSearchCutoff=-100: got HTTP %s; stored cutoff=%s' % (
             st, cfg.get('flatSearchCutoff')))
    print('probe_weaviate_11400 done')

if __name__ == '__main__':
    main()

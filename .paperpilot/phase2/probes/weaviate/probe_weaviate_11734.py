"""probe for weaviate/weaviate#11734  multiTenancyConfig accepts null for boolean autoTenantCreation/autoTenantActivation
version: 1.38.0 | gt: PENDING_SELF_LABELED | class: type_coercion
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
        'multiTenancyConfig': {'enabled': True, 'autoTenantCreation': None, 'autoTenantActivation': None},
    }
    st, body, _ = http('POST', BASE + '/schema', payload)
    stored = None
    if st == 200:
        _, stored, _ = http('GET', BASE + '/schema/TestClass')
    mtc = (stored or {}).get('multiTenancyConfig', {})
    emit('c1', http_status=st, multiTenancyConfig=mtc,
         obs='POST schema autoTenantCreation/Activation=null: got HTTP %s; stored multiTenancyConfig=%s (bug: 200 with null booleans; correct: 422)' % (
             st, mtc))
    print('probe_weaviate_11734 done')

if __name__ == '__main__':
    main()

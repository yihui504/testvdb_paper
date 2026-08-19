"""probe for weaviate/weaviate#11738  phoneNumber.defaultCountry accepts invalid ISO 3166-1 code "ZZ"
version: 1.38.0 | gt: PENDING_SELF_LABELED | class: param_validation
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready

BASE = os.environ.get('WEAVIATE_BASE', 'http://localhost:8080/v1')

def main():
    wait_ready(BASE + '/.well-known/ready')
    http('DELETE', BASE + '/schema/TestClass')
    st1, _, _ = http('POST', BASE + '/schema', {
        'class': 'TestClass', 'vectorizer': 'none',
        'properties': [{'name': 'phone', 'dataType': ['phoneNumber']}],
    })
    emit('c1', http_status=st1, obs='POST schema with phoneNumber property: got HTTP %s' % st1)

    st2, b2, _ = http('POST', BASE + '/objects', {
        'class': 'TestClass', 'properties': {'phone': {'input': '+1234567890', 'defaultCountry': 'ZZ'}},
    })
    emit('c2', http_status=st2,
         obs='POST object phone.defaultCountry="ZZ": got HTTP %s (bug: 200 stored and processed; correct: 422 invalid ISO code)' % st2)
    print('probe_weaviate_11738 done')

if __name__ == '__main__':
    main()

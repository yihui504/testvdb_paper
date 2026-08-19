"""probe for weaviate/weaviate#11739  phoneNumber.input accepts alphabetic chars like "CALL-NOW" without validation
version: 1.38.0 | gt: PENDING_SELF_LABELED | class: param_validation
NOTE needs_manual: some phone systems intentionally allow letter mnemonics and convert them; whether
rejection is required is a judgment call. Record actual server behavior (status + body).
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
        'class': 'TestClass', 'properties': {'phone': {'input': '+1-555-CALL-NOW', 'defaultCountry': 'US'}},
    })
    emit('c2', http_status=st2, body=b2,
         obs='POST object phone.input="+1-555-CALL-NOW" (alphabetic): got HTTP %s; body=%s (bug: 200 stored raw alphabetic; correct: 422)' % (
             st2, b2))
    print('probe_weaviate_11739 done')

if __name__ == '__main__':
    main()

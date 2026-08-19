"""probe for weaviate/weaviate#11745  Text property accepts strings containing ASCII control chars (SOH, STX, ETX)
version: 1.38.0 | gt: PENDING_SELF_LABELED | class: param_validation
NOTE needs_manual: curl/HTTP layer behavior on raw control bytes varies; must verify the control bytes
actually reach and are stored by the API. Raw 0x01/0x02/0x03 bytes sent via requests .data=.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready
import requests

BASE = os.environ.get('WEAVIATE_BASE', 'http://localhost:8080/v1')

def raw_post(path, body_bytes):
    try:
        r = requests.post(BASE + path, data=body_bytes,
                          headers={'Content-Type': 'application/json'}, timeout=30)
        try:
            return r.status_code, r.json()
        except Exception:
            return r.status_code, None
    except Exception as e:
        return None, 'EXCEPTION: %s' % e

def main():
    wait_ready(BASE + '/.well-known/ready')
    http('DELETE', BASE + '/schema/TestText')
    st1, _, _ = http('POST', BASE + '/schema', {
        'class': 'TestText', 'properties': [{'name': 'text_field', 'dataType': ['text']}],
    })
    emit('c1', http_status=st1, obs='POST schema TestText: got HTTP %s' % st1)
    body = b'{"class":"TestText","properties":{"text_field":"abc\x01\x02\x03def"}}'
    st2, b2 = raw_post('/objects', body)
    emit('c2', http_status=st2,
         obs='POST object text_field with raw 0x01 0x02 0x03 control bytes: got HTTP %s (bug: 200 stored raw control chars; correct: 422/sanitize)' % st2)
    print('probe_weaviate_11745 done')

if __name__ == '__main__':
    main()

"""probe for weaviate/weaviate#11743  text property accepts strings containing NUL bytes (\\x00) without validation
version: 1.38.0 | gt: PENDING_SELF_LABELED | class: param_validation
NOTE needs_manual: whether a raw NUL byte in JSON is parsed/forwarded depends on client+server JSON
parsing; must confirm actual bytes reach the API and are stored. Index-truncation impact needs a query.
Raw-byte body sent via requests .data= (not .json=) to preserve the literal NUL byte.
"""
import os, sys, json
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
    http('DELETE', BASE + '/schema/TestClass')
    st1, _, _ = http('POST', BASE + '/schema', {
        'class': 'TestClass', 'vectorizer': 'none',
        'properties': [{'name': 'text_field', 'dataType': ['text']}],
    })
    emit('c1', http_status=st1, obs='POST schema with text property: got HTTP %s' % st1)

    body = b'{"class":"TestClass","properties":{"text_field":"hello\x00world"}}'
    st2, b2 = raw_post('/objects', body)
    obj_id = ((b2 or {}).get('id') if isinstance(b2, dict) else None)
    emit('c2', http_status=st2,
         obs='POST object with raw NUL byte in text_field: got HTTP %s; id=%s (bug: 200 accepted NUL; correct: 422)' % (
             st2, obj_id))

    if st2 == 200 and obj_id:
        st3, stored, _ = http('GET', BASE + ('/objects/TestClass/%s' % obj_id))
        val = (stored or {}).get('properties', {}).get('text_field')
        emit('c3', http_status=st3, text_field=val,
             obs='GET object text_field: got HTTP %s; value=%r (check silent truncation at NUL)' % (st3, val))
    print('probe_weaviate_11743 done')

if __name__ == '__main__':
    main()

"""probe for weaviate/weaviate#11744  Text property accepts strings containing lone UTF-16 surrogates
version: 1.38.0 | gt: PENDING_SELF_LABELED | class: param_validation
NOTE needs_manual: whether a \\ud800 escape is even accepted/forwarded depends on client+server JSON
parser; must verify the raw escape reaches the API regardless of local decode. Retrieval may error.
Lone surrogate is sent as the literal 6-char escape sequence \ud800 inside the JSON string (raw body via .data=).
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
    # control: normal text
    st2, b2, _ = http('POST', BASE + '/objects', {'class': 'TestText', 'properties': {'text_field': 'hello world'}})
    emit('c2', http_status=st2, obs='CONTROL POST object normal text "hello world": got HTTP %s' % st2)
    # bug: literal \ud800 escape (real backslash-u-d-8-0-0 chars) in JSON string
    body = b'{"class":"TestText","properties":{"text_field":"\\ud800"}}'
    st3, b3 = raw_post('/objects', body)
    emit('c3', http_status=st3, obs='POST object text_field="\\\\ud800" (lone surrogate escape): got HTTP %s (bug: 200 accepted; correct: 400/422)' % st3)
    print('probe_weaviate_11744 done')

if __name__ == '__main__':
    main()

"""probe for weaviate/weaviate#11736  blob accepts long non-base64 garbage string without validation
version: 1.38.0 | gt: PENDING_SELF_LABELED | class: param_validation
NOTE needs_manual: the garbage string is syntactically valid base64 (len%4==0, allowed alphabet);
whether it 'should' be rejected is a semantic judgment that may vary by server logic. Record stored value/status.
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
        'properties': [{'name': 'blob_field', 'dataType': ['blob']}],
    })
    emit('c1', http_status=st1, obs='POST schema with blob property: got HTTP %s' % st1)

    garbage = 'x' * 100
    st2, b2, _ = http('POST', BASE + '/objects', {
        'class': 'TestClass', 'properties': {'blob_field': garbage},
    })
    emit('c2', http_status=st2,
         obs='POST object blob_field=%s (100 x chars): got HTTP %s (bug: 200 stored garbage as-is; correct: 422). stored_id=%s' % (
             garbage, st2, (b2 or {}).get('id') if b2 else None))
    print('probe_weaviate_11736 done')

if __name__ == '__main__':
    main()

"""probe for weaviate/weaviate#11735  int64 boundary 9223372036854775807 silently truncated to 9223372036854776000
version: 1.38.0 | gt: PENDING_SELF_LABELED | class: type_coercion
NOTE needs_manual: response serialization (JSON number) may itself lose precision before/independent
of storage; distinguish storage truncation from JSON read/write round-trip loss. Record both stored GET and raw response value.
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
        'properties': [{'name': 'int_field', 'dataType': ['int']}],
    })
    emit('c1', http_status=st1, obs='POST schema with int property: got HTTP %s' % st1)

    st2, b2, _ = http('POST', BASE + '/objects', {
        'class': 'TestClass', 'properties': {'int_field': 9223372036854775807},
    })
    obj_id = ((b2 or {}).get('id') if b2 else None)
    emit('c2', http_status=st2, obs='POST object int_field=9223372036854775807: got HTTP %s; id=%s' % (st2, obj_id))

    stored = None
    if b2 and b2.get('id'):
        st3, stored, _ = http('GET', BASE + '/objects/TestClass/%s' % b2.get('id'))
        val = (stored or {}).get('properties', {}).get('int_field')
        emit('c3', http_status=st3, int_field=val,
             obs='GET object int_field: got HTTP %s; stored value=%s (expect exact 9223372036854775807; bug: 9223372036854776000)' % (
                 st3, val))
    print('probe_weaviate_11735 done')

if __name__ == '__main__':
    main()

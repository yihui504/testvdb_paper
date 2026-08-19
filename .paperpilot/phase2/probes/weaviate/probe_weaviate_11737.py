"""probe for weaviate/weaviate#11737  date accepts year 0000 and pre-1970 values without RFC3339 validation
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
        'properties': [{'name': 'date_field', 'dataType': ['date']}],
    })
    emit('c1', http_status=st1, obs='POST schema with date property: got HTTP %s' % st1)

    st2, b2, _ = http('POST', BASE + '/objects', {
        'class': 'TestClass', 'properties': {'date_field': '0000-01-01T00:00:00Z'},
    })
    emit('c2', http_status=st2,
         obs='POST object date_field="0000-01-01T00:00:00Z" (year 0000): got HTTP %s (bug: 200 accepted; RFC3339 forbids year 0000)' % st2)

    st3, b3, _ = http('POST', BASE + '/objects', {
        'class': 'TestClass', 'properties': {'date_field': '1800-06-15T08:30:00Z'},
    })
    emit('c3', http_status=st3,
         obs='POST object date_field="1800-06-15T08:30:00Z" (pre-epoch): got HTTP %s (bug: 200 accepted)' % st3)
    print('probe_weaviate_11737 done')

if __name__ == '__main__':
    main()

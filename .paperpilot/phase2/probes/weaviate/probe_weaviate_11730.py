"""probe for weaviate/weaviate#11730  tokenization accepts empty string despite OpenAPI enum constraint
version: 1.38.0 | gt: TP_FIXED_PR | class: param_validation
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
        'properties': [{'name': 'text_field', 'dataType': ['text'], 'tokenization': ''}],
    }
    st, body, _ = http('POST', BASE + '/schema', payload)
    emit('c1', http_status=st,
         obs='POST schema with property tokenization="": got HTTP %s (bug: 200 created class with empty tokenization; correct: 422)' % st)
    print('probe_weaviate_11730 done')

if __name__ == '__main__':
    main()

"""probe for weaviate/weaviate#11661  GET /v1/objects returns 500 instead of 4xx when limit exceeds QUERY_MAXIMUM_RESULTS
version: 1.38.0 | gt: PENDING_SELF_LABELED | class: behavior
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready

BASE = os.environ.get('WEAVIATE_BASE', 'http://localhost:8080/v1')

def main():
    wait_ready(BASE + '/.well-known/ready')
    st, body, text = http('GET', BASE + '/objects?limit=10001')
    emit('c1', http_status=st, body=body, text=text,
         obs='GET /v1/objects?limit=10001 (over QUERY_MAXIMUM_RESULTS=10000): got HTTP %s; body=%s (bug: 500 Internal Server Error; correct: 4xx)' % (
             st, body))
    print('probe_weaviate_11661 done')

if __name__ == '__main__':
    main()

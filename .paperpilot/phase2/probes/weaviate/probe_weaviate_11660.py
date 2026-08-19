"""probe for weaviate/weaviate#11660  REST API GET /v1/objects silently accepts negative limit
version: 1.38.0 | gt: PENDING_SELF_LABELED | class: param_validation
NOTE needs_manual: no objects inserted; negative-limit behavior may depend on whether any objects
exist (empty vs non-empty result set). Observe response body to judge.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready

BASE = os.environ.get('WEAVIATE_BASE', 'http://localhost:8080/v1')

def main():
    wait_ready(BASE + '/.well-known/ready')
    st, body, _ = http('GET', BASE + '/objects?limit=-1')
    emit('c1', http_status=st, body=body,
         obs='GET /v1/objects?limit=-1: got HTTP %s; body=%s (bug: 200 with empty objects; correct: 4xx)' % (
             st, body))
    print('probe_weaviate_11660 done')

if __name__ == '__main__':
    main()

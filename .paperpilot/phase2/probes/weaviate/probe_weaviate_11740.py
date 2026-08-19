"""probe for weaviate/weaviate#11740  GraphQL queries accept negative limit values
version: 1.38.0 | gt: PENDING_SELF_LABELED | class: param_validation
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready

BASE = os.environ.get('WEAVIATE_BASE', 'http://localhost:8080/v1')

def main():
    wait_ready(BASE + '/.well-known/ready')
    http('DELETE', BASE + '/schema/TestLimit')
    st1, _, _ = http('POST', BASE + '/schema', {
        'class': 'TestLimit', 'properties': [{'name': 'name', 'dataType': ['text']}],
    })
    emit('c1', http_status=st1, obs='POST schema TestLimit: got HTTP %s' % st1)
    # insert two objects so GraphQL results are non-empty
    http('POST', BASE + '/batch/objects', {'objects': [
        {'class': 'TestLimit', 'properties': {'name': 'item1'}},
        {'class': 'TestLimit', 'properties': {'name': 'item2'}},
    ]})
    # control: limit=0 should be rejected 400
    st2, b2, t2 = http('POST', BASE + '/graphql', {'query': '{ Get { TestLimit(limit: 0) { name } } }'})
    emit('c2', http_status=st2,
         obs='CONTROL GraphQL limit=0: got HTTP %s (expect 400 "limit must be greater than 0")' % st2)
    # bug: limit=-1 accepted 200
    st3, b3, _ = http('POST', BASE + '/graphql', {'query': '{ Get { TestLimit(limit: -1) { name } } }'})
    emit('c3', http_status=st3,
         obs='GraphQL limit=-1: got HTTP %s (bug: 200 accepted; correct: 400)' % st3)
    # bug: limit=-100 accepted 200
    st4, b4, _ = http('POST', BASE + '/graphql', {'query': '{ Get { TestLimit(limit: -100) { name } } }'})
    emit('c4', http_status=st4,
         obs='GraphQL limit=-100: got HTTP %s (bug: 200 accepted; correct: 400)' % st4)
    print('probe_weaviate_11740 done')

if __name__ == '__main__':
    main()

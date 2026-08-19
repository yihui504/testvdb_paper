"""probe for weaviate/weaviate#11731  replicationConfig.deletionStrategy accepts empty string outside enum
version: 1.38.0 | gt: PENDING_SELF_LABELED | class: param_validation
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
        'replicationConfig': {'factor': 1, 'deletionStrategy': ''},
    }
    st, body, _ = http('POST', BASE + '/schema', payload)
    emit('c1', http_status=st,
         obs='POST schema with replicationConfig.deletionStrategy="": got HTTP %s (bug: 200 stored empty deletionStrategy; correct: 422)' % st)
    print('probe_weaviate_11731 done')

if __name__ == '__main__':
    main()

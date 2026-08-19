"""probe for weaviate/weaviate#11729  shardingConfig.desiredCount accepts negatives but rejects zero
version: 1.38.0 | gt: TP_FIXED_PR | class: param_validation
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready

BASE = os.environ.get('WEAVIATE_BASE', 'http://localhost:8080/v1')

def main():
    wait_ready(BASE + '/.well-known/ready')
    http('DELETE', BASE + '/schema/TestZero')
    http('DELETE', BASE + '/schema/TestNeg')
    # control: desiredCount=0 should be rejected 422 (proves validation exists)
    st0, b0, _ = http('POST', BASE + '/schema', {'class': 'TestZero', 'shardingConfig': {'desiredCount': 0}})
    emit('c1', http_status=st0,
         obs='CONTROL POST schema desiredCount=0: got HTTP %s (expect 422 rejection)' % st0)
    # bug: desiredCount=-1 accepted with 200
    st1, b1, _ = http('POST', BASE + '/schema', {'class': 'TestNeg', 'shardingConfig': {'desiredCount': -1}})
    emit('c2', http_status=st1,
         obs='POST schema desiredCount=-1: got HTTP %s (bug: 200 accepted despite negative; correct: 422)' % st1)
    print('probe_weaviate_11729 done')

if __name__ == '__main__':
    main()

"""probe for weaviate/weaviate#12041  Batch delete returns HTTP 500 instead of 422 when match.where or match.class missing
version: 1.38.2 | gt: TP_FIXED_PR | class: behavior
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready

BASE = os.environ.get('WEAVIATE_BASE', 'http://localhost:8080/v1')

def main():
    wait_ready(BASE + '/.well-known/ready')
    http('DELETE', BASE + '/schema/BoundaryTestBatchDelete')
    st1, _, _ = http('POST', BASE + '/schema', {
        'class': 'BoundaryTestBatchDelete', 'vectorizer': 'none',
        'properties': [{'name': 'title', 'dataType': ['text']}],
    })
    emit('c1', http_status=st1, obs='POST schema BoundaryTestBatchDelete: got HTTP %s' % st1)
    # Case A: match.class present, match.where missing
    st2, b2, _ = http('DELETE', BASE + '/batch/objects',
                      {'match': {'class': 'BoundaryTestBatchDelete'}, 'output': 'minimal'})
    emit('c2', http_status=st2,
         obs='batch delete with class but missing where: got HTTP %s (bug: 500 "validate: empty match.where clause"; correct: 422)' % st2)
    # Case B: empty match object (both missing)
    st3, b3, _ = http('DELETE', BASE + '/batch/objects', {'match': {}, 'output': 'minimal'})
    emit('c3', http_status=st3,
         obs='batch delete with empty match {}: got HTTP %s (bug: 500 "validate: empty match.class clause"; correct: 422)' % st3)
    print('probe_weaviate_12041 done')

if __name__ == '__main__':
    main()

"""probe for weaviate/weaviate#11981  POST /v1/batch/objects accepts empty vector [] and reports per-item SUCCESS
version: 1.38.2 | gt: FP_BY_DESIGN | class: behavior
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready

BASE = os.environ.get('WEAVIATE_BASE', 'http://localhost:8080/v1')

def main():
    wait_ready(BASE + '/.well-known/ready')
    http('DELETE', BASE + '/schema/BatchVectorBugRepro')
    st1, _, _ = http('POST', BASE + '/schema', {
        'class': 'BatchVectorBugRepro', 'vectorizer': 'none', 'vectorIndexType': 'hnsw',
        'vectorIndexConfig': {'distance': 'cosine'},
    })
    emit('c1', http_status=st1, obs='POST schema BatchVectorBugRepro: got HTTP %s' % st1)
    # control: singular POST with vector=[] should be 422
    st2, b2, _ = http('POST', BASE + '/objects', {
        'class': 'BatchVectorBugRepro', 'properties': {'name': 'control-singular'}, 'vector': [],
    })
    emit('c2', http_status=st2,
         obs='CONTROL singular POST vector=[]: got HTTP %s (expect 422)' % st2)
    # bug: batch valid item + empty-vector item
    st3, b3, _ = http('POST', BASE + '/batch/objects', {'objects': [
        {'class': 'BatchVectorBugRepro', 'id': '11111111-1111-4111-8111-111111111111',
         'properties': {'name': 'valid-item'}, 'vector': [0.1, 0.2, 0.3, 0.4]},
        {'class': 'BatchVectorBugRepro', 'id': '22222222-2222-4222-8222-222222222222',
         'properties': {'name': 'bad-empty-vector'}, 'vector': []},
    ]})
    statuses = None
    if b3 and isinstance(b3, dict) and b3.get('results'):
        statuses = [r.get('status') for r in b3['results']]
    emit('c3', http_status=st3, results=statuses,
         obs='batch with empty-vector item: got HTTP %s; per-item statuses=%s (bug: both report SUCCESS; correct: per-item FAILED)' % (
             st3, statuses))
    print('probe_weaviate_11981 done')

if __name__ == '__main__':
    main()

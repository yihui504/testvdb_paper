"""probe for qdrant/qdrant#9149  shard_number=0 and negative values accepted
version: 1.18.1 | gt: TP_FIXED_PR | class: param_validation
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready

BASE = 'http://localhost:6333'

def main():
    if not wait_ready(BASE + '/'):
        emit('setup', observation='server not ready')
        return
    for name, shard in [('test_shard_zero', 0), ('test_shard_neg', -1)]:
        http('DELETE', BASE + '/collections/' + name)
        s, b, t = http('PUT', BASE + '/collections/' + name,
                       {"vectors": {"size": 4, "distance": "Cosine"}, "shard_number": shard})
        emit('c%d' % (1 if shard == 0 else 2), http_status=s, observation=(
            'shard_number=%s create -> status=%s%s' % (shard, s,
              ' (accepted, BUG)' if s == 200 else ' (rejected, FIX)')))
    print('probe_qdrant_9149 done')

if __name__ == '__main__':
    main()

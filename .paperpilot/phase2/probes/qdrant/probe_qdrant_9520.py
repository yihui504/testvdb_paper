"""probe for qdrant/qdrant#9520  Server crash on shard_number=INT_MAX (missing upper-bound validation)
version: 1.18.2 | gt: TP_FIXED_PR | class: crash
"""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready

BASE = 'http://localhost:6333'

def main():
    if not wait_ready(BASE + '/'):
        emit('setup', observation='server not ready')
        return
    http('DELETE', BASE + '/collections/test_shard_max')
    # INT_MAX shard: 用短 timeout 观察挂起/连接关闭,避免长阻塞
    s, b, t = http('PUT', BASE + '/collections/test_shard_max',
                   {"vectors": {"size": 4, "distance": "Cosine"}, "shard_number": 2147483647},
                   timeout=40)
    emit('c1', http_status=s, observation=(
        'shard_number=INT_MAX create -> status=%s err=%r' % (s, t)))

    # crash类: server-health 检查, 确认服务未被击穿
    time.sleep(1)
    hs, hb, ht = http('GET', BASE + '/')
    emit('server_health', http_status=hs, observation=('GET / after INT_MAX -> status=%s' % hs))

    http('DELETE', BASE + '/collections/test_rep0')
    s, b, t = http('PUT', BASE + '/collections/test_rep0',
                   {"vectors": {"size": 4, "distance": "Cosine"}, "replication_factor": 0})
    emit('c2', http_status=s, observation=(
        'replication_factor=0 create -> status=%s body=%r (control: expect 422)' % (s, t)))
    print('probe_qdrant_9520 done')

if __name__ == '__main__':
    main()

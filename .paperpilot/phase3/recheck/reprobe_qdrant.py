"""qdrant 存在性复验适配版: BASE 从 env QDRANT_BASE 读 (默认 6333), 逻辑与原 probe 一致.

用法: QDRANT_BASE=http://localhost:6344 python reprobe_qdrant.py <num>
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..', 'phase2', 'probes'))
from probe_common import http, emit, wait_ready

BASE = os.environ.get('QDRANT_BASE', 'http://localhost:6333')
NUM = int(sys.argv[1])


def p9017():
    col = 'test_hnsw_bug_r'
    http('DELETE', BASE + '/collections/' + col)
    http('PUT', BASE + '/collections/' + col, {"vectors": {"size": 4, "distance": "Cosine"}})
    http('PUT', BASE + '/collections/' + col + '/points', {"points": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4]}]})
    s, b, t = http('POST', BASE + '/collections/' + col + '/points/search',
                   {"vector": [0.1, 0.2, 0.3, 0.4], "limit": 3, "params": {"hnsw_ef": 0}})
    n = len(b.get('result', [])) if b else None
    emit('c1', http_status=s, resp_code=(b or {}).get('status.code'), observation=(
        'hnsw_ef=0 search -> status=%s, %s results%s' % (s, n,
          ' (accepted, BUG)' if s == 200 else ' (rejected, FIX)')))


def p9149():
    for name, shard, cid in [('test_shard_zero_r', 0, 1), ('test_shard_neg_r', -1, 2)]:
        http('DELETE', BASE + '/collections/' + name)
        s, b, t = http('PUT', BASE + '/collections/' + name,
                       {"vectors": {"size": 4, "distance": "Cosine"}, "shard_number": shard})
        emit('c%d' % cid, http_status=s, observation=(
            'shard_number=%s create -> status=%s%s' % (shard, s,
              ' (accepted, BUG)' if s == 200 else ' (rejected, FIX)')))


def p10120():
    col = 'test_count_bug_r'
    http('DELETE', BASE + '/collections/' + col)
    http('PUT', BASE + '/collections/' + col, {"vectors": {"size": 4, "distance": "Cosine"}})
    pts = [{"id": i, "vector": [0.1, 0.2, 0.3, 0.4], "payload": {"f": "x" if i % 2 else None}} for i in range(1, 21)]
    http('PUT', BASE + '/collections/' + col + '/points?wait=true', {"points": pts})
    # is_empty: exact=false 应与 exact=true 一致; bug = under-count
    s, b, _ = http('POST', BASE + '/collections/' + col + '/points/count',
                   {"exact": True, "filter": {"must": [{"is_empty": {"field": "f"}}]}})
    exact = (b or {}).get('result', {}).get('count')
    s2, b2, _ = http('POST', BASE + '/collections/' + col + '/points/count',
                     {"exact": False, "filter": {"must": [{"is_empty": {"field": "f"}}]}})
    approx = (b2 or {}).get('result', {}).get('count')
    emit('c1', http_status=s, exact_count=exact, approx_count=approx, observation=(
        'is_empty count: exact=%s approx=%s%s' % (exact, approx,
          ' (MISMATCH, BUG)' if exact != approx else ' (consistent, FIX)')))


def p9045():
    """Empty-vector upsert + wait=false panic probe. 独立容器上跑."""
    col = 'test_panic_r'
    http('DELETE', BASE + '/collections/' + col)
    http('PUT', BASE + '/collections/' + col, {"vectors": {"size": 4, "distance": "Cosine"}})
    http('PUT', BASE + '/collections/' + col + '/points?wait=true',
         {"points": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4]}]})
    crashed = False
    for i in range(10):
        s, b, t = http('PUT', BASE + '/collections/' + col + '/points?wait=false',
                       {"points": [{"id": 100 + i, "vector": []}]})
        if s is None:
            crashed = True
            break
        emit('c_iter%d' % i, http_status=s, observation='empty-vector wait=false upsert -> %s' % s)
    # crash 后服务是否还活着
    s, b, _ = http('GET', BASE + '/')
    emit('c_alive', http_status=s, observation='server alive check -> %s' % s)
    emit('c1', crashed=crashed, observation='panic after %d empty-vector upserts: %s' % (i, crashed))


if __name__ == '__main__':
    if not wait_ready(BASE + '/'):
        emit('setup', observation='server not ready')
        sys.exit(1)
    {9017: p9017, 9149: p9149, 10120: p10120, 9045: p9045}[NUM]()
    print('reprobe_qdrant %d done' % NUM)

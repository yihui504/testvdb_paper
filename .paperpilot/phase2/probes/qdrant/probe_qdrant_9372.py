"""probe for qdrant/qdrant#9372  Strict mode inconsistently validates zero values
version: 1.18.2 | gt: PENDING_SELF_LABELED | class: param_validation
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready

BASE = 'http://localhost:6333'

def main():
    if not wait_ready(BASE + '/'):
        emit('setup', observation='server not ready')
        return
    # c1 control: max_query_limit=0 correctly rejected
    s, b, t = http('PUT', BASE + '/collections/ctl',
                   {"vectors": {"size": 4, "distance": "Cosine"},
                    "strict_mode_config": {"enabled": True, "max_query_limit": 0}})
    emit('c1', http_status=s, observation=('max_query_limit=0 create -> status=%s (expect 422)' % s))

    # c2: filter_max_conditions=0 (the defect)
    s, b, t = http('PUT', BASE + '/collections/exp_a',
                   {"vectors": {"size": 4, "distance": "Cosine"},
                    "strict_mode_config": {"enabled": True, "filter_max_conditions": 0, "max_query_limit": 100}})
    s2 = 'BUG' if s == 200 else 'OK'
    # 尝试一次带 filter 的 scroll 观察是否 'Filter condition limit reached'
    ss, sb, st = http('POST', BASE + '/collections/exp_a/points/scroll',
                      {"filter": {"must": [{"key": "kw", "match": {"value": "x"}}]}, "limit": 1})
    emit('c2', http_status=s, observation=(
        'filter_max_conditions=0 create -> status=%s (%s); then filtered scroll -> status=%s body=%r' % (s, s2, ss, st)))

    # c3: upsert_max_batchsize=0 (the defect)
    s, b, t = http('PUT', BASE + '/collections/exp_b',
                   {"vectors": {"size": 4, "distance": "Cosine"},
                    "strict_mode_config": {"enabled": True, "upsert_max_batchsize": 0, "max_query_limit": 100}})
    s2 = 'BUG' if s == 200 else 'OK'
    us, ub, ut = http('PUT', BASE + '/collections/exp_b/points',
                      {"points": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4]}]})
    emit('c3', http_status=s, observation=(
        'upsert_max_batchsize=0 create -> status=%s (%s); then upsert -> status=%s body=%r' % (s, s2, us, ut)))
    print('probe_qdrant_9372 done')

if __name__ == '__main__':
    main()

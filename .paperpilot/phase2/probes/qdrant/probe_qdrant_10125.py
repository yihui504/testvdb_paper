"""probe for qdrant/qdrant#10125  count exact=false compound filter under-counts (independence assumption)
version: 1.18.3 | gt: PENDING_SELF_LABELED | class: semantics
"""
import os, sys, time, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready

BASE = 'http://localhost:6333'
COL = 'c'
N = 500
KWS = ['red', 'blue', 'green', 'yellow']

def count(exact, flt):
    return http('POST', BASE + '/collections/' + COL + '/points/count',
                {"exact": exact, "filter": flt})

def main():
    if not wait_ready(BASE + '/'):
        emit('setup', observation='server not ready')
        return
    http('DELETE', BASE + '/collections/' + COL)
    http('PUT', BASE + '/collections/' + COL,
         {"vectors": {"size": 2, "distance": "Cosine"}, "optimizer_config": {"indexing_threshold": 1}})
    r = random.Random(42)
    pts = [{"id": i + 1, "vector": [1.0, 0.0],
            "payload": {"kw": r.choice(KWS), "cat": r.choice(["x", "y"])}} for i in range(N)]
    http('PUT', BASE + '/collections/' + COL + '/points?wait=true', {"points": pts})
    http('PUT', BASE + '/collections/' + COL + '/index', {"field_name": "kw", "field_schema": "keyword"})
    http('PUT', BASE + '/collections/' + COL + '/index', {"field_name": "cat", "field_schema": "keyword"})
    time.sleep(3)

    # c1 control single-condition must kw=red (exact should equal approx)
    s, b, _ = count(False, {"must": [{"key": "kw", "match": {"value": "red"}}]})
    single = (b or {}).get('result', {}).get('count')
    emit('c1', http_status=s, observation=('control single kw=red exact=false -> %s (leaf estimator)' % single))

    # c2 same-field compound must kw=red AND must_not kw=blue (== red, should equal single)
    s, b, _ = count(False, {"must": [{"key": "kw", "match": {"value": "red"}}],
                            "must_not": [{"key": "kw", "match": {"value": "blue"}}]})
    c2 = (b or {}).get('result', {}).get('count')
    emit('c2', http_status=s, observation=(
        'compound kw=red AND NOT kw=blue exact=false -> %s vs single=%s (undercount=%+d, BUG if much lower)' % (
          c2, single, c2 - single)))

    # c3 cross-field compound must kw=red AND must cat=x
    s, b, _ = count(False, {"must": [{"key": "kw", "match": {"value": "red"}},
                                     {"key": "cat", "match": {"value": "x"}}]})
    c3 = (b or {}).get('result', {}).get('count')
    emit('c3', http_status=s, observation=('cross-field kw=red AND cat=x exact=false -> %s' % c3))
    print('probe_qdrant_10125 done')

if __name__ == '__main__':
    main()

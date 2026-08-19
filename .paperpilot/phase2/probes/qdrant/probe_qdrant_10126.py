"""probe for qdrant/qdrant#10126  count exact=false on geo_radius degenerates (fixed value / saturates)
version: 1.18.3 | gt: PENDING_SELF_LABELED | class: semantics
"""
import os, sys, time, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready

BASE = 'http://localhost:6333'
COL = 'c'
N = 1000

def count(exact, radius):
    return http('POST', BASE + '/collections/' + COL + '/points/count',
                {"exact": exact, "filter": {"must": [{"key": "loc", "geo_radius": {
                    "center": {"lat": 0, "lon": 0}, "radius": radius}}]}})

def main():
    if not wait_ready(BASE + '/'):
        emit('setup', observation='server not ready')
        return
    http('DELETE', BASE + '/collections/' + COL)
    http('PUT', BASE + '/collections/' + COL,
         {"vectors": {"size": 2, "distance": "Cosine"}, "optimizer_config": {"indexing_threshold": 1}})
    r = random.Random(42)
    pts = [{"id": i + 1, "vector": [1.0, 0.0],
            "payload": {"loc": {"lat": r.uniform(-89, 89), "lon": r.uniform(-179, 179)}}} for i in range(N)]
    http('PUT', BASE + '/collections/' + COL + '/points?wait=true', {"points": pts})
    http('PUT', BASE + '/collections/' + COL + '/index', {"field_name": "loc", "field_schema": "geo"})
    time.sleep(3)

    # c1 ground truth exact=true radius 2000km
    s, b, _ = count(True, 2000000)
    g = (b or {}).get('result', {}).get('count')
    emit('c1', http_status=s, observation=('count exact=true geo_radius 2000km -> %s (ground truth)' % g))

    # c2 defect: exact=false radius 2000km
    s, b, _ = count(False, 2000000)
    a = (b or {}).get('result', {}).get('count')
    emit('c2', http_status=s, observation=(
        'count exact=false geo_radius 2000km -> %s vs exact=%s (%+.0f%%%s)' % (
          a, g, (a - g) / float(g) * 100 if g else 0, ' collapse, BUG' if g and a > g * 1.5 else '')))

    # c3 exact=false radius 5000km vs 2000km (should differ, issue: same fixed value)
    s, b, _ = count(False, 5000000)
    c3 = (b or {}).get('result', {}).get('count')
    emit('c3', http_status=s, observation=('count exact=false geo_radius 5000km -> %s (vs 2000km=%s; same fixed value = BUG)' % (c3, a)))

    # c4 exact=false large radius 10000km (saturates to total)
    s, b, _ = count(False, 10000000)
    c4 = (b or {}).get('result', {}).get('count')
    emit('c4', http_status=s, observation=('count exact=false geo_radius 10000km -> %s (total=N=%d; saturates = BUG)' % (c4, N)))
    print('probe_qdrant_10126 done')

if __name__ == '__main__':
    main()

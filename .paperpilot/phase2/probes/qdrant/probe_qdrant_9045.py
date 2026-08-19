"""probe for qdrant/qdrant#9045  Empty vector [] upsert with wait=false can trigger server panic
version: 1.12.1 | gt: TP_FIXED_PR | class: crash
"""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready

BASE = 'http://localhost:6333'
COL = 'test'

def count():
    _, b, _ = http('GET', BASE + '/collections/' + COL)
    return (b or {}).get('result', {}).get('points_count')

def main():
    if not wait_ready(BASE + '/'):
        emit('setup', observation='server not ready')
        return
    http('DELETE', BASE + '/collections/' + COL)
    http('PUT', BASE + '/collections/' + COL, {"vectors": {"size": 4, "distance": "Cosine"}})

    # c1: control sync path
    s, b, t = http('PUT', BASE + '/collections/' + COL + '/points?wait=true',
                   {"points": [{"id": 1, "vector": []}]})
    emit('c1', http_status=s, observation=('sync empty-vector upsert -> status=%s, count=%s' % (s, count())))

    # c2: async path
    s, b, t = http('PUT', BASE + '/collections/' + COL + '/points',
                   {"points": [{"id": 2, "vector": []}]})
    emit('c2', http_status=s, resp_code=(b or {}).get('status.code'), observation=(
        'async empty-vector upsert -> status=%s count=%s' % (s, count())))

    # crash类: 确认 server 仍存活
    time.sleep(1)
    hs, hb, ht = http('GET', BASE + '/')
    emit('server_health', http_status=hs, observation=('GET / after crash attempt -> status=%s' % hs))
    print('probe_qdrant_9045 done')

if __name__ == '__main__':
    main()

"""probe for qdrant/qdrant#9421  POST /cluster/recover returns 500 in standalone -> should be 4xx
version: 1.18.2 | gt: TP_FIXED_PR | class: behavior
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready

BASE = 'http://localhost:6333'

def main():
    if not wait_ready(BASE + '/'):
        emit('setup', observation='server not ready')
        return
    _, cb, _ = http('GET', BASE + '/cluster')
    status = (cb or {}).get('result', {}).get('status')
    emit('setup', observation=('GET /cluster -> result.status=%s' % status))

    s, b, t = http('POST', BASE + '/cluster/recover')
    emit('c1', http_status=s, observation=(
        'cluster recover in standalone -> status=%s body=%r%s' % (
          s, t, ' (500 server error, BUG; should be 4xx)' if s == 500 else ' (4xx/other, OK)')))
    print('probe_qdrant_9421 done')

if __name__ == '__main__':
    main()

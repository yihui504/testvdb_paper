"""probe for milvus-io/milvus#47635  [Bug]: Search fails with Code 0 immediately after Collection.load() returns success
version: 2.3 | gt: TP_ACK_CLOSED_NOFIX | class: behavior
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready, milvus_client, milvus_drop, milvus_create, milvus_index

def main():
    wait_ready('http://localhost:19530/healthz')

    # RISK: v2.3 gRPC-era issue; harness pymilvus (newer) may be incompatible with v2.3 server.
    mc = milvus_client()
    # Reporter notes Standalone has low success rate; maximize hit chance with a
    # FRESH collection per attempt (first-load race window is widest) and no sleep.
    N = 20
    for attempt in range(N):
        name = 'test_47635_%d' % attempt
        milvus_drop(mc, name)
        try:
            mc.create_collection(name, dimension=4)
            mc.insert(name, [{'id': 0, 'vector': [0.1, 0.2, 0.3, 0.4]}])
            mc.flush(name)
            milvus_index(mc, name, {'field_name': 'vector', 'index_type': 'FLAT', 'metric_type': 'L2'})
            mc.load_collection(name)
            # no sleep: search immediately after load() returns to hit the race
            try:
                res = mc.search(name, [[0.1, 0.2, 0.3, 0.4]], anns_field='vector', limit=1,
                                search_params={'metric_type': 'L2'})
                emit('c1', attempt=attempt, outcome='ok', result_count=len(res[0]),
                     observation='attempt %d search ok (count=%d)' % (attempt, len(res[0])))
            except Exception as e:
                msg = str(e)
                code0 = 'code=0' in msg or 'code = 0' in msg
                notloaded = 'not loaded' in msg
                emit('c1', attempt=attempt, outcome='exception', exception=msg,
                     code_0=code0, not_loaded=notloaded,
                     observation='attempt %d search raised (code0=%s notloaded=%s): %s' % (attempt, code0, notloaded, msg))
        except Exception as e:
            emit('c1', attempt=attempt, outcome='setup_exception', exception=str(e),
                 observation='setup failed on attempt %d: %s' % (attempt, e))
    for attempt in range(N):
        milvus_drop(mc, 'test_47635_%d' % attempt)


    print('probe_milvus_47635 done')

if __name__ == '__main__':
    main()

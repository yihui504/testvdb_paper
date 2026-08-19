"""probe for milvus-io/milvus#47636  [Bug]: Expr parser returns code=0 (Success) and leaks internal lexer errors
version: 2.3 | gt: STALE_NO_FIX | class: behavior
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready, milvus_client, milvus_drop, milvus_create, milvus_index

def main():
    wait_ready('http://localhost:19530/healthz')

    # RISK: v2.3 gRPC-era issue, STALE_NO_FIX; behavior may differ on harness image.
    mc = milvus_client()
    milvus_drop(mc, 'test_47636')
    mc.create_collection('test_47636', dimension=4)
    try:
        mc.insert('test_47636', [{'id': 'a1', 'vector': [0.1, 0.2, 0.3, 0.4]}])
        mc.flush('test_47636')
        milvus_index(mc, 'test_47636', {'field_name': 'vector', 'index_type': 'FLAT', 'metric_type': 'L2'})
        mc.load_collection('test_47636')
    except Exception as e:
        emit('setup', observation='setup failed: %s' % e)
        print('probe_milvus_47636 done')
        return
    try:
        # invalid token '===' should surface a non-success code, not expose lexer internals
        r = mc.query('test_47636', filter="tag === 'x'", output_fields=['id'])
        emit('c1', outcome='ok', observation='invalid expr tag === accepted without error')
    except Exception as e:
        emit('c1', outcome='exception', exception=str(e),
             observation='invalid expr tag === raised MilvusException: %s' % e)
    milvus_drop(mc, 'test_47636')


    print('probe_milvus_47636 done')

if __name__ == '__main__':
    main()

"""probe for milvus-io/milvus#47752  [Bug]: Index parameter ef validation missing - accepts ef=0
version: 2.6.10 | gt: TP_ACK_CLOSED_NOFIX | class: param_validation
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready, milvus_client, milvus_drop, milvus_create, milvus_index

def main():
    wait_ready('http://localhost:19530/healthz')

    mc = milvus_client()
    milvus_drop(mc, 'test_47752')
    mc.create_collection('test_47752', dimension=128, metric_type='L2')
    mc.insert('test_47752', [{'id': i, 'vector': [0.1] * 128} for i in range(10)])
    milvus_index(mc, 'test_47752', {'field_name': 'vector', 'index_type': 'HNSW', 'metric_type': 'L2',
                                             'params': {'M': 16, 'efConstruction': 100}})
    mc.load_collection('test_47752')
    try:
        r = mc.search('test_47752', [[0.1] * 128], anns_field='vector', limit=10,
                      search_params={'metric_type': 'L2', 'ef': 0})
        emit('c1', outcome='ok', accepted=True, result_count=len(r[0]),
             observation='HNSW search ef=0 accepted (defect), returned %d results' % len(r[0]))
    except Exception as e:
        emit('c1', outcome='exception', accepted=False, exception=str(e),
             observation='HNSW search ef=0 rejected: %s' % e)


    print('probe_milvus_47752 done')

if __name__ == '__main__':
    main()

"""probe for milvus-io/milvus#50194  [Bug] Concurrent delete and search returns stale/deleted data
version: 2.6.16 | gt: BY_DESIGN | class: behavior
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready, milvus_client, milvus_drop, milvus_create, milvus_index

BASE = 'http://localhost:19530'


def _drop(name):
    http('POST', BASE + '/v2/vectordb/collections/drop', {'collectionName': name, 'dbName': 'default'})


def _create(name, **kw):
    p = {'collectionName': name}
    p.update(kw)
    return http('POST', BASE + '/v2/vectordb/collections/create', p)


def _insert(name, data, **kw):
    p = {'collectionName': name, 'data': data}
    p.update(kw)
    return http('POST', BASE + '/v2/vectordb/entities/insert', p)


def _upsert(name, data, **kw):
    p = {'collectionName': name, 'data': data}
    p.update(kw)
    return http('POST', BASE + '/v2/vectordb/entities/upsert', p)


def _search(name, data, **kw):
    p = {'collectionName': name, 'data': data}
    p.update(kw)
    return http('POST', BASE + '/v2/vectordb/entities/search', p)


def _query(name, **kw):
    p = {'collectionName': name}
    p.update(kw)
    return http('POST', BASE + '/v2/vectordb/entities/query', p)


def _describe(name):
    return http('POST', BASE + '/v2/vectordb/collections/describe', {'collectionName': name, 'dbName': 'default'})


def _load(name):
    return http('POST', BASE + '/v2/vectordb/collections/load', {'collectionName': name, 'dbName': 'default'})


def _idx_create(name, index_params):
    return http('POST', BASE + '/v2/vectordb/indexes/create',
                {'collectionName': name, 'indexParams': index_params})


def _emit_case(case_id, resp, note):
    s, b, t = resp
    code = (b or {}).get('code') if isinstance(b, dict) else None
    try:
        raw = str(b or t)[:400]
    except Exception:
        raw = str(t)[:400]
    emit(case_id, http_status=s, resp_code=code, raw=raw,
         observation=note + ' (http=%s code=%s)' % (s, code))

def main():
    wait_ready('http://localhost:19530/healthz')

    import threading
    _drop('test_stale_data')
    _create('test_stale_data', dimension=4, metricType='L2')
    _idx_create('test_stale_data', [{'fieldName': 'vector', 'metricType': 'L2',
                                     'indexType': 'HNSW', 'params': {'M': 16, 'efConstruction': 128}}])
    _insert('test_stale_data', [{'id': i, 'vector': [0.1, 0.2, 0.3, 0.4]} for i in range(10)])
    _load('test_stale_data')
    s_before, bd, t = _search('test_stale_data', [[0.1, 0.2, 0.3, 0.4]], limit=10,
                              outputFields=['id'])
    emit('c1_before', http_status=s_before, observation='search before delete: ' + str(bd))
    search_ids = {}
    def deleter():
        http('POST', BASE + '/v2/vectordb/entities/delete',
             {'collectionName': 'test_stale_data', 'filter': 'id in [1,2,3,4,5]', 'dbName': 'default'})
    def searcher():
        s, bd, t = _search('test_stale_data', [[0.1, 0.2, 0.3, 0.4]], limit=10, outputFields=['id'])
        ids = [h.get('id') for h in (bd or {}).get('data', [])] if isinstance(bd, dict) else []
        search_ids['post'] = ids
    ths = [threading.Thread(target=deleter), threading.Thread(target=searcher)]
    for th in ths:
        th.start()
    for th in ths:
        th.join()
    s, bd, t = _search('test_stale_data', [[0.1, 0.2, 0.3, 0.4]], limit=10, outputFields=['id'])
    ids_after = [h.get('id') for h in (bd or {}).get('data', [])] if isinstance(bd, dict) else []
    emit('c1', http_status=s, ids_after_concurrent=search_ids.get('post'),
         ids_after_second=ids_after,
         observation='stale-data check: deleted ids 1-5 appearing after delete is defect, got %s' % ids_after)


    print('probe_milvus_50194 done')

if __name__ == '__main__':
    main()

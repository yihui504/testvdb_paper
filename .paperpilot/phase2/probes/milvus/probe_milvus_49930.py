"""probe for milvus-io/milvus#49930  [Bug]: REST API v2 accepts invalid searchParams (ef=0/-1 for HNSW, nprobe=0/-1 for IVF_FLAT) without validation
version: 2.6.16 | gt: TP_ACK_OPEN | class: param_validation
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

    _drop('test_hnsw_ef')
    _drop('test_ivf_nprobe')
    _create('test_hnsw_ef', dimension=4, metricType='L2')
    _idx_create('test_hnsw_ef', [{'fieldName': 'vector', 'metricType': 'L2',
                                  'indexType': 'HNSW',
                                  'params': {'M': 16, 'efConstruction': 128}}])
    _insert('test_hnsw_ef', [{'id': 1, 'vector': [0.1, 0.2, 0.3, 0.4]}])
    _load('test_hnsw_ef')
    _create('test_ivf_nprobe', dimension=4, metricType='L2')
    _idx_create('test_ivf_nprobe', [{'fieldName': 'vector', 'metricType': 'L2',
                                     'indexType': 'IVF_FLAT', 'params': {'nlist': 128}}])
    _insert('test_ivf_nprobe', [{'id': i, 'vector': [0.1, 0.2, 0.3, 0.4]} for i in range(2)])
    _load('test_ivf_nprobe')
    s, bd, t = _search('test_hnsw_ef', [[0.1, 0.2, 0.3, 0.4]], limit=5, searchParams={'ef': -1})
    _emit_case('c1', (s, bd, t), 'HNSW search ef=-1; defect if code 0 with results')
    s, bd, t = _search('test_hnsw_ef', [[0.1, 0.2, 0.3, 0.4]], limit=5, searchParams={'ef': 0})
    _emit_case('c2', (s, bd, t), 'HNSW search ef=0; defect if code 0 with results')
    s, bd, t = _search('test_ivf_nprobe', [[0.1, 0.2, 0.3, 0.4]], limit=5,
                       searchParams={'nprobe': 0})
    _emit_case('c3', (s, bd, t), 'IVF_FLAT search nprobe=0; defect if code 0 with results')


    print('probe_milvus_49930 done')

if __name__ == '__main__':
    main()

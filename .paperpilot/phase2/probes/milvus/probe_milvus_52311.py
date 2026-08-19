"""probe for milvus-io/milvus#52311  [Bug]: REST API v2 silently accepts `group_by_field` on vector fields (gRPC rejects "unsupported data type")
version: 3.0.0 | gt: TP_FIXED_PR | class: semantics
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

    _drop('test_gv')
    _create('test_gv', dimension=4)
    _insert('test_gv', [{'id': i, 'vector': [0.1, 0.2, 0.3, 0.4]} for i in range(10)])
    _load('test_gv')
    s, bd, t = _search('test_gv', [[0.5, 0.5, 0.5, 0.5]], limit=5,
                       groupParams={'groupByField': 'vector', 'groupSize': 1})
    _emit_case('c1', (s, bd, t),
               'search groupByField=vector; defect if accepted and grouping silently ignored')
    mc = milvus_client()
    try:
        r = mc.search('test_gv', [[0.5, 0.5, 0.5, 0.5]], anns_field='vector', limit=5,
                      search_params={'metric_type': 'L2', 'group_by_field': 'vector',
                                     'group_size': 1})
        emit('c1_grpc', observation='gRPC group_by vector accepted: ' + str(r))
    except Exception as e:
        emit('c1_grpc', exception=str(e),
             observation='gRPC group_by vector rejected (unsupported data type): %s' % e)


    print('probe_milvus_52311 done')

if __name__ == '__main__':
    main()

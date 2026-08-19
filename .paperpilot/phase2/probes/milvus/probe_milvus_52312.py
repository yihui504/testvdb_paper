"""probe for milvus-io/milvus#52312  [Bug]: REST API v2 `entities/upsert` accepts string numbers for Int64 primary key (gRPC rejects)
version: 3.0.0 | gt: TP_DUP_TRACKED | class: type_coercion
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

    _drop('test_upsert_pk')
    _create('test_upsert_pk', dimension=4)
    _insert('test_upsert_pk', [{'id': 100, 'vector': [0.1, 0.2, 0.3, 0.4]}])
    s, bd, t = _upsert('test_upsert_pk', [{'id': '100', 'vector': [0.9, 0.9, 0.9, 0.9]}])
    _emit_case('c1', (s, bd, t),
               'REST upsert string PK 100; defect if accepted overwites existing record')
    s, bd, t = _query('test_upsert_pk', filter='id==100', outputFields=['id', 'vector'])
    emit('c1_q', http_status=s, observation='query id==100 after string-PK upsert: ' + str(bd))
    mc = milvus_client()
    try:
        mc.upsert('test_upsert_pk', [{'id': '100', 'vector': [0.2, 0.2, 0.2, 0.2]}])
        emit('c1_grpc', observation='gRPC upsert string PK accepted (unexpected)')
    except Exception as e:
        emit('c1_grpc', exception=str(e),
             observation='gRPC upsert string PK rejected (expect DataNotMatch id should be int64): %s' % e)


    print('probe_milvus_52312 done')

if __name__ == '__main__':
    main()

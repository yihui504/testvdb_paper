"""probe for milvus-io/milvus#52308  [Bug]: REST API v2 `entities/insert` accepts string numbers for Int64 primary key (type coercion gap; gRPC rejects)
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

    _drop('test_pk')
    _create('test_pk', schema={
        'autoId': False, 'enableDynamicField': False,
        'fields': [{'fieldName': 'id', 'dataType': 'Int64', 'isPrimary': True},
                   {'fieldName': 'vector', 'dataType': 'FloatVector',
                    'elementTypeParams': {'dim': 4}}]})
    _idx_create('test_pk', [{'fieldName': 'vector', 'metricType': 'COSINE',
                             'indexType': 'AUTOINDEX'}])
    s, bd, t = _insert('test_pk', [{'id': '123', 'vector': [0.1, 0.2, 0.3, 0.4]}])
    _emit_case('c1', (s, bd, t), 'REST insert string PK 123; defect if accepted')
    s, bd, t = _query('test_pk', filter='id==123', outputFields=['id'])
    emit('c1_q', http_status=s, observation='query id==123: ' + str(bd))
    mc = milvus_client()
    try:
        mc.insert('test_pk', [{'id': '123', 'vector': [0.1, 0.2, 0.3, 0.4]}])
        emit('c1_grpc', observation='gRPC insert string PK accepted (unexpected)')
    except Exception as e:
        emit('c1_grpc', exception=str(e), observation='gRPC insert string PK rejected: %s' % e)
    s, bd, t = _insert('test_pk', [{'id': 'abc', 'vector': [0.5, 0.5, 0.5, 0.5]}])
    _emit_case('c2', (s, bd, t), 'REST insert non-numeric string PK abc; report coerced value')
    s, bd, t = _query('test_pk', filter='id==0', outputFields=['id'])
    emit('c2_q', http_status=s, observation='query id==0 (abc->0?): ' + str(bd))


    print('probe_milvus_52308 done')

if __name__ == '__main__':
    main()

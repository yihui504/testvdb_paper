"""probe for milvus-io/milvus#52313  [Bug]: entities/insert JSON field — plain strings stored in inconsistent formats across REST/gRPC; written values unreadable via gRPC (round-trip failure)
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

    _drop('test_json')
    _create('test_json', schema={
        'autoId': False, 'enableDynamicField': False,
        'fields': [{'fieldName': 'id', 'dataType': 'Int64', 'isPrimary': True},
                   {'fieldName': 'vector', 'dataType': 'FloatVector',
                    'elementTypeParams': {'dim': 4}},
                   {'fieldName': 'meta', 'dataType': 'JSON'}]})
    _idx_create('test_json', [{'fieldName': 'vector', 'metricType': 'COSINE',
                               'indexType': 'AUTOINDEX'}])
    _load('test_json')  # v3.0.0 REST entities/insert needs the collection loaded
    s, bd, t = _insert('test_json', [{'id': 100, 'vector': [0.1, 0.2, 0.3, 0.4], 'meta': 'plain_string'}])
    _emit_case('c1', (s, bd, t),
               'REST insert plain-string into JSON field; defect if accepted (asymmetric round-trip)')
    mc = milvus_client()
    try:
        mc.insert('test_json', [{'id': 101, 'vector': [0.1, 0.2, 0.3, 0.4], 'meta': 'plain_string'}])
        emit('c2', observation='gRPC insert same plain string accepted')
    except Exception as e:
        emit('c2', exception=str(e), observation='gRPC insert plain string: %s' % e)
    s, bd, t = _query('test_json', filter='id in [100,101]', outputFields=['meta'])
    emit('c_q', http_status=s, observation='query meta both ids: ' + str(bd))
    try:
        g = mc.get('test_json', ids=[100, 101], output_fields=['meta'])
        emit('c_grpc_get', observation='gRPC get ids 100,101: ' + str(g))
    except Exception as e:
        emit('c_grpc_get', exception=str(e),
             observation='gRPC get failed (REST-written value unreadable): %s' % e)


    print('probe_milvus_52313 done')

if __name__ == '__main__':
    main()

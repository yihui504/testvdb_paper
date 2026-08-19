"""probe for milvus-io/milvus#52307  [Bug]: entities/upsert JSON field — plain string overwrites valid JSON; written value unreadable via gRPC; REST/gRPC store inconsistent formats
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
    _insert('test_json', [{'id': 0, 'vector': [0.1, 0.2, 0.3, 0.4], 'meta': {'important': 'data'}}])
    s, bd, t = _upsert('test_json', [{'id': 0, 'vector': [0.9, 0.9, 0.9, 0.9], 'meta': 'invalid_json'}])
    _emit_case('c1', (s, bd, t),
               'REST upsert bare string into JSON field; defect if accepted overwrites JSON')
    s, bd, t = _query('test_json', filter='id in [0,1]', outputFields=['meta'])
    emit('c1_q', http_status=s, observation='query meta after REST upsert: ' + str(bd))
    mc = milvus_client()
    try:
        g = mc.get('test_json', ids=[0], output_fields=['meta'])
        emit('c1_grpc_get', observation='gRPC get id=0 meta: ' + str(g))
    except Exception as e:
        emit('c1_grpc_get', exception=str(e),
             observation='gRPC get id=0 failed (round-trip failure): %s' % e)
    try:
        mc.upsert('test_json', [{'id': 1, 'vector': [0.8] * 4, 'meta': 'grpc_plain_str'}])
        s, bd, t = _query('test_json', filter='id==1', outputFields=['meta'])
        emit('c1b', http_status=s, observation='after gRPC upsert plain str query meta: ' + str(bd))
    except Exception as e:
        emit('c1b', exception=str(e), observation='gRPC upsert plain str: %s' % e)


    print('probe_milvus_52307 done')

if __name__ == '__main__':
    main()

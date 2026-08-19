"""probe for milvus-io/milvus#52315  [Bug]: REST API v2 `entities/insert` accepts string-encoded vector values (gRPC rejects)
version: 3.0.0 | gt: TP_FIXED_PR | class: type_coercion
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

    _drop('test_vec_str')
    _create('test_vec_str', dimension=4)
    s, bd, t = _insert('test_vec_str', [{'id': 0, 'vector': '[0.1,0.2,0.3,0.4]'}])
    _emit_case('c1', (s, bd, t),
               'REST insert string-encoded vector; defect if accepted and parsed to float vector')
    s, bd, t = _search('test_vec_str', [[0.1, 0.2, 0.3, 0.4]], annsField='vector', limit=5,
                       outputFields=['id'])
    emit('c1_s', http_status=s, observation='search after string-vector insert: ' + str(bd))
    mc = milvus_client()
    try:
        mc.insert('test_vec_str', [{'id': 1, 'vector': '[0.1,0.2,0.3,0.4]'}])
        emit('c1_grpc', observation='gRPC insert string vector accepted (unexpected)')
    except Exception as e:
        emit('c1_grpc', exception=str(e),
             observation='gRPC insert string vector rejected (expected should be float_vector): %s' % e)


    print('probe_milvus_52315 done')

if __name__ == '__main__':
    main()

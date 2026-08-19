"""probe for milvus-io/milvus#49844  [Bug]: REST API v2 query accepts null/missing filter and silently returns all entities
version: 2.6.16 | gt: FP_BY_DESIGN | class: semantics
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

    _drop('test_coll')
    _create('test_coll', dimension=4)
    _insert('test_coll', [{'id': 1, 'vector': [0.1, 0.2, 0.3, 0.4]},
                          {'id': 2, 'vector': [0.2, 0.2, 0.3, 0.4]}])
    s, bd, t = http('POST', BASE + '/v2/vectordb/entities/query',
                    {'collectionName': 'test_coll', 'filter': None, 'outputFields': ['id']})
    _emit_case('c1', (s, bd, t),
               'query filter=null; claim filter required -> should error, defect if all rows code 0')
    s, bd, t = http('POST', BASE + '/v2/vectordb/entities/query',
                    {'collectionName': 'test_coll', 'outputFields': ['id']})
    _emit_case('c2', (s, bd, t), 'query filter omitted; defect if all rows returned code 0')
    s, bd, t = http('POST', BASE + '/v2/vectordb/entities/query',
                    {'collectionName': 'test_coll', 'filter': '', 'outputFields': ['id']})
    _emit_case('c3', (s, bd, t), 'control filter empty string documented query-all; expect success')


    print('probe_milvus_49844 done')

if __name__ == '__main__':
    main()

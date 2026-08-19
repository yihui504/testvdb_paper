"""probe for milvus-io/milvus#49849  [Bug]: REST API v2 insert returns insertCount=1 for duplicate primary key (upsert semantics)
version: 2.6.16 | gt: SELF_CLOSED | class: semantics
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

    _drop('test_coll_sem')
    _create('test_coll_sem', dimension=4, metricType='L2')
    _insert('test_coll_sem', [{'id': 1, 'vector': [0.1, 0.2, 0.3, 0.4]}])
    s, bd, t = _insert('test_coll_sem', [{'id': 1, 'vector': [0.9, 0.8, 0.7, 0.6]}])
    _emit_case('c1', (s, bd, t),
               'duplicate-PK insert (overwrite) reports insertCount; defect if says 1 for overwrite')
    s, bd, t = _query('test_coll_sem', filter='id==1', outputFields=['id', 'vector'])
    emit('c1_rb', http_status=s, observation='query id==1 after overwrite: ' + str(bd))


    print('probe_milvus_49849 done')

if __name__ == '__main__':
    main()

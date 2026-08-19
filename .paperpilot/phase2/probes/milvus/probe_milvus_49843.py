"""probe for milvus-io/milvus#49843  [Bug]: REST API v2 silently drops negative collection.ttl.seconds on collection create
version: 2.6.16 | gt: TP_FIXED_PR | class: semantics
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

    _drop('test_ttl_neg')
    s, bd, t = _create('test_ttl_neg', dimension=4, metricType='L2',
                       properties={'collection.ttl.seconds': -100})
    _emit_case('c1', (s, bd, t),
               'create with negative TTL; defect if code 0 while TTL silently dropped')
    s, bd, t = _describe('test_ttl_neg')
    emit('c1_rb', http_status=s, resp_code=(bd or {}).get('code'),
         describe=(bd or {}).get('data') if isinstance(bd, dict) else None,
         observation='describe after negative-TTL create: check collection.ttl.seconds presence')
    s, bd, t = http('POST', BASE + '/v2/vectordb/collections/alter_properties',
                    {'collectionName': 'test_ttl_neg',
                     'properties': {'collection.ttl.seconds': -100}})
    _emit_case('c2', (s, bd, t),
               'control alter_properties negative TTL; expected range error code 1100')


    print('probe_milvus_49843 done')

if __name__ == '__main__':
    main()

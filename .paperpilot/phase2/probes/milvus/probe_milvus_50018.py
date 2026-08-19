"""probe for milvus-io/milvus#50018  [Bug]: REST API v2 aliases/list accepts empty collectionName while other endpoints properly reject it
version: 2.6.16 | gt: TP_ACK_CLOSED_NOFIX | class: param_validation
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

    _drop('test_aliases')
    _create('test_aliases', dimension=4, metricType='L2')
    http('POST', BASE + '/v2/vectordb/aliases/create',
         {'collectionName': 'test_aliases', 'alias': 'alias_50018', 'dbName': 'default'})
    s, bd, t = http('POST', BASE + '/v2/vectordb/aliases/list', {'collectionName': '', 'dbName': 'default'})
    _emit_case('c1', (s, bd, t),
               'aliases/list collectionName empty; defect if code 0 instead of 1802 required error')
    s, bd, t = http('POST', BASE + '/v2/vectordb/collections/describe',
                    {'collectionName': '', 'dbName': 'default'})
    _emit_case('c2', (s, bd, t),
               'control collections/describe empty name; expect code 1802 Field validatation failed')


    print('probe_milvus_50018 done')

if __name__ == '__main__':
    main()

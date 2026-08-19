"""probe for milvus-io/milvus#49850  [Bug]: REST API v2 describe indexes requires indexName, cannot list all indexes
version: 2.6.16 | gt: SELF_CLOSED | class: doc_mismatch
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

    _drop('test_idx')
    _create('test_idx', dimension=4)
    _idx_create('test_idx', [{'fieldName': 'vector', 'metricType': 'L2', 'indexType': 'AUTOINDEX'}])
    s, bd, t = http('POST', BASE + '/v2/vectordb/indexes/describe', {'collectionName': 'test_idx'})
    _emit_case('c1', (s, bd, t),
               'describe indexes without indexName; claim cannot list all (missing required IndexName)')
    s, bd, t = http('POST', BASE + '/v2/vectordb/indexes/describe',
                    {'collectionName': 'test_idx', 'indexName': 'vector'})
    _emit_case('c2', (s, bd, t), 'control describe with indexName; expect code 0')


    print('probe_milvus_49850 done')

if __name__ == '__main__':
    main()

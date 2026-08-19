"""probe for milvus-io/milvus#49928  [Bug]: Default proxy.maxDimension=32768 is too permissive, potential DoS risk via high-dimensional collection creation
version: 2.6.16 | gt: BY_DESIGN | class: behavior
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

    _drop('test_large_dim')
    _drop('test_large_dim2')
    s, bd, t = _create('test_large_dim', schema={
        'autoID': False, 'enableDynamicField': True,
        'fields': [{'fieldName': 'id', 'dataType': 'Int64', 'isPrimary': True},
                   {'fieldName': 'vector', 'dataType': 'FloatVector',
                    'elementTypeParams': {'dim': 32768}}]})
    _emit_case('c1', (s, bd, t),
               'create dim=32768; defect if accepted (default max too high, DoS risk)')
    s, bd, t = _create('test_large_dim2', schema={
        'autoID': False, 'enableDynamicField': True,
        'fields': [{'fieldName': 'id', 'dataType': 'Int64', 'isPrimary': True},
                   {'fieldName': 'vector', 'dataType': 'FloatVector',
                    'elementTypeParams': {'dim': 32769}}]})
    _emit_case('c2', (s, bd, t),
               'control dim=32769; expect invalid dimension in range 2..32768')


    print('probe_milvus_49928 done')

if __name__ == '__main__':
    main()

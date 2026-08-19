"""probe for milvus-io/milvus#50355  [Bug]: Upsert fails on autoID=true collections despite documentation claiming support
version: 2.6.17 | gt: TP_FIXED_PR | class: behavior
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

    _drop('test_upsert_autoid')
    _create('test_upsert_autoid', dimension=4, metricType='L2', autoID=True,
            schema={'autoID': True, 'primaryFieldName': 'id',
                    'fields': [{'fieldName': 'id', 'dataType': 'Int64', 'isPrimary': True},
                               {'fieldName': 'vector', 'dataType': 'FloatVector',
                                'elementTypeParams': {'dim': 4}}]})
    s, bd, t = _upsert('test_upsert_autoid', [{'vector': [1.0, 2.0, 3.0, 4.0], 'color': 'red'}])
    _emit_case('c1', (s, bd, t),
               'upsert without PK on autoID collection; claim should auto-gen id but fails code 1100')
    s, bd, t = _insert('test_upsert_autoid', [{'vector': [5.0, 6.0, 7.0, 8.0], 'color': 'blue'}])
    _emit_case('c2', (s, bd, t), 'control insert without PK succeeds (proves autoID works)')


    print('probe_milvus_50355 done')

if __name__ == '__main__':
    main()

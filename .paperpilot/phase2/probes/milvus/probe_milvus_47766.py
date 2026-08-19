"""probe for milvus-io/milvus#47766  [Bug]: Data type validation missing - accepts integer into string field
version: 2.6.10 | gt: TP_ACK_CLOSED_NOFIX | class: type_coercion
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

    _drop('test_47766')
    _create('test_47766', dimension=4)
    _insert('test_47766', [{'id': 1, 'vector': [0.1, 0.2, 0.3, 0.4], 'text_field': 'hello'}])
    s, bd, t = _insert('test_47766', [{'id': 2, 'vector': [0.2, 0.2, 0.3, 0.4],
                                       'text_field': 12345}])
    _emit_case('c1', (s, bd, t),
               'insert int into established VARCHAR dynamic field; defect if accepted (type mismatch)')
    s, bd, t = _query('test_47766', filter='id in [1,2]', outputFields=['text_field'])
    emit('c1_q', http_status=s, observation='query both text_field values: ' + str(bd))


    print('probe_milvus_47766 done')

if __name__ == '__main__':
    main()

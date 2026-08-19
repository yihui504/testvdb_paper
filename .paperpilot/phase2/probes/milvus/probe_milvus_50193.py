"""probe for milvus-io/milvus#50193  [Bug] get_stats returns rowCount=0 after successful insert and load (v2.6.16, regression from #30663)
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

    _drop('test_rowcount')
    _create('test_rowcount', dimension=4)
    _insert('test_rowcount', [{'id': i, 'value': i, 'vector': [0.1, 0.2, 0.3, 0.4]}
                              for i in range(5)])
    _load('test_rowcount')
    s, bd, t = http('POST', BASE + '/v2/vectordb/collections/get_stats',
                    {'collectionName': 'test_rowcount'})
    _emit_case('c1', (s, bd, t),
               'get_stats after insert+load; defect if rowCount=0 while query sees 5 rows')
    s, bd, t = _query('test_rowcount', filter='id>=0', outputFields=['id'])
    emit('c1_q', http_status=s, observation='query row count result: ' + str(bd))


    print('probe_milvus_50193 done')

if __name__ == '__main__':
    main()

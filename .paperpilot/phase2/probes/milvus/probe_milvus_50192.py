"""probe for milvus-io/milvus#50192  [Bug] Concurrent rename and create with same target name both succeed, causing state violation
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

    import threading
    _drop('test_rename_src')
    _drop('test_rename_dst')
    _create('test_rename_src', dimension=4, metricType='L2')
    _insert('test_rename_src', [{'id': 1, 'vector': [0.1, 0.2, 0.3, 0.4]}])
    results = {}
    def rename():
        s, bd, t = http('POST', BASE + '/v2/vectordb/collections/rename',
                        {'collectionName': 'test_rename_src', 'newCollectionName': 'test_rename_dst',
                         'dbName': 'default'})
        results['rename'] = (s, (bd or {}).get('code') if isinstance(bd, dict) else None)
    def create_conflict():
        s, bd, t = http('POST', BASE + '/v2/vectordb/collections/create',
                        {'collectionName': 'test_rename_dst', 'dimension': 4, 'metricType': 'L2'})
        results['create'] = (s, (bd or {}).get('code') if isinstance(bd, dict) else None)
    ths = [threading.Thread(target=rename), threading.Thread(target=create_conflict)]
    for th in ths:
        th.start()
    for th in ths:
        th.join()
    emit('c1', rename_code=results.get('rename'), create_code=results.get('create'),
         observation='concurrent rename->dst and create(dst); defect if BOTH succeed (state violation): %s' % results)


    print('probe_milvus_50192 done')

if __name__ == '__main__':
    main()

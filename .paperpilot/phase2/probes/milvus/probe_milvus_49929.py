"""probe for milvus-io/milvus#49929  [Bug]: REST API and PyMilvus SDK have inconsistent default index creation behavior
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

    _drop('test_rest_idx')
    _drop('test_sdk_idx')
    _create('test_rest_idx')  # collection without indexParams (REST leaves no index)
    s, bd, t = _idx_create('test_rest_idx',
                           [{'fieldName': 'vector', 'metricType': 'L2', 'indexType': 'IVF_FLAT'}])
    _emit_case('c1', (s, bd, t), 'REST create_index on bare collection; expect code 0 success')
    # SDK quick-create auto-makes AUTOINDEX, then create_index should fail (divergence)
    mc = milvus_client()
    milvus_drop(mc, 'test_sdk_idx')
    try:
        mc.create_collection('test_sdk_idx', dimension=4, metric_type='L2')
        try:
            idx = milvus_index(mc, 'test_sdk_idx', {'field_name': 'vector', 'index_type': 'AUTOINDEX',
                                                             'metric_type': 'L2'})
            emit('c2', observation='SDK create_index succeeded (no divergence): ' + str(idx))
        except Exception as e:
            emit('c2', exception=str(e),
                 observation='SDK create_index failed after quick-create (AUTOINDEX already exists): %s' % e)
    except Exception as e:
        emit('c2', exception=str(e), observation='SDK create_collection failed: %s' % e)


    print('probe_milvus_49929 done')

if __name__ == '__main__':
    main()

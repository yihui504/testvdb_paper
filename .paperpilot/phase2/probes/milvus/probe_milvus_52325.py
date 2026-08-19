"""probe for milvus-io/milvus#52325  [Bug]: REST v2 entities/search silently ignores strictGroupSize
version: 3.0.0 | gt: TP_FIXED_PR | class: semantics
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

def _py_create(mc, name, fields, dim=4):
    milvus_drop(mc, name)
    from pymilvus import DataType
    DT = {'INT64': DataType.INT64, 'FLOAT_VECTOR': DataType.FLOAT_VECTOR,
          'JSON': DataType.JSON, 'VARCHAR': DataType.VARCHAR, 'BOOL': DataType.BOOL,
          'DOUBLE': DataType.DOUBLE, 'INT16': DataType.INT16, 'INT32': DataType.INT32}
    schema = mc.create_schema(auto_id=False, enable_dynamic_field=False)
    first_scalar = True
    for fname, dtype, maxlen, nullable in fields:
        if dtype == 'FLOAT_VECTOR':
            schema.add_field(fname, DT[dtype], dim=dim)
        else:
            kw = {}
            if first_scalar:
                kw['is_primary'] = True
                first_scalar = False
            if maxlen:
                kw['max_length'] = maxlen
            if nullable:
                kw['nullable'] = True
            schema.add_field(fname, DT[dtype], **kw)
    mc.create_collection(name, schema=schema, consistency_level='Strong')

def main():
    wait_ready('http://localhost:19530/healthz')

    mc = milvus_client()
    milvus_drop(mc, 'gs_demo')
    _py_create(mc, 'gs_demo', [('id', 'INT64', 0, False), ('vector', 'FLOAT_VECTOR', 0, False),
                                ('cat', 'INT64', 0, False)])
    rows = [{'id': i, 'vector': [0.1 + i * 0.01, 0.2, 0.3, 0.4], 'cat': i % 5} for i in range(15)]
    mc.insert('gs_demo', rows)
    milvus_index(mc, 'gs_demo', {'field_name': 'vector', 'index_type': 'AUTOINDEX', 'metric_type': 'COSINE'})
    mc.load_collection('gs_demo')
    s, bd, t = _search('gs_demo', [[0.5, 0.5, 0.5, 0.5]], limit=15,
                       groupParams={'groupByField': 'cat', 'groupSize': 2,
                                    'strictGroupSize': True},
                       outputFields=['cat'])
    n = len((bd or {}).get('data', [])) if isinstance(bd, dict) else -1
    _emit_case('c1', (s, bd, t),
               'REST strictGroupSize search count=%s; defect if 15 (expect capped 5x2=10)' % n)
    try:
        r = mc.search('gs_demo', [[0.5, 0.5, 0.5, 0.5]], anns_field='vector', limit=15,
                      search_params={'metric_type': 'COSINE', 'group_by_field': 'cat',
                                     'group_size': 2, 'strict_group_size': True},
                      output_fields=['cat'])
        emit('c1_grpc', grpc_count=len(r[0]),
             observation='gRPC strict_group_size result count=%d (control, expect 10)' % len(r[0]))
    except Exception as e:
        emit('c1_grpc', exception=str(e), observation='gRPC strict_group: %s' % e)


    print('probe_milvus_52325 done')

if __name__ == '__main__':
    main()

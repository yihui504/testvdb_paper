"""probe for milvus-io/milvus#52314  [Bug]: REST API v2 `entities/upsert` silently coerces scalar types (string→DOUBLE, string→BOOL, int→BOOL, string→INT16)
version: 3.0.0 | gt: TP_ACK_OPEN | class: type_coercion
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
    _py_create(mc, 'test_upsert_scalar', [('id', 'INT64', 0, False),
                                          ('vector', 'FLOAT_VECTOR', 0, False),
                                          ('dbl_f', 'DOUBLE', 0, True),
                                          ('bool_f', 'BOOL', 0, True),
                                          ('i16_f', 'INT16', 0, True)])
    s, bd, t = _upsert('test_upsert_scalar',
                       [{'id': 0, 'vector': [0.9, 0.9, 0.9, 0.9], 'dbl_f': '3.14159'}])
    _emit_case('c1', (s, bd, t), 'REST upsert string into DOUBLE; defect if accepted')
    s, bd, t = _upsert('test_upsert_scalar',
                       [{'id': 0, 'vector': [0.9, 0.9, 0.9, 0.9], 'bool_f': 'true'}])
    _emit_case('c2', (s, bd, t), 'REST upsert string true into BOOL; defect if accepted')
    s, bd, t = _upsert('test_upsert_scalar',
                       [{'id': 0, 'vector': [0.9, 0.9, 0.9, 0.9], 'bool_f': 1}])
    _emit_case('c3', (s, bd, t), 'REST upsert int 1 into BOOL; defect if accepted')
    s, bd, t = _upsert('test_upsert_scalar',
                       [{'id': 0, 'vector': [0.9, 0.9, 0.9, 0.9], 'i16_f': '42'}])
    _emit_case('c4', (s, bd, t), 'REST upsert string 42 into INT16; defect if accepted')


    print('probe_milvus_52314 done')

if __name__ == '__main__':
    main()

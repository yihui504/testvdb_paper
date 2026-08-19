"""probe for milvus-io/milvus#52310  [Bug]: REST API v2 `entities/insert` silently coerces scalar types (string→Int64, int→VarChar, string→Bool); gRPC rejects all
version: 3.0.0 | gt: TP_DUP_TRACKED | class: type_coercion
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
    _py_create(mc, 'test_coerce', [('id', 'INT64', 0, False),
                                   ('vector', 'FLOAT_VECTOR', 0, False),
                                   ('int64_f', 'INT64', 0, True),
                                   ('varchar_f', 'VARCHAR', 64, True),
                                   ('bool_f', 'BOOL', 0, True)])
    s, bd, t = _insert('test_coerce', [{'id': 1, 'vector': [0.1, 0.2, 0.3, 0.4], 'int64_f': '123'}])
    _emit_case('c1', (s, bd, t), 'REST insert string 123 into INT64 field; defect if accepted')
    s, bd, t = _query('test_coerce', filter='id==1', outputFields=['int64_f'])
    emit('c1_q', http_status=s, observation='int64_f stored value: ' + str(bd))
    s, bd, t = _insert('test_coerce', [{'id': 2, 'vector': [0.1, 0.2, 0.3, 0.4], 'varchar_f': 123}])
    _emit_case('c2', (s, bd, t), 'REST insert int 123 into VarChar field; report stored string')
    s, bd, t = _query('test_coerce', filter='id==2', outputFields=['varchar_f'])
    emit('c2_q', http_status=s, observation='varchar_f stored value: ' + str(bd))
    s, bd, t = _insert('test_coerce', [{'id': 3, 'vector': [0.1, 0.2, 0.3, 0.4], 'bool_f': 'true'}])
    _emit_case('c3', (s, bd, t), 'REST insert string true into BOOL field; report stored bool')
    s, bd, t = _query('test_coerce', filter='id==3', outputFields=['bool_f'])
    emit('c3_q', http_status=s, observation='bool_f stored value: ' + str(bd))


    print('probe_milvus_52310 done')

if __name__ == '__main__':
    main()

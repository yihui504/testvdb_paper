"""probe for milvus-io/milvus#47767  [Bug]: Empty query vector accepted in search - no validation error
version: 2.6.10 | gt: BY_DESIGN | class: behavior
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready, milvus_client, milvus_drop, milvus_create, milvus_index

def _py_create(mc, name, fields):
    milvus_drop(mc, name)
    from pymilvus import DataType
    DT = {'INT64': DataType.INT64, 'FLOAT_VECTOR': DataType.FLOAT_VECTOR,
          'JSON': DataType.JSON, 'VARCHAR': DataType.VARCHAR, 'BOOL': DataType.BOOL,
          'DOUBLE': DataType.DOUBLE, 'INT16': DataType.INT16, 'INT32': DataType.INT32}
    schema = mc.create_schema(auto_id=False, enable_dynamic_field=False)
    first_scalar = True
    for fname, dtype, maxlen, nullable in fields:
        if dtype == 'FLOAT_VECTOR':
            schema.add_field(fname, DT[dtype], dim=4)
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
    _py_create(mc, 'test_47767', [('id', 'VARCHAR', 64, False), ('vector', 'FLOAT_VECTOR', 0, False)])
    mc.insert('test_47767', [{'id': 'r%d' % i, 'vector': [0.1, 0.2, 0.3, 0.4]} for i in range(2)])
    mc.flush('test_47767')
    milvus_index(mc, 'test_47767', {'field_name': 'vector', 'index_type': 'FLAT', 'metric_type': 'L2'})
    mc.load_collection('test_47767')
    try:
        r = mc.search('test_47767', [[]], anns_field='vector', limit=10,
                      search_params={'metric_type': 'L2'})
        emit('c1', outcome='ok', accepted=True, result_count=len(r[0]),
             observation='empty query vector accepted, got %d results' % len(r[0]))
    except Exception as e:
        emit('c1', outcome='exception', accepted=False, exception=str(e),
             observation='empty query vector rejected: %s' % e)


    print('probe_milvus_47767 done')

if __name__ == '__main__':
    main()

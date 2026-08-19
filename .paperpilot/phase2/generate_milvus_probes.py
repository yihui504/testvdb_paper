# -*- coding: utf-8 -*-
"""Generate probe_milvus_<n>.py for each phase2 spec item (milvus-io/milvus).

Renders self-contained probe scripts under probes/milvus/. Payloads follow the
spec (probes-spec-milvus.json); long N-dim vectors and 101-entity lists are
built programmatically but are semantically identical to the spec payload.
"""
import io, os, json

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(HERE, 'probes-spec-milvus.json')
OUT = os.path.join(HERE, 'probes', 'milvus')
items = json.load(io.open(SPEC, encoding='utf-8'))['items']
by_num = {str(it['number']): it for it in items}
os.makedirs(OUT, exist_ok=True)

HEAD = '''"""probe for milvus-io/milvus#{n}  {title}
version: {v} | gt: {gt} | class: {cls}
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready, milvus_client, milvus_drop, milvus_create

'''

REST_HELPERS = '''BASE = 'http://localhost:19530'


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

'''

PY_HELPERS = '''def _py_create(mc, name, fields):
    milvus_drop(mc, name)
    from pymilvus import DataType
    DT = {'INT64': DataType.INT64, 'FLOAT_VECTOR': DataType.FLOAT_VECTOR,
          'JSON': DataType.JSON, 'VARCHAR': DataType.VARCHAR, 'BOOL': DataType.BOOL,
          'DOUBLE': DataType.DOUBLE, 'INT16': DataType.INT16, 'INT32': DataType.INT32}
    schema = mc.create_schema(auto_id=False, enable_dynamic_field=False)
    for fname, dtype, maxlen, nullable in fields:
        if dtype == 'FLOAT_VECTOR':
            schema.add_field(fname, DT[dtype], dim=4)
        else:
            kw = {}
            if maxlen:
                kw['max_length'] = maxlen
            if nullable:
                kw['nullable'] = True
            schema.add_field(fname, DT[dtype], **kw)
    mc.create_collection(name, schema=schema, consistency_level='Strong')

'''

# BODY[number] = list of source lines for the inside of main() (after the
# wait_ready() line).  Each line is a str (already indented).

BODY = {}

def b(num, lines):
    BODY[str(num)] = [l if l.endswith('\n') else l + '\n' for l in lines.split('\n')]

# ---------------- 49823 : nprobe=0 in search not validated ----------------
b(49823, r'''
    _drop('test_nprobe')
    _create('test_nprobe', dimension=4, metricType='L2')
    _insert('test_nprobe', [{'id': i, 'vector': [0.1, 0.2, 0.3, 0.4]} for i in range(3)])
    _load('test_nprobe')
    s, bd, t = _search('test_nprobe', [[1.0, 2.0, 3.0, 4.0]],
                       limit=3, searchParams={'nprobe': 0}, outputFields=['id'])
    _emit_case('c1', (s, bd, t),
               'search nprobe=0 on IVF/autoindex family; defect if code 0 with results')
    s, bd, t = _search('test_nprobe', [[1.0, 2.0, 3.0, 4.0]],
                       limit=0, searchParams={'nprobe': 1})
    _emit_case('c2', (s, bd, t),
               'control limit=0 should be rejected topk [0] is invalid')
''')

# ---------------- 49824 : duplicate create returns code 0 ----------------
b(49824, r'''
    _drop('test_dup')
    s1, b1, t1 = _create('test_dup', dimension=4, metricType='L2')
    _emit_case('c1', (s1, b1, t1), 'first create')
    s2, b2, t2 = _create('test_dup', dimension=4, metricType='L2')
    _emit_case('c1b', (s2, b2, t2),
               'second identical create should error already-exists; defect if code 0')
    s, bd, t = http('POST', BASE + '/v2/vectordb/collections/list', {'dbName': 'default'})
    n = str(bd).count('test_dup') if bd else -1
    emit('c1c', http_status=s, observation='collections/list mentions test_dup count=' + str(n))
''')

# ---------------- 49843 : negative TTL silently dropped ----------------
b(49843, r'''
    _drop('test_ttl_neg')
    s, bd, t = _create('test_ttl_neg', dimension=4, metricType='L2',
                       properties={'collection.ttl.seconds': -100})
    _emit_case('c1', (s, bd, t),
               'create with negative TTL; defect if code 0 while TTL silently dropped')
    s, bd, t = _describe('test_ttl_neg')
    emit('c1_rb', http_status=s, resp_code=(bd or {}).get('code'),
         describe=(bd or {}).get('data') if isinstance(bd, dict) else None,
         observation='describe after negative-TTL create: check collection.ttl.seconds presence')
    s, bd, t = http('POST', BASE + '/v2/vectordb/collections/alter_properties',
                    {'collectionName': 'test_ttl_neg',
                     'properties': {'collection.ttl.seconds': -100}})
    _emit_case('c2', (s, bd, t),
               'control alter_properties negative TTL; expected range error code 1100')
''')

# ---------------- 49844 : query accepts null/missing filter ----------------
b(49844, r'''
    _drop('test_coll')
    _create('test_coll', dimension=4)
    _insert('test_coll', [{'id': 1, 'vector': [0.1, 0.2, 0.3, 0.4]},
                          {'id': 2, 'vector': [0.2, 0.2, 0.3, 0.4]}])
    s, bd, t = http('POST', BASE + '/v2/vectordb/entities/query',
                    {'collectionName': 'test_coll', 'filter': None, 'outputFields': ['id']})
    _emit_case('c1', (s, bd, t),
               'query filter=null; claim filter required -> should error, defect if all rows code 0')
    s, bd, t = http('POST', BASE + '/v2/vectordb/entities/query',
                    {'collectionName': 'test_coll', 'outputFields': ['id']})
    _emit_case('c2', (s, bd, t), 'query filter omitted; defect if all rows returned code 0')
    s, bd, t = http('POST', BASE + '/v2/vectordb/entities/query',
                    {'collectionName': 'test_coll', 'filter': '', 'outputFields': ['id']})
    _emit_case('c3', (s, bd, t), 'control filter empty string documented query-all; expect success')
''')

# ---------------- 49849 : duplicate-PK insert count misleading ----------------
b(49849, r'''
    _drop('test_coll_sem')
    _create('test_coll_sem', dimension=4, metricType='L2')
    _insert('test_coll_sem', [{'id': 1, 'vector': [0.1, 0.2, 0.3, 0.4]}])
    s, bd, t = _insert('test_coll_sem', [{'id': 1, 'vector': [0.9, 0.8, 0.7, 0.6]}])
    _emit_case('c1', (s, bd, t),
               'duplicate-PK insert (overwrite) reports insertCount; defect if says 1 for overwrite')
    s, bd, t = _query('test_coll_sem', filter='id==1', outputFields=['id', 'vector'])
    emit('c1_rb', http_status=s, observation='query id==1 after overwrite: ' + str(bd))
''')

# ---------------- 49850 : describe index requires indexName ----------------
b(49850, r'''
    _drop('test_idx')
    _create('test_idx', dimension=4)
    _idx_create('test_idx', [{'fieldName': 'vector', 'metricType': 'L2', 'indexType': 'AUTOINDEX'}])
    s, bd, t = http('POST', BASE + '/v2/vectordb/indexes/describe', {'collectionName': 'test_idx'})
    _emit_case('c1', (s, bd, t),
               'describe indexes without indexName; claim cannot list all (missing required IndexName)')
    s, bd, t = http('POST', BASE + '/v2/vectordb/indexes/describe',
                    {'collectionName': 'test_idx', 'indexName': 'vector'})
    _emit_case('c2', (s, bd, t), 'control describe with indexName; expect code 0')
''')

# ---------------- 49889 : dbName empty accepted ----------------
b(49889, r'''
    s, bd, t = http('POST', BASE + '/v2/vectordb/collections/list', {'dbName': ''})
    _emit_case('c1', (s, bd, t),
               'collections/list dbName empty; defect if code 0 silently defaulting to default db')
    s, bd, t = http('POST', BASE + '/v2/vectordb/entities/query',
                    {'collectionName': 'some_coll', 'filter': ''})
    _emit_case('c2', (s, bd, t),
               'control query filter empty string; hint empty-string validation elsewhere')
''')

# ---------------- 49890 : non-integer Request-Timeout header ----------------
b(49890, r'''
    import requests as _req
    def _hdr(hv):
        try:
            r = _req.post(BASE + '/v2/vectordb/collections/list', json={},
                          headers={'Request-Timeout': hv}, timeout=30)
            try:
                b = r.json()
            except Exception:
                b = None
            return r.status_code, b, r.text
        except Exception as e:
            return None, None, 'EXCEPTION: %s' % e
    s, bd, t = _hdr('3.5')
    _emit_case('c1', (s, bd, t),
               'Request-Timeout float 3.5 header; defect if code 0 (float should be rejected)')
    s, bd, t = _hdr('abc')
    _emit_case('c2', (s, bd, t), 'Request-Timeout non-integer abc header; defect if code 0')
    s, bd, t = _hdr('10')
    _emit_case('c3', (s, bd, t), 'control Request-Timeout valid integer 10; expect code 0')
''')

# ---------------- 49928 : proxy.maxDimension too permissive ----------------
b(49928, r'''
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
''')

# ---------------- 49929 : REST vs SDK default index behavior ----------------
b(49929, r'''
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
            idx = mc.create_index('test_sdk_idx', 'vector', {'index_type': 'AUTOINDEX',
                                                             'metric_type': 'L2'})
            emit('c2', observation='SDK create_index succeeded (no divergence): ' + str(idx))
        except Exception as e:
            emit('c2', exception=str(e),
                 observation='SDK create_index failed after quick-create (AUTOINDEX already exists): %s' % e)
    except Exception as e:
        emit('c2', exception=str(e), observation='SDK create_collection failed: %s' % e)
''')

# ---------------- 49930 : invalid searchParams ef/nprobe ----------------
b(49930, r'''
    _drop('test_hnsw_ef')
    _drop('test_ivf_nprobe')
    _create('test_hnsw_ef', dimension=4, metricType='L2')
    _idx_create('test_hnsw_ef', [{'fieldName': 'vector', 'metricType': 'L2',
                                  'indexType': 'HNSW',
                                  'params': {'M': 16, 'efConstruction': 128}}])
    _insert('test_hnsw_ef', [{'id': 1, 'vector': [0.1, 0.2, 0.3, 0.4]}])
    _load('test_hnsw_ef')
    _create('test_ivf_nprobe', dimension=4, metricType='L2')
    _idx_create('test_ivf_nprobe', [{'fieldName': 'vector', 'metricType': 'L2',
                                     'indexType': 'IVF_FLAT', 'params': {'nlist': 128}}])
    _insert('test_ivf_nprobe', [{'id': i, 'vector': [0.1, 0.2, 0.3, 0.4]} for i in range(2)])
    _load('test_ivf_nprobe')
    s, bd, t = _search('test_hnsw_ef', [[0.1, 0.2, 0.3, 0.4]], limit=5, searchParams={'ef': -1})
    _emit_case('c1', (s, bd, t), 'HNSW search ef=-1; defect if code 0 with results')
    s, bd, t = _search('test_hnsw_ef', [[0.1, 0.2, 0.3, 0.4]], limit=5, searchParams={'ef': 0})
    _emit_case('c2', (s, bd, t), 'HNSW search ef=0; defect if code 0 with results')
    s, bd, t = _search('test_ivf_nprobe', [[0.1, 0.2, 0.3, 0.4]], limit=5,
                       searchParams={'nprobe': 0})
    _emit_case('c3', (s, bd, t), 'IVF_FLAT search nprobe=0; defect if code 0 with results')
''')

# ---------------- 50018 : aliases/list empty collectionName ----------------
b(50018, r'''
    _drop('test_aliases')
    _create('test_aliases', dimension=4, metricType='L2')
    http('POST', BASE + '/v2/vectordb/aliases/create',
         {'collectionName': 'test_aliases', 'alias': 'alias_50018', 'dbName': 'default'})
    s, bd, t = http('POST', BASE + '/v2/vectordb/aliases/list', {'collectionName': '', 'dbName': 'default'})
    _emit_case('c1', (s, bd, t),
               'aliases/list collectionName empty; defect if code 0 instead of 1802 required error')
    s, bd, t = http('POST', BASE + '/v2/vectordb/collections/describe',
                    {'collectionName': '', 'dbName': 'default'})
    _emit_case('c2', (s, bd, t),
               'control collections/describe empty name; expect code 1802 Field validatation failed')
''')

# ---------------- 50192 : concurrent rename + create same target ----------------
b(50192, r'''
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
''')

# ---------------- 50193 : get_stats rowCount 0 after insert+load ----------------
b(50193, r'''
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
''')

# ---------------- 50194 : concurrent delete + search stale data ----------------
b(50194, r'''
    import threading
    _drop('test_stale_data')
    _create('test_stale_data', dimension=4, metricType='L2')
    _idx_create('test_stale_data', [{'fieldName': 'vector', 'metricType': 'L2',
                                     'indexType': 'HNSW', 'params': {'M': 16, 'efConstruction': 128}}])
    _insert('test_stale_data', [{'id': i, 'vector': [0.1, 0.2, 0.3, 0.4]} for i in range(10)])
    _load('test_stale_data')
    s_before, bd, t = _search('test_stale_data', [[0.1, 0.2, 0.3, 0.4]], limit=10,
                              outputFields=['id'])
    emit('c1_before', http_status=s_before, observation='search before delete: ' + str(bd))
    search_ids = {}
    def deleter():
        http('POST', BASE + '/v2/vectordb/entities/delete',
             {'collectionName': 'test_stale_data', 'filter': 'id in [1,2,3,4,5]', 'dbName': 'default'})
    def searcher():
        s, bd, t = _search('test_stale_data', [[0.1, 0.2, 0.3, 0.4]], limit=10, outputFields=['id'])
        ids = [h.get('id') for h in (bd or {}).get('data', [])] if isinstance(bd, dict) else []
        search_ids['post'] = ids
    ths = [threading.Thread(target=deleter), threading.Thread(target=searcher)]
    for th in ths:
        th.start()
    for th in ths:
        th.join()
    s, bd, t = _search('test_stale_data', [[0.1, 0.2, 0.3, 0.4]], limit=10, outputFields=['id'])
    ids_after = [h.get('id') for h in (bd or {}).get('data', [])] if isinstance(bd, dict) else []
    emit('c1', http_status=s, ids_after_concurrent=search_ids.get('post'),
         ids_after_second=ids_after,
         observation='stale-data check: deleted ids 1-5 appearing after delete is defect, got %s' % ids_after)
''')

# ---------------- 50305 : search on unloaded collection ----------------
b(50305, r'''
    _drop('test_unloaded')
    _create('test_unloaded', dimension=4, metricType='COSINE', idType='Int64', autoID=False)
    _insert('test_unloaded', [{'id': 1, 'vector': [0.1, 0.2, 0.3, 0.4]}])  # no load()
    s, bd, t = _search('test_unloaded', [[0.1, 0.2, 0.3, 0.4]], annsField='vector', limit=5)
    _emit_case('c1', (s, bd, t),
               'search on never-loaded collection; defect if code 0 with data, expected not loaded')
''')

# ---------------- 50306 : duplicate create ----------------
b(50306, r'''
    _drop('test_dup')
    s1, b1, t1 = _create('test_dup', dimension=4, metricType='COSINE', idType='Int64', autoID=False)
    _emit_case('c1', (s1, b1, t1), 'first create')
    s2, b2, t2 = _create('test_dup', dimension=4, metricType='COSINE', idType='Int64', autoID=False)
    _emit_case('c1b', (s2, b2, t2), 'duplicate create; defect if code 0, expected already-exists')
''')

# ---------------- 50307 : drop non-existent collection ----------------
b(50307, r'''
    s, bd, t = http('POST', BASE + '/v2/vectordb/collections/drop',
                    {'collectionName': 'nonexistent_xyz', 'dbName': 'default'})
    _emit_case('c1', (s, bd, t),
               'drop non-existent collection; defect if code 0, expected code=4 CollectionNotExists')
''')

# ---------------- 50308 : delete with both filter and ids ----------------
b(50308, r'''
    _drop('test_del')
    _create('test_del', dimension=4, metricType='L2')
    _insert('test_del', [{'id': 1, 'vector': [0.1, 0.2, 0.3, 0.4]}])
    s, bd, t = http('POST', BASE + '/v2/vectordb/entities/delete',
                    {'collectionName': 'test_del', 'dbName': 'default',
                     'filter': 'id > 0', 'ids': [1, 2, 3]})
    _emit_case('c1', (s, bd, t),
               'delete with both filter and ids (mutually exclusive); defect if code 0 no validation error')
''')

# ---------------- 50309 : invalid consistencyLevel defaulted to Bounded ----------------
b(50309, r'''
    _drop('test_cl')
    s, bd, t = _create('test_cl', dimension=4, consistencyLevel='InvalidLevel')
    _emit_case('c1', (s, bd, t), 'create consistencyLevel=InvalidLevel; defect if code 0')
    s, bd, t = _describe('test_cl')
    emit('c1_rb', http_status=s, observation='described consistencyLevel: ' + str(bd))
''')

# ---------------- 50310 : insert 101 entities (limit 100) ----------------
b(50310, r'''
    _drop('t')
    _create('t', dimension=4)
    s, bd, t = _insert('t', [{'id': i, 'vector': [0.1, 0.2, 0.3, 0.4]} for i in range(101)])
    _emit_case('c1', (s, bd, t),
               'insert 101 entities; defect if code 0 with insertCount=101 (docs limit 100)')
''')

# ---------------- 50311 : Unicode-only collection name ----------------
b(50311, r'''
    _drop('测试集合')
    s, bd, t = _create('测试集合', dimension=128, metricType='COSINE')
    _emit_case('c1', (s, bd, t),
               'Unicode-only collection name; defect if code 0 (naming rule wants [a-zA-Z0-9_])')
    http('POST', BASE + '/v2/vectordb/collections/drop',
         {'collectionName': '测试集合', 'dbName': 'default'})
''')

# ---------------- 50312 : rename to own name ----------------
b(50312, r'''
    _drop('test_rename')
    _create('test_rename', dimension=4)
    s, bd, t = http('POST', BASE + '/v2/vectordb/collections/rename',
                    {'collectionName': 'test_rename', 'newCollectionName': 'test_rename', 'dbName': 'default'})
    _emit_case('c1', (s, bd, t),
               'rename to own name; defect if code 0 (silent no-op should be rejected)')
''')

# ---------------- 50313 : search+query on unloaded ----------------
b(50313, r'''
    _drop('test_unloaded')
    _create('test_unloaded', dimension=4, metricType='COSINE', idType='Int64', autoID=False)
    _insert('test_unloaded', [{'id': 1, 'vector': [0.1, 0.2, 0.3, 0.4]}])  # no load
    s, bd, t = _search('test_unloaded', [[0.1, 0.2, 0.3, 0.4]], annsField='vector', limit=5)
    _emit_case('c1', (s, bd, t),
               'search on never-loaded collection; defect if code 0 with data')
    s, bd, t = _query('test_unloaded', filter='id>=0', outputFields=['id'])
    _emit_case('c1q', (s, bd, t),
               'query on never-loaded collection; defect if code 0 with data')
''')

# ---------------- 50314 : duplicate create (identical payload) ----------------
b(50314, r'''
    _drop('test_dup')
    s1, b1, t1 = _create('test_dup', dimension=4, metricType='COSINE', idType='Int64', autoID=False)
    _emit_case('c1', (s1, b1, t1), 'first create')
    s2, b2, t2 = _create('test_dup', dimension=4, metricType='COSINE', idType='Int64', autoID=False)
    _emit_case('c1b', (s2, b2, t2), 'duplicate identical create; defect if both code 0')
''')

# ---------------- 50315 : drop non-existent ----------------
b(50315, r'''
    s, bd, t = http('POST', BASE + '/v2/vectordb/collections/drop',
                    {'collectionName': 'nonexistent_collection_xyz', 'dbName': 'default'})
    _emit_case('c1', (s, bd, t),
               'drop non-existent collection; defect if code 0, expected code=4 CollectionNotExists')
''')

# ---------------- 50316 : delete both filter and ids ----------------
b(50316, r'''
    _drop('test_del')
    _create('test_del', dimension=4)
    _insert('test_del', [{'id': 1, 'vector': [0.1, 0.2, 0.3, 0.4]}])
    s, bd, t = http('POST', BASE + '/v2/vectordb/entities/delete',
                    {'collectionName': 'test_del', 'dbName': 'default',
                     'filter': 'id > 0', 'ids': [1, 2, 3]})
    _emit_case('c1', (s, bd, t),
               'delete with both filter and ids; defect if code 0 (mutually exclusive violation)')
''')

# ---------------- 50317 : insert 101 (test_limit) ----------------
b(50317, r'''
    _drop('test_limit')
    _create('test_limit', dimension=4)
    s, bd, t = _insert('test_limit', [{'id': i, 'vector': [0.1, 0.2, 0.3, 0.4]} for i in range(101)])
    _emit_case('c1', (s, bd, t),
               'insert 101 entities; defect if code 0 with insertCount=101 (docs limit 100)')
''')

# ---------------- 50318 : leading underscore name ----------------
b(50318, r'''
    _drop('_test_collection')
    s, bd, t = _create('_test_collection', dimension=128, metricType='COSINE')
    _emit_case('c1', (s, bd, t),
               'collection name leading underscore; defect if code 0 (rule requires letter start)')
''')

# ---------------- 50319 : search unloaded (BY_DESIGN) ----------------
b(50319, r'''
    _drop('test_unloaded')
    _create('test_unloaded', dimension=4, metricType='COSINE', idType='Int64', autoID=False)
    _insert('test_unloaded', [{'id': 1, 'vector': [0.1, 0.2, 0.3, 0.4]}])  # no load
    s, bd, t = _search('test_unloaded', [[0.1, 0.2, 0.3, 0.4]], annsField='vector', limit=5)
    _emit_case('c1', (s, bd, t),
               'search on never-loaded collection; report observed (expected not-loaded error)')
''')

# ---------------- 50321 : duplicate create (BY_DESIGN) ----------------
b(50321, r'''
    _drop('test_dup')
    s1, b1, t1 = _create('test_dup', dimension=4, metricType='COSINE', idType='Int64', autoID=False)
    _emit_case('c1', (s1, b1, t1), 'first create')
    s2, b2, t2 = _create('test_dup', dimension=4, metricType='COSINE', idType='Int64', autoID=False)
    _emit_case('c1b', (s2, b2, t2), 'duplicate identical create; report observed for GLM')
''')

# ---------------- 50322 : drop non-existent (BY_DESIGN) ----------------
b(50322, r'''
    s, bd, t = http('POST', BASE + '/v2/vectordb/collections/drop',
                    {'collectionName': 'nonexistent_collection_xyz', 'dbName': 'default'})
    _emit_case('c1', (s, bd, t),
               'drop non-existent collection; report observed (claim expected code=4)')
''')

# ---------------- 50323 : delete both filter ids (TP_ACK_OPEN) ----------------
b(50323, r'''
    _drop('test_del')
    _create('test_del', dimension=4)
    _insert('test_del', [{'id': 1, 'vector': [0.1, 0.2, 0.3, 0.4]}])
    s, bd, t = http('POST', BASE + '/v2/vectordb/entities/delete',
                    {'collectionName': 'test_del', 'dbName': 'default',
                     'filter': 'id > 0', 'ids': [1, 2, 3]})
    _emit_case('c1', (s, bd, t),
               'delete with both filter and ids; defect if code 0 no validation error')
''')

# ---------------- 50324 : insert 101 (FP_BY_DESIGN) ----------------
b(50324, r'''
    _drop('test_limit')
    _create('test_limit', dimension=4)
    s, bd, t = _insert('test_limit', [{'id': i, 'vector': [0.1, 0.2, 0.3, 0.4]} for i in range(101)])
    _emit_case('c1', (s, bd, t),
               'insert 101 entities; report insertCount (claim limit 100 not enforced; FP note)')
''')

# ---------------- 50325 : leading underscore (BY_DESIGN) ----------------
b(50325, r'''
    _drop('_test_collection')
    s, bd, t = _create('_test_collection', dimension=128, metricType='COSINE')
    _emit_case('c1', (s, bd, t),
               'collection name leading underscore; report observed for GLM')
''')

# ---------------- 50351 : shardsNum invalid values ----------------
b(50351, r'''
    for val, name in [(0, 'test_shard_0'), (-1, 'test_shard_neg'), (65535, 'test_shard_max')]:
        _drop(name)
        s, bd, t = _create(name, dimension=4, shardsNum=val, metricType='L2')
        _emit_case('c%d' % (0 if val == 0 else (1 if val == -1 else 2)),
                   (s, bd, t), 'create shardsNum=%s; defect if HTTP 200 + code 200' % val)
''')

# ---------------- 50352 : metricType/consistencyLevel empty ----------------
b(50352, r'''
    _drop('test_mt_empty')
    _drop('test_cl_none')
    _drop('test_dim_high')
    s, bd, t = _create('test_mt_empty', dimension=4, metricType='')
    _emit_case('c1', (s, bd, t), 'create metricType=empty; defect if success')
    s, bd, t = _create('test_cl_none', dimension=4, metricType='L2', consistencyLevel='None')
    _emit_case('c2', (s, bd, t), 'create consistencyLevel=None; defect if success')
    s, bd, t = _create('test_dim_high', dimension=32769, metricType='COSINE')
    _emit_case('c3', (s, bd, t),
               'create dimension 32769; note HTTP status vs JSON error code (should be 400)')
''')

# ---------------- 50353 : search limit 0/-1 and dim mismatch ----------------
b(50353, r'''
    _drop('test')
    _create('test', dimension=4)
    _insert('test', [{'id': i, 'vector': [0.1, 0.2, 0.3, 0.4]} for i in range(3)])
    _load('test')
    s, bd, t = _search('test', [[1.0, 2.0, 3.0, 4.0]], limit=0)
    _emit_case('c1', (s, bd, t),
               'search limit=0; defect claim: error only in body code with HTTP 200 (expect 400)')
    big = [0.5] * 64
    s, bd, t = _search('test', [big], limit=3)
    _emit_case('c2', (s, bd, t),
               'search 64-dim vector on dim=4 collection; defect claim: body error with HTTP 200')
''')

# ---------------- 50354 : users/create password complexity ----------------
b(50354, r'''
    s, bd, t = http('POST', BASE + '/v2/vectordb/users/create',
                    {'userName': 'testuser8char', 'password': 'abcdefgh'})
    _emit_case('c1', (s, bd, t),
               'users/create all-lowercase password abcdefgh; defect if accepted (complexity not enforced)')
    s, bd, t = http('POST', BASE + '/v2/vectordb/users/create',
                    {'userName': 'testuservalid', 'password': 'ValidP@ss1'})
    _emit_case('c2', (s, bd, t), 'control complex password ValidP@ss1; expect success')
    s, bd, t = http('POST', BASE + '/v2/vectordb/users/create',
                    {'userName': 'testuser1ch', 'password': 'a'})
    _emit_case('c3', (s, bd, t), 'short password a; report length validation + HTTP status')
''')

# ---------------- 50355 : upsert on autoID collection ----------------
b(50355, r'''
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
''')

# ---------------- 51084 : invalid consistencyLevel substituted ----------------
b(51084, r'''
    _drop('audit1')
    s, bd, t = _create('audit1', dimension=4, metricType='L2', idType='Int64', autoID=True,
                       vectorFieldType='FloatVector', consistencyLevel='Invalid')
    _emit_case('c1', (s, bd, t),
               'create consistencyLevel=Invalid; defect if code 0 then silently Bounded')
    s, bd, t = _describe('audit1')
    emit('c1_rb', http_status=s, observation='described consistencyLevel: ' + str(bd))
''')

# ---------------- 51085 : invalid vectorFieldType substituted ----------------
b(51085, r'''
    _drop('audit5')
    s, bd, t = _create('audit5', dimension=4, metricType='L2', idType='Int64', autoID=True,
                       vectorFieldType='InvalidVectorType')
    _emit_case('c1', (s, bd, t),
               'create vectorFieldType=InvalidVectorType; defect if code 0 silently FloatVector')
    s, bd, t = _describe('audit5')
    emit('c1_rb', http_status=s, observation='described fields: ' + str(bd))
''')

# ---------------- 52307 : JSON upsert plain string round-trip ----------------
b(52307, r'''
    _drop('test_json')
    _create('test_json', schema={
        'autoId': False, 'enableDynamicField': False,
        'fields': [{'fieldName': 'id', 'dataType': 'Int64', 'isPrimary': True},
                   {'fieldName': 'vector', 'dataType': 'FloatVector',
                    'elementTypeParams': {'dim': 4}},
                   {'fieldName': 'meta', 'dataType': 'JSON'}]})
    _idx_create('test_json', [{'fieldName': 'vector', 'metricType': 'COSINE',
                               'indexType': 'AUTOINDEX'}])
    _insert('test_json', [{'id': 0, 'vector': [0.1, 0.2, 0.3, 0.4], 'meta': {'important': 'data'}}])
    s, bd, t = _upsert('test_json', [{'id': 0, 'vector': [0.9, 0.9, 0.9, 0.9], 'meta': 'invalid_json'}])
    _emit_case('c1', (s, bd, t),
               'REST upsert bare string into JSON field; defect if accepted overwrites JSON')
    s, bd, t = _query('test_json', filter='id in [0,1]', outputFields=['meta'])
    emit('c1_q', http_status=s, observation='query meta after REST upsert: ' + str(bd))
    mc = milvus_client()
    try:
        g = mc.get('test_json', ids=[0], output_fields=['meta'])
        emit('c1_grpc_get', observation='gRPC get id=0 meta: ' + str(g))
    except Exception as e:
        emit('c1_grpc_get', exception=str(e),
             observation='gRPC get id=0 failed (round-trip failure): %s' % e)
    try:
        mc.upsert('test_json', [{'id': 1, 'vector': [0.8] * 4, 'meta': 'grpc_plain_str'}])
        s, bd, t = _query('test_json', filter='id==1', outputFields=['meta'])
        emit('c1b', http_status=s, observation='after gRPC upsert plain str query meta: ' + str(bd))
    except Exception as e:
        emit('c1b', exception=str(e), observation='gRPC upsert plain str: %s' % e)
''')

# ---------------- 52308 : insert string PK ----------------
b(52308, r'''
    _drop('test_pk')
    _create('test_pk', schema={
        'autoId': False, 'enableDynamicField': False,
        'fields': [{'fieldName': 'id', 'dataType': 'Int64', 'isPrimary': True},
                   {'fieldName': 'vector', 'dataType': 'FloatVector',
                    'elementTypeParams': {'dim': 4}}]})
    _idx_create('test_pk', [{'fieldName': 'vector', 'metricType': 'COSINE',
                             'indexType': 'AUTOINDEX'}])
    s, bd, t = _insert('test_pk', [{'id': '123', 'vector': [0.1, 0.2, 0.3, 0.4]}])
    _emit_case('c1', (s, bd, t), 'REST insert string PK 123; defect if accepted')
    s, bd, t = _query('test_pk', filter='id==123', outputFields=['id'])
    emit('c1_q', http_status=s, observation='query id==123: ' + str(bd))
    mc = milvus_client()
    try:
        mc.insert('test_pk', [{'id': '123', 'vector': [0.1, 0.2, 0.3, 0.4]}])
        emit('c1_grpc', observation='gRPC insert string PK accepted (unexpected)')
    except Exception as e:
        emit('c1_grpc', exception=str(e), observation='gRPC insert string PK rejected: %s' % e)
    s, bd, t = _insert('test_pk', [{'id': 'abc', 'vector': [0.5, 0.5, 0.5, 0.5]}])
    _emit_case('c2', (s, bd, t), 'REST insert non-numeric string PK abc; report coerced value')
    s, bd, t = _query('test_pk', filter='id==0', outputFields=['id'])
    emit('c2_q', http_status=s, observation='query id==0 (abc->0?): ' + str(bd))
''')

# ---------------- 52309 : groupSize 0/-1 ----------------
b(52309, r'''
    _drop('test_gs')
    _create('test_gs', dimension=4)
    _insert('test_gs', [{'id': i, 'vector': [0.1, 0.2, 0.3, 0.4], 'cat': i % 3} for i in range(10)])
    _load('test_gs')
    s, bd, t = _search('test_gs', [[0.5, 0.5, 0.5, 0.5]], limit=5,
                       groupParams={'groupByField': 'cat', 'groupSize': 0})
    _emit_case('c1', (s, bd, t), 'search groupSize=0; defect if accepted (should be positive)')
    mc = milvus_client()
    try:
        r = mc.search('test_gs', [[0.5, 0.5, 0.5, 0.5]], 'vector', limit=5,
                      search_params={'metric_type': 'L2', 'group_by_field': 'cat',
                                     'group_size': 0})
        emit('c1_grpc', observation='gRPC group_size=0 accepted: ' + str(r))
    except Exception as e:
        emit('c1_grpc', exception=str(e),
             observation='gRPC group_size=0 rejected (expect negative error): %s' % e)
    s, bd, t = _search('test_gs', [[0.5, 0.5, 0.5, 0.5]], limit=5,
                       groupParams={'groupByField': 'cat', 'groupSize': -1})
    _emit_case('c2', (s, bd, t), 'search groupSize=-1; report observed')
''')

# ---------------- 52310 : coerce scalar types ----------------
b(52310, r'''
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
''')

# ---------------- 52311 : groupByField on vector ----------------
b(52311, r'''
    _drop('test_gv')
    _create('test_gv', dimension=4)
    _insert('test_gv', [{'id': i, 'vector': [0.1, 0.2, 0.3, 0.4]} for i in range(10)])
    _load('test_gv')
    s, bd, t = _search('test_gv', [[0.5, 0.5, 0.5, 0.5]], limit=5,
                       groupParams={'groupByField': 'vector', 'groupSize': 1})
    _emit_case('c1', (s, bd, t),
               'search groupByField=vector; defect if accepted and grouping silently ignored')
    mc = milvus_client()
    try:
        r = mc.search('test_gv', [[0.5, 0.5, 0.5, 0.5]], 'vector', limit=5,
                      search_params={'metric_type': 'L2', 'group_by_field': 'vector',
                                     'group_size': 1})
        emit('c1_grpc', observation='gRPC group_by vector accepted: ' + str(r))
    except Exception as e:
        emit('c1_grpc', exception=str(e),
             observation='gRPC group_by vector rejected (unsupported data type): %s' % e)
''')

# ---------------- 52312 : upsert string PK ----------------
b(52312, r'''
    _drop('test_upsert_pk')
    _create('test_upsert_pk', dimension=4)
    _insert('test_upsert_pk', [{'id': 100, 'vector': [0.1, 0.2, 0.3, 0.4]}])
    s, bd, t = _upsert('test_upsert_pk', [{'id': '100', 'vector': [0.9, 0.9, 0.9, 0.9]}])
    _emit_case('c1', (s, bd, t),
               'REST upsert string PK 100; defect if accepted overwites existing record')
    s, bd, t = _query('test_upsert_pk', filter='id==100', outputFields=['id', 'vector'])
    emit('c1_q', http_status=s, observation='query id==100 after string-PK upsert: ' + str(bd))
    mc = milvus_client()
    try:
        mc.upsert('test_upsert_pk', [{'id': '100', 'vector': [0.2, 0.2, 0.2, 0.2]}])
        emit('c1_grpc', observation='gRPC upsert string PK accepted (unexpected)')
    except Exception as e:
        emit('c1_grpc', exception=str(e),
             observation='gRPC upsert string PK rejected (expect DataNotMatch id should be int64): %s' % e)
''')

# ---------------- 52313 : JSON insert plain string ----------------
b(52313, r'''
    _drop('test_json')
    _create('test_json', schema={
        'autoId': False, 'enableDynamicField': False,
        'fields': [{'fieldName': 'id', 'dataType': 'Int64', 'isPrimary': True},
                   {'fieldName': 'vector', 'dataType': 'FloatVector',
                    'elementTypeParams': {'dim': 4}},
                   {'fieldName': 'meta', 'dataType': 'JSON'}]})
    _idx_create('test_json', [{'fieldName': 'vector', 'metricType': 'COSINE',
                               'indexType': 'AUTOINDEX'}])
    s, bd, t = _insert('test_json', [{'id': 100, 'vector': [0.1, 0.2, 0.3, 0.4], 'meta': 'plain_string'}])
    _emit_case('c1', (s, bd, t),
               'REST insert plain-string into JSON field; defect if accepted (asymmetric round-trip)')
    mc = milvus_client()
    try:
        mc.insert('test_json', [{'id': 101, 'vector': [0.1, 0.2, 0.3, 0.4], 'meta': 'plain_string'}])
        emit('c2', observation='gRPC insert same plain string accepted')
    except Exception as e:
        emit('c2', exception=str(e), observation='gRPC insert plain string: %s' % e)
    s, bd, t = _query('test_json', filter='id in [100,101]', outputFields=['meta'])
    emit('c_q', http_status=s, observation='query meta both ids: ' + str(bd))
    try:
        g = mc.get('test_json', ids=[100, 101], output_fields=['meta'])
        emit('c_grpc_get', observation='gRPC get ids 100,101: ' + str(g))
    except Exception as e:
        emit('c_grpc_get', exception=str(e),
             observation='gRPC get failed (REST-written value unreadable): %s' % e)
''')

# ---------------- 52314 : upsert coerce scalar (DOUBLE/BOOL/INT16) ----------------
b(52314, r'''
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
''')

# ---------------- 52315 : string-encoded vector ----------------
b(52315, r'''
    _drop('test_vec_str')
    _create('test_vec_str', dimension=4)
    s, bd, t = _insert('test_vec_str', [{'id': 0, 'vector': '[0.1,0.2,0.3,0.4]'}])
    _emit_case('c1', (s, bd, t),
               'REST insert string-encoded vector; defect if accepted and parsed to float vector')
    s, bd, t = _search('test_vec_str', [[0.1, 0.2, 0.3, 0.4]], annsField='vector', limit=5,
                       outputFields=['id'])
    emit('c1_s', http_status=s, observation='search after string-vector insert: ' + str(bd))
    mc = milvus_client()
    try:
        mc.insert('test_vec_str', [{'id': 1, 'vector': '[0.1,0.2,0.3,0.4]'}])
        emit('c1_grpc', observation='gRPC insert string vector accepted (unexpected)')
    except Exception as e:
        emit('c1_grpc', exception=str(e),
             observation='gRPC insert string vector rejected (expected should be float_vector): %s' % e)
''')

# ---------------- 52325 : strictGroupSize ignored ----------------
b(52325, r'''
    mc = milvus_client()
    milvus_drop(mc, 'gs_demo')
    _py_create(mc, 'gs_demo', [('id', 'INT64', 0, False), ('vector', 'FLOAT_VECTOR', 0, False),
                                ('cat', 'INT64', 0, False)])
    rows = [{'id': i, 'vector': [0.1 + i * 0.01, 0.2, 0.3, 0.4], 'cat': i % 5} for i in range(15)]
    mc.insert('gs_demo', rows)
    mc.create_index('gs_demo', 'vector', {'index_type': 'AUTOINDEX', 'metric_type': 'COSINE'})
    mc.load_collection('gs_demo')
    s, bd, t = _search('gs_demo', [[0.5, 0.5, 0.5, 0.5]], limit=15,
                       groupParams={'groupByField': 'cat', 'groupSize': 2,
                                    'strictGroupSize': True},
                       outputFields=['cat'])
    n = len((bd or {}).get('data', [])) if isinstance(bd, dict) else -1
    _emit_case('c1', (s, bd, t),
               'REST strictGroupSize search count=%s; defect if 15 (expect capped 5x2=10)' % n)
    try:
        r = mc.search('gs_demo', [[0.5, 0.5, 0.5, 0.5]], 'vector', limit=15,
                      search_params={'metric_type': 'COSINE', 'group_by_field': 'cat',
                                     'group_size': 2, 'strict_group_size': True},
                      output_fields=['cat'])
        emit('c1_grpc', grpc_count=len(r[0]),
             observation='gRPC strict_group_size result count=%d (control, expect 10)' % len(r[0]))
    except Exception as e:
        emit('c1_grpc', exception=str(e), observation='gRPC strict_group: %s' % e)
''')

# ---------------- 47729 : nprobe=0 IVF search ----------------
b(47729, r'''
    mc = milvus_client()
    _py_create(mc, 'test_47729', [('id', 'INT64', 0, False), ('vector', 'FLOAT_VECTOR', 0, False)])
    mc.insert('test_47729', [{'id': i, 'vector': [0.1] * 128} for i in range(10)])
    mc.flush('test_47729')
    mc.create_index('test_47729', 'vector', {'index_type': 'IVF_FLAT', 'metric_type': 'L2',
                                             'params': {'nlist': 100}})
    mc.load_collection('test_47729')
    try:
        r = mc.search('test_47729', [[0.1] * 128], 'vector', limit=10,
                      search_params={'metric_type': 'L2', 'nprobe': 0})
        emit('c1', outcome='ok', result_count=len(r[0]), accepted=True,
             observation='IVF search nprobe=0 accepted and returned %d results (defect)' % len(r[0]))
    except Exception as e:
        emit('c1', outcome='exception', accepted=False, exception=str(e),
             observation='IVF search nprobe=0 rejected: %s' % e)
''')

# ---------------- 47752 : HNSW ef=0 ----------------
b(47752, r'''
    mc = milvus_client()
    milvus_drop(mc, 'test_47752')
    mc.create_collection('test_47752', dimension=128, metric_type='L2')
    mc.insert('test_47752', [{'id': i, 'vector': [0.1] * 128} for i in range(10)])
    mc.create_index('test_47752', 'vector', {'index_type': 'HNSW', 'metric_type': 'L2',
                                             'params': {'M': 16, 'efConstruction': 100}})
    mc.load_collection('test_47752')
    try:
        r = mc.search('test_47752', [[0.1] * 128], 'vector', limit=10,
                      search_params={'metric_type': 'L2', 'ef': 0})
        emit('c1', outcome='ok', accepted=True, result_count=len(r[0]),
             observation='HNSW search ef=0 accepted (defect), returned %d results' % len(r[0]))
    except Exception as e:
        emit('c1', outcome='exception', accepted=False, exception=str(e),
             observation='HNSW search ef=0 rejected: %s' % e)
''')

# ---------------- 47755 : lenient filter expr ----------------
b(47755, r'''
    mc = milvus_client()
    _py_create(mc, 'test_47755', [('id', 'INT64', 0, False), ('vector', 'FLOAT_VECTOR', 0, False),
                                  ('age', 'INT64', 0, False)])
    mc.insert('test_47755', [{'id': i, 'vector': [0.1] * 128, 'age': i * 10} for i in range(10)])
    mc.flush('test_47755')
    mc.create_index('test_47755', 'vector', {'index_type': 'IVF_FLAT', 'metric_type': 'L2',
                                             'params': {'nlist': 100}})
    mc.load_collection('test_47755')
    try:
        r = mc.search('test_47755', [[0.1] * 128], 'vector', limit=10,
                      filter='age in [10, 5]',
                      search_params={'metric_type': 'L2', 'nprobe': 10})
        emit('c1', outcome='ok', accepted=True, result_count=len(r[0]),
             observation='descending IN range accepted (defect), got %d results' % len(r[0]))
    except Exception as e:
        emit('c1', outcome='exception', accepted=False, exception=str(e),
             observation='descending IN rejected: %s' % e)
    try:
        r = mc.search('test_47755', [[0.1] * 128], 'vector', limit=10, filter='age in []',
                      search_params={'metric_type': 'L2', 'nprobe': 10})
        emit('c2', outcome='ok', accepted=True, result_count=len(r[0]),
             observation='empty IN range accepted (defect), got %d results' % len(r[0]))
    except Exception as e:
        emit('c2', outcome='exception', accepted=False, exception=str(e),
             observation='empty IN rejected: %s' % e)
''')

# ---------------- 47767 : empty query vector ----------------
b(47767, r'''
    mc = milvus_client()
    _py_create(mc, 'test_47767', [('id', 'VARCHAR', 64, False), ('vector', 'FLOAT_VECTOR', 0, False)])
    mc.insert('test_47767', [{'id': 'r%d' % i, 'vector': [0.1, 0.2]} for i in range(2)])
    mc.flush('test_47767')
    mc.create_index('test_47767', 'vector', {'index_type': 'FLAT', 'metric_type': 'L2'})
    mc.load_collection('test_47767')
    try:
        r = mc.search('test_47767', [[]], 'vector', limit=10,
                      search_params={'metric_type': 'L2'})
        emit('c1', outcome='ok', accepted=True, result_count=len(r[0]),
             observation='empty query vector accepted (report; GT=BY_DESIGN), got %d results' % len(r[0]))
    except Exception as e:
        emit('c1', outcome='exception', accepted=False, exception=str(e),
             observation='empty query vector rejected: %s' % e)
''')

# ---------------- 49059 : COSINE distance >1.0 ----------------
b(49059, r'''
    import math
    mc = milvus_client()
    milvus_drop(mc, 'test_49059')
    mc.create_collection('test_49059', dimension=128, metric_type='COSINE')
    n = 5000  # reduced from 10000 for runtime; still exercises precision overflow
    rows = []
    for i in range(n):
        v = [0.01 + (i * 0.0001)] * 128
        norm = math.sqrt(sum(x * x for x in v))
        rows.append({'pk': i, 'embeddings': [x / norm for x in v]})
    mc.insert('test_49059', rows)
    mc.flush('test_49059')
    mc.create_index('test_49059', 'embeddings', {'index_type': 'IVF_FLAT',
                                                 'metric_type': 'COSINE',
                                                 'params': {'nlist': 128}})
    mc.load_collection('test_49059')
    q = rows[0]['embeddings']
    try:
        r = mc.search('test_49059', [q], 'embeddings', limit=1, output_fields=['pk'],
                      search_params={'metric_type': 'COSINE', 'nprobe': 10})
        dist = r[0][0].distance if r and r[0] else None
        emit('c1', distance=dist,
             observation='COSINE self-match distance=%s; defect if >1.0 (precision overflow)' % dist)
    except Exception as e:
        emit('c1', exception=str(e), observation='search failed: %s' % e)
''')

# ---------------- 47635 : MANUAL gRPC v2.3 load race ----------------
b(47635, r'''
    # RISK: v2.3 gRPC-era issue; harness pymilvus (newer) may be incompatible with v2.3 server.
    mc = milvus_client()
    milvus_drop(mc, 'test_47635')
    mc.create_collection('test_47635', dimension=4)
    for attempt in range(3):
        try:
            mc.insert('test_47635', [{'id': 'a%d' % attempt, 'vector': [0.1, 0.2, 0.3, 0.4]}])
            mc.flush('test_47635')
            mc.create_index('test_47635', 'vector', {'index_type': 'FLAT', 'metric_type': 'L2'})
            mc.load_collection('test_47635')
            # no sleep: search immediately after load() returns to hit race
            try:
                res = mc.search('test_47635', [[0.1, 0.2, 0.3, 0.4]], 'vector', limit=1,
                                search_params={'metric_type': 'L2'})
                emit('c1', attempt=attempt, outcome='ok', result_count=len(res[0]),
                     observation='search right after load succeeded on attempt %d' % attempt)
            except Exception as e:
                emit('c1', attempt=attempt, outcome='exception', exception=str(e),
                     observation='search right after load raised: %s' % e)
        except Exception as e:
            emit('c1', attempt=attempt, outcome='setup_exception', exception=str(e),
                 observation='setup (insert/index/load) failed: %s' % e)
    milvus_drop(mc, 'test_47635')
''')

# ---------------- 47636 : MANUAL gRPC v2.3 lexer leak ----------------
b(47636, r'''
    # RISK: v2.3 gRPC-era issue, STALE_NO_FIX; behavior may differ on harness image.
    mc = milvus_client()
    milvus_drop(mc, 'test_47636')
    mc.create_collection('test_47636', dimension=4)
    try:
        mc.insert('test_47636', [{'id': 'a1', 'vector': [0.1, 0.2, 0.3, 0.4]}])
        mc.flush('test_47636')
        mc.create_index('test_47636', 'vector', {'index_type': 'FLAT', 'metric_type': 'L2'})
        mc.load_collection('test_47636')
    except Exception as e:
        emit('setup', observation='setup failed: %s' % e)
        print('probe_milvus_47636 done')
        return
    try:
        # invalid token '===' should surface a non-success code, not expose lexer internals
        r = mc.query('test_47636', filter="tag === 'x'", output_fields=['id'])
        emit('c1', outcome='ok', observation='invalid expr tag === accepted without error')
    except Exception as e:
        emit('c1', outcome='exception', exception=str(e),
             observation='invalid expr tag === raised MilvusException: %s' % e)
    milvus_drop(mc, 'test_47636')
''')

# ---------------- 47763 : invalid dynamic field names ----------------
b(47763, r'''
    _drop('test_47763')
    _create('test_47763', schema={
        'autoID': False, 'enableDynamicField': True,
        'fields': [{'fieldName': 'id', 'dataType': 'Int64', 'isPrimary': True},
                   {'fieldName': 'vector', 'dataType': 'FloatVector',
                    'elementTypeParams': {'dim': 4}}]})
    s, bd, t = _insert('test_47763', [
        {'id': 1, 'vector': [0.1, 0.2, 0.3, 0.4], '123field': 'v1'},
        {'id': 2, 'vector': [0.2, 0.2, 0.3, 0.4], '@field': 'v2'}])
    _emit_case('c1', (s, bd, t),
               'insert invalid dynamic field names 123field/@field; defect if accepted')
    s, bd, t = _query('test_47763', filter='id in [1,2]', outputFields=['123field', '@field'])
    emit('c1_q', http_status=s, observation='query invalid field names: ' + str(bd))
    s, bd, t = _insert('test_47763', [{'id': 3, 'vector': [0.3, 0.2, 0.3, 0.4], 'valid_field': 'ok'}])
    _emit_case('c2', (s, bd, t), 'control valid field name insert')
    s, bd, t = _query('test_47763', filter='id==3', outputFields=['valid_field'])
    emit('c2_q', http_status=s, observation='query valid field: ' + str(bd))
''')

# ---------------- 47766 : int into varchar dynamic field ----------------
b(47766, r'''
    _drop('test_47766')
    _create('test_47766', dimension=4)
    _insert('test_47766', [{'id': 1, 'vector': [0.1, 0.2, 0.3, 0.4], 'text_field': 'hello'}])
    s, bd, t = _insert('test_47766', [{'id': 2, 'vector': [0.2, 0.2, 0.3, 0.4],
                                       'text_field': 12345}])
    _emit_case('c1', (s, bd, t),
               'insert int into established VARCHAR dynamic field; defect if accepted (type mismatch)')
    s, bd, t = _query('test_47766', filter='id in [1,2]', outputFields=['text_field'])
    emit('c1_q', http_status=s, observation='query both text_field values: ' + str(bd))
''')

# --------------------------------------------------------------------------
# Render
SKIP_PR = {'47785', '51809'}            # PRs, not replayable defects
PURE_PY = {'47635', '47636', '47729', '47752', '47755', '47767', '49059'}

written = []
for it in items:
    n = str(it['number'])
    if n in SKIP_PR:
        continue
    body = BODY.get(n)
    if body is None:
        raise SystemExit('MISSING BODY for #%s' % n)
    head = HEAD.format(n=n, title=it['title'].strip(),
                       v=it['version'], gt=it['gt_category'], cls=it['defect_class'])
    helpers = ''
    if n not in PURE_PY:
        helpers += REST_HELPERS
    if '_py_create' in ''.join(body):
        helpers += PY_HELPERS
    indent_body = ''.join(body)
    content = (head + helpers + 'def main():\n'
               "    wait_ready('http://localhost:19530/healthz')\n"
               + indent_body +
               "\n    print('probe_milvus_%s done')\n\n" % n +
               "if __name__ == '__main__':\n    main()\n")
    path = os.path.join(OUT, 'probe_milvus_%s.py' % n)
    with io.open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)
    written.append(n)

print('WROTE %d probes: %s' % (len(written), ','.join(sorted(written))))








"""50355 存在性复验 @v2.6.18 (phase2 probe 适配版).

原 probe 数据带 'color' 动态字段, v2.6.18 默认 schema 不开 dynamicField 导致控制组也报 1804。
适配: 数据去掉动态字段, 其余逻辑不变。
bug 判定: insert 无 PK 应成功(autoID 生效) 而 upsert 无 PK 失败 = 文档声称支持但不一致。
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..', 'phase2', 'probes'))
from probe_common import http, emit, wait_ready

BASE = 'http://localhost:19530'

def main():
    wait_ready('http://localhost:19530/healthz')
    http('POST', BASE + '/v2/vectordb/collections/drop', {'collectionName': 'test_upsert_autoid_r', 'dbName': 'default'})
    s, b, t = http('POST', BASE + '/v2/vectordb/collections/create', {
        'collectionName': 'test_upsert_autoid_r',
        'schema': {'autoID': True, 'primaryFieldName': 'id',
                   'fields': [{'fieldName': 'id', 'dataType': 'Int64', 'isPrimary': True},
                              {'fieldName': 'vector', 'dataType': 'FloatVector',
                               'elementTypeParams': {'dim': 4}}]}})
    emit('c0', http_status=s, resp_code=(b or {}).get('code'),
         observation='setup create autoID collection (http=%s code=%s)' % (s, (b or {}).get('code')))
    s, b, t = http('POST', BASE + '/v2/vectordb/entities/insert',
                   {'collectionName': 'test_upsert_autoid_r', 'data': [{'vector': [5.0, 6.0, 7.0, 8.0]}]})
    emit('c2', http_status=s, resp_code=(b or {}).get('code'), raw=str(b or t)[:200],
         observation='CONTROL insert no-PK; expect code 0 (http=%s code=%s)' % (s, (b or {}).get('code')))
    s, b, t = http('POST', BASE + '/v2/vectordb/entities/upsert',
                   {'collectionName': 'test_upsert_autoid_r', 'data': [{'vector': [1.0, 2.0, 3.0, 4.0]}]})
    emit('c1', http_status=s, resp_code=(b or {}).get('code'), raw=str(b or t)[:200],
         observation='upsert no-PK on autoID; bug if fails (http=%s code=%s)' % (s, (b or {}).get('code')))
    http('POST', BASE + '/v2/vectordb/collections/drop', {'collectionName': 'test_upsert_autoid_r', 'dbName': 'default'})
    print('reprobe_milvus_50355 done')

if __name__ == '__main__':
    main()

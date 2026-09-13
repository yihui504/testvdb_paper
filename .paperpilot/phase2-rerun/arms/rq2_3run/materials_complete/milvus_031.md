=== 候选缺陷 milvus_031 ===
[vendor=milvus version=2.6.17 defect_type=behavior endpoint=entities+upsert]
--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] upsert without PK on autoID collection -> http=200, code=1804
- [c2] control: insert without PK -> http=200, code=1804

执行日志全文（output_milvus_031.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_upsert_autoid", "dbName": "default"}
=== RESP 1 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_upsert_autoid", "dimension": 4, "metricType": "L2", "autoID": true, "schema": {"autoID": true, "primaryFieldName": "id", "fields": [{"fieldName": "id", "dataType": "Int64", "isPrimary": true}, {"fieldName": "vector", "dataType": "FloatVector", "elementTypeParams": {"dim": 4}}]}}
=== RESP 2 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/entities/upsert
payload: {"collectionName": "test_upsert_autoid", "data": [{"vector": [1.0, 2.0, 3.0, 4.0], "color": "red"}]}
=== RESP 3 ===
status: 200
body: {"code":1804,"message":"fail to deal the insert data, error: has pass more field without dynamic schema, please check it: invalid parameter"}

=== REQ 4 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_upsert_autoid", "data": [{"vector": [5.0, 6.0, 7.0, 8.0], "color": "blue"}]}
=== RESP 4 ===
status: 200
body: {"code":1804,"message":"fail to deal the insert data, error: has pass more field without dynamic schema, please check it: invalid parameter"}
--- 契约依据（expected，M3 重建版） ---
[经端点过滤与依据核查后，无 endpoint=entities+upsert 的可核查约束行]

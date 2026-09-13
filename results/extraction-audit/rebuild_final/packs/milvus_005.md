=== 候选缺陷 milvus_005 ===
[vendor=milvus version=2.6.10 defect_type=doc_mismatch endpoint=entities+insert]
--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] insert dynamic field names '123field'/'@field' -> http=200, code=0
- [c1_q] query field '123field' -> http=200, code=65535, message: parse output field name failed: 123field
- [c2] control: insert valid field name -> http=200, code=0
- [c2_q] control: query valid field -> http=200, code=101, message: collection not loaded

执行日志全文（output_milvus_005.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_<tracked>", "dbName": "default"}
=== RESP 1 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_<tracked>", "schema": {"autoID": false, "enableDynamicField": true, "fields": [{"fieldName": "id", "dataType": "Int64", "isPrimary": true}, {"fieldName": "vector", "dataType": "FloatVector", "elementTypeParams": {"dim": 4}}]}}
=== RESP 2 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_<tracked>", "data": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4], "123field": "v1"}, {"id": 2, "vector": [0.2, 0.2, 0.3, 0.4], "@field": "v2"}]}
=== RESP 3 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":2,"insertIds":[1,2]}}

=== REQ 4 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_<tracked>", "filter": "id in [1,2]", "outputFields": ["123field", "@field"]}
=== RESP 4 ===
status: 200
body: {"code":65535,"message":"parse output field name failed: 123field"}

=== REQ 5 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_<tracked>", "data": [{"id": 3, "vector": [0.3, 0.2, 0.3, 0.4], "valid_field": "ok"}]}
=== RESP 5 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":1,"insertIds":[3]}}

=== REQ 6 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_<tracked>", "filter": "id==3", "outputFields": ["valid_field"]}
=== RESP 6 ===
status: 200
body: {"code":101,"message":"failed to query: collection not loaded[collection=468359262963438392]"}

=== REQ 7 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_<tracked>", "dbName": "default"}
=== RESP 7 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 8 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_<tracked>", "schema": {"autoID": false, "enableDynamicField": true, "fields": [{"fieldName": "id", "dataType": "Int64", "isPrimary": true}, {"fieldName": "vector", "dataType": "FloatVector", "elementTypeParams": {"dim": 4}}]}}
=== RESP 8 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 9 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_<tracked>", "data": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4], "123field": "v1"}, {"id": 2, "vector": [0.2, 0.2, 0.3, 0.4], "@field": "v2"}]}
=== RESP 9 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":2,"insertIds":[1,2]}}

=== REQ 10 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_<tracked>", "filter": "id in [1,2]", "outputFields": ["123field", "@field"]}
=== RESP 10 ===
status: 200
body: {"code":65535,"message":"parse output field name failed: 123field"}

=== REQ 11 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_<tracked>", "data": [{"id": 3, "vector": [0.3, 0.2, 0.3, 0.4], "valid_field": "ok"}]}
=== RESP 11 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":1,"insertIds":[3]}}

=== REQ 12 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_<tracked>", "filter": "id==3", "outputFields": ["valid_field"]}
=== RESP 12 ===
status: 200
body: {"code":101,"message":"failed to query: collection not loaded[collection=468359683278836488]"}
--- 契约依据（expected，M3 重建版） ---
[经端点过滤与依据核查后，无 endpoint=entities+insert 的可核查约束行]

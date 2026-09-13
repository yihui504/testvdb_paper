=== 候选缺陷 milvus_006 ===
[vendor=milvus version=2.6.10 defect_type=type_coercion endpoint=entities+insert]
--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] insert int into VARCHAR dynamic field -> http=200, code=0
- [c1_q] query text_field -> http=200, code=0, data: id=1 text_field=hello, id=2 text_field=12345

执行日志全文（output_milvus_006.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_<tracked>", "dbName": "default"}
=== RESP 1 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_<tracked>", "dimension": 4}
=== RESP 2 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_<tracked>", "data": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4], "text_field": "hello"}]}
=== RESP 3 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":1,"insertIds":[1]}}

=== REQ 4 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_<tracked>", "data": [{"id": 2, "vector": [0.2, 0.2, 0.3, 0.4], "text_field": 12345}]}
=== RESP 4 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":1,"insertIds":[2]}}

=== REQ 5 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_<tracked>", "filter": "id in [1,2]", "outputFields": ["text_field"]}
=== RESP 5 ===
status: 200
body: {"code":0,"cost":0,"data":[{"id":1,"text_field":"hello"},{"id":2,"text_field":12345}]}


=== REQ 6 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_<tracked>", "dbName": "default"}
=== RESP 6 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 7 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_<tracked>", "dimension": 4}
=== RESP 7 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 8 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_<tracked>", "data": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4], "text_field": "hello"}]}
=== RESP 8 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":1,"insertIds":[1]}}

=== REQ 9 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_<tracked>", "data": [{"id": 2, "vector": [0.2, 0.2, 0.3, 0.4], "text_field": 12345}]}
=== RESP 9 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":1,"insertIds":[2]}}

=== REQ 10 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_<tracked>", "filter": "id in [1,2]", "outputFields": ["text_field"]}
=== RESP 10 ===
status: 200
body: {"code":0,"cost":0,"data":[{"id":1,"text_field":"hello"},{"id":2,"text_field":12345}]}
--- 契约依据（expected，M3 重建版） ---
[经端点过滤与依据核查后，无 endpoint=entities+insert 的可核查约束行]

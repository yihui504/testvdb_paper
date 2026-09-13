=== 候选缺陷 milvus_039 ===
[vendor=milvus version=3.0.0 defect_type=type_coercion endpoint=entities+upsert]
--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] REST upsert string PK '100' -> http=200, code=0
- [c1_q] query id=100 after string-PK upsert -> http=200, code=0, data: id=100 vector=[0.9,0.9,0.9,0.9]
- [c1_grpc] gRPC upsert string PK -> DataNotMatchException code=1, message: id field should be int64, got str

执行日志全文（output_milvus_039.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_upsert_pk", "dbName": "default"}
=== RESP 1 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_upsert_pk", "dimension": 4}
=== RESP 2 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_upsert_pk", "data": [{"id": 100, "vector": [0.1, 0.2, 0.3, 0.4]}]}
=== RESP 3 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":1,"insertIds":[100]}}

=== REQ 4 ===
POST http://localhost:19530/v2/vectordb/entities/upsert
payload: {"collectionName": "test_upsert_pk", "data": [{"id": "100", "vector": [0.9, 0.9, 0.9, 0.9]}]}
=== RESP 4 ===
status: 200
body: {"code":0,"cost":0,"data":{"upsertCount":1,"upsertIds":[100]}}

=== REQ 5 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_upsert_pk", "filter": "id==100", "outputFields": ["id", "vector"]}
=== RESP 5 ===
status: 200
body: {"code":0,"cost":0,"data":[{"id":100,"vector":[0.9,0.9,0.9,0.9]}]}


=== REQ 6 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_upsert_pk", "dbName": "default"}
=== RESP 6 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 7 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_upsert_pk", "dimension": 4}
=== RESP 7 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 8 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_upsert_pk", "data": [{"id": 100, "vector": [0.1, 0.2, 0.3, 0.4]}]}
=== RESP 8 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":1,"insertIds":[100]}}

=== REQ 9 ===
POST http://localhost:19530/v2/vectordb/entities/upsert
payload: {"collectionName": "test_upsert_pk", "data": [{"id": "100", "vector": [0.9, 0.9, 0.9, 0.9]}]}
=== RESP 9 ===
status: 200
body: {"code":0,"cost":0,"data":{"upsertCount":1,"upsertIds":[100]}}

=== REQ 10 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_upsert_pk", "filter": "id==100", "outputFields": ["id", "vector"]}
=== RESP 10 ===
status: 200
body: {"code":0,"cost":0,"data":[{"id":100,"vector":[0.9,0.9,0.9,0.9]}]}
--- 契约依据（expected，M3 重建版） ---
{"constraint_id": "milvus_upsert_schema_match_001", "endpoint": "entities+upsert", "description": "data must match collection schema (page verbatim)", "assertion": "\"the keys in an entity object should match the collection schema\" (schema declares id Int64)", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Vector%20(v2)/Upsert.md", "source_type": "documentation", "evidence_tier": "explicit"}

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




--- 契约依据（expected，来自该版本 API 契约） ---
[契约中无 endpoint=entities+upsert 的约束条目]

相关契约段（关键词定位 4 条）：
{"endpoint": "collection+create", "kind": "state_constraints", "description": "Primary key constraint", "assertion": "Exactly one primary field per collection with type Int64 or VarChar", "source_url": "https://milvus.io/docs/schema.md", "confidence": 0.95}
{"endpoint": "collections+fields+add", "kind": "type_constraints", "description": "INT64 scalar data type", "assertion": "dataType == Int64", "source_url": "https://milvus.io/docs/schema.md", "confidence": 1.0}
{"endpoint": "collection+create", "kind": "type_constraints", "description": "Valid dataType value: INT64", "assertion": "dataType == 'INT64'", "source_url": "https://milvus.io/docs/schema.md", "confidence": 0.95}
{"endpoint": "collections+create", "kind": "assertion", "description": "Primary key must be Int64 or VarChar", "source_url": "https://milvus.io/docs/schema.md", "confidence": 1.0}

API 模板：endpoint=entities+insert doc_quote='Insert entities' source=None

VERDICT: UNKNOWN (replay capture — no attack-agent assertion output; raw HTTP only)

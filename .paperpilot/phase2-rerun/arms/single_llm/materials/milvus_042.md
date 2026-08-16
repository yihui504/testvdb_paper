=== 候选缺陷 milvus_042 ===
[vendor=milvus version=3.0.0 defect_type=type_coercion endpoint=entities+insert]

--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] REST insert string-encoded vector -> http=200, code=0
- [c1_s] search after string-vector insert -> http=200, code=0, data: id=0 distance=1
- [c1_grpc] gRPC insert string vector -> DataNotMatchException code=1, message: vector field should be float_vector, got str

执行日志全文（output_milvus_042.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_vec_str", "dbName": "default"}
=== RESP 1 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_vec_str", "dimension": 4}
=== RESP 2 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_vec_str", "data": [{"id": 0, "vector": "[0.1,0.2,0.3,0.4]"}]}
=== RESP 3 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":1,"insertIds":[0]}}

=== REQ 4 ===
POST http://localhost:19530/v2/vectordb/entities/search
payload: {"collectionName": "test_vec_str", "data": [[0.1, 0.2, 0.3, 0.4]], "annsField": "vector", "limit": 5, "outputFields": ["id"]}
=== RESP 4 ===
status: 200
body: {"code":0,"cost":0,"data":[{"distance":1,"id":0}],"topks":[1]}


=== REQ 5 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_vec_str", "dbName": "default"}
=== RESP 5 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 6 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_vec_str", "dimension": 4}
=== RESP 6 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 7 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_vec_str", "data": [{"id": 0, "vector": "[0.1,0.2,0.3,0.4]"}]}
=== RESP 7 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":1,"insertIds":[0]}}

=== REQ 8 ===
POST http://localhost:19530/v2/vectordb/entities/search
payload: {"collectionName": "test_vec_str", "data": [[0.1, 0.2, 0.3, 0.4]], "annsField": "vector", "limit": 5, "outputFields": ["id"]}
=== RESP 8 ===
status: 200
body: {"code":0,"cost":0,"data":[{"distance":1,"id":0}],"topks":[1]}




--- 契约依据（expected，来自该版本 API 契约） ---
约束条目（3 条，来自 milvus 3.0.0 契约，endpoint=entities+insert）：
{"constraint_id": "milvus_state_insert_collection_001", "endpoint": "entities+insert", "type": "state_constraint", "description": "Insert requires existing collection", "assertion": "collection MUST exist before insert", "source_url": "https://milvus.io/docs/schema.md", "confidence": 1.0}
{"assertion_id": "milvus_behavioral_insert_then_get_001", "endpoint": "entities+insert", "description": "Inserted entities should be retrievable", "source_url": "https://milvus.io/docs/insert-update.md", "confidence": 1.0}
{"assertion_id": "milvus_assert_insert_success_001", "endpoint": "entities+insert", "description": "Inserting valid data succeeds", "source_url": "https://milvus.io/docs/schema.md", "confidence": 1.0}

API 模板：endpoint=entities+insert doc_quote='Insert entities' source=None

VERDICT: UNKNOWN (replay capture — no attack-agent assertion output; raw HTTP only)

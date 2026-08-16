=== 候选缺陷 milvus_040 ===
[vendor=milvus version=3.0.0 defect_type=semantics endpoint=entities+insert]

--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] REST insert plain-string into JSON field -> http=200, code=0
- [c2] gRPC insert plain string -> DataNotMatchException code=1, message: Invalid JSON string
- [c_q] query meta -> http=200, code=0, data: id=100 meta=plain_string
- [c_grpc_get] gRPC get -> error: unexpected character (REST-written value unreadable)

执行日志全文（output_milvus_040.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "repro_<tracked>", "dbName": "default"}
=== RESP 1 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "repro_<tracked>", "dbName": "default", "schema": {"autoId": false, "enableDynamicField": false, "fields": [{"fieldName": "id", "dataType": "Int64", "isPrimary": true}, {"fieldName": "vector", "dataType": "FloatVector", "elementTypeParams": {"dim": 4}}, {"fieldName": "meta", "dataType": "JSON"}]}}
=== RESP 2 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/indexes/create
payload: {"collectionName": "repro_<tracked>", "dbName": "default", "indexParams": [{"fieldName": "vector", "metricType": "COSINE", "indexType": "AUTOINDEX"}]}
=== RESP 3 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 4 ===
POST http://localhost:19530/v2/vectordb/collections/load
payload: {"collectionName": "repro_<tracked>", "dbName": "default"}
=== RESP 4 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 5 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "repro_<tracked>", "dbName": "default", "data": [{"id": 100, "vector": [0.1, 0.2, 0.3, 0.4], "meta": "plain_string"}]}
=== RESP 5 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":1,"insertIds":[100]}}



--- 契约依据（expected，来自该版本 API 契约） ---
约束条目（3 条，来自 milvus 3.0.0 契约，endpoint=entities+insert）：
{"constraint_id": "milvus_state_insert_collection_001", "endpoint": "entities+insert", "type": "state_constraint", "description": "Insert requires existing collection", "assertion": "collection MUST exist before insert", "source_url": "https://milvus.io/docs/schema.md", "confidence": 1.0}
{"assertion_id": "milvus_behavioral_insert_then_get_001", "endpoint": "entities+insert", "description": "Inserted entities should be retrievable", "source_url": "https://milvus.io/docs/insert-update.md", "confidence": 1.0}
{"assertion_id": "milvus_assert_insert_success_001", "endpoint": "entities+insert", "description": "Inserting valid data succeeds", "source_url": "https://milvus.io/docs/schema.md", "confidence": 1.0}

相关契约段（关键词定位 3 条）：
{"endpoint": "collections+fields+add", "kind": "type_constraints", "description": "JSON scalar data type", "assertion": "dataType == JSON", "source_url": "https://milvus.io/docs/schema.md", "confidence": 1.0}
{"endpoint": "collection+create", "kind": "type_constraints", "description": "Supported data type: JSON", "assertion": "dataType == 'JSON'", "source_url": "https://milvus.io/docs/schema.md", "confidence": 0.95}
{"endpoint": "collection+create", "kind": "type_constraints", "description": "Valid dataType value: JSON", "assertion": "dataType == 'JSON'", "source_url": "https://milvus.io/docs/schema.md", "confidence": 0.95}

API 模板：endpoint=entities+insert doc_quote='Insert entities' source=None

VERDICT: UNKNOWN (replay capture — no attack-agent assertion output; raw HTTP only)

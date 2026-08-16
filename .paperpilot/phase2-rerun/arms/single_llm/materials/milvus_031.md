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



--- 契约依据（expected，来自该版本 API 契约） ---
约束条目（8 条，来自 milvus 2.6.17 契约，endpoint=entities+upsert）：
{"constraint_id": "milvus_type_entities_delete_001", "endpoint": "entities+delete", "type": "type_constraint", "description": "filter must be a valid boolean expression string", "assertion": "filter is a valid boolean expression", "source_url": "https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go", "confidence": 1.0}
{"constraint_id": "milvus_type_entities_get_001", "endpoint": "entities+get", "type": "type_constraint", "description": "id must match the collection primary key type (Int64 or VarChar)", "assertion": "id type matches collection primary key type", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Vector%20(v2)/Get.md", "confidence": 1.0}
{"constraint_id": "milvus_type_entities_upsert_001", "endpoint": "entities+upsert", "type": "type_constraint", "description": "Primary key field must be specified in data for upsert", "assertion": "data contains primary key field", "source_url": "https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go", "confidence": 1.0}
{"constraint_id": "milvus_state_entities_upsert_001", "endpoint": "entities+upsert", "type": "state_constraint", "description": "If primary key exists, entity is updated; if not, inserted. Collection must have a primary key defined", "assertion": "upsert: update if PK exists, insert if NOT; collection has PK defined", "source_url": "https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go", "confidence": 1.0}
{"constraint_id": "milvus_state_entities_delete_001", "endpoint": "entities+delete", "type": "state_constraint", "description": "Deleted entities cannot be recovered", "assertion": "delete is irreversible", "source_url": "https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go", "confidence": 1.0}
{"constraint_id": "milvus_state_entities_upsert_002", "endpoint": "entities+upsert", "type": "state_constraint", "description": "Primary key must match existing entity's key for updates", "assertion": "for updates: PK value matches existing entity PK", "source_url": "https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go", "confidence": 0.8}
{"assertion_id": "milvus_behavioral_entities_delete_001", "endpoint": "entities+delete", "description": "Delete returns 400 on invalid filter expression", "source_url": "https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go", "confidence": 1.0}
{"assertion_id": "milvus_behavioral_entities_get_001", "endpoint": "entities+get", "description": "Get entities returns 400 if id type mismatches collection schema", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Vector%20(v2)/Get.md", "confidence": 1.0}

相关契约段（关键词定位 1 条）：
{"endpoint": "entities+insert", "kind": "state_constraints", "description": "Collection must exist and be loaded; if autoID is disabled, primary key must be provided", "assertion": "collection exists AND is loaded AND (autoID OR primary key provided)", "source_url": "https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go", "confidence": 1.0}

VERDICT: UNKNOWN (replay capture — no attack-agent assertion output; raw HTTP only)

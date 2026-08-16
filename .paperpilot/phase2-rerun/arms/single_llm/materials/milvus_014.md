=== 候选缺陷 milvus_014 ===
[vendor=milvus version=2.6.16 defect_type=behavior endpoint=collections+create]

--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] create collection with dim=32768 -> http=200, code=0
- [c2] control: create with dim=32769 -> http=200, code=65535

执行日志全文（output_milvus_014.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_large_dim", "dbName": "default"}
=== RESP 1 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_large_dim2", "dbName": "default"}
=== RESP 2 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_large_dim", "schema": {"autoID": false, "enableDynamicField": true, "fields": [{"fieldName": "id", "dataType": "Int64", "isPrimary": true}, {"fieldName": "vector", "dataType": "FloatVector", "elementTypeParams": {"dim": 32768}}]}}
=== RESP 3 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 4 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_large_dim2", "schema": {"autoID": false, "enableDynamicField": true, "fields": [{"fieldName": "id", "dataType": "Int64", "isPrimary": true}, {"fieldName": "vector", "dataType": "FloatVector", "elementTypeParams": {"dim": 32769}}]}}
=== RESP 4 ===
status: 200
body: {"code":65535,"message":"invalid dimension: 32769 of field vector. float vector dimension should be in range 2 ~ 32768"}

=== REQ 5 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_large_dim", "dbName": "default"}
=== RESP 5 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 6 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_large_dim2", "dbName": "default"}
=== RESP 6 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 7 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_large_dim", "schema": {"autoID": false, "enableDynamicField": true, "fields": [{"fieldName": "id", "dataType": "Int64", "isPrimary": true}, {"fieldName": "vector", "dataType": "FloatVector", "elementTypeParams": {"dim": 32768}}]}}
=== RESP 7 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 8 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_large_dim2", "schema": {"autoID": false, "enableDynamicField": true, "fields": [{"fieldName": "id", "dataType": "Int64", "isPrimary": true}, {"fieldName": "vector", "dataType": "FloatVector", "elementTypeParams": {"dim": 32769}}]}}
=== RESP 8 ===
status: 200
body: {"code":65535,"message":"invalid dimension: 32769 of field vector. float vector dimension should be in range 2 ~ 32768"}



--- 契约依据（expected，来自该版本 API 契约） ---
约束条目（11 条，来自 milvus 2.6.16 契约，endpoint=collections+create）：
{"constraint_id": "milvus_type_collections_create_001", "endpoint": "collections+create", "type": "type_constraint", "description": "collectionName must be a string", "assertion": "collectionName is of type string", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "confidence": 1.0}
{"constraint_id": "milvus_type_collections_create_002", "endpoint": "collections+create", "type": "type_constraint", "description": "metricType must be L2, IP, or COSINE", "assertion": "metricType in [L2, IP, COSINE]", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "confidence": 1.0}
{"constraint_id": "milvus_type_collections_create_003", "endpoint": "collections+create", "type": "type_constraint", "description": "consistencyLevel must be Strong, Session, Bounded, or Eventually", "assertion": "consistencyLevel in [Strong, Session, Bounded, Eventually]", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "confidence": 1.0}
{"constraint_id": "milvus_range_collections_create_001", "endpoint": "collections+create", "type": "range_constraint", "description": "dimension must be 1-32768 for FloatVector", "assertion": "1 <= dimension <= 32768", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "confidence": 1.0}
{"constraint_id": "milvus_range_collections_create_002", "endpoint": "collections+create", "type": "range_constraint", "description": "shardsNum must be >= 1", "assertion": "shardsNum >= 1", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "confidence": 1.0}
{"constraint_id": "milvus_range_collections_create_003", "endpoint": "collections+create", "type": "range_constraint", "description": "partitionsNum >= 1", "assertion": "partitionsNum >= 1", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "confidence": 1.0}
{"constraint_id": "milvus_range_collections_create_004", "endpoint": "collections+create", "type": "range_constraint", "description": "ttlSeconds must be >= 0", "assertion": "ttlSeconds >= 0", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "confidence": 1.0}
{"constraint_id": "milvus_range_collections_create_005", "endpoint": "collections+create", "type": "range_constraint", "description": "VarChar max_length must be 1-65535", "assertion": "1 <= VarChar.max_length <= 65535", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "confidence": 1.0}
{"constraint_id": "milvus_state_collections_create_001", "endpoint": "collections+create", "type": "state_constraint", "description": "Collection creation is atomic; collection names are unique within a database, and re-creation is idempotent when the schema is unchanged", "assertion": "collection creation is atomic AND collectionName is unique within dbName; re-creating an existing collection with the SAME schema is an idempotent no-op returning 200, re-creating with a DIFFERENT schema returns an error", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "confidence": 1.0}
{"assertion_id": "milvus_behavioral_collections_create_001", "endpoint": "collections+create", "description": "Create collection returns 200 on success", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "confidence": 1.0}
{"assertion_id": "milvus_behavioral_collections_create_002", "endpoint": "collections+create", "description": "Create collection returns 400 on invalid parameters; duplicate name is not an error when the schema is unchanged (idempotent no-op)", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "confidence": 1.0}

相关契约段（关键词定位 1 条）：
{"endpoint": "collections+create", "kind": "state_constraints", "description": "Collection creation is atomic; collection name must be unique within a database", "assertion": "collection creation is atomic AND collectionName is unique within dbName", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "confidence": 1.0}

API 模板：endpoint=users+create doc_quote='200 on success; 400 if user already exists or password too weak' source=None

VERDICT: UNKNOWN (replay capture — no attack-agent assertion output; raw HTTP only)

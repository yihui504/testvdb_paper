=== 候选缺陷 milvus_028 ===
[vendor=milvus version=2.6.17 defect_type=param_validation endpoint=collections+create]
--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] create with metricType=empty -> http=200, code=0
- [c2] create with consistencyLevel=None -> http=200, code=0
- [c3] create with dimension=32769 -> http=200, code=65535

执行日志全文（output_milvus_028.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_mt_empty", "dbName": "default"}
=== RESP 1 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_cl_none", "dbName": "default"}
=== RESP 2 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_dim_high", "dbName": "default"}
=== RESP 3 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 4 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_mt_empty", "dimension": 4, "metricType": ""}
=== RESP 4 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 5 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_cl_none", "dimension": 4, "metricType": "L2", "consistencyLevel": "None"}
=== RESP 5 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 6 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_dim_high", "dimension": 32769, "metricType": "COSINE"}
=== RESP 6 ===
status: 200
body: {"code":65535,"message":"invalid dimension: 32769 of field vector. float vector dimension should be in range 2 ~ 32768"}
--- 契约依据（expected，M3 重建版） ---
{"constraint_id": "milvus_type_collections_create_001", "endpoint": "collections+create", "type": "type_constraint", "description": "collectionName must be a string", "assertion": "collectionName is of type string", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "confidence": 1.0, "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "milvus_type_collections_create_002", "endpoint": "collections+create", "type": "type_constraint", "description": "metricType must be L2, IP, or COSINE", "assertion": "metricType in [L2, IP, COSINE]", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "confidence": 1.0, "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "milvus_type_collections_create_003", "endpoint": "collections+create", "type": "type_constraint", "description": "consistencyLevel must be Strong, Session, Bounded, or Eventually", "assertion": "consistencyLevel in [Strong, Session, Bounded, Eventually]", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "confidence": 1.0, "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}
{"assertion_id": "milvus_behavioral_collections_create_001", "endpoint": "collections+create", "description": "Create collection returns 200 on success", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "confidence": 1.0, "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}
{"assertion_id": "milvus_behavioral_collections_create_001", "endpoint": "collections+create", "description": "Create collection returns 200 on success", "category": "behavioral", "expected_behavior": "returns 200 with code: 0 and empty data object", "confidence": 1.0, "defect_type_if_violated": "Type1_IllegalSuccess", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "doc_version": "2.6.x", "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "milvus_type_collections_create_001", "endpoint": "collections+create", "description": "collectionName must be a string", "assertion": "collectionName is of type string", "type": "type_constraint", "confidence": 1.0, "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "source_status": "reachable", "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "milvus_type_collections_create_003", "endpoint": "collections+create", "description": "consistencyLevel must be Strong, Session, Bounded, or Eventually", "assertion": "consistencyLevel in [Strong, Session, Bounded, Eventually]", "type": "type_constraint", "confidence": 1.0, "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "source_status": "reachable", "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}
VERDICT: UNKNOWN (replay capture — no attack-agent assertion output; raw HTTP only)

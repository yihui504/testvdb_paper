=== 候选缺陷 milvus_010 ===
[vendor=milvus version=2.6.16 defect_type=semantics endpoint=collections+create]
--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] create with negative TTL -> http=200, code=0
- [c1_rb] describe collection after negative-TTL create -> http=200
- [c2] control: alter_properties with negative TTL -> http=200, code=1100

执行日志全文（output_milvus_010.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_ttl_neg", "dbName": "default"}
=== RESP 1 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_ttl_neg", "dimension": 4, "metricType": "L2", "properties": {"collection.ttl.seconds": -100}}
=== RESP 2 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/collections/describe
payload: {"collectionName": "test_ttl_neg", "dbName": "default"}
=== RESP 3 ===
status: 200
body: {"code":0,"data":{"aliases":[],"autoId":false,"collectionID":468358976047044489,"collectionName":"test_ttl_neg","consistencyLevel":"Bounded","description":"","enableDynamicField":true,"fields":[{"autoId":false,"clusteringKey":false,"description":"","id":100,"name":"id","nullable":false,"partitionKey":false,"primaryKey":true,"type":"Int64"},{"autoId":false,"clusteringKey":false,"description":"","id":101,"name":"vector","nullable":false,"params":[{"key":"dim","value":"4"}],"partitionKey":false,"primaryKey":false,"type":"FloatVector"}],"functions":[],"indexes":[{"fieldName":"vector","indexName":"vector","metricType":"L2"}],"load":"LoadStateLoading","partitionsNum":1,"properties":[{"key":"timezone","value":"UTC"}],"shardsNum":1},"message":""}

=== REQ 4 ===
POST http://localhost:19530/v2/vectordb/collections/alter_properties
payload: {"collectionName": "test_ttl_neg", "properties": {"collection.ttl.seconds": -100}}
=== RESP 4 ===
status: 200
body: {"code":1100,"message":"collection TTL is out of range, expect [-1, 3155760000], got -100: invalid parameter"}

=== REQ 5 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_ttl_neg", "dbName": "default"}
=== RESP 5 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 6 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_ttl_neg", "dimension": 4, "metricType": "L2", "properties": {"collection.ttl.seconds": -100}}
=== RESP 6 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 7 ===
POST http://localhost:19530/v2/vectordb/collections/describe
payload: {"collectionName": "test_ttl_neg", "dbName": "default"}
=== RESP 7 ===
status: 200
body: {"code":0,"data":{"aliases":[],"autoId":false,"collectionID":468359796041078668,"collectionName":"test_ttl_neg","consistencyLevel":"Bounded","description":"","enableDynamicField":true,"fields":[{"autoId":false,"clusteringKey":false,"description":"","id":100,"name":"id","nullable":false,"partitionKey":false,"primaryKey":true,"type":"Int64"},{"autoId":false,"clusteringKey":false,"description":"","id":101,"name":"vector","nullable":false,"params":[{"key":"dim","value":"4"}],"partitionKey":false,"primaryKey":false,"type":"FloatVector"}],"functions":[],"indexes":[{"fieldName":"vector","indexName":"vector","metricType":"L2"}],"load":"LoadStateLoading","partitionsNum":1,"properties":[{"key":"timezone","value":"UTC"}],"shardsNum":1},"message":""}

=== REQ 8 ===
POST http://localhost:19530/v2/vectordb/collections/alter_properties
payload: {"collectionName": "test_ttl_neg", "properties": {"collection.ttl.seconds": -100}}
=== RESP 8 ===
status: 200
body: {"code":1100,"message":"collection TTL is out of range, expect [-1, 3155760000], got -100: invalid parameter"}
--- 契约依据（expected，M3 重建版） ---
{"constraint_id": "milvus_type_collections_create_001", "endpoint": "collections+create", "type": "type_constraint", "description": "collectionName must be a string", "assertion": "collectionName is of type string", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "confidence": 1.0, "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "milvus_type_collections_create_002", "endpoint": "collections+create", "type": "type_constraint", "description": "metricType must be L2, IP, or COSINE", "assertion": "metricType in [L2, IP, COSINE]", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "confidence": 1.0, "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "milvus_type_collections_create_003", "endpoint": "collections+create", "type": "type_constraint", "description": "consistencyLevel must be Strong, Session, Bounded, or Eventually", "assertion": "consistencyLevel in [Strong, Session, Bounded, Eventually]", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "confidence": 1.0, "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}
{"assertion_id": "milvus_behavioral_collections_create_001", "endpoint": "collections+create", "description": "Create collection returns 200 on success", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "confidence": 1.0, "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}
{"assertion_id": "milvus_behavioral_collections_create_001", "endpoint": "collections+create", "description": "Create collection returns 200 on success", "category": "behavioral", "expected_behavior": "returns 200 with code: 0 and empty data object", "confidence": 1.0, "defect_type_if_violated": "Type1_IllegalSuccess", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "doc_version": "2.6.x", "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "milvus_type_collections_create_001", "endpoint": "collections+create", "description": "collectionName must be a string", "assertion": "collectionName is of type string", "type": "type_constraint", "confidence": 1.0, "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "source_status": "reachable", "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "milvus_type_collections_create_003", "endpoint": "collections+create", "description": "consistencyLevel must be Strong, Session, Bounded, or Eventually", "assertion": "consistencyLevel in [Strong, Session, Bounded, Eventually]", "type": "type_constraint", "confidence": 1.0, "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "source_status": "reachable", "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}
VERDICT: UNKNOWN (replay capture — no attack-agent assertion output; raw HTTP only)

=== 候选缺陷 milvus_023 ===
[vendor=milvus version=2.6.17 defect_type=behavior endpoint=collections+drop]

--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] drop non-existent collection -> http=200, code=0

执行日志全文（output_milvus_023.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "nonexistent_collection_xyz", "dbName": "default"}
=== RESP 1 ===
status: 200
body: {"code":0,"data":{}}



--- 契约依据（expected，来自该版本 API 契约） ---
约束条目（3 条，来自 milvus 2.6.17 契约，endpoint=collections+drop）：
{"constraint_id": "milvus_type_collections_drop_001", "endpoint": "collections+drop", "type": "type_constraint", "description": "collectionName must be a non-empty string", "assertion": "collectionName is non-empty string", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Drop.md", "confidence": 1.0}
{"constraint_id": "milvus_state_collections_drop_001", "endpoint": "collections+drop", "type": "state_constraint", "description": "Drop is irreversible; all data in the collection is permanently deleted", "assertion": "drop is irreversible AND all data is permanently deleted", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Drop.md", "confidence": 1.0}
{"assertion_id": "milvus_behavioral_collections_drop_001", "endpoint": "collections+drop", "description": "Drop collection returns 200 on success; dropping a non-existent collection is treated as idempotent success (200, empty data)", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Drop.md", "confidence": 1.0}

相关契约段（关键词定位 4 条）：
{"endpoint": "collections+drop", "kind": "type_constraints", "description": "collectionName must be a non-empty string", "assertion": "collectionName is non-empty string", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Drop.md", "confidence": 1.0}
{"endpoint": "collections+load", "kind": "type_constraints", "description": "collectionName must be a non-empty string for load", "assertion": "collectionName is non-empty string", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Load.md", "confidence": 1.0}
{"endpoint": "collections+rename", "kind": "type_constraints", "description": "collectionName and newCollectionName must be non-empty strings", "assertion": "collectionName is non-empty string AND newCollectionName is non-empty string", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Rename.md", "confidence": 1.0}
{"endpoint": "partitions+create", "kind": "type_constraints", "description": "partitionName must be a non-empty string", "assertion": "partitionName is non-empty string", "source_url": "https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go", "confidence": 1.0}

VERDICT: UNKNOWN (replay capture — no attack-agent assertion output; raw HTTP only)

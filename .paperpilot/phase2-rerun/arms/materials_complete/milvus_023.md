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
--- 契约依据（expected，M3 重建版） ---
{"constraint_id": "milvus_type_collections_drop_001", "endpoint": "collections+drop", "type": "type_constraint", "description": "collectionName must be a non-empty string", "assertion": "collectionName is non-empty string", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Drop.md", "confidence": 1.0, "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}
{"endpoint": "collections+drop", "kind": "type_constraints", "description": "collectionName must be a non-empty string", "assertion": "collectionName is non-empty string", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "confidence": 1.0, "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "milvus_type_collections_drop_001", "endpoint": "collections+drop", "description": "collectionName must be a non-empty string", "assertion": "collectionName is non-empty string", "type": "type_constraint", "confidence": 1.0, "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Drop.md", "source_status": "reachable", "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}

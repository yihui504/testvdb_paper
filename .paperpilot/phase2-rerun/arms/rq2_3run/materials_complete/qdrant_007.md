=== 候选缺陷 qdrant_007 ===
[vendor=qdrant version=1.18.2 defect_type=behavior endpoint=collections+{collection_name}+points+batch]
--- 观察到的行为（observed） ---

执行日志全文（output_qdrant_007.log）：
=== REQ 1 ===
DELETE http://localhost:6333/collections/test_batch2
=== RESP 1 ===
status: 200
body: {"result":false,"status":"ok","time":0.001802436}

=== REQ 2 ===
PUT http://localhost:6333/collections/test_batch2
payload: {"vectors": {"size": 4, "distance": "Cosine"}}
=== RESP 2 ===
status: 200
body: {"result":true,"status":"ok","time":0.313413442}

=== REQ 3 ===
PUT http://localhost:6333/collections/test_batch2/points?wait=true
payload: {"points": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 2, "vector": [0.5, 0.6, 0.7, 0.8]}, {"id": 3, "vector": [0.9, 0.9, 0.9, 0.9]}]}
=== RESP 3 ===
status: 200
body: {"result":{"operation_id":1,"status":"completed"},"status":"ok","time":0.00865381}

=== REQ 4 ===
POST http://localhost:6333/collections/test_batch2/points/count
payload: {"exact": true}
=== RESP 4 ===
status: 200
body: {"result":{"count":3},"status":"ok","time":0.001314561}

=== REQ 5 ===
POST http://localhost:6333/collections/test_batch2/points/batch
payload: {"operations": [{"upsert": {"points": [{"id": 4, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 5, "vector": [0.5, 0.6, 0.7, 0.8]}, {"id": 6, "vector": [0.1, 0.2, 0.3]}]}}]}
=== RESP 5 ===
status: 400
body: {"status":{"error":"Wrong input: Vector dimension error: expected dim: 4, got 3"},"time":0.000021096}

=== REQ 6 ===
POST http://localhost:6333/collections/test_batch2/points/count
payload: {"exact": true}
=== RESP 6 ===
status: 200
body: {"result":{"count":3},"status":"ok","time":0.000092489}

=== REQ 7 ===
DELETE http://localhost:6333/collections/test_batch2
=== RESP 7 ===
status: 200
body: {"result":false,"status":"ok","time":0.000070651}

=== REQ 8 ===
PUT http://localhost:6333/collections/test_batch2
payload: {"vectors": {"size": 4, "distance": "Cosine"}}
=== RESP 8 ===
status: 200
body: {"result":true,"status":"ok","time":0.289524464}

=== REQ 9 ===
PUT http://localhost:6333/collections/test_batch2/points?wait=true
payload: {"points": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 2, "vector": [0.5, 0.6, 0.7, 0.8]}, {"id": 3, "vector": [0.9, 0.9, 0.9, 0.9]}]}
=== RESP 9 ===
status: 200
body: {"result":{"operation_id":1,"status":"completed"},"status":"ok","time":0.003470479}

=== REQ 10 ===
POST http://localhost:6333/collections/test_batch2/points/count
payload: {"exact": true}
=== RESP 10 ===
status: 200
body: {"result":{"count":3},"status":"ok","time":0.00014049}

=== REQ 11 ===
POST http://localhost:6333/collections/test_batch2/points/batch
payload: {"operations": [{"upsert": {"points": [{"id": 4, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 5, "vector": [0.5, 0.6, 0.7, 0.8]}, {"id": 6, "vector": [0.1, 0.2, 0.3]}]}}]}
=== RESP 11 ===
status: 400
body: {"status":{"error":"Wrong input: Vector dimension error: expected dim: 4, got 3"},"time":0.00001256}

=== REQ 12 ===
POST http://localhost:6333/collections/test_batch2/points/count
payload: {"exact": true}
=== RESP 12 ===
status: 200
body: {"result":{"count":3},"status":"ok","time":0.000164095}
--- 契约依据（expected，M3 重建版） ---
{"constraint_id": "qdrant_type_create_collection_001", "endpoint": "collections+{collection_name}", "type": "type_constraint", "description": "collection_name is string", "assertion": "collection_name type is string", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_type_update_collection_002", "endpoint": "collections+{collection_name}", "type": "type_constraint", "description": "All update fields are optional; at least one must be provided", "assertion": "At least one update field must be provided.", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_type_upsert_points_003", "endpoint": "collections+{collection_name}+points", "type": "type_constraint", "description": "id is integer (uint64) or UUID string; vector is array of floats or object of named vectors; payload is key-value object", "assertion": "id type is integer (uint64) or UUID string; vector type is array of floats or object of named vectors; payload type is key-value object.", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_range_create_collection_001", "endpoint": "collections+{collection_name}", "type": "range_constraint", "description": "shard_number minimum=1", "assertion": "shard_number >= 1", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_range_create_collection_002", "endpoint": "collections+{collection_name}", "type": "range_constraint", "description": "replication_factor minimum=1", "assertion": "replication_factor >= 1", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_state_update_collection_002", "endpoint": "collections+{collection_name}", "type": "state_constraint", "description": "Blocking operation - waits for current optimizations to complete", "assertion": "Update blocks until current optimizations complete.", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 0.9, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_state_delete_collection_003", "endpoint": "collections+{collection_name}", "type": "state_constraint", "description": "Destructive operation - permanently deletes collection and all its data", "assertion": "Collection deletion permanently removes the collection and all its data.", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"assertion_id": "qdrant_behavioral_003", "endpoint": "collections+{collection_name}", "description": "200 with collection info; 404 if not found", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"assertion_id": "qdrant_behavioral_017", "endpoint": "collections", "description": "200 with list of collections", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"endpoint": "collections+{collection_name}+points+batch", "kind": "state_constraints", "description": "All operations in batch are executed atomically", "assertion": "Batch update operations are executed atomically.", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"endpoint": "collections+{collection_name}", "kind": "state_constraints", "description": "Atomic collection creation: after 200 response, collection is fully initialized and ready for operations", "assertion": "Atomic collection creation. After 200 response, collection is fully initialized and ready for operations.", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_type_upsert_points_003", "endpoint": "collections+{collection_name}+points", "description": "id is integer (uint64) or UUID string; vector is array of floats or object of named vectors; payload is key-value object", "assertion": "id type is integer (uint64) or UUID string; vector type is array of floats or object of named vectors; payload type is key-value object.", "type": "type_constraint", "confidence": 1.0, "evidence_tier": "inferred_from_behavior", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "source_status": "reachable", "doc_version": "1.18.x", "source_verified": true, "source_type": "structured-spec"}

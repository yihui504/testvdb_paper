=== 候选缺陷 qdrant_015 ===
[vendor=qdrant version=1.18.2 defect_type=crash endpoint=collections+{collection_name}]
--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] create with shard_number=INT_MAX -> status=None (read timeout)
- [server_health] GET / after INT_MAX create -> status=200
- [c2] control: create with replication_factor=0 -> status=422, body: replication_factor: value 0 invalid, must be 1 or larger

执行日志全文（output_qdrant_015.log）：
=== REQ 1 ===
DELETE http://localhost:6333/collections/test_shard_max
=== RESP 1 ===
status: 200
body: {"result":false,"status":"ok","time":0.000105154}

=== REQ 2 ===
PUT http://localhost:6333/collections/test_shard_max
payload: {"vectors": {"size": 4, "distance": "Cosine"}, "shard_number": 2147483647}
=== RESP 2 ===
status: None
body: 

=== REQ 3 ===
GET http://localhost:6333/
=== RESP 3 ===
status: None
body: 

=== REQ 4 ===
DELETE http://localhost:6333/collections/test_rep0
=== RESP 4 ===
status: None
body: 

=== REQ 5 ===
PUT http://localhost:6333/collections/test_rep0
payload: {"vectors": {"size": 4, "distance": "Cosine"}, "replication_factor": 0}
=== RESP 5 ===
status: None
body: 

=== REQ 6 ===
DELETE http://localhost:6333/collections/test_shard_max
=== RESP 6 ===
status: 200
body: {"result":false,"status":"ok","time":0.000065359}

=== REQ 7 ===
PUT http://localhost:6333/collections/test_shard_max
payload: {"vectors": {"size": 4, "distance": "Cosine"}, "shard_number": 2147483647}
=== RESP 7 ===
status: None
body: 

=== REQ 8 ===
GET http://localhost:6333/
=== RESP 8 ===
status: None
body: 

=== REQ 9 ===
DELETE http://localhost:6333/collections/test_rep0
=== RESP 9 ===
status: None
body: 

=== REQ 10 ===
PUT http://localhost:6333/collections/test_rep0
payload: {"vectors": {"size": 4, "distance": "Cosine"}, "replication_factor": 0}
=== RESP 10 ===
status: None
body:
--- 契约依据（expected，M3 重建版） ---
{"constraint_id": "qdrant_type_create_collection_001", "endpoint": "collections+{collection_name}", "type": "type_constraint", "description": "collection_name is string", "assertion": "collection_name type is string", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_type_update_collection_002", "endpoint": "collections+{collection_name}", "type": "type_constraint", "description": "All update fields are optional; at least one must be provided", "assertion": "At least one update field must be provided.", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_type_upsert_points_003", "endpoint": "collections+{collection_name}+points", "type": "type_constraint", "description": "id is integer (uint64) or UUID string; vector is array of floats or object of named vectors; payload is key-value object", "assertion": "id type is integer (uint64) or UUID string; vector type is array of floats or object of named vectors; payload type is key-value object.", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_type_overwrite_payload_004", "endpoint": "collections+{collection_name}+points+payload", "type": "type_constraint", "description": "Overwrite replaces entire payload, not merged", "assertion": "PUT payload replaces the entire payload; it does not merge.", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 0.9, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_range_create_collection_001", "endpoint": "collections+{collection_name}", "type": "range_constraint", "description": "shard_number minimum=1", "assertion": "shard_number >= 1", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_range_create_collection_002", "endpoint": "collections+{collection_name}", "type": "range_constraint", "description": "replication_factor minimum=1", "assertion": "replication_factor >= 1", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_range_scroll_points_005", "endpoint": "collections+{collection_name}+points+scroll", "type": "range_constraint", "description": "limit default=10 (adjustable)", "assertion": "limit default=10", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_range_search_points_006", "endpoint": "collections+{collection_name}+points+search", "type": "range_constraint", "description": "hnsw_ef applicable when exact=false", "assertion": "hnsw_ef parameter is applicable only when exact=false.", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 0.9, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_range_search_groups_007", "endpoint": "collections+{collection_name}+points+search+groups", "type": "range_constraint", "description": "group_size >= 1; limit >= 1", "assertion": "group_size >= 1 AND limit >= 1", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_range_query_points_008", "endpoint": "collections+{collection_name}+points+query", "type": "range_constraint", "description": "limit default=10", "assertion": "limit default=10 for query endpoint.", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_range_recommend_009", "endpoint": "collections+{collection_name}+points+recommend", "type": "range_constraint", "description": "strategy must be one of: average_vector, best_score, sum_scores", "assertion": "strategy IN (average_vector, best_score, sum_scores)", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_state_update_collection_002", "endpoint": "collections+{collection_name}", "type": "state_constraint", "description": "Blocking operation - waits for current optimizations to complete", "assertion": "Update blocks until current optimizations complete.", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 0.9, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_state_delete_collection_003", "endpoint": "collections+{collection_name}", "type": "state_constraint", "description": "Destructive operation - permanently deletes collection and all its data", "assertion": "Collection deletion permanently removes the collection and all its data.", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_state_set_payload_006", "endpoint": "collections+{collection_name}+points+payload", "type": "state_constraint", "description": "Atomic - all matched points get the payload", "assertion": "Payload set is atomic: all matched points receive the payload.", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_state_count_points_008", "endpoint": "collections+{collection_name}+points+count", "type": "state_constraint", "description": "exact=true performs full scan; exact=false uses segment statistics", "assertion": "exact=true performs a full scan; exact=false uses segment statistics.", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_state_search_points_009", "endpoint": "collections+{collection_name}+points+search", "type": "state_constraint", "description": "If exact=true, performs brute-force search (slow but accurate); if exact=false, uses HNSW for approximate search", "assertion": "When exact=true, search uses brute-force; when exact=false, search uses HNSW.", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_state_query_points_010", "endpoint": "collections+{collection_name}+points+query", "type": "state_constraint", "description": "prefetch queries execute first, then final query runs on combined results", "assertion": "prefetch queries execute first, then the final query runs on combined results.", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_state_create_index_011", "endpoint": "collections+{collection_name}+index", "type": "state_constraint", "description": "Index creation is async; query optimization applies after index is built", "assertion": "Index creation is asynchronous; query optimization applies after the index is built.", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_state_update_aliases_012", "endpoint": "collections+aliases", "type": "state_constraint", "description": "All alias operations in a single request are applied atomically", "assertion": "All alias operations in a single request are applied atomically.", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"assertion_id": "qdrant_behavioral_003", "endpoint": "collections+{collection_name}", "description": "200 with collection info; 404 if not found", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"assertion_id": "qdrant_behavioral_004", "endpoint": "collections+{collection_name}+exists", "description": "Returns {'result': {'exists': true/false}}", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"assertion_id": "qdrant_behavioral_008", "endpoint": "collections+{collection_name}+points+search", "description": "200 with ranked results descending by score; 4XX on invalid params", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"assertion_id": "qdrant_behavioral_009", "endpoint": "collections+{collection_name}+points+scroll", "description": "200 with points list and next_page_offset for pagination", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"assertion_id": "qdrant_behavioral_010", "endpoint": "collections+{collection_name}+points+count", "description": "200 with count result", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"assertion_id": "qdrant_behavioral_011", "endpoint": "collections+{collection_name}+points+query", "description": "200 with result points; supports multi-stage query pipeline via prefetch", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"assertion_id": "qdrant_behavioral_017", "endpoint": "collections", "description": "200 with list of collections", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"endpoint": "collections+{collection_name}", "kind": "range_constraints", "description": "shard_number minimum=1", "assertion": "shard_number >= 1", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"endpoint": "collections+{collection_name}", "kind": "range_constraints", "description": "replication_factor minimum=1", "assertion": "replication_factor >= 1", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"endpoint": "collections+{collection_name}", "kind": "range_constraints", "description": "timeout minimum=1", "assertion": "timeout >= 1", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"endpoint": "collections+{collection_name}", "kind": "state_constraints", "description": "Atomic collection creation: after 200 response, collection is fully initialized and ready for operations", "assertion": "Atomic collection creation. After 200 response, collection is fully initialized and ready for operations.", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_range_create_collection_002", "endpoint": "collections+{collection_name}", "description": "replication_factor minimum=1", "assertion": "replication_factor >= 1", "type": "range_constraint", "confidence": 1.0, "evidence_tier": "inferred_from_behavior", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "source_status": "reachable", "doc_version": "1.18.x", "source_verified": true, "source_type": "structured-spec"}
{"constraint_id": "qdrant_range_create_collection_001", "endpoint": "collections+{collection_name}", "description": "shard_number minimum=1", "assertion": "shard_number >= 1", "type": "range_constraint", "confidence": 1.0, "evidence_tier": "inferred_from_behavior", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "source_status": "reachable", "doc_version": "1.18.x", "source_verified": true, "source_type": "structured-spec"}
{"constraint_id": "qdrant_range_search_groups_007", "endpoint": "collections+{collection_name}+points+search+groups", "description": "group_size >= 1; limit >= 1", "assertion": "group_size >= 1 AND limit >= 1", "type": "range_constraint", "confidence": 1.0, "evidence_tier": "inferred_from_behavior", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "source_status": "reachable", "doc_version": "1.18.x", "source_verified": true, "source_type": "structured-spec"}
{"constraint_id": "qdrant_type_upsert_points_003", "endpoint": "collections+{collection_name}+points", "description": "id is integer (uint64) or UUID string; vector is array of floats or object of named vectors; payload is key-value object", "assertion": "id type is integer (uint64) or UUID string; vector type is array of floats or object of named vectors; payload type is key-value object.", "type": "type_constraint", "confidence": 1.0, "evidence_tier": "inferred_from_behavior", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "source_status": "reachable", "doc_version": "1.18.x", "source_verified": true, "source_type": "structured-spec"}

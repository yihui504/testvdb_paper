=== 候选缺陷 qdrant_001 ===
[vendor=qdrant version=1.12.1 defect_type=crash endpoint=points]

--- 观察到的行为（observed） ---

执行日志全文（output_qdrant_001.log）：
=== REQ 1 ===
DELETE http://localhost:6333/collections/test
=== RESP 1 ===
status: 200
body: {"result":false,"status":"ok","time":0.000896975}

=== REQ 2 ===
PUT http://localhost:6333/collections/test
payload: {"vectors": {"size": 4, "distance": "Cosine"}}
=== RESP 2 ===
status: 200
body: {"result":true,"status":"ok","time":0.635760215}

=== REQ 3 ===
PUT http://localhost:6333/collections/test/points?wait=true
payload: {"points": [{"id": 1, "vector": []}]}
=== RESP 3 ===
status: 400
body: {"status":{"error":"Wrong input: Vector dimension error: expected dim: 4, got 0"},"time":0.025609229}

=== REQ 4 ===
GET http://localhost:6333/collections/test
=== RESP 4 ===
status: 200
body: {"result":{"status":"green","optimizer_status":"ok","indexed_vectors_count":0,"points_count":0,"segments_count":8,"config":{"params":{"vectors":{"size":4,"distance":"Cosine"},"shard_number":1,"replication_factor":1,"write_consistency_factor":1,"on_disk_payload":true},"hnsw_config":{"m":16,"ef_construct":100,"full_scan_threshold":10000,"max_indexing_threads":0,"on_disk":false},"optimizer_config":{"deleted_threshold":0.2,"vacuum_min_vector_number":1000,"default_segment_number":0,"max_segment_size":null,"memmap_threshold":null,"indexing_threshold":20000,"flush_interval_sec":5,"max_optimization_threads":null},"wal_config":{"wal_capacity_mb":32,"wal_segments_ahead":0},"quantization_config":null,"strict_mode_config":{"enabled":false}},"payload_schema":{}},"status":"ok","time":0.000676351}

=== REQ 5 ===
PUT http://localhost:6333/collections/test/points
payload: {"points": [{"id": 2, "vector": []}]}
=== RESP 5 ===
status: 200
body: {"result":{"operation_id":1,"status":"acknowledged"},"status":"ok","time":0.000130011}

=== REQ 6 ===
GET http://localhost:6333/collections/test
=== RESP 6 ===
status: 200
body: {"result":{"status":"green","optimizer_status":"ok","indexed_vectors_count":0,"points_count":0,"segments_count":8,"config":{"params":{"vectors":{"size":4,"distance":"Cosine"},"shard_number":1,"replication_factor":1,"write_consistency_factor":1,"on_disk_payload":true},"hnsw_config":{"m":16,"ef_construct":100,"full_scan_threshold":10000,"max_indexing_threads":0,"on_disk":false},"optimizer_config":{"deleted_threshold":0.2,"vacuum_min_vector_number":1000,"default_segment_number":0,"max_segment_size":null,"memmap_threshold":null,"indexing_threshold":20000,"flush_interval_sec":5,"max_optimization_threads":null},"wal_config":{"wal_capacity_mb":32,"wal_segments_ahead":0},"quantization_config":null,"strict_mode_config":{"enabled":false}},"payload_schema":{}},"status":"ok","time":0.000059306}

=== REQ 7 ===
GET http://localhost:6333/
=== RESP 7 ===
status: 200
body: {"title":"qdrant - vector search engine","version":"1.12.1","commit":"9c20e9e27960228019b4606f137ca82b42fc3e66"}



--- 契约依据（expected，来自该版本 API 契约） ---
约束条目（23 条，来自 qdrant 1.12.1 契约，endpoint=points）：
{"constraint_id": "qdrant_type_upsert_points_003", "endpoint": "collections+{collection_name}+points", "type": "type_constraint", "description": "id is integer (uint64) or UUID string; vector is array of floats or object of named vectors; payload is key-value object", "assertion": "id type is integer (uint64) or UUID string; vector type is array of floats or object of named vectors; payload type is key-value object.", "source_url": "https://api.qdrant.tech/v-1-18-x/api-reference/points/upsert-points", "confidence": 1.0}
{"constraint_id": "qdrant_type_overwrite_payload_004", "endpoint": "collections+{collection_name}+points+payload", "type": "type_constraint", "description": "Overwrite replaces entire payload, not merged", "assertion": "PUT payload replaces the entire payload; it does not merge.", "source_url": "https://api.qdrant.tech/v-1-18-x/api-reference", "confidence": 0.9}
{"constraint_id": "qdrant_range_scroll_points_005", "endpoint": "collections+{collection_name}+points+scroll", "type": "range_constraint", "description": "limit default=10 (adjustable)", "assertion": "limit default=10", "source_url": "https://api.qdrant.tech/v-1-18-x/api-reference", "confidence": 1.0}
{"constraint_id": "qdrant_range_search_points_006", "endpoint": "collections+{collection_name}+points+search", "type": "range_constraint", "description": "hnsw_ef applicable when exact=false", "assertion": "hnsw_ef parameter is applicable only when exact=false.", "source_url": "https://api.qdrant.tech/v-1-18-x/api-reference/search/points", "confidence": 0.9}
{"constraint_id": "qdrant_range_search_groups_007", "endpoint": "collections+{collection_name}+points+search+groups", "type": "range_constraint", "description": "group_size >= 1; limit >= 1", "assertion": "group_size >= 1 AND limit >= 1", "source_url": "https://api.qdrant.tech/v-1-18-x/api-reference", "confidence": 1.0}
{"constraint_id": "qdrant_range_query_points_008", "endpoint": "collections+{collection_name}+points+query", "type": "range_constraint", "description": "limit default=10", "assertion": "limit default=10 for query endpoint.", "source_url": "https://api.qdrant.tech/v-1-18-x/api-reference", "confidence": 1.0}
{"constraint_id": "qdrant_range_recommend_009", "endpoint": "collections+{collection_name}+points+recommend", "type": "range_constraint", "description": "strategy must be one of: average_vector, best_score, sum_scores", "assertion": "strategy IN (average_vector, best_score, sum_scores)", "source_url": "https://api.qdrant.tech/v-1-18-x/api-reference", "confidence": 1.0}
{"constraint_id": "qdrant_state_upsert_points_004", "endpoint": "collections+{collection_name}+points", "type": "state_constraint", "description": "Atomic batch upsert - all points inserted or none", "assertion": "Batch upsert is atomic: all points are inserted or none.", "source_url": "https://api.qdrant.tech/v-1-18-x/api-reference/points/upsert-points", "confidence": 1.0}
{"constraint_id": "qdrant_state_delete_points_005", "endpoint": "collections+{collection_name}+points+delete", "type": "state_constraint", "description": "Deletion is atomic for the matched set", "assertion": "Point deletion is atomic for the matched set.", "source_url": "https://api.qdrant.tech/v-1-18-x/api-reference", "confidence": 1.0}
{"constraint_id": "qdrant_state_set_payload_006", "endpoint": "collections+{collection_name}+points+payload", "type": "state_constraint", "description": "Atomic - all matched points get the payload", "assertion": "Payload set is atomic: all matched points receive the payload.", "source_url": "https://api.qdrant.tech/v-1-18-x/api-reference/points/set-payload", "confidence": 1.0}
{"constraint_id": "qdrant_state_batch_update_007", "endpoint": "collections+{collection_name}+points+batch", "type": "state_constraint", "description": "Batch operations are NOT promised to be atomic; on error, operations may be none, partially, or fully applied; writes are idempotent and clients should retry", "assertion": "Batch update operations may be partially applied on failure; atomicity is not guaranteed; clients must retry to reach a consistent state", "source_url": "https://api.qdrant.tech/v-1-18-x/api-reference", "confidence": 1.0}
{"constraint_id": "qdrant_state_count_points_008", "endpoint": "collections+{collection_name}+points+count", "type": "state_constraint", "description": "exact=true performs full scan; exact=false uses segment statistics", "assertion": "exact=true performs a full scan; exact=false uses segment statistics.", "source_url": "https://api.qdrant.tech/v-1-18-x/api-reference", "confidence": 1.0}
{"constraint_id": "qdrant_state_search_points_009", "endpoint": "collections+{collection_name}+points+search", "type": "state_constraint", "description": "If exact=true, performs brute-force search (slow but accurate); if exact=false, uses HNSW for approximate search", "assertion": "When exact=true, search uses brute-force; when exact=false, search uses HNSW.", "source_url": "https://api.qdrant.tech/v-1-18-x/api-reference/search/points", "confidence": 1.0}
{"constraint_id": "qdrant_state_query_points_010", "endpoint": "collections+{collection_name}+points+query", "type": "state_constraint", "description": "prefetch queries execute first, then final query runs on combined results", "assertion": "prefetch queries execute first, then the final query runs on combined results.", "source_url": "https://api.qdrant.tech/v-1-18-x/api-reference", "confidence": 1.0}
{"assertion_id": "qdrant_behavioral_005", "endpoint": "collections+{collection_name}+points", "description": "200 on success; 4XX on validation error", "source_url": "https://api.qdrant.tech/v-1-18-x/api-reference/points/upsert-points", "confidence": 1.0}
{"assertion_id": "qdrant_behavioral_006", "endpoint": "collections+{collection_name}+points", "description": "200 with matching points (missing IDs are silently omitted)", "source_url": "https://api.qdrant.tech/v-1-18-x/api-reference", "confidence": 1.0}
{"assertion_id": "qdrant_behavioral_007", "endpoint": "collections+{collection_name}+points+delete", "description": "200 on success; 400 if neither points nor filter provided", "source_url": "https://api.qdrant.tech/v-1-18-x/api-reference", "confidence": 1.0}
{"assertion_id": "qdrant_behavioral_008", "endpoint": "collections+{collection_name}+points+search", "description": "200 with ranked results descending by score; 4XX on invalid params", "source_url": "https://api.qdrant.tech/v-1-18-x/api-reference/search/points", "confidence": 1.0}
{"assertion_id": "qdrant_behavioral_009", "endpoint": "collections+{collection_name}+points+scroll", "description": "200 with points list and next_page_offset for pagination", "source_url": "https://api.qdrant.tech/v-1-18-x/api-reference", "confidence": 1.0}
{"assertion_id": "qdrant_behavioral_010", "endpoint": "collections+{collection_name}+points+count", "description": "200 with count result", "source_url": "https://api.qdrant.tech/v-1-18-x/api-reference", "confidence": 1.0}
{"assertion_id": "qdrant_behavioral_011", "endpoint": "collections+{collection_name}+points+query", "description": "200 with result points; supports multi-stage query pipeline via prefetch", "source_url": "https://api.qdrant.tech/v-1-18-x/api-reference", "confidence": 1.0}
{"assertion_id": "qdrant_behavioral_012", "endpoint": "collections+{collection_name}+points+recommend", "description": "200 with ranked results", "source_url": "https://api.qdrant.tech/v-1-18-x/api-reference", "confidence": 1.0}
{"assertion_id": "qdrant_behavioral_016", "endpoint": "collections+{collection_name}+points+payload", "description": "200 on success; 400 if no points or filter specified", "source_url": "https://api.qdrant.tech/v-1-18-x/api-reference/points/set-payload", "confidence": 1.0}

相关契约段（关键词定位 3 条）：
{"endpoint": "collections+{collection_name}+points+search", "kind": "range_constraints", "description": "hnsw_ef applicable when exact=false", "assertion": "hnsw_ef parameter is applicable only when exact=false.", "source_url": "https://api.qdrant.tech/v-1-18-x/api-reference/search/points", "confidence": 0.9}
{"endpoint": "collections+{collection_name}+points+count", "kind": "state_constraints", "description": "exact=true performs full scan; exact=false uses segment statistics", "assertion": "exact=true performs a full scan; exact=false uses segment statistics.", "source_url": "https://api.qdrant.tech/v-1-18-x/api-reference", "confidence": 1.0}
{"endpoint": "collections+{collection_name}+points+search", "kind": "state_constraints", "description": "If exact=true, performs brute-force search (slow but accurate); if exact=false, uses HNSW for approximate search", "assertion": "When exact=true, search uses brute-force; when exact=false, search uses HNSW.", "source_url": "https://api.qdrant.tech/v-1-18-x/api-reference/search/points", "confidence": 1.0}

VERDICT: UNKNOWN (replay capture — no attack-agent assertion output; raw HTTP only)

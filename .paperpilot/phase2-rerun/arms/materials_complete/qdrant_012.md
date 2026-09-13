=== 候选缺陷 qdrant_012 ===
[vendor=qdrant version=1.18.2 defect_type=param_validation endpoint=points]
--- 观察到的行为（observed） ---

执行日志全文（output_qdrant_012.log）：
=== REQ 1 ===
DELETE http://localhost:6333/collections/test_mustnot
=== RESP 1 ===
status: 200
body: {"result":false,"status":"ok","time":0.000060189}

=== REQ 2 ===
PUT http://localhost:6333/collections/test_mustnot
payload: {"vectors": {"size": 4, "distance": "Cosine"}}
=== RESP 2 ===
status: 200
body: {"result":true,"status":"ok","time":0.289571764}

=== REQ 3 ===
PUT http://localhost:6333/collections/test_mustnot/points
payload: {"points": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4], "payload": {"tag": "x"}}, {"id": 2, "vector": [0.1, 0.2, 0.3, 0.4], "payload": {"tag": "y"}}]}
=== RESP 3 ===
status: 200
body: {"result":{"operation_id":1,"status":"acknowledged"},"status":"ok","time":0.00030563}

=== REQ 4 ===
POST http://localhost:6333/collections/test_mustnot/points/query
payload: {"query": [0.1, 0.2, 0.3, 0.4], "limit": 5, "filter": {"must_not": {"key": "tag", "match": {"value": "x"}}}}
=== RESP 4 ===
status: 200
body: {"result":{"points":[{"id":2,"version":1,"score":1.0}]},"status":"ok","time":0.000568857}

=== REQ 5 ===
DELETE http://localhost:6333/collections/test_mustnot
=== RESP 5 ===
status: 200
body: {"result":false,"status":"ok","time":0.000061755}

=== REQ 6 ===
PUT http://localhost:6333/collections/test_mustnot
payload: {"vectors": {"size": 4, "distance": "Cosine"}}
=== RESP 6 ===
status: 200
body: {"result":true,"status":"ok","time":0.396569238}

=== REQ 7 ===
PUT http://localhost:6333/collections/test_mustnot/points
payload: {"points": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4], "payload": {"tag": "x"}}, {"id": 2, "vector": [0.1, 0.2, 0.3, 0.4], "payload": {"tag": "y"}}]}
=== RESP 7 ===
status: 200
body: {"result":{"operation_id":1,"status":"acknowledged"},"status":"ok","time":0.000132202}

=== REQ 8 ===
POST http://localhost:6333/collections/test_mustnot/points/query
payload: {"query": [0.1, 0.2, 0.3, 0.4], "limit": 5, "filter": {"must_not": {"key": "tag", "match": {"value": "x"}}}}
=== RESP 8 ===
status: 200
body: {"result":{"points":[{"id":2,"version":1,"score":1.0}]},"status":"ok","time":0.000327549}
--- 契约依据（expected，M3 重建版） ---
{"constraint_id": "qdrant_type_upsert_points_003", "endpoint": "collections+{collection_name}+points", "type": "type_constraint", "description": "id is integer (uint64) or UUID string; vector is array of floats or object of named vectors; payload is key-value object", "assertion": "id type is integer (uint64) or UUID string; vector type is array of floats or object of named vectors; payload type is key-value object.", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_type_overwrite_payload_004", "endpoint": "collections+{collection_name}+points+payload", "type": "type_constraint", "description": "Overwrite replaces entire payload, not merged", "assertion": "PUT payload replaces the entire payload; it does not merge.", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 0.9, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_range_scroll_points_005", "endpoint": "collections+{collection_name}+points+scroll", "type": "range_constraint", "description": "limit default=10 (adjustable)", "assertion": "limit default=10", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_range_search_points_006", "endpoint": "collections+{collection_name}+points+search", "type": "range_constraint", "description": "hnsw_ef applicable when exact=false", "assertion": "hnsw_ef parameter is applicable only when exact=false.", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 0.9, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_range_search_groups_007", "endpoint": "collections+{collection_name}+points+search+groups", "type": "range_constraint", "description": "group_size >= 1; limit >= 1", "assertion": "group_size >= 1 AND limit >= 1", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_range_query_points_008", "endpoint": "collections+{collection_name}+points+query", "type": "range_constraint", "description": "limit default=10", "assertion": "limit default=10 for query endpoint.", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_range_recommend_009", "endpoint": "collections+{collection_name}+points+recommend", "type": "range_constraint", "description": "strategy must be one of: average_vector, best_score, sum_scores", "assertion": "strategy IN (average_vector, best_score, sum_scores)", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_state_set_payload_006", "endpoint": "collections+{collection_name}+points+payload", "type": "state_constraint", "description": "Atomic - all matched points get the payload", "assertion": "Payload set is atomic: all matched points receive the payload.", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_state_count_points_008", "endpoint": "collections+{collection_name}+points+count", "type": "state_constraint", "description": "exact=true performs full scan; exact=false uses segment statistics", "assertion": "exact=true performs a full scan; exact=false uses segment statistics.", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_state_search_points_009", "endpoint": "collections+{collection_name}+points+search", "type": "state_constraint", "description": "If exact=true, performs brute-force search (slow but accurate); if exact=false, uses HNSW for approximate search", "assertion": "When exact=true, search uses brute-force; when exact=false, search uses HNSW.", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_state_query_points_010", "endpoint": "collections+{collection_name}+points+query", "type": "state_constraint", "description": "prefetch queries execute first, then final query runs on combined results", "assertion": "prefetch queries execute first, then the final query runs on combined results.", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"assertion_id": "qdrant_behavioral_008", "endpoint": "collections+{collection_name}+points+search", "description": "200 with ranked results descending by score; 4XX on invalid params", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"assertion_id": "qdrant_behavioral_009", "endpoint": "collections+{collection_name}+points+scroll", "description": "200 with points list and next_page_offset for pagination", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"assertion_id": "qdrant_behavioral_010", "endpoint": "collections+{collection_name}+points+count", "description": "200 with count result", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"assertion_id": "qdrant_behavioral_011", "endpoint": "collections+{collection_name}+points+query", "description": "200 with result points; supports multi-stage query pipeline via prefetch", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_type_upsert_points_003", "endpoint": "collections+{collection_name}+points", "description": "id is integer (uint64) or UUID string; vector is array of floats or object of named vectors; payload is key-value object", "assertion": "id type is integer (uint64) or UUID string; vector type is array of floats or object of named vectors; payload type is key-value object.", "type": "type_constraint", "confidence": 1.0, "evidence_tier": "inferred_from_behavior", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "source_status": "reachable", "doc_version": "1.18.x", "source_verified": true, "source_type": "structured-spec"}
{"constraint_id": "qdrant_range_scroll_points_005", "endpoint": "collections+{collection_name}+points+scroll", "description": "limit default=10 (adjustable)", "assertion": "limit default=10", "type": "range_constraint", "confidence": 1.0, "evidence_tier": "inferred_from_behavior", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "source_status": "reachable", "doc_version": "1.18.x", "source_verified": true, "source_type": "structured-spec"}
{"constraint_id": "qdrant_range_search_groups_007", "endpoint": "collections+{collection_name}+points+search+groups", "description": "group_size >= 1; limit >= 1", "assertion": "group_size >= 1 AND limit >= 1", "type": "range_constraint", "confidence": 1.0, "evidence_tier": "inferred_from_behavior", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "source_status": "reachable", "doc_version": "1.18.x", "source_verified": true, "source_type": "structured-spec"}
{"constraint_id": "qdrant_range_query_points_008", "endpoint": "collections+{collection_name}+points+query", "description": "limit default=10", "assertion": "limit default=10 for query endpoint.", "type": "range_constraint", "confidence": 1.0, "evidence_tier": "inferred_from_behavior", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "source_status": "reachable", "doc_version": "1.18.x", "source_verified": true, "source_type": "structured-spec"}
{"constraint_id": "qdrant_state_set_payload_006", "endpoint": "collections+{collection_name}+points+payload", "description": "Atomic - all matched points get the payload", "assertion": "Payload set is atomic: all matched points receive the payload.", "type": "state_constraint", "confidence": 1.0, "evidence_tier": "inferred_from_behavior", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "source_status": "reachable", "doc_version": "1.18.x", "source_verified": true, "source_type": "structured-spec"}
{"constraint_id": "qdrant_state_query_points_010", "endpoint": "collections+{collection_name}+points+query", "description": "prefetch queries execute first, then final query runs on combined results", "assertion": "prefetch queries execute first, then the final query runs on combined results.", "type": "state_constraint", "confidence": 1.0, "evidence_tier": "inferred_from_behavior", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "source_status": "reachable", "doc_version": "1.18.x", "source_verified": true, "source_type": "structured-spec"}
{"assertion_id": "qdrant_behavioral_011", "endpoint": "collections+{collection_name}+points+query", "description": "200 with result points; supports multi-stage query pipeline via prefetch", "category": "behavioral", "expected_behavior": "Returns 200 with array of scored points.", "confidence": 1.0, "evidence_tier": "inferred_from_behavior", "defect_type_if_violated": "Type3_RuntimeFailure", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "doc_version": "1.18.x", "source_verified": true, "source_type": "structured-spec"}
{"constraint_id": "qdrant_range_recommend_009", "endpoint": "collections+{collection_name}+points+recommend", "description": "strategy must be one of: average_vector, best_score, sum_scores", "assertion": "strategy IN (average_vector, best_score, sum_scores)", "type": "range_constraint", "confidence": 1.0, "evidence_tier": "inferred_from_behavior", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "source_status": "reachable", "doc_version": "1.18.x", "source_verified": true, "source_type": "structured-spec"}

=== 候选缺陷 weaviate_005 ===
[vendor=weaviate version=1.38.0 defect_type=param_validation endpoint=POST /schema]
--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] control: POST schema with desiredCount=0 -> http=422
- [c2] POST schema with desiredCount=-1 -> http=200

执行日志全文（output_weaviate_005.log）：
=== REQ 1 ===
DELETE http://localhost:18080/v1/schema/TestZero
=== RESP 1 ===
status: 200
body: 

=== REQ 2 ===
DELETE http://localhost:18080/v1/schema/TestNeg
=== RESP 2 ===
status: 200
body: 

=== REQ 3 ===
POST http://localhost:18080/v1/schema
payload: {"class": "TestZero", "shardingConfig": {"desiredCount": 0}}
=== RESP 3 ===
status: 422
body: {"allowed":null,"error":[{"message":"updating db: TYPE_ADD_CLASS: apply add class: create index: failed to read sharding state: invalid sharding state: physical shards unavailable"}]}


=== REQ 4 ===
POST http://localhost:18080/v1/schema
payload: {"class": "TestNeg", "shardingConfig": {"desiredCount": -1}}
=== RESP 4 ===
status: 200
body:

--- 契约依据（expected，M1 过滤后初稿） ---
约束条目（8 条，来自 weaviate 1.38.0 契约，endpoint=POST /schema）：
{"constraint_id": "weaviate_type_schema_create_001", "endpoint": "/schema POST", "type": "type_constraint", "description": "class field must be CamelCase", "assertion": "properties.class matches /^[A-Z][a-zA-Z0-9]*$/", "source_url": "https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json", "confidence": 0.95, "_audit": {"g1": "aligned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["CamelCase", "class", "matches", "properties"], "priority": "bulk"}}
{"constraint_id": "weaviate_type_schema_create_002", "endpoint": "/schema POST", "type": "type_constraint", "description": "vectorIndexType must be one of allowed index types", "assertion": "properties.vectorIndexType in {hnsw, flat, dynamic, bwes}", "source_url": "https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json", "confidence": 0.95, "_audit": {"g1": "aligned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["allowed", "dynamic", "flat", "hnsw", "index", "one", "properties", "types", "vectorIndexType"], "priority": "bulk"}}
{"constraint_id": "weaviate_type_schema_create_003", "endpoint": "/schema POST", "type": "type_constraint", "description": "properties[].tokenization must be a valid enum value", "assertion": "properties.properties[].tokenization in {word, lowercase, whitespace, field, trigram, gse, kagome_kr, kagome_ja, gse_ch}", "source_url": "https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json", "confidence": 0.95, "_audit": {"g1": "aligned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["enum", "gse", "gse_ch", "kagome_ja", "kagome_kr", "lowercase", "properties", "tokenization", "trigram", "valid", "whitespace", "word"], "priority": "bulk"}}
{"constraint_id": "weaviate_type_tenants_create_001", "endpoint": "/schema/{className}/tenants POST", "type": "type_constraint", "description": "Tenant.activityStatus on create must be ACTIVE or INACTIVE", "assertion": "body[].activityStatus in {ACTIVE, INACTIVE}", "source_url": "https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json", "confidence": 0.95, "_audit": {"g1": "aligned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["ACTIVE", "INACTIVE", "Tenant", "activityStatus", "body", "create"], "priority": "bulk"}}
{"constraint_id": "weaviate_range_schema_replication_001", "endpoint": "/schema POST", "type": "range_constraint", "description": "replicationConfig.factor is an integer (default 1)", "assertion": "replicationConfig.factor >= 1", "source_url": "https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json", "confidence": 0.85, "_audit": {"g1": "aligned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["default", "factor", "replicationConfig"], "priority": "bulk"}}
{"assertion_id": "weaviate_behavioral_schema_create_001", "endpoint": "/schema POST", "description": "creating collection with disallowed vectorIndexType returns 422 RestrictionViolationResponse", "source_url": "https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json", "confidence": 0.95, "_audit": {"g1": "aligned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["RestrictionViolationResponse", "creating", "disallowed", "vectorIndexType"], "priority": "bulk"}}
{"assertion_id": "weaviate_behavioral_schema_create_002", "endpoint": "/schema POST", "description": "exceeding collections/shards usage limit returns 429 UsageLimitExceededResponse", "source_url": "https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json", "confidence": 0.95, "_audit": {"g1": "aligned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["UsageLimitExceededResponse", "collections", "limit", "shards", "usage"], "priority": "bulk"}}
{"assertion_id": "weaviate_behavioral_tenants_create_001", "endpoint": "/schema/{className}/tenants POST", "description": "exceeding tenant usage limit returns 429 with limit: tenants", "source_url": "https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json", "confidence": 0.95, "_audit": {"g1": "aligned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["limit", "tenant", "tenants", "usage"], "priority": "bulk"}}
VERDICT: UNKNOWN (replay capture — no attack-agent assertion output; raw HTTP only)
--- 补充契约行（M1 端点过滤后） ---
{"constraint_id": "weaviate_type_schema_create_002", "endpoint": "/schema POST", "description": "vectorIndexType must be one of allowed index types", "assertion": "properties.vectorIndexType in {hnsw, flat, dynamic, bwes}", "type": "type_constraint", "confidence": 0.95, "evidence_tier": "explicit", "source_url": "https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json", "source_status": "reachable", "_audit": {"g1": "aligned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["allowed", "dynamic", "flat", "hnsw", "index", "one", "properties", "types", "vectorIndexType"], "priority": "bulk"}}
{"assertion_id": "weaviate_behavioral_schema_create_001", "endpoint": "/schema POST", "description": "creating collection with disallowed vectorIndexType returns 422 RestrictionViolationResponse", "category": "behavioral", "expected_behavior": "422 with errorCode CONFIG_NOT_ALLOWED and restriction vector_index_type", "confidence": 0.95, "evidence_tier": "explicit", "defect_type_if_violated": "Type1_IllegalSuccess", "source_url": "https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json", "doc_version": "1.38.0", "_audit": {"g1": "aligned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["CONFIG_NOT_ALLOWED", "RestrictionViolationResponse", "creating", "disallowed", "errorCode", "restriction", "vectorIndexType", "vector_index_type"], "priority": "bulk"}}
{"assertion_id": "weaviate_behavioral_index_update_001", "endpoint": "/schema/{className}/indexes/{propertyName} PUT", "description": "downgrading from blockmax algorithm is rejected", "category": "behavioral", "expected_behavior": "422 (rejection); only WAND->BlockMax migration allowed", "confidence": 0.9, "evidence_tier": "explicit", "defect_type_if_violated": "Type1_IllegalSuccess", "source_url": "https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json", "doc_version": "1.38.0", "_audit": {"g1": "aligned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["BlockMax", "WAND", "algorithm", "allowed", "blockmax", "from", "migration", "only", "rejected"], "priority": "bulk"}}

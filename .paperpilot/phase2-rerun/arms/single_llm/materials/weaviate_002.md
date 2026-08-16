=== 候选缺陷 weaviate_002 ===
[vendor=weaviate version=1.37.4 defect_type=param_validation endpoint=POST /schema]

--- 观察到的行为（observed） ---

执行日志全文（output_weaviate_002.log）：
=== REQ 1 ===
DELETE http://localhost:18080/v1/schema/TestFC
=== RESP 1 ===
status: 200
body: 

=== REQ 2 ===
POST http://localhost:18080/v1/schema
payload: {"class": "TestFC", "vectorizer": "none", "vectorIndexConfig": {"distance": "cosine", "flatSearchCutoff": -100}, "properties": [{"name": "text", "dataType": ["text"]}]}
=== RESP 2 ===
status: 200
body: {"class":"TestFC","invertedIndexConfig":{"bm25":{"b":0.75,"k1":1.2},"cleanupIntervalSeconds":60,"stopwords":{"additions":null,"preset":"en","removals":null},"usingBlockMaxWAND":true},"multiTenancyConfig":{"autoTenantActivation":false,"autoTenantCreation":false,"enabled":false},"properties":[{"dataType":["text"],"indexFilterable":true,"indexRangeFilters":false,"indexSearchable":true,"name":"text","tokenization":"word"}],"replicationConfig":{"asyncEnabled":false,"deletionStrategy":"TimeBasedResolution","factor":1},"shardingConfig":{"virtualPerPhysical":128,"desiredCount":1,"actualCount":1,"desiredVirtualCount":128,"actualVirtualCount":128,"key":"_id","strategy":"hash","function":"murmur3"},"vectorIndexConfig":{"skip":false,"cleanupIntervalSeconds":300,"maxConnections":32,"efConstruction":128,"ef":-1,"dynamicEfMin":100,"dynamicEfMax":500,"dynamicEfFactor":8,"vectorCacheMaxObjects":1000000000000,"flatSearchCutoff":-100,"distance":"cosine","pq":{"enabled":false,"bitCompression":false,"segments":0,"centroids":256,"trainingLimit":100000,"encoder":{"type":"kmeans","distribution":"log-normal"}},"bq":{"enabled":false},"sq":{"enabled":false,"trainingLimit":100000,"rescoreLimit":20},"rq":{"enabled":false,"bits":8,"rescoreLimit":20},"filterStrategy":"acorn","multivector":{"enabled":false,"muvera":{"enabled":false,"ksim":4,"dprojections":16,"repetitions":10},"aggregation":"maxSim"},"skipDefaultQuantization":false,"trackDefaultQuantization":false},"vectorIndexType":"hnsw","vectorizer":"none"}


=== REQ 3 ===
GET http://localhost:18080/v1/schema/TestFC
=== RESP 3 ===
status: 200
body: {"class":"TestFC","invertedIndexConfig":{"bm25":{"b":0.75,"k1":1.2},"cleanupIntervalSeconds":60,"stopwords":{"additions":null,"preset":"en","removals":null},"usingBlockMaxWAND":true},"multiTenancyConfig":{"autoTenantActivation":false,"autoTenantCreation":false,"enabled":false},"properties":[{"dataType":["text"],"indexFilterable":true,"indexRangeFilters":false,"indexSearchable":true,"name":"text","tokenization":"word"}],"replicationConfig":{"asyncEnabled":false,"deletionStrategy":"TimeBasedResolution","factor":1},"shardingConfig":{"actualCount":1,"actualVirtualCount":128,"desiredCount":1,"desiredVirtualCount":128,"function":"murmur3","key":"_id","strategy":"hash","virtualPerPhysical":128},"vectorIndexConfig":{"bq":{"enabled":false},"cleanupIntervalSeconds":300,"distance":"cosine","dynamicEfFactor":8,"dynamicEfMax":500,"dynamicEfMin":100,"ef":-1,"efConstruction":128,"filterStrategy":"acorn","flatSearchCutoff":-100,"maxConnections":32,"multivector":{"aggregation":"maxSim","enabled":false,"muvera":{"dprojections":16,"enabled":false,"ksim":4,"repetitions":10}},"pq":{"bitCompression":false,"centroids":256,"enabled":false,"encoder":{"distribution":"log-normal","type":"kmeans"},"segments":0,"trainingLimit":100000},"rq":{"bits":8,"enabled":false,"rescoreLimit":20},"skip":false,"skipDefaultQuantization":false,"sq":{"enabled":false,"rescoreLimit":20,"trainingLimit":100000},"trackDefaultQuantization":false,"vectorCacheMaxObjects":1000000000000},"vectorIndexType":"hnsw","vectorizer":"none"}




--- 契约依据（expected，来自该版本 API 契约） ---
约束条目（8 条，来自 weaviate 1.37.4 契约，endpoint=POST /schema）：
{"constraint_id": "weaviate_type_schema_create_001", "endpoint": "/schema POST", "type": "type_constraint", "description": "class field must be CamelCase", "assertion": "properties.class matches /^[A-Z][a-zA-Z0-9]*$/", "source_url": "https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json", "confidence": 0.95}
{"constraint_id": "weaviate_type_schema_create_002", "endpoint": "/schema POST", "type": "type_constraint", "description": "vectorIndexType must be one of allowed index types", "assertion": "properties.vectorIndexType in {hnsw, flat, dynamic, bwes}", "source_url": "https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json", "confidence": 0.95}
{"constraint_id": "weaviate_type_schema_create_003", "endpoint": "/schema POST", "type": "type_constraint", "description": "properties[].tokenization must be a valid enum value", "assertion": "properties.properties[].tokenization in {word, lowercase, whitespace, field, trigram, gse, kagome_kr, kagome_ja, gse_ch}", "source_url": "https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json", "confidence": 0.95}
{"constraint_id": "weaviate_type_tenants_create_001", "endpoint": "/schema/{className}/tenants POST", "type": "type_constraint", "description": "Tenant.activityStatus on create must be ACTIVE or INACTIVE", "assertion": "body[].activityStatus in {ACTIVE, INACTIVE}", "source_url": "https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json", "confidence": 0.95}
{"constraint_id": "weaviate_range_schema_replication_001", "endpoint": "/schema POST", "type": "range_constraint", "description": "replicationConfig.factor is an integer (default 1)", "assertion": "replicationConfig.factor >= 1", "source_url": "https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json", "confidence": 0.85}
{"assertion_id": "weaviate_behavioral_schema_create_001", "endpoint": "/schema POST", "description": "creating collection with disallowed vectorIndexType returns 422 RestrictionViolationResponse", "source_url": "https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json", "confidence": 0.95}
{"assertion_id": "weaviate_behavioral_schema_create_002", "endpoint": "/schema POST", "description": "exceeding collections/shards usage limit returns 429 UsageLimitExceededResponse", "source_url": "https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json", "confidence": 0.95}
{"assertion_id": "weaviate_behavioral_tenants_create_001", "endpoint": "/schema/{className}/tenants POST", "description": "exceeding tenant usage limit returns 429 with limit: tenants", "source_url": "https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json", "confidence": 0.95}

VERDICT: UNKNOWN (replay capture — no attack-agent assertion output; raw HTTP only)

=== 候选缺陷 weaviate_010 ===
[vendor=weaviate version=1.38.2 defect_type=behavior endpoint=DELETE /batch/objects]

--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] POST schema BoundaryTestBatchDelete -> http=200
- [c2] batch delete with class but missing where -> http=500, body: validate: empty match.where clause
- [c3] batch delete with empty match {} -> http=500, body: validate: empty match.class clause

执行日志全文（output_weaviate_010.log）：
=== REQ 1 ===
DELETE http://localhost:18080/v1/schema/BoundaryTestBatchDelete
=== RESP 1 ===
status: 200
body: 

=== REQ 2 ===
POST http://localhost:18080/v1/schema
payload: {"class": "BoundaryTestBatchDelete", "vectorizer": "none", "properties": [{"name": "title", "dataType": ["text"]}]}
=== RESP 2 ===
status: 200
body: {"class":"BoundaryTestBatchDelete","invertedIndexConfig":{"bm25":{"b":0.75,"k1":1.2},"cleanupIntervalSeconds":60,"stopwords":{"additions":null,"preset":"en","removals":null},"usingBlockMaxWAND":true},"multiTenancyConfig":{"autoTenantActivation":false,"autoTenantCreation":false,"enabled":false},"properties":[{"dataType":["text"],"indexFilterable":true,"indexRangeFilters":false,"indexSearchable":true,"name":"title","tokenization":"word"}],"shardingConfig":{"virtualPerPhysical":128,"desiredCount":1,"actualCount":1,"desiredVirtualCount":128,"actualVirtualCount":128,"key":"_id","strategy":"hash","function":"murmur3"},"vectorIndexConfig":{"skip":false,"cleanupIntervalSeconds":300,"maxConnections":32,"efConstruction":128,"ef":-1,"dynamicEfMin":100,"dynamicEfMax":500,"dynamicEfFactor":8,"vectorCacheMaxObjects":1000000000000,"flatSearchCutoff":40000,"distance":"cosine","pq":{"enabled":false,"bitCompression":false,"segments":0,"centroids":256,"trainingLimit":100000,"encoder":{"type":"kmeans","distribution":"log-normal"}},"bq":{"enabled":false},"sq":{"enabled":false,"trainingLimit":100000,"rescoreLimit":20},"rq":{"enabled":false,"bits":8,"rescoreLimit":20},"filterStrategy":"acorn","multivector":{"enabled":false,"muvera":{"enabled":false,"ksim":4,"dprojections":16,"repetitions":10},"aggregation":"maxSim"},"skipDefaultQuantization":false,"trackDefaultQuantization":false},"vectorIndexType":"hnsw","vectorizer":"none","replicationConfig":{"deletionStrategy":"TimeBasedResolution","factor":1,"asyncEnabled":false}}


=== REQ 3 ===
DELETE http://localhost:18080/v1/batch/objects
payload: {"match": {"class": "BoundaryTestBatchDelete"}, "output": "minimal"}
=== RESP 3 ===
status: 500
body: {"error":[{"message":"validate: empty match.where clause"}]}


=== REQ 4 ===
DELETE http://localhost:18080/v1/batch/objects
payload: {"match": {}, "output": "minimal"}
=== RESP 4 ===
status: 500
body: {"error":[{"message":"validate: empty match.class clause"}]}




--- 契约依据（expected，来自该版本 API 契约） ---
约束条目（1 条，来自 weaviate 1.38.2 契约，endpoint=DELETE /batch/objects）：
{"constraint_id": "weaviate_range_batch_delete_001", "endpoint": "DELETE /batch/objects", "type": "range_constraint", "description": "max deletions per request = QUERY_MAXIMUM_RESULTS (default 10000)", "assertion": "deleted count <= QUERY_MAXIMUM_RESULTS", "source_url": "https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json", "confidence": 0.95}

相关契约段（关键词定位 4 条）：
{"endpoint": "POST /schema", "kind": "type_constraints", "description": "class field must be CamelCase (capital first letter, alphanumeric only)", "assertion": "class matches regex ^[A-Z][a-zA-Z0-9]*$", "source_url": "https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json", "confidence": 0.95}
{"endpoint": "POST /schema", "kind": "type_constraints", "description": "properties[].dataType must be array of valid types or class references", "assertion": "properties[].dataType is array of strings; first-capital values are class references", "source_url": "https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json", "confidence": 0.95}
{"endpoint": "POST /batch/objects", "kind": "state_constraints", "description": "idempotent by UUID -- existing UUIDs overwritten (PUT semantics per item)", "assertion": "batch create is idempotent; existing UUIDs are replaced", "source_url": "https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json", "confidence": 0.95}
{"endpoint": "POST /batch/objects", "kind": "state_constraints", "description": "429 WHOLE BATCH rejected (no partial fill)", "assertion": "usage limit exceeded rejects entire batch, no partial success", "source_url": "https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json", "confidence": 0.95}

VERDICT: UNKNOWN (replay capture — no attack-agent assertion output; raw HTTP only)

=== 候选缺陷 milvus_003 ===
[vendor=milvus version=2.6.10 defect_type=param_validation endpoint=entities+search]

--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] HNSW search with ef=0 -> http=200, code=0, returned 10 results

执行日志全文（output_milvus_003.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "repro_<tracked>", "dimension": 8, "metricType": "L2", "dbName": "default"}
=== RESP 1 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "repro_<tracked>", "dbName": "default", "data": [{"id": 0, "vector": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]}, {"id": 1, "vector": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]}, {"id": 2, "vector": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]}, {"id": 3, "vector": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]}, {"id": 4, "vector": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]}, {"id": 5, "vector": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]}, {"id": 6, "vector": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]}, {"id": 7, "vector": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]}, {"id": 8, "vector": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]}, {"id": 9, "vector": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]}]}
=== RESP 2 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":10,"insertIds":[0,1,2,3,4,5,6,7,8,9]}}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/indexes/create
payload: {"collectionName": "repro_<tracked>", "dbName": "default", "indexParams": [{"fieldName": "vector", "indexName": "idx_vec", "metricType": "L2", "indexType": "HNSW", "params": {"M": 8, "efConstruction": 64}}]}
=== RESP 3 ===
status: 200
body: {"code":65535,"message":"CreateIndex failed: creating multiple indexes on same field is not supported"}

=== REQ 4 ===
POST http://localhost:19530/v2/vectordb/collections/load
payload: {"collectionName": "repro_<tracked>", "dbName": "default"}
=== RESP 4 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 5 ===
POST http://localhost:19530/v2/vectordb/entities/search
payload: {"collectionName": "repro_<tracked>", "dbName": "default", "data": [[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]], "limit": 3, "searchParams": {"ef": 0}, "outputFields": ["id"]}
=== RESP 5 ===
status: 200
body: {"code":0,"cost":0,"data":[{"distance":0,"id":0},{"distance":0,"id":1},{"distance":0,"id":2}],"topks":[3]}




--- 契约依据（expected，来自该版本 API 契约） ---
约束条目（10 条，来自 milvus 2.6.10 契约，endpoint=entities+search）：
{"constraint_id": "milvus_type_entities_delete_001", "endpoint": "entities+delete", "type": "type_constraint", "description": "filter must be a valid boolean expression string", "assertion": "filter is a valid boolean expression", "source_url": "https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go", "confidence": 1.0}
{"constraint_id": "milvus_type_entities_get_001", "endpoint": "entities+get", "type": "type_constraint", "description": "id must match the collection primary key type (Int64 or VarChar)", "assertion": "id type matches collection primary key type", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Vector%20(v2)/Get.md", "confidence": 1.0}
{"constraint_id": "milvus_type_entities_search_001", "endpoint": "entities+search", "type": "type_constraint", "description": "data must be array of float arrays, annsField must be a vector field, limit must be positive integer", "assertion": "data is array[array[float]] AND annsField is a vector field AND limit > 0", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Vector%20(v2)/Search.md", "confidence": 1.0}
{"constraint_id": "milvus_range_entities_search_001", "endpoint": "entities+search", "type": "range_constraint", "description": "vector dimensions in data must match collection vector dimension", "assertion": "vector dimension == collection dimension", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Vector%20(v2)/Search.md", "confidence": 1.0}
{"constraint_id": "milvus_range_entities_search_002", "endpoint": "entities+search", "type": "range_constraint", "description": "limit + offset must be < 16384", "assertion": "limit + offset < 16384", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Vector%20(v2)/Search.md", "confidence": 1.0}
{"constraint_id": "milvus_state_entities_delete_001", "endpoint": "entities+delete", "type": "state_constraint", "description": "Deleted entities cannot be recovered", "assertion": "delete is irreversible", "source_url": "https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go", "confidence": 1.0}
{"constraint_id": "milvus_state_entities_search_001", "endpoint": "entities+search", "type": "state_constraint", "description": "Collection must be loaded; index must exist on annsField", "assertion": "collection is loaded AND index exists on annsField", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Vector%20(v2)/Search.md", "confidence": 1.0}
{"assertion_id": "milvus_behavioral_entities_search_001", "endpoint": "entities+search", "description": "Search returns 400 on vector dimension mismatch", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Vector%20(v2)/Search.md", "confidence": 1.0}
{"assertion_id": "milvus_behavioral_entities_delete_001", "endpoint": "entities+delete", "description": "Delete returns 400 on invalid filter expression", "source_url": "https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go", "confidence": 1.0}
{"assertion_id": "milvus_behavioral_entities_get_001", "endpoint": "entities+get", "description": "Get entities returns 400 if id type mismatches collection schema", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Vector%20(v2)/Get.md", "confidence": 1.0}

VERDICT: UNKNOWN (replay capture — no attack-agent assertion output; raw HTTP only)

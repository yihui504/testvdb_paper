=== 候选缺陷 milvus_009 ===
[vendor=milvus version=2.6.16 defect_type=param_validation endpoint=entities+search]

--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] search with nprobe=0 on IVF/autoindex -> http=200, code=0
- [c2] control: search with limit=0 -> http=200, code=65535

执行日志全文（output_milvus_009.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_nprobe", "dbName": "default"}
=== RESP 1 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_nprobe", "dimension": 4, "metricType": "L2"}
=== RESP 2 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_nprobe", "data": [{"id": 0, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 1, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 2, "vector": [0.1, 0.2, 0.3, 0.4]}]}
=== RESP 3 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":3,"insertIds":[0,1,2]}}

=== REQ 4 ===
POST http://localhost:19530/v2/vectordb/collections/load
payload: {"collectionName": "test_nprobe", "dbName": "default"}
=== RESP 4 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 5 ===
POST http://localhost:19530/v2/vectordb/entities/search
payload: {"collectionName": "test_nprobe", "data": [[1.0, 2.0, 3.0, 4.0]], "limit": 3, "searchParams": {"nprobe": 0}, "outputFields": ["id"]}
=== RESP 5 ===
status: 200
body: {"code":0,"cost":0,"data":[{"distance":24.3,"id":0},{"distance":24.3,"id":1},{"distance":24.3,"id":2}],"topks":[3]}


=== REQ 6 ===
POST http://localhost:19530/v2/vectordb/entities/search
payload: {"collectionName": "test_nprobe", "data": [[1.0, 2.0, 3.0, 4.0]], "limit": 0, "searchParams": {"nprobe": 1}}
=== RESP 6 ===
status: 200
body: {"code":65535,"message":"topk [0] is invalid, it should be in range [1, 16384], but got 0"}

=== REQ 7 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_nprobe", "dbName": "default"}
=== RESP 7 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 8 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_nprobe", "dimension": 4, "metricType": "L2"}
=== RESP 8 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 9 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_nprobe", "data": [{"id": 0, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 1, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 2, "vector": [0.1, 0.2, 0.3, 0.4]}]}
=== RESP 9 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":3,"insertIds":[0,1,2]}}

=== REQ 10 ===
POST http://localhost:19530/v2/vectordb/collections/load
payload: {"collectionName": "test_nprobe", "dbName": "default"}
=== RESP 10 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 11 ===
POST http://localhost:19530/v2/vectordb/entities/search
payload: {"collectionName": "test_nprobe", "data": [[1.0, 2.0, 3.0, 4.0]], "limit": 3, "searchParams": {"nprobe": 0}, "outputFields": ["id"]}
=== RESP 11 ===
status: 200
body: {"code":0,"cost":0,"data":[{"distance":24.3,"id":0},{"distance":24.3,"id":1},{"distance":24.3,"id":2}],"topks":[3]}


=== REQ 12 ===
POST http://localhost:19530/v2/vectordb/entities/search
payload: {"collectionName": "test_nprobe", "data": [[1.0, 2.0, 3.0, 4.0]], "limit": 0, "searchParams": {"nprobe": 1}}
=== RESP 12 ===
status: 200
body: {"code":65535,"message":"topk [0] is invalid, it should be in range [1, 16384], but got 0"}



--- 契约依据（expected，来自该版本 API 契约） ---
约束条目（10 条，来自 milvus 2.6.16 契约，endpoint=entities+search）：
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

相关契约段（关键词定位 3 条）：
{"endpoint": "entities+search", "kind": "type_constraints", "description": "data must be array of float arrays, annsField must be a vector field, limit must be positive integer", "assertion": "data is array[array[float]] AND annsField is a vector field AND limit > 0", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Vector%20(v2)/Search.md", "confidence": 1.0}
{"endpoint": "entities+query", "kind": "range_constraints", "description": "limit + offset must be < 16384", "assertion": "limit + offset < 16384", "source_url": "https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go", "confidence": 1.0}
{"endpoint": "entities+search", "kind": "range_constraints", "description": "limit + offset must be < 16384", "assertion": "limit + offset < 16384", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Vector%20(v2)/Search.md", "confidence": 1.0}

VERDICT: UNKNOWN (replay capture — no attack-agent assertion output; raw HTTP only)

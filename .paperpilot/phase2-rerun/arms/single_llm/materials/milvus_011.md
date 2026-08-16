=== 候选缺陷 milvus_011 ===
[vendor=milvus version=2.6.16 defect_type=semantics endpoint=entities+query]

--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] query with filter=null -> http=200, code=0, returned all rows
- [c2] query with filter omitted -> http=200, code=0, returned all rows
- [c3] control: query with filter='' -> http=200, code=0

执行日志全文（output_milvus_011.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_coll", "dbName": "default"}
=== RESP 1 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_coll", "dimension": 4}
=== RESP 2 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_coll", "data": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 2, "vector": [0.2, 0.2, 0.3, 0.4]}]}
=== RESP 3 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":2,"insertIds":[1,2]}}

=== REQ 4 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_coll", "filter": null, "outputFields": ["id"]}
=== RESP 4 ===
status: 200
body: {"code":0,"cost":0,"data":[{"id":1},{"id":2}]}


=== REQ 5 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_coll", "outputFields": ["id"]}
=== RESP 5 ===
status: 200
body: {"code":0,"cost":0,"data":[{"id":1},{"id":2}]}


=== REQ 6 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_coll", "filter": "", "outputFields": ["id"]}
=== RESP 6 ===
status: 200
body: {"code":0,"cost":0,"data":[{"id":1},{"id":2}]}


=== REQ 7 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_coll", "dbName": "default"}
=== RESP 7 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 8 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_coll", "dimension": 4}
=== RESP 8 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 9 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_coll", "data": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 2, "vector": [0.2, 0.2, 0.3, 0.4]}]}
=== RESP 9 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":2,"insertIds":[1,2]}}

=== REQ 10 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_coll", "filter": null, "outputFields": ["id"]}
=== RESP 10 ===
status: 200
body: {"code":0,"cost":0,"data":[{"id":1},{"id":2}]}


=== REQ 11 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_coll", "outputFields": ["id"]}
=== RESP 11 ===
status: 200
body: {"code":0,"cost":0,"data":[{"id":1},{"id":2}]}


=== REQ 12 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_coll", "filter": "", "outputFields": ["id"]}
=== RESP 12 ===
status: 200
body: {"code":0,"cost":0,"data":[{"id":1},{"id":2}]}




--- 契约依据（expected，来自该版本 API 契约） ---
约束条目（7 条，来自 milvus 2.6.16 契约，endpoint=entities+query）：
{"constraint_id": "milvus_type_entities_delete_001", "endpoint": "entities+delete", "type": "type_constraint", "description": "filter must be a valid boolean expression string", "assertion": "filter is a valid boolean expression", "source_url": "https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go", "confidence": 1.0}
{"constraint_id": "milvus_type_entities_query_001", "endpoint": "entities+query", "type": "type_constraint", "description": "filter must be a valid boolean expression string", "assertion": "filter is a valid boolean expression", "source_url": "https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go", "confidence": 1.0}
{"constraint_id": "milvus_type_entities_get_001", "endpoint": "entities+get", "type": "type_constraint", "description": "id must match the collection primary key type (Int64 or VarChar)", "assertion": "id type matches collection primary key type", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Vector%20(v2)/Get.md", "confidence": 1.0}
{"constraint_id": "milvus_range_entities_query_001", "endpoint": "entities+query", "type": "range_constraint", "description": "limit + offset must be < 16384", "assertion": "limit + offset < 16384", "source_url": "https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go", "confidence": 1.0}
{"constraint_id": "milvus_state_entities_delete_001", "endpoint": "entities+delete", "type": "state_constraint", "description": "Deleted entities cannot be recovered", "assertion": "delete is irreversible", "source_url": "https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go", "confidence": 1.0}
{"assertion_id": "milvus_behavioral_entities_delete_001", "endpoint": "entities+delete", "description": "Delete returns 400 on invalid filter expression", "source_url": "https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go", "confidence": 1.0}
{"assertion_id": "milvus_behavioral_entities_get_001", "endpoint": "entities+get", "description": "Get entities returns 400 if id type mismatches collection schema", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Vector%20(v2)/Get.md", "confidence": 1.0}

相关契约段（关键词定位 2 条）：
{"endpoint": "collections+drop", "kind": "state_constraints", "description": "Drop is irreversible; all data in the collection is permanently deleted", "assertion": "drop is irreversible AND all data is permanently deleted", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Drop.md", "confidence": 1.0}
{"endpoint": "entities+insert", "kind": "range_constraints", "description": "Max 100 entities per single insert call via REST API", "assertion": "len(data) <= 100", "source_url": "https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go", "confidence": 1.0}

API 模板：endpoint=entities+insert doc_quote='200 on success with insert count and IDs; 400 on schema mismatch' source=None

VERDICT: UNKNOWN (replay capture — no attack-agent assertion output; raw HTTP only)

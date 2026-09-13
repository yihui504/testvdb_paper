=== 候选缺陷 milvus_005 ===
[vendor=milvus version=2.6.10 defect_type=doc_mismatch endpoint=entities+insert]
--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] insert dynamic field names '123field'/'@field' -> http=200, code=0
- [c1_q] query field '123field' -> http=200, code=65535, message: parse output field name failed: 123field
- [c2] control: insert valid field name -> http=200, code=0
- [c2_q] control: query valid field -> http=200, code=101, message: collection not loaded

执行日志全文（output_milvus_005.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_<tracked>", "dbName": "default"}
=== RESP 1 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_<tracked>", "schema": {"autoID": false, "enableDynamicField": true, "fields": [{"fieldName": "id", "dataType": "Int64", "isPrimary": true}, {"fieldName": "vector", "dataType": "FloatVector", "elementTypeParams": {"dim": 4}}]}}
=== RESP 2 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_<tracked>", "data": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4], "123field": "v1"}, {"id": 2, "vector": [0.2, 0.2, 0.3, 0.4], "@field": "v2"}]}
=== RESP 3 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":2,"insertIds":[1,2]}}

=== REQ 4 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_<tracked>", "filter": "id in [1,2]", "outputFields": ["123field", "@field"]}
=== RESP 4 ===
status: 200
body: {"code":65535,"message":"parse output field name failed: 123field"}

=== REQ 5 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_<tracked>", "data": [{"id": 3, "vector": [0.3, 0.2, 0.3, 0.4], "valid_field": "ok"}]}
=== RESP 5 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":1,"insertIds":[3]}}

=== REQ 6 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_<tracked>", "filter": "id==3", "outputFields": ["valid_field"]}
=== RESP 6 ===
status: 200
body: {"code":101,"message":"failed to query: collection not loaded[collection=468359262963438392]"}

=== REQ 7 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_<tracked>", "dbName": "default"}
=== RESP 7 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 8 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_<tracked>", "schema": {"autoID": false, "enableDynamicField": true, "fields": [{"fieldName": "id", "dataType": "Int64", "isPrimary": true}, {"fieldName": "vector", "dataType": "FloatVector", "elementTypeParams": {"dim": 4}}]}}
=== RESP 8 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 9 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_<tracked>", "data": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4], "123field": "v1"}, {"id": 2, "vector": [0.2, 0.2, 0.3, 0.4], "@field": "v2"}]}
=== RESP 9 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":2,"insertIds":[1,2]}}

=== REQ 10 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_<tracked>", "filter": "id in [1,2]", "outputFields": ["123field", "@field"]}
=== RESP 10 ===
status: 200
body: {"code":65535,"message":"parse output field name failed: 123field"}

=== REQ 11 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_<tracked>", "data": [{"id": 3, "vector": [0.3, 0.2, 0.3, 0.4], "valid_field": "ok"}]}
=== RESP 11 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":1,"insertIds":[3]}}

=== REQ 12 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_<tracked>", "filter": "id==3", "outputFields": ["valid_field"]}
=== RESP 12 ===
status: 200
body: {"code":101,"message":"failed to query: collection not loaded[collection=468359683278836488]"}

--- 契约依据（expected，M1 过滤后初稿） ---
约束条目（11 条，来自 milvus 2.6.10 契约，endpoint=entities+insert）：
{"constraint_id": "milvus_type_entities_insert_001", "endpoint": "entities+insert", "type": "type_constraint", "description": "data must contain field values matching collection schema data types", "assertion": "data field types match collection schema", "source_url": "https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go", "confidence": 1.0, "_audit": {"g1": "aligned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": [], "priority": "bulk"}}
{"constraint_id": "milvus_type_entities_delete_001", "endpoint": "entities+delete", "type": "type_constraint", "description": "filter must be a valid boolean expression string", "assertion": "filter is a valid boolean expression", "source_url": "https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go", "confidence": 1.0, "_audit": {"g1": "aligned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["filter"], "priority": "bulk"}}
{"constraint_id": "milvus_type_entities_get_001", "endpoint": "entities+get", "type": "type_constraint", "description": "id must match the collection primary key type (Int64 or VarChar)", "assertion": "id type matches collection primary key type", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Vector%20(v2)/Get.md", "confidence": 1.0, "_audit": {"g1": "aligned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": [], "priority": "bulk"}}
{"constraint_id": "milvus_range_entities_insert_001", "endpoint": "entities+insert", "type": "range_constraint", "description": "REST insert has no fixed row-count limit; request size is bounded by payload-size limits, not by an entity count", "assertion": "no fixed upper bound on len(data); inserts of any row count that fits the request payload are accepted (HTTP 200)", "source_url": "https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go", "confidence": 1.0, "_audit": {"g1": "aligned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["HTTP", "any", "are", "bound", "bounded", "count", "entity", "has", "insert", "len", "limit", "not"], "priority": "bulk"}}
{"constraint_id": "milvus_range_entities_insert_002", "endpoint": "entities+insert", "type": "range_constraint", "description": "Vector dimension must match collection dimension", "assertion": "vector dimension == collection dimension", "source_url": "https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go", "confidence": 1.0, "_audit": {"g1": "aligned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["Vector"], "priority": "bulk"}}
{"constraint_id": "milvus_state_entities_insert_001", "endpoint": "entities+insert", "type": "state_constraint", "description": "Collection must exist and be loaded; if autoID is disabled, primary key must be provided", "assertion": "collection exists AND is loaded AND (autoID OR primary key provided)", "source_url": "https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go", "confidence": 1.0, "_audit": {"g1": "aligned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["AND", "Collection", "autoID", "key", "primary"], "priority": "bulk"}}
{"constraint_id": "milvus_state_entities_delete_001", "endpoint": "entities+delete", "type": "state_constraint", "description": "Deleted entities cannot be recovered", "assertion": "delete is irreversible", "source_url": "https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go", "confidence": 1.0, "_audit": {"g1": "aligned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["delete", "entities"], "priority": "bulk"}}
{"assertion_id": "milvus_behavioral_entities_insert_001", "endpoint": "entities+insert", "description": "Insert returns insert count and IDs on success", "source_url": "https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go", "confidence": 1.0, "_audit": {"g1": "aligned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["IDs", "Insert", "count", "insert"], "priority": "bulk"}}
{"assertion_id": "milvus_behavioral_entities_insert_002", "endpoint": "entities+insert", "description": "Insert returns 400 on schema mismatch", "source_url": "https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go", "confidence": 1.0, "_audit": {"g1": "aligned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["Insert"], "priority": "bulk"}}
{"assertion_id": "milvus_behavioral_entities_delete_001", "endpoint": "entities+delete", "description": "Delete returns 400 on invalid filter expression", "source_url": "https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go", "confidence": 1.0, "_audit": {"g1": "aligned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["Delete", "filter"], "priority": "bulk"}}
{"assertion_id": "milvus_behavioral_entities_get_001", "endpoint": "entities+get", "description": "Get entities returns 400 if id type mismatches collection schema", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Vector%20(v2)/Get.md", "confidence": 1.0, "_audit": {"g1": "aligned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["Get", "entities"], "priority": "bulk"}}
相关契约段（关键词定位 1 条）：
API 模板：endpoint=resource_groups+list doc_quote='200 with list of resource group names' source=None
VERDICT: UNKNOWN (replay capture — no attack-agent assertion output; raw HTTP only)
--- 补充契约行（M1 端点过滤后） ---
{"constraint_id": "milvus_state_entities_insert_001", "endpoint": "entities+insert", "description": "Collection must exist and be loaded; if autoID is disabled, primary key must be provided", "assertion": "collection exists AND is loaded AND (autoID OR primary key provided)", "type": "state_constraint", "confidence": 1.0, "source_url": "https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go", "source_status": "reachable", "_audit": {"g1": "aligned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["AND", "Collection", "autoID", "key", "primary"], "priority": "bulk"}}
{"constraint_id": "milvus_type_entities_insert_001", "endpoint": "entities+insert", "description": "data must contain field values matching collection schema data types", "assertion": "data field types match collection schema", "type": "type_constraint", "confidence": 1.0, "source_url": "https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go", "source_status": "reachable", "_audit": {"g1": "aligned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": [], "priority": "bulk"}}
{"constraint_id": "milvus_range_entities_insert_001", "endpoint": "entities+insert", "description": "Max 100 entities per single insert call via REST API", "assertion": "len(data) <= 100", "type": "range_constraint", "confidence": 1.0, "source_url": "https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go", "source_status": "reachable", "_audit": {"g1": "aligned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["Max", "call", "entities", "insert", "len", "per"], "priority": "bulk"}}

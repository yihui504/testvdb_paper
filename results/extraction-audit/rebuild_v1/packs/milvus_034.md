=== 候选缺陷 milvus_034 ===
[vendor=milvus version=3.0.0 defect_type=semantics endpoint=entities+upsert]
--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] REST upsert bare string into JSON field -> http=200, code=0
- [c1_q] query meta after REST upsert -> http=200, code=101, message: collection not loaded
- [c1_grpc_get] gRPC get id=0 -> code=101, message: collection not loaded
- [c1b] gRPC upsert plain string -> DataNotMatchException code=1, message: Invalid JSON string

执行日志全文（output_milvus_034.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_json", "dbName": "default"}
=== RESP 1 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_json", "schema": {"autoId": false, "enableDynamicField": false, "fields": [{"fieldName": "id", "dataType": "Int64", "isPrimary": true}, {"fieldName": "vector", "dataType": "FloatVector", "elementTypeParams": {"dim": 4}}, {"fieldName": "meta", "dataType": "JSON"}]}}
=== RESP 2 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/indexes/create
payload: {"collectionName": "test_json", "indexParams": [{"fieldName": "vector", "metricType": "COSINE", "indexType": "AUTOINDEX"}]}
=== RESP 3 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 4 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_json", "data": [{"id": 0, "vector": [0.1, 0.2, 0.3, 0.4], "meta": {"important": "data"}}]}
=== RESP 4 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":1,"insertIds":[0]}}

=== REQ 5 ===
POST http://localhost:19530/v2/vectordb/entities/upsert
payload: {"collectionName": "test_json", "data": [{"id": 0, "vector": [0.9, 0.9, 0.9, 0.9], "meta": "invalid_json"}]}
=== RESP 5 ===
status: 200
body: {"code":0,"cost":0,"data":{"upsertCount":1,"upsertIds":[0]}}

=== REQ 6 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_json", "filter": "id in [0,1]", "outputFields": ["meta"]}
=== RESP 6 ===
status: 200
body: {"code":101,"message":"failed to query: collection not loaded[collection=468359099811365880]"}

=== REQ 7 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_json", "filter": "id==1", "outputFields": ["meta"]}
=== RESP 7 ===
status: 200
body: {"code":101,"message":"failed to query: collection not loaded[collection=468359099811365880]"}

=== REQ 8 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_json", "dbName": "default"}
=== RESP 8 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 9 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_json", "schema": {"autoId": false, "enableDynamicField": false, "fields": [{"fieldName": "id", "dataType": "Int64", "isPrimary": true}, {"fieldName": "vector", "dataType": "FloatVector", "elementTypeParams": {"dim": 4}}, {"fieldName": "meta", "dataType": "JSON"}]}}
=== RESP 9 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 10 ===
POST http://localhost:19530/v2/vectordb/indexes/create
payload: {"collectionName": "test_json", "indexParams": [{"fieldName": "vector", "metricType": "COSINE", "indexType": "AUTOINDEX"}]}
=== RESP 10 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 11 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_json", "data": [{"id": 0, "vector": [0.1, 0.2, 0.3, 0.4], "meta": {"important": "data"}}]}
=== RESP 11 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":1,"insertIds":[0]}}

=== REQ 12 ===
POST http://localhost:19530/v2/vectordb/entities/upsert
payload: {"collectionName": "test_json", "data": [{"id": 0, "vector": [0.9, 0.9, 0.9, 0.9], "meta": "invalid_json"}]}
=== RESP 12 ===
status: 200
body: {"code":0,"cost":0,"data":{"upsertCount":1,"upsertIds":[0]}}

=== REQ 13 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_json", "filter": "id in [0,1]", "outputFields": ["meta"]}
=== RESP 13 ===
status: 200
body: {"code":101,"message":"failed to query: collection not loaded[collection=468359869996729341]"}

=== REQ 14 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_json", "filter": "id==1", "outputFields": ["meta"]}
=== RESP 14 ===
status: 200
body: {"code":101,"message":"failed to query: collection not loaded[collection=468359869996729341]"}

--- 契约依据（expected，M1 过滤后初稿） ---
[经端点过滤后无相关契约行；需人工考古 endpoint=entities+upsert]
[契约中无 endpoint=entities+upsert 的约束条目]
相关契约段（关键词定位 4 条）：
API 模板：endpoint=entities+get doc_quote='Get entities' source=None
VERDICT: UNKNOWN (replay capture — no attack-agent assertion output; raw HTTP only)
--- 补充契约行（M1 端点过滤后） ---
{"constraint_id": "milvus_type_entities_upsert_001", "endpoint": "entities+upsert", "description": "Primary key field must be specified in data for upsert", "assertion": "data contains primary key field", "type": "type_constraint", "confidence": 1.0, "source_url": "https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go", "source_status": "reachable", "_audit": {"g1": "MISMATCH", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["Primary", "key", "primary", "upsert"], "priority": "bulk"}}

=== 候选缺陷 milvus_037 ===
[vendor=milvus version=3.0.0 defect_type=type_coercion endpoint=entities+insert]
--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] REST insert string '123' into INT64 field -> http=200, code=0
- [c1_q] query int64_f -> http=200, code=101, message: collection not loaded
- [c2] REST insert int 123 into VarChar field -> http=200, code=0
- [c2_q] query varchar_f -> http=200, code=101, message: collection not loaded
- [c3] REST insert string 'true' into BOOL field -> http=200, code=0
- [c3_q] query bool_f -> http=200, code=101, message: collection not loaded

执行日志全文（output_milvus_037.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_coerce", "data": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4], "int64_f": "123"}]}
=== RESP 1 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":1,"insertIds":[1]}}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_coerce", "filter": "id==1", "outputFields": ["int64_f"]}
=== RESP 2 ===
status: 200
body: {"code":101,"message":"failed to query: collection not loaded[collection=468359099812566979]"}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_coerce", "data": [{"id": 2, "vector": [0.1, 0.2, 0.3, 0.4], "varchar_f": 123}]}
=== RESP 3 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":1,"insertIds":[2]}}

=== REQ 4 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_coerce", "filter": "id==2", "outputFields": ["varchar_f"]}
=== RESP 4 ===
status: 200
body: {"code":101,"message":"failed to query: collection not loaded[collection=468359099812566979]"}

=== REQ 5 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_coerce", "data": [{"id": 3, "vector": [0.1, 0.2, 0.3, 0.4], "bool_f": "true"}]}
=== RESP 5 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":1,"insertIds":[3]}}

=== REQ 6 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_coerce", "filter": "id==3", "outputFields": ["bool_f"]}
=== RESP 6 ===
status: 200
body: {"code":101,"message":"failed to query: collection not loaded[collection=468359099812566979]"}

=== REQ 7 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_coerce", "data": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4], "int64_f": "123"}]}
=== RESP 7 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":1,"insertIds":[1]}}

=== REQ 8 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_coerce", "filter": "id==1", "outputFields": ["int64_f"]}
=== RESP 8 ===
status: 200
body: {"code":101,"message":"failed to query: collection not loaded[collection=468359869997930433]"}

=== REQ 9 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_coerce", "data": [{"id": 2, "vector": [0.1, 0.2, 0.3, 0.4], "varchar_f": 123}]}
=== RESP 9 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":1,"insertIds":[2]}}

=== REQ 10 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_coerce", "filter": "id==2", "outputFields": ["varchar_f"]}
=== RESP 10 ===
status: 200
body: {"code":101,"message":"failed to query: collection not loaded[collection=468359869997930433]"}

=== REQ 11 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_coerce", "data": [{"id": 3, "vector": [0.1, 0.2, 0.3, 0.4], "bool_f": "true"}]}
=== RESP 11 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":1,"insertIds":[3]}}

=== REQ 12 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_coerce", "filter": "id==3", "outputFields": ["bool_f"]}
=== RESP 12 ===
status: 200
body: {"code":101,"message":"failed to query: collection not loaded[collection=468359869997930433]"}

--- 契约依据（expected，M1 过滤后初稿） ---
约束条目（3 条，来自 milvus 3.0.0 契约，endpoint=entities+insert）：
{"constraint_id": "milvus_state_insert_collection_001", "endpoint": "entities+insert", "type": "state_constraint", "description": "Insert requires existing collection", "assertion": "collection MUST exist before insert", "source_url": "https://milvus.io/docs/schema.md", "confidence": 1.0, "_audit": {"g1": "page-unversioned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["Insert", "MUST", "before", "insert"], "priority": "bulk"}}
{"assertion_id": "milvus_behavioral_insert_then_get_001", "endpoint": "entities+insert", "description": "Inserted entities should be retrievable", "source_url": "https://milvus.io/docs/insert-update.md", "confidence": 1.0, "_audit": {"g1": "page-unversioned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["Inserted", "entities"], "priority": "bulk"}}
{"assertion_id": "milvus_assert_insert_success_001", "endpoint": "entities+insert", "description": "Inserting valid data succeeds", "source_url": "https://milvus.io/docs/schema.md", "confidence": 1.0, "_audit": {"g1": "page-unversioned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": [], "priority": "bulk"}}
相关契约段（关键词定位 4 条）：
API 模板：endpoint=entities+insert doc_quote='Insert entities' source=None
VERDICT: UNKNOWN (replay capture — no attack-agent assertion output; raw HTTP only)
--- 补充契约行（M1 端点过滤后） ---
{"constraint_id": "milvus_type_entities_insert_001", "endpoint": "entities+insert", "description": "data must contain field values matching collection schema data types", "assertion": "data field types match collection schema", "type": "type_constraint", "confidence": 1.0, "source_url": "https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go", "source_status": "reachable", "_audit": {"g1": "MISMATCH", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": [], "priority": "bulk"}}
{"constraint_id": "milvus_range_entities_insert_001", "endpoint": "entities+insert", "description": "Max 100 entities per single insert call via REST API", "assertion": "len(data) <= 100", "type": "range_constraint", "confidence": 1.0, "source_url": "https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go", "source_status": "reachable", "_audit": {"g1": "MISMATCH", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["Max", "call", "entities", "insert", "len", "per"], "priority": "bulk"}}

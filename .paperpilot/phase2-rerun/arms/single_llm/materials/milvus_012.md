=== 候选缺陷 milvus_012 ===
[vendor=milvus version=2.6.16 defect_type=param_validation endpoint=collections+list]

--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] collections/list with dbName empty -> http=200, code=0
- [c2] control: query with filter='' -> http=200, code=100

执行日志全文（output_milvus_012.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/collections/list
payload: {"dbName": ""}
=== RESP 1 ===
status: 200
body: {"code":0,"data":["test_nprobe","test_ttl_neg","test_coll"]}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "some_coll", "filter": ""}
=== RESP 2 ===
status: 200
body: {"code":100,"message":"can't find collection[database=default][collection=some_coll]"}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/collections/list
payload: {"dbName": ""}
=== RESP 3 ===
status: 200
body: {"code":0,"data":["test_nprobe","test_ttl_neg","test_coll"]}

=== REQ 4 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "some_coll", "filter": ""}
=== RESP 4 ===
status: 200
body: {"code":100,"message":"can't find collection[database=default][collection=some_coll]"}



--- 契约依据（expected，来自该版本 API 契约） ---
[契约中无 endpoint=collections+list 的约束条目]

相关契约段（关键词定位 4 条）：
{"endpoint": "databases+drop", "kind": "state_constraints", "description": "Cannot drop the default database; database must be empty (no collections)", "assertion": "dbName != '_default' AND database has no collections", "source_url": "https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go", "confidence": 1.0}
{"endpoint": "collections+drop", "kind": "type_constraints", "description": "collectionName must be a non-empty string", "assertion": "collectionName is non-empty string", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Drop.md", "confidence": 1.0}
{"endpoint": "collections+load", "kind": "type_constraints", "description": "collectionName must be a non-empty string for load", "assertion": "collectionName is non-empty string", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Load.md", "confidence": 1.0}
{"endpoint": "collections+rename", "kind": "type_constraints", "description": "collectionName and newCollectionName must be non-empty strings", "assertion": "collectionName is non-empty string AND newCollectionName is non-empty string", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Rename.md", "confidence": 1.0}

API 模板：endpoint=collections+create doc_quote='200 on success; 400 on invalid parameters; 404 if database does not exist' source=None

VERDICT: UNKNOWN (replay capture — no attack-agent assertion output; raw HTTP only)

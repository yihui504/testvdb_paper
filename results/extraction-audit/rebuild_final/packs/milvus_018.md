=== 候选缺陷 milvus_018 ===
[vendor=milvus version=2.6.16 defect_type=behavior endpoint=collections+rename]
--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] concurrent rename->dst and create(dst): rename -> http=200, code=0; create -> http=200, code=0

执行日志全文（output_milvus_018.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_rename_src", "dbName": "default"}
=== RESP 1 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_rename_dst", "dbName": "default"}
=== RESP 2 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_rename_src", "dimension": 4, "metricType": "L2"}
=== RESP 3 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 4 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_rename_src", "data": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4]}]}
=== RESP 4 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":1,"insertIds":[1]}}

=== REQ 5 ===
POST http://localhost:19530/v2/vectordb/collections/rename
payload: {"collectionName": "test_rename_src", "newCollectionName": "test_rename_dst", "dbName": "default"}
=== RESP 5 ===
status: 200
body: {"code":65535,"message":"duplicated new collection name default:test_rename_dst with other collection name or alias"}

=== REQ 6 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_rename_dst", "dimension": 4, "metricType": "L2"}
=== RESP 6 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 7 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_rename_src", "dbName": "default"}
=== RESP 7 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 8 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_rename_dst", "dbName": "default"}
=== RESP 8 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 9 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_rename_src", "dimension": 4, "metricType": "L2"}
=== RESP 9 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 10 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_rename_src", "data": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4]}]}
=== RESP 10 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":1,"insertIds":[1]}}

=== REQ 11 ===
POST http://localhost:19530/v2/vectordb/collections/rename
payload: {"collectionName": "test_rename_src", "newCollectionName": "test_rename_dst", "dbName": "default"}
=== RESP 11 ===
status: 200
body: {"code":65535,"message":"duplicated new collection name default:test_rename_dst with other collection name or alias"}

=== REQ 12 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_rename_dst", "dimension": 4, "metricType": "L2"}
=== RESP 12 ===
status: 200
body: {"code":0,"data":{}}
--- 契约依据（expected，M3 重建版） ---
{"constraint_id": "milvus_type_collections_rename_001", "endpoint": "collections+rename", "type": "type_constraint", "description": "collectionName and newCollectionName must be non-empty strings", "assertion": "collectionName is non-empty string AND newCollectionName is non-empty string", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Rename.md", "confidence": 1.0, "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "milvus_type_collections_rename_001", "endpoint": "collections+rename", "description": "collectionName and newCollectionName must be non-empty strings", "assertion": "collectionName is non-empty string AND newCollectionName is non-empty string", "type": "type_constraint", "confidence": 1.0, "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Rename.md", "source_status": "reachable", "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}
--- 维护者态度参考（developer_cognition，vendor=milvus） ---
以下为该 vendor 维护者在历史 issue 中对同类现象的明确 by-design 表态（供判定参考；与本案是否相关由你判断）：
- [相关 issues: [50192]] Concurrent rename+create idempotent semantics: rename(dst) racing with create(dst) both returning success is tolerated—rename to an existing-name target is treated as idempotent no-op when parameters match（维护者原话: "sounds like a by designed. Milvus returns success if creating a collection with the same name and parameters."）
- [相关 issues: [50193]] get_stats rowCount reflects flushed data only: rowCount=0 after insert before flush is expected (query returns full rows; stats lag by design)（维护者原话: "This is by design. The entities number in collection stats only shows the data that flushed. Please retry with flush() after insert()."）
- [相关 issues: [50319]] REST v2 quick-create mode semantics: creating via quick/fast mode (dimension-only) auto-loads and does not enforce full schema/load-state checks; search on such collections succeeding is expected（维护者原话: "The behavior described here appears to come from REST v2 quick/fast collection creation mode, not from search/query bypassing the collection load-stat"）
- [相关 issues: [50351]] REST v2 create ignores unconsumed top-level fields: params not consumed by quick-create (e.g. top-level shardsNum) are silently ignored rather than rejected; consumed via params.shardsNum（维护者原话: "I think this is by design. The payload in this issue uses top-level shardsNum, but this field is not consumed by the REST v2 create API. shardsNum is "）

VERDICT: UNKNOWN (replay capture — no attack-agent assertion output; raw HTTP only)

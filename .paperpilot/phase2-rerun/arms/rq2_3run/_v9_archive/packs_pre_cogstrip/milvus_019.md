=== 候选缺陷 milvus_019 ===
[vendor=milvus version=2.6.16 defect_type=behavior endpoint=collections+get_stats]
--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] get_stats after insert+load -> http=200, code=0, rowCount=0
- [c1_q] query after insert+load -> http=200, code=0, returned 5 rows (id 0-4)

执行日志全文（output_milvus_019.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_rowcount", "dbName": "default"}
=== RESP 1 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_rowcount", "dimension": 4}
=== RESP 2 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_rowcount", "data": [{"id": 0, "value": 0, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 1, "value": 1, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 2, "value": 2, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 3, "value": 3, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 4, "value": 4, "vector": [0.1, 0.2, 0.3, 0.4]}]}
=== RESP 3 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":5,"insertIds":[0,1,2,3,4]}}

=== REQ 4 ===
POST http://localhost:19530/v2/vectordb/collections/load
payload: {"collectionName": "test_rowcount", "dbName": "default"}
=== RESP 4 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 5 ===
POST http://localhost:19530/v2/vectordb/collections/get_stats
payload: {"collectionName": "test_rowcount"}
=== RESP 5 ===
status: 200
body: {"code":0,"data":{"rowCount":0}}

=== REQ 6 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_rowcount", "filter": "id>=0", "outputFields": ["id"]}
=== RESP 6 ===
status: 200
body: {"code":0,"cost":0,"data":[{"id":0},{"id":1},{"id":2},{"id":3},{"id":4}]}


=== REQ 7 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_rowcount", "dbName": "default"}
=== RESP 7 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 8 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_rowcount", "dimension": 4}
=== RESP 8 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 9 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_rowcount", "data": [{"id": 0, "value": 0, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 1, "value": 1, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 2, "value": 2, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 3, "value": 3, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 4, "value": 4, "vector": [0.1, 0.2, 0.3, 0.4]}]}
=== RESP 9 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":5,"insertIds":[0,1,2,3,4]}}

=== REQ 10 ===
POST http://localhost:19530/v2/vectordb/collections/load
payload: {"collectionName": "test_rowcount", "dbName": "default"}
=== RESP 10 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 11 ===
POST http://localhost:19530/v2/vectordb/collections/get_stats
payload: {"collectionName": "test_rowcount"}
=== RESP 11 ===
status: 200
body: {"code":0,"data":{"rowCount":0}}

=== REQ 12 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_rowcount", "filter": "id>=0", "outputFields": ["id"]}
=== RESP 12 ===
status: 200
body: {"code":0,"cost":0,"data":[{"id":0},{"id":1},{"id":2},{"id":3},{"id":4}]}
--- 契约依据（expected，M3 重建版） ---
[经端点过滤与依据核查后，无 endpoint=collections+get_stats 的可核查约束行]
--- 维护者态度参考（developer_cognition，vendor=milvus） ---
以下为该 vendor 维护者在历史 issue 中对同类现象的明确 by-design 表态（供判定参考；与本案是否相关由你判断）：
- [相关 issues: [50192]] Concurrent rename+create idempotent semantics: rename(dst) racing with create(dst) both returning success is tolerated—rename to an existing-name target is treated as idempotent no-op when parameters match（维护者原话: "sounds like a by designed. Milvus returns success if creating a collection with the same name and parameters."）
- [相关 issues: [50193]] get_stats rowCount reflects flushed data only: rowCount=0 after insert before flush is expected (query returns full rows; stats lag by design)（维护者原话: "This is by design. The entities number in collection stats only shows the data that flushed. Please retry with flush() after insert()."）
- [相关 issues: [50319]] REST v2 quick-create mode semantics: creating via quick/fast mode (dimension-only) auto-loads and does not enforce full schema/load-state checks; search on such collections succeeding is expected（维护者原话: "The behavior described here appears to come from REST v2 quick/fast collection creation mode, not from search/query bypassing the collection load-stat"）
- [相关 issues: [50351]] REST v2 create ignores unconsumed top-level fields: params not consumed by quick-create (e.g. top-level shardsNum) are silently ignored rather than rejected; consumed via params.shardsNum（维护者原话: "I think this is by design. The payload in this issue uses top-level shardsNum, but this field is not consumed by the REST v2 create API. shardsNum is "）

VERDICT: UNKNOWN (replay capture — no attack-agent assertion output; raw HTTP only)

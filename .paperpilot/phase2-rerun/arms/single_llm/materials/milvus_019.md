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




--- 契约依据（expected，来自该版本 API 契约） ---
约束条目（1 条，来自 milvus 2.6.16 契约，endpoint=collections+get_stats）：
{"assertion_id": "milvus_behavioral_collections_get_stats_001", "endpoint": "collections+get_stats", "description": "Get stats returns row count and statistics", "source_url": "https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go", "confidence": 1.0}

API 模板：endpoint=collections+load doc_quote='200 on success; 404 if collection not found; 400 if no index exists on collection' source=None

VERDICT: UNKNOWN (replay capture — no attack-agent assertion output; raw HTTP only)

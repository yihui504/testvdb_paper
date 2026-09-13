=== 候选缺陷 milvus_029 ===
[vendor=milvus version=2.6.17 defect_type=behavior endpoint=entities+search]
--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] search with limit=0 -> http=200, code=65535
- [c2] search 64-dim vector on dim=4 collection -> http=200, code=1801

执行日志全文（output_milvus_029.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test", "dbName": "default"}
=== RESP 1 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test", "dimension": 4}
=== RESP 2 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test", "data": [{"id": 0, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 1, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 2, "vector": [0.1, 0.2, 0.3, 0.4]}]}
=== RESP 3 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":3,"insertIds":[0,1,2]}}

=== REQ 4 ===
POST http://localhost:19530/v2/vectordb/collections/load
payload: {"collectionName": "test", "dbName": "default"}
=== RESP 4 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 5 ===
POST http://localhost:19530/v2/vectordb/entities/search
payload: {"collectionName": "test", "data": [[1.0, 2.0, 3.0, 4.0]], "limit": 0}
=== RESP 5 ===
status: 200
body: {"code":65535,"message":"topk [0] is invalid, it should be in range [1, 16384], but got 0"}

=== REQ 6 ===
POST http://localhost:19530/v2/vectordb/entities/search
payload: {"collectionName": "test", "data": [[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]], "limit": 3}
=== RESP 6 ===
status: 200
body: {"code":1801,"message":"can only accept json format request, error: dimension: 4, but length of []float: 64: invalid parameter[expected=FloatVector][actual=[[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]]]"}
--- 契约依据（expected，M3 重建版） ---
{"endpoint": "entities+search", "kind": "type_constraints", "description": "data must be array of float arrays, annsField must be a vector field, limit must be positive integer", "assertion": "data is array[array[float]] AND annsField is a vector field AND limit > 0", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Vector%20(v2)/Search.md", "confidence": 1.0, "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}

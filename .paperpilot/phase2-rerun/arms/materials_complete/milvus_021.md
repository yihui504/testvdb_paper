=== 候选缺陷 milvus_021 ===
[vendor=milvus version=2.6.17 defect_type=behavior endpoint=entities+search]
--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] search on never-loaded collection -> http=200, code=0

执行日志全文（output_milvus_021.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_unloaded", "dbName": "default"}
=== RESP 1 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_unloaded", "dimension": 4, "metricType": "COSINE", "idType": "Int64", "autoID": false}
=== RESP 2 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_unloaded", "data": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4]}]}
=== RESP 3 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":1,"insertIds":[1]}}

=== REQ 4 ===
POST http://localhost:19530/v2/vectordb/entities/search
payload: {"collectionName": "test_unloaded", "data": [[0.1, 0.2, 0.3, 0.4]], "annsField": "vector", "limit": 5}
=== RESP 4 ===
status: 200
body: {"code":0,"cost":0,"data":[{"distance":1,"id":1}],"topks":[1]}
--- 契约依据（expected，M3 重建版） ---
[经端点过滤与依据核查后，无 endpoint=entities+search 的可核查约束行]

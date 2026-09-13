=== 候选缺陷 milvus_004 ===
[vendor=milvus version=2.6.10 defect_type=param_validation endpoint=entities+delete]
--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] search with descending IN range -> http=200, code=0, 1 result
- [c2] search with empty IN range -> http=200, code=0, 0 results

执行日志全文（output_milvus_004.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "repro_<tracked>", "dimension": 8, "metricType": "L2", "dbName": "default"}
=== RESP 1 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "repro_<tracked>", "dbName": "default", "data": [{"id": 0, "vector": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], "age": 0}, {"id": 1, "vector": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], "age": 10}, {"id": 2, "vector": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], "age": 20}, {"id": 3, "vector": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], "age": 30}, {"id": 4, "vector": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], "age": 40}]}
=== RESP 2 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":5,"insertIds":[0,1,2,3,4]}}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/entities/delete
payload: {"collectionName": "repro_<tracked>", "dbName": "default", "filter": "age in [10, 5]"}
=== RESP 3 ===
status: 200
body: {"code":0,"data":{"deleteCount":1}}
--- 契约依据（expected，M3 重建版） ---
[经端点过滤与依据核查后，无 endpoint=entities+delete 的可核查约束行]

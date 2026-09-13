=== 候选缺陷 milvus_024 ===
[vendor=milvus version=2.6.17 defect_type=behavior endpoint=entities+delete]
--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] delete with both filter and ids -> http=200, code=0

执行日志全文（output_milvus_024.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_del", "dbName": "default"}
=== RESP 1 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_del", "dimension": 4}
=== RESP 2 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_del", "data": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4]}]}
=== RESP 3 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":1,"insertIds":[1]}}

=== REQ 4 ===
POST http://localhost:19530/v2/vectordb/entities/delete
payload: {"collectionName": "test_del", "dbName": "default", "filter": "id > 0", "ids": [1, 2, 3]}
=== RESP 4 ===
status: 200
body: {"code":0,"data":{"deleteCount":1}}
--- 契约依据（expected，M3 重建版） ---
[经端点过滤与依据核查后，无 endpoint=entities+delete 的可核查约束行]

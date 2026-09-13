=== 候选缺陷 milvus_011 ===
[vendor=milvus version=2.6.16 defect_type=semantics endpoint=entities+query]
--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] query with filter=null -> http=200, code=0, returned all rows
- [c2] query with filter omitted -> http=200, code=0, returned all rows
- [c3] control: query with filter='' -> http=200, code=0

执行日志全文（output_milvus_011.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_coll", "dbName": "default"}
=== RESP 1 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_coll", "dimension": 4}
=== RESP 2 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_coll", "data": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 2, "vector": [0.2, 0.2, 0.3, 0.4]}]}
=== RESP 3 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":2,"insertIds":[1,2]}}

=== REQ 4 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_coll", "filter": null, "outputFields": ["id"]}
=== RESP 4 ===
status: 200
body: {"code":0,"cost":0,"data":[{"id":1},{"id":2}]}


=== REQ 5 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_coll", "outputFields": ["id"]}
=== RESP 5 ===
status: 200
body: {"code":0,"cost":0,"data":[{"id":1},{"id":2}]}


=== REQ 6 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_coll", "filter": "", "outputFields": ["id"]}
=== RESP 6 ===
status: 200
body: {"code":0,"cost":0,"data":[{"id":1},{"id":2}]}


=== REQ 7 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_coll", "dbName": "default"}
=== RESP 7 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 8 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_coll", "dimension": 4}
=== RESP 8 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 9 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_coll", "data": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 2, "vector": [0.2, 0.2, 0.3, 0.4]}]}
=== RESP 9 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":2,"insertIds":[1,2]}}

=== REQ 10 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_coll", "filter": null, "outputFields": ["id"]}
=== RESP 10 ===
status: 200
body: {"code":0,"cost":0,"data":[{"id":1},{"id":2}]}


=== REQ 11 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_coll", "outputFields": ["id"]}
=== RESP 11 ===
status: 200
body: {"code":0,"cost":0,"data":[{"id":1},{"id":2}]}


=== REQ 12 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_coll", "filter": "", "outputFields": ["id"]}
=== RESP 12 ===
status: 200
body: {"code":0,"cost":0,"data":[{"id":1},{"id":2}]}
--- 契约依据（expected，M3 重建版） ---
[经端点过滤与依据核查后，无 endpoint=entities+query 的可核查约束行]

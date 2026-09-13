=== 候选缺陷 milvus_020 ===
[vendor=milvus version=2.6.16 defect_type=behavior endpoint=entities+search]
--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1_before] search before delete -> http=200, code=0, 10 results (id 0-9)
- [c1] search after deleting ids 1-5 -> http=200, code=0, returned ids [0,1,2,3,4,5,6,7,8,9]

执行日志全文（output_milvus_020.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_stale_data", "dbName": "default"}
=== RESP 1 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_stale_data", "dimension": 4, "metricType": "L2"}
=== RESP 2 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/indexes/create
payload: {"collectionName": "test_stale_data", "indexParams": [{"fieldName": "vector", "metricType": "L2", "indexType": "HNSW", "params": {"M": 16, "efConstruction": 128}}]}
=== RESP 3 ===
status: 200
body: {"code":65535,"message":"CreateIndex failed: at most one distinct index is allowed per field"}

=== REQ 4 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_stale_data", "data": [{"id": 0, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 1, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 2, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 3, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 4, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 5, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 6, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 7, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 8, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 9, "vector": [0.1, 0.2, 0.3, 0.4]}]}
=== RESP 4 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":10,"insertIds":[0,1,2,3,4,5,6,7,8,9]}}

=== REQ 5 ===
POST http://localhost:19530/v2/vectordb/collections/load
payload: {"collectionName": "test_stale_data", "dbName": "default"}
=== RESP 5 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 6 ===
POST http://localhost:19530/v2/vectordb/entities/search
payload: {"collectionName": "test_stale_data", "data": [[0.1, 0.2, 0.3, 0.4]], "limit": 10, "outputFields": ["id"]}
=== RESP 6 ===
status: 200
body: {"code":0,"cost":0,"data":[{"distance":0,"id":0},{"distance":0,"id":1},{"distance":0,"id":2},{"distance":0,"id":3},{"distance":0,"id":4},{"distance":0,"id":5},{"distance":0,"id":6},{"distance":0,"id":7},{"distance":0,"id":8},{"distance":0,"id":9}],"topks":[10]}


=== REQ 7 ===
POST http://localhost:19530/v2/vectordb/entities/search
payload: {"collectionName": "test_stale_data", "data": [[0.1, 0.2, 0.3, 0.4]], "limit": 10, "outputFields": ["id"]}
=== RESP 7 ===
status: 200
body: {"code":0,"cost":0,"data":[{"distance":0,"id":0},{"distance":0,"id":1},{"distance":0,"id":2},{"distance":0,"id":3},{"distance":0,"id":4},{"distance":0,"id":5},{"distance":0,"id":6},{"distance":0,"id":7},{"distance":0,"id":8},{"distance":0,"id":9}],"topks":[10]}


=== REQ 8 ===
POST http://localhost:19530/v2/vectordb/entities/delete
payload: {"collectionName": "test_stale_data", "filter": "id in [1,2,3,4,5]", "dbName": "default"}
=== RESP 8 ===
status: 200
body: {"code":0,"data":{"deleteCount":5}}

=== REQ 9 ===
POST http://localhost:19530/v2/vectordb/entities/search
payload: {"collectionName": "test_stale_data", "data": [[0.1, 0.2, 0.3, 0.4]], "limit": 10, "outputFields": ["id"]}
=== RESP 9 ===
status: 200
body: {"code":0,"cost":0,"data":[{"distance":0,"id":0},{"distance":0,"id":1},{"distance":0,"id":2},{"distance":0,"id":3},{"distance":0,"id":4},{"distance":0,"id":5},{"distance":0,"id":6},{"distance":0,"id":7},{"distance":0,"id":8},{"distance":0,"id":9}],"topks":[10]}


=== REQ 10 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_stale_data", "dbName": "default"}
=== RESP 10 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 11 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_stale_data", "dimension": 4, "metricType": "L2"}
=== RESP 11 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 12 ===
POST http://localhost:19530/v2/vectordb/indexes/create
payload: {"collectionName": "test_stale_data", "indexParams": [{"fieldName": "vector", "metricType": "L2", "indexType": "HNSW", "params": {"M": 16, "efConstruction": 128}}]}
=== RESP 12 ===
status: 200
body: {"code":65535,"message":"CreateIndex failed: at most one distinct index is allowed per field"}

=== REQ 13 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_stale_data", "data": [{"id": 0, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 1, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 2, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 3, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 4, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 5, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 6, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 7, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 8, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 9, "vector": [0.1, 0.2, 0.3, 0.4]}]}
=== RESP 13 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":10,"insertIds":[0,1,2,3,4,5,6,7,8,9]}}

=== REQ 14 ===
POST http://localhost:19530/v2/vectordb/collections/load
payload: {"collectionName": "test_stale_data", "dbName": "default"}
=== RESP 14 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 15 ===
POST http://localhost:19530/v2/vectordb/entities/search
payload: {"collectionName": "test_stale_data", "data": [[0.1, 0.2, 0.3, 0.4]], "limit": 10, "outputFields": ["id"]}
=== RESP 15 ===
status: 200
body: {"code":0,"cost":0,"data":[{"distance":0,"id":0},{"distance":0,"id":1},{"distance":0,"id":2},{"distance":0,"id":3},{"distance":0,"id":4},{"distance":0,"id":5},{"distance":0,"id":6},{"distance":0,"id":7},{"distance":0,"id":8},{"distance":0,"id":9}],"topks":[10]}


=== REQ 16 ===
POST http://localhost:19530/v2/vectordb/entities/search
payload: {"collectionName": "test_stale_data", "data": [[0.1, 0.2, 0.3, 0.4]], "limit": 10, "outputFields": ["id"]}
=== RESP 16 ===
status: 200
body: {"code":0,"cost":0,"data":[{"distance":0,"id":0},{"distance":0,"id":1},{"distance":0,"id":2},{"distance":0,"id":3},{"distance":0,"id":4},{"distance":0,"id":5},{"distance":0,"id":6},{"distance":0,"id":7},{"distance":0,"id":8},{"distance":0,"id":9}],"topks":[10]}


=== REQ 17 ===
POST http://localhost:19530/v2/vectordb/entities/delete
payload: {"collectionName": "test_stale_data", "filter": "id in [1,2,3,4,5]", "dbName": "default"}
=== RESP 17 ===
status: 200
body: {"code":0,"data":{"deleteCount":5}}

=== REQ 18 ===
POST http://localhost:19530/v2/vectordb/entities/search
payload: {"collectionName": "test_stale_data", "data": [[0.1, 0.2, 0.3, 0.4]], "limit": 10, "outputFields": ["id"]}
=== RESP 18 ===
status: 200
body: {"code":0,"cost":0,"data":[{"distance":0,"id":0},{"distance":0,"id":1},{"distance":0,"id":2},{"distance":0,"id":3},{"distance":0,"id":4},{"distance":0,"id":5},{"distance":0,"id":6},{"distance":0,"id":7},{"distance":0,"id":8},{"distance":0,"id":9}],"topks":[10]}
--- 契约依据（expected，M3 重建版） ---
[经端点过滤与依据核查后，无 endpoint=entities+search 的可核查约束行]

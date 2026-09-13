=== 候选缺陷 milvus_003 ===
[vendor=milvus version=2.6.10 defect_type=param_validation endpoint=entities+search]
--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] HNSW search with ef=0 -> http=200, code=0, returned 10 results

执行日志全文（output_milvus_003.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "repro_<tracked>", "dimension": 8, "metricType": "L2", "dbName": "default"}
=== RESP 1 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "repro_<tracked>", "dbName": "default", "data": [{"id": 0, "vector": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]}, {"id": 1, "vector": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]}, {"id": 2, "vector": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]}, {"id": 3, "vector": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]}, {"id": 4, "vector": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]}, {"id": 5, "vector": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]}, {"id": 6, "vector": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]}, {"id": 7, "vector": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]}, {"id": 8, "vector": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]}, {"id": 9, "vector": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]}]}
=== RESP 2 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":10,"insertIds":[0,1,2,3,4,5,6,7,8,9]}}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/indexes/create
payload: {"collectionName": "repro_<tracked>", "dbName": "default", "indexParams": [{"fieldName": "vector", "indexName": "idx_vec", "metricType": "L2", "indexType": "HNSW", "params": {"M": 8, "efConstruction": 64}}]}
=== RESP 3 ===
status: 200
body: {"code":65535,"message":"CreateIndex failed: creating multiple indexes on same field is not supported"}

=== REQ 4 ===
POST http://localhost:19530/v2/vectordb/collections/load
payload: {"collectionName": "repro_<tracked>", "dbName": "default"}
=== RESP 4 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 5 ===
POST http://localhost:19530/v2/vectordb/entities/search
payload: {"collectionName": "repro_<tracked>", "dbName": "default", "data": [[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]], "limit": 3, "searchParams": {"ef": 0}, "outputFields": ["id"]}
=== RESP 5 ===
status: 200
body: {"code":0,"cost":0,"data":[{"distance":0,"id":0},{"distance":0,"id":1},{"distance":0,"id":2}],"topks":[3]}
--- 契约依据（expected，M3 重建版） ---
[经端点过滤与依据核查后，无 endpoint=entities+search 的可核查约束行]

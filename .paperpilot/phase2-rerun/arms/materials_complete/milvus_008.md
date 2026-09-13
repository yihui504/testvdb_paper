=== 候选缺陷 milvus_008 ===
[vendor=milvus version=2.6.12 defect_type=behavior endpoint=entities+search]
--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] COSINE identical-vector search over 100 queries: max_distance=1.000000238418579, 11 queries with distance>1.0

执行日志全文（output_milvus_008.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "repro_<tracked>", "dimension": 4, "metricType": "COSINE", "dbName": "default"}
=== RESP 1 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "repro_<tracked>", "dbName": "default", "data": [{"id": 0, "vector": [0.1, 0.1, 0.1, 0.1]}, {"id": 1, "vector": [0.1, 0.1, 0.1, 0.1]}, {"id": 2, "vector": [0.1, 0.1, 0.1, 0.1]}, {"id": 3, "vector": [0.1, 0.1, 0.1, 0.1]}, {"id": 4, "vector": [0.1, 0.1, 0.1, 0.1]}, {"id": 5, "vector": [0.1, 0.1, 0.1, 0.1]}, {"id": 6, "vector": [0.1, 0.1, 0.1, 0.1]}, {"id": 7, "vector": [0.1, 0.1, 0.1, 0.1]}, {"id": 8, "vector": [0.1, 0.1, 0.1, 0.1]}, {"id": 9, "vector": [0.1, 0.1, 0.1, 0.1]}]}
=== RESP 2 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":10,"insertIds":[0,1,2,3,4,5,6,7,8,9]}}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/indexes/create
payload: {"collectionName": "repro_<tracked>", "dbName": "default", "indexParams": [{"fieldName": "vector", "indexName": "idx_vec", "metricType": "COSINE", "indexType": "FLAT", "params": {"nlist": 8}}]}
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
payload: {"collectionName": "repro_<tracked>", "dbName": "default", "data": [[0.1, 0.1, 0.1, 0.1]], "limit": 3, "outputFields": ["*"]}
=== RESP 5 ===
status: 200
body: {"code":0,"cost":0,"data":[{"distance":1,"id":0,"vector":[0.1,0.1,0.1,0.1]},{"distance":1,"id":1,"vector":[0.1,0.1,0.1,0.1]},{"distance":1,"id":2,"vector":[0.1,0.1,0.1,0.1]}],"topks":[3]}
--- 契约依据（expected，M3 重建版） ---
{"constraint_id": "milvus_metric_cosine_range_001", "endpoint": "entities+search", "description": "COSINE metric: similarity distance value range", "assertion": "COSINE: similarity distance value range is [-1, 1]; a greater value indicates a greater similarity", "source_url": "https://raw.githubusercontent.com/milvus-io/milvus-docs/v2.6.x/site/en/userGuide/search-query-get/metric.md", "source_type": "documentation", "evidence_tier": "explicit"}

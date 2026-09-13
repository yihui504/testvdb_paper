=== 候选缺陷 milvus_007 ===
[vendor=milvus version=2.6.10 defect_type=behavior endpoint=entities+search]
--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] empty query vector -> MilvusException code=65535 (server message: ...vector type must be the same, field vector - type VECTOR_FLOAT, search info type VECTOR_SPARSE_U32_F32...)

执行日志全文（output_milvus_007.log）：
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
payload: {"collectionName": "repro_<tracked>", "dbName": "default", "indexParams": [{"fieldName": "vector", "indexName": "idx_vec", "metricType": "L2", "indexType": "IVF_FLAT", "params": {"nlist": 8}}]}
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
payload: {"collectionName": "repro_<tracked>", "dbName": "default", "data": [[]], "limit": 3, "outputFields": ["id"]}
=== RESP 5 ===
status: 200
body: {"code":1801,"message":"can only accept json format request, error: dimension: 8, but length of []float: 0: invalid parameter[expected=FloatVector][actual=[[]]]"}
--- 契约依据（expected，M3 重建版） ---
[经端点过滤与依据核查后，无 endpoint=entities+search 的可核查约束行]

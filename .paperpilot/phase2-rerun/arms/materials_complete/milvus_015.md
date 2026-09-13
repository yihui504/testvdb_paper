=== 候选缺陷 milvus_015 ===
[vendor=milvus version=2.6.16 defect_type=behavior endpoint=indexes+create]
--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] REST create_index on bare collection -> http=200, code=100
- [c2] SDK create_index after quick-create -> MilvusException code=65535 (message: CreateIndex failed: creating multiple indexes on same field is not supported)

执行日志全文（output_milvus_015.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_rest_idx", "dbName": "default"}
=== RESP 1 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_sdk_idx", "dbName": "default"}
=== RESP 2 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_rest_idx"}
=== RESP 3 ===
status: 200
body: {"code":1100,"message":"dimension is required for quickly create collection(default metric type: COSINE): invalid parameter[expected=collectionName \u0026 dimension][actual=collectionName]"}

=== REQ 4 ===
POST http://localhost:19530/v2/vectordb/indexes/create
payload: {"collectionName": "test_rest_idx", "indexParams": [{"fieldName": "vector", "metricType": "L2", "indexType": "IVF_FLAT"}]}
=== RESP 4 ===
status: 200
body: {"code":100,"message":"collection not found[database=default][collection=test_rest_idx]"}

=== REQ 5 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_rest_idx", "dbName": "default"}
=== RESP 5 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 6 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_sdk_idx", "dbName": "default"}
=== RESP 6 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 7 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_rest_idx"}
=== RESP 7 ===
status: 200
body: {"code":1100,"message":"dimension is required for quickly create collection(default metric type: COSINE): invalid parameter[expected=collectionName \u0026 dimension][actual=collectionName]"}

=== REQ 8 ===
POST http://localhost:19530/v2/vectordb/indexes/create
payload: {"collectionName": "test_rest_idx", "indexParams": [{"fieldName": "vector", "metricType": "L2", "indexType": "IVF_FLAT"}]}
=== RESP 8 ===
status: 200
body: {"code":100,"message":"collection not found[database=default][collection=test_rest_idx]"}
--- 契约依据（expected，M3 重建版） ---
[经端点过滤与依据核查后，无 endpoint=indexes+create 的可核查约束行]

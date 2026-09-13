=== 候选缺陷 milvus_016 ===
[vendor=milvus version=2.6.16 defect_type=param_validation endpoint=entities+search]
--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] HNSW search with ef=-1 -> http=200, code=0
- [c2] HNSW search with ef=0 -> http=200, code=0
- [c3] IVF_FLAT search with nprobe=0 -> http=200, code=0

执行日志全文（output_milvus_016.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_hnsw_ef", "dbName": "default"}
=== RESP 1 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_ivf_nprobe", "dbName": "default"}
=== RESP 2 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_hnsw_ef", "dimension": 4, "metricType": "L2"}
=== RESP 3 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 4 ===
POST http://localhost:19530/v2/vectordb/indexes/create
payload: {"collectionName": "test_hnsw_ef", "indexParams": [{"fieldName": "vector", "metricType": "L2", "indexType": "HNSW", "params": {"M": 16, "efConstruction": 128}}]}
=== RESP 4 ===
status: 200
body: {"code":65535,"message":"CreateIndex failed: at most one distinct index is allowed per field"}

=== REQ 5 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_hnsw_ef", "data": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4]}]}
=== RESP 5 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":1,"insertIds":[1]}}

=== REQ 6 ===
POST http://localhost:19530/v2/vectordb/collections/load
payload: {"collectionName": "test_hnsw_ef", "dbName": "default"}
=== RESP 6 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 7 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_ivf_nprobe", "dimension": 4, "metricType": "L2"}
=== RESP 7 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 8 ===
POST http://localhost:19530/v2/vectordb/indexes/create
payload: {"collectionName": "test_ivf_nprobe", "indexParams": [{"fieldName": "vector", "metricType": "L2", "indexType": "IVF_FLAT", "params": {"nlist": 128}}]}
=== RESP 8 ===
status: 200
body: {"code":65535,"message":"CreateIndex failed: at most one distinct index is allowed per field"}

=== REQ 9 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_ivf_nprobe", "data": [{"id": 0, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 1, "vector": [0.1, 0.2, 0.3, 0.4]}]}
=== RESP 9 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":2,"insertIds":[0,1]}}

=== REQ 10 ===
POST http://localhost:19530/v2/vectordb/collections/load
payload: {"collectionName": "test_ivf_nprobe", "dbName": "default"}
=== RESP 10 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 11 ===
POST http://localhost:19530/v2/vectordb/entities/search
payload: {"collectionName": "test_hnsw_ef", "data": [[0.1, 0.2, 0.3, 0.4]], "limit": 5, "searchParams": {"ef": -1}}
=== RESP 11 ===
status: 200
body: {"code":0,"cost":0,"data":[{"distance":0,"id":1}],"topks":[1]}


=== REQ 12 ===
POST http://localhost:19530/v2/vectordb/entities/search
payload: {"collectionName": "test_hnsw_ef", "data": [[0.1, 0.2, 0.3, 0.4]], "limit": 5, "searchParams": {"ef": 0}}
=== RESP 12 ===
status: 200
body: {"code":0,"cost":0,"data":[{"distance":0,"id":1}],"topks":[1]}


=== REQ 13 ===
POST http://localhost:19530/v2/vectordb/entities/search
payload: {"collectionName": "test_ivf_nprobe", "data": [[0.1, 0.2, 0.3, 0.4]], "limit": 5, "searchParams": {"nprobe": 0}}
=== RESP 13 ===
status: 200
body: {"code":0,"cost":0,"data":[{"distance":0,"id":0},{"distance":0,"id":1}],"topks":[2]}


=== REQ 14 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_hnsw_ef", "dbName": "default"}
=== RESP 14 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 15 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_ivf_nprobe", "dbName": "default"}
=== RESP 15 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 16 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_hnsw_ef", "dimension": 4, "metricType": "L2"}
=== RESP 16 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 17 ===
POST http://localhost:19530/v2/vectordb/indexes/create
payload: {"collectionName": "test_hnsw_ef", "indexParams": [{"fieldName": "vector", "metricType": "L2", "indexType": "HNSW", "params": {"M": 16, "efConstruction": 128}}]}
=== RESP 17 ===
status: 200
body: {"code":65535,"message":"CreateIndex failed: at most one distinct index is allowed per field"}

=== REQ 18 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_hnsw_ef", "data": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4]}]}
=== RESP 18 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":1,"insertIds":[1]}}

=== REQ 19 ===
POST http://localhost:19530/v2/vectordb/collections/load
payload: {"collectionName": "test_hnsw_ef", "dbName": "default"}
=== RESP 19 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 20 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_ivf_nprobe", "dimension": 4, "metricType": "L2"}
=== RESP 20 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 21 ===
POST http://localhost:19530/v2/vectordb/indexes/create
payload: {"collectionName": "test_ivf_nprobe", "indexParams": [{"fieldName": "vector", "metricType": "L2", "indexType": "IVF_FLAT", "params": {"nlist": 128}}]}
=== RESP 21 ===
status: 200
body: {"code":65535,"message":"CreateIndex failed: at most one distinct index is allowed per field"}

=== REQ 22 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_ivf_nprobe", "data": [{"id": 0, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 1, "vector": [0.1, 0.2, 0.3, 0.4]}]}
=== RESP 22 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":2,"insertIds":[0,1]}}

=== REQ 23 ===
POST http://localhost:19530/v2/vectordb/collections/load
payload: {"collectionName": "test_ivf_nprobe", "dbName": "default"}
=== RESP 23 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 24 ===
POST http://localhost:19530/v2/vectordb/entities/search
payload: {"collectionName": "test_hnsw_ef", "data": [[0.1, 0.2, 0.3, 0.4]], "limit": 5, "searchParams": {"ef": -1}}
=== RESP 24 ===
status: 200
body: {"code":0,"cost":0,"data":[{"distance":0,"id":1}],"topks":[1]}


=== REQ 25 ===
POST http://localhost:19530/v2/vectordb/entities/search
payload: {"collectionName": "test_hnsw_ef", "data": [[0.1, 0.2, 0.3, 0.4]], "limit": 5, "searchParams": {"ef": 0}}
=== RESP 25 ===
status: 200
body: {"code":0,"cost":0,"data":[{"distance":0,"id":1}],"topks":[1]}


=== REQ 26 ===
POST http://localhost:19530/v2/vectordb/entities/search
payload: {"collectionName": "test_ivf_nprobe", "data": [[0.1, 0.2, 0.3, 0.4]], "limit": 5, "searchParams": {"nprobe": 0}}
=== RESP 26 ===
status: 200
body: {"code":0,"cost":0,"data":[{"distance":0,"id":0},{"distance":0,"id":1}],"topks":[2]}
--- 契约依据（expected，M3 重建版） ---
{"endpoint": "entities+search", "kind": "type_constraints", "description": "data must be array of float arrays, annsField must be a vector field, limit must be positive integer", "assertion": "data is array[array[float]] AND annsField is a vector field AND limit > 0", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Vector%20(v2)/Search.md", "confidence": 1.0, "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}
{"endpoint": "entities+search", "kind": "range_constraints", "description": "limit + offset must be < 16384", "assertion": "limit + offset < 16384", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Vector%20(v2)/Search.md", "confidence": 1.0, "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}

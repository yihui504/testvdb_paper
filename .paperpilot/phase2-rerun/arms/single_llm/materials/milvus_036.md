=== 候选缺陷 milvus_036 ===
[vendor=milvus version=3.0.0 defect_type=param_validation endpoint=entities+search]

--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] REST search with groupSize=0 -> http=200, code=0
- [c1_grpc] gRPC search with group_size=0 -> MilvusException code=1100, message: metric type not match: expected=COSINE, actual=L2
- [c2] REST search with groupSize=-1 -> http=200, code=0

执行日志全文（output_milvus_036.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_gs", "dbName": "default"}
=== RESP 1 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_gs", "dimension": 4}
=== RESP 2 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_gs", "data": [{"id": 0, "vector": [0.1, 0.2, 0.3, 0.4], "cat": 0}, {"id": 1, "vector": [0.1, 0.2, 0.3, 0.4], "cat": 1}, {"id": 2, "vector": [0.1, 0.2, 0.3, 0.4], "cat": 2}, {"id": 3, "vector": [0.1, 0.2, 0.3, 0.4], "cat": 0}, {"id": 4, "vector": [0.1, 0.2, 0.3, 0.4], "cat": 1}, {"id": 5, "vector": [0.1, 0.2, 0.3, 0.4], "cat": 2}, {"id": 6, "vector": [0.1, 0.2, 0.3, 0.4], "cat": 0}, {"id": 7, "vector": [0.1, 0.2, 0.3, 0.4], "cat": 1}, {"id": 8, "vector": [0.1, 0.2, 0.3, 0.4], "cat": 2}, {"id": 9, "vector": [0.1, 0.2, 0.3, 0.4], "cat": 0}]}
=== RESP 3 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":10,"insertIds":[0,1,2,3,4,5,6,7,8,9]}}

=== REQ 4 ===
POST http://localhost:19530/v2/vectordb/collections/load
payload: {"collectionName": "test_gs", "dbName": "default"}
=== RESP 4 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 5 ===
POST http://localhost:19530/v2/vectordb/entities/search
payload: {"collectionName": "test_gs", "data": [[0.5, 0.5, 0.5, 0.5]], "limit": 5, "groupParams": {"groupByField": "cat", "groupSize": 0}}
=== RESP 5 ===
status: 200
body: {"code":0,"cost":0,"data":[{"distance":0.9128709,"id":0},{"distance":0.9128709,"id":1},{"distance":0.9128709,"id":2},{"distance":0.9128709,"id":3},{"distance":0.9128709,"id":4}],"topks":[5]}


=== REQ 6 ===
POST http://localhost:19530/v2/vectordb/entities/search
payload: {"collectionName": "test_gs", "data": [[0.5, 0.5, 0.5, 0.5]], "limit": 5, "groupParams": {"groupByField": "cat", "groupSize": -1}}
=== RESP 6 ===
status: 200
body: {"code":0,"cost":0,"data":[{"distance":0.9128709,"id":0},{"distance":0.9128709,"id":1},{"distance":0.9128709,"id":2},{"distance":0.9128709,"id":3},{"distance":0.9128709,"id":4}],"topks":[5]}


=== REQ 7 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_gs", "dbName": "default"}
=== RESP 7 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 8 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_gs", "dimension": 4}
=== RESP 8 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 9 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_gs", "data": [{"id": 0, "vector": [0.1, 0.2, 0.3, 0.4], "cat": 0}, {"id": 1, "vector": [0.1, 0.2, 0.3, 0.4], "cat": 1}, {"id": 2, "vector": [0.1, 0.2, 0.3, 0.4], "cat": 2}, {"id": 3, "vector": [0.1, 0.2, 0.3, 0.4], "cat": 0}, {"id": 4, "vector": [0.1, 0.2, 0.3, 0.4], "cat": 1}, {"id": 5, "vector": [0.1, 0.2, 0.3, 0.4], "cat": 2}, {"id": 6, "vector": [0.1, 0.2, 0.3, 0.4], "cat": 0}, {"id": 7, "vector": [0.1, 0.2, 0.3, 0.4], "cat": 1}, {"id": 8, "vector": [0.1, 0.2, 0.3, 0.4], "cat": 2}, {"id": 9, "vector": [0.1, 0.2, 0.3, 0.4], "cat": 0}]}
=== RESP 9 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":10,"insertIds":[0,1,2,3,4,5,6,7,8,9]}}

=== REQ 10 ===
POST http://localhost:19530/v2/vectordb/collections/load
payload: {"collectionName": "test_gs", "dbName": "default"}
=== RESP 10 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 11 ===
POST http://localhost:19530/v2/vectordb/entities/search
payload: {"collectionName": "test_gs", "data": [[0.5, 0.5, 0.5, 0.5]], "limit": 5, "groupParams": {"groupByField": "cat", "groupSize": 0}}
=== RESP 11 ===
status: 200
body: {"code":0,"cost":0,"data":[{"distance":0.9128709,"id":0},{"distance":0.9128709,"id":1},{"distance":0.9128709,"id":2},{"distance":0.9128709,"id":3},{"distance":0.9128709,"id":4}],"topks":[5]}


=== REQ 12 ===
POST http://localhost:19530/v2/vectordb/entities/search
payload: {"collectionName": "test_gs", "data": [[0.5, 0.5, 0.5, 0.5]], "limit": 5, "groupParams": {"groupByField": "cat", "groupSize": -1}}
=== RESP 12 ===
status: 200
body: {"code":0,"cost":0,"data":[{"distance":0.9128709,"id":0},{"distance":0.9128709,"id":1},{"distance":0.9128709,"id":2},{"distance":0.9128709,"id":3},{"distance":0.9128709,"id":4}],"topks":[5]}




--- 契约依据（expected，来自该版本 API 契约） ---
约束条目（9 条，来自 milvus 3.0.0 契约，endpoint=entities+search）：
{"constraint_id": "milvus_range_hnsw_ef_001", "endpoint": "entities+search", "type": "range_constraint", "description": "ef parameter for HNSW search", "assertion": "ef in [1, 2147483647]", "source_url": "https://milvus.io/docs/index.md", "confidence": 1.0}
{"constraint_id": "milvus_range_ivf_nprobe_001", "endpoint": "entities+search", "type": "range_constraint", "description": "IVF nprobe must be in range [1, nlist]", "assertion": "nprobe >= 1 AND nprobe <= nlist", "source_url": "https://milvus.io/docs/index.md", "confidence": 1.0}
{"constraint_id": "milvus_range_ivf_flat_nprobe_001", "endpoint": "entities+search", "type": "range_constraint", "description": "nprobe parameter for IVF_FLAT search", "assertion": "nprobe in [1, nlist]", "source_url": "https://milvus.io/docs/index.md", "confidence": 1.0}
{"constraint_id": "milvus_range_ivf_pq_nprobe_001", "endpoint": "entities+search", "type": "range_constraint", "description": "nprobe parameter for IVF_PQ search", "assertion": "nprobe in [1, nlist]", "source_url": "https://milvus.io/docs/index.md", "confidence": 1.0}
{"constraint_id": "milvus_range_ivf_sq8_nprobe_001", "endpoint": "entities+search", "type": "range_constraint", "description": "nprobe parameter for IVF_SQ8 search", "assertion": "nprobe in [1, nlist]", "source_url": "https://milvus.io/docs/index.md", "confidence": 1.0}
{"constraint_id": "milvus_range_scann_nprobe_001", "endpoint": "entities+search", "type": "range_constraint", "description": "nprobe parameter for SCANN search", "assertion": "nprobe in [1, nlist]", "source_url": "https://milvus.io/docs/index.md", "confidence": 1.0}
{"constraint_id": "milvus_state_search_load_001", "endpoint": "entities+search", "type": "state_constraint", "description": "Search requires collection to be loaded", "assertion": "collection MUST be loaded before search", "source_url": "https://milvus.io/docs/single-vector-search.md", "confidence": 1.0}
{"constraint_id": "milvus_state_search_requires_load_001", "endpoint": "entities+search", "type": "state_constraint", "description": "Collection must be loaded before searching", "assertion": "collection.load_state == 'loaded' before search", "source_url": "https://milvus.io/docs/single-vector-search.md", "confidence": 1.0}
{"assertion_id": "milvus_assert_search_empty_001", "endpoint": "entities+search", "description": "Searching empty collection returns empty results", "source_url": "https://milvus.io/docs/single-vector-search.md", "confidence": 1.0}

API 模板：endpoint=entities+insert doc_quote='Insert entities' source=None

VERDICT: UNKNOWN (replay capture — no attack-agent assertion output; raw HTTP only)

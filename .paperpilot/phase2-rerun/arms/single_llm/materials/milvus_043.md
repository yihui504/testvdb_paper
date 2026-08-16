=== 候选缺陷 milvus_043 ===
[vendor=milvus version=3.0.0 defect_type=semantics endpoint=entities+search]

--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] REST search with strictGroupSize=true, groupSize=5 -> http=200, code=0, returned 15 results
- [c1_grpc] gRPC search with strict_group_size -> returned 15 results

执行日志全文（output_milvus_043.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/entities/search
payload: {"collectionName": "gs_demo", "data": [[0.5, 0.5, 0.5, 0.5]], "limit": 15, "groupParams": {"groupByField": "cat", "groupSize": 2, "strictGroupSize": true}, "outputFields": ["cat"]}
=== RESP 1 ===
status: 200
body: {"code":0,"cost":0,"data":[{"cat":4,"distance":0.9667964,"id":14},{"cat":3,"distance":0.964861,"id":13},{"cat":2,"distance":0.96265984,"id":12},{"cat":1,"distance":0.96018463,"id":11},{"cat":0,"distance":0.95742714,"id":10},{"cat":4,"distance":0.9543795,"id":9},{"cat":3,"distance":0.9510345,"id":8},{"cat":2,"distance":0.9473851,"id":7},{"cat":1,"distance":0.943425,"id":6},{"cat":0,"distance":0.9391486,"id":5},{"cat":4,"distance":0.93455064,"id":4},{"cat":3,"distance":0.929627,"id":3},{"cat":2,"distance":0.92437416,"id":2},{"cat":1,"distance":0.91878945,"id":1},{"cat":0,"distance":0.9128709,"id":0}],"topks":[15]}


=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/entities/search
payload: {"collectionName": "gs_demo", "data": [[0.5, 0.5, 0.5, 0.5]], "limit": 15, "groupParams": {"groupByField": "cat", "groupSize": 2, "strictGroupSize": true}, "outputFields": ["cat"]}
=== RESP 2 ===
status: 200
body: {"code":0,"cost":0,"data":[{"cat":4,"distance":0.9667964,"id":14},{"cat":3,"distance":0.964861,"id":13},{"cat":2,"distance":0.96265984,"id":12},{"cat":1,"distance":0.96018463,"id":11},{"cat":0,"distance":0.95742714,"id":10},{"cat":4,"distance":0.9543795,"id":9},{"cat":3,"distance":0.9510345,"id":8},{"cat":2,"distance":0.9473851,"id":7},{"cat":1,"distance":0.943425,"id":6},{"cat":0,"distance":0.9391486,"id":5},{"cat":4,"distance":0.93455064,"id":4},{"cat":3,"distance":0.929627,"id":3},{"cat":2,"distance":0.92437416,"id":2},{"cat":1,"distance":0.91878945,"id":1},{"cat":0,"distance":0.9128709,"id":0}],"topks":[15]}




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

相关契约段（关键词定位 1 条）：
{"endpoint": "collections+create", "kind": "state_constraints", "description": "Collection must have exactly one primary key", "assertion": "isPrimary MUST be true for exactly one field", "source_url": "https://milvus.io/docs/schema.md", "confidence": 1.0}

API 模板：endpoint=entities+insert doc_quote='Insert entities' source=None

VERDICT: UNKNOWN (replay capture — no attack-agent assertion output; raw HTTP only)

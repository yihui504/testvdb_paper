=== 候选缺陷 milvus_038 ===
[vendor=milvus version=3.0.0 defect_type=semantics endpoint=entities+search]
--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] REST search with groupByField=vector -> http=200, code=0
- [c1_grpc] gRPC search with group_by=vector -> MilvusException code=1100, message: metric type not match: expected=COSINE, actual=L2

执行日志全文（output_milvus_038.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_gv", "dbName": "default"}
=== RESP 1 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_gv", "dimension": 4}
=== RESP 2 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_gv", "data": [{"id": 0, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 1, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 2, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 3, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 4, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 5, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 6, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 7, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 8, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 9, "vector": [0.1, 0.2, 0.3, 0.4]}]}
=== RESP 3 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":10,"insertIds":[0,1,2,3,4,5,6,7,8,9]}}

=== REQ 4 ===
POST http://localhost:19530/v2/vectordb/collections/load
payload: {"collectionName": "test_gv", "dbName": "default"}
=== RESP 4 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 5 ===
POST http://localhost:19530/v2/vectordb/entities/search
payload: {"collectionName": "test_gv", "data": [[0.5, 0.5, 0.5, 0.5]], "limit": 5, "groupParams": {"groupByField": "vector", "groupSize": 1}}
=== RESP 5 ===
status: 200
body: {"code":0,"cost":0,"data":[{"distance":0.9128709,"id":0},{"distance":0.9128709,"id":1},{"distance":0.9128709,"id":2},{"distance":0.9128709,"id":3},{"distance":0.9128709,"id":4}],"topks":[5]}


=== REQ 6 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_gv", "dbName": "default"}
=== RESP 6 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 7 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_gv", "dimension": 4}
=== RESP 7 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 8 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_gv", "data": [{"id": 0, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 1, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 2, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 3, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 4, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 5, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 6, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 7, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 8, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 9, "vector": [0.1, 0.2, 0.3, 0.4]}]}
=== RESP 8 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":10,"insertIds":[0,1,2,3,4,5,6,7,8,9]}}

=== REQ 9 ===
POST http://localhost:19530/v2/vectordb/collections/load
payload: {"collectionName": "test_gv", "dbName": "default"}
=== RESP 9 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 10 ===
POST http://localhost:19530/v2/vectordb/entities/search
payload: {"collectionName": "test_gv", "data": [[0.5, 0.5, 0.5, 0.5]], "limit": 5, "groupParams": {"groupByField": "vector", "groupSize": 1}}
=== RESP 10 ===
status: 200
body: {"code":0,"cost":0,"data":[{"distance":0.9128709,"id":0},{"distance":0.9128709,"id":1},{"distance":0.9128709,"id":2},{"distance":0.9128709,"id":3},{"distance":0.9128709,"id":4}],"topks":[5]}

--- 契约依据（expected，M1 过滤后初稿） ---
约束条目（9 条，来自 milvus 3.0.0 契约，endpoint=entities+search）：
{"constraint_id": "milvus_range_hnsw_ef_001", "endpoint": "entities+search", "type": "range_constraint", "description": "ef parameter for HNSW search", "assertion": "ef in [1, 2147483647]", "source_url": "https://milvus.io/docs/index.md", "confidence": 1.0, "_audit": {"g1": "page-unversioned", "g2": "UNRESOLVABLE", "issue_no": false, "page": "none", "kw_hits": [], "priority": "bulk"}}
{"constraint_id": "milvus_range_ivf_nprobe_001", "endpoint": "entities+search", "type": "range_constraint", "description": "IVF nprobe must be in range [1, nlist]", "assertion": "nprobe >= 1 AND nprobe <= nlist", "source_url": "https://milvus.io/docs/index.md", "confidence": 1.0, "_audit": {"g1": "page-unversioned", "g2": "UNRESOLVABLE", "issue_no": false, "page": "none", "kw_hits": [], "priority": "bulk"}}
{"constraint_id": "milvus_range_ivf_flat_nprobe_001", "endpoint": "entities+search", "type": "range_constraint", "description": "nprobe parameter for IVF_FLAT search", "assertion": "nprobe in [1, nlist]", "source_url": "https://milvus.io/docs/index.md", "confidence": 1.0, "_audit": {"g1": "page-unversioned", "g2": "UNRESOLVABLE", "issue_no": false, "page": "none", "kw_hits": [], "priority": "bulk"}}
{"constraint_id": "milvus_range_ivf_pq_nprobe_001", "endpoint": "entities+search", "type": "range_constraint", "description": "nprobe parameter for IVF_PQ search", "assertion": "nprobe in [1, nlist]", "source_url": "https://milvus.io/docs/index.md", "confidence": 1.0, "_audit": {"g1": "page-unversioned", "g2": "UNRESOLVABLE", "issue_no": false, "page": "none", "kw_hits": [], "priority": "bulk"}}
{"constraint_id": "milvus_range_ivf_sq8_nprobe_001", "endpoint": "entities+search", "type": "range_constraint", "description": "nprobe parameter for IVF_SQ8 search", "assertion": "nprobe in [1, nlist]", "source_url": "https://milvus.io/docs/index.md", "confidence": 1.0, "_audit": {"g1": "page-unversioned", "g2": "UNRESOLVABLE", "issue_no": false, "page": "none", "kw_hits": [], "priority": "bulk"}}
{"constraint_id": "milvus_range_scann_nprobe_001", "endpoint": "entities+search", "type": "range_constraint", "description": "nprobe parameter for SCANN search", "assertion": "nprobe in [1, nlist]", "source_url": "https://milvus.io/docs/index.md", "confidence": 1.0, "_audit": {"g1": "page-unversioned", "g2": "UNRESOLVABLE", "issue_no": false, "page": "none", "kw_hits": [], "priority": "bulk"}}
{"constraint_id": "milvus_state_search_load_001", "endpoint": "entities+search", "type": "state_constraint", "description": "Search requires collection to be loaded", "assertion": "collection MUST be loaded before search", "source_url": "https://milvus.io/docs/single-vector-search.md", "confidence": 1.0, "_audit": {"g1": "page-unversioned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["MUST", "Search", "before", "search"], "priority": "bulk"}}
{"constraint_id": "milvus_state_search_requires_load_001", "endpoint": "entities+search", "type": "state_constraint", "description": "Collection must be loaded before searching", "assertion": "collection.load_state == 'loaded' before search", "source_url": "https://milvus.io/docs/single-vector-search.md", "confidence": 1.0, "_audit": {"g1": "page-unversioned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["Collection", "before", "search"], "priority": "bulk"}}
{"assertion_id": "milvus_assert_search_empty_001", "endpoint": "entities+search", "description": "Searching empty collection returns empty results", "source_url": "https://milvus.io/docs/single-vector-search.md", "confidence": 1.0, "_audit": {"g1": "page-unversioned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["results"], "priority": "bulk"}}
API 模板：endpoint=roles+grant_privilege_v2 doc_quote='Grant privilege V2' source=None
--- 契约依据·主断言（M1，_provenance 已剥） ---
{"constraint_id": "milvus_state_group_by_field_001", "endpoint": "entities+search", "description": "group_by_field must be a scalar field (grouping by vector field not supported)", "assertion": "group_by_field refers to a scalar (non-vector) field", "type": "state_constraint", "evidence_tier": "explicit", "source_url": "https://raw.githubusercontent.com/milvus-io/milvus-docs/99af7351/site/en/userGuide/search-query-get/grouping-search.md", "_audit": {"g1": "page-unversioned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["group_by_field", "grouping", "not", "scalar"], "priority": "main"}}
VERDICT: UNKNOWN (replay capture — no attack-agent assertion output; raw HTTP only)
--- 补充契约行（M1 端点过滤后） ---
{"constraint_id": "milvus_type_entities_search_001", "endpoint": "entities+search", "description": "data must be array of float arrays, annsField must be a vector field, limit must be positive integer", "assertion": "data is array[array[float]] AND annsField is a vector field AND limit > 0", "type": "type_constraint", "confidence": 1.0, "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Vector%20(v2)/Search.md", "source_status": "reachable", "_audit": {"g1": "MISMATCH", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["AND", "annsField", "array", "float", "limit"], "priority": "bulk"}}
{"constraint_id": "milvus_range_entities_search_001", "endpoint": "entities+search", "description": "vector dimensions in data must match collection vector dimension", "assertion": "vector dimension == collection dimension", "type": "range_constraint", "confidence": 1.0, "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Vector%20(v2)/Search.md", "source_status": "reachable", "_audit": {"g1": "MISMATCH", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["match"], "priority": "bulk"}}

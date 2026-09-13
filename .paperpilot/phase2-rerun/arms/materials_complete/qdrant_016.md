=== 候选缺陷 qdrant_016 ===
[vendor=qdrant version=1.18.2 defect_type=behavior endpoint=collections+{collection_name}+points+query]
--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] lookup referencing non-existent collection -> status=200, 3 results
- [c2] control: lookup referencing valid collection -> status=200

执行日志全文（output_qdrant_016.log）：
=== REQ 1 ===
DELETE http://localhost:6333/collections/test_lookup_source
=== RESP 1 ===
status: 200
body: {"result":false,"status":"ok","time":0.00276579}

=== REQ 2 ===
PUT http://localhost:6333/collections/test_lookup_source
payload: {"vectors": {"size": 4, "distance": "Cosine"}}
=== RESP 2 ===
status: 200
body: {"result":true,"status":"ok","time":0.321462371}

=== REQ 3 ===
PUT http://localhost:6333/collections/test_lookup_source/points?wait=true
payload: {"points": [{"id": 0, "vector": [0.1, 0.2, 0.3, 0.4], "payload": {"tag": "t0"}}, {"id": 1, "vector": [0.1, 0.2, 0.3, 0.4], "payload": {"tag": "t1"}}, {"id": 2, "vector": [0.1, 0.2, 0.3, 0.4], "payload": {"tag": "t2"}}, {"id": 3, "vector": [0.1, 0.2, 0.3, 0.4], "payload": {"tag": "t3"}}, {"id": 4, "vector": [0.1, 0.2, 0.3, 0.4], "payload": {"tag": "t4"}}]}
=== RESP 3 ===
status: 200
body: {"result":{"operation_id":1,"status":"completed"},"status":"ok","time":0.010886418}

=== REQ 4 ===
DELETE http://localhost:6333/collections/test_lookup_target
=== RESP 4 ===
status: 200
body: {"result":false,"status":"ok","time":0.000072588}

=== REQ 5 ===
PUT http://localhost:6333/collections/test_lookup_target
payload: {"vectors": {"size": 4, "distance": "Cosine"}}
=== RESP 5 ===
status: 200
body: {"result":true,"status":"ok","time":0.296707869}

=== REQ 6 ===
PUT http://localhost:6333/collections/test_lookup_target/points?wait=true
payload: {"points": [{"id": 0, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 1, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 2, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 3, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 4, "vector": [0.1, 0.2, 0.3, 0.4]}]}
=== RESP 6 ===
status: 200
body: {"result":{"operation_id":1,"status":"completed"},"status":"ok","time":0.005122177}

=== REQ 7 ===
POST http://localhost:6333/collections/test_lookup_source/points/query
payload: {"query": [0.3, 0.3, 0.3, 0.3], "limit": 3, "lookup_from": {"collection": "nonexistent_collection_xyz", "vector": "default"}}
=== RESP 7 ===
status: 200
body: {"result":{"points":[{"id":4,"version":1,"score":0.91287094},{"id":0,"version":1,"score":0.91287094},{"id":3,"version":1,"score":0.91287094}]},"status":"ok","time":0.004096501}

=== REQ 8 ===
POST http://localhost:6333/collections/test_lookup_source/points/query
payload: {"query": [0.3, 0.3, 0.3, 0.3], "limit": 3, "lookup_from": {"collection": "test_lookup_target", "vector": "default"}}
=== RESP 8 ===
status: 200
body: {"result":{"points":[{"id":4,"version":1,"score":0.91287094},{"id":0,"version":1,"score":0.91287094},{"id":3,"version":1,"score":0.91287094}]},"status":"ok","time":0.000313989}
--- 契约依据（expected，M3 重建版） ---
[v1.18.2 openapi 及其派生文档中无 lookup_from.collection 的存在性约束条目]
openapi 中 lookup_from 的全部语义（原文）："The location used to lookup vectors.
If not specified - use current collection. Note: the other collection should
have the same vector size as the current collection"
来源：https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json （structured-spec，tag-pinned）

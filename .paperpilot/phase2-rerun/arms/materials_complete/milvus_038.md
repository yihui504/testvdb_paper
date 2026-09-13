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
--- 契约依据（expected，M3 重建版） ---
{"constraint_id": "milvus_state_group_by_field_001", "endpoint": "entities+search", "description": "group_by_field enables Grouping Search", "assertion": "documentation presents group_by_field as grouping search results over a scalar field's values (examples: docId, category); no normative statement about vector-field values being rejected", "source_url": "https://raw.githubusercontent.com/milvus-io/milvus-docs/99af7351/site/en/userGuide/search-query-get/grouping-search.md", "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}

# Blind second-pass adjudication (pack + pinned source)

对以下 25 个候选缺陷逐案裁决。每案的源码 clone 路径已给出，可在其中 grep/Read 查证。
逐案输出一个 JSON 行。

你是一名独立的缺陷裁决员，执行部署通道人工裁决者的角色。对下列每个候选缺陷
给出裁决：该案路由到人工审查后应判往何处。

## 裁决规则（与部署的 pack-materials 规则一致）

1. **材料范围**：每案的材料包（观察记录 + 契约行）+ 该案对应版本的源码 clone。
   你可以 grep/Read 源码中任意文件来查证行为与意图。**不得**查询 issue
   tracker、不得联网、不得读取任何认知/情报（developer_cognition /
   intelligence）材料。
2. **三选一裁决**：
   - `CONFIRM_AS_DEFECT`：证据足以确认这是文档-实现不一致缺陷
     （观察行为与包内文档约束矛盾，或构成包内材料支持的客观违反，
     且源码中无明文 by-design 意图证据）。
   - `RETURN`：证据不足（缺执行记录、缺可核查契约锚点、前提失真、
     观察未隔离所声称行为、材料自相矛盾）。
   - `REJECT`：材料表明这不是缺陷（文档语句为描述性而非规范性、
     行为在文档允许范围内、或源码含明文 by-design 意图证据）。
3. 源码的作用有二：为 by-design 抗辩找明文意图证据（注释/文档串）；定位
   "契约预测缺失校验"处的实现，以判断行为是否属实、是否被隔离。
4. 唯一裁决只看证据，不猜测维护者会怎么判。

输出格式（每案一个 JSON 行）：
{"case": "<案号>", "ruling": "CONFIRM_AS_DEFECT|RETURN|REJECT",
 "rationale": "<一两句中文理由，引用包内或源码的具体证据>"}




--------

## 案 1: qdrant_026

**源码 clone**：`c:\Users\11428\Desktop\testvdb_paper\.sourcedeps\qdrant\v1.19.0`

# 候选缺陷 qdrant_026

[vendor=qdrant version=1.19.0 endpoint=groups]
--- 观察到的行为（observed） ---

重放环境:qdrant v1.19.0 container (port 6338);证据来源:container replay,HTTP interactions captured verbatim。

=== DELETE /collections/gdemo ===
-> 200 {"result":true,"status":"ok","time":0.014015108}
=== PUT /collections/gdemo ===
{"vectors": {"size": 4, "distance": "Euclid"}}
-> 200 {"result":true,"status":"ok","time":0.243744152}
=== PUT /collections/gdemo/points?wait=true ===
{"points": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4], "payload": {"grp": "a"}}, {"id": 2, "vector": [0.1, 0.2, 0.3, 0.4], "payload": {"grp": "b"}}, {"id": 3, "vector": [0.1, 0.2, 0.3, 0.4], "payload": {"grp": "a"}}, {"id": 4, "vector": [0.1, 0.2, 0.3, 0.4], "payload": {"grp": "b"}}, {"id": 5, "vector": [0.1, 0.2, 0.3, 0.4], "payload": {"grp": "a"}}, {"id": 6, "vector": [0.1, 0.2, 0.3, 0.4], "payload": {"grp": "b"}}, {"id": 7, "vector": [0.1, 0.2, 0.3, 0.4], "payload": {"grp": "a"}}, {"id": 8, "vector": [0.1, 0.2, 0.3, 0.4], "payload": {"grp": "b"}}]}
-> 200 {"result":{"operation_id":1,"status":"completed"},"status":"ok","time":0.004632063}
=== POST /collections/gdemo/points/query/groups ===
{"group_by": "grp", "limit": 2, "group_size": 3}
-> 200 {"result":{"groups":[{"hits":[{"id":3,"version":0,"score":1.0},{"id":1,"version":0,"score":1.0},{"id":5,"version":0,"score":1.0}],"id":"a"},{"hits":[{"id":6,"version":0,"score":1.0},{"id":2,"version":0,"score":1.0},{"id":4,"version":0,"score":1.0}],"id":"b"}]},"status":"ok","time":0.001400367}
=== POST /collections/gdemo/points/query/groups ===
{"group_by": "grp", "limit": 2, "group_size": 3}
-> 200 {"result":{"groups":[{"hits":[{"id":5,"version":0,"score":1.0},{"id":1,"version":0,"score":1.0},{"id":3,"version":0,"score":1.0}],"id":"a"},{"hits":[{"id":2,"version":0,"score":1.0},{"id":6,"version":0,"score":1.0},{"id":4,"version":0,"score":1.0}],"id":"b"}]},"status":"ok","time":0.000778015}
=== POST /collections/gdemo/points/query/groups ===
{"group_by": "grp", "limit": 2, "group_size": 3}
-> 200 {"result":{"groups":[{"hits":[{"id":1,"version":0,"score":1.0},{"id":5,"version":0,"score":1.0},{"id":3,"version":0,"score":1.0}],"id":"a"},{"hits":[{"id":2,"version":0,"score":1.0},{"id":6,"version":0,"score":1.0},{"id":4,"version":0,"score":1.0}],"id":"b"}]},"status":"ok","time":0.000834957}
=== POST /collections/gdemo/points/query/groups ===
{"group_by": "grp", "limit": 2, "group_size": 3}
-> 200 {"result":{"groups":[{"hits":[{"id":1,"version":0,"score":1.0},{"id":5,"version":0,"score":1.0},{"id":3,"version":0,"score":1.0}],"id":"a"},{"hits":[{"id":2,"version":0,"score":1.0},{"id":4,"version":0,"score":1.0},{"id":6,"version":0,"score":1.0}],"id":"b"}]},"status":"ok","time":0.000723067}
=== POST /collections/gdemo/points/query/groups ===
{"group_by": "grp", "limit": 2, "group_size": 3}
-> 200 {"result":{"groups":[{"hits":[{"id":5,"version":0,"score":1.0},{"id":1,"version":0,"score":1.0},{"id":3,"version":0,"score":1.0}],"id":"a"},{"hits":[{"id":6,"version":0,"score":1.0},{"id":2,"version":0,"score":1.0},{"id":4,"version":0,"score":1.0}],"id":"b"}]},"status":"ok","time":0.000920347}
=== POST /collections/gdemo/points/query/groups ===
{"group_by": "grp", "limit": 2, "group_size": 3}
-> 200 {"result":{"groups":[{"hits":[{"id":4,"version":0,"score":1.0},{"id":6,"version":0,"score":1.0},{"id":2,"version":0,"score":1.0}],"id":"b"},{"hits":[{"id":3,"version":0,"score":1.0},{"id":1,"version":0,"score":1.0},{"id":5,"version":0,"score":1.0}],"id":"a"}]},"status":"ok","time":0.000743167}
=== POST /collections/gdemo/points/query/groups ===
{"group_by": "grp", "limit": 2, "group_size": 3}
-> 200 {"result":{"groups":[{"hits":[{"id":6,"version":0,"score":1.0},{"id":4,"version":0,"score":1.0},{"id":2,"version":0,"score":1.0}],"id":"b"},{"hits":[{"id":3,"version":0,"score":1.0},{"id":1,"version":0,"score":1.0},{"id":5,"version":0,"score":1.0}],"id":"a"}]},"status":"ok","time":0.000485072}
=== POST /collections/gdemo/points/query/groups ===
{"group_by": "grp", "limit": 2, "group_size": 3}
-> 200 {"result":{"groups":[{"hits":[{"id":1,"version":0,"score":1.0},{"id":3,"version":0,"score":1.0},{"id":5,"version":0,"score":1.0}],"id":"a"},{"hits":[{"id":6,"version":0,"score":1.0},{"id":2,"version":0,"score":1.0},{"id":4,"version":0,"score":1.0}],"id":"b"}]},"status":"ok","time":0.000327518}
=== POST /collections/gdemo/points/query/groups ===
{"group_by": "grp", "limit": 2, "group_size": 3}
-> 200 {"result":{"groups":[{"hits":[{"id":6,"version":0,"score":1.0},{"id":2,"version":0,"score":1.0},{"id":4,"version":0,"score":1.0}],"id":"b"},{"hits":[{"id":1,"version":0,"score":1.0},{"id":3,"version":0,"score":1.0},{"id":5,"version":0,"score":1.0}],"id":"a"}]},"status":"ok","time":0.000777721}
=== POST /collections/gdemo/points/query/groups ===
{"group_by": "grp", "limit": 2, "group_size": 3}
-> 200 {"result":{"groups":[{"hits":[{"id":5,"version":0,"score":1.0},{"id":3,"version":0,"score":1.0},{"id":1,"version":0,"score":1.0}],"id":"a"},{"hits":[{"id":6,"version":0,"score":1.0},{"id":2,"version":0,"score":1.0},{"id":4,"version":0,"score":1.0}],"id":"b"}]},"status":"ok","time":0.000849965}
[STDOUT]
10 identical requests -> 10 distinct member-set signatures
[[null, [1, 3, 5]], [null, [6, 2, 4]]]
[[null, [1, 5, 3]], [null, [2, 4, 6]]]
[[null, [1, 5, 3]], [null, [2, 6, 4]]]
[[null, [3, 1, 5]], [null, [6, 2, 4]]]
[[null, [4, 6, 2]], [null, [3, 1, 5]]]
[[null, [5, 1, 3]], [null, [2, 6, 4]]]
[[null, [5, 1, 3]], [null, [6, 2, 4]]]
[[null, [5, 3, 1]], [null, [6, 2, 4]]]
[[null, [6, 2, 4]], [null, [1, 3, 5]]]
[[null, [6, 4, 2]], [null, [3, 1, 5]]]
--- 契约依据（expected，M3 重建版） ---
{"constraint_id": "qdrant_range_search_groups_007", "endpoint": "collections+{collection_name}+points+search+groups", "description": "group_size >= 1; limit >= 1", "assertion": "group_size >= 1 AND limit >= 1", "type": "range_constraint", "confidence": 1.0, "evidence_tier": "inferred_from_behavior", "source_url": "https://github.com/qdrant/qdrant/blob/v1.19.0/docs/redoc/master/openapi.json", "source_status": "reachable", "doc_version": "1.18.x", "source_verified": true, "source_type": "structured-spec"}
{"constraint_id": "qdrant_range_search_groups_007", "endpoint": "collections+{collection_name}+points+search+groups", "description": "group_size >= 1; limit >= 1", "assertion": "group_size >= 1 AND limit >= 1", "type": "range_constraint", "confidence": 1.0, "evidence_tier": "inferred_from_behavior", "source_url": "https://github.com/qdrant/qdrant/blob/v1.19.0/docs/redoc/master/openapi.json", "source_status": "reachable", "doc_version": "1.18.x", "source_verified": true, "source_type": "structured-spec"}



--------

## 案 2: milvus_019

**源码 clone**：`c:\Users\11428\Desktop\testvdb_paper\.sourcedeps\milvus\v2.6.16`

=== 候选缺陷 milvus_019 ===
[vendor=milvus version=2.6.16 defect_type=behavior endpoint=collections+get_stats]
--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] get_stats after insert+load -> http=200, code=0, rowCount=0
- [c1_q] query after insert+load -> http=200, code=0, returned 5 rows (id 0-4)

执行日志全文（output_milvus_019.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_rowcount", "dbName": "default"}
=== RESP 1 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_rowcount", "dimension": 4}
=== RESP 2 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_rowcount", "data": [{"id": 0, "value": 0, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 1, "value": 1, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 2, "value": 2, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 3, "value": 3, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 4, "value": 4, "vector": [0.1, 0.2, 0.3, 0.4]}]}
=== RESP 3 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":5,"insertIds":[0,1,2,3,4]}}

=== REQ 4 ===
POST http://localhost:19530/v2/vectordb/collections/load
payload: {"collectionName": "test_rowcount", "dbName": "default"}
=== RESP 4 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 5 ===
POST http://localhost:19530/v2/vectordb/collections/get_stats
payload: {"collectionName": "test_rowcount"}
=== RESP 5 ===
status: 200
body: {"code":0,"data":{"rowCount":0}}

=== REQ 6 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_rowcount", "filter": "id>=0", "outputFields": ["id"]}
=== RESP 6 ===
status: 200
body: {"code":0,"cost":0,"data":[{"id":0},{"id":1},{"id":2},{"id":3},{"id":4}]}


=== REQ 7 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_rowcount", "dbName": "default"}
=== RESP 7 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 8 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_rowcount", "dimension": 4}
=== RESP 8 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 9 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_rowcount", "data": [{"id": 0, "value": 0, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 1, "value": 1, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 2, "value": 2, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 3, "value": 3, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 4, "value": 4, "vector": [0.1, 0.2, 0.3, 0.4]}]}
=== RESP 9 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":5,"insertIds":[0,1,2,3,4]}}

=== REQ 10 ===
POST http://localhost:19530/v2/vectordb/collections/load
payload: {"collectionName": "test_rowcount", "dbName": "default"}
=== RESP 10 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 11 ===
POST http://localhost:19530/v2/vectordb/collections/get_stats
payload: {"collectionName": "test_rowcount"}
=== RESP 11 ===
status: 200
body: {"code":0,"data":{"rowCount":0}}

=== REQ 12 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_rowcount", "filter": "id>=0", "outputFields": ["id"]}
=== RESP 12 ===
status: 200
body: {"code":0,"cost":0,"data":[{"id":0},{"id":1},{"id":2},{"id":3},{"id":4}]}
--- 契约依据（expected，M3 重建版） ---
[经端点过滤与依据核查后，无 endpoint=collections+get_stats 的可核查约束行]
VERDICT: UNKNOWN (replay capture — no attack-agent assertion output; raw HTTP only)



--------

## 案 3: milvus_005

**源码 clone**：`c:\Users\11428\Desktop\testvdb_paper\.sourcedeps\milvus\v2.6.10`

=== 候选缺陷 milvus_005 ===
[vendor=milvus version=2.6.10 defect_type=doc_mismatch endpoint=entities+insert]
--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] insert dynamic field names '123field'/'@field' -> http=200, code=0
- [c1_q] query field '123field' -> http=200, code=65535, message: parse output field name failed: 123field
- [c2] control: insert valid field name -> http=200, code=0
- [c2_q] control: query valid field -> http=200, code=101, message: collection not loaded

执行日志全文（output_milvus_005.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_<tracked>", "dbName": "default"}
=== RESP 1 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_<tracked>", "schema": {"autoID": false, "enableDynamicField": true, "fields": [{"fieldName": "id", "dataType": "Int64", "isPrimary": true}, {"fieldName": "vector", "dataType": "FloatVector", "elementTypeParams": {"dim": 4}}]}}
=== RESP 2 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_<tracked>", "data": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4], "123field": "v1"}, {"id": 2, "vector": [0.2, 0.2, 0.3, 0.4], "@field": "v2"}]}
=== RESP 3 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":2,"insertIds":[1,2]}}

=== REQ 4 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_<tracked>", "filter": "id in [1,2]", "outputFields": ["123field", "@field"]}
=== RESP 4 ===
status: 200
body: {"code":65535,"message":"parse output field name failed: 123field"}

=== REQ 5 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_<tracked>", "data": [{"id": 3, "vector": [0.3, 0.2, 0.3, 0.4], "valid_field": "ok"}]}
=== RESP 5 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":1,"insertIds":[3]}}

=== REQ 6 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_<tracked>", "filter": "id==3", "outputFields": ["valid_field"]}
=== RESP 6 ===
status: 200
body: {"code":101,"message":"failed to query: collection not loaded[collection=468359262963438392]"}

=== REQ 7 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_<tracked>", "dbName": "default"}
=== RESP 7 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 8 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_<tracked>", "schema": {"autoID": false, "enableDynamicField": true, "fields": [{"fieldName": "id", "dataType": "Int64", "isPrimary": true}, {"fieldName": "vector", "dataType": "FloatVector", "elementTypeParams": {"dim": 4}}]}}
=== RESP 8 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 9 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_<tracked>", "data": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4], "123field": "v1"}, {"id": 2, "vector": [0.2, 0.2, 0.3, 0.4], "@field": "v2"}]}
=== RESP 9 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":2,"insertIds":[1,2]}}

=== REQ 10 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_<tracked>", "filter": "id in [1,2]", "outputFields": ["123field", "@field"]}
=== RESP 10 ===
status: 200
body: {"code":65535,"message":"parse output field name failed: 123field"}

=== REQ 11 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_<tracked>", "data": [{"id": 3, "vector": [0.3, 0.2, 0.3, 0.4], "valid_field": "ok"}]}
=== RESP 11 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":1,"insertIds":[3]}}

=== REQ 12 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_<tracked>", "filter": "id==3", "outputFields": ["valid_field"]}
=== RESP 12 ===
status: 200
body: {"code":101,"message":"failed to query: collection not loaded[collection=468359683278836488]"}
--- 契约依据（expected，M3 重建版） ---
[经端点过滤与依据核查后，无 endpoint=entities+insert 的可核查约束行]



--------

## 案 4: milvus_038

**源码 clone**：`C:\Users\11428\Desktop\mftui\TestVDB\.sourcedeps\milvus\v3.0.0`

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



--------

## 案 5: milvus_030

**源码 clone**：`c:\Users\11428\Desktop\testvdb_paper\.sourcedeps\milvus\v2.6.17`

=== 候选缺陷 milvus_030 ===
[vendor=milvus version=2.6.17 defect_type=doc_mismatch endpoint=users+create]
--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] users/create with all-lowercase password 'abcdefgh' -> http=200, code=0
- [c2] control: users/create with complex password 'ValidP@ss1' -> http=200, code=0
- [c3] users/create with short password 'a' -> http=200, code=1100

执行日志全文（output_milvus_030.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/users/create
payload: {"userName": "testuser8char", "password": "abcdefgh"}
=== RESP 1 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/users/create
payload: {"userName": "testuservalid", "password": "ValidP@ss1"}
=== RESP 2 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/users/create
payload: {"userName": "testuser1ch", "password": "a"}
=== RESP 3 ===
status: 200
body: {"code":1100,"message":"invalid password length: invalid parameter[1 out of range 6 \u003c= value \u003c= 72]"}
--- 契约依据（expected，M3 重建版） ---
[经端点过滤与依据核查后，无 endpoint=users+create 的可核查约束行]



--------

## 案 6: milvus_036

**源码 clone**：`C:\Users\11428\Desktop\mftui\TestVDB\.sourcedeps\milvus\v3.0.0`

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
--- 契约依据（expected，M3 重建版） ---
{"constraint_id": "milvus_state_search_load_001", "endpoint": "entities+search", "type": "state_constraint", "description": "Search requires collection to be loaded", "assertion": "collection MUST be loaded before search", "source_url": "https://milvus.io/docs/single-vector-search.md", "confidence": 1.0, "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "milvus_state_search_requires_load_001", "endpoint": "entities+search", "type": "state_constraint", "description": "Collection must be loaded before searching", "assertion": "collection.load_state == 'loaded' before search", "source_url": "https://milvus.io/docs/single-vector-search.md", "confidence": 1.0, "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}
{"assertion_id": "milvus_assert_search_empty_001", "endpoint": "entities+search", "description": "Searching empty collection returns empty results", "source_url": "https://milvus.io/docs/single-vector-search.md", "confidence": 1.0, "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}



--------

## 案 7: milvus_043

**源码 clone**：`C:\Users\11428\Desktop\mftui\TestVDB\.sourcedeps\milvus\v3.0.0`

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
--- 契约依据（expected，M3 重建版） ---
{"constraint_id": "milvus_state_search_load_001", "endpoint": "entities+search", "type": "state_constraint", "description": "Search requires collection to be loaded", "assertion": "collection MUST be loaded before search", "source_url": "https://milvus.io/docs/single-vector-search.md", "confidence": 1.0, "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "milvus_state_search_requires_load_001", "endpoint": "entities+search", "type": "state_constraint", "description": "Collection must be loaded before searching", "assertion": "collection.load_state == 'loaded' before search", "source_url": "https://milvus.io/docs/single-vector-search.md", "confidence": 1.0, "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}
{"assertion_id": "milvus_assert_search_empty_001", "endpoint": "entities+search", "description": "Searching empty collection returns empty results", "source_url": "https://milvus.io/docs/single-vector-search.md", "confidence": 1.0, "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}



--------

## 案 8: milvus_011

**源码 clone**：`c:\Users\11428\Desktop\testvdb_paper\.sourcedeps\milvus\v2.6.16`

=== 候选缺陷 milvus_011 ===
[vendor=milvus version=2.6.16 defect_type=semantics endpoint=entities+query]
--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] query with filter=null -> http=200, code=0, returned all rows
- [c2] query with filter omitted -> http=200, code=0, returned all rows
- [c3] control: query with filter='' -> http=200, code=0

执行日志全文（output_milvus_011.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_coll", "dbName": "default"}
=== RESP 1 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_coll", "dimension": 4}
=== RESP 2 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_coll", "data": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 2, "vector": [0.2, 0.2, 0.3, 0.4]}]}
=== RESP 3 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":2,"insertIds":[1,2]}}

=== REQ 4 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_coll", "filter": null, "outputFields": ["id"]}
=== RESP 4 ===
status: 200
body: {"code":0,"cost":0,"data":[{"id":1},{"id":2}]}


=== REQ 5 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_coll", "outputFields": ["id"]}
=== RESP 5 ===
status: 200
body: {"code":0,"cost":0,"data":[{"id":1},{"id":2}]}


=== REQ 6 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_coll", "filter": "", "outputFields": ["id"]}
=== RESP 6 ===
status: 200
body: {"code":0,"cost":0,"data":[{"id":1},{"id":2}]}


=== REQ 7 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_coll", "dbName": "default"}
=== RESP 7 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 8 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_coll", "dimension": 4}
=== RESP 8 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 9 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_coll", "data": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 2, "vector": [0.2, 0.2, 0.3, 0.4]}]}
=== RESP 9 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":2,"insertIds":[1,2]}}

=== REQ 10 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_coll", "filter": null, "outputFields": ["id"]}
=== RESP 10 ===
status: 200
body: {"code":0,"cost":0,"data":[{"id":1},{"id":2}]}


=== REQ 11 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_coll", "outputFields": ["id"]}
=== RESP 11 ===
status: 200
body: {"code":0,"cost":0,"data":[{"id":1},{"id":2}]}


=== REQ 12 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "test_coll", "filter": "", "outputFields": ["id"]}
=== RESP 12 ===
status: 200
body: {"code":0,"cost":0,"data":[{"id":1},{"id":2}]}
--- 契约依据（expected，M3 重建版） ---
[经端点过滤与依据核查后，无 endpoint=entities+query 的可核查约束行]



--------

## 案 9: weaviate_007

**源码 clone**：`c:\Users\11428\Desktop\testvdb_paper\.sourcedeps\weaviate\v1.38.0`

=== 候选缺陷 weaviate_007 ===
[vendor=weaviate version=1.38.0 defect_type=type_coercion endpoint=/schema]
--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] POST schema with distance=null -> http=200, stored distance=cosine

执行日志全文（output_weaviate_007.log）：
=== REQ 1 ===
DELETE http://localhost:18080/v1/schema/TestClass
=== RESP 1 ===
status: 200
body: 

=== REQ 2 ===
POST http://localhost:18080/v1/schema
payload: {"class": "TestClass", "vectorizer": "none", "vectorIndexConfig": {"distance": null}}
=== RESP 2 ===
status: 200
body: {"class":"TestClass","invertedIndexConfig":{"bm25":{"b":0.75,"k1":1.2},"cleanupIntervalSeconds":60,"stopwords":{"additions":null,"preset":"en","removals":null},"usingBlockMaxWAND":true},"multiTenancyConfig":{"autoTenantActivation":false,"autoTenantCreation":false,"enabled":false},"properties":null,"shardingConfig":{"virtualPerPhysical":128,"desiredCount":1,"actualCount":1,"desiredVirtualCount":128,"actualVirtualCount":128,"key":"_id","strategy":"hash","function":"murmur3"},"vectorIndexConfig":{"skip":false,"cleanupIntervalSeconds":300,"maxConnections":32,"efConstruction":128,"ef":-1,"dynamicEfMin":100,"dynamicEfMax":500,"dynamicEfFactor":8,"vectorCacheMaxObjects":1000000000000,"flatSearchCutoff":40000,"distance":"cosine","pq":{"enabled":false,"bitCompression":false,"segments":0,"centroids":256,"trainingLimit":100000,"encoder":{"type":"kmeans","distribution":"log-normal"}},"bq":{"enabled":false},"sq":{"enabled":false,"trainingLimit":100000,"rescoreLimit":20},"rq":{"enabled":false,"bits":8,"rescoreLimit":20},"filterStrategy":"acorn","multivector":{"enabled":false,"muvera":{"enabled":false,"ksim":4,"dprojections":16,"repetitions":10},"aggregation":"maxSim"},"skipDefaultQuantization":false,"trackDefaultQuantization":false},"vectorIndexType":"hnsw","vectorizer":"none","replicationConfig":{"deletionStrategy":"TimeBasedResolution","factor":1,"asyncEnabled":false}}


=== REQ 3 ===
GET http://localhost:18080/v1/schema/TestClass
=== RESP 3 ===
status: 200
body: {"class":"TestClass","invertedIndexConfig":{"bm25":{"b":0.75,"k1":1.2},"cleanupIntervalSeconds":60,"stopwords":{"additions":null,"preset":"en","removals":null},"usingBlockMaxWAND":true},"multiTenancyConfig":{"autoTenantActivation":false,"autoTenantCreation":false,"enabled":false},"properties":null,"shardingConfig":{"actualCount":1,"actualVirtualCount":128,"desiredCount":1,"desiredVirtualCount":128,"function":"murmur3","key":"_id","strategy":"hash","virtualPerPhysical":128},"vectorIndexConfig":{"bq":{"enabled":false},"cleanupIntervalSeconds":300,"distance":"cosine","dynamicEfFactor":8,"dynamicEfMax":500,"dynamicEfMin":100,"ef":-1,"efConstruction":128,"filterStrategy":"acorn","flatSearchCutoff":40000,"maxConnections":32,"multivector":{"aggregation":"maxSim","enabled":false,"muvera":{"dprojections":16,"enabled":false,"ksim":4,"repetitions":10}},"pq":{"bitCompression":false,"centroids":256,"enabled":false,"encoder":{"distribution":"log-normal","type":"kmeans"},"segments":0,"trainingLimit":100000},"rq":{"bits":8,"enabled":false,"rescoreLimit":20},"skip":false,"skipDefaultQuantization":false,"sq":{"enabled":false,"rescoreLimit":20,"trainingLimit":100000},"trackDefaultQuantization":false,"vectorCacheMaxObjects":1000000000000},"vectorIndexType":"hnsw","vectorizer":"none","replicationConfig":{"deletionStrategy":"TimeBasedResolution","factor":1,"asyncEnabled":false}}
--- 契约依据（expected，M3 重建版） ---
{"constraint_id": "weaviate_type_schema_create_001", "endpoint": "/schema POST", "type": "type_constraint", "description": "class field must be CamelCase", "assertion": "properties.class matches /^[A-Z][a-zA-Z0-9]*$/", "source_url": "https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json", "confidence": 0.95, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "weaviate_type_schema_create_002", "endpoint": "/schema POST", "type": "type_constraint", "description": "vectorIndexType must be one of allowed index types", "assertion": "properties.vectorIndexType in {hnsw, flat, dynamic, bwes}", "source_url": "https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json", "confidence": 0.95, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "weaviate_type_schema_create_003", "endpoint": "/schema POST", "type": "type_constraint", "description": "properties[].tokenization must be a valid enum value", "assertion": "properties.properties[].tokenization in {word, lowercase, whitespace, field, trigram, gse, kagome_kr, kagome_ja, gse_ch}", "source_url": "https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json", "confidence": 0.95, "source_type": "structured-spec", "evidence_tier": "explicit"}
{"constraint_id": "weaviate_type_tenants_create_001", "endpoint": "/schema/{className}/tenants POST", "type": "type_constraint", "description": "Tenant.activityStatus on create must be ACTIVE or INACTIVE", "assertion": "body[].activityStatus in {ACTIVE, INACTIVE}", "source_url": "https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json", "confidence": 0.95, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "weaviate_type_tenants_update_001", "endpoint": "/schema/{className}/tenants PUT", "type": "type_constraint", "description": "Tenant.activityStatus on update must be ACTIVE, INACTIVE, or OFFLOADED", "assertion": "body[].activityStatus in {ACTIVE, INACTIVE, OFFLOADED}", "source_url": "https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json", "confidence": 0.95, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "weaviate_type_index_update_001", "endpoint": "/schema/{className}/indexes/{propertyName} PUT", "type": "type_constraint", "description": "searchable.algorithm must be blockmax (WAND->BlockMax migration only; downgrade rejected)", "assertion": "body.searchable.algorithm == 'blockmax'", "source_url": "https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json", "confidence": 0.9, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "weaviate_range_schema_replication_001", "endpoint": "/schema POST", "type": "range_constraint", "description": "replicationConfig.factor is an integer (default 1)", "assertion": "replicationConfig.factor >= 1", "source_url": "https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json", "confidence": 0.85, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "weaviate_state_schema_delete_001", "endpoint": "/schema/{className} DELETE", "type": "state_constraint", "description": "deleting a collection permanently deletes all data objects in the collection", "assertion": "after DELETE /schema/{className}, GET /objects?class={className} returns empty", "source_url": "https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json", "confidence": 0.95, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "weaviate_state_tenants_delete_001", "endpoint": "/schema/{className}/tenants DELETE", "type": "state_constraint", "description": "deleting tenants permanently deletes all tenant data", "assertion": "after DELETE tenants, GET tenant returns 404 and its data is gone", "source_url": "https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json", "confidence": 0.9, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "weaviate_state_schema_update_001", "endpoint": "/schema/{className} PUT", "type": "state_constraint", "description": "PUT does NOT add properties (use POST /schema/{className}/properties) and does NOT rename", "assertion": "PUT /schema/{className} does not change properties count or names", "source_url": "https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json", "confidence": 0.9, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"assertion_id": "weaviate_behavioral_schema_create_001", "endpoint": "/schema POST", "description": "creating collection with disallowed vectorIndexType returns 422 RestrictionViolationResponse", "source_url": "https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json", "confidence": 0.95, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"assertion_id": "weaviate_behavioral_schema_create_002", "endpoint": "/schema POST", "description": "exceeding collections/shards usage limit returns 429 UsageLimitExceededResponse", "source_url": "https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json", "confidence": 0.95, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"assertion_id": "weaviate_behavioral_tenants_create_001", "endpoint": "/schema/{className}/tenants POST", "description": "exceeding tenant usage limit returns 429 with limit: tenants", "source_url": "https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json", "confidence": 0.95, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "weaviate_range_schema_replication_001", "endpoint": "/schema POST", "description": "replicationConfig.factor is an integer (default 1)", "assertion": "replicationConfig.factor >= 1", "type": "range_constraint", "confidence": 0.85, "evidence_tier": "inferred_from_behavior", "source_url": "https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json", "source_status": "reachable", "source_type": "structured-spec"}
{"constraint_id": "weaviate_type_schema_create_001", "endpoint": "/schema POST", "description": "class field must be CamelCase", "assertion": "properties.class matches /^[A-Z][a-zA-Z0-9]*$/", "type": "type_constraint", "confidence": 0.95, "evidence_tier": "inferred_from_behavior", "source_url": "https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json", "source_status": "reachable", "source_type": "structured-spec"}
{"constraint_id": "weaviate_type_schema_create_002", "endpoint": "/schema POST", "description": "vectorIndexType must be one of allowed index types", "assertion": "properties.vectorIndexType in {hnsw, flat, dynamic, bwes}", "type": "type_constraint", "confidence": 0.95, "evidence_tier": "inferred_from_behavior", "source_url": "https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json", "source_status": "reachable", "source_type": "structured-spec"}
{"constraint_id": "weaviate_type_schema_create_003", "endpoint": "/schema POST", "description": "properties[].tokenization must be a valid enum value", "assertion": "properties.properties[].tokenization in {word, lowercase, whitespace, field, trigram, gse, kagome_kr, kagome_ja, gse_ch}", "type": "type_constraint", "confidence": 0.95, "evidence_tier": "explicit", "source_url": "https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json", "source_status": "reachable", "source_type": "structured-spec"}
{"constraint_id": "weaviate_state_schema_update_001", "endpoint": "/schema/{className} PUT", "description": "PUT does NOT add properties (use POST /schema/{className}/properties) and does NOT rename", "assertion": "PUT /schema/{className} does not change properties count or names", "type": "state_constraint", "confidence": 0.9, "evidence_tier": "inferred_from_behavior", "source_url": "https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json", "source_status": "reachable", "source_type": "structured-spec"}
{"constraint_id": "weaviate_type_tenants_create_001", "endpoint": "/schema/{className}/tenants POST", "description": "Tenant.activityStatus on create must be ACTIVE or INACTIVE", "assertion": "body[].activityStatus in {ACTIVE, INACTIVE}", "type": "type_constraint", "confidence": 0.95, "evidence_tier": "inferred_from_behavior", "source_url": "https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json", "source_status": "reachable", "source_type": "structured-spec"}
{"constraint_id": "weaviate_type_tenants_update_001", "endpoint": "/schema/{className}/tenants PUT", "description": "Tenant.activityStatus on update must be ACTIVE, INACTIVE, or OFFLOADED", "assertion": "body[].activityStatus in {ACTIVE, INACTIVE, OFFLOADED}", "type": "type_constraint", "confidence": 0.95, "evidence_tier": "inferred_from_behavior", "source_url": "https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json", "source_status": "reachable", "source_type": "structured-spec"}



--------

## 案 10: milvus_010

**源码 clone**：`c:\Users\11428\Desktop\testvdb_paper\.sourcedeps\milvus\v2.6.16`

=== 候选缺陷 milvus_010 ===
[vendor=milvus version=2.6.16 defect_type=semantics endpoint=collections+create]
--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] create with negative TTL -> http=200, code=0
- [c1_rb] describe collection after negative-TTL create -> http=200
- [c2] control: alter_properties with negative TTL -> http=200, code=1100

执行日志全文（output_milvus_010.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_ttl_neg", "dbName": "default"}
=== RESP 1 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_ttl_neg", "dimension": 4, "metricType": "L2", "properties": {"collection.ttl.seconds": -100}}
=== RESP 2 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/collections/describe
payload: {"collectionName": "test_ttl_neg", "dbName": "default"}
=== RESP 3 ===
status: 200
body: {"code":0,"data":{"aliases":[],"autoId":false,"collectionID":468358976047044489,"collectionName":"test_ttl_neg","consistencyLevel":"Bounded","description":"","enableDynamicField":true,"fields":[{"autoId":false,"clusteringKey":false,"description":"","id":100,"name":"id","nullable":false,"partitionKey":false,"primaryKey":true,"type":"Int64"},{"autoId":false,"clusteringKey":false,"description":"","id":101,"name":"vector","nullable":false,"params":[{"key":"dim","value":"4"}],"partitionKey":false,"primaryKey":false,"type":"FloatVector"}],"functions":[],"indexes":[{"fieldName":"vector","indexName":"vector","metricType":"L2"}],"load":"LoadStateLoading","partitionsNum":1,"properties":[{"key":"timezone","value":"UTC"}],"shardsNum":1},"message":""}

=== REQ 4 ===
POST http://localhost:19530/v2/vectordb/collections/alter_properties
payload: {"collectionName": "test_ttl_neg", "properties": {"collection.ttl.seconds": -100}}
=== RESP 4 ===
status: 200
body: {"code":1100,"message":"collection TTL is out of range, expect [-1, 3155760000], got -100: invalid parameter"}

=== REQ 5 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_ttl_neg", "dbName": "default"}
=== RESP 5 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 6 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_ttl_neg", "dimension": 4, "metricType": "L2", "properties": {"collection.ttl.seconds": -100}}
=== RESP 6 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 7 ===
POST http://localhost:19530/v2/vectordb/collections/describe
payload: {"collectionName": "test_ttl_neg", "dbName": "default"}
=== RESP 7 ===
status: 200
body: {"code":0,"data":{"aliases":[],"autoId":false,"collectionID":468359796041078668,"collectionName":"test_ttl_neg","consistencyLevel":"Bounded","description":"","enableDynamicField":true,"fields":[{"autoId":false,"clusteringKey":false,"description":"","id":100,"name":"id","nullable":false,"partitionKey":false,"primaryKey":true,"type":"Int64"},{"autoId":false,"clusteringKey":false,"description":"","id":101,"name":"vector","nullable":false,"params":[{"key":"dim","value":"4"}],"partitionKey":false,"primaryKey":false,"type":"FloatVector"}],"functions":[],"indexes":[{"fieldName":"vector","indexName":"vector","metricType":"L2"}],"load":"LoadStateLoading","partitionsNum":1,"properties":[{"key":"timezone","value":"UTC"}],"shardsNum":1},"message":""}

=== REQ 8 ===
POST http://localhost:19530/v2/vectordb/collections/alter_properties
payload: {"collectionName": "test_ttl_neg", "properties": {"collection.ttl.seconds": -100}}
=== RESP 8 ===
status: 200
body: {"code":1100,"message":"collection TTL is out of range, expect [-1, 3155760000], got -100: invalid parameter"}
--- 契约依据（expected，M3 重建版） ---
{"constraint_id": "milvus_type_collections_create_001", "endpoint": "collections+create", "type": "type_constraint", "description": "collectionName must be a string", "assertion": "collectionName is of type string", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "confidence": 1.0, "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "milvus_type_collections_create_002", "endpoint": "collections+create", "type": "type_constraint", "description": "metricType must be L2, IP, or COSINE", "assertion": "metricType in [L2, IP, COSINE]", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "confidence": 1.0, "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "milvus_type_collections_create_003", "endpoint": "collections+create", "type": "type_constraint", "description": "consistencyLevel must be Strong, Session, Bounded, or Eventually", "assertion": "consistencyLevel in [Strong, Session, Bounded, Eventually]", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "confidence": 1.0, "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}
{"assertion_id": "milvus_behavioral_collections_create_001", "endpoint": "collections+create", "description": "Create collection returns 200 on success", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "confidence": 1.0, "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}
{"assertion_id": "milvus_behavioral_collections_create_001", "endpoint": "collections+create", "description": "Create collection returns 200 on success", "category": "behavioral", "expected_behavior": "returns 200 with code: 0 and empty data object", "confidence": 1.0, "defect_type_if_violated": "Type1_IllegalSuccess", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "doc_version": "2.6.x", "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "milvus_type_collections_create_001", "endpoint": "collections+create", "description": "collectionName must be a string", "assertion": "collectionName is of type string", "type": "type_constraint", "confidence": 1.0, "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "source_status": "reachable", "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "milvus_type_collections_create_003", "endpoint": "collections+create", "description": "consistencyLevel must be Strong, Session, Bounded, or Eventually", "assertion": "consistencyLevel in [Strong, Session, Bounded, Eventually]", "type": "type_constraint", "confidence": 1.0, "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "source_status": "reachable", "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}
VERDICT: UNKNOWN (replay capture — no attack-agent assertion output; raw HTTP only)



--------

## 案 11: milvus_013

**源码 clone**：`c:\Users\11428\Desktop\testvdb_paper\.sourcedeps\milvus\v2.6.16`

=== 候选缺陷 milvus_013 ===
[vendor=milvus version=2.6.16 defect_type=param_validation endpoint=collections+list]
--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] Request-Timeout=3.5 (float) header -> http=200, code=0
- [c2] Request-Timeout=abc (string) header -> http=200, code=0
- [c3] control: Request-Timeout=10 (integer) -> http=200, code=0

执行日志全文（output_milvus_013.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/collections/list
headers: {"Request-Timeout": "3.5"}
payload: {}
=== RESP 1 ===
status: 200
body: {"code":0,"data":[]}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/collections/list
headers: {"Request-Timeout": "abc"}
payload: {}
=== RESP 2 ===
status: 200
body: {"code":0,"data":[]}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/collections/list
headers: {"Request-Timeout": "10"}
payload: {}
=== RESP 3 ===
status: 200
body: {"code":0,"data":[]}
--- 契约依据（expected，M3 重建版） ---
[本版本文档中无 endpoint=collections+list 的约束条目]
[本版本文档中无 Request-Timeout 的类型约束条目]
已核查的引用页（2.6.x REST API 参考，实测可访问，来源类型=documentation）：
- https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md
- https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Drop.md
- https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Load.md
- https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Rename.md
- https://milvus.io/api-reference/restful/v2.6.x/v2/Vector%20(v2)/Get.md
- https://milvus.io/api-reference/restful/v2.6.x/v2/Vector%20(v2)/Search.md
核查结论：上述页面的 Parameters 表仅将 Authorization 列为 header 参数；Request-Timeout
仅出现在 curl 示例行中，不含任何类型或取值约束的描述。



--------

## 案 12: qdrant_027

**源码 clone**：`c:\Users\11428\Desktop\testvdb_paper\.sourcedeps\qdrant\v1.19.0`

# 候选缺陷 qdrant_027

[vendor=qdrant version=1.19.0 endpoint=index]
--- 观察到的行为（observed） ---

重放环境:qdrant v1.19.0 container (port 6338);证据来源:container replay,HTTP interactions captured verbatim。

=== DELETE /collections/idxdemo ===
-> 200 {"result":true,"status":"ok","time":0.008861772}
=== PUT /collections/idxdemo ===
{"vectors": {"size": 4, "distance": "Euclid"}}
-> 200 {"result":true,"status":"ok","time":0.224044041}
=== PUT /collections/idxdemo/points?wait=true ===
{"points": [{"id": 1, "vector": [1.0, 1.0, 1.0, 1.0], "payload": {"tag": "t1", "n": 1}}, {"id": 2, "vector": [2.0, 2.0, 2.0, 2.0], "payload": {"tag": "t2", "n": 2}}, {"id": 3, "vector": [3.0, 3.0, 3.0, 3.0], "payload": {"tag": "t0", "n": 3}}, {"id": 4, "vector": [4.0, 4.0, 4.0, 4.0], "payload": {"tag": "t1", "n": 4}}, {"id": 5, "vector": [5.0, 5.0, 5.0, 5.0], "payload": {"tag": "t2", "n": 5}}, {"id": 6, "vector": [6.0, 6.0, 6.0, 6.0], "payload": {"tag": "t0", "n": 6}}, {"id": 7, "vector": [7.0, 7.0, 7.0, 7.0], "payload": {"tag": "t1", "n": 7}}, {"id": 8, "vector": [8.0, 8.0, 8.0, 8.0], "payload": {"tag": "t2", "n": 8}}, {"id": 9, "vector": [9.0, 9.0, 9.0, 9.0], "payload": {"tag": "t0", "n": 9}}, {"id": 10, "vector": [10.0, 10.0, 10.0, 10.0], "payload": {"tag": "t1", "n": 10}}, {"id": 11, "vector": [11.0, 11.0, 11.0, 11.0], "payload": {"tag": "t2", "n": 11}}, {"id": 12, "vector": [12.0, 12.0, 12.0, 12.0], "payload": {"tag": "t0", "n": 12}}, {"id": 13, "vector": [13.0, 13.0, 13.0, 13.0], "payload": {"tag": "t1", "n": 13}}, {"id": 14, "vector": [14.0, 14.0, 14.0, 14.0], "payload": {"tag": "t2", "n": 14}}, {"id": 15, "vector": [15.0, 15.0, 15.0, 15.0], "payload": {"tag": "t0", "n": 15}}, {"id": 16, "vector": [16.0, 16.0, 16.0, 16.0], "payload": {"tag": "t1", "n": 16}}, {"id": 17, "vector": [17.0, 17.0, 17.0, 17.0], "payload": {"tag": "t2", "n": 17}}, {"id": 18, "vector": [18.0, 18.0, 18.0, 18.0], "payload": {"tag": "t0", "n": 18}}, {"id": 19, "vector": [19.0, 19.0, 19.0, 19.0], "payload": {"tag": "t1", "n": 19}}, {"id": 20, "vector": [20.0, 20.0, 20.0, 20.0], "payload": {"tag": "t2", "n": 20}}]}
-> 200 {"result":{"operation_id":1,"status":"completed"},"status":"ok","time":0.003736864}
=== PUT /collections/idxdemo/index ===
{"field_name": "tag", "field_schema": ["keyword"]}
-> 200 {"result":{"operation_id":3,"status":"acknowledged"},"status":"ok","time":0.011375286}
=== GET /collections/idxdemo ===
-> 200 {"result":{"status":"green","optimizer_status":"ok","indexed_vectors_count":0,"points_count":20,"segments_count":8,"config":{"params":{"vectors":{"size":4,"distance":"Euclid"},"shard_number":1,"replication_factor":1,"write_consistency_factor":1,"on_disk_payload":true},"hnsw_config":{"m":16,"ef_construct":100,"full_scan_threshold":10000,"max_indexing_threads":0,"on_disk":false},"optimizer_config":{"deleted_threshold":0.2,"vacuum_min_vector_number":1000,"default_segment_number":0,"max_segment_size":null,"memmap_threshold":null,"indexing_threshold":10000,"flush_interval_sec":5,"max_optimization_threads":null,"prevent_unoptimized":null},"wal_config":{"wal_capacity_mb":32,"wal_segments_ahead":0,"wal_retain_closed":1},"quantization_config":null},"payload_schema":{},"update_queue":{"length":1}},"status":"ok","time":0.000346443}
[STDOUT]
PUT index field_schema=['keyword'] -> 200 {"result": {"operation_id": 3, "status": "acknowledged"}, "status": "ok", "time": 0.011375286}
payload_schema after: {}
--- 契约依据（expected，M3 重建版） ---
{"constraint_id": "qdrant_state_create_index_011", "endpoint": "collections+{collection_name}+index", "description": "Index creation is async; query optimization applies after index is built", "assertion": "Index creation is asynchronous; query optimization applies after the index is built.", "type": "state_constraint", "confidence": 1.0, "evidence_tier": "inferred_from_behavior", "source_url": "https://github.com/qdrant/qdrant/blob/v1.19.0/docs/redoc/master/openapi.json", "source_status": "reachable", "doc_version": "1.18.x", "source_verified": true, "source_type": "structured-spec"}



--------

## 案 13: milvus_012

**源码 clone**：`c:\Users\11428\Desktop\testvdb_paper\.sourcedeps\milvus\v2.6.16`

=== 候选缺陷 milvus_012 ===
[vendor=milvus version=2.6.16 defect_type=param_validation endpoint=collections+list]
--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] collections/list with dbName empty -> http=200, code=0
- [c2] control: query with filter='' -> http=200, code=100

执行日志全文（output_milvus_012.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/collections/list
payload: {"dbName": ""}
=== RESP 1 ===
status: 200
body: {"code":0,"data":["test_nprobe","test_ttl_neg","test_coll"]}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "some_coll", "filter": ""}
=== RESP 2 ===
status: 200
body: {"code":100,"message":"can't find collection[database=default][collection=some_coll]"}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/collections/list
payload: {"dbName": ""}
=== RESP 3 ===
status: 200
body: {"code":0,"data":["test_nprobe","test_ttl_neg","test_coll"]}

=== REQ 4 ===
POST http://localhost:19530/v2/vectordb/entities/query
payload: {"collectionName": "some_coll", "filter": ""}
=== RESP 4 ===
status: 200
body: {"code":100,"message":"can't find collection[database=default][collection=some_coll]"}
--- 契约依据（expected，M3 重建版） ---
描述性依据（documentation，v2.6.x 段）：dbName 参数文档描述为
"The name of an existing database."（string，无 required 标注，无非空/拒绝语义声明）
来源：https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/List.md



--------

## 案 14: milvus_025

**源码 clone**：`c:\Users\11428\Desktop\testvdb_paper\.sourcedeps\milvus\v2.6.17`

=== 候选缺陷 milvus_025 ===
[vendor=milvus version=2.6.17 defect_type=param_validation endpoint=entities+insert]
--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] insert 101 entities -> http=200, code=0, insertCount=101

执行日志全文（output_milvus_025.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_limit", "dbName": "default"}
=== RESP 1 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_limit", "dimension": 4}
=== RESP 2 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_limit", "data": [{"id": 0, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 1, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 2, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 3, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 4, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 5, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 6, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 7, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 8, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 9, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 10, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 11, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 12, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 13, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 14, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 15, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 16, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 17, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 18, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 19, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 20, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 21, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 22, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 23, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 24, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 25, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 26, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 27, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 28, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 29, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 30, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 31, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 32, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 33, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 34, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 35, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 36, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 37, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 38, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 39, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 40, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 41, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 42, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 43, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 44, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 45, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 46, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 47, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 48, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 49, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 50, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 51, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 52, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 53, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 54, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 55, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 56, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 57, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 58, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 59, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 60, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 61, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 62, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 63, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 64, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 65, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 66, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 67, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 68, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 69, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 70, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 71, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 72, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 73, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 74, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 75, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 76, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 77, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 78, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 79, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 80, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 81, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 82, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 83, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 84, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 85, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 86, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 87, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 88, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 89, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 90, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 91, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 92, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 93, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 94, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 95, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 96, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 97, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 98, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 99, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 100, "vector": [0.1, 0.2, 0.3, 0.4]}]}
=== RESP 3 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":101,"insertIds":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100]}}
--- 契约依据（expected，M3 重建版） ---
[经端点过滤与依据核查后，无 endpoint=entities+insert 的可核查约束行]



--------

## 案 15: milvus_020

**源码 clone**：`c:\Users\11428\Desktop\testvdb_paper\.sourcedeps\milvus\v2.6.16`

=== 候选缺陷 milvus_020 ===
[vendor=milvus version=2.6.16 defect_type=behavior endpoint=entities+search]
--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1_before] search before delete -> http=200, code=0, 10 results (id 0-9)
- [c1] search after deleting ids 1-5 -> http=200, code=0, returned ids [0,1,2,3,4,5,6,7,8,9]

执行日志全文（output_milvus_020.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_stale_data", "dbName": "default"}
=== RESP 1 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_stale_data", "dimension": 4, "metricType": "L2"}
=== RESP 2 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/indexes/create
payload: {"collectionName": "test_stale_data", "indexParams": [{"fieldName": "vector", "metricType": "L2", "indexType": "HNSW", "params": {"M": 16, "efConstruction": 128}}]}
=== RESP 3 ===
status: 200
body: {"code":65535,"message":"CreateIndex failed: at most one distinct index is allowed per field"}

=== REQ 4 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_stale_data", "data": [{"id": 0, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 1, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 2, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 3, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 4, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 5, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 6, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 7, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 8, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 9, "vector": [0.1, 0.2, 0.3, 0.4]}]}
=== RESP 4 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":10,"insertIds":[0,1,2,3,4,5,6,7,8,9]}}

=== REQ 5 ===
POST http://localhost:19530/v2/vectordb/collections/load
payload: {"collectionName": "test_stale_data", "dbName": "default"}
=== RESP 5 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 6 ===
POST http://localhost:19530/v2/vectordb/entities/search
payload: {"collectionName": "test_stale_data", "data": [[0.1, 0.2, 0.3, 0.4]], "limit": 10, "outputFields": ["id"]}
=== RESP 6 ===
status: 200
body: {"code":0,"cost":0,"data":[{"distance":0,"id":0},{"distance":0,"id":1},{"distance":0,"id":2},{"distance":0,"id":3},{"distance":0,"id":4},{"distance":0,"id":5},{"distance":0,"id":6},{"distance":0,"id":7},{"distance":0,"id":8},{"distance":0,"id":9}],"topks":[10]}


=== REQ 7 ===
POST http://localhost:19530/v2/vectordb/entities/search
payload: {"collectionName": "test_stale_data", "data": [[0.1, 0.2, 0.3, 0.4]], "limit": 10, "outputFields": ["id"]}
=== RESP 7 ===
status: 200
body: {"code":0,"cost":0,"data":[{"distance":0,"id":0},{"distance":0,"id":1},{"distance":0,"id":2},{"distance":0,"id":3},{"distance":0,"id":4},{"distance":0,"id":5},{"distance":0,"id":6},{"distance":0,"id":7},{"distance":0,"id":8},{"distance":0,"id":9}],"topks":[10]}


=== REQ 8 ===
POST http://localhost:19530/v2/vectordb/entities/delete
payload: {"collectionName": "test_stale_data", "filter": "id in [1,2,3,4,5]", "dbName": "default"}
=== RESP 8 ===
status: 200
body: {"code":0,"data":{"deleteCount":5}}

=== REQ 9 ===
POST http://localhost:19530/v2/vectordb/entities/search
payload: {"collectionName": "test_stale_data", "data": [[0.1, 0.2, 0.3, 0.4]], "limit": 10, "outputFields": ["id"]}
=== RESP 9 ===
status: 200
body: {"code":0,"cost":0,"data":[{"distance":0,"id":0},{"distance":0,"id":1},{"distance":0,"id":2},{"distance":0,"id":3},{"distance":0,"id":4},{"distance":0,"id":5},{"distance":0,"id":6},{"distance":0,"id":7},{"distance":0,"id":8},{"distance":0,"id":9}],"topks":[10]}


=== REQ 10 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_stale_data", "dbName": "default"}
=== RESP 10 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 11 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_stale_data", "dimension": 4, "metricType": "L2"}
=== RESP 11 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 12 ===
POST http://localhost:19530/v2/vectordb/indexes/create
payload: {"collectionName": "test_stale_data", "indexParams": [{"fieldName": "vector", "metricType": "L2", "indexType": "HNSW", "params": {"M": 16, "efConstruction": 128}}]}
=== RESP 12 ===
status: 200
body: {"code":65535,"message":"CreateIndex failed: at most one distinct index is allowed per field"}

=== REQ 13 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_stale_data", "data": [{"id": 0, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 1, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 2, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 3, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 4, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 5, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 6, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 7, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 8, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 9, "vector": [0.1, 0.2, 0.3, 0.4]}]}
=== RESP 13 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":10,"insertIds":[0,1,2,3,4,5,6,7,8,9]}}

=== REQ 14 ===
POST http://localhost:19530/v2/vectordb/collections/load
payload: {"collectionName": "test_stale_data", "dbName": "default"}
=== RESP 14 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 15 ===
POST http://localhost:19530/v2/vectordb/entities/search
payload: {"collectionName": "test_stale_data", "data": [[0.1, 0.2, 0.3, 0.4]], "limit": 10, "outputFields": ["id"]}
=== RESP 15 ===
status: 200
body: {"code":0,"cost":0,"data":[{"distance":0,"id":0},{"distance":0,"id":1},{"distance":0,"id":2},{"distance":0,"id":3},{"distance":0,"id":4},{"distance":0,"id":5},{"distance":0,"id":6},{"distance":0,"id":7},{"distance":0,"id":8},{"distance":0,"id":9}],"topks":[10]}


=== REQ 16 ===
POST http://localhost:19530/v2/vectordb/entities/search
payload: {"collectionName": "test_stale_data", "data": [[0.1, 0.2, 0.3, 0.4]], "limit": 10, "outputFields": ["id"]}
=== RESP 16 ===
status: 200
body: {"code":0,"cost":0,"data":[{"distance":0,"id":0},{"distance":0,"id":1},{"distance":0,"id":2},{"distance":0,"id":3},{"distance":0,"id":4},{"distance":0,"id":5},{"distance":0,"id":6},{"distance":0,"id":7},{"distance":0,"id":8},{"distance":0,"id":9}],"topks":[10]}


=== REQ 17 ===
POST http://localhost:19530/v2/vectordb/entities/delete
payload: {"collectionName": "test_stale_data", "filter": "id in [1,2,3,4,5]", "dbName": "default"}
=== RESP 17 ===
status: 200
body: {"code":0,"data":{"deleteCount":5}}

=== REQ 18 ===
POST http://localhost:19530/v2/vectordb/entities/search
payload: {"collectionName": "test_stale_data", "data": [[0.1, 0.2, 0.3, 0.4]], "limit": 10, "outputFields": ["id"]}
=== RESP 18 ===
status: 200
body: {"code":0,"cost":0,"data":[{"distance":0,"id":0},{"distance":0,"id":1},{"distance":0,"id":2},{"distance":0,"id":3},{"distance":0,"id":4},{"distance":0,"id":5},{"distance":0,"id":6},{"distance":0,"id":7},{"distance":0,"id":8},{"distance":0,"id":9}],"topks":[10]}
--- 契约依据（expected，M3 重建版） ---
[经端点过滤与依据核查后，无 endpoint=entities+search 的可核查约束行]



--------

## 案 16: milvus_015

**源码 clone**：`c:\Users\11428\Desktop\testvdb_paper\.sourcedeps\milvus\v2.6.16`

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



--------

## 案 17: milvus_021

**源码 clone**：`c:\Users\11428\Desktop\testvdb_paper\.sourcedeps\milvus\v2.6.17`

=== 候选缺陷 milvus_021 ===
[vendor=milvus version=2.6.17 defect_type=behavior endpoint=entities+search]
--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] search on never-loaded collection -> http=200, code=0

执行日志全文（output_milvus_021.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_unloaded", "dbName": "default"}
=== RESP 1 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_unloaded", "dimension": 4, "metricType": "COSINE", "idType": "Int64", "autoID": false}
=== RESP 2 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_unloaded", "data": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4]}]}
=== RESP 3 ===
status: 200
body: {"code":0,"cost":0,"data":{"insertCount":1,"insertIds":[1]}}

=== REQ 4 ===
POST http://localhost:19530/v2/vectordb/entities/search
payload: {"collectionName": "test_unloaded", "data": [[0.1, 0.2, 0.3, 0.4]], "annsField": "vector", "limit": 5}
=== RESP 4 ===
status: 200
body: {"code":0,"cost":0,"data":[{"distance":1,"id":1}],"topks":[1]}
--- 契约依据（expected，M3 重建版） ---
[经端点过滤与依据核查后，无 endpoint=entities+search 的可核查约束行]



--------

## 案 18: qdrant_016

**源码 clone**：`c:\Users\11428\Desktop\testvdb_paper\.sourcedeps\qdrant\v1.18.2`

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



--------

## 案 19: milvus_001

**源码 clone**：`c:\Users\11428\Desktop\testvdb_paper\.sourcedeps\milvus\v2.3.0`

=== 候选缺陷 milvus_001 ===
[vendor=milvus version=2.3 defect_type=behavior endpoint=entities+search]
--- 观察到的行为（observed） ---
[无可用观察记录：raw 为空且 log 未捕获（milvus_001 特例，探针未记录原始 HTTP）]
--- 契约依据（expected，M3 重建版） ---
[受测版本 2.3.0 的版本文档段已下线（v2.3.x → 302），约束依据无法核查]
观察证据：原始执行未捕获任何 HTTP 交互（output_milvus_001.log = "[no raw HTTP captured]"）。



--------

## 案 20: qdrant_014

**源码 clone**：`c:\Users\11428\Desktop\testvdb_paper\.sourcedeps\qdrant\v1.18.2`

=== 候选缺陷 qdrant_014 ===
[vendor=qdrant version=1.18.2 defect_type=behavior endpoint=cluster+recover]
--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [setup] GET /cluster -> status=disabled
- [c1] cluster recover in standalone -> status=500, body: Service internal error: Qdrant is running in standalone mode

执行日志全文（output_qdrant_014.log）：
=== REQ 1 ===
GET http://localhost:6333/cluster
=== RESP 1 ===
status: 200
body: {"result":{"status":"disabled"},"status":"ok","time":2.37e-6}

=== REQ 2 ===
POST http://localhost:6333/cluster/recover
=== RESP 2 ===
status: 500
body: {"status":{"error":"Service internal error: Qdrant is running in standalone mode"},"time":0.015995971}

=== REQ 3 ===
GET http://localhost:6333/cluster
=== RESP 3 ===
status: 200
body: {"result":{"status":"disabled"},"status":"ok","time":3.173e-6}

=== REQ 4 ===
POST http://localhost:6333/cluster/recover
=== RESP 4 ===
status: 500
body: {"status":{"error":"Service internal error: Qdrant is running in standalone mode"},"time":0.018369187}
--- 契约依据（expected，M3 重建版） ---
[v-1-18-x 文档对 POST /cluster/recover 无行为约束条目]
该页仅含端点签名与示例响应，无 standalone 模式前提或错误行为的任何声明。
来源：https://api.qdrant.tech/v-1-18-x/api-reference/distributed/recover-current-peer



--------

## 案 21: milvus_027

**源码 clone**：`c:\Users\11428\Desktop\testvdb_paper\.sourcedeps\milvus\v2.6.17`

=== 候选缺陷 milvus_027 ===
[vendor=milvus version=2.6.17 defect_type=param_validation endpoint=collections+create]
--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c0] create with shardsNum=0 -> http=200, code=0
- [c1] create with shardsNum=-1 -> http=200, code=0
- [c2] create with shardsNum=65535 -> http=200, code=0

执行日志全文（output_milvus_027.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_shard_0", "dbName": "default"}
=== RESP 1 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_shard_0", "dimension": 4, "shardsNum": 0, "metricType": "L2"}
=== RESP 2 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_shard_neg", "dbName": "default"}
=== RESP 3 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 4 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_shard_neg", "dimension": 4, "shardsNum": -1, "metricType": "L2"}
=== RESP 4 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 5 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_shard_max", "dbName": "default"}
=== RESP 5 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 6 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_shard_max", "dimension": 4, "shardsNum": 65535, "metricType": "L2"}
=== RESP 6 ===
status: 200
body: {"code":0,"data":{}}
--- 契约依据（expected，M3 重建版） ---
{"constraint_id": "milvus_type_collections_create_001", "endpoint": "collections+create", "type": "type_constraint", "description": "collectionName must be a string", "assertion": "collectionName is of type string", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "confidence": 1.0, "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "milvus_type_collections_create_002", "endpoint": "collections+create", "type": "type_constraint", "description": "metricType must be L2, IP, or COSINE", "assertion": "metricType in [L2, IP, COSINE]", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "confidence": 1.0, "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "milvus_type_collections_create_003", "endpoint": "collections+create", "type": "type_constraint", "description": "consistencyLevel must be Strong, Session, Bounded, or Eventually", "assertion": "consistencyLevel in [Strong, Session, Bounded, Eventually]", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "confidence": 1.0, "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}
{"assertion_id": "milvus_behavioral_collections_create_001", "endpoint": "collections+create", "description": "Create collection returns 200 on success", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "confidence": 1.0, "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}
{"assertion_id": "milvus_behavioral_collections_create_001", "endpoint": "collections+create", "description": "Create collection returns 200 on success", "category": "behavioral", "expected_behavior": "returns 200 with code: 0 and empty data object", "confidence": 1.0, "defect_type_if_violated": "Type1_IllegalSuccess", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "doc_version": "2.6.x", "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "milvus_type_collections_create_001", "endpoint": "collections+create", "description": "collectionName must be a string", "assertion": "collectionName is of type string", "type": "type_constraint", "confidence": 1.0, "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "source_status": "reachable", "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}
VERDICT: UNKNOWN (replay capture — no attack-agent assertion output; raw HTTP only)



--------

## 案 22: milvus_033

**源码 clone**：`c:\Users\11428\Desktop\testvdb_paper\.sourcedeps\milvus\v2.6.19`

=== 候选缺陷 milvus_033 ===
[vendor=milvus version=2.6.19 defect_type=semantics endpoint=collections+create]
--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] create with vectorFieldType=InvalidVectorType -> http=200, code=0
- [c1_rb] describe collection -> http=200, code=0, vector field type=FloatVector

执行日志全文（output_milvus_033.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "audit5", "dbName": "default"}
=== RESP 1 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "audit5", "dimension": 4, "metricType": "L2", "idType": "Int64", "autoID": true, "vectorFieldType": "InvalidVectorType"}
=== RESP 2 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/collections/describe
payload: {"collectionName": "audit5", "dbName": "default"}
=== RESP 3 ===
status: 200
body: {"code":0,"data":{"aliases":[],"autoId":true,"collectionID":468359343909110797,"collectionName":"audit5","consistencyLevel":"Bounded","description":"","enableDynamicField":true,"fields":[{"autoId":true,"clusteringKey":false,"description":"","id":100,"name":"id","nullable":false,"partitionKey":false,"primaryKey":true,"type":"Int64"},{"autoId":false,"clusteringKey":false,"description":"","id":101,"name":"vector","nullable":false,"params":[{"key":"dim","value":"4"}],"partitionKey":false,"primaryKey":false,"type":"FloatVector"}],"functions":[],"indexes":[{"fieldName":"vector","indexName":"vector","metricType":"L2"}],"load":"LoadStateLoading","partitionsNum":1,"properties":[{"key":"timezone","value":"UTC"}],"shardsNum":1},"message":""}
--- 契约依据（expected，M3 重建版） ---
{"constraint_id": "milvus_type_collections_create_001", "endpoint": "collections+create", "type": "type_constraint", "description": "collectionName must be a string", "assertion": "typeof collectionName === 'string'", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "confidence": 1.0, "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "milvus_type_collections_create_002", "endpoint": "collections+create", "type": "type_constraint", "description": "metricType must be L2, IP, or COSINE", "assertion": "metricType in ['L2', 'IP', 'COSINE']", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "confidence": 1.0, "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "milvus_type_collections_create_003", "endpoint": "collections+create", "type": "type_constraint", "description": "consistencyLevel must be Strong, Session, Bounded, or Eventually", "assertion": "consistencyLevel in ['Strong', 'Session', 'Bounded', 'Eventually']", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "confidence": 1.0, "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}
{"assertion_id": "milvus_behavioral_collections_create_001", "endpoint": "collections+create", "description": "Returns 200 on success, 400 on invalid parameters, 404 if database does not exist", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "confidence": 1.0, "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}
{"assertion_id": "milvus_behavioral_collections_create_001", "endpoint": "collections+create", "description": "Create collection returns 200 on success", "category": "behavioral", "expected_behavior": "returns 200 with code: 0 and empty data object", "confidence": 1.0, "defect_type_if_violated": "Type1_IllegalSuccess", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "doc_version": "2.6.x", "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "milvus_type_collections_create_001", "endpoint": "collections+create", "description": "collectionName must be a string", "assertion": "collectionName is of type string", "type": "type_constraint", "confidence": 1.0, "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "source_status": "reachable", "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "milvus_type_collections_create_003", "endpoint": "collections+create", "description": "consistencyLevel must be Strong, Session, Bounded, or Eventually", "assertion": "consistencyLevel in [Strong, Session, Bounded, Eventually]", "type": "type_constraint", "confidence": 1.0, "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "source_status": "reachable", "source_type": "documentation", "evidence_tier": "inferred_from_behavior"}
VERDICT: UNKNOWN (replay capture — no attack-agent assertion output; raw HTTP only)



--------

## 案 23: qdrant_015

**源码 clone**：`c:\Users\11428\Desktop\testvdb_paper\.sourcedeps\qdrant\v1.18.2`

=== 候选缺陷 qdrant_015 ===
[vendor=qdrant version=1.18.2 defect_type=crash endpoint=collections+{collection_name}]
--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] create with shard_number=INT_MAX -> status=None (read timeout)
- [server_health] GET / after INT_MAX create -> status=200
- [c2] control: create with replication_factor=0 -> status=422, body: replication_factor: value 0 invalid, must be 1 or larger

执行日志全文（output_qdrant_015.log）：
=== REQ 1 ===
DELETE http://localhost:6333/collections/test_shard_max
=== RESP 1 ===
status: 200
body: {"result":false,"status":"ok","time":0.000105154}

=== REQ 2 ===
PUT http://localhost:6333/collections/test_shard_max
payload: {"vectors": {"size": 4, "distance": "Cosine"}, "shard_number": 2147483647}
=== RESP 2 ===
status: None
body: 

=== REQ 3 ===
GET http://localhost:6333/
=== RESP 3 ===
status: None
body: 

=== REQ 4 ===
DELETE http://localhost:6333/collections/test_rep0
=== RESP 4 ===
status: None
body: 

=== REQ 5 ===
PUT http://localhost:6333/collections/test_rep0
payload: {"vectors": {"size": 4, "distance": "Cosine"}, "replication_factor": 0}
=== RESP 5 ===
status: None
body: 

=== REQ 6 ===
DELETE http://localhost:6333/collections/test_shard_max
=== RESP 6 ===
status: 200
body: {"result":false,"status":"ok","time":0.000065359}

=== REQ 7 ===
PUT http://localhost:6333/collections/test_shard_max
payload: {"vectors": {"size": 4, "distance": "Cosine"}, "shard_number": 2147483647}
=== RESP 7 ===
status: None
body: 

=== REQ 8 ===
GET http://localhost:6333/
=== RESP 8 ===
status: None
body: 

=== REQ 9 ===
DELETE http://localhost:6333/collections/test_rep0
=== RESP 9 ===
status: None
body: 

=== REQ 10 ===
PUT http://localhost:6333/collections/test_rep0
payload: {"vectors": {"size": 4, "distance": "Cosine"}, "replication_factor": 0}
=== RESP 10 ===
status: None
body:
--- 契约依据（expected，M3 重建版） ---
{"constraint_id": "qdrant_type_create_collection_001", "endpoint": "collections+{collection_name}", "type": "type_constraint", "description": "collection_name is string", "assertion": "collection_name type is string", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_type_update_collection_002", "endpoint": "collections+{collection_name}", "type": "type_constraint", "description": "All update fields are optional; at least one must be provided", "assertion": "At least one update field must be provided.", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_type_upsert_points_003", "endpoint": "collections+{collection_name}+points", "type": "type_constraint", "description": "id is integer (uint64) or UUID string; vector is array of floats or object of named vectors; payload is key-value object", "assertion": "id type is integer (uint64) or UUID string; vector type is array of floats or object of named vectors; payload type is key-value object.", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_type_overwrite_payload_004", "endpoint": "collections+{collection_name}+points+payload", "type": "type_constraint", "description": "Overwrite replaces entire payload, not merged", "assertion": "PUT payload replaces the entire payload; it does not merge.", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 0.9, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_range_create_collection_001", "endpoint": "collections+{collection_name}", "type": "range_constraint", "description": "shard_number minimum=1", "assertion": "shard_number >= 1", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_range_create_collection_002", "endpoint": "collections+{collection_name}", "type": "range_constraint", "description": "replication_factor minimum=1", "assertion": "replication_factor >= 1", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_range_scroll_points_005", "endpoint": "collections+{collection_name}+points+scroll", "type": "range_constraint", "description": "limit default=10 (adjustable)", "assertion": "limit default=10", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_range_search_points_006", "endpoint": "collections+{collection_name}+points+search", "type": "range_constraint", "description": "hnsw_ef applicable when exact=false", "assertion": "hnsw_ef parameter is applicable only when exact=false.", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 0.9, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_range_search_groups_007", "endpoint": "collections+{collection_name}+points+search+groups", "type": "range_constraint", "description": "group_size >= 1; limit >= 1", "assertion": "group_size >= 1 AND limit >= 1", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_range_query_points_008", "endpoint": "collections+{collection_name}+points+query", "type": "range_constraint", "description": "limit default=10", "assertion": "limit default=10 for query endpoint.", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_range_recommend_009", "endpoint": "collections+{collection_name}+points+recommend", "type": "range_constraint", "description": "strategy must be one of: average_vector, best_score, sum_scores", "assertion": "strategy IN (average_vector, best_score, sum_scores)", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_state_update_collection_002", "endpoint": "collections+{collection_name}", "type": "state_constraint", "description": "Blocking operation - waits for current optimizations to complete", "assertion": "Update blocks until current optimizations complete.", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 0.9, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_state_delete_collection_003", "endpoint": "collections+{collection_name}", "type": "state_constraint", "description": "Destructive operation - permanently deletes collection and all its data", "assertion": "Collection deletion permanently removes the collection and all its data.", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_state_set_payload_006", "endpoint": "collections+{collection_name}+points+payload", "type": "state_constraint", "description": "Atomic - all matched points get the payload", "assertion": "Payload set is atomic: all matched points receive the payload.", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_state_count_points_008", "endpoint": "collections+{collection_name}+points+count", "type": "state_constraint", "description": "exact=true performs full scan; exact=false uses segment statistics", "assertion": "exact=true performs a full scan; exact=false uses segment statistics.", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_state_search_points_009", "endpoint": "collections+{collection_name}+points+search", "type": "state_constraint", "description": "If exact=true, performs brute-force search (slow but accurate); if exact=false, uses HNSW for approximate search", "assertion": "When exact=true, search uses brute-force; when exact=false, search uses HNSW.", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_state_query_points_010", "endpoint": "collections+{collection_name}+points+query", "type": "state_constraint", "description": "prefetch queries execute first, then final query runs on combined results", "assertion": "prefetch queries execute first, then the final query runs on combined results.", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_state_create_index_011", "endpoint": "collections+{collection_name}+index", "type": "state_constraint", "description": "Index creation is async; query optimization applies after index is built", "assertion": "Index creation is asynchronous; query optimization applies after the index is built.", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_state_update_aliases_012", "endpoint": "collections+aliases", "type": "state_constraint", "description": "All alias operations in a single request are applied atomically", "assertion": "All alias operations in a single request are applied atomically.", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"assertion_id": "qdrant_behavioral_003", "endpoint": "collections+{collection_name}", "description": "200 with collection info; 404 if not found", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"assertion_id": "qdrant_behavioral_004", "endpoint": "collections+{collection_name}+exists", "description": "Returns {'result': {'exists': true/false}}", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"assertion_id": "qdrant_behavioral_008", "endpoint": "collections+{collection_name}+points+search", "description": "200 with ranked results descending by score; 4XX on invalid params", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"assertion_id": "qdrant_behavioral_009", "endpoint": "collections+{collection_name}+points+scroll", "description": "200 with points list and next_page_offset for pagination", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"assertion_id": "qdrant_behavioral_010", "endpoint": "collections+{collection_name}+points+count", "description": "200 with count result", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"assertion_id": "qdrant_behavioral_011", "endpoint": "collections+{collection_name}+points+query", "description": "200 with result points; supports multi-stage query pipeline via prefetch", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"assertion_id": "qdrant_behavioral_017", "endpoint": "collections", "description": "200 with list of collections", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"endpoint": "collections+{collection_name}", "kind": "range_constraints", "description": "shard_number minimum=1", "assertion": "shard_number >= 1", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"endpoint": "collections+{collection_name}", "kind": "range_constraints", "description": "replication_factor minimum=1", "assertion": "replication_factor >= 1", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"endpoint": "collections+{collection_name}", "kind": "range_constraints", "description": "timeout minimum=1", "assertion": "timeout >= 1", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"endpoint": "collections+{collection_name}", "kind": "state_constraints", "description": "Atomic collection creation: after 200 response, collection is fully initialized and ready for operations", "assertion": "Atomic collection creation. After 200 response, collection is fully initialized and ready for operations.", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "confidence": 1.0, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "qdrant_range_create_collection_002", "endpoint": "collections+{collection_name}", "description": "replication_factor minimum=1", "assertion": "replication_factor >= 1", "type": "range_constraint", "confidence": 1.0, "evidence_tier": "inferred_from_behavior", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "source_status": "reachable", "doc_version": "1.18.x", "source_verified": true, "source_type": "structured-spec"}
{"constraint_id": "qdrant_range_create_collection_001", "endpoint": "collections+{collection_name}", "description": "shard_number minimum=1", "assertion": "shard_number >= 1", "type": "range_constraint", "confidence": 1.0, "evidence_tier": "inferred_from_behavior", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "source_status": "reachable", "doc_version": "1.18.x", "source_verified": true, "source_type": "structured-spec"}
{"constraint_id": "qdrant_range_search_groups_007", "endpoint": "collections+{collection_name}+points+search+groups", "description": "group_size >= 1; limit >= 1", "assertion": "group_size >= 1 AND limit >= 1", "type": "range_constraint", "confidence": 1.0, "evidence_tier": "inferred_from_behavior", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "source_status": "reachable", "doc_version": "1.18.x", "source_verified": true, "source_type": "structured-spec"}
{"constraint_id": "qdrant_type_upsert_points_003", "endpoint": "collections+{collection_name}+points", "description": "id is integer (uint64) or UUID string; vector is array of floats or object of named vectors; payload is key-value object", "assertion": "id type is integer (uint64) or UUID string; vector type is array of floats or object of named vectors; payload type is key-value object.", "type": "type_constraint", "confidence": 1.0, "evidence_tier": "inferred_from_behavior", "source_url": "https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json", "source_status": "reachable", "doc_version": "1.18.x", "source_verified": true, "source_type": "structured-spec"}



--------

## 案 24: weaviate_003

**源码 clone**：`c:\Users\11428\Desktop\testvdb_paper\.sourcedeps\weaviate\v1.37.4`

=== 候选缺陷 weaviate_003 ===
[vendor=weaviate version=1.37.4 defect_type=param_validation endpoint=/schema]
--- 观察到的行为（observed） ---

执行日志全文（output_weaviate_003.log）：
=== REQ 1 ===
DELETE http://localhost:18080/v1/schema/TestRep
=== RESP 1 ===
status: 200
body: 

=== REQ 2 ===
POST http://localhost:18080/v1/schema
payload: {"class": "TestRep", "vectorizer": "none", "replicationConfig": {"factor": -1}, "vectorIndexConfig": {"distance": "cosine"}, "properties": [{"name": "text", "dataType": ["text"]}]}
=== RESP 2 ===
status: 200
body: {"class":"TestRep","invertedIndexConfig":{"bm25":{"b":0.75,"k1":1.2},"cleanupIntervalSeconds":60,"stopwords":{"additions":null,"preset":"en","removals":null},"usingBlockMaxWAND":true},"multiTenancyConfig":{"autoTenantActivation":false,"autoTenantCreation":false,"enabled":false},"properties":[{"dataType":["text"],"indexFilterable":true,"indexRangeFilters":false,"indexSearchable":true,"name":"text","tokenization":"word"}],"replicationConfig":{"asyncEnabled":false,"deletionStrategy":"TimeBasedResolution","factor":1},"shardingConfig":{"virtualPerPhysical":128,"desiredCount":1,"actualCount":1,"desiredVirtualCount":128,"actualVirtualCount":128,"key":"_id","strategy":"hash","function":"murmur3"},"vectorIndexConfig":{"skip":false,"cleanupIntervalSeconds":300,"maxConnections":32,"efConstruction":128,"ef":-1,"dynamicEfMin":100,"dynamicEfMax":500,"dynamicEfFactor":8,"vectorCacheMaxObjects":1000000000000,"flatSearchCutoff":40000,"distance":"cosine","pq":{"enabled":false,"bitCompression":false,"segments":0,"centroids":256,"trainingLimit":100000,"encoder":{"type":"kmeans","distribution":"log-normal"}},"bq":{"enabled":false},"sq":{"enabled":false,"trainingLimit":100000,"rescoreLimit":20},"rq":{"enabled":false,"bits":8,"rescoreLimit":20},"filterStrategy":"acorn","multivector":{"enabled":false,"muvera":{"enabled":false,"ksim":4,"dprojections":16,"repetitions":10},"aggregation":"maxSim"},"skipDefaultQuantization":false,"trackDefaultQuantization":false},"vectorIndexType":"hnsw","vectorizer":"none"}


=== REQ 3 ===
GET http://localhost:18080/v1/schema/TestRep
=== RESP 3 ===
status: 200
body: {"class":"TestRep","invertedIndexConfig":{"bm25":{"b":0.75,"k1":1.2},"cleanupIntervalSeconds":60,"stopwords":{"additions":null,"preset":"en","removals":null},"usingBlockMaxWAND":true},"multiTenancyConfig":{"autoTenantActivation":false,"autoTenantCreation":false,"enabled":false},"properties":[{"dataType":["text"],"indexFilterable":true,"indexRangeFilters":false,"indexSearchable":true,"name":"text","tokenization":"word"}],"replicationConfig":{"asyncEnabled":false,"deletionStrategy":"TimeBasedResolution","factor":1},"shardingConfig":{"actualCount":1,"actualVirtualCount":128,"desiredCount":1,"desiredVirtualCount":128,"function":"murmur3","key":"_id","strategy":"hash","virtualPerPhysical":128},"vectorIndexConfig":{"bq":{"enabled":false},"cleanupIntervalSeconds":300,"distance":"cosine","dynamicEfFactor":8,"dynamicEfMax":500,"dynamicEfMin":100,"ef":-1,"efConstruction":128,"filterStrategy":"acorn","flatSearchCutoff":40000,"maxConnections":32,"multivector":{"aggregation":"maxSim","enabled":false,"muvera":{"dprojections":16,"enabled":false,"ksim":4,"repetitions":10}},"pq":{"bitCompression":false,"centroids":256,"enabled":false,"encoder":{"distribution":"log-normal","type":"kmeans"},"segments":0,"trainingLimit":100000},"rq":{"bits":8,"enabled":false,"rescoreLimit":20},"skip":false,"skipDefaultQuantization":false,"sq":{"enabled":false,"rescoreLimit":20,"trainingLimit":100000},"trackDefaultQuantization":false,"vectorCacheMaxObjects":1000000000000},"vectorIndexType":"hnsw","vectorizer":"none"}
--- 契约依据（expected，M3 重建版） ---
{"constraint_id": "weaviate_type_schema_create_001", "endpoint": "/schema POST", "type": "type_constraint", "description": "class field must be CamelCase", "assertion": "properties.class matches /^[A-Z][a-zA-Z0-9]*$/", "source_url": "https://github.com/weaviate/weaviate/blob/v1.37.4/openapi-specs/schema.json", "confidence": 0.95, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "weaviate_type_schema_create_002", "endpoint": "/schema POST", "type": "type_constraint", "description": "vectorIndexType must be one of allowed index types", "assertion": "properties.vectorIndexType in {hnsw, flat, dynamic, bwes}", "source_url": "https://github.com/weaviate/weaviate/blob/v1.37.4/openapi-specs/schema.json", "confidence": 0.95, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "weaviate_type_schema_create_003", "endpoint": "/schema POST", "type": "type_constraint", "description": "properties[].tokenization must be a valid enum value", "assertion": "properties.properties[].tokenization in {word, lowercase, whitespace, field, trigram, gse, kagome_kr, kagome_ja, gse_ch}", "source_url": "https://github.com/weaviate/weaviate/blob/v1.37.4/openapi-specs/schema.json", "confidence": 0.95, "source_type": "structured-spec", "evidence_tier": "explicit"}
{"constraint_id": "weaviate_type_tenants_create_001", "endpoint": "/schema/{className}/tenants POST", "type": "type_constraint", "description": "Tenant.activityStatus on create must be ACTIVE or INACTIVE", "assertion": "body[].activityStatus in {ACTIVE, INACTIVE}", "source_url": "https://github.com/weaviate/weaviate/blob/v1.37.4/openapi-specs/schema.json", "confidence": 0.95, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "weaviate_type_tenants_update_001", "endpoint": "/schema/{className}/tenants PUT", "type": "type_constraint", "description": "Tenant.activityStatus on update must be ACTIVE, INACTIVE, or OFFLOADED", "assertion": "body[].activityStatus in {ACTIVE, INACTIVE, OFFLOADED}", "source_url": "https://github.com/weaviate/weaviate/blob/v1.37.4/openapi-specs/schema.json", "confidence": 0.95, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "weaviate_type_index_update_001", "endpoint": "/schema/{className}/indexes/{propertyName} PUT", "type": "type_constraint", "description": "searchable.algorithm must be blockmax (WAND->BlockMax migration only; downgrade rejected)", "assertion": "body.searchable.algorithm == 'blockmax'", "source_url": "https://github.com/weaviate/weaviate/blob/v1.37.4/openapi-specs/schema.json", "confidence": 0.9, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "weaviate_range_schema_replication_001", "endpoint": "/schema POST", "type": "range_constraint", "description": "replicationConfig.factor is an integer (default 1)", "assertion": "replicationConfig.factor >= 1", "source_url": "https://github.com/weaviate/weaviate/blob/v1.37.4/openapi-specs/schema.json", "confidence": 0.85, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "weaviate_state_schema_delete_001", "endpoint": "/schema/{className} DELETE", "type": "state_constraint", "description": "deleting a collection permanently deletes all data objects in the collection", "assertion": "after DELETE /schema/{className}, GET /objects?class={className} returns empty", "source_url": "https://github.com/weaviate/weaviate/blob/v1.37.4/openapi-specs/schema.json", "confidence": 0.95, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "weaviate_state_tenants_delete_001", "endpoint": "/schema/{className}/tenants DELETE", "type": "state_constraint", "description": "deleting tenants permanently deletes all tenant data", "assertion": "after DELETE tenants, GET tenant returns 404 and its data is gone", "source_url": "https://github.com/weaviate/weaviate/blob/v1.37.4/openapi-specs/schema.json", "confidence": 0.9, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "weaviate_state_schema_update_001", "endpoint": "/schema/{className} PUT", "type": "state_constraint", "description": "PUT does NOT add properties (use POST /schema/{className}/properties) and does NOT rename", "assertion": "PUT /schema/{className} does not change properties count or names", "source_url": "https://github.com/weaviate/weaviate/blob/v1.37.4/openapi-specs/schema.json", "confidence": 0.9, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"assertion_id": "weaviate_behavioral_schema_create_001", "endpoint": "/schema POST", "description": "creating collection with disallowed vectorIndexType returns 422 RestrictionViolationResponse", "source_url": "https://github.com/weaviate/weaviate/blob/v1.37.4/openapi-specs/schema.json", "confidence": 0.95, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"assertion_id": "weaviate_behavioral_schema_create_002", "endpoint": "/schema POST", "description": "exceeding collections/shards usage limit returns 429 UsageLimitExceededResponse", "source_url": "https://github.com/weaviate/weaviate/blob/v1.37.4/openapi-specs/schema.json", "confidence": 0.95, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"assertion_id": "weaviate_behavioral_tenants_create_001", "endpoint": "/schema/{className}/tenants POST", "description": "exceeding tenant usage limit returns 429 with limit: tenants", "source_url": "https://github.com/weaviate/weaviate/blob/v1.37.4/openapi-specs/schema.json", "confidence": 0.95, "source_type": "structured-spec", "evidence_tier": "inferred_from_behavior"}
{"constraint_id": "weaviate_range_schema_replication_001", "endpoint": "/schema POST", "description": "replicationConfig.factor is an integer (default 1)", "assertion": "replicationConfig.factor >= 1", "type": "range_constraint", "confidence": 0.85, "evidence_tier": "inferred_from_behavior", "source_url": "https://github.com/weaviate/weaviate/blob/v1.37.4/openapi-specs/schema.json", "source_status": "reachable", "source_type": "structured-spec"}
{"constraint_id": "weaviate_type_schema_create_001", "endpoint": "/schema POST", "description": "class field must be CamelCase", "assertion": "properties.class matches /^[A-Z][a-zA-Z0-9]*$/", "type": "type_constraint", "confidence": 0.95, "evidence_tier": "inferred_from_behavior", "source_url": "https://github.com/weaviate/weaviate/blob/v1.37.4/openapi-specs/schema.json", "source_status": "reachable", "source_type": "structured-spec"}
{"constraint_id": "weaviate_type_schema_create_002", "endpoint": "/schema POST", "description": "vectorIndexType must be one of allowed index types", "assertion": "properties.vectorIndexType in {hnsw, flat, dynamic, bwes}", "type": "type_constraint", "confidence": 0.95, "evidence_tier": "inferred_from_behavior", "source_url": "https://github.com/weaviate/weaviate/blob/v1.37.4/openapi-specs/schema.json", "source_status": "reachable", "source_type": "structured-spec"}
{"constraint_id": "weaviate_type_schema_create_003", "endpoint": "/schema POST", "description": "properties[].tokenization must be a valid enum value", "assertion": "properties.properties[].tokenization in {word, lowercase, whitespace, field, trigram, gse, kagome_kr, kagome_ja, gse_ch}", "type": "type_constraint", "confidence": 0.95, "evidence_tier": "explicit", "source_url": "https://github.com/weaviate/weaviate/blob/v1.37.4/openapi-specs/schema.json", "source_status": "reachable", "source_type": "structured-spec"}
{"constraint_id": "weaviate_state_schema_update_001", "endpoint": "/schema/{className} PUT", "description": "PUT does NOT add properties (use POST /schema/{className}/properties) and does NOT rename", "assertion": "PUT /schema/{className} does not change properties count or names", "type": "state_constraint", "confidence": 0.9, "evidence_tier": "inferred_from_behavior", "source_url": "https://github.com/weaviate/weaviate/blob/v1.37.4/openapi-specs/schema.json", "source_status": "reachable", "source_type": "structured-spec"}
{"constraint_id": "weaviate_type_tenants_create_001", "endpoint": "/schema/{className}/tenants POST", "description": "Tenant.activityStatus on create must be ACTIVE or INACTIVE", "assertion": "body[].activityStatus in {ACTIVE, INACTIVE}", "type": "type_constraint", "confidence": 0.95, "evidence_tier": "inferred_from_behavior", "source_url": "https://github.com/weaviate/weaviate/blob/v1.37.4/openapi-specs/schema.json", "source_status": "reachable", "source_type": "structured-spec"}
{"constraint_id": "weaviate_type_tenants_update_001", "endpoint": "/schema/{className}/tenants PUT", "description": "Tenant.activityStatus on update must be ACTIVE, INACTIVE, or OFFLOADED", "assertion": "body[].activityStatus in {ACTIVE, INACTIVE, OFFLOADED}", "type": "type_constraint", "confidence": 0.95, "evidence_tier": "inferred_from_behavior", "source_url": "https://github.com/weaviate/weaviate/blob/v1.37.4/openapi-specs/schema.json", "source_status": "reachable", "source_type": "structured-spec"}



--------

## 案 25: milvus_031

**源码 clone**：`c:\Users\11428\Desktop\testvdb_paper\.sourcedeps\milvus\v2.6.17`

=== 候选缺陷 milvus_031 ===
[vendor=milvus version=2.6.17 defect_type=behavior endpoint=entities+upsert]
--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] upsert without PK on autoID collection -> http=200, code=1804
- [c2] control: insert without PK -> http=200, code=1804

执行日志全文（output_milvus_031.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_upsert_autoid", "dbName": "default"}
=== RESP 1 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_upsert_autoid", "dimension": 4, "metricType": "L2", "autoID": true, "schema": {"autoID": true, "primaryFieldName": "id", "fields": [{"fieldName": "id", "dataType": "Int64", "isPrimary": true}, {"fieldName": "vector", "dataType": "FloatVector", "elementTypeParams": {"dim": 4}}]}}
=== RESP 2 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/entities/upsert
payload: {"collectionName": "test_upsert_autoid", "data": [{"vector": [1.0, 2.0, 3.0, 4.0], "color": "red"}]}
=== RESP 3 ===
status: 200
body: {"code":1804,"message":"fail to deal the insert data, error: has pass more field without dynamic schema, please check it: invalid parameter"}

=== REQ 4 ===
POST http://localhost:19530/v2/vectordb/entities/insert
payload: {"collectionName": "test_upsert_autoid", "data": [{"vector": [5.0, 6.0, 7.0, 8.0], "color": "blue"}]}
=== RESP 4 ===
status: 200
body: {"code":1804,"message":"fail to deal the insert data, error: has pass more field without dynamic schema, please check it: invalid parameter"}
--- 契约依据（expected，M3 重建版） ---
[经端点过滤与依据核查后，无 endpoint=entities+upsert 的可核查约束行]

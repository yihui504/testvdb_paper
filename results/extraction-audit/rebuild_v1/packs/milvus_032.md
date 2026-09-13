=== 候选缺陷 milvus_032 ===
[vendor=milvus version=2.6.19 defect_type=semantics endpoint=collections+create]
--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] create with consistencyLevel=Invalid -> http=200, code=0
- [c1_rb] describe collection -> http=200, code=0, consistencyLevel=Bounded

执行日志全文（output_milvus_032.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "audit1", "dbName": "default"}
=== RESP 1 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "audit1", "dimension": 4, "metricType": "L2", "idType": "Int64", "autoID": true, "vectorFieldType": "FloatVector", "consistencyLevel": "Invalid"}
=== RESP 2 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/collections/describe
payload: {"collectionName": "audit1", "dbName": "default"}
=== RESP 3 ===
status: 200
body: {"code":0,"data":{"aliases":[],"autoId":true,"collectionID":468359343909110777,"collectionName":"audit1","consistencyLevel":"Bounded","description":"","enableDynamicField":true,"fields":[{"autoId":true,"clusteringKey":false,"description":"","id":100,"name":"id","nullable":false,"partitionKey":false,"primaryKey":true,"type":"Int64"},{"autoId":false,"clusteringKey":false,"description":"","id":101,"name":"vector","nullable":false,"params":[{"key":"dim","value":"4"}],"partitionKey":false,"primaryKey":false,"type":"FloatVector"}],"functions":[],"indexes":[{"fieldName":"vector","indexName":"vector","metricType":"L2"}],"load":"LoadStateLoading","partitionsNum":1,"properties":[{"key":"timezone","value":"UTC"}],"shardsNum":1},"message":""}

--- 契约依据（expected，M1 过滤后初稿） ---
约束条目（8 条，来自 milvus 2.6.19 契约，endpoint=collections+create）：
{"constraint_id": "milvus_type_collections_create_001", "endpoint": "collections+create", "type": "type_constraint", "description": "collectionName must be a string", "assertion": "typeof collectionName === 'string'", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "confidence": 1.0, "_audit": {"g1": "aligned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["collectionName"], "priority": "bulk"}}
{"constraint_id": "milvus_type_collections_create_002", "endpoint": "collections+create", "type": "type_constraint", "description": "metricType must be L2, IP, or COSINE", "assertion": "metricType in ['L2', 'IP', 'COSINE']", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "confidence": 1.0, "_audit": {"g1": "aligned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["COSINE", "metricType"], "priority": "bulk"}}
{"constraint_id": "milvus_type_collections_create_003", "endpoint": "collections+create", "type": "type_constraint", "description": "consistencyLevel must be Strong, Session, Bounded, or Eventually", "assertion": "consistencyLevel in ['Strong', 'Session', 'Bounded', 'Eventually']", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "confidence": 1.0, "_audit": {"g1": "aligned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["Bounded", "Eventually", "Session", "Strong", "consistencyLevel"], "priority": "bulk"}}
{"constraint_id": "milvus_range_collections_create_001", "endpoint": "collections+create", "type": "range_constraint", "description": "dimension must be between 1 and 32768 for FloatVector", "assertion": "dimension >= 1 && dimension <= 32768", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "confidence": 1.0, "_audit": {"g1": "aligned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["FloatVector", "dimension"], "priority": "bulk"}}
{"constraint_id": "milvus_range_collections_create_002", "endpoint": "collections+create", "type": "range_constraint", "description": "shardsNum must be >= 1", "assertion": "shardsNum >= 1", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "confidence": 1.0, "_audit": {"g1": "aligned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["shardsNum"], "priority": "bulk"}}
{"constraint_id": "milvus_range_collections_create_003", "endpoint": "collections+create", "type": "range_constraint", "description": "VarChar max_length must be between 1 and 65535", "assertion": "max_length >= 1 && max_length <= 65535", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "confidence": 1.0, "_audit": {"g1": "aligned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["VarChar", "max_length"], "priority": "bulk"}}
{"constraint_id": "milvus_state_collections_create_001", "endpoint": "collections+create", "type": "state_constraint", "description": "Collection creation is atomic; collection names are unique within a database, and re-creation is idempotent when the schema is unchanged", "assertion": "collection creation is atomic AND collectionName is unique within dbName; re-creating an existing collection with the SAME schema is an idempotent no-op returning 200, re-creating with a DIFFERENT schema returns an error", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "confidence": 1.0, "_audit": {"g1": "aligned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["AND", "Collection", "are", "collectionName", "database", "dbName", "error", "names", "schema", "when"], "priority": "bulk"}}
{"assertion_id": "milvus_behavioral_collections_create_001", "endpoint": "collections+create", "description": "Returns 200 on success, 400 on invalid parameters, 404 if database does not exist", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "confidence": 1.0, "_audit": {"g1": "aligned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["database", "not", "parameters"], "priority": "bulk"}}
相关契约段（关键词定位 1 条）：
{"endpoint": "collections+create", "kind": "type_constraints", "description": "consistencyLevel must be Strong, Session, Bounded, or Eventually", "assertion": "consistencyLevel in ['Strong', 'Session', 'Bounded', 'Eventually']", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "confidence": 1.0, "_audit": {"g1": "NO_VC_ROW", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["Bounded", "Eventually", "Session", "Strong", "consistencyLevel"], "priority": "bulk"}}
--- 补充契约行（M1 端点过滤后） ---
{"assertion_id": "milvus_behavioral_collections_create_001", "endpoint": "collections+create", "description": "Create collection returns 200 on success", "category": "behavioral", "expected_behavior": "returns 200 with code: 0 and empty data object", "confidence": 1.0, "defect_type_if_violated": "Type1_IllegalSuccess", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "doc_version": "2.6.x", "_audit": {"g1": "aligned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["Create", "code", "object"], "priority": "bulk"}}
{"constraint_id": "milvus_type_collections_create_001", "endpoint": "collections+create", "description": "collectionName must be a string", "assertion": "collectionName is of type string", "type": "type_constraint", "confidence": 1.0, "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "source_status": "reachable", "_audit": {"g1": "aligned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["collectionName"], "priority": "bulk"}}
{"constraint_id": "milvus_state_collections_create_001", "endpoint": "collections+create", "description": "Collection creation is atomic; collection name must be unique within a database", "assertion": "collection creation is atomic AND collectionName is unique within dbName", "type": "state_constraint", "confidence": 1.0, "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "source_status": "reachable", "_audit": {"g1": "aligned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["AND", "Collection", "collectionName", "database", "dbName", "name"], "priority": "bulk"}}
{"constraint_id": "milvus_type_collections_create_003", "endpoint": "collections+create", "description": "consistencyLevel must be Strong, Session, Bounded, or Eventually", "assertion": "consistencyLevel in [Strong, Session, Bounded, Eventually]", "type": "type_constraint", "confidence": 1.0, "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "source_status": "reachable", "_audit": {"g1": "aligned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["Bounded", "Eventually", "Session", "Strong", "consistencyLevel"], "priority": "bulk"}}
--- 维护者态度参考（developer_cognition，vendor=milvus） ---
以下为该 vendor 维护者在历史 issue 中对同类现象的明确 by-design 表态（供判定参考；与本案是否相关由你判断）：
- [相关 issues: [50192]] Concurrent rename+create idempotent semantics: rename(dst) racing with create(dst) both returning success is tolerated—rename to an existing-name target is treated as idempotent no-op when parameters match（维护者原话: "sounds like a by designed. Milvus returns success if creating a collection with the same name and parameters."）
- [相关 issues: [50193]] get_stats rowCount reflects flushed data only: rowCount=0 after insert before flush is expected (query returns full rows; stats lag by design)（维护者原话: "This is by design. The entities number in collection stats only shows the data that flushed. Please retry with flush() after insert()."）
- [相关 issues: [50319]] REST v2 quick-create mode semantics: creating via quick/fast mode (dimension-only) auto-loads and does not enforce full schema/load-state checks; search on such collections succeeding is expected（维护者原话: "The behavior described here appears to come from REST v2 quick/fast collection creation mode, not from search/query bypassing the collection load-stat"）
- [相关 issues: [50351]] REST v2 create ignores unconsumed top-level fields: params not consumed by quick-create (e.g. top-level shardsNum) are silently ignored rather than rejected; consumed via params.shardsNum（维护者原话: "I think this is by design. The payload in this issue uses top-level shardsNum, but this field is not consumed by the REST v2 create API. shardsNum is "）

VERDICT: UNKNOWN (replay capture — no attack-agent assertion output; raw HTTP only)


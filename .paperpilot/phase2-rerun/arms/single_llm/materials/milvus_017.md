=== 候选缺陷 milvus_017 ===
[vendor=milvus version=2.6.16 defect_type=param_validation endpoint=aliases+list]

--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] aliases/list with collectionName empty -> http=200, code=0
- [c2] control: collections/describe with empty name -> http=200, code=1802

执行日志全文（output_milvus_017.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_aliases", "dbName": "default"}
=== RESP 1 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_aliases", "dimension": 4, "metricType": "L2"}
=== RESP 2 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/aliases/create
payload: {"collectionName": "test_aliases", "alias": "alias_<tracked>", "dbName": "default"}
=== RESP 3 ===
status: 200
body: {"code":1802,"message":"missing required parameters, error: Key: 'AliasCollectionReq.AliasName' Error:Field validation for 'AliasName' failed on the 'required' tag"}

=== REQ 4 ===
POST http://localhost:19530/v2/vectordb/aliases/list
payload: {"collectionName": "", "dbName": "default"}
=== RESP 4 ===
status: 200
body: {"code":0,"data":[]}

=== REQ 5 ===
POST http://localhost:19530/v2/vectordb/collections/describe
payload: {"collectionName": "", "dbName": "default"}
=== RESP 5 ===
status: 200
body: {"code":1802,"message":"missing required parameters, error: Key: 'CollectionNameReq.CollectionName' Error:Field validation for 'CollectionName' failed on the 'required' tag"}

=== REQ 6 ===
POST http://localhost:19530/v2/vectordb/collections/drop
payload: {"collectionName": "test_aliases", "dbName": "default"}
=== RESP 6 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 7 ===
POST http://localhost:19530/v2/vectordb/collections/create
payload: {"collectionName": "test_aliases", "dimension": 4, "metricType": "L2"}
=== RESP 7 ===
status: 200
body: {"code":0,"data":{}}

=== REQ 8 ===
POST http://localhost:19530/v2/vectordb/aliases/create
payload: {"collectionName": "test_aliases", "alias": "alias_<tracked>", "dbName": "default"}
=== RESP 8 ===
status: 200
body: {"code":1802,"message":"missing required parameters, error: Key: 'AliasCollectionReq.AliasName' Error:Field validation for 'AliasName' failed on the 'required' tag"}

=== REQ 9 ===
POST http://localhost:19530/v2/vectordb/aliases/list
payload: {"collectionName": "", "dbName": "default"}
=== RESP 9 ===
status: 200
body: {"code":0,"data":[]}

=== REQ 10 ===
POST http://localhost:19530/v2/vectordb/collections/describe
payload: {"collectionName": "", "dbName": "default"}
=== RESP 10 ===
status: 200
body: {"code":1802,"message":"missing required parameters, error: Key: 'CollectionNameReq.CollectionName' Error:Field validation for 'CollectionName' failed on the 'required' tag"}



--- 契约依据（expected，来自该版本 API 契约） ---
[契约中无 endpoint=aliases+list 的约束条目]

相关契约段（关键词定位 4 条）：
{"endpoint": "collections+drop", "kind": "type_constraints", "description": "collectionName must be a non-empty string", "assertion": "collectionName is non-empty string", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Drop.md", "confidence": 1.0}
{"endpoint": "collections+load", "kind": "type_constraints", "description": "collectionName must be a non-empty string for load", "assertion": "collectionName is non-empty string", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Load.md", "confidence": 1.0}
{"endpoint": "collections+rename", "kind": "type_constraints", "description": "collectionName and newCollectionName must be non-empty strings", "assertion": "collectionName is non-empty string AND newCollectionName is non-empty string", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Rename.md", "confidence": 1.0}
{"endpoint": "collections+create", "kind": "type_constraints", "description": "collectionName must be a string", "assertion": "collectionName is of type string", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md", "confidence": 1.0}

API 模板：endpoint=aliases+list doc_quote='200 with list of aliases' source=None

VERDICT: UNKNOWN (replay capture — no attack-agent assertion output; raw HTTP only)

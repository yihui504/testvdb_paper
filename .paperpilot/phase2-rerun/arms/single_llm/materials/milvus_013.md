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



--- 契约依据（expected，来自该版本 API 契约） ---
[契约中无 endpoint=collections+list 的约束条目]

相关契约段（关键词定位 4 条）：
{"endpoint": "collections+drop", "kind": "type_constraints", "description": "collectionName must be a non-empty string", "assertion": "collectionName is non-empty string", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Drop.md", "confidence": 1.0}
{"endpoint": "collections+load", "kind": "type_constraints", "description": "collectionName must be a non-empty string for load", "assertion": "collectionName is non-empty string", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Load.md", "confidence": 1.0}
{"endpoint": "collections+rename", "kind": "type_constraints", "description": "collectionName and newCollectionName must be non-empty strings", "assertion": "collectionName is non-empty string AND newCollectionName is non-empty string", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Rename.md", "confidence": 1.0}
{"endpoint": "partitions+create", "kind": "type_constraints", "description": "partitionName must be a non-empty string", "assertion": "partitionName is non-empty string", "source_url": "https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go", "confidence": 1.0}

VERDICT: UNKNOWN (replay capture — no attack-agent assertion output; raw HTTP only)

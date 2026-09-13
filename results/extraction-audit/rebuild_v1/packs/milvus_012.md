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

--- 契约依据（expected，M1 过滤后初稿） ---
[经端点过滤后无相关契约行；需人工考古 endpoint=collections+list]
[契约中无 endpoint=collections+list 的约束条目]
相关契约段（关键词定位 4 条）：
API 模板：endpoint=collections+create doc_quote='200 on success; 400 on invalid parameters; 404 if database does not exist' source=None
VERDICT: UNKNOWN (replay capture — no attack-agent assertion output; raw HTTP only)

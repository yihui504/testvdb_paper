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

--- 契约依据（expected，M1 过滤后初稿） ---
[经端点过滤后无相关契约行；需人工考古 endpoint=collections+list]
[契约中无 endpoint=collections+list 的约束条目]
相关契约段（关键词定位 4 条）：
--- 契约依据·主断言（M1，_provenance 已剥） ---
{"constraint_id": "milvus_type_request_timeout_001", "endpoint": "entities+query", "description": "Request-Timeout header must be an integer", "assertion": "header Request-Timeout matches ^[0-9]+$ (non-integer rejected)", "type": "state_constraint", "evidence_tier": "explicit", "source_url": "https://milvus.io/api-reference/restful/v2.3.x/v2/Vector%20(v2)/Query.md", "_audit": {"g1": "MISMATCH", "g2": "DEAD_LINK", "issue_no": false, "page": "none", "kw_hits": [], "priority": "main"}}
VERDICT: UNKNOWN (replay capture — no attack-agent assertion output; raw HTTP only)

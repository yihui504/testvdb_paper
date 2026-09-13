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

--- 契约依据（expected，M1 过滤后初稿） ---
约束条目（3 条，来自 milvus 2.6.17 契约，endpoint=users+create）：
{"constraint_id": "milvus_type_users_create_001", "endpoint": "users+create", "type": "type_constraint", "description": "userName must be a non-empty string", "assertion": "userName is non-empty string", "source_url": "https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go", "confidence": 1.0, "_audit": {"g1": "aligned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["userName"], "priority": "bulk"}}
{"constraint_id": "milvus_range_users_create_001", "endpoint": "users+create", "type": "range_constraint", "description": "password must be 8-64 characters", "assertion": "8 <= len(password) <= 64", "source_url": "https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go", "confidence": 1.0, "_audit": {"g1": "aligned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["len", "password"], "priority": "bulk"}}
{"assertion_id": "milvus_behavioral_users_create_001", "endpoint": "users+create", "description": "Create user returns 400 if password too weak or user already exists", "source_url": "https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go", "confidence": 1.0, "_audit": {"g1": "aligned", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["Create", "password", "user"], "priority": "bulk"}}
相关契约段（关键词定位 4 条）：
{"endpoint": "users+create", "kind": "range_constraints", "description": "password must be 8-64 characters", "assertion": "8 <= len(password) <= 64", "source_url": "https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go", "confidence": 1.0, "_audit": {"g1": "NO_VC_ROW", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["len", "password"], "priority": "bulk"}}
{"endpoint": "users+create", "kind": "assertion", "description": "Create user returns 400 if password too weak or user already exists", "source_url": "https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go", "confidence": 1.0, "_audit": {"g1": "NO_VC_ROW", "g2": "OK", "issue_no": false, "page": "text", "kw_hits": ["Create", "password", "user"], "priority": "bulk"}}
API 模板：endpoint=users+create doc_quote='200 on success; 400 if user already exists or password too weak' source=None
VERDICT: UNKNOWN (replay capture — no attack-agent assertion output; raw HTTP only)

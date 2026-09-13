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

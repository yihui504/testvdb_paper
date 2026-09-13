=== 候选缺陷 milvus_041 ===
[vendor=milvus version=3.0.0 defect_type=type_coercion endpoint=entities+upsert]
--- 观察到的行为（observed） ---
观察摘要（probe 产出）：
- [c1] REST upsert string into DOUBLE field -> http=200, code=0
- [c2] REST upsert string 'true' into BOOL field -> http=200, code=0
- [c3] REST upsert int 1 into BOOL field -> http=200, code=0
- [c4] REST upsert string '42' into INT16 field -> http=200, code=0

执行日志全文（output_milvus_041.log）：
=== REQ 1 ===
POST http://localhost:19530/v2/vectordb/entities/upsert
payload: {"collectionName": "test_upsert_scalar", "data": [{"id": 0, "vector": [0.9, 0.9, 0.9, 0.9], "dbl_f": "3.14159"}]}
=== RESP 1 ===
status: 200
body: {"code":0,"cost":0,"data":{"upsertCount":1,"upsertIds":[0]}}

=== REQ 2 ===
POST http://localhost:19530/v2/vectordb/entities/upsert
payload: {"collectionName": "test_upsert_scalar", "data": [{"id": 0, "vector": [0.9, 0.9, 0.9, 0.9], "bool_f": "true"}]}
=== RESP 2 ===
status: 200
body: {"code":0,"cost":0,"data":{"upsertCount":1,"upsertIds":[0]}}

=== REQ 3 ===
POST http://localhost:19530/v2/vectordb/entities/upsert
payload: {"collectionName": "test_upsert_scalar", "data": [{"id": 0, "vector": [0.9, 0.9, 0.9, 0.9], "bool_f": 1}]}
=== RESP 3 ===
status: 200
body: {"code":0,"cost":0,"data":{"upsertCount":1,"upsertIds":[0]}}

=== REQ 4 ===
POST http://localhost:19530/v2/vectordb/entities/upsert
payload: {"collectionName": "test_upsert_scalar", "data": [{"id": 0, "vector": [0.9, 0.9, 0.9, 0.9], "i16_f": "42"}]}
=== RESP 4 ===
status: 200
body: {"code":0,"cost":0,"data":{"upsertCount":1,"upsertIds":[0]}}

=== REQ 5 ===
POST http://localhost:19530/v2/vectordb/entities/upsert
payload: {"collectionName": "test_upsert_scalar", "data": [{"id": 0, "vector": [0.9, 0.9, 0.9, 0.9], "dbl_f": "3.14159"}]}
=== RESP 5 ===
status: 200
body: {"code":0,"cost":0,"data":{"upsertCount":1,"upsertIds":[0]}}

=== REQ 6 ===
POST http://localhost:19530/v2/vectordb/entities/upsert
payload: {"collectionName": "test_upsert_scalar", "data": [{"id": 0, "vector": [0.9, 0.9, 0.9, 0.9], "bool_f": "true"}]}
=== RESP 6 ===
status: 200
body: {"code":0,"cost":0,"data":{"upsertCount":1,"upsertIds":[0]}}

=== REQ 7 ===
POST http://localhost:19530/v2/vectordb/entities/upsert
payload: {"collectionName": "test_upsert_scalar", "data": [{"id": 0, "vector": [0.9, 0.9, 0.9, 0.9], "bool_f": 1}]}
=== RESP 7 ===
status: 200
body: {"code":0,"cost":0,"data":{"upsertCount":1,"upsertIds":[0]}}

=== REQ 8 ===
POST http://localhost:19530/v2/vectordb/entities/upsert
payload: {"collectionName": "test_upsert_scalar", "data": [{"id": 0, "vector": [0.9, 0.9, 0.9, 0.9], "i16_f": "42"}]}
=== RESP 8 ===
status: 200
body: {"code":0,"cost":0,"data":{"upsertCount":1,"upsertIds":[0]}}
--- 契约依据（expected，M3 重建版） ---
{"constraint_id": "milvus_upsert_schema_match_001", "endpoint": "entities+upsert", "description": "data must match collection schema (page verbatim)", "assertion": "\"the keys in an entity object should match the collection schema\" (observed: string->DOUBLE, 'true'->BOOL, 1->BOOL, '42'->INT16 all accepted)", "source_url": "https://milvus.io/api-reference/restful/v2.6.x/v2/Vector%20(v2)/Upsert.md", "source_type": "documentation", "evidence_tier": "explicit"}

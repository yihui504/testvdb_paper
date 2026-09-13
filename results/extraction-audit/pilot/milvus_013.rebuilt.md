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

--- 契约依据（expected，来自 milvus 2.6.16 该版本文档） ---
[本版本文档中无 endpoint=collections+list 的约束条目]
[本版本文档中无 Request-Timeout 的类型约束条目]

已核查的引用页（均为 2.6.x REST API 参考，实测可访问，来源类型＝文档）：
- https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md
- https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Drop.md
- https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Load.md
- https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Rename.md
- https://milvus.io/api-reference/restful/v2.6.x/v2/Vector%20(v2)/Get.md
- https://milvus.io/api-reference/restful/v2.6.x/v2/Vector%20(v2)/Search.md
核查结论：上述页面的 Parameters 表仅将 `Authorization` 列为 header 参数；`Request-Timeout`
仅出现在 curl 示例行（`--header "Request-Timeout: 5"`）中，不含任何类型或取值约束的描述。

VERDICT: UNKNOWN (replay capture — no attack-agent assertion output; raw HTTP only)

=== 候选缺陷 milvus_001 ===
[vendor=milvus version=2.3 defect_type=behavior endpoint=entities+search]
--- 观察到的行为（observed） ---
[无可用观察记录：raw 为空且 log 未捕获（milvus_001 特例，探针未记录原始 HTTP）]
--- 契约依据（expected，M3 重建版） ---
[受测版本 2.3.0 的版本文档段已下线（v2.3.x → 302），约束依据无法核查]
观察证据：原始执行未捕获任何 HTTP 交互（output_milvus_001.log = "[no raw HTTP captured]"）。

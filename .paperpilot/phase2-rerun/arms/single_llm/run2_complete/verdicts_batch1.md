{"defect_id": "milvus_008", "verdict": "CONFIRMED", "confidence": 0.7, "rationale": "契约明确 COSINE identical 向量 distance==0（=1-similarity），实测 identical 向量 distance=1 且 100 查询中 11 个 >1.0（max 1.00000024），违反文档化度量定义且含浮点越界"}
{"defect_id": "milvus_010", "verdict": "CONFIRMED", "confidence": 0.8, "rationale": "同版本 alter_properties 对 ttl.seconds=-100 明确报错 out of range [-1,3155760000]，create 却以相同值 code=0 成功，同一参数同版本校验不一致"}
{"defect_id": "milvus_013", "verdict": "CONFIRMED", "confidence": 0.6, "rationale": "文档考古契约明确 Request-Timeout 必须为整数且非整数应拒绝，实测 3.5 与 abc 均静默接受（截断/忽略），违反文档化类型校验；但契约条目原 endpoint 为 entities+query，置信略降"}
{"defect_id": "milvus_014", "verdict": "FALSE_POSITIVE", "confidence": 0.95, "rationale": "dim=32768 在契约范围 [1,32768] 内成功、dim=32769 被正确拒绝，行为与契约完全一致，无缺陷"}
{"defect_id": "milvus_018", "verdict": "FALSE_POSITIVE", "confidence": 0.9, "rationale": "候选宣称 rename+create 双成功，但日志中 rename 实际返回 code=65535 duplicate-name 错误（契约要求的目标名不存在校验正常生效），宣称现象未被复现"}
{"defect_id": "milvus_019", "verdict": "FALSE_POSITIVE", "confidence": 0.9, "rationale": "rowCount=0 而查询可见数据与维护者 #50193 对完全相同现象的明确 by-design 表态（stats 只反映 flushed 数据）吻合，属设计行为"}
{"defect_id": "milvus_022", "verdict": "FALSE_POSITIVE", "confidence": 0.95, "rationale": "契约明文规定相同 schema 重复 create 为幂等 no-op 返回 200（behavioral_002），维护者 #50192 亦确认为 by-design，行为符合契约"}

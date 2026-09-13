{"defect_id": "milvus_008", "verdict": "CONFIRMED", "confidence": 0.85, "rationale": "COSINE 相同向量检索返回 distance=1（部分查询达 1.0000002>1），而补充契约明确规定 distance=1-相似度、相同向量 distance==0，观察值明确违反该 explicit 契约"}
{"defect_id": "milvus_010", "verdict": "CONFIRMED", "confidence": 0.75, "rationale": "create 携带 TTL=-100 返回 200/code=0 静默接受（describe 中也不见该 ttl 属性），而对照 alter_properties 对同一值 -100 返回 code=1100 拒绝，同一参数两条路径校验不一致，且契约要求 ttlSeconds>=0"}
{"defect_id": "milvus_013", "verdict": "CONFIRMED", "confidence": 0.65, "rationale": "补充契约规定 Request-Timeout 头必须为整数（非整数应拒绝），但 float 3.5 与字符串 abc 均被静默接受并 200/code=0 成功，属未按文档校验的参数验证缺陷"}
{"defect_id": "milvus_014", "verdict": "FALSE_POSITIVE", "confidence": 0.9, "rationale": "dim=32768 在契约范围 [1,32768] 内被接受、对照 32769 被拒绝且报错信息一致，观察行为完全符合契约，无缺陷"}
{"defect_id": "milvus_018", "verdict": "FALSE_POSITIVE", "confidence": 0.75, "rationale": "日志显示 rename 两次实际返回 code=65535 拒绝（newCollectionName 冲突）、仅 create 成功，候选声称的双双成功并发现象未在执行日志中出现，且该行为符合契约新名字不得已存在的要求"}
{"defect_id": "milvus_019", "verdict": "FALSE_POSITIVE", "confidence": 0.85, "rationale": "rowCount=0 仅反映已 flush 数据，维护者对完全相同场景已明确表态 by-design（50193），且契约仅要求返回行统计、未要求与未 flush 写入实时一致"}
{"defect_id": "milvus_022", "verdict": "FALSE_POSITIVE", "confidence": 0.95, "rationale": "同 schema 重复 create 返回 200 正是契约 state_001/behavioral_002 明文允许的幂等 no-op，维护者亦表态 by-design（50192），完全符合预期"}

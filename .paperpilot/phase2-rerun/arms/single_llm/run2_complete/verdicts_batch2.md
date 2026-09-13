{"defect_id": "milvus_026", "verdict": "FALSE_POSITIVE", "confidence": 0.8, "rationale": "契约仅要求 collectionName 为字符串，材料中无任何命名格式约束（无禁下划线规则），前导下划线名创建成功不违反任何已记录约束"}
{"defect_id": "milvus_027", "verdict": "FALSE_POSITIVE", "confidence": 0.7, "rationale": "维护者对同类现象（issue 50351）明确表态 REST v2 create 不消费顶层 shardsNum、静默忽略属 by design，200 反映字段被忽略而非接受非法值"}
{"defect_id": "milvus_028", "verdict": "CONFIRMED", "confidence": 0.65, "rationale": "metricType=\"\" 与 consistencyLevel=\"None\" 均违反契约枚举约束却返回 200/code=0（仅 dimension 越界被正确拒绝），无效参数未按文档返回 400"}
{"defect_id": "milvus_032", "verdict": "CONFIRMED", "confidence": 0.85, "rationale": "consistencyLevel=\"Invalid\" 不在文档四枚举内，服务器静默接受并 coercing 为默认 Bounded（describe 证实），违反 400-on-invalid-parameters 契约"}
{"defect_id": "milvus_033", "verdict": "FALSE_POSITIVE", "confidence": 0.65, "rationale": "契约 8 条中无 vectorFieldType 约束，该字段未记录在案且按维护者对未消费字段静默忽略的 by-design 表态（50351）属预期行为"}
{"defect_id": "milvus_038", "verdict": "CONFIRMED", "confidence": 0.8, "rationale": "文档明确 group_by 仅支持标量字段，REST 对 groupByField=vector 静默接受且分组未生效（10 条相同向量应归 1 组却返回 5 条）而非报错"}
{"defect_id": "qdrant_016", "verdict": "CONFIRMED", "confidence": 0.85, "rationale": "lookup_from 引用不存在的集合按 OpenAPI 契约应 400/404，实际静默返回 200 及源集合结果，与有效集合对照组行为完全相同"}

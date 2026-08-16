# fixH 派发记录表（M1 残留断言修复 + 对照翻错定责验证，4 case 单轮）

容器组：milvus 2.6.17（031→022→026→025 串行）。派发 = clean_run/prompts/{did}.txt 生成器
原文 + 防呆段（同 fixG）。

| # | did | vendor | version | reviewer 会话 | 派发时间 | 判词 | 校验 | 备注 |
|---|-----|--------|---------|--------------|---------|------|------|------|
| 1 | milvus_031 | milvus | 2.6.17 | agent-h-01 | 2026-08-16 | FALSE_POSITIVE | PASS | 回归✗(fixG C→F)——因果排除：审的是enableDynamicField次现象(upsert端点)，被修断言(create端点)未引用=现象焦点漂移非修复伤害 |
| 2 | milvus_022 | milvus | 2.6.17 | agent-h-02 | 2026-08-16 | FALSE_POSITIVE | PASS | 定责✓PASS(fixG C→F)——三断言同向消费(001/002修复版+M1)+errIgnoredCreateCollection接地+双路径证伪 |
| 3 | milvus_026 | milvus | 2.6.17 | agent-h-03 | 2026-08-16 | CONFIRMED | PASS | 观察：仍C——归因改变=现象焦点漂移(fixA轮strictGroupSize/fixG轮consistencyLevel/fixH轮dbName)，fixH轮显式消费C锚点判dbName真实不一致(012邻域) |
| 4 | milvus_025 | milvus | 2.6.17 | agent-h-04 | 2026-08-16 | CONFIRMED | PASS | 对照维持(漂移带C/C/F+C+C)——暴露同族残留断言range_entities_insert_001(max100, v2文档无此上限,待批) |

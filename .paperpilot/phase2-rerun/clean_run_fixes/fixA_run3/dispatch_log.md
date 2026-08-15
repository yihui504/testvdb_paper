# fixA_run3 派发记录表（纪律 §7.1）

> Run 标识：**fixA_run3**（2026-08-15 起）。配置 = v2 材料 + fixA 单锚点（与 fixA/fixA_run2 完全一致）。
> 派发 prompt = clean_run/prompts/ 生成器原文；模型统一标准档 GLM-5.2（每 case 新会话）。
> 同容器串行/异容器并行；milvus_001 空日志例外沿用 clean 判词（同前两轮处置）。

| # | did | vendor | version | reviewer 会话 | 派发时间 | 判词 | 校验 | 备注 |
|---|-----|--------|---------|--------------|---------|------|------|------|
| 1 | milvus_002 | milvus | 2.6.10 | agent-r3-01 | 2026-08-15 | FALSE_POSITIVE | PASS | nprobe=0 无可观测危害（run2 判 CONFIRMED——轮方差） |
| 2 | qdrant_001 | qdrant | 1.12.1 | agent-r3-02 | 2026-08-15 | CONFIRMED | PASS | wait 校验旁路 |
| 3 | weaviate_001 | weaviate | 1.37.4 | agent-r3-03 | 2026-08-15 | CONFIRMED | PASS | dynamicEfMin>Max 无校验 |
| 4 | milvus_003 | milvus | 2.6.10 | agent-r3-04 | 2026-08-15 | CONFIRMED | PASS | ef=0 无校验（引锚点） |
| 5 | qdrant_002 | qdrant | 1.18.0 | agent-r3-05 | 2026-08-15 | FALSE_POSITIVE | VOID |容器版本错配→作废重判(VOID_LOG)  hnsw_ef≥0 契约明确 |
| 6 | weaviate_002 | weaviate | 1.37.4 | agent-r3-06 | 2026-08-15 | CONFIRMED | PASS | flatSearchCutoff 无校验 |
| 7 | milvus_004 | milvus | 2.6.10 | agent-r3-07 | 2026-08-15 | FALSE_POSITIVE | PASS | oracle 数据集假设错误（run2 判 CONFIRMED——轮方差） |
| 8 | qdrant_003 | qdrant | 1.18.0 | agent-r3-08 | 2026-08-15 | CONFIRMED | VOID |容器版本错配→作废重判(VOID_LOG)  score_threshold 越界 |
| 9 | weaviate_003 | weaviate | 1.37.4 | agent-r3-09 | 2026-08-15 | CONFIRMED | PASS | factor=-1 静默改写 |
| 10 | milvus_005 | milvus | 2.6.10 | agent-r3-10 | 2026-08-15 | CONFIRMED | PASS | insert/query 字段名不对称校验 |
| 11 | qdrant_004 | qdrant | 1.18.0 | agent-r3-11 | 2026-08-15 | FALSE_POSITIVE | VOID |容器版本错配→作废重判(VOID_LOG)  维度校验正常 |
| 12 | weaviate_004 | weaviate | 1.37.4 | agent-r3-12 | 2026-08-15 | CONFIRMED | PASS | ef=-1 无范围校验 |
| 13 | milvus_006 | milvus | 2.6.10 | agent-r3-13 | 2026-08-15 | FALSE_POSITIVE | PASS | dynamic field 按原类型存储=设计特性（run2 判 CONFIRMED——轮方差） |
| 14 | qdrant_005 | qdrant | 1.18.1 | agent-r3-14 | 2026-08-15 | FALSE_POSITIVE | VOID |容器版本错配→作废重判(VOID_LOG)  NonZeroU32 类型级校验 |
| 15 | weaviate_005 | weaviate | 1.38.0 | agent-r3-15 | 2026-08-15 | CONFIRMED | VOID | 容器版本错配(1.37.4)→作废重判(VOID_LOG) |
| 16 | milvus_007 | milvus | 2.6.10 | agent-r3-16 | 2026-08-15 | FALSE_POSITIVE | PASS | 契约误读（run2 判 CONFIRMED——轮方差） |
| 17 | qdrant_006 | qdrant | 1.18.1 | agent-r3-17 | 2026-08-15 | FALSE_POSITIVE | VOID |容器版本错配→作废重判(VOID_LOG)  payload 可选字段语义 |
| 18 | weaviate_005 | weaviate | 1.38.0 | agent-r3-18 | 2026-08-15 | CONFIRMED | PASS | 重判（首判容器错配作废见#15）；desiredCount 负值静默失败 |
| 19 | milvus_008 | milvus | 2.6.12 | agent-r3-19 | 2026-08-15 | CONFIRMED | VOID | 容器版本错配(2.6.10)→作废重判(VOID_LOG) |
| 20 | weaviate_006 | weaviate | 1.38.0 | agent-r3-20 | 2026-08-15 | CONFIRMED | PASS | tokenization 空串绕过枚举校验（run2 判 FP——轮方差） |
| 21 | qdrant_002 | qdrant | 1.18.0 | agent-r3-21 | 2026-08-15 | FALSE_POSITIVE | PASS | 重判（首判容器错配）；graceful fallback by-design |
| 22 | milvus_008 | milvus | 2.6.12 | agent-r3-22 | 2026-08-15 | FALSE_POSITIVE | PASS | 重判（首判容器错配）；索引重复拒绝=设计行为 |
| 23 | weaviate_007 | weaviate | 1.38.0 | agent-r3-23 | 2026-08-15 | CONFIRMED | PASS | distance=null 静默回退默认 |
| 24 | qdrant_003 | qdrant | 1.18.0 | agent-r3-24 | 2026-08-15 | CONFIRMED | PASS | 重判；score_threshold 越界无校验 |
| 25 | weaviate_008 | weaviate | 1.38.0 | agent-r3-25 | 2026-08-15 | FALSE_POSITIVE | PASS | allowEmpty=true 显式设计（run2 判 CONFIRMED——轮方差） |
| 26 | qdrant_004 | qdrant | 1.18.0 | agent-r3-26 | 2026-08-15 | CONFIRMED | PASS | 重判；wait=false 校验旁路（run2 判 FP——轮方差） |
| 27 | qdrant_005 | qdrant | 1.18.1 | agent-r3-27 | 2026-08-15 | FALSE_POSITIVE | PASS | 重判；NonZeroU32 类型级校验 |
| 28 | qdrant_006 | qdrant | 1.18.1 | agent-r3-28 | 2026-08-15 | FALSE_POSITIVE | PASS | 重判；payload 可选=设计灵活性 |
| 29 | qdrant_007 | qdrant | 1.18.2 | agent-r3-29 | 2026-08-15 | FALSE_POSITIVE | PASS | 重判；batch 前置校验=原子语义（run2 判 CONFIRMED——轮方差） |
| 30 | weaviate_009 | weaviate | 1.38.2 | agent-r3-30 | 2026-08-15 | CONFIRMED | PASS | 空向量静默丢弃 |
| 31 | milvus_009 | milvus | 2.6.16 | agent-r3-31 | 2026-08-15 | FALSE_POSITIVE | PASS | nprobe=0 无契约无校验（run2 判 CONFIRMED——轮方差） |
| 32 | milvus_010 | milvus | 2.6.16 | agent-r3-32 | 2026-08-15 | CONFIRMED | PASS | TTL properties 旁路校验；会话越界二判 009 已 void(VOID_LOG) |
| 33 | qdrant_008 | qdrant | 1.18.2 | agent-r3-33 | 2026-08-15 | FALSE_POSITIVE | PASS |  |
| 34 | weaviate_010 | weaviate | 1.38.2 | agent-r3-34 | 2026-08-15 | FALSE_POSITIVE | PASS | batch delete 防误删校验 |
| 35 | milvus_011 | milvus | 2.6.16 | agent-r3-35 | 2026-08-15 | FALSE_POSITIVE | PASS | filter null/empty 等价=设计 |
| 36 | qdrant_009 | qdrant | 1.18.2 | agent-r3-36 | 2026-08-15 | CONFIRMED | PASS | 空 vectors config 后插入拒绝 |
| 37 | milvus_012 | milvus | 2.6.16 | agent-r3-37 | 2026-08-15 | FALSE_POSITIVE | PASS | dbName 空串=默认库设计 |
| 38 | qdrant_010 | qdrant | 1.18.2 | agent-r3-38 | 2026-08-15 | FALSE_POSITIVE | PASS | 空 vectors config 后插入拒绝=设计（run2 判 CONFIRMED——轮方差） |
| 39 | milvus_013 | milvus | 2.6.16 | agent-r3-39 | 2026-08-15 | CONFIRMED | PASS | timeout 头非法值静默忽略 |
| 40 | qdrant_011 | qdrant | 1.18.2 | agent-r3-40 | 2026-08-15 | FALSE_POSITIVE | PASS | nullable should=无约束设计 |
| 42 | qdrant_012 | qdrant | 1.18.2 | agent-r3-42 | 2026-08-15 | FALSE_POSITIVE | VOID | 无源码接地→作废重判(VOID_LOG) |
| 45 | milvus_016 | milvus | 2.6.16 | agent-r3-45 | 2026-08-15 | CONFIRMED | PASS | searchParams 无范围校验 |
| 46 | qdrant_012 | qdrant | 1.18.2 | agent-r3-46 | 2026-08-15 | FALSE_POSITIVE | PASS | 三判（两次无接地作废见VOID_LOG）；must_not 语义正确 |
| 47 | milvus_017 | milvus | 2.6.16 | agent-r3-47 | 2026-08-15 | FALSE_POSITIVE | PASS | 参数名用错非缺陷 |
| 48 | qdrant_013 | qdrant | 1.18.2 | agent-r3-48 | 2026-08-15 | FALSE_POSITIVE | PASS | query null→scroll 降级设计 |
| 49 | milvus_018 | milvus | 2.6.16 | agent-r3-49 | 2026-08-15 | CONFIRMED | PASS | rename HTTP200 vs 契约400 |
| 50 | qdrant_014 | qdrant | 1.18.2 | agent-r3-50 | 2026-08-15 | FALSE_POSITIVE | PASS | standalone 模式 cluster 操作=设计 |
| 51 | milvus_019 | milvus | 2.6.16 | agent-r3-51 | 2026-08-15 | CONFIRMED | PASS | rowCount=0 vs 契约不变量 |
| 52 | qdrant_015 | qdrant | 1.18.2 | agent-r3-52 | 2026-08-15 | CONFIRMED | PASS | shard_number 无上界→崩溃；实测致容器 exit 137（自愈重启）；milvus 连带 Exited(1) 重建 |
| 53 | milvus_020 | milvus | 2.6.16 | agent-r3-53 | 2026-08-15 | CONFIRMED | PASS | MVCC 时间戳窗口脏读 |
| 54 | qdrant_016 | qdrant | 1.18.2 | agent-r3-54 | 2026-08-15 | CONFIRMED | PASS | lookup_from 不校验集合存在性 |
| 55 | qdrant_017 | qdrant | 1.18.2 | agent-r3-55 | 2026-08-15 | FALSE_POSITIVE | PASS | 分页无重复+锚点 by-design |
| 56 | milvus_021 | milvus | 2.6.17 | agent-r3-56 | 2026-08-15 | FALSE_POSITIVE | VOID | 无源码接地→作废重判(VOID_LOG) |
| 57 | qdrant_018 | qdrant | 1.18.3 | agent-r3-57 | 2026-08-15 | CONFIRMED | PASS | IsEmpty 硬编码 50% 估计；qdrant 18/18 完成 |
| 58 | milvus_021 | milvus | 2.6.17 | agent-r3-58 | 2026-08-15 | CONFIRMED | PASS | 重判；未加载集合可搜索（首判作废见#56） |
| 59 | milvus_022 | milvus | 2.6.17 | agent-r3-59 | 2026-08-15 | FALSE_POSITIVE | PASS | 幂等 create 源码显式设计 |
| 60 | milvus_023 | milvus | 2.6.17 | agent-r3-60 | 2026-08-15 | CONFIRMED | PASS | 幂等 drop 违反契约 404（run2 判 FP——轮方差灰区） |
| 61 | milvus_024 | milvus | 2.6.17 | agent-r3-61 | 2026-08-15 | CONFIRMED | PASS | ids 参数静默忽略（run2 判 FP——轮方差灰区） |
| 62 | milvus_025 | milvus | 2.6.17 | agent-r3-62 | 2026-08-15 | FALSE_POSITIVE | PASS |  |
| 63 | milvus_026 | milvus | 2.6.17 | agent-r3-63 | 2026-08-15 | FALSE_POSITIVE | PASS | 校验在 params 内正常工作 |
| 64 | milvus_027 | milvus | 2.6.17 | agent-r3-64 | 2026-08-15 | CONFIRMED | PASS | shardsNum 缺下界校验 |
| 65 | milvus_028 | milvus | 2.6.17 | agent-r3-65 | 2026-08-15 | FALSE_POSITIVE | PASS | 可选参数默认值设计（run2 判 CONFIRMED——轮方差灰区） |
| 66 | milvus_029 | milvus | 2.6.17 | agent-r3-66 | 2026-08-15 | CONFIRMED | PASS | limit=0 HTTP200 vs 契约400（run2 判 FP——轮方差） |
| 67 | milvus_030 | milvus | 2.6.17 | agent-r3-67 | 2026-08-15 | CONFIRMED | PASS | 密码校验存在但文档不一致（run2 判 FP——轮方差） |
| 68 | milvus_031 | milvus | 2.6.17 | agent-r3-68 | 2026-08-15 | FALSE_POSITIVE | PASS | autoID upsert 需显式 PK |
| 69 | milvus_032 | milvus | 2.6.19 | agent-r3-69 | 2026-08-15 | CONFIRMED | PASS | consistencyLevel 无效值静默回退（run2 判 FP——轮方差灰区） |
| 70 | milvus_033 | milvus | 2.6.19 | agent-r3-70 | 2026-08-15 | FALSE_POSITIVE | PASS | 未知参数忽略=前向兼容（run2 判 CONFIRMED——轮方差灰区） |
| 71 | milvus_034 | milvus | 3.0.0 | agent-r3-71 | 2026-08-15 | CONFIRMED | PASS | JSON 字段无类型校验（引锚点） |
| 72 | milvus_035 | milvus | 3.0.0 | agent-r3-72 | 2026-08-15 | CONFIRMED | PASS | Int64 边界类型校验缺失（type coercion 簇） |
| 73 | milvus_036 | milvus | 3.0.0 | agent-r3-73 | 2026-08-15 | CONFIRMED | PASS | groupSize 内部校验存在但 REST 层不拒 |
| 74 | milvus_037 | milvus | 3.0.0 | agent-r3-74 | 2026-08-15 | CONFIRMED | PASS | JSON 字段直转无校验（type coercion 簇） |
| 75 | milvus_038 | milvus | 3.0.0 | agent-r3-75 | 2026-08-15 | FALSE_POSITIVE | PASS | 参数结构不匹配=语义问题（run2 判 CONFIRMED——轮方差灰区） |
| 76 | milvus_039 | milvus | 3.0.0 | agent-r3-76 | 2026-08-15 | FALSE_POSITIVE | PASS | 字符串ID upsert 强转 by-design（与 run2 同向） |
| 77 | milvus_040 | milvus | 3.0.0 | agent-r3-77 | 2026-08-15 | FALSE_POSITIVE | PASS | JSON 标量合法（run2 判 CONFIRMED——轮方差灰区） |
| 78 | milvus_041 | milvus | 3.0.0 | agent-r3-78 | 2026-08-15 | FALSE_POSITIVE | PASS | 复现失败称日志不可靠（run2 判 CONFIRMED——轮方差灰区） |
| 79 | milvus_042 | milvus | 3.0.0 | agent-r3-79 | 2026-08-15 | FALSE_POSITIVE | PASS | 向量字符串=by-design（run2 判 CONFIRMED——轮方差灰区） |
| 80 | milvus_043 | milvus | 3.0.0 | agent-r3-80 | 2026-08-15 | CONFIRMED | PASS | strictGroupSize 未传递到缩减逻辑 |

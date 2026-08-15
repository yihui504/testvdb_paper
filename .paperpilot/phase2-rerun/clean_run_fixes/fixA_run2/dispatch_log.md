# fixA_run2 派发记录表（纪律 §7.1）

> Run 标识：**fixA_run2**（2026-08-15 起）。配置 = v2 材料 + fixA 单锚点（audit 0 FAIL 已确认）。
> 派发 prompt = clean_run/prompts/ 生成器原文（材料指针未变，泄漏扫描沿用 0 命中结论）。
> 模型：统一标准档 GLM-5.2（每 case 新会话 = 新 reviewer，默认档）。
> 顺序：同容器内 case 串行；3 vendor 容器并行。
> milvus_001（空日志例外，纪律 §2.6）：沿用 clean 判词（fixA 不触及该 case 材料），与 fixA-run1 处置一致。

| # | did | vendor | version | reviewer 会话 | 派发时间 | 判词 | 校验 | 备注 |
|---|-----|--------|---------|--------------|---------|------|------|------|
| 1 | weaviate_001 | weaviate | 1.37.4 | agent-r2-01 | 2026-08-15 | CONFIRMED | PASS | 会话越界判同版本4case，仅保留派发目标001（首个判定）；002-004作废见VOID_LOG |
| 2 | milvus_002 | milvus | 2.6.10 | agent-r2-02 | 2026-08-15 | CONFIRMED | VOID | 首判合格(CONFIRMED 0.95 ex1317)但编排归档失误丢失→作废重判(VOID_LOG) |
| 3 | qdrant_001 | qdrant | 1.12.1 | agent-r2-03 | 2026-08-15 | CONFIRMED | VOID | 首判合格(CONFIRMED 0.95 ex1776)但编排归档失误丢失→作废重判(VOID_LOG) |
| 4 | milvus_002 | milvus | 2.6.10 | agent-r2-04 | 2026-08-15 | CONFIRMED | PASS | 重判（首判作废见#2）；nprobe 缺范围校验 |
| 5 | qdrant_001 | qdrant | 1.12.1 | agent-r2-05 | 2026-08-15 | CONFIRMED | PASS | 重判（首判作废见#3）；wait=false 校验旁路 |
| 6 | weaviate_002 | weaviate | 1.37.4 | agent-r2-06 | 2026-08-15 | CONFIRMED | PASS | 重判（首判作废见VOID_LOG）；flatSearchCutoff 负值 |
| 7 | milvus_003 | milvus | 2.6.10 | agent-r2-07 | 2026-08-15 | CONFIRMED | PASS |  |
| 8 | qdrant_002 | qdrant | 1.18.0 | agent-r2-08 | 2026-08-15 | FALSE_POSITIVE | VOID | 容器版本错配(1.12.1)→作废重判(VOID_LOG)；容器已切1.18.0 |
| 9 | weaviate_003 | weaviate | 1.37.4 | agent-r2-09 | 2026-08-15 | CONFIRMED | PASS | factor=-1 静默修正 |
| 13 | milvus_005 | milvus | 2.6.10 | agent-r2-13 | 2026-08-15 | CONFIRMED | PASS | insert/query 字段名校验不一致（通道内不对称） |
| 14 | qdrant_003 | qdrant | 1.18.0 | agent-r2-14 | 2026-08-15 | CONFIRMED | PASS | score_threshold 越界无校验 |
| 15 | weaviate_005 | weaviate | 1.38.0 | agent-r2-15 | 2026-08-15 | CONFIRMED | PASS | desiredCount=-1 200但404 |
| 16 | milvus_006 | milvus | 2.6.10 | agent-r2-16 | 2026-08-15 | CONFIRMED | PASS | 整数→VarChar 强转 |
| 17 | qdrant_004 | qdrant | 1.18.0 | agent-r2-17 | 2026-08-15 | FALSE_POSITIVE | PASS | wait 异步语义 by-design |
| 18 | weaviate_006 | weaviate | 1.38.0 | agent-r2-18 | 2026-08-15 | FALSE_POSITIVE | PASS | 空串默认值 by-design |
| 19 | milvus_007 | milvus | 2.6.10 | agent-r2-19 | 2026-08-15 | CONFIRMED | PASS | HTTP 200 包装 vs 契约 400 |
| 20 | qdrant_005 | qdrant | 1.18.1 | agent-r2-20 | 2026-08-15 | FALSE_POSITIVE | VOID | 容器版本错配(1.18.0)→作废重判(VOID_LOG) |
| 21 | weaviate_007 | weaviate | 1.38.0 | agent-r2-21 | 2026-08-15 | CONFIRMED | PASS | distance=null 静默回退默认 |
| 22 | qdrant_005 | qdrant | 1.18.1 | agent-r2-22 | 2026-08-15 | FALSE_POSITIVE | PASS | 重判（首判作废见#20）；NonZeroU32 类型级校验=by-design |
| 23 | weaviate_008 | weaviate | 1.38.0 | agent-r2-23 | 2026-08-15 | CONFIRMED | PASS | activityStatus 枚举校验缺失 |
| 24 | milvus_008 | milvus | 2.6.12 | agent-r2-24 | 2026-08-15 | FALSE_POSITIVE | PASS | annsField 自动检测 by-design |
| 25 | qdrant_006 | qdrant | 1.18.1 | agent-r2-25 | 2026-08-15 | FALSE_POSITIVE | PASS | filter 行为正常 |
| 26 | weaviate_009 | weaviate | 1.38.2 | agent-r2-26 | 2026-08-15 | CONFIRMED | PASS | 空向量持久化 |
| 27 | weaviate_010 | weaviate | 1.38.2 | agent-r2-27 | 2026-08-15 | FALSE_POSITIVE | PASS | batch delete 校验=正常防御 |
| 28 | milvus_009 | milvus | 2.6.16 | agent-r2-28 | 2026-08-15 | CONFIRMED | VOID | 平铺格式无verdicts数组→作废重判(VOID_LOG) |
| 29 | qdrant_007 | qdrant | 1.18.2 | agent-r2-29 | 2026-08-15 | CONFIRMED | PASS | batch 非原子 |
| 30 | milvus_009 | milvus | 2.6.16 | agent-r2-30 | 2026-08-15 | CONFIRMED | PASS | 重判（首判平铺作废见#28）；nprobe 无范围校验 |
| 31 | qdrant_008 | qdrant | 1.18.2 | agent-r2-31 | 2026-08-15 | FALSE_POSITIVE | VOID | 无源码接地→作废重判(VOID_LOG) |
| 32 | milvus_010 | milvus | 2.6.16 | agent-r2-32 | 2026-08-15 | CONFIRMED | PASS | CREATE/ALTER TTL 校验不一致 |
| 33 | qdrant_008 | qdrant | 1.18.2 | agent-r2-33 | 2026-08-15 | FALSE_POSITIVE | PASS | 重判（首判无接地作废见#31）；scroll filter 正常 |
| 34 | milvus_011 | milvus | 2.6.16 | agent-r2-34 | 2026-08-15 | FALSE_POSITIVE | PASS | filter null/empty 等价=match-all 语义 |
| 35 | qdrant_009 | qdrant | 1.18.2 | agent-r2-35 | 2026-08-15 | CONFIRMED | PASS |  |
| 36 | milvus_012 | milvus | 2.6.16 | agent-r2-36 | 2026-08-15 | FALSE_POSITIVE | PASS | dbName 默认值=正常语义 |
| 37 | qdrant_010 | qdrant | 1.18.2 | agent-r2-37 | 2026-08-15 | CONFIRMED | PASS | 空 vectors config 集合 |
| 38 | milvus_013 | milvus | 2.6.16 | agent-r2-38 | 2026-08-15 | CONFIRMED | PASS | 非法 timeout 头静默忽略（A组FIXED_PR） |
| 39 | qdrant_011 | qdrant | 1.18.2 | agent-r2-39 | 2026-08-15 | FALSE_POSITIVE | PASS | Option null=无过滤语义 |
| 40 | milvus_014 | milvus | 2.6.16 | agent-r2-40 | 2026-08-15 | FALSE_POSITIVE | PASS | 维度校验正常工作 |
| 41 | qdrant_012 | qdrant | 1.18.2 | agent-r2-41 | 2026-08-15 | FALSE_POSITIVE | PASS | must_not 语义正确 |
| 42 | milvus_015 | milvus | 2.6.16 | agent-r2-42 | 2026-08-15 | FALSE_POSITIVE | PASS | 不存在集合建索引=正确报错 |
| 43 | qdrant_013 | qdrant | 1.18.2 | agent-r2-43 | 2026-08-15 | FALSE_POSITIVE | VOID | 平铺格式无verdicts数组→作废重判(VOID_LOG) |
| 44 | milvus_016 | milvus | 2.6.16 | agent-r2-44 | 2026-08-15 | CONFIRMED | PASS | searchParams ef/nprobe 无范围校验 |
| 45 | qdrant_013 | qdrant | 1.18.2 | agent-r2-45 | 2026-08-15 | FALSE_POSITIVE | PASS | 重判（首判平铺作废见#43）；query null=by-design |
| 46 | milvus_017 | milvus | 2.6.16 | agent-r2-46 | 2026-08-15 | FALSE_POSITIVE | PASS |  |
| 47 | qdrant_014 | qdrant | 1.18.2 | agent-r2-47 | 2026-08-15 | FALSE_POSITIVE | PASS | standalone 模式 cluster 操作=正确报错 |
| 48 | milvus_018 | milvus | 2.6.16 | agent-r2-48 | 2026-08-15 | CONFIRMED | PASS | rename 重名 HTTP200 vs 契约400 |
| 49 | qdrant_015 | qdrant | 1.18.2 | agent-r2-49 | 2026-08-15 | CONFIRMED | PASS | shard_number 无上界→崩溃；实测致 qdrant 容器 OOM Exited(137)+milvus 连带 Exited(1)（纪律§5.4，重建后继续） |
| 50 | milvus_019 | milvus | 2.6.16 | agent-r2-50 | 2026-08-15 | CONFIRMED | PASS | rowCount=0 SegmentState 过滤 |
| 51 | qdrant_016 | qdrant | 1.18.2 | agent-r2-51 | 2026-08-15 | CONFIRMED | PASS |  |
| 52 | milvus_020 | milvus | 2.6.16 | agent-r2-52 | 2026-08-15 | CONFIRMED | PASS | search-delete 可见性 gap |
| 53 | qdrant_017 | qdrant | 1.18.2 | agent-r2-53 | 2026-08-15 | FALSE_POSITIVE | PASS | 分页无重复+HNSW 锚点 by-design |
| 54 | milvus_021 | milvus | 2.6.17 | agent-r2-54 | 2026-08-15 | FALSE_POSITIVE | PASS | 日志无缺陷断言+limit校验完备 |
| 55 | qdrant_018 | qdrant | 1.18.3 | agent-r2-55 | 2026-08-15 | CONFIRMED | PASS | estimate_cardinality IsEmpty 缺失 |
| 56 | milvus_022 | milvus | 2.6.17 | agent-r2-56 | 2026-08-15 | FALSE_POSITIVE | PASS | 幂等 create by-design |
| 57 | milvus_023 | milvus | 2.6.17 | agent-r2-57 | 2026-08-15 | FALSE_POSITIVE | PASS | 幂等 drop by-design（源码显式注释） |
| 58 | milvus_024 | milvus | 2.6.17 | agent-r2-58 | 2026-08-15 | FALSE_POSITIVE | PASS | 未定义 ids 参数被忽略=正常解析 |
| 59 | milvus_025 | milvus | 2.6.17 | agent-r2-59 | 2026-08-15 | CONFIRMED | PASS | 批量上限100缺失校验 |
| 60 | milvus_026 | milvus | 2.6.17 | agent-r2-60 | 2026-08-15 | FALSE_POSITIVE | PASS | 维度校验正常（契约文档错） |
| 61 | milvus_027 | milvus | 2.6.17 | agent-r2-61 | 2026-08-15 | CONFIRMED | PASS | shardsNum 静默修正（REST/gRPC 差异） |
| 62 | milvus_028 | milvus | 2.6.17 | agent-r2-62 | 2026-08-15 | CONFIRMED | PASS | consistencyLevel 顶层字段被忽略 |
| 63 | milvus_029 | milvus | 2.6.17 | agent-r2-63 | 2026-08-15 | FALSE_POSITIVE | PASS | 校验正常工作 |
| 64 | milvus_030 | milvus | 2.6.17 | agent-r2-64 | 2026-08-15 | FALSE_POSITIVE | PASS | 密码长度=bcrypt 设计约束 |
| 65 | milvus_031 | milvus | 2.6.17 | agent-r2-65 | 2026-08-15 | FALSE_POSITIVE | PASS | dynamic schema 正确校验 |
| 66 | milvus_032 | milvus | 2.6.19 | agent-r2-66 | 2026-08-15 | FALSE_POSITIVE | PASS | consistencyLevel 顶层忽略（与028同现象相反结论——轮方差灰区实证） |
| 67 | milvus_033 | milvus | 2.6.19 | agent-r2-67 | 2026-08-15 | CONFIRMED | PASS | vectorFieldType 被忽略 |
| 68 | milvus_034 | milvus | 3.0.0 | agent-r2-68 | 2026-08-15 | CONFIRMED | PASS | JSON 字段只查长度不查语法 |
| 69 | milvus_035 | milvus | 3.0.0 | agent-r2-69 | 2026-08-15 | CONFIRMED | PASS | Int64 字符串强转（type coercion 簇） |
| 70 | milvus_036 | milvus | 3.0.0 | agent-r2-70 | 2026-08-15 | CONFIRMED | PASS | groupSize 无范围校验 |
| 71 | milvus_037 | milvus | 3.0.0 | agent-r2-71 | 2026-08-15 | CONFIRMED | PASS | INT64/BOOL/VARCHAR 自动强转（type coercion 簇） |
| 72 | milvus_038 | milvus | 3.0.0 | agent-r2-72 | 2026-08-15 | CONFIRMED | PASS | groupByField JSON tag 不匹配静默忽略 |
| 73 | milvus_039 | milvus | 3.0.0 | agent-r2-73 | 2026-08-15 | FALSE_POSITIVE | PASS | 字符串ID upsert 强转（035同源码相反结论——轮方差） |
| 74 | milvus_040 | milvus | 3.0.0 | agent-r2-74 | 2026-08-15 | CONFIRMED | PASS | JSON 字段无 Unmarshal 校验 |
| 75 | milvus_041 | milvus | 3.0.0 | agent-r2-75 | 2026-08-15 | CONFIRMED | PASS | Bool/Double/Int16 cast 强转（type coercion 簇） |
| 76 | milvus_042 | milvus | 3.0.0 | agent-r2-76 | 2026-08-15 | CONFIRMED | PASS | 向量字符串强转（52315 同源码） |
| 77 | milvus_043 | milvus | 3.0.0 | agent-r2-77 | 2026-08-15 | CONFIRMED | PASS | strictGroupSize 不生效（SearchGroupByOperator 逻辑缺陷） |

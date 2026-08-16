# fixF_run3 派发记录表（最终配置轮间方差复测 run3，70 重判 + milvus_001 沿用 clean）

配置 = fixF 完全一致（fixA 锚点 + qdrant 13 锚点 + C/G 锚点 + 契约 M1/M2/Q1/Q2 + fixH 001/002 + fixI range_insert_001 + 原版 SOP）。MF 176，本轮零材料改动。
容器组同 fixF/run2。三 vendor 异容器并行、组内串行、切组前核对容器版本。
派发 = clean_run/prompts/{did}.txt 生成器原文 + 防呆段（同 fixF）。

| # | did | vendor | version | reviewer 会话 | 派发时间 | 判词 | 校验 | 备注 |
|---|-----|--------|---------|--------------|---------|------|------|------|
| 1 | milvus_001 | milvus | 2.3 | — | — | FALSE_POSITIVE | 沿用 | GT=CONFIRMED ✗ 沿用 clean（同 fixF/run2） |
| 2 | milvus_002 | milvus | 2.6.10 | agent-h-02 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓ |
| 3 | milvus_003 | milvus | 2.6.10 | agent-h-03 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓ |
| 4 | milvus_004 | milvus | 2.6.10 | agent-h-04 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=CONFIRMED ✗ |
| 5 | milvus_005 | milvus | 2.6.10 | agent-h-05 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓ |
| 6 | milvus_006 | milvus | 2.6.10 | agent-h-06 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓ |
| 7 | milvus_007 | milvus | 2.6.10 | agent-h-07 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE ✓ |
| 55 | qdrant_002 | qdrant | 1.18.0 | agent-h-55 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓（run2/run3 连续翻正——range gte>lt 结构性取证通道稳定开启） |
| 56 | qdrant_003 | qdrant | 1.18.0 | agent-h-56 | 2026-08-16 | CONFIRMED | PASS | GT=FALSE_POSITIVE ✗ |
| 57 | qdrant_004 | qdrant | 1.18.0 | agent-h-57 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=CONFIRMED ✗ |
| 64 | weaviate_001 | weaviate | 1.37.4 | agent-h-64 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓ |
| 65 | weaviate_002 | weaviate | 1.37.4 | agent-h-65 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓ |
| 66 | weaviate_003 | weaviate | 1.37.4 | agent-h-66 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=CONFIRMED ✗ |
| 67 | weaviate_004 | weaviate | 1.37.4 | agent-h-67 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE ✓ |
| 8 | milvus_008 | milvus | 2.6.12 | agent-h-08 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=CONFIRMED ✗（fixF C/fixG-era 漂移带; run3 审 outputFields 次现象→FP, 现象漂移再实证） |
| 9 | milvus_009 | milvus | 2.6.16 | agent-h-09 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓（run2/run3 连翻正——nprobe 物理约束结构性取证通道稳定） |
| 10 | milvus_010 | milvus | 2.6.16 | agent-h-10 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓ |
| 11 | milvus_011 | milvus | 2.6.16 | agent-h-11 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE ✓ |
| 12 | milvus_012 | milvus | 2.6.16 | agent-h-12 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=CONFIRMED ✗ |
| 13 | milvus_013 | milvus | 2.6.16 | agent-h-13 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓ |
| 14 | milvus_014 | milvus | 2.6.16 | agent-h-14 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE ✓ |
| 15 | milvus_015 | milvus | 2.6.16 | agent-h-15 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE ✓ |
| 16 | milvus_016 | milvus | 2.6.16 | agent-h-16 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=CONFIRMED ✗ |
| 17 | milvus_017 | milvus | 2.6.16 | agent-h-17 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=CONFIRMED ✗ |
| 18 | milvus_018 | milvus | 2.6.16 | agent-h-18 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE ✓ |
| 19 | milvus_019 | milvus | 2.6.16 | agent-h-19 | 2026-08-16 | CONFIRMED | PASS | GT=FALSE_POSITIVE ✗（GT=FP; run2/run3 连判 C 错向——get_stats rowCount 真现象独立发现, 同源漂移） |
| 20 | milvus_020 | milvus | 2.6.16 | agent-h-20 | 2026-08-16 | CONFIRMED | PASS | GT=FALSE_POSITIVE ✗ |
| 21 | milvus_021 | milvus | 2.6.17 | agent-h-21 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE ✓ |
| 22 | milvus_022 | milvus | 2.6.17 | agent-h-22 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE ✓（M1 适用类 run3 回 F——errIgnoredCreateCollection 显式接地, 修复消费回归） |
| 23 | milvus_023 | milvus | 2.6.17 | agent-h-23 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE ✓（M2 适用类 run3 回 F——errIgnoredDropCollection 接地, 修复消费回归） |
| 24 | milvus_024 | milvus | 2.6.17 | agent-h-24 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓ |
| 25 | milvus_025 | milvus | 2.6.17 | agent-h-25 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE ✓（fixI 断言修复 run3 保持 F——三连保持） |
| 26 | milvus_026 | milvus | 2.6.17 | agent-h-26 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE ✓ |
| 27 | milvus_027 | milvus | 2.6.17 | agent-h-27 | 2026-08-16 | CONFIRMED | PASS | GT=FALSE_POSITIVE ✗ |
| 28 | milvus_028 | milvus | 2.6.17 | agent-h-28 | 2026-08-16 | CONFIRMED | PASS | GT=FALSE_POSITIVE ✗ |
| 29 | milvus_029 | milvus | 2.6.17 | agent-h-29 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=CONFIRMED ✗ |
| 30 | milvus_030 | milvus | 2.6.17 | agent-h-30 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓（GT=FP run3 错向 C——文档-行为锚点副作用/密码范围文档分歧） |
| 31 | milvus_031 | milvus | 2.6.17 | agent-h-31 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓（五轮 C/F/F/C/C——autoID 主现象+锚点, 概率性翻正偏主现象） |
| 32 | milvus_032 | milvus | 2.6.19 | agent-h-32 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓ |
| 33 | milvus_033 | milvus | 2.6.19 | agent-h-33 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓（GT=FP run3 错向 C——vectorFieldType 未消费即静默忽略 vs run2 F, 灰区漂移） |
| 34 | milvus_034 | milvus | 3.0.0 | agent-h-34 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓（run3 回 C 对向——3.0.0 组 run2 系统性 F/run3 分裂, 轮方差实锤） |
| 35 | milvus_035 | milvus | 3.0.0 | agent-h-35 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=CONFIRMED ✗ |
| 36 | milvus_036 | milvus | 3.0.0 | agent-h-36 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓（groupSize 物理约束, run3 C 对向） |
| 37 | milvus_037 | milvus | 3.0.0 | agent-h-37 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=CONFIRMED ✗ |
| 38 | milvus_038 | milvus | 3.0.0 | agent-h-38 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=CONFIRMED ✗ |
| 39 | milvus_039 | milvus | 3.0.0 | agent-h-39 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=CONFIRMED ✗（run3 回 F 错向——type coercion 灰区方向反复, fixF C/run2 C/run3 F→三轮 2C1F） |
| 40 | milvus_040 | milvus | 3.0.0 | agent-h-40 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=CONFIRMED ✗ |
| 41 | milvus_041 | milvus | 3.0.0 | agent-h-41 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=CONFIRMED ✗ |
| 42 | milvus_042 | milvus | 3.0.0 | agent-h-42 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=CONFIRMED ✗ |
| 43 | milvus_043 | milvus | 3.0.0 | agent-h-43 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=CONFIRMED ✗ |
| 54 | qdrant_001 | qdrant | 1.12.1 | agent-h-54 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=CONFIRMED ✗（fixF/run2 两轮 C, run3 F——三分裂） |
| 58 | qdrant_005 | qdrant | 1.18.1 | agent-h-58 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE ✓ |
| 59 | qdrant_006 | qdrant | 1.18.1 | agent-h-59 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE ✓ |
| 60 | qdrant_007 | qdrant | 1.18.2 | agent-h-60 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE ✓（Q2 断言修复三轮保持 F） |
| 61 | qdrant_008 | qdrant | 1.18.2 | agent-h-61 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE ✓ |
| 62 | qdrant_009 | qdrant | 1.18.2 | agent-h-62 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE ✓（Q1 断言修复三轮保持 F） |
| 63 | qdrant_010 | qdrant | 1.18.2 | agent-h-63 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE ✓（三轮 C/C/F——D2 锚点适用类轮方差） |
| 68 | qdrant_011 | qdrant | 1.18.2 | agent-h-68 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE ✓ |
| 69 | qdrant_012 | qdrant | 1.18.2 | agent-h-69 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE ✓ |
| 70 | qdrant_013 | qdrant | 1.18.2 | agent-h-70 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE ✓ |
| 71 | qdrant_014 | qdrant | 1.18.2 | agent-h-71 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓（顽固FN池一员 run3 翻正 C——错误码语义结构性取证, 三轮 F/F/C） |
| 72 | qdrant_015 | qdrant | 1.18.2 | agent-h-72 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓（GT=FP run3 错向 C；实测可能致 OOM） |
| 73 | qdrant_016 | qdrant | 1.18.2 | agent-h-73 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓ |
| 74 | qdrant_017 | qdrant | 1.18.2 | agent-h-74 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE ✓ |
| — | qdrant_015 实测注记 | | | | 2026-08-16 | — | — | 015 复现致容器 OOM Exited(137)（纪律§5.4 同 clean/run2 轮）；017 已在退出前完成；容器已重建切 1.18.3 |
| 75 | qdrant_018 | qdrant | 1.18.3 | agent-h-75 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓（三连中: fixF/run2/run3 全 C） |
| 68 | weaviate_005 | weaviate | 1.38.0 | agent-h-108 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓ |
| 69 | weaviate_006 | weaviate | 1.38.0 | agent-h-109 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓ |
| 70 | weaviate_007 | weaviate | 1.38.0 | agent-h-110 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓（GT=FP run3 错向 C——三轮 C/F/C 方差带） |
| 71 | weaviate_008 | weaviate | 1.38.0 | agent-h-111 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓ |
| 72 | weaviate_009 | weaviate | 1.38.2 | agent-h-114 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE ✓（三轮 C/F/F） |
| 73 | weaviate_010 | weaviate | 1.38.2 | agent-h-75R | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓（G 锚点四连中 fixG/fixF/run2/run3; 首派判词 verdict 字段与 rationale 矛盾→VOID 重判, 见 VOID_LOG） |

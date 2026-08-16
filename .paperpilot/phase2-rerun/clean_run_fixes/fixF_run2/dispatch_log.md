# fixF_run2 派发记录表（最终配置轮间方差复测 run2，70 重判 + milvus_001 沿用 clean）

配置 = fixF 完全一致（fixA 锚点 + qdrant 13 锚点 + C/G 锚点 + 契约 M1/M2/Q1/Q2 + fixH 001/002 + fixI range_insert_001 + 原版 SOP）。MF 176，本轮零材料改动。
容器组：milvus 2.6.10(002-007)→2.6.12(008)→2.6.16(009-020)→2.6.17(021-031)→2.6.19(032-033)→3.0.0(034-043)；qdrant 1.12.1(001)→1.18.0(002-004)→1.18.1(005-006)→1.18.2(007-017)→1.18.3(018)；weaviate 1.37.4(001-004)→1.38.0(005-008)→1.38.2(009-010)。三 vendor 异容器并行、组内串行、切组前核对容器版本。
派发 = clean_run/prompts/{did}.txt 生成器原文 + 防呆段（同 fixF）。

| # | did | vendor | version | reviewer 会话 | 派发时间 | 判词 | 校验 | 备注 |
|---|-----|--------|---------|--------------|---------|------|------|------|
| 1 | milvus_001 | milvus | 2.3 | — | — | FALSE_POSITIVE | 沿用 | GT=CONFIRMED ✗ 沿用 clean（同 fixF） |
| 2 | milvus_002 | milvus | 2.6.10 | agent-g-02 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓ |
| 3 | milvus_003 | milvus | 2.6.10 | agent-g-03 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓ |
| 4 | milvus_004 | milvus | 2.6.10 | agent-g-04 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=CONFIRMED ✗ |
| 5 | milvus_005 | milvus | 2.6.10 | agent-g-05 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=CONFIRMED ✗ |
| 6 | milvus_006 | milvus | 2.6.10 | agent-g-06 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓ |
| 7 | milvus_007 | milvus | 2.6.10 | agent-g-07 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE ✓ |
| 55 | qdrant_002 | qdrant | 1.18.0 | agent-g-55 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓ |
| 56 | qdrant_003 | qdrant | 1.18.0 | agent-g-56 | 2026-08-16 | CONFIRMED | PASS | GT=FALSE_POSITIVE ✗ |
| 57 | qdrant_004 | qdrant | 1.18.0 | agent-g-57 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓ |
| 64 | weaviate_001 | weaviate | 1.37.4 | agent-g-64 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓ |
| 65 | weaviate_002 | weaviate | 1.37.4 | agent-g-65 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓ |
| 66 | weaviate_003 | weaviate | 1.37.4 | agent-g-66 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓ |
| 67 | weaviate_004 | weaviate | 1.37.4 | agent-g-67 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE ✓ |
| 8 | milvus_008 | milvus | 2.6.12 | agent-g-08 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=CONFIRMED ✗（fixF 轮 C；run2 审出 by-design 注释→漂移回FP） |
| 9 | milvus_009 | milvus | 2.6.16 | agent-g-09 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓ |
| 10 | milvus_010 | milvus | 2.6.16 | agent-g-10 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=CONFIRMED ✗ |
| 11 | milvus_011 | milvus | 2.6.16 | agent-g-11 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE ✓ |
| 12 | milvus_012 | milvus | 2.6.16 | agent-g-12 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=CONFIRMED ✗ |
| 13 | milvus_013 | milvus | 2.6.16 | agent-g-13 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=CONFIRMED ✗ |
| 14 | milvus_014 | milvus | 2.6.16 | agent-g-14 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE ✓ |
| 15 | milvus_015 | milvus | 2.6.16 | agent-g-15 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE ✓ |
| 16 | milvus_016 | milvus | 2.6.16 | agent-g-16 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓ |
| 17 | milvus_017 | milvus | 2.6.16 | agent-g-17 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓ |
| 18 | milvus_018 | milvus | 2.6.16 | agent-g-18 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE ✓ |
| 19 | milvus_019 | milvus | 2.6.16 | agent-g-19 | 2026-08-16 | CONFIRMED | PASS | GT=FALSE_POSITIVE ✗（GT=FP 但 reviewer 独立发现 get_stats rowCount=0 真现象→漂移错向） |
| 20 | milvus_020 | milvus | 2.6.16 | agent-g-20 | 2026-08-16 | CONFIRMED | PASS | GT=FALSE_POSITIVE ✗ |
| 21 | milvus_021 | milvus | 2.6.17 | agent-g-21 | 2026-08-16 | CONFIRMED | PASS | GT=FALSE_POSITIVE ✗ |
| 22 | milvus_022 | milvus | 2.6.17 | agent-g-22 | 2026-08-16 | CONFIRMED | PASS | GT=FALSE_POSITIVE ✗（fixE/fixH 断言修复后 fixF F 对向；run2 漂移 C——契约方向同向但 reviewer 消费失效, 轮方差） |
| 23 | milvus_023 | milvus | 2.6.17 | agent-g-23 | 2026-08-16 | CONFIRMED | PASS | GT=FALSE_POSITIVE ✗ |
| 24 | milvus_024 | milvus | 2.6.17 | agent-g-24 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓ |
| 25 | milvus_025 | milvus | 2.6.17 | agent-g-25 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE ✓ |
| 26 | milvus_026 | milvus | 2.6.17 | agent-g-26 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE ✓（fixF F 对向首现；run2 漂移 C） |
| 27 | milvus_027 | milvus | 2.6.17 | agent-g-27 | 2026-08-16 | CONFIRMED | PASS | GT=FALSE_POSITIVE ✗ |
| 28 | milvus_028 | milvus | 2.6.17 | agent-g-28 | 2026-08-16 | CONFIRMED | PASS | GT=FALSE_POSITIVE ✗（fixA 锚点副作用面已知） |
| 29 | milvus_029 | milvus | 2.6.17 | agent-g-29 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=CONFIRMED ✗ |
| 30 | milvus_030 | milvus | 2.6.17 | agent-g-30 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=CONFIRMED ✗ |
| 31 | milvus_031 | milvus | 2.6.17 | agent-g-31 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓（三轮四判：fixG C✓/fixH F✗/fixF F✗/run2 C✓——审 enableDynamicField 次现象+锚点消费, 现象漂移概率性再实证） |
| 32 | milvus_032 | milvus | 2.6.19 | agent-g-32 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓ |
| 33 | milvus_033 | milvus | 2.6.19 | agent-g-33 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=CONFIRMED ✗ |
| 34 | milvus_034 | milvus | 3.0.0 | agent-g-34 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=CONFIRMED ✗ |
| 35 | milvus_035 | milvus | 3.0.0 | agent-g-35 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=CONFIRMED ✗ |
| 36 | milvus_036 | milvus | 3.0.0 | agent-g-36 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=CONFIRMED ✗ |
| 37 | milvus_037 | milvus | 3.0.0 | agent-g-37 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=CONFIRMED ✗ |
| 38 | milvus_038 | milvus | 3.0.0 | agent-g-38 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=CONFIRMED ✗ |
| 39 | milvus_039 | milvus | 3.0.0 | agent-g-39 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓ |
| 40 | milvus_040 | milvus | 3.0.0 | agent-g-40 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓ |
| 41 | milvus_041 | milvus | 3.0.0 | agent-g-41 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓ |
| 42 | milvus_042 | milvus | 3.0.0 | agent-g-42 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓ |
| 43 | milvus_043 | milvus | 3.0.0 | agent-g-43 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓ |
| 54 | qdrant_001 | qdrant | 1.12.1 | agent-g-54 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓ |
| 58 | qdrant_005 | qdrant | 1.18.1 | agent-g-58 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE ✓ |
| 59 | qdrant_006 | qdrant | 1.18.1 | agent-g-59 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE ✓ |
| 60 | qdrant_007 | qdrant | 1.18.2 | agent-g-60 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE ✓ |
| 61 | qdrant_008 | qdrant | 1.18.2 | agent-g-61 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE ✓ |
| 62 | qdrant_009 | qdrant | 1.18.2 | agent-g-62 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE ✓ |
| 63 | qdrant_010 | qdrant | 1.18.2 | agent-g-63 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE ✓（fixE 断言修复类 Q1 适用; fixF 轮漂移错向 C, run2 回 F 对向） |
| 68 | qdrant_011 | qdrant | 1.18.2 | agent-g-68 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE ✓ |
| 69 | qdrant_012 | qdrant | 1.18.2 | agent-g-69 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE ✓ |
| 70 | qdrant_013 | qdrant | 1.18.2 | agent-g-70 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE ✓ |
| 71 | qdrant_014 | qdrant | 1.18.2 | agent-g-71 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=CONFIRMED ✗ |
| 72 | qdrant_015 | qdrant | 1.18.2 | agent-g-72 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=CONFIRMED ✗（conf 0.5 低置信；excerpt=描述性检索结论非源码原文——clean 轮同退化模式, 已归档; 备注） |
| 73 | qdrant_016 | qdrant | 1.18.2 | agent-g-73 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓ |
| 74 | qdrant_017 | qdrant | 1.18.2 | agent-g-74 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE ✓ |
| 75 | qdrant_018 | qdrant | 1.18.3 | agent-g-75 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓ |
| 68 | weaviate_005 | weaviate | 1.38.0 | agent-g-108 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓ |
| 69 | weaviate_006 | weaviate | 1.38.0 | agent-g-109 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓ |
| 70 | weaviate_007 | weaviate | 1.38.0 | agent-g-110 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=CONFIRMED ✗ |
| 71 | weaviate_008 | weaviate | 1.38.0 | agent-g-111 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=CONFIRMED ✗ |
| 72 | weaviate_009 | weaviate | 1.38.2 | agent-g-114 | 2026-08-16 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE ✓（fixG 轮曾 C 翻正、fixF 轮 C 漂移错向; run2 回 F 对向——三轮方差实证） |
| 73 | weaviate_010 | weaviate | 1.38.2 | agent-g-115 | 2026-08-16 | CONFIRMED | PASS | GT=CONFIRMED ✓（G 锚点三连中：fixG/fixF/run2 全翻正, 判词直接引用 PR 12049/12040/11878/12262） |

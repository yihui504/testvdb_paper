# fixF 派发记录表（最终配置全量单轮快照，70 重判 + milvus_001 沿用 clean）

配置 = fixA 锚点 + qdrant 13 锚点 + C/G 锚点 + 契约 M1/M2/Q1/Q2 + fixH 001/002 + fixI range_insert_001 + 原版 SOP。
容器组：milvus 2.6.10(002-007)→2.6.12(008)→2.6.16(009-020)→2.6.17(021-031)→2.6.19(032-033)→3.0.0(034-043)；qdrant 1.12.1(001)→1.18.0(002-004)→1.18.1(005-006)→1.18.2(007-017)→1.18.3(018)；weaviate 1.37.4(001-004)→1.38.0(005-008)→1.38.2(009-010)。三 vendor 异容器并行、组内串行、切组前核对容器版本。
派发 = clean_run/prompts/{did}.txt 生成器原文 + 防呆段（同 fixG/H）。

| # | did | vendor | version | reviewer 会话 | 派发时间 | 判词 | 校验 | 备注 |
|---|-----|--------|---------|--------------|---------|------|------|------|
| 1 | milvus_001 | milvus | 2.3 | agent-f-01 | FALSE_POSITIVE | PASS | GT=CONFIRMED fixF=FALSE_POSITIVE ✗ 沿用clean |
| 2 | milvus_002 | milvus | 2.6.10 | agent-f-02 | CONFIRMED | PASS | GT=CONFIRMED fixF=CONFIRMED ✓ |
| 3 | milvus_003 | milvus | 2.6.10 | agent-f-03 | CONFIRMED | PASS | GT=CONFIRMED fixF=CONFIRMED ✓ |
| 4 | milvus_004 | milvus | 2.6.10 | agent-f-04 | FALSE_POSITIVE | PASS | GT=CONFIRMED fixF=FALSE_POSITIVE ✗ |
| 5 | milvus_005 | milvus | 2.6.10 | agent-f-05 | CONFIRMED | PASS | GT=CONFIRMED fixF=CONFIRMED ✓ |
| 6 | milvus_006 | milvus | 2.6.10 | agent-f-06 | CONFIRMED | PASS | GT=CONFIRMED fixF=CONFIRMED ✓ |
| 7 | milvus_007 | milvus | 2.6.10 | agent-f-07 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE fixF=FALSE_POSITIVE ✓ |
| 8 | milvus_008 | milvus | 2.6.12 | agent-f-08 | CONFIRMED | PASS | GT=CONFIRMED fixF=CONFIRMED ✓ |
| 9 | milvus_009 | milvus | 2.6.16 | agent-f-09 | FALSE_POSITIVE | PASS | GT=CONFIRMED fixF=FALSE_POSITIVE ✗ |
| 10 | milvus_010 | milvus | 2.6.16 | agent-f-10 | CONFIRMED | PASS | GT=CONFIRMED fixF=CONFIRMED ✓ |
| 11 | milvus_011 | milvus | 2.6.16 | agent-f-11 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE fixF=FALSE_POSITIVE ✓ |
| 12 | milvus_012 | milvus | 2.6.16 | agent-f-12 | FALSE_POSITIVE | PASS | GT=CONFIRMED fixF=FALSE_POSITIVE ✗ |
| 13 | milvus_013 | milvus | 2.6.16 | agent-f-13 | CONFIRMED | PASS | GT=CONFIRMED fixF=CONFIRMED ✓ |
| 14 | milvus_014 | milvus | 2.6.16 | agent-f-14 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE fixF=FALSE_POSITIVE ✓ |
| 15 | milvus_015 | milvus | 2.6.16 | agent-f-15 | CONFIRMED | PASS | GT=FALSE_POSITIVE fixF=CONFIRMED ✗ |
| 16 | milvus_016 | milvus | 2.6.16 | agent-f-16 | CONFIRMED | PASS | GT=CONFIRMED fixF=CONFIRMED ✓ |
| 17 | milvus_017 | milvus | 2.6.16 | agent-f-17 | CONFIRMED | PASS | GT=CONFIRMED fixF=CONFIRMED ✓ |
| 18 | milvus_018 | milvus | 2.6.16 | agent-f-18 | CONFIRMED | PASS | GT=FALSE_POSITIVE fixF=CONFIRMED ✗ |
| 19 | milvus_019 | milvus | 2.6.16 | agent-f-19 | CONFIRMED | PASS | GT=FALSE_POSITIVE fixF=CONFIRMED ✗ |
| 20 | milvus_020 | milvus | 2.6.16 | agent-f-20 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE fixF=FALSE_POSITIVE ✓ |
| 21 | milvus_021 | milvus | 2.6.17 | agent-f-21 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE fixF=FALSE_POSITIVE ✓ |
| 22 | milvus_022 | milvus | 2.6.17 | agent-f-22 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE fixF=FALSE_POSITIVE ✓ |
| 23 | milvus_023 | milvus | 2.6.17 | agent-f-23 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE fixF=FALSE_POSITIVE ✓ |
| 24 | milvus_024 | milvus | 2.6.17 | agent-f-24 | FALSE_POSITIVE | PASS | GT=CONFIRMED fixF=FALSE_POSITIVE ✗ |
| 25 | milvus_025 | milvus | 2.6.17 | agent-f-25 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE fixF=FALSE_POSITIVE ✓ |
| 26 | milvus_026 | milvus | 2.6.17 | agent-f-26 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE fixF=FALSE_POSITIVE ✓ |
| 27 | milvus_027 | milvus | 2.6.17 | agent-f-27 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE fixF=FALSE_POSITIVE ✓ |
| 28 | milvus_028 | milvus | 2.6.17 | agent-f-28 | CONFIRMED | PASS | GT=FALSE_POSITIVE fixF=CONFIRMED ✗ |
| 29 | milvus_029 | milvus | 2.6.17 | agent-f-29 | FALSE_POSITIVE | PASS | GT=CONFIRMED fixF=FALSE_POSITIVE ✗ |
| 30 | milvus_030 | milvus | 2.6.17 | agent-f-30 | FALSE_POSITIVE | PASS | GT=CONFIRMED fixF=FALSE_POSITIVE ✗ |
| 31 | milvus_031 | milvus | 2.6.17 | agent-f-31 | FALSE_POSITIVE | PASS | GT=CONFIRMED fixF=FALSE_POSITIVE ✗ |
| 32 | milvus_032 | milvus | 2.6.19 | agent-f-32 | CONFIRMED | PASS | GT=CONFIRMED fixF=CONFIRMED ✓ |
| 33 | milvus_033 | milvus | 2.6.19 | agent-f-33 | CONFIRMED | PASS | GT=CONFIRMED fixF=CONFIRMED ✓ |
| 34 | milvus_034 | milvus | 3.0.0 | agent-f-34 | CONFIRMED | PASS | GT=CONFIRMED fixF=CONFIRMED ✓ |
| 35 | milvus_035 | milvus | 3.0.0 | agent-f-35 | FALSE_POSITIVE | PASS | GT=CONFIRMED fixF=FALSE_POSITIVE ✗ |
| 36 | milvus_036 | milvus | 3.0.0 | agent-f-36 | CONFIRMED | PASS | GT=CONFIRMED fixF=CONFIRMED ✓ |
| 37 | milvus_037 | milvus | 3.0.0 | agent-f-37 | CONFIRMED | PASS | GT=CONFIRMED fixF=CONFIRMED ✓ |
| 38 | milvus_038 | milvus | 3.0.0 | agent-f-38 | CONFIRMED | PASS | GT=CONFIRMED fixF=CONFIRMED ✓ |
| 39 | milvus_039 | milvus | 3.0.0 | agent-f-39 | FALSE_POSITIVE | PASS | GT=CONFIRMED fixF=FALSE_POSITIVE ✗ |
| 40 | milvus_040 | milvus | 3.0.0 | agent-f-40 | CONFIRMED | PASS | GT=CONFIRMED fixF=CONFIRMED ✓ |
| 41 | milvus_041 | milvus | 3.0.0 | agent-f-41 | CONFIRMED | PASS | GT=CONFIRMED fixF=CONFIRMED ✓ |
| 42 | milvus_042 | milvus | 3.0.0 | agent-f-42 | CONFIRMED | PASS | GT=CONFIRMED fixF=CONFIRMED ✓ |
| 43 | milvus_043 | milvus | 3.0.0 | agent-f-43 | CONFIRMED | PASS | GT=CONFIRMED fixF=CONFIRMED ✓ |
| 44 | qdrant_001 | qdrant | 1.12.1 | agent-f-44 | CONFIRMED | PASS | GT=CONFIRMED fixF=CONFIRMED ✓ |
| 45 | qdrant_002 | qdrant | 1.18.0 | agent-f-45 | FALSE_POSITIVE | PASS | GT=CONFIRMED fixF=FALSE_POSITIVE ✗ |
| 46 | qdrant_003 | qdrant | 1.18.0 | agent-f-46 | CONFIRMED | PASS | GT=FALSE_POSITIVE fixF=CONFIRMED ✗ |
| 47 | qdrant_004 | qdrant | 1.18.0 | agent-f-47 | FALSE_POSITIVE | PASS | GT=CONFIRMED fixF=FALSE_POSITIVE ✗ |
| 48 | qdrant_005 | qdrant | 1.18.1 | agent-f-48 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE fixF=FALSE_POSITIVE ✓ |
| 49 | qdrant_006 | qdrant | 1.18.1 | agent-f-49 | CONFIRMED | PASS | GT=FALSE_POSITIVE fixF=CONFIRMED ✗ |
| 50 | qdrant_007 | qdrant | 1.18.2 | agent-f-50 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE fixF=FALSE_POSITIVE ✓ |
| 51 | qdrant_008 | qdrant | 1.18.2 | agent-f-51 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE fixF=FALSE_POSITIVE ✓ |
| 52 | qdrant_009 | qdrant | 1.18.2 | agent-f-52 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE fixF=FALSE_POSITIVE ✓ |
| 53 | qdrant_010 | qdrant | 1.18.2 | agent-f-53 | CONFIRMED | PASS | GT=FALSE_POSITIVE fixF=CONFIRMED ✗ |
| 54 | qdrant_011 | qdrant | 1.18.2 | agent-f-54 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE fixF=FALSE_POSITIVE ✓ |
| 55 | qdrant_012 | qdrant | 1.18.2 | agent-f-55 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE fixF=FALSE_POSITIVE ✓ |
| 56 | qdrant_013 | qdrant | 1.18.2 | agent-f-56 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE fixF=FALSE_POSITIVE ✓ |
| 57 | qdrant_014 | qdrant | 1.18.2 | agent-f-57 | FALSE_POSITIVE | PASS | GT=CONFIRMED fixF=FALSE_POSITIVE ✗ |
| 58 | qdrant_015 | qdrant | 1.18.2 | agent-f-58 | CONFIRMED | PASS | GT=CONFIRMED fixF=CONFIRMED ✓ |
| 59 | qdrant_016 | qdrant | 1.18.2 | agent-f-59 | FALSE_POSITIVE | PASS | GT=CONFIRMED fixF=FALSE_POSITIVE ✗ |
| 60 | qdrant_017 | qdrant | 1.18.2 | agent-f-60 | FALSE_POSITIVE | PASS | GT=FALSE_POSITIVE fixF=FALSE_POSITIVE ✓ |
| 61 | qdrant_018 | qdrant | 1.18.3 | agent-f-61 | CONFIRMED | PASS | GT=CONFIRMED fixF=CONFIRMED ✓ |
| 62 | weaviate_001 | weaviate | 1.37.4 | agent-f-62 | CONFIRMED | PASS | GT=CONFIRMED fixF=CONFIRMED ✓ |
| 63 | weaviate_002 | weaviate | 1.37.4 | agent-f-63 | CONFIRMED | PASS | GT=CONFIRMED fixF=CONFIRMED ✓ |
| 64 | weaviate_003 | weaviate | 1.37.4 | agent-f-64 | CONFIRMED | PASS | GT=CONFIRMED fixF=CONFIRMED ✓ |
| 65 | weaviate_004 | weaviate | 1.37.4 | agent-f-65 | CONFIRMED | PASS | GT=FALSE_POSITIVE fixF=CONFIRMED ✗ |
| 66 | weaviate_005 | weaviate | 1.38.0 | agent-f-66 | CONFIRMED | PASS | GT=CONFIRMED fixF=CONFIRMED ✓ |
| 67 | weaviate_006 | weaviate | 1.38.0 | agent-f-67 | CONFIRMED | PASS | GT=CONFIRMED fixF=CONFIRMED ✓ |
| 68 | weaviate_007 | weaviate | 1.38.0 | agent-f-68 | CONFIRMED | PASS | GT=CONFIRMED fixF=CONFIRMED ✓ |
| 69 | weaviate_008 | weaviate | 1.38.0 | agent-f-69 | FALSE_POSITIVE | PASS | GT=CONFIRMED fixF=FALSE_POSITIVE ✗ |
| 70 | weaviate_009 | weaviate | 1.38.2 | agent-f-70 | CONFIRMED | PASS | GT=FALSE_POSITIVE fixF=CONFIRMED ✗ |
| 71 | weaviate_010 | weaviate | 1.38.2 | agent-f-71 | CONFIRMED | PASS | GT=CONFIRMED fixF=CONFIRMED ✓ |

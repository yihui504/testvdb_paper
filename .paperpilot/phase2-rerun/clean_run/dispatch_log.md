# clean_run 派发记录表（纪律 §7.1）

> Run 标识：**clean**（2026-08-14 起）。材料包 v2（audit 0 FAIL）；派发 prompt = gen_dispatch_v2.py 单 case 生成（clean_run/prompts/，泄漏扫描 0 命中）。
> 模型：统一标准档 GLM-5.2（每 case 新会话 = 新 reviewer，默认档）。
> 顺序：同容器内 case 串行；3 vendor 容器并行。

| # | did | vendor | version | reviewer 会话 | 派发时间 | 判词 | 校验 | 备注 |
|---|-----|--------|---------|--------------|---------|------|------|------|
| 1 | weaviate_009 | weaviate | 1.38.2 | agent-r01 | 2026-08-14 | CONFIRMED | PASS | GT=B组CONFIRMED 判对 |
| 2 | weaviate_010 | weaviate | 1.38.2 | agent-r02 | 2026-08-14 | FALSE_POSITIVE | PASS | GT=B组CONFIRMED→FN; 源码接地找到by-design校验 |
| 3 | milvus_001 | milvus | 2.3 | agent-r03 | 2026-08-14 | FALSE_POSITIVE | 例外(见VOID_LOG) | 空日志→2次会话系统性放弃,接受并披露; 历史三轮同材料CONFIRMED |
| 4 | weaviate_001 | weaviate | 1.37.4 | agent-r04 | 2026-08-14 | CONFIRMED | PASS | GT=B组CONFIRMED 判对 |
| 5 | milvus_002 | milvus | 2.6.10 | agent-r05 | 2026-08-14 | CONFIRMED | PASS |  |
| 6 | weaviate_002 | weaviate | 1.37.4 | agent-r06 | 2026-08-14 | CONFIRMED | PASS |  |
| 7 | milvus_003 | milvus | 2.6.10 | agent-r07 | 2026-08-14 | CONFIRMED | PASS |  |
| 8 | weaviate_003 | weaviate | 1.37.4 | agent-r08 | 2026-08-14 | CONFIRMED | PASS | factor=-1静默纠正 |
| 9 | milvus_004 | milvus | 2.6.10 | agent-r09 | 2026-08-14 | FALSE_POSITIVE | PASS | GT=A组CONFIRMED→FN |
| 10 | weaviate_004 | weaviate | 1.37.4 | agent-r10 | 2026-08-14 | FALSE_POSITIVE | PASS | ef=-1 sentinel by-design |
| 11 | milvus_005 | milvus | 2.6.10 | agent-r11 | 2026-08-14 | FALSE_POSITIVE | PASS |  |
| 12 | milvus_006 | milvus | 2.6.10 | agent-r12 | 2026-08-14 | CONFIRMED | PASS |  |
| 13 | weaviate_005 | weaviate | 1.38.0 | agent-r13 | 2026-08-14 | CONFIRMED | PASS |  |
| 14 | milvus_007 | milvus | 2.6.10 | agent-r14 | 2026-08-14 | FALSE_POSITIVE | PASS |  |
| 15 | weaviate_006 | weaviate | 1.38.0 | agent-r15 | 2026-08-14 | FALSE_POSITIVE | PASS |  |
| 16 | qdrant_001 | qdrant | 1.12.1 | agent-r16 | 2026-08-14 | CONFIRMED | PASS |  |
| 17 | milvus_008 | milvus | 2.6.12 | agent-r17 | 2026-08-14 | FALSE_POSITIVE | PASS |  |
| 18 | weaviate_007 | weaviate | 1.38.0 | agent-r18 | 2026-08-14 | CONFIRMED | PASS |  |
| 19 | qdrant_002 | qdrant | 1.18.0 | agent-r19 | 2026-08-14 | FALSE_POSITIVE | PASS |  |
| 20 | milvus_009 | milvus | 2.6.16 | agent-r20 | 2026-08-14 | CONFIRMED | PASS |  |
| 21 | weaviate_008 | weaviate | 1.38.0 | agent-r21 | 2026-08-14 | CONFIRMED | PASS |  |
| 22 | qdrant_003 | qdrant | 1.18.0 | agent-r22 | 2026-08-14 | FALSE_POSITIVE | PASS |  |
| 23 | milvus_010 | milvus | 2.6.16 | agent-r23 | 2026-08-14 | CONFIRMED | PASS |  |
| 24 | qdrant_004 | qdrant | 1.18.0 | agent-r24 | 2026-08-14 | CONFIRMED | PASS |  |
| 25 | milvus_011 | milvus | 2.6.16 | agent-r25 | 2026-08-14 | CONFIRMED | PASS |  |
| 26 | qdrant_005 | qdrant | 1.18.1 | agent-r26 | 2026-08-14 | FALSE_POSITIVE | PASS | GT=A组CONFIRMED→FN; 9149 GT存疑case(audit-report §2: dev判对GT错), 分析时披露 |
| 27 | milvus_012 | milvus | 2.6.16 | agent-r27 | 2026-08-14 | FALSE_POSITIVE | PASS |  |
| 28 | qdrant_006 | qdrant | 1.18.1 | agent-r28 | 2026-08-14 | FALSE_POSITIVE | PASS | GT=C组FP→TN判对(#9255 fixture原型) |
| 29 | milvus_013 | milvus | 2.6.16 | agent-r29 | 2026-08-14 | FALSE_POSITIVE | PASS |  |
| 30 | qdrant_007 | qdrant | 1.18.1 | agent-r30 | 2026-08-14 | FALSE_POSITIVE | PASS |  |
| 31 | milvus_014 | milvus | 2.6.16 | agent-r31 | 2026-08-14 | FALSE_POSITIVE | PASS |  |
| 32 | qdrant_007 | qdrant | 1.18.2 | agent-r32 | 2026-08-14 | FALSE_POSITIVE | PASS | 重判: 首派prompt版本误写1.18.1(编排失误,已void); 本次按生成器原文1.18.2 |
| 33 | milvus_015 | milvus | 2.6.16 | agent-r33 | 2026-08-14 | FALSE_POSITIVE | PASS |  |
| 34 | qdrant_008 | qdrant | 1.18.2 | agent-r34 | 2026-08-14 | FALSE_POSITIVE | PASS |  |
| 35 | milvus_016 | milvus | 2.6.16 | agent-r35 | 2026-08-14 | CONFIRMED | PASS |  |
| 36 | qdrant_009 | qdrant | 1.18.2 | agent-r36 | 2026-08-14 | FALSE_POSITIVE | PASS |  |
| 37 | milvus_017 | milvus | 2.6.16 | agent-r37 | 2026-08-14 | FALSE_POSITIVE | PASS |  |
| 38 | qdrant_009 | qdrant | 1.18.2 | agent-r38 | 2026-08-14 | FALSE_POSITIVE | PASS | 重判(首判JSON损坏已void) |
| 39 | milvus_018 | milvus | 2.6.16 | agent-r39 | 2026-08-14 | CONFIRMED | PASS |  |
| 40 | qdrant_010 | qdrant | 1.18.2 | agent-r40 | 2026-08-14 | FALSE_POSITIVE | PASS |  |
| 40 | milvus_018 | milvus | 2.6.16 | agent-r40 | 2026-08-14 | FALSE_POSITIVE | PASS | 重判(首判格式平铺已void); 重判结果与首判相反 |
| 41 | qdrant_011 | qdrant | 1.18.2 | agent-r41 | 2026-08-14 | CONFIRMED | PASS |  |
| 42 | milvus_019 | milvus | 2.6.16 | agent-r42 | 2026-08-14 | CONFIRMED | PASS |  |
| 43 | qdrant_012 | qdrant | 1.18.2 | agent-r43 | 2026-08-14 | CONFIRMED | PASS |  |
| 44 | milvus_020 | milvus | 2.6.16 | agent-r44 | 2026-08-14 | CONFIRMED | PASS |  |
| 45 | qdrant_013 | qdrant | 1.18.2 | agent-r45 | 2026-08-14 | FALSE_POSITIVE | PASS |  |
| 46 | milvus_008 | milvus | 2.6.12 | agent-r46 | 2026-08-14 | FALSE_POSITIVE | PASS | 重判(首判JSON损坏已void) |
| 47 | qdrant_014 | qdrant | 1.18.2 | agent-r47 | 2026-08-14 | FALSE_POSITIVE | PASS |  |
| 47 | qdrant_015 | qdrant | 1.18.2 | agent-r47 | 2026-08-14 | CONFIRMED | PASS | INT_MAX shard实测致容器OOM退出(137); 容器已重建 |
| 49 | milvus_021 | milvus | 2.6.17 | agent-r49 | 2026-08-14 | FALSE_POSITIVE | PASS | 重派(首派连接中断无判词; milvus容器Exited1已重建) |
| 50 | qdrant_016 | qdrant | 1.18.2 | agent-r50 | 2026-08-14 | CONFIRMED | PASS |  |
| 51 | milvus_022 | milvus | 2.6.17 | agent-r51 | 2026-08-15 | CONFIRMED | PASS |  |
| 52 | qdrant_017 | qdrant | 1.18.2 | agent-r52 | 2026-08-15 | FALSE_POSITIVE | PASS |  |
| 53 | milvus_023 | milvus | 2.6.17 | agent-r53 | 2026-08-15 | CONFIRMED | PASS |  |
| 54 | qdrant_018 | qdrant | 1.18.3 | agent-r54 | 2026-08-15 | CONFIRMED | PASS |  |
| 54 | milvus_024 | milvus | 2.6.17 | agent-r54 | 2026-08-15 | FALSE_POSITIVE | PASS |  |
| 55 | milvus_025 | milvus | 2.6.17 | agent-r55 | 2026-08-15 | CONFIRMED | PASS |  |
| 56 | milvus_026 | milvus | 2.6.17 | agent-r56 | 2026-08-15 | FALSE_POSITIVE | PASS |  |
| 57 | milvus_027 | milvus | 2.6.17 | agent-r57 | 2026-08-15 | CONFIRMED | PASS |  |
| 58 | milvus_028 | milvus | 2.6.17 | agent-r58 | 2026-08-15 | CONFIRMED | PASS |  |
| 59 | milvus_029 | milvus | 2.6.17 | agent-r59 | 2026-08-15 | FALSE_POSITIVE | PASS |  |
| 60 | milvus_030 | milvus | 2.6.17 | agent-r60 | 2026-08-15 | CONFIRMED | PASS |  |
| 61 | milvus_031 | milvus | 2.6.17 | agent-r61 | 2026-08-15 | FALSE_POSITIVE | PASS |  |
| 62 | milvus_032 | milvus | 2.6.19 | agent-r62 | 2026-08-15 | CONFIRMED | PASS |  |
| 63 | milvus_033 | milvus | 2.6.19 | agent-r63 | 2026-08-15 | CONFIRMED | PASS |  |
| 64 | milvus_034 | milvus | 3.0.0 | agent-r64 | 2026-08-15 | CONFIRMED | PASS |  |
| 65 | milvus_035 | milvus | 3.0.0 | agent-r65 | 2026-08-15 | FALSE_POSITIVE | PASS |  |
| 66 | milvus_036 | milvus | 3.0.0 | agent-r66 | 2026-08-15 | CONFIRMED | PASS |  |
| 67 | milvus_037 | milvus | 3.0.0 | agent-r67 | 2026-08-15 | FALSE_POSITIVE | PASS |  |
| 68 | milvus_038 | milvus | 3.0.0 | agent-r68 | 2026-08-15 | FALSE_POSITIVE | PASS |  |
| 69 | milvus_039 | milvus | 3.0.0 | agent-r69 | 2026-08-15 | FALSE_POSITIVE | PASS |  |
| 70 | milvus_040 | milvus | 3.0.0 | agent-r70 | 2026-08-15 | CONFIRMED | PASS |  |
| 71 | milvus_041 | milvus | 3.0.0 | agent-r71 | 2026-08-15 | FALSE_POSITIVE | PASS |  |
| 72 | milvus_042 | milvus | 3.0.0 | agent-r72 | 2026-08-15 | FALSE_POSITIVE | PASS |  |
| 73 | milvus_043 | milvus | 3.0.0 | agent-r73 | 2026-08-15 | CONFIRMED | PASS | 71/71 完成; 容器全清 |

# arm-sl-run3 派发记录表（single-LLM 臂第 3轮）

> 配置与 run1 零改动（同 prompt 文件复制、同 PREREG 模板）。GLM-5.2 标准档纯调用。

| # | did | vendor | 调用时间 | verdict | conf | 备注 |
|---|-----|--------|---------|------|------|------|
| 序号 | did | vendor | 时间 | verdict | conf | - |
| 1 | qdrant_006 | qdrant | 2025-01-16 | FALSE_POSITIVE | 0.9 | - |
| 2 | qdrant_007 | qdrant | 2025-01-16 | FALSE_POSITIVE | 0.85 | - |
| 3 | qdrant_008 | qdrant | 2025-01-16 | FALSE_POSITIVE | 0.9 | - |
| 4 | qdrant_009 | qdrant | 2025-01-16 | CONFIRMED | 0.95 | - |
| 5 | qdrant_010 | qdrant | 2025-01-16 | CONFIRMED | 0.95 | - |
| 6 | qdrant_011 | qdrant | 2025-01-16 | FALSE_POSITIVE | 0.8 | - |
| 7 | qdrant_012 | qdrant | 2025-01-16 | FALSE_POSITIVE | 0.9 | - |
| 8 | qdrant_013 | qdrant | 2025-01-16 | FALSE_POSITIVE | 0.7 | - |
| 9 | qdrant_014 | qdrant | 2025-01-16 | FALSE_POSITIVE | 0.85 | - |
| 10 | qdrant_015 | qdrant | 2025-01-16 | CONFIRMED | 0.9 | - |
| 11 | qdrant_016 | qdrant | 2025-01-16 | FALSE_POSITIVE | 0.8 | - |
| 12 | qdrant_017 | qdrant | 2025-01-16 | FALSE_POSITIVE | 0.9 | - |
| 13 | qdrant_018 | qdrant | 2025-01-16 | CONFIRMED | 0.95 | - |
| 14 | weaviate_001 | weaviate | 2025-01-16 | CONFIRMED | 0.95 | - |
| 15 | weaviate_002 | weaviate | 2025-01-16 | CONFIRMED | 0.95 | - |
| 16 | weaviate_003 | weaviate | 2025-01-16 | CONFIRMED | 0.95 | - |
| 17 | weaviate_004 | weaviate | 2025-01-16 | FALSE_POSITIVE | 0.85 | - |
| 18 | weaviate_005 | weaviate | 2025-01-16 | CONFIRMED | 0.9 | - |
| 19 | weaviate_006 | weaviate | 2025-01-16 | CONFIRMED | 0.95 | - |
| 20 | weaviate_007 | weaviate | 2025-01-16 | FALSE_POSITIVE | 0.8 | - |
| 21 | weaviate_008 | weaviate | 2025-01-16 | CONFIRMED | 0.95 | - |
| 22 | weaviate_009 | weaviate | 2025-01-16 | FALSE_POSITIVE | 0.85 | - |
| 23 | weaviate_010 | weaviate | 2025-01-16 | FALSE_POSITIVE | 0.9 | - |
| 1 | milvus_001-milvus_024 | milvus | 2026-08-16 19:15:10 | 9C20F | 0.772 | batch1 |
| 1 | milvus_035 | milvus | 2026-08-16 | CONFIRMED | 0.95 | - |
| 2 | milvus_036 | milvus | 2026-08-16 | CONFIRMED | 0.90 | - |
| 3 | milvus_037 | milvus | 2026-08-16 | CONFIRMED | 0.92 | - |
| 4 | milvus_038 | milvus | 2026-08-16 | CONFIRMED | 0.85 | - |
| 5 | milvus_039 | milvus | 2026-08-16 | CONFIRMED | 0.93 | - |
| 6 | milvus_040 | milvus | 2026-08-16 | CONFIRMED | 0.90 | - |
| 7 | milvus_041 | milvus | 2026-08-16 | CONFIRMED | 0.91 | - |
| 8 | milvus_042 | milvus | 2026-08-16 | CONFIRMED | 0.94 | - |
| 9 | milvus_043 | milvus | 2026-08-16 | FALSE_POSITIVE | 0.70 | - |
| 10 | qdrant_001 | qdrant | 2026-08-16 | FALSE_POSITIVE | 0.75 | - |
| 11 | qdrant_002 | qdrant | 2026-08-16 | CONFIRMED | 0.88 | - |
| 12 | qdrant_003 | qdrant | 2026-08-16 | FALSE_POSITIVE | 0.65 | - |
| 13 | qdrant_004 | qdrant | 2026-08-16 | FALSE_POSITIVE | 0.70 | - |
| 14 | qdrant_005 | qdrant | 2026-08-16 | FALSE_POSITIVE | 0.80 | - |
| 1 | milvus_025 | milvus | 2026-08-16 19:23:58 | FALSE_POSITIVE | 0.90 | - |
| 2 | milvus_026 | milvus | 2026-08-16 19:23:58 | FALSE_POSITIVE | 0.85 | - |
| 3 | milvus_027 | milvus | 2026-08-16 19:23:58 | CONFIRMED | 0.95 | - |
| 4 | milvus_028 | milvus | 2026-08-16 19:23:58 | CONFIRMED | 0.90 | - |
| 5 | milvus_029 | milvus | 2026-08-16 19:23:58 | FALSE_POSITIVE | 0.85 | - |
| 6 | milvus_030 | milvus | 2026-08-16 19:23:58 | CONFIRMED | 0.80 | - |
| 7 | milvus_031 | milvus | 2026-08-16 19:23:58 | FALSE_POSITIVE | 0.85 | - |
| 8 | milvus_032 | milvus | 2026-08-16 19:23:58 | CONFIRMED | 0.90 | - |
| 9 | milvus_033 | milvus | 2026-08-16 19:23:58 | CONFIRMED | 0.90 | - |
| 10 | milvus_034 | milvus | 2026-08-16 19:23:58 | CONFIRMED | 0.95 | - |
| 11 | milvus_035 | milvus | 2026-08-16 19:23:58 | CONFIRMED | 0.95 | - |
| 12 | milvus_036 | milvus | 2026-08-16 19:23:58 | CONFIRMED | 0.90 | - |
| 13 | milvus_037 | milvus | 2026-08-16 19:23:58 | CONFIRMED | 0.95 | - |
| 14 | milvus_038 | milvus | 2026-08-16 19:23:58 | FALSE_POSITIVE | 0.70 | - |
| 15 | milvus_039 | milvus | 2026-08-16 19:23:58 | CONFIRMED | 0.95 | - |
| 16 | milvus_040 | milvus | 2026-08-16 19:23:58 | CONFIRMED | 0.95 | - |
| 17 | milvus_041 | milvus | 2026-08-16 19:23:58 | CONFIRMED | 0.95 | - |
| 18 | milvus_042 | milvus | 2026-08-16 19:23:58 | CONFIRMED | 0.95 | - |
| 19 | milvus_043 | milvus | 2026-08-16 19:23:58 | FALSE_POSITIVE | 0.80 | - |
| 20 | qdrant_001 | qdrant | 2026-08-16 19:23:58 | CONFIRMED | 0.90 | - |
| 21 | qdrant_002 | qdrant | 2026-08-16 19:23:58 | FALSE_POSITIVE | 0.85 | - |
| 22 | qdrant_003 | qdrant | 2026-08-16 19:23:58 | FALSE_POSITIVE | 0.80 | - |
| 23 | qdrant_004 | qdrant | 2026-08-16 19:23:58 | CONFIRMED | 0.90 | - |
| 24 | qdrant_005 | qdrant | 2026-08-16 19:23:58 | FALSE_POSITIVE | 0.95 | - |

> **429 事故记录**：run2 批次1/2 与 run3 批次2 因 API 速率限制中断（2026-08-16 19:13 前后）；
> 补跑批次 b1b(15)/b2b(23)/run3-b2b(14) 串行化完成，零缺口。run3 milvus_042
> rationale 未转义引号致 JSON 损坏，机械修复（引号→单引号，判词不变）。

# arm-sl-run2 派发记录表（single-LLM 臂第 2轮）

> 配置与 run1 零改动（同 prompt 文件复制、同 PREREG 模板）。GLM-5.2 标准档纯调用。

| # | did | vendor | 调用时间 | verdict | conf | 备注 |
|---|-----|--------|---------|------|------|------|
| 1 | qdrant_006 | qdrant | 2026-08-16 11:13:56 | FALSE_POSITIVE | 0.7 | - |
| 10 | milvus_010 | milvus | 2026-08-16 | CONFIRMED | 0.95 | - |
| 11 | milvus_011 | milvus | 2026-08-16 | FALSE_POSITIVE | 0.90 | - |
| 12 | milvus_012 | milvus | 2026-08-16 | FALSE_POSITIVE | 0.85 | - |
| 13 | milvus_013 | milvus | 2026-08-16 | FALSE_POSITIVE | 0.75 | - |
| 14 | milvus_014 | milvus | 2026-08-16 | FALSE_POSITIVE | 0.95 | - |
| 15 | milvus_015 | milvus | 2026-08-16 | FALSE_POSITIVE | 0.85 | - |
| 16 | milvus_016 | milvus | 2026-08-16 | CONFIRMED | 0.80 | - |
| 17 | milvus_017 | milvus | 2026-08-16 | CONFIRMED | 0.75 | - |
| 18 | milvus_018 | milvus | 2026-08-16 | FALSE_POSITIVE | 0.85 | - |
| 19 | milvus_019 | milvus | 2026-08-16 | CONFIRMED | 0.90 | - |
| 20 | milvus_020 | milvus | 2026-08-16 | CONFIRMED | 0.92 | - |
| 21 | milvus_021 | milvus | 2026-08-16 | CONFIRMED | 0.88 | - |
| 22 | milvus_022 | milvus | 2026-08-16 | FALSE_POSITIVE | 0.95 | - |
| 23 | milvus_023 | milvus | 2026-08-16 | FALSE_POSITIVE | 0.92 | - |
| 24 | milvus_024 | milvus | 2026-08-16 | FALSE_POSITIVE | 0.70 | - |
| 1 | milvus_026 | milvus | $(date +%Y-%m-%d\ %H:%M:%S) | FALSE_POSITIVE | 0.95 | - |

> **429 事故记录**：run2 批次1/2 与 run3 批次2 因 API 速率限制中断（2026-08-16 19:13 前后）；
> 补跑批次 b1b(15)/b2b(23)/run3-b2b(14) 串行化完成，零缺口。run3 milvus_042
> rationale 未转义引号致 JSON 损坏，机械修复（引号→单引号，判词不变）。

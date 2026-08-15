# fixE 派发记录表

| # | did | vendor | version | reviewer 会话 | 派发时间 | 判词 | 校验 | 备注 |
|---|-----|--------|---------|--------------|---------|------|------|------|
| 1 | milvus_022 | milvus | 2.6.17 | agent-e-01 | 2026-08-16 | FALSE_POSITIVE | PASS | M1 修复适用✓对向（GT=C） |
| 2 | qdrant_007 | qdrant | 1.18.2 | agent-e-02 | 2026-08-16 | FALSE_POSITIVE | PASS | Q2 修复适用✓对向——fixD 失败模式（锚点被旧契约压倒）被解除 |
| 3 | milvus_023 | milvus | 2.6.17 | agent-e-03 | 2026-08-16 | FALSE_POSITIVE | PASS | M2 修复适用✓对向 |
| 4 | qdrant_009 | qdrant | 1.18.2 | agent-e-04 | 2026-08-16 | FALSE_POSITIVE | PASS | Q1 修复适用✓对向 |
| 5 | milvus_025 | milvus | 2.6.17 | agent-e-05 | 2026-08-16 | CONFIRMED | PASS | 对照保持✓（契约 max=100 未动） |
| 6 | qdrant_010 | qdrant | 1.18.2 | agent-e-06 | 2026-08-16 | FALSE_POSITIVE | PASS | Q1 修复适用✓对向 |
| 7 | milvus_018 | milvus | 2.6.16 | agent-e-07 | 2026-08-16 | FALSE_POSITIVE | PASS | 重判(首判容器错配作废)；对照劣化✗(GT=B)——rename契约未动、引用约束与修复无涉=灰区轮方差(018 三轮 C/C/F 漂移带) |
| 8 | qdrant_002 | qdrant | 1.18.0 | agent-e-08 | 2026-08-16 | FALSE_POSITIVE | PASS | 对照劣化✗(GT=A)——hnsw_ef 约束未动=轮方差(F/F/F+C 漂移带) |

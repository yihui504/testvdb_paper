# fixD 派发记录表（纪律 §7.1）

> Run 标识：**fixD**（2026-08-15 起）。配置 = 原版 SOP + fixA 锚点 + qdrant D2/D3/D4 三锚点（FIXD_PLAN §2）。
> 派发 prompt = clean_run/prompts/ 原文；模型统一标准档 GLM-5.2（每 case 新会话）。
> 子集 = qdrant 9（fixC 同款）+ 稳定对照 013/015 = 11 case；milvus/weaviate 零重判。

| # | did | vendor | version | reviewer 会话 | 派发时间 | 判词 | 校验 | 备注 |
|---|-----|--------|---------|--------------|---------|------|------|------|
| 1 | qdrant_002 | qdrant | 1.18.0 | agent-d-01 | 2026-08-15 | CONFIRMED | PASS | gt=A 对向✓（fixC 曾错 F；本轮 B 物理驱动） |
| 2 | qdrant_003 | qdrant | 1.18.0 | agent-d-02 | 2026-08-15 | FALSE_POSITIVE | PASS | gt=C 对向✓（fixC 曾错 C；无 D1 锚点仍翻正——轮方差利好） |
| 3 | qdrant_004 | qdrant | 1.18.0 | agent-d-03 | 2026-08-15 | CONFIRMED | PASS | gt=A 对向✓ |
| 4 | qdrant_007 | qdrant | 1.18.2 | agent-d-04 | 2026-08-15 | CONFIRMED | PASS | gt=C 错向✗；判词引用 D4 锚点原文但契约A压倒未消费——锚点-契约冲突时例外条款启用随会话 |
| 5 | qdrant_009 | qdrant | 1.18.2 | agent-d-05 | 2026-08-15 | FALSE_POSITIVE | PASS | gt=C 对向✓；D2 锚点显式消费 |
| 6 | qdrant_010 | qdrant | 1.18.2 | agent-d-06 | 2026-08-15 | FALSE_POSITIVE | PASS | gt=C 对向✓；D2 消费翻正（fixC 曾错 C） |
| 7 | qdrant_011 | qdrant | 1.18.2 | agent-d-07 | 2026-08-15 | FALSE_POSITIVE | PASS | gt=C 对向✓；D3 消费 |
| 8 | qdrant_012 | qdrant | 1.18.2 | agent-d-08 | 2026-08-15 | FALSE_POSITIVE | PASS | gt=C 对向✓；D3 消费翻正（fixC 曾错 C） |
| 9 | qdrant_013 | qdrant | 1.18.2 | agent-d-09 | 2026-08-15 | FALSE_POSITIVE | PASS | 稳定对照保持✓ |
| 10 | qdrant_015 | qdrant | 1.18.2 | agent-d-10 | 2026-08-15 | FALSE_POSITIVE | PASS | 稳定对照劣化✗（gt=A fixA三轮全C对→FP）；待查判词是否锚点泛化误伤 |
| 11 | qdrant_017 | qdrant | 1.18.2 | agent-d-11 | 2026-08-15 | CONFIRMED | PASS | gt=C 错向✗（scroll offset 未实现——锚点不适用类，轮方差） |

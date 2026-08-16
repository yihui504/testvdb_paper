# fixG 派发记录表（C/G 锚点注入效果验证，8 case 单轮）

容器组：milvus 2.6.17（031→025→022→026 串行）‖ weaviate 1.38.2（010→009）→ 1.38.0（005→007）。
派发 = clean_run/prompts/{did}.txt 生成器原文 + 防呆段（只审候选清单内 case / verdicts 数组格式 /
JSON 自检 / 内嵌引号转义 / 禁止留测试脚本）。每 case 新会话。

| # | did | vendor | version | reviewer 会话 | 派发时间 | 判词 | 校验 | 备注 |
|---|-----|--------|---------|--------------|---------|------|------|------|
| 1 | milvus_031 | milvus | 2.6.17 | agent-g-01 | 2026-08-16 | CONFIRMED | PASS | 适用✓翻正(基线F/F/F)——C锚点适用类；判词根因=upsert inInsert=false 硬编码 |
| 2 | weaviate_010 | weaviate | 1.38.2 | agent-g-02 | 2026-08-16 | CONFIRMED | PASS | 适用✓翻正(基线F/F/F)——判词显式消费G锚点(PRs 11878/12049/12040/12262) |
| 3 | milvus_025 | milvus | 2.6.17 | agent-g-03 | 2026-08-16 | CONFIRMED | PASS | 近邻对照维持基线多数(C/C/F→C)——判C归因契约len(data)<=100违反，未消费C锚点 |
| 4 | weaviate_009 | weaviate | 1.38.2 | agent-g-04 | 2026-08-16 | FALSE_POSITIVE | PASS | 近邻对照翻正(C/C/C→F)——归因auto-schema源码取证，未消费G锚点(轮方差翻正) |
| 5 | milvus_022 | milvus | 2.6.17 | agent-g-05 | 2026-08-16 | CONFIRMED | PASS | 稳定对照翻错✗(F/F/F→C)——消费fixA锚点+残留旧断言state_collections_create_001(M1范围外)，C锚点零引用 |
| 6 | milvus_026 | milvus | 2.6.17 | agent-g-06 | 2026-08-16 | CONFIRMED | PASS | 稳定对照翻错✗(F/F/F→C)——消费fixA锚点(宽泛匹配)，C锚点零引用 |
| 7 | weaviate_005 | weaviate | 1.38.0 | agent-g-07 | 2026-08-16 | CONFIRMED | PASS | 稳定对照保持✓(C/C/C→C) |
| 8 | weaviate_007 | weaviate | 1.38.0 | agent-g-08 | 2026-08-16 | CONFIRMED | PASS | 稳定对照保持✓(C/C/C→C) |

格式注：本轮判词 source_excerpt/files_examined 为平铺位置（防呆段模板所致），archive_verdict.py
已兼容双位置校验（嵌套 steps.source_grounding 或顶层），校验强度不变。

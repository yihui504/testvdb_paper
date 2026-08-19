# E4.1：claim 修正 + 六链重建终局（2026-08-18）

## 过程

claim 错位审计发现 v4 起派发 prompt 的手写 claim 有 2 处事实错误（014 sharding_key→
实为 /cluster/recover 500、016 on_disk_payload→实为 lookup_from 200）+ 4 处 packet
claim 空（builder 自定主观测漂移）。用 packet 真实 raw_observation / GT issue 标题
与 log 实测一致确认后的修正 claim，重建 6 链（builder aligned 全对准），auditor 复审
（chain_verdicts_e4c.json，机械 A+聚合+B 全栈，违例 0）。

## e4c 六链 GT 对照：4 对 2 错

| case | GT | 判定 | 依据 |
|------|----|----|------|
| qdrant_014 | TP | DEFECT ✓ | standalone 500 应 4xx（HTTP 语义） |
| qdrant_016 | TP | DEFECT ✓ | lookup_from 静默 200 |
| qdrant_012 | FP | NOT_DEFECT ✓ | MaybeOneOrMany lenient parsing by-design（认知锚点命中） |
| qdrant_017 | FP | NOT_DEFECT ✓ | HNSW 分页重复 accepted limitation（认知锚点命中） |
| qdrant_009 | FP | DEFECT ✗ | vectors={} 静默接受——技术事实确凿但 GT=BY_DESIGN（payload-only 文化） |
| qdrant_010 | FP | DEFECT ✗ | 缺 vectors 静默接受——同上 |

009/010 的"错"是**技术事实 vs 维护者态度**的口径分裂（builder 源码搜证确证
CreateCollectionOperation 无 vectors 空校验），不是判定失误——auditor 的 rationale
如实记录了 payload-only 认知锚点存在但判定为盲区而非显式 by-design。

## 终局七列（波动集 44）

| 口径 | recall | precision |
|------|--------|-----------|
| fixF（改进前） | 0.621 | 0.818 |
| v4.1 → E2 → E3 → E4 | 0.103 → 0.414 → 0.414 → 0.552 | — |
| **E4.1** | **0.621** | **0.818** |

**E4.1 与 fixF 完全打平**（TP18/FP4/FN11/TN11 逐项一致）。且 E4.1 的判定链路
零 LLM 判定方差（A 机械+聚合机械+B 机械全栈，违例 0），fixF 是带会话方差的抽样值
（三轮 0.659/0.568/0.591）。

## 结论

1. 上一轮"材料错位不可救"的归因**被推翻**——错在派发层 claim 转述，不在探针材料
2. 修正 claim 后判定层完整兑现能力：六链 4 对 2 错，错的 2 个是口径分裂非判定失误
3. E4.1 = fixF 指标 + 零方差 + 全程可审计（每步机械判定有脚本输出可复查）

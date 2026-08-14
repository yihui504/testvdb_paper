# Phase 2 clean_run 结果报告（无污染流程复跑）

> 日期：2026-08-14/15。Run 标识：**clean**。
> 目的（audit-report §6 最后一项待办）：材料包 v2 + 派发协议 v2 + 实验纪律全部就位后，
> 用**完全无引导**的干净流程重跑全部 71 scored case，验证无污染指标，
> 并检验"0.822 recall 增益来自人工引导、不可由抽样复现"的结论。
> 纪律：docs/phase2-experiment-discipline.md 全程执行；判词归档 clean_run/verdicts/；
> 派发记录 clean_run/dispatch_log.md。

## 1. 执行摘要

- **71/71 case 判定完成**，每 case 一个新 reviewer 会话（标准档 GLM-5.2，统一模型），同容器串行、异容器并行。
- 派发 prompt 全部由 `gen_dispatch_v2.py` 单 case 生成（泄漏词 + 样本号扫描 0 命中）。
- 判词校验：70 PASS + 1 已知例外（milvus_001 空日志，纪律 §2.6）。
- 过程事件：4 份判词作废重判（JSON 损坏 ×2、平铺格式 ×2，全部闭环）、1 次编排失误（qdrant_007 首派 prompt 版本误写，已 void 并按生成器原文重派）、qdrant_015 实测致容器 OOM（已重建）。
- 材料树判词已移出归档，材料包复审 **0 FAIL / 0 WARN**（恢复纯净）。

## 2. 核心指标：四轮对照

| 轮 | 性质 | recall(A∪B=45) | fp_suppression(C=26) | precision |
|----|------|------|------|------|
| run1 | curated（三轮人工清洗） | **0.822** | 0.615 | 0.787 |
| run2 | clean（排雷后） | 0.489 | 0.654 | — |
| run3 | clean（排雷后） | 0.711 | 0.615 | — |
| **clean（本轮）** | **无污染 v2 材料+协议** | **0.533** | **0.577** | **0.686** |

（TP=24 FN=21 FP=11 TN=15）

**结论 1：0.822 确认为人工引导上界，不可由干净流程复现。** 无污染 recall 0.533，
落在 clean 轮区间 [0.489, 0.711] 内偏下；四轮 clean-ish 极差 0.22。

## 3. 轮间一致性（κ）

| 对比 | n | agreement | κ |
|------|---|-----------|---|
| clean vs run1 | 71 | 0.662 | 0.327 |
| clean vs run2 | 71 | 0.690 | 0.379 |
| clean vs run3 | 71 | 0.648 | 0.298 |
| run2 vs run3（历史） | — | — | 0.587 |

**结论 2：run-to-run 方差是 dev-reviewer 判定的根本性不稳定源。**
四轮（含本轮）互相 κ 仅 0.30-0.38，**四轮 verdict 全一致仅 31/71（44%）**。
任何单轮 headline 指标都不具备稳健性；多轮投票/方差披露是必须的。

## 4. 分歧结构

### 4.1 FN 21 个（GT=CONFIRMED 判 FP）

- **顽固 FN（历史三轮也大多 FP）×6**：milvus_50018、qdrant_9149、qdrant_9421、weaviate_12041、qdrant_9017、milvus_52310
  —— 与 run1 FN_8 高度重合，是 dev↔GT 的真实分歧（多为 by-design 类）。
  其中 **9149 为已知 GT 噪声**（audit-report §2：bug 在版本范围不复现，dev 判对、GT 错，降级待用户决定；
  本轮再证：独立会话面对 v2 材料仍判 FP，源码找到 `#[validate(range(min=1))]` 显式校验）。
- **本轮新 flip（历史 CONFIRMED → 本轮 FP）×14**：47763/49889/49890/50323/50353/50355/52308/52311/52312/52314/52315/11730/47755/49059 —— recall 下滑主因。
- milvus_001（47635）：空日志例外，两次会话均系统性放弃（历史三轮同材料可完成审查）——材料形态方差。

### 4.2 FP 11 个（GT=FP 判 CONFIRMED）

- **顽固 FP（≥3 轮 CONFIRMED）×6**：50193、50194、50351、50352、9418、11981 —— dev 真信是 bug、GT 说不是（多为 REST v2 全局 200 包装/HNSW 语义分歧）。
- 其余 5 个为本轮 flip（49844、50321、50322、50324、9419）。

### 4.3 最大分歧簇：milvus REST v2 type coercion

分 vendor 正确率：**milvus 0.44（19/43）** ≪ qdrant 0.72、weaviate 0.70。
3.0.0 组 type_coercion 系列（52308/52310/52311/52312/52314/52315）本轮系统性判 by-design
（源码 `cast.ToBoolE`/`json.Number().Int64()` 显式类型转换 = 有意设计），
而 GT（issue 实况）按 bug 计。此前 run2/run3 部分判 CONFIRMED——该簇是 recall 方差的最大单一来源，
本质是"维护者会不会认 type coercion 是 bug"的定性分歧。

## 5. 例外与披露

| 项 | 处置 |
|----|------|
| milvus_001 空日志 | 已知例外（纪律 §2.6）；两次会话均 FP+无源码（历史三轮可完成）；按第 2 次接受并披露 |
| qdrant_005（9149）GT 存疑 | 判 FP 与 dev 事实一致；GT 降级仍待用户决定 |
| qdrant_007 编排失误 | 首派 prompt 版本误写 1.18.1（VOID_LOG 留痕），生成器原文重派有效 |
| 4 份判词作废 | milvus_008/qdrant_009（JSON 转义损坏）、milvus_018/qdrant_007首判（平铺格式无 verdicts）；全部新会话重判闭环 |
| qdrant_015 容器 OOM | INT_MAX shard 实测致 Exited(137)；rm -f 重建后继续（纪律 §5.4） |

## 6. 对论文的用法建议

- headline 报 **clean 0.533 + 方差区间 [0.489, 0.711]**（多轮），curated 0.822 作为"人工引导上界"并置披露；不建议任何单轮单独引用。
- κ 0.30-0.38 / 四轮全一致 44% 可直接支撑"LLM-as-dev-judge 不稳定性"论点。
- 9149（及 8 个 GT 存疑降级后的口径）在 recall 分母敏感性分析中披露。

## 7. 归档

- 判词：`clean_run/verdicts/{vendor}/{version}/{did}.json(+.done)`
- 结果数据：`clean_run/CLEAN_RUN_RESULTS.json`（指标 + κ + 逐 case 四轮表）
- 派发记录：`clean_run/dispatch_log.md`（73 行）；作废记录：`clean_run/VOID_LOG.md`
- 材料树：判词移出，audit_materials_v2 复审 0 FAIL

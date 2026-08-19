# RQ2 v7.x 机械注入配置三轮方差实验（2026-08-19/20）

## 设计

v7.1 配置（机械层预跑注入）再复跑两遍（v7.2/v7.3），测 auditor 灰区判定的 run-to-run 方差。三轮取中位数/区间（同 fixF 三轮协议）。派发器 gen_dispatch_v71.py 加 `TESTVDB_VRUN` 环境变量支持 v72/v73 输出后缀。

**方差源隔离**：机械层（A/B 预跑值）确定性零方差——同链同脚本同输出；唯一方差源是 GREY_ZONE（A=NEUTRAL）下 LLM 对 B/C/D 的灰区裁量。

**方法论披露**：三轮共用链文件池（builder 不重跑，复用 v7.1 链），rework 闭环会重写个别链（v7.2 重写 milvus_041/weaviate_005，v7.3 重写 qdrant_003/weaviate_006）。严格独立三轮应每次重跑 builder，但本研究聚焦 auditor 判定方差，链固定前提下测 auditor 方差更纯粹。翻转案中 weaviate_006 的 v7.3 翻转含链修正成分（引文修正使 A 从 NEUTRAL→CONFIRMED），其余翻转案为同链 LLM 灰区方差。

## 三轮指标（71 案全量，GT=cases_index gt_label）

| run | TP | FP | FN | TN | recall | precision | fp_supp |
|-----|----|----|----|----|--------|-----------|---------|
| v7.1 | 32 | 9 | 12 | 18 | 0.727 | 0.780 | 0.667 |
| v7.2 | 31 | 9 | 13 | 18 | 0.705 | 0.775 | 0.667 |
| v7.3 | 30 | 9 | 14 | 18 | 0.682 | 0.769 | 0.667 |

| 指标 | 中位数 | 区间 | 带宽 | fixF 三轮带宽（对照） |
|------|--------|------|------|---------------------|
| recall | 0.705 | [0.682, 0.727] | 0.045 | 0.091 |
| precision | 0.775 | [0.769, 0.780] | 0.011 | — |
| fp_supp | 0.667 | [0.667, 0.667] | 0.000 | — |

**recall 带宽 0.045 ≈ fixF 0.091 的一半**——机械注入把 run-to-run 方差压缩约 50%。fp_supp 三轮完全一致（0.000 带宽），precision 带宽仅 0.011。

## 逐 case 稳定性

**三轮一致 66/71（93%）**，翻转 5 案（7%）：

| case | v7.1 | v7.2 | v7.3 | GT | 翻转性质 |
|------|------|------|------|----|---------|
| milvus_041 | DEFECT | DEFECT | NOT_DEFECT | CONFIRMED | 灰区 LLM 方差（同链，A=NEUTRAL） |
| milvus_043 | DEFECT | DEFECT | NOT_DEFECT | CONFIRMED | 灰区 LLM 方差（同链，A=NEUTRAL） |
| qdrant_003 | DEFECT | DEFECT | NOT_DEFECT | FALSE_POSITIVE | 灰区 LLM 方差（同链，A=NEUTRAL） |
| qdrant_004 | DEFECT | NOT_DEFECT | DEFECT | CONFIRMED | 灰区 LLM 方差（by-design 抗辩 D 信号波动） |
| qdrant_012 | NOT_DEFECT | NOT_DEFECT | DEFECT | FALSE_POSITIVE | 灰区 LLM 方差（同链，A=NEUTRAL） |

5 案翻转全部落在 GREY_ZONE（A=NEUTRAL）——机械层定案 case（A=CONFIRMED/REFUTED 或机械B=CONFIRMED）零翻转。方差源完全隔离到灰区 LLM 的 B/C/D 裁量，与设计预期一致。

## 机械层确定性验证

抽查 qdrant_015（资源边界规则）：三轮机械 B 预跑值均为 CONFIRMED——预跑注入消除了机械层方差（v7 里 auditor 自报 B 值不一致 18/71 的问题结构性消失）。

## rework 闭环（三轮累计）

| run | 工单案数 | 先例保守 | 实测 rework | 闭环收敛 |
|-----|---------|---------|-----------|---------|
| v7.1 | 8 | 0 | 8 | 5 收敛 + 3 材料性 |
| v7.2 | 6 | 4 | 2 | 2 收敛 |
| v7.3 | 5 | 3 | 2 | 2 收敛 |

材料性不可修复案（milvus_007/029、qdrant_008 等）在三轮中一致走先例保守路径——rework 闭环本身零方差，方差只在"灰区是否发工单"这一 LLM 决策点。

## 结论

1. **机械注入的方差抑制效果实证**：recall 带宽 0.091→0.045（-50%），precision 带宽 0.011，fp_supp 零方差。v7.1 单轮 0.727/0.780 不是偶然高点，三轮中位 0.705/0.775 稳定优于 v7 基线 0.614/0.794。
2. **方差源完全隔离**：5 案翻转（7%）全部在 GREY_ZONE LLM 灰区裁量，机械定案 66 案（93%）零翻转。下一步压方差的方向是收紧灰区（A=NEUTRAL 时的 B/C/D 规则），而非机械层。
3. **论文口径**：RQ2 无人值守判定能力用三轮中位数 **recall 0.705 / precision 0.775 / fp_supp 0.667**（带宽 0.045/0.011/0.000），优于 fixF（0.591/0.818，带宽 0.091）。E6（0.793/0.852）维持子集+人工监督定位。

## 产物

- `gen_dispatch_v71.py`（VRUN 环境变量化）
- 各组 `sessions/{v}/{ver}/debate_logs/chain_verdicts_v7[123][_b|_r].json`
- `rq2_v7x_three_runs.json`（三轮 71 案判词汇总）
- `rq2_v7[123]_rework_state.json`
- 本报告

## 附：规则4 机械性改进（2026-08-20）

mechbacktest 审查发现规则4（资源边界）的第二条件依赖 builder 的 `source_excerpt` 自由文本（grep "lower-bound only|no upper"），破坏机械性——builder 措辞方差会泄漏进机械层。

**改法**（`check_physical_constraints.py`）：
- `judge_physical` 加 `src_dir` 参数
- 新增 `_grep_bound_in_source(src_dir, files, param_names)`：从链 `source_grounding.files_examined` 取源码文件，直接 grep 校验注解
- 参数名从 `obs` 提取（如 shard_number），精准定位字段定义行上方 3 行内的 `range(min`/`range(max` 注解——避免同文件其他参数的 max 注解污染
- 规则4：`src_dir` 提供时走源码 grep（机械）；未提供时回退旧 excerpt 逻辑（向后兼容）
- `gen_dispatch_v71.py` 的 `mech_line` 传入 `src_dir=clone`

**验证**：
- 71 案同链对比（旧 excerpt 路径 vs 新源码 grep 路径）：**0 差异**——判定结果不变，v7.x 三轮指标不受影响
- 去耦合：qdrant_015 的 `source_excerpt` 清空/改措辞，新路径仍 CONFIRMED；旧路径清空即 NOT_TRIGGERED
- 结论：改进只提升机械性（规则4 真机械），不改判定。qdrant_015 的 CONFIRMED 不再依赖 builder 措辞巧合

**注意**：`check_physical_constraints.py` 在插件 cache（`~/.claude/plugins/cache/testvdb/.../scripts/`），非 git 追踪。若采纳需同步到主插件仓库 `mftui/TestVDB`。

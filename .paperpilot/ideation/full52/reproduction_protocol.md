# Reproduction Anchor 实验 Protocol（C3）

> 2026-07-15。把 dev-reviewer 的 reproduction anchor 从「事后验证 kill 质量」提升为「判定时的独立 anchor」。
> **重要**：本 protocol 在准备过程中纠正了 checklist C3 / rebuttal §5 的一个错误假设（见 §0）。

---

## 0. 关键修正（必读）

**先前错误假设**：「reproduction 补 source 漏的 3 个 silent-absent residual（q3/q37/q52）」。

读 [stage2_source_full16.md](stage2_source_full16.md) + [t22 三条件消融](../../../TestVDB/scripts/t22_three_condition_ablation_results.json) 后确认：
- source 漏的 3 个（q3 shardsNum / q37 metricType / q52 empty vector）是 **by-design silent fallback**（行为真的发生，但是设计如此——default/clamp）。
- 这 3 个里，**q3/q37 是 threat-model anchor 补的**（t22 JSON: `threat caught_residuals = [q3_shardsNum, q37_metricType]`），q52 source+threat 都漏（`both_union` note: q52 leaks）。
- reproduction anchor（§3.4 定义）杀的是 **tooling artifact**（脚本误读响应）。它 live 上看到「行为发生了」，但**不区分 by-design vs bug**——判 by-design 必须 source。

**结论：reproduction 补不了 source 漏的 3 个（那是 threat 的活）。** 三个 anchor 按 FP 成因分工，不是互相补盲区。

---

## 1. reproduction anchor 的真实定位

| FP 成因类 | 典型案例 | reproduction | source | threat |
|---|---|---|---|---|
| **tooling artifact**（脚本误读响应/漏带参数/误读拒绝码）| `rowCount` 缺失被误读为「返回 -1」；oracle 漏带 `outputFields` | **能（主战场）** | 能（查源码知无此验证）| 弱 |
| **by-design silent fallback**（default/clamp）| shardsNum=0→default；metricType=""→COSINE | **不能**（不区分 by-design）| 能（查 default 常数）| 能（boundary-default）|
| **contract hallucination**（造错契约）| `constant.go` 复杂度要求 | 不能 | **能（主战场）** | 弱 |

**reproduction 的独立价值** = 在 tooling artifact 类上，**不查源码、纯 live 复现就能 kill**，作 source 的独立兜底（source 不可用 / agent 定位失败时）+ tooling artifact 的主战武器。

---

## 2. 候选池

**不用 16 FP retrospective 池**——那里 tooling artifact 少（脚本误读类大多在提交前就被 dev-reviewer kill，能进 52 pool 的多是 by-design）。

**用 27 killed 池**（[T2 Exp 4](../../../TestVDB/scripts/T2_REPROBE_REPORT.md) 已 live re-probe + 分类）：
- **tooling artifact 类（15）** = reproduction 主战场：
  - INPUT_VALIDATED_REJECT (5) — oracle 误读拒绝响应
  - CORRECT_REJECT_CONVENTION (5) — oracle 误解 REST 拒绝约定（HTTP 200 包业务错）
  - ORACLE_SCRIPT_BUG (5) — oracle 漏带 outputFields 等
- **by-design/state 类（12）** = source 主战场，**reproduction 预期失败/误判**（对照）：
  - UPSERT_SEMANTICS(4) + IDEMPOTENT(4) + STATE_CORRECT(2) + DYNAMIC_FIELD(1) + ACCEPTED(1)

---

## 3. 判定逻辑（reproduction anchor，独立、不查源码）

对每个 candidate：
1. 从 defect_id + dev-reviewer 记录的 raw 请求，**重建最小请求**（剥离脚本可能的干扰，补全必要参数——参考 dev-reviewer.md 第 1 步）
2. 在 fresh live 容器（milvus v2.6.19）上发请求
3. 看 raw 响应是否**真的表现「声称的违规」**：
   - 响应正常 / 其实是拒绝（code≠0）/ 脚本漏带字段 → **tooling artifact → reproduction 判 FP（kill）**
   - 响应确实违规 → 不 kill（交给 source/threat）

**关键**：reproduction 只判「违规是否真的发生」，**不判「是不是 by-design」**——这是它的能力边界。

---

## 4. 稳定性标准

每个 candidate 跑 **N=5 次**（fresh 容器或同容器重置），记录每次响应：
- **确定性类**（响应码固定，如 INPUT_VALIDATED_REJECT）：5/5 一致 → 稳定 kill
- **间歇类**（race / eventual consistency）：≥3/5 表现「违规」→ 算复现成功（标注间歇）
- 不一致 → 标 `unstable`，不纳入 kill 计数（诚实）

---

## 5. 成功阈值（修正）

**主指标**：reproduction 在 **15 个 tooling artifact 类** FP 上的独立 kill 率：
- **≥ 10/15（67%）** → reproduction 是 tooling artifact 的有效独立 anchor → 多 anchor 按 FP 成因分工的表述成立（dev-reviewer 升级）
- **5–9/15** → 部分有效，表述降调（reproduction 是 source 的补充确认，非独立主力）
- **< 5/15** → 价值有限，表述基本不动

**副指标（诚实边界）**：reproduction 在 **12 个 by-design 类**上的**误判率**。预期它误判成 TP（live 看到行为发生就当 bug）——高误判率恰恰**证明 reproduction 不能单独替代 source**，这是必须如实报告的能力边界。

---

## 6. 实际结果（2026-07-15 跑完）

**tooling_artifact reproduction KILL 12/14（达标 ≥10）；by_design 误判 9/11；unstable 0。**（`TestVDB/scripts/reproduction_anchor_results.json`，N=5，milvus v2.6.19）→ 达标表述成立（见 rebuttal-snippets §5）。

关键边界：C15/C27（live code=0）tooling 也 MISS——**reproduction 对「live code=0 接受行为」统一失效**（不论 by-design 还是 tooling），不能替代 source。副产品：诊断验证 q12/state_001 的 rowCount 异步滞后是 milvus 真实行为。

---

## 6.x 预期表述分支（事前假设，已由上面实际结果取代）

**达标（≥10/15 tooling artifact）**：
> dev-reviewer 的多 anchor 按 **FP 成因分工**：source-grounding 反 contract hallucination / by-design，reproduction 反 tooling artifact（脚本误读），threat-model 补 boundary-default 残余。reproduction 的独立价值是不查源码、纯 live 复现抓脚本误读，作 source 的兜底。三者不是冗余，是针对不同 FP 成因的互补。

**未达标**：reproduction 作为 source 的冗余确认，不升级多 anchor 表述；诚实报告其在 by-design 类上的误判边界。

---

## 7. 实施清单

- [ ] 从 `t2_full_27_reprobe_results.json` 提取 15 个 tooling artifact candidate 的 defect_id + raw 请求
- [ ] 复用 `t2_full_27_reprobe.py` 的 live re-probe 基础设施，加：① N=5 稳定性循环 ②「违规是否真发生」判定（不看源码）
- [ ] 跑 15 tooling artifact（主）+ 12 by-design（对照）
- [ ] 统计：reproduction 独立 kill（tooling artifact）+ 误判（by-design）+ unstable 计数
- [ ] 按阈值判定表述分支，回填 rebuttal-snippets §5

---

## 8. 与 source / threat 的分工（避免重复claim）

- **source**：by-design silent fallback + contract hallucination（查源码/default 常数）—— 已 validated（31%→81%）
- **threat-model**：补 source 漏的 by-design boundary-default 残余（q3/q37）—— exploratory，n=12 不稳定
- **reproduction**：tooling artifact（脚本误读）—— 本实验要验证的第三 anchor

三者按 FP 成因正交分工，**不存在「reproduction 补 source 盲区」**——这是本 protocol 纠正的核心误解。

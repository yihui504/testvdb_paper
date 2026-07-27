# Dual-Review Report — TestVDB v3（PPT v2.3 重写版）

> Paper: TestVDB v3（7 页，2 figures + 6 tables + 9 节，无 TI layer）
> Date: 2026-07-27 · venue TBD → SE 顶会 fallback
> 6 reviewer（3 态度 + 3 expertise）独立审稿。**评分不合并**——两 verdict 并列。

## 顶层摘要（两 verdict 并列）

| 半边 | Verdict | 关键 |
|---|---|---|
| **态度**（会议 1-5）| **Weak Accept (~7/10)** | R1 7/10, R2 3/5 weak-accept, R3 4/5 accept。比 mock-review（6.3 borderline）改善——action plan 改生效 |
| **expertise**（四档 + Meta）| **ACCEPT** | R1 Accept（Novelty Excellent）/ R2-R3 Weak Accept → unanimous shortcut |

### 共识（两半边一致）

- **核心 framing 站得住**：3 态度 + 3 expertise 都认可 doc-impl + hallucination/self-preference + source-grounded falsifier。**无 reviewer 质疑新故事线**（vs archive 旧版 TI 被 5-family 实验挑战，重写成功规避）
- **最强 weakness 共识**：post-hoc 操作点 selection bias（5 reviewer）+ external validity / VDBMS 外泛化（5 reviewer）

### 分歧（dual-review 设计预期）

- 态度 R2 严（post-hoc 标 [CRITICAL, not fixable]）vs expertise R1 宽（Novelty Excellent, Accept）—— R1 用 cache verified novelty delta vs MASTOR，R2 严方法论统计。这是双套互补：expertise 看到 novelty 真实，态度看到统计风险。

## Score Summary

| Dimension | 态度 R1 | 态度 R2 | 态度 R3 | expertise R1 | expertise R2 | expertise R3 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Soundness | 4 | 3 | 4 | Adequate | **Weak** | Adequate |
| Significance | 4 | 3 | 4 | Adequate | Adequate | Adequate |
| Novelty | 4 | 3 | 4 | **Excellent** | Adequate | Adequate *(prov)* |
| Presentation | 4 | 3 | 5 | **Excellent** | Adequate | Adequate |
| **Overall** | **7/10** | **3/5** | **4/5** | **Accept** | **Weak Accept** | **Weak Accept** |

## Attitude Half

3 review：[r1.md](.self_xept/dual-review/.in-progress/attitude/r1.md) 客观 / [r2.md](.self_xept/dual-review/.in-progress/attitude/r2.md) 严格 / [r3.md](.self_xept/dual-review/.in-progress/attitude/r3.md) 友好

- **R1 (7/10 weak-accept)**：W post-hoc 操作点 / external validity / yield selection bias
- **R2 (3/5 weak-accept)**：W post-hoc [CRITICAL] / multi-perspective baseline / VDBFuzz n=1
- **R3 (4/5 accept)**：S oracle 排除论证 / dev-reviewer 设计 / 49 TP 实际影响

## Expertise Half

完整：[expertise-report.md](.self_xept/dual-review/.in-progress/expertise/expertise-report.md)（3 review + Meta-Review）

- **R1 Domain Expert（Accept）**：Novelty Excellent（source-as-falsifier vs MASTOR source-as-oracle 是 verified delta）；Presentation Excellent。W: single-model / post-hoc / VDBMS-only
- **R2 Area Specialist（Weak Accept）**：Soundness Weak（post-hoc selection bias [major, unfixable]）。注：R2 称漏 AugmenTest/ChatAssert——**三态核实 False**（论文 §7 有 cite，reviewer 漏看）
- **R3 General（Weak Accept）**：全 Adequate（Novelty provisional）。W: novelty vs REST-API 边界 / post-hoc / external validation
- **Meta**：**ACCEPT**（unanimous shortcut）

## Unified Action Plan

完整：[merged-action-plan.md](.self_xept/dual-review/.in-progress/merged-action-plan.md)

**[both] + major（4 簇，must-fix）**：
1. **post-hoc 操作点 selection-aware CI**（5 reviewer 共识，最强信号）—— 报告 selection-aware CI 或显式标"conditional on selected operating point"
2. **external validity mini case**（5 reviewer 共识）—— 1 个 non-VDBMS case 或更显 future work
3. single LLM backbone 第三 family —— 标 highest-value next experiment
4. impl-as-correct false negative —— 已讨论，可补量化

**[both] + minor（2 簇）**：VDBFuzz n=1 降调 / Novelty vs REST-API 边界强化

**[attitude-only]（2 簇 minor）**：multi-perspective 表 / yield selection bias

**[expertise-only]（1 簇 minor + 1 False）**：cost 表 / 漏 AugmenTest（False，论文有）

## 三态核实亮点

| Weakness | Verdict | Note |
|---|---|---|
| post-hoc 操作点 selection bias | **Valid** | 论文加了 rationale，但 Wilson CI 未含 selection uncertainty（统计本质）|
| external validity / VDBMS 外泛化 | **Valid** | §8 future work，无 case study |
| single LLM backbone + κ=1.0 | **Valid** | 已加 Wilson [83,100]，可更显 limitation |
| 漏 AugmenTest/ChatAssert（R2）| **False** | 论文 §7 line 311-313 有 cite，reviewer 漏看 |

## 对比 mock-review（重写前 6.3）vs dual-review（重写+改+扩后）

| 项 | mock-review（重写后立即）| dual-review（action plan 改 + 扩展后）|
|---|---|---|
| 态度 Overall | 6.3 borderline（R1 7/R2 4/R3 8）| ~7 weak-accept（R1 7/R2 6/R3 8）|
| expertise Meta | （未跑）| **ACCEPT** |
| post-hoc 操作点 | R2 4/10 拒稿信号 | 5 reviewer 仍提，但论文已加 selection rationale，降为"selection-aware CI"建议（fixable）|
| multi-perspective 展开 | R2 拒稿（未展开）| 已加 voting rule + operating point，R2 仍提但弱化 |
| 核心 framing | 站得住 | **站得住**（无 reviewer 质疑新故事线）|

**重写 + action plan 改 + 扩展的整体效果**：从 mock-review 的 borderline（6.3）升到 dual-review 的 weak-accept 共识（~7）+ expertise ACCEPT。R2 的拒稿信号（post-hoc）从"未展开"降为"selection-aware CI 可改"。

## 流程透明

- 6 reviewer 同步并行（避免 background session-restart 丢，上次 dual-review 教训）
- 剥注释 330 行 0 残留
- expertise R1/R2 cache abstract-first（MASTOR/SATORI abstract-level，避免 fetch 慢）
- 主 agent 三态核实（合并 checker 角色，避免上次 checker 幻觉误报）

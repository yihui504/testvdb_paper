# Dual-Review Report — TestVDB v3（第三版）

> Paper: TestVDB v3（abstract single-backbone caveat + CouchDB portability framing + minus-source ablation + cross-model κ 修正 + Bonferroni CI + reduce-ai）
> Date: 2026-07-28 · 6 reviewer · **评分不合并**

## 顶层摘要

| 半边 | Verdict | vs v2 | vs v1 |
|---|---|---|---|
| **态度** | ~7/10 weak-accept（R1 7 / R2 ~6 / R3 8）| ↑（6.5→7）| ≈ |
| **expertise** | **ACCEPT**（unanimous Weak Accept）| = | = |

**核心 framing 站得住**（第三次确认，无 reviewer 质疑 doc-impl + dev-reviewer + source grounding）。

## Score Summary

| Dimension | 态度 R1 | 态度 R2 | 态度 R3 | exp R1 | exp R2 | exp R3 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Soundness | 3 | 3 | 4 | **Weak** | **Weak** | Adequate |
| Significance | 4 | 3 | 4 | Adequate | Adequate | Adequate |
| Novelty | 4 | 3 | 4 | **Adequate** ↑ | Adequate | Adequate *(prov)* |
| Verifiability | — | — | — | Adequate | **Excellent** ↑ | **Excellent** ↑ |
| Presentation | 4 | 3 | 5 | Adequate | Adequate | Adequate |
| **Overall** | **7/10** | **3/5** | **4/5** | **Weak Accept** | **Weak Accept** | **Weak Accept** |

## 三版对比（v1 → v2 → v3）

| | v1（初版）| v2（κ 修正+minus-source）| **v3（abstract caveat+CouchDB framing）** |
|---|---|---|---|
| 态度 | ~7 | ~6.5（κ 引入新 weakness）| **~7**（abstract caveat 改善）|
| expertise Meta | ACCEPT（R1 Accept）| ACCEPT（全 WA，R1 Novelty Weak）| **ACCEPT**（全 WA，R1 Novelty **Adequate**）|
| R1 Novelty | Excellent | Weak | **Adequate**（恢复）|
| R2/R3 Verifiability | Adequate | Adequate | **Excellent**（minus-source + Bonferroni 提升信任）|
| 核心 framing | 站得住 | 站得住 | **站得住** |
| 最强 weakness | post-hoc / κ=1.0 | cross-family / post-hoc | **post-hoc / cross-family**（inherent limitation）|

## Attitude Half

3 review：[r1.md](.in-progress/attitude/r1.md) / [r2.md](.in-progress/attitude/r2.md) / [r3.md](.in-progress/attitude/r3.md)

- **R1 (7/10)**：post-hoc [MEDIUM] / cross-family [MEDIUM] / Weaviate yield-only [LOW]
- **R2 (3/5 weak-accept)**：post-hoc p-hacking [HIGH] / external validation [HIGH] / cross-family presentation [HIGH]
- **R3 (4/5 accept)**：oracle exclusion S / source-grounded falsification S / 49 TP S

## Expertise Half

完整：[expertise-report.md](.in-progress/expertise/expertise-report.md)

- **R1 Domain（Weak Accept）**：Novelty **Adequate**（v2 Weak 恢复）/ Soundness Weak（post-hoc + cross-family）/ 缺 AugmenTest cite
- **R2 Area（Weak Accept）**：Soundness Weak / Verifiability **Excellent**（v3 改善）/ Specialty: REST-API oracles + LLM-as-judge
- **R3 General（Weak Accept）**：全 Adequate / Verifiability **Excellent**
- **Meta**：**ACCEPT**（unanimous shortcut。Soundness R1/R2 Weak 但 R3 Adequate → [Mixed]；无 consensus Poor）

## Unified Action Plan

完整：[merged-action-plan.md](.in-progress/merged-action-plan.md)

**[both] major（residual，inherent limitation）**：
1. post-hoc selection-aware CI（4 reviewer）—— 已有 Bonferroni，residual 需 pre-registration
2. cross-family framing（3 reviewer）—— 已有 abstract caveat，§6 呈现可重排（full re-run 放前）
3. external validation（2 reviewer）—— CouchDB 已标 portability framing

**结论**：residual weakness 是 **inherent limitation**——文字层面已尽（Bonferroni + caveat + open question + portability framing）。根本解决需实际改进（pre-registration / 更多 family / 更多 non-VDBMS），非文字修改能消除。论文已诚实面对，适合投稿。

# Dual-Review Report — TestVDB v3（第二版）

> Paper: TestVDB v3（含 minus-source ablation + cross-model κ 修正 + CouchDB external validity + reduce-ai）
> Date: 2026-07-28 · 6 reviewer（3 态度 + 3 expertise）· **评分不合并**

## 顶层摘要（两 verdict 并列）

| 半边 | Verdict | 变化（vs 第一版）|
|---|---|---|
| **态度** | ~6.5/10 weak-accept（R1 6 / R2 ~5.4 / R3 8）| 略降（7→6.5）——κ 修正 + minus-source isolation concern |
| **expertise** | **ACCEPT**（三位 Weak Accept → unanimous）| 仍 ACCEPT（但 R1 从 Accept 降到 Weak Accept——Novelty Weak）|

**核心 framing 站得住**——无 reviewer 质疑 doc-impl + dev-reviewer + source grounding。minus-source ablation 被 R2-attitude 挑战"没完全隔离 source"（仍含 clean-repro + threat-model），但其他 reviewer 认可。

## Score Summary

| Dimension | 态度 R1 | 态度 R2 | 态度 R3 | exp R1 | exp R2 | exp R3 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Soundness | 3 | 3 | 4 | Adequate | **Weak** | Adequate |
| Significance | 4 | 3 | 4 | Adequate | Adequate | Adequate |
| Novelty | 4 | 3 | 4 | **Weak** | **Excellent** | Adequate *(prov)* |
| Presentation | 4 | 3 | 5 | Adequate | **Weak** | Adequate |
| **Overall** | **6/10** | **2.7/5** | **4/5** | **Weak Accept** | **Weak Accept** | **Weak Accept** |

## Attitude Half

3 review：[r1.md](.in-progress/attitude/r1.md) / [r2.md](.in-progress/attitude/r2.md) / [r3.md](.in-progress/attitude/r3.md)

- **R1 (6/10)**：post-hoc CI [CRITICAL] / cross-family unproven [HIGH] / no recall catalog [HIGH]
- **R2 (2.7/5 weak-accept)**：minus-source isolation [HIGH] / post-hoc CI [HIGH] / cross-model κ undermines [HIGH]
- **R3 (4/5 accept)**：oracle exclusion S / dev-reviewer design S / evaluation rigor S（Bonferroni + threats）

## Expertise Half

完整：[expertise-report.md](.in-progress/expertise/expertise-report.md)（3 review + Meta-Review）

- **R1 Domain Expert（Weak Accept）**：Novelty **Weak**（source-grounded falsification 是 known technique）/ Verifiability **Weak**。竞品 verified（VDBFuzz/AGORA+/SATORI/MASTOR/Toradocu）
- **R2 Area Specialist（Weak Accept）**：Novelty **Excellent**（domain-specific application is novel）/ Soundness **Weak**（post-hoc selection）/ Presentation **Weak**。Specialty: LLM-as-judge + DB testing
- **R3 General（Weak Accept）**：全 Adequate（Novelty provisional）
- **Meta**：**ACCEPT**（unanimous shortcut；无 consensus Poor / 无 substance consensus Weak——各准则 Weak 来自不同 reviewer）

**Novelty 分歧**：R1 Weak（known technique）vs R2 Excellent（domain-specific novel）——这是正常 reviewer 分歧，论文可强化"source as falsifier（非 oracle）的方向性不对称"framing。

## Unified Action Plan

完整：[merged-action-plan.md](.in-progress/merged-action-plan.md)

**[both] major（must-fix）**：
1. **post-hoc selection-aware CI**（4 reviewer 共识，最强信号）—— 论文已加 Bonferroni 估算，reviewer 仍觉 headline CI 未充分 caveat
2. **cross-family κ 在 abstract/contributions 显式 caveat**（4 reviewer）—— 论文 §6 已诚实报告，但 abstract 仍广义 claim "LLM-derived oracle"
3. **external validity 扩展**（2 reviewer）—— CouchDB 只 1 个 non-VDBMS，无 defect found

**[attitude-only] major**：minus-source fully crossed ablation（R2：minus-source 仍含其他 anchor，没完全隔离 source）

**[expertise-only] minor**：Novelty positioning（R1 Weak vs R2 Excellent 分歧）

## 对比 v3 第一版 dual-review

| | 第一版（无 minus-source/κ 修正/CouchDB）| **第二版（本版）** |
|---|---|---|
| 态度 | ~7 weak-accept | ~6.5 weak-accept（略降：κ 修正引入新 weakness）|
| expertise Meta | ACCEPT（R1 Accept）| ACCEPT（全 Weak Accept——R1 因 Novelty Weak 降）|
| 核心 framing | 站得住 | **站得住** |
| 最大变化 | — | κ=1.0 修正（诚实报告 family-specific）+ minus-source ablation（source 是 recall 核心）+ CouchDB（external validity 探索）|

**总评**：第二版比第一版**更诚实**（κ 修正 + minus-source + CouchDB），但引入了新 weakness（cross-family caveat + minus-source isolation）。核心贡献不变，Meta 仍 ACCEPT。投稿前需在 abstract/contributions 显式标 single-backbone limitation（回应 4-reviewer 共识）。

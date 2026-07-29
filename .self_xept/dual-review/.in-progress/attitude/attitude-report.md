# Attitude Half — TestVDB v5（v4 修订后验证轮）

> Target Venue: SE conference（ISSTA/ICSE/FSE tier）· Overall Prediction: Weak Accept · Date: 2026-07-29 · 3 reviewer（客观/严格/友好），评分不合并

## Score Summary

| Dimension | R1 (客观) | R2 (严格) | R3 (友好) |
|---|:---:|:---:|:---:|
| Soundness | 4/5 | 3/5 | 4/5 |
| Significance | 4/5 | 3/5 | 4/5 |
| Novelty | 4/5 | 4/5 | 4/5 |
| Presentation | 4/5 | 3/5 | 4/5 |
| **Overall** | **Accept (7/10)** | **Weak Accept (3/10)** | **Accept (8/10)** |

3 份完整 review：[r1.md](r1.md) / [r2.md](r2.md) / [r3.md](r3.md)

## Reviewer 1 — 客观
> Confidence: 4/5 · Overall: Accept (7/10)
Strengths: problem framing + Table 1 exclusion / dev-reviewer three-check / 48-candidate retrospective + ablation / honest threat modeling。
Weaknesses: **[major, fixable]** post-hoc operating-point CI（Bonferroni 未进表）/ **[major, fixable]** single-backbone headline 未 fully qualify（cross-model κ=0.14–0.51）/ **[major, fixable]** RQ3 reverse direction n=1 / [minor] Table 1 PBT row / [minor] §8 portability probe / [minor, unfixable] implementation-as-correct 未量化。

## Reviewer 2 — 严格
> Confidence: 5/5 · Overall: Weak Accept (3/10)
Strengths: problem isolation / source-grounded falsification / 49 TP + 15 merged-PR。
Weaknesses: **[major, fixable]** post-hoc garden-of-forking-paths / **[major, fixable]** VDBFuzz n=1 + 无 v1.18.2 crash baseline / **[major, fixable]** external negative evidence / [minor] selection bias 未量化 / [minor] implementation-as-correct 未 stress-test。
Scores: Soundness 3 | Significance 3 | Novelty 4 | Presentation 3。

## Reviewer 3 — 友好
> Confidence: 4/5 · Overall: Accept (8/10)
Strengths: clear problem definition / dev-reviewer substantial contribution / rigorous evaluation + ablation / 49 TP + per-vendor nuance / honest limitation。
Weaknesses: 全 [minor, fixable]（cross-family / post-hoc / RQ3 complementarity framing / threat-model anchor）。

## Verification（主代理回论文三态核实）

| # | Source | Claim | Verdict | Note |
|---|---|---|---|---|
| 1 | R2-W2 | "VDBFuzz does not report crash coverage on v1.18.2; 0/14 incomparable without baseline" | **Misleading** | 论文 §6.3 明确："on Qdrant v1.18.2... VDBFuzz ran over 26,000 mutated requests and reached 0... The two Qdrant crashes VDBFuzz reports in its own case study are also fixed in v1.18.2"——这就是 v1.18.2 crash baseline（26k requests, 0 crash）。R2 漏读 systematic direction 段。v4 reframe（systematic vs controlled）正是为 rebut 这点，但 R2 仍按 v4 前的"n=1"框架读 |
| 2 | R1-W2 / R2-W1 / R3-W2 | "Post-hoc operating-point selection inflates uncertainty" | **Valid** | 论文承认 + Bonferroni + bootstrap（[53,83]/[71,96]）；R1 建议 Bonferroni CI 进表。residual inherent |
| 3 | R1-W1 / R2-W3 | "Single-backbone / cross-family / external validity" | **Valid** | inherent，文字已尽（caveat + 3-family κ + portability framing） |
| 4 | R2-W4 | "48-candidate selection bias 未量化" | **Valid** | 论文承认 non-random；capture-recapture 是 future work |
| 5 | R1-W6 / R2-W5 | "Implementation-as-correct 未 stress-test" | **Valid** | inherent（无 GT catalog） |

## Action Plan

**Must Fix** — 多人 Valid major
- post-hoc operating-point（R1/R2/R3 + expertise 共识）：已有 Bonferroni + bootstrap，**R1 建议 Bonferroni CI 进表**（v5 新具体建议，cheap）。residual inherent。

**Should Fix** — Misleading
- R2-W2 VDBFuzz baseline：论文 §6.3 已有 26k requests 0 crash，但 R2 漏读 → 可在 §6.3 更显著标注"crash baseline: 0 crashes on 26k requests"让 strict reviewer 不漏（v4 reframe 已做，可再加一句明确"this is the crash baseline"）。

**Optional / inherent**
- cross-family / external validation / implementation-as-correct / selection bias：inherent，文字已尽。

## Overall Prediction
**Weak Accept band**（2 Accept + 1 Weak Accept，均分 6.0；adjusted ~6.5 若 R2-W2 漏读修正）。vs v4（6.75）略低，主因 R2 降到 3/10（部分基于 W2 VDBFuzz-baseline 漏读，核实为 Misleading——论文 §6.3 已有 26k-request crash baseline）。

**v4 修订验证**：R1 Objective 持平（7），R3 Friendly 升（7→8），R2 Strict 降（6→3，但降因含漏读）。核心 framing 第五次确认站得住。

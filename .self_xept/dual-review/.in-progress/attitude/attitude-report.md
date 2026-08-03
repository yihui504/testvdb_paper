# Attitude Half — TestVDB v6（v5 polish 后验证轮）

> Target Venue: SE conference（ISSTA/ICSE/FSE tier）· Overall Prediction: Weak Accept · Date: 2026-07-31 · 3 reviewer，评分不合并

## Score Summary

| Dimension | R1 (客观) | R2 (严格) | R3 (友好) |
|---|:---:|:---:|:---:|
| Soundness | 4/5 | 3/5 | 5/5 |
| Significance | 4/5 | 4/5 | 4/5 |
| Novelty | 4/5 | 4/5 | 4/5 |
| Presentation | 4/5 | 3/5 | 4/5 |
| **Overall** | **Accept (7.5/10)** | **Weak Accept (3.5/10)** | **Accept (7/10)** |

3 份完整 review：[r1.md](r1.md) / [r2.md](r2.md) / [r3.md](r3.md)

## Reviewer 1 — 客观
> Confidence: 4/5 · Overall: Accept (7.5/10)
Strengths: clear problem isolation / source-grounded falsification sound / 49 TP + 15 merged-PR real-world / credible threat diagnosis。
Weaknesses: **[major, fixable]** post-hoc operating point（Bonferroni 未 primary）/ **[major, fixable]** single-backbone（cross-family κ=0.14-0.51）/ [minor] source-access requirement / [minor] per-run variance display。

## Reviewer 2 — 严格
> Confidence: 4/5 · Overall: Weak Accept (3.5/10)
Strengths: oracle-exclusion argument / dev-reviewer 3-check sound / bidirectional probe / honest threats。
Weaknesses: **[major, fixable]** post-hoc selection（Wilson 未含 selection）/ **[major, fixable]** non-random retrospective sample（无 audit）/ **[major, fixable]** cross-family（κ + recall drop）/ **[major, fixable]** RQ3 VDBFuzz asymmetry（n=1 controlled）/ [minor] portability。

## Reviewer 3 — 友好
> Confidence: 4/5 · Overall: Accept (7/10)
Strengths: clear contribution / sound design / 49 TP practical / complementary coverage。
Weaknesses: 全 [minor, fixable]。

## Verification（主代理回论文三态核实）

| # | Source | Claim | Verdict | Note |
|---|---|---|---|---|
| 1 | R2-W4 | "RQ3 n=1 underpowered, conflates template gaps with oracle limits" | **Misleading** | 论文 §6.3 已区分 systematic（v1.18.2, 26k requests, 0/14 silent-accept reached）vs controlled（v1.4.0/v1.18.0, n=1 mechanism）；R2 漏读 systematic direction。Bonferroni + bootstrap 也已含 |
| 2 | R1-W2 / R2-W1 | post-hoc operating-point selection | **Valid** | 论文承认 + Bonferroni + bootstrap；residual inherent |
| 3 | R1-W1 / R2-W3 | single-backbone / cross-family | **Valid** | inherent（κ=0.14-0.51 + recall 18-56%）|
| 4 | R1-W4 / R2-W5 | external validity / portability | **Valid** | inherent（CouchDB/ES 0 defect）|
| 5 | R2-W2 | non-random 48-candidate sample | **Valid** | 论文承认 non-random；capture-recapture 是 future work |

## Action Plan

**Must Fix** — 多人 Valid major（inherent）
- post-hoc operating-point（R1/R2/R3 + expertise 共识）：已有 Bonferroni + bootstrap，residual inherent。

**Should Fix** — Misleading
- RQ3 systematic 显式（R2-W4 漏读）：§6.3 已有 systematic 段，可在 systematic direction 首句更显著标 "crash baseline" 让 strict reviewer 不漏读。

**Optional / inherent**
- cross-family / external / non-random：inherent，文字已尽。

## Overall Prediction
**Weak Accept band**（2 Accept + 1 Weak Accept，均分 ~6.0；adjusted ~6.5 若 R2 RQ3 漏读修正）。vs v5（~6.0）持平。v6 polish（Figure 1 / judge→agent / PBT / feedback 删 / reduce-ai）**未被任何态度 reviewer 标为新 issue**——改动 clean。核心 framing 第六次确认站得住。

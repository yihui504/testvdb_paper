# Mock Review Report — Round 8
> **Target Venue:** SE top-tier (ISSTA/FSE/ICSE bar; venue TBD, soft target ISSTA 2027-01) · **Overall Prediction:** Weak Accept (revise) · **Date:** 2026-07-17 (round 8)
> **Paper:** TestVDB v2 — after check-submission + reduce-ai pass (LLM-as-oracle → LLM-derived oracle; title/bib/abbreviation consistency; 6 em-dash rewrites; abstract trim; emergencystretch).
> **Previous:** Round 7 (Accept, 2A+1WA) — `.self_xept/mock-review-r{1,2,3}-r7.md`. Round-8 reviews: `.self_xept/mock-review-r{1,2,3}.md`.

## Score Summary
| Dimension | R1 (Objective) | R2 (Critical) | R3 (Friendly) | Mean |
|-----------|:-:|:-:|:-:|:-:|
| Soundness | 4/5 | 3/5 | 4/5 | 3.67 |
| Significance | 4/5 | 3/5 | 5/5 | 4.00 |
| Novelty | 4/5 | 4/5 | 4/5 | 4.00 |
| Presentation | 4/5 | 4/5 | 4/5 | 4.00 |
| **Overall** | 4/5 (Weak Accept) | 3/5 (Borderline) | 4.5/5 (Accept) | **3.83** |
| Confidence | 4/5 | 4/5 | 4/5 | 4.00 |

Mean Overall ≈ 3.83/5 → **Weak Accept band**. Two reviewers in the accept band; R2 borderline-but-revisable ("with revision... a stronger paper").

## Consensus (all three)
Problem real and timely; the two-layer error model (family-specific vs task-intrinsic) is the clearest conceptual contribution; Table 1 (oracle exclusion) and Table 3 (cross-model vs source) are strong; positioning vs AGORA+/SATORI/MASTOR is sharp; honesty about limitations is commendable. Three recurring concerns: (1) RQ3 n=9 probe too small; (2) "85% residual" reads as a population claim; (3) dev-reviewer lacks cross-model validation.

## Verification
| # | Source | Claim (abridged) | Verdict | Note |
|---|--------|------------------|---------|------|
| 1 | R1-W1 / R2-W1 / R3-W1 | RQ3 nine-clause probe too small for the task-intrinsic claim; 2/9 TI → wide CI | **Valid** | Three-reviewer consensus. Paper self-flags as "pilot" but abstract/contributions present it as supported. |
| 2 | R1-W3 / R2-W3 / R3-W2 | "85% conformance residual" presented as population prevalence; actually sample composition | **Misleading** | Paper caveats it in RQ1, Threats, and Discussion ("reflects what TestVDB is designed to surface"), but abstract/intro state "about 85% are conformance defects" without an inline qualifier. |
| 3 | R2-W2 / R3-W4 | dev-reviewer uses a single family (GLM-5.2); 81% FP suppression may be GLM-specific; no cross-model check | **Valid** | Threats calls the cross-model ablation "open"; reviewers want at least a consistency check on a subset. |
| 4 | R1-W2 | task-intrinsic classification procedure unclear (verbatim vs semantic? who judges "reproduces"?) | **Valid** | §regime / RQ3 says DeepSeek "reproduced GLM's over-strict clause in 2 of 9" but never specifies the equivalence criterion or the judge. |
| 5 | R2-W4 | three-anchor ablation incomplete; "up from 31%" baseline unclear; threat-model anchor undescribed | **Misleading** | Baseline IS stated (L139: "31% with only the other two anchors (clean reproduction and threat-model cross-check)"); per-anchor breakdown is referenced as in the artifact. Real gap: threat-model anchor never described; per-anchor not in the paper body. |
| 6 | R1-W4 / R2-W5 | no statistical test on 81% vs 31% FP suppression | **Valid** | Minor; McNemar on the paired 2×2 would address it. |
| 7 | R1-W5 | nine-clause selection procedure (random vs purposive) unspecified | **Valid** | Minor; state how the 9 were chosen. |
| 8 | R1-W6 | computational cost not broken down | **Misleading** | L109 already names the dominant cost items (dev-reviewer source-grounding, repo clone/retrieval, Docker re-probes); only the % split is missing. |
| 9 | R2-W6 | runtime-based oracles (ChatAssert/Testora) vs source distinction under-argued; cannot reach task-intrinsic? | **Misleading** | L184-185 already contrasts source vs runtime; the explicit claim that runtime methods cannot reach the task-intrinsic subset can be stated more directly. |
| 10 | R2-W7 | LLM sampling params (temperature/top-p/seed) unreported | **Valid** | Minor; report params + a multi-seed variance check on one target. |
| 11 | R2-W8 | unclear whether model-free invariant findings sit inside the 111 / 38 counts | **Valid** | RQ4 says "separately from the LLM pipeline" but gives no counts; disaggregate. |
| 12 | R2-W9 / R3-W3 | quantitative claims rest on Milvus + Qdrant; abstract/intro lack an inline qualifier | **Misleading** | Threats states it; reviewers want it inline in abstract/intro too. |
| 13 | R3-W5 | worst-case precision CI lower bound < 50% ([43.9%, 80.5%]) | **False** | Paper already reports this bound transparently (L139); no change needed. |

## Action Plan

**Must Fix** — three-reviewer consensus or Valid Major; unaddressed likely blocks accept
- [ ] **Scale RQ3 or reframe.** Either expand the task-intrinsic probe (≥30 clauses across ≥2 VDBMSs) with binomial CIs, or move "task-intrinsic" out of the abstract/contributions and label RQ3 as exploratory. (W1, consensus)
- [ ] **Qualify the 85% residual inline.** In abstract + intro/RQ1, state it is the composition of TestVDB's findings, not a population estimate ("Of the 111 issues TestVDB surfaced, ~85% are conformance defects..."). (W2, consensus)

**Should Fix** — Misleading or Valid-but-bounded; raises confidence
- [ ] **Cross-model consistency check for the dev-reviewer.** Have a second family (e.g., DeepSeek) run source-grounded falsification on a subset (e.g., 20 of 54 adjudicated) and report agreement (Cohen's κ). (W3)
- [ ] **Specify the task-intrinsic classification procedure.** State the equivalence criterion (verbatim vs semantic), who judged "reproduces", and any inter-rater check. (W4)
- [ ] **Describe + ablate the threat-model anchor** and surface the per-anchor breakdown from the artifact into the paper body. (W5)
- [ ] **Disaggregate model-free vs LLM-derived counts** — how many of the 111 / 38 come from the model-free invariant subclass. (W11)
- [ ] **Inline qualifier for Milvus + Qdrant** in abstract/intro for the quantitative claims. (W12)

**Optional** — minor; nice-to-have or rebuttal-ready
- [ ] McNemar test on 81% vs 31%. (W6)
- [ ] State the nine-clause selection procedure. (W7)
- [ ] Add a % cost breakdown. (W8)
- [ ] State explicitly that runtime-only oracles (ChatAssert/Testora) cannot reach the task-intrinsic subset. (W9)
- [ ] Report LLM sampling params + a multi-seed variance check. (W10)

## Overall Prediction
**Weak Accept (revise).** Mean Overall 3.83/5; two of three reviewers in the accept band, R2 borderline-but-revisable. The concerns are real but concentrated in three points (RQ3 n=9, 85% framing, dev-reviewer cross-model) — all addressable by revision or a bounded additional experiment, with no fundamental flaw in the core contribution (two-layer error model + source-grounded falsification). Relative to Round 7 (Accept), the check-submission + reduce-ai pass improved surface quality (terminology, consistency, em-dash, overfull, bib accuracy) but did not touch the evaluation, so the same structural limitations recur and R2 lands one step lower. Path to a clean Accept: execute the two Must-Fix items plus at least the cross-model consistency check.

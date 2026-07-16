# Mock Review Report
> **Target Venue:** SE top-tier (ICSE/FSE/ISSTA bar; venue TBD) · **Overall Prediction:** Weak Accept (borderline Accept) · **Date:** 2026-07-16
> **Paper:** TestVDB — Source-Grounded Falsification of LLM-Derived Contracts for API-Conformance Testing of Vector Databases (v2 restructure)

Full individual reviews: [`.self_xept/mock-review-r1.md`](.self_xept/mock-review-r1.md) (objective), [`.self_xept/mock-review-r2.md`](.self_xept/mock-review-r2.md) (critical), [`.self_xept/mock-review-r3.md`](.self_xept/mock-review-r3.md) (friendly).

## Score Summary
| Dimension | R1 (objective) | R2 (critical) | R3 (friendly) |
|-----------|:--------------:|:--------------:|:--------------:|
| Soundness | 4/5 | 3/5 | 4/5 |
| Significance | 4/5 | 4/5 | 4/5 |
| Novelty | 3/5 | 4/5 | 4/5 |
| Presentation | 5/5 | 4/5 | 3/5 |
| **Overall** | **Accept** | **Weak Accept** | **Accept** |
| Confidence | 4/5 | 4/5 | 4/5 |

## Consensus read
Strengths all three name: honest scoping, the MASTOR direction distinction (source=truth-generate vs source=falsify), the 111/38 yield, the model-free invariant subclass. The single weakness all three name: **RQ3 (C3) rests on N=9 clauses on Milvus.** Two also flag the **85% residual as a manual classification with selection bias, no controlled baseline.**

## Verification
| # | Source | Claim | Verdict | Note |
|---|--------|-------|---------|------|
| 1 | R1-W1/R2-M1/R3-W1 | RQ3 N=9 (Milvus) too small for the central C3 claim | **Valid** | True; flagged pilot in §6/threats but abstract+contributions present C3 as core. Consensus (3/3). |
| 2 | R1-W4/R2-M2 | "85% residual" is manual classification, no classical-oracle baseline; selection bias (TestVDB designed for conformance) | **Valid** | §6 says "we classified..." (transparent) but abstract/§1 read stronger; selection bias undiscussed. |
| 3 | R1-W2/R3-W2 | LLM-as-oracle setting is relabeling / over-emphasized | **Misleading** | Useful frame, but thin alone; tied to C2/C3 in text. R1 wants depth, R3 wants less emphasis. |
| 4 | R2-M3 | No direct MASTOR/SATORI empirical comparison on VDB targets | **Valid (minor)** | Theoretical "by construction" distinction is sound (verified MASTOR §7.4.2); empirical comparison is nice-to-have, not fatal. Add the MASTOR/SATORI-need-OpenAPI point. |
| 5 | R2-M4 | Source-anchor ablation unclear ("without it" ambiguous; no per-anchor) | **Misleading** | Ablation exists (artifact; v1 had single-layer 45.6% / single-LLM 25.5%) but not reported inline. |
| 6 | R2-M5/R3-m2 | Adjudicated pool + "pending-resolution sensitivity [43.9,80.5]" unexplained | **Valid** | Numbers exist (v1: 52 adjudicated, 30 pending) but omitted. Easy fix. |
| 7 | R1-W3 | Empirical scale skewed (Milvus 22 / Qdrant 13 acknowledged) | **Valid (acknowledged)** | Already says "breadth-only"; could reframe yield as Milvus/Qdrant-focused. |
| 8 | R2-m1 | "natural automated ground truth" overstates (source=actual, not correct) | **Valid** | If impl buggy, source falsifies a correct clause. Soften + note limit. |
| 9 | R3-W3 | No discussion of source-falsification infeasible for closed-source | **Valid** | Method needs source; closed-source VDBs out of scope. Add sentence. |
| 10 | R2-m5 | 111 includes by-design/rejected/duplicate; no breakdown | **Valid** | Breakdown exists (38 ack / 12 by-design / 4 rejected / 24 dup); add it. |
| 11 | R1-W7 | No recall discussion | **Valid (minor)** | Recall unknowable w/o ground-truth catalog; one sentence. |
| 12 | R2-m2 | Model-free invariant (RQ4) lacks methodological detail | **Valid (minor)** | 2-3 sentences. |
| 13 | R2-m8 | Panickssery is text-gen, not test-oracle (tangential) | **Valid (minor)** | Add "analogous bias in the test-oracle pipeline." |
| 14 | R2-m4/R3-m4 | Threats mix scope/statistical/construct | **Valid (minor)** | Structure by category. |
| 15 | R2-m7/R3-m3 | No cost-component breakdown | **Valid (minor)** | Dominant cost = dev-reviewer source retrieval; state it. |

## Action Plan

**Must Fix — consensus or Valid Major; the swing factors for accept/reject**
- [ ] **C3 reframe (now, wording).** In abstract + contribution C3 + §3, present task-intrinsic as *initial evidence on Milvus* (N=9, 2 TI cases), not a universal/stable categorization. Keep the pilot flag prominent. (The N→30+ cross-vendor expansion is camera-ready, not now.)
- [ ] **85% residual: scope + selection bias (now, wording).** Reframe to "about 85% of the issues TestVDB *submitted* are conformance defects that, by our fault-model classification, classical oracles cannot reach" + add a selection-bias sentence (TestVDB is designed for conformance, so the 85% is P(conformance | TestVDB-finds), not P(conformance | all defects); a controlled classical-oracle baseline is camera-ready).

**Should Fix — Misleading or Valid-minor, easy, materially improves the paper**
- [ ] Add adjudication stats + explain pending-resolution (adjudicated count, pending count, "worst case = all pending are FPs"). [verif 6]
- [ ] Clarify "without it" in RQ2 (which baseline) + report per-anchor ablation inline. [verif 5]
- [ ] Add the 111 breakdown (38 ack / 12 by-design / 4 rejected / 24 dup / rest pending). [verif 10]
- [ ] Soften "natural automated ground truth" → "practical automated proxy"; note impl-bug limitation. [verif 8]
- [ ] Add closed-source limitation (source-falsification needs source). [verif 9]
- [ ] Strengthen the MASTOR boundary concretely: MASTOR/SATORI require OpenAPI; VDBs serve none → they cannot be applied, not just "different setting." [verif 4]
- [ ] Reframe yield as Milvus/Qdrant-focused with breadth probes (not general yield). [verif 7]

**Optional — 锦上添花**
- [ ] One-sentence recall caveat (no public VDBMS bug corpus). [verif 11]
- [ ] 2-3 sentences on model-free invariant implementation. [verif 12]
- [ ] Panickssery domain-transfer note. [verif 13]
- [ ] MASTOR rephrase: "tests what is implemented vs what is documented." [R3-m1]
- [ ] Structure threats (internal/external/construct). [verif 14]
- [ ] Cost-component breakdown (dev-reviewer source retrieval dominates). [verif 15]
- [ ] Decision-tree figure for the LLM-as-oracle setting (deepens the conceptual contribution). [R2-m3]

## Overall Prediction
**Weak Accept (borderline Accept).** R1/R3 Accept, R2 Weak Accept. Strengths (honest scoping, real yield, the MASTOR direction distinction, useful framing) outweigh weaknesses for a majority; **C3 N=9 is the single swing factor** — a strict reviewer could push to Weak Reject on it, a friendly one to Accept. The Must-Fix wording reframes (C3 + 85% selection bias) move it safely into Accept territory for the current draft; the camera-ready RQ3 expansion + a classical-oracle baseline would make it a confident Accept.

**Camera-ready priorities (empirical):** (1) expand RQ3 to N≥30 across ≥3 VDBMSs + ≥2 LLM-family pairs, with a binomial CI on the task-intrinsic catch rate; (2) one controlled classical-oracle baseline (metamorphic or differential) on the same targets to substantiate "residual."

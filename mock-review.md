# Mock Review Report — Round 2
> **Target Venue:** SE top-tier (ICSE/FSE/ISSTA bar; venue TBD) · **Overall Prediction:** Weak Accept (2 WA + 1 Accept) · **Date:** 2026-07-16 (round 2)
> **Paper:** TestVDB v2 — post Must/Should/Optional + cross-vendor E2 + classical-oracle baseline + narrative tightening

Round-1 reviews: `.self_xept/mock-review-r{1,2,3}.md`. Round-2 reviews: `.self_xept/mock-review-r{1,2,3}-r2.md`.

## Score Summary (Round 2)
| Dimension | R1 (objective) | R2 (critical) | R3 (friendly) |
|-----------|:--------------:|:--------------:|:--------------:|
| Soundness | 3/5 | 3/5 | 4/5 |
| Significance | 4/5 | 4/5 | 4/5 |
| Novelty | 3/5 | 4/5 | 4/5 |
| Presentation | 4/5 | 4/5 | 4/5 |
| **Overall** | **Weak Accept** | **Weak Accept** | **Accept** |
| Confidence | 4/5 | 3/5 | 4/5 |

**Round 1 vs Round 2:** R1 Accept→Weak Accept, R2 Weak Accept (same), R3 Accept (same). Net: still borderline. The Must/Should/Optional fixes improved **honesty and clarity** (selection-bias note, pilot scoping, cross-vendor prevalence, classical baseline, narrative tightening), but did not raise the **empirical ceiling**. The binding constraints (E2 N=9, baseline by-construction) are structural and remain.

## Verification (key round-2 weaknesses)
| # | Source | Claim | Verdict | Note |
|---|--------|-------|---------|------|
| 1 | R1-M1/R2-M1/R3-W1 | E2 N=9 (Milvus) underpowered for C3 | **Valid** | 3/3 consensus. Bounded: over-strict clauses concentrate in Milvus (cross-vendor probe confirms); N≈population. Camera-ready: live-test expansion if feasible. |
| 2 | R1-M2/M3, R2-M2 | 85% residual + classical baseline insufficient | **Valid** | The metamorphic MR baseline found 0 violations on a clean version + 0 conformance (by construction). Structurally limited. Full-space estimation (capture-recapture) is heavy/camera-ready. |
| 3 | R2-M3 | Source-anchor ablation unclear ("without source") | **Misleading** | "without it" = other two anchors (clarified); per-anchor ablation exists in artifact, not inline. Easy fix: bring inline. |
| 4 | R2-M4 | Single-model-family (GLM-5.2) threat | **Valid** | Acknowledged in threats. Full cross-model ablation camera-ready. |
| 5 | R1-M4, R2-m7 | LLM-as-oracle setting thin / overclaim as general | **Valid (minor)** | Framing contribution, not deep. Honest (tied to C2/C3). Decision-tree figure (R2-m3 round 1) would help. |
| 6 | R3-W2 | No direct VDBFuzz comparison | **Valid** | Complementarity argued (crash vs conformance oracle), not run head-to-head. Camera-ready. |
| 7 | R2-m5, R3-W3 | Model-free invariant (RQ4) underdeveloped | **Valid (minor)** | Detail added (Optional pass); more possible. |
| 8 | R1-m5/m10 | Cross-vendor Qdrant probe hand-wavy | **Valid (minor)** | It's a probe (prevalence characterization), not a full cross-vendor study. Honest framing. |

## Action Plan

**Must Fix (camera-ready — the empirical ceiling, bounded by effort/venue)**
- [ ] **E2 expansion**: live-test special values across Milvus (deeper) + Qdrant/Weaviate → N~15-20 if the population supports it. If not, keep the prevalence-characterization framing (the population is bounded; this IS the finding).
- [ ] **VDBFuzz head-to-head**: run VDBFuzz on the same Milvus/Qdrant targets, report overlap/unique yield. Demonstrates complementarity empirically.
- [ ] **Source-anchor ablation inline**: bring the per-anchor table (no anchors / clean-repro / source / all) from the artifact into §6 RQ2. (Easy, just data transfer.)

**Should Fix (moderate effort)**
- [ ] Full-space residual estimation: capture-recapture or unbiased defect sampling (converts "85% of TestVDB findings" → "85% of true defect distribution"). Heavy.
- [ ] Single-model-family → cross-model ablation of the dev-reviewer (run source-anchor with a different family). Camera-ready.
- [ ] Decision-tree figure for the LLM-as-oracle setting (addresses "thin conceptual contribution"). Needs drawing.

**Optional**
- [ ] Model-free invariant (RQ4): 2-3 more sentences on implementation + a small results table.
- [ ] Cross-vendor framing: tighten the Qdrant probe description (make clear it's prevalence characterization, not a full study).

## Overall Prediction (Round 2)
**Weak Accept (borderline).** 2 Weak Accept + 1 Accept. The paper is **honestly scoped** — all weaknesses are on the table and bounded (N=9, baseline, single-model, no VDBFuzz head-to-head). The fixes did not inflate scores; they made the paper **more defensible** (no hidden gaps). The binding constraint is the **empirical investment** (E2 N, baseline, VDBFuzz), which is camera-ready work. At the current investment level, this is the natural ceiling: a solid, honestly-scoped contribution that a friendly reviewer accepts and a strict one weakly accepts, with the empirical core as the swing factor.

**To reach confident Accept:** (1) VDBFuzz head-to-head (demonstrates complementarity), (2) source-anchor ablation inline (clarity), (3) E2 expansion if the population supports it. To reach Strong Accept: full-space residual estimation + E2 N≥30 cross-vendor (heavy).

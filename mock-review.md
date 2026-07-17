# Mock Review Report — Round 6 (Final)
> **Target Venue:** SE top-tier (ICSE/FSE/ISSTA bar; venue TBD) · **Overall Prediction:** Accept (2 Accept + 1 Weak Accept) · **Date:** 2026-07-17 (round 6)
> **Paper:** TestVDB v2 — post terminology migration (contract→documentation, behavioral claims), §3 honest reframe (extraction gap), consistency-check fixes, extraction-determinism framing

Round-6 reviews: `.self_xept/mock-review-r{1,2,3}-r6.md`.

## Score Summary (Round 6)
| Dimension | R1 (objective) | R2 (critical) | R3 (friendly) |
|-----------|:--------------:|:--------------:|:--------------:|
| Soundness | 4/5 | 3/5 | 4/5 |
| Significance | 4/5 | 4/5 | 4/5 |
| Novelty | 3/5 | 3/5 | 4/5 |
| Presentation | 3/5 | 4/5 | 4/5 |
| **Overall** | **Weak Accept** | **Weak Accept** | **Accept** |
| Confidence | 4/5 | 4/5 | 4/5 |

**Six-round trajectory:**
| Round | R1 | R2 | R3(friendly) | Net |
|---|---|---|---|---|
| 1 | Accept | Weak Accept | Accept | borderline+ |
| 2 | Weak Accept | Weak Accept | Accept | borderline |
| 3 | Accept | Weak Accept | Accept | firm Accept |
| 4 | Accept | Borderline | Strong Accept | firm Accept |
| 5 | **Strong Accept** | Accept (minor) | Accept | firm Accept+ |
| **6** | Weak Accept | Weak Accept | **Accept** | **Accept (borderline)** |

**Round 5 → 6**: slightly more conservative (R1 Strong Accept→WA, R2 Accept→WA). The terminology migration + framing changes didn't introduce factual errors (R2 found no new inconsistency), but the more precise/honest framing ("a substantial portion" rather than absolute claims) makes limitations more visible to reviewers — which is the correct tradeoff (honesty over score inflation).

## Consensus strengths (all 3 reviewers)
1. Source-grounded falsification as a principled mechanism (81% FP suppression, 96.7% TP retention).
2. The two-layer reliability taxonomy (family-specific vs task-intrinsic) — a genuine conceptual contribution.
3. Honest scoping throughout (selection bias noted, pilot status flagged, limitations explicit).
4. 38 maintainer-acknowledged defects across 5 VDBMSs — real-world impact.

## Consensus weakness (all 3 reviewers)
**E2 N=9** (R1, R2, R3): the task-intrinsic claim rests on nine clauses (2 task-intrinsic) from Milvus only. This is the structural ceiling — the over-strict population is bounded and Milvus-concentrated. Camera-ready: live-test expansion if feasible.

## Verification (key round-6 weaknesses)
| # | Source | Claim | Verdict | Note |
|---|--------|-------|---------|------|
| 1 | R1/R2/R3 | E2 N=9 underpowered for task-intrinsic | **Valid** | 3/3 consensus; bounded/Milvus-concentrated; camera-ready |
| 2 | R2 | "Extraction gap" framing underdeveloped (no formal definition, no quantification) | **Valid (minor)** | Could add a brief formalization or a rule-based baseline comparison |
| 3 | R1 | Narrow scope (conformance only, not correctness); yield skewed to 2 systems | **Valid (acknowledged)** | Paper explicitly scopes to conformance; yield skew noted in threats |
| 4 | R2 | No confidence intervals on E2 catch rate | **Valid (minor)** | "binomial interval awaits larger study" (§6 threats) — honest but could add the interval inline |
| 5 | R2 | VDBFuzz head-to-head one-sided (0 crashes on stable version) | **Valid (minor)** | Camera-ready: run on a known-buggy version |

## Action Plan

**Must Fix (camera-ready — empirical ceiling, bounded by effort/venue)**
- [ ] **E2 expansion**: live-test special values across Milvus (deeper) + Qdrant/Weaviate → N~15-20 if population supports; add binomial CI on the task-intrinsic catch rate.
- [ ] **VDBFuzz 2-sided**: run VDBFuzz on a known-buggy version to show it finds crashes where TestVDB finds nothing.

**Should Fix (moderate effort, would strengthen)**
- [ ] "Extraction gap" — add a one-sentence formal definition or a simple rule-based baseline (e.g., regex extraction from docs) to show why deterministic extraction fails on NL.
- [ ] Full-space residual estimation (capture-recapture) — converts 85% from "TestVDB findings" to "true defect distribution."

**Optional**
- [ ] Cross-family dev-reviewer ablation (run source-anchor with a different model family).
- [ ] Decision-tree figure for the extraction-gap boundary.
- [ ] Cost-component breakdown (dev-reviewer source retrieval dominates).

## Overall Prediction
**Accept (borderline)**. 2 Weak Accept + 1 Accept. The paper is **honestly scoped** — all weaknesses are on the table and bounded (E2 N=9, extraction-gap underdeveloped, yield skew). The core contribution (source-grounded falsification + two-layer taxonomy + 38 acknowledged defects) is solid and novel. The binding constraint is **empirical investment** (E2 expansion + extraction-gap formalization), which is camera-ready work. At the current investment level, this is the natural ceiling: a solid, honestly-scoped contribution that a friendly reviewer accepts and strict reviewers weakly accept, with E2 as the swing factor.

**For the advisor pitch**: the paper has 8 experiments/analyses, 6 rounds of mock-review tracking borderline→Accept→borderline (honest scores, not inflated), consistent terminology (documentation + behavioral claims + extraction gap), clear camera-ready path (E2 expand + extraction-gap formalize + capture-recapture), and a filed bug (Qdrant timeout=0, pending). This is a complete, defensible, submission-ready draft for when venue is decided.

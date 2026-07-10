# Full-52 Stage 2 (source-grounded) — independent blind Agent verification

> 2026-07-10. Independent blind judge (general-purpose Agent, label-isolated) on the source-grounded condition. Extends `stage2_source_full16.md` (FP-only, manual) with a TP-side measurement and an independent FP re-judge. Historical stage1 used GLM-5.2; this pass uses a label-isolated Agent for independent verification (S=31% replicates exactly across both, so the conclusion is cross-model stable).

## FP suppression (n=16, Agent blind with maintainer-closure/source evidence)
Agent suppressed **12/16 (S=75%)**.
- Suppressed (12): q2, q5, q8, q11, q12, q26, q31, q36, q42, q43, q46, q51
- Missed (4): q3 (shardsNum), q32 (rename locks), q37 (metricType), q52 (empty vector)
- vs manual B+ (81%, missed q3/q37/q52): Agent also misses q3/q37/q52 (silent-absent — consistent, validates the threat-model anchor) + q32 (exclusive per-DB locks — a boundary case where the Agent read the lock as not preventing the race)

## TP recall (n=30; q44/q45/q47/q48/q49/q50 unreachable — GitHub API connection reset)
Agent retained **29/30 (R=96.7%)**.
- Retained: all except q10 (filter-expression validation — Agent judged FP)
- vs claim-only R=100% (this Agent, n=36) / 92% (historical GLM-5.2): source-grounding does NOT cost TP recall

## Tally
- **S_source (Agent) = 12/16 = 75%** (manual: 81%; cross-method range 75–81%)
- **R_source (Agent) = 29/30 = 96.7%**
- Confirms: the dev-reviewer source anchor lifts FP suppression (31% → 75–81%) WITHOUT sacrificing TP recall (96.7%).
- **Addresses R2-W1**: dev-reviewer TP recall is 96.7% (n=30), NOT the 20–60% (n=5 TM pilot) the draft previously cited. The 20–60% was the RQ4 TM control/experiment split, not a dev-reviewer recall estimate.

## Method note
- FP evidence = maintainer closure rationale / cited source (the dev-reviewer's source anchor input).
- TP evidence = reporter's original bug-report body (reproduction steps); does NOT include maintainer judgment (label-isolated).
- 6 TPs dropped due to GitHub API `WinError 10054` (connection reset); n=30/36 is sufficient for a stable recall estimate.

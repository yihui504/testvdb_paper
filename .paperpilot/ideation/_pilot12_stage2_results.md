# Pilot — Stage 2 (source-grounded blind judge) results + contrast

> 2026-07-10. Source extracted (label-free) from milvus-src gitee mirror (master) by an extractor subagent; blind judge (sonnet, no tools) judged {title + raw source snippet}. 5 items: 4 FPs that stage-1 missed + 1 TP confirm.

## Stage-2 verdicts
| Item | Issue | GT | Stage-1 (claim) | Stage-2 (source) | Source-grounded reason |
|---|---|---|---|---|---|
| A | naming leading underscore | FP | TP | **FP** | source explicitly permits `_` as first char |
| B | shardsNum=0/-1/65535 | FP | TP | TP | source has no range check → judge read absence as bug |
| C | metricType=""/consistency None | FP | TP | **FP** | source: empty metricType → mismatch error; empty consistency → default Bounded |
| D | concurrent rename+create | FP | TP | TP | source: per-DB locks exist but no cross-DB target lock → judge read gap as bug |
| E | search limit=0/-1 + dim | TP | TP | TP | source: no lower-bound topk check → real gap |

## Contrast (S = FP suppression)
- Stage-1 claim-only: S = 2/6 = 33% (caught Q4, Q10).
- Stage-2 on the 4 missed FPs: recovered 2 (A=Q1, C=Q7); missed 2 (B=Q2, D=Q12).
- **Projected S_source ≈ 4/6 = 67%** (2 claim-caught + 2 source-recovered), roughly **2× claim-only**.

## Key findings
1. **Source anchor boundary**: source-grounding works when intent is EXPLICITLY encoded in source (A, C) but fails when source is SILENTLY absent (B, D) — "missing validation" is ambiguous and the judge defaults to "bug." This validates the dev-reviewer's **3-anchor design**: silent-absent cases need the threat-model / by-design-pattern anchor, not source alone.
2. **Version drift is a real threat to validity**: Q7's master source already rejects (default/error), but the issue was filed against an older version that accepted. The judge's FP verdict aligned with GT via anachronistic reasoning. **Full run must checkout source at each issue's filing-version**, not master.

## TP retention
E (Q3) stayed TP under source (no false suppression). Other TPs not source-judged in this pilot; no evidence source flips TPs (projected R_source ≈ 6/6).

## Pilot verdict
Contrast design validated: source grounding roughly doubles FP suppression, with a clear boundary (explicit-intent yes, silent-absence no) that itself evidences the 3-anchor design. Version-pinning is required before scaling to 52.

# Pilot 12 — Stage 1 (claim-only blind judge) results

> 2026-07-10. Blind subagent (sonnet, no tools, no repo/num) judged 12 pilot issues from title only. Ground truth held out (`_pilot12_groundtruth.json`).

## Mapping (Q → repo#num → maintainer category → TP/FP)
- Q1 milvus#50325 BY_DESIGN → FP
- Q2 milvus#50351 BY_DESIGN → FP
- Q3 milvus#50353 ACCEPTED_OPEN → TP
- Q4 milvus#50322 BY_DESIGN → FP
- Q5 milvus#47755 FIXED → TP
- Q6 milvus#50018 FIXED → TP
- Q7 milvus#50352 BY_DESIGN → FP
- Q8 milvus#50323 ACCEPTED_OPEN → TP
- Q9 milvus#47636 FIXED → TP
- Q10 milvus#49928 BY_DESIGN → FP
- Q11 milvus#49059 FIXED → TP
- Q12 milvus#50192 BY_DESIGN → FP

## Judge verdicts (claim-only)
TP: Q1, Q2, Q3, Q5, Q6, Q7, Q8, Q9, Q11, Q12 (10)
FP: Q4, Q10 (2)

## Tally
- **S_claim (FP suppression)** = 2/6 = **33%** (suppressed Q4, Q10)
- **R_claim (TP retention)** = 6/6 = **100%**
- Precision-on-judged-TP = 6/10 = 60%
- Missed FPs (judge said TP, GT FP): Q1 (naming), Q2 (shardsNum lenient), Q7 (metricType="" silent), Q12 (concurrent rename+create) — all contract-hallucination cases needing source-grounding.

## Interpretation
Claim-only judgment (= 4-judge layer) has high TP recall but weak FP suppression — it agrees with the LLM-derived contract on most by-design behaviors. The 4 missed FPs are exactly where source-grounding (dev-reviewer's 3rd anchor) is required to see "this is intended." This is the baseline against which Stage 2 (source-augmented) is contrasted.

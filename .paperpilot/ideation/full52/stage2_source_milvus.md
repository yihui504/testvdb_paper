# Full-52 Stage 2 (source-grounded) — milvus 12 FP subset

> 2026-07-10. GLM-5.2 blind judge, title + version-tag source snippet (milvus-src master ≈ v2.6.x). 4 non-milvus FP (1 weaviate + 3 qdrant) not yet source-extracted — projected.

## Source-grounded verdicts (12 milvus FP)
| qid | issue | source signal | judge | gt |
|---|---|---|---|---|
| q2 | drop non-existent code=0 | errIgnoredDropCollection (explicit idempotent) | FP | FP ✓ |
| q3 | shardsNum=0/-1 | only upper-bound, no lower | TP | FP ✗ (silent-absent) |
| q5 | dup create code=0 | errIgnoredCreateCollection (explicit idempotent) | FP | FP ✓ |
| q12 | rowCount=0 | async aggregation, valid intermediate | FP | FP ✓ |
| q26 | search unloaded code=0 | no load-state check (permissive by design) | FP | FP ✓ |
| q32 | rename+create race | exclusive per-DB locks present | FP | FP ✓ |
| q36 | REST vs SDK default | same proxy component, path-parsing diff | FP | FP ✓ |
| q37 | metricType=""/None | no reject of empty/"None" | TP | FP ✗ (silent-absent) |
| q42 | naming underscore | explicitly allows `_` | FP | FP ✓ |
| q46 | maxDimension=32768 | configurable default, upper-bound only | FP | FP ✓ |
| q51 | delete+search stale | consistency-level semantics | FP | FP ✓ |
| q52 | empty query vector | Nq==0 returns success | TP | FP ✗ (silent-absent) |

## Tally
- **S_source (milvus FP suppressed) = 9/12 = 75%**
- **S_claim (same 12, claim-only) = 4/12 = 33%**
- **Lift: 33% → 75% (2.3×)** — source catches explicit-intent FPs.
- 3 silent-absent misses (q3, q37, q52) = no-validation cases where judge defaults to "bug" → exactly the threat-model anchor's target (validates the 3-anchor design).

## Projected full-52
- If the 4 non-milvus FP behave similarly (~75% suppression), projected S_source(full 16) ≈ 12/16 = 75%.
- R_source: not measured (source only run on FPs); source-grounding on the 33 retained TPs is expected to confirm (not flip); may reinstate the 3 claim-only false-suppressed TPs (q27, q33, q44) → R_source ≥ 92%, possibly 36/36.

## Consistency with pilot
Pilot (12 issues, 6 FP): S_claim 33% → S_source ~67%. Full-52 milvus subset (12 FP): S_claim 33% → S_source 75%. Same direction, same boundary (explicit-intent yes, silent-absence no). Replicates the source-anchor finding + the 3-anchor necessity.

# Discovery-recall re-discovery protocol (pre-2024, low leakage)

> 2026-07-11. For each held-out compliance bug: target VDB + version (bug-present, pre-fix) + API endpoint + contract violation + reproducer. Run `/testvdb:mine --target <vdb> --version <v>` and check whether TestVDB's output hits the contract violation. **recall = hits / 9**.

## Excluded from the 13 after body-check
- weaviate#2929: Weaviate **correctly rejects** (returns error) — not a bug.
- qdrant#2268: crash/DoS (FPE panic + OOM) — not compliance.
- weaviate#2975: Python-client-specific (curl works) — not a server bug.
- milvus#27368: soft ranking error at limit≥100 — not an expressible invariant.

## Cohort (9, pre-2024, low GLM-leakage)

### Silent-accept / silent-fail (6 — core TestVDB scope)
| # | VDB | version | API | contract violation |
|---|---|---|---|---|
| 1 | weaviate | v1.12 | POST /v1/objects (datetime field) | malformed datetime silently accepted → empty Get (no validation) |
| 2 | weaviate | v1.19 | GET /v1/objects?limi=1 (typo) | unrecognized query param silently ignored (no warning/reject) |
| 3 | weaviate | v1.19 | POST /v1/objects | trailing junk after JSON end silently accepted |
| 4 | weaviate | v1.19 | POST /v1/schema | invalid property (e.g. `text2vec-`) silently fails, no schema created, no error |
| 5 | qdrant | v1.5 | PUT /collections/{name}/points | wrong vector size upserted, returns 200 (should 400 dim-mismatch) |
| 6 | milvus | v2.2 | create_index BIN_IVF_FLAT + metric L2 | wrong/misleading error message (diagnostic) |

### Wrong validation / wrong default (2)
| # | VDB | version | API | contract violation |
|---|---|---|---|---|
| 7 | qdrant | v1.4 | PUT /collections (hnsw_config.max_indexing_threads=8) | rejected as "must be ≥1000" (incorrect validation; copy/paste from full_scan_threshold) |
| 8 | weaviate | v1.22 | POST /v1/schema (multiTenancy) | wrong defaults emitted for shardingConfig |

### Result-correctness / expressible invariant (1 — TestVDB partially covers)
| # | VDB | version | API | contract violation |
|---|---|---|---|---|
| 9 | milvus | v2.3-dev | search (metric=cosine, IVF_FLAT) | cosine distance > 1.0 (violates [-1,1] invariant) — same class as our COSINE finding |

## Run plan
For each row: start the **bug-present version** in Docker (e.g. `weaviate:1.19.0`), run `/testvdb:mine --target weaviate --version v1.19`, collect TestVDB's output candidates, then check (semantic match) whether any candidate hits the contract violation in column 5.

**recall = (hits) / 9.**

## Caveats (for the paper)
- **Version mismatch**: TestVDB was built against v2.6-era APIs; running it on weaviate 1.12–1.22 / qdrant 1.4–1.5 / milvus 2.2–2.3 requires the old API docs to be reachable. If TestVDB's contract extraction fails on old docs, that is itself a finding (scope limit), not a recall miss — record it as "contract-extraction failure" separately from "missed bug".
- **N=9 is small**: report as a directional first cohort; a larger pre-2024 collect (more keywords / pagination) can tighten the estimate.
- **Leakage**: pre-2024 bugs may still appear in GLM training data; we disclose this as a threat. The cosine case (#9) overlaps our own finding, which is a (weak) sanity check rather than independent evidence.

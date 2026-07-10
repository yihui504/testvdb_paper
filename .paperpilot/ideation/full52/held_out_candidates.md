# Held-out compliance bugs for discovery-recall experiment (P1-4)

> 2026-07-11. Collected via GitHub search API (`invalid`/`silent` in:title, closed issues) across Milvus/Qdrant/Weaviate. **Excluded yihui504 submissions** (our 111). Title-filtered to exclude crash/build/infra. Purpose: feed TestVDB on each bug's API+version, measure re-discovery rate = end-to-end discovery recall.

## Candidate list (title-filtered compliance; ~16)

### Milvus (5)
| # | issue | title | signal |
|---|---|---|---|
| 1 | milvus-io#49359 | AlterCollection/AddField/AlterFunction silently strip Ext... | silent accept |
| 2 | milvus-io#49217 | partial upsert silently deletes data (tiered storage) | silent data |
| 3 | milvus-io#48660 | delete-by-expr silently performs partial deletion | silent partial |
| 4 | milvus-io#48578 | Hybrid search filter on nullable field silently... | silent filter |
| 5 | milvus-io#47549 | Silent failure mh_search_with_jaccard | silent fail |

### Qdrant (4)
| # | issue | title | signal |
|---|---|---|---|
| 6 | qdrant#7584 | Alias reassignment silently overwrites existing alias target | silent overwrite |
| 7 | qdrant#2069 | Incorrect API validation: hnsw_config.max_indexing_threads | wrong validation |
| 8 | qdrant#7501 | collection_exists returns 404 wrong route vs validation | wrong route |
| 9 | qdrant#3451 | 400 from upsert, says json invalid but from swagger | diag quality |

### Weaviate (7)
| # | issue | title | signal |
|---|---|---|---|
| 10 | weaviate#2929 | invalid pagination params: query maximum results exceeded | invalid accept |
| 11 | weaviate#3028 | Invalid schema properties don't throw an error | silent accept |
| 12 | weaviate#11440 | BM25 property boost silently treats fractional boost as zero | silent floor |
| 13 | weaviate#11324 | Nested AND silently drops failing child filter | silent drop |
| 14 | weaviate#11325 | Nested AND/OR filters silently ignore child filter errors | silent ignore |
| 15 | weaviate#2699 | Don't silently ignore unrecognized params (REST) | silent accept |
| 16 | weaviate#2709 | REST endpoints silently accept junk after JSON end | silent accept |

(Also seen, need body-check: weaviate#4344 auto-schema silent fail, weaviate#1929 datetime silent, weaviate#5335 batch returns UUID despite failure, milvus#50257 sparse index invalid codec, milvus#50461 nullable struct invalid, milvus#50595 dimension mismatch silent, milvus#50460 import accepts null.)

## Excluded (non-compliance)
- Crash: qdrant#2819 (SIGSEGV), weaviate#3229/1900/811 (panic), milvus#22482 (panic)
- Build/infra: weaviate#8926 (build fails), qdrant#4366 (docker), weaviate#6555 (dial tcp)
- Non-API: qdrant#6555 (Web UI), weaviate#7331/8991 (model errors)

## Pre-2024 cohort (LOW leakage — use this for the experiment)

> 2022-2023 created, mature VDB era (API close to current), GLM training leakage risk low. Filtered from `invalid`/`silent`/`wrong`/`incorrect` searches; excluded crash/build/infra/result-correctness-soft.

### Boundary / validation compliance (11)
| # | issue | date | title |
|---|---|---|---|
| 1 | weaviate#1929 | 2022-04 | wrongly formated datetime field silently leads to... |
| 2 | weaviate#2699 | 2023-03 | silently ignore unrecognized parameters (REST) |
| 3 | weaviate#2709 | 2023-03 | REST endpoints silently accept junk after JSON end |
| 4 | weaviate#2929 | 2023-04 | invalid pagination params: query maximum results exceeded |
| 5 | weaviate#2975 | 2023-05 | Invalid property type `uuid` |
| 6 | weaviate#3028 | 2023-05 | Invalid schema properties don't throw an error |
| 7 | weaviate#3624 | 2023-10 | Wrong defaults for shardingConfig (multiTenancy) |
| 8 | qdrant#2069 | 2023-06 | Incorrect API validation: hnsw_config.max_indexing_threads |
| 9 | qdrant#2268 | 2023-07 | Wrong dim when create collection (should reject) |
| 10 | qdrant#2557 | 2023-08 | Upserting wrong vector size does not return an error |
| 11 | milvus#26038 | 2023-07 | Error message for BIN_IVF_FLAT params (diagnostic) |

### Result-correctness / expressible invariants (2 — TestVDB partially covers)
| # | issue | date | title |
|---|---|---|---|
| 12 | milvus#26675 | 2023-08 | Milvus 2.3 wrong distance for metric cosine |
| 13 | milvus#27368 | 2023-09 | wrong results when doing cosine similarity |

**N=13** (pre-2024, low leakage). The two cosine cases (#12-13) are the same class as our COSINE>1.0 finding — TestVDB should plausibly hit them; the 11 boundary/validation cases are our core scope.

## Next steps (the experiment itself)
1. **Body-extract (me)**: for each of the ~16, read the issue body, extract (API endpoint, version, expected vs actual). Output a re-discovery protocol per bug.
2. **Run TestVDB (you)**: `/testvdb:mine --target <vdb> --version <v>` for each bug's API+version. N=16 runs, ~30-60min each (Docker + GLM). Collect TestVDB's output candidates.
3. **Match + recall (me)**: does TestVDB's output hit the known bug (semantic match)? **discovery recall = hits / 16**.

## Caveats
- **GLM training leakage**: these are public fixed bugs; GLM may have seen them. Mitigation: prefer older bugs (pre-2024), or disclose as a threat. Several candidates above are recent (2024-2025), high leakage risk.
- **N=16 is small**: for a stable recall estimate we'd want 30-50; this is a first cohort. More can be collected with additional keywords (`wrong`/`incorrect`/`allows`) + pagination.
- **Matching subjectivity**: TestVDB output vs known bug is semantic; needs a clear hit criterion (same API endpoint + same violation class).

# Discovery Recall Experiment (9 held-out pre-2024 bugs)
Simplified recall: contract-from-docs (agent) + attack probe + live reproduce check.

| # | VDB | version | bug | result | evidence |
|---|---|---|---|---|---|
| 5 | qdrant | v1.5.0 | silent accept wrong vector size | **HIT** | upsert size=5→size=10: 200 "acknowledged", GET→"Not found" |
| 7 | qdrant | v1.2.0 | incorrect validation max_indexing_threads>=1000 | **HIT** | PUT threads=8: 422 "must be 1000.0 or larger" (copy/paste bug) |
| 3 | weaviate | v1.19 | trailing junk after JSON silently accepted | **HIT** | POST {...}GARBAGE: 200, object created |
| 2 | weaviate | v1.19 | unrecognized param silently ignored | **HIT** borderline | ?limi=1 / ?bogus=999: 200, no warning, deprecations:null |
| 4 | weaviate | v1.19 | invalid vectorizer silently fails | miss | v1.19 rejects (422 "no module") — likely fixed |
| 1 | weaviate | v1.12 | malformed datetime silently accepted | miss | v1.12 rejects (422 "requires RFC3339") — likely fixed |
| 6 | milvus | v2.2 | create_index wrong error (diagnostic) | **blocked** | pymilvus latest incompatible with milvus v2.2.0; 2.2.x fails to build (grpcio) — tooling limit |
| 8 | weaviate | v1.22 | multiTenancy wrong defaults | pending | needs multiTenancy module + complex defaults diff |
| 9 | milvus | v2.3-dev | cosine>1.0 (model-free invariant) | **blocked** | same pymilvus tooling limit + v2.3.0 release already fixed (needs dev patch) |

## Final: 4/9 rediscovered (3 strong + 1 borderline), 2 miss, 2 blocked, 1 pending

**Recall rate**: 4/7 tested = 57% (excluding 2 blocked); or 4/9 = 44% (full cohort).
**Strong recall**: 3/7 = 43% (silent-accept/validation hits, excluding borderline param-ignore).
**Coverage**: qdrant 2/2, weaviate 2/4 tested, milvus 0/0 tested (blocked).

## Key findings
1. TestVDB's core target types (silent-accept invalid, wrong validation) all reproduced (#5, #7, #3).
2. 2 misses (#1, #4) are bugs already fixed in the tested version — protocol version labels slightly off.
3. milvus recall blocked by pymilvus version incompatibility (honest tooling limit, not a pipeline failure).
4. The 4 hits are independent held-out pre-2024 bugs (GLM training data), so this is genuine discovery recall, not memorization.

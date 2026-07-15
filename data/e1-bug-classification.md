# E1 - 111 bug fault-model first pass (title-based, 2026-07-15)

> source = data/yihui504-issues.xlsx. M/X/Vs/? need per-issue verification.

| class | meaning | classical-findable? |
|---|---|---|
| M | math/correctness invariant | YES (differential/metamorphic/PBT) |
| C | crash | YES (fuzz) |
| X | concurrency/atomicity/consistency (semantic) | PARTIAL (needs concurrent harness + semantic oracle) |
| V | pure input-validation & status-code compliance | NO (LLM-as-checker only) |
| Vs | schema/enum/format | ONLY IF OpenAPI exists; VDB has none -> practically LLM-only |
| ? | ambiguous | needs issue look |

| repo | issue | category | class | title | url |
|---|---|---|---|---|---|
| chroma-core | 7375 | BUG_OPEN | X | [Bug]:   Concurrent `create_collection` + `delete_collection` on the same collection name causes lost update (both return success) | https://github.com/chroma-core/chroma/issues/7375 |
| meilisearch | 6479 | OPEN_NO_LABEL | V | Typo tolerance `minWordSizeForTypos` settings have no effect on search results | https://github.com/meilisearch/meilisearch/issues/6479 |
| meilisearch | 6480 | CLOSED_NO_LABEL | V | Vector search returns 400 `missing_search_hybrid` despite `hybrid` documented as optional | https://github.com/meilisearch/meilisearch/issues/6480 |
| meilisearch | 6481 | CLOSED_NO_LABEL | V | Embedder `dimensions=4097` accepted by settings API, exceeding documented max of 4096 | https://github.com/meilisearch/meilisearch/issues/6481 |
| milvus-io | 47635 | FIXED | V | [Bug]: Search fails with Code 0 immediately after Collection.load() returns success | https://github.com/milvus-io/milvus/issues/47635 |
| milvus-io | 47636 | FIXED | V | [Bug]: Expr parser returns code=0 (Success) and leaks internal lexer errors | https://github.com/milvus-io/milvus/issues/47636 |
| milvus-io | 47729 | FIXED | V | [Bug]: Index parameter nprobe validation missing - accepts nprobe=0 | https://github.com/milvus-io/milvus/issues/47729 |
| milvus-io | 47752 | FIXED | V | [Bug]: Index parameter ef validation missing - accepts ef=0 | https://github.com/milvus-io/milvus/issues/47752 |
| milvus-io | 47755 | FIXED | V | [Bug]: Filter expression validation too lenient | https://github.com/milvus-io/milvus/issues/47755 |
| milvus-io | 47763 | FIXED | V | [Bug]:  Field name validation missing - accepts invalid field names causing data inaccessibility | https://github.com/milvus-io/milvus/issues/47763 |
| milvus-io | 47766 | FIXED | V | [Bug]: Data type validation missing - accepts integer into string field | https://github.com/milvus-io/milvus/issues/47766 |
| milvus-io | 47767 | BY_DESIGN | V | [Bug]: Empty query vector accepted in search - no validation error | https://github.com/milvus-io/milvus/issues/47767 |
| milvus-io | 49059 | FIXED | M | [Bug]: COSINE Metric Returns Distance > 1.0 for Identical Vectors (Precision Overflow) | https://github.com/milvus-io/milvus/issues/49059 |
| milvus-io | 49823 | ACCEPTED_OPEN | V | [Bug]: REST API v2 accepts nprobe=0 in search requests without validation | https://github.com/milvus-io/milvus/issues/49823 |
| milvus-io | 49824 | CLOSED_NO_LABEL | V | [Bug]: REST API v2 returns success when creating a collection with a duplicate name | https://github.com/milvus-io/milvus/issues/49824 |
| milvus-io | 49843 | FIXED | V | [Bug]: REST API v2 silently drops negative collection.ttl.seconds on collection create | https://github.com/milvus-io/milvus/issues/49843 |
| milvus-io | 49844 | ACCEPTED_OPEN | V | [Bug]: REST API v2 query accepts null/missing filter and silently returns all entities | https://github.com/milvus-io/milvus/issues/49844 |
| milvus-io | 49849 | CLOSED_NO_LABEL | V | [Bug]: REST API v2 insert returns insertCount=1 for duplicate primary key (upsert semantics) | https://github.com/milvus-io/milvus/issues/49849 |
| milvus-io | 49850 | CLOSED_NO_LABEL | V | [Bug]: REST API v2 describe indexes requires indexName, cannot list all indexes | https://github.com/milvus-io/milvus/issues/49850 |
| milvus-io | 49889 | ACCEPTED_OPEN | V | [Bug]: REST API v2 accepts empty string for `dbName` parameter | https://github.com/milvus-io/milvus/issues/49889 |
| milvus-io | 49890 | FIXED | V | [Bug]: REST API v2 accepts non-integer `Request-Timeout` header values | https://github.com/milvus-io/milvus/issues/49890 |
| milvus-io | 49928 | BY_DESIGN | V | [Bug]: Default proxy.maxDimension=32768 is too permissive, potential DoS risk via high-dimensional collection creation | https://github.com/milvus-io/milvus/issues/49928 |
| milvus-io | 49929 | BY_DESIGN | V | [Bug]: REST API and PyMilvus SDK have inconsistent default index creation behavior | https://github.com/milvus-io/milvus/issues/49929 |
| milvus-io | 49930 | ACCEPTED_OPEN | V | [Bug]: REST API v2 accepts invalid searchParams (ef=0/-1 for HNSW, nprobe=0/-1 for IVF_FLAT) without validation | https://github.com/milvus-io/milvus/issues/49930 |
| milvus-io | 50018 | FIXED | V | [Bug]: REST API v2 aliases/list accepts empty collectionName while other endpoints properly reject it | https://github.com/milvus-io/milvus/issues/50018 |
| milvus-io | 50192 | BY_DESIGN | X | [Bug] Concurrent rename and create with same target name both succeed, causing state violation | https://github.com/milvus-io/milvus/issues/50192 |
| milvus-io | 50193 | BY_DESIGN | M | [Bug] get_stats returns rowCount=0 after successful insert and load (v2.6.16, regression from #30663) | https://github.com/milvus-io/milvus/issues/50193 |
| milvus-io | 50194 | BY_DESIGN | X | [Bug] Concurrent delete and search returns stale/deleted data | https://github.com/milvus-io/milvus/issues/50194 |
| milvus-io | 50305 | CLOSED_NO_LABEL | V | [Bug] Search on unloaded collection returns valid results (code=0) | https://github.com/milvus-io/milvus/issues/50305 |
| milvus-io | 50306 | CLOSED_NO_LABEL | V | [Bug] Duplicate collection creation returns code=0 instead of error | https://github.com/milvus-io/milvus/issues/50306 |
| milvus-io | 50307 | CLOSED_NO_LABEL | V | [Bug] Drop non-existent collection returns code=0 instead of code=4 | https://github.com/milvus-io/milvus/issues/50307 |
| milvus-io | 50308 | CLOSED_NO_LABEL | V | [Bug] Delete accepts both filter and ids (mutually exclusive) silently | https://github.com/milvus-io/milvus/issues/50308 |
| milvus-io | 50309 | CLOSED_NO_LABEL | V | [Bug] Consistency level silently accepts invalid values and defaults to Bounded | https://github.com/milvus-io/milvus/issues/50309 |
| milvus-io | 50310 | CLOSED_NO_LABEL | V | [Bug] REST API: Insert accepts 101 entities (exceeding documented 100 limit) | https://github.com/milvus-io/milvus/issues/50310 |
| milvus-io | 50311 | CLOSED_NO_LABEL | V | [Bug] REST API: Unicode-only collection names silently accepted | https://github.com/milvus-io/milvus/issues/50311 |
| milvus-io | 50312 | CLOSED_NO_LABEL | V | [Bug] Rename collection to its own name returns code=0 | https://github.com/milvus-io/milvus/issues/50312 |
| milvus-io | 50313 | CLOSED_NO_LABEL | V | [Bug] Search on unloaded collection returns valid results (code=0) | https://github.com/milvus-io/milvus/issues/50313 |
| milvus-io | 50314 | CLOSED_NO_LABEL | V | [Bug] Duplicate collection creation returns code=0 instead of error | https://github.com/milvus-io/milvus/issues/50314 |
| milvus-io | 50315 | CLOSED_NO_LABEL | V | [Bug] Drop non-existent collection returns code=0 instead of code=4 | https://github.com/milvus-io/milvus/issues/50315 |
| milvus-io | 50316 | CLOSED_NO_LABEL | V | [Bug] Delete endpoint accepts both filter and ids (mutually exclusive) silently | https://github.com/milvus-io/milvus/issues/50316 |
| milvus-io | 50317 | CLOSED_NO_LABEL | V | [Bug] REST API: Insert accepts 101 entities (exceeding documented 100 limit) | https://github.com/milvus-io/milvus/issues/50317 |
| milvus-io | 50318 | CLOSED_NO_LABEL | V | [Bug] Collection names with leading underscore accepted despite naming rules | https://github.com/milvus-io/milvus/issues/50318 |
| milvus-io | 50319 | BY_DESIGN | V | [Bug]: Search on unloaded collection returns valid results (code=0) | https://github.com/milvus-io/milvus/issues/50319 |
| milvus-io | 50321 | BY_DESIGN | V | [Bug]: Duplicate collection creation returns code=0 instead of error | https://github.com/milvus-io/milvus/issues/50321 |
| milvus-io | 50322 | BY_DESIGN | V | [Bug]: Drop non-existent collection returns code=0 instead of code=4 | https://github.com/milvus-io/milvus/issues/50322 |
| milvus-io | 50323 | ACCEPTED_OPEN | V | [Bug]: Delete endpoint accepts both filter and ids (mutually exclusive) silently | https://github.com/milvus-io/milvus/issues/50323 |
| milvus-io | 50324 | FIXED | V | [Bug]: REST API: Insert accepts 101 entities (exceeding documented 100 limit) | https://github.com/milvus-io/milvus/issues/50324 |
| milvus-io | 50325 | BY_DESIGN | V | [Bug]: Collection names with leading underscore accepted despite naming rules | https://github.com/milvus-io/milvus/issues/50325 |
| milvus-io | 50351 | BY_DESIGN | V | [Bug]: REST API v2: shardsNum=0/-1/65535 accepted with HTTP 200 + code=200 | https://github.com/milvus-io/milvus/issues/50351 |
| milvus-io | 50352 | BY_DESIGN | V | [Bug]: REST API v2: metricType="" and consistencyLevel="None" silently accepted on collections/create | https://github.com/milvus-io/milvus/issues/50352 |
| milvus-io | 50353 | ACCEPTED_OPEN | V | [Bug]: REST API v2: search returns HTTP 200 for limit=0/-1 and dimension mismatch | https://github.com/milvus-io/milvus/issues/50353 |
| milvus-io | 50354 | ACCEPTED_OPEN | V | [Bug]: REST API v2: password complexity not enforced — "abcdefgh" accepted on users/create | https://github.com/milvus-io/milvus/issues/50354 |
| milvus-io | 50355 | FIXED | V | [Bug]: Upsert fails on autoID=true collections despite documentation claiming support | https://github.com/milvus-io/milvus/issues/50355 |
| milvus-io | 51084 | FIXED | V | [Bug]: REST API silently substitutes invalid `consistencyLevel` enum value with default instead of rejecting | https://github.com/milvus-io/milvus/issues/51084 |
| milvus-io | 51085 | FIXED | V | [Bug]: REST API silently substitutes invalid `vectorFieldType` enum value with default instead of rejecting | https://github.com/milvus-io/milvus/issues/51085 |
| qdrant | 8688 | BUG_OPEN | M | [Bug]: Cosine similarity score strictly exceeds upper bound of 1.0 for identical vectors | https://github.com/qdrant/qdrant/issues/8688 |
| qdrant | 9017 | FIXED | V | hnsw_ef accepts 0 | https://github.com/qdrant/qdrant/issues/9017 |
| qdrant | 9027 | REJECTED | V | score_threshold_range_issue | https://github.com/qdrant/qdrant/issues/9027 |
| qdrant | 9039 | FIXED | V | Bug: Async upsert silently discards dimension-mismatched vectors (Poor Diagnostics) | https://github.com/qdrant/qdrant/issues/9039 |
| qdrant | 9044 | BUG_OPEN | V | Collection creation accepts `size=65536` despite FAQ stating maximum is 65,535 (off-by-one) | https://github.com/qdrant/qdrant/issues/9044 |
| qdrant | 9045 | FIXED | C | Bug: Empty vector `[]` upsert with `wait=false` can trigger server panic (zero-length assertion failure) | https://github.com/qdrant/qdrant/issues/9045 |
| qdrant | 9149 | FIXED | V | shard_number=0 and negative values accepted during collection creation | https://github.com/qdrant/qdrant/issues/9149 |
| qdrant | 9255 | FIXED | M | Payload filter returns points with missing payload field (payload=None) | https://github.com/qdrant/qdrant/issues/9255 |
| qdrant | 9364 | CLOSED_NO_LABEL | X | Bug: Batch operations partially apply despite returning HTTP 400 error (atomicity violation) | https://github.com/qdrant/qdrant/issues/9364 |
| qdrant | 9365 | CLOSED_NO_LABEL | M | Bug: Payload index returns incorrect filtered results — index corruption after creation | https://github.com/qdrant/qdrant/issues/9365 |
| qdrant | 9366 | CLOSED_NO_LABEL | X | Bug: Named vector lifecycle operations (update+delete) corrupt search — returns 400 | https://github.com/qdrant/qdrant/issues/9366 |
| qdrant | 9371 | REJECTED | X | Bug: Batch operations not atomic — valid points persisted despite HTTP 400 error | https://github.com/qdrant/qdrant/issues/9371 |
| qdrant | 9372 | BUG_OPEN | V | Strict mode inconsistently validates zero values — allows creation of unusable collections | https://github.com/qdrant/qdrant/issues/9372 |
| qdrant | 9373 | FIXED | M | Bug: Payload index silently returns severely incomplete results — 2/25 matching points after wait:true | https://github.com/qdrant/qdrant/issues/9373 |
| qdrant | 9416 | FIXED | V | `vectors={}` silently accepted during collection creation — produces unusable collection | https://github.com/qdrant/qdrant/issues/9416 |
| qdrant | 9417 | FIXED | V | Missing `vectors` field silently accepted during collection creation — produces unusable collection | https://github.com/qdrant/qdrant/issues/9417 |
| qdrant | 9418 | FIXED | V | `filter.should=null` silently accepted in query/search — null filter condition ignored | https://github.com/qdrant/qdrant/issues/9418 |
| qdrant | 9419 | FIXED | V | `filter.must_not` accepts object instead of array — type mismatch silently ignored | https://github.com/qdrant/qdrant/issues/9419 |
| qdrant | 9420 | FIXED | V | `query=null` silently accepted — returns all points instead of being rejected | https://github.com/qdrant/qdrant/issues/9420 |
| qdrant | 9421 | FIXED | V | `POST /cluster/recover` returns HTTP 500 in standalone mode — should return 4xx | https://github.com/qdrant/qdrant/issues/9421 |
| qdrant | 9520 | BUG_OPEN | C | Server crash on collection creation with shard_number=INT_MAX — missing upper-bound validation unlike replication_factor | https://github.com/qdrant/qdrant/issues/9520 |
| qdrant | 9521 | BUG_OPEN | M | Silent data loss: named vector upsert in single-vector collection returns 200 OK but point is discarded | https://github.com/qdrant/qdrant/issues/9521 |
| qdrant | 9522 | BUG_OPEN | V | Query API silently returns 200 OK when lookup_from references a non-existent collection | https://github.com/qdrant/qdrant/issues/9522 |
| qdrant | 9523 | REJECTED | M | Search offset pagination returns duplicate point IDs across pages (HNSW approximation) | https://github.com/qdrant/qdrant/issues/9523 |
| qdrant | 9524 | FIXED | V | Invalid filter conditions silently accepted (200 OK) with poor error diagnostics across search/query/scroll endpoints | https://github.com/qdrant/qdrant/issues/9524 |
| qdrant | 9525 | BUG_OPEN | V | Systemic: serde deserialization errors across 7 endpoints expose Rust internal types (usize/u32/f32) and lack parameter names | https://github.com/qdrant/qdrant/issues/9525 |
| weaviate | 11395 | CLOSED_NO_LABEL | V | [Bug]: dynamicEfMin > dynamicEfMax accepted during collection creation (no validation) | https://github.com/weaviate/weaviate/issues/11395 |
| weaviate | 11396 | CLOSED_NO_LABEL | V | [Bug]: flatSearchCutoff accepts negative values (no validation) | https://github.com/weaviate/weaviate/issues/11396 |
| weaviate | 11397 | CLOSED_NO_LABEL | V | [Bug]: replicationFactor=-1 accepted and silently normalized to 1 (no validation) | https://github.com/weaviate/weaviate/issues/11397 |
| weaviate | 11398 | CLOSED_NO_LABEL | V | [Bug]: bq.rescoreLimit=-1 accepted and silently discarded (no validation) | https://github.com/weaviate/weaviate/issues/11398 |
| weaviate | 11399 | BUG_OPEN | V | dynamicEfMin > dynamicEfMax accepted during collection creation (no validation) | https://github.com/weaviate/weaviate/issues/11399 |
| weaviate | 11400 | BUG_OPEN | V | flatSearchCutoff accepts negative values (no validation) | https://github.com/weaviate/weaviate/issues/11400 |
| weaviate | 11401 | BUG_OPEN | V | replicationFactor=-1 accepted and silently normalized to 1 (no validation) | https://github.com/weaviate/weaviate/issues/11401 |
| weaviate | 11402 | BUG_OPEN | V | bq.rescoreLimit=-1 accepted and silently discarded (no validation) | https://github.com/weaviate/weaviate/issues/11402 |
| weaviate | 11433 | CLOSED_NO_LABEL | V | [Schema Validation] Negative `ef` value (-1) accepted in vectorIndexConfig without validation error | https://github.com/weaviate/weaviate/issues/11433 |
| weaviate | 11436 | REJECTED | V | Negative `ef` value (-1) accepted in vectorIndexConfig without validation error | https://github.com/weaviate/weaviate/issues/11436 |
| weaviate | 11660 | BUG_OPEN | V | REST API GET /v1/objects silently accepts negative limit parameter | https://github.com/weaviate/weaviate/issues/11660 |
| weaviate | 11661 | BUG_OPEN | V | REST API GET /v1/objects returns HTTP 500 instead of 4xx when limit exceeds QUERY_MAXIMUM_RESULTS | https://github.com/weaviate/weaviate/issues/11661 |
| weaviate | 11729 | FIXED | V | shardingConfig.desiredCount accepts negative values but rejects zero | https://github.com/weaviate/weaviate/issues/11729 |
| weaviate | 11730 | BUG_OPEN | Vs | tokenization accepts empty string despite explicit OpenAPI enum constraint | https://github.com/weaviate/weaviate/issues/11730 |
| weaviate | 11731 | BUG_OPEN | Vs | replicationConfig.deletionStrategy accepts empty string outside explicit OpenAPI enum | https://github.com/weaviate/weaviate/issues/11731 |
| weaviate | 11732 | BUG_OPEN | V | vectorIndexConfig.distance silently accepts null and defaults to cosine | https://github.com/weaviate/weaviate/issues/11732 |
| weaviate | 11734 | BUG_OPEN | V | multiTenancyConfig accepts null for boolean fields autoTenantCreation and autoTenantActivation | https://github.com/weaviate/weaviate/issues/11734 |
| weaviate | 11735 | BUG_OPEN | M | int64 boundary value 9223372036854775807 silently truncated to 9223372036854776000 | https://github.com/weaviate/weaviate/issues/11735 |
| weaviate | 11736 | BUG_OPEN | V | blob accepts long non-base64 garbage string without validation | https://github.com/weaviate/weaviate/issues/11736 |
| weaviate | 11737 | BUG_OPEN | Vs | date accepts year 0000 and pre-1970 values without proper RFC3339 validation | https://github.com/weaviate/weaviate/issues/11737 |
| weaviate | 11738 | BUG_OPEN | Vs | phoneNumber.defaultCountry accepts invalid ISO 3166-1 alpha-2 code "ZZ" | https://github.com/weaviate/weaviate/issues/11738 |
| weaviate | 11739 | BUG_OPEN | V | phoneNumber.input accepts alphabetic characters like "CALL-NOW" without validation | https://github.com/weaviate/weaviate/issues/11739 |
| weaviate | 11740 | BUG_OPEN | V | GraphQL queries accept negative limit values | https://github.com/weaviate/weaviate/issues/11740 |
| weaviate | 11741 | BUG_OPEN | V | Tenant creation accepts empty string for activityStatus | https://github.com/weaviate/weaviate/issues/11741 |
| weaviate | 11742 | BUG_OPEN | V | PQ bitCompression accepts string "true" instead of requiring boolean true | https://github.com/weaviate/weaviate/issues/11742 |
| weaviate | 11743 | BUG_OPEN | V | text property accepts strings containing NUL bytes (\x00) without validation | https://github.com/weaviate/weaviate/issues/11743 |
| weaviate | 11744 | BUG_OPEN | V | Text property accepts strings containing lone UTF-16 surrogates | https://github.com/weaviate/weaviate/issues/11744 |
| weaviate | 11745 | BUG_OPEN | V | Text property accepts strings containing ASCII control characters (SOH, STX, ETX) | https://github.com/weaviate/weaviate/issues/11745 |
| weaviate | 11981 | FIXED | V | POST /v1/batch/objects accepts empty vector `[]` and reports per-item SUCCESS (singular POST /v1/objects rejects with 422) | https://github.com/weaviate/weaviate/issues/11981 |
| weaviate | 12041 | FIXED | V | Batch delete returns HTTP 500 instead of 422 when match.where or match.class is missing | https://github.com/weaviate/weaviate/issues/12041 |

**Tally (111):** classical-findable(M+C)=11 (10%); residual(V+Vs+X)=100 (90%); ambiguous=0
**Acknowledged 38:** classical-findable=4 (11%); residual=34 (89%)
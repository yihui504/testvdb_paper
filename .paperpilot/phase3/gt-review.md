# Phase 3 GT 材料复核表（45 bugs → 15 存在版本）

定位规则: A组=fix-PR merged_at 前最近 server release(并行线取与报告版本较大者); 无 merged fix-PR → 保守取报告版本; B组=报告版本。milvus "2.3"→v2.3.22 (phase2 约定)。

## milvus v2.3.22 (1 bugs)

| did | group | rep.ver | fix-PR (merged_at) | endpoint | param | 弱对齐 |
|---|---|---|---|---|---|---|
| milvus_47635 | B | 2.3.22 | — | entities+search | `load` | race bug, 无固定参数名 |

## milvus v2.6.10 (5 bugs)

| did | group | rep.ver | fix-PR (merged_at) | endpoint | param | 弱对齐 |
|---|---|---|---|---|---|---|
| milvus_47729 | B | 2.6.10 | — | entities+search | `nprobe` |  |
| milvus_47752 | B | 2.6.10 | — | entities+search | `ef` |  |
| milvus_47755 | B | 2.6.10 | — | entities+delete | `filter` | 校验宽松, 命名或偏 |
| milvus_47763 | A | 2.6.10 | — | entities+insert | `fieldName` |  |
| milvus_47766 | B | 2.6.10 | — | entities+insert | `dataType` | 类型混淆 bug, 命名或偏 |

## milvus v2.6.12 (1 bugs)

| did | group | rep.ver | fix-PR (merged_at) | endpoint | param | 弱对齐 |
|---|---|---|---|---|---|---|
| milvus_49059 | B | 2.6.12 | — | entities+search | `metric_type` |  |

## milvus v2.6.16 (4 bugs)

| did | group | rep.ver | fix-PR (merged_at) | endpoint | param | 弱对齐 |
|---|---|---|---|---|---|---|
| milvus_49823 | B | 2.6.16 | — | entities+insert | `nprobe` |  |
| milvus_49889 | B | 2.6.16 | — | collections+create | `dbName` |  |
| milvus_49930 | B | 2.6.16 | — | collections+create | `searchParams` |  |
| milvus_50018 | B | 2.6.16 | — | aliases+list | `collectionName` |  |

## milvus v2.6.17 (4 bugs)

| did | group | rep.ver | fix-PR (merged_at) | endpoint | param | 弱对齐 |
|---|---|---|---|---|---|---|
| milvus_49890 | A | 2.6.16 | milvus#50195 (2026-06-01) | entities+insert | `Request-Timeout` |  |
| milvus_50323 | B | 2.6.17 | — | entities+insert | `filter` | filter+ids 互斥 |
| milvus_50353 | B | 2.6.17 | — | entities+search | `limit` |  |
| milvus_50354 | B | 2.6.17 | — | users+create | `password` |  |

## milvus v2.6.18 (2 bugs)

| did | group | rep.ver | fix-PR (merged_at) | endpoint | param | 弱对齐 |
|---|---|---|---|---|---|---|
| milvus_49843 | A | 2.6.16 | milvus#50731 (2026-06-26) | collections+alter | `collection.ttl.seconds` |  |
| milvus_50355 | A | 2.6.17 | milvus-docs#3513 (2026-06-08) | entities+upsert | `autoID` |  |

## milvus v2.6.19 (2 bugs)

| did | group | rep.ver | fix-PR (merged_at) | endpoint | param | 弱对齐 |
|---|---|---|---|---|---|---|
| milvus_51084 | A | 2.6.19 | milvus#51088 (2026-07-08) | collections+create | `consistencyLevel` |  |
| milvus_51085 | A | 2.6.19 | milvus#51088 (2026-07-08) | entities+insert | `vectorFieldType` |  |

## milvus v3.0.0 (10 bugs)

| did | group | rep.ver | fix-PR (merged_at) | endpoint | param | 弱对齐 |
|---|---|---|---|---|---|---|
| milvus_52307 | A | 3.0.0 | milvus#52261 (2026-08-11) | entities+upsert | `json_field` | JSON 字段 bug, 命名或偏 |
| milvus_52308 | B | 3.0.0 | — | entities+insert | `id` | 主键类型强转, 命名或偏 |
| milvus_52309 | A | 3.0.0 | milvus#52346 (2026-08-11) | entities+insert | `group_size` |  |
| milvus_52310 | B | 3.0.0 | — | entities+insert | `data` | 标量强转, 命名或偏 |
| milvus_52311 | A | 3.0.0 | milvus#52346 (2026-08-11) | entities+search | `group_by_field` |  |
| milvus_52312 | B | 3.0.0 | — | entities+insert | `id` | 同 52308 (upsert) |
| milvus_52313 | A | 3.0.0 | milvus#52261 (2026-08-11) | entities+insert | `json_field` | 同 52307 (dup 对) |
| milvus_52314 | B | 3.0.0 | — | entities+upsert | `data` | 同 52310 (upsert) |
| milvus_52315 | A | 3.0.0 | milvus#52261 (2026-08-11) | entities+insert | `vector` |  |
| milvus_52325 | A | 3.0.0 | milvus#52346 (2026-08-11) | entities+search | `strictGroupSize` |  |

## qdrant v1.18.0 (2 bugs)

| did | group | rep.ver | fix-PR (merged_at) | endpoint | param | 弱对齐 |
|---|---|---|---|---|---|---|
| qdrant_9039 | A | 1.18.0 | qdrant#9058 (2026-05-16) | points | `vector` | 诊断缺陷, 命名或偏 |
| qdrant_9045 | A | 1.12.1 | qdrant#9070 (2026-05-19) | points | `wait` |  |

## qdrant v1.18.2 (5 bugs)

| did | group | rep.ver | fix-PR (merged_at) | endpoint | param | 弱对齐 |
|---|---|---|---|---|---|---|
| qdrant_9017 | A | 1.18.0 | qdrant#9320 (2026-06-08) | points | `hnsw_ef` |  |
| qdrant_9149 | A | 1.18.1 | qdrant#9178 (2026-06-05) | collections+{collection_name} | `shard_number` |  |
| qdrant_9421 | A | 1.18.2 | qdrant#9431 (2026-06-25) | cluster+recover | `recover` | 模式不匹配 bug, 命名或偏 |
| qdrant_9520 | A | 1.18.2 | qdrant#9594 (2026-06-29) | collections+{collection_name} | `shard_number` |  |
| qdrant_9522 | A | 1.18.2 | qdrant#9531 (2026-07-15) | collections+{collection_name}+points+query | `lookup_from` |  |

## qdrant v1.19.0 (1 bugs)

| did | group | rep.ver | fix-PR (merged_at) | endpoint | param | 弱对齐 |
|---|---|---|---|---|---|---|
| qdrant_10120 | A | 1.18.3 | qdrant#10128 (2026-08-08) | points+count | `exact` |  |

## weaviate v1.37.4 (3 bugs)

| did | group | rep.ver | fix-PR (merged_at) | endpoint | param | 弱对齐 |
|---|---|---|---|---|---|---|
| weaviate_11399 | A | 1.37.4 | — | GET /schema | `dynamicEfMin` |  |
| weaviate_11400 | A | 1.37.4 | — | GET /schema | `flatSearchCutoff` |  |
| weaviate_11401 | A | 1.37.4 | — | /schema | `replicationFactor` |  |

## weaviate v1.38.0 (3 bugs)

| did | group | rep.ver | fix-PR (merged_at) | endpoint | param | 弱对齐 |
|---|---|---|---|---|---|---|
| weaviate_11730 | A | 1.38.0 | — | POST /schema | `tokenization` |  |
| weaviate_11732 | A | 1.38.0 | — | /schema | `distance` |  |
| weaviate_11741 | A | 1.38.0 | — | /schema/{className}/tenants | `activityStatus` |  |

## weaviate v1.38.1 (1 bugs)

| did | group | rep.ver | fix-PR (merged_at) | endpoint | param | 弱对齐 |
|---|---|---|---|---|---|---|
| weaviate_11729 | A | 1.38.0 | weaviate#11824 (2026-06-24) | POST /schema | `desiredCount` |  |

## weaviate v1.38.2 (1 bugs)

| did | group | rep.ver | fix-PR (merged_at) | endpoint | param | 弱对齐 |
|---|---|---|---|---|---|---|
| weaviate_12041 | A | 1.38.2 | weaviate#12049 (2026-07-08) | DELETE /batch/objects | `match` | match.where 缺失, 命名或偏 |

## 需重点 probe 验证的条目

- **跨版本跳跃**: qdrant_9045 报告于 v1.12.1, 存在版本定位 v1.18.0 (fix #9070 merged 2026-05-19 前最后 release) — 跳过 6 个 minor, 中途可能已被其他改动修复, probe 必验。
- **doc-fix 型**: milvus_50355 (milvus-docs#3513/3514) — bug=文档与实现不一致, 修复=改文档; probe 验证 v2.6.18 文档/行为仍不一致。
- **race bug**: milvus_47635 — 低概率触发, probe 用多 collection 重试; gt.json param=load 为弱对齐占位。

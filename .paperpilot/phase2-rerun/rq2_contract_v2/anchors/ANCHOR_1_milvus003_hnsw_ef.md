# 锚 1｜milvus_003 (issue #47752) — HNSW `ef` 取值域明文

- **来源**: milvus-io/milvus-docs, branch `v2.6.x`, `site/en/userGuide/indexes/floating-vector/hnsw.md`
- **URL**: https://milvus.io/docs/hnsw.md （Index-specific search params 节）
- **验证日期**: 2026-08-30（GitHub 源文件逐字提取）
- **对应缺陷**: milvus_003 / issue #47752 "Index parameter ef validation missing - accepts ef=0"（TP，维护者 assigned liliu-z，milestone 2.6.14 已修复）

## 原文（逐字）

> ### Index-specific search params
>
> The following table lists the parameters that can be configured in `search_params.params` when searching on the index.
>
> | Parameter | Description | Value Range | Tuning Suggestion |
> |---|---|---|---|
> | `ef` | Controls the breadth of search during nearest neighbor retrieval. ... | **Type: Integer Range: [1, *int_max*]** **Default value**: *limit* (TopK nearest neighbors to return) | ... In most cases, we recommend you set a value within this range: [K, 10K]. |

## 断言映射

- 约束: `ef ∈ [1, 2147483647]`（integer），施加于 entities+search 的 `searchParams.params.ef`（HNSW 系索引）
- 违反形态: `ef=0` —— 明文域外值被 silent accept
- evidence_tier: **explicit**（Value Range 表逐字）
- 我方契约现状: 知识采集未覆盖 `hnsw.md`（searchParams 描述仅 "Search parameters including metricType, radius, range_filter"）→ **采集覆盖缺口**

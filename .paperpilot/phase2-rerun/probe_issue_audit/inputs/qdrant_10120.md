# qdrant_10120 (group=A, version=1.18.3)

## issue 标题
`count` `exact=false` on `is_empty` under-counts ~35% consistently; `is_null` on the same field is correct

## issue body（截断 1500 字符）
## Current Behavior

`POST /collections/{c}/points/count` with `exact=false` on an `is_empty` condition over a keyword-indexed field returns a **consistent ~-35% under-count** across collection sizes. `exact=true` returns the correct count. This occurs at **steady state** (after indexing completes), outside the documented "unreliable during indexing" window.

On the **same collection**, the analogous `is_null` condition returns identical (correct) counts on both `exact=true` and `exact=false` paths. This isolates the bug to the `is_empty` condition's cardinality estimation path, not the field, the index, or the general count estimator.

The error is a **stable percentage** (~-35%), not the `total/2` fallback — verified across collection sizes 200, 500, and 1000.

The Qdrant OpenAPI specification (v1.18.3, [`openapi.json`](https://github.com/qdrant/qdrant/blob/v1.18.3/docs/redoc/v1.8.x/openapi.json)) defines `exact` as:

> "If `true`, count exact number of points. If `false`, count approximate number of points faster. **Approximate count might be unreliable during the indexing process.** Default: `true`"

And `IsEmptyCondition` as:

> "Select points with **empty payload** for a specified field"

The ~-35% under-count occurs at steady state (after indexing completes), which is outside the documented unreliability window. The documentation does not state that `is_empty` approximate counts would be systematically biased where `is_null` on the same field is exact.

## Steps to Rep

## stage2_aggregation.confirmed
endpoint=points+count
defect_type=semantics
related_issue_numbers=[10120]

## 探针脚本
.paperpilot/phase2/probes/qdrant/probe_qdrant_10120.py
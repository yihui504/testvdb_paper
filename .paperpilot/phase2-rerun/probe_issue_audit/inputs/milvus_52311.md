# milvus_52311 (group=A, version=3.0.0)

## issue 标题
[Bug]: REST API v2 silently accepts `group_by_field` on vector fields (gRPC rejects "unsupported data type")

## issue body（截断 1500 字符）
### Is there an existing issue for this?

- [x] I have searched the existing issues

### Environment

```markdown
- Milvus version: v3.0.0 (release 2026-07-29, commit f46a0328558be155d11266a1a2b90602ccc9b366)
- Deployment mode: standalone (Docker, `milvusdb/milvus:v3.0.0`)
- MQ type: N/A
- SDK version: REST API v2 only (curl). pymilvus used for gRPC comparison.
- OS: Windows 11 (Docker Desktop)
- CPU/Memory: N/A
- GPU: None
```

### Current Behavior


The REST API v2 `POST /v2/vectordb/entities/search` endpoint silently accepts `groupByField` set to a **vector field** (e.g., `"vector"`). The request returns `code: 0` with normal search results — **grouping is silently ignored**, producing identical results to a search without `group_by`.

The gRPC path correctly rejects this:

```
code=2001, message="unsupported data type VECTOR_FLOAT for group by operator
at ../internal/core/src/exec/operator/search-groupby/SearchGroupByOperator.cpp:169"
```

The [Grouping Search documentation](https://milvus.io/docs/grouping-search.md) describes grouping by scalar fields (e.g., `docId`, `color`). Grouping by a vector field is semantically invalid — vectors cannot be compared for equality-based grouping.

### Expected Behavior


The REST API should reject `groupByField` set to a vector field with an explicit error (`code != 0`), consistent with gRPC behavior. At minimum, it should not silently ignore the parameter (users may believe grouping is working when it isn't).


### Steps To Reproduc

## stage2_aggregation.confirmed
endpoint=entities+search
defect_type=semantics
related_issue_numbers=[52311]

## 探针脚本
.paperpilot/phase2/probes/milvus/probe_milvus_52311.py
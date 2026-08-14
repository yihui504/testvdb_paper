# milvus_52309 (group=A, version=3.0.0)

## issue 标题
[Bug]: REST API v2 `entities/search` accepts `group_size=0` and `-1` (gRPC rejects as "negative")

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


The REST API v2 `POST /v2/vectordb/entities/search` endpoint accepts `groupSize=0` and `groupSize=-1` in `groupParams` without validation (`code: 0`). The gRPC path correctly rejects both:

```
gRPC: code=1100, message="input group size:0 is negative, failed to do search_groupby"
gRPC: code=1100, message="input group size:-1 is negative, failed to do search_groupby"
```

The [Grouping Search documentation](https://milvus.io/docs/grouping-search.md) states:

> "By default, Grouping Search returns only one entity per group. If you want to increase the number of results to return per group, you can control this with the `group_size` and `strict_group_size` parameters."

This implies `group_size` is a positive integer that "increases" results per group — `0` and `-1` are semantically meaningless.

### Expected Behavior


`groupSize` should be validated as ≥ 1. REST should reject `0` and negative values with an explicit error, consistent with gRPC.


### Steps To Reproduce

```markdown
# 1. Create + load collection
curl -X POST http:

## stage2_aggregation.confirmed
endpoint=entities+insert
defect_type=param_validation
related_issue_numbers=[52309]

## 探针脚本
.paperpilot/phase2/probes/milvus/probe_milvus_52309.py
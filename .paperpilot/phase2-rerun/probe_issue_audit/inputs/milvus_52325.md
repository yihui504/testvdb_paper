# milvus_52325 (group=A, version=3.0.0)

## issue 标题
[Bug]: REST v2 entities/search silently ignores strictGroupSize

## issue body（截断 1500 字符）
### Is there an existing issue for this?

- [x] I have searched the existing issues

### Environment

```markdown
- Milvus version: v3.0.0 (release 2026-07-29, commit f46a0328558be155d11266a1a2b90602ccc9b366)
- Deployment mode: standalone (Docker, `milvusdb/milvus:v3.0.0`)
- SDK version: REST API v2 (curl) + pymilvus 2.5.5 (gRPC comparison)
- OS: Windows 11 (Docker Desktop)
```

### Current Behavior


On v3.0.0, `POST /v2/vectordb/entities/search` silently ignores `groupParams.strictGroupSize`. The parameter is accepted (`code: 0`) but has no effect — results are identical whether `strictGroupSize` is `true` or `false`. The gRPC path honors the same parameter.

With 5 groups (`cat` 0–4) × 3 points each = 15 points:

| group_size | strictGroupSize | limit | REST returns | gRPC returns |
|---|---|---|---|---|
| 1 | true | 15 | 15 (should be 5) | 5 |
| 2 | true | 15 | 15 (should be 10) | 10 |
| 1 | true | 10 | 10 (should be 5) | 5 |
| 1 | false | 15 | 15 | 5 |

REST behaves as if `strictGroupSize` is always `false`, regardless of the value sent.

### Expected Behavior


Per the [REST v2 Search documentation](https://milvus.io/api-reference/restful/v3.0.x/v2/Vector%20(v2)/Search.md):

> **strictGroupSize** *(boolean)*: Whether to return only the top k entities for each group. This parameter is only valid when groupingField is specified.

REST should honor `strictGroupSize=true` and cap each group at `groupSize` entities, consistent with the gRPC path.


### Steps To Reproduce

``

## stage2_aggregation.confirmed
endpoint=entities+search
defect_type=semantics
related_issue_numbers=[52325]

## 探针脚本
.paperpilot/phase2/probes/milvus/probe_milvus_52325.py
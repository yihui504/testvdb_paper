# milvus_49823 (group=B, version=2.6.16)

## issue 标题
[Bug]: REST API v2 accepts nprobe=0 in search requests without validation

## issue body（截断 1500 字符）
### Is there an existing issue for this?

- [x] I have searched the existing issues

### Environment

```markdown
- Milvus version: v2.6.16
- Deployment mode(standalone or cluster): standalone
- MQ type(rocksmq, pulsar or kafka): rocksmq
- SDK version(e.g. pymilvus v2.0.0rc2): REST API v2 (via curl)
- OS(Ubuntu or CentOS): Docker on Windows
- CPU/Memory: N/A
- GPU: N/A
- Others: Reproduced via Milvus REST API v2 (`/v2/vectordb/entities/search`)
```

### Current Behavior

When performing a vector search with `nprobe=0` via the REST API v2, Milvus accepts the request and returns results with `code=0` (success). The `nprobe` parameter controls how many IVF buckets to probe during search. A value of `0` is semantically invalid — it means "probe zero buckets", which should logically yield no results and should be rejected at the API layer.

**Actual response:**
```json
{
    "code": 0,
    "cost": 0,
    "data": [
        {"distance": 0, "id": 1},
        {"distance": 64, "id": 2},
        {"distance": 256, "id": 3}
    ],
    "topks": [3]
}
```

For comparison, Milvus correctly rejects `limit=0` (topk=0) with a clear error:
```json
{
    "code": 65535,
    "message": "topk [0] is invalid, it should be in range [1, 16384], but got 0"
}
```

This indicates that Milvus has parameter validation for `topk/limit` but is missing equivalent validation for `nprobe`.

### Expected Behavior

Milvus should reject search requests with `nprobe=0` (and likely any `nprobe < 1`) with an error res

## stage2_aggregation.confirmed
endpoint=entities+insert
defect_type=param_validation
related_issue_numbers=[49823]

## 探针脚本
.paperpilot/phase2/probes/milvus/probe_milvus_49823.py
# milvus_52310 (group=B, version=3.0.0)

## issue 标题
[Bug]: REST API v2 `entities/insert` silently coerces scalar types (string→Int64, int→VarChar, string→Bool); gRPC rejects all

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


The REST API v2 `entities/insert` endpoint silently coerces compatible-but-wrong types across scalar fields:

| Input type | Field type | REST v2 | Stored value | gRPC |
|-----------|-----------|---------|-------------|------|
| `"123"` (string) | Int64 | **accepted** | 123 | rejected |
| `123` (int) | VarChar | **accepted** | "123" | rejected |
| `"true"` (string) | Bool | **accepted** | true | rejected |
| `"1.5"` (string) | Float | **accepted** | 1.5 | rejected |

Issue #47766 fixed type validation on the gRPC path (milestone 2.6.14, closed 2026-05-08), but the REST API v2 path still exhibits the same behavior in v3.0.0.

The [Number Field documentation](https://milvus.io/docs/number.md) defines each scalar type with a specific data type code (`INT64`, `BOOL`, `FLOAT`, etc.) and describes them as storing specific value types — integers, booleans, or floating-point numbers. Cross-type coercion (string → Int64, int → VarChar, string → Bool) is not documented behavior.


### Expected Behavior


Scalar field types should enforce 

## stage2_aggregation.confirmed
endpoint=entities+insert
defect_type=type_coercion
related_issue_numbers=[52310]

## 探针脚本
.paperpilot/phase2/probes/milvus/probe_milvus_52310.py
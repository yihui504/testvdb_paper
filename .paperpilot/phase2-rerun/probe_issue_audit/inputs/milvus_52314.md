# milvus_52314 (group=B, version=3.0.0)

## issue 标题
[Bug]: REST API v2 `entities/upsert` silently coerces scalar types (string→DOUBLE, string→BOOL, int→BOOL, string→INT16)

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


The REST API v2 `POST /v2/vectordb/entities/upsert` endpoint silently coerces cross-type values for all scalar field types. The [Number Field documentation](https://milvus.io/docs/number.md) defines each scalar type with a specific data type code (`DOUBLE`, `BOOL`, `INT16`) and describes them as storing specific value types. Cross-type coercion (string → DOUBLE, string → BOOL, int → BOOL, string → INT16) is not documented behavior.

| Input | Field type | REST v2 | Stored value | gRPC |
|-------|-----------|---------|-------------|------|
| `"3.14159"` (string) | DOUBLE | **accepted** | 3.14159 | rejected |
| `"true"` (string) | BOOL | **accepted** | true | rejected |
| `1` (int) | BOOL | **accepted** | true | rejected |
| `"42"` (string) | INT16 | **accepted** | 42 | rejected |

The stored values are correct (coercion is consistent), but the input type is not validated. gRPC validates types client-side and rejects all cross-type inputs.


### Expected Behavior


Scalar field types should enforce strict type checking on the UPSE

## stage2_aggregation.confirmed
endpoint=entities+upsert
defect_type=type_coercion
related_issue_numbers=[52314]

## 探针脚本
.paperpilot/phase2/probes/milvus/probe_milvus_52314.py
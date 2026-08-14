# milvus_52315 (group=A, version=3.0.0)

## issue 标题
[Bug]: REST API v2 `entities/insert` accepts string-encoded vector values (gRPC rejects)

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


The REST API v2 `POST /v2/vectordb/entities/insert` endpoint accepts **string-encoded vector values** (JSON string containing a float array) for FLOAT_VECTOR fields. The [Dense Vector documentation](https://milvus.io/docs/dense-vector.md) describes vectors as "arrays of floating-point numbers with a fixed length, such as `[0.2, 0.7, 0.1, 0.8, ...]`" — a string representation like `"[0.1,0.2,0.3,0.4]"` is not an array of floating-point numbers, it is a serialized string.

```json
{"vector": "[0.1,0.2,0.3,0.4]"}  ← string, not array
```

The server parses the string and stores it correctly as a real float vector. gRPC rejects this with `DataNotMatchException: "should be float_vector, got str"`.

This is a different bug shape from scalar type coercion: it involves a **container field type** (FLOAT_VECTOR) accepting a **string-encoded representation** of its expected array format.


### Expected Behavior


Vector fields should only accept JSON arrays of numbers (`[0.1, 0.2, 0.3, 0.4]`), not string-encoded representations (`"[0.1,0.2

## stage2_aggregation.confirmed
endpoint=entities+insert
defect_type=type_coercion
related_issue_numbers=[52315]

## 探针脚本
.paperpilot/phase2/probes/milvus/probe_milvus_52315.py
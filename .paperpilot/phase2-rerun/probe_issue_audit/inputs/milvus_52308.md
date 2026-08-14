# milvus_52308 (group=B, version=3.0.0)

## issue 标题
[Bug]: REST API v2 `entities/insert` accepts string numbers for Int64 primary key (type coercion gap; gRPC rejects)

## issue body（截断 1500 字符）
### Is there an existing issue for this?

- [x] I have searched the existing issues

### Environment

```markdown
- Milvus version: v3.0.0 (release 2026-07-29, commit f46a0328558be155d11266a1a2b90602ccc9b366)
- Deployment mode: standalone (Docker, `milvusdb/milvus:v3.0.0`)
- MQ type: N/A (standalone default)
- SDK version: REST API v2 only (curl). pymilvus used for gRPC comparison only.
- OS: Windows 11 (Docker Desktop)
- CPU/Memory: N/A
- GPU: None
```

### Current Behavior


The REST API v2 `POST /v2/vectordb/entities/insert` endpoint silently coerces string numeric values into Int64 primary key fields. Inserting `{"id": "123", ...}` is accepted (`code: 0`) and stored as integer `123`.

The [Primary Field documentation](https://milvus.io/docs/primary-field.md) defines primary keys as `Int64` or `VarChar` data types. When a field is declared as `Int64`, a string value `"123"` should not be silently coerced — it should be rejected for type mismatch.

The **gRPC path** (pymilvus) correctly rejects the same input with `DataTypeVariableSetException`.

### Expected Behavior


Primary key fields declared as `Int64` should enforce strict type checking. A string value `"123"` should be rejected with a non-zero error code, consistent with the gRPC path.


### Steps To Reproduce

```markdown
**1. Create a collection with Int64 PK (autoID=false):**


curl -X POST http://localhost:19530/v2/vectordb/collections/create \
  -H "Content-Type: application/json" \
  -d '{
    "collectionName"

## stage2_aggregation.confirmed
endpoint=entities+insert
defect_type=type_coercion
related_issue_numbers=[52308]

## 探针脚本
.paperpilot/phase2/probes/milvus/probe_milvus_52308.py
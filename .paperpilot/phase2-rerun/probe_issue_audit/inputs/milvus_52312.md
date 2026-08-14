# milvus_52312 (group=B, version=3.0.0)

## issue 标题
[Bug]: REST API v2 `entities/upsert` accepts string numbers for Int64 primary key (gRPC rejects)

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


The REST API v2 `POST /v2/vectordb/entities/upsert` endpoint silently coerces string numeric values into Int64 primary key fields. Upserting `{"id": "100", ...}` is accepted (`code: 0`) and **overwrites the existing record**.

The [Primary Field documentation](https://milvus.io/docs/primary-field.md) defines primary keys as `Int64` or `VarChar`. When declared as `Int64`, a string value `"100"` should be rejected for type mismatch.

gRPC correctly rejects: `DataNotMatchException: "id field should be a int64, but got a str"`


### Expected Behavior


Primary key fields declared as `Int64` should enforce strict type checking on the UPSERT endpoint, consistent with gRPC.


### Steps To Reproduce

```markdown
# 1. Create + load collection
curl -X POST http://localhost:19530/v2/vectordb/collections/create \
  -H "Content-Type: application/json" \
  -d '{"collectionName":"test_upsert_pk","dimension":4}'

curl -X POST http://localhost:19530/v2/vectordb/entities/insert \
  -H "Content-Type: application/json" \
  -d '{"collectionName":"te

## stage2_aggregation.confirmed
endpoint=entities+insert
defect_type=type_coercion
related_issue_numbers=[52312]

## 探针脚本
.paperpilot/phase2/probes/milvus/probe_milvus_52312.py
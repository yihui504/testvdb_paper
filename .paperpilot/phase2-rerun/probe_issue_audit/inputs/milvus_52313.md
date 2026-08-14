# milvus_52313 (group=A, version=3.0.0)

## issue 标题
[Bug]: entities/insert JSON field — plain strings stored in inconsistent formats across REST/gRPC; written values unreadable via gRPC (round-trip failure)

## issue body（截断 1500 字符）
### Is there an existing issue for this?

- [x] I have searched the existing issues

### Environment

- Milvus version: v3.0.0 (release 2026-07-29, commit f46a0328558be155d11266a1a2b90602ccc9b366)
- Deployment mode: standalone (Docker, `milvusdb/milvus:v3.0.0`)
- SDK version: REST API v2 (curl) + pymilvus 2.5.5 (gRPC comparison)
- OS: Windows 11 (Docker Desktop)

### Current Behavior

On v3.0.0, `POST /v2/vectordb/entities/insert` accepts a plain string (e.g. `"plain_string"`) for a `DataType.JSON` field on **both** REST and gRPC paths (HTTP 200 / no exception). Three independently verifiable problems result:

1. **Round-trip failure via gRPC — but only for REST-written records.** `pymilvus` `get()` on a record inserted via **REST** raises `MilvusException: Unexpected error, message=<Expected object or value>`. The official gRPC client cannot read back records the server accepted.
2. **REST and gRPC store the same input in different formats.** A plain string inserted via REST is stored bare (`plain_string`); the same plain string inserted via gRPC is stored JSON-encoded (`"plain_string"`, with quotes). Identical input produces different stored bytes depending on which API wrote it.
3. **Newly inserted records are unqueryable from gRPC.** Any record whose JSON field holds a REST-written plain string is invisible to gRPC-side JSON predicates (`JSON_CONTAINS`, etc.) — the client cannot even retrieve it by primary key.

### Expected Behavior

- A record inserted through any offic

## stage2_aggregation.confirmed
endpoint=entities+insert
defect_type=semantics
related_issue_numbers=[52313]

## 探针脚本
.paperpilot/phase2/probes/milvus/probe_milvus_52313.py
# milvus_52307 (group=A, version=3.0.0)

## issue 标题
[Bug]: entities/upsert JSON field — plain string overwrites valid JSON; written value unreadable via gRPC; REST/gRPC store inconsistent formats

## issue body（截断 1500 字符）
### Is there an existing issue for this?

- [x] I have searched the existing issues

### Environment

- Milvus version: v3.0.0 (release 2026-07-29, commit f46a0328558be155d11266a1a2b90602ccc9b366)
- Deployment mode: standalone (Docker, `milvusdb/milvus:v3.0.0`)
- SDK version: REST API v2 (curl) + pymilvus 2.5.5 (gRPC comparison)
- OS: Windows 11 (Docker Desktop)

### Current Behavior

On v3.0.0, `POST /v2/vectordb/entities/upsert` accepts a plain string (e.g. `"invalid_json"`) for a `DataType.JSON` field on **both** REST and gRPC paths (HTTP 200 / no exception). Three independently verifiable problems result:

1. **Upsert overwrites existing valid JSON data.** A record whose `meta` was `{"important":"data"}` becomes the plain string `invalid_json` — the original structured data is lost.
2. **Round-trip failure via gRPC.** After the upsert, `pymilvus` `get()` on the affected record raises `MilvusException: Unexpected error, message=<Expected object or value>`. The official gRPC client cannot read back data the server accepted.
3. **REST and gRPC store the same input in different formats.** A plain string written via REST upsert is stored bare (`invalid_json`); the same plain string written via gRPC upsert is stored JSON-encoded (`"grpc_plain_str"`, with quotes). Same input, different stored bytes.

### Expected Behavior

- A value written to a `DataType.JSON` field must be readable via the official gRPC client (round-trip integrity). The server must not accept a write it canno

## stage2_aggregation.confirmed
endpoint=entities+upsert
defect_type=semantics
related_issue_numbers=[52307]

## 探针脚本
.paperpilot/phase2/probes/milvus/probe_milvus_52307.py
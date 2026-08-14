# milvus_49843 (group=A, version=2.6.16)

## issue 标题
[Bug]: REST API v2 silently drops negative collection.ttl.seconds on collection create

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
- Others: Reproduced via Milvus REST API v2 (`/v2/vectordb/collections/create` and `/v2/vectordb/collections/alter_properties`)
```

### Current Behavior

When creating a collection with a negative `collection.ttl.seconds` property via the REST API v2, Milvus returns `code=0` (success) but **silently drops the TTL property** — the created collection has no TTL set at all.

This is inconsistent with the `alter_properties` endpoint, which correctly rejects negative TTL values with a clear error message:

```
{"code":1100,"message":"collection TTL is out of range, expect [-1, 3155760000], got -100: invalid parameter"}
```

**Create with negative TTL (BUG — returns success but TTL is silently dropped):**
```json
// Request: POST /v2/vectordb/collections/create
{"collectionName":"test_ttl_neg","dimension":4,"metricType":"L2","properties":{"collection.ttl.seconds":-100}}

// Response:
{"code":0,"data":{}}

// But describe shows NO TTL property:
// "properties": [{"key": "timezone", "value": "UTC"}]
// Missing: "collection.ttl.seconds"
```

**Alter with negative TTL (correctly rejects):**
```json
// Request: POST /v2/

## stage2_aggregation.confirmed
endpoint=collections+alter
defect_type=semantics
related_issue_numbers=[49843]

## 探针脚本
.paperpilot/phase2/probes/milvus/probe_milvus_49843.py
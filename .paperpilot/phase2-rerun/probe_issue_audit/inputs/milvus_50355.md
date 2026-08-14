# milvus_50355 (group=A, version=2.6.17)

## issue 标题
[Bug]: Upsert fails on autoID=true collections despite documentation claiming support

## issue body（截断 1500 字符）
### Is there an existing issue for this?

- [x] I have searched the existing issues

### Environment

```markdown
- Milvus version: v2.6.17
- Deployment mode(standalone or cluster): standalone (Docker)
- MQ type(rocksmq, pulsar or kafka): rocksmq (standalone default)
- SDK version(e.g. pymilvus v2.0.0rc2): REST API v2 (/v2/vectordb) & PyMilvus
- OS(Ubuntu or CentOS): Windows 11 (Docker Desktop)
- CPU/Memory: N/A
- GPU: N/A
- Others:
```

### Current Behavior


Upsert operation does not work with `autoID=true` collections. When no primary key is provided (the correct usage for autoID), upsert fails across all SDKs. This contradicts the official v2.6.x documentation which explicitly states that upsert should auto-generate primary keys when autoID is enabled.

**Cross-SDK test results:**

| SDK | autoID | Provided PK? | Operation | Result | Error Message |
|-----|--------|-------------|-----------|--------|---------------|
| REST API v2 | true | ❌ | upsert | ❌ code=1100 | "upsert can not assign primary field data when auto id enabled id" |
| PyMilvus | true | ❌ | upsert | ❌ DataNotMatchException | "Insert missed an field `id`" |
| REST API v2 | true | ✅ | upsert | ❌ code=1804 | "set primary key but autoID == true" |
| PyMilvus | true | ✅ | upsert | ❌ MilvusException | "the number of fields is less than needed" |
| REST API v2 | false | ✅ | upsert | ✅ code=200 | — |
| PyMilvus | false | ✅ | upsert | ✅ upsert_count=1 | — |
| REST API v2 | true | ❌ | insert | ✅ code=200 | auto-gene

## stage2_aggregation.confirmed
endpoint=entities+upsert
defect_type=behavior
related_issue_numbers=[50355]

## 探针脚本
.paperpilot/phase2/probes/milvus/probe_milvus_50355.py
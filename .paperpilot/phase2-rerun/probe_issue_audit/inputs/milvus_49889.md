# milvus_49889 (group=B, version=2.6.16)

## issue 标题
[Bug]: REST API v2 accepts empty string for `dbName` parameter

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
- Others: Reproduced via Milvus REST API v2
```

### Current Behavior

The Milvus v2 REST API accepts empty strings (`""`) for the `dbName` parameter across multiple endpoints. The official documentation defines `dbName` as "The name of an **existing** database" — an empty string is not a valid database name, yet the API returns `code: 0` (success) with no validation error.

This is the same category of bug as #49844 (filter null/missing accepted), which has been `triage/accepted`.

**Empty dbName on collections/list:**
```bash
curl -s -X POST 'http://localhost:19530/v2/vectordb/collections/list' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer root:Milvus' \
  -d '{"dbName": ""}'
```
Response: `{"code":0,"data":[]}` — success, silently defaults to the default database.

**Empty dbName on collections/describe:**
```bash
curl -s -X POST 'http://localhost:19530/v2/vectordb/collections/describe' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer root:Milvus' \
  -d '{"collectionName": "test_collection", "dbName": ""}'
```
Response: `{"code":0,"data":{...}}` — success, no val

## stage2_aggregation.confirmed
endpoint=collections+create
defect_type=param_validation
related_issue_numbers=[49889]

## 探针脚本
.paperpilot/phase2/probes/milvus/probe_milvus_49889.py
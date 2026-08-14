# milvus_50018 (group=B, version=2.6.16)

## issue 标题
[Bug]: REST API v2 aliases/list accepts empty collectionName while other endpoints properly reject it

## issue body（截断 1500 字符）
### Is there an existing issue for this?

- [x] I have searched the existing issues (similar: #49889 for dbName=""; #49843 for TTL)

### Environment

```
- Milvus version: v2.6.16
- Deployment mode(standalone or cluster): standalone
- MQ type(rocksmq, pulsar or kafka): rocksmq
- SDK version(e.g. pymilvus v2.0.0rc2): REST API v2 (via curl)
- OS(Ubuntu or CentOS): Docker on Windows
- CPU/Memory: N/A
- GPU: N/A
- Others: Reproduced via Milvus REST API v2 (/v2/vectordb/aliases/list)
```

### Current Behavior

The POST /v2/vectordb/aliases/list endpoint accepts an empty string for the collectionName parameter and returns code=0 (success). This is inconsistent with other endpoints that accept collectionName -- most of which correctly reject empty strings with code=1802 and a validation error message.

aliases/list with collectionName="" (BUG):
```
curl -s -X POST 'http://localhost:19530/v2/vectordb/aliases/list'   -H 'Content-Type: application/json'   -H 'Authorization: Bearer root:Milvus'   -d '{"collectionName":"", "dbName":"default"}'
# Response: {"code":0, "data":[]}
```

For contrast -- most other endpoints correctly reject empty collectionName:

collections/create  collectionName="" -> code=1802, "Field validation for 'CollectionName' failed on the 'required' tag"
collections/describe collectionName="" -> code=1802
collections/drop    collectionName="" -> code=1802
collections/load    collectionName="" -> code=1802
aliases/list        collectionName="" -> code=0  <-- BUG (mis

## stage2_aggregation.confirmed
endpoint=aliases+list
defect_type=param_validation
related_issue_numbers=[50018]

## 探针脚本
.paperpilot/phase2/probes/milvus/probe_milvus_50018.py
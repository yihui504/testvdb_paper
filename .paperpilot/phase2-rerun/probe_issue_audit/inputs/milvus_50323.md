# milvus_50323 (group=B, version=2.6.17)

## issue 标题
[Bug]: Delete endpoint accepts both filter and ids (mutually exclusive) silently

## issue body（截断 1500 字符）
### Is there an existing issue for this?

- [x] I have searched the existing issues

### Environment

```markdown
- Milvus version: v2.6.17
- Deployment mode: standalone (Docker)
- MQ type: rocksmq (standalone default)
- SDK version: REST API (v2/vectordb)
- OS: Windows 11 (Docker Desktop)
- CPU/Memory: Docker default
- GPU: None
- Others: Fresh install, no prior data
```

### Current Behavior


The `entities/delete` endpoint silently accepts **both** `filter` and `ids` parameters simultaneously — documented as **mutually exclusive**. The operation proceeds using `filter` and ignores `ids`, returning `deleteCount` matching the filter.

```
POST /v2/vectordb/entities/delete
{"collectionName": "test", "dbName": "default", "filter": "id > 0", "ids": [1, 2, 3]}

Response: {"code": 0, "data": {"deleteCount": 1}}
```


### Expected Behavior

Return validation error when both `filter` and `ids` are provided simultaneously.


### Steps To Reproduce

```markdown
import requests
BASE = "http://localhost:19530/v2/vectordb"
H = {"Content-Type": "application/json"}

# Setup
requests.post(f"{BASE}/collections/create", json={
    "collectionName": "test_del", "dimension": 4, "metricType": "COSINE",
    "idType": "Int64", "autoID": False}, headers=H)
requests.post(f"{BASE}/entities/insert", json={
    "collectionName": "test_del", "data": [{"id": 1, "vector": [0.1,0.2,0.3,0.4]}]
}, headers=H)

# Delete with BOTH filter AND ids
r = requests.post(f"{BASE}/entities/delete", json={
    "collecti

## stage2_aggregation.confirmed
endpoint=entities+insert
defect_type=behavior
related_issue_numbers=[50323]

## 探针脚本
.paperpilot/phase2/probes/milvus/probe_milvus_50323.py
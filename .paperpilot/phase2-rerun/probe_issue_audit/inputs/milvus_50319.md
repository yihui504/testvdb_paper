# milvus_50319 (group=C, version=2.6.17)

## issue 标题
[Bug]: Search on unloaded collection returns valid results (code=0)

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


Search (`entities/search`) and query (`entities/query`) on a collection that was **never loaded** (`collections/load`) return `code=0` with valid data, instead of rejecting with "collection not loaded".

```
POST /v2/vectordb/entities/search
{"collectionName": "test", "data": [[0.1, 0.2, 0.3, 0.4]], "annsField": "vector", "limit": 5}

Response: {"code": 0, "data": [{"id": 1, "distance": 0.999}, {"id": 2, "distance": 0.998}]}
```

### Expected Behavior


Return `code=1` with message "collection not loaded". The REST API contract requires `load` before `search`/`query`.

### Steps To Reproduce

```markdown
import requests
BASE = "http://localhost:19530/v2/vectordb"
H = {"Content-Type": "application/json"}

# 1. Create collection
requests.post(f"{BASE}/collections/create", json={
    "collectionName": "test_unloaded", "dimension": 4, "metricType": "COSINE",
    "idType": "Int64", "autoID": False}, headers=H)

# 2. Insert data (DO NOT call load)
requests.post(f"{BASE}/entities/insert", json={
    "collectionName": "test_unloaded",
    "data": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4]}]
},

## stage2_aggregation.confirmed
endpoint=entities+search
defect_type=behavior
related_issue_numbers=[50319]

## 探针脚本
.paperpilot/phase2/probes/milvus/probe_milvus_50319.py
# milvus_50324 (group=C, version=2.6.17)

## issue 标题
[Bug]: REST API: Insert accepts 101 entities (exceeding documented 100 limit)

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


The `entities/insert` endpoint accepts **101 entities** in a single REST call, returning `insertCount=101` with `code=0`. The REST API documentation states a limit of **100 entities per call**.

```
POST /v2/vectordb/entities/insert
{"collectionName": "test", "data": [101 entities]}

Response: {"code": 0, "data": {"insertCount": 101}}
```

### Expected Behavior


Return validation error when the entity count exceeds 100, per REST API documentation.


### Steps To Reproduce

```markdown
import requests
BASE = "http://localhost:19530/v2/vectordb"
H = {"Content-Type": "application/json"}

requests.post(f"{BASE}/collections/create", json={
    "collectionName": "test_limit", "dimension": 4, "metricType": "COSINE",
    "idType": "Int64", "autoID": False}, headers=H)

data = [{"id": i, "vector": [0.1, 0.2, 0.3, 0.4]} for i in range(101)]
r = requests.post(f"{BASE}/entities/insert", json={
    "collectionName": "test_limit", "data": data}, headers=H)
print(r.json())  # {"code": 0, "data": {"insertCount": 101}}
```

### Milvus Log


```
No error or warning generated.
```


### Anything else?


## stage2_aggregation.confirmed
endpoint=entities+insert
defect_type=param_validation
related_issue_numbers=[50324]

## 探针脚本
.paperpilot/phase2/probes/milvus/probe_milvus_50324.py
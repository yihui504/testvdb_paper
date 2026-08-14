# milvus_50321 (group=C, version=2.6.17)

## issue 标题
[Bug]: Duplicate collection creation returns code=0 instead of error

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

Creating a collection with an **already-existing name** returns `{"code": 0, "data": {}}` — identical to a successful first creation. No error code or "collection already exists" message.

### Expected Behavior

Return a non-zero error code with message indicating "collection already exists".

### Steps To Reproduce

```markdown
import requests
BASE = "http://localhost:19530/v2/vectordb"
H = {"Content-Type": "application/json"}
payload = {"collectionName": "test_dup", "dimension": 4, "metricType": "COSINE", "idType": "Int64", "autoID": False}

# First create — succeeds (code=0)
requests.post(f"{BASE}/collections/create", json=payload, headers=H)

# Second create with SAME name — should fail, but succeeds (code=0)
r = requests.post(f"{BASE}/collections/create", json=payload, headers=H)
print(r.json())  # {"code": 0, "data": {}} ← BUG
```

### Milvus Log

```
No error log generated — duplicate creation returns success silently.
```

### Anything else?


- Tested on fresh install with no prior collections, aliases, or special configurations
- Both creates return identical responses — impo

## stage2_aggregation.confirmed
endpoint=collections+create
defect_type=behavior
related_issue_numbers=[50321]

## 探针脚本
.paperpilot/phase2/probes/milvus/probe_milvus_50321.py
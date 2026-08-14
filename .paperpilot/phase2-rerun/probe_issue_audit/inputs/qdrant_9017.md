# qdrant_9017 (group=A, version=1.18.0)

## issue 标题
hnsw_ef accepts 0

## issue body（截断 1500 字符）
## Current Behavior

Qdrant accepts `params.hnsw_ef: 0` in search requests and returns HTTP 200 OK with results, despite `hnsw_ef=0` being semantically invalid for the HNSW algorithm. This allows a meaningless parameter value to bypass server-side validation and succeed silently.

Confirmed on both **v1.17.1** and **v1.18.0**. Independently verified against a standalone `qdrant/qdrant:v1.18.0` Docker container on `localhost:6334`.

## Steps to Reproduce

1. Start a Qdrant instance (e.g., `docker run -p 6333:6333 qdrant/qdrant:v1.18.0`)
2. Create a collection with a 4-dimensional Cosine vector config:

```python
import requests

BASE = "http://localhost:6333"
COLLECTION = "test_hnsw_bug"

requests.put(f"{BASE}/collections/{COLLECTION}", json={
    "vectors": {"size": 4, "distance": "Cosine"}
})
```

3. Insert a point:

```python
import time
time.sleep(0.5)

requests.put(f"{BASE}/collections/{COLLECTION}/points", json={
    "points": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4]}]
})
```

4. Search with `hnsw_ef=0` (should be rejected but isn't):

```python
r = requests.post(f"{BASE}/collections/{COLLECTION}/points/search", json={
    "vector": [0.1, 0.2, 0.3, 0.4],
    "limit": 3,
    "params": {"hnsw_ef": 0}
})
print(r.status_code, r.json())
# Expected: 400 or 422
# Actual: 200 OK with search results (score=1.0)
```

**Observed output**:
```
Search hnsw_ef=0: status=200
Response: {
  "result": [
    {
      "id": 1,
      "version": 1,
      "score": 1.0
    }
  ],
  "status": "o

## stage2_aggregation.confirmed
endpoint=points
defect_type=param_validation
related_issue_numbers=[9017]

## 探针脚本
.paperpilot/phase2/probes/qdrant/probe_qdrant_9017.py
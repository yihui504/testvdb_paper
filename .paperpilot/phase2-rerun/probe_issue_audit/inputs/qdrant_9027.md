# qdrant_9027 (group=C, version=1.18.0)

## issue 标题
score_threshold_range_issue

## issue body（截断 1500 字符）
## Current Behavior

Qdrant accepts `score_threshold` values outside the [0.0, 1.0] range in search requests and returns HTTP 200 OK, despite such values being semantically invalid for similarity scores. Both positive overflow (e.g., `score_threshold=2.0`) and negative values (e.g., `score_threshold=-0.5`) bypass server-side validation and succeed silently.

Confirmed on **v1.18.0**. Independently verified against a standalone `qdrant/qdrant:v1.18.0` Docker container on `localhost:6335`.

## Steps to Reproduce

1. Start a Qdrant instance (e.g., `docker run -p 6333:6333 qdrant/qdrant:v1.18.0`)

2. Create a collection with a 4-dimensional Cosine vector config:

```python
import requests

BASE = "http://localhost:6333"
COLLECTION = "test_score_threshold_bug"

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

4. Search with `score_threshold=2.0` (should be rejected but isn't):

```python
r = requests.post(f"{BASE}/collections/{COLLECTION}/points/search", json={
    "vector": [0.1, 0.2, 0.3, 0.4],
    "limit": 5,
    "score_threshold": 2.0
})
print(r.status_code, r.json())
# Expected: 400 or 422
# Actual: 200 OK with empty results
```

5. Search with `score_threshold=-0.5` (should be rejected but isn't):

```python
r = requests.post(f

## stage2_aggregation.confirmed
endpoint=points
defect_type=behavior
related_issue_numbers=[9027]

## 探针脚本
.paperpilot/phase2/probes/qdrant/probe_qdrant_9027.py
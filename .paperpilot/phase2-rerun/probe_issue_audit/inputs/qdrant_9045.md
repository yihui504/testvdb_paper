# qdrant_9045 (group=A, version=1.12.1)

## issue 标题
Bug: Empty vector `[]` upsert with `wait=false` can trigger server panic (zero-length assertion failure)

## issue body（截断 1500 字符）
## Summary

When upserting a point with an empty vector `[]` (zero dimensions) **without** the `wait=true` parameter, the API returns HTTP 200 with `"status": "acknowledged"`. While the point is eventually discarded during async processing, the zero-length vector can reach internal code paths that assert on non-zero length, causing **server panics** in distributed/sharded deployments.

This is distinct from the general "async upsert skips validation" issue (#2557, closed as not_planned) because empty vectors pose a **server stability risk** beyond mere poor diagnostics.

## Current Behavior

```python
import requests, time

BASE = "http://localhost:6333"

# Setup: create 4-dim collection
requests.put(f"{BASE}/collections/test", json={"vectors": {"size": 4, "distance": "Cosine"}})
time.sleep(0.5)

# With wait=true: correctly rejects empty vector
r_wait = requests.put(f"{BASE}/collections/test/points?wait=true", json={
    "points": [{"id": 1, "vector": []}]
})
print(f"wait=true:  status={r_wait.status_code}")  # 400 ✅

# Without wait: silently accepts empty vector
r_nowait = requests.put(f"{BASE}/collections/test/points", json={
    "points": [{"id": 2, "vector": []}]
})
print(f"wait=false: status={r_nowait.status_code}")  # 200 ❌
```

## Why This Is Different From #2557

I'm aware that #2557 (async upsert dimension validation) was closed as "not planned". This issue is filed separately because empty vectors are **qualitatively different** from wrong-dimension vectors:

| Aspe

## stage2_aggregation.confirmed
endpoint=points
defect_type=crash
related_issue_numbers=[9045]

## 探针脚本
.paperpilot/phase2/probes/qdrant/probe_qdrant_9045.py
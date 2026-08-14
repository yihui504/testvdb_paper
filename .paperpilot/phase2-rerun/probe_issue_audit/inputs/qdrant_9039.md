# qdrant_9039 (group=A, version=1.18.0)

## issue 标题
Bug: Async upsert silently discards dimension-mismatched vectors (Poor Diagnostics)

## issue body（截断 1500 字符）
**Note**: This issue was previously reported as [#2557](https://github.com/qdrant/qdrant/issues/2557). This report provides additional evidence with a comparative analysis of `wait=true` vs `wait=fal·se` behavior, and reclassifies the defect from `IllegalSuccess` to `PoorDiagnostics` based on deeper investigation.

## Summary

When upserting a point with a wrong-dimension vector (e.g., 3-dim vector into a 4-dim collection) **without** the `wait=true` parameter, the API returns HTTP 200 with `"status": "acknowledged"`, but the point is **silently discarded** during async processing. In contrast, the same operation **with** `wait=true` correctly returns HTTP 400 with a clear error message.

This creates a diagnostic gap: users who rely on the default async behavior receive no indication that their data was rejected, potentially leading to data loss without any error feedback.

## Current Behavior

```python
import requests, time

BASE = "http://localhost:6333"

# Setup: create 4-dim collection
requests.put(f"{BASE}/collections/test", json={"vectors": {"size": 4, "distance": "Cosine"}})
time.sleep(0.5)

# With wait=true: correctly rejects
r_wait = requests.put(f"{BASE}/collections/test/points?wait=true", json={
    "points": [{"id": 1, "vector": [0.1, 0.2, 0.3]}]  # 3-dim into 4-dim
})
print(f"wait=true:  status={r_wait.status_code}")  # 400 ✅
print(f"  error: {r_wait.json()}")  # "Vector dimension error: expected dim: 4, got 3"

# Without wait: silently discards
r_nowait = requ

## stage2_aggregation.confirmed
endpoint=points
defect_type=type_coercion
related_issue_numbers=[9039]

## 探针脚本
.paperpilot/phase2/probes/qdrant/probe_qdrant_9039.py
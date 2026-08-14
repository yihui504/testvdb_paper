# qdrant_9523 (group=C, version=1.18.2)

## issue 标题
Search offset pagination returns duplicate point IDs across pages (HNSW approximation)

## issue body（截断 1500 字符）
---

## Current Behavior

When using the Search API (`POST /collections/{collection_name}/points/search`) with `offset`-based pagination, Qdrant v1.18.2 returns **duplicate point IDs across pages**. Points that appear on page 1 (offset=0) reappear on page 2 (offset=10) and page 3 (offset=20), violating the basic pagination contract that successive pages should contain non-overlapping result sets.

This makes offset-based pagination unreliable for enumerating search results.

## Steps to Reproduce

**Environment**: Qdrant v1.18.2 via Docker (`qdrant/qdrant:v1.18.2`), running at `http://localhost:6333`.

**1. Create collection with 25 points:**

```bash
curl -X PUT http://localhost:6333/collections/test_pagination_dedup \
  -H "Content-Type: application/json" \
  -d '{"vectors": {"size": 4, "distance": "Cosine"}}'
```

**2. Seed 25 points with sequential IDs:**

```bash
curl -X PUT http://localhost:6333/collections/test_pagination_dedup/points \
  -H "Content-Type: application/json" \
  -d '{
    "points": [
      {"id": 0, "vector": [0.1, 0.05, 0.033, 0.025], "payload": {"idx": 0, "group": 0}},
      {"id": 1, "vector": [0.2, 0.10, 0.067, 0.050], "payload": {"idx": 1, "group": 1}},
      {"id": 2, "vector": [0.3, 0.15, 0.100, 0.075], "payload": {"idx": 2, "group": 2}},
      {"id": 3, "vector": [0.4, 0.20, 0.133, 0.100], "payload": {"idx": 3, "group": 3}},
      {"id": 4, "vector": [0.5, 0.25, 0.167, 0.125], "payload": {"idx": 4, "group": 4}},
      {"id": 5, "vector": [0.6, 0

## stage2_aggregation.confirmed
endpoint=collections+{collection_name}+points
defect_type=behavior
related_issue_numbers=[9523]

## 探针脚本
.paperpilot/phase2/probes/qdrant/probe_qdrant_9523.py
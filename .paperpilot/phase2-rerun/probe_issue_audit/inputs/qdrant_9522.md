# qdrant_9522 (group=A, version=1.18.2)

## issue 标题
Query API silently returns 200 OK when lookup_from references a non-existent collection

## issue body（截断 1500 字符）
---

## Current Behavior

When using the Query API (`POST /collections/{collection_name}/points/query`) with the `lookup_from` parameter referencing a **non-existent collection**, Qdrant v1.18.2 silently returns `200 OK` with results from the source collection, instead of returning a `400` or `404` error indicating that the lookup target collection does not exist.

The API performs no validation on the `lookup_from.collection` field, so typos or references to deleted collections produce silently incorrect results with no error feedback.

## Steps to Reproduce

**Environment**: Qdrant v1.18.2 via Docker (`qdrant/qdrant:v1.18.2`), running at `http://localhost:6333`.

**1. Create source collection:**

```bash
curl -X PUT http://localhost:6333/collections/test_lookup_source \
  -H "Content-Type: application/json" \
  -d '{"vectors": {"size": 4, "distance": "Cosine"}}'
```

**2. Create target collection:**

```bash
curl -X PUT http://localhost:6333/collections/test_lookup_target \
  -H "Content-Type: application/json" \
  -d '{"vectors": {"size": 4, "distance": "Cosine"}}'
```

**3. Seed source collection with 5 points:**

```bash
curl -X PUT http://localhost:6333/collections/test_lookup_source/points \
  -H "Content-Type: application/json" \
  -d '{
    "points": [
      {"id": 0, "vector": [0.1, 0.2, 0.3, 0.4], "payload": {"tag": "src_0", "category": "A"}},
      {"id": 1, "vector": [0.2, 0.4, 0.6, 0.8], "payload": {"tag": "src_1", "category": "A"}},
      {"id": 2, "vector": [0

## stage2_aggregation.confirmed
endpoint=collections+{collection_name}+points+query
defect_type=behavior
related_issue_numbers=[9522]

## 探针脚本
.paperpilot/phase2/probes/qdrant/probe_qdrant_9522.py
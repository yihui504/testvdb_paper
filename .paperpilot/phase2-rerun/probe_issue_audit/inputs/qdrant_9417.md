# qdrant_9417 (group=C, version=1.18.2)

## issue 标题
Missing `vectors` field silently accepted during collection creation — produces unusable collection

## issue body（截断 1500 字符）
## Current Behavior

When creating a collection via `PUT /collections/{collection_name}`, omitting the `vectors` field entirely from the request body is accepted with HTTP 200, despite the fact that a collection without vector configuration cannot serve any vector operations. The resulting collection is silently broken.

```bash
curl -X PUT "http://localhost:6333/collections/broken2" \
  -H "Content-Type: application/json" \
  -d '{"shard_number": 1}'
# → HTTP 200 ✅ (WRONG — should be 4xx)
```

The created collection has no vector configuration and rejects all subsequent operations:
```bash
curl -X PUT "http://localhost:6333/collections/broken2/points?wait=true" \
  -H "Content-Type: application/json" \
  -d '{"points": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4]}]}'
# → HTTP 400: "Wrong input: Default vector config is not found in collection"
```

## Steps to Reproduce

1. Start Qdrant v1.18.2:
   ```bash
   docker run -p 6333:6333 qdrant/qdrant:v1.18.2
   ```

2. Create a collection **without** the `vectors` field:
   ```bash
   curl -X PUT "http://localhost:6333/collections/no_vectors" \
     -H "Content-Type: application/json" \
     -d '{"shard_number": 1}'
   # Expected: 4xx
   # Actual: 200
   ```

3. Verify the collection exists but is broken:
   ```bash
   curl "http://localhost:6333/collections/no_vectors"
   # → 200 — collection exists, but no vector config
   ```

4. Attempt to insert data:
   ```bash
   curl -X PUT "http://localhost:6333/collections/no_vectors/poin

## stage2_aggregation.confirmed
endpoint=collections+{collection_name}+points
defect_type=param_validation
related_issue_numbers=[9417]

## 探针脚本
.paperpilot/phase2/probes/qdrant/probe_qdrant_9417.py
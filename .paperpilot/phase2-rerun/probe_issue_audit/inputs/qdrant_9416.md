# qdrant_9416 (group=C, version=1.18.2)

## issue 标题
`vectors={}` silently accepted during collection creation — produces unusable collection

## issue body（截断 1500 字符）

## Current Behavior

When creating a collection via `PUT /collections/{collection_name}`, passing an empty object `{}` as the `vectors` parameter is accepted with HTTP 200, creating a collection that has **no vector configuration**. The resulting collection is completely unusable — any subsequent insert or search operation fails with a confusing error.

```bash
curl -X PUT "http://localhost:6333/collections/broken" \
  -H "Content-Type: application/json" \
  -d '{"vectors": {}}'
# → HTTP 200 ✅ (WRONG — should be 4xx)
```

Subsequent operations on the broken collection fail:
```bash
curl -X PUT "http://localhost:6333/collections/broken/points?wait=true" \
  -H "Content-Type: application/json" \
  -d '{"points": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4]}]}'
# → HTTP 400: "Wrong input: Default vector config is not found in collection"
```

The error message references "Default vector config" but the user just created the collection — they have no idea why the default vector config is missing.

## Steps to Reproduce

1. Start Qdrant v1.18.2:
   ```bash
   docker run -p 6333:6333 qdrant/qdrant:v1.18.2
   ```

2. Create a collection with empty vectors object:
   ```bash
   curl -X PUT "http://localhost:6333/collections/broken" \
     -H "Content-Type: application/json" \
     -d '{"vectors": {}}'
   # Expected: 4xx
   # Actual: 200
   ```

3. Try to insert a point:
   ```bash
   curl -X PUT "http://localhost:6333/collections/broken/points?wait=true" \
     -H "Content-Type: applic

## stage2_aggregation.confirmed
endpoint=collections+{collection_name}+points
defect_type=param_validation
related_issue_numbers=[9416]

## 探针脚本
.paperpilot/phase2/probes/qdrant/probe_qdrant_9416.py
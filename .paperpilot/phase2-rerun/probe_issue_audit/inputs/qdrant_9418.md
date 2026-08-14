# qdrant_9418 (group=C, version=1.18.2)

## issue 标题
`filter.should=null` silently accepted in query/search — null filter condition ignored

## issue body（截断 1500 字符）
## Current Behavior

When sending a query request to `POST /collections/{collection_name}/points/query` with `filter.should=null`, the API returns HTTP 200 with results as if no filter was applied. The null value is silently accepted and ignored, rather than being rejected with a validation error.

```bash
curl -X POST "http://localhost:6333/collections/test/points/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": [0.1, 0.2, 0.3, 0.4],
    "limit": 5,
    "filter": {"should": null}
  }'
# → HTTP 200 ✅ (WRONG — should be 4xx)
# Returns all points (null filter silently ignored)
```

Note: the `should` field in a filter expects an array of condition objects, not `null`.

## Steps to Reproduce

1. Start Qdrant v1.18.2:
   ```bash
   docker run -p 6333:6333 qdrant/qdrant:v1.18.2
   ```

2. Create a test collection and insert data:
   ```bash
   # Create collection
   curl -X PUT "http://localhost:6333/collections/test_filter_null" \
     -H "Content-Type: application/json" \
     -d '{"vectors": {"size": 4, "distance": "Cosine"}}'

   # Insert points
   curl -X PUT "http://localhost:6333/collections/test_filter_null/points?wait=true" \
     -H "Content-Type: application/json" \
     -d '{"points": [
       {"id": 1, "vector": [0.1, 0.2, 0.3, 0.4], "payload": {"tag": "A"}},
       {"id": 2, "vector": [0.1, 0.2, 0.3, 0.4], "payload": {"tag": "B"}}
     ]}'
   ```

3. Query with `filter.should=null`:
   ```bash
   curl -X POST "http://localhost:6333/collections/te

## stage2_aggregation.confirmed
endpoint=collections+{collection_name}+points
defect_type=param_validation
related_issue_numbers=[9418]

## 探针脚本
.paperpilot/phase2/probes/qdrant/probe_qdrant_9418.py
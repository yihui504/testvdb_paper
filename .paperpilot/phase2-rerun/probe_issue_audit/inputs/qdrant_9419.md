# qdrant_9419 (group=C, version=1.18.2)

## issue 标题
`filter.must_not` accepts object instead of array — type mismatch silently ignored

## issue body（截断 1500 字符）
## Current Behavior

When sending a query request with `filter.must_not` set to an object (instead of the expected array), the API returns HTTP 200 with results as if no filter was applied. The type mismatch is silently ignored.

```bash
curl -X POST "http://localhost:6333/collections/test/points/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": [0.1, 0.2, 0.3, 0.4],
    "limit": 5,
    "filter": {
      "must_not": {"key": "tag", "match": {"value": "x"}}
    }
  }'
# → HTTP 200 ✅ (WRONG — should be 4xx)
# filter.must_not expects an ARRAY of conditions, not a single object
```

The `must_not` field in a filter expects an **array** of condition objects. Passing a single object is a type error that should be rejected.

## Steps to Reproduce

1. Start Qdrant v1.18.2:
   ```bash
   docker run -p 6333:6333 qdrant/qdrant:v1.18.2
   ```

2. Create a test collection and insert data:
   ```bash
   curl -X PUT "http://localhost:6333/collections/test_mustnot" \
     -H "Content-Type: application/json" \
     -d '{"vectors": {"size": 4, "distance": "Cosine"}}'

   curl -X PUT "http://localhost:6333/collections/test_mustnot/points?wait=true" \
     -H "Content-Type: application/json" \
     -d '{"points": [
       {"id": 1, "vector": [0.1, 0.2, 0.3, 0.4], "payload": {"tag": "x"}},
       {"id": 2, "vector": [0.1, 0.2, 0.3, 0.4], "payload": {"tag": "y"}}
     ]}'
   ```

3. Query with `filter.must_not` as an object (not array):
   ```bash
   curl -X POST "http://localho

## stage2_aggregation.confirmed
endpoint=points
defect_type=param_validation
related_issue_numbers=[9419]

## 探针脚本
.paperpilot/phase2/probes/qdrant/probe_qdrant_9419.py
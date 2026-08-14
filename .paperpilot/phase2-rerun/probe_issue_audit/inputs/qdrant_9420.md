# qdrant_9420 (group=C, version=1.18.2)

## issue 标题
`query=null` silently accepted — returns all points instead of being rejected

## issue body（截断 1500 字符）
## Current Behavior

When sending a query request with `query=null`, the API returns HTTP 200 with the full point set ordered by ID, rather than rejecting the null value. This is a silent fallback behavior that contradicts user intent.

```bash
curl -X POST "http://localhost:6333/collections/test/points/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": null,
    "limit": 5
  }'
# → HTTP 200 ✅ (WRONG — should be 4xx)
# Returns all points ordered by ID
# The null query is silently treated as "no query" instead of rejected
```

## Steps to Reproduce

1. Start Qdrant v1.18.2:
   ```bash
   docker run -p 6333:6333 qdrant/qdrant:v1.18.2
   ```

2. Create a test collection and insert data:
   ```bash
   curl -X PUT "http://localhost:6333/collections/test_qnull" \
     -H "Content-Type: application/json" \
     -d '{"vectors": {"size": 4, "distance": "Cosine"}}'

   curl -X PUT "http://localhost:6333/collections/test_qnull/points?wait=true" \
     -H "Content-Type: application/json" \
     -d '{"points": [
       {"id": 10, "vector": [0.5, 0.5, 0.5, 0.5]},
       {"id": 1,  "vector": [0.1, 0.2, 0.3, 0.4]},
       {"id": 5,  "vector": [0.3, 0.3, 0.3, 0.3]}
     ]}'
   ```

3. Query with `query=null`:
   ```bash
   curl -X POST "http://localhost:6333/collections/test_qnull/points/query" \
     -H "Content-Type: application/json" \
     -d '{"query": null, "limit": 5}'
   # Expected: 4xx — null is not a valid query
   # Actual: 200, returns [id:1, id:5, id:10] ordere

## stage2_aggregation.confirmed
endpoint=collections+{collection_name}+points
defect_type=param_validation
related_issue_numbers=[9420]

## 探针脚本
.paperpilot/phase2/probes/qdrant/probe_qdrant_9420.py
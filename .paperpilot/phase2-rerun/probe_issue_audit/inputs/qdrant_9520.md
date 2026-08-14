# qdrant_9520 (group=A, version=1.18.2)

## issue 标题
Server crash on collection creation with shard_number=INT_MAX — missing upper-bound validation unlike replication_factor

## issue body（截断 1500 字符）
## Current Behavior

When creating a collection with `shard_number` set to `2147483647` (INT_MAX), the Qdrant server becomes unresponsive and closes the connection after ~25 seconds without returning any HTTP response. The server process may crash or become unstable, requiring a restart.

This is a **Type3_RuntimeFailure**: instead of validating the input and returning a `400`/`422` error, the server attempts to allocate resources for 2+ billion shards and crashes.

## Steps to Reproduce

1. Start Qdrant v1.18.2:

```bash
docker run -p 6333:6333 qdrant/qdrant:v1.18.2
```

2. Create a collection with `shard_number=2147483647` (INT_MAX):

```bash
curl -X PUT http://localhost:6333/collections/test_shard_max \
  -H "Content-Type: application/json" \
  -d '{"vectors": {"size": 4, "distance": "Cosine"}, "shard_number": 2147483647}'
```

3. Observe the request hangs for ~25 seconds, then the connection is closed by the server:

```
curl: (52) Empty reply from server
```

4. The server is now unresponsive. Subsequent requests also fail:

```bash
curl http://localhost:6333/
# Connection refused or empty response
```

5. **Compare** with `replication_factor=0`, which is correctly validated and rejected:

```bash
curl -X PUT http://localhost:6333/collections/test_rep0 \
  -H "Content-Type: application/json" \
  -d '{"vectors": {"size": 4, "distance": "Cosine"}, "replication_factor": 0}'
```

Response (correct behavior):

```json
{
  "status": {
    "error": "Validation error in JSON bod

## stage2_aggregation.confirmed
endpoint=collections+{collection_name}
defect_type=crash
related_issue_numbers=[9520]

## 探针脚本
.paperpilot/phase2/probes/qdrant/probe_qdrant_9520.py
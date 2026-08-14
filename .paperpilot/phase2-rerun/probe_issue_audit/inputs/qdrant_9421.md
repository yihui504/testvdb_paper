# qdrant_9421 (group=A, version=1.18.2)

## issue 标题
`POST /cluster/recover` returns HTTP 500 in standalone mode — should return 4xx

## issue body（截断 1500 字符）
## Current Behavior

When calling `POST /cluster/recover` on a Qdrant instance running in **standalone** (non-distributed) mode, the API returns HTTP 500 Internal Server Error. This is incorrect — the server is not experiencing an internal error; it's running in a mode where the requested operation is not applicable.

```bash
curl -X POST "http://localhost:6333/cluster/recover"
# → HTTP 500 ❌ (WRONG — should be 4xx)
# {"status":{"error":"Service internal error: Qdrant is running in standalone mode"}}
```

The error message body is correct in describing the situation ("Qdrant is running in standalone mode"), but the **HTTP status code is wrong**. A 500-series status code indicates a server-side failure, which is misleading for an operation that simply doesn't apply in the current mode.

## Steps to Reproduce

1. Start Qdrant v1.18.2 in standalone mode (default):
   ```bash
   docker run -p 6333:6333 qdrant/qdrant:v1.18.2
   ```

2. Call the cluster recover endpoint:
   ```bash
   curl -X POST "http://localhost:6333/cluster/recover" -i
   # → HTTP/1.1 500 Internal Server Error
   # {"status":{"error":"Service internal error: Qdrant is running in standalone mode"},"time":0.000135}
   ```

3. Verify the instance is not distributed:
   ```bash
   curl "http://localhost:6333/cluster"
   # → {"result":{"status":"disabled"},"status":"ok","time":0.0}
   ```

### MRE Script

```python
#!/usr/bin/env python3
"""MRE: POST /cluster/recover returns 500 in standalone mode on Qdrant v1.18.2"

## stage2_aggregation.confirmed
endpoint=cluster+recover
defect_type=behavior
related_issue_numbers=[9421]

## 探针脚本
.paperpilot/phase2/probes/qdrant/probe_qdrant_9421.py
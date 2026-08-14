# milvus_49930 (group=B, version=2.6.16)

## issue 标题
[Bug]: REST API v2 accepts invalid searchParams (ef=0/-1 for HNSW, nprobe=0/-1 for IVF_FLAT) without validation

## issue body（截断 1500 字符）
### Is there an existing issue for this?

- [x] I have searched the existing issues

### Environment

```markdown
- Milvus version: v2.6.16
- Deployment mode(standalone or cluster): standalone
- MQ type(rocksmq, pulsar or kafka): rocksmq
- SDK version(e.g. pymilvus v2.0.0rc2): REST API v2
- OS(Ubuntu or CentOS): Docker on Windows
- CPU/Memory: N/A
- GPU: N/A
- Others: Reproduced via Milvus REST API v2
```

### Current Behavior

The REST API v2 accepts invalid `searchParams` values for HNSW and IVF_FLAT indexes without validation. Specifically:

1. **HNSW `ef` parameter**: Values of `0` and `-1` are accepted in search requests, despite being semantically invalid. The `ef` parameter controls the search width in HNSW — a value of `0` or negative means "search zero nodes", which should be rejected.

2. **IVF_FLAT `nprobe` parameter**: Values of `0` and `-1` are accepted (as also reported in #49823 for AUTOINDEX).

This is a **systematic parameter validation gap** in the REST API v2 search endpoint — `searchParams` are passed through to the search engine without any range validation, while other parameters like `limit` (topk) and `offset` are properly validated.

**Verified on v2.6.16:**

```python
import requests
BASE = 'http://localhost:19530'
HEADERS = {'Authorization': 'Bearer root:Milvus', 'Content-Type': 'application/json'}

# === HNSW ef validation gap ===
# Create HNSW collection
requests.post(f'{BASE}/v2/vectordb/collections/create', headers=HEADERS, json={
    "collectio

## stage2_aggregation.confirmed
endpoint=collections+create
defect_type=param_validation
related_issue_numbers=[49930]

## 探针脚本
.paperpilot/phase2/probes/milvus/probe_milvus_49930.py
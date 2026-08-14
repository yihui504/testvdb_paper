# milvus_49928 (group=C, version=2.6.16)

## issue 标题
[Bug]: Default proxy.maxDimension=32768 is too permissive, potential DoS risk via high-dimensional collection creation

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
- CPU/Memory: 8GB RAM
- GPU: N/A
- Others: Reproduced via Milvus REST API v2
```

### Current Behavior

The default `proxy.maxDimension` is set to **32768**, which allows creating collections with extremely high-dimensional vectors. While the dimension validation itself works correctly (rejects values outside the 2~32768 range), the default upper bound is too permissive and creates a **Denial of Service (DoS) risk** in multi-tenant or resource-constrained environments.

**Verified on v2.6.16:**

```python
import requests
BASE = 'http://localhost:19530'
HEADERS = {'Authorization': 'Bearer root:Milvus', 'Content-Type': 'application/json'}

# dim=32768 → ACCEPTED (within default range)
r = requests.post(f'{BASE}/v2/vectordb/collections/create', headers=HEADERS, json={
    "collectionName": "test_large_dim",
    "schema": {"autoID": False, "enableDynamicField": True, "fields": [
        {"fieldName": "id", "dataType": "Int64", "isPrimary": True},
        {"fieldName": "vector", "dataType": "FloatVector", "elementTypeParams": {"dim": 32768}}
    ]}
})
print(r.json())  # {"code": 0, "data": {}} — succeeds!

# dim=32769 → correctly REJECTED
# {"code": 65535

## stage2_aggregation.confirmed
endpoint=collections+create
defect_type=behavior
related_issue_numbers=[49928]

## 探针脚本
.paperpilot/phase2/probes/milvus/probe_milvus_49928.py
# milvus_49929 (group=C, version=2.6.16)

## issue 标题
[Bug]: REST API and PyMilvus SDK have inconsistent default index creation behavior

## issue body（截断 1500 字符）
### Is there an existing issue for this?

- [x] I have searched the existing issues

### Environment

```markdown
- Milvus version: v2.6.16
- Deployment mode(standalone or cluster): standalone
- MQ type(rocksmq, pulsar or kafka): rocksmq
- SDK version(e.g. pymilvus v2.0.0rc2): REST API v2 + PyMilvus SDK
- OS(Ubuntu or CentOS): Docker on Windows
- CPU/Memory: N/A
- GPU: N/A
- Others: Reproduced with both REST API v2 and PyMilvus SDK
```

### Current Behavior

The REST API v2 and PyMilvus SDK have **inconsistent default behaviors** when creating a collection:

1. **REST API** `POST /v2/vectordb/collections/create` **without `indexParams`**: Creates a collection **without any index**. A subsequent `create_index` call succeeds because no index exists yet.

2. **PyMilvus SDK** `client.create_collection(collection_name, dimension=4)`: Creates a collection **with a default AUTOINDEX automatically**. A subsequent `client.create_index()` call **fails** because an index already exists on the vector field.

This behavioral difference means the same logical operation (create collection → create index) produces different outcomes depending on which API is used, which can confuse users and break cross-API compatibility.

### Verification on v2.6.16

**REST API — create_index succeeds:**
```python
import requests
BASE = 'http://localhost:19530'
HEADERS = {'Authorization': 'Bearer root:Milvus', 'Content-Type': 'application/json'}

# Create collection WITHOUT indexParams
requests.post(f'{BASE

## stage2_aggregation.confirmed
endpoint=entities+insert
defect_type=behavior
related_issue_numbers=[49929]

## 探针脚本
.paperpilot/phase2/probes/milvus/probe_milvus_49929.py
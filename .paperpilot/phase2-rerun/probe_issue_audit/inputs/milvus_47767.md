# milvus_47767 (group=C, version=2.6.10)

## issue 标题
[Bug]: Empty query vector accepted in search - no validation error

## issue body（截断 1500 字符）
### Is there an existing issue for this?

- [x] I have searched the existing issues

### Environment

```markdown
- Milvus version: v2.6.10
- Deployment mode(standalone or cluster): Standalone
- MQ type(rocksmq, pulsar or kafka): rocksmq
- SDK version(e.g. pymilvus v2.0.0rc2): PyMilvus v2.6.10
- OS(Ubuntu or CentOS): Windows (Client) / Linux (Server)
- CPU/Memory: N/A
- GPU: N/A
- Others: Docker Compose deployment
```

### Current Behavior

Milvus v2.6.10 accepts an empty query vector `[]` when performing search operations, which violates the documented requirement that vector dimensions must be greater than zero and query vectors must match the collection dimension.

### Expected Behavior

Search should fail with a clear error message indicating that query vector cannot be empty and must match the collection dimension.

Example expected error:
```
<ParamError: (code=1100, message=Invalid search parameter 'query_vector': vector cannot be empty, expected dimension 2)>
```

### Steps To Reproduce

```markdown
1. Create a collection with vector field (dimension > 0)
2. Insert test data into collection
3. Create index and load collection
4. Attempt to search with empty query vector `[]`
5. Observe that search s**Complete Reproduction Script:**

from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility

# Connect to Milvus
connections.connect(alias="default", host="localhost", port="19530")

def cleanup_collection(collection_name):
    """Clean

## stage2_aggregation.confirmed
endpoint=databases+drop
defect_type=behavior
related_issue_numbers=[47767]

## 探针脚本
.paperpilot/phase2/probes/milvus/probe_milvus_47767.py
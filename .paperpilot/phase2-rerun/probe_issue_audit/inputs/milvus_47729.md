# milvus_47729 (group=B, version=2.6.10)

## issue 标题
[Bug]: Index parameter nprobe validation missing - accepts nprobe=0

## issue body（截断 1500 字符）
### Is there an existing issue for this?

- [x] I have searched the existing issues

### Environment

```markdown
- Milvus version:v2.6.10
- Deployment mode(standalone or cluster):Standalone
- MQ type(rocksmq, pulsar or kafka):rocksmq
- SDK version(e.g. pymilvus v2.0.0rc2):PyMilvus v2.6.10
- OS(Ubuntu or CentOS): Windows (Client) / Linux (Server)
- CPU/Memory:N/A 
- GPU:N/A 
- Others: Docker Compose deployment
```

### Current Behavior

Milvus v2.6.10 accepts `nprobe=0` when searching with IVF indexes (IVF_FLAT, IVF_PQ, IVF_SQ8, SCANN, BIN_IVF_FLAT), which violates the documented requirement that `nprobe` must be a positive integer (> 0).

### Expected Behavior

Search should fail with a clear error message indicating that `nprobe` must be a positive integer greater than 0.

Example expected error:
```
<ParamError: (code=1100, message=Invalid search parameter 'nprobe': value must be greater than 0, but got 0)>
```

### Steps To Reproduce

```markdown
1. Create a collection with vector field
2. Insert test data into collection
3. Create an IVF index with valid `nlist` parameter
4. Attempt to search with `nprobe=0`
5. Observe that search succeeds (should fail)
**Complete Reproduction Script:**

from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility

# Connect to Milvus
connections.connect(alias="default", host="localhost", port="19530")

def cleanup_collection(collection_name):
    """Clean up existing collection"""
    if utility.has_col

## stage2_aggregation.confirmed
endpoint=entities+search
defect_type=param_validation
related_issue_numbers=[47729]

## 探针脚本
.paperpilot/phase2/probes/milvus/probe_milvus_47729.py
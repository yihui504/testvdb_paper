# milvus_47752 (group=B, version=2.6.10)

## issue 标题
[Bug]: Index parameter ef validation missing - accepts ef=0

## issue body（截断 1500 字符）
### Is there an existing issue for this?

- [x] I have searched the existing issues

### Environment

```markdown
- Milvus version: v2.6.10
- Deployment mode(standalone or cluster):Standalone
- MQ type(rocksmq, pulsar or kafka):rocksmq
- SDK version(e.g. pymilvus v2.0.0rc2):PyMilvus v2.6.10
- OS(Ubuntu or CentOS): Windows (Client) / Linux (Server)
- CPU/Memory: N/A
- GPU: N/A
- Others: Docker Compose deployment
```

### Current Behavior

Milvus v2.6.10 accepts `ef=0` when searching with HNSW indexes (HNSW, HNSW_PQ, HNSW_SQ, HNSW_PRQ), which violates the documented requirement that `ef` must be a positive integer (> 0).

### Expected Behavior

Search should fail with a clear error message indicating that `ef` must be a positive integer greater than 0.

Example expected error:
```
<ParamError: (code=1100, message=Invalid search parameter 'ef': value must be greater than 0, but got 0)>
```

### Steps To Reproduce

```markdown
1. Create a collection with vector field
2. Insert test data into collection
3. Create an HNSW index with valid parameters
4. Attempt to search with `ef=0`
5. Observe that search succeeds (should fail)


from pymilvus import MilvusClient

client = MilvusClient(uri="http://localhost:19530")
collection_name = "test_hnsw_ef_0"

# Create collection and index
client.create_collection(
    collection_name=collection_name,
    dimension=128,
    metric_type="L2"
)
client.insert(collection_name=collection_name, data=[{"vector": [0.1]*128, "id": 1}])

# Create HNSW 

## stage2_aggregation.confirmed
endpoint=entities+search
defect_type=param_validation
related_issue_numbers=[47752]

## 探针脚本
.paperpilot/phase2/probes/milvus/probe_milvus_47752.py
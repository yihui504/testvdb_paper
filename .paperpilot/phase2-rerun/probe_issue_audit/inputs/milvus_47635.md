# milvus_47635 (group=B, version=2.3)

## issue 标题
[Bug]: Search fails with Code 0 immediately after Collection.load() returns success

## issue body（截断 1500 字符）
### Is there an existing issue for this?

- [x] I have searched the existing issues

### Environment

```markdown
- Milvus version:v2.3.x
- Deployment mode(standalone or cluster):Standalone (also affects Distributed)
- MQ type(rocksmq, pulsar or kafka):rocksmq
- SDK version(e.g. pymilvus v2.0.0rc2):PyMilvus v2.3.x
- OS(Ubuntu or CentOS): Windows (Client) / Linux (Server)
- CPU/Memory: N/A
- GPU: N/A
- Others: Docker Compose deployment
```

### Current Behavior

When calling `collection.search()` immediately after `collection.load()` returns success, the operation fails with `MilvusException: (code=0, message=collection not loaded)`. This indicates a race condition between the `QueryCoord` acknowledging the load and the `QueryNode` finishing shard leader election or view publication.

The error code `0` is defined as **Success** in the Milvus API specification, but the operation actually fails. This violates the API contract and prevents robust error handling in client applications.

### Error Message
```
<MilvusException: (code=0, message=attempt #0: fail to get shard leaders from QueryCoord: collection=464083723551487556: collection not loaded: unrecoverable error: fail to search on all shard leaders)>
```

### Expected Behavior

`collection.load()` should only return success when the collection is actually ready to serve requests, or `search()` should internally retry/wait if the collection is in the process of becoming ready. The error code should be a proper error code (e

## stage2_aggregation.confirmed
endpoint=entities+search
defect_type=behavior
related_issue_numbers=[47635]

## 探针脚本
.paperpilot/phase2/probes/milvus/probe_milvus_47635.py
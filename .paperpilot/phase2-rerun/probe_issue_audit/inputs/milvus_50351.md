# milvus_50351 (group=C, version=2.6.17)

## issue 标题
[Bug]: REST API v2: shardsNum=0/-1/65535 accepted with HTTP 200 + code=200

## issue body（截断 1500 字符）
### Is there an existing issue for this?

- [x] I have searched the existing issues

### Environment

```markdown
- Milvus version: v2.6.17
- Deployment mode: standalone (Docker)
- MQ type: rocksmq (standalone default)
- SDK version: REST API v2 (/v2/vectordb)
- OS: Windows 11 (Docker Desktop)
- Others: Verified on fresh install
```

### Current Behavior


The `POST /v2/vectordb/collections/create` endpoint accepts out-of-range `shardsNum` values (0, -1, 65535) and returns **both HTTP 200 AND JSON code=200 (success)**. This is a dual-layer protocol violation: the API claims success at both the HTTP transport layer and the application message layer, but creates a collection with undefined shard behavior.

**shardsNum=0** (minimum is documented as 1):
```bash
curl -s -X POST 'http://localhost:19530/v2/vectordb/collections/create' \
  -H 'Content-Type: application/json' \
  -d '{"collectionName":"test_shard_0","dimension":4,"shardsNum":0,"metricType":"L2"}'

# Response: {"code":200,"data":{}}   ← code=200 means SUCCESS!
```

**shardsNum=-1** (negative value):
```bash
curl -s -X POST 'http://localhost:19530/v2/vectordb/collections/create' \
  -H 'Content-Type: application/json' \
  -d '{"collectionName":"test_shard_neg","dimension":4,"shardsNum":-1,"metricType":"L2"}'

# Response: {"code":200,"data":{}}   ← code=200 means SUCCESS!
```

**shardsNum=65535** (potentially resource-exhausting):
```bash
curl -s -X POST 'http://localhost:19530/v2/vectordb/collections/create' \
  -H 'Con

## stage2_aggregation.confirmed
endpoint=collections+create
defect_type=param_validation
related_issue_numbers=[50351]

## 探针脚本
.paperpilot/phase2/probes/milvus/probe_milvus_50351.py
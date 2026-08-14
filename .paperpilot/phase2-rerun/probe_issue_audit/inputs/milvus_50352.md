# milvus_50352 (group=C, version=2.6.17)

## issue 标题
[Bug]: REST API v2: metricType="" and consistencyLevel="None" silently accepted on collections/create

## issue body（截断 1500 字符）
### Is there an existing issue for this?

- [x] I have searched the existing issues

### Environment

```markdown
- Milvus version: v2.6.17
- Deployment mode(standalone or cluster): standalone (Docker)
- MQ type(rocksmq, pulsar or kafka): rocksmq (standalone default)
- SDK version(e.g. pymilvus v2.0.0rc2): REST API v2 (/v2/vectordb)
- OS(Ubuntu or CentOS): Windows 11 (Docker Desktop)
- CPU/Memory: N/A
- GPU: N/A
- Others:
```

### Current Behavior

The `POST /v2/vectordb/collections/create` endpoint has **multiple parameter validation gaps** across dimension, metricType, and consistencyLevel. All invalid inputs return HTTP 200 instead of HTTP 4xx.

#### 1. dimension boundary values accepted with HTTP 200

| Test Value | HTTP Status | JSON code | Message |
|-----------|------------|-----------|---------|
| dimension=0 | **200** | 1100 | "dimension is required..." (misleading: treats 0 as missing) |
| dimension=-1 | **200** | 65535 | "should be in range 2 ~ 32768" |
| dimension=32769 | **200** | 65535 | "should be in range 2 ~ 32768" |

Documented valid range: 1 ~ 32768

```bash
curl -s -X POST 'http://localhost:19530/v2/vectordb/collections/create' \
  -H 'Content-Type: application/json' \
  -d '{"collectionName":"test_dim_0","dimension":0,"metricType":"COSINE"}'
# HTTP 200 / {"code":1100,"message":"dimension is required..."}
```

#### 2. metricType enum violations accepted with HTTP 200

| Test Value | HTTP Status | JSON code | Behavior |
|-----------|------------|-----------

## stage2_aggregation.confirmed
endpoint=collections+create
defect_type=param_validation
related_issue_numbers=[50352]

## 探针脚本
.paperpilot/phase2/probes/milvus/probe_milvus_50352.py
# milvus_50353 (group=B, version=2.6.17)

## issue 标题
[Bug]: REST API v2: search returns HTTP 200 for limit=0/-1 and dimension mismatch

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

`POST /v2/vectordb/entities/search` returns HTTP 200 for all invalid parameter values, placing error information only in the JSON body.

#### 1. limit (topK) boundary values

| limit | HTTP | code | Message |
|-------|------|------|---------|
| 0 | 200 | 65535 | "topk [0] is invalid, should be in range [1, 16384]" |
| -1 | 200 | 65535 | "topk [-1] is invalid" |
| -100 | 200 | 65535 | "topk [-100] is invalid" |

```bash
curl -s -X POST 'http://localhost:19530/v2/vectordb/entities/search' \
  -H 'Content-Type: application/json' \
  -d '{"collectionName":"test","data":[[1,2,3,4]],"limit":0}'
# HTTP 200 / {"code":65535,"message":"topk [0] is invalid..."}
```

#### 2. Vector dimension mismatch (collection dim=4)

| Vector dim | HTTP | code | Message |
|-----------|------|------|---------|
| 64 | 200 | 1801 | "dimension: 4, but length of []float: 64" |
| 128 | 200 | 1801 | "dimension: 4, but length of []float: 128" |
| 2 | 200 | 1801 | "dimension: 4, but length of []float: 2" |

**Note**: Earlier versions (pre-v2.6) reported "length of [

## stage2_aggregation.confirmed
endpoint=entities+search
defect_type=behavior
related_issue_numbers=[50353]

## 探针脚本
.paperpilot/phase2/probes/milvus/probe_milvus_50353.py
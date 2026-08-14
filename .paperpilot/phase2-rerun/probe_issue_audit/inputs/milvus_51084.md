# milvus_51084 (group=A, version=2.6.19)

## issue 标题
[Bug]: REST API silently substitutes invalid `consistencyLevel` enum value with default instead of rejecting

## issue body（截断 1500 字符）
### Is there an existing issue for this?

- [x] I have searched the existing issues

### Environment

```markdown
- Milvus version: **v2.6.19** (also reproduced on v2.6.17 image)
- Deployment mode: standalone (Docker Compose, official `milvusdb/milvus:v2.6.19`)
- MQ type: rocksmq (default for standalone)
- SDK version: N/A — reproduced via raw HTTP/REST (`curl` + Python `urllib`)
- OS: Windows 11 (Docker Desktop); Milvus container runs Linux
- CPU/Memory: host 8 vCPU / 16 GB; container default
- GPU: none
- Others: REST endpoint `POST /v2/vectordb/collections/create`
```

### Current Behavior


When creating a collection via the REST API with an **invalid `consistencyLevel` enum string** (e.g. `"Invalid"`), Milvus returns `200 OK` with `code: 0` (success) and **silently substitutes the default value `Bounded`**, rather than rejecting the request.

The client has no way to know their input was invalid — `describe` later returns `"Bounded"`, masking the typo/bug in the client.

```http
POST /v2/vectordb/collections/create
{"collectionName":"audit1","dimension":4,"metricType":"L2","idType":"Int64","autoID":true,"vectorFieldType":"FloatVector","consistencyLevel":"Invalid"}

HTTP/1.1 200 OK
{"code":0,"data":{}}

POST /v2/vectordb/collections/describe
{"collectionName":"audit1"}

HTTP/1.1 200 OK
{"code":0,"data":{ ..., "consistencyLevel":"Bounded", ...}}
```


### Expected Behavior


Return a non-success response (HTTP 4xx, or HTTP 200 with `code != 0`) with a clear error message s

## stage2_aggregation.confirmed
endpoint=collections+create
defect_type=semantics
related_issue_numbers=[51084]

## 探针脚本
.paperpilot/phase2/probes/milvus/probe_milvus_51084.py
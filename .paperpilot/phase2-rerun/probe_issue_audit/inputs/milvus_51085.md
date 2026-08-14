# milvus_51085 (group=A, version=2.6.19)

## issue 标题
[Bug]: REST API silently substitutes invalid `vectorFieldType` enum value with default instead of rejecting

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


When creating a collection via the REST API with an **invalid `vectorFieldType` enum string** (e.g. `"InvalidVectorType"`), Milvus returns `200 OK` with `code: 0` (success) and **silently substitutes the default `FloatVector`**, rather than rejecting the request.

The client has no way to know their input was invalid — the collection is created with a vector field of type `FloatVector`, masking the typo/bug in the client.

```http
POST /v2/vectordb/collections/create
{"collectionName":"audit5","dimension":4,"metricType":"L2","idType":"Int64","autoID":true,"vectorFieldType":"InvalidVectorType"}

HTTP/1.1 200 OK
{"code":0,"data":{}}

POST /v2/vectordb/collections/describe
{"collectionName":"audit5"}

HTTP/1.1 200 OK
{"code":0,"data":{"fields":[
  {"name":"id","type":"Int64","primaryKey":true},
  {"name":"vector","type":"FloatVector", ...}
]}}
```


### Expected Behavior


Return a non-su

## stage2_aggregation.confirmed
endpoint=entities+insert
defect_type=semantics
related_issue_numbers=[51085]

## 探针脚本
.paperpilot/phase2/probes/milvus/probe_milvus_51085.py
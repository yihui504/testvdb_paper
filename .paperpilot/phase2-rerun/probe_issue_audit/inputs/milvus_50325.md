# milvus_50325 (group=C, version=2.6.17)

## issue 标题
[Bug]: Collection names with leading underscore accepted despite naming rules

## issue body（截断 1500 字符）
### Is there an existing issue for this?

- [x] I have searched the existing issues

### Environment

```markdown
- Milvus version: v2.6.17
- Deployment mode: standalone (Docker)
- MQ type: rocksmq (standalone default)
- SDK version: REST API (v2/vectordb)
- OS: Windows 11 (Docker Desktop)
- CPU/Memory: Docker default
- GPU: None
- Others: Fresh install, no prior data
```

### Current Behavior


Collection names starting with an **underscore** (e.g., `_test_collection`) are accepted with `code=0`. According to discussion #19273 and naming conventions, collection names should match `[a-zA-Z][a-zA-Z0-9_]*` — starting with a letter.

Note: Unicode-only names (e.g., Chinese characters) are **correctly rejected** with code=1100 in v2.6.17. This issue is specifically about leading underscores.

```
POST /v2/vectordb/collections/create
{"collectionName": "_test_underscore", "dimension": 128, "metricType": "COSINE"}

Response: {"code": 0, "data": {}}
```


### Expected Behavior

Return validation error for names starting with underscore, consistent with the naming convention `[a-zA-Z][a-zA-Z0-9_]*`.


### Steps To Reproduce

```markdown
import requests
r = requests.post("http://localhost:19530/v2/vectordb/collections/create",
    json={"collectionName": "_test_collection", "dimension": 128, "metricType": "COSINE"},
    headers={"Content-Type": "application/json"})
print(r.json())  # {"code": 0, "data": {}} ← BUG
```

### Milvus Log

```
No error or warning generated.
```


### Anythi

## stage2_aggregation.confirmed
endpoint=collections+list
defect_type=param_validation
related_issue_numbers=[50325]

## 探针脚本
.paperpilot/phase2/probes/milvus/probe_milvus_50325.py
# weaviate_12041 (group=A, version=1.38.2)

## issue 标题
Batch delete returns HTTP 500 instead of 422 when match.where or match.class is missing

## issue body（截断 1500 字符）
### How to reproduce this bug?


Clean weaviate v1.38.2 container, default config. Create any class, then send a batch delete missing a required field:

```bash
# Setup
curl -X POST "http://localhost:8080/v1/schema" \
  -H "Content-Type: application/json" \
  -d '{"class":"BoundaryTestBatchDelete","vectorizer":"none",
       "properties":[{"name":"title","dataType":["text"]}]}'
```

**Case A — `match.class` present, `match.where` absent** (docs mark `where` as required):

```bash
curl -X DELETE "http://localhost:8080/v1/batch/objects" \
  -H "Content-Type: application/json" \
  -d '{"match":{"class":"BoundaryTestBatchDelete"},"output":"minimal"}'
```

**Case B — empty `match` object** (both required fields absent):

```bash
curl -X DELETE "http://localhost:8080/v1/batch/objects" \
  -H "Content-Type: application/json" \
  -d '{"match":{},"output":"minimal"}'
```

---

### What is the expected behavior?


Per the [batch delete docs](https://weaviate.io/developers/weaviate/api/rest/batch#delete-objects), both `match.class` and `match.where` are listed as **required** fields:

```
"match": {
  "class": "<ClassName>",   # required
  "where": { ... },         # required
}
```

A missing required field is a client-side validation error, so the server should return **`422 Unprocessable Entity`** (or `400`) with the same message body — consistent with how weaviate handles other invalid request bodies elsewhere in the batch endpoint.

---


### What is the actual behavior?


Both case

## stage2_aggregation.confirmed
endpoint=DELETE /batch/objects
defect_type=behavior
related_issue_numbers=[12041]

## 探针脚本
.paperpilot/phase2/probes/weaviate/probe_weaviate_12041.py
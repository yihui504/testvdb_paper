# weaviate_11732 (group=A, version=1.38.0)

## issue 标题
vectorIndexConfig.distance silently accepts null and defaults to cosine

## issue body（截断 1500 字符）
### How to reproduce this bug?


```bash
# Docker setup (only first time)
docker run -d --name weaviate-test \
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
  -e DEFAULT_VECTORIZER_MODULE=none \
  -p 8080:8080 \
  semitechnologies/weaviate:1.38.0

# Wait for startup
sleep 5

# Create a class with distance set to null
curl -s -X POST http://localhost:8080/v1/schema \
  -H "Content-Type: application/json" \
  -d '{
    "class": "TestClass",
    "vectorizer": "none",
    "vectorIndexConfig": {
      "distance": null
    }
  }'

# Expected: 422 validation error
# Actual: 200 OK - class created with distance silently set to "cosine"
```


### What is the expected behavior?

The `distance` field must be a valid distance metric. According to the official Weaviate documentation on [Distance Metrics](https://docs.weaviate.io/weaviate/config-refs/distances), only 5 values are valid:

> cosine, dot, l2-squared, hamming, manhattan

The server's own error message for other invalid distance values confirms this list:

> "unrecognized distance metric, choose one of [cosine, dot, l2-squared, manhattan, hamming]"

`null` is not a valid distance metric. Weaviate should reject it with HTTP 422 and a message like:

> "vectorIndexConfig.distance must be one of: cosine, dot, l2-squared, manhattan, hamming"

### What is the actual behavior?


Weaviate accepts `null` distance and returns HTTP 200, silently defaulting to `"cosine"` without warning:

```json
{
  "class": "TestClass",
  "vectorIn

## stage2_aggregation.confirmed
endpoint=/schema
defect_type=type_coercion
related_issue_numbers=[11732]

## 探针脚本
.paperpilot/phase2/probes/weaviate/probe_weaviate_11732.py
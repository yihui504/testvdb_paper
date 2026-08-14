# weaviate_11730 (group=A, version=1.38.0)

## issue 标题
tokenization accepts empty string despite explicit OpenAPI enum constraint

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

# Create a class with tokenization set to empty string ""
curl -s -X POST http://localhost:8080/v1/schema \
  -H "Content-Type: application/json" \
  -d '{
    "class": "TestClass",
    "vectorizer": "none",
    "properties": [
      {
        "name": "text_field",
        "dataType": ["text"],
        "tokenization": ""
      }
    ]
  }'

# Expected: 422 validation error
# Actual: 200 OK - class created with empty tokenization
```


### What is the expected behavior?


The `tokenization` field should only accept values from its documented enum. According to the OpenAPI specification ([schema.json](https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json)), the `Property.tokenization` field has an explicit `enum` constraint:

```json
"tokenization": {
  "description": "Which tokenizer is used, if not set, this is inferred from the data type.",
  "type": "string",
  "enum": [
    "word",
    "lowercase",
    "whitespace",
    "field",
    "trigram",
    "gse",
    "kagome_kr",
    "kagome_ja",
    "gse_ch"
  ]
}
```

An empty string `""` is not a member of this enum. Weaviate should reject it with HTTP 422 and a message like:

> "tokenization must be one of: word, lowercase, white

## stage2_aggregation.confirmed
endpoint=POST /schema
defect_type=param_validation
related_issue_numbers=[11730]

## 探针脚本
.paperpilot/phase2/probes/weaviate/probe_weaviate_11730.py
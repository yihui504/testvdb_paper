# weaviate_11436 (group=C, version=1.37.4)

## issue 标题
Negative `ef` value (-1) accepted in vectorIndexConfig without validation error

## issue body（截断 1500 字符）
### How to reproduce this bug?


1. Start Weaviate v1.37.4 with anonymous access:
   ```bash
   docker run -p 8080:8080 -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true -e DEFAULT_VECTORIZER_MODULE=none semitechnologies/weaviate:1.37.4
   ```

2. Create a collection with `ef=-1` in vectorIndexConfig:
   ```bash
   curl -X POST http://localhost:8080/v1/schema \
     -H 'Content-Type: application/json' \
     -d '{
       "class": "TestEfneg",
       "vectorizer": "none",
       "vectorIndexConfig": {
         "distance": "cosine",
         "ef": -1
       },
       "properties": [{"name": "text", "dataType": ["text"]}]
     }'
   ```

3. Observe that the request succeeds with HTTP 200 and the collection is created.

### What is the expected behavior?

The server should reject `ef=-1` with a 422 Unprocessable Entity response and a clear validation error message. The `ef` parameter in HNSW controls the size of the dynamic list for the nearest neighbors during search — it must be a positive integer. Negative values have no valid semantic interpretation in the HNSW algorithm and should be caught during schema validation.

### What is the actual behavior?

The server accepts `ef=-1` without error, creating a collection with an invalid configuration. This could lead to undefined behavior during search operations.


### Supporting information


Similar validation gaps may exist for other HNSW parameters:
- `maxConnections=0` is also accepted (though `0` is at least non-negative)
- `bq

## stage2_aggregation.confirmed
endpoint=/schema
defect_type=param_validation
related_issue_numbers=[11436]

## 探针脚本
.paperpilot/phase2/probes/weaviate/probe_weaviate_11436.py
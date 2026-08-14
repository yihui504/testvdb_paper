# weaviate_11981 (group=C, version=1.38.2)

## issue 标题
POST /v1/batch/objects accepts empty vector `[]` and reports per-item SUCCESS (singular POST /v1/objects rejects with 422)

## issue body（截断 1500 字符）
### How to reproduce this bug?


```bash
# 1. Start Weaviate v1.38.2 (single node, anonymous access, no vectorizer module)
docker run -d --name weaviate-batch-vector-bug \
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
  -e DEFAULT_VECTORIZER_MODULE=none \
  -e PERSISTENCE_DATA_PATH=/var/lib/weaviate \
  -p 8080:8080 \
  semitechnologies/weaviate:1.38.2

# Wait for startup
sleep 8

# 2. Create a class (vectorizer=none, distance=cosine, dimension implied by first vector)
curl -s -o /dev/null -w "create class: %{http_code}\n" -X POST http://localhost:8080/v1/schema \
  -H "Content-Type: application/json" \
  -d '{
    "class": "BatchVectorBugRepro",
    "vectorizer": "none",
    "vectorIndexType": "hnsw",
    "vectorIndexConfig": {"distance": "cosine"}
  }'

# 3. CONTROL: singular POST /v1/objects with vector=[] correctly returns 422
curl -s -o /dev/null -w "singular POST /v1/objects with vector=[]: %{http_code}\n" -X POST http://localhost:8080/v1/objects \
  -H "Content-Type: application/json" \
  -d '{
    "class": "BatchVectorBugRepro",
    "properties": {"name": "control-singular"},
    "vector": []
  }'
# Expected output: singular POST /v1/objects with vector=[]: 422

# 4. BUG: POST /v1/batch/objects with a mixed batch (valid item + empty-vector item) returns 200,
#    and BOTH items report per-item "result.status": "SUCCESS"
curl -s -X POST http://localhost:8080/v1/batch/objects \
  -H "Content-Type: application/json" \
  -d '{
    "objects": [
      {
        "class

## stage2_aggregation.confirmed
endpoint=POST /batch/objects
defect_type=behavior
related_issue_numbers=[11981]

## 探针脚本
.paperpilot/phase2/probes/weaviate/probe_weaviate_11981.py
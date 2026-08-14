# weaviate_11729 (group=A, version=1.38.0)

## issue 标题
shardingConfig.desiredCount accepts negative values but rejects zero

## issue body（截断 1500 字符）
### How to reproduce this bug?


```bash
# Setup
docker run -d --name weaviate-test \
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
  -e PERSISTENCE_DATA_PATH=/var/lib/weaviate \
  -p 8080:8080 \
  semitechnologies/weaviate:1.38.0

sleep 15

# Test case 1: desiredCount=0 IS rejected (control)
curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:8080/v1/schema \
  -H "Content-Type: application/json" \
  -d '{"class":"TestZero","shardingConfig":{"desiredCount":0}}'
# Returns: 422

# Test case 2: desiredCount=-1 is NOT rejected (the bug)
curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:8080/v1/schema \
  -H "Content-Type: application/json" \
  -d '{"class":"TestNeg","shardingConfig":{"desiredCount":-1}}'
# Returns: 200 (bug!)

# Cleanup
docker rm -f weaviate-test
```

### What is the expected behavior?

Weaviate should reject ALL non-positive `desiredCount` values consistently. A shard count must be a positive integer (>=1). Weaviate already validates `desiredCount=0` and rejects it with 422, proving this field is validated. The same validation should reject `-1`, `-100`, and any other non-positive value.

### What is the actual behavior?


Weaviate inconsistently accepts `desiredCount=-1` (returns 200 and creates the schema) while rejecting `desiredCount=0` (returns 422). Both values are equally invalid for a shard count, but only one is rejected. A negative shard count is logically impossible and leads to undefined behavior during vector indexin

## stage2_aggregation.confirmed
endpoint=POST /schema
defect_type=param_validation
related_issue_numbers=[11729]

## 探针脚本
.paperpilot/phase2/probes/weaviate/probe_weaviate_11729.py
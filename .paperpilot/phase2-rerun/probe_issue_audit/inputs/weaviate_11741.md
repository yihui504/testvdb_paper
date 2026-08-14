# weaviate_11741 (group=A, version=1.38.0)

## issue 标题
Tenant creation accepts empty string for activityStatus

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

# Step 1: Create a class with multi-tenancy enabled
curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:8080/v1/schema \
  -H "Content-Type: application/json" \
  -d '{"class":"TestTenant","multiTenancyConfig":{"enabled":true}}'
# Returns: 200

# Test case 1: Valid activityStatus "ACTIVE" works (control)
curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:8080/v1/schema/TestTenant/tenants \
  -H "Content-Type: application/json" \
  -d '[{"name":"tenant_valid","activityStatus":"ACTIVE"}]'
# Returns: 200

# Test case 2: activityStatus="" (empty string) is NOT rejected (the bug)
curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:8080/v1/schema/TestTenant/tenants \
  -H "Content-Type: application/json" \
  -d '[{"name":"tenant_empty","activityStatus":""}]'
# Returns: 200 (bug!)

# Cleanup
docker rm -f weaviate-test
```

### What is the expected behavior?


The `activityStatus` field for tenant creation is an enum with exactly two valid values: `"ACTIVE"` and `"INACTIVE"`. An empty string `""` is neither. Weaviate should reject it with 422 at tenant creation time. The OpenAPI schema for the tenant creation endpoint defines `activityStatus` as an enum type, and an empty string violates the enum constra

## stage2_aggregation.confirmed
endpoint=/schema/{className}/tenants
defect_type=param_validation
related_issue_numbers=[11741]

## 探针脚本
.paperpilot/phase2/probes/weaviate/probe_weaviate_11741.py
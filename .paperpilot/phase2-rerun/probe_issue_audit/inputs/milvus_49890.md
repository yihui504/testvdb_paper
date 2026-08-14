# milvus_49890 (group=A, version=2.6.16)

## issue 标题
[Bug]: REST API v2 accepts non-integer `Request-Timeout` header values

## issue body（截断 1500 字符）
### Is there an existing issue for this?

- [x] I have searched the existing issues

### Environment

```markdown
- Milvus version: v2.6.16
- Deployment mode(standalone or cluster): standalone
- MQ type(rocksmq, pulsar or kafka): rocksmq
- SDK version(e.g. pymilvus v2.0.0rc2): REST API v2 (via curl)
- OS(Ubuntu or CentOS): Docker on Windows
- CPU/Memory: N/A
- GPU: N/A
- Others: Reproduced via Milvus REST API v2
```

### Current Behavior

The Milvus v2 REST API accepts `Request-Timeout` header values that are not integers, violating the documented type constraint. Both float values (e.g., `3.5`) and string values (e.g., `"abc"`) are accepted without validation, returning `code: 0` (success) instead of a type error.

The `Request-Timeout` header is documented as `integer` type in the [v2.3.x API reference](https://milvus.io/api-reference/restful/v2.3.x/v2/Vector%20(v2)/Query.md).

**Float value for Request-Timeout (should be integer):**
```bash
curl -s -X POST 'http://localhost:19530/v2/vectordb/collections/list' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer root:Milvus' \
  -H 'Request-Timeout: 3.5' \
  -d '{}'
```
Response: `{"code":0,"data":[]}` — success, no validation error. The fractional part is silently discarded (timeout set to 3 seconds instead of 3.5).

**String value for Request-Timeout (should be integer):**
```bash
curl -s -X POST 'http://localhost:19530/v2/vectordb/collections/list' \
  -H 'Content-Type: application/json' \
  -H 'Authoriz

## stage2_aggregation.confirmed
endpoint=entities+insert
defect_type=param_validation
related_issue_numbers=[49890]

## 探针脚本
.paperpilot/phase2/probes/milvus/probe_milvus_49890.py
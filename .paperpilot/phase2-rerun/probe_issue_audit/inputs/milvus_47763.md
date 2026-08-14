# milvus_47763 (group=A, version=2.6.10)

## issue 标题
[Bug]:  Field name validation missing - accepts invalid field names causing data inaccessibility

## issue body（截断 1500 字符）
### Is there an existing issue for this?

- [x] I have searched the existing issues

### Environment

```markdown
- Milvus version: v2.6.10
- Deployment mode(standalone or cluster): Standalone
- MQ type(rocksmq, pulsar or kafka): rocksmq
- SDK version(e.g. pymilvus v2.0.0rc2): PyMilvus v2.6.10
- OS(Ubuntu or CentOS): Windows (Client) / Linux (Server)
- CPU/Memory: N/A
- GPU: N/A
- Others: Docker Compose deployment
```

### Current Behavior

Milvus v2.6.10 accepts field names that violate documented naming rules (numeric prefixes, special characters, hyphens), and more critically, **the stored data becomes inaccessible** - users cannot query these fields after insertion.

### Expected Behavior

Field names should be validated according to the documented naming rules:
- Must start with a letter or underscore
- Can only contain letters, numbers, and underscores

Example expected error during INSERT:
```
<ParamError: (code=1100, message=Invalid field name '123field': field name must start with a letter or underscore)>
```

### Steps To Reproduce

```markdown
1. Create a collection with `enable_dynamic_field=True`
2. Insert data with a field name that starts with a number (e.g., `123field`)
3. Observe that the insertion succeeds (BUG)
4. Try to query the inserted data using the same field name
5. Observe that the query fails with `parse output field name failed`
**Complete Reproduction Script:**

from pymilvus import MilvusClient

client = MilvusClient("http://localhost:19530")

c

## stage2_aggregation.confirmed
endpoint=entities+insert
defect_type=doc_mismatch
related_issue_numbers=[47763]

## 探针脚本
.paperpilot/phase2/probes/milvus/probe_milvus_47763.py
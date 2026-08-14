# milvus_47766 (group=B, version=2.6.10)

## issue 标题
[Bug]: Data type validation missing - accepts integer into string field

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

Milvus v2.6.10 accepts integers inserted into string fields through dynamic field functionality, violating data type consistency requirements documented in official documentation.

**Key Issue**: When a dynamic field is first established as a string type (VARCHAR), subsequent insertions with integer values should be rejected but are instead accepted, causing data type inconsistency within the same field.

### Expected Behavior

Milvus should validate data types when inserting into dynamic fields. According to the official documentation, entities within the same collection should have the same data types.

Once a field is established with a specific type (VARCHAR for strings), subsequent insertions with incompatible types (INT64 for integers) should be rejected.

Example expected error:
```
<ParamError: (code=1100, message=Invalid data type for field 'text_field': expected VARCHAR, got INT64)>
```

### Steps To Reproduce

```markdown
1. Create a collection with dynamic field enabled (default behavior)
2. Insert first record with a string va

## stage2_aggregation.confirmed
endpoint=entities+insert
defect_type=type_coercion
related_issue_numbers=[47766]

## 探针脚本
.paperpilot/phase2/probes/milvus/probe_milvus_47766.py
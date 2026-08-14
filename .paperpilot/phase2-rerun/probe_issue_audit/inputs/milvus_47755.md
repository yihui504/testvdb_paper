# milvus_47755 (group=B, version=2.6.10)

## issue 标题
[Bug]: Filter expression validation too lenient

## issue body（截断 1500 字符）
### Is there an existing issue for this?

- [x] I have searched the existing issues

### Environment

```markdown
- Milvus version:v2.6.10
- Deployment mode(standalone or cluster):Standalone
- MQ type(rocksmq, pulsar or kafka):rocksmq
- SDK version(e.g. pymilvus v2.0.0rc2):PyMilvus v2.6.10
- OS(Ubuntu or CentOS): Windows (Client) / Linux (Server)
- CPU/Memory:N/A 
- GPU:N/A 
- Others: Docker Compose deployment
```

### Current Behavior

Milvus v2.6.10 accepts filter expressions with descending ranges (e.g., `field in [10, 5]`), which are semantically incorrect. While the syntax is valid, the expression should be rejected or normalized to ensure consistent behavior.

### Expected Behavior

Filter expressions should be validated for semantic correctness:

1. **Descending ranges**: Should be rejected or automatically normalized to ascending order
2. **Empty ranges**: Should be rejected with clear error message
3. **Single value in IN**: Should warn or suggest using equality operator
4. **Invalid LIKE usage**: Should fail when used on non-string fields
5. **Invalid JSON paths**: Should fail or handle gracefully with clear error messages

Example expected error for descending range:
```
<ParamError: (code=1100, message=Invalid filter expression: range values must be in ascending order, got [10, 5])>
```

Example expected error for empty range:
```
<ParamError: (code=1100, message=Invalid filter expression: IN expression cannot have empty range)>
```

### Steps To Reproduce

```mar

## stage2_aggregation.confirmed
endpoint=entities+delete
defect_type=param_validation
related_issue_numbers=[47755]

## 探针脚本
.paperpilot/phase2/probes/milvus/probe_milvus_47755.py
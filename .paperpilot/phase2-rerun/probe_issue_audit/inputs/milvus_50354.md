# milvus_50354 (group=B, version=2.6.17)

## issue 标题
[Bug]: REST API v2: password complexity not enforced — "abcdefgh" accepted on users/create

## issue body（截断 1500 字符）
### Is there an existing issue for this?

- [x] I have searched the existing issues

### Environment

```markdown
- Milvus version: v2.6.17
- Deployment mode(standalone or cluster): standalone (Docker)
- MQ type(rocksmq, pulsar or kafka): rocksmq (standalone default)
- SDK version(e.g. pymilvus v2.0.0rc2): REST API v2 (/v2/vectordb)
- OS(Ubuntu or CentOS): Windows 11 (Docker Desktop)
- CPU/Memory: N/A
- GPU: N/A
- Others:
```

### Current Behavior

`POST /v2/vectordb/users/create` has two distinct validation failures:

**1. HTTP status code always 200**: Password validation failures return HTTP 200 instead of HTTP 4xx, making programmatic error detection impossible.

**2. Password complexity not enforced**: The official documentation requires passwords to contain 3 of 4 character types (uppercase, lowercase, numbers, special characters), but the API only enforces length (6-256 characters). A password of all lowercase letters like `"abcdefgh"` is accepted.

#### Verified test results (with valid usernames):

| Password | Length | HTTP | code | Message | Bug? |
|----------|--------|------|------|---------|------|
| `""` (empty) | 0 | **200** | 1802 | "Field validation for 'Password' failed on the 'required' tag" | HTTP should be 4xx |
| `"a"` | 1 | **200** | 1100 | "1 out of range 6 <= value <= 256" | HTTP should be 4xx |
| `"abcdefgh"` | 8 | **200** | 200 | User created | **Complexity not enforced** |
| `"ValidP@ss1"` | 9 | 200 | 200 | User created | Expected ✅ |

#### Validat

## stage2_aggregation.confirmed
endpoint=users+create
defect_type=doc_mismatch
related_issue_numbers=[50354]

## 探针脚本
.paperpilot/phase2/probes/milvus/probe_milvus_50354.py
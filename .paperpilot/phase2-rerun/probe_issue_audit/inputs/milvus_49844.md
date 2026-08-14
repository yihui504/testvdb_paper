# milvus_49844 (group=C, version=2.6.16)

## issue 标题
[Bug]: REST API v2 query accepts null/missing filter and silently returns all entities

## issue body（截断 1500 字符）
## Is your feature request related to a problem? Please describe.

REST API v2 `/v2/vectordb/entities/query` accepts `null` or **missing** `filter` parameter and silently returns all entities in the collection, despite the official documentation marking `filter` as a **required** parameter.

This behavior creates a security risk: a client-side bug that omits the `filter` field (e.g., `filter=None` in Python, which serializes to JSON `null`) will unintentionally leak the entire collection's data without any error or warning.

## Describe the problem you're trying to solve

### Current Behavior

The `filter` parameter is documented as **required** in the REST API v2 specification:
- https://milvus.io/api-reference/restful/v2.4.x/v2/Vector%20(v2)/Query.md states: `filter (string, required)`
- The PyMilvus SDK documentation also marks `filter` as `[REQUIRED]`, noting: *"You can set this parameter to an empty string to skip scalar filtering."*

However, the REST API v2 implementation treats `null`/missing `filter` as "no filter" and returns all entities:

**Case 1: `filter` is `null` (Python `None` → JSON `null`)**
```bash
curl -s 'http://localhost:19530/v2/vectordb/entities/query' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer root:Milvus' \
  -d '{"collectionName":"test_coll","filter":null,"outputFields":["id"]}'
```
Response: `{"code":0,"data":[{"id":1},{"id":2}]}` — returns all rows ❌

**Case 2: `filter` field is completely omitted**
```bash
curl -s 'htt

## stage2_aggregation.confirmed
endpoint=entities+insert
defect_type=semantics
related_issue_numbers=[49844]

## 探针脚本
.paperpilot/phase2/probes/milvus/probe_milvus_49844.py
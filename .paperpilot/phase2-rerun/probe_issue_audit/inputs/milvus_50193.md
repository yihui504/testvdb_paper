# milvus_50193 (group=C, version=2.6.16)

## issue 标题
[Bug] get_stats returns rowCount=0 after successful insert and load (v2.6.16, regression from #30663)

## issue body（截断 1500 字符）
## Bug: get_stats returns rowCount=0 immediately after successful insert and load

### Environment
- Milvus version: v2.6.16
- Deployment mode: Standalone (Docker)
- SDK: REST API v2

### Current Behavior
After inserting entities into a collection and loading it, `collections/get_stats` returns `rowCount=0`, while `entities/query` with a filter correctly returns the inserted data. This inconsistency means the stats endpoint provides incorrect information about the collection state.

### Expected Behavior
`get_stats` should return the correct `rowCount` matching the actual number of entities in the collection after insert + load.

### Steps To Reproduce
1. Create a collection with a FloatVector field (dim=4)
2. Insert 5 entities
3. Load the collection
4. Call `get_stats` — observe `rowCount=0`
5. Call `query` with filter `id > 0` — observe 5 results returned

### Reproduction Script
```python
import requests
import time

BASE = "http://localhost:19530"
HEADERS = {"Authorization": "Bearer root:Milvus"}

# Create collection
payload = {
    "collectionName": "test_rowcount",
    "schema": {
        "autoID": False,
        "enableDynamicField": True,
        "fields": [
            {"fieldName": "id", "dataType": "Int64", "isPrimary": True},
            {"fieldName": "vector", "dataType": "FloatVector", "elementTypeParams": {"dim": 4}},
            {"fieldName": "value", "dataType": "Int64"}
        ]
    }
}
r = requests.post(f"{BASE}/v2/vectordb/collections/create", json=payloa

## stage2_aggregation.confirmed
endpoint=collections+load
defect_type=behavior
related_issue_numbers=[50193]

## 探针脚本
.paperpilot/phase2/probes/milvus/probe_milvus_50193.py
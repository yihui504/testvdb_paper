# milvus_50194 (group=C, version=2.6.16)

## issue 标题
[Bug] Concurrent delete and search returns stale/deleted data

## issue body（截断 1500 字符）
## Bug: Concurrent delete and search returns stale data after deletion

### Environment
- Milvus version: v2.6.16
- Deployment mode: Standalone (Docker)
- SDK: REST API v2

### Current Behavior
When entities are deleted from a collection and a search is performed concurrently, the search results may include entities that have already been deleted. This is a data corruption issue where stale/deleted data is returned to the user.

### Expected Behavior
After entities are deleted, subsequent search operations should not return those deleted entities. The search results should reflect the current state of the collection.

### Steps To Reproduce
1. Create a collection with a FloatVector field (dim=4)
2. Insert 10+ entities
3. Create an HNSW index and load the collection
4. Concurrently: delete some entities AND search for vectors
5. Observe that search results include entities that were just deleted

### Reproduction Script
```python
import requests
import time
import threading

BASE = "http://localhost:19530"
HEADERS = {"Authorization": "Bearer root:Milvus"}

# Create collection
payload = {
    "collectionName": "test_stale_data",
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
r = requests.p

## stage2_aggregation.confirmed
endpoint=entities+insert
defect_type=behavior
related_issue_numbers=[50194]

## 探针脚本
.paperpilot/phase2/probes/milvus/probe_milvus_50194.py
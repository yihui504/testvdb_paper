# qdrant_9149 (group=A, version=1.18.1)

## issue 标题
shard_number=0 and negative values accepted during collection creation

## issue body（截断 1500 字符）
## Current Behavior

When creating a collection via the REST API, `shard_number=0` and negative values (e.g. `-1`) are accepted without returning an error. The collection is created successfully with HTTP 200.

## Steps to Reproduce

**Test `shard_number=0`:**

1. Start a Qdrant instance (v1.18.1)
2. Run the following script:

```python
import requests, sys, uuid
BASE = 'http://localhost:6333'
c = 'test_shard_' + uuid.uuid4().hex[:8]
r = requests.put(f'{BASE}/collections/{c}', json={
    "vectors": {"size": 4, "distance": "Cosine"},
    "shard_number": 0
})
if r.status_code == 200:
    print(f'[DEFECT: ILLEGAL_SUCCESS] shard_number=0 accepted ({r.status_code})')
    sys.exit(1)
else:
    print(f'properly rejected shard_number=0: {r.status_code}')
    sys.exit(0)
```

**Test `shard_number=-1`:**

```python
r = requests.put(f'{BASE}/collections/{c}', json={
    "vectors": {"size": 4, "distance": "Cosine"},
    "shard_number": -1
})
if r.status_code == 200:
    print(f'[DEFECT: ILLEGAL_SUCCESS] shard_number=-1 accepted ({r.status_code})')
    sys.exit(1)
else:
    print(f'properly rejected shard_number=-1: {r.status_code}')
    sys.exit(0)
```

## Expected Behavior

The API should reject `shard_number` values <= 0 with a 400 Bad Request and a descriptive error message indicating that `shard_number` must be a positive integer.

## Possible Solution

Add input validation for `shard_number` in the collection creation endpoint. At minimum, check that the value is a positive integer 

## stage2_aggregation.confirmed
endpoint=collections+{collection_name}
defect_type=param_validation
related_issue_numbers=[9149]

## 探针脚本
.paperpilot/phase2/probes/qdrant/probe_qdrant_9149.py
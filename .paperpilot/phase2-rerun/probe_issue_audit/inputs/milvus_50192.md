# milvus_50192 (group=C, version=2.6.16)

## issue 标题
[Bug] Concurrent rename and create with same target name both succeed, causing state violation

## issue body（截断 1500 字符）
## Bug: Concurrent rename and create with same target name both succeed, causing state violation

### Environment
- Milvus version: v2.6.16
- Deployment mode: Standalone (Docker)
- SDK: REST API v2

### Current Behavior
When a rename operation and a create operation target the same collection name concurrently, **both operations succeed** (return code 0). This results in a state violation where the system allows conflicting collection names to coexist.

### Expected Behavior
Only one of the operations should succeed. Either the rename succeeds and the create fails with a conflict error, or the create succeeds and the rename fails. The system should never allow two collections with the same name to exist.

### Steps To Reproduce
1. Create a source collection with a unique name
2. Insert some data into the source collection
3. Concurrently send a rename request to rename the source collection to a new name, and a create request to create a new collection with the same new name
4. Observe that both requests return success (code 0)

### Reproduction Script
```python
import requests
import json
import sys
import uuid
import time
import threading

BASE = "http://localhost:19530"
HEADERS = {"Authorization": "Bearer root:Milvus"}

collection_name = "test_rename_src_" + uuid.uuid4().hex[:8]
new_name = "test_rename_dst_" + uuid.uuid4().hex[:8]

# SETUP: Create source collection
payload = {
    "collectionName": collection_name,
    "schema": {
        "autoID": False,
        "enableDy

## stage2_aggregation.confirmed
endpoint=collections+rename
defect_type=behavior
related_issue_numbers=[50192]

## 探针脚本
.paperpilot/phase2/probes/milvus/probe_milvus_50192.py
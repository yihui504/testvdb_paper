# qdrant_9255 (group=C, version=1.18.1)

## issue 标题
Payload filter returns points with missing payload field (payload=None)

## issue body（截断 1500 字符）
<!--- Provide a general summary of the issue in the Title above -->

## Current Behavior
<!--- Tell us what happens instead of the expected behavior -->

When performing a search with a payload filter (e.g., `{"must":[{"key":"color","match":{"value":"red"}}]}`), the response includes points where the `payload` field is `None` or the filtered key is entirely absent. These points do not satisfy the filter condition, yet they are returned in the search results alongside points that genuinely match.

Observed output: `filter color=red returned point with color=None`

## Steps to Reproduce
<!--- Provide a link to a live example, or an unambiguous set of steps to -->
<!--- reproduce this bug. Include code to reproduce, if relevant -->

1. Start Qdrant v1.18.1:

```
docker run -d --name qdrant-payload-bug -p 6333:6333 -p 6334:6334 qdrant/qdrant:v1.18.1
```

2. Create a collection:

```
curl -X PUT 'http://localhost:6333/collections/test_payload_filter' -H 'Content-Type: application/json' -d '{"vectors": {"size": 4, "distance": "Cosine"}}'
```

3. Insert 10 points — even IDs have `color=red`, odd IDs have `color=blue`, and point id=3 and id=6 have no `color` payload at all:

```
curl -X PUT 'http://localhost:6333/collections/test_payload_filter/points?wait=true' -H 'Content-Type: application/json' -d '{"points": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4], "payload": {"color": "red"}}, {"id": 2, "vector": [0.5, 0.6, 0.7, 0.8], "payload": {"color": "blue"}}, {"id": 3, "vector": [0.9, 0.

## stage2_aggregation.confirmed
endpoint=collections+{collection_name}+points
defect_type=semantics
related_issue_numbers=[9255]

## 探针脚本
.paperpilot/phase2/probes/qdrant/probe_qdrant_9255.py
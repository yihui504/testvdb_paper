# qdrant_9371 (group=C, version=1.18.2)

## issue 标题
Bug: Batch operations not atomic — valid points persisted despite HTTP 400 error

## issue body（截断 1500 字符）
## Current Behavior

When a batch point operation (`POST /collections/{name}/points/batch`) contains a mix of valid and invalid operations, the API returns HTTP 400 (indicating the batch was rejected), but the **valid operations within the batch are partially applied** — count increases despite the error.

### Reproduced evidence

```
Collection created with vectors: {size: 4, distance: "Cosine"}

--- Test A: All-valid batch (control) ---
Batch with 3 valid points → HTTP 200
Count: 3 ✓

--- Test B: Mixed valid+invalid batch ---
Batch: 2 valid points (dim=4) + 1 invalid point (dim=3)
→ HTTP 400 ← server says "rejected"
Response: {"status": {"error": "Wrong input: Vector dimension error: expected dim: 4, got 3"}}

Count before batch: 3
Count after batch:  5 ← INCREASED! The 2 valid points were inserted despite the 400 error.
```

The bug was confirmed in **2 independent executions** (original test + MRE script). It is **state-dependent** — a freshly restarted container may not exhibit the issue, suggesting it relates to accumulated operational state.

## Steps to Reproduce

> ⚠️ The bug may not appear on a fresh container. Run significant CRUD operations first.

1. Start Qdrant v1.18.2: `docker run -p 6333:6333 qdrant/qdrant:v1.18.2`
2. Create collection: `vectors: {size: 4, distance: "Cosine"}`
3. Upsert 3 valid points individually (IDs 1-3, vector dim=4)
4. Send a mixed batch via `POST /collections/{name}/points/batch`:
```json
{
  "operations": [{
    "upsert": {
      "poin

## stage2_aggregation.confirmed
endpoint=collections+{collection_name}+points+batch
defect_type=behavior
related_issue_numbers=[9371]

## 探针脚本
.paperpilot/phase2/probes/qdrant/probe_qdrant_9371.py
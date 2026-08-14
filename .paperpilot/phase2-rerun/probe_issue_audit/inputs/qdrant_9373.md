# qdrant_9373 (group=C, version=1.18.2)

## issue 标题
Bug: Payload index silently returns severely incomplete results — 2/25 matching points after wait:true

## issue body（截断 1500 字符）
## Current Behavior

After creating a keyword payload index on a string field with `wait: true`, filtered queries return only **2 out of 25** matching points — a 92% miss rate. The index creation returns HTTP 200 (indicating the index was built successfully), and the collection point count confirms all 50 points exist, but the indexed field returns severely truncated results with no error or warning.

### Reproduced evidence

```
Collection created
50 points inserted with payload (25 cat_a, 25 cat_b)
Count before index: 50                         ← all 50 points confirmed present
Payload index created on 'category_id'          ← wait: true passed in JSON body
Filter cat_a via indexed field: 2 points (expected 25)  ← 92% MISS RATE

=== VERDICT: DEFECT_FOUND (Type4_StateLogicViolation) ===
Indexed search returned 2 points, expected 25
```

The bug was confirmed in **2 independent executions** (original test + MRE script). It is **state-dependent** — a freshly restarted container returns correct results (25/25). The bug only manifests after the container has accumulated significant operational history (hours of CRUD operations).

### Container state comparison

| Test | Container Uptime | Operations | Result |
|------|-----------------|-----------|--------|
| Original execution | ~8 hours | 64 scripts, many collections | 2/25 ❌ |
| MRE (pre-restart) | ~10 hours | Same state | 2/25 ❌ |
| Control (post-restart) | ~0 hours | Fresh container | 25/25 ✅ |

## Steps to Reproduce

> ⚠️ 

## stage2_aggregation.confirmed
endpoint=collections+{collection_name}+points+count
defect_type=behavior
related_issue_numbers=[9373]

## 探针脚本
.paperpilot/phase2/probes/qdrant/probe_qdrant_9373.py
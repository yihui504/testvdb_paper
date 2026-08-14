# milvus_49059 (group=B, version=2.6.12)

## issue 标题
[Bug]: COSINE Metric Returns Distance > 1.0 for Identical Vectors (Precision Overflow)

## issue body（截断 1500 字符）
### Is there an existing issue for this?

- [x] I have searched the existing issues

### Environment

```markdown
- Milvus version: v2.6.12 (also reproduced on v2.3.7)
- Deployment mode(standalone or cluster):standalone (Docker)
- MQ type(rocksmq, pulsar or kafka):rocksmq
- SDK version(e.g. pymilvus v2.0.0rc2):pymilvus v2.6.12
- OS(Ubuntu or CentOS): Windows / Linux (Docker)
- CPU/Memory: N/A (Mathematical precision issue, hardware independent)
- GPU: N/A 
- Others: Vector config: Dimensions: 128, Metric: `COSINE`, Index: `IVF_FLAT`
```

### Current Behavior

When performing a vector search using the `COSINE` metric type, the distance returned for identical vectors is strictly greater than `1.0` (e.g., `1.0000001192092896`). 

This happens due to unhandled floating-point precision loss (imprecision) during dot product/cosine calculation at the C++ core (Segcore/Knowhere) without proper boundary clamping before returning the result to the client.

### Expected Behavior

The calculation result for identical normalized vectors using the `COSINE` metric should be bounded. It should strictly adhere to the mathematical definition of Cosine Similarity/Distance (e.g. `<= 1.0`). 

It is highly recommended to add a clamp function (e.g., `std::min(1.0f, std::max(-1.0f, result))`) at the core execution node before returning the metric to the client to avoid mathematical invariant violations.

### Steps To Reproduce

```markdown
from pymilvus import connections, Collection, FieldSchema, C

## stage2_aggregation.confirmed
endpoint=entities+search
defect_type=crash
related_issue_numbers=[49059]

## 探针脚本
.paperpilot/phase2/probes/milvus/probe_milvus_49059.py
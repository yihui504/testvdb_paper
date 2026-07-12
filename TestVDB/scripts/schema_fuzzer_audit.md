# 19-probe fuzzer audit (R2-W2 实跑背书)

**Date**: 2026-07-13
**Target**: milvus 2.6.19 (Docker standalone, `testvdb-milvus-standalone`)
**Script**: `TestVDB/scripts/schema_fuzzer.py` (the paper's "hand-written boundary fuzzer, 19 probes, no LLM")
**Purpose**: R2-W2 asked to "run the 19-probe fuzzer against the 5 unique TPs and report they miss" rather than argue structurally. This file is the run log + per-TP cross-check.

## Fuzzer output (19 probes against milvus v2.6.19)

```
Total probes (excl setup): 19
API-ACCEPTED (potential spec violations): 7
API-rejected (spec-conformant): 12

--- POTENTIAL VIOLATIONS ---
  * metricType missing                      [collections/create]  http=200 code=0
  * consistencyLevel=INVALID (doc:enum)     [collections/create]  http=200 code=0
  * consistencyLevel=42 (int,doc:enum)      [collections/create]  http=200 code=0
  * nprobe=0 (doc:>=1?)                     [entities/search]     http=200 code=0
  * nprobe=-1                               [entities/search]     http=200 code=0
  * query limit=-1                          [entities/query]      http=200 code=0
  * query limit=0                           [entities/query]      http=200 code=0

--- API-REJECTED (12) ---
  dim=0/-1/32769, dim='128' string, metricType=INVALID, collectionName empty/missing,
  search limit=-1/0/16385, wrong-dim query, query limit=16385
```

Matches paper §5.3 "7 accepted, 5 genuine violations" (2 of the 7 accepted are by-design defaults).

## Per-TP cross-check: does any of the 19 probes trigger the TP?

| TP | Class | Trigger condition | In the 19 probes? | Run result |
|---|---|---|---|---|
| milvus #47636 | diag. | malformed filter expr $\to$ code=0 + lexer leak | No: search probes use `data` (no filter); query probes use `filter:"id > 0"` (well-formed) | **0/19** |
| milvus #47635 | state | load() $\to$ search returns code=0 | No: probes are stateless single-requests; no `load` probe, no load$\to$search sequence | **0/19** |
| milvus #50323 | state | delete accepts both filter+ids (mutually exclusive) | No: 19 probes cover create/search/query only; **no delete endpoint** | **0/19** |

## Non-milvus TPs (fuzzer is milvus-only)

`schema_fuzzer.py` `BASE = http://localhost:19530/v2/vectordb` — milvus-only by construction.
- qdrant #9039: out of fuzzer scope (not targeted)
- weaviate #12041: out of fuzzer scope (not targeted)

## Conclusion

**0/5 unique TPs are triggered by the 19-probe fuzzer instance** — confirmed by running the fuzzer on milvus v2.6.19 (3 milvus TPs: 0/19 probes each) and by the fuzzer's milvus-only scope (2 non-milvus TPs). This converts the Round-19 structural argument into a run-backed claim for the milvus subset; the 2 non-milvus TPs remain out-of-scope by construction (the fuzzer does not target those systems).

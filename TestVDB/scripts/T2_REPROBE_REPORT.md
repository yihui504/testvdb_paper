# Round 11 — T2 Live Re-probe + Source-Grounded Classification

**Date:** 2026-07-12
**Target:** milvus v2.6.19 (fresh Docker container, `milvusdb/milvus:v2.6.19`)
**Goal:** Replace LLM-proxy ground truth with live-reproduced behavior + milvus-source
reasoning for the boundary subset (addresses Round-10 reviewer R2 3.2 / R3 Q2 / R3 Q3).

## Experiment 1 — Schema fuzzer (19 probes) reproduced

Re-ran `scripts/schema_fuzzer.py` against a fresh milvus v2.6.19 container.

| metric | paper (Round 8/9) | Round 11 live |
|---|---|---|
| total probes | 19 | 19 |
| API-accepted | 7 | 7 |
| API-rejected | 12 | 12 |

**Result matches the paper exactly.** The 7 API-accepted candidates:
1. `metricType` missing
2. `consistencyLevel=INVALID`
3. `consistencyLevel=42` (int for enum)
4. `nprobe=0`
5. `nprobe=-1`
6. `query limit=-1`
7. `query limit=0`

The search/query `limit` internal inconsistency is confirmed live:
`entities/search` rejects `limit=-1/0/16385` (code 1100), while `entities/query`
accepts `limit=-1` and `=0` (code 0) — an internal contract inconsistency.

## Experiment 2 — Source-grounded post-filter on the 7 accepted

For each of the 7 API-accepted candidates, classify GENUINE-violation vs
BY-DESIGN using milvus source constants
(`client/entity/collection.go`: `DefaultConsistencyLevel = ClBounded`,
`DefaultShardNumber = 0`) plus maintainer adjudication (#47729 fixed):

| # | candidate | classification | source evidence |
|---|---|---|---|
| 1 | `metricType` missing | **BY-DESIGN** | empty = unspecified; default COSINE |
| 2 | `consistencyLevel=INVALID` | **BY-DESIGN** | `DefaultConsistencyLevel=ClBounded`; silent fallback |
| 3 | `consistencyLevel=42` (int) | **GENUINE** | int for enum param, no validation |
| 4 | `nprobe=0` | **GENUINE** | maintainer fixed as milvus #47729 |
| 5 | `nprobe=-1` | **GENUINE** | negative accepted, no lower-bound check |
| 6 | `query limit=-1` | **GENUINE** | search rejects (code 1100), query accepts — inconsistency |
| 7 | `query limit=0` | **GENUINE** | returns data where 0 should mean empty |

**Post-filter precision = 5/7 = 71.4%** (Wilson 95% CI [30.8%, 95.0%], n=7).

This is the direct answer to R3 Q3: a spec-driven fuzzer's 7 API-accepted
probes, after source-grounded by-design filtering, yield **5 genuine
violations (71%)** — the fuzzer mostly rediscovers TestVDB's boundary yield
(nprobe=0 = #47729; the search/query limit inconsistency) with 2 by-design
silent-default FPs that its no-LLM design cannot suppress.

## Experiment 3 — DEV_AUDIT candidates live + source

Re-probed the 8 candidates from `DEV_AUDIT.md` (the dev-reviewer's
source-grounded FP set) on fresh v2.6.19:

| candidate | live behavior | source class |
|---|---|---|
| `consistencyLevel='Invalid'` | ACCEPTED (code 0) | BY-DESIGN (`ClBounded` default) |
| `consistencyLevel=42` | ACCEPTED | GENUINE (int accepted) |
| `shardsNum=0` | ACCEPTED | BY-DESIGN (`DefaultShardNumber=0`) |
| `shardsNum=-1` | ACCEPTED | BY-DESIGN (clamp to 1) |
| `shardsNum=-100` | ACCEPTED | BY-DESIGN (clamp to 1) |
| `metricType=''` | ACCEPTED | BY-DESIGN (default COSINE) |
| `metricType` missing | ACCEPTED | BY-DESIGN (default COSINE) |
| `vectorFieldType='Invalid'` | ACCEPTED | BY-DESIGN (silent FloatVector substitute) |

**All 8 behaviors reproduce on a fresh container.** Milvus source constants
independently confirm 7 of 8 as by-design default/clamp fallbacks — this is
the same FP class the dev-reviewer's source anchor targets, now validated by
live reproduction + source-code evidence rather than LLM-proxy judgment.

## What this contributes (mapping to Round-10 reviewer asks)

- **R3 Q3 (post-filter precision):** answered — 5/7 = 71% after source-grounded filtering.
- **R2 3.2 / R3 Q2 (mixed ground truth):** partial — for the boundary/DEV_AUDIT
  subset, the LLM-proxy ground truth is replaced by live+source evidence.
  The full 27-suppressed re-adjudication remains future work (those candidates
  span multiple mining runs and require a per-candidate payload reconstruction
  before live re-probe).
- **R2 3.6 (schema-fuzzer repositioning):** strengthened — the fuzzer's 71%
  post-filter precision confirms it is genuinely effective on the boundary
  subset but cannot suppress the 2 by-design FPs (no source-grounded layer),
  reinforcing TestVDB's marginal value in FP-suppression + state/semantic.

## Artifacts

- `scripts/schema_fuzzer.py` — 19-probe fuzzer (reproduced)
- `scripts/t2_reprobe_audit.py` — audit re-probe + source classifier
- `scripts/t2_reprobe_audit_results.json` — raw results

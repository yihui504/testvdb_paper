# Spec-Driven Mining Pipeline — Design Plan

**Date**: 2026-07-05
**Status**: Design (awaiting implementation); all architectural decisions LOCKED via 2026-07-05 grilling session
**Related**: `2026-06-07-testvdb-v2-evolution-design.md`, `2026-06-14-batch-c-cleanup-design.md`
**Companion docs** (produced by grilling session):
- `2026-07-05-probe-spec-dsl.md` — full DSL spec (vocabularies, execution schemas, worked examples)
- `2026-07-05-spec-driven-mining-adrs-and-glossary.md` — 10 ADRs + glossary (canonical decision record)

> Reader guide: start here for architecture and migration path; consult the DSL
> spec for schema details; consult the ADR file for "why this decision" rationale.

---

## 1. Background — Why this plan exists

A qdrant v1.18.2 mining run (session `2026-07-05T06-19-10Z`) revealed that
the current pipeline **fails to effectively consume `threat_model.json`**:

- threat-modeler agent outputs `attack_surface.areas[].attack_order` as **empty fields** (0/4 populated)
- `threat_model_injector.py` then **fabricates** the "attack order" text via hardcoded DB-specific mappings
- attack agents (`attack-boundary` / `attack-state` / `attack-semantic`) receive these as fuzzy labels,
  not executable specs → 35 generated scripts were all simple single-threaded boundary tests
- DEBATE_S1 has **no adherence check** → agents skipping the prescribed probe pattern go unchallenged
- Result: 5 candidate defects, of which 0–1 would survive upstream maintainer triage
  (see `results/qdrant/v1.18.2/2026-07-05T06-19-10Z/maintenance_review.md`)

### 1.1 First attempt (rejected as non-general)

Initial fix proposed **bug_shape enumeration**: 5 fixed shapes, 5 fixed agents, 5 fixed templates.

**This breaks generality**: `threat_model.json` is regenerated for **every (DB, version) pair**.
qdrant v1.18.2 has 5 bug_shapes; weaviate might have GraphQL schema validation issues;
pgvector might have SQL injection vectors. Hardcoding shapes makes the pipeline DB-specific.

### 1.2 Core insight (this design)

> **threat_model must self-describe the tests it needs. The pipeline provides
> generic execution primitives, not DB-specific bug knowledge.**

The unit of contract between threat-modeler and attack agents becomes a
**self-describing ProbeSpec**, executed against a small set of **DB-agnostic
probe patterns** (concurrent / drift / cross_surface / etc.). These patterns
are testing primitives, not bug categories.

---

## 2. Design principles

1. **DB-agnostic pipeline core** — no bug_shape names, no endpoint names, no DB-specific code in the pipeline
2. **threat_model owns the bug knowledge** — pipeline only owns *how to execute and verify*
3. **probe patterns are testing primitives** — small open set reflecting *test shapes* (concurrent, sequential, drift, etc.), not *bug categories*
4. **Spec-driven agents** — agents are spec executors; they do not freelance
5. **Adherence is structural** — verify code implements the spec's pattern, not a fixed AST fingerprint
6. **Open extensibility** — adding a new probe pattern is an explicit, reviewed pipeline change (not silent LLM improvisation)

---

## 3. Architecture

```
Stage: Threat Model Construction
  threat-modeler agent → threat_model.json
  (DB-specific content, schema-driven ProbeSpecs)
        │
        ▼  (JSON → JSON, no fabrication)
Stage: Spec Verification (NEW)
  scripts/threat_model_completeness.py
  (rejects threat_model.json with empty/malformed ProbeSpecs)
        │
        ▼
Stage: Attack Generation
  attack-spec-executor agent (replaces boundary/state/semantic)
  reads ProbeSpec[i].probe_pattern.type → loads matching template
  fills DB-specific params from ProbeSpec → emits script
        │
        ▼
Stage: DEBATE_S1 (augmented)
  existing checks: py_compile, risky_scripts, api_format, target_neutrality
  NEW: scripts/spec_adherence.py
       (verifies script implements ProbeSpec.probe_pattern)
        │
        ▼  (existing pipeline continues)
   execution / judges / verify-live / reporter
```

---

## 4. Schema — ProbeSpec (the contract)

> Replaces `attack_surface.areas[].attack_order[]` (currently empty) and the
> injector's fabricated text. Defined in `lib/threat_model/schema.py` (new).

### 4.1 Top-level threat_model.json additions

```jsonc
{
  "_meta": { ... },
  "attack_surface": {
    "high_priority_areas": [
      {
        "area": "<DB-specific name>",
        "rationale": "...",
        "historical_defect_count": <int>,
        "bug_shapes": ["<DB-specific tags>"],
        "mapped_contract_endpoints": ["..."],
        "probe_specs": [           // ← NEW: structured, self-describing
          { ... ProbeSpec ... }
        ]
      }
    ]
  }
}
```

### 4.2 ProbeSpec schema (the unit of work)

```jsonc
{
  "id": "bs02-race-concurrent-delete-upsert",   // unique, DB-specific
  "bug_shape_tags": ["concurrency-data-race"],  // informational, not used by pipeline
  "rationale": "<why this probe, in natural language>",

  "target": {
    "endpoint": "PUT /collections/{name}/points",
    "method": "PUT",
    "endpoint_ref": "structured_contract.json:endpoint_registry[<idx>]"
  },

  "invariant": "<natural-language statement of correct behavior>",
  // e.g. "for a fixed (collection, point_id), after concurrent {upsert, delete}
  //        operations quiesce, the final state must have count ∈ {0,1} and
  //        if count==1 the stored vector must equal one of the submitted vectors"

  "probe_pattern": {                            // ← core: self-describing execution
    "type": "concurrent",                       // pipeline primitive (open enum)
    "setup": [                                  // ordered steps
      {"kind": "create_collection", "name": "T1"},
      {"kind": "pre_populate", "id": 1, "vector": [0.5,0.5,0.5,0.5]}
    ],
    "execution": {
      "threads": 20,
      "rounds_per_thread": 50,
      "operations": [
        {"op": "upsert", "target_id": 1, "vector_template": "thread_idx_normalized"},
        {"op": "delete", "target_id": 1}
      ],
      "synchronization": "join_all_then_quiesce(wait_seconds=2)"
    },
    "verification": [                           // ordered assertions
      {"kind": "count", "expect": "<=1"},
      {"kind": "scroll", "target_id": 1, "expect_vector_in": "submitted_set"},
      {"kind": "no_5xx"}
    ]
  },

  "oracle": {
    "defect_found_when":
      "final_count > 1 OR (final_count == 1 AND point_missing) OR any_5xx",
    "false_positive_when":
      "test infra race (network reset) — re-run to confirm"
  },

  "evidence": {                                 // for the eventual defect report
    "historical_refs": ["PR #6593", "issue #..."],
    "doc_refs": ["raw_knowledge.md:line N"],
    "expected_doc_behavior": "<what docs say should happen>"
  }
}
```

### 4.3 Why this works for any DB

- All structural keys (`target`, `invariant`, `probe_pattern`, `oracle`) are **DB-agnostic**.
- DB-specific content lives in **values** (endpoint path, vector template, doc refs).
- `bug_shape_tags` is informational only — pipeline never branches on it.
- Adding a new bug class = adding new ProbeSpecs with new ids; **no pipeline change needed** unless a new `probe_pattern.type` is required.

---

## 5. Probe patterns — the pipeline primitives

`probe_pattern.type` is a **small, open enum of testing primitives**. Initial set:

| type | Semantics | Required execution features | Verification typically used |
|---|---|---|---|
| `single_request` | One HTTP call, observe response | one request, response status/body assertions | status code, error message content |
| `sequential` | Ordered chain of N requests | ≥2 sequential requests with ordering | final state matches expectation |
| `concurrent` | Multiple workers racing on shared state | threading/asyncio + sync point + final-state read | count, presence/absence, no 5xx |
| `drift_after_mutation` | Snapshot query result before/after a mutation | ≥2 reads at distinct times + diff | reads agree (within documented tolerance) |
| `cross_surface` | Same query via ≥2 transports (REST vs gRPC) | ≥2 transports issuing identical query | responses semantically equal |
| `mutation_during_read` | Read happening while write in flight | concurrent reader + writer + final reconciliation | reader never observes inconsistent state |
| `boundary_value` | Enumerate {0, -1, max, NaN, empty, null, very-long} | parametrized table of inputs + per-row verdict | documented acceptance/rejection per value |

**Adding a new pattern** = an explicit pipeline change:
1. Define `templates/probe_patterns/<new>.py.tmpl`
2. Add to `PROBE_PATTERN_FEATURES` in `spec_adherence.py`
3. Document in this plan
4. Bump schema version

Until a pattern is registered, `threat_model_completeness.py` rejects ProbeSpecs using it.

### 5.1 Why these are primitives, not bug categories

Each pattern describes **how to execute and verify**, not **what bug class** it targets.
- `concurrent` can find race conditions *or* deadlocks *or* resource exhaustion — bug class depends on the ProbeSpec's `invariant`/`oracle`
- `drift_after_mutation` can find index drift *or* cache staleness *or* replica divergence — same
- A new bug class (e.g. "vector quantization precision loss") reuses existing patterns (it's `drift_after_mutation` with quantization as the mutation)

This is the key that makes the pipeline DB-agnostic.

---

## 6. Component designs

### 6.1 `templates/probe_patterns/<type>.py.tmpl`

DB-agnostic Jinja-style templates. Each renders a complete, self-contained Python script.

**Template contract** (every template must implement):
- Read DB URL via `TESTVDB_DB_URL` env var (uniform across DBs)
- `setup()` — execute `probe_pattern.setup[]`
- `execute()` — execute `probe_pattern.execution`
- `verify()` — execute `probe_pattern.verification[]`, collect pass/fail
- `print("VERDICT: <VERDICT_FOUND|NO_DEFECT|AMBIGUOUS>")` based on `oracle`
- `cleanup()` — best-effort teardown
- Embed the full ProbeSpec as a JSON comment in the script header (so adherence checker can read it)

**Example skeleton (`concurrent.py.tmpl`)**:
```python
import threading, time, requests, os, sys, json
BASE = os.environ["TESTVDB_DB_URL"]

def setup(spec):
    # render from spec.probe_pattern.setup[]
    # e.g. create collection, pre-populate
    ...

def worker(spec, idx, results):
    for round_idx in range(spec.execution.rounds_per_thread):
        op = spec.execution.operations[round_idx % len(spec.execution.operations)]
        # execute op against target_id
        ...
    results[idx] = ...

def execute(spec):
    results = [None] * spec.execution.threads
    threads = [threading.Thread(target=worker, args=(spec, i, results)) for i in range(spec.execution.threads)]
    for t in threads: t.start()
    for t in threads: t.join()
    time.sleep(spec.execution.synchronization.wait_seconds)
    return results

def verify(spec, results):
    # apply spec.probe_pattern.verification[] assertions
    # return dict of pass/fail per assertion
    ...

def verdict(spec, verification):
    # apply spec.oracle.defect_found_when
    return "VERDICT_FOUND" if ... else "NO_DEFECT"

if __name__ == "__main__":
    spec = json.loads(os.environ["TESTVDB_PROBE_SPEC"])
    setup(spec); results = execute(spec); v = verify(spec, results)
    print(f"VERDICT: {verdict(spec, v)}")
```

### 6.2 `agents/threat-modeler.md` — output schema change

**Replace** the current loosely-defined `attack_order` field with a hard ProbeSpec schema requirement.

Add to agent prompt:
> Each `high_priority_area` MUST contain `probe_specs: [ProbeSpec]`. Each ProbeSpec MUST populate `id`, `target`, `invariant`, `probe_pattern` (with a registered `type`), `oracle`, `evidence`. ProbeSpecs are the unit of work consumed by attack-spec-executor; vague labels like `"race_condition"` are insufficient. If you cannot describe the probe as a self-describing spec, omit it (do not pad with empty labels).

**threat-modeler must consult** the registered pattern list in
`docs/specs/probe-patterns-registry.md` (new doc) so it doesn't invent new types.

### 6.3 `agents/attack-spec-executor.md` (NEW; replaces attack-boundary/state/semantic)

Single agent. Responsibilities:
1. Receive `ProbeSpec[i]` and `<target_contract>` as input
2. Look up `templates/probe_patterns/<probe_pattern.type>.py.tmpl`
3. Render template with ProbeSpec's params + target contract details (endpoint path, payload schema)
4. Emit `<session_dir>/debate_logs/probe-<spec_id>.py`
5. Run `py_compile`; if fails, fix and retry (max 2 internal retries)
6. **Forbidden** to change `probe_pattern.type`'s execution semantics — only fill in DB-specific values

**Migration**: existing `attack-{boundary,state,semantic}.md` are kept as **fallback** for one release cycle (legacy mode), but their output is held to the same adherence gate (§6.5).

### 6.4 `scripts/threat_model_completeness.py` (NEW)

Runs immediately after threat-modeler agent, before any mining.

Checks (each on every `probe_specs[]` in every area):
- `id` unique and non-empty
- `target.endpoint` references an endpoint that exists in `structured_contract.json:endpoint_registry`
- `invariant` is a non-trivial natural-language statement (≥ 20 chars)
- `probe_pattern.type` ∈ registered patterns set
- `probe_pattern.setup`/`execution`/`verification` are non-empty lists
- `oracle.defect_found_when` is non-empty
- `evidence.expected_doc_behavior` references a real doc location

**Failure mode**: report first missing field, exit non-zero, force threat-modeler re-run.

### 6.5 `scripts/spec_adherence.py` (NEW)

Runs in DEBATE_S1, after the existing 4 checks. For each `probe-*.py` script:

1. Parse ProbeSpec from script header comment (renderer must embed it)
2. Determine `probe_pattern.type`
3. Look up required **structural features** for that pattern in `PROBE_PATTERN_FEATURES`
4. Static-analyze script AST for those features
5. If any missing → reject, route back to attack-spec-executor for rewrite (max 2 retries)

**`PROBE_PATTERN_FEATURES` (initial)**:
```python
PROBE_PATTERN_FEATURES = {
    "concurrent": {
        "must_contain": [
            ("threading.Thread", "asyncio.create_task"),  # any one
            "join",                                        # sync point
            "VERDICT",                                     # verdict output
        ],
        "verification_shape": "post_quiesce_state_read",  # at least one read after sync
    },
    "drift_after_mutation": {
        "must_contain": ["VERDICT"],
        "verification_shape": "two_reads_with_diff",      # ≥2 reads + comparison
        "min_distinct_queries": 2,
    },
    "cross_surface": {
        "must_contain": ["grpc", "requests"],  # both transports
        "verification_shape": "transport_response_diff",
    },
    "boundary_value": {
        "verification_shape": "parametrized_table",       # ≥3 distinct input values tested
        "min_input_variants": 3,
    },
    # single_request, sequential: minimal structural requirements
}
```

**Why this stays DB-agnostic**: features are about *test shape*, not *bug shape*.
`concurrent` always needs threading regardless of which DB; `cross_surface`
always needs ≥2 transports regardless of which API surface.

### 6.6 `scripts/threat_model_injector.py` — simplification

**Remove** all DB-specific "inference" branches (the lines that turn
`concurrency-data-race-point-mutation` into `"concurrent_delete+upsert_same_id"`).

Replace with pure JSON→text rendering of `probe_specs[]`. Output is a
spec listing, not a fabricated narrative.

Expected diff: ~300 lines deleted, ~80 lines added.

---

## 7. Migration path

### Phase 1 — Verifiers only (1–2 days, no agent change)
1. Add `scripts/threat_model_completeness.py`
2. Add `scripts/spec_adherence.py` (with current ProbeSpec schema, even though threat_model.json doesn't populate it yet — gate runs but finds nothing to check)
3. Wire both into pipeline_state transitions
4. **Effect**: existing threat-modeler outputs flagged as incomplete; existing attack scripts flagged as non-conforming. Surface the gap, don't break the pipeline.

### Phase 2 — Schema + templates (1 week)
1. Define `lib/threat_model/schema.py` (formal ProbeSpec schema)
2. Write 5 probe pattern templates (`concurrent`, `drift_after_mutation`, `cross_surface`, `sequential`, `single_request`)
3. Update `agents/threat-modeler.md` prompt: require ProbeSpecs
4. **Effect**: threat-modeler output becomes structured; templates ready.

### Phase 3 — Spec-executor agent (1 week)
1. Write `agents/attack-spec-executor.md`
2. Run alongside `attack-{boundary,state,semantic}` for one release (shadow mode)
3. Compare adherence pass-rate; switch over when ≥80%
4. **Effect**: agents stop freelancing; scripts become spec-faithful.

### Phase 4 — Cleanup (1 week)
1. Remove `attack-{boundary,state,semantic}` agents
2. Simplify `threat_model_injector.py` to pure renderer
3. Update `commands/mine.md` SOP
4. **Effect**: pipeline core is DB-agnostic, ~40% less code in attack-gen path.

---

## 8. Failure modes & mitigations

| Risk | Mitigation |
|---|---|
| threat-modeler invents new `probe_pattern.type` not in registry | `threat_model_completeness.py` rejects; agent prompted to use registered types or propose one explicitly via a "new-pattern-request" ProbeSpec (handled in Phase 2.5) |
| Templates can't express a real test (e.g. snapshot + WAL replay) | Add new pattern type with template; explicit pipeline change; documented in registry |
| ProbeSpec too rigid → threat-modeler emits too few specs | Track `probe_specs_count` per area; if <2, prompt re-run |
| attack-spec-executor fills template wrongly (params mismatched) | `spec_adherence.py` runs a smoke execution (dry-run with N=1) and rejects on TypeError |
| Cross-DB normalization breaks (e.g. weaviate GraphQL not REST) | ProbeSpec.target uses abstract `endpoint` + `transport`; template normalizes per DB via `_target_api_reference.md` (existing) |
| Existing attack agents break in Phase 1 | Verifiers run in non-blocking "report mode" first; blocking enabled once stable |

---

## 9. Acceptance criteria

The redesign is considered successful when, on the next qdrant mining run AND at least one cross-DB run (e.g. weaviate or milvus):

1. `threat_model_completeness.py` passes (all areas have non-empty `probe_specs`)
2. `spec_adherence.py` blocks ≥90% of scripts that don't implement their declared pattern
3. attack-spec-executor produces ≥80% of scripts from templates (vs from-scratch)
4. **Maintainer-view triage** of resulting defects accepts ≥50% as legitimate bugs (vs current 0–20%)
5. No DB-specific code added to `scripts/` or `templates/` (all DB knowledge in `intelligence/<db>/`)

Criteria 4 is the real success measure — the others are leading indicators.

---

## 10. Out of scope (explicit non-goals)

- **Source-code fuzzing** (cargo-fuzz, atheris) — different pipeline, out of scope
- **Static analysis of target DB source** for untested paths — useful but separate
- **Replacing the threat-modeler agent itself** — only its output schema is constrained
- **Cross-DB transferable bug libraries** — future work, not required for this design

---

## 11. File inventory (what changes / what's added)

```
NEW:
  lib/threat_model/schema.py                              (ProbeSpec schema)
  docs/specs/probe-patterns-registry.md                   (registered pattern list)
  docs/specs/2026-07-05-spec-driven-mining-pipeline.md    (this plan)
  scripts/threat_model_completeness.py                    (verifier)
  scripts/spec_adherence.py                               (DEBATE_S1 gate)
  templates/probe_patterns/concurrent.py.tmpl
  templates/probe_patterns/drift_after_mutation.py.tmpl
  templates/probe_patterns/cross_surface.py.tmpl
  templates/probe_patterns/sequential.py.tmpl
  templates/probe_patterns/single_request.py.tmpl
  agents/attack-spec-executor.md

MODIFIED:
  agents/threat-modeler.md                                (output schema)
  scripts/threat_model_injector.py                        (simplify to renderer)
  commands/mine.md                                        (SOP updates)
  settings.json                                           (wire new gates)

DEPRECATED (Phase 4):
  agents/attack-boundary.md
  agents/attack-state.md
  agents/attack-semantic.md
```

---

## 12. Open questions

1. **gRPC client setup for `cross_surface` pattern**: do we ship a per-DB gRPC helper, or require attack-spec-executor to write client code? *Lean: ship helpers in `lib/clients/<db>_grpc.py`.*
2. **ProbeSpec versioning**: if schema evolves, do old threat_model.json files break? *Lean: schema_version field + migrator.*
3. **How to express bug shapes that cross multiple ProbeSpecs** (e.g. "race condition that also causes drift")? *Lean: emit two ProbeSpecs, link by `related_spec_ids`.*
4. **Should `boundary_value` always be derivable from contract constraints, or can threat-modeler supply its own value table?** *Lean: threat-modeler supplies; contract is for adherence verification.*

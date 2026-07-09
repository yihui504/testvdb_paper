# ProbeSpec DSL — Comprehensive Design

**Date**: 2026-07-05
**Status**: Design (extends `2026-07-05-spec-driven-mining-pipeline.md` §4-§6)
**Decisions locked**: Q1=A (fixed DSL vocabulary), Q2=A (atomic kinds only)

---

## 1. Design goals

1. **Expressive enough** to cover 6 probe patterns × typical scenarios (~30+ test shapes)
2. **Structured enough** for static adherence checking (every kind → AST features)
3. **DB-agnostic vocabulary**, DB-specific values (rendered per-DB by templates)
4. **Non-Turing-complete** — no control flow, no arbitrary code, no recursive refs
5. **Extensible by explicit pipeline change** — adding kinds/patterns requires schema bump + renderer + adherence rule + registry doc

---

## 2. ProbeSpec top-level schema

```yaml
schema_version: "1.0"   # required, for migrator

id: <string, unique>
bug_shape_tags: [<string>]            # informational only, pipeline never branches on this
rationale: <string>

target:
  contract_endpoint: <string>         # ref: structured_contract.json:endpoint_registry[idx]
  default_transport: rest | grpc

invariant: <string>                   # natural-language correct behavior (doc only, not executed)

probe_pattern:
  type: single_request | sequential | concurrent |
        drift_after_mutation | cross_surface | boundary_value
  setup: [<SetupStep>]
  execution: <ExecutionSpec>          # shape determined by `type` (see §5)
  synchronization: <SyncSpec>
  verification: [<VerificationStep>]

oracle:
  defect_found_when: <string>         # natural language, translated by template
  false_positive_when: <string>

evidence:
  historical_refs: [<string>]
  doc_refs: [<string>]
  expected_doc_behavior: <string>
```

---

## 3. Vocabularies

### 3.1 Setup vocabulary (8 kinds)

| kind | params | semantics |
|---|---|---|
| `create_collection` | `name`, `vectors_config?`, `sparse_vectors_config?`, `quantization_config?`, `sharding_method?`, `replication_factor?`, `write_consistency_factor?`, `on_disk_payload?`, `hnsw_config?`, `optimizers_config?` | idempotent: drop-then-create |
| `drop_collection` | `name` | idempotent |
| `pre_populate` | `collection`, `points: [{id, vector, payload?}] \| generator`, `wait: bool` | bulk upsert |
| `create_payload_index` | `collection`, `field`, `field_schema`, `wait: bool` | field_schema ∈ {keyword, integer, float, bool, geo, datetime, text, uuid, match_text} |
| `drop_payload_index` | `collection`, `field`, `wait: bool` | |
| `create_alias` | `alias`, `target_collection` | |
| `update_collection_config` | `collection`, `params` | e.g. `{hnsw_config: {m: 16}}` |
| `setup_quantization` | `collection`, `config`, `wait: bool` | |

### 3.2 Operation vocabulary (10 kinds)

Each op has `id` (string, unique within ProbeSpec) for verification references.

| op | params | notes |
|---|---|---|
| `upsert` | `collection`, `id`, `vector`, `payload?`, `wait: bool` | single point |
| `upsert_batch` | `collection`, `points \| generator`, `wait: bool` | bulk; atomicity semantics declared in `oracle` |
| `delete` | `collection`, `id?` \| `filter`, `wait: bool` | by-id or by-filter |
| `set_payload` | `collection`, `id`, `payload`, `wait: bool` | merge payload |
| `clear_payload` | `collection`, `id`, `wait: bool` | remove all payload |
| `search` | `collection`, `vector \| named_vector`, `filter?`, `limit?`, `offset?`, `params?`, `with_payload?`, `with_vector?` | ranked results |
| `query` | `collection`, `query`, `using?`, `filter?`, `limit?`, `prefetch?`, `params?` | unified query API |
| `count` | `collection`, `filter?`, `exact: bool` | returns integer |
| `scroll` | `collection`, `filter?`, `limit?`, `offset?`, `with_payload?`, `with_vector?` | paginated scan |
| `snapshot` | `collection`, `action: create \| restore \| delete`, `location?`, `wait: bool` | |

### 3.3 Verification vocabulary (12 kinds)

Each step has `severity` ∈ `{critical, major, minor}` for verdict aggregation (§7).

| kind | params | checks |
|---|---|---|
| `count_is` | `collection`, `filter?`, `exact: bool`, `op: eq\|le\|ge\|gt\|lt`, `value: int`, `tolerance?: int` | filtered count comparison |
| `point_present` | `collection`, `id` | point found in any read |
| `point_absent` | `collection`, `id` | point not in any read |
| `vector_equals` | `collection`, `id`, `expected: vector`, `tolerance?: float` | stored vector matches |
| `vector_in_set` | `collection`, `id`, `candidates: [vector]` | stored vector ∈ candidates |
| `payload_equals` | `collection`, `id`, `key`, `value` | payload field matches |
| `no_5xx` | `op_ids?: [string]` (default: all) | no op returned 5xx |
| `no_status` | `op_ids: [string]`, `statuses: [int]` | listed ops avoided given statuses |
| `status_is` | `op_id: string`, `expected: int` | specific op returned expected status |
| `body_contains` | `op_id: string`, `substring \| regex` | response body matches |
| `two_reads_agree` | `read_a_id`, `read_b_id`, `op: eq\|le\|ge`, `value?: int`, `tolerance?: int` | for drift pattern |
| `responses_equal` | `op_a_id`, `op_b_id`, `ignore_fields?: [string]` | for cross_surface |

---

## 4. Data generators

| generator | params | produces |
|---|---|---|
| `random` | `dim`, `seed?`, `count` | uniform random unit vectors |
| `zeros` | `dim`, `count` | zero vectors (distance=0 test) |
| `ones` | `dim`, `count` | ones |
| `extreme` | `type: nan\|inf\|null\|max_float\|min_float`, `dim`, `count` | invalid-value probes |
| `sequence` | `start`, `count`, `dim` | unique sequential ids with deterministic vectors |

Generators are deterministic (seeded). Same ProbeSpec → same data.

---

## 5. ExecutionSpec — per pattern

### 5.1 `single_request`
```yaml
execution:
  op: <Operation>            # exactly one
```

### 5.2 `sequential`
```yaml
execution:
  ops: [<Operation>]         # ordered
```

### 5.3 `concurrent`
```yaml
execution:
  worker_groups:
    - name: <string>          # e.g. writers, readers
      size: <int>             # thread count
      rounds: <int>           # iterations per worker
      ops: [<Operation>]      # round-robin per round
```

### 5.4 `drift_after_mutation`
```yaml
execution:
  reads_before: [<Operation>]   # each has an id
  mutation: <Operation>
  reads_after: [<Operation>]    # mirror reads_before; verification compares by id
```

### 5.5 `cross_surface`
```yaml
execution:
  transports: [<string>]        # required, e.g. ["rest", "grpc"]
  op: <Operation>               # rendered via each transport
```

### 5.6 `boundary_value`
```yaml
execution:
  base_op: <Operation template>     # op with {{slot}} placeholders
  cases:
    - name: <string>
      slot_values: {<slot>: <value>}
      expected:
        status: <int>?
        body_contains: <string>?
        verdict: defect | no_defect | ambiguous
```

---

## 6. Synchronization spec

```yaml
synchronization:
  after_setup: wait_quiesce | none         # default: wait_quiesce
  between_ops: wait_quiesce | none          # for sequential; default: none
  after_execution:
    method: join_all | barrier | sleep
    quiesce_seconds: <int>
    wait_for_indexing: <bool>               # poll collection state until indexed
```

---

## 7. Verification aggregation → verdict

Each step produces `{passed: bool, severity: str, detail: str}`. Template collects all and applies:

```python
def aggregate(results):
    failed = [r for r in results if not r.passed]
    critical = [r for r in failed if r.severity == "critical"]
    major = [r for r in failed if r.severity == "major"]
    minor = [r for r in failed if r.severity == "minor"]

    if critical: return "VERDICT_FOUND"          # any critical = bug
    if len(major) >= 2: return "VERDICT_FOUND"   # 2+ majors = strong signal
    if len(major) == 1 or len(minor) >= 3: return "AMBIGUOUS"
    return "NO_DEFECT"
```

All steps run regardless of prior failures (no fail-fast) — diagnostic value.

---

## 8. Adherence rules

### Per-pattern (orthogonal to kinds)
```python
PROBE_PATTERN_FEATURES = {
    "single_request": {"ops_required": 1, "verification_min": 1},
    "sequential": {"ops_required_min": 2, "verification_min": 1, "ordering_enforced": True},
    "concurrent": {
        "must_contain_ast_any": ["threading.Thread", "asyncio.create_task", "concurrent.futures"],
        "must_contain_call": "join",
        "worker_groups_min": 1,
        "verification_min": 1,
        "post_quiesce_state_read": True,
    },
    "drift_after_mutation": {
        "reads_before_min": 1, "reads_after_min": 1, "mutation_required": True,
        "must_use_verification": ["two_reads_agree"],
    },
    "cross_surface": {
        "transports_required_min": 2,
        "must_use_verification": ["responses_equal"],
        "transport_clients_present": ["rest", "grpc"],
    },
    "boundary_value": {"cases_min": 3, "parametrized_table_required": True},
}
```

### Per-kind (orthogonal)
```python
KIND_FEATURES = {
    "upsert":  {"must_call_endpoint": "PUT .*points"},
    "delete":  {"must_call_endpoint_any": ["POST .*points/delete", "DELETE .*points"]},
    "search":  {"must_call_endpoint": "POST .*points/search"},
    # ... one per kind
}
```

Static check: AST contains a `requests.<verb>(path)` matching the regex.

---

## 9. Cross-DB rendering contract

Every `templates/probe_patterns/<type>.py.tmpl` must:

1. Read env: `TESTVDB_DB_URL`, `TESTVDB_TARGET`, `TESTVDB_PROBE_SPEC` (JSON)
2. Embed ProbeSpec as header comment: `# PROBE_SPEC: <json>` (for adherence checker)
3. For each kind, dispatch to `lib/clients/<db>/<vocab>.py` helper
4. Output `VERDICT: <FOUND|NO_DEFECT|AMBIGUOUS>` and exit code 0/1/2
5. Be deterministic — same inputs → same script

`lib/clients/<db>/<vocab>.py` is the **only** DB-specific code. Acceptance criterion #5 holds.

---

## 10. Schema versioning & migration

- `schema_version: "1.0"` required at ProbeSpec root
- Add fields: minor bump (1.0 → 1.1); old specs still valid
- Remove/rename: major bump (1.x → 2.0); migrator required
- `scripts/probe_spec_migrate.py` reads old → writes new

---

## 11. Extensibility protocol

### Add a new kind
1. Add to `lib/threat_model/schema.py` vocabulary
2. Implement `lib/clients/<db>/<vocab>.py` per DB
3. Add to `KIND_FEATURES` in `spec_adherence.py`
4. Update `docs/specs/probe-patterns-registry.md`
5. Bump schema minor

### Add a new pattern type
1. Define execution schema (in this doc §5)
2. Write `templates/probe_patterns/<type>.py.tmpl`
3. Add to `PROBE_PATTERN_FEATURES` in `spec_adherence.py`
4. Add to registered types in `threat_model_completeness.py`
5. Update registry doc
6. Bump schema minor

Until protocol complete, completeness verifier rejects ProbeSpecs using unregistered kinds/patterns.

---

## 12. Coverage matrix — patterns × scenarios

| Scenario | Pattern | Key vocab | Covered |
|---|---|---|---|
| timeout=-1 accepted | boundary_value | upsert (slot=timeout) + status_is | ✅ |
| group_size inconsistency | sequential | search + two_reads_agree | ✅ |
| async invalid named vector drops | sequential | upsert(wait=false) + point_absent + scroll | ✅ |
| approx count ignores filter | drift_after_mutation | count(exact=true) → upsert → count(exact=false) + two_reads_agree | ✅ |
| concurrent delete+upsert race | concurrent | writers+deleters; count_is≤1 + vector_in_set | ✅ |
| payload index drift | drift_after_mutation | pre_populate → search → create_payload_index → search → two_reads_agree | ✅ |
| REST vs gRPC search diff | cross_surface | search via [rest,grpc] + responses_equal | ✅ |
| snapshot + concurrent write | concurrent | writers + snapshot creator; no_5xx | ✅ |
| empty vector panic | boundary_value | upsert(vector=[]) + status_is | ✅ |
| large batch OOM | boundary_value | upsert_batch(slot=count) + no_5xx | ✅ |

All 10 historical scenarios expressible. New inexpressible scenario = signal that a new pattern/kind is needed (§11).

---

## 13. Worked example — concurrent race

```yaml
schema_version: "1.0"
id: bs02-race-concurrent-delete-upsert
bug_shape_tags: [concurrency-data-race-point-mutation]
rationale: >
  BS-02 + PR #6593 historical: concurrent delete+upsert on same id should leave
  collection in {0,1} point state, with survivor (if any) having a submitted vector.

target:
  contract_endpoint: "PUT /collections/{name}/points"
  default_transport: rest

invariant: >
  For a fixed (collection, point_id), after concurrent {upsert, delete} quiesce,
  final state must have count ∈ {0, 1} and if count == 1 the stored vector must
  equal one of the submitted vectors.

probe_pattern:
  type: concurrent
  setup:
    - kind: create_collection
      name: race_t1
      vectors_config: {size: 4, distance: Cosine}
    - kind: pre_populate
      collection: race_t1
      points: [{id: 1, vector: [0.5, 0.5, 0.5, 0.5]}]
      wait: true
  execution:
    worker_groups:
      - name: writers
        size: 10
        rounds: 50
        ops:
          - op: upsert
            id: w_upsert
            params: {collection: race_t1, id: 1, vector: [0.1, 0.2, 0.3, 0.4], wait: false}
      - name: deleters
        size: 10
        rounds: 50
        ops:
          - op: delete
            id: d_delete
            params: {collection: race_t1, id: 1, wait: false}
  synchronization:
    after_execution: {method: join_all, quiesce_seconds: 2, wait_for_indexing: false}
  verification:
    - kind: count_is
      collection: race_t1
      exact: true
      op: le
      value: 1
      severity: critical
    - kind: vector_in_set
      collection: race_t1
      id: 1
      candidates: [[0.5,0.5,0.5,0.5], [0.1,0.2,0.3,0.4]]
      severity: major
    - kind: no_5xx
      severity: critical

oracle:
  defect_found_when: >
    count > 1 (duplication) OR (count == 1 AND vector not in candidates)
    OR any op returned 5xx
  false_positive_when: test infra network reset; re-run to confirm

evidence:
  historical_refs: ["PR #6593"]
  doc_refs: ["raw_knowledge.md:L200"]
  expected_doc_behavior: >
    Upsert + delete on same id should serialize via WAL; final state deterministic.
```

---

## 14. Worked example — drift

```yaml
schema_version: "1.0"
id: bs03-payload-index-drift-after-write
bug_shape_tags: [payload-index-state-drift]
rationale: BS-03 / issues #9373 #7132.

target:
  contract_endpoint: "POST /collections/{name}/points/search"
  default_transport: rest

invariant: >
  A filtered count must return the same number of points regardless of
  whether a payload index exists for the filtered field.

probe_pattern:
  type: drift_after_mutation
  setup:
    - kind: create_collection
      name: drift_t1
      vectors_config: {size: 4, distance: Cosine}
    - kind: pre_populate
      collection: drift_t1
      points: {generator: sequence, params: {start: 1, count: 100, dim: 4}}
      wait: true
  execution:
    reads_before:
      - op: count
        id: r1_pre
        params: {collection: drift_t1, filter: {must: [{key: v, range: {gte: 50}}]}, exact: true}
    mutation:
      op: create_payload_index
      id: m_idx
      params: {collection: drift_t1, field: v, field_schema: integer, wait: true}
    reads_after:
      - op: count
        id: r1_post
        params: {collection: drift_t1, filter: {must: [{key: v, range: {gte: 50}}]}, exact: true}
  synchronization:
    after_execution: {method: sleep, quiesce_seconds: 1, wait_for_indexing: true}
  verification:
    - kind: two_reads_agree
      read_a_id: r1_pre
      read_b_id: r1_post
      op: eq
      severity: critical
    - kind: count_is
      collection: drift_t1
      filter: {must: [{key: v, range: {gte: 50}}]}
      exact: true
      op: eq
      value: 50
      severity: major

oracle:
  defect_found_when: >
    r1_pre.count != r1_post.count (index changed filtered result)
    OR final count != 50 (data corruption)

evidence:
  historical_refs: ["issue #9373", "issue #7132"]
```

---

## 15. Open design issues (need decision)

1. **Op id uniqueness scope**: per ProbeSpec? per execution block? — *Rec: per ProbeSpec.*
2. **Filter schema**: qdrant-style DSL as universal, or abstract filter model rendered per DB? — *Rec: abstract model.*
3. **Vector format**: dense `[float]`, named `{name: [float]}`, sparse `{indices, values}`, multivector `[[float]]`? — *Rec: unified `vector` field shaped by content.*
4. **Error semantics for setup ops**: setup failure = ProbeSpec design error or test defect? — *Rec: design error; abort with SCRIPT_ERROR.*
5. **Shared setup across ProbeSpecs**: a heavy pre_populate is wasteful to repeat. — *Rec: out of scope v1; each spec hermetic.*
6. **Transport client availability**: cross_surface needs gRPC; what if DB lacks it? — *Rec: completeness verifier rejects for DBs lacking required transports.*
7. **Verification cross-collections**: alias routing needs `scroll` over alias. — *Rec: op params accept `collection_or_alias`.*
8. **`boundary_value` slot templating**: JSON value substitution or path-based? — *Rec: JSON-path, validated against op schema.*
9. **Determinism in concurrent pattern**: random scheduling → varying results. — *Rec: declare `expected_determinism: high|medium|low` for flake handling.*
10. **Generator seeding**: explicit seed for reproducibility? — *Rec: required when any generator used.*

---

## 16. Deliberately NOT supported

To keep adherence checkable and pipeline DB-agnostic:

- **No control flow** (no if/else, no loops in ProbeSpec — loops inside templates via pattern semantics)
- **No arbitrary code** (no `custom_script` kind — escape hatch is §11 extension)
- **No cross-ProbeSpec references** (hermetic specs; shared setup deferred)
- **No inline timed waits** (timing in `synchronization` only)
- **No assertions on natural language** (`invariant` is documentation, not executed)
- **No client-side result computation** (no expression language; use `body_contains` regex for simple cases; complex math → propose new verification kind)

These restrictions are the price of guaranteed adherence checking. Real ProbeSpecs needing them = §11 extension signal.

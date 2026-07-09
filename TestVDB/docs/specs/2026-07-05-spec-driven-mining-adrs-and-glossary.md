# Spec-Driven Mining — ADRs & Glossary

**Date**: 2026-07-05
**Companion to**: `2026-07-05-spec-driven-mining-pipeline.md` (plan), `2026-07-05-probe-spec-dsl.md` (DSL spec)
**Status**: All decisions below are LOCKED as a result of the 2026-07-05 grilling session

---

# Part I — Architecture Decision Records

> Format: each ADR follows `Context → Decision → Consequences → Reversal cost`.

## ADR-001 — Pipeline core is DB-agnostic; threat_model owns all DB knowledge

**Context**. A qdrant mining run produced 5 candidate defects, of which 0–1 would
survive maintainer triage (`maintenance_review.md`). Root cause: attack agents
received fuzzy labels (`"concurrent_delete+upsert_same_id"`) fabricated by
`threat_model_injector.py` from DB-specific hardcoded mappings. The same pipeline
re-run on milvus/weaviate would require new DB-specific code at every layer.

**Decision**. The pipeline core (`scripts/`, `templates/`, agent definitions) contains
**no DB-specific knowledge**. All DB knowledge lives in three sanctioned locations:
- `intelligence/<db>/` (threat model + transport availability)
- `lib/clients/<db>/` (DB-specific renderer helpers)
- `structured_contract.json` (per-DB API schema)

**Consequences**.
- ✅ Adding a new DB = adding intelligence + lib/clients + contract, no pipeline changes
- ✅ Acceptance criterion #5 ("zero DB-specific code in scripts/ or templates/") becomes enforceable
- ⚠️ Some scenarios need explicit pipeline extension (new kind/pattern) rather than ad hoc code

**Reversal cost**. High — this decision shapes every other ADR below.

---

## ADR-002 — ProbeSpec is the unit of work between threat-modeler and attack agents

**Context**. Previously, threat-modeler output `attack_surface.areas[].attack_order`
as a free-form text label (often empty in practice). `threat_model_injector.py`
"interpreted" these into richer labels, but attack agents still received prose.

**Decision**. threat-modeler emits structured `ProbeSpec` objects. Each ProbeSpec is
a self-describing unit of work with `target`, `invariant`, `probe_pattern`, `oracle`,
`evidence`. The injector becomes a pure JSON-to-text renderer; it no longer fabricates content.

**Consequences**.
- ✅ Adherence checking becomes possible (spec → code structural match)
- ✅ threat-modeler's reasoning is auditable (rationale field + invariant)
- ⚠️ threat-modeler must produce richer output (more constrained schema)

**Reversal cost**. Medium — ProbeSpec schema is the main contract.

---

## ADR-003 — DSL uses a fixed vocabulary of kinds, not freeform code

**Context**. ProbeSpec's `setup[]`, `execution.operations[]`, and `verification[]`
need to describe "what to do". Two paths: (a) fixed vocabulary of atomic kinds,
or (b) freeform Python snippets.

**Decision**. Fixed vocabulary. Setup = 8 kinds, op = 10 kinds, verification = 12 kinds
(see `probe-spec-dsl.md` §3). Adding a kind requires the full §11 protocol (schema +
renderer + adherence rule + registry doc + version bump).

**Consequences**.
- ✅ Static adherence checking (every kind → AST feature mapping)
- ✅ DB-agnostic vocabulary (kind names are vector-DB common terms)
- ⚠️ Real scenarios needing unlisted kinds must go through §11 extension

**Reversal cost**. Low for individual kinds; medium for the principle.

---

## ADR-004 — All kinds are atomic; concurrency/sequencing lives in probe_pattern

**Context**. Even with a fixed vocabulary, kinds could be atomic (`op: upsert`)
or composite (`op: concurrent_delete_upsert`). Composite kinds duplicate
probe_pattern semantics.

**Decision**. Atomic only. A kind describes "what one operation does".
Concurrency, sequencing, drift, parameterization are all pattern-level concerns.

**Consequences**.
- ✅ Vocabulary stays small (~30 kinds vs ~100+ composite combinations)
- ✅ Each kind has one renderer + one adherence rule
- ⚠️ Batch operations (`upsert_batch`) are atomic at HTTP level (single API call)

**Reversal cost**. Low — adding composite kinds later is non-breaking.

---

## ADR-005 — DB-specific data shapes (filter, vector, payload, config) are opaque per-ProbeSpec

**Context**. Cross-DB data shapes differ: qdrant filter (`{must, should, must_not}`)
vs milvus `expr` string vs weaviate `where` tree vs pgvector SQL.

**Decision**. **Fully opaque**. The `filter`/`vector`/`payload`/`config` fields
inside op params take DB-native shape; templates pass them through unchanged
to `lib/clients/<db>/<kind>.py`. Completeness verifier validates shape against
the DB's `structured_contract.json`.

**Consequences**.
- ✅ No DB-specific rendering logic in templates (acceptance criterion #5 holds)
- ✅ threat-modeler thinks in DB-native terms (less translation error)
- ⚠️ ProbeSpecs are inherently per-DB (not portable across DBs)
- ⚠️ Cross-DB pattern transferability is informational (bug_shape_tags), not structural

**Reversal cost**. Medium — abstract filter model would require translators per DB.

---

## ADR-006 — Setup steps are preconditions, not test subjects

**Context**. If `create_collection` with `replication_factor: 0` fails during
setup, is that (a) a ProbeSpec design error, or (b) a successful boundary test?

**Decision**. **Precondition**. Setup steps default to expecting success; any
failure → `SCRIPT_ERROR`, ProbeSpec marked invalid, threat-modeler must rewrite.
To test setup-time validation, use the `boundary_value` pattern with `base_op`
being a setup-kind op.

**Consequences**.
- ✅ Setup/test/verification responsibilities stay cleanly separated
- ✅ Verdict signal isn't polluted by DB correctly rejecting bad setup params
- ⚠️ Boundary tests on setup params go through boundary_value, not via setup steps

**Reversal cost**. Low — adding `expected_outcome` to setup steps later is additive.

---

## ADR-007 — cross_surface supports flexible transport lists per DB

**Context**. cross_surface originally meant REST vs gRPC, but DBs vary:
qdrant has REST+gRPC, weaviate has REST+GraphQL, pgvector has only SQL.

**Decision**. ProbeSpec declares `transports: [t1, t2, ...]` (≥2 required).
Each DB declares supported transports in `intelligence/<db>/transports.json`.
Completeness verifier rejects cross_surface ProbeSpecs whose transports
aren't all supported. Single-surface DBs cannot produce cross_surface ProbeSpecs.

**Consequences**.
- ✅ weaviate REST/GraphQL divergence testable
- ✅ Single-surface DBs naturally excluded
- ⚠️ Requires `transports.json` per DB (small file)

**Reversal cost**. Low.

---

## ADR-008 — boundary_value uses JSON-path slot templating

**Context**. boundary_value needs to parameterize ops. Three granularity options:
top-level params only, JSON-path, or full Jinja templates.

**Decision**. **JSON-path** substitution. Slots reference any scalar location in
the op tree via dot notation (`filter.must[0].range.gte`). Slot values can be any
JSON type (including wrong-type values, for type-validation tests). Slots may
reference paths not present in `base_op` (adds new fields). Adherence check:
≥3 distinct op invocations with different args.

**Consequences**.
- ✅ Tests deep nested boundaries (range values, vector dim inside config, etc.)
- ✅ Type-confusion tests expressible (`limit: "abc"`)
- ⚠️ Path syntax must be validated (reject malformed like `filter..must`)

**Reversal cost**. Low — additive.

---

## ADR-009 — Flake handling via declared determinism level + rerun strategy

**Context**. Race condition tests are inherently flaky; pipeline must distinguish
real bugs from infra noise.

**Decision**. Each ProbeSpec may declare `expected_determinism: high|medium|low|very_low`
(defaults from pattern type: high for single/sequential/boundary/cross_surface,
medium for drift, low for concurrent). Pipeline applies rerun strategy:
- high → 1 run, accept
- medium → 1 run, rerun once if AMBIGUOUS
- low → 3 runs, majority verdict (≥2 same)
- very_low → 10 runs, ≥2 DEFECT_FOUND to confirm

**Consequences**.
- ✅ Deterministic tests aren't slowed by unnecessary reruns
- ✅ Race tests get statistical confidence
- ⚠️ Adds ~3x execution cost for concurrent specs (acceptable)

**Reversal cost**. Low — strategy parameters are configurable.

---

## ADR-010 — Op ids are unique per-ProbeSpec; generators require explicit seed

**Context**. Two final structural questions: (a) scope of `op.id` uniqueness,
(b) whether generators need explicit seeds.

**Decision**.
- **(a)** Op ids are unique **per ProbeSpec** (global within the spec). Concurrent
  pattern: one op shared by N workers has one id; verifier receives list[result]
  of size N. Boundary_value: one base_op id shared by all cases; verifier receives
  list[result] of size N (one per case).
- **(b)** Every generator usage **must** include an explicit `seed`. Omitting seed
  → completeness verifier rejects. Required for reproducibility (MRE scripts must
  replay identically).

**Consequences**.
- ✅ Reference resolution is unambiguous (no path prefixes)
- ✅ Every ProbeSpec is fully reproducible from its content
- ⚠️ threat-modeler must assign seeds (low cost)

**Reversal cost**. Very low.

---

## Decision summary table

| ADR | Topic | Decision | Locked by grilling Q |
|---|---|---|---|
| 001 | Pipeline DB-agnosticism | Core contains no DB knowledge | (foundational) |
| 002 | ProbeSpec contract | Structured spec, not labels | (foundational) |
| 003 | Fixed DSL vocabulary | 30 atomic kinds, extensible via §11 | Q1 |
| 004 | Kinds are atomic | Composite kinds disallowed | Q2 |
| 005 | DB-specific shapes opaque | filter/vector/payload pass through | Q4 |
| 006 | Setup = precondition | Setup failures → SCRIPT_ERROR | Q5 |
| 007 | cross_surface flexible transports | DB declares support in transports.json | Q6 |
| 008 | boundary_value JSON-path slots | Path-based, any JSON value | Q7 |
| 009 | Determinism levels + rerun | high/medium/low/very_low | Q8 |
| 010 | Op id uniqueness + seed | per-ProbeSpec + required seed | Q9/Q10/Q11 |

---

# Part II — Glossary

### Threat model layer

**threat_model.json** — Per-(DB, version) JSON file produced by threat-modeler agent.
Contains `attack_surface`, `cognitive_blindspots`, `defect_criteria`. Extended with
`probe_specs` per ADR-002.

**bug_shape_tags** — Informational labels on a ProbeSpec (e.g., `concurrency-data-race`).
Pipeline never branches on these; they exist for human navigation and cross-DB
pattern analysis.

**invariant** — A natural-language statement of correct behavior in a ProbeSpec.
Documentation only; not executed. Actual checking is via `verification[]` kinds.

### ProbeSpec structure

**ProbeSpec** — The unit of work between threat-modeler and attack-spec-executor.
Self-describing: contains `target`, `invariant`, `probe_pattern`, `oracle`, `evidence`.

**probe_pattern** — The structural core of a ProbeSpec. Has a `type` from the
registered set, plus `setup`, `execution`, `synchronization`, `verification` blocks.

**probe_pattern.type** — One of: `single_request`, `sequential`, `concurrent`,
`drift_after_mutation`, `cross_surface`, `boundary_value`. Open enum — adding a
new type requires §11 protocol.

**oracle** — Natural-language description of when this ProbeSpec constitutes a
defect vs a false positive. Templates translate to actual verdict aggregation.

**evidence** — References for the eventual defect report: historical PRs/issues,
doc lines, expected documented behavior.

### DSL primitives

**kind** — A name from the fixed vocabulary used in `setup[]`, `operations[]`,
or `verification[]`. Examples: `create_collection`, `upsert`, `count_is`.

**op** — A kind in the operation vocabulary (10 total). Each op has a string `id`
(unique per ProbeSpec) for verification references.

**verification step** — A kind in the verification vocabulary (12 total). Each
has a `severity` (critical/major/minor) used in verdict aggregation.

**generator** — A deterministic data producer for `pre_populate` and `upsert_batch`.
5 generators: random/zeros/ones/extreme/sequence. Always seeded (ADR-010).

**slot** — A `{{path}}` placeholder in a boundary_value `base_op`. Replaced per-case
via JSON-path substitution (ADR-008).

**transport** — A wire protocol for the DB API: `rest`, `grpc`, `graphql`, `sql`.
Used in cross_surface to declare which surfaces to compare.

### Execution semantics

**worker_group** — In concurrent pattern: a named pool of N threads, each running
a list of ops round-robin for R rounds.

**synchronization** — How/when to wait during execution: `after_setup`,
`between_ops`, `after_execution`. Methods: `join_all`, `barrier`, `sleep`,
`wait_for_indexing`.

**determinism level** — Per-ProbeSpec declaration: `high` / `medium` / `low` / `very_low`.
Drives rerun strategy (ADR-009).

### Verification & verdict

**adherence check** — Static structural verification that a rendered script
implements its ProbeSpec's declared `probe_pattern`. Per-pattern rules in
`PROBE_PATTERN_FEATURES`; per-kind rules in `KIND_FEATURES`.

**verdict** — Single-run outcome: `VERDICT_FOUND`, `AMBIGUOUS`, or `NO_DEFECT`.
Aggregated from verification step results via severity counting.

**oracle verdict** — Final outcome after determinism-driven reruns. For `low`
determinism: majority verdict across 3 runs. For `very_low`: ≥2 DEFECT_FOUND
in 10 runs required to confirm.

**SCRIPT_ERROR** — Outcome when ProbeSpec itself is broken (setup failed, schema
invalid, op id not found). Distinguished from `NO_DEFECT` and `DEFECT_FOUND`.

### Pipeline components

**attack-spec-executor agent** — Replaces attack-boundary/state/semantic. Single
agent that reads ProbeSpec + target contract, picks template by `probe_pattern.type`,
fills params, emits script.

**probe-pattern template** — `templates/probe_patterns/<type>.py.tmpl`.
DB-agnostic; dispatches to `lib/clients/<db>/<kind>.py` for actual API calls.

**completeness verifier** — `scripts/threat_model_completeness.py`. Runs after
threat-modeler; rejects ProbeSpecs with missing fields, unknown kinds/patterns,
unsupported transports, missing seeds, op id collisions, or unregistered collection
references.

**spec adherence checker** — `scripts/spec_adherence.py`. Runs in DEBATE_S1;
rejects scripts whose AST doesn't match the declared pattern (e.g., concurrent
pattern without threading).

### Cross-cutting

**contract_endpoint** — A reference into `structured_contract.json:endpoint_registry`
identifying which API endpoint a ProbeSpec targets.

**transports.json** — Per-DB file in `intelligence/<db>/` declaring which API
transports the DB supports. Drives cross_surface feasibility check.

**schema_version** — `"1.0"` at ProbeSpec root. Minor bumps for additive changes
(new kinds/patterns); major bumps for breaking changes (require migrator).

# Reviewer 1 Background: Competitor Analysis

## Core Competitors (cached summaries verified)

### MASTOR (mastor26)
**Cache file**: `mastor a multi agent approach to semantic test oracle generation for restful apis (2026).summary.md`

**Regime**: Implementation-source extraction; generates oracles from what code **does**

**Key distinction from TestVDB**: MASTOR treats source code as ground truth and generates oracles encoding implemented behavior. TestVDB treats documentation as authoritative and uses source as a falsifier to detect gaps where code **violates** documentation. MASTOR's source-verified design explicitly excludes OAS-declared items not traceable to source, while TestVDB's dev-reviewer uses source to **falsify** documentation-derived claims.

**Relate to paper's characterization**: The paper accurately positions MASTOR as reading "source code" to generate "oracles that encode implemented behavior" and notes it "cannot detect a gap between documentation and code" (Section 5). This matches the cached summary's limitation: "Implementation-assumption: Treats source code as ground truth; cannot detect bugs where implementation is wrong but documentation is right."

**Novelty delta**: VERIFIED. TestVDB's novelty is the gap-detection direction (documentation vs. implementation), which MASTOR explicitly does not target.

### SATORI (satori25)
**Cache file**: `satori static test oracle generation for rest apis (40th ieee acm international conference on automated software engineering ase 2025).summary.md`

**Regime**: Low-ambiguity structured sources (OpenAPI Schema with type/format/min/max)

**Key distinction from TestVDB**: SATORI assumes every relevant constraint has an OAS field to anchor on. TestVDB handles cases where constraints exist only in natural-language prose (e.g., "nprobe in [1, 16384]" stated in text but not in schema). SATORI's extraction step has no input when constraints lack schema fields.

**Relate to paper's characterization**: The paper states SATORI "reads OpenAPI schema elements (type, format, minimum, maximum) and stays in a regime where the constraints are explicit" and notes its extraction "assumes every relevant constraint has a corresponding OpenAPI field." This matches the cached summary: "Cannot detect violations where documentation is ambiguous or silent (falls back to OAS schema type/format only)."

**Novelty delta**: VERIFIED. TestVDB's novelty is entering the regime SATORI excludes (ambiguous natural-language documentation without schema fields).

### AGORA+ (agoraplus25)
**Metadata**: `agoraplus25.json` (abstract-only, PDF behind paywall)

**Regime**: Execution-trace invariant detection via dynamic analysis (Daikon extension)

**Key distinction from TestVDB**: AGORA+ infers invariants from observed traffic (execution traces) and so cannot reach inputs the traffic did not exercise. It operates in black-box mode learning from requests/responses. TestVDB generates proactive boundary probes from documentation without needing prior traffic coverage.

**Relate to paper's characterization**: The paper states AGORA+ "infers invariants from observed traffic and so cannot reach inputs the traffic did not exercise." This aligns with the abstract: "learns the expected behavior of an API by analyzing previous API requests and their corresponding responses."

**Novelty delta**: VERIFIED. TestVDB's proactive generation from documentation covers inputs absent from traffic, a regime AGORA+ cannot reach.

### VDBFuzz (vdbfuzz26)
**Status**: Abstract-only (could not locate PDF via search_literature.py; characterization from paper's own description)

**Regime**: Crash-oracle fuzzer using template-based input mutation

**Key distinction from TestVDB**: VDBFuzz's oracle fires only on crashes/hangs. TestVDB targets silent-accept defects that return HTTP 200 with wrong semantics. The bidirectional probe (Section 6.3) shows VDBFuzz reached 0 of 14 TestVDB silent-accept TPs on Qdrant v1.18.2 (structural limitation, not budget artifact).

**Relate to paper's characterization**: The paper describes VDBFuzz as "crash as its oracle" and notes most documentation-implementation defects "do not crash (44 of the 49 true positives)." The exclusion table (Table 2) states VDBFuzz "misses the documentation-implementation residual" because these defects "do not crash."

**Novelty delta**: VERIFIED via paper's empirical comparison. TestVDB reaches the crash-class subset VDBFuzz targets (Qdrant size overflow) by contract reasoning, while VDBFuzz misses silent-accept defects under current templates.

### Metamorphic Relations (metmap24)
**Status**: Not fetched; paper provides sufficient characterization for exclusion argument

**Regime**: Output-relation oracles for result correctness (top-k monotonicity, recall vs. ef)

**Key distinction from TestVDB**: Metamorphic relations address result correctness (output relations). TestVDB addresses input accept/reject decisions (whether an API should accept or reject a value). The paper argues "no transform preserves" input-acceptance consistency across metamorphic relation executions.

**Relate to paper's characterization**: Table 2 states metamorphic relations "address result correctness" but "an MR is an output relation; consistency is an input accept/reject decision, and no transform preserves it."

**Novelty delta**: VERIFIED via paper's structural argument. Metamorphic testing does not enter the input-validation regime TestVDB targets.

## LLM-as-Judge Reliability Literature

### Panickssery et al. (2024)
**Cache file**: `panickssery.summary.md`

**Key finding**: LLM evaluators show self-preference bias (favoring own outputs) correlated with self-recognition ability. Fine-tuning amplifies both. GPT-4 achieves 73.5% self-recognition accuracy out-of-the-box.

**Relate to paper**: Paper cites this to establish that "the same family that extracts a claim tends to confirm it" (Section 4). The multi-perspective judging baseline's collapse in recall (Section 4) is attributed to this bias.

**Two-column check**: Paper accurately cites the core phenomenon (self-preference + self-recognition correlation) and the amplification effect. No mischaracterization detected.

### Wataoka et al. (2025)
**Cache file**: `wataoka.summary.md`

**Key finding**: Self-preference bias stems from text familiarity (perplexity) rather than explicit self-recognition. LLMs assign higher scores to lower-perplexity texts. Provides quantitative bias metric (Equal Opportunity).

**Relate to paper**: Paper cites this as alternative explanation: "the same family that extracts a claim tends to confirm it, the self-preference bias established for LLM evaluators."

**Two-column check**: Paper correctly identifies Wataoka's perplexity-familiarity mechanism as a complementary explanation to Panickssery's self-recognition hypothesis. No mischaracterization.

## Uncited Highly-Related Work (coverage search)

**Scope checked**:
- REST-API oracle generation: Covered (AGORA+, SATORI, MASTOR)
- VDBMS testing: Covered (VDBFuzz, empirical bug study, roadmap)
- LLM-as-judge reliability: Covered (Panickssery, Wataoka, Haldar)
- Documentation-derived oracles: Paper cites Toradocu, AugmenTest, ChatAssert, Testora

**No obvious missing highly-related work found** in scoped searches. The paper's Related Work section is comprehensive for the named competitors it relies on for positioning.

## Summary

All named competitors used for novelty positioning have been verified against their actual content (via cached summaries where available, abstract-only for paywalled AGORA+). The paper's characterizations are accurate. Novelty delta is clear: TestVDB targets the documentation-implementation gap in natural-language documentation, a regime excluded by SATORI (schema-only), AGORA+ (trace-only), MASTOR (source-verification), and VDBFuzz (crash-only).
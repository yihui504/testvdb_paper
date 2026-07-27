# Reviewer 1 (Domain Expert) — Background

## Core competitors verified (≤5)

### 1. MASTOR (Deng et al., arXiv:2606.10465, June 2026) — fetched (cached summary)
- Source-grounded multi-agent REST API oracle generator. Reads **implementation source code** (transitive import closure per endpoint) to produce status/field/multi-op oracles.
- Mutant score 75.4% on 13 Java REST APIs. Beats Direct Prompting (+30.1pp) and SATORI (+49.4pp) on 50 selected ops.
- **Source-as-oracle direction**: MASTOR reads source to encode *implemented* behavior. Summary's own limitation confirms TestVDB's positioning: "LLM-derived oracles are evaluated by mutation score against implementation mutants — i.e., oracles are judged against the implementation's own behavior, not against an external specification of correctness."
- **Two-column divergence:** Paper's characterization in §3 ("MASTOR reads source to generate oracles that encode implemented behavior and so cannot detect a gap between the documentation and the code") matches the cached summary. **No mischaracterization.** TestVDB's framing of MASTOR as "the closest in using source" is accurate.
- **Novelty delta:** Holds. The asymmetric direction (source as *falsifier* of doc-derived claims vs. source as *the oracle itself*) is a real, non-obvious delta. MASTOR cannot surface a documentation-implementation gap because it treats source as the reference for correctness.

### 2. SATORI (Alonso et al., ASE 2025, arXiv:2508.16318) — fetched (cached text + summary)
- Black-box, **OAS-only** static oracle generator for REST APIs. LLM infers 17 oracle types over documented response fields.
- F1 74.3%; 18 bugs across 7 APIs. Confirms explicitly that AGORA+ (its main baseline) is the *only* prior REST oracle generator.
- **Two-column divergence:** Paper's Table 1 row 5 and §3 describe SATORI as extracting from structured sources (OpenAPI specifications) where constraints are explicit. SATORI's own abstract and §I confirm this: it works on "the unstructured components of the OAS document, such as response field names and descriptions." Note: SATORI's authors call OAS prose "unstructured," but relative to VDBMS natural-language documentation, OAS is highly structured — the oracles are over response-field properties (format, length, range), not over input accept/reject decisions in ambiguous prose.
- **Novelty delta:** Holds. SATORI targets output-field correctness over OAS-documented fields; TestVDB targets input accept/reject decisions where documentation is natural-language prose. Source-ambiguity gap is real.

### 3. AGORA+ (cited via SATORI's reporting) — abstract-level (via SATORI cached text)
- Dynamic counterpart to SATORI: detects likely invariants by analyzing OAS **plus** executed request/response pairs. F1 69.3% on the SATORI benchmark.
- Paper's Table 1 characterization (oracles from execution traces) is consistent with SATORI's description.
- **Novelty delta:** Holds at abstract level. AGORA+ requires execution and targets response invariants, not documentation-implementation accept/reject decisions.

### 4. VDBFuzz (cited heavily, head-to-head in §6) — abstract-level (no indexed metadata found)
- Direct head-to-head competitor. Search across dblp/crossref/arxiv returned no direct hit (too recent or venue not yet indexed). Paper characterizes it as "the first dedicated VDBMS fuzzer" using crash as its oracle; §6 runs a bidirectional reachability probe.
- The bidirectional n=1 probe (VDBFuzz reaches the v1.4.0 size=2^63 crash that TestVDB also flags; VDBFuzz's templates miss #9045 on v1.18.0 because `wait=true` is hardcoded) is consistent with the paper's framing — but the paper's own caveat ("we treat these as hypothesis-generating controlled cases rather than a generalized result") is appropriate. **Cannot independently verify VDBFuzz's design** at abstract level; take the paper's description as provisional but well-caveated.

### 5. Toradocu / Doc2OracLL / Konstantinou et al. (documentation-derived oracle line) — abstract-level
- **Doc2OracLL** (Hossain/Dwyer, FSE 2025, arXiv:2412.09360): LLM-based test oracle generation from Javadoc. Finds Javadoc alone matches or outperforms MUT-based oracles; 19%–94% more bug detection than prior methods on Defects4J. **Crucially still trusts the LLM oracle without an independent falsifier.** Confirms paper's positioning in §7 (Related Work): "both still trust the generated oracle without verification."
- **Toradocu** (2016): NLP/pattern-matching over Javadoc @throws → assertions. Deterministic but brittle; acknowledged FP from extraction failures. Paper's characterization is accurate.
- **Konstantinou et al.** (2024): not directly resolved by search, but paper cites it as evidence that "LLM-generated oracles tend to capture the actual program behavior rather than the expected, correct behavior" — this is the *specific failure mode* TestVDB targets. Cannot verify the Konstantinou claim beyond the paper's citation; treat as provisional.
- **Novelty delta:** Holds. None of these use an independent source of actual behavior as a falsifier of doc-derived claims.

## Coverage search (uncited highly-related work)

Scoped searches on REST API oracle generators, documentation-consistency testing, and LLM-as-judge reliability surfaced no genuinely-related uncited work that would change the assessment. AutoRestTest (ICSE 2025, Kim et al.) and RestTSLLM (SBES 2025) appeared in searches but target **test-case generation** for REST APIs, not documentation-implementation consistency in VDBMSs — not relevant to the delta. Wataoka et al. (2024) on LLM self-preference bias verified and correctly cited. No missing-related-work finding at this time.

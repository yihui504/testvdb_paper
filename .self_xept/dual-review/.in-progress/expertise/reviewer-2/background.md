# Reviewer 2 Background - Specialty Areas

## Specialty Areas
1. **LLM-as-judge / evaluator reliability** (self-preference bias, self-inconsistency, hallucination)
2. **REST-API test-oracle extraction from structured sources** (OpenAPI/traces/source-as-oracle)

## Core Competitors Verified

### REST-API Oracle Extraction (Specialty b)

**SATORI (satori25)**: Static approach using LLM to analyze OpenAPI spec (field names/descriptions) → generates status/field oracles. F1 74.3% vs AGORA+ 69.3%. 18 bugs found. Key limitation: reads OAS, not implementation source—cannot detect gaps between documentation and code.

**MASTOR (mastor26)**: Multi-agent approach reading implementation source code → generates semantic oracles (status, field, cross-operation consistency). 75.4% mutation score, 69.9% vs SATORI 20.5% on same oracle types. Uses source as ground truth, not documentation.

**AGORA+ (agoraplus25)**: Dynamic invariant inference from execution traces. Requires diverse test suite; limited by traffic coverage. (Paywall—abstract only).

### LLM-as-Judge Reliability (Specialty a)

**Panickssery et al. (panickssery24)**: Established that LLM evaluators favor their own outputs (self-preference bias). Shows linear correlation between self-recognition capability and self-preference strength. GPT-4 shows 73.5% self-recognition accuracy.

**Wataoka et al. (wataoka24)**: Quantifies self-preference bias metric using Equal Opportunity framework. GPT-4 exhibits significant self-preference bias. Identifies perplexity as root cause—LLMs prefer lower-perplexity (more familiar) texts regardless of authorship.

**Haldar et al. (haldar25)**: "Rating Roulette: Self-Inconsistency in LLM-As-A-Judge Frameworks" (EMNLP 2025). Not yet available—abstract-only.

## Relational Verification (Two-Column Check)

### SATORI Characterization
Paper's claim (§3.2, Table 1 row 4): "reliable extraction from low-ambiguity structured sources; the ambiguous-prose regime is out of scope."

**Verdict**: ✓ ACCURATE. SATORI explicitly analyzes OpenAPI specs—field names and descriptions are semi-structured, not free-form prose. The paper correctly places SATORI in the low-ambiguity regime.

### MASTOR Characterization
Paper's claim: "source code... and so cannot detect a gap between documentation and code; TestVDB reads source as a falsifier of documentation-derived claims."

**Verdict**: ✓ ACCURATE. MASTOR reads source to encode implemented behavior—it documents what code does, not whether documentation matches. TestVDB's falsification direction is novel.

### Self-Preference Characterization
Paper's claim (§2.3, Panickssery citation): "the judge tends to confirm the extractor's claim."

**Verdict**: ✓ SUPPORTED. Panickssery shows self-recognition correlates with self-preference. If the same family extracts and judges, confirmation bias is expected. The paper's diagnosis is sound.

### Wataoka Root Cause
Paper's claim (§2.3): Self-preference "compounds hallucination: an over-strict extracted claim is more likely to be confirmed."

**Verdict**: ✓ STRENGTHENED by Wataoka. Wataoka shows the root cause is perplexity (familiarity), not authorship awareness per se. Over-strict claims from the same family share training distribution → lower perplexity for that family → higher confirmation. This reinforces the compound-effect claim.

## Missing Work (Coverage Gaps)

**Haldar et al. (haldar25)**: Self-inconsistency (same judge, same input, different runs). The paper addresses this indirectly through variance in single-run recall (15-78%) and the any-confirmed ensemble, but doesn't cite Haldar explicitly. This is a minor gap—empirical acknowledgment exists, but formal citation missing.

**AugmenTest (augmentest25)**: LLM-driven oracles from documentation. Cited in §4, but positioning could be clearer. AugmenTest infers oracles from available docs and verifies via runtime; TestVDB uses source as falsifier. The delta is real but could be more explicit.

## Coverage Search (Within Specialty)

Scoped search for "REST API test oracle LLM documentation 2024 2025" on arXiv:
- RESTOR (Zhou et al. 2026): Single-traffic oracle via LLM fine-tuning. Focuses on field selection from traces, not documentation interpretation. Out of scope for TestVDB's prose-interpretation regime.
- Various LLM-as-judge calibration papers: TestVDB's falsifier approach sidesteps calibration entirely by using implementation source as ground truth. Relevant but not direct competition.

No uncited highly-related work within specialty. The paper's Related Work covers the key REST-oracle line (AGORA+, SATORI, MASTOR) and the LLM-judge reliability line (Panickssery, Wataoka).

## Novelty Delta Verdict (Within Specialty)

**REST-oracle extraction**: TestVDB's novelty is the **falsification direction**—reading source to disconfirm documentation-derived claims. SATORI/MASTOR/AGORA+ all source ground-truth in one direction (spec or implementation); TestVDB does bidirectional checking. Clear, non-trivial delta.

**LLM-as-judge**: Source-grounded falsification as a mitigation for self-preference/self-inconsistency is novel. Prior work addresses calibration (PAIRS, debiasing) but not independent implementation-source anchoring.

## Cross-Family Generalization Caveat

Paper acknowledges cross-model re-run shows family-specific verdicts (κ = 0.14/0.37/0.51). This is an honest limitation—no claim of universal backbone robustness. The 3-run any-confirmed ensemble operating point is post-hoc; the paper flags this with Wilson CIs and bootstrap validation. Methodologically sound given the exploratory nature of LLM-as-judge work.

## Summary

The paper accurately characterizes its competitors within my specialty areas. The novelty delta (source-grounded falsification) is real and well-differentiated from SATORI/MASTOR/AGORA+. Minor citation gap for Haldar's self-inconsistency work, but empirical acknowledgment exists. No missing highly-related uncited work within the scoped search.

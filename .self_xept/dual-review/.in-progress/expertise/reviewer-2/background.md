# Reviewer 2 Background - Area Specialist (LLM-as-Judge Reliability + REST-API Oracle Extraction)

## Specialty Areas
1. **LLM-as-judge reliability**: self-preference bias, self-inconsistency, hallucination in extraction
2. **REST-API test-oracle extraction**: tools that derive oracles from structured sources vs. natural-language documentation

## Core Competitors Verified (≤5, within specialty)

### LLM-as-Judge Reliability
1. **panickssery24** - LLM Evaluators Recognize and Favor Their Own Generations (fetched)
   - Two-column check: Paper characterizes as "self-preference bias" where LLMs favor own outputs — summary confirms this is the core finding (GPT-4 73.5% self-recognition, >90% after fine-tuning)
   - Novelty delta: TestVDB cites this correctly for same-family judgment bias (Section 4). Paper's finding that fine-tuning amplifies bias supports TestVDB's design choice to use source grounding instead of same-family judge panels.

2. **wataoka24** - Self-Preference Bias in LLM-as-a-Judge (fetched)
   - Two-column check: Paper claims perplexity (text familiarity) as root cause — summary confirms GPT-4 shows 0.52 bias on Equal Opportunity metric, correlation with perplexity across all models except one
   - Novelty delta: TestVDB does NOT cite this work. This is a **missing related work** item — Wataoka provides an alternative explanation (perplexity vs. self-recognition) for self-preference that TestVDB's discussion (Section 4) could engage with. The quantitative metrics (0.52 bias for GPT-4) provide a framework for measuring bias that TestVDB does not adopt.

3. **haldar25** - Rating Roulette: Self-Inconsistency in LLM-As-A-Judge Frameworks (fetched)
   - Two-column check: Paper claims low intra-rater reliability across runs — summary confirms Llama α = 0.33, Qwen α = 0.79 on SummaC, MT-Bench α = 0.27–0.56, all below 0.8 threshold
   - Novelty delta: TestVDB cites this correctly for intra-judge inconsistency (Section 4). Paper's recommendation to aggregate across runs aligns with TestVDB's any-confirmed ensemble, but TestVDB does not discuss the reliability-performance tradeoff Haldar identifies (no-sampling degrades accuracy).

### REST-API Oracle Extraction
4. **satori25** - Static API Test ORacle Inference (SATORI) (fetched)
   - Two-column check: Paper claims extraction from OpenAPI specifications — summary confirms 17 oracle types, F1 74.3% (GPT-4o), restricted to OAS field-constrained regime
   - Novelty delta: TestVDB correctly characterizes SATORI as low-ambiguity structured-source extraction (Section 2, Table 1). Paper's limitation "cannot detect violations where documentation is ambiguous" directly supports TestVDB's claim that SATORI cannot handle the natural-language prose regime. The novelty delta is clear: SATORI reads OAS schema fields; TestVDB interprets prose.

5. **mastor26** - Multi-Agent Approach to Semantic Test Oracle Generation for RESTful APIs (fetched)
   - Two-column check: Paper claims source-based oracle generation for implemented behavior — summary confirms Java-only, 10,022 oracles across 13 APIs, mutation score 75.4%
   - Novelty delta: TestVDB correctly characterizes MASTOR as implementation-source extraction (Section 2, Table 1). Paper's limitation "treats source as ground truth; cannot detect bugs where implementation is wrong but documentation is right" is the inverse of TestVDB's goal. The delta is clear: MASTOR encodes what code **does**; TestVDB detects where code **violates** documentation.

## Coverage Search (within specialty)

No uncited highly-related work surfaced. Scoped searches for "LLM judge hallucination oracle," "natural-language documentation oracle extraction," and "self-preference bias test oracle" returned hits already cited in paper (Panickssery, Wataoka, AugmenTest) or outside scope (general LLM evaluation, not oracle-specific).

## Relational Findings Summary

**Verified characterizations** (no mischaracterization found):
- Panickssery: correctly cited for same-family bias
- Haldar: correctly cited for intra-judge inconsistency
- SATORI: correctly characterized as OAS-based, low-ambiguity
- MASTOR: correctly characterized as source-based, implementation-truth

**Missing related work**:
- **Wataoka24**: Provides perplexity-based explanation for self-preference (alternative to Panickssery's self-recognition mechanism), quantitative bias metric (0.52 for GPT-4), and evidence that bias stems from text familiarity not explicit self-identification. TestVDB's discussion of self-preference (Section 4) could engage with both mechanisms.

**Novelty positioning**: TestVDB's claim to target the "ambiguous-prose regime" vs. SATORI/MASTOR's "structured-source regime" is validated by both competitors' limitations sections. The documentation-implementation gap is indeed the residual both leave untouched.

# Reviewer 2 Background: Competitor Analysis

## Cached Literature Analysis

### MASTOR (Deng et al. 2026)
**Paper's Characterization**: MASTOR described as "state-of-the-art in LLM-based semantic oracle generation" with multi-agent architecture achieving 75.4% mutation score, +49.4 pp over SATORI.

**Actual Characterization**: 
- Multi-agent system: SourceExtractionAgent → SingleOpOracleAgent/MultiOpOracleAgent → ChallengerAgent review
- Two-phase design (analysis → generation with review/regeneration)
- Source-code grounded via transitive import closure
- 75.4% MS across 13 REST APIs (251K LoC, 296 operations)
- Per-API scores: 69.0%-95.9%

**Novelty Delta**: TestVDB extends beyond REST APIs to vector databases. TestVDB's multi-agent architecture (16 agents across 5 phases) is significantly more complex than MASTOR's 2-phase design. TestVDB targets specialized DB operations (index type mismatches, search semantics, vector parameter validation) rather than generic REST patterns. TestVDB's dev-reviewer phase simulates developer cognition, absent from MASTOR.

### SATORI (Alonso et al. 2025)
**Paper's Characterization**: SATORI as "only prior work on LLM-based semantic oracle generation for REST APIs" with static specification-only approach (74.3% F1), significantly outperformed by MASTOR (+49.4 pp gap).

**Actual Characterization**:
- Black-box static analysis from OpenAPI Specification
- 17 unary oracle types (string, boolean, number, array properties)
- 74.3% F1-Score (vs. AGORA+U 69.3%)
- Found 18 real bugs in 7 APIs ($0.28 per bug)
- Limitation: requires detailed OAS, unary oracles only

**Novelty Delta**: TestVDB applies LLM-based oracle generation to vector database domain (no OAS equivalent). TestVDB uses source-code analysis (like MASTOR) not specification-only (like SATORI). TestVDB's domain-specific oracles (HNSW parameters, ef/search consistency, collection state transitions) have no analog in SATORI's generic REST patterns. TestVDB's focus on semantic fault detection (search correctness, parameter interactions) vs. SATORI's format/value constraints.

### Panickssery et al. (2024)
**Paper's Characterization**: Demonstrates "LLM-as-judge systems exhibit significant self-preference bias" — inflation when judge evaluates own outputs. Quantitative framework for measuring bias via Equal Opportunity metric.

**Actual Characterization**:
- LLMs show self-recognition ability (>50% out-of-the-box, >90% after fine-tuning)
- Linear correlation between self-recognition and self-preference
- GPT-4: 73.5% self-recognition, highest self-preference
- Causal evidence: fine-tuning amplifies both properties
- Root cause: LLMs prefer outputs they recognize as their own

**Novelty Delta**: TestVDB's LLM-as-judge mechanism (judge-evidence, judge-novelty, judge-severity) uses LLMs to evaluate defect candidates. TestVDB mitigates self-preference by using separate models for generation (defect finding) and judgment (evidence review), but does not explicitly measure or correct for bias. Panickssery's framework could quantify bias in TestVDB's judge agents.

### Wataoka et al. (2025)
**Paper's Characterization**: Alternative explanation for self-preference — "LLMs prefer texts more familiar to them (lower perplexity)" regardless of self-generation. Quantitative metric based on fairness theory.

**Actual Characterization**:
- GPT-4 shows highest self-preference (0.52 on 0-1 scale)
- Root cause: perplexity familiarity, not explicit self-recognition
- LLMs assign higher scores to lower-perplexity texts
- Correlation holds across all tested models except two
- LLMs exhibit lower perplexity on own outputs

**Novelty Delta**: TestVDB's judge agents may exhibit similar bias — assigning higher scores to defect candidates that match expected patterns (lower perplexity) regardless of actual quality. Wataoka's metric could measure bias in TestVDB's judge-evidence and judge-severity agents. The perplexity-based explanation suggests TestVDB could use style transfer or paraphrasing to reduce familiarity bias.

## Domain Comparison

| Dimension | REST APIs (MASTOR/SATORI) | Vector DBs (TestVDB) |
|-----------|---------------------------|---------------------|
| **Interface** | HTTP/JSON (OpenAPI) | Native APIs (Python/JS clients) |
| **State Model** | Stateless resources | Collection/index state, server configuration |
| **Fault Types** | Status codes, field constraints, cross-endpoint consistency | Index type mismatches, search semantics, parameter validation |
| **Oracle Grounding** | Source code (MASTOR) or OAS (SATORI) | Implementation + documentation + contract formalization |
| **Test Generation** | Fuzzing, model-based, search-based | Multi-strategy attacks (boundary, semantic, state) |
| **Multi-Agent Design** | 7 agents (MASTOR) | 16 agents across 5 phases |

## Key Takeaways for Reviewer 2

1. **LLM-as-Judge Reliability**: Both Panickssery and Wataoka demonstrate systematic biases in LLM evaluation. TestVDB's judge agents (judge-evidence, judge-novelty, judge-severity) are vulnerable to these biases but does not measure or mitigate them.

2. **Semantic Oracle Generation**: MASTOR demonstrates source-code analysis outperforms specification-only approaches (+49.4 pp). TestVDB follows MASTOR's implementation-grounded approach rather than SATORI's black-box method.

3. **Domain Specificity**: TestVDB targets vector database defects with no analog in REST API testing. Specialized oracles (ef/search consistency, HNSW parameter validation) go beyond generic format/value checking.

4. **Multi-Agent Complexity**: TestVDB's 16-agent architecture is significantly more complex than MASTOR's 7-agent system. Additional phases (threat modeling, orchestration, developer simulation) increase system complexity but enable domain-specific fault detection.

5. **Evidence Grounding**: Both MASTOR and TestVDB ground assertions in source code (MASTOR via transitive import closure, TestVDB via source bundle analysis). This grounding improves oracle precision over specification-only approaches.
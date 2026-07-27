# MASTOR — Summary (context-independent)

**Citation:** Deng et al., "MASTOR: A Multi-Agent Approach to Semantic Test Oracle Generation for RESTful APIs", arXiv:2606.10465 [cs.SE], June 2026 (J. ACM format, appears to target TOSEM/JACM).

## Problem
Existing REST API testing tools do test-case generation well, but their oracles are limited to HTTP status codes, runtime failures, and schema conformance. These miss semantic faults (incorrect field composition across execution paths, cross-operation data inconsistencies) encoded in implementation source code.

## Method
Two-phase multi-agent pipeline operating on **implementation source code** (not on documentation):
1. **Source Analysis phase.** `SourceExtractionAgent` reads each endpoint's transitive import closure (controllers, service layer, repositories, data models) and produces a structured **Source context** capturing request parameter constraints and response schema. OAS anchors endpoint discovery; OAS items not traceable to source are placed in `*_pending` fields (precision-biased: omit rather than hallucinate).
2. **Oracle Generation phase.** Two parallel paths over the Source contexts:
   - **Single-operation path:** status oracles + field oracles via four strategies (forward-valid, forward-invalid, backward-valid, backward-invalid) covering boundary values, branching pairs, catch-block analysis.
   - **Multi-operation path:** behavioral consistency oracles over cross-operation semantic associations (identifier flow, resource lifecycle, state propagation).
   - Both paths pass through a `ChallengerAgent` review that emits improvement hints (one regeneration pass), then deterministic normalization (filters no-assertion oracles, hallucinated parameters).

Agents communicate only via shared `OutputStore` (blackboard); orchestrator (`MastorAgent`) is deterministic, no autonomous goal-seeking.

## Key Quantitative Results
- **Benchmark:** 13 open-source Java REST APIs (296 operations, 251,303 LoC) from WFD and PRAB datasets. Subject selection: surveyed 60+ REST testing studies, kept projects referenced by ≥8.
- **Overall mutation score (RQ1): 75.4%** (5,064 killed / 6,719 covered mutants), range 69.0%–95.9%. Oracle count: 10,022 (6,102 status / 3,575 field / 263 multi-op).
- **Baseline comparison (RQ2)** on 50 selected operations (status+field only): MASTOR 69.9% vs. Direct Prompting 39.8% (+30.1pp) vs. SATORI 20.5% (+49.4pp).
- **Ablation (RQ3):** Multi-Op Generation and ChallengerAgent both contribute; Multi-Op is the larger contributor.
- **Cost (RQ4):** median $0.56 per API (DeepSeek V4 Pro + Qwen3.6-Plus, open-source models).

## Dataset & Venue
Java REST API benchmark (WFD + PRAB); appears to target a major software engineering venue (JACM-style formatting).

## Limitations (as stated)
- Equivalent mutants not identified; surviving mutants may include some equivalent ones.
- Java-only (Spring Boot, Jersey, JDK HTTP).
- OAS-anchored: requires an OAS to anchor endpoint discovery (operations not in OAS are not discovered from source alone).
- Oracle correctness depends on LLM code reasoning; ChallengerAgent reduces but does not eliminate hallucination.
- LLM-derived oracles are evaluated by mutation score against implementation mutants — i.e., oracles are judged against the implementation's own behavior, not against an external specification of correctness.

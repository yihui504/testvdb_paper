# TestVDB — Paper Plan

> Companion to idea-analysis.md. Target venue decided with advisor: VLDB (rolling) primary, ISSTA'27 alternate.

## Target Venue & Timeline

- **Primary**: VLDB (rolling monthly deadline) — fastest path to precedence; DB community avoids the SE competitor-reviewer overlap; DDLCheck (VLDB'25) precedent.
- **Alternate**: ISSTA'27 — testing-specialist venue, receptive to method+empirical, slightly earlier cycle than ICSE/FSE.
- **Timeline**: ~6–8 weeks to submission. Scoop pressure dictates speed over perfection; fill the 3 evaluation gaps (see roadmap), polish prose, submit.

## Research Questions

1. **RQ1 (Capability)**: Can TestVDB detect real API-compliance defects across VDBMSs? (111 issues, 36 acknowledged, 5 systems.)
2. **RQ2 (Hallucination)**: Is contract hallucination propagation observable, and does source-grounded counter-evidence mitigate it? (12 by-design cases, #50354 trace.)
3. **RQ3 (CTS effectiveness)**: How much does the dev-reviewer counter-evidence layer improve precision over single-layer LLM judgment? (12.9%→69.2%, 5.4×; FP-removal 80.6%.)
4. **RQ4 (TM pilot, exploratory)**: Does a threat-model prior help? (Honestly inconclusive — reported as exploratory with design limitations.)

## Claimed Contributions

1. First LLM-driven realization + large-scale empirical study of VDBMS API-compliance defect detection.
2. Contract-Truth Separation — design principle isolating LLM assertions from a maintainer-authority truth layer.
3. dev-reviewer counter-evidence mechanism (3 anchors); 80.6% FP removal, 5.4× precision; TP-recall 20–60% reported honestly.
4. Contract hallucination propagation finding (12 by-design = 25%).
5. Exploratory threat-model pilot with honest limitations.
6. Empirics + open-source system.

## Methodology Overview

Five-stage pipeline: contract extraction (LLM knowledge-extractor from API docs) → attack generation (boundary/semantic/state agents + threat-model prior) → 4-judge debate → **dev-reviewer (CTS counter-evidence: clean repro / source-grounding / TM cross-check)** → two-layer novelty gate.

## Experiment Design

- **Systems**: Milvus, Qdrant, Weaviate, MeiliSearch, Chroma (pinned target versions).
- **Baselines**: single-layer LLM judgment (ablation, 4/31 = 12.9%); complementarity comparison vs VDBFuzz (crash).
- **Metrics**: acknowledged count, precision = acknowledged/(acknowledged + by-design + rejected) = 36/52 = 69.2%, FP-removal rate (80.6%), defect-type distribution.
- **Ablation**: Milvus v2.6.19 (1834 raw → 31 Stage-2 → 4 confirmed); TM double-blind on v2.6.17 (exploratory, n=5).
- **Gaps to fill**: (a) cross-library dev-reviewer ablation, (b) stronger-model re-triage of 48 adjudicated issues, (c) contract-hallucination frequency statistics.

## Paper Outline

1. Introduction (motivation, core reversal, CTS, results, contributions)
2. Background & Problem Formulation (VDBMS architecture, taxonomy, API compliance, oracle problem)
3. Approach (overview, contract extraction + TM, attack + 4-judge, CTS + dev-reviewer, novelty gate)
4. Contract Hallucination Propagation (finding, 12 by-design, mitigation)
5. Evaluation (RQ1–RQ4 + threats to validity)
6. Related Work
7. Conclusion & Future Work

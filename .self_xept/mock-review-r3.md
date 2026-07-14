# Reviewer 3 — Independent Review

## Summary

TestVDB targets an important and timely problem: API compliance defects in Vector Database Management Systems (VDBMSs), which constitute 43% of VDBMS bugs but lack practical oracles. The paper introduces Contract-Truth Separation (CTS), a design principle that isolates LLM-generated contract assertions from a maintainer-authority truth layer to counter "contract hallucination propagation" — a phenomenon where hallucinated constraints are self-confirmed when one LLM family both generates and judges against a contract. Across five VDBMSs, TestVDB produced 111 submissions; 52 were adjudicated, yielding 36 maintainer-acknowledged issues (28 fixed, 8 accepted-open). The dev-reviewer's source anchor lifts false-positive suppression from 31% to 81% at 96.7% TP retention in a controlled retrospective, with 69.2% aggregate precision (Wilson 95% CI [55.7%, 80.1%]). The paper also identifies a model-free invariant oracle subclass (e.g., COSINE distance >1.0 for identical vectors) that reproduces across vendors and violates hard mathematical bounds. The work is honest about limitations, reports a negative result for the threat-model anchor, and frames breadth systems as attack-surface probes rather than statistical evidence.

## Strengths

**1. The problem is real and the gap is genuine.** The paper convincingly establishes that non-crash compliance defects are a substantial, unaddressed slice of VDBMS reliability. The 43% figure from the roadmap study and the complementary bug study provide solid grounding, and Table 1's exclusion reasoning makes it clear that no existing oracle candidate (crash, differential, metamorphic) covers API compliance. LLM-driven testing is overused in some contexts, but here it is a last-resort oracle — not hype-driven but necessary.

**2. Contract hallucination propagation is a transferable insight.** The characterization of self-confirmation when one LLM family both extracts and judges is, to my knowledge, novel in the LLM-driven testing literature. Section 5's two observed forms (fabricated provenance and over-strict intent) are well-motivated, and the mitigation — source-grounded falsification — is architecturally sound. The conclusion's argument that this generalizes to REST contract testing, configuration validation, and policy-as-code is credible and worth emphasizing. This is the paper's broadest conceptual contribution.

**3. The model-free invariant oracle is a strong, contingent technical finding.** The COSINE >1.0 invariant violation, independently reproduced on both Milvus and Qdrant, violates a hard mathematical bound and needs no LLM judgment at all. This is the paper's "most defensible technical finding" (as the authors themselves frame it) — expressible, model-free, and cross-vendor. It survives agent-design variations and provides a lower-bound on oracle capability independent of the full LLM pipeline.

**4. The evaluation is honest and well-structured.** The paper openly reports RQ4 as a negative/exploratory result (threat-model anchor is a noisy complement, not a clean validated contribution). It gives wide confidence intervals and acknowledges that the 5-unique-TP claim (Table 3) is a lower bound relative to one 19-probe fuzzer instance, not a fuzzer-class upper bound. The breadth systems (Weaviate, MeiliSearch, Chroma) are framed as attack-surface probes rather than statistical evidence — exactly the right call given 21/30 Weaviate submissions remain pending. The sensitivity analysis (Section 6.3) bounding worst-case precision under different unadjudicated assumptions is rigorous.

**5. The controlled retrospective is the right method.** The RQ3 same-population comparison (claim-only vs. source-grounded over the same 52 adjudicated candidates) is much stronger than cross-tier comparisons. The 31% → 81% FP-suppression lift at 96.7% TP retention is clean evidence that the dev-reviewer's source anchor is the primary validated contribution.

**6. Incremental value is clearly articulated.** Table 3 and the surrounding text explicitly distinguish TPs reachable only by the full LLM pipeline (5 unique: 3 diagnostic-quality, 2 state/logic) from those reachable by spec-driven fuzzing or model-free invariants. The 19-probe boundary fuzzer concedes effectiveness on the boundary/validation subset but shows TestVDB's marginal value on state/logic, diagnostic, and spec-gap bugs.

**7. The complementarity with VDBFuzz is well-positioned.** The paper clearly frames TestVDB as complementary to crash-focused fuzzing, not competing. The yield is almost entirely non-crash (35/36), and the paper acknowledges that head-to-head empirical comparison is future work rather than making an overstated claim.

**8. The writing is clear and the structure is logical.** The introduction motivates the problem, establishes the gap, and positions the contribution. Section 5's contract hallucination propagation framing is concise and well-supported. The evaluation structure (RQ1-RQ4) is easy to follow, and the threats-to-validity section is thorough.

## Weaknesses / Suggestions for Improvement

### [Major] 1. Recall cohort is small (4/9 testable bugs).

**[Major]** The held-out rediscovery study reports 4/9 recall (44.4%, Wilson 95% CI [18.9%, 73.3%]), but only 7 were testable due to SDK incompatibility blocking 2. The lower bound clearing zero is non-trivial, but a 4/9 testable cohort is small. The confidence interval is wide (55 percentage points), which reflects honest reporting but also means the recall estimate is noisy.

**Suggestion:** In the final version, explicitly emphasize that recall is a preliminary, bounded estimate (4/9 testable; 2 blocked by tooling) and that a larger recall cohort is future work. Consider adding a sentence in the conclusion bounding the recall scope and calling out SDK incompatibility as a practical limit.

### [Major] 2. Breadth systems give little adjudicated signal.

**[Major]** Weaviate has 21/30 submissions pending/open, MeiliSearch 3 submissions with 0 adjudicated, and Chroma 1 submission pending. The paper frames these as breadth probes rather than statistical evidence, which is the right call, but it leaves the cross-system generalization claim effectively resting on Milvus and Qdrant only. Weaviate's high pending rate appears to reflect maintainer triage latency (none rejected) rather than substantive invalidation, but without adjudication we cannot draw strong conclusions.

**Suggestion:** In Section 6.1 (RQ1), add a sentence acknowledging that Weaviate/MeiliSearch/Chroma are preliminary probes and that cross-system generalization is claimed primarily for Milvus and Qdrant. This is already implied but not stated explicitly. A minor framing tweak would reduce the risk of over-generalization.

### [Major] 3. Threat-model anchor ablation is confounded and noisy.

**[Major]** RQ4's negative result is confounded by a wiring gap (threat-modeler populated `threat_model.json`, but dev-reviewer consumed `developer_cognition.json`), and even after fixing the wiring, the threat anchor is unstable across runs and over-fires on state/concurrency FPs. The paper honestly reports this as "noisy complement," not dead weight, but the $n=12$ sample is small and the instability means the anchor's standalone effect is bounded.

**Suggestion:** The paper's current framing is already honest ("we do not claim the three-anchor design as a clean validated contribution on the strength of $n=12$"). To strengthen, consider adding a sentence in RQ4 explicitly calling out the wiring gap as a limitation and noting that a larger-scale threat-model ablation is future work. This would preempt reviewer concerns about experimental soundness.

### [Minor] 4. Reproduction anchor remains design-level future work.

**[Minor]** The dev-reviewer has three anchors (reproduction, source, threat-model), but the reproduction anchor — "build a minimal reproducer against a live VDBMS" — is not evaluated in the paper. The threat-model anchor is ablated (noisy), and the source anchor is validated as primary. The reproduction anchor is a natural next step for strengthening FP suppression.

**Suggestion:** In Section 5 (Approach), add a brief sentence acknowledging that the reproduction anchor is not yet evaluated and is left as future work. This is a minor point but would make the contribution claims more precise.

### [Minor] 5. Ground-truth tiers across baselines are asymmetric.

**[Minor]** Table 3 and Figure 2 show precision across multiple arms (Single-LLM, Single-Layer, TestVDB), but each uses different ground truths (LLM self-judgment, API-acceptance, blind re-triage, maintainer). The paper already makes this asymmetry explicit rather than drawing invalid cross-tier conclusions, which is the right choice, but the reader must work harder to compare across tiers.

**Suggestion:** Consider adding a brief sentence in Section 6.3 (Baseline Comparisons) summarizing which tier is the fairest head-to-head comparison (the retrospective tier, same 52-candidate pool) and which are directional bounds. This would help readers navigate the complexity without overstating claims.

### [Minor] 6. Single-layer counterfactual precision (45.6%) combines heterogeneous triage.

**[Minor]** The 45.6% figure for the single-layer counterfactual combines maintainer-adjudicated baseline (36/52) with 27 live-re-probed FPs. The paper acknowledges that triage might reclassify a few of the 27 and that the arm is bounded to one feedback cycle, but the heterogeneous triage source makes the 45.6% figure a directional bound rather than a clean end-to-end operating point.

**Suggestion:** The current framing ("we report it as a directional lift at zero recall cost") is already appropriate. To further clarify, consider adding a parenthetical acknowledging the heterogeneous triage (maintainer-adjudicated plus live re-probed) when first introducing the 45.6% figure.

### [Minor] 7. Excluded set may hide FP tail.

**[Minor]** 17 of the 29 excluded submissions are Milvus, closed without label. The paper bounds the worst case (36/81 = 44.4% if all excluded were FPs) but notes that closed-no-label may reflect maintainer non-engagement rather than invalidity.

**Suggestion:** The current sensitivity analysis already bounds this. To strengthen, consider adding a sentence in the threats-to-validity section explicitly calling out the excluded-set limitation and suggesting that label-preserving closure (e.g., "wontfix" vs. silent close) would improve future triage signal.

## Questions for Authors

1. **Recall scaling:** The held-out rediscovery study reports 4/9 recall (44.4%, CI [18.9%, 73.3%]), with 2 bugs blocked by SDK incompatibility. Do you have plans to expand the recall cohort beyond 9 bugs, or is this a practical limit due to pre-2024 VDBMS availability and Docker containerization constraints? A larger cohort would substantially tighten the confidence interval.

2. **Cross-system generalization:** The cross-system claim rests primarily on Milvus and Qdrant, with Weaviate/MeiliSearch/Chroma as breadth probes. Do you have plans to re-run adjudication on Weaviate submissions once maintainer triage completes, or to target additional VDBMSs with stronger maintainer engagement to validate cross-system generalization beyond Milvus/Qdrant?

3. **Threat-model anchor design:** The threat-model anchor is ablated as a noisy complement, catching some boundary-default FPs that source misses but over-firing on state/concurrency. Have you considered refining the blindspot mechanism (e.g., more precise state/concurrency patterns, or conditional firing rules) to reduce over-firing, or is the current design already a local optimum given the $n=12$ sample?

## Scores

- **Originality / Novelty:** 4/5
  - Contract-Truth Separation and contract hallucination propagation are new insights to my knowledge.
  - LLM-driven testing is not novel, but applying it to VDBMS API compliance and identifying the self-confirmation failure mode is a strong directional contribution.
  - Model-free invariant oracles (COSINE >1.0) are incremental but well-executed.

- **Significance / Impact:** 4/5
  - The problem (43% of VDBMS bugs lack oracles) is significant and timely given LLM dependence on VDBMSs.
  - CTS is a transferable principle that generalizes beyond VDBMSs (REST contract testing, config validation, policy-as-code).
  - 36 maintainer-acknowledged issues (28 fixed) demonstrate real-world impact.
  - Limit: recall cohort is small, and cross-system generalization needs broader validation.

- **Presentation / Clarity:** 5/5
  - The paper is well-structured and clearly written.
  - Tables and figures (especially Table 3 incremental yield and Figure 2 precision tiers) are effective.
  - The threats-to-validity section is thorough and honest.
  - Minor: some baseline complexity requires careful reading, but the paper guides the reader well.

- **Soundness / Technical correctness:** 4/5
  - The controlled retrospective (same 52-candidate pool) is a strong methodological choice.
  - The evaluation honestly reports negative results and bounded limitations.
  - The model-free invariant oracle is technically sound and cross-vendor reproduced.
  - Limit: recall estimate is noisy; threat-model anchor is unstable and confounded by wiring gap; breadth systems give little adjudicated signal. These are acknowledged but remain real limitations.

## Overall Recommendation

**Accept**

## Confidence

**4/5**

I have read the paper carefully and evaluated it against the PVLDB/VLDB criteria. My confidence is high but not absolute because: (1) the recall estimate is based on 4/9 testable bugs with a wide CI; (2) the threat-model anchor's instability and wiring-gap confound limit the strength of that ablation; and (3) the breadth systems (Weaviate/MeiliSearch/Chroma) provide limited adjudicated signal. However, the paper's honesty about these limitations, the strength of the controlled retrospective, and the transferability of the CTS principle justify an Accept verdict.
# Reviewer 3: Friendly Review

## Summary

TestVDB addresses an important and timely gap in VDBMS testing: detecting documentation-implementation defects where systems silently accept inputs that violate their API documentation. The authors convincingly argue that most VDBMS defects are logical bugs that produce no crash, rendering crash-oracle fuzzers like VDBFuz ineffective for the majority of cases. They propose a four-stage LLM pipeline that extracts behavioral claims from documentation, generates tests, executes them against sandboxed VDBMSs, and confirms defects. The key innovation is the dev-reviewer agent, which uses source code as an independent falsifier to suppress false positives caused by LLM hallucination and self-preference bias.

The paper makes a solid contribution. The empirical evaluation shows practical impact: 107 submitted issues with 49 maintainer-acknowledged defects across three production VDBMSs, including 15 merged fixes. The false-positive analysis is methodical and the dev-reviewer design demonstrates real improvement (74% recall vs. 37% without source grounding). The writing is clear, the scope is well-defined, and the authors are honest about limitations.

## Strengths

1. **Clear problem definition with careful scoping.** The authors wisely distinguish documentation-implementation consistency from result correctness and argue convincingly that deterministic oracles cannot handle natural-language documentation boundaries. Table 1's oracle exclusion argument is a valuable conceptual contribution that clarifies when LLM-derived oracles are actually necessary and why prior REST-API oracle tools (AGORA+, SATORI, MASTOR) don't transfer to the ambiguous-prose regime.

2. **Strong empirical results with real-world impact.** Submitting 107 issues to three production VDBMSs and achieving 49 maintainer acknowledgments (including 15 merged fixes) is substantive evidence of practical value. This goes beyond toy examples and shows the approach works at scale. The yield precision of 68.1% on adjudicated submissions is respectable for an automated defect detection system.

3. **Thorough analysis of failure modes.** Sections 4-5 provide a nuanced diagnosis of two false-positive mechanisms (extraction hallucination, judgment self-preference) and explain why naive multi-perspective judging fails structurally, not as a tuning problem. The dev-reviewer's three-check design (reproducibility, evidence sufficiency, falsifiability) is a thoughtful solution that leverages source code as ground truth. The ablation study showing source alone suppresses 75% of false positives is compelling evidence that the source-grounded anchor is the dominant contributor.

4. **Honest threat reporting and operating-point transparency.** The authors report full per-run variance for recall (15-78%) and explicitly flag the 3-run union as a post-hoc operating point. This candor builds trust. The cross-model check (DeepSeek vs. GLM-5.2) showing κ=1.0 on twenty candidates addresses family-specific bias concerns. The RQ3 bidirectional probe acknowledges n=1 per direction rather than overstating generalizability.

5. **Well-structured evaluation with multiple research questions.** The paper addresses three distinct questions: detection capability (RQ1), false-positive suppression (RQ2), and comparison with VDBFuzz (RQ3). Each has appropriate methodology. The controlled retrospective on 48 maintainer-adjudicated candidates provides solid evidence for the dev-reviewer's effectiveness.

## Weaknesses

1. **Ground truth limitations constrain generalization.** The 48-candidate retrospective is maintainer-adjudicated but non-random, and the authors acknowledge they have no unbiased defect catalog. This makes it hard to generalize recall beyond this specific dataset. The single-run recall variance (15-78%) is substantial, and while the union ensemble mitigates this, it raises questions about stability. A capture-recapture estimation or systematic sampling strategy would strengthen external validity.

2. **Limited generalization evidence beyond VDBMSs.** The authors claim transferability to "structurally similar documentation regimes" (REST APIs without OpenAPI, configuration validation, policy-as-code) but provide no empirical validation. Weaviate appears only in yield numbers (13 acknowledged from 30 submitted), not in the controlled retrospective. Even one non-VDBMS case study would significantly bolster the transferability argument.

3. **RQ3 bidirectional probe is small (n=1 per direction).** While the Qdrant case studies are illustrative, they are hypothesis-generating rather than conclusive. The integer-overflow crash reachable by contract reasoning is a strong example, but the silent-accept defect missed by VDBFuzz could reflect incomplete template coverage rather than a fundamental oracle limitation. The authors acknowledge this, but the section could be more clearly labeled as exploratory.

4. **Cost and scalability details are sparse.** A full run costs ~$10 per target and uses 10^4 LLM calls. The authors say this is "on the order of" and dominated by source grounding, but there's no systematic cost breakdown. For researchers who want to replicate or extend this work, a clearer accounting of where the tokens go (extraction vs. generation vs. adjudication vs. dev-reviewer) would be helpful.

## Questions

1. **Pending adjudications:** Could you provide more detail on the 35 pending maintainer adjudications? Are there patterns (type of constraint, documentation ambiguity, VDBMS) that correlate with pending status? This might shed light on what makes a defect harder to adjudicate and inform future tool design.

2. **Multi-perspective judging failure:** In Section 4, you note that multi-perspective judging reaches 80% precision but 15% recall. Could you elaborate on the 85% of cases where the judges converge on the wrong claim? Are there documentation patterns (e.g., passive voice, implicit constraints, "optional" without explicit zero-handling) that systematically mislead all judges?

3. **State-dependent defects:** How does the dev-reviewer handle concurrent or state-dependent defects? The three-check design mentions "state and concurrency FPs" as unstable in the threat-model anchor, but it's unclear whether the source-grounded anchor can reliably falsify race conditions or transactional anomalies that only manifest under specific execution orders.

4. **Cross-model agreement:** For the cross-model check (DeepSeek vs. GLM-5.2), you report perfect agreement (κ=1.0) on twenty candidates. Was this a convenience sample, or were these twenty selected because they were borderline/ambiguous? Perfect agreement is surprising and suggests either strong source evidence or selection bias—some clarification would strengthen the claim.

5. **Template coverage in RQ3:** You note that VDBFuzz's template suite doesn't probe wait=false. Is this a gap in VDBFuzz's current templates, or a fundamental limitation of structure-only fuzzing? Would augmenting VDBFuzz's templates to cover all documented parameters address the coverage gap, or would the oracle problem (crash-only) still remain?

## Scores

**Soundness:** 4/5 - The approach is technically sound and the evaluation is thorough. The controlled retrospective provides solid evidence, though generalization is limited by the non-random ground truth and VDBMS-only scope. The RQ3 probe is small but acknowledged as exploratory.

**Significance:** 4/5 - Documentation-implementation defects are a real and under-studied problem for critical infrastructure (VDBMSs in LLM stacks). The 49 acknowledged defects (15 fixed) show practical impact. The work would be stronger with evidence beyond VDBMSs, but the VDBMS contribution alone is meaningful.

**Novelty:** 4/5 - The dev-reviewer's source-grounded falsification is a novel contribution to LLM-as-judge reliability. The two-mode failure analysis (extraction hallucination, judgment self-preference) provides a useful framework for understanding LLM-derived oracle limitations. The documentation-implementation defect framing is a useful refinement over prior work on structured sources.

**Presentation:** 5/5 - Clear, well-organized writing. The exclusion argument (Table 1) effectively motivates the problem and distinguishes the work from prior REST-API oracle tools. The example path in Section 3.4 concretely illustrates the pipeline. Threats are reported honestly with appropriate caveats.

**Overall:** 8/10 - A solid contribution that addresses an important problem with a well-designed solution and substantive evaluation. The work would benefit from broader generalization evidence and clearer cost accounting, but it meets the bar for publication. The 15 merged fixes across three production VDBMSs demonstrate real-world value.

**Confidence:** 4/5 - I am familiar with VDBMS testing, LLM-as-judge reliability, and REST-API oracle literature, which supports confident assessment of the approach and evaluation methodology. I am not a domain expert in the specific internals of Milvus/Qdrant/Weaviate, but this did not affect my assessment of the core technical contribution.

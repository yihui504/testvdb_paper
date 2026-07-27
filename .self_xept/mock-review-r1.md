# Reviewer 1: Objective Review

## Summary

This paper addresses documentation-implementation defects in Vector Database Management Systems (VDBMSs)—cases where a system silently accepts inputs that violate its API documentation. The authors propose TestVDB, a four-stage pipeline that uses LLMs to extract behavioral claims from natural-language documentation, generate tests, execute them against sandboxed VDBMS instances, and confirm defects. A key contribution is the "dev-reviewer" agent, which acts as a source-grounded falsifier to suppress false positives caused by LLM hallucination during claim extraction and self-preference bias during judgment. The authors evaluate on three VDBMSs (Milvus, Qdrant, Weaviate), report 49 maintainer-acknowledged true-positive defects out of 107 submitted issues (15 fixed via merged PR), and demonstrate that the dev-reviewer improves recall from 37% to 74% on a 48-candidate retrospective. A bidirectional comparison with VDBFuzz shows complementary coverage: TestVDB reaches a crash-class defect via contract reasoning, while VDBFuzz misses a silent-accept defect under its current templates.

## Strengths

1. **Clear problem definition and oracle exclusion argument.** The authors precisely define "documentation-implementation defects" and systematically rule out alternative oracles (crash, differential, metamorphic, property-based, REST-API tools) in Table 1 (Section 2). This makes the case for LLM-derived oracles compelling and shows the residual problem space is genuinely under-served.

2. **Strong empirical grounding with real-world impact.** The 107 submitted issues with 49 maintainer-acknowledged TPs across three production VDBMSs (Table 2, Section 5.1) demonstrate practical relevance. The 15 merged-PR fixes provide concrete evidence that the defects matter to maintainers.

3. **Well-diagnosed false-positive problem.** Section 4 correctly identifies two distinct failure modes (hallucination in extraction, self-preference in judgment) and explains why multi-perspective judging is structurally insufficient. The diagnosis is specific and supported by the data (80% precision but only 15% recall for the multi-perspective baseline).

4. **Source-grounded falsification is a sound mitigation.** The dev-reviewer's three-check design (independent reproducibility, evidence sufficiency, falsifiability) and three anchors (clean-reproduction, source-grounded, threat-model) directly address the diagnosed failure modes. The ablation in Section 5.2 (source alone suppresses 75% of FPs, source+threat-model 91%) isolates the contribution of each anchor.

5. **Transparent methodology.** The authors disclose the post-hoc nature of the 3-run union operating point (Section 5.2, Table 3) and flag it as justified by falsifier semantics rather than pre-registered. They report single-run variance (recall 15–78%) and provide Wilson CIs for all precision/recall estimates.

## Weaknesses

1. **[major, fixable] Weak external validity for RQ2 (false-positive suppression).** The 48-candidate retrospective covers only Milvus (32 candidates) and Qdrant (16 candidates). Weaviate is yield-only. The authors acknowledge this in the threats section, but it limits confidence that the dev-reviewer's 67% precision / 74% recall generalizes beyond the two systems in the controlled study. The cross-model check (DeepSeek vs. GLM-5.2, κ=1.0 on 20 candidates) helps, but 20 candidates is a small sample and the check only measures agreement, not ground-truth recall. Fix: Either expand the retrospective to include Weaviate candidates, or explicitly frame RQ2 as "on Milvus and Qdrant" rather than a general claim.

2. **[major, fixable] RQ3 bidirectional probe has insufficient statistical power.** Each direction in the TestVDB-VDBFuzz comparison is n=1 (Section 5.3, Table 4). The Qdrant v1.4.0 and v1.18.0 cases are hypothesis-generating, but the paper treats them as a controlled comparison. n=1 cannot distinguish whether VDBFuzz missing #9045 is a template coverage issue, a budget issue, or a fundamental limitation. The authors partially acknowledge this ("we treat these as hypothesis-generating controlled cases"), but the abstract and conclusion state the result more definitively ("clarifies what each tool reaches") than the data supports. Fix: Either run multiple VDBFuzz configurations (e.g., varied budgets, template augmentations) or downgrade the RQ3 framing to "exploratory comparison" rather than a definitive reachability claim.

3. **[minor, fixable] Post-hoc operating point selection is not fully defended.** The 3-run any-confirmed union is reported as the headline (Section 5.2, Table 3), but this is a post-hoc choice after observing the data. The authors justify it by falsifier semantics ("a candidate that survives any independent falsification is more likely a true defect"), but this is an a priori principle, not an empirical validation. No comparison is provided against alternative operating points (e.g., majority-vote of 3 runs, or a pre-specified confirmation threshold). Fix: Add a brief analysis showing how the 3-run union compares to other plausible operating points (e.g., 3-run majority, 2-run union) on precision/recall trade-offs, or explicitly state the 3-run union was selected after observing the per-run variance.

4. **[minor, fixable] Abstract oversells the oracle exclusion argument.** The abstract states "Because the boundary is natural-language prose, deterministic oracles (differential, metamorphic, property-based) cannot adjudicate these accept/reject decisions," which is stronger than the paper actually supports. Table 1 shows these oracles miss the documentation-implementation residual, but the paper does not prove they *cannot* be extended to handle it (e.g., by incorporating documentation interpretation as a preprocessing step). Fix: Rephrase to "Existing instantiations of deterministic oracles miss the documentation-implementation residual" or similar qualifying language.

5. **[minor, fixable] The "implementation-as-correct" assumption is under-examined.** Section 6 acknowledges that source-grounded falsification treats the implementation as correct, so an implementation bug can wrongly falsify a correct documentation clause. The 15 merged-PR fixes are cited as evidence the assumption holds often enough, but this is circular: the fixes are precisely cases where the documentation was right and the implementation was wrong. No analysis is provided of whether any confirmed TPs might be "false negatives" where the dev-reviewer wrongly falsified a correct claim because the implementation had a bug. Fix: Add a brief discussion or example of how a user might detect such cases (e.g., when a maintainer rejects a confirmed TP as "wont-fix" because the documentation itself is wrong).

## Questions for Authors

1. **On RQ2 generalization:** The 48-candidate retrospective is Milvus- and Qdrant-heavy. Do you have any data on how the dev-reviewer performs on Weaviate candidates, or on VDBMSs outside your study (e.g., Pinecone, pgvector)? Even a small holdout sample would strengthen the external validity claim.

2. **On RQ3 methodology:** The n=1 bidirectional probe is limited. Did you consider augmenting VDBFuzz's template coverage or budget for the Qdrant v1.18.0 case to test whether #9045 is reachable with additional fuzzing resources? Even if unsuccessful, this would strengthen the claim that VDBFuzz misses it due to fundamental oracle limitations rather than incomplete input coverage.

3. **On the dev-reviewer's threat-model anchor:** Section 5.2 reports that the threat-model anchor alone suppresses 6/12 FPs (50%) but is "unstable on state and concurrency FPs." Can you elaborate on what makes state/concurrency false positives resistant to threat-model filtering? Is the issue incomplete coverage of by-design patterns, or ambiguity in distinguishing concurrency bugs from by-design behavior?

## Scores

- **Soundness:** 4/5 — The methodology is sound and well-documented, with clear threat acknowledgment. The main weakness is RQ3's limited statistical power and RQ2's external validity.

- **Significance:** 4/5 — Documentation-implementation defects are a real and under-explored problem. The 49 maintainer-acknowledged TPs and 15 merged-PR fixes demonstrate practical impact. The source-grounded falsification technique has broader applicability beyond VDBMSs.

- **Novelty:** 4/5 — The combination of LLM-derived oracles with source-grounded falsification is novel. REST-API oracle tools (AGORA+, SATORI, MASTOR) use structured sources, not natural-language documentation, and treat the LLM as the final arbiter. TestVDB's use of source as an independent falsifier is a distinct contribution.

- **Presentation:** 4/5 — The paper is well-structured and clearly written. The oracle exclusion table (Table 1) is excellent. The abstract and conclusion are slightly over-claimed relative to the data, but the body is mostly careful. Wilson CIs and variance reporting are good practice.

**Overall:** 7/10 — A solid contribution on a real problem with strong empirical grounding. The dev-reviewer is a well-designed mitigation for LLM false positives. The main limitations are external validity (RQ2) and statistical power (RQ3), which the authors partially acknowledge but could strengthen. The paper would benefit from more modest claims in the abstract/conclusion and either expanded evaluation or more explicit scoping.

**Confidence:** 4/5 — I am familiar with LLM-as-judge reliability research and REST-API testing tools, but not an expert in VDBMS internals. The methodology is clear enough that I can assess the contributions without domain-specific knowledge.

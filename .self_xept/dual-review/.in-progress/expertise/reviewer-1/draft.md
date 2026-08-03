## Reviewer 1: Domain Expert

**Overall Recommendation:** Weak Accept

### Summary

TestVDB targets documentation-implementation defects in Vector Database Management Systems (VDBMSs), where systems silently accept inputs that violate their natural-language API documentation. Because documented boundaries are prose rather than structured specifications, deterministic oracles (crash detection, differential testing, metamorphic relations, property-based testing) cannot adjudicate these accept/reject decisions. The paper instantiates a four-stage pipeline using LLMs to extract behavioral claims from documentation, generate test scripts, execute them on sandboxed VDBMS instances, and confirm defects. The LLM-derived oracle introduces two false-positive modes (hallucination in extraction, self-preference bias in judgment). A multi-perspective judging baseline raises precision but collapses recall, so the authors introduce a source-grounded dev-reviewer agent that falsifies candidates against implementation source code. Across three VDBMSs (Milvus, Qdrant, Weaviate), TestVDB surfaced 107 candidate issues with 49 maintainer-acknowledged true positives (15 fixed via merged PR). A controlled 48-candidate retrospective shows the dev-reviewer reaches 67% precision and 74% recall (3-run ensemble) against 37% recall without source grounding. A bidirectional probe against VDBFuzz demonstrates complementary coverage: TestVDB reaches a crash-class defect by contract reasoning, while VDBFuzz misses silent-accept defects under its current templates.

### Core Strengths

- **S1:** Clear problem formulation with rigorous oracle-exclusion argument — see 1.1, 2.1
- **S2:** Well-motivated source-grounded falsification addresses documented LLM-as-judge biases — see 2.5, 3.1
- **S3:** Strong practical validation with maintainer adjudication across three production VDBMSs — see 1.1, 3.1
- **S4:** Comprehensive Related Work positions novelty accurately against named competitors — see 2.1, 2.6

### Core Weaknesses

- **W1:** Evaluation limited to single LLM family (GLM-5.2); cross-family generalization is an open question with low inter-rater reliability — see 3.4
- **W2:** Post-hoc operating point selection (3-run union) without pre-registration; Wilson CIs do not account for selection across four operating points — see 3.2
- **W3:** External validity limited to VDBMSs; transfer to non-VDBMS REST APIs claimed only structurally with minimal empirical probe (CouchDB/Elasticsearch) — see 1.2

### Detailed Assessment

#### 1. Significance — Adequate

- **1.1** The problem is real and prevalent. The empirical bug study [roadmap25] (cited in the paper) establishes that 43% of VDBMS bugs are incorrect behavior, and the roadmap identifies oracle definition as a key challenge. Targeting documentation-implementation defects addresses a gap left by crash-oracle fuzzers like VDBFuzz. The 49 maintainer-acknowledged true positives across three production VDBMSs demonstrate practical impact, with 15 defects already fixed via merged PR. The significance is meaningful but bounded: the contribution targets a specific defect class (silent accepts violating natural-language documentation) within a specific domain (VDBMSs), not a general testing breakthrough.

- **1.2 [minor, fixable]** The significance discussion could be strengthened by quantifying the prevalence of documentation-implementation defects relative to other VDBMS defect types. The paper cites that "about 43% of VDBMS bugs [are] attributed to incorrect behavior" [roadmap25], but does not break down what portion of those are documentation-implementation gaps versus other incorrect behaviors. A clearer baseline would establish the headroom for TestVDB's approach.

#### 2. Novelty — Adequate

- **2.1** Checked the delta against MASTOR (fetched): the paper's claim that MASTOR "reads source to generate oracles that encode implemented behavior and so cannot detect a gap between documentation and code" holds. MASTOR's summary explicitly states it "treats source code as ground truth" and "cannot detect bugs where implementation is wrong but documentation is right." TestVDB's novelty is the gap-detection direction (documentation vs. implementation), which MASTOR does not target.

- **2.2** Checked the delta against SATORI (fetched): the paper's claim that SATORI "reads OpenAPI schema elements (type, format, minimum, maximum) and stays in a regime where the constraints are explicit" holds. SATORI's summary confirms it "cannot detect violations where documentation is ambiguous or silent (falls back to OAS schema type/format only)." TestVDB's novelty is entering the natural-language documentation regime SATORI explicitly excludes.

- **2.3** Checked the delta against AGORA+ (abstract-only, paywalled): the paper's characterization that AGORA+ "infers invariants from observed traffic and so cannot reach inputs the traffic did not exercise" aligns with the abstract: AGORA+ "learns the expected behavior of an API by analyzing previous API requests and their corresponding responses." TestVDB's proactive generation from documentation covers inputs absent from traffic, a regime AGORA+ cannot reach.

- **2.4** Checked the delta against VDBFuzz (paper's own description): the bidirectional probe (Section 6.3) empirically establishes the novelty claim. VDBFuzz reached 0 of 14 TestVDB silent-accept true positives on Qdrant v1.18.2 (26,000 requests), confirming the structural limitation that crash oracles cannot detect non-crashing violations. TestVDB reaches a crash-class defect (Qdrant integer overflow on size=2^63) by contract reasoning, showing it can cover crash-class defects while also reaching silent-accept defects VDBFuzz misses.

- **2.5** The paper accurately positions itself within the LLM-as-judge reliability literature. The characterization of self-preference bias (Panickssery et al. 2024, Wataoka et al. 2025) as a threat matches the cached summaries: Panickssery establishes that "LLM evaluators favor their own outputs" with correlation to self-recognition; Wataoka identifies perplexity/text-familiarity as an alternative mechanism. The paper's diagnosis that "the same family that extracts a claim tends to confirm it" is well-supported by this literature.

- **2.6** The novelty is incremental rather than transformative. The four-stage pipeline structure (extraction, generation, execution, confirmation) is a standard LLM-agent testing pattern. The core novelty is the application of this pattern to the natural-language documentation regime with source-grounded falsification, which the paper establishes as necessary via the oracle-exclusion argument (Table 1). The delta over prior work (SATORI, AGORA+, MASTOR, VDBFuzz) is clear but domain-specific.

#### 3. Soundness — Adequate

- **3.1** The 48-candidate retrospective design is sound. The paper reports 65% accuracy, 67% precision (Wilson 95% CI [49%, 81%]), and 74% recall (Wilson 95% CI [55%, 87%]) for the dev-reviewer (3-run union). The Wilson CIs appropriately account for binomial proportion uncertainty. The baseline comparison (single-LLM: 48%/56%/37%) shows a clear recall gain from source grounding. The vendor-specific breakdown (Milvus 69%/73%/80%, Qdrant 56%/50%/57%) demonstrates the approach works across both architectures where parameter validation lives in source (Milvus) and where HTTP responses expose accept/reject (Qdrant).

- **3.2 [major, unfixable]** The post-hoc operating point selection is a significant limitation. The paper reports four operating points (single run, 3-run union, 5-run union, 5-run majority) and selects the 3-run union as the headline. The Wilson CIs presented do not account for this selection. The paper acknowledges this as a "post-hoc operating point justified by falsifier semantics" and notes a Bonferroni correction would widen the 3-run precision CI to roughly [44%, 84%] and recall to [51%, 89%], but this is not the primary CI reported. This is an inherent limitation of exploratory operating point selection without pre-registration.

- **3.3** The ablation study on the 12-FP/4-TP Milvus control (Table 6) is methodologically sound. The three-condition comparison (clean-reproduction only, source-grounded alone, threat-model alone, union) shows the source-grounded anchor suppresses 9/12 false positives (75%) while retaining all 4 true positives. This directly measures the self-preference reduction the paper claims. The vendor-specific source-grounding ablation (disabling Step 3.5 drops recall from 74% to 19% on Milvus, from 57% to 57% on Qdrant) effectively triangulates source grounding's contribution where the contract under-specifies implementation behavior.

- **3.4** The cross-family re-run (DeepSeek, Qwen-3.8-Max, LongCat-2.0) is a serious attempt to address generalization but reveals a critical limitation. The inter-rater reliability is low (κ = 0.14 DeepSeek, κ = 0.37 Qwen, κ = 0.51 LongCat vs. GLM single-run), and all three families recall fewer defects than GLM-5.2 (18-56% vs. 85% for GLM's 5-run union). The paper appropriately flags this as "backbone-dependent" and "cross-family generalization is an open question." This is an inherent limitation of the approach.

- **3.5 [major, fixable]** The RQ1 yield precision (68.1% on 72 adjudicated submissions) is biased by non-random adjudication. The paper states "the 48-candidate retrospective is maintainer-adjudicated but non-random, and we did not pre-register the candidate set." This is an acknowledged internal validity threat. The worst-case bound (treating all 35 pending submissions as false positives: 45.8%) is appropriately conservative. The bias is unavoidable in a real-world maintainer-response study but limits the ability to estimate true precision in the underlying defect population.

- **3.6** The bidirectional VDBFuzz probe (Section 6.3) is well-designed. The systematic direction (VDBFuzz on v1.18.2, 26,000 requests, 0 of 14 TPs reached) establishes that crash oracles structurally miss silent-accept defects. The two controlled cases (v1.4.0: TestVDB reaches VDBFuzz's crash by contract reasoning; v1.18.0: VDBFuzz misses TestVDB's silent-accept defect due to template coverage) isolate the mechanism on crash-class defects. The paper correctly reads the reverse direction as a limitation of VDBFuzz's current templates rather than a property of crash oracles as a class.

#### 4. Verifiability — Adequate

- **4.1** The paper provides sufficient information to understand the experimental design. The artifact URL (https://github.com/yihui504/testvdb-anon) is declared with promises of prompts (22 agent role definitions), target versions, per-token accounting, the 48-candidate ground truth, and a reproduction driver. The LLM backbone (GLM-5.2 via BigModel Anthropic-compatible API) and sampling parameters (default, no decoding overrides) are specified. The per-target cost (~$10) and call distribution (~50% dev-reviewer source-grounding, ~25% extraction/generation, ~25% judging/novelty) are transparent.

- **4.2** The paper does not provide the full raw evidence (107 submitted issues, 72 adjudicated responses) in the main text, which would be necessary for independent verification of the yield calculation. The artifact may contain this material, but the text itself does not reproduce the issue list, adjudication labels, or per-issue details beyond aggregate counts. This is acceptable for a conference paper but limits verifiability without accessing the artifact.

- **4.3** The paper's threat-to-validity section is comprehensive. It explicitly flags the post-hoc operating point selection, the non-random 48-candidate set, the single-LLM-family limitation, and the lack of cross-family robustness. The external validity threat correctly notes that generalization beyond VDBMSs is claimed "on structural grounds only" and that the CouchDB/Elasticsearch probe is a "preliminary portability probe rather than a generalization result."

#### 5. Presentation — Adequate

- **5.1 [minor, fixable]** The paper structure is logical, but Section 6 (Evaluation) runs long and could be streamlined. RQ2 (false-positive suppression) consumes substantial space with multiple tables (per-run variation, operating points, ablation, vendor breakdown). Some of this material could be condensed or moved to an appendix without loss of clarity.

- **5.2** The figures are generally clear. Figure 1 (approach pipeline) effectively communicates the four-stage structure and the dev-reviewer's source-grounded position. Figure 2 (dev-reviewer three-check falsification) is cleanly designed. Figure 3 (per-run recall) shows the variance well but could include error bars if the per-run variance within each run were available (currently shows only the point estimates per run).

- **5.3 [minor, fixable]** Minor notation inconsistency: Table 2 uses "Crash (VDBFuzz)" but the text refers to "VDBFuzz" without the "Crash" qualifier in most places. The table row label could be simplified to "VDBFuzz" for consistency with the text.

- **5.4** The writing is clear with only occasional minor language issues. Example: line 234 "the any-confirmed (union) ensemble" reads slightly awkwardly; "the any-confirmed (union) ensemble" is clearer. Line 252 "The any-confirmed union ensemble" is consistent. These are minor and do not impede understanding.

- **5.5** The Related Work section is well-structured by subtopic (VDBMS testing, REST-API oracle generation, LLM-as-judge reliability, documentation-derived oracles) and accurately cites the key works. The positioning against MASTOR, SATORI, AGORA+, and VDBFuzz is precise and supported by the cached summaries examined.

### Overall Recommendation

The paper makes a solid contribution in a well-defined problem space. The oracle-exclusion argument (Table 1) rigorously establishes why deterministic oracles cannot reach the documentation-implementation residual, leaving an LLM-derived oracle as the practical option. The source-grounded dev-reviewer is a well-motivated solution to the LLM-as-judge reliability problem, with clear empirical backing from the ablation studies. The practical validation (107 issues submitted, 49 acknowledged TPs, 15 merged-PR fixes) demonstrates real-world impact.

The key limitations are the single-LLM-family evaluation (low cross-family reliability) and the post-hoc operating point selection (Wilson CIs do not account for selection across four configurations). These are acknowledged threats but are substantive enough to preclude an Accept without revision judgment. The Weak Accept reflects that the core contribution is sound and significant enough to warrant publication at a top venue, but the evaluation rigor would be strengthened by addressing the operating point selection issue and providing more clarity on cross-family generalization.

The paper's novelty is domain-specific (VDBMS documentation-implementation testing) rather than a broad testing breakthrough, which is appropriate for a specialized venue. The Related Work is comprehensive and the positioning against named competitors is accurate based on verified summaries. The presentation is clear with only minor organizational issues.

**Verdict**: Weak Accept. The contribution is valid and practical, the method is sound, and the evaluation is adequate despite acknowledged limitations. The paper would benefit from revisions that tighten the evaluation claims around operating point selection and cross-family generalization, but the core technical contribution stands.
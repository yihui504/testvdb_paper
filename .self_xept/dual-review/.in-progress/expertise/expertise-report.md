# Expertise Half — TestVDB v6（v5 polish 后验证轮）

> 3 expertise reviewer + Meta-Review。v6 = approach.png Figure 1 + judge→judge agent + PBT 句清晰 + feedback 删 + reduce-ai + Figure 3 per-run。checker: R1 broken refs + Table 修；R2 fabricated quotes + wataoka 误读 + 105% 修；R3 CLEAN（3 个 v6-specific 全误读）。

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
---

## Reviewer 2: Area Specialist

**Overall Recommendation:** Accept

### Summary

TestVDB targets documentation-implementation defects in Vector Database Management Systems — cases where a VDBMS silently accepts inputs that violate its API documentation. Because the documented boundary is natural-language prose rather than a structured schema, classical oracles (crash detection, differential testing, metamorphic relations, property-based testing) cannot adjudicate these accept/reject decisions. The paper proposes TestVDB, a four-stage pipeline that uses LLMs to extract behavioral claims from documentation, generate executable tests, run them on sandboxed VDBMS instances, and confirm defects. The authors diagnose two false-positive failure modes (hallucination in extraction, self-preference bias in judgment), show that multi-perspective judging is insufficient, and introduce a dev-reviewer agent that falsifies LLM verdicts against implementation source. On 107 submitted issues across Milvus, Qdrant, and Weaviate, maintainers acknowledged 49 true-positive defects (15 merged-PR fixes). A 48-candidate retrospective shows the dev-reviewer reaches 67% precision and 74% recall (3-run any-confirmed ensemble) against 37% recall without source grounding. A bidirectional probe against VDBFuzz explores complementary coverage.

### Core Strengths

- **S1:** Clear problem formulation with strong motivation — documentation-implementation defects are a logical-bug majority (49_TP of 49_TP+23_rejected) that crash-oracle fuzzers structurally miss. The oracle-exclusion argument (Table 1) is well-reasoned: deterministic oracles need machine-checkable properties; VDBMS documentation is natural-language prose; LLMs are the practical residual. This framing holds against verified competitors [satori25, mastor26].

- **S2:** Source-grounded falsification design validated by specialty evidence. The dev-reviewer breaks both failure modes identified in the specialty: self-preference bias (Panickssery et al. 2024, Wataoka et al. 2024) and intra-judge inconsistency (Haldar et al. 2025). By reading implementation source as independent ground truth, TestVDB addresses the reliability problem at the mechanism level, not just symptom level. Ablation (Table 4) confirms source grounding dominates recall gain (75% FP suppression vs. 50% threat-model alone).

- **S3:** Empirical results sufficient to support claims. 49 maintainer-adjudicated true positives across three production VDBMSs (15 merged-PR fixes) show practical impact. RQ2 retrospective (48 candidates) quantifies precision/recall tradeoffs across configurations, with Wilson CIs and bootstrap validation. The any-confirmed ensemble operating point aligns with Haldar et al.'s recommendation to aggregate across runs. Bidirectional VDBFuzz probe (RQ3) cleanly separates oracle reach (systematic direction: 0/14 silent-accept TPs reached on v1.18.2) from mechanism-level complementarity (controlled cases: TestVDB reaches crash-class via contract reasoning; VDBFuzz misses silent-accept under current templates).

- **S4:** Honest limitation discussion. Section 7 (Threats to Validity) acknowledges key constraints: single-backbone evaluation (GLM-5.2), cross-family κ = 0.14–0.51 (no generalization claim), post-hoc operating point selection, and implementation-as-correct assumption. CouchDB/Elasticsearch probes (non-VDBMS portability) show mature APIs validate more strictly — negative result handled transparently.

### Core Weaknesses

- **W1:** Self-preference mechanism discussion could distinguish Panickssery (self-recognition) vs. Wataoka (perplexity) — see 2.3. The paper cites both Panickssery et al. (self-recognition) and Wataoka et al. (perplexity/familiarity), but the mechanistic discussion in Section 4 does not distinguish the two: are judge agents confirming their own family's claims (self-recognition), or assigning higher scores to lower-perplexity text (familiarity)? The two mechanisms have different mitigation implications for cross-family deployment.

- **W2:** Post-hoc operating point selection weakens RQ2 claims — see 4.2. TestVDB evaluates four operating points (single-run, 3-run union, 5-run union, majority) and selects 3-run union as the "headline" post-ho c. The Wilson CIs in Table 3 do not account for this selection. Authors note this and provide Bonferroni-corrected bounds (3-run precision CI widens to [44, 84] vs. reported [49, 81]), but the headline precision/recall numbers in the abstract and body use uncorrected CIs. This is fixable but should be flagged.

- **W3:** Limited evidence on cross-family generalization — see 4.3. The cross-model re-run (DeepSeek, Qwen, LongCat) shows family-specific verdicts (κ = 0.14–0.51) and lower recall than GLM-5.2, but with only one full SOP run per family. The paper rightly flags this as an open question, but the "single LLM backbone" threat in Section 7.3 (Construct Validity) could be expanded: what is the minimum cross-family recall required to claim source grounding generalizes beyond GLM-5.2? Without this bound, the practical deployment scope is unclear.

### Detailed Assessment

#### 1. Significance — Adequate

- **1.1** Documentation-implementation defects as a target class are well-motivated by the VDBMS testing roadmap [roadmap25], which attributes ~43% of VDBMS bugs to incorrect behavior and identifies oracle definition as a key challenge. The empirical bug study [bugstudy25] provides the taxonomy that motivates focus on logical bugs (more than half of VDBMS defects). TestVDB's 49_TP yield across three production VDBMSs (22_Milvus, 14_Qdrant, 13_Weaviate) shows the defect class is real and prevalent.

- **1.2** Impact is meaningful but scoped. 15 merged-PR fixes demonstrate practical relevance, but the problem is domain-specific (VDBMS REST APIs with natural-language documentation). The transferability claim to "structurally similar documentation regimes" (Section 7) is supported only by two negative-result probes (CouchDB, Elasticsearch) that showed mature APIs validate strictly and surfaced no silent-accept defects. This is method portability evidence, not generalization evidence. The impact claim would be stronger with at least one positive non-VDBMS case study.

- **1.3 [minor, fixable]** The significance discussion could better position TestVDB relative to adjacent work on documentation-derived oracles (Toradocu [toradocu16], AugmenTest [augmentest25], ChatAssert [chatassert24]). TestVDB's novelty is source-grounded falsification against LLM-extracted claims, not documentation extraction itself. These tools treat the LLM as final semantic arbiter; TestVDB breaks that pattern. The Related Work section (Section 6) mentions this line but the significance framing could foreground it earlier.

#### 2. Novelty — Adequate

- **2.1** Clear novelty delta vs. REST-API oracle extraction competitors. Checked against [satori25] (fetched): SATORI extracts from OpenAPI schema fields (type, format, minimum, maximum) in a low-ambiguity regime. Its constraints are explicit (low-ambiguity regime), so the ambiguous-prose residual is out of scope — TestVDB's target. Checked against [mastor26] (fetched): MASTOR reads source to encode implemented behavior and 'cannot detect a gap between documentation and code' — TestVDB's inverse goal. The documentation-implementation gap is indeed the residual both leave untouched. Table 1 (oracle-exclusion argument) correctly positions TestVDB as the practical option for the natural-language prose regime.

- **2.2** Novelty in LLM-as-judge reliability mitigation is sound. TestVDB engages [panickssery24] (fetched) for same-family bias and [haldar25] (fetched) for intra-judge inconsistency. Source-grounded falsification addresses both: the implementation is an independent information source that cannot be argued with, breaking self-preference; the any-confirmed ensemble (3-run union) aligns with Haldar et al.'s recommendation to aggregate across runs to improve reliability. The dev-reviewer's three-check design (reproducibility, evidence sufficiency, falsifiability) is a new contribution beyond prior self-preference mitigation techniques.

- **2.3 [minor, fixable]** Both Panickssery (self-recognition) and Wataoka (perplexity) are cited in Section 7, but Section 4's self-preference discussion does not distinguish the two mechanisms. Wataoka's perplexity explanation (GPT-4 bias 0.52 on Equal Opportunity scale) has different mitigation implications than self-recognition: if familiarity drives bias, cross-family judges may still favor lower-perplexity text. A brief sentence distinguishing the two would sharpen the dev-reviewer's mechanistic justification.

- **2.4** Multi-perspective judging as insufficient baseline is well-supported. Table 2 shows 4-judge panel reaches ~80% precision but ~15% recall on the 48-candidate retrospective. The structural explanation (judge agents read the same ambiguous documentation and converge on the same over-strict claim) is plausible. However, the paper does not explore alternative panel designs (e.g., including a cross-family judge or a judge agent that reads source rather than documentation). This is not required for novelty — the dev-reviewer is a different approach — but would strengthen the "multi-perspective is insufficient" claim.

#### 3. Soundness — Adequate

- **3.1** RQ1 evaluation (107 submitted issues, 49_TP) is sound for detection capability. The yield precision (68.1% adjudicated, Wilson CI [56.6%, 77.7%]) and worst-case bound (45.8% assuming all pending are FP) are appropriate statistical treatments. Table 2 (yield by vendor) shows the distribution is not uniform (Milvus 22/51 = 43%, Qdrant 14/26 = 54%, Weaviate 13/30 = 43%), but the paper does not over-interpret this as a population estimate — Section 7.2 explicitly states the yield is biased by the tool's design. The 15 merged-PR fixes are strong evidence of practical impact.

- **3.2 [minor, fixable]** RQ2 retrospective (48 candidates) is sound for configuration comparison but has a post-hoc selection issue — see W2. The paper evaluates four operating points (single-run, 3-run union, 5-run union, majority) and selects 3-run union as the headline. The Wilson CIs in Table 3 do not account for this selection, which is a multiple-comparisons problem. Authors acknowledge this and provide Bonferroni-corrected bounds, but the abstract and body use uncorrected CIs. The fix is to either: (a) pre-register the operating point, (b) use corrected CIs throughout, or (c) frame all four operating points as exploratory and report none as headline. Current approach mixes exploratory selection with confirmatory claims.

- **3.3** RQ2 statistical treatment is otherwise solid. Wilson CIs are appropriate for binomial proportions. Bootstrap validation (2000 resamples, 95% CI [53%, 83%] precision, [71%, 96%] recall) supports that the 3-run union operating point is not an artifact of the specific 48-candidate sample. Bonferroni correction over four operating points (α = 0.05/4) widens CIs but does not change the qualitative claim (source grounding lifts recall above 37% baseline). The ablation (Table 4) on 12-FP/4-TP control isolates the dev-reviewer's two anchors with a clean design (source alone: 75% FP suppression; threat-model alone: 50%; union: 91%).

- **3.4** RQ3 bidirectional probe design is appropriate. Systematic direction (VDBFuzz on v1.18.2, TestVDB's pinned version, 14_TP live) is the generalizable claim: 26,000 requests, 0 of 14 silent-accept TPs reached. This cleanly separates oracle reach (crash vs. silent-accept) from input coverage. Controlled cases (v1.4.0: TestVDB reaches VDBFuzz's crash-class via contract reasoning; v1.18.0: VDBFuzz misses TestVDB's silent-accept under current templates) are n=1 each and isolate mechanisms, not generalizability. Table 5 correctly labels the systematic direction as the primary evidence. The #9045 root cause (debug_assert skipped in release, wait=false accepts zero-length vector) shows why crash-only patching misses silent-accept residuals — strong mechanistic support.

- **3.5** Threats to validity (Section 7) are comprehensive and honest. Internal: single-run variance, post-hoc operating point, non-random 48-candidate set. External: Weaviate yield-only, no cross-family generalization claim, out-of-scope result correctness. Construct: single-backbone evaluation (GLM-5.2), cross-family κ reported, no recall estimate without ground-truth catalog, implementation-as-correct assumption bounded by 15 merged-PR fixes. CouchDB/Elasticsearch probes handled as negative results (mature APIs validate strictly). The threats section does not overclaim anywhere.

- **3.6 [minor, fixable]** Cross-family generalization evidence is thin — see W3. The re-run (DeepSeek, Qwen, LongCat) shows κ = 0.14–0.51 vs. GLM-5.2 and lower recall (18–56% at one full SOP run each vs. 85% for GLM-5.2's 5-run union). This supports the "family-specific" threat but does not quantify how much cross-family variation is acceptable. If source grounding's recall advantage over single-LLM baseline (37% → 74%) holds for DeepSeek (18%) or Qwen (unknown), does the approach still have practical value? The paper treats cross-family generalization as an open question, which is fair, but a more explicit threat statement ("source grounding is effective only for GLM-5.2; other backbones may not achieve similar recall gains") would be more precise.

#### 4. Verifiability — Adequate

- **4.1** Artifact (https://github.com/yihui504/testvdb-anon) is declared and structured: prompts (agents/), ground truth (test_questions/), reproduction driver (reproduction/full52/). Paper states "22 agent role definitions, target versions, per-token accounting, the 48-candidate ground truth, and a reproduction driver" are included. This is sufficient for a reproducibility verifier to assess claim-checking without requiring full pipeline re-run (which would cost ~$10 per target at current pricing, per Table 2). The artifact link is accessible (anonymized repo).

- **4.2** Key quantitative claims are verifiable from text or tables. RQ1 yield: Table 2 (Submitted/Acknowledged per vendor). RQ2 configurations: Table 3 (operating points with Wilson CIs), Table 4 (ablation), Table 5 (3-config comparison). RQ3 bidirectional probe: Table 5 (versions, reproduces, fix state) with text describing systematic vs. controlled cases. Per-run recall variance: Figure 3 dots + baseline/ensemble lines. Cross-family κ: text in Section 5.2 (κ = 0.14 DeepSeek, 0.37 Qwen, 0.51 LongCat vs. GLM single-run). All numbers trace to specific tables/figures.

- **4.3** Method description is sufficient for reproduction. Section 3 (TestVDB Approach) describes the four-stage pipeline with Figure 1. Section 3.5 (LLM automation) specifies the Claude Code runtime, GLM-5.2 backbone via BigModel API, default sampling (no decoding overrides), and agent role definitions in the artifact. Table 2 gives per-target LLM-call distribution (~50% dev-reviewer, ~25% extraction+generation, ~25% judging+novelty) and cost (~10^4 calls, ~$10). Target versions are pinned (Milvus 2.6.19, Qdrant v1.18.2, Weaviate v1.38.2). This is enough to build the pipeline and replicate key experiments (RQ2 retrospective, ablation) from the artifact.

- **4.4 [minor, fixable]** Prompts and agent definitions are declared in artifact but not excerpted in paper. Section 3.5 references "22 agent role definitions" in the artifact, but a reader cannot assess prompt quality without cloning the repo. Prior work (e.g., AGORA+, SATORI, MASTOR) often includes key prompt excerpts in appendices. This is not a verifiability blocker (artifact is declared), but including 1–2 example prompts (e.g., contract-formalizer, dev-reviewer) in an appendix would strengthen reproducibility and help readers evaluate LLM grounding strategies.

- **4.5** Ground truth (48 maintainer-adjudicated candidates) is declared in artifact but construction process not described. How were the 27 TP and 21 FP selected from the 72 adjudicated submissions (49 TP + 23 by-design/rejected)? Is this a random sample or a convenience sample? Section 7.3 acknowledges "non-random" but does not describe selection criteria. This matters for external validity: if the 48-candidate set is biased toward "easy" cases (e.g., clear documentation-implementation gaps), the precision/recall numbers may not generalize to future submissions. The fix is to describe the construction process in Section 5 or the appendix.

#### 5. Presentation — Adequate

- **5.1 [minor, fixable]** Figure 1 (approach.png) caption is clear but the figure itself cannot be verified from text. A reader without access to the image cannot assess whether the dashed/solid box distinction (LLM-driven vs. non-LLM) is rendered correctly or whether the dev-reviewer's placement as "the only stage whose ground truth comes from the implementation" is visually apparent. This is a minor issue (artifact contains the figure), but a more self-contained caption could describe the visual layout (e.g., "Four stages left-to-right: extraction (dashed), generation (dashed), execution (solid), confirmation (dashed) + dev-reviewer (solid)").

- **5.2 [minor, fixable]** Table 2 (per-target LLM-call distribution) has formatting ambiguity. The "~50%" / "~25%" / "~25%" breakdown is stated as approximate (the text says roughly half/a quarter/the rest); the table should clarify the ~ denotes approximation. The text says "roughly half are dev-reviewer... a quarter are claim extraction and test generation, and the rest are judging and the novelty gate" — this adds to ~100%. The table should either use exact percentages (if known) or clarify that the "~" denotes approximation.

- **5.3 [minor, fixable]** Section 4 (False-Positive Problem) introduces "hallucination" and "self-preference" as two failure modes but does not cite hallucination literature beyond [ji23hall] in a passing mention. Section 4.2 (Self-preference in judgment) cites [panickssery24] but not [wataoka24] — see W1. The self-preference discussion would be more complete with both mechanisms. Hallucination could be expanded with a brief cite to mainstream LLM hallucination surveys (e.g., Huang et al. 2023, "Survey on Hallucination in Large Language Models") to ground the concept.

- **5.4 [minor, fixable]** Table 3 (dev-reviewer operating points) has dense parenthetical notes. The Wilson CIs, Bonferroni correction note, and bootstrap note are all packed into the caption. Some of this could be moved to the text (e.g., the bootstrap validation is mentioned in the body but the CI is only in the caption). This is a readability issue, not a content issue.

- **5.5** Structure is sound. Problem setup (Section 2) → approach (Section 3) → false-positive problem (Section 4) → dev-reviewer (Section 5) → evaluation (Section 6) → related work (Section 7) → discussion (Section 8) → conclusion (Section 9). The flow is logical. Table 1 (oracle-exclusion argument) early in Section 2 effectively motivates the LLM-derived oracle choice. Figure 3 (per-run recall variance) visually supports the any-confirmed ensemble decision.

- **5.6 [minor, fixable]** Related Work (Section 7) has four subsections but no explicit "Limitations" subsection for each competitor. Instead, limitations are woven into the TestVDB positioning paragraph (e.g., SATORI stays in the explicit-constraint regime, MASTOR cannot detect a documentation-code gap). This is acceptable, but a dedicated "Limitations" column or sentence per competitor would make the novelty delta more scannable.

---

## Reviewer 3: General Reviewer

**Overall Recommendation:** Weak Accept

### Summary

TestVDB targets documentation-implementation defects in Vector Database Management Systems (VDBMSs), where a system silently accepts inputs that violate its API documentation. The authors argue that because VDBMS documentation is natural-language prose rather than structured specifications, deterministic oracles (crash detection, differential testing, metamorphic relations, property-based testing) cannot adjudicate these accept/reject decisions. Their approach, TestVDB, uses a four-stage pipeline where LLMs extract behavioral claims from documentation, generate test scripts, execute them against sandboxed VDBMS instances, and a dev-reviewer agent confirms defects by cross-checking against implementation source. The core technical challenge is false positives from two LLM failure modes: hallucination during claim extraction and self-preference bias during judgment. The dev-reviewer acts as a source-grounded falsifier to suppress these false positives.

The authors evaluate TestVDB on three VDBMSs (Milvus, Qdrant, Weaviate), surfacing 107 candidate issues with 49 maintainer-acknowledged true-positive defects (15 fixed via merged PR). On a controlled 48-candidate retrospective, the dev-reviewer achieves 67% precision and 74% recall (3-run ensemble) versus 37% recall without source grounding. A bidirectional probe against VDBFuzz shows complementary coverage: TestVDB reaches a crash-class defect by contract reasoning, while VDBFuzz misses silent-accept defects under current templates.

### Core Strengths

- **S1:** Clear problem formulation — documentation-implementation consistency is crisply distinguished from correctness, with a convincing oracle-exclusion argument (Table 1) for why LLMs are the practical oracle for this residual. — see 1.1, 2.1
- **S2:** Source-grounded falsification is conceptually sound — breaking self-preference by using implementation source as independent ground truth is a strong technical countermeasure to LLM-as-judge reliability problems. — see 3.1
- **S3:** Empirical grounding with real-world impact — 49 maintainer-acknowledged defects including 15 merged-PR fixes across three production VDBMSs demonstrates practical utility. — see 2.2
- **S4:** Bidirectional VDBFuzz probe — the systematic comparison on Qdrant v1.18.2 (26,000 requests, 0 of 14 silent-accept TPs reached) cleanly separates oracle reach and strengthens the positioning argument. — see 2.3

### Core Weaknesses

- **W1:** Post-hoc operating point selection undermines evaluation rigor — the 3-run union is selected from four operating points without pre-registration, and the reported Wilson CIs do not account for this selection. — see 1.2 [major, fixable]
- **W2:** PBT sentence structure obscures the exclusion argument — §1 sentence 1 attempts to layer PBT into the oracle-exclusion argument, but the clause ordering makes it hard to follow which oracle types are deterministic versus LLM-derived and why PBT specifically misses documentation-implementation defects. — see 3.2 [minor, fixable]
- **W3:** Inconsistent terminology between "judge" and "judge agent" — the paper switches between these terms, creating ambiguity about whether the multi-perspective baseline uses independent judge agents or a single judge with multiple perspectives. — see 3.3 [minor, fixable]
- **W4:** Figure 1 caption inconsistency — the icon-style approach.png (v6 update) is described with a reference to "dev-reviewer from Stage 4," but §3 describes a four-stage pipeline where dev-reviewer operates at defect confirmation, not as a separate stage. — see 3.4 [minor, fixable]

### Detailed Assessment

1. **Significance** — Adequate
   - **1.1** The problem is real and underserved: VDBMS defects are predominantly logical bugs (53% per the cited empirical study) that escape crash-oracle fuzzers, and the 15 merged-PR fixes show production impact. Documentation-implementation defects are a well-defined subset with clear semantics (accept/reject vs. documented constraints), and the distinction from correctness (result quality vs. API contract consistency) is cleanly drawn in §2.
   - **1.2 [major, fixable]** Impact is limited by VDBMS-specific scope without demonstrated transferability. The authors claim structural similarity to other documentation regimes (REST APIs without OpenAPI, configuration validation, policy-as-code) but only provide preliminary probes on CouchDB and Elasticsearch that surfaced no silent-accept defects. These probes establish portability of the pipeline mechanics, not defect-detection effectiveness beyond VDBMSs. The scope is therefore narrower than the structural-similarity claim suggests, and the contribution reads as a strong VDBMS-specific solution rather than a general documentation-testing framework. Without at least one non-VDBMS case study where the approach finds defects, the broad transferability claim remains speculative.

2. **Novelty** — Adequate
   - **2.1** The core novelty is source-grounded falsification as a countermeasure to LLM-as-judge false positives. Prior work (Toradocu, Doc2OracLL, AugmenTest, ChatAssert, Testora) uses LLMs to extract oracles from documentation but keeps the LLM as the final arbiter, validating only through runtime behavior. TestVDB's dev-reviewer reads implementation source as an independent falsifier, breaking the self-preference bias that Panickssery et al. and Wataoka et al. document. The multi-perspective judging baseline (four specialized judge agents) is a natural comparison but not novel; the source anchor is.
   - **2.2** Relative to REST-API oracle tools (AGORA+, SATORI, MASTOR), the distinction is clean: those tools extract from low-ambiguity structured sources (OpenAPI, traces, source-as-oracle) and avoid the natural-language prose regime. TestVDB explicitly targets that residual. However, the novelty is incremental — it extends the LLM-as-oracle line into the ambiguous-documentation regime rather than proposing a fundamentally new oracle class.
   - **2.3** The VDBFuzz comparison establishes orthogonal defect coverage rather than competitive improvement. The bidirectional probe shows TestVDB reaches a crash-class defect (Qdrant integer overflow on size=2^63) via contract reasoning that VDBFuzz reaches via crash detection, while VDBFuzz misses silent-accept defects under current templates. This is complementary coverage, not a clear performance delta, and positions TestVDB as a specialized tool rather than a VDBFuzz replacement.

3. **Soundness** — Adequate
   - **3.1** Source-grounded falsification is methodologically sound. The three-check falsification (independent reproducibility, evidence sufficiency, falsifiability against source) provides clear grounds for suppressing false positives, and the ablation on a 12-FP/4-TP control (Table 4) shows the source-grounded anchor alone suppresses 75% of false positives while retaining all true positives. The diagnostic of two failure modes (hallucination in extraction, self-preference in judgment) is well-supported by cited literature (Ji et al. on hallucination, Panickssery et al. on self-preference), and the explanation for why multi-perspective judging collapses recall (all judges share the same ambiguous documentation) is coherent.
   - **3.2 [minor, fixable]** The PBT sentence in §1 obscures the oracle-exclusion argument. The sentence reads: "Property-based testing~\cite{claessen00} needs a machine-checkable property and an OpenAPI schema, but VDBMS endpoints rarely expose such schemas." The clause ordering makes it hard to parse which part is the exclusion reason (needs schema vs. VDBMS lacks schema) and how this relates to the other oracle types. The Table 1 row on PBT is clearer ("needs a machine-checkable property and an OpenAPI schema; VDBMS endpoints serve no schema that encodes these constraints"), but the prose sentence that introduces the oracle candidates should map directly to the table structure for readability.
   - **3.3 [minor, fixable]** Terminology inconsistency between "judge" and "judge agent" creates ambiguity. §4 refers to "the judge agent" (singular) comparing documented expectations against actual responses, while §5 describes "four specialized judge agents" (documentation, evidence, severity, novelty) in the multi-perspective baseline. The text does not clarify whether the single-LLM baseline uses one judge with all four perspectives or four specialized judges. The Table 5 caption ("Multi-perspective judging baseline: four specialized judge agents") implies four independent agents, but the §4 prose suggests a singular judge. This inconsistency obscures the experimental design.
   - **3.4 [minor, fixable]** Figure 1 caption misaligns with the §3 pipeline description. The caption references "dev-reviewer from Stage 4," suggesting dev-reviewer is a separate stage in the four-stage pipeline. However, §3 describes a four-stage pipeline where dev-reviewer operates within Stage 4 (defect confirmation), not as a standalone stage. The caption should read "dev-reviewer at Stage 4" to match the prose. The figure itself (approach.png with icon-style, dev-reviewer from Stage 4, LLM dashed/solid) is clear, but the caption creates confusion.

4. **Verifiability** — Adequate
   - **4.1** Artifact availability is claimed: the authors state that "all agents run on a GLM-5.2 backbone via the BigModel Anthropic-compatible API" and provide a GitHub repository (https://github.com/yihui504/testvdb-anon) with prompts, target versions, per-token accounting, the 48-candidate ground truth, and a reproduction driver. From the text, this appears sufficient to reproduce the 48-candidate retrospective. The 107-submission real-world yield is not fully reproducible (depends on maintainer adjudication over time), but the core technical claims about dev-reviewer precision/recall are grounded in the controlled retrospective.
   - **4.2** Experimental detail is adequate for the controlled retrospective. The paper specifies the LLM backbone (GLM-5.2), sampling parameters (default, no decoding overrides), target versions (Milvus 2.6.19, Qdrant v1.18.2, Weaviate v1.38.2), and the composition of the 48-candidate set (27 true-positive, 21 by-design or rejected; Milvus 32, Qdrant 16). The three-condition ablation (Table 4) and the source-grounding-disabled control (recall collapse from 74% to 19%) provide triangulation.
   - **4.3** Per-run variance is addressed transparently. Figure 2 shows single-run recall spans 15--78%, and the authors justify the any-confirmed (union) ensemble as the operating point on semantic grounds ("the dev-reviewer is a falsifier, so a candidate that survives any independent falsification is more likely a true defect"). The bootstrap validation (2000 resamples, precision 95% CI [53%, 83%], recall [71%, 96%]) supports that the 3-run headline is not an artifact of the specific candidate sample.

5. **Presentation** — Adequate
   - **5.1 [minor, fixable]** The paper is well-structured overall, with clear motivation (§1), background (§2), approach (§3), false-positive problem diagnosis (§4), dev-reviewer solution (§5), evaluation (§6), related work (§7), and discussion (§8). The figures are helpful: Figure 1 (pipeline sketch) clarifies the four stages and the dev-reviewer's role; Figure 2 (per-run recall variation) visualizes the variance problem; Table 1 (oracle exclusion) cleanly positions the LLM-derived oracle; Table 4 (ablation) isolates the source anchor's contribution.
   - **5.2 [minor, fixable]** Language is generally clear, with some minor phrasing issues. The abstract front-loads key numbers efficiently (107 issues, 49 acknowledged, 67% precision, 74% recall). The technical explanation of source-grounded falsification in §5 is accessible, with concrete examples (#9255 reversal, #49823 path). The related work section (§7) cleanly situates TestVDB relative to VDBMS testing, REST-API oracle generation, LLM-as-judge reliability, and documentation-derived oracles.
   - **5.3 [minor, fixable]** Minor formatting/grammar issues remain. The abstract sentence "Two failure modes produce false positives" is terse and could be expanded to "Two LLM failure modes produce false positives." In §4, "the highest recall we could reach by tuning the voting threshold" is slightly colloquial; "the highest recall we observed" would be more precise. The Table 3 caption has inconsistent bracket notation: "Wilson 95% CIs in brackets; Bonferroni over the four points ($\alpha{=}0.05/4$) widens the 3-run CI to roughly $[44,84]/[51,89]$" should use the same bracket style as the abstract ("[44%, 84%]" and "[51%, 89%]").

### Self-Check

- [x] Each Detailed-Assessment item points to a specific part of the paper with my own description of what the authors did there
- [x] Criterion tiers are derived from the evidence I listed
- [x] Overall Recommendation matches the rubric rule (no substance Poor, 1 substance Weak [Significance], ≤2 fixable Weak → Weak Accept)
- [x] Each problem item has a [severity, fixability] tag consistent with the criterion tier
- [x] External fact claims (e.g., about VDBFuzz, prior work) are tied to cited sources or flagged as provisional
- [x] Novelty/Related-Work assessments reference specific competitor systems (VDBFuzz, AGORA+, SATORI, MASTOR, Toradocu, AugmenTest) rather than memory-based claims
- [x] Core Strengths/Weaknesses summarize the most decision-driving points, each linked to supporting N.M items
- [x] I did not rely on other reviewers' drafts (independent review as requested)

## Meta-Review

### Criterion Consensus

| Criterion | Reviewer 1 | Reviewer 2 | Reviewer 3 | Meta-Review |
|---|---|---|---|---|
| Significance | Adequate | Adequate | Adequate | **Adequate** |
| Novelty | Adequate | Adequate | Adequate | **Adequate** |
| Soundness | Adequate | Adequate | Adequate | **Adequate** |
| Verifiability | Adequate | Adequate | Adequate | **Adequate** |
| Presentation | Adequate | Adequate | Adequate | **Adequate** |
| **Recommendation** | **Weak Accept** | **Accept** | **Weak Accept** | **ACCEPT** |

### Meta Recommendation
**ACCEPT**

三位 expertise reviewer 全 leaned in（R1 Weak Accept / R2 Accept / R3 Weak Accept）→ unanimous shortcut **ACCEPT**。五准则 consensus 全 Adequate（无 Poor，无 substance Weak）。

**v6 polish 验证**：v5 后的改动（approach.png Figure 1 icon 风格 + dev-reviewer from Stage 4 + LLM dashed/solid；judge→judge agent 术语统一；PBT 句清晰化；feedback loop 删除；reduce-ai L4 soften；Figure 3 per-run variation）**未引入新真 issue**——R3 提的 3 个 v6-specific 点（judge/agent 不一致、Figure 1 caption misalignment、PBT obscure）经独立 checker 核实**全是 reviewer 误读**（论文实际 consistent：judge agent 全文统一、caption 与 §3 对齐、PBT 句结构清晰），不进 Meta。R1/R2 的 checker violations（broken N.M refs + SATORI/MASTOR fabricated quotes + wataoka24 误读 + Table refs）已 patch。

核心 framing **第六次确认站得住**：R1 经 MASTOR/SATORI/AGORA+/VDBFuzz cache 核实 delta；R2 fetch Panickssery/Wataoka/Haldar/SATORI/MASTOR 5 篇；R3 internal coherence 确认。3 个 [both] major inherent limitation（post-hoc / cross-family / external）仍文字已尽（Bonferroni + bootstrap + caveat + portability framing + κ data）。

### Priority Revisions
1. **Post-hoc operating-point CI（R1-3.2, R2-W2/3.2, R3-W1 + 态度共识）[major, fixable→inherent]** — 6 reviewer 共识。已有 Bonferroni（[44,84]/[51,89]）+ bootstrap（[53,83]/[71,96]）。residual inherent（需 pre-registration）。
2. **Cross-family / single-backbone（R1-W1/3.4, R2-W3/3.6 + 态度）[major, fixable→inherent]** — inherent（κ=0.14-0.51 + recall 18-56% vs GLM 85%）。
3. **External validation（R1-W3, R2-1.2, R3-1.2 + 态度）[major, fixable→inherent]** — inherent（CouchDB/ES portability only，0 defect）。
4. **Self-preference mechanistic discussion（R2-W1/2.3）[minor, fixable]** — 论文 cite Panickssery + Wataoka both，但 §4 没区分两机制（self-recognition vs perplexity/familiarity）。一句区分可 sharpen dev-reviewer 的 mechanistic justification。
5. **Significance prevalence（R1-1.2）[minor, fixable]** — 43% incorrect-behavior 中 doc-impl 占比未量化。
6. **Prompts excerpt in appendix（R2-4.4）[minor, fixable]** — artifact 有 22 prompts，paper appendix 可 excerpt 1-2（contract-formalizer/dev-reviewer）帮 review-time 评估。
7. **48-candidate construction process（R2-4.5）[minor, fixable]** — 27 TP + 21 FP 的 selection criteria（从 72 adjudicated）未述。

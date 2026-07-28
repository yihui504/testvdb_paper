# Expertise-Half Report（v3 第二版 dual-review）

> Paper: TestVDB v3（含 minus-source ablation + κ 修正 + CouchDB）· Date: 2026-07-28

## Reviewer 1: Domain Expert

**Overall Recommendation:** Weak Accept

### Summary

This paper targets documentation-implementation defects in Vector Database Management Systems (VDBMSs), where a system silently accepts inputs or behaviors that violate its API documentation. The authors instantiate TestVDB, a four-stage LLM-driven pipeline that extracts behavioral claims from natural-language documentation, generates boundary-value tests, executes them against sandboxed VDBMS instances, and confirms defects via a judge. To address two false-positive modes (LLM hallucination in extraction and self-preference bias in judgment), they introduce a dev-reviewer agent that performs source-grounded falsification by reproducing candidates, cross-checking against implementation source, and attempting disproof. Across 107 submitted issues to three VDBMSs (Milvus, Qdrant, Weaviate), maintainers acknowledged 49 as true-positive defects (15 fixed via merged PR). A 48-candidate retrospective shows the dev-reviewer reaches 67% precision and 74% recall against a 37% recall baseline without source grounding. A bidirectional probe against VDBFuzz demonstrates complementary coverage.

### Core Strengths

- **S1:** Well-motivated problem definition — the paper characterizes a real defect class (documentation-implementation inconsistency) that crash-oracle fuzzers miss, supported by empirical bug study context and a clear oracle-exclusion argument (Table 2). — see 1.1, 2.1

- **S2:** Source-grounded falsification addresses a real reliability challenge — the dev-reviewer's three-check approach (independent reproducibility, evidence sufficiency, falsifiability) provides a principled method to mitigate LLM false positives, with empirical recall gains (37% to 74%) that justify the added complexity. — see 3.1, 3.3

- **S3:** Real-world impact with production bug finds — 49 maintainer-acknowledged true positives across three production VDBMSs, including 15 merged-PR fixes, demonstrates practical utility beyond toy systems. — see 4.1

### Core Weaknesses

- **W1:** Cross-family generalization unverified — the full evaluation uses a single LLM family (GLM-5.2); a full independent cross-model re-run shows verdict is family-specific (κ = 0.14 DeepSeek, 0.51 LongCat), undermining claims about LLM-as-judge reliability as a general solution. — see 3.2 [major, unfixable]

- **W2:** Statistical rigor concerns on operating point selection — the headline 3-run union operating point is selected post-hoc across four candidates without Bonferroni correction or pre-registration; the reported Wilson CIs do not account for this selection, overstating precision. — see 4.2 [major, fixable]

- **W3:** External validation limited to VDBMSs — transferability beyond VDBMSs is claimed on structural grounds only; a single non-VDBMS case (Apache CouchDB) is reported as a preliminary external validation, which is insufficient to support generalization claims to REST APIs without OpenAPI, configuration validation, or policy-as-code. — see 5.1 [major, unfixable]

### Detailed Assessment

**1. Significance — Adequate**

- **1.1** The problem is well-motivated: documentation-implementation defects are a real concern for systems with natural-language API documentation, and the paper cites empirical context (bug study showing >50% VDBMS bugs are functional failures) to establish importance. The 49 maintainer-acknowledged defects across three production VDBMSs demonstrate practical impact. — see Section 1, Table 4

- **1.2 [minor, fixable]** The scope is narrower than the framing suggests: the approach is VDBMS-specific in evaluation, and claims about transferability to "REST APIs without OpenAPI, configuration validation, and policy-as-code" (Section 7) are not empirically validated beyond a single CouchDB pilot. This limits the claimed significance to a narrower domain than the abstract implies. — see Section 7

**2. Novelty — Weak**

- **2.1** The core novelty claim—source-grounded falsification as an independent verification signal for LLM-derived test oracles—stands relative to prior REST-API oracle tools (AGORA+, SATORI, MASTOR). Those tools extract from structured sources (traces, OpenAPI, source) and operate in low-ambiguity regimes; TestVDB explicitly targets the ambiguous-prose regime where those tools cannot apply. The paper correctly characterizes this delta in Section 6. — see Section 6, Table 2

- **2.2 [major, fixable]** The novelty is incremental rather than transformative. Documentation-derived oracles have been explored since Toradocu (2016), and LLM-based approaches (Doc2OracLL, AugmenTest, ChatAssert, Testora) already use LLMs for oracle generation. TestVDB's contribution is the specific architecture (multi-agent pipeline + source-grounded falsifier), but this is an engineering delta on a known problem rather than a paradigm shift. — see Section 6

- **2.3 [minor, unfixable]** Related Work coverage is adequate for the immediate area (VDBMS testing, REST-API oracles, LLM-as-judge reliability) but omits some adjacent work on hallucination mitigation (e.g., retrieval-augmented generation for documentation, citation-grounded generation) that could inform the design space.

**3. Soundness — Adequate**

- **3.1** The core claims are supported by appropriate methodology. The 48-candidate retrospective is maintainer-adjudicated (27 TP, 21 FP), providing a reasonable ground truth for measuring precision/recall. The ablation study (Table 5) isolates the dev-reviewer's two anchors (source-grounded, threat-model) and shows source grounding contributes the dominant recall gain. The bidirectional VDBFuzz probe (Section 4.3) is a useful controlled comparison, though limited to n=1 cases per direction. — see Section 4

- **3.2 [major, unfixable]** Cross-family LLM generalization is not demonstrated. The paper reports that a full independent re-run with DeepSeek and LongCat-2.0 shows the verdict is family-specific (κ = 0.14 for DeepSeek, 0.51 for LongCat vs. GLM single-run). This undermines the claim that source-grounded falsification is a general solution to LLM-as-judge reliability; it may be GLM-5.2-specific. Without evidence of cross-family robustness, the approach's general applicability is uncertain. — see Section 4.2, Table 6

- **3.3** The dev-reviewer's three-check design is sound and well-justified. The example of #9255 reversal (Section 5) effectively illustrates how the clean-reproduction anchor suppresses a false positive caused by assertion-depending-on-unrequested-field. The source-grounded anchor's dominance in the ablation (75% FP suppression) strongly supports the design choice. — see Section 5, Table 5

**4. Verifiability — Weak**

- **4.1 [major, fixable]** The paper states that "the full prompts, target versions, and per-token accounting are in the artifact, which we will release at a persistent URL upon acceptance" (Section 3), but no artifact URL is provided for review. Without access to prompts, agent configurations, or the raw 48-candidate adjudication data, key claims cannot be independently verified. The paper depends on LLM behavior that is highly configuration-dependent; verifiability requires releasing the exact prompts and sampling parameters. — see Section 3

- **4.2 [major, fixable]** Statistical reporting has fixable issues. The headline operating point (3-run union) is selected post-hoc from four candidates (single-run, 3-run union, 5-run union, 5-run majority) without adjusting for multiple comparisons. The reported Wilson CIs ([49%, 81%] precision, [55%, 87%] recall) do not account for this selection, overstating certainty. A Bonferroni correction would widen the CIs substantially (the paper acknowledges this qualitatively but does not report corrected intervals). — see Section 4.2, Table 6

- **4.3 [minor, fixable]** The paper does not report the exact 48-candidate composition (which specific issues, their vendors, severity categories). Without this detail, it is unclear whether the retrospective is representative of the 107-submission population or a cherry-picked subset. — see Section 4.2

**5. Presentation — Adequate**

- **5.1** The paper is well-structured and generally clear. The pipeline diagram (Figure 1) effectively communicates the four-stage architecture and the dev-reviewer's feedback loop. The oracle-exclusion table (Table 2) is a useful teaching tool for why LLM-derived oracles are necessary. The writing is accessible, with only occasional minor grammatical issues.

- **5.2 [minor, fixable]** Some notation is inconsistent: "GLM-5.2" appears in the cost table (Table 3) but "GLM-5.2" vs. "GLM" is used interchangeably elsewhere. The model family should be named consistently.

- **5.3 [minor, fixable]** The abstract and introduction sometimes overstate the scope. The abstract claims transfer to "REST APIs without OpenAPI, configuration validation, and policy-as-code," but the evaluation is VDBMS-only with only a single CouchDB pilot reported in Section 7. The claims should be tempered to reflect the limited external validation.

## Reviewer 2: Area Specialist

**Overall Recommendation:** Weak Accept

### Summary

The paper targets documentation-implementation defects in Vector Database Management Systems (VDBMSs), where a system silently accepts inputs that violate its API documentation. Because the documented boundary is natural-language prose, deterministic oracles (crash-based, differential testing, metamorphic relations, property-based testing) cannot adjudicate these accept/reject decisions, leaving an LLM as the practical oracle. The authors instantiate TestVDB, a four-stage pipeline that uses LLMs to extract behavioral claims from documentation, generate tests, execute them in sandboxed Docker instances, and confirm defects via adjudication. They identify two false-positive failure modes (extraction hallucination and judgment self-preference bias), show that multi-perspective judging is insufficient, and introduce a dev-reviewer agent that acts as a source-grounded falsifier. On 107 submitted issues across three VDBMSs, maintainers acknowledged 49 true-positive defects (15 fixed via merged PR). On a controlled 48-candidate retrospective, the dev-reviewer reaches 67% precision and 74% recall (3-run ensemble) versus 37% recall without source grounding. A bidirectional probe against VDBFuzz shows complementary coverage.

### Core Strengths

- **S1:** The oracle-exclusion argument (Table 1) is sound and well-structured, systematically walking through why deterministic oracles cannot reach the documentation-implementation residual and why an LLM is the practical option — see 2.1, Table 1.
- **S2:** The dev-reviewer design as a source-grounded falsifier is a principled engineering solution to the two-mode false-positive problem (extraction hallucination and self-preference bias) — see 4.1, 4.2, Figure 3.
- **S3:** The bidirectional probe against VDBFuzz on Qdrant (RQ3) provides concrete evidence of complementary coverage between crash-oracle and documentation-implementation approaches — see 5.3, Table 5.

### Core Weaknesses

- **W1:** The post-hoc selection of the 3-run union as the headline operating point without pre-registration weakens the RQ2 statistical claim — the Wilson CIs do not account for selection across four operating points — see 5.2, Table 4.
- **W2:** Related Work coverage of documentation-derived oracles misses AugmenTest, a directly relevant LLM-based oracle inference system that addresses false positives through iterative prompt repair — see 6.4, 2.3.
- **W3:** External validation is limited to a single non-VDBMS case study (Apache CouchDB) with n=5 probes; the transferability claim beyond VDBMSs is structural-only without empirical breadth — see 6.1, 7.

### Detailed Assessment

#### 1. Significance — Adequate

The paper addresses a real problem: documentation-implementation defects are costly (corrupting query semantics in RAG applications) and prevalent (49 true positives across three VDBMSs, with 15 fixed). The problem statement is clear, and the 107-submission yield demonstrates practical impact. However, the scope is narrower than the framing implies: the approach targets only consistency (accept/reject vs documentation) and explicitly excludes result correctness (ANN recall, ranking), which is acknowledged as out of scope but limits the problem coverage. The VDBMS-specific evaluation (three systems) bounds the generalization claim, and the transfer to other regimes is claimed on structural grounds only with minimal empirical validation (one CouchDB case study, n=5). The contribution is significant within VDBMS testing but does not clearly transcend to the broader testing domain that the introduction suggests.

**1.1** The problem is well-motivated by the empirical bug study and roadmap, which attribute 43% of VDBMS bugs to incorrect behavior and identify oracle definition as a key challenge — see 1, 2. The 49 maintainer-acknowledged defects (15 merged-PR-fixed) across three production VDBMSs demonstrate real-world impact and address a gap left by crash-focused fuzzers like VDBFuzz.

**1.2 [major, fixable]** The transferability claim beyond VDBMSs is insufficiently empirically validated. The Discussion section 7.1 claims transfer to structurally similar documentation regimes (REST APIs without OpenAPI, configuration validation, policy-as-code) on structural grounds only, with a single non-VDBMS case study (Apache CouchDB 3.4.3, n=5 probes). CouchDB rejected every clearly-invalid probe with a 400 error, and the only silent-accept (limit=0) was graceful behavior rather than a defect. This contrast sharpens the motivation but does not validate transfer to other domains. One non-VDBMS case study is insufficient to support the generalization claim; even two additional non-VDBMS targets (e.g., a configuration validation system and a policy-as-code service) would materially strengthen the external validity. The claim should be narrowed to VDBMSs or backed by additional cross-domain validation.

#### 2. Novelty — Excellent

The paper makes a clear, non-obvious delta relative to prior work. The oracle-exclusion argument (Table 1) is a precise characterization of why deterministic oracles miss the documentation-implementation residual and why an LLM is the practical option. This is novel framing relative to REST-API oracle tools (AGORA+, SATORI, MASTOR), which operate in low-ambiguity structured regimes (OpenAPI, traces, source) and explicitly exclude the ambiguous-prose regime. The dev-reviewer design as a source-grounded falsifier is novel relative to prior LLM-as-judge work: Panickssery et al. (self-preference bias) and Haldar et al. (intra-judge inconsistency) document reliability problems but do not propose falsifier-based mitigations; Toradocu, Doc2OracLL, and ChatAssert treat the LLM as the final semantic arbiter without an independent verification source. TestVDB's use of implementation source as the falsifier's ground truth, separating extraction and judgment roles, is a clear technical advance. The bidirectional probe against VDBFuzz is a novel methodological contribution for demonstrating complementary coverage between oracle approaches.

**2.1** The oracle-exclusion argument (Table 1) is a precise characterization of the residual gap. Each row walks through a candidate oracle (crash, differential testing, metamorphic relations, property-based testing, REST doc/spec-derived oracles) and explains structurally why it misses the documentation-implementation defect class. This establishes the LLM-derived oracle as the practical option by elimination rather than assertion, which is sound framing.

**2.2** The dev-reviewer design is novel relative to prior LLM-as-judge reliability work. The paper correctly identifies that Panickssery et al. (self-preference bias) and Haldar et al. (intra-judge inconsistency) document problems but do not propose falsifier-based mitigations. TestVDB introduces implementation source as an independent information source, breaking self-preference by grounding the falsifier in a different signal (what the code actually does vs what the documentation says). This is a clear non-obvious delta.

**2.3 [minor, unfixable]** Related Work coverage of documentation-derived oracles misses AugmenTest, a directly relevant LLM-based oracle inference system. The paper cites Toradocu (deterministic NLP), Doc2OracLL (LLM extraction, documentation quality impact), ChatAssert (iterative prompt repair), and Testora (PR-description regression oracle), but AugmenTest (which infers oracles from available documentation and addresses false positives through iterative refinement) is not cited. AugmenTest is a prior LLM-based documentation-derived oracle that directly overlaps with the regime TestVDB targets. Missing this citation weakens the novelty positioning relative to the LLM-based oracle literature; however, the dev-reviewer's source-grounded falsification approach is distinct from AugmenTest's iterative prompt repair, so the core novelty claim stands. This is a citation gap that should be corrected but does not invalidate the technical contribution.

#### 3. Soundness — Weak

The core claims are partially supported but have significant gaps. The RQ1 detection capability claim (107 submitted, 49 acknowledged) is supported by maintainer adjudication, which is a reasonable ground truth, but the yield precision (68.1%) is likely optimistic given 35 still-pending submissions. The RQ2 false-positive suppression claim (67% precision, 74% recall on 48-candidate retrospective) is supported by maintainer-adjudicated data, but the post-hoc selection of the 3-run union as the headline operating point, without pre-registration and without adjusting CIs for selection across four operating points, weakens the statistical claim. The RQ3 VDBFuzz comparison is sound as a hypothesis-generating probe (each direction n=1) but is not statistically generalizable. The ablation study (12-FP/4-TP control) isolates the dev-reviewer's two anchors well, but the full 48-candidate retrospective uses a single LLM family (GLM-5.2), and cross-family re-runs show the verdict is family-specific (κ = 0.14 DeepSeek, κ = 0.51 LongCat), which limits generalization. The paper acknowledges the cross-family limitation but does not fully quantify its impact on the headline results.

**3.1** The RQ1 detection capability evaluation is sound by maintainer-adjudicated ground truth. The yield precision (68.1% on 72 adjudicated submissions, Wilson 95% CI [56.6%, 77.7%]) is a reasonable estimate, though the worst-case bound (45.8% treating all 35 pending as false positives, Wilson 95% CI [36.7%, 55.2%]) shows the sensitivity to pending adjudication. The 15 merged-PR fixes across three production VDBMSs demonstrate practical impact and validate that the surfaced defects are real — see 5.1, Table 3.

**3.2 [major, fixable]** The RQ2 false-positive suppression claim is weakened by post-hoc operating point selection. The paper reports four operating points (single-run band, 3-run union, 5-run union, 5-run majority) and selects the 3-run union as the headline because it sits at the knee of the precision-recall trade-off. However, this selection is post-hoc (not pre-registered), and the Wilson CIs reported for the 3-run union (precision [49%, 81%], recall [55%, 87%]) do not account for selection across the four operating points. The paper acknowledges this limitation but does not provide corrected CIs (e.g., Bonferroni-adjusted, which would widen the precision CI to roughly [44%, 84%] and the recall CI to roughly [51%, 89%]). Without pre-registration or corrected inference, the statistical claim is overstated. Fix: clearly mark the 3-run union as a post-hoc operating point justified by falsifier semantics, report Bonferroni-adjusted CIs, or pre-register a single operating point in future work.

**3.3 [major, fixable]** The RQ2 evaluation is limited by single-family LLM usage. All dev-reviewer results use GLM-5.2, and a full independent cross-model re-run on all 48 candidates (DeepSeek and LongCat-2.0, each running the complete SOP with independent live probes and source exploration) shows the verdict is family-specific (κ = 0.14 DeepSeek, κ = 0.51 LongCat vs GLM single-run). The paper acknowledges this limitation in the threats to validity, but it materially weakens the generalization claim: the headline 67% precision and 74% recall may not transfer to other LLM families, and without cross-family robustness, the approach is family-specific rather than generally applicable. Fix: quantify the cross-family variance (e.g., report DeepSeek and LongCat precision/recall alongside GLM) or narrow the claim to GLM-5.2 only.

**3.4** The RQ3 VDBFuzz bidirectional probe is sound as a hypothesis-generating case study but not statistically generalizable. Each direction is n=1, and the paper correctly treats these as controlled cases rather than generalized results. The #9045 root cause analysis (vector validation under debug_assert, release builds skip, wait=false accepts zero-length while wait=true rejects) provides concrete evidence of why crash-focused patching misses documentation-implementation residuals. The probe is methodologically solid for demonstrating complementary coverage but cannot claim generalizability beyond the specific Qdrant versions tested — see 5.3, Table 5.

#### 4. Verifiability — Adequate

The paper provides sufficient detail to verify the core claims. The approach section (3) describes the four-stage pipeline with enough detail to understand the flow (claim extraction, test generation, sandboxed execution, defect confirmation) and the dev-reviewer's three-check falsification (independently reproducible, evidence sufficient, falsifiable). The evaluation section (5) reports the yield breakdown by vendor (Table 3), the 48-candidate retrospective with Wilson CIs (Table 4), and the bidirectional probe versions (Table 5). The artifact (promised at a persistent URL upon acceptance) should contain full prompts, target versions, and per-token accounting, which would support replication. However, the paper does not provide the full prompt texts or detailed SOPs in the main text, which limits immediate verifiability without the artifact. The Docker-pinned versions (Milvus 2.6.19, Qdrant v1.18.2, Weaviate v1.38.2) and LLM specification (GLM-5.2, default sampling) are reported, which is sufficient for re-producibility but not for direct replication without the artifact.

**4.1** The pipeline description (3.1-3.4) provides sufficient detail to understand the flow. The dev-reviewer's three-check falsification (4.1, Figure 3) is clearly articulated: (1) independently reproducible under a clean probe, (2) evidence sufficient via cross-checking response through an independent channel, (3) falsifiable by alternative documented interpretation (by-design, wont-fix, implementation choice). This is sufficient to verify the conceptual approach.

**4.2 [minor, fixable]** The evaluation reporting lacks some details needed for immediate replication. The paper promises artifact release with full prompts, target versions, and per-token accounting, which is good, but the main text does not provide example prompts or detailed SOPs. For instance, the contract-formalizer role prompt, the attack-agent boundary-test generation logic, and the dev-reviewer source-grounding procedures are described at a high level but not specified in detail. Without the artifact, a reader could not directly replicate the LLM-based steps. Fix: include appendix material with example prompts and SOP key steps, or ensure the artifact is comprehensive and released at submission time rather than upon acceptance.

#### 5. Presentation — Weak

The paper is well-structured and readable overall, but has several presentation issues that impede clarity. The introduction clearly states the problem, the approach, and the contributions. The four-stage pipeline figure (Figure 1) is clear and well-designed. However, there are several weaknesses: (1) Table 4 (dev-reviewer operating points) is difficult to parse because the single-run band is reported as a range (15-78% recall) rather than a point estimate with variance, making comparison with the 3-run/5-run union points less direct; (2) the related work section (6) has gaps (missing AugmenTest) and could be more systematically organized by regime (structured-source vs ambiguous-prose oracles, LLM-as-judge reliability); (3) the threats to validity (5.4) are honest but not fully integrated with the results—for instance, the cross-family limitation (verdict is family-specific) is acknowledged but its impact on the headline 67%/74% numbers is not quantified; (4) minor language issues appear (e.g., "Wilson 95% CI" formatting, inconsistent notation for test statistics). The paper is understandable and coherent, but presentation weaknesses reduce its effectiveness.

**5.1 [minor, fixable]** Table 4 (dev-reviewer operating points) is difficult to parse. The single-run band is reported as ranges (44-65% accuracy, 50-73% precision, 15-78% recall) rather than point estimates with variance, which makes visual comparison with the 3-run union (65% accuracy, 67% precision, 74% recall) and 5-run union (62% accuracy, 62% precision, 85% recall) less direct. The ranges reflect high variance across runs, which is an important finding, but the table would be clearer if single-run statistics were reported as mean ± SD or median [IQR] rather than ranges. Fix: reformat Table 4 with consistent point estimates (mean or median) and variance measures (SD or IQR).

**5.2 [minor, fixable]** The Related Work section (6) has organizational and coverage gaps. The section covers VDBMS testing (6.1), REST-API oracle generation (6.2), LLM-as-judge reliability (6.3), and documentation-derived oracles (6.4), which is reasonable, but 6.4 misses AugmenTest (a directly relevant LLM-based oracle inference system). The organization could be clearer if structured by regime: (a) structured-source oracles (AGORA+, SATORI, MASTOR, which operate on OpenAPI/traces/source), (b) ambiguous-prose oracles (Toradocu, Doc2OracLL, ChatAssert, Testora, AugmenTest, which target natural-language documentation), (c) LLM-as-judge reliability (Panickssery, Haldar, Ji). This would clarify the delta TestVDB makes relative to each regime. Fix: restructure 6 by regime and add the AugmenTest citation.

**5.3 [minor, fixable]** Minor language and formatting issues appear throughout. Examples: "Wilson 95% CI" is notated inconsistently (sometimes brackets, sometimes parentheses); test statistics (κ, Wilson) are used but not always clearly defined for readers unfamiliar with them; some phrasing is awkward ("the any-confirmed union ensemble is the operating point we match to this variance"). These do not impede understanding but reduce polish. Fix: copy-edit for consistency and clarity, with a focus on statistical notation and phrasing.

## Reviewer 3: General Reviewer

**Overall Recommendation:** Weak Accept

### Summary
This paper presents TestVDB, a system for detecting documentation-implementation defects in Vector Database Management Systems (VDBMSs). The authors identify a gap where existing crash-oracle fuzzers like VDBFuzz miss logical bugs that manifest as silent acceptance of invalid inputs rather than crashes. TestVDB uses LLMs to extract behavioral claims from natural-language documentation, generate tests, and adjudicate whether responses violate documented expectations. A key contribution is a "dev-reviewer" agent that grounds verdicts in implementation source code to counter two LLM failure modes: hallucination in claim extraction and self-preference bias in judgment. The authors report 107 submitted issues across three VDBMSs with 49 maintainer-acknowledged true positives (15 fixed via merged PR), and on a 48-candidate retrospective, the dev-reviewer achieves 67% precision and 74% recall versus 37% recall without source grounding.

### Core Strengths
- **S1:** Well-motivated problem space — see 1.1, the distinction between crash-oracle and documentation-implementation defects is clearly articulated with a concrete example (nprobe=0).
- **S2:** Oracle-exclusion argument is systematic — see 2.1, Table 1 provides a clear walkthrough of why each existing oracle candidate misses the documentation-implementation residual.
- **S3:** Source-grounded falsification contribution is sound — see 3.1, the dev-reviewer's three-check falsification mechanism is well-specified with appropriate justification for moving ground truth from LLM to implementation source.
- **S4:** Empirical evaluation demonstrates real-world impact — see 4.1, the 49 maintainer-acknowledged defects including 15 merged PR fixes show practical utility beyond a theoretical contribution.

### Core Weaknesses
- **W1:** Novelty is incremental rather than transformative — see 2.2, the core LLM-as-judge reliability problem and source-grounded falsification solution are not new ideas; the contribution is primarily in applying known techniques to a new domain (VDBMSs).
- **W2:** Post-hoc operating point selection weakens RQ2 claims — see 4.2 [major, fixable], the 3-run union ensemble is selected after examining multiple operating points without pre-registration, and the Wilson CIs do not account for this selection, risking overfitting to the retrospective dataset.
- **W3:** External validity is limited — see 4.3 [major, fixable], generalization claims beyond VDBMSs rest on a single CouchDB pilot (n=5 probes) with no defects found; this is insufficient evidence for the broader transferability claim to "REST APIs without OpenAPI, configuration validation, and policy-as-code."

### Detailed Assessment

#### 1. Significance — Adequate

- **1.1** The problem is well-motivated. Section 1 clearly articulates why documentation-implementation defects matter: they corrupt query semantics in retrieval-augmented LLM applications where wrong context silently reaches the model. The Milvus #49823 example (nprobe=0 accepted despite documented range [1, 16384]) is a concrete instance that shows real impact. The 15 merged-PR fixes across three production VDBMSs demonstrate that maintainers recognize and prioritize these defects, supporting practical significance.

- **1.2 [minor, fixable]** Scope is narrower than framing suggests. The title and introduction position this as a general solution to "documentation-implementation defects," but the evaluation is VDBMS-only. Section 6 (Discussion) acknowledges this but claims transferability to "REST APIs without OpenAPI, configuration validation, and policy-as-code" on structural grounds alone. The CouchDB pilot (n=5 probes, zero defects found) is insufficient evidence for this broader claim, which overstates the scope relative to what's empirically demonstrated.

#### 2. Novelty — Adequate (provisional)

- **2.1** The oracle-exclusion argument is the strongest novelty contribution. Table 1 provides a systematic walkthrough of why each existing oracle candidate (crash, differential, metamorphic, property-based, REST doc/spec-derived) misses the documentation-implementation residual, with specific citations to each tool and a clear structural reason. This framing clarifies why LLMs are the practical oracle for this residual and is a useful conceptual contribution for researchers in oracle design.

- **2.2 [major, unfixable]** Core reliability techniques are not new. Section 5 identifies two LLM failure modes (hallucination at extraction, self-preference in judgment) and cites established work on both [ji23hall, panickssery24]. Source-grounded falsification as a mitigation is conceptually similar to prior work on using independent signals to correct LLM biases, though the specific application to test oracles and the three-check mechanism (reproducibility, evidence sufficiency, falsifiability) is a reasonable instantiation. The contribution is primarily domain-specific (VDBMSs) rather than methodologically novel.

- **2.3** Related work coverage is adequate for a VDBMS-focused contribution. Section 7 cites REST-API oracle tools (AGORA+, SATORI, MASTOR) and explains the boundary: those tools assume low-ambiguity structured sources, while TestVDB targets the ambiguous-prose regime. The distinction is clear. I have not surveyed the broader LLM-as-judge or documentation-derived oracle literature, so my Novelty assessment is provisional pending a reviewer with field expertise.

#### 3. Soundness — Adequate

- **3.1** The core claim is supported. Section 4.1 (RQ1) reports 107 submitted issues with 49 maintainer-acknowledged true positives. Table 2 breaks this down by vendor (Milvus 22/51, Qdrant 14/26, Weaviate 13/30). The 68.1% precision (Wilson 95% CI [56.6%, 77.7%]) on adjudicated submissions and 15 merged-PR fixes across three production VDBMSs are concrete evidence that TestVDB surfaces real defects worth fixing.

- **3.2 [major, fixable]** Operating point selection in RQ2 is post-hoc and not accounted for in uncertainty. Section 4.2 evaluates four operating points (single-run, 3-run union, 5-run union, 5-run majority) and selects the 3-run union as the headline because "it sits at the knee of the precision-recall trade-off." This selection is hypothesis-generating rather than hypothesis-testing, and the Wilson CIs in Table 4 do not account for selection across four operating points. A Bonferroni correction (α=0.05/4) would widen the 3-run precision CI to roughly [44%, 84%] and recall to [51%, 89%], which the authors acknowledge but do not incorporate into their headline claims. The 37% → 74% recall gain comparison is against a single-LLM baseline, but Table 5 shows that multi-perspective judging achieves 80% precision at 15% recall—substantially different precision-recall trade-offs that make the "without source grounding" comparison potentially cherry-picked.

- **3.3** Method ablation is well-designed. Section 4.2 reports a three-condition ablation on a 12-FP/4-TP control (Table 6): clean-reproduction only (17% FP suppression), source-grounded alone (75%), threat-model alone (50%), union (91%). The source-grounded anchor is clearly the dominant contributor, and the isolation of source grounding's contribution on the full 48-candidate retrospective (recall drops from 74% to 19% without it) provides strong evidence that source access drives the recall gain.

- **3.4** Threats to validity are appropriately disclosed. Section 4.4 clearly states limitations: single-run variance (15–78% recall), the 48-candidate retrospective is maintainer-adjudicated but non-random and not pre-registered, no public ground-truth defect catalog exists for VDBMSs (so recall cannot be estimated), the implementation-as-correct assumption bounds the approach, and cross-family generalization is an open question (κ=0.14 DeepSeek, κ=0.51 LongCat vs. GLM). This transparency is adequate.

#### 4. Verifiability — Adequate

- **4.1** Paper is self-contained for the core pipeline. Section 3 provides a clear four-stage description (behavioral-claim extraction, test-script generation, sandboxed execution, defect confirmation) with a diagram (Figure 1). The dev-reviewer's three-check falsification mechanism (Figure 2, Section 5) is specified with sufficient detail to understand the logic: independently reproducible, evidence sufficient, falsifiable. The Milvus #49823 example walk-through (Section 3) anchors the abstract description.

- **4.2 [minor, fixable]** Artifact availability is claimed but not verifiable from text. Section 3 states "The full prompts, target versions, and per-token accounting are in the artifact, which we will release at a persistent URL upon acceptance." This is standard practice, but the URL is not provided, so I cannot verify the artifact exists or assess its completeness. Section 3 also mentions cost (roughly $10 per target at current API pricing) and LLM-call distribution (Table 3), which is useful but does not substitute for inspecting the actual prompts and implementation.

- **4.3** Critical parameters are reported. Section 4.2 specifies the retrospective size (48 candidates: 27 TP, 21 FP), the VDBMS versions under test (Milvus 2.6.19, Qdrant v1.18.2, Weaviate v1.38.2), the LLM backbone (GLM-5.2), and the operating points evaluated. This is sufficient to understand the experimental setup.

#### 5. Presentation — Adequate

- **5.1** Structure is logical and follows a clear narrative arc. Introduction → Problem Setup (oracle-exclusion) → Approach (TestVDB pipeline) → False-Positive Problem (diagnosing LLM failure modes) → Dev-Reviewer (solution) → Evaluation (three RQs) → Related Work → Discussion/Limitations → Conclusion. Sectioning is appropriate and the flow is coherent.

- **5.2** Writing is clear with minor issues. The prose is generally understandable, but some sentences are dense and could be simplified for clarity. For example, the second sentence in the abstract ("Because the boundary is natural-language prose, current instantiations...") packs three oracle types and a structural reason into one clause. The technical description is adequate but could be more accessible.

- **5.3 [minor, fixable]** Some notation inconsistency. Table 1 uses bullet symbols for row separators that appear as rendered characters; this is a minor formatting issue. Figure 1 and Figure 2 use TikZ diagrams that are clear but could benefit from more explicit labels (e.g., "NL docs" and "impl source" in Figure 1 are somewhat terse).

- **5.4** Citations are adequate for a domain-focused paper. I have not verified whether critical works are missing, but the cited works (VDBFuzz, AGORA+, SATORI, MASTOR, LLM-as-judge reliability studies) are relevant and properly contextualized.

## Meta-Review

### Criterion Consensus

| Criterion | Reviewer 1 | Reviewer 2 | Reviewer 3 | Meta-Review |
|---|---|---|---|---|
| Significance | Adequate | Adequate | Adequate | **Adequate** |
| Novelty | Weak | Excellent | Adequate *(prov)* | **Adequate** *[Mixed]* |
| Soundness | Adequate | Weak | Adequate | **Adequate** *[Mixed]* |
| Verifiability | Weak | Adequate | Adequate | **Adequate** *[Mixed]* |
| Presentation | Adequate | Weak | Adequate | **Adequate** *[Mixed]* |
| **Recommendation** | **Weak Accept** | **Weak Accept** | **Weak Accept** | **ACCEPT** |

### Meta Recommendation

**ACCEPT**

三位均 Weak Accept → unanimous shortcut。无 consensus Poor、无 substance consensus Weak（Novelty/Soundness/Verifiability/Presentation 各有 1 位 Weak 但非同一准则 ≥2 票）→ ACCEPT 规则。

### Priority Revisions

1. **[major, fixable]** post-hoc 操作点 selection-aware CI（R1-att + R2-att + R1-exp + R2-exp 共识）
2. **[major, fixable]** cross-family κ 诚实报告（论文已改，但 abstract/contributions 需更显式 caveat）
3. **[major, fixable]** external validity 扩展（CouchDB 只 1 个 non-VDBMS，R2-exp 建议 ≥2）
4. **[major, fixable]** minus-source fully crossed ablation（R2-att：minus-source 仍含 clean-repro + threat-model，没完全隔离 source）
5. **[minor, fixable]** Novelty positioning（R1-exp 评 Weak：source-grounded falsification 是 known technique；R2-exp 评 Excellent：domain-specific application is novel）

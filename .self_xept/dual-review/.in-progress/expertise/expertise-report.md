# Expertise-Half Report（dual-review expertise 半边）

> Paper: TestVDB v3 · paper type: technical · Date: 2026-07-27
> R1/R2 cache abstract-first（MASTOR/SATORI abstract-level）；R3 无 cache。

## Reviewer 1: Domain Expert

**Overall Recommendation:** Accept

### Summary

This paper introduces TestVDB, a system for detecting documentation-implementation defects in Vector Database Management Systems (VDBMSs). A documentation-implementation defect occurs when a VDBMS silently accepts an input that violates its API documentation (e.g., accepting `nprobe=0` when the documentation specifies the range as [1, 16384]). Because the documented boundary is natural-language prose rather than a structured specification, deterministic oracles (crash detection, differential testing, metamorphic relations, property-based testing, and structured-source extraction tools) cannot adjudicate these accept/reject decisions, leaving an LLM as the practical oracle.

The authors instantiate a four-stage pipeline: behavioral-claim extraction (LLM reads documentation to emit structured claims), test-script generation (attack agents turn claims into executable probes), sandboxed execution (Docker-pinned VDBMS instances), and defect confirmation (judge compares documented expectation against actual response). The LLM introduces two false-positive modes: hallucination in extraction (LLM emits constraints stronger than documentation states) and self-preference in judgment (same family that extracts tends to confirm). Multi-perspective judging raises precision but collapses recall. To address this, the authors introduce a dev-reviewer agent that performs source-grounded falsification: reproducing each candidate under a clean probe, cross-checking against implementation source, and trying to disprove it.

TestVDB surfaced 107 candidate issues across three VDBMSs (Milvus, Qdrant, Weaviate); maintainers acknowledged 49 as true-positive defects, with 15 fixed via merged PR. On a controlled retrospective over 48 maintainer-adjudicated candidates, the dev-reviewer reaches 67% precision and 74% recall (3-run any-confirmed ensemble) against 37% recall without source grounding. A bidirectional probe against VDBFuzz shows complementary coverage: TestVDB reaches a crash-class defect (Qdrant integer overflow on size=2^63) by contract reasoning, while VDBFuzz misses a TestVDB silent-accept defect (wait=false accepting zero-length vector) under current templates.

### Core Strengths

- **S1:** Well-motivated defect class — see 1.1, 2.1. The paper clearly identifies a structural gap in current VDBMS testing (crash oracles miss silent-accept defects) and provides empirical motivation (44 of 49 true positives do not crash).

- **S2:** Systematic oracle-exclusion argument — see 2.2. Table 1 rigorously positions TestVDB against the oracle landscape (crash, differential testing, metamorphic relations, property-based testing, REST-API oracles) and identifies the residual where LLM-derived oracles are necessary.

- **S3:** Novel falsification mechanism — see 2.3, 3.1. The dev-reviewer's source-grounded falsification is a clear advance over prior work: MASTOR uses source-as-oracle (encoding implemented behavior, missing gaps), while TestVDB uses source-as-falsifier (detecting doc-implementation gaps).

- **S4:** Strong empirical validation — see 4.1, 4.2. 49 maintainer-acknowledged true positives across three production VDBMSs, with 15 merged-PR fixes, demonstrate practical impact. The bidirectional probe against VDBFuzz provides concrete evidence of complementarity.

- **S5:** Honest treatment of limitations — see 4.3, 5.1. The paper transparently reports the post-hoc operating point selection, single-LLM-family evaluation, implementation-as-correct assumption, and Weaviate yield-only generalization.

### Core Weaknesses

- **W1:** Single-model evaluation — see 4.3 [major, fixable]. All dev-reviewer results use GLM-5.2; a cross-model check on only 20 candidates (with moderate CI width) leaves open the possibility of family-specific effects. A more comprehensive cross-model validation would strengthen the reliability claim.

- **W2:** Post-hoc operating point selection — see 4.2 [major, fixable]. The 3-run union headline operating point is selected post-hoc from four candidates, and the Wilson CIs do not account for this selection. Pre-registration or a more principled selection criterion would strengthen internal validity.

- **W3:** Narrow generalization evidence — see 4.4 [minor, unfixable]. Evaluation is VDBMS-only; transfer to other natural-language documentation regimes (REST APIs without OpenAPI, configuration validation, policy-as-code) is claimed on structural grounds only. One non-VDBMS case study would materially strengthen the generalization claim.

### Detailed Assessment

1. **Significance** — Adequate

   - **1.1** [strength] The problem is well-motivated and real. The paper cites an empirical bug study showing that more than half of VDBMS defects manifest as functional failures (Section 1, line 33), and the roadmap identifies oracle definition as a key challenge (Section 1, line 33). The 49 maintainer-acknowledged defects across three production VDBMSs (Section 6, line 199) demonstrate that the defect class is prevalent and impactful.

   - **1.2** [limitation] The significance is bounded by the VDBMS-specific evaluation. While the problem class (documentation-implementation defects) is clearly important for VDBMSs, the paper does not empirically demonstrate transfer to other domains where natural-language documentation is the norm (e.g., configuration validation, policy-as-code). The generalization claim (Section 8, line 316) is structural only, which limits the claimed impact to VDBMSs until future validation occurs.

2. **Novelty** — Excellent

   - **2.1** [strength] The paper makes a clear structural advance over VDBFuzz, the first dedicated VDBMS fuzzer. VDBFuzz uses crash as its oracle and therefore cannot reach silent-accept defects (Section 7, line 302). TestVDB targets exactly this gap: defects that silently accept violating inputs and produce no crash. The bidirectional probe (Section 6, line 272-276) empirically validates complementarity: TestVDB reaches a crash-class defect (Qdrant integer overflow on size=2^63) by contract reasoning, while VDBFuzz misses a TestVDB silent-accept defect (wait=false accepting zero-length vector) under current templates. This is a verified novelty delta against a named baseline.

   - **2.2** [strength] The paper positions itself against REST-API oracle tools (AGORA+, SATORI, MASTOR) with a clear regime distinction. AGORA+ infers invariants from observed traffic and cannot reach inputs the traffic did not exercise (Section 7, line 305). SATORI reads OpenAPI schema elements (type, format, minimum, maximum) and stays in a regime where constraints are explicit (Section 7, line 305). MASTOR reads source to generate oracles encoding implemented behavior and cannot detect a gap between documentation and code (Section 7, line 305). TestVDB operates in the ambiguous-prose regime where constraints are implicit in natural-language documentation, uses source as a falsifier (not oracle generator), and targets exactly the doc-implementation gap. The exclusion argument in Table 1 (Section 2, line 62-78) systematically maps the oracle landscape and identifies the residual where TestVDB operates. This is a well-supported novelty claim.

   - **2.3** [strength] The dev-reviewer's source-grounded falsification is a novel mechanism absent in prior work. Toradocu pioneered NL-to-oracle extraction using deterministic NLP and pattern matching, targeting simple syntactic patterns like Javadoc @throws comments (Section 7, line 311). It acknowledged false positives from extraction failures but did not correct them. TestVDB advances this line in two ways: (1) LLM-based semantic interpretation handles ambiguous prose beyond simple syntactic patterns, and (2) source-grounded falsification provides an independent verification signal (implementation source) to suppress false positives, which Toradocu lacked. The three-check falsification (independently reproducible, evidence sufficient, falsifiable) in Figure 3 (Section 5, line 156-179) is a concrete technical contribution.

3. **Soundness** — Adequate

   - **3.1** [strength] The evaluation design is appropriate for the claims. RQ1 (detection capability) is answered by 107 submitted issues with 49 maintainer-acknowledged true positives across three VDBMSs (Section 6, line 199). RQ2 (false-positive suppression) is answered by a controlled retrospective over 48 maintainer-adjudicated candidates, comparing the dev-reviewer against a single-LLM baseline and multi-perspective judging (Section 6, line 218-256). RQ3 (comparison with VDBFuzz) is answered by a bidirectional reachability probe on Qdrant (Section 6, line 272-290). Each research question maps to an appropriate evaluation methodology.

   - **3.2** [strength] The ablation study isolates the dev-reviewer's contribution. Table 4 (Section 6, line 239-253) shows a three-condition ablation on a 12-FP/4-TP control: source-grounded alone suppresses 9/12 false positives (75%), threat-model alone suppresses 6/12 (50%), and their union suppresses 11/12 (91%), each retaining all 4 true positives. This clearly establishes that the source-grounded anchor is the dominant contributor, with the threat-model anchor adding coverage on by-design patterns. The design (each anchor alone vs. union) is sound.

   - **3.3** [strength] The statistical reporting is appropriate. The paper reports Wilson 95% CIs for precision (e.g., 67% [49, 81] for the 3-run union, Table 3, Section 6, line 221-235), which correctly accounts for the binomial proportion and small sample size. The cross-model agreement check (Cohen's kappa=1.0 on 20 candidates, Wilson CI [83, 100], Section 6, line 256) is appropriate for measuring inter-rater reliability. The internal validity threats section (Section 6, line 292-297) honestly acknowledges the post-hoc operating point selection and the non-random retrospective sample.

   - **3.4** [limitation] The single-LLM-family evaluation bounds the reliability claim. All dev-reviewer results use GLM-5.2 (Section 4, line 126). The cross-model check (DeepSeek agreeing with GLM-5.2 on 20 candidates, Section 6, line 256) provides some evidence against strong family-specificity, but the sample is small (n=20) and the Wilson CI [83, 100] leaves moderate family-specific effects statistically compatible. A more comprehensive cross-model evaluation (e.g., 2-3 additional families on a larger candidate set) would strengthen the claim that the dev-reviewer's verdict is not strongly family-specific when source evidence is explicit (Section 6, line 297). This is a fixable gap.

   - **3.5** [limitation] The post-hoc operating point selection weakens internal validity. The paper reports four operating points (single-run band, 3-run union, 5-run union, 5-run majority) and selects the 3-run union as the headline (Table 3, Section 6, line 221-235). The selection is justified post-hoc by falsifier semantics (a candidate that survives any independent falsification is more likely a true defect), but this justification was not pre-registered. The Wilson CIs do not account for selection across the four operating points, which introduces the risk of overstating precision. Pre-registration of the operating point selection criterion or a more principled selection (e.g., the point maximizing F1-score on a held-out validation set) would address this. This is a fixable gap.

   - **3.6** [limitation] The Weaviate evaluation is yield-only, which limits cross-vendor generalization. The controlled retrospective covers Milvus (32 candidates) and Qdrant (16 candidates), Section 6, line 218. Weaviate is included in the yield analysis (30 submitted, 13 acknowledged, Table 2, Section 6, line 201-216) but not in the controlled retrospective. The external validity threats section (Section 6, line 295) acknowledges that "generalization to Weaviate is yield-only" but does not explain why a retrospective was not run. Without Weaviate in the retrospective, the dev-reviewer's precision/recall claims are vendor-specific to Milvus/Qdrant until validated. This is a fixable gap.

4. **Verifiability** — Adequate

   - **4.1** [strength] The paper discloses sufficient implementation details for replication. Section 4 (line 125-127) describes the multi-agent pipeline on the Claude Code runtime, 20 agents with task-structured role prompts, GLM-5.2 backbone under default sampling, and pinned target versions (Milvus 2.6.19, Qdrant v1.18.2, Weaviate v1.38.2). The wall-clock cost (on the order of $10 per target) and LLM call volume (roughly 10^4 calls) are disclosed. The paper states that "full prompts, target versions, and per-token accounting are in the artifact, which we will release at a persistent URL upon acceptance" (Section 4, line 126-127). This is sufficient to conceptually reproduce the pipeline.

   - **4.2** [strength] The paper links to an artifact. The statement that artifact release is "upon acceptance" (Section 4, line 127) indicates the artifact exists and will be made available. The disclosure of the Docker-pinned versions and the source clone mechanism (Section 4, line 126: "clones each target's source at the pinned version... the clone is the only ground truth") provides enough information for a third party to set up the execution environment. The sandboxed execution design (Section 4, line 116-118) is clearly described. From the text, the artifact link is declared and the described execution environment is reproducible.

   - **4.3** [limitation] The 48-candidate retrospective is not fully characterized. The paper states that the retrospective is "maintainer-adjudicated" (Section 6, line 218) but does not describe how the 48 candidates were selected from the full 72 adjudicated set (49 TP + 23 by-design/rejected). Was it a random sample? A stratified sample by vendor? A convenience sample? The internal validity threats section (Section 6, line 293) acknowledges that "we did not pre-register the candidate set" but does not describe the selection process. Without knowing how the 48 were selected, readers cannot assess selection bias. This is a fixable gap (disclose the selection process in the artifact or revision).

   - **4.4** [limitation] The artifact link is conditional on acceptance. While the paper states the artifact will be released (Section 4, line 127), it does not provide a persistent URL or DOI that reviewers can access pre-publication. For a system paper, providing a working artifact (even a beta demo) would strengthen verifiability. This is a fixable gap.

5. **Presentation** — Excellent

   - **5.1** [strength] The paper is well-structured and readable. The introduction clearly motivates the problem (documentation-implementation defects, the oracle gap), positions against prior work, and states the contributions (Section 1, line 30-51). The pipeline section (Section 4, line 80-127) provides a clear step-by-step description with a concrete example (the #49823 path, Section 4, line 122-124). The evaluation section (Section 6) is organized by research question with tables summarizing results. The figures (Figure 1 pipeline, Figure 2 dev-reviewer checks) are clear and informative.

   - **5.2** [strength] The writing is clear and precise. The distinction between consistency (accept/reject matches documentation) and correctness (result is mathematically right) is crisply drawn (Section 2, line 56-58). The exclusion argument (Table 1) systematically walks through each oracle candidate and explains why it misses the documentation-implementation residual. The related work section (Section 7) clearly distinguishes the paper's contributions from each line of prior work (VDBMS testing, REST-API oracles, LLM-as-judge reliability, documentation-derived oracles).

   - **5.3** [strength] The paper uses appropriate notation and terminology. The mathematical notation (e.g., nprobe in [1, 16384], Section 1, line 37) is clear. The tables are well-formatted and captioned. The reference list appears comprehensive (VDBFuzz, AGORA+, SATORI, MASTOR, Toradocu, and other relevant works are cited).

   - **5.4** [minor, fixable] Some sentences are long and could be shortened for clarity. For example, Section 6, line 272-276 ("On Qdrant v1.18.2, VDBFuzz (default configuration) ran over 26,000 mutated requests and found 0 crashes; the two Qdrant case-study crashes are fixed in this version...") is a dense sentence that could be split. This is a minor style issue.

   - **5.5** [minor, fixable] Some abbreviations are not explicitly defined on first use. "LLM" is used in the abstract (line 16) without expansion; "API" is used without expansion (line 16). These are standard abbreviations in the field, but defining them on first use would improve accessibility for readers outside the immediate subfield. This is a minor style issue.

## Reviewer 2: Area Specialist (LLM-based test generation / Database-system testing)

**Overall Recommendation:** Weak Accept

### Summary

TestVDB targets documentation-implementation defects in Vector Database Management Systems (VDBMSs) — cases where a VDBMS silently accepts inputs violating its API documentation. Because documentation is natural-language prose rather than structured specifications, deterministic oracles (crash, differential, metamorphic, property-based) cannot adjudicate accept/reject decisions. The paper instantiates a four-stage pipeline using LLMs to extract behavioral claims from documentation, generate tests, execute them, and confirm defects. Two false-positive failure modes arise: hallucination in claim extraction and self-preference bias in judgment. A multi-perspective judging baseline improves precision but collapses recall, so the paper introduces a dev-reviewer agent that falsifies LLM verdicts against implementation source. Evaluation across three VDBMSs (Milvus, Qdrant, Weaviate) yields 107 submitted issues with 49 maintainer-acknowledged true-positive defects (15 merged-PR-fixed). On a 48-candidate retrospective, dev-reviewer achieves 67% precision and 74% recall vs 37% recall without source grounding. A bidirectional probe against VDBFuzz shows complementary coverage.

### Core Strengths

- **S1:** Well-positioned novelty at LLM-as-judge and REST-oracle intersection — TestVDB is first to use source as independent falsifier for LLM-derived oracles, bridging self-preference theory (Panickssery) to test-oracle practice — see 2.2.

- **S2:** Oracle-exclusion argument (Table 1) clearly motivates why deterministic oracles miss documentation-implementation defects and why LLM is the practical residual — see 2.1.

- **S3:** Source-grounded falsification is technically sound — implementation source as independent ground truth breaks self-preference cycle by giving LLM a factual signal it cannot argue with — see 3.2.

- **S4:** Practical impact demonstrated — 15 merged-PR fixes across production VDBMSs show defects are real, not artifacts — see 4.1.

### Core Weaknesses

- **W1:** Operating-point selection (3-run union) is post-hoc with no pre-registration, yet Wilson CIs do not account for selection across four operating points — inflation of statistical confidence — see 4.2.

- **W2:** External validity limited for Weaviate (yield-only, no controlled retrospective) and untested for non-VDBMS regimes claimed transferable (REST APIs without OpenAPI, configuration validation, policy-as-code) — see 4.4.

- **W3:** Implementation-as-correct assumption bounds approach — an implementation bug can wrongly falsify a correct documentation clause, creating false negatives of dev-reviewer — see 5.1.

### Detailed Assessment

#### 1. Significance — Adequate

**1.1** The problem is real and costly — silent-accept defects corrupt query semantics in retrieval-augmented LLM stacks, allowing wrong context to reach models without error signals (Section 1). VDBMS bug study shows 43% of defects are incorrect behavior, and existing fuzzers miss the logical-bug majority. The defect class matters.

**1.2 [major, fixable]** Impact ceiling is unclear because evaluation is VDBMS-only. Discussion (Section 5) claims transferability to structurally similar regimes (REST APIs without OpenAPI, configuration validation, policy-as-code) on structural grounds only, with zero empirical tests. Even one non-VDBMS case study would materially strengthen significance. Currently, significance is Adequate — real problem within VDBMSs, but unproven beyond.

#### 2. Novelty — Adequate

**2.1** The paper correctly identifies the novelty delta vs prior work. Table 1's oracle-exclusion argument is sound — it walks through crash oracles (VDBFuzz), differential testing, metamorphic relations, property-based testing, and REST-API tools (AGORA+, SATORI, MASTOR), showing each misses the documentation-implementation residual. The positioning that this leaves LLM as practical oracle is clear and convincing.

**2.2** Vs LLM-as-judge reliability work, the novelty is specific and well-anchored. Checked against fetched core competitors (Panickssery et al. on self-preference, Ji et al. on hallucination, Haldar et al. on intra-judge inconsistency), the paper correctly characterizes each threat and maps it to test-oracle pipeline failure modes. The contribution is applying this theory to test-oracle practice with source-grounded falsification as countermeasure. This is incremental but real — prior work studied the bias; TestVDB operationalizes a fix.

**2.3 [major, fixable]** Related Work coverage in documentation-derived oracles is missing AugmenTest and ChatAssert. The paper cites Toradocu (pioneer) and Doc2OracLL (LLM extension), but misses AugmenTest (2025), which infers oracles from available documentation using LLMs, and ChatAssert (2024), which addresses false positives through iterative prompt repair guided by execution feedback. Both are in scope — LLM-based oracle generation and false-positive suppression. AugmenTest is particularly relevant because it directly parallels TestVDB's LLM extraction from documentation. Positioning novelty delta against both would strengthen Related Work coverage.

**2.4** Vs REST-API oracle tools, novelty is clear. Checked against fetched AGORA+, SATORI, MASTOR, the paper accurately characterizes each as operating in low-ambiguity regimes (traces, OpenAPI schema, source) that avoid the natural-language documentation regime TestVDB enters. MASTOR is correctly identified as closest — it reads source but cannot detect documentation-implementation gaps — and TestVDB's use of source as falsifier targets exactly that gap. Novelty here is solid.

#### 3. Soundness — Weak

**3.1** RQ1 detection capability is well-supported. 107 submitted issues with 49 maintainer-acknowledged TPs and 15 merged-PR fixes across three production VDBMSs provides strong evidence that surfaced defects are real. Yield precision 68.1% (adjudicated-only) and worst-case 45.8% (including pending) is reasonable given the high-variance LLM judgment. Wilson CIs appropriately quantify uncertainty.

**3.2 [major, unfixable]** RQ2 operating-point selection is post-hoc with unaccounted selection bias. The paper reports four operating points (single-run band, 3-run union, 5-run union, 5-run majority) and selects 3-run union as headline "post-hoc, justified by falsifier semantics" (Section 4.2). However, Wilson CIs in Table 3 do not account for this selection across multiple configurations. This inflates statistical confidence — the reported 95% CI for precision [49%, 81%] and recall [55%, 87%] are conditional on selecting the best-looking operating point after seeing the data. Proper handling requires either (a) pre-registering the operating point or (b) correcting CIs for selection (e.g., via selective inference frameworks). The current CIs are anti-conservative.

**3.3** RQ3 VDBFuzz comparison is methodologically sound as hypothesis-generating probe. The bidirectional design (TestVDB reaching VDBFuzz's crash, VDBFuzz missing TestVDB's silent-accept) with n=1 per direction is appropriately framed as controlled case studies, not generalized results. The #9045 root-cause analysis showing crash-site patches recurred without fixing the documentation-implementation residual is compelling evidence for why crash-oracle approaches miss this defect class.

**3.4 [major, fixable]** External validity is limited for Weaviate and untested beyond VDBMSs. The paper explicitly acknowledges (Section 4.4) that generalization to Weaviate is yield-only — no controlled retrospective as for Milvus/Qdrant. This leaves the dev-reviewer's precision/recall claims empirically supported for only two of three studied VDBMSs. More critically, the transferability claim to non-VDBMS regimes (REST APIs without OpenAPI, configuration validation, policy-as-code) is purely structural without any empirical test. Even one proof-of-concept outside VDBMSs (e.g., one REST API without OpenAPI) would materially strengthen external validity. Currently, Soundness is Weak — strong internal evidence on two VDBMSs, but unproven generalization.

**3.5** Threats to validity (Section 4.4) are well-discussed. Internal validity correctly flags single-run variance, post-hoc operating-point selection, and non-random retrospective. External validity correctly flags Weaviate limitation and untested transfers. Construct validity correctly flags single-LLM-family evaluation (mitigated by cross-model check) and implementation-as-correct assumption. The threats section is thorough and honest.

#### 4. Verifiability — Adequate

**4.1** The paper states artifact availability (prompts, target versions, per-token accounting to be released at persistent URL upon acceptance). This meets the bar for replication — a motivated researcher could reconstruct the pipeline from the described components (20 agents with role prompts, GLM-5.2 backbone, Docker-pinned versions). Source clones at pinned versions (milvus-src v2.6.19, qdrant-src v1.18.2, weaviate-src v1.38.2) are specified.

**4.2 [minor, fixable]** Section 3 ("LLM automation") lacks concrete cost accounting details that would aid reproducibility. The paper reports "$10 per target" and "10^4 LLM calls" but does not break down per-stage costs or provide the per-token accounting it promises. Adding a table with cost breakdown (claim extraction: $X, test generation: $Y, execution: $Z, dev-reviewer: $W) would make the cost claim verifiable without revealing proprietary pricing.

**4.3** The 48-candidate retrospective is well-documented for replication. Table 3 and ablation Table 4 provide sufficient detail on the control set (27 TP, 21 FP) and configuration variants for another group to attempt reproduction.

#### 5. Presentation — Adequate

**5.1** Structure is logical and follows standard empirical-paper template (introduction/background, approach, FP analysis, dev-reviewer, evaluation, related work, discussion, conclusion). Figures (pipeline diagram, dev-reviewer three-check flow) are clear and aid understanding.

**5.2 [minor, fixable]** Table 1 (oracle exclusion) has dense formatting — the "Why it misses" column is text-heavy and could be split into two sub-columns (defect class reached, reason for missing) for better readability.

**5.3 [minor, fixable]** Section 4.2 uses precision-recall trade-off terminology ("knee of the trade-off") without a visual precision-recall curve. Adding a P-R curve with four operating points marked would make the operating-point selection more transparent and help readers see the "knee."

**5.4 [minor, fixable]** The Related Work section (Section 6) misses two in-scope works: AugmenTest (2025) on LLM-based oracle inference from documentation, and ChatAssert (2024) on false-positive suppression via iterative prompt repair. Both directly relate to TestVDB's LLM extraction and false-positive mitigation. Citing and positioning against them would strengthen Related Work coverage.

**5.5** Writing quality is generally high. The abstract clearly states the problem, approach, false-positive modes, dev-reviewer solution, and key results. Technical prose is precise in describing the pipeline and evaluation.

## Reviewer 3: General Reviewer

**Overall Recommendation:** Weak Accept

### Summary

The paper presents TestVDB, a system for detecting documentation-implementation defects in Vector Database Management Systems (VDBMSs)—a defect class where systems silently accept inputs that violate their API documentation. The authors argue that because API documentation is natural-language prose rather than structured specifications, existing deterministic oracles (crash-based fuzzing, differential testing, metamorphic relations) cannot adjudicate accept/reject decisions, leaving LLMs as the practical oracle. TestVDB instantiates a four-stage pipeline using LLMs for claim extraction, test generation, sandboxed execution, and defect confirmation. To address LLM false positives from hallucination and self-preference bias, they introduce a "dev-reviewer" agent that falsifies claims against implementation source. They evaluate on three VDBMSs (Milvus, Qdrant, Weaviate), reporting 49 maintainer-acknowledged true-positive defects from 107 submitted issues, with a dev-reviewer retrospective achieving 67% precision and 74% recall versus 37% recall without source grounding. A bidirectional probe against VDBFuzz shows complementary coverage.

### Core Strengths

- **S1:** Clear articulation of the oracle problem and why existing deterministic approaches miss the documentation-implementation residual — see 1.1, 1.2.
- **S2:** Systematic oracle-exclusion argument (Table 1) that structurally motivates LLM-derived oracles as the necessary approach for this defect class — see 1.3.
- **S3:** Well-motivated dev-reviewer design addressing two specific false-positive failure modes (hallucination, self-preference) with a falsification architecture — see 3.1, 3.2.
- **S4:** Substantial real-world impact: 15 merged-PR fixes across three production VDBMSs — see 4.1.

### Core Weaknesses

- **W1:** Novelty relative to REST-API oracle literature is unclear — the paper claims TestVDB targets "ambiguous-prose documentation" but doesn't systematically differentiate from prior work's "low-ambiguity structured sources" regime — see 2.1.
- **W2:** Statistical rigor on the dev-reviewer operating point is insufficient — the 3-run union ensemble is a post-hoc selection without pre-registration, and Wilson CIs don't account for selection across four operating points — see 4.2 [major, fixable].
- **W3:** External validation beyond VDBMSs is absent, limiting confidence in transferability claims — see 4.3.

### Detailed Assessment

1. **Significance** — Adequate
   - **1.1** The paper targets a real and impactful problem: VDBMS defects that silently corrupt query semantics without crashing. The bug study they cite (Section 1) attributes 43% of VDBMS bugs to incorrect behavior, making this a substantive target. The 15 merged-PR fixes across production systems demonstrate practical impact beyond toy examples.
   - **1.2** However, the scope is narrower than the framing suggests. The paper explicitly limits itself to "documentation-implementation consistency" and explicitly excludes "result correctness" (ANN recall, ranking) as out of scope. This focused scope is defensible but limits significance to a subset of VDBMS correctness issues. The impact on the broader VDBMS testing agenda is therefore partial.
   - **1.3 [minor, fixable]** The contribution statement (Section 1, last paragraph) would benefit from explicitly stating what is NOT claimed (result correctness, closed-source systems) to set precise expectations for readers unfamiliar with the VDBMS testing roadmap.

2. **Novelty** — Provisional Adequate
   - **2.1 [major, fixable]** The novelty positioning relative to REST-API oracle tools (AGORA+, SATORI, MASTOR) needs clarification. The paper claims these tools "extract from low-ambiguity structured sources" and that TestVDB enters the "ambiguous-prose regime," but the boundary is not demonstrated. Are there examples where AGORA+ or SATORI *attempted* to extract from natural-language documentation and failed? Or is this a theoretical exclusion argument? Without concrete comparison cases, the "ambiguous-prose" regime reads as a post-hoc distinction rather than a demonstrated delta.
   - **2.2** Within the LLM-as-judge reliability line, the contribution of source-grounded falsification to break self-preference bias (Section 5) appears novel. Prior work (Toradocu, Doc2OracLL, ChatAssert) uses runtime feedback or iterative prompt repair, not implementation source as an independent falsifier. This is a clear methodological delta.
   - **2.3 [minor, fixable]** The Related Work section (Section 7) should explicitly state whether Toradocu, Doc2OracLL, or ChatAssert were evaluated on VDBMS-like natural-language API documentation. If they were tested on Javadoc (structured) and failed on prose, that would strengthen the novelty claim. If they were never evaluated on prose, the delta is untested.

3. **Soundness** — Adequate
   - **3.1** The oracle-exclusion argument (Table 1) is structurally sound: each deterministic oracle candidate is ruled out for a documented reason (crash oracles miss silent accepts; differential testing cannot adjudicate accept/reject; metamorphic relations address output not input; property-based testing requires machine-checkable properties; REST-API tools require structured sources). The logical chain that leaves LLMs as the residual follows from these exclusions.
   - **3.2** The dev-reviewer three-check falsification design (Section 5, Figure 3) is sound: independently reproducible, evidence-sufficient, and falsifiable checks directly address the failure modes diagnosed in Section 4 (hallucination, self-preference). The cross-model check (DeepSeek agreeing on 20 candidates, Cohen's κ=1.0) provides evidence that the verdict is not strongly family-specific when source evidence is explicit.
   - **3.3 [major, unfixable]** The implementation-as-correct assumption (acknowledged in Section 8) is a structural limitation: an implementation bug can wrongly falsify a correct clause. The authors report observing "maintainer-rejected confirmed TPs where the documentation itself was wrong" but do not quantify this failure mode. Without knowing the false-negative rate from this assumption, the precision/recall estimates are biased upward. This is inherent to the approach and cannot be fixed without a ground-truth defect catalog.

4. **Verifiability** — Adequate
   - **4.1** The paper provides sufficient methodological detail to reproduce the pipeline: the four-stage architecture (Section 3), the dev-reviewer three checks (Section 5), and the LLM runtime configuration (Section 3, "LLM automation"). The authors state that "full prompts, target versions, and per-token accounting are in the artifact" and commit to releasing it at a persistent URL upon acceptance, which satisfies the verifiability bar for a technical paper.
   - **4.2 [major, fixable]** The statistical reporting on the dev-reviewer operating point is insufficient. The 3-run union ensemble is selected as the "headline" from four operating points (single run, 3-run union, 5-run union, 5-run majority), and the authors explicitly flag this as "post-hoc." However, the Wilson 95% CIs in Table 2 do not account for selection across operating points. A pre-registered analysis plan or a correction for multiple comparisons would strengthen verifiability. As written, the recall gain (37%→74%) may be partially attributable to cherry-picking the operating point.
   - **4.3** The bidirectional VDBFuzz probe (Section 6, RQ3) provides two concrete case studies (Qdrant v1.4.0 integer-overflow crash, Qdrant v1.18.0 empty-vector accept) that demonstrate complementary coverage. The authors correctly note that "each direction is n=1" and treat these as "hypothesis-generating controlled cases rather than a generalized result," which is an appropriate limitation statement. The root-cause analysis of #9045 (debug_assert conditional, wait=true vs wait=false path divergence) is detailed and verifiable.
   - **4.4 [minor, fixable]** The paper reports "single-run recall varies widely (15–78%)" but does not show the distribution of per-run recall or quantify the variance (e.g., standard deviation, interquartile range). Reporting these metrics would improve verifiability of the LLM judge's high-variance claim.

5. **Presentation** — Adequate
   - **5.1** The paper is well-structured: Introduction → Problem Setup → Approach → False-Positive Problem → Dev-Reviewer → Evaluation → Related Work → Discussion → Conclusion. The narrative flow is logical, and each section builds on the previous. The figures (Figure 1 pipeline, Figure 3 dev-reviewer checks) are clear and support the text.
   - **5.2** The writing is generally clear, with precise terminology (e.g., "documentation-implementation consistency" vs "result correctness," "accept/reject" vs "crash"). The example case studies (Milvus #49823, Qdrant #9255, Qdrant #9045) are well-chosen and illustrative.
   - **5.3 [minor, fixable]** Table 2 (operating points) uses "---" for accuracy on the "5-run majority" configuration, which is unclear. Is this missing data, or is accuracy undefined for majority voting? A footnote or explicit "N/A" would clarify.
   - **5.4 [minor, fixable]** The Related Work section (Section 7) is dense and would benefit from sub-paragraph breaks to separate the four threads (VDBMS testing, REST-API oracles, LLM-as-judge, documentation-derived oracles) for readability.

## Meta-Review

### Criterion Consensus

| Criterion | Reviewer 1 | Reviewer 2 | Reviewer 3 | Meta-Review |
|---|---|---|---|---|
| Significance | Adequate | Adequate | Adequate | **Adequate** |
| Novelty | Excellent | Adequate | Adequate *(prov)* | **Adequate** |
| Soundness | Adequate | Weak | Adequate | **Adequate** *[Mixed]* |
| Verifiability | Adequate | Adequate | Adequate | **Adequate** |
| Presentation | Excellent | Adequate | Adequate | **Adequate** |
| **Recommendation** | **Accept** | **Weak Accept** | **Weak Accept** | **ACCEPT** |

### Meta Recommendation

**ACCEPT**

三位 individual recommendation 均 Weak Accept 或更好（R1 Accept, R2/R3 Weak Accept）→ unanimous shortcut 直接判 ACCEPT。无 consensus Poor、无 substance consensus Weak（Soundness 上 R2 Weak 但 R1/R3 Adequate → consensus Adequate [Mixed]）→ ACCEPT 规则适用。

论文落在此处的 justification：source-as-falsifier 方向性不对称 vs MASTOR（source-as-oracle）是 verified novelty delta（R1 评 Novelty Excellent）；49 TP + 15 merged-PR industry impact 实质；Table 1 排除论证 + dev-reviewer 3-check + ablation 构成可证伪设计。三份 review 都识别 post-hoc 操作点 + external validity 为主要 gap，但都判为 fixable in revision。

### Priority Revisions

1. **[major, fixable]** post-hoc 操作点 selection-aware CI（R1-3.5 / R2-3.2 / R3-4.2 + 态度 R1/R2 共识）
2. **[major, fixable]** external validity mini case（R1-1.2 / R2-3.4 / R3-W3 + 态度 R1/R3 共识）
3. **[major, fixable]** single LLM backbone 第三 family（R1-W1 + R3-3.2）
4. **[minor, fixable]** Novelty vs REST-API 边界强化（R3-W1）
5. **[minor, fixable]** cost breakdown 表（R2-4.2）
6. **[minor, fixable]** Presentation（R1-5.4/5.5 / R3-5.3/5.4）

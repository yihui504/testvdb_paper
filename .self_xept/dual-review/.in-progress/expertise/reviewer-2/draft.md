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

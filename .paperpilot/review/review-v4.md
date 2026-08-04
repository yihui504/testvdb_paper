## Reviewer 1: Domain Expert

**Overall Recommendation:** Accept

### Summary
TestVDB targets documentation-implementation defects in Vector Database Management Systems (VDBMSs)—cases where a VDBMS silently accepts inputs or produces behaviors that violate its API documentation. Because VDBMS documentation is natural-language prose rather than structured specifications, deterministic oracles (crash-based, differential testing, metamorphic relations, property-based testing) cannot adjudicate these accept/reject decisions. The paper instantiates a four-stage pipeline (behavioral-claim extraction from documentation, test-script generation, sandboxed execution, defect confirmation) using LLMs to read documentation, generate tests, and adjudicate responses. Two false-positive failure modes emerge: hallucination in extraction (LLM invents constraints the documentation does not state) and self-preference bias in judgment (same-family LLMs over-confirm their own extracted claims). A multi-perspective judging baseline raises precision but collapses recall, so the authors introduce a dev-reviewer agent that acts as a source-grounded falsifier—reproducing each candidate, cross-checking against implementation source, and attempting disproof. Evaluation on three VDBMSs (Milvus, Qdrant, Weaviate) yields 107 submitted issues with 50 maintainer-acknowledged true-positive defects (15 merged-PR-fixed). On a controlled 48-candidate retrospective, the dev-reviewer reaches 67% precision and 74% recall (3-run ensemble) against 37% recall without source grounding. A bidirectional probe against VDBFuzz shows complementary coverage: TestVDB reaches a crash-class defect by contract reasoning, while VDBFuzz misses a silent-accept defect under current templates.

### Core Strengths
- **S1:** Clear problem formulation — the paper carves out a genuine, previously unaddressed defect class (documentation-implementation gaps) and rigorously argues why existing oracles cannot reach it (Section 2, Table 1). The exclusion argument is systematic and convincing.

- **S2:** Source-grounded falsification is a sound, well-motivated contribution — the dev-reviewer's three-check design (independent reproducibility, evidence sufficiency, falsifiability) is a principled response to the two diagnosed false-positive modes (Sections 3–4). Moving ground truth from the LLM to the implementation is a strong conceptual move.

- **S3:** Evaluation is unusually thorough for an LLM-based testing tool — the paper reports maintainer-adjudicated yield (50 TP of 107 submitted), a controlled 48-candidate retrospective with precision/recall, ablation studies, and a bidirectional probe against a domain-specific fuzzer (RQ1–RQ3). The 15 merged-PR fixes demonstrate practical impact.

- **S4:** Related work positioning is precise — the paper correctly distinguishes its target from SATORI (response-field oracles vs. input-acceptance) and MASTOR (implemented-behavior encoding vs. documentation-implementation gap detection), and appropriately leverages LLM-as-judge reliability literature (Panickssery, Wataoka, Haldar) to motivate the false-positive problem.

### Core Weaknesses
- **W1:** Cross-family generalization is an open, unaddressed question — Section 6 reports that the dev-reviewer's verdict is family-specific (Cohen's κ vs. GLM: 0.32 DeepSeek, 0.20 LongCat, 0.18 Qwen), with recall collapsing to 19–56% across three additional backbones. The paper acknowledges this as a limitation but provides no mitigation or path to resolution. This undermines the claim that source-grounded falsification is a robust solution to self-preference bias. — see 2.2

- **W2:** Construct validity: implementation-as-correct assumption is unbounded — the dev-reviewer treats the implementation source as ground truth for falsifying documentation-derived claims (Section 4). An implementation bug can wrongly suppress a true documentation-implementation defect. The paper argues this is rare (no observed FPs traced to implementation bugs) but provides no systematic analysis or falsification-test design to bound this risk. — see 2.3

- **W3:** Statistical rigor gaps on operating-point selection — the headline 74% recall (3-run any-confirmed ensemble) is a post-hoc selection among four operating points (Section 6, Table 4). Wilson CIs do not account for this selection, and the Bonferroni-corrected intervals are reported as a side note rather than the primary error bars. The bootstrap validation is a partial mitigation but does not fully address selection bias. — see 2.1

- **W4:** External validity is limited to VDBMSs with weak transfer evidence — the paper claims transferability to structurally similar documentation regimes (REST APIs without OpenAPI, configuration validation) on structural grounds only. The CouchDB case study (Section 7) is a single non-VDBMS example; Elasticsearch rejected every invalid probe (a failed probe, not successful transfer). One working example is insufficient to support transferability claims. — see 1.2

### Detailed Assessment

**1. Significance — Adequate**

- **1.1** The problem addressed is real and motivated. The empirical bug study (Section 1, paragraph 1) establishes that VDBMS defects are predominantly logical bugs, and the roadmap (Section 1) identifies oracle definition as a key challenge. Documentation-implementation defects are a genuine gap in coverage. The 15 merged-PR fixes across three production VDBMSs demonstrate practical impact.

- **1.2 [minor, fixable]** The scope is narrower than the framing suggests. The paper targets only VDBMSs with natural-language API documentation. Transfer to other systems (REST APIs without OpenAPI, configuration validation) is claimed on structural grounds only and not empirically validated beyond one CouchDB example (Section 7). This limits the significance of the contribution to the VDBMS domain unless transfer is demonstrated more broadly.

**2. Novelty — Excellent**

- **2.1** The novelty delta is clear and substantial. The paper's four-stage pipeline is a new instantiation of LLM-derived oracles for documentation-implementation testing. The dev-reviewer's source-grounded falsification (three-check design: independent reproducibility, evidence sufficiency, falsifiability) is not present in prior work. MASTOR reads source to generate oracles encoding implemented behavior; TestVDB reads source to falsify documentation-derived claims—these are fundamentally different targets. SATORI generates response-field oracles from OpenAPI; TestVDB targets input-acceptance on system-level prose—also a different target.

- **2.2** The paper correctly positions itself against REST-API oracle work. Section 5 (Related Work) accurately characterizes SATORI's scope (response-field properties from OpenAPI) and MASTOR's scope (implemented-behavior encoding from source), and articulates why neither addresses the documentation-implementation residual. This is verified by reading the cached summaries for both works.

- **2.3** The application of LLM-as-judge reliability insights (Panickssery, Wataoka: self-preference; Haldar: self-inconsistency) to the test-oracle domain is novel. The diagnosis of two failure modes (extraction hallucination, judgment self-preference) and the response (source-grounded falsification to move ground truth from LLM to implementation) is a genuine contribution not present in the cited LLM-as-judge papers.

**3. Soundness — Adequate**

- **3.1** The method is well-designed and appropriate to the problem. The four-stage pipeline (Section 3) is a logical decomposition of the documentation-implementation testing workflow. The dev-reviewer's three-check falsification (Section 4) is a principled response to the diagnosed false-positive modes. The multi-agent architecture with role prompts is a reasonable implementation choice.

- **3.2 [major, fixable]** Cross-family generalization is an unresolved threat to construct validity. Section 6 reports that three additional LLM backbones (DeepSeek, Qwen-3.8-Max, LongCat-2.0) achieve recall of 19–56% vs. GLM's 74% on the same 48-candidate retrospective, with Cohen's κ in the 0.18–0.32 range (slight-to-fair agreement). This shows the dev-reviewer's verdict is family-specific. The paper acknowledges this as a limitation but offers no mitigation (e.g., a cross-family voting scheme, a family-agnostic falsification protocol, or an analysis of what causes family-specific verdicts). This undermines the claim that source-grounded falsification is a robust solution to LLM-as-judge bias. The soundness of the method depends on an unproven assumption that a single family (GLM) is representative.

- **3.3 [major, fixable]** The implementation-as-correct assumption is unbounded. The dev-reviewer treats the implementation source as ground truth for falsifying documentation-derived claims (Section 4, paragraph 3). An implementation bug can cause the dev-reviewer to wrongly suppress a true documentation-implementation defect (a false negative). The paper argues this is rare ("no false positive was traced to an implementation bug") but provides no systematic analysis or falsification-test design to bound this risk. For example, a maintainer could close a confirmed candidate as wont-fix because the implementation behavior is intentional, even if the documentation is right and the implementation is buggy. The paper does not quantify this false-negative rate or describe a protocol for detecting it.

- **3.4** The evaluation on three VDBMSs (Milvus, Qdrant, Weaviate) with 107 submitted issues and 50 maintainer-acknowledged TPs provides reasonable evidence of detection capability. The 48-candidate retrospective with maintainer-adjudicated ground truth is a strong validity check. The bidirectional probe against VDBFuzz (Section 6, RQ3) is a well-designed complementarity test, though the systematic direction (VDBFuzz on v1.18.2, 26,000 requests, 0 of 14 TPs reached) is the generalizable result.

**4. Verifiability — Adequate**

- **4.1** The paper provides sufficient information to understand and follow the work. The four-stage pipeline is clearly described (Section 3). The dev-reviewer's three-check design is well-specified (Section 4, Figure 3). The evaluation protocol (RQ1–RQ3) is transparent. The paper links to an artifact (prompts, ground truth, reproduction driver) and declares it reachable. Based on the text, the artifact appears to contain the necessary materials (22 agent role definitions, 48-candidate ground truth, reproduction scripts), though I did not attempt to clone or run it.

- **4.2 [minor, fixable]** The cost accounting is approximate but transparent. Table 2 reports a per-target LLM-call distribution (~50% dev-reviewer source-grounding, ~25% claim extraction + test generation, ~25% judging + novelty gate) with a rough total cost of ~$10 per target at current API pricing. This is sufficient for reproducibility but could be more precise (e.g., exact token counts, per-stage costs).

- **4.3** The statistical reporting is generally thorough but has gaps (see Weakness W3). Wilson CIs are reported for precision and recall, but the headline operating point (3-run any-confirmed) is a post-hoc selection among four operating points. The Bonferroni correction is noted but not used as the primary error bar, and the bootstrap validation, while helpful, does not fully address selection bias. This is verifiability-impairing because the uncertainty around the headline 74% recall is larger than reported.

**5. Presentation — Adequate**

- **5.1** The paper is well-structured and readable. The introduction clearly motivates the problem and situates the contribution. The approach (Section 3) is logically laid out with a helpful figure (Figure 1). The false-positive problem (Section 4) and dev-reviewer solution (Section 4) are tightly argued. The evaluation (Section 6) is comprehensive and well-organized.

- **5.2 [minor, fixable]** There are occasional minor language issues and phrasing ambiguities. For example, Section 6, paragraph 2: "The yield is biased toward documentation-implementation defects by the tool's design (Section 7); the proportion reflects our yield, not a population estimate." This is awkwardly phrased and could be clarified. Section 6, paragraph 4: "Single-run recall varies widely (15--78%) because the LLM judge agent is high-variance" could be more precise about the source of variance (sampling vs. prompt sensitivity).

- **5.3 [minor, fixable]** The figures and tables are generally clear but have minor issues. Figure 2 (per-run recall) uses dots for individual runs but does not label the runs explicitly; the caption clarifies but a legend or run labels would help. Table 4 (operating points) reports "N/A" for 5-run majority accuracy but the value is inferable from the precision/recall; filling the cell would be cleaner.

- **5.4 [minor, fixable]** Threats to validity (Section 6, paragraph 7) are discussed but could be more explicit about the construct validity threat from cross-family variance. The paper notes that "all dev-reviewer results use a single LLM family (GLM-5.2)" and that cross-model re-runs show family-specific verdicts, but it does not flag this as a core construct validity threat in the threats section.

### Questions for Authors
- **Q1:** How would you design a cross-family robust version of the dev-reviewer? For example, a voting scheme across families, or a family-agnostic falsification protocol that achieves more stable recall? — Intended effect: If the authors provide a concrete mitigation plan for the cross-family generalization gap (item 3.2), the Soundness rating would move toward Adequate (currently held down by the unmitigated family-specific verdict issue).

- **Q2:** Can you design a falsification test for the implementation-as-correct assumption? For example, a protocol where the dev-reviewer also checks the implementation against independent sources (e.g., other vendors' documentation for cross-vendor APIs, or semantic consistency checks)? — Intended effect: If the authors provide a systematic way to bound the risk of implementation bugs causing false negatives (item 3.3), the Soundness rating would move toward Adequate.

- **Q3:** Why not use the Bonferroni-corrected CIs as the primary error bars for the headline 74% recall? This would transparently account for the operating-point selection bias. — Intended effect: If the authors adopt the Bonferroni-corrected intervals (or a more principled correction) as the primary uncertainty quantification (item 3.4, Weakness W3), the Verifiability rating would move toward Adequate (currently Adequate but with a statistical rigor gap).

- **Q4:** Can you provide more than one successful non-VDBMS transfer example? The CouchDB case study is promising, but Elasticsearch rejected every invalid probe. A second successful example (e.g., configuration validation in another system) would strengthen the transferability claim. — Intended effect: If the authors demonstrate transfer beyond one VDBMS+one successful non-VDBMS example (item 1.2, Weakness W4), the Significance rating would move toward Adequate (currently Adequate but with narrow scope).

---

## Reviewer 2: Area Specialist

**Overall Recommendation:** Accept

### Summary

This paper introduces TestVDB, a system for detecting documentation-implementation defects in Vector Database Management Systems (VDBMSs) using LLMs to extract behavioral claims from natural-language documentation, generate tests, execute them against sandboxed VDBMS instances, and confirm defects via a source-grounded dev-reviewer agent. The key insight is that when API documentation is prose rather than structured schemas (OpenAPI), deterministic oracles cannot adjudicate accept/reject decisions, leaving LLMs as the practical oracle. The authors identify two false-positive failure modes (extraction hallucination and judgment self-preference) and show that a multi-perspective judging baseline raises precision but collapses recall, motivating the dev-reviewer that falsifies LLM verdicts against implementation source. Across three VDBMSs (Milvus, Qdrant, Weaviate), TestVDB surfaced 107 submitted issues with 50 maintainer-acknowledged true-positive defects (15 fixed via merged PR). On a controlled 48-candidate retrospective, the dev-reviewer achieves 65% accuracy, 67% precision, and 74% recall (3-run any-confirmed ensemble), against a 37% recall baseline without source grounding. A bidirectional probe against VDBFuzz shows complementary coverage: TestVDB reaches a crash-class defect by contract reasoning (integer overflow) that VDBFuzz finds, while VDBFuzz misses a TestVDB silent-accept defect (zero-length vector acceptance) under its crash-only oracle.

### Core Strengths

- **S1:** Well-motivated problem statement targeting the documentation-implementation gap left by existing oracles — see Table 1 (oracle exclusion argument) and §7 (VDBFuzz probe).
- **S2:** Source-grounded dev-reviewer effectively mitigates LLM-as-judge false positives, lifting recall from 37% to 74% on a controlled retrospective — see 4.3, Table 4, Figure 4.
- **S3:** Comprehensive evaluation across three VDBMSs with maintainer-adjudicated ground truth, plus controlled retrospective and bidirectional VDBFuzz probe — see §7.
- **S4:** Strong contextualization with REST-API oracle work (SATORI, AGORA+, MASTOR) and LLM-as-judge reliability literature (Panickssery, Wataoka, Haldar) — see §6 and §8.

### Core Weaknesses

- **W1:** Results rely on a single LLM family (GLM-5.2); cross-family generalization is open question — see 7.3 and Table 6 (κ inter-family agreement: 0.32/0.20/0.18).
- **W2:** Evaluation limited to three VDBMSs; external validity beyond VDBMSs is weak (only brief CouchDB/Elasticsearch probes in §8) — see 7.2.
- **W3:** Candidate set in retrospective is maintainer-adjudicated but non-random; no pre-registration; selection bias possible — see 7.2, Table 2 Wilson CIs, and Bonferroni correction note.

### Detailed Assessment

#### 1. Significance — Adequate

- **1.1 [strength]** The problem is well-defined and motivated: documentation-implementation defects are prevalent (44 of 50 true positives are non-crashing) and structurally missed by crash oracles (VDBFuzz). The oracle-exclusion argument in Table 1 systematically walks through why deterministic oracles (differential, metamorphic, property-based, REST-API tools) cannot reach the residual, leaving LLMs as the only practical option. This is a real, impactful gap for VDBMS reliability.

- **1.2 [strength]** The 50 maintainer-acknowledged true positives (15 merged-PR fixes) across three production VDBMSs demonstrate practical impact. The defect examples are concrete: Milvus silently accepting `nprobe=0` (documented range [1, 16384]), Qdrant accepting zero-length vectors with `wait=false`, Weaviate allowing deletion of nonexistent classes. These corrupt query semantics in downstream RAG pipelines.

- **1.3 [weakness]** Significance beyond VDBMSs is claimed but weakly demonstrated. The CouchDB 3.4.3 (three gaps reproduced on 3.5.2) and Elasticsearch 8.11.0 (rejected all probes) case studies in §8 are positive but minimal. Transfer to "structurally similar documentation regimes" (REST APIs without OpenAPI, configuration validation, policy-as-code) is asserted on structural grounds only, with no empirical test. The contribution could be broader, but the evidence is VDBMS-centric.

- **1.4 [weakness, fixable]** The yield precision (69.4%) is reported with context but still biased by the tool's design toward documentation-implementation defects. The paper correctly states this is not a population estimate (§7), but readers may misinterpret it. A brief sensitivity analysis (e.g., how yield varies with documentation style: explicit vs. implicit constraints) would clarify the scope.

**Overall:** Adequate. The problem is real and well-motivated within VDBMSs, with practical impact demonstrated, but generalization beyond VDBMSs is claimed rather than shown.

#### 2. Novelty — Adequate

- **2.1 [strength]** The two-axis contribution framing (documentation-implementation defects + LLM-derived oracle with source-grounded falsification) is novel. Table 1 systematically excludes existing oracles and positions TestVDB in the residual. The dev-reviewer's three-check falsification (independently reproducible, evidence sufficient, falsifiable) is a concrete mechanism for mitigating LLM-as-judge false positives.

- **2.2 [strength]** The diagnosis of two false-positive failure modes is precise and well-integrated with literature:
  - **Extraction hallucination:** LLM over-formalizes ambiguous prose ("optional, default 1" → "must be ≥ 1"). This is the test-oracle instance of general LLM hallucination~\cite{ji23hall}.
  - **Self-preference in judgment:** Same-family extractor and judge over-confirm due to self-recognition~\cite{panickssery24} and perplexity-based familiarity~\cite{wataoka24}. Multi-perspective judging cannot break documentation ambiguity, so recall collapses (15%). This is strongly supported by the literature.

- **2.3 [strength]** The dev-reviewer's **source-grounded falsification** is a novel contribution: implementation source is the only independent information channel that can break self-preference (Table 5 ablation: source alone suppresses 75% of FPs, retains all 4 TPs). The concept of using the implementation as a reference oracle for the documentation-derived claim is clever and well-motivated.

- **2.4 [weakness, unfixable]** The delta against MASTOR~\cite{mastor26} (closest prior work) is clear: MASTOR reads source to generate oracles encoding **implemented** behavior; TestVDB reads source to falsify **documented** claims. MASTOR cannot detect documentation-implementation gaps; TestVDB targets exactly that gap. However, the delta against SATORI~\cite{satori25} and AGORA+~\cite{agoraplus25} is thinner: both target response-field oracles under per-field anchoring (OpenAPI or traces), while TestVDB targets input-acceptance on prose. The paper correctly argues this is a distinct regime, but the novelty delta is incremental for the LLM-as-judge component.

- **2.5 [weakness, fixable]** The bidirectional probe with VDBFuzz (§7.3, Table 7) is methodologically sound but the **systematic direction** (26K requests, 0/14 TPs reached) conflates budget with scope. VDBFuzz ran 26K requests, but whether 26K is sufficient to cover 14 diverse silent-accept defects is not established. A more direct comparison would equip VDBFuzz with custom templates for the 14 defects and show it misses them systematically. The controlled cases (v1.4.0, v1.18.0) are convincing $n=1$ examples, but the systematic direction could be misread as general coverage when it may be a budget artifact.

**Overall:** Adequate. The core novelty (source-grounded falsification for documentation-implementation defects) is clear and well-positioned against REST-API oracle tools and LLM-as-judge reliability literature.

#### 3. Soundness — Adequate

- **3.1 [strength]** The oracle-exclusion argument (Table 1) is rigorous and well-explained. Each row explains why a standard oracle cannot reach the documentation-implementation residual: crash oracles miss 44/50 TPs; differential testing cannot adjudicate accept/reject that diverges by design; metamorphic relations address result correctness, not input-acceptance; property-based testing needs OpenAPI schemas (rare for VDBMSs); REST-API tools target response-field/runtime properties under per-field anchoring. The residual leaves an LLM as the only practical option, which logically motivates the approach.

- **3.2 [strength]** The false-positive diagnosis is empirically grounded. Two failure modes are identified with distinct causes (extraction hallucination vs. self-preference) and supported by literature citations. The multi-perspective judging baseline (four specialized judge agents) is a reasonable counterfactual: it reaches 80% precision but 15% recall (Table 3), confirming that the problem is structural (judges read same ambiguous documentation), not a tuning problem. This motivates the dev-reviewer.

- **3.3 [strength]** The dev-reviewer evaluation is thorough and well-controlled:
  - **Controlled retrospective:** 48 maintainer-adjudicated candidates (27 TP, 21 FP) with clear ground truth.
  - **Three ablation configurations (Table 5):** source alone suppresses 75% FPs (9/12), threat-model alone 50% (6/12), union 91% (11/12), each retaining all 4 TPs. This isolates the source-grounded anchor as the dominant contributor.
  - **Source-disable experiment (§7.2):** Disabling Step 3.5 (source grounding) collapses recall from 74% to 19% and precision from 67% to 56%, directly measuring source grounding's contribution.
  - **Operating-point analysis (Table 4):** The 3-run any-confirmed ensemble is justified as falsifier semantics (surviving any independent falsification → higher likelihood of true defect) and sits at the precision-recall knee. Bootstrap validation supports robustness.

- **3.4 [strength]** The VDBFuzz bidirectional probe (Table 7) is conceptually strong: it shows TestVDB reaches a crash-class defect (Qdrant integer overflow on `size=2^63`) by contract reasoning, while VDBFuzz misses a silent-accept defect (`wait=false` accepts zero-length vector) under its templates. This demonstrates complementary coverage (crash vs. silent-accept) and validates that documentation-implementation defects are not a subset of crash defects.

- **3.5 [weakness, fixable]** The single-LLM baseline for the retrospective (48%/56%/37%) is somewhat underspecified. Which LLM family? GLM-5.2 with what prompts? The comparison against multi-perspective judging (50%/80%/15%) uses the same backbone (GLM-5.2), but the single-LLM configuration is not detailed. Since this is the baseline for the dev-reviewer's gains, clarity on the prompt setup would strengthen reproducibility.

- **3.6 [weakness, unfixable]** The **implementation-as-correct assumption** (dev-reviewer treats source as ground truth) is a fundamental limitation. An implementation bug could wrongly falsify a correct documentation claim, producing false negatives. The paper acknowledges this and notes no such FPs were observed in the retrospective, but the rate is unquantified. A conservative estimate (even if small) would strengthen the threat discussion.

- **3.7 [weakness, unfixable]** Cross-family generalization is open and concerning. A cross-model re-run (DeepSeek, Qwen-3.8-Max, LongCat-2.0) shows the verdict is family-specific: Cohen's κ vs. GLM's 3-run union = 0.32/0.20/0.18 (slight-to-fair band). Recall drops sharply for other families (DeepSeek 56%, LongCat 22%, Qwen 19% vs. GLM's 74%). The paper correctly flags this as an open question, but it limits confidence that the approach generalizes beyond GLM-5.2.

**Overall:** Adequate. The approach is sound, well-motivated, and empirically supported with thorough ablations and controlled comparisons. The main limitations (implementation-as-correct assumption, cross-family dependence) are acknowledged and clearly framed as open questions rather than ignored.

#### 4. Verifiability — Adequate

- **4.1 [strength]** The artifact description is comprehensive. The paper promises: full prompts (22 agent role definitions), target versions (Milvus 2.6.19, Qdrant v1.18.2, Weaviate v1.38.2), per-token accounting, 48-candidate ground truth, and reproduction driver. The artifact URL (https://github.com/yihui504/testvdb-anon) is declared reachable. This is sufficient for a technical paper—cloning the repository would be the next step for full verification, but the description meets the bar.

- **4.2 [strength]** The evaluation is well-documented and reproducible in principle:
  - **VDBMS versions are pinned** (Milvus 2.6.19, Qdrant v1.18.2, Weaviate v1.38.2).
  - **LLM configuration is explicit:** GLM-5.2 backbone via BigModel Anthropic-compatible API, default sampling, no decoding overrides.
  - **Cost per target** is reported (~$10, dominated by source grounding and live Docker re-probes; Table 3 breaks down LLM-call distribution).

- **4.3 [strength]** Statistical reporting is better than many LLM-as-judge papers:
  - **Wilson 95% CIs** for precision/recall (e.g., 67% precision [49%, 81%]).
  - **Bonferroni correction** across four operating points is noted (would widen 3-run CI to [44%, 84%] / [51%, 89%]).
  - **Bootstrap validation** (2000 resamples) supports robustness (precision [53%, 83%] / recall [71%, 96%]).
  - **Cohen's κ** for inter-family agreement is reported (0.32 DeepSeek, 0.20 LongCat, 0.18 Qwen).

- **4.4 [weakness, fixable]** The **48-candidate retrospective** is maintainer-adjudicated but **non-random and not pre-registered**. The paper acknowledges selection bias and correctly treats this as a limitation (§7.2). However, reporting the selection criteria explicitly (e.g., "candidates flagged by the pipeline that received maintainer adjudication") and basic demographics (e.g., distribution across vendors, defect types) would improve transparency. A capture-recapture estimation of the total defect space, even if rough, would be better than no population estimate at all.

- **4.5 [weakness, fixable]** The **systematic VDBFuzz direction** (26K requests, 0/14 TPs reached) is methodologically limited. The paper argues this is structural (silent accepts return HTTP 200, crash oracles cannot detect them by construction), which is logically sound. However, 26K requests across 14 diverse defects may not cover the input space sufficiently. A more targeted experiment would be: **equipping VDBFuzz with custom templates for the 14 defects and running it until it finds each or exhausts a budget**. This would directly show VDBFuzz can (or cannot) reach these defects, rather than inferring it from a single fixed-budget run. The current comparison is suggestive but not conclusive.

- **4.6 [weakness, fixable]** The **multi-perspective judging baseline configuration** (four specialized judge agents, majority-of-four voting) is not fully specified. The paper lists the four roles (Table 3: documentation, evidence, severity, novelty) but does not detail their prompts, how they vote, or whether they use chain-of-thought. Since this baseline is central to establishing the dev-reviewer's necessity, reproducibility matters. The prompts should be in the artifact, but a brief summary in the paper (or appendix) would improve self-containedness.

**Overall:** Adequate. The paper provides sufficient detail to understand and verify the core approach, with good statistical reporting and artifact declaration. The main reproducibility gaps (non-random retrospective, VDBFuzz budget, multi-perspective prompts) are fixable with modest additions and do not undermine the core claims.

#### 5. Presentation — Adequate

- **5.1 [strength]** The structure is logical and readable. Table 1 (oracle exclusion) and Figure 1 (pipeline diagram) clearly position TestVDB in the landscape. The false-positive problem (§5) → dev-reviewer (§6) → evaluation (§7) flow is coherent. The Related Work (§8) is well-organized by theme (VDBMS testing, REST-API oracles, LLM-as-judge reliability, documentation-derived oracles).

- **5.2 [strength, minor, fixable]** The writing is generally clear, with good examples. The §4.2 example (Milvus `#49823` path: documentation → contract → probe → response → judge → dev-reviewer verification) is concrete and helpful. However, some technical density could be reduced for clarity:
  - **Table 4 (operating points):** The "per-run band" row (44–65% accuracy, 50–73% precision, 15–78% recall) packs three ranges into one cell. Splitting this into three rows (accuracy, precision, recall) or using a clearer tabular structure would make the variance more readable.
  - **Table 5 (ablation):** The "union (source + threat)" cell (91% FP suppression) is slightly misleading—11/12 FPs suppressed is 91.7%, but the cell rounds to integers. Reporting "91%" is fine, but "11/12 (92%)" would be precise.

- **5.3 [weakness, minor, fixable]** The **Cohen's κ inter-family agreement** results (DeepSeek 0.32, LongCat 0.20, Qwen 0.18) are reported in text but **not visualized**. A small figure (e.g., a heatmap or agreement matrix) would make the family-specific disagreement more intuitive than raw numbers. This is a quality-of-life improvement, not substantive.

- **5.4 [weakness, minor, fixable]** The **CouchDB/Elasticsearch case studies** in §8 are under-developed. They validate transferability but are terse. A small table (analogous to Table 7) listing the specific gaps found (e.g., `limit=0` returns zero rows, `limit=-1` silently accepted) would strengthen the generalization claim and make the non-VDBMS regime concrete. Currently, readers must infer the gaps from inline prose.

- **5.5 [weakness, minor, fixable]** **The Wilson CIs** are well-reported but could be more consistently formatted:
  - Some are inline (67% [49%, 81%]), others in text (e.g., Bonferroni correction discussion).
  - Consolidating all CIs into one table (operating points × metrics) would improve readability and comparison.

- **5.6 [strength, minor, fixable]** The **artifact URL** (https://github.com/yihui504/testvdb-anon) is declared reachable and the description (prompts under `agents/`, ground truth under `test_questions/`, reproduction under `reproduction/full52/`) suggests good organization. However, the paper does not explicitly state whether a **Docker image** or **reproduction script** exists for end-to-end pipeline execution. Adding a one-line reproduction command (e.g., "run `docker compose up` to execute the full pipeline on a controlled VDBMS version") would strengthen artifact usability.

**Overall:** Adequate. The paper is well-structured and readable, with strong examples and positioning. Minor tabular/visual improvements would enhance clarity but do not obstruct understanding.

### Questions for Authors

- **Q1:** The 48-candidate retrospective is maintainer-adjudicated but non-random. What are the selection criteria for inclusion, and how might they bias the precision/recall estimates? If you re-ran the pipeline on all 107 submissions (not just adjudicated ones), would the precision change materially?

  **Intended effect:** If selection is biased toward easy-to-adjudicate cases, the reported 67% precision may under- or over-estimate performance on the full candidate set. Clarifying selection criteria would assess generalizability.

- **Q2:** The systematic VDBFuzz direction (26K requests, 0/14 TPs reached) is used to argue that crash oracles cannot reach silent-accept defects. To strengthen this claim, have you considered equipping VDBFuzz with custom templates for each of the 14 defects and running it until it either detects each or exhausts a budget? This would directly show whether VDBFuzz's miss is structural or budgetary.

  **Intended effect:** Would resolve the ambiguity around whether 26K requests is sufficient coverage, making the complementary coverage argument more conclusive.

- **Q3:** Cross-family generalization is identified as an open question (κ values 0.32/0.20/0.18; recall drops to 56%/22%/19% vs. 74% for GLM-5.2). Have you considered a **hybrid approach** where the dev-reviewer runs multiple families in parallel and takes a majority vote? Given the observed variance (e.g., DeepSeek strong on Milvus, weak on Qdrant; Qwen weak on both), a family-specific routing strategy (e.g., "use DeepSeek for Milvus, GLM for Qdrant") might improve robustness. Is this direction worth exploring?

  **Intended effect:** If cross-family robustness is a concern, a hybrid/voting strategy could improve generalization without new architectural changes. Clarifies whether this is a future direction or a non-starter.


---

## Reviewer 3: General Reviewer

**Overall Recommendation:** Weak Accept

### Summary
This paper introduces TestVDB, a system for detecting documentation-implementation defects in Vector Database Management Systems (VDBMSs). The authors identify a class of defects where VDBMSs silently accept inputs that violate their API documentation (e.g., accepting `nprobe=0` when documentation specifies range [1, 16384]). Because these defects don't crash systems, they escape traditional fuzzers like VDBFuzz. The authors propose a four-stage LLM pipeline: (1) behavioral-claim extraction from documentation, (2) test-script generation, (3) sandboxed execution, and (4) defect confirmation. To address LLM false positives from hallucination and self-preference bias, they introduce a "dev-reviewer" agent that cross-checks claims against implementation source code. The authors report surfacing 107 candidate issues across Milvus, Qdrant, and Weaviate, with 50 maintainer-acknowledged true positives (15 fixed via merged PR), and demonstrate that source-grounded falsification improves recall from 37% to 74% on a controlled 48-candidate retrospective. A bidirectional comparison with VDBFuzz shows complementary coverage.

### Core Strengths
- **S1:** Well-motivated problem area with clear practical relevance — silent-accept defects in VDBMSs are a real issue that crashes-oracle fuzzers miss. — see 1.1, 1.2
- **S2:** The dev-reviewer's source-grounded falsification is a sensible countermeasure to self-preference bias and provides the methodological core novelty. — see 2.1, 2.2
- **S3:** Comprehensive evaluation with multiple complementary angles (real-world yield, controlled retrospective, bidirectional fuzzer comparison, cross-family validation). — see 3.1, 3.2, 3.3
- **S4:** Honest limitation discussion, particularly around LLM backbone dependence and the implementation-as-correct assumption. — see 3.4

### Core Weaknesses
- **W1:** Cross-family generalization is demonstrably weak — Cohen's κ values (0.18–0.32) against DeepSeek/Qwen/LongCat show the method is backbone-specific, yet the paper's framing doesn't adequately acknowledge this as a central limitation. — see 2.3
- **W2:** Operating-point selection (3-run union ensemble) is post-hoc; the Wilson confidence intervals don't account for this selection, creating potential overfitting to the retrospective. — see 3.5
- **W3:** The Weaviate evaluation is under-specified relative to Milvus/Qdrant — only an 11-candidate "controlled subset" with no per-vendor recall headline. — see 3.6

### Detailed Assessment

1. **Significance** — Adequate
   - **1.1** The problem motivation is strong. The authors convincingly establish that documentation-implementation defects are prevalent (50 true positives acknowledged by maintainers) and costly in the VDBMS domain (corrupt query semantics in RAG applications where wrong context reaches models). This is not a toy problem. — see Introduction, Section 2
   - **1.2** The impact claim is bounded but meaningful. The 15 merged-PR fixes across three production VDBMSs demonstrate practical relevance, though the 69% adjudicated yield (50 of 72 adjudicated) means nearly one-third of submissions are false positives or still pending. The authors correctly note this is biased by tool design, not a population estimate. — see Section 7 (RQ1), Table 3
   - **1.3 [minor, fixable]** The paper could strengthen significance by quantifying downstream impact. Beyond "corrupt query semantics," what is the actual user-facing harm? Silent-accept defects on parameters like `nprobe` or `wait=false` presumably affect retrieval quality, but the paper doesn't characterize this with latency, recall, or user-experience metrics. A single concrete example tracing a defect through to degraded RAG output would ground the significance claim. — see Section 1

2. **Novelty** — Adequate
   - **2.1** The source-grounded falsifier pattern is the clearest novel contribution. Most LLM-as-judge work treats the LLM as the final semantic arbiter (e.g., Toradocu, AugmenTest); TestVDB instead uses the implementation source as an independent falsifier. This is a sensible design choice that addresses the well-established self-preference bias problem~\cite{panickssery24,wataoka24}. — see Section 5, Figure 2
   - **2.2** The oracle-exclusion argument (Table 1) is thorough and correctly positions TestVDB relative to differential testing, metamorphic relations, property-based testing, and REST-API oracle tools (AGORA+, SATORI, MASTOR). The table clearly shows why none of these reach the documentation-acceptance residual. This framing is solid. — see Section 2, Table 1
   - **2.3 [major, fixable]** Cross-family generalization is weak. The independent cross-model re-run on DeepSeek, Qwen-3.8-Max, and LongCat-2.0 shows Cohen's κ values of 0.32, 0.18, and 0.20 respectively against GLM-5.2's 3-run union. This is the "slight-to-fair" band, indicating the verdict is family-specific. The paper acknowledges this ("we cannot claim cross-family robustness") but frames it as a limitation rather than a central architectural constraint. Given that all results use a single backbone (GLM-5.2), the method is effectively backbone-dependent. A clearer framing would treat source-grounded falsification as a technique that requires backbone-specific tuning rather than a general solution. The DeepSeek result (75% recall on Milvus) shows the approach can transfer, but the Qdrant collapse (0% vs. GLM's 29%) reveals vendor-specific sensitivity. — see Section 7 (RQ2)
   - **2.4 [minor, fixable]** Related Work coverage is adequate but could be deeper. The paper cites REST-API oracle tools (AGORA+, SATORI, MASTOR) but doesn't deeply engage with whether their LLM-as-judge architectures also exhibit self-preference bias or whether source-grounded falsification could port to those domains. The connection to LLM-as-judge reliability work~\cite{panickssery24,wataoka24} is strong, but the paper could benefit from discussing whether Toradocu/AugmenTest's false-positive modes map to the hallucination/self-preference taxonomy here. — see Section 6 (Related Work)

3. **Soundness** — Adequate
   - **3.1** The main claims are supported by appropriate evaluation design. RQ1 (detection capability) uses real-world submission and maintainer adjudication as ground truth — the right proxy for defect true-positives when no catalog exists. RQ2 (false-positive suppression) uses a controlled 48-candidate retrospective with maintainer-adjudicated ground truth, which is methodologically sound. RQ3 (VDBFuzz comparison) uses a bidirectional probe with both systematic (26,000 requests on v1.18.2) and controlled (n=1 on v1.4.0, v1.18.0) cases. The triangulation across these three angles strengthens confidence. — see Section 7
   - **3.2** The ablation study (Table 5) on a 12-FP/4-TP Milvus control cleanly isolates the dev-reviewer's two anchors: source grounding suppresses 75% of false positives, threat-model anchor 50%, union 91%. This directly measures the self-preference reduction the authors claim. — see Section 7 (RQ2), Table 5
   - **3.3** The "source disabled" control (Section 7, RQ2) is a strong falsification test: disabling source grounding collapses recall from 74% to 19% and precision from 67% to 56%. This establishes source grounding as the dominant contributor to recall, not a marginal add-on. — see Section 7 (RQ2)
   - **3.4** The limitations section is honest about the implementation-as-correct assumption and the potential for false negatives when the documentation is right but the implementation is buggy. The 15 merged-PR fixes (implementation confirmed buggy) and 0 false positives traced to implementation bugs suggest this assumption holds in practice, but the authors correctly flag this as unquantified. — see Section 8 (Discussion and Limitations)
   - **3.5 [major, fixable]** Operating-point selection is post-hoc. The authors report four operating points (single run, 3-run union, 5-run union, 5-run majority) and select the 3-run union as the headline because it "sits at the knee of the precision-recall trade-off." This is a reasonable qualitative choice, but the Wilson CIs in Table 4 don't account for selection across four points, creating potential overfitting. The authors acknowledge this ("the Wilson CIs... do not account for this selection") and provide a Bonferroni-corrected CI that widens to [44%, 84%] / [51%, 89%], plus a bootstrap validation giving [53%, 83%] / [71%, 96%]. These alternative CIs support the qualitative claim, but the post-hoc selection weakens the statistical rigor. Pre-registering the operating point or using a held-out validation set would have strengthened this. — see Section 7 (RQ2), Table 4
   - **3.6 [minor, fixable]** The Weaviate evaluation is under-specified. The 48-candidate retrospective covers Milvus (32) and Qdrant (16) with per-vendor breakdown (Milvus 69%/73%/80% accuracy/precision/recall, Qdrant 56%/50%/57%), but Weaviate only gets an 11-candidate "controlled subset" with no per-vendor recall headline. The paper states Weaviate's "sparse maintainer-fixed TP density (3 of 30) precludes a per-vendor recall headline," which is fair, but this asymmetry is worth a clearer methodological note. — see Section 7 (RQ2)
   - **3.7 [minor, fixable]** The CouchDB case study (Section 8) is a promising portability probe but under-developed. The authors report three reproduced gaps on `/._changes` (`limit=0`, `limit=abc`, `limit=-1`) that mirror the VDBMS pattern, but this is n=1 without maintainer adjudication or comparison to a crash-oracle baseline. A fuller non-VDBMS evaluation would strengthen the transferability claim, which is currently only "structural." — see Section 8 (Discussion and Limitations)

4. **Verifiability** — Excellent
   - **4.1** The paper provides comprehensive replication materials. The artifact (https://github.com/yihui504/testvdb-anon) includes full agent prompts (22 definitions under `agents/`), target versions (Milvus 2.6.19, Qdrant v1.18.2, Weaviate v1.38.2), the 48-candidate ground truth (`test_questions/`), and a reproduction driver (`reproduction/full52/`). Per-token accounting and API provider details (GLM-5.2 via BigModel Anthropic-compatible API, default sampling) are specified. The appendix excerpts the two most critical agent prompts (contract-formalizer, dev-reviewer). This is well above the minimum for reproducibility. — see Section 3, Appendix
   - **4.2** The cost breakdown (Table 2) — roughly 50% dev-reviewer source-grounding, 25% claim extraction/test generation, 25% judging/novelty gate, ~$10 per target — gives readers a clear sense of computational footprint. This is useful for practical adoption. — see Section 3, Table 2

5. **Presentation** — Adequate
   - **5.1** The paper is well-structured and clearly written. The four-stage pipeline (Section 3) is easy to follow, and Figure 1 provides a helpful visual overview. The false-positive problem (Section 4) and dev-reviewer solution (Section 5) are logically separated. — see Sections 3–5
   - **5.2 [minor, fixable]** Figure 3 (per-run recall across five independent runs) could be clearer. The dots show raw recall values (15–78%), but the y-axis scaling (0–108%) makes the variance harder to read. A box-and-whisker plot or explicit error bars would better communicate the distribution. — see Section 7 (RQ2), Figure 3
   - **5.3 [minor, fixable]** Table 4 (operating points) is dense. The Wilson CIs are inline (e.g., 67% [49, 81]), and the Bonferroni-corrected and bootstrap alternatives are in prose. Consolidating all CI variants into the table (as separate rows) would make comparison easier. — see Section 7 (RQ2), Table 4
   - **5.4 [minor, fixable]** Minor formatting: Table 1 rows could be more consistently formatted (row 6 "LLM-derived oracle (TestVDB)" is bolded as the take-away, but the "Why it misses" column for this row is also bolded, which is visually redundant). — see Section 2, Table 1
   - **5.5 [minor, fixable]** The paper uses both "source-grounded" and "source grounding" as variants; standardizing on one would improve consistency. — see throughout Section 5–7

### Questions for Authors
- **Q1:** The cross-family results show DeepSeek reaches 75% recall on Milvus but 0% on Qdrant. Is this Qdrant collapse due to a specific architectural difference (e.g., HTTP response structure) that the dev-reviewer's source-grepping pattern doesn't generalize to? Understanding this would help readers assess whether the backbone-dependence is fundamental or fixable with prompt engineering. — intended effect: if the authors clarify the root cause of the Qdrant collapse, item 2.3's rating could move from Weak to Adequate.
- **Q2:** The 3-run union ensemble is selected post-hoc as "knee of the precision-recall trade-off." Would a 4-run union materially change the headline numbers? Providing the full operating-point curve (precision/recall vs. k-run union for k=1–5) would let readers verify that 3-run is indeed the knee. — intended effect: if the authors provide the full curve, item 3.5's concern about post-hoc selection would be mitigated.
- **Q3:** The Weaviate evaluation is limited to an 11-candidate "controlled subset." Are the 11 candidates representative of the 30 submitted to Weaviate, or are they cherry-picked? If the latter, the controlled-subset results may overstate performance. — intended effect: clarifying sampling methodology for item 3.6.

---

## Meta-Review (Round 4, post-v8 revisions)

### Criterion Consensus

| Criterion | Reviewer 1 (Domain) | Reviewer 2 (Area) | Reviewer 3 (Generalist) | Meta-Review |
|---|---|---|---|---|
| Significance | Adequate | Adequate | Adequate | **Adequate** |
| Novelty | Excellent | Adequate | Adequate | **Adequate** [Mixed: R1 Excellent] |
| Soundness | Adequate | Adequate | Adequate | **Adequate** |
| Verifiability | Adequate | Adequate | Excellent | **Adequate** [Mixed: R3 Excellent] |
| Presentation | Adequate | Adequate | Adequate | **Adequate** |
| **Recommendation** | **Accept** | **Accept** | **Weak Accept** | **ACCEPT** |

### Meta Recommendation

**ACCEPT**

All three reviewers leaned in (2 Accept + 1 Weak Accept), so the unanimous shortcut applies — every individual recommendation is Weak Accept or better. This **matches Round 3's verdict** (2 Accept + 1 WA) and confirms the v8 revisions (yield-number refresh, Weaviate controlled subset, CouchDB non-VDBMS case study) hold the ACCEPT band against a fresh independent re-read.

**Why not higher.** The consensus is capped at ACCEPT by three limitations all three reviewers independently flagged (all inherent to the contribution design):
- **Cross-family generalization** (R1 3.2, R2 3.7, R3 2.3 [major]): verdict is family-specific — Cohen's κ = 0.32/0.20/0.18 vs GLM-5.2, recall collapses to 19–56% on DeepSeek/Qwen/LongCat. Headline results are single-family (GLM-5.2).
- **Post-hoc operating-point selection** (R1 W3, R2 W3, R3 3.5 [major]): the 3-run union headline is selected post-hoc from four operating points; Wilson CIs do not account for this selection. Bonferroni + bootstrap are disclosed partial mitigations.
- **Implementation-as-correct assumption** (R1 W2, R2 3.6, R3 3.4): the dev-reviewer treats source as ground truth; an implementation bug could wrongly falsify a correct documentation claim. No observed FP was traced to an implementation bug, but the rate is unbounded.

**What the v8 revisions bought.**
- **Yield-number refresh (c58f351)** closed the artifact-vs-paper inconsistency (49→50 TP, Weaviate 13→14, yield 68.1→69.4%); no R4 reviewer flagged a number mismatch — the refresh held.
- **Weaviate controlled subset (8d4c00b)** partially addressed the prior "Weaviate yield-only" concern: an 11-candidate dev-reviewer probe (7 confirmed + 4 FP, overturning 5 stage2 decisions) demonstrates the falsifier runs on a third VDBMS. R2/R3 still note the per-vendor recall asymmetry (no Weaviate recall headline due to sparse TP density 3/30).
- **CouchDB non-VDBMS case study (aaf1e8e/8adaddf/5929919)** flipped the prior "CouchDB 0 defect" claim: three `_changes` input-validation gaps (limit=0 doc-impl contradiction; limit=abc→HTTP 500 badarg; limit=-1 silent unlimited) reproduced on CouchDB 3.5.2 (source byte-identical to 3.4.3). R1/R2 still flag this as n=1 and probe-observed (not maintainer-adjudicated); the 500-badarg gap has maintainer-fix precedent (COUCHDB-2375).

**Checker value (independent grounding).** R4's checker stage caught two issues a single-pass review would have missed:
- **R1 tier-vs-recommendation contradiction**: R1 rated Novelty Excellent (a substance criterion) but recommended Weak Accept; per rubric this satisfies Accept. R1 upgraded its Overall to Accept to match its tiers — moving R4 from 1-Accept+2-WA to 2-Accept+1-WA.
- **R3 broken references**: "Table 6" (does not exist; cross-family κ is in §7 prose) and "Figure 4" (dev-reviewer diagram is Figure 2) — both patched before synthesis.

This is exactly the grounding-error catch the independent-checker stage is for.

### Priority Revisions

1. **[consensus, major, inherent]** Cross-family generalization (R1 3.2, R2 3.7, R3 2.3): single LLM backbone (GLM-5.2); verdict is family-specific (κ 0.32/0.20/0.18). A multi-family voting/routing scheme or a full multi-family rerun is the primary future-work item; cannot be fully closed within revision.
2. **[consensus, major, fixable]** Post-hoc operating-point (R1 W3, R2 W3, R3 3.5): pre-register the operating point or hold out a validation set; Bonferroni + bootstrap already disclosed.
3. **[consensus, major, inherent-ish]** Implementation-as-correct (R1 W2, R2 3.6, R3 3.4): bound the false-negative rate when source is buggy; the 0-observed-FP-from-implementation-bug retrospective is the current (retrospective) bound.
4. **[R2/R3, minor, fixable]** Weaviate per-vendor recall asymmetry (R2 1.3, R3 W3/3.6): the 11-candidate probe addresses "yield-only" but not the recall headline; a larger Weaviate controlled set would close it.
5. **[R1/R2/R3, minor, fixable]** Non-VDBMS transfer (R1 W4, R2 W2/1.3, R3 3.7): the CouchDB case study gives n=1 with 3.5.2 reproduction; maintainer adjudication of the `_changes` 500-badarg gap (COUCHDB-2375 precedent) would convert "probe-observed gaps" into "confirmed TP."
6. **[R2, minor, fixable]** VDBFuzz budget-vs-scope (R2 2.5/4.5): equip VDBFuzz with custom templates per the 14 silent-accept defects to show the miss is structural, not budgetary.

**Trajectory:** R1 (3×WA) → R2 (3×WA) → R3 (2 Accept + 1 WA, ACCEPT) → **R4 (2 Accept + 1 WA, ACCEPT)**. R4 confirms R3's verdict under fresh independent review + grounding checks; the v8 revisions held the ACCEPT band and closed prior soundness mismatches (numbers, Weaviate yield-only, CouchDB 0-defect) without yet clearing the inherent cross-family / operating-point / implementation-as-correct ceiling.

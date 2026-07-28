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

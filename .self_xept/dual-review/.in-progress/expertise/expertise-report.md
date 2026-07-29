# Expertise Half — TestVDB v5（v4 修订后验证轮）

> 3 expertise reviewer + Meta-Review。v4 修订验证。checker: R1 3.1 Milvus/overall 混淆已 patch；R2 多为无 cache 视野误报；R3 CLEAN。**独立性 caveat：R1/R2 Detailed 大量雷同（论文+cache 相同→措辞趋同），R3 为独立确认。**

## Reviewer 1: Domain Expert

**Overall Recommendation:** Weak Accept

### Summary

TestVDB targets documentation-implementation defects in Vector Database Management Systems (VDBMSs): cases where a VDBMS silently accepts inputs or produces behaviors that violate its API documentation (e.g., accepting `nprobe=0` when documentation declares range `[1, 16384]`). Because the documented boundary is natural-language prose rather than a structured specification, deterministic oracles (crash detection, differential testing, metamorphic relations, property-based testing, REST-API spec-derived oracles) cannot adjudicate these accept/reject decisions. TestVDB instantiates a four-stage LLM pipeline: behavioral-claim extraction from documentation, test-script generation, sandboxed execution against Docker-pinned VDBMS instances (Milvus 2.6.19, Qdrant v1.18.2, Weaviate v1.38.2), and defect confirmation. The LLM-derived oracle introduces two false-positive modes: hallucination in extraction (LLM infers constraints documentation does not state) and self-preference bias in judgment (same-family LLM confirms its own extracted claim). Multi-perspective judging (four specialized judges voting) improves precision but collapses recall. TestVDB introduces a dev-reviewer agent as a source-grounded falsifier that independently reproduces candidates, cross-checks against implementation source, and attempts disproof. On 107 submitted issues across three VDBMSs, maintainers acknowledged 49 true-positive defects (15 merged-PR-fixed). A 48-candidate retrospective shows the dev-reviewer achieves 67% precision and 74% recall (3-run any-confirmed ensemble) versus 37% recall without source grounding. A bidirectional probe against VDBFuzz on Qdrant shows complementary coverage: TestVDB reaches a VDBFuzz crash-class defect by contract reasoning (integer overflow on `size=$2^{63}$`), while VDBFuzz misses a TestVDB silent-accept defect (`wait=false` accepting zero-length vectors) under its current templates.

### Core Strengths

- **S1:** Problem targeting is well-motivated and empirically grounded — VDBMS bug study shows 43% attributed to incorrect behavior and oracle definition is a key challenge, with most defects being functional failures rather than crashes — see 1.1, 2.1.

- **S2:** Oracle exclusion argument (Table 1) systematically traces why deterministic oracles miss documentation-implementation defects and positions LLM-derived oracles as the residual solution — see 2.1.

- **S3:** Source-grounded falsification via dev-reviewer is a sound architectural response to LLM false-positive modes; three-check falsification (independently reproducible, evidence sufficient, falsifiable) and the use of implementation source as independent ground truth break self-preference bias — see 5.1–5.3, 6.2.

- **S4:** Bidirectional VDBFuzz probe on Qdrant provides concrete evidence of complementary oracle coverage: TestVDB reaches crash-class defects through contract reasoning that VDBFuzz also reaches, while VDBFuzz misses silent-accept defects under current templates — see 6.3.

- **S5:** Empirical evaluation demonstrates practical impact: 49 maintainer-acknowledged true positives across three production VDBMSs, 15 merged-PR fixes, and external validity probes on CouchDB/Elasticsearch show the pipeline ports to non-VDBMS REST APIs — see 6.1, 7.

### Core Weaknesses

- **W1:** Cross-family generalization is an open question and acknowledged as a limitation; all results use a single LLM family (GLM-5.2), and an independent cross-model re-run shows verdict is family-specific (κ = 0.14–0.51 vs. GLM single-run) — this limits claims about LLM-derived oracle reliability beyond the evaluated backbone — see 2.3, 6.2.

- **W2:** Operating point selection is post-hoc; the 3-run any-confirmed ensemble is selected as the headline operating point after observing the precision-recall trade-off, yet the Wilson CIs in Table 2 do not account for this selection — the Bonferroni correction widens the precision CI to [44%, 84%] and recall to [51%, 89%], which changes the qualitative confidence interval — see 6.2, 6.4.

- **W3:** The worst-case-bound precision claim (46% treating unadjudicated submissions as false positives) is overly conservative given the maintainer-adjudicated yield precision of 68.1% — the paper should lead with the adjudicated number and treat the worst-case as a sensitivity bound, not the primary metric — see 6.1.

- **W4:** RQ3 external validity is weak: CouchDB and Elasticsearch probes show no silent-accept defects (only `limit=0` returning empty result sets, which is graceful behavior) because mature non-VDBMS APIs validate more strictly. The portability claim ("structurally similar documentation regimes") is therefore supported only by successful pipeline execution, not by defect detection in the target domain — see 7.

### Detailed Assessment

1. **Significance** — Adequate

- **1.1** The problem is significant and well-motivated. The paper anchors the contribution in an empirical VDBMS bug study showing 43% of defects attributed to incorrect behavior, with oracle definition identified as a key challenge (introduction, 2.1). The focus on logical bugs that do not crash addresses a real gap left by crash-oracle fuzzers like VDBFuzz.

- **1.2 [major, fixable]** The single-backbone limitation (GLM-5.2 only) significantly narrows the claims about LLM-derived oracle reliability. Section 6.2 reports an independent cross-model re-run (DeepSeek, Qwen-3.8-Max, LongCat-2.0) showing verdict is family-specific (κ = 0.14–0.51). This means the dev-reviewer's effectiveness is backbone-dependent, yet the abstract does not qualify the headline results ("67% precision and 74% recall") with "on GLM-5.2." The contribution is the pipeline architecture and the source-grounded falsifier concept, but the quantitative results should be explicitly scoped to the evaluated LLM family until cross-family robustness is demonstrated.

- **1.3** Practical impact is clearly demonstrated: 49 maintainer-acknowledged true positives across three production VDBMSs, 15 merged-PR fixes, and 107 submitted issues total. The Table 3 yield breakdown by vendor (Milvus 22/51 TP, Qdrant 14/26 TP, Weaviate 13/30 TP) shows the tool successfully surfaced real documentation-implementation defects in the wild.

2. **Novelty** — Adequate

- **2.1** Tested against verified competitors MASTOR (mastor26) and SATORI (satori25) via cached full texts. The paper correctly characterizes the delta:
  - **MASTOR** extracts from implementation source and encodes what code **does**; it cannot detect where code violates documentation because it treats source as ground truth (Section 2, Table 1 exclusion row). MASTOR's precision-biased design explicitly excludes OAS-declared items not traceable to source, while TestVDB's dev-reviewer uses source to **falsify** documentation-derived claims.
  - **SATORI** extracts from OpenAPI schema fields (type, format, minimum, maximum) and stays in the low-ambiguity regime where constraints are explicit. TestVDB handles the high-ambiguity regime where constraints exist only in natural-language prose (e.g., "nprobe in [1, 16384]" stated in text but absent from schema).
  The characterization is accurate. The delta is the documentation-implementation **gap detection** regime, not the general LLM-as-oracle idea (which AugmenTest established for code documentation, see Related Work).

- **2.2** Checked against AugmenTest (augmentest25, arXiv:2501.17461): AugmenTest infers oracles from documentation using LLMs but validates through runtime behavior only (compilation feedback, differential execution). TestVDB correctly positions its novelty as **source-grounded falsification** — the dev-reviewer introduces implementation source as an independent verification signal, breaking the LLM-as-final-arbiter pattern. The Related Work discussion is accurate.

- **2.3** Self-preference bias as a false-positive mode is correctly grounded in Panickssery et al. (panickssery24) and Wataoka et al. (wataoka24). These works establish self-preference for LLM-as-judge in text evaluation; TestVDB correctly extends it to the test-oracle pipeline where the same family extracts and judges. The multi-perspective judging baseline (Table 4) is a sound approach to mitigating self-preference, and the finding that it collapses recall due to shared documentation ambiguity is well-demonstrated.

- **2.4 [major, fixable]** Missing systematic coverage of REST-API oracle derivation from natural-language documentation using pre-LLM NLP/pattern-matching techniques (e.g., Toradocu for Javadoc @throws comments). The Related Work mentions Toradocu but positions it as "deterministic extraction handles simple syntactic patterns," which may understate its coverage of natural-language API documentation. A targeted comparison or at least a citation to the NLP-based literature on extracting constraints from prose would strengthen the novelty positioning.

- **2.5 [minor, fixable]** The bidirectional VDBFuzz probe (Section 6.3, Table 6) is a strong complementarity argument, but VDBFuzz itself could not be fetched via literature search scripts (multiple queries returned no results). The paper relies on the VDBFuzz citation as provided; an independent verification of VDBFuzz's crash-detection limitations would strengthen the "structural blindness" claim. Given the context, this is acceptable but worth flagging.

3. **Soundness** — Adequate

- **3.1** The core claims are supported by the evaluation. The 48-candidate retrospective (27 TP, 21 by-design or rejected) with maintainer adjudication provides a reasonable ground truth. The dev-reviewer's recall gain from 37% (single-LLM baseline) to 74% (3-run any-confirmed with source grounding) is well-demonstrated in Table 5 and the source-disabled ablation (Section 6.2: disabling Step 3.5 drops overall recall from 74% to 19%; on Milvus specifically, from 80% to 5%). The three-check falsification design (independently reproducible, evidence sufficient, falsifiable) is sound, and the #9255 reversal example illustrates suppression of a false positive whose root cause was `assertion_depends_on_unrequested_field`.

- **3.2 [major, fixable]** Operating point selection bias. The headline operating point (3-run any-confirmed ensemble) is selected post-hoc from four reported operating points (Table 5). The Wilson CIs reported for the 3-run union (precision [49%, 81%], recall [55%, 87%]) do not account for selection across these four points. The Bonferroni correction (α = 0.05/4) mentioned in the text widens the CIs to roughly precision [44%, 84%] and recall [51%, 89%]. This is a standard adjustment for multiple comparisons in operating-point selection, but the paper should report the adjusted CIs as primary or at least acknowledge the selection clearly in the abstract ("we select the 3-run union as the operating point; Bonferroni-adjusted 95% CIs are precision [44%, 84%], recall [51%, 89%]"). Without this, the CIs are artificially narrow.

- **3.3** Threats to validity are thoroughly discussed. Internal validity threats (single-run variance, post-hoc operating point, non-random 48-candidate set) are acknowledged. External validity threats (Weaviate yield-only, single LLM family, no cross-family robustness, no result correctness claims) are also acknowledged. The implementation-as-correct assumption is bounded: 15 merged-PR fixes suggest it holds often enough to be useful, but the paper correctly notes it cannot guarantee correctness and could wrongly falsify right documentation.

- **3.4 [minor, fixable]** RQ3 external validity is weak but acknowledged. The CouchDB and Elasticsearch probes (Section 7) executed successfully but found no silent-accept defects because mature non-VDBMS APIs validate more strictly. The portability claim ("structurally similar documentation regimes") is therefore supported only by pipeline execution, not by defect detection. The paper should explicitly frame this as a **portability probe** (does the pipeline run end-to-end on a non-VDBMS target?) rather than a generalization result ("CouchDB and Elasticsearch confirmed the pattern"). The current framing risks overstating external validity.

4. **Verifiability** — Adequate

- **4.1** The paper provides sufficient information to understand and replicate the core pipeline. The four-stage architecture (claim extraction, test generation, execution, confirmation) and the dev-reviewer's three-check falsification are clearly described (Section 3, Section 5). Figure 1 and Figure 3 illustrate the pipeline and dev-reviewer workflow. The abstract and body state that the full prompts, target versions, and per-token accounting will be released at a persistent URL upon acceptance.

- **4.2 [minor, fixable]** Artifact availability is declared ("we will release [the artifact] at a persistent URL upon acceptance") but not yet available. For Verifiability, the paper should either (a) provide a GitHub repo link to the current state (even if under the anonymity embargo) or (b) explicitly state that the artifact is under embargo and will be released upon camera-ready. The current "we will release... upon acceptance" is ambiguous about whether the code exists now or will be created later.

- **4.3** Link rot check: Table 1 citations (AGORA+, SATORI, MASTOR, VDBFuzz, AugmenTest, metamap, etc.) and Related Work citations appear to be properly formatted. No obviously broken links detected in the references section. The VDBFuzz citation could not be independently fetched via literature search, but the provided bibliographic entry is consistent with its description.

5. **Presentation** — Adequate

- **5.1 [minor, fixable]** Worst-case-bound precision led abstract. The abstract states "maintainer-adjudicated yield precision 68%, or 46% as a worst-case bound treating unadjudicated submissions as false positives." This is technically correct but misleading: the adjudicated precision (68%) is the primary metric, and the 46% worst-case bound should be a secondary sensitivity analysis. The abstract should lead with the adjudicated number and footnote the worst-case bound.

- **5.2 [minor, fixable]** Metric terminology: Section 6.2 uses "accuracy" but Table 5 and the ablation text report "65% accuracy" for the 3-run union. In a binary classification context (TP vs. not-TP), this is standard accuracy, but given the class imbalance (27 TP, 21 FP in the 48-candidate set), accuracy is less informative than precision/recall/F1. The paper should consistently use precision/recall/F1 for the main discussion and mention accuracy only parenthetically.

- **5.3 [minor, fixable]** Table 6 (bidirectional VDBFuzz probe versions) formatting: The table lists three Qdrant versions but the prose describes "controlled cases on v1.4.0 and v1.18.0 (n=1 each)." The table correctly shows v1.4.0 (VDBFuzz crash) and v1.18.0 (TestVDB #9045) as controlled cases, but the "n=1 each" notation is more transparent than the implicit "single case per version" reading. Consider clarifying as "n=1 for each controlled version."

- **5.4** Structure and readability are strong. The paper follows a logical flow: problem motivation → oracle exclusion argument → approach → false-positive diagnosis → dev-reviewer solution → evaluation (RQ1–RQ3) → limitations. Figures and tables are well-placed. The Related Work correctly positions the contribution relative to MASTOR, SATORI, AugmenTest, and self-preference bias literature.

---

## Reviewer 2: Area Specialist

**Overall Recommendation:** Weak Accept

### Summary

TestVDB addresses the test-oracle problem for Vector Database Management Systems (VDBMSs) where documentation declares constraints in natural-language prose (e.g., `nprobe` range `[1, 16384]`) that implementation may silently violate. Because these constraints are not encoded in structured schemas or machine-checkable contracts, deterministic oracles (crash detection, schema validation, differential testing) cannot detect accept/reject violations. TestVDB instantiates a four-stage LLM pipeline: behavioral-claim extraction from documentation, test-script generation, sandboxed Docker-pinned execution against production VDBMS instances (Milvus 2.6.19, Qdrant v1.18.2, Weaviate v1.38.2), and defect confirmation. The LLM-derived oracle introduces two false-positive modes identified in the LLM-as-judge literature: hallucination during extraction (LLM infers constraints documentation does not state) and self-preference bias during judgment (same-family LLM confirms its own extracted claim). TestVDB introduces a dev-reviewer agent as a source-grounded falsifier that independently reproduces candidates, cross-checks against implementation source, and applies three-check falsification (independently reproducible, evidence sufficient, falsifiable). On 107 submitted issues across three VDBMSs, maintainers acknowledged 49 true-positive defects (15 merged-PR-fixed). A 48-candidate retrospective shows the dev-reviewer achieves 67% precision and 74% recall (3-run any-confirmed ensemble) versus 37% recall without source grounding. The paper demonstrates external validity via portability to CouchDB/Elasticsearch and complementary coverage with VDBFuzz on Qdrant.

### Core Strengths

- **S1:** The test-oracle problem for documentation-implementation gaps is well-motivated and empirically grounded — VDBMS bug study shows 43% attributed to incorrect behavior, with most defects being functional silent-accept bugs rather than crashes, positioning this as a gap left by crash-oracle fuzzers — see 1.1, 2.1.

- **S2:** Oracle exclusion argument (Table 1) systematically traces why deterministic oracles (crash detection, schema validation, differential testing, metamorphic relations) miss documentation-implementation defects and positions LLM-derived oracles as the residual solution — see 2.1.

- **S3:** Source-grounded falsification via dev-reviewer is a sound architectural response to LLM false-positive modes; three-check falsification (independently reproducible, evidence sufficient, falsifiable) and the use of implementation source as independent ground truth directly addresses self-preference bias documented in Panickssery et al. and Wataoka et al. — see 5.1–5.3, 6.2.

- **S4:** Empirical evaluation demonstrates practical impact: 49 maintainer-acknowledged true positives across three production VDBMSs, 15 merged-PR fixes, and external validity probes on CouchDB/Elasticsearch show the pipeline ports to non-VDBMS REST APIs — see 6.1, 7.

- **S5:** Bidirectional VDBFuzz probe on Qdrant provides concrete evidence of complementary oracle coverage: TestVDB reaches crash-class defects through contract reasoning that VDBFuzz also reaches (integer overflow on `size=$2^{63}$`), while VDBFuzz misses TestVDB silent-accept defects (`wait=false` accepting zero-length vectors) under its current templates — see 6.3.

### Core Weaknesses

- **W1:** LLM-as-judge reliability claims are not independently measured for self-preference bias. The paper cites Panickssery et al. and Wataoka et al. as motivation for multi-perspective judging and dev-reviewer source grounding, but does not apply their quantitative bias metrics to measure whether TestVDB's judge agents (judge-evidence, judge-novelty, judge-severity) actually exhibit reduced self-preference compared to single-LLM judging — see 2.3, 6.2.

- **W2:** The worst-case-bound precision claim (46% treating unadjudicated submissions as false positives) is overly conservative given the maintainer-adjudicated yield precision of 68.1% — the abstract should lead with the adjudicated number and treat the worst-case as a sensitivity bound — see 6.1.

- **W3:** RQ3 external validity is weak: CouchDB and Elasticsearch probes show no silent-accept defects (only `limit=0` returning empty result sets, which is graceful behavior) because mature non-VDBMS APIs validate more strictly. The portability claim ("structurally similar documentation regimes") is therefore supported only by successful pipeline execution, not by defect detection in the target domain — see 7.

- **W4:** Operating point selection is post-hoc; the 3-run any-confirmed ensemble is selected as the headline operating point after observing the precision-recall trade-off, yet the Wilson CIs in Table 2 do not account for this selection — the Bonferroni correction widens the precision CI to [44%, 84%] and recall to [51%, 89%], which changes the qualitative confidence interval — see 6.2, 6.4.

### Detailed Assessment

1. **Significance** — Adequate

- **1.1** The problem is significant and well-motivated. The paper anchors the contribution in an empirical VDBMS bug study showing 43% of defects attributed to incorrect behavior, with oracle definition identified as a key challenge (introduction, 2.1). The focus on logical bugs that do not crash addresses a real gap left by crash-oracle fuzzers like VDBFuzz.

- **1.2 [minor, fixable]** LLM-as-judge reliability claims require independent verification. The paper correctly cites Panickssery et al. (self-preference bias correlates with self-recognition) and Wataoka et al. (self-preference stems from perplexity familiarity) as motivation for multi-perspective judging and source-grounded falsification. However, the paper does not apply Wataoka's Equal Opportunity metric or Panickssery's self-recognition tests to measure whether TestVDB's judge agents actually exhibit reduced bias. The dev-reviewer's source grounding should reduce self-preference (as Wataoka suggests lower perplexity/familiarity drives bias), but this remains unmeasured. The paper should report bias metrics for (a) single-LLM judging, (b) multi-perspective judging, and (c) dev-reviewer judging to demonstrate the claimed bias reduction.

- **1.3** Practical impact is clearly demonstrated: 49 maintainer-acknowledged true positives across three production VDBMSs, 15 merged-PR fixes, and 107 submitted issues total. The Table 3 yield breakdown by vendor (Milvus 22/51 TP, Qdrant 14/26 TP, Weaviate 13/30 TP) shows the tool successfully surfaced real documentation-implementation defects in the wild.

2. **Novelty** — Adequate

- **2.1** Tested against verified competitors MASTOR (mastor26) and SATORI (satori25) via cached full texts. The paper correctly characterizes the delta:
  - **MASTOR** extracts from implementation source and encodes what code **does**; it cannot detect where code violates documentation because it treats source as ground truth (Section 2, Table 1 exclusion row). MASTOR's precision-biased design explicitly excludes OAS-declared items not traceable to source, while TestVDB's dev-reviewer uses source to **falsify** documentation-derived claims.
  - **SATORI** extracts from OpenAPI schema fields (type, format, minimum, maximum) and stays in the low-ambiguity regime where constraints are explicit. TestVDB handles the high-ambiguity regime where constraints exist only in natural-language prose (e.g., "nprobe in [1, 16384]" stated in text but absent from schema).
  The characterization is accurate. The delta is the documentation-implementation **gap detection** regime, not the general LLM-as-oracle idea (which AugmenTest established for code documentation, see Related Work).

- **2.2** Checked against AugmenTest (augmentest25, arXiv:2501.17461): AugmenTest infers oracles from documentation using LLMs but validates through runtime behavior only (compilation feedback, differential execution). TestVDB correctly positions its novelty as **source-grounded falsification** — the dev-reviewer introduces implementation source as an independent verification signal, breaking the LLM-as-final-arbiter pattern. The Related Work discussion is accurate.

- **2.3** Self-preference bias as a false-positive mode is correctly grounded in Panickssery et al. (panickssery24) and Wataoka et al. (wataoka24). These works establish self-preference for LLM-as-judge in text evaluation; TestVDB correctly extends it to the test-oracle pipeline where the same family extracts and judges. The multi-perspective judging baseline (Table 4) is a sound approach to mitigating self-preference, and the finding that it collapses recall due to shared documentation ambiguity is well-demonstrated.

- **2.4 [major, fixable]** LLM-as-judge bias not independently measured. The paper relies on Panickssery and Wataoka as motivational citation but does not apply their metrics to TestVDB's own judge agents. Wataoka's Equal Opportunity metric (bias = P(judge=self|human=self) - P(judge=self|human≠self)) could be computed on TestVDB's judge-evidence decisions to quantify self-preference. Panickssery's self-recognition test could determine whether judge-evidence recognizes its own extracted claims. Without these measurements, the claim that dev-reviewer "addresses self-preference bias" is asserted rather than demonstrated. The paper should report bias metrics for all three judge agents to validate the mitigation strategy.

- **2.5 [minor, fixable]** The bidirectional VDBFuzz probe (Section 6.3, Table 6) is a strong complementarity argument, but VDBFuzz itself could not be fetched via literature search scripts (multiple queries returned no results). The paper relies on the VDBFuzz citation as provided; an independent verification of VDBFuzz's crash-detection limitations would strengthen the "structural blindness" claim. Given the context, this is acceptable but worth flagging.

3. **Soundness** — Adequate

- **3.1** The core claims are supported by the evaluation. The 48-candidate retrospective (27 TP, 21 by-design or rejected) with maintainer adjudication provides a reasonable ground truth. The dev-reviewer's recall gain from 37% (single-LLM baseline) to 74% (3-run any-confirmed with source grounding) is well-demonstrated in Table 5 and the source-disabled ablation (Section 6.2: disabling Step 3.5 drops overall recall from 74% to 19%; on Milvus specifically, from 80% to 5%). The three-check falsification design (independently reproducible, evidence sufficient, falsifiable) is sound, and the #9255 reversal example illustrates suppression of a false positive whose root cause was `assertion_depends_on_unrequested_field`.

- **3.2 [major, fixable]** Operating point selection bias. The headline operating point (3-run any-confirmed ensemble) is selected post-hoc from four reported operating points (Table 5). The Wilson CIs reported for the 3-run union (precision [49%, 81%], recall [55%, 87%]) do not account for selection across these four points. The Bonferroni correction (α = 0.05/4) mentioned in the text widens the CIs to roughly precision [44%, 84%] and recall [51%, 89%]. This is a standard adjustment for multiple comparisons in operating-point selection, but the paper should report the adjusted CIs as primary or at least acknowledge the selection clearly in the abstract ("we select the 3-run union as the operating point; Bonferroni-adjusted 95% CIs are precision [44%, 84%], recall [51%, 89%]"). Without this, the CIs are artificially narrow.

- **3.3** Threats to validity are thoroughly discussed. Internal validity threats (single-run variance, post-hoc operating point, non-random 48-candidate set) are acknowledged. External validity threats (Weaviate yield-only, single LLM family, no cross-family robustness, no result correctness claims) are also acknowledged. The implementation-as-correct assumption is bounded: 15 merged-PR fixes suggest it holds often enough to be useful, but the paper correctly notes it cannot guarantee correctness and could wrongly falsify right documentation.

- **3.4 [minor, fixable]** RQ3 external validity is weak but acknowledged. The CouchDB and Elasticsearch probes (Section 7) executed successfully but found no silent-accept defects because mature non-VDBMS APIs validate more strictly. The portability claim ("structurally similar documentation regimes") is therefore supported only by pipeline execution, not by defect detection. The paper should explicitly frame this as a **portability probe** (does the pipeline run end-to-end on a non-VDBMS target?) rather than a generalization result ("CouchDB and Elasticsearch confirmed the pattern"). The current framing risks overstating external validity.

4. **Verifiability** — Adequate

- **4.1** The paper provides sufficient information to understand and replicate the core pipeline. The four-stage architecture (claim extraction, test generation, execution, confirmation) and the dev-reviewer's three-check falsification are clearly described (Section 3, Section 5). Figure 1 and Figure 3 illustrate the pipeline and dev-reviewer workflow. The abstract and body state that the full prompts, target versions, and per-token accounting will be released at a persistent URL upon acceptance.

- **4.2 [minor, fixable]** Artifact availability is declared ("we will release [the artifact] at a persistent URL upon acceptance") but not yet available. For Verifiability, the paper should either (a) provide a GitHub repo link to the current state (even if under the anonymity embargo) or (b) explicitly state that the artifact is under embargo and will be released upon camera-ready. The current "we will release...upon acceptance" is ambiguous about whether the code exists now or will be created later.

- **4.3** Link rot check: Table 1 citations (AGORA+, SATORI, MASTOR, VDBFuzz, AugmenTest, metamap, etc.) and Related Work citations appear to be properly formatted. No obviously broken links detected in the references section. The VDBFuzz citation could not be independently fetched via literature search, but the provided bibliographic entry is consistent with its description.

5. **Presentation** — Adequate

- **5.1 [minor, fixable]** Worst-case-bound precision led abstract. The abstract states "maintainer-adjudicated yield precision 68%, or 46% as a worst-case bound treating unadjudicated submissions as false positives." This is technically correct but misleading: the adjudicated precision (68%) is the primary metric, and the 46% worst-case bound should be a secondary sensitivity analysis. The abstract should lead with the adjudicated number and footnote the worst-case bound.

- **5.2 [minor, fixable]** Metric terminology: Section 6.2 uses "accuracy" but Table 5 and the ablation text report "65% accuracy" for the 3-run union. In a binary classification context (TP vs. not-TP), this is standard accuracy, but given the class imbalance (27 TP, 21 FP in the 48-candidate set), accuracy is less informative than precision/recall/F1. The paper should consistently use precision/recall/F1 for the main discussion and mention accuracy only parenthetically.

- **5.3 [minor, fixable]** Table 6 (bidirectional VDBFuzz probe versions) formatting: The table lists three Qdrant versions but the prose describes "controlled cases on v1.4.0 and v1.18.0 (n=1 each)." The table correctly shows v1.4.0 (VDBFuzz crash) and v1.18.0 (TestVDB #9045) as controlled cases, but the "n=1 each" notation is more transparent than the implicit "single case per version" reading. Consider clarifying as "n=1 for each controlled version."

- **5.4** Structure and readability are strong. The paper follows a logical flow: problem motivation → oracle exclusion argument → approach → false-positive diagnosis → dev-reviewer solution → evaluation (RQ1–RQ3) → limitations. Figures and tables are well-placed. The Related Work correctly positions the contribution relative to MASTOR, SATORI, AugmenTest, and self-preference bias literature.
---

## Reviewer 3: General Reviewer

**Overall Recommendation:** Weak Accept

### Summary
TestVDB targets documentation-implementation defects in Vector Database Management Systems (VDBMSs)—cases where a system silently accepts inputs that violate its API documentation. Because these boundaries are expressed in natural-language prose, deterministic oracles (crash detection, differential testing, metamorphic relations, property-based testing, REST-API spec-derived tools) cannot adjudicate accept/reject decisions, leaving an LLM as the practical oracle. The authors instantiate a four-stage pipeline (behavioral-claim extraction, test-script generation, sandboxed execution, defect confirmation) that uses LLMs to read documentation, generate tests, and adjudicate responses. Two failure modes produce false positives: hallucination in claim extraction and self-preference bias in judgment. A multi-perspective judging baseline raises precision but collapses recall, so the authors introduce a dev-reviewer agent that acts as a source-grounded falsifier, reproducing each candidate, cross-checking it against source, and trying to disprove it. TestVDB surfaced 107 candidate issues across three VDBMSs (Milvus, Qdrant, Weaviate); maintainers acknowledged 49 as true-positive defects (15 fixed via merged PR, 16 with open fix-PRs, 18 acknowledged but unfixed). On a controlled 48-candidate retrospective, the dev-reviewer reaches 67% precision and 74% recall (3-run ensemble), versus 37% recall without the source anchor. A bidirectional probe against VDBFuzz shows TestVDB reaches a crash-class defect by contract reasoning, while VDBFuzz misses a TestVDB silent-accept defect under its current templates.

### Core Strengths
- **S1:** Clear problem framing and systematic oracle exclusion argument — see 1.1, 2.1
- **S2:** Source-grounded falsification as a principled countermeasure to LLM false positives — see 3.1, 3.3
- **S3:** Substantial real-world validation (107 submissions, 49 maintainer-acknowledged defects) — see 4.1
- **S4:** Careful ablation and threat-model analysis — see 4.2, 4.3

### Core Weaknesses
- **W1:** Post-hoc operating-point selection without pre-registration — see 4.2
- **W2:** Single-backbone limitation (GLM-5.2 only) with weak cross-family generalization — see 4.2
- **W3:** Concrete external-validation case is too shallow to support portability claims — see 4.1, 5.1
- **W4:** Verifiability gaps in reproducibility details — see 5.1

### Detailed Assessment

#### 1. **Significance** — Adequate
- **1.1** The paper targets a real and costly problem: silent-accept defects in VDBMSs that corrupt query semantics without crashing (Section 1). The bug study cited (43% of VDBMS bugs from incorrect behavior, oracle definition as a key challenge) establishes practical relevance. The 49 maintainer-acknowledged defects across three production systems demonstrate the problem's prevalence. Documentation-implementation defects as a distinct class is a meaningful contribution that prior VDBMS testing work (VDBFuzz) misses by design.
- **1.2 [major, fixable]** The external validity claim is weakened by a single shallow non-VDBMS case. Section 6 probes CouchDB and Elasticsearch, each extracting only five claims and finding no silent-accept defects except limit=0/size=0 (both return empty result sets, not defects). This is presented as "probing method portability" rather than defect detection, but the portability claim in Section 1 ("transfer to documentation regimes beyond VDBMSs... claimed on structural grounds only") is not empirically substantiated. One case study that finds zero defects does not establish "transferability only to structurally similar documentation regimes." Either drop the generalization claim or add a second non-VDBMS case where defects are actually found.

#### 2. **Novelty** — Adequate (provisional)
- **2.1** The LLM-derived oracle for natural-language documentation is novel relative to prior REST-API oracle tools. Table 1 (oracle exclusion argument) clearly positions TestVDB against crash oracles (VDBFuzz), differential testing, metamorphic relations, property-based testing, and REST-API spec-derived tools (AGORA+, SATORI, MASTOR). The distinction is sound: prior tools rely on structured sources (OpenAPI, traces, source-as-oracle) and avoid ambiguous-prose documentation. TestVDB enters a regime others explicitly exclude.
- **2.2 [major, fixable]** The Related Work section does not cite or compare against specific fetched competitors beyond high-level descriptions. For AGORA+ (traces), SATORI (OpenAPI), and MASTOR (source-as-oracle), the paper describes their approaches generically but does not cite specific implementation details or empirical results from those papers. As a generalist without field context, I assess novelty as provisional—this contribution is novel relative to the paper's own characterization of prior work, but I cannot verify whether the characterization is complete or accurate without concrete competitor references. (Self-check: I have not surveyed the field, so this rating is provisional on the paper's Related Work being comprehensive.)

#### 3. **Soundness** — Adequate
- **3.1** The core claim—that source-grounded falsification lifts recall from 37% to 74% while maintaining precision—is supported by a controlled retrospective (Section 4.2). The 48-candidate maintainer-adjudicated set (27 TP, 21 FP) is a reasonable ground truth proxy. The ablation in Table 3 isolates source grounding's contribution: disabling it drops recall from 74% to 19%. The three-condition ablation (Table 4) shows source alone suppresses 75% of FPs while retaining all TPs. The 107-submission real-world yield (49 acknowledged TPs, 15 merged-PR fixes) demonstrates practical impact.
- **3.2 [major, fixable]** Post-hoc operating-point selection weakens the RQ2 claim. Table 3 reports four operating points (single-run band, 3-run union, 5-run union, 5-run majority), and the paper selects the 3-run union as the headline because "it sits at the knee of the precision-recall trade-off at modest reproducibility cost." This selection is not pre-registered; the Wilson CIs in the table do not account for selection across the four operating points. The paper acknowledges this ("post-hoc operating point justified by falsifier semantics") and provides a bootstrap validation that widens CIs to [53%, 83%] precision and [71%, 96%] recall, which does not change the qualitative claim. However, the primary claim should be based on a pre-specified operating point or a correction for multiple comparisons. The Bonferroni correction mentioned in the text (α=0.05/4) would widen CIs but is not applied in the table. Fix: Either pre-register the 3-run union as the primary analysis or statistically adjust for selection.
- **3.3 [minor, fixable]** The bidirectional VDBFuzz probe (Section 4.3) claims the systematic direction (VDBFuzz on v1.18.2, 26k requests, 0 of 14 TPs reached) is "the generalizable one" and the two controlled cases (v1.4.0, v1.18.0) are "n=1 each." However, the systematic direction uses VDBFuzz's default configuration; it is unclear whether alternative VDBFuzz configurations (different mutation strategies, longer runs) could reach silent-accept defects. The paper reads the reverse direction (VDBFuzz missing #9045) as a limitation of "current templates," which is fair, but the forward direction claim (VDBFuzz structurally cannot reach silent-accept defects) would be stronger with a brief exploration of whether any crash-oracle configuration could reach them via side effects (e.g., memory corruption from invalid input, assertion failures in debug builds).
- **3.4 [minor, fixable]** The implementation-as-correct assumption (Section 6) bounds the approach but is not empirically quantified. The paper states "We did not observe maintainer-rejected confirmed TPs where the documentation itself was wrong" but does not report the false-negative rate. A negative result (no such cases observed) is not evidence that the rate is low. If the dataset includes maintainer-rejected candidates, report how many were confirmed TPs by the dev-reviewer but rejected as documentation errors. This would bound the false-negative risk.

#### 4. **Verifiability** — Weak
- **4.1 [major, fixable]** Key reproducibility details are missing or incomplete. Section 3.5 ("LLM automation") states that "roughly half of the calls are dev-reviewer source-grounding steps" and provides approximate per-target call distribution (Table 2), but does not give:
  - Exact prompt templates for the 20 agents (only "full prompts... are in the artifact")
  - Sampling parameters (temperature, top-p, max tokens) for GLM-5.2
  - Per-stage token counts or cost breakdown beyond the "~$10 per target" aggregate
  - The exact version hashes for the three source clones (milvus-src v2.6.19, qdrant-src v1.18.2, weaviate-src v1.38.2 are given as version numbers, not git commits)
  
  The artifact promise ("full prompts, target versions, and per-token accounting... we will release at a persistent URL upon acceptance") is insufficient for verifiability. A reviewer should be able to assess whether the prompts are well-constructed and whether the sampling parameters are appropriate without waiting for post-publication artifact release. Fix: Move key prompt templates (at least for the contract-formalizer, attack agents, judge quartet, and dev-reviewer) and sampling parameters to an appendix or supplemental material.
- **4.2 [major, fixable]** The 48-candidate retrospective set is not fully described. The paper gives high-level breakdown (27 TP, 21 FP; Milvus 32, Qdrant 16) but does not list the specific candidates (issue IDs or claim descriptions) that comprise the retrospective. Without this, a reviewer cannot verify whether the set is representative or cherry-picked, nor can they independently assess the per-vendor breakdown (Milvus 69%/73%/80% vs. Qdrant 56%/50%/57%). The artifact should include the full retrospective catalog with claim descriptions and maintainer verdicts.
- **4.3 [minor, fixable]** The "full independent cross-model re-run on all 48 candidates" with DeepSeek, Qwen, and LongCat reports κ values but does not give the per-model precision/recall numbers or per-candidate verdict tables. Without these, the claim that "All three families recall fewer defects than GLM-5.2 (18--56% vs. 85%)" cannot be verified. The "85%" figure for GLM is also ambiguous: the table shows 74% recall for the 3-run union, but 85% is cited for the 5-run union—clarify which baseline is being compared against.
- **4.4** The paper explicitly states which results are maintainer-adjudicated (RQ1 yield, RQ2 retrospective) and which are estimated (RQ3 comparison with VDBFuzz, where the reverse direction is limited by current templates). The bidirectional probe design is clear: the systematic direction (VDBFuzz on v1.18.2) is the strong claim, and the controlled cases illustrate mechanisms on crash-class defects. The threat model in Section 4.4 honestly discusses internal validity (single-run variance, post-hoc selection), external validity (generalization limited to Weaviate yield-only, non-VDBMS transfer untested), and construct validity (single-backbone limitation). This is a model threat discussion.

#### 5. **Presentation** — Adequate
- **5.1** The paper is well-structured and clearly written. The four-stage pipeline (Figure 1) and dev-reviewer three-check falsification (Figure 2) are visually clear. The oracle exclusion argument (Table 1) effectively positions the contribution. The operating-point table (Table 3) is appropriately detailed with Wilson CIs and bootstrap validation notes.
- **5.2 [minor, fixable]** Minor inconsistencies and gaps:
  - Abstract states "maintainer-adjudicated yield precision 68%, or 46% as a worst-case bound" but Section 4.1 gives exact numbers as "68.1%" and "45.8%"—round to whole numbers in the abstract or use the precise numbers consistently.
  - Section 4.3 states "26,000 mutated requests" in prose but Table 5 writes "26{,}000"—use consistent formatting (26,000).
  - Section 6 claims "The extraction, probing, and falsification steps all port across non-VDBMS targets" but the CouchDB/Elasticsearch cases only demonstrate extraction and probing (falsification is not described for these targets).
  - The Related Work section cites AugmenTest and ChatAssert but does not describe their approaches or how TestVDB differs—either add a sentence or move these citations to a broader "LLM-as-judge" paragraph.
- **5.3 [minor, fixable]** The contribution list (Section 1) states "A bidirectional probe against VDBFuzz that explores complementary coverage" but the paper itself frames this as "how many defects detected by TestVDB can the existing crash-oracle approach reach, and vice versa?"—the "complementary coverage" framing in the contribution list slightly overstates the finding, which is primarily that VDBFuzz misses silent-accept defects under current templates. The bidirectional probe does show complementarity (TestVDB reaches a crash-class defect by contract reasoning), but the primary message is limitation of crash oracles, not full complementarity.

### Self-Check
- [x] Each Detailed-Assessment item points to a specific part of the paper (section/table/figure) and describes what the authors did there.
- [x] Criterion tiers are derived from the evidence listed.
- [x] Overall Recommendation matches the rubric (no Poor, no substance Weak, 1 fixable Weak → Weak Accept).
- [x] Each problem item is tagged [severity, fixability] consistent with criterion tier.
- [x] External-fact claims about prior work are flagged as provisional (2.2, Novelty assessed as provisional without field survey).
- [x] Core Strengths/Weaknesses summarize the most decision-relevant points and link to supporting N.M items.
- [x] No LaTeX comment remnants (% lines, \iffalse) in the source—read the stripped content only.

## Meta-Review

### Criterion Consensus

| Criterion | Reviewer 1 | Reviewer 2 | Reviewer 3 | Meta-Review |
|---|---|---|---|---|
| Significance | Adequate | Adequate | Adequate | **Adequate** |
| Novelty | Adequate | Adequate | Adequate *(prov)* | **Adequate** |
| Soundness | Adequate | Adequate | Adequate | **Adequate** |
| Verifiability | Adequate | Adequate | Weak | **Adequate** *(Mixed)* |
| Presentation | Adequate | Adequate | Adequate | **Adequate** |
| **Recommendation** | **Weak Accept** | **Weak Accept** | **Weak Accept** | **ACCEPT** |

### Meta Recommendation
**ACCEPT**

三位 expertise reviewer 一致 Weak Accept → unanimous shortcut **ACCEPT**。无 consensus Poor，无 substance 准则 consensus Weak。**Presentation consensus 从 v4 的 [Mixed]（R1 Weak）升为全 Adequate**——v4 修订（Table 5 caption 定义 per-run band / any-confirmed / majority / Wilson-vs-bootstrap 关系）直接修复了 R1 v4 的 Presentation Weak 驱动因素，v5 验证达成。Verifiability 新现 [Mixed]（R3 Weak）：R3 要求 prompts / sampling parameters / 48-candidate catalog 移入 appendix（不只 artifact promise），并指出 §6.2 "18–56% vs. 85%" 比较口径 ambiguous（85% 是 5-run union，但 κ 是 vs GLM single-run）——这是 v5 新抓的 fixable 点，非致命。

核心 framing **第五次确认站得住**：R1 经 MASTOR/SATORI cache 核实 delta 准确 + AugmenTest（arXiv:2501.17461）positioning 正确（v4 §2 前置起效）；R2 fetch 5 篇（含 haldar25）核实 characterization；R3 internal coherence check 确认 abstract 68%/46% 与 §6.1 一致、§6.3 systematic framing 成立、Table 5 定义一致——**v4 修订被独立 reviewer 确认生效**。

3 个 [both] major inherent limitation（post-hoc / cross-family / external validation）仍是被所有 reviewer 共识但文字已尽的 residual；v5 新增 Verifiability fixable 项（prompts appendix + 85% 口径澄清）。

### Priority Revisions
1. **Verifiability: prompts / sampling / 48-candidate catalog（R3 4.1/4.2）[major, fixable]** — v5 新抓。论文承诺 artifact upon acceptance，但 R3 要求关键 prompts（contract-formalizer / attack / judge / dev-reviewer）+ sampling 参数 + 48-candidate issue ID 移入 appendix 供 review-time 核查。这是修订周期可解的（appendix 补），非 inherent。
2. **§6.2 cross-model "85%" 口径澄清（R3 4.3）[minor, fixable]** — "18–56% vs. 85%" 中 85% 是 GLM 5-run union recall，但 κ 比较的是 vs GLM single-run；比较 basis 应显式（要么都 single-run，要么注明 85% = GLM multi-run upper）。
3. **Post-hoc operating-point CI（R1 3.2, R2 W1, R3 3.2 + 态度共识）[major, fixable→inherent]** — 6 reviewer 共识。已有 Bonferroni + bootstrap，residual 需 pre-registration（inherent）。
4. **External validation（R1 W4, R2 W3, R3 1.2 + 态度）[major, fixable→inherent]** — CouchDB/ES portability only。inherent（需 non-VDBMS defect case）。
5. **Cross-family / single-backbone（R1 W1, R3 W2 + 态度）[major, fixable→inherent]** — inherent（需更多 family）。
6. **Worst-case-bound framing（R1 W3/5.1）[minor, fixable]** — abstract 应 lead with adjudicated 68%，worst-case 46% 作 sensitivity。v4 加了 68%/46%，但 R1 认为仍偏保守。

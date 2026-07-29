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

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
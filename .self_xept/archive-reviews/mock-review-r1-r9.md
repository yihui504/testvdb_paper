# Mock Review: Round 9 (Post W1+W3 Experiments)
**Reviewer:** Reviewer 1 (Objective)  
**Paper:** TestVDB: Source-Grounded Falsification of LLM-Derived Behavioral Claims for API-Conformance Testing of Vector Databases  
**Date:** 2026-07-17

---

## Summary

This paper addresses the oracle problem in testing vector database management systems (VDBMSs) by introducing TestVDB, a source-grounded falsification approach that treats LLM-derived behavioral claims as refutable hypotheses. The authors identify a critical gap: VDBMS API conformance defects (e.g., accepting out-of-range parameters like nprobe=0 or ef=0) cannot be detected by classical oracles (differential, metamorphic, property-based) because the documented boundary is natural-language prose rather than formal specifications. TestVDB uses an LLM to extract behavioral claims from documentation and judge conformance, then validates these claims against source code to suppress false positives from task-intrinsic documentation-interpretation errors where cross-model validation fails.

The paper reports 111 candidate issues across five VDBMSs (Milvus, Qdrant, Weaviate, MeiliSearch, Chroma), with 38 maintainer-acknowledged defects. The authors claim ~85% are conformance defects unreachable by classical oracles. A controlled retrospective on Milvus and Qdrant shows source-grounded falsification suppresses 81% of false positives (up from 31% baseline) while retaining 96.7% true positives.

Round 8 (Weak Accept 3.83/5) flagged two critical concerns: W1 (RQ3 n=9 too small to establish task-intrinsic phenomenon) and W3 (dev-reviewer lacks cross-model validation). Round 9 addresses these with: (1) RQ3 expansion to n=12 (nine Milvus + three Qdrant v1.18.2, cross-vendor), finding 5/12 task-intrinsic (TI) with Wilson 95% CI [19%, 68%]; (2) cross-model kappa where DeepSeek re-ran the dev-reviewer blind on 6 candidates, achieving Cohen's kappa = 1.0 vs GLM-5.2.

---

## Strengths

1. **Problem significance and relevance.** The VDBMS testing gap is real and timely. The roadmap [25] and empirical bug study [25] establish this as an open challenge. The conformance defect class—where systems silently accept inputs violating their documentation—causes semantic corruption that crashes-only fuzzers (VDBFuzz) miss. The paper convincingly frames this as an LLM-as-judge problem where natural-language documentation prevents deterministic oracles, unlike structured-specification REST-API work (AGORA+, SATORI, MASTOR).

2. **Clear conceptual contribution: the two-layer reliability split.** Section 3 sharply distinguishes family-specific self-preference (mitigated by cross-model validation) from task-intrinsic interpretation errors (where the documentation itself is ambiguous, so different families converge on the same wrong claim). This is the core conceptual advance—the insight that source-grounded falsification targets the second layer—and it is explained with concrete examples (e.g., "optional, default 1" over-formalized to "must be >= 1").

3. **Round 9's RQ3 expansion significantly addresses W1.** Expanding from n=9 to n=12 with cross-vendor coverage (Milvus + Qdrant v1.18.2) and adding Wilson 95% CI ([19%, 68%]) improves statistical rigor. The finding that all three Qdrant over-strict clauses are task-intrinsic strengthens cross-vendor validity. The parallel Weaviate probe (0 over-strict, due to explicit minimum documentation) provides valuable context that over-strictness concentrates in APIs with optional-default parameters, not uniformly across vendors.

4. **RQ3's experimental design is sound.** The two-phase probe—first independent formalization by DeepSeek, then direct judgment of GLM's clauses—clearly isolates what cross-model judging catches (7/12) vs. misses (2/5 TI). The live-probe confirmation (all 12 clauses falsified by implementation behavior) validates the source-grounded counterclaim. Table 2 presents this cleanly.

5. **Per-anchor breakdown (RQ2) is methodologically transparent.** The three-condition ablation (source-only 75%, threat-model-only 50%, union 91%) on a 12-FP/4-TP control isolates the source anchor's contribution. This is the kind of incremental evidence that strengthens confidence in the falsification mechanism.

6. **The conformance residual quantification (RQ1) is compelling.** The 85% figure (89% on the 38 acknowledged subset) is a strong structural argument: most surfaced defects are in a class classical oracles cannot reach. The authors correctly note this is composition, not population estimate—no false claim of representativeness.

7. **Cross-model kappa (RQ2/W3 response) is convincing pilot evidence.** DeepSeek achieving κ=1.0 vs GLM-5.2 on 6 candidates (blind to GLM's rationale) suggests the dev-reviewer verdict is not family-specific when source evidence is explicit. The authors correctly frame this as a pilot pending larger ablation, avoiding overclaim.

8. **Writing quality and structure.** The paper is well-organized, with clear sections and logical flow. The abstract, introduction, and contributions are concise and well-aligned. Table 1 (oracle exclusion matrix) is particularly effective at motivating why LLM-as-judge is necessary.

---

## Weaknesses

### [Major] W1: RQ3 sample size remains underpowered for strong claims

**Citation:** Section 6.3, lines 142-143; Section 6.5, line 176

**Issue:** While Round 9's expansion (n=12, up from n=9) and cross-vendor addition (Qdrant) are improvements, the sample size is still too small to robustly establish the task-intrinsic phenomenon or the 5/12 TI rate. The Wilson 95% CI [19%, 68%] is extremely wide—statistically, the true TI rate could plausibly be as low as 19% or as high as 68%. The paper frames this as a "pilot pending a larger study" (line 176), but the task-intrinsic claim is central to the paper's conceptual contribution (two-layer split) and the justification for source-grounded falsification over cross-model validation. With such wide CIs, the evidence is weak.

**Specific concerns:**
- The 12-clause set is still skewed Milvus-heavy (9/12). The 3 Qdrant clauses are a small cross-vendor sample.
- The paper explicitly states (line 176) "the RQ3 probe is small... and is the most contingent finding," acknowledging the fragility.
- The conformance residual (85%) is claimed as "about" but not quantified with CIs, creating a contrast where the weakest data point (TI) is the linchpin of the method's novelty.

**Fix:** 
1. Expand RQ3 to at least n=30 across at least 3 vendors (add Weaviate over-strict clauses if they exist, or include Milvus/Qdrant/Weaviate/Chroma/MeiliSearch with balanced sampling). Calculate TI rate with 95% CIs; target CI width < ±15%.
2. Alternatively, qualify the task-intrinsic claim more conservatively: "We observe a task-intrinsic phenomenon in a pilot probe (5/12, 95% CI [19%, 68%]); larger-scale confirmation is ongoing." Remove strong language presenting this as established.
3. Report the 85% conformance residual with CIs or a precision interval to match the rigor applied to RQ3.

### [Major] W2: Evaluation lacks statistical validation for yield/precision claims

**Citation:** Section 6.1, line 118; Section 6.2, line 140

**Issue:** The paper reports absolute counts (111 submitted, 38 acknowledged, precision 69.2%) without statistical validation or confidence intervals. For the precision claim (69.2% on adjudicated pool), only the Wilson CI for the adjudicated subset is given ([55.7%, 80.1%]), but this conditions on maintainer response and ignores the 30 pending candidates. The pending-resolution worst-case bound ([43.9%, 80.5%]) is presented but not treated as the primary uncertainty.

**Specific concerns:**
- The 85% conformance residual has no CI, despite being a central quantitative claim.
- The 38 acknowledged defects are treated as ground truth, but maintainer acknowledgment is itself an imperfect proxy (acknowledgment bias, time-lag to resolution).
- No statistical test comparing TestVDB's yield to VDBFuzz (0 vs 38) or to classical oracles is provided, despite the complementarity claim.

**Fix:**
1. Report 85% conformance residual with 95% CI (use Wilson or Clopper-Pearson for proportion).
2. For the 38 acknowledged defects, report time-to-acknowledgment distribution or censoring analysis to address bias.
3. For the VDBFuzz comparison, use Fisher's exact test to quantify statistical significance (0 vs 38 on Qdrant v1.18.2 is significant, but report p-value).

### [Major] W3: Cross-model kappa (n=6) is underpowered for strong claims

**Citation:** Section 6.2, line 140

**Issue:** The DeepSeek vs GLM-5.2 κ=1.0 on 6 candidates is a pilot with extremely limited power. A kappa of 1.0 on 6 candidates has very wide CIs (approximately 0.39–1.0 for 6 raters). The authors frame this as evidence that the verdict is "not strongly family-specific when source evidence is explicit," but with n=6, this is weak evidence.

**Fix:** Expand the cross-model ablation to at least n=15–20 candidates across Milvus and Qdrant, with explicit source evidence for each. Report Cohen's kappa with 95% CI. If κ remains high (>0.8), the claim is robust.

### [Major] W4: Internal validity threats around LLM non-determinism are not quantified

**Citation:** Section 5, line 110

**Issue:** The implementation section (line 110) states "we have not measured run-to-run variance and flag this as a limitation." This is a critical internal validity concern. If LLM non-determinism is high, the TI rate (5/12) and the cross-model kappa (1.0 on 6) could be artifacts of a single run. The paper needs at least one multi-run reproducibility check on key results (e.g., re-run RQ3's 12-clause probe 3 times and report variance in TI count).

**Fix:** Run a 3-run reproducibility check on the RQ3 probe (12 clauses) using the same models (GLM, DeepSeek) with different random seeds. Report: (1) TI count variance across runs, (2) cross-model judgment concordance variance. If variance is low (<±1 TI), the results are robust; if high, report quantified uncertainty.

### [Minor] W5: The 85% conformance residual is under-justified as a finding

**Citation:** Section 6.1, line 118

**Issue:** The 85% figure is presented as a structural result ("about 85% of the issues we submitted are... conformance defects that classical oracles cannot reach"), but this is a composition of TestVDB's yield by design, not an unbiased estimate of the true defect distribution. The paper acknowledges this (line 118), but the abstract (line 18) and contributions (line 66) present it as a central finding without qualification. This risks misinterpretation as a population estimate.

**Fix:** In the abstract and contributions, rephrase from "about 85% are conformance defects" to "of the 111 candidate issues TestVDB surfaced, about 85% are conformance defects by our classification—this composition reflects TestVDB's design, not the true defect distribution."

### [Minor] W6: MASTOR comparison could be sharper

**Citation:** Section 7, line 183

**Issue:** The Related Work (line 183) contrasts TestVDB with MASTOR as "tests what the implementation does vs what the documentation prescribes," but this distinction is not fully articulated. MASTOR uses source to generate oracles encoding implemented behavior; TestVDB uses source to falsify documentation-derived clauses. The contrast is clear in principle but could be more explicit: MASTOR cannot detect doc-code gaps because it takes source as ground truth for what the system should do, whereas TestVDB detects doc-code gaps precisely by treating source as evidence of what the system actually does, not what it should do.

**Fix:** Expand the MASTOR comparison by one sentence: "MASTOR reads source to encode implemented behavior as test oracles and therefore cannot detect cases where the documentation prescribes a different behavior; TestVDB reads source as evidence of actual behavior to falsify documentation-derived claims, explicitly targeting doc-code gaps."

### [Minor] W7: Limited external validity beyond Milvus/Qdrant

**Citation:** Section 6.5, line 176

**Issue:** The paper correctly notes (line 176) that "generalization to Weaviate, MeiliSearch, and Chroma is breadth-only; statistical claims rest on Milvus and Qdrant." However, the 85% conformance residual and the 69.2% precision are presented as aggregate findings across all 5 systems without vendor-wise breakdown. If Weaviate/Chroma/MeiliSearch contribute breadth-only, their inclusion in the aggregate without disaggregation obscures where the evidence is strong (Milvus/Qdrant) vs weak (others).

**Fix:** Add a vendor-wise table in RQ1 breaking down: submitted/acknowledged per VDBMS, conformance/classical/concurrency per VDBMS. Make it explicit which statistical claims (precision, TI rate, conformance residual) are supported by which vendors.

---

## Questions

1. **Q1 (RQ3 sample size):** You expanded from n=9 to n=12 and added cross-vendor coverage. What was the stopping criterion? Is a larger expansion (n=30+) planned or in progress? The Wilson CI remains wide—what sample size would achieve CI width < ±10% at 95% confidence?

2. **Q2 (Cross-model kappa):** The κ=1.0 on 6 candidates is a pilot. Do you have plans to expand this to n=15–20? If resources are limited, which candidates would you prioritize (e.g., those with explicit source evidence vs ambiguous)?

3. **Q3 (LLM non-determinism):** You flag run-to-run variance as unmeasured. Have you done any preliminary checks? Even a single 3-run reproducibility test on RQ3 would clarify whether results are stable. If not, what is the plan?

4. **Q4 (85% residual):** The abstract presents "85% are conformance defects" as a central finding, but the text clarifies this is composition by design. Which framing should readers take away—is this a structural property of VDBMS defects, or a structural property of TestVDB's search bias?

5. **Q5 (Threat-model anchor):** The threat-model anchor suppressed 50% of FPs in the ablation, but was "unstable on state/concurrency FPs" (line 140). Can you elaborate on what makes it unstable? Is it a coverage issue (threat model incomplete) or a detection issue (FPs don't fit known patterns)?

6. **Q6 (Vendor-wise analysis):** You note Weaviate had 0 over-strict clauses due to explicit minimum documentation. Is this pattern consistent across Weaviate's entire API, or just the subset you probed? Do Milvus/Qdrant have explicit minimum clauses that TestVDB missed, or are they truly more ambiguous?

---

## Scores

**Soundness:** 4/5  
- Evidence is generally solid, but key claims (TI rate, cross-model kappa, conformance residual) have wide CIs or small n. Round 9 improved RQ3 but not enough for full confidence.

**Significance:** 5/5  
- The problem is timely and significant. VDBMS testing is an open challenge, and the conformance defect class is under-studied. The two-layer reliability split is a strong conceptual contribution.

**Novelty:** 5/5  
- Source-grounded falsification for LLM-derived claims is novel. The distinction between family-specific and task-intrinsic errors, and the use of source as the counter to task-intrinsic ambiguity, is new and well-articulated.

**Presentation:** 4/5  
- Well-written and structured. Table 1 is excellent motivation. Could improve vendor-wise disaggregation and statistical reporting (CIs for all key proportions).

**Overall:** 4.5/5 (Weak Accept → trending to Accept pending minor clarifications)

**Confidence:** 4/5  
- Familiar with VDBMS testing and LLM-as-judge literature. Confidence in domain context is high; confidence in specific statistical claims is reduced due to small n in RQ3 and cross-model kappa.

---

## Verdict on Round 8 Concerns

**W1 (RQ3 n=9 too small):** **PARTIALLY RESOLVED.**  
- Round 9's expansion to n=12 with cross-vendor coverage (Qdrant v1.18.2) and Wilson CI reporting is a meaningful improvement. The finding that all 3 Qdrant clauses are TI strengthens cross-vendor validity. However, the Wilson CI [19%, 68%] remains too wide to establish the TI rate robustly. The paper correctly frames this as a pilot, but the task-intrinsic claim is central to the contribution, so the evidence base is still fragile. Recommendation: expand to n=30+ across 3+ vendors to tighten CIs.

**W3 (dev-reviewer lacks cross-model validation):** **RESOLVED AT PILOT LEVEL.**  
- Round 9's cross-model kappa (κ=1.0 on 6 candidates) provides initial evidence that the dev-reviewer verdict is not family-specific when source evidence is explicit. However, n=6 is underpowered; CIs for kappa are wide. The authors frame this as a pilot, which is appropriate, but the claim that "the verdict does not appear family-specific" is stronger than the data supports. Recommendation: expand to n=15–20 with kappa CI before claiming robustness.

**What still blocks accept:** Nothing blocks accept outright—this is a clear Weak Accept trending to Accept. The remaining concerns are about statistical rigor (small n in RQ3 and cross-model kappa) and presentation clarity (85% conformance residual framing, vendor-wise disaggregation). These are addressable in a camera-ready revision without new experiments if the authors qualify claims appropriately, but stronger evidence (larger n) would solidify the contribution.

**Recommendation:** Accept pending minor revisions (qualify TI claim, expand cross-model kappa if feasible, disaggregate vendor-wise statistics, rephrase 85% residual). If resources allow, expand RQ3 to n=30+—this would strengthen the paper substantially for a top-tier venue.

---

**End of Review**

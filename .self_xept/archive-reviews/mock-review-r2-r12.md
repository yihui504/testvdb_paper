# Mock Review: Reviewer 2 (Critical) - Round 12

## Summary

TestVDB addresses the oracle problem for API conformance defects in Vector Database Management Systems by proposing source-grounded falsification of LLM-derived behavioral claims. The round-12 revision makes substantial progress on my round-11 concerns. The task-intrinsic error probe has expanded from n=12 to n=29 across three subtypes (12 over-strict parameters, 4 by-design behaviors, 13 explicit-bound negatives), with the pooled task-intrinsic rate at 9/16 (Wilson 95% CI [33%, 77%])—still underpowered but materially improved from the round-11 baseline of 5/12. The within-vendor contrast now includes a specificity check showing 0/13 over-formalization on explicit-bound parameters versus 9/16 on optional-default APIs, providing stronger evidence that documentation style rather than vendor identity is the driver. Cross-model validation for the dev-reviewer has expanded from n=6 to n=20 (Cohen's κ=1.0) across five subtypes, addressing the single-family concern. However, the mechanism remains correlative rather than causal, and the statistical support for the central task-intrinsic claim, while improved, still falls short of the power needed for strong quantitative assertions. The paper has evolved from "promising but methodologically weak" to "solid contribution with acknowledged limitations."

## Strengths

1. **Clear problem articulation.** The VDBMS conformance defect class is well-defined with concrete examples (nprobe=0, ef=0, negative score thresholds). Table 1 effectively maps each oracle family to the defect subset it cannot reach, establishing the residual that motivates the LLM-as-oracle setting.

2. **Conceptual contribution: two-layer error model.** The distinction between family-specific self-preference and task-intrinsic documentation-interpretation errors is insightful and grounded in a plausible mechanism. Section 4 clearly articulates why cross-model validation covers the former but not the latter, motivating source-grounded falsification as the necessary countermeasure.

3. **Controlled ablation design.** The precision ablation (single-LLM 25.5% → single source cycle 45.6% → full pipeline 69.2%) isolates incremental contributions and shows that each component adds value, not just the end-to-end system.

4. **Statistical transparency.** The paper reports Wilson binomial confidence intervals for precision (69.2%, 95% CI [55.7%, 80.1%]) and the pending-resolution worst-case bound ([43.9%, 80.5%]), which is more rigorous than point estimates alone. The task-intrinsic rate now includes confidence intervals for both the unpooled (5/12: [19%, 68%]) and pooled (9/16: [33%, 77%]) estimates.

5. **Honest limitation statements.** Section 8 explicitly bounds the approach (requires source, treats implementation as correct) and the threats section acknowledges that statistical claims rest on Milvus and Qdrant, showing commendable candor.

6. **Round-12 progress on the specificity check (new).** The addition of thirteen explicit-bound parameters (Qdrant's shard_number, replication_factor, write_consistency_factor, full_scan_threshold; Weaviate's ef, dynamicEfMin, dynamicEfMax, efConstruction, maxConnections, vectorIndexType, replicationConfig.factor; Milvus's dimension, num_partitions) showing 0/13 over-formalization provides a critical specificity check that confirms the task-intrinsic phenomenon concentrates in ambiguous optional-default APIs and is absent where documentation states explicit bounds. This materially strengthens the within-vendor contrast.

7. **Round-12 progress on cross-model validation (expanded).** The dev-reviewer cross-model check has expanded from n=6 to n=20 (Cohen's κ=1.0) spanning input-validation, upsert-semantics, idempotent-drop, correct-reject, and dynamic-field subtypes, substantially addressing my round-11 concern that the single-family results might be a GLM-specific artifact.

## Weaknesses

### **[Major] 1. The mechanism remains correlative, not causal.**

**Location:** Section 7, RQ3, lines 145-150

**Issue:** The round-12 addition of a specificity check (0/13 on explicit bounds) strengthens the within-vendor contrast, but the mechanism remains correlative. The paper observes that optional-default parameters are over-formalized while explicit-minimum parameters are not, and proposes "documentation style as the driver." However, this is still a correlation, not a demonstrated causal mechanism. Alternative explanations remain unruled out: (a) search and collection parameters may be implemented by different teams with different testing cultures, (b) optional-default parameters may be harder to test with boundary values because the default logic is more complex, (c) the three over-strict search parameters may share a common code path that treats 0 as a sentinel value, while collection parameters reject 0 via separate validation. The specificity check rules out the possibility that the phenomenon generalizes to all parameters, but it does not isolate documentation style as the causal driver.

**Fix:** The falsifiable prediction (optional-default APIs are over-formalization candidates; explicit-minimum APIs are not) is good, but the paper should soften the mechanism claim from "documentation style is the driver" to "documentation style correlates with over-formalization" and acknowledge that team structure, implementation complexity, or testing culture could be confounders. The current presentation (line 145: "isolates documentation style as the driver rather than the vendor") overstates the evidence.

### **[Major] 2. Insufficient statistical support for the central task-intrinsic error claim (RQ3).**

**Location:** Section 7, RQ3, lines 145-150; Abstract, line 20

**Issue:** The core novelty claim—that source-grounded falsification resolves task-intrinsic documentation-interpretation errors that cross-model validation cannot—rests on a probe of twenty-nine clauses, but the task-intrinsic subset is only sixteen (nine over-strict parameters pooled with four by-design behaviors, excluding the thirteen explicit-bound negatives). The paper reports a pooled task-intrinsic rate of 9/16 (Wilson [33%, 77%]), which is better than the round-11 baseline of 5/12 ([19%, 68%]), but this confidence interval remains too wide to support strong claims about prevalence or generality. The abstract still presents the task-intrinsic phenomenon as a supported central contribution when the statistical support remains exploratory. The paper acknowledges that "the over-strict subset remains the most contingent finding" in the threats section, but this caution is not reflected in the abstract's presentation strength.

**Fix:** Either (a) scale the probe to a statistically powered sample (n≥50 task-intrinsic clauses across multiple VDBMSs) or (b) reframe RQ3 as exploratory evidence and remove the "task-intrinsic" terminology from the abstract until confirmed. The current improved-but-still-underpowered support (CI width 44 percentage points) does not justify the abstract's presentation of the task-intrinsic layer as a validated contribution.

### **[Major] 3. Missing full cross-model validation for the source-grounded falsification verdicts.**

**Location:** Section 7, RQ2, line 142; Section 7, threats to validity, line 182

**Issue:** The round-12 expansion of cross-model checks from n=6 to n=20 (Cohen's κ=1.0) is a meaningful improvement and partially addresses my round-11 concern. However, twenty candidates is still a fraction of the full 54-candidate adjudicated set. Without a consistency check on the full set, we cannot rule out that the 81% FP suppression figure is partially a GLM-specific artifact. The threats section states that "all source-anchor results use a single model family (GLM-5.2)" and notes the cross-model check as suggestive evidence, but this leaves the core quantitative claim (81% FP suppression) resting primarily on single-family validation.

**Fix:** Run a cross-model consistency check on the full 54 adjudicated candidates: have DeepSeek perform the dev-reviewer's source-grounded falsification on all 54 and report agreement rate (Cohen's κ). The current n=20 check spans five subtypes but does not cover the full evidence base for the 81% claim. If scaling to 54 is infeasible, soften the 81% claim to "on GLM-5.2, the source anchor suppresses 81%" and acknowledge that cross-model consistency is preliminary.

### **[Major] 4. The "85% conformance residual" is still presented without sufficient qualification.**

**Location:** Abstract, line 20; Section 7, RQ1, line 120

**Issue:** The abstract states "about 85% are, by our classification, conformance defects that classical oracles cannot reach" and presents this as a central finding. Round-12 adds the clarification "this is the composition of our findings, not a population estimate" in the abstract, which is an improvement over round-11. However, the presentation still reads as a population claim in RQ1 ("about 85% of the issues we submitted are, by this classification, conformance defects"), when it is actually a sample-composition figure. Without capture-recapture estimation or an unbiased defect sample, the 85% figure cannot support general claims about the prevalence of conformance defects in VDBMSs.

**Fix:** The round-12 abstract clarification ("about 85% of the issues we submitted are, by our classification, conformance defects") is better, but RQ1 should be reworded to match: "Of the 111 issues TestVDB surfaced, 85% are, by our classification, conformance defects that classical oracles cannot reach." Avoid language that implies this proportion generalizes to all VDBMS defects.

### **[Major] 5. Incomplete ablation of the dev-reviewer's three anchors.**

**Location:** Section 5, line 108-109; Section 7, RQ2, line 140

**Issue:** The dev-reviewer applies three anchors (clean reproduction, source-grounded falsification, threat-model cross-check), but the paper claims "the source anchor suppresses 81% of false positives (up from 31%)" without clarifying what "without it" means. Round-12 provides per-anchor breakdown in the artifact, but the main text still does not state the baseline explicitly. Is the 31% baseline with no anchors at all, or with only the clean-reproduction anchor? The threat-model anchor is described as "unstable on state/concurrency FPs" but never fully described or ablated in the main text.

**Fix:** State the baseline explicitly in RQ2: "up from 31% when only the clean-reproduction anchor is applied" (or whatever the baseline actually was). Explain the threat-model anchor in the main text and report its ablation contribution, not just in the artifact.

### **[Minor] 6. Missing statistical test for the 81% vs. 31% FP suppression comparison.**

**Location:** Section 7, RQ2, line 140

**Issue:** The paper claims "the source anchor suppresses 81% of false positives (up from 31%)" but does not report whether this difference is statistically significant. With n=54 adjudicated candidates, a McNemar's test for paired binary outcomes or Fisher's exact test could assess whether the source anchor adds predictive power beyond the other anchors.

**Fix:** Perform a statistical test (McNemar's or Fisher's exact) on the 2×2 table (source anchor present/absent × FP/TP) and report the p-value. If p < 0.05, state that the improvement is significant; if not, soften the claim to "suggestive improvement."

### **[Minor] 7. Incomplete comparison with recent LLM-based oracle work.**

**Location:** Section 9, lines 189-196

**Issue:** The paper compares against AGORA+, SATORI, MASTOR, Toradocu, Doc2OracLL, ChatAssert, and Testora, but the critical distinction—source vs. runtime verification—is under-explored. ChatAssert uses compilation and execution feedback; Testora uses differential execution. Both rely on runtime behavior, which cannot distinguish between a correct implementation and a bug that coincidentally satisfies the LLM's oracle. The related work section does not explicitly state whether these tools would or would not detect the task-intrinsic errors on the sixteen-clause probe, leaving readers uncertain whether TestVDB is strictly better or merely better-validated.

**Fix:** Add a sentence clarifying that ChatAssert, Testora, and Toradocu rely on runtime feedback and therefore cannot distinguish correct implementations from bugs that happen to satisfy the LLM's interpretation. Explicitly state that the sixteen-clause probe is, by definition, inaccessible to runtime-only methods.

### **[Minor] 8. Missing reproducibility details for LLM sampling.**

**Location:** Section 6, line 112

**Issue:** The paper states agents use "the runtime's default sampling" but does not specify temperature, top-p, or whether random seeds are fixed. For reproducibility and to rule out the possibility that the 81% FP suppression is sampling-dependent, the implementation section should report the sampling parameters and whether results vary across multiple runs.

**Fix:** Report temperature and top-p values for the LLM backbone, and run a small reproducibility check: execute the full pipeline on one VDBMS with three different random seeds and report variance. If variance is low, note this as evidence of stability; if high, report the range and flag reproducibility as a limitation.

### **[Minor] 9. Unclear boundary between model-free invariant oracle and LLM pipeline.**

**Location:** Section 7, RQ4, lines 178-180

**Issue:** The model-free invariant subclass (COSINE bounds, index completeness) is presented as separately detecting mathematical-invariant violations with no LLM involvement, but it is unclear whether these findings are included in the 111 total submissions or counted separately. If included, they inflate the denominator without leveraging TestVDB's core novelty. If separate, the paper should report the count explicitly.

**Fix:** Explicitly state how many of the 111 submissions come from the model-free invariant subclass versus the LLM pipeline. Break down the 38 acknowledged defects by source (LLM vs. model-free) and clarify whether the 69.2% precision applies to the full set or only to LLM-derived candidates.

### **[Minor] 10. Limited external validity beyond two VDBMSs.**

**Location:** Section 7, threats to validity, line 182

**Issue:** The paper correctly notes that "statistical claims rest on Milvus and Qdrant," and this narrow scope undermines generalizability. Weaviate (30 submissions, 3 acknowledged), MeiliSearch (3, 0), and Chroma (1, 0) provide breadth but not statistical weight. The abstract and introduction do not explicitly state that the quantitative results (precision, FP suppression, task-intrinsic catch rate) are primarily validated on two systems.

**Fix:** Qualify all quantitative claims in the abstract and introduction with "on Milvus and Qdrant" or similar. For example: "A controlled retrospective on Milvus and Qdrant shows the source anchor suppresses 81% of false positives." Avoid presenting these figures as universally applicable to all five VDBMSs.

## Questions for Authors

1. **On the mechanism:** You propose that documentation style (optional default vs. explicit minimum) drives over-formalization. Have you ruled out alternative explanations? For example, are the search and collection parameters implemented by different teams? Do they share test coverage or code paths that could explain the difference? How would you falsify the documentation-style hypothesis itself?

2. **On the task-intrinsic error probe:** The pooled estimate (9/16, Wilson [33%, 77%]) is an improvement over round-11, but the confidence interval remains wide. What stopping rule determined the twenty-nine-clause sample? If this is meant to be exploratory, why is it presented as a supported contribution in the abstract? Do you have plans to scale this probe to n≥50, and what would constitute adequate statistical power?

3. **On the 81% FP suppression claim:** To what extent does this figure depend on GLM-5.2's specific behavior when reading source code? The round-12 expansion to n=20 cross-model candidates is progress, but why not run DeepSeek on the full 54-candidate adjudicated set to fully validate that the 81% figure is not a GLM-specific artifact?

4. **On the 85% conformance residual:** You acknowledge this is the composition of your findings, not a population estimate. Do you have any evidence about whether conformance defects are equally prevalent in practice, or is TestVDB's focus on conformance purely a design choice that may miss other defect classes?

## Scores

- **Soundness:** 4/5 (Good). **IMPROVED from round-11 (3/5).** The method is conceptually sound and the ablations are well-designed. The round-12 addition of a specificity check (0/13 on explicit bounds) materially strengthens the within-vendor contrast, and the expansion of cross-model validation from n=6 to n=20 partially addresses the single-family concern. However, the mechanism remains correlative rather than causal, and the core task-intrinsic claim still rests on a probe (n=16) that is underpowered for strong quantitative assertions. The lack of full cross-model validation on the 54-candidate adjudicated set persists.

- **Significance:** 4/5 (Good). **IMPROVED from round-11 (3/5).** The problem setting is real and the two-layer error model is a meaningful conceptual contribution. The round-12 falsifiable prediction and specificity check strengthen the theoretical contribution by providing a testable hypothesis with empirical support. The practical impact is clearer with the expanded evidence base, though the 85% residual figure is still presented without sufficient qualification and the task-intrinsic claim remains exploratory.

- **Novelty:** 4/5 (Good). **UNCHANGED from round-11.** The source-grounded falsification approach is a genuine advance over prior LLM-based oracle work, which relies on runtime feedback or structured specifications. The distinction between family-specific and task-intrinsic errors is novel and well-motivated. The round-12 addition of a specificity check strengthens the novelty by showing the phenomenon concentrates in ambiguous APIs and is absent where documentation is explicit.

- **Presentation:** 4/5 (Good). **IMPROVED from round-11 (3/5).** The paper is clearly written, with excellent use of concrete examples and a strong table mapping oracle families to defect subsets. The round-12 addition of the specificity check and expanded cross-model validation is well-integrated into RQ3. The abstract now includes the "composition of our findings" clarification, which is an improvement, but it still overstates the statistical support for the task-intrinsic claim.

- **Overall:** 4/5 (Good). **IMPROVED from round-11 (3/5).** The core idea is solid, and the evaluation is more honest than most (confidence intervals, ablations, explicit limitations). The round-12 additions—specificity check (0/13 on explicit bounds), expanded cross-model validation (n=20, κ=1.0), and pooled task-intrinsic estimate (9/16)—are genuine progress that materially address my round-11 concerns about mechanism support and single-family validation. However, the mechanism remains descriptive rather than mechanistic, and methodological weaknesses—still-underpowered probe for the central novelty claim (n=16), lack of full cross-model validation on the 54-candidate adjudicated set, and the misleading 85% residual presentation—still limit confidence in the quantitative results. The paper has evolved from "promising but methodologically weak" to "solid contribution with acknowledged limitations." A strong accept.

- **Confidence:** 4/5 (High). I am familiar with the LLM-as-judge literature and REST-API oracle work, and I have read the full paper carefully across rounds 8, 9, 10, 11, and 12. The statistical critique is grounded in standard binomial proportion methods, and the cross-model ablation gap is a straightforward methodological requirement. The round-12 additions are meaningful improvements that move the paper forward, and I am confident in the assessment but leave room for the authors to provide additional data that would further strengthen the claims.

## Summary of Round-11 Concerns Status

| Concern | Round-11 Status | Round-12 Status |
|---------|----------------|-----------------|
| **(a) n underpowered (n=12)** | Major - CI [19%, 68%] too wide | Partially addressed - expanded to n=16 pooled, CI [33%, 77%] still wide but materially improved |
| **(b) mechanism correlative not causal** | Major - within-vendor contrast only | Partially addressed - added specificity check (0/13 explicit bounds) strengthens correlation but mechanism remains correlative |
| **(c) cross-model n=6 insufficient** | Major - single-family artifact concern | Partially addressed - expanded to n=20 (κ=1.0) across 5 subtypes, but full 54-candidate validation still missing |
| **(d) 85% residual misleading** | Major - sample composition vs population | Partially addressed - abstract adds "composition of our findings" clarification, but RQ1 presentation still overstates |
| **(e) incomplete ablation** | Major - anchor baseline unclear | Still open - artifact has breakdown but main text still unclear |
| **(f) mechanism attribution premature** | New in round-11 - causal claim overstates evidence | Still open - softened language would fix ("correlates with" vs "is the driver") |

**Overall progress:** 3 concerns partially addressed, 3 still open. The improvements on (a), (b), and (c) are substantive enough to upgrade from 3/5 to 4/5, but the methodological limitations prevent a 5/5.

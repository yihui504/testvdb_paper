# Mock Review: Reviewer 2 (Critical) - Round 11

## Summary

TestVDB addresses the oracle problem for API conformance defects in Vector Database Management Systems by proposing source-grounded falsification of LLM-derived behavioral claims. The authors distinguish between family-specific LLM errors (mitigated by cross-model validation) and task-intrinsic documentation-interpretation errors (requiring source as ground truth). Across 5 VDBMSs, TestVDB surfaced 111 issues; maintainers acknowledged 38 as defects, with the source anchor suppressing 81% of false positives on Milvus and Qdrant. The round-11 revision adds a within-vendor contrast on Qdrant showing that search parameters with optional defaults are over-strict while collection parameters with explicit minimums reject 0 correctly, plus a falsifiable prediction that parameters with optional defaults are over-formalization candidates while explicit-minimum parameters are not. This addition partially addresses my round-10 objection (3) about post-hoc findings by providing a falsifiable prediction, but the mechanism (documentation style as driver) remains correlative rather than causal, and the statistical support remains weak (n=3 per style). The paper is a promising contribution but needs stronger empirical backing for its central novelty claims.

## Strengths

1. **Clear problem articulation.** The VDBMS conformance defect class is well-defined with concrete examples (nprobe=0, ef=0, negative score thresholds). Table 1 effectively maps each oracle family to the defect subset it cannot reach, establishing the residual that motivates the LLM-as-oracle setting.

2. **Conceptual contribution: two-layer error model.** The distinction between family-specific self-preference and task-intrinsic documentation-interpretation errors is insightful and grounded in a plausible mechanism. Section 4 clearly articulates why cross-model validation covers the former but not the latter, motivating source-grounded falsification as the necessary countermeasure.

3. **Controlled ablation design.** The precision ablation (single-LLM 25.5% → single source cycle 45.6% → full pipeline 69.2%) isolates incremental contributions and shows that each component adds value, not just the end-to-end system.

4. **Statistical transparency.** The paper reports Wilson binomial confidence intervals for precision (69.2%, 95% CI [55.7%, 80.1%]) and acknowledges the pending-resolution worst-case bound ([43.9%, 80.5%]), which is more rigorous than point estimates alone.

5. **Honest limitation statements.** Section 8 explicitly bounds the approach (requires source, treats implementation as correct) and the threats section acknowledges the small RQ3 probe size and single-model-family limitation, showing commendable candor.

6. **Round-11 progress on falsifiable prediction (new).** The within-vendor contrast on Qdrant—search parameters with optional defaults (timeout, group_size, score_threshold) are over-strict, while collection parameters with explicit minimums (shard_number, replication_factor, write_consistency_factor) reject 0 correctly—provides a concrete falsifiable prediction that moves beyond pure post-hoc observation. This is a meaningful step toward addressing objection (3) from round-10.

## Weaknesses

### **[Major] 1. The within-vendor contrast remains descriptive, not mechanistic.**

**Location:** Section 7, RQ3, lines 142-143 (round-11 addition)

**Issue:** The round-11 addition observes that Qdrant search parameters with optional defaults are over-strict while collection parameters with explicit minimums are not, and proposes "documentation style as the driver" as the mechanism. However, this remains correlative. The paper has not demonstrated that documentation style causes over-formalization—only that the two co-occur in this sample. Alternative explanations remain: (a) search and collection parameters may be implemented by different teams with different testing cultures, (b) search parameters may be harder to test with boundary values, (c) the three search parameters may share a common code path that treats 0 as a sentinel value, while collection parameters reject 0 via separate validation. The within-vendor contrast controls for vendor identity but does not isolate documentation style as the causal driver.

**Fix:** Either (a) add a within-parameter-type contrast (e.g., find a Qdrant search parameter that has an explicit minimum and test whether it is over-strict, which would falsify the documentation-style hypothesis) or (b) soften the causal claim to "correlates with" and acknowledge that team structure, implementation difficulty, or testing culture could be confounders. The falsifiable prediction is good, but the mechanism attribution remains premature.

### **[Major] 2. Insufficient statistical support for the central task-intrinsic error claim (RQ3).**

**Location:** Section 7, RQ3, lines 142-143; Table 2; Abstract, line 20

**Issue:** The core novelty claim—that source-grounded falsification resolves task-intrinsic documentation-interpretation errors that cross-model validation cannot—rests on a probe of only twelve clauses (nine Milvus + three Qdrant). The paper acknowledges this as "exploratory" and reports a Wilson interval of [19%, 68%] for the 5/12 task-intrinsic rate, but this remains too wide to support strong claims about prevalence or generality. A single additional task-intrinsic clause would change the rate to 50%, undermining the stability of the phenomenon. The round-11 addition of three Qdrant clauses helps (bringing n from 9 to 12), but this is still woefully underpowered.

**Fix:** Scale the probe to a statistically powered sample (n≥50 clauses across multiple VDBMSs) and report exact binomial confidence intervals. If scaling is infeasible, reframe RQ3 as exploratory evidence and remove the "task-intrinsic" terminology from the abstract until confirmed. The current presentation outpaces the empirical support.

### **[Major] 3. Missing cross-model validation for the dev-reviewer's source-grounded falsification.**

**Location:** Section 6, line 110; Section 7, threats to validity, line 172

**Issue:** All source-anchor results use a single model family (GLM-5.2). The paper claims source-grounded falsification addresses task-intrinsic errors, but if the dev-reviewer itself exhibits family-specific bias when reading source code, the 81% FP suppression may be inflated. The threats section mentions a "preliminary cross-model check" with DeepSeek on six candidates (κ=1.0), but this is too small to assess consistency across the full 54-candidate adjudicated set. Without a larger consistency check, we cannot rule out that the 81% figure is partially a GLM-specific artifact.

**Fix:** Run a cross-model consistency check on the full 54 adjudicated candidates: have DeepSeek perform the dev-reviewer's source-grounded falsification on all 54 and report agreement rate (Cohen's κ). If κ < 0.6, the single-family results are unreliable; if κ ≥ 0.6, report this validation and note the remaining uncertainty. The six-candidate pilot is insufficient.

### **[Major] 4. The "85% conformance residual" is a sample composition, not a population estimate.**

**Location:** Abstract, line 22; Section 7, RQ1, lines 117-118

**Issue:** The abstract states "about 85% are, by our classification, conformance defects that classical oracles cannot reach" and presents this as a central finding. However, this is not an estimate of the true VDBMS defect distribution—it is the composition of TestVDB's own biased sample, which the paper acknowledges only in Section 8. The presentation in the abstract and RQ1 reads as a population claim ("the residual is 85%") when it is actually a sample-composition figure ("our findings are 85% conformance"). Without capture-recapture estimation or an unbiased defect sample, the 85% figure cannot support general claims about the prevalence of conformance defects in VDBMSs.

**Fix:** Reword the abstract and RQ1 to clearly state that this is the composition of TestVDB's findings, not an estimate of the true defect distribution. For example: "Of the 111 issues TestVDB surfaced, 85% are, by our classification, conformance defects that classical oracles cannot reach." Avoid language that implies this proportion generalizes to all VDBMS defects.

### **[Major] 5. Incomplete ablation of the dev-reviewer's three anchors.**

**Location:** Section 5, line 108-109; Section 7, RQ2, line 140

**Issue:** The dev-reviewer applies three anchors (clean reproduction, source-grounded falsification, threat-model cross-check), but the paper claims "the source anchor suppresses 81% of false positives (up from 31%)" without clarifying what "without it" means. Is the 31% baseline with no anchors at all, or with only the clean-reproduction anchor? Without per-anchor ablation, we cannot assess whether source-grounded falsification is the primary contributor or whether the live API re-probe does most of the work. The threat-model anchor is never described or ablated.

**Fix:** Report per-anchor ablation: precision/recall for (a) no anchors, (b) clean reproduction only, (c) source only, (d) all three. Replace "up from 31% without it" with "up from 31% when only the clean-reproduction anchor is applied" (or whatever the baseline actually was). Explain the threat-model anchor and ablate it.

### **[Minor] 6. Missing statistical test for the 81% vs. 31% FP suppression comparison.**

**Location:** Section 7, RQ2, line 140

**Issue:** The paper claims "the source anchor suppresses 81% of false positives (up from 31%)" but does not report whether this difference is statistically significant. With n=54 adjudicated candidates, a McNemar's test for paired binary outcomes or Fisher's exact test could assess whether the source anchor adds predictive power beyond the other anchors.

**Fix:** Perform a statistical test (McNemar's or Fisher's exact) on the 2×2 table (source anchor present/absent × FP/TP) and report the p-value. If p < 0.05, state that the improvement is significant; if not, soften the claim to "suggestive improvement."

### **[Minor] 7. Incomplete comparison with recent LLM-based oracle work.**

**Location:** Section 9, lines 179-186

**Issue:** The paper compares against AGORA+, SATORI, MASTOR, Toradocu, Doc2OracLL, ChatAssert, and Testora, but the critical distinction—source vs. runtime verification—is under-explored. ChatAssert uses compilation and execution feedback; Testora uses differential execution. Both rely on runtime behavior, which cannot distinguish between a correct implementation and a bug that coincidentally satisfies the LLM's oracle. The related work section does not explicitly state whether these tools would or would not detect the task-intrinsic errors on the twelve-clause probe, leaving readers uncertain whether TestVDB is strictly better or merely better-validated.

**Fix:** Add a sentence clarifying that ChatAssert, Testora, and Toradocu rely on runtime feedback and therefore cannot distinguish correct implementations from bugs that happen to satisfy the LLM's interpretation. Explicitly state that the twelve-clause probe is, by definition, inaccessible to runtime-only methods.

### **[Minor] 8. Missing reproducibility details for LLM sampling.**

**Location:** Section 6, line 110

**Issue:** The paper states agents use "the runtime's default sampling" but does not specify temperature, top-p, or whether random seeds are fixed. For reproducibility and to rule out the possibility that the 81% FP suppression is sampling-dependent, the implementation section should report the sampling parameters and whether results vary across multiple runs.

**Fix:** Report temperature and top-p values for the LLM backbone, and run a small reproducibility check: execute the full pipeline on one VDBMS with three different random seeds and report variance. If variance is low, note this as evidence of stability; if high, report the range and flag reproducibility as a limitation.

### **[Minor] 9. Unclear boundary between model-free invariant oracle and LLM pipeline.**

**Location:** Section 7, RQ4, lines 168-169

**Issue:** The model-free invariant subclass (COSINE bounds, index completeness) is presented as separately detecting mathematical-invariant violations with no LLM involvement, but it is unclear whether these findings are included in the 111 total submissions or counted separately. If included, they inflate the denominator without leveraging TestVDB's core novelty. If separate, the paper should report the count explicitly.

**Fix:** Explicitly state how many of the 111 submissions come from the model-free invariant subclass versus the LLM pipeline. Break down the 38 acknowledged defects by source (LLM vs. model-free) and clarify whether the 69.2% precision applies to the full set or only to LLM-derived candidates.

### **[Minor] 10. Limited external validity beyond two VDBMSs.**

**Location:** Section 7, threats to validity, line 172

**Issue:** The paper correctly notes that "statistical claims rest on Milvus and Qdrant," but this narrow scope undermines generalizability. Weaviate (30 submissions, 3 acknowledged), MeiliSearch (3, 0), and Chroma (1, 0) provide breadth but not statistical weight. The abstract and introduction do not explicitly state that the quantitative results (precision, FP suppression, task-intrinsic catch rate) are primarily validated on two systems.

**Fix:** Qualify all quantitative claims in the abstract and introduction with "on Milvus and Qdrant" or similar. For example: "A controlled retrospective on Milvus and Qdrant shows the source anchor suppresses 81% of false positives." Avoid presenting these figures as universally applicable to all five VDBMSs.

## Questions for Authors

1. **On the within-vendor contrast:** You propose that documentation style (optional default vs. explicit minimum) drives over-formalization. Have you controlled for alternative explanations? For example, are the search and collection parameters implemented by different teams? Do they share test coverage or code paths that could explain the difference? How would you falsify the documentation-style hypothesis itself?

2. **On the task-intrinsic error probe:** What stopping rule determined the twelve-clause sample size for RQ3? If this is meant to be exploratory, why is it presented as a supported contribution in the abstract rather than as preliminary evidence? Do you have plans to scale this probe, and what would constitute adequate statistical power?

3. **On the 81% FP suppression claim:** To what extent does this figure depend on GLM-5.2's specific behavior when reading source code? Have you validated that DeepSeek produces similar source-grounded falsification verdicts on the full 54-candidate adjudicated set, not just the 6-candidate pilot?

4. **On the 85% conformance residual:** You acknowledge this is the composition of your findings, not a population estimate. Do you have any evidence about whether conformance defects are equally prevalent in practice, or is TestVDB's focus on conformance purely a design choice that may miss other defect classes?

## Scores

- **Soundness:** 3/5 (Acceptable). **UNCHANGED from round-10.** The method is conceptually sound and the ablations are well-designed. The round-11 addition of a within-vendor contrast and falsifiable prediction is a meaningful step forward, but the mechanism remains correlative rather than causal, and the core task-intrinsic error claim still rests on a probe that is too small (n=12) to support strong quantitative assertions. The lack of cross-model validation for the dev-reviewer beyond a 6-candidate pilot also persists.

- **Significance:** 3/5 (Acceptable). **UNCHANGED from round-10.** The problem setting is real and the two-layer error model is a meaningful conceptual contribution. The round-11 falsifiable prediction strengthens the theoretical contribution by providing a testable hypothesis, but the practical impact remains unclear without evidence that the approach scales beyond Milvus and Qdrant, and the 85% residual figure is still misleadingly presented as a prevalence estimate rather than a sample composition.

- **Novelty:** 4/5 (Good). **UNCHANGED from round-10.** The source-grounded falsification approach is a genuine advance over prior LLM-based oracle work, which relies on runtime feedback or structured specifications. The distinction between family-specific and task-intrinsic errors is novel and well-motivated. The round-11 addition of a falsifiable prediction strengthens the novelty by moving beyond pure post-hoc observation.

- **Presentation:** 4/5 (Good). **UNCHANGED from round-10.** The paper is clearly written, with excellent use of concrete examples and a strong table mapping oracle families to defect subsets. The round-11 addition is well-integrated into RQ3, but the abstract still overstates the statistical support for the task-intrinsic claim, and the 85% residual is presented without sufficient qualification.

- **Overall:** 3/5 (Acceptable). **UNCHANGED from round-10.** The core idea is solid, and the evaluation is more honest than most (confidence intervals, ablations, explicit limitations). The round-11 addition of a within-vendor contrast and falsifiable prediction is genuine progress that partially addresses my objection (3) about post-hoc findings. However, the mechanism remains descriptive rather than mechanistic, and the methodological weaknesses—small probe size for the central novelty claim (n=12), lack of cross-model validation for the dev-reviewer beyond a 6-candidate pilot, and the misleading 85% residual presentation—still limit confidence in the quantitative results. With revision to address the major issues, particularly scaling the RQ3 probe and adding full cross-model checks, this would be a stronger paper.

- **Confidence:** 4/5 (High). I am familiar with the LLM-as-judge literature and REST-API oracle work, and I have read the full paper carefully across rounds 8, 9, 10, and 11. The statistical critique is grounded in standard binomial proportion methods, and the cross-model ablation gap is a straightforward methodological requirement. The round-11 addition is a meaningful improvement but does not resolve the core methodological limitations. I am confident in the assessment but leave room for the authors to provide additional data that would change the scores.

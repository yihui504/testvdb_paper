# Mock Review: Reviewer 2 (Critical)

## Summary

TestVDB addresses the oracle problem for API conformance defects in Vector Database Management Systems by proposing source-grounded falsification of LLM-derived behavioral claims. The authors distinguish between family-specific LLM errors (mitigated by cross-model validation) and task-intrinsic documentation-interpretation errors (requiring source as ground truth). Across 5 VDBMSs, TestVDB surfaced 111 issues; maintainers acknowledged 38 as defects, with the source anchor suppressing 81% of false positives. While the problem is real and the two-layer error model is conceptually sound, the evaluation has methodological limitations: the central task-intrinsic error claim rests on a small probe (N=9 clauses), the "85% conformance residual" is a biased sample composition rather than a population estimate, and key components lack cross-model validation. The paper is a promising contribution but needs stronger empirical support for its novelty claims.

## Strengths

1. **Clear problem articulation.** The VDBMS conformance defect class is well-defined with concrete examples (nprobe=0, ef=0, negative score thresholds). Table 1 effectively maps each oracle family to the defect subset it cannot reach, establishing the residual that motivates the LLM-as-oracle setting.

2. **Conceptual contribution: two-layer error model.** The distinction between family-specific self-preference and task-intrinsic documentation-interpretation errors is insightful and grounded in a plausible mechanism. Section 4 clearly articulates why cross-model validation covers the former but not the latter, motivating source-grounded falsification as the necessary countermeasure.

3. **Controlled ablation design.** The precision ablation (single-LLM 25.5% → single source cycle 45.6% → full pipeline 69.2%) isolates incremental contributions and shows that each component adds value, not just the end-to-end system.

4. **Statistical transparency.** The paper reports Wilson binomial confidence intervals for precision (69.2%, 95% CI [55.7%, 80.1%]) and acknowledges the pending-resolution worst-case bound ([43.9%, 80.5%]), which is more rigorous than point estimates alone.

5. **Honest limitation statements.** Section 8 explicitly bounds the approach (requires source, treats implementation as correct) and the threats section acknowledges the small RQ3 probe size and single-model-family limitation, showing commendable candor.

## Weaknesses

### **[Major] 1. Insufficient statistical support for the central task-intrinsic error claim (RQ3).**

**Location:** Section 7, RQ3, lines 142-143; Table 2; Abstract, line 20

**Issue:** The core novelty claim—that source-grounded falsification resolves task-intrinsic documentation-interpretation errors that cross-model validation cannot—rests on a probe of only nine clauses from a single VDBMS (Milvus). The paper acknowledges this as "the most contingent finding" and treats it as "a pilot pending a larger study," yet the abstract and contributions present it as a supported finding. With n=9, the observed 2/9 task-intrinsic rate has a 95% Wilson interval of approximately [7%, 56%], which is too wide to support strong claims about prevalence or generality. A single additional task-intrinsic clause would change the rate to 33%, undermining the stability of the phenomenon.

**Fix:** Scale the probe to a statistically powered sample (n≥50 clauses across multiple VDBMSs) and report exact binomial confidence intervals. If scaling is infeasible, reframe RQ3 as exploratory evidence and remove the "task-intrinsic" terminology from the abstract until confirmed. The current presentation outpaces the empirical support.

### **[Major] 2. Missing cross-model validation for the dev-reviewer's source-grounded falsification.**

**Location:** Section 6, line 110; Section 7, threats to validity, line 172

**Issue:** All source-anchor results use a single model family (GLM-5.2). The paper claims source-grounded falsification addresses task-intrinsic errors, but if the dev-reviewer itself exhibits family-specific bias when reading source code, the 81% FP suppression may be inflated. The threats section states "a full cross-model ablation of the dev-reviewer is open," but this is a methodological gap, not a future-work item. Without at least a consistency check that a second family produces similar source-grounded verdicts on a subset of candidates, we cannot rule out that the 81% figure is partially a GLM-specific artifact.

**Fix:** Run a cross-model consistency check on the 54 adjudicated candidates: have a second family (e.g., DeepSeek) perform the dev-reviewer's source-grounded falsification on a random subset (e.g., 20 candidates) and report agreement rate (Cohen's κ). If κ < 0.6, the single-family results are unreliable; if κ ≥ 0.6, report this validation and note the remaining uncertainty.

### **[Major] 3. The "85% conformance residual" is a sample composition, not a population estimate.**

**Location:** Abstract, line 22; Section 7, RQ1, lines 117-118

**Issue:** The abstract states "about 85% are, by our classification, conformance defects that classical oracles cannot reach" and presents this as a central finding. However, this is not an estimate of the true VDBMS defect distribution—it is the composition of TestVDB's own biased sample, which the paper acknowledges only in Section 8. The presentation in the abstract and RQ1 reads as a population claim ("the residual is 85%") when it is actually a sample-composition figure ("our findings are 85% conformance"). Without capture-recapture estimation or an unbiased defect sample, the 85% figure cannot support general claims about the prevalence of conformance defects in VDBMSs.

**Fix:** Reword the abstract and RQ1 to clearly state that this is the composition of TestVDB's findings, not an estimate of the true defect distribution. For example: "Of the 111 issues TestVDB surfaced, 85% are, by our classification, conformance defects that classical oracles cannot reach." Avoid language that implies this proportion generalizes to all VDBMS defects.

### **[Major] 4. Incomplete ablation of the dev-reviewer's three anchors.**

**Location:** Section 5, line 108-109; Section 7, RQ2, line 140

**Issue:** The dev-reviewer applies three anchors (clean reproduction, source-grounded falsification, threat-model cross-check), but the paper claims "the source anchor suppresses 81% of false positives (up from 31%)" without clarifying what "without it" means. Is the 31% baseline with no anchors at all, or with only the clean-reproduction anchor? Without per-anchor ablation, we cannot assess whether source-grounded falsification is the primary contributor or whether the live API re-probe does most of the work. The threat-model anchor is never described or ablated.

**Fix:** Report per-anchor ablation: precision/recall for (a) no anchors, (b) clean reproduction only, (c) source only, (d) all three. Replace "up from 31% without it" with "up from 31% when only the clean-reproduction anchor is applied" (or whatever the baseline actually was). Explain the threat-model anchor and ablate it.

### **[Minor] 5. Missing statistical test for the 81% vs. 31% FP suppression comparison.**

**Location:** Section 7, RQ2, line 140

**Issue:** The paper claims "the source anchor suppresses 81% of false positives (up from 31%)" but does not report whether this difference is statistically significant. With n=54 adjudicated candidates, a McNemar's test for paired binary outcomes or Fisher's exact test could assess whether the source anchor adds predictive power beyond the other anchors.

**Fix:** Perform a statistical test (McNemar's or Fisher's exact) on the 2×2 table (source anchor present/absent × FP/TP) and report the p-value. If p < 0.05, state that the improvement is significant; if not, soften the claim to "suggestive improvement."

### **[Minor] 6. Incomplete comparison with recent LLM-based oracle work.**

**Location:** Section 9, lines 179-186

**Issue:** The paper compares against AGORA+, SATORI, MASTOR, Toradocu, Doc2OracLL, ChatAssert, and Testora, but the critical distinction—source vs. runtime verification—is under-explored. ChatAssert uses compilation and execution feedback; Testora uses differential execution. Both rely on runtime behavior, which cannot distinguish between a correct implementation and a bug that coincidentally satisfies the LLM's oracle. The related work section does not explicitly state whether these tools would or would not detect the task-intrinsic errors on the nine-clause Milvus probe, leaving readers uncertain whether TestVDB is strictly better or merely better-validated.

**Fix:** Add a sentence clarifying that ChatAssert, Testora, and Toradocu rely on runtime feedback and therefore cannot distinguish correct implementations from bugs that happen to satisfy the LLM's interpretation. Explicitly state that the Milvus nine-clause probe is, by definition, inaccessible to runtime-only methods.

### **[Minor] 7. Missing reproducibility details for LLM sampling.**

**Location:** Section 6, line 110

**Issue:** The paper states agents use "the runtime's default sampling" but does not specify temperature, top-p, or whether random seeds are fixed. For reproducibility and to rule out the possibility that the 81% FP suppression is sampling-dependent, the implementation section should report the sampling parameters and whether results vary across multiple runs.

**Fix:** Report temperature and top-p values for the LLM backbone, and run a small reproducibility check: execute the full pipeline on one VDBMS with three different random seeds and report variance. If variance is low, note this as evidence of stability; if high, report the range and flag reproducibility as a limitation.

### **[Minor] 8. Unclear boundary between model-free invariant oracle and LLM pipeline.**

**Location:** Section 7, RQ4, lines 168-169

**Issue:** The model-free invariant subclass (COSINE bounds, index completeness) is presented as separately detecting mathematical-invariant violations with no LLM involvement, but it is unclear whether these findings are included in the 111 total submissions or counted separately. If included, they inflate the denominator without leveraging TestVDB's core novelty. If separate, the paper should report the count explicitly.

**Fix:** Explicitly state how many of the 111 submissions come from the model-free invariant subclass versus the LLM pipeline. Break down the 38 acknowledged defects by source (LLM vs. model-free) and clarify whether the 69.2% precision applies to the full set or only to LLM-derived candidates.

### **[Minor] 9. Limited external validity beyond two VDBMSs.**

**Location:** Section 7, threats to validity, line 172

**Issue:** The paper correctly notes that "statistical claims rest on Milvus and Qdrant," but this narrow scope undermines generalizability. Weaviate (30 submissions, 3 acknowledged), MeiliSearch (3, 0), and Chroma (1, 0) provide breadth but not statistical weight. The abstract and introduction do not explicitly state that the quantitative results (precision, FP suppression, task-intrinsic catch rate) are primarily validated on two systems.

**Fix:** Qualify all quantitative claims in the abstract and introduction with "on Milvus and Qdrant" or similar. For example: "A controlled retrospective on Milvus and Qdrant shows the source anchor suppresses 81% of false positives." Avoid presenting these figures as universally applicable to all five VDBMSs.

## Questions for Authors

1. **On the task-intrinsic error probe:** What stopping rule determined the nine-clause sample size for RQ3? If this is meant to be exploratory, why is it presented as a supported contribution in the abstract rather than as preliminary evidence? Do you have plans to scale this probe, and what would constitute adequate statistical power?

2. **On the 81% FP suppression claim:** To what extent does this figure depend on GLM-5.2's specific behavior when reading source code? Have you validated that a second LLM family produces similar source-grounded falsification verdicts on the adjudicated set? If not, how should readers interpret the reliability of this number?

3. **On the 85% conformance residual:** You acknowledge this is the composition of your findings, not a population estimate. Do you have any evidence about whether conformance defects are equally prevalent in practice, or is TestVDB's focus on conformance purely a design choice that may miss other defect classes?

## Scores

- **Soundness:** 3/5 (Acceptable). The method is conceptually sound and the ablations are well-designed, but the core task-intrinsic error claim rests on a probe that is too small to support strong quantitative assertions (n=9), and the lack of cross-model validation for the dev-reviewer introduces uncertainty about whether the 81% FP suppression is a general effect or a GLM-specific artifact.

- **Significance:** 3/5 (Acceptable). The problem setting is real and the two-layer error model is a meaningful conceptual contribution. However, the practical impact is unclear without evidence that the approach scales beyond Milvus and Qdrant, and the 85% residual figure is misleadingly presented as a prevalence estimate rather than a sample composition.

- **Novelty:** 4/5 (Good). The source-grounded falsification approach is a genuine advance over prior LLM-based oracle work, which relies on runtime feedback or structured specifications. The distinction between family-specific and task-intrinsic errors is novel and well-motivated.

- **Presentation:** 4/5 (Good). The paper is clearly written, with excellent use of concrete examples and a strong table mapping oracle families to defect subsets. However, the abstract overstates the statistical support for the task-intrinsic claim, and the 85% residual is presented without sufficient qualification.

- **Overall:** 3/5 (Acceptable). The core idea is solid, and the evaluation is more honest than most (confidence intervals, ablations, explicit limitations). However, the methodological weaknesses—small probe size for the central novelty claim, lack of cross-model validation for the dev-reviewer, and the misleading 85% residual presentation—limit confidence in the quantitative results. With revision to address the major issues, particularly scaling the RQ3 probe and adding cross-model checks, this would be a stronger paper.

- **Confidence:** 4/5 (High). I am familiar with the LLM-as-judge literature and REST-API oracle work, and I have read the full paper carefully. The statistical critique is grounded in standard binomial proportion methods, and the cross-model ablation gap is a straightforward methodological requirement. I am confident in the assessment but leave room for the authors to provide additional data that would change the scores.

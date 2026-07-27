# Reviewer 2: Mock Review of TestVDB

## Summary

This paper proposes TestVDB, a four-stage pipeline that uses LLMs to detect documentation-implementation defects in vector database management systems (VDBMSs). The authors motivate this problem class by observing that most VDBMS defects are logical bugs that do not crash, and thus escape existing crash-oracle fuzzers such as VDBFuzz. Their core technical contribution is the introduction of a "dev-reviewer" agent that acts as a source-grounded falsifier to suppress false positives arising from two failure modes: LLM hallucination in behavioral-claim extraction and self-preference bias in judgment. The paper reports 49 maintainer-acknowledged true-positive defects across three VDBMSs (Milvus, Qdrant, Weaviate), with 15 fixed via merged PRs. On a 48-candidate maintainer-adjudicated retrospective, the dev-reviewer achieves 67% precision and 74% recall (3-run any-confirmed ensemble), compared to 37% recall without source grounding. A bidirectional probe against VDBFuzz shows complementary coverage on Qdrant.

The work addresses a real and timely problem—LLM-derived oracles for natural-language documentation—and the source-grounded falsification approach is technically sound. However, the evaluation has several post-hoc characteristics that weaken confidence in the reported operating points, and the paper would benefit from more explicit acknowledgment of these limitations and clearer motivation for the chosen ensemble strategy.

## Strengths

1. **Well-motivated problem setting.** The distinction between crash-oracle detection (VDBFuzz) and documentation-implementation consistency is clearly articulated. The example case (Milvus #49823: `nprobe=0`) effectively illustrates the defect class.

2. **Technical contribution is properly motivated.** The two false-positive modes (extraction hallucination, judgment self-preference) are clearly explained, and the structural insufficiency of multi-perspective judging (80% precision, 15% recall) is a credible baseline that justifies the need for an independent signal (source code).

3. **RQ1 demonstrates practical impact.** The 49 maintainer-acknowledged true positives with 15 merged-PR fixes across three production VDBMSs provide concrete evidence of practical relevance.

4. **Oracle-exclusion argument (Table 1) is systematic.** The paper walks through standard oracle candidates and explains why each misses the documentation-implementation residual, which helps justify why an LLM-derived oracle is necessary in this regime.

## Weaknesses

### **[HIGH, partially fixable] Post-hoc operating point selection in RQ2**

The paper reports multiple operating points (single run, 3-run union, 5-run union, 5-run majority) in Table 2 and selects the 3-run union as the headline, explicitly labeling it a "post-hoc operating point justified by falsifier semantics." This selection is concerning for two reasons:

1. **Statistical inference problem.** When multiple operating points are computed on the same 48-candidate set and one is selected post-hoc as the headline, standard confidence intervals do not account for selection bias. The Wilson 95% CIs reported (e.g., precision [49%, 81%]) understate the true uncertainty because they condition on the chosen operating point rather than the full exploratory process.

2. **Lack of pre-registered analysis plan.** The paper does not describe a pre-specified rule for when the 3-run union vs. 5-run union vs. majority would be selected. The justification ("under-confirmation is costlier than forwarding a false positive") is a semantic rationale for preferring high-recall operating points, but it does not explain why 3 runs is the optimal trade-off rather than 1 or 5.

The threat would be mitigated if the paper reported the full exploratory analysis (including operating points that were tried and abandoned) and provided a principled decision rule (e.g., "we select the highest-recall operating point with precision ≥ 60%"). As written, the selection appears cherry-picked.

### **[HIGH, not easily fixable] Limited statistical power in cross-model check**

The paper reports a cross-model check where DeepSeek re-runs the dev-reviewer on twenty candidates and achieves Cohen's κ = 1.0 with GLM-5.2, then concludes "the verdict does not appear strongly family-specific when source evidence is explicit." This claim is statistically weak:

1. **Sample size is too small.** Twenty candidates with κ = 1.0 yields a Wilson 95% CI on agreement of [83%, 100%]. This interval is compatible with moderate family-specificity (agreement as low as 83%) but the paper presents the result as strong evidence against family-specificity.

2. **Selection bias.** The twenty candidates were not randomly sampled from the 48-candidate retrospective. Without explicit description of the selection criteria, it is unclear whether they were chosen because they were "easy" cases (clear source evidence) or because they were representative of the full distribution.

3. **No estimate of recall.** The paper explicitly states "we do not estimate recall because no public ground-truth defect catalog for VDBMSs exists." This creates an asymmetry: the dev-reviewer's precision is evaluated against maintainer adjudication, but its recall (the probability it detects a defect that exists) is unknown. The κ = 1.0 result on twenty candidates suggests consistency, not sensitivity.

A stronger cross-model validation would either (a) report performance on the full 48-candidate set under DeepSeek, or (b) provide a statistical power analysis showing that twenty candidates is sufficient to detect a meaningful family-specificity effect given the observed κ = 1.0.

### **[MEDIUM, fixable] VDBFuzz bidirectional probe is hypothesis-generating only**

RQ3 reports a bidirectional reachability probe between TestVDB and VDBFuzz on Qdrant. The paper correctly states "each direction is n=1; we treat these as hypothesis-generating controlled cases rather than a generalized result." However, two limitations weaken the section's contribution:

1. **Template limitation claim is not independently verified.** The paper interprets VDBFuzz's failure to detect TestVDB's #9045 as a "limitation of VDBFuzz's current templates and input coverage" rather than a fundamental limitation of crash oracles. This claim would be stronger if the paper examined VDBFuzz's template source or ran VDBFuzz with a `wait=false` seed to confirm the limitation.

2. **No discussion of oracle asymmetry.** The paper observes that TestVDB reaches a VDBFuzz crash (integer overflow on `size=2^63`) by contract reasoning, while VDBFuzz misses a TestVDB silent-accept defect (#909045). This suggests an asymmetry: crash-oracle tools are a subset of documentation-implementation testing. The paper does not explicitly discuss whether this asymmetry is expected (i.e., whether VDBFuzz is *designed* to miss silent-accept defects) or whether it represents a gap in VDBFuzz's coverage.

The section would be strengthened by framing the bidirectional probe as an analysis of *oracle coverage* rather than just tool comparison, and by more explicitly grounding the "template limitation" claim in VDBFuzz's design or configuration.

### **[MEDIUM, fixable] Multi-perspective judging baseline under-specified**

Section 5 (The False-Positive Problem) states that multi-perspective judging reaches "about 80% precision but only about 15% recall" but does not provide details on the judge design, voting rule, or operating point selection. This baseline is critical to the paper's core claim (that source grounding is necessary because multi-perspective judging is insufficient), yet it receives only two sentences of description.

The paper would benefit from a brief table or figure showing:
- The four specialized judge roles (documentation, evidence, severity, novelty) and their prompts/objectives
- The voting rule (majority? unanimity? weighted?)
- The precision/recall operating points for different voting thresholds
- Why 15% recall is the selected operating point (is it the highest-recall configuration that still achieves 80% precision? or the result of a specific parameter setting?)

Without these details, it is difficult to assess whether multi-perspective judging is fundamentally insufficient (as the paper claims) or whether it was under-tuned.

### **[LOW, not fixable] Page limit constraints}

At 6 pages (ACM sigconf format), the paper is at the lower bound for SE top-conference full papers. The condensed treatment of RQ2 (multiple operating points, ensemble selection) and RQ3 (bidirectional probe) is likely due to space constraints, but the trade-off is a weakened evaluation story. If the venue allows, extending to 8-10 pages would allow the paper to (a) describe the cross-model check methodology more thoroughly, (b) expand the multi-perspective judging baseline, and (c) provide a more principled discussion of operating point selection.

## Questions

1. **Operating point selection.** Beyond the semantic justification ("under-confirmation is costlier"), is there a quantitative criterion for selecting the 3-run union over the 5-run union or majority? For example, did you pre-specify a target precision threshold (e.g., ≥ 60%) and select the highest-recall operating point that meets it? Or did you evaluate the full exploratory analysis and then select the 3-run union post-hoc?

2. **Cross-model validation.** Why was the cross-model check limited to twenty candidates rather than the full 48-candidate retrospective? Were the twenty candidates selected randomly, or were they chosen based on some criterion (e.g., availability of source evidence, diversity of defect types)? If the former, what was the sampling procedure?

3. **VDBFuzz template limitation.** You claim that VDBFuzz's failure to detect #9045 is due to a "limitation of VDBFuzz's current templates." Did you examine VDBFuzz's template source or run VDBFuzz with a manually specified `wait=false` input to verify this claim? Or is the claim inferred from the fact that VDBFuzz found 0 crashes on the version where #9045 is live?

4. **Multi-perspective judging.** The paper reports 80% precision and 15% recall for multi-perspective judging. What voting rule achieved these numbers (majority, unanimity, weighted)? Does 15% recall represent the highest-recall operating point that maintains ≥ 80% precision, or is it a specific configuration you tested?

5. **Yield calculation.** In RQ1, you report 49 true positives out of 107 submitted issues (45.8% worst-case yield precision). Did you estimate the false-negative rate (defects that exist but TestVDB failed to detect)? If not, is there a way to bound this quantity (e.g., by manual inspection of a random sample of closed/resolved issues that TestVDB did not flag)?

## Scores

- **Soundness:** 3/5 — The core approach (source-grounded falsification) is sound, but the evaluation has post-hoc characteristics (operating point selection, cross-model sample selection) that weaken confidence in the reported metrics. The threats to validity section acknowledges some limitations, but not the post-hoc selection bias in RQ2.

- **Significance:** 4/5 — The problem is real (49 maintainer-acknowledged defects, 15 merged-PR fixes), and the dev-reviewer is a practical contribution. However, the limited recall evaluation (no estimate of false-negative rate) means the true yield in production VDBMSs is unknown.

- **Novelty:** 4/5 — LLM-derived oracles for REST APIs have been explored (AGORA+, SATORI, MASTOR), but the application to natural-language documentation and the source-grounded falsification approach are novel. The paper clearly articulates the distinction between low-ambiguity structured sources (OpenAPI, traces) and high-ambiguity prose documentation.

- **Presentation:** 4/5 — The writing is clear and the oracle-exclusion table (Table 1) effectively motivates the problem. However, the multi-perspective judging baseline is under-specified (two sentences), and the operating point selection discussion could be more explicit about the exploratory analysis process.

**Overall:** 4/10 — The technical contribution is solid and the problem is well-motivated, but the evaluation has post-hoc characteristics that limit confidence in the reported operating points. With a more principled operating point selection criterion and a fuller cross-model validation, this would be a stronger paper.

**Confidence:** 4/5 — I am familiar with LLM-as-judge reliability issues and VDBMS testing, but I am not an expert on vector database internals or the specific VDBFuzz implementation. My assessment of the post-hoc operating point selection is based on general statistical principles and SE evaluation standards, not domain-specific knowledge of VDBMS testing benchmarks.

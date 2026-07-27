# Round 9 Review: TestVDB (Reviewer 2 — Critical)

## Summary

This Round 9 revision addresses two Major weaknesses from Round 8: W1 (RQ3's n=9 probe was underpowered) and W3 (single-model dev-reviewer lacked reliability validation). The authors have expanded RQ3 to n=12 (Milvus + Qdrant) and added a DeepSeek cross-model check with Cohen's κ=1.0 on n=6. While these changes demonstrate the experimental direction, **the evidence remains statistically underpowered** for the paper's core claims. The central problem is that the TI phenomenon rate of 5/12 (Wilson 95% CI [19%, 68%]) is too wide to claim any generalizable finding, and the cross-model κ=1.0 on n=6 is indistinguishable from chance agreement when the underlying task is binary adjudication on a small, selected sample. The paper's framing of "over-strict concentrates in optional-default APIs" reads as post hoc rationalization rather than a principled finding. I recommend **Weak Accept** with a request that the authors either (a) substantially expand the probe to n≥30 across at least 3 vendors, or (b) downscope the task-intrinsic error claims to "exploratory findings" and reframe RQ3 as a pilot study.

---

## Strengths

1. **Improved experimental design over Round 8.** The expansion from n=9 to n=12, and the addition of Qdrant v1.18.2 as a cross-vendor check, are steps in the right direction. The three Qdrant clauses being task-intrinsic is a strong signal that the phenomenon is not Milvus-specific.

2. **Source-grounded falsification remains methodologically sound.** The core idea—treating LLM-derived claims as falsifiable hypotheses against implementation behavior—is well-motivated and theoretically grounded. The RQ2 retrospective (source anchor suppresses 81% of FPs at 96.7% TP retention) is the paper's strongest evidence and is largely unchanged from Round 8.

3. **Transparent uncertainty reporting.** The authors correctly report Wilson 95% CIs for the TI rate (5/12 → [19%, 68%]) and flag the RQ3 probe as "pending a larger study" (§6.3). This honesty about limitations is commendable.

4. **Per-anchor breakdown in RQ2.** The isolation of source (75%), threat-model (50%), and union (91%) contributions clarifies where precision gains come from and strengthens the causal claim about source-grounded falsification.

---

## Weaknesses

### [Major] W1: RQ3's n=12 probe remains statistically underpowered for the TI rate claim.

**Section 6.3, lines 143-170; Table 3**

The core claim in RQ3 is that "cross-model validation cannot resolve task-intrinsic documentation-interpretation errors" (§6.3). The evidence is a probe of 12 over-strict clauses, where 5 are task-intrinsic (both GLM and DeepSeek independently over-formalize). The authors report a TI rate of 5/12 with a Wilson 95% CI of [19%, 68%]. This interval is too wide to support any meaningful generalization:

- **Precision problem:** A CI of ±25 percentage points means the true TI rate could be as low as 19% (barely above chance) or as high as 68% (dominant). With this uncertainty, the paper cannot claim that "task-intrinsic errors are a substantial subclass" or that "cross-model validation misses a nontrivial fraction."
- **Power analysis absent:** The authors do not justify why n=12 is sufficient. A post-hoc power calculation for detecting a TI rate of 42% (5/12) against a null of 0% (no TI phenomenon) yields ~53% power at α=0.05—worse than a coin flip. To achieve 80% power, the required sample is n≈26. The current n=12 is underpowered by a factor of 2.
- **Selection bias unclear:** How were the 12 clauses selected? If they were chosen from a larger pool of GLM-extracted clauses because they were "suspiciously over-strict," the TI rate is inflated by selection bias. The paper does not describe the sampling procedure.

**Concrete fix:** Either (a) expand the probe to n≥30 across at least 3 vendors (Milvus, Qdrant, Weaviate) with a documented random sampling strategy from the full set of GLM-extracted clauses, then re-compute the TI rate and CI; or (b) reframe RQ3 as an exploratory pilot ("We observed a TI rate of 5/12 (95% CI [19%, 68%]); further work is needed to determine if this phenomenon generalizes") and remove claims about cross-model validation's insufficiency.

---

### [Major] W2: κ=1.0 on n=6 is not convincing evidence for dev-reviewer reliability.

**Section 6.2, line 140; §7.3, lines 176-177**

Round 8 flagged that the dev-reviewer used a single LLM family (GLM-5.2) with no cross-model validation. Round 9 adds a DeepSeek re-run on 6 candidates, reporting Cohen's κ=1.0 (perfect agreement). This is presented as evidence that "the verdict does not appear family-specific" (§6.2). However:

- **κ is misleading for small, binary-adjudication samples.** κ=1.0 on n=6 could easily arise from chance agreement on a small, selected sample. The 95% CI for κ on n=6 with perfect agreement is approximately [0.60, 1.0] (using exact binomial CI for the agreement rate), which overlaps with "moderate agreement." The authors do not report uncertainty.
- **Selection bias threat.** The 6 candidates were "blind to GLM-5.2's rationale" (§6.2), but the paper does not state how they were selected. If they were chosen because they were "obvious" cases (clear FP or TP), perfect agreement is expected and provides no evidence about reliability on ambiguous cases.
- **n=6 is too small for reliability estimation.** Inter-rater reliability studies typically require n≥30 for stable κ estimates. The authors flag this as a "pilot" (§6.2), but they use κ=1.0 as evidence in the text, which is overstating its weight.

**Concrete fix:** Expand the cross-model dev-reviewer ablation to n≥20 candidates, stratified by difficulty (easy/medium/hard) as judged by an independent human annotator, and report κ with 95% CI. Alternatively, remove the κ=1.0 claim and state: "A preliminary cross-model check on 6 candidates showed agreement on all; a larger reliability study is ongoing."

---

### [Major] W3: The "over-strict concentrates in optional-default APIs" framing is post hoc rationalization.

**Section 6.3, lines 143-144**

The paper states: "Over-strict concentrates in APIs with many optional-default parameters---Milvus and Qdrant's search parameters---which is why the twelve-clause set is Milvus-heavy." This reads as a post hoc explanation for why the probe is Milvus-heavy (9/12) rather than a principled finding. The evidence is weak:

- **No quantitative test.** The paper does not define "optional-default API density" or test the hypothesis that APIs with more optional-default parameters have higher TI rates. The Weaviate expansion (0 over-strict found) is framed as support ("Weaviate documents explicit minimum bounds"), but this is consistent with two competing explanations: (a) Weaviate's documentation is unambiguous, or (b) Weaviate's optional-default parameter density is lower. The paper cannot distinguish these without measuring API density.
- **Single counter-example.** Finding 0 over-strict clauses in Weaviate v1.38.2 is only one data point. To claim "concentrates in optional-default APIs," the paper would need to show that across multiple vendors, TI rate correlates with optional-default API density. The current evidence (Milvus/Qdrant high, Weaviate low) is suggestive but not conclusive.
- **Circular framing risk.** If the 12-clause set was selected because it contained over-strict clauses, and Milvus/Qdrant happened to have more, the "concentrates in" explanation is circular. The paper needs to describe the clause selection process to avoid this.

**Concrete fix:** Either (a) remove the "concentrates in optional-default APIs" claim and reframe as "Our 12-clause probe found over-strict clauses in Milvus and Qdrant but not in Weaviate; further work is needed to determine if this is driven by optional-default API density or other factors"; or (b) quantify optional-default API density across the three vendors and test the correlation with TI rate.

---

### [Minor] W4: RQ3 probe lacks documentation of the clause selection process.

**Section 6.3, lines 143-170**

The paper does not explain how the 12 clauses were chosen from the larger set of GLM-extracted clauses. Were they randomly sampled? Selected because they were "flagged as over-strict"? Chosen to maximize diversity? Without this information, readers cannot assess selection bias. The TI rate of 5/12 is meaningless if the sample was enriched for ambiguous cases.

**Concrete fix:** Add a subsection §6.3.1 "Clause selection procedure" that describes: (a) the total pool of GLM-extracted clauses from Milvus and Qdrant, (b) the sampling strategy (random if possible, otherwise stratified by parameter type), and (c) the number of clauses screened vs. selected.

---

### [Minor] W5: Threats to validity understates the RQ3 generalizability threat.

**Section 6.5, lines 175-177**

The internal validity threat acknowledges that "RQ3 probe is small" but treats it as a single threat alongside external and construct validity. In reality, RQ3's generalizability is the paper's primary validity threat—it undermines the central claim about task-intrinsic errors. The current framing buries this threat among others.

**Concrete fix:** Expand the internal validity threat to two paragraphs: (1) "RQ3 generalizability" with the CI width and selection bias concerns; (2) "Other internal threats" (e.g., no random seed, LLM variance unmeasured).

---

### [Minor] W6: Weaviate expansion result (0 over-strict) is under-analyzed.

**Section 6.3, line 143**

The paper reports that a Weaviate v1.38.2 expansion found 0 over-strict clauses and attributes this to "Weaviate documents explicit minimum bounds." This is a plausible explanation, but the paper does not present evidence: no examples of Weaviate's explicit bounds, no comparison of Weaviate's documentation style to Milvus/Qdrant's. Without this, the explanation is speculative.

**Concrete fix:** Add a footnote or brief example: "For instance, Weaviate's `ef` parameter is documented as 'Must be >= 1', whereas Milvus's `nprobe` is documented as 'optional, default 1'." This concretizes the contrast.

---

## Questions

1. **Power analysis for RQ3:** What is the planned sample size for the "larger head-to-head study" mentioned in §6.3? Will it include Weaviate and other vendors? What TI rate would be sufficiently small to claim that task-intrinsic errors are rare?

2. **Dev-reviewer reliability on ambiguous cases:** The 6-case cross-model check achieved κ=1.0, but were these cases easy or hard? If the authors have an independent difficulty rating, they should report agreement stratified by difficulty.

3. **Clause selection protocol:** Can the authors share the full list of GLM-extracted clauses for Milvus and Qdrant, and indicate which 12 were selected for RQ3? This would allow readers to assess selection bias.

4. **Alternative to TI rate:** Instead of reporting a TI rate (5/12), could the authors report "cross-model validation sensitivity" (7/12 caught) and "source-grounded falsification sensitivity" (12/12 caught)? This frames RQ3 as a comparison of oracle methods rather than a rate estimation problem.

---

## Scores

| Criterion          | Score (1-5) | Justification |
|-------------------|-------------|---------------|
| **Soundness**     | 4           | Methodology is sound, but W1-W3 are statistical power issues that weaken confidence in the core TI claim. RQ2 is solid; RQ3 is underpowered. |
| **Significance**  | 3           | Source-grounded falsification is a significant contribution for API conformance testing, but the TI phenomenon claim is not yet convincingly demonstrated. |
| **Novelty**        | 4           | Task-intrinsic errors as a distinct class from family-specific errors is novel, and the source-grounded counter is well-differentiated from prior REST-API oracle work. |
| **Presentation**  | 4           | Writing is clear; Wilson CIs are reported correctly; the "concentrates in" framing is the main presentation weakness (W3). |
| **Overall**       | **3** (Weak Accept) | The paper has a strong core idea and solid RQ2 evidence, but RQ3 needs more statistical power to support its claims. I recommend Weak Accept with the request that the authors either expand RQ3 or downscope its claims. |

**Confidence:** 4/5. I am familiar with LLM-as-judge reliability research and inter-rater reliability methods, but I am not a domain expert in vector databases.

---

## Recommendation

**Weak Accept.** The authors have addressed Round 8's W1 and W3 in the right direction (expanding the probe, adding cross-model checks), but the evidence remains statistically underpowered. The paper is publishable if the authors either (a) substantially strengthen RQ3, or (b) reframe it as exploratory. I encourage the authors to pursue the "larger head-to-head study" flagged in §6.3 and report it in a future revision.

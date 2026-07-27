# Mock Review: TestVDB (Round 10, Post-Reframe)
## Reviewer 2 (Critical)

**Score Change:** Round 8/9: 3/5 → Round 10: **3/5** (no change)

## Summary

The authors have reframed RQ3 as "(exploratory)" and elevated the vendor-wise distribution to a contribution. While the abstract now accurately cautions that RQ3 is "not a statistical generalization," the core problems I raised in rounds 8 and 9 remain. The refactoring is an honest admission of weakness rather than a solution. Explicitly labeling RQ3 as exploratory does not rescue the claim from its evidentiary deficits—it merely admits them. The "bounded by phenomenon" argument is unconvincing as a defense for not expanding the probe. The distribution finding, while better motivated, remains post-hoc pattern-spotting without a falsifiable prediction.

## Strengths

1. **Honest reframing.** The abstract's explicit disclaimer that RQ3 is "exploratory, not a statistical generalization" is intellectually honest and manages expectations. Section 6.3's opening ("The central claim is that source-grounded falsification resolves task-intrinsic documentation-interpretation errors...; this probe is exploratory, not a statistical generalization") is clear.

2. **Improved contribution C3.** The third contribution now explicitly mentions the exploratory nature and the optional-default API pattern, which is better aligned with the actual evidence.

3. **Source-grounded anchor evidence.** RQ2's controlled retrospective (81% FP suppression, 96.7% TP retention) remains strong and is the paper's methodological core. The single-LLM ablation (25.5% → 45.6% → 69.2% precision) is convincing.

4. **Clearer articulation of the TI layer.** Section 3's two-layer error split (family-specific vs. task-intrinsic) is well-motivated and the distinction is now sharp.

## Weaknesses

### Major 1: "Exploratory" is an admission, not a solution (RQ3 framing)

The authors believe that labeling RQ3 as "(exploratory)" resolves my small-n objection. It does not. It concedes it.

**What changed:** Round 8/9 presented RQ3 as a general claim about the TI phenomenon. Round 10 labels it "exploratory" and adds disclaimers in the abstract and Section 6.3.

**Why it's insufficient:**

- **Scientific status of exploratory findings.** Exploratory findings are hypotheses, not conclusions. They deserve provisional status in a discussion section or a dedicated "exploratory analysis" subsection, not as a full RQ with equal billing to RQ1 (yield: n=111 submissions, 38 acknowledged) and RQ2 (controlled retrospective: n=54 adjudicated). The evidentiary gap is stark: RQ1/2 are on hundreds of adjudicated samples; RQ3 is on twelve clauses.

- **Abstract placement.** The abstract states: "in an exploratory twelve-clause pilot on Milvus and Qdrant, a different family reproduced GLM's over-strict claim in 5." This is appropriate. But then it adds the optional-default pattern: "the over-strict phenomenon concentrates in optional-default APIs (none on Weaviate, whose docs state explicit bounds)." This elevates a post-hoc observation to a contribution-level claim without a predictive model.

- **Contribution C3 language.** The contribution bullet reads: "Task-intrinsic documentation-interpretation errors and the source-grounded counter... [then lists the 5/12 TI rate and optional-default pattern]." The framing blurs the line between a falsifiable claim (source resolves TI errors) and a speculative pattern (optional-default concentration). The latter should be in discussion, not contribution.

- **What "exploratory" actually means.** In a venue like ISSTA/ICSE/FSE, "exploratory" typically means "we found something interesting and are reporting it, but replication is needed before we claim it as a general law." Here, the authors use it as a shield against criticism of n=12. The proper response to a small-n critique is to expand the probe or qualify the claim's scope—not to relabel the RQ and move on.

**Fix:**

1. **Move RQ3 content to Discussion.** Collapse RQ3 into a subsection within §6 (Discussion and Limitations) titled "Exploratory observation on task-intrinsic errors." Present the 12-clause probe as a preliminary finding, not a full RQ. Remove the "(exploratory)" label from the RQ itself—there should be no RQ.

2. **Qualify the optional-default claim.** In Discussion, frame it as a hypothesis for future work: "We observed that over-strict clauses concentrated in APIs with many optional-default parameters (9/12 in our probe). If this pattern holds, it would suggest [mechanism]. Testing this on a larger sample is future work."

3. **Remove optional-default from Contribution C3.** Contribution C3 should read: "Task-intrinsic documentation-interpretation errors and the source-grounded counter. We show that cross-model validation misses [X]% of task-intrinsic errors while source-grounded falsification catches all, on a controlled twelve-clause probe." Stop there. The optional-default pattern does not belong in the contribution.

4. **Add a falsifiable prediction.** If the authors want the optional-default pattern to be taken seriously, they must predict where else it should hold and test it. For example: "We predict that VDBMSs with explicit numeric bounds in documentation (e.g., 'Must be >= 1') will show lower over-strict rates than those with optional-default phrasing." Test this on Weaviate vs. Milvus/Qdrant with a larger sample.

### Major 2: "Bounded by phenomenon" is deflection, not justification (RQ3 sample size)

The authors argue that "scaling to n=30 is bounded by the phenomenon rather than by sampling effort." I find this unconvincing.

**The claim (§6.3):** "which is why the twelve-clause set is Milvus-heavy and why scaling to n=30 is bounded by the phenomenon rather than by sampling effort."

**Why it's problematic:**

- **What does "bounded by the phenomenon" actually mean?** The phrase is vague. Does it mean:
  1. There are only ~30 optional-default parameters across all VDBMSs (supply constraint)?
  2. Over-strict errors are rare and you'd need to mine thousands of docs to find 30 (incidence constraint)?
  3. Something else?

  The paper does not operationalize this. Without a clear definition, it reads as hand-waving to avoid doing the work.

- **Counterargument: Mine more.** If the claim is "over-strict concentrates in optional-default APIs," the straightforward expansion is to mine ALL optional-default parameters across Milvus, Qdrant, and Weaviate. Count them. Test them. Report the over-strict rate. The authors did this for Weaviate (0 over-strict found), so why not do it systematically for all three?

- **Supply vs. incidence.** The authors seem to be arguing that optional-default APIs are rare (supply constraint). But Section 6.3 states: "over-strict concentrates in APIs with many optional-default parameters (Milvus, Qdrant's search parameters)." If there are "many," why stop at 12? A systematic parameter census would settle this.

- **The 95% CI problem remains.** The Wilson interval [19%, 68%] on 5/12 is still too wide to support claims about "concentration" or "absence." Saying "this is exploratory" does not make a wide interval useful—it just means you have no idea what the true rate is.

**Fix:**

1. **Drop the "bounded by phenomenon" line.** It's not needed. If n=12 is a pilot, call it a pilot and say "a larger study is ongoing." Don't invent a phenomenon-based justification.

2. **Do the parameter census.** For Milvus, Qdrant, and Weaviate, count:
   - How many total parameters exist in the search/index APIs?
   - How many are optional-default phrasing?
   - How many have explicit bounds?
   - For each category, what is the over-strict rate?

   This is a table you can build from existing documentation. It costs weeks, not months, and it would settle the supply question. If the total number of optional-default parameters is ~30, say so. If it's ~300, then the "bounded by phenomenon" argument is weak.

3. **Reframe the limitation.** In §6.4 (Threats to validity), you already state: "The RQ3 probe is small (twelve clauses...) and is the most contingent finding." That's sufficient. You don't need the "bounded by phenomenon" defense.

### Major 3: The distribution finding is still post-hoc (vendor-wise pattern)

The elevation of the vendor-wise distribution to a finding (abstract + §6.3) is an improvement over round 9, but it remains pattern-spotting without a causal model.

**The claim:** Over-strict concentrates in optional-default APIs (Milvus 9, Qdrant 3, Weaviate 0). Weaviate's gaps are conformance bugs, not over-formalized clauses.

**Why it's still post-hoc:**

- **No predictive falsification.** The authors observed the pattern *after* mining the 12 clauses. A finding becomes evidence when it predicts something not yet observed. For example: "We predict that any VDBMS with explicit bounds ('Must be >= 1') will show <10% over-strict rate, while those with optional-default phrasing will show >40%." Then test it on a new VDBMS (e.g., MeiliSearch, Chroma, or a different version of Weaviate).

- **The Weaviate control is underexplained.** The paper states: "Weaviate v1.38.2 surfaces no over-strict clauses, because Weaviate documents 'Must be >= 1' for ef, dynamicEfMin, etc." This is a plausible mechanism (explicit bounds prevent over-formalization), but it's not tested. Did the authors *only* find no over-strict clauses because they looked harder? How many optional-default parameters does Weaviate actually have? If the number is small, the pattern is trivial.

- **Causal mechanism is underspecified.** Why would optional-default phrasing lead to over-strict interpretation? The paper implies that LLMs misread "optional, default X" as "must be >= X" rather than "0 means default." Is this a documented LLM bias? The authors should cite prior work on LLM misinterpretation of default-value semantics or test the hypothesis directly.

**Fix:**

1. **Add the mechanism to the abstract.** Change: "the over-strict phenomenon concentrates in optional-default APIs" → "the over-strict phenomenon concentrates in optional-default APIs, possibly because LLMs misinterpret 'optional, default X' as 'must be >= X' rather than '0 selects default'." Flag it as a hypothesis.

2. **Test on a new VDBMS.** Pick MeiliSearch or Chroma (already in scope) and mine their optional-default parameters. Report the over-strict rate. If it's >0, the "Weaviate is special" claim is weakened. If it's 0, the pattern holds.

3. **Add a parameter table.** In the artifact or appendix, list:
   - For each VDBMS: total search/index parameters, optional-default count, explicit-bound count.
   - Over-strict rate per category.
   This would make the concentration claim quantitative rather than anecdotal.

### Minor 1: Inconsistent capitalization of "optional-default"

Throughout the paper, "optional-default" appears with and without hyphens. Standardize on "optional-default" (hyphenated) as a compound adjective.

**Fix:** Global search-and-replace to enforce consistency.

### Minor 2: Table 2 caption clarity

Table 2 caption: "Cross-model judging vs source-grounded falsification on twelve GLM over-strict clauses (nine Milvus + three Qdrant v1.18.2, live-probe-confirmed)."

**Issue:** It doesn't explicitly state which columns are which, though the table layout makes it obvious. For accessibility, spell it out.

**Fix:** "Cross-model judging vs source-grounded falsification on twelve GLM over-strict clauses... Columns: Over-strict clause, TI (task-intrinsic), Cross-model judging result, Source-grounded result."

### Minor 3: Section 6.3 opening is slightly defensive

The first sentence of §6.3: "The central claim is that source-grounded falsification resolves task-intrinsic documentation-interpretation errors that cross-model validation cannot; this probe is exploratory, not a statistical generalization."

**Issue:** "The central claim is..." reads as a defensive pre-emption against criticism. You're stating your claim, but the "central" framing is unnecessary.

**Fix:** Remove "The central claim is." Just state: "Source-grounded falsification resolves task-intrinsic documentation-interpretation errors that cross-model validation cannot. The probe below is exploratory..."

## Questions

1. **Parameter census.** How many total optional-default parameters exist across Milvus, Qdrant, and Weaviate search/index APIs? You report 12 tested (9 Milvus, 3 Qdrant). Is the total supply ~15, ~50, or ~150? This is critical for evaluating the "bounded by phenomenon" argument.

2. **Weaviate's parameter profile.** You state Weaviate has "explicit bounds" (e.g., "Must be >= 1"). Does Weaviate have *any* optional-default parameters? If so, how many? If not, why not? This would clarify whether Weaviate is genuinely different or just has a different documentation style.

3. **Prediction for new VDBMS.** If I gave you a new VDBMS with 50 optional-default parameters and 20 explicit-bound parameters, what over-strict rate would you predict for each category? The paper doesn't give enough to make a quantitative prediction.

4. **Cross-model validation design.** In RQ3, you used DeepSeek as the second model. Why DeepSeek? Was it chosen *a priori* for diversity, or *post hoc* for performance? The paper should discuss model selection criteria.

## Scores

**Soundness: 3/5** — RQ1 and RQ2 are sound with strong evidence (n=111 submissions, controlled retrospective). RQ3 is weak: n=12, wide CI, post-hoc pattern. The exploratory framing is honest but doesn't fix the evidentiary deficit.

**Significance: 3/5** — Source-grounded falsification is a significant methodological contribution. The TI phenomenon, if real, is important. But the evidence for TI is too weak to carry the significance weight the paper assigns to it.

**Novelty: 4/5** — Source-grounded falsification is novel and distinct from prior REST-API oracle work. The two-layer error split (family-specific + task-intrinsic) is a good contribution.

**Presentation: 4/5** — The writing is clear and the reframing is honest. The paper manages expectations well. The "bounded by phenomenon" line is the only murky spot.

**Overall: 3/5** — No change from round 8/9. The paper has a strong methodological core (RQ1, RQ2) and a promising observation (RQ3), but the evidence for RQ3 remains thin. Labeling it "exploratory" doesn't make it publication-ready as a full RQ.

**Confidence: 4/5** — I am confident in my assessment of the evidence gap in RQ3. I am less confident about the "bounded by phenomenon" interpretation because the paper doesn't define it clearly.

## Verdict

**Weak Accept (with revisions).**

The paper's core contribution—source-grounded falsification and its demonstrated effectiveness (RQ2)—is strong enough to warrant publication. The RQ3 exploratory finding is interesting but under-evidenced. I recommend the authors:

1. **Demote RQ3 to a Discussion subsection.**
2. **Add a parameter census** (total optional-default vs. explicit-bound counts).
3. **Make a falsifiable prediction** about the optional-default pattern.
4. **Drop the "bounded by phenomenon" line** or operationalize it clearly.

With these changes, the paper would be a **4/5** for me. As it stands, it's a **3/5** with significant merit.

---

**Meta-comment:** I appreciate the authors' honesty in reframing RQ3 as exploratory. That level of intellectual integrity is rare. My critique is not about the refraction being dishonest—it's about it being insufficient. The right move is to treat RQ3 as a hypothesis-generation exercise and publish it as such, not as a full RQ with equal billing to well-supported claims.

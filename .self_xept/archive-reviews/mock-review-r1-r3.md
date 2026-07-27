# Mock Review: TestVDB

**Reviewer:** R1 (simulated ICSE/FSE/ISSTA reviewer)  
**Date:** 2026-07-16  
**Venue target:** SE top-tier (ICSE/FSE/ISSTA)

## Summary

This paper presents TestVDB, a source-grounded falsification approach for detecting API conformance defects in Vector Database Management Systems (VDBMSs). The authors identify that ~85% of VDBMS defects are "conformance defects" where systems silently accept inputs violating documented contracts (e.g., `nprobe=0`, `ef=0`). These are unreachable by classical oracles (crash detection, differential testing, metamorphic relations, property-based testing) because they require semantic judgment against natural-language contracts.

The core contribution is framing this as an "LLM-as-oracle setting" where a language model must both extract contracts and judge conformance. The authors identify two error layers: family-specific bias (mitigated by cross-model validation) and task-intrinsic errors (where ambiguous documentation leads multiple LLM families to infer the same wrong contract). For the latter, they propose "source-grounded falsification" — treating LLM-derived contracts as refutable hypotheses and using source code as ground truth.

**Empirical results:** TestVDB surfaced 111 candidate issues across 5 VDBMSs, with 38 maintainer-acknowledged defects. A controlled retrospective shows source-grounded falsification suppresses 81% of false positives (up from 31%) while retaining 96.7% true positives. A pilot study on 9 Milvus clauses shows cross-model validation misses task-intrinsic errors (0/2 caught) while source-grounded falsification catches all 9.

## Strengths

**1. Clear problem framing with strong empirical motivation.** The 85% residual figure is compelling, and Table 1 effectively maps where each classical oracle fails. The distinction between conformance vs. correctness is clean, and the VDBMS domain is timely given the LLM retrieval boom.

**2. Conceptual contribution: The LLM-as-oracle setting.** Section 3 crisply separates this work from prior REST-API oracle work (AGORA+, SATORI, MASTOR) by identifying where deterministic assertions are impossible. This boundary is real and previously unnamed in the literature.

**3. Honest scoping of the pilot study (RQ3).** The authors explicitly state the nine-clause probe is small and treat it as a pilot pending larger study. The threat-to-validity section flags this as the most contingent finding. This transparency builds trust.

**4. Strong source-grounded falsification results.** The precision improvement (81% vs. 31% false positive suppression) is substantial and statistically grounded (Wilson CI). The ablation cascade (25.5% → 45.6% → 69.2%) clearly shows where value comes from.

**5. Reusable model-free invariant oracle subclass.** The COSINE bounds and index completeness checks are independently valuable and orthogonal to the LLM pipeline.

## Weaknesses

### [Major] M1: Conceptual contribution extent is unclear

**Evidence:** Section 3 claims "LLM-as-oracle setting" as a conceptual contribution, but the core novelty appears to be the *combination* of three existing ideas:
- LLM-as-judge (well-established in general NLP)
- Cross-model validation to mitigate self-preference (standard technique)
- Source as ground truth for falsification (standard in testing)

The "LLM-as-oracle setting" framing is valuable, but it reads as a categorization rather than a novel insight. The paper does not formally characterize this setting beyond the definition in §3.1. No theoretical framework distinguishes which problems belong to this setting vs. others.

**Fix:** Strengthen the conceptual contribution by either:
- (a) Formalizing the setting with a decision tree or properties that characterize when a problem belongs to it, or
- (b) Repositioning §3 as a "problem categorization" rather than a primary contribution, focusing the novelty claim on the source-grounded falsification mechanism itself.

### [Major] M2: Selection bias in the 85% residual quantification

**Evidence:** §6.1 (RQ1) states "about 85% of the issues we submitted are, by this classification, conformance defects" but acknowledges "this composition reflects what TestVDB is designed to surface, not the true defect distribution." The 85% figure is central to the paper's motivation (Abstract, Introduction, Table 1), yet it is based on a sample heavily biased by TestVDB's design.

The paper uses this figure to claim classical oracles miss the "large majority" of conformance defects. But if TestVDB is optimized for conformance defects, the 85% is a design artifact, not a domain property. No attempt is made to estimate the true distribution (e.g., capture-recapture, unbiased sampling).

**Fix:** Either:
- (a) Downplay the 85% as an observed residual in TestVDB's output rather than a claim about the true defect distribution, or
- (b) Add a structured estimate (even a simple capture-recapture on Milvus) to bound the true conformance defect prevalence.

### [Major] M3: E2 (N=9) pilot is underpowered for the central claim

**Evidence:** The task-intrinsic vs. family-specific error split is the paper's central mechanistic claim. Yet the evidence is a pilot on 9 clauses from a single system (Milvus). The binomial uncertainty is large: catching 0/2 task-intrinsic errors with cross-model validation could be consistent with a 30-50% catch rate at this sample size.

The paper treats this as a pilot (acknowledged in threats), but the claim appears prominently in the abstract, contributions list, and RQ3. A reviewer expecting SE top-tier rigor would expect at least 20-30 clauses across 2-3 systems for a claim of this centrality.

**Fix:** Either:
- (a) Expand the pilot to a proper study (20+ clauses, 2+ VDBMSs), or
- (b) Reduce the claim prominence and explicitly label it as "preliminary evidence suggesting..." rather than a core contribution.

### [Major] M4: Classical-oracle baseline is weak

**Evidence:** RQ1 claims "classical-oracle suite" found no violations on Qdrant v1.18.2, but the suite is only "a metamorphic relation set (distance symmetry, top-k monotonicity, the COSINE bound, self-similarity)." This is not a comprehensive classical-oracle baseline.

Missing from the comparison:
- **Crash oracle:** VDBFuzz is cited but not run as a controlled baseline. The head-to-head in §6.1 is on a different version and not systematic.
- **Differential testing:** The paper says differential testing "cannot adjudicate accept/reject" but provides no empirical evidence attempting it (e.g., cross-vendor probes).
- **Property-based testing:** Schemathesis/QuickREST are cited as inapplicable due to lack of OpenAPI, but no attempt is made to test this claim (e.g., hand-crafting a schema for Milvus).

The VDBFuzz head-to-head (0 crashes vs. conformance defects) supports complementarity but does not prove classical oracles miss conformance defects systematically.

**Fix:** Strengthen the classical-oracle evaluation by either:
- (a) Running VDBFuzz/NoREC/TLP/DQE-style oracles on the same versions as TestVDB and reporting yield, or
- (b) Reducing the exclusion claim to "by construction, these oracles cannot reach accept/reject decisions" (theoretical argument) and removing empirical baseline pretense.

### [Major] M5: MASTOR/AGORA+/SATORI distinction is under-argued

**Evidence:** §3.1 claims prior work "avoids this setting by keeping deterministic, executable assertions." But Table 1 and §7 suggest a spectrum:
- AGORA+ (dynamic invariants from traces) → deterministic
- SATORI (LLM reads OpenAPI) → deterministic  
- MASTOR (multi-agent over source) → closer to TestVDB

The paper argues MASTOR "tests what the implementation does" while TestVDB "tests what the documentation prescribes," but both use source as ground truth. The distinction appears to be:
- MASTOR: source → oracle (encode implemented behavior)
- TestVDB: doc → LLM-derived contract → source falsifies it

This is a real difference, but the paper claims MASTOR "cannot detect a gap between documentation and code." If MASTOR reads source to generate oracles about implemented behavior, it seems it could detect doc-code gaps by comparing doc-derived oracles to source-derived oracles. The distinction needs clearer exposition.

**Fix:** Clarify the MASTOR/TestVDB boundary by:
- (a) Adding a concrete example showing where MASTOR would miss a defect TestVDB catches (or vice versa), or
- (b) Rephrasing to acknowledge MASTOR operates in a neighboring setting rather than claiming strict separation.

### [Minor] m1: Abstract overclaims the "task-intrinsic" evidence

**Evidence:** Abstract states "cross-model judging misses the task-intrinsic subset (0/2)" but this is from the N=9 pilot. A reader would expect this evidence to be robust before appearing in the abstract.

**Fix:** Rephrase abstract to "in a pilot study on nine clauses, cross-model judging missed both task-intrinsic errors."

### [Minor] m2: "LLM-as-oracle" terminology conflation

**Evidence:** The paper uses "LLM-as-oracle" to mean both:
- LLM as semantic judge (no deterministic assertion possible)
- LLM as contract extractor and judge (TestVDB's specific pipeline)

This conflation blurs the boundary between the setting (general) and the method (specific).

**Fix:** Distinguish terminology: "LLM-as-oracle setting" (general) vs. "LLM-as-judge pipeline" (TestVDB's instantiation).

### [Minor] m3: No recall estimation

**Evidence:** §6 acknowledges "we do not estimate recall because there is no public ground-truth defect catalog." This is a standard limitation, but the paper provides no bounding argument (e.g., manual inspection of a sample of rejected candidates, or capture-recapture with another method).

**Fix:** Add even a weak recall bound (e.g., "we estimate recall ≥ X% because a manual sample of Y rejected candidates showed Z% were likely true positives").

## Questions

1. **On the LLM-as-oracle setting:** Could you formalize this setting with decision criteria? When is a problem "in" vs. "out" of this setting? What properties distinguish it from classical oracle problems?

2. **On the 85% residual:** You acknowledge this reflects TestVDB's design bias. Do you have any evidence (even a simple capture-recapture on Milvus) to bound the true conformance defect prevalence?

3. **On the E2 pilot:** What would it take to scale this to 20-30 clauses across 2-3 VDBMSs? Is this a planned extension or a fundamental limitation (e.g., access to source, manual annotation cost)?

## Scores

| Dimension | Score (1-5) | Rationale |
|-----------|-------------|------------|
| **Soundness** | 4 | Methodology is sound, threats acknowledged, but classical-oracle baseline is weak (M4) and E2 pilot underpowered (M3). |
| **Significance** | 4 | VDBMS conformance is a timely, important problem; 38 acknowledged defects is real impact. Limited by 85% selection bias (M2). |
| **Novelty** | 3 | LLM-as-oracle setting is a useful categorization but feels incremental over existing LLM-as-judge + source-falsification ideas. Source-grounded falsification is novel but narrowly scoped. |
| **Presentation** | 4 | Clear structure, good tables, honest threat disclosure. Some terminology conflation (m2) and MASTOR distinction needs work (M5). |
| **Overall** | **Accept** | The problem is real, the approach is sensible, and the empirical results are substantive enough for acceptance. The major weaknesses are about calibration of claims rather than fatal flaws. AnAccept verdict assumes the authors will tone down the 85% residual claim and expand the E2 pilot or reduce its prominence. |

**Confidence:** 4 (familiar with VDBMS testing, LLM-as-judge literature, and SE research standards)

---

**Recommendation:** Accept pending revisions on M1-M5, particularly M2 (85% residual framing) and M3 (E2 pilot scope).

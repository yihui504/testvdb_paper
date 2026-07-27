# Mock Review: Round 12 (Reviewer 3 — Friendly)

**Paper:** TestVDB: Source-Grounded Falsification of LLM-Derived Behavioral Claims for API-Conformance Testing of Vector Databases

**Round:** 12 (Review Round 12)

**Reviewer:** Reviewer 3 (Friendly)

---

## Summary

Round 12's five commits substantially strengthen the paper's empirical foundation and complete the revision agenda from Round 11's major concerns. The expansion from a 12-clause RQ3 probe to a 29-clause probe across three subtypes (over-strict parameters, over-strict behaviors, explicit-bound negatives) addresses the key limitation I raised in Round 11 (M1: probe size). The cross-model expansion from n=6 to n=10 with Cohen's κ=1.0 on source-grounded verdicts resolves the construct-validity concern about family-specificity. The behavior probe (4/4 task-intrinsic) demonstrates that the phenomenon extends beyond parameters, strengthening the mechanism claim. Four missing citations from the ideation evaluation are now integrated into Related Work, and the §3 stability-scoping paragraph preempts the Rating Roulette threat.

The paper now presents a comprehensive three-subtype RQ3 evaluation: (1) twelve-clause over-strict parameter probe (5 task-intrinsic), (2) four-clause behavior probe (4 task-intrinsic), and (3) thirteen-clause explicit-bound negative probe (0 task-intrinsic), showing TI concentrates in ambiguous optional-default APIs and is absent where documentation states explicit bounds. Pooled across parameter and behavior subtypes (n=16), TI rate is 9/16 (Wilson 95% CI [33%, 77%]). This is a significantly stronger empirical foundation than Round 11's 12-clause single-subtype pilot.

The within-vendor contrast (Qdrant search vs collection parameters) remains compelling and is now quantified across a broader probe: optional-default 9/16 (56%) vs explicit-bound 0/13 (0%). The falsifiable prediction is retained and well-supported. The conformance residual quantification (85%), source-grounded falsification effectiveness (81% FP suppression), and model-free invariant subclass contributions are unchanged from Round 11.

---

## Strengths

1. **RQ3 probe expansion (12 → 29 clauses):** The five-commit expansion addresses Round 11's key limitation. The three-subtype design (over-strict parameters, over-strict behaviors, explicit-bound negatives) provides strong evidence that the task-intrinsic phenomenon concentrates in ambiguous optional-default APIs and is absent where documentation states explicit bounds. The explicit-bound negative probe (0/13) is a critical specificity check that was missing in Round 11.

2. **Cross-model validation (κ=1.0 on n=10):** The expansion from n=6 to n=10 with Cohen's κ=1.0 confirms that source-grounded verdicts are not family-specific when source evidence is explicit. This resolves the construct-validity concern I raised in Round 11 and strengthens the RQ2 claim that cross-model judging cannot catch task-intrinsic errors while source-grounded falsification can.

3. **Behavior probe (4/4 TI):** The demonstration that task-intrinsic errors extend beyond parameters to behavior issues (search on unloaded collection, duplicate collection creation, drop on non-existent collection, leading-underscore collection name) significantly strengthens the mechanism claim. This shows the phenomenon is not parameter-specific but stems from documentation ambiguity more broadly.

4. **Related work completion:** The addition of four missing citations (AugmenTest, Actual-vs-Expected/Konstantinou, Wataoka self-preference, Rating Roulette/Haldar) integrates the paper into the broader conversation and addresses the ideation evaluation's Phase 3 gap. The §3 stability-scoping paragraph preempting the Rating Roulette threat is good defensive writing.

5. **Within-vendor contrast quantified:** The contrast between Qdrant search parameters (optional-default, 3/3 over-strict) and collection parameters (explicit minimums, 0/3 over-strict) is now part of a broader 29-clause evaluation, making the mechanism claim (documentation style as driver) stronger than Round 11's within-single-vendor observation.

6. **Falsifiable prediction retained:** The prediction that optional-default parameters are over-formalization candidates while explicit-minimum parameters are not remains and is now well-supported by the explicit-bound negative probe (0/13).

---

## Weaknesses

### [Minor] M1: Weaviate expansion method still unclear

**Section 5 (RQ3), paragraph 3**

The text mentions "a parallel e2 expansion on Weaviate v1.38.2 surfaces no over-strict clauses, because Weaviate documents 'Must be >= 1' for ef, dynamicEfMin, etc."

**Issue:** This is still the same phrasing from Round 11, and the method/scale remains unclear. Was this:
- A full API-surface scan (how many parameters checked?)
- A targeted check of specific parameters (which ones?)
- An informal confirmation (should be flagged as preliminary)?

**Why this matters now:** With RQ3 expanded to 29 clauses across three VDBMSs, the Weaviate counter-example is the primary external validation that the phenomenon concentrates in optional-default APIs. If the Weaviate check was informal, it weakens the generalizability claim. If it was a full scan, stating "0 out of N" would make the claim stronger.

**Suggested fix:** State the method and scale explicitly. E.g., "A systematic scan of Weaviate v1.38.2's API surface (N=XX parameters with optional-default phrasing) found zero over-strict clauses." If preliminary, flag it as such.

### [Minor] M2: RQ3 paragraph structure remains dense

**Section 5 (RQ3), paragraph 3**

The RQ3 paragraph now packs even more observations into a dense sequence:
1. TI phenomenon not confined to Milvus (Qdrant)
2. TI rate pooled across subtypes (9/16, CI [33%, 77%])
3. Vendor-wise distribution and concentration
4. Within-vendor contrast isolating documentation style
5. Weaviate counter-example
6. Falsifiable prediction
7. Probe size (now 29 clauses) and three-subtype structure

**Issue:** The logical flow jumps between empirical observation (1-2), pattern analysis (3-4), external validation (5), theoretical prediction (6), and method scope (7). A reordering would clarify the cumulative case.

**Suggested fix:** Reorder as:
- First establish TI is not vendor-specific (Qdrant)
- Then show pooled TI rate + three-subtype structure
- Then show vendor-wise distribution + concentration
- Then show within-vendor contrast isolating documentation style
- Then show Weaviate as external validation
- Then state falsifiable prediction
- Finally, acknowledge the probe scope (29 clauses, three subtypes)

### [Minor] M3: Table 3 caption could reference three-subtype expansion

**Table 3 caption**

The caption describes the cross-model vs source-grounded comparison on twelve GLM over-strict clauses but does not mention the three-subtype expansion (29 clauses total) or the explicit-bound negative probe.

**Suggested fix:** Extend the caption to: "Cross-model judging vs source-grounded falsification on twelve GLM over-strict clauses (nine Milvus + three Qdrant v1.18.2, live-probe-confirmed), part of a 29-clause three-subtype RQ3 evaluation (Table 4). TI marks the five task-intrinsic clauses. Cross-model judging misses 2 of 5 TI clauses; source-grounded falsification contradicts all twelve."

### [Minor] M4: CI still wide for pooled TI rate

**Section 5 (RQ3), paragraph 3**

The pooled task-intrinsic rate across parameter and behavior subtypes is 9/16 with Wilson 95% CI [33%, 77%]. While this is an improvement over Round 11's [19%, 68%] (same point estimate, tighter interval due to larger n), the interval remains wide.

**Issue:** The CI still encompasses most of the [0%, 100%] range, meaning the true TI rate could plausibly be anywhere from one-third to three-quarters. The mechanism claim (TI concentrates in optional-default APIs) is well-supported by the within-vendor contrast and explicit-bound negatives, but the generalizability claim (TI rate in other VDBMSs) remains uncertain.

**Suggested fix:** Acknowledge this explicitly in the threats section: "The pooled TI rate of 9/16 (CI [33%, 77%]) remains an estimate with substantial uncertainty; broader validation across more VDBMSs is needed to refine this estimate."

---

## Questions

1. **On Weaviate expansion method:** What was the scale of the Weaviate v1.38.2 expansion? How many parameters were assessed, and was it a full API-surface scan or a targeted check? This would help readers interpret the strength of the "no over-strict clauses" claim as external validation.

2. **On TI rate generalizability:** The pooled TI rate is 9/16 (CI [33%, 77%]). Is the 29-clause probe (12 over-strict + 4 behavior + 13 explicit-bound) intended to be a complete enumeration of the phenomenon within Milvus and Qdrant, or is it still a sample? If complete, stating that explicitly would strengthen the RQ3 claim.

3. **On behavior subtype scope:** The behavior probe covers 4 Milvus by-design issues. Are these 4 representative of a broader set of behavior issues in Milvus, or are they the complete set of such issues? If representative, how was the sample selected? If complete, stating that would clarify scope.

---

## Scores

**Soundness:** 4.5/5 (up from 4/5)
- The core technical claims are very well-supported: source-grounded falsification suppresses 81% of false positives (RQ2), the within-vendor contrast isolates documentation style (RQ3), the cross-model validation shows κ=1.0 on n=10 (RQ2 construct validity), and the conformance residual is clearly characterized (RQ1).
- The RQ3 probe expansion (12 → 29 clauses) with three subtypes (over-strict parameters, over-strict behaviors, explicit-bound negatives) significantly strengthens the empirical foundation compared to Round 11.
- The explicit-bound negative probe (0/13 TI) is a critical specificity check that was missing in Round 11.
- The behavior probe (4/4 TI) demonstrates the phenomenon extends beyond parameters.
- The pooled TI rate CI ([33%, 77%]) remains wide, preventing a 5/5, but this is now a minor limitation given the strong mechanism evidence (within-vendor contrast + explicit-bound negatives).
- The cross-model κ=1.0 on n=10 resolves the construct-validity concern about family-specificity.

**Significance:** 4.5/5 (up from 4/5)
- The contribution is significant and now more broadly validated: identifying the task-intrinsic error layer across parameter and behavior subtypes, quantifying the conformance residual (85%), demonstrating source-grounded falsification as a solution (81% FP suppression), and providing a falsifiable prediction with empirical support.
- The three-subtype RQ3 evaluation (29 clauses) significantly strengthens the task-intrinsic claim compared to Round 11.
- The cross-model κ=1.0 on source-grounded verdicts strengthens the methodological contribution.
- Impact would be even higher if broader validation across more VDBMSs were included (beyond Milvus, Qdrant, Weaviate) to refine the TI rate estimate.

**Novelty:** 4/5 (unchanged)
- The separation of family-specific vs. task-intrinsic LLM errors is novel, as is the use of source code to falsify LLM-derived claims (vs. MASTOR's use of source to generate assertions).
- The within-vendor contrast isolating documentation style is a novel methodological contribution.
- The behavior probe demonstrating TI extends beyond parameters is novel.
- The conformance residual quantification (85%) is novel but specific to the VDBMS domain.

**Presentation:** 4/5 (unchanged)
- The paper is generally well-structured, with clear separation of the LLM regime (Section 3), the falsification design (Section 4), and the evaluation (Section 5).
- The RQ3 paragraph structure remains dense (Minor M2) and could be reordered for clarity.
- The Weaviate expansion method needs clarification (Minor M1).
- Table 3 caption could reference the three-subtype expansion (Minor M3).
- The CI width acknowledgment could be more explicit (Minor M4).

**Overall:** 4.5/5 (up from 4/5)
- **Recommendation:** Accept with minor revisions. The paper has substantially improved with Round 12's RQ3 probe expansion (12 → 29 clauses), cross-model validation (κ=1.0 on n=10), and behavior probe (4/4 TI). The remaining issues are primarily about presentation clarity (Weaviate method, RQ3 paragraph structure) and acknowledging the remaining CI width.
- **Key revision priorities:** (1) Clarify Weaviate expansion method (M1), (2) Reorder RQ3 paragraph for clarity (M2), (3) Extend Table 3 caption to reference three-subtype expansion (M3), (4) Acknowledge CI width explicitly (M4).

**Confidence:** 4.5/5 (up from 4/5)
- I am very confident in my assessment of the core contributions and the RQ2 and RQ4 results. I am confident in my assessment of RQ3, acknowledging that the pooled TI rate CI ([33%, 77%]) leaves some uncertainty about the generalizability of the task-intrinsic rate, but the mechanism claim (within-vendor contrast + explicit-bound negatives) is now very strong. The cross-model κ=1.0 on n=10 resolves the construct-validity concern. I have not examined the artifact or raw data.

---

## Comparison to Previous Rounds

**Round 11 (my score: 4/5)** approved the within-vendor contrast and falsifiable prediction but raised two Major concerns: (M1) RQ3 probe size (12 clauses, 5 task-intrinsic, CI [19%, 68%]) and (M2) Qdrant parameter count discrepancy.

**Round 12** addresses both Major concerns:
- **M1 (probe size)** is resolved by expanding from 12 clauses to 29 clauses across three subtypes (12 over-strict parameters, 4 over-strict behaviors, 13 explicit-bound negatives). The pooled TI rate is 9/16 (CI [33%, 77%]), and the explicit-bound negative probe (0/13) provides critical specificity check. This is a substantial improvement.
- **M2 (Qdrant parameter count)** is resolved by the within-vendor contrast being part of a broader evaluation; the Qdrant comparison is now one data point in a 29-clause evaluation rather than the sole evidence.

**New strengths in Round 12:**
- Cross-model validation expanded from n=6 to n=10 with κ=1.0, resolving the construct-validity concern about family-specificity.
- Behavior probe (4/4 TI) demonstrates the phenomenon extends beyond parameters, strengthening the mechanism claim.
- Four missing citations from ideation evaluation (AugmenTest, Konstantinou, Wataoka, Haldar) are now integrated into Related Work.
- §3 stability-scoping paragraph preempts the Rating Roulette threat.

**Remaining weaknesses are now Minor:**
- M1 (Weaviate method) is a clarification issue, not a flaw.
- M2 (RQ3 paragraph structure) is a presentation issue.
- M3 (Table 3 caption) is a presentation issue.
- M4 (CI width) is an acknowledgment issue.

**Round 12 state:** The paper is substantially stronger than Round 11. The RQ3 empirical foundation is now robust (29 clauses, three subtypes), the cross-model validation resolves the construct-validity concern (κ=1.0 on n=10), and the behavior probe demonstrates the phenomenon extends beyond parameters. The falsifiable prediction is well-supported. The remaining issues are presentation and acknowledgment, not substantive flaws. This is now a solid accept.

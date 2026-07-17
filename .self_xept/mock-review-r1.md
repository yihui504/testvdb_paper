## Summary

The paper addresses API conformance testing for Vector Database Management Systems (VDBMSs), targeting a class of defects where systems silently accept inputs violating their documentation (e.g., out-of-range parameters like `nprobe=0`, `ef=0`). The authors argue that approximately 85% of conformance defects are unreachable by classical oracles (differential, metamorphic, property-based) because accept/reject decisions are documented in natural language rather than formal specifications. They propose TestVDB, which uses an LLM to extract behavioral claims from documentation and judges conformance, then falsifies these claims against source code to address LLM interpretation errors. Across five VDBMSs, TestVDB surfaced 111 candidate issues with 38 maintainer-acknowledged defects; a controlled retrospective shows source-grounded falsification suppresses 81% of false positives (up from 31%) while retaining 96.7% of true positives. The core contribution is identifying and addressing "task-intrinsic" documentation-interpretation errors that cross-model validation cannot catch, through source-grounded falsification.

## Strengths

1. **Clear problem framing with quantitative motivation** (Table 1, Section 3): The paper systematically maps where classical oracles fail on the conformance defect residual. The 85% figure (38 acknowledged defects classified) provides concrete scope for the problem space, and the exclusion analysis (Table 1) is methodical.

2. **Empirically grounded two-layer reliability model** (Section 4): The separation of family-specific vs. task-intrinsic LLM errors is well-motivated. The nine-clause Milvus probe (Table 2) provides direct evidence: cross-model judging caught 6/9 over-strict clauses but missed both task-intrinsic ones, while source-grounded falsification caught all 9. This isolates where source adds value beyond cross-model validation.

3. **Substantial real-world evaluation** (Section 6): 111 submitted issues across five VDBMSs with 38 maintainer-acknowledged defects provides meaningful scale. The acknowledgment rate (34.2% overall, 43.1% on Milvus, 50% on Qdrant) indicates the surfaced issues are non-trivial. The controlled retrospective (54 adjudicated candidates) with Wilson 95% CI [55.7%, 80.1%] precision is rigorous.

4. **Clear positioning against prior work** (Section 7): The paper carefully distinguishes its setting from REST-API oracle work (AGORA+, SATORI, MASTOR), explaining why those approaches don't transfer: they extract from structured sources (OpenAPI, traces, source) where constraints are explicit, whereas VDBMS documentation is ambiguous natural language requiring interpretation. The contrast with MASTOR is particularly sharp: MASTOR tests what the implementation does (source as reference), while TestVDB tests what documentation prescribes (source as actual-behavior reference).

5. **Rigorous ablation and threat analysis** (Section 6, Table 2, RQ2): The single-LLM (25.5% precision) → single-source-cycle (45.6%) → full-multi-agent-with-source (69.2%) progression cleanly shows where precision gains come from. The threats-to-validity section is explicit about the small RQ3 probe being the most contingent finding.

## Weaknesses

1. **[Major] Small sample for the central task-intrinsic claim** (Section 6, RQ3): The nine-clause Milvus probe (Table 2) is the primary evidence that cross-model validation misses task-intrinsic errors. The paper treats this as a "pilot," but without a larger study, the 2/9 task-intrinsic fraction (22%) is highly contingent. A binomial confidence interval on 2/9 would be wide (approximately [3%, 60%] at 95% CI), and generalization to other VDBMSs or documentation patterns is speculative. Fix: Expand the probe to 30+ clauses across Milvus and at least one additional VDBMS, or clearly frame this as an initial finding requiring further validation.

2. **[Major] Unclear construct validity for "task-intrinsic" classification** (Section 4, RQ3): The paper defines task-intrinsic errors as those where "a different family independently reproduces the over-strict clause" (line 88), but the operational procedure is not fully specified. Did the second family (DeepSeek) reproduce the clause *verbatim*, or was there semantic equivalence judgment involved? If semantic judgment was required, who judged it—another LLM or a human? If another LLM, the classification may itself be LLM-dependent. Fix: Specify the exact decision procedure for classifying a clause as task-intrinsic, including who/what determines "reproduces" and whether inter-rater reliability was measured.

3. **[Major] Selection bias threat under-specified** (Section 6, RQ1): The paper states "This composition reflects what TestVDB is designed to surface, not the true defect distribution" (line 118), but doesn't quantify the selection bias. TestVDB targets documentation-specified constraints, so it will naturally find conformance defects. However, without a random defect sample or capture-recapture estimation, the 85% conformance residual cannot be interpreted as a population parameter. Fix: Add a sentence estimating the selection bias direction (e.g., "TestVDB is biased toward finding conformance defects, so the 85% residual likely overestimates the true population fraction") or conduct a capture-recapture study if feasible.

4. **[Minor] No statistical testing on precision gains** (Section 6, RQ2): The paper reports 81% FP suppression with source vs. 31% without, but does not test whether this difference is statistically significant. Given n=54 adjudicated candidates, McNemar's test or a similar paired test could assess significance. Fix: Add a statistical significance test (e.g., McNemar's test on the paired before/after FP suppression) or a confidence interval on the 81% vs. 31% difference.

5. **[Minor] Threat to internal validity on "task-intrinsic" probe scope** (Section 6, Threats): The paper notes the RQ3 probe is small and Milvus-specific, but doesn't address whether the nine clauses were selected randomly or cherry-picked. If they were selected because the authors already suspected they were task-intrinsic, the probe may overestimate the phenomenon's prevalence. Fix: Specify the selection procedure for the nine clauses (random sample from all over-strict clauses? purposively selected?) and, if purposive, acknowledge the selection bias explicitly.

6. **[Minor] No discussion of computational cost beyond raw LLM calls** (Section 5): The paper reports "on the order of $10^4$ LLM calls and roughly $\$10$ per target" (line 110), but doesn't break down where time/cost goes (e.g., what fraction is dev-reviewer source-reading vs. attack generation vs. live API probes). Fix: Add a brief cost breakdown (e.g., "60% dev-reviewer, 20% attack agents, 20% live probes") to help readers assess scalability.

## Questions for Authors

1. **RQ3 generalization:** The nine-clause Milvus probe is the key evidence for task-intrinsic errors. Do you have plans (or preliminary data) from a larger study—either more clauses in Milvus or clauses from another VDBMS—that would strengthen confidence that this phenomenon generalizes beyond the initial pilot?

2. **Task-intrinsic classification procedure:** You define task-intrinsic as when a second family "independently reproduces the over-strict clause." Was this reproduction verbatim, or did you allow semantic equivalence? Who made the equivalence judgment, and did you measure inter-rater reliability if multiple humans were involved?

3. **Selection bias quantification:** You acknowledge that the 85% conformance residual reflects TestVDB's design rather than the true distribution. Have you considered (or could you add) a simple capture-recapture estimate or a random defect sample to bound the population fraction, even roughly?

## Scores

- **Soundness:** 4/5 — The method is technically sound and the evaluation is rigorous, but the central task-intrinsic claim rests on a small sample (nine clauses) that limits confidence in generalization. The controlled retrospective and ablation study are solid, but the construct validity for task-intrinsic classification could be sharper.

- **Significance:** 4/5 — The problem is real and the solution (source-grounded falsification) addresses a genuine gap in LLM-as-judge reliability. The 85% conformance residual quantifies a meaningful limitation of classical oracles, and the approach is reusable beyond VDBMSs (as acknowledged in Discussion). The impact would be higher with stronger evidence for task-intrinsic errors.

- **Novelty:** 4/5 — The separation of family-specific vs. task-intrinsic LLM errors is novel, and the use of source to falsify LLM-derived claims (rather than as the oracle itself, as in MASTOR) is a clear advance over prior REST-API oracle work. The positioning against AGORA+, SATORI, and MASTOR is sharp.

- **Presentation:** 4/5 — The writing is clear and the structure is logical. Table 1 (oracle exclusion analysis) and Table 2 (cross-model vs. source) are excellent. The main weakness is that the small RQ3 probe could be flagged more prominently as a preliminary finding. The Related Work section is thorough.

- **Overall:** 4/5 — (Weak accept). The paper addresses a real problem with a well-motivated solution and strong empirical evaluation (111 submissions, 38 acknowledged). The method is sound and the contributions are clear. The primary limitation is the small sample for the task-intrinsic claim, which is central but presented as a pilot. With broader validation of that finding, this would be a strong accept. As is, it's a solid contribution that moves the field forward.

- **Confidence:** 4/5 — I am confident in my assessment of the paper's strengths and weaknesses. The evaluation metrics and study design are clear, and the threats to validity are explicit. My only uncertainty is about the generalizability of the task-intrinsic finding, which the paper itself flags as contingent.

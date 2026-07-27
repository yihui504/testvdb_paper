# Mock Review: TestVDB - Source-Grounded Falsification for VDB API Conformance Testing

## Summary

TestVDB addresses a timely and important problem: detecting API conformance defects in vector database management systems (VDBMSs) where the only available oracle is natural-language documentation. The paper introduces source-grounded falsification, a technique that uses implementation code to validate LLM-derived behavioral claims, demonstrating 111 submitted issues with 38 maintainer-acknowledged defects across five VDBMSs. The work is well-motivated and technically sound, with solid empirical results, but has limitations in scope (conformance vs. correctness) and evaluation scale that prevent a stronger rating.

## Strengths

1. **Timely and important problem domain** (Introduction, §1): Vector database testing is underexplored despite its critical role in LLM applications. The 2026 VDBFuzz ICSE paper establishes this as a hot area, and TestVDB carves out a distinct niche (conformance vs. crashes) that complements prior work.

2. **Clear problem formulation and oracle taxonomy** (§2-3): The classification of oracle types and the 85% conformance residual statistic (Table 1) convincingly motivates why existing approaches (differential, metamorphic, property-based) cannot reach this defect class. The distinction between conformance and correctness is well-drawn.

3. **Novel technical contribution** (§4-5): Source-grounded falsification is a genuine innovation. Using the implementation to falsify LLM-derived claims is a smart counter to the LLM-as-oracle reliability problem, and the two-layer error model (family-specific vs. task-intrinsic) is insightful.

4. **Solid empirical evaluation** (§6): The RQ2 results on false-positive suppression (81% with source vs. 31% without) and the RQ3 head-to-head with cross-model validation provide concrete evidence. The 38 acknowledged defects across 111 submissions demonstrates real-world impact.

5. **Clear articulation of limitations** (§7): The paper is appropriately circumspect about what it does not cover (soft correctness, closed-source systems, recall estimation). The threat-to-validity discussion is thorough.

## Weaknesses

### [Major] W1: Limited scope - conformance ≠ correctness

**Evidence:** Throughout the paper, especially §2 and §7. The abstract explicitly states: "TestVDB targets conformance; result correctness of vector search remains open and is not our claim." The evaluation only reports on accept/reject violations.

**Impact:** This dramatically narrows the problem space. The most critical defects in VDBMSs—incorrect ANN search results, ranking errors, recall failures—are excluded. What remains is a specialized corner of the testing problem. While valid, this scope limits the paper's significance to the broader SE community. For a top-tier venue, the contribution feels niche.

**Suggested fix:** Expand the discussion of why conformance is chosen as the starting point. Add a concrete estimate of the prevalence of conformance vs. correctness defects in the wild (perhaps from the bug study data). Strengthen the argument for why this is the right first step before tackling the harder correctness problem.

### [Major] W2: Evaluation scale is modest for five systems

**Evidence:** Table 2 shows the distribution is heavily skewed: Milvus (51 submitted, 22 acknowledged), Qdrant (26/13), and Weaviate (30/3). MeiliSearch (3/0) and Chroma (1/0) contribute essentially nothing. The statistical claims rest primarily on two systems.

**Impact:** For a paper claiming results across "five VDBMSs," this is misleading. The breadth is superficial; the real evidence is from Milvus and Qdrant. This undermines the generalizability claims and weakens the significance dimension.

**Suggested fix:** Either (a) deepen the evaluation on Milvus and Qdrant to strengthen those claims, or (b) remove the weaker systems and frame this as a two-system study. A balanced 5-system evaluation would require similar submission volumes across all, or at least some acknowledged defects in each.

### [Major] W3: RQ3 probe is too small to support the strong claim

**Evidence:** §6, RQ3 paragraph and Table 3. The task-intrinsic error evaluation uses only 9 clauses from Milvus. The paper admits "we treat them as a pilot pending a larger study."

**Impact:** This is the centerpiece evidence for the novel two-layer error model, yet it's based on a handful of examples. For a top-tier venue, this sample size is inadequate to support the broad claims about task-intrinsic vs. family-specific errors. The binomial confidence interval must be enormous.

**Suggested fix:** Expand this evaluation. There are 51 submitted Milvus issues—surely more over-strict clauses exist. Run the same analysis on the full set of candidate clauses to provide a more robust estimate. The current 9-clause pilot is not publication-ready for a major venue.

### [Minor] W4: Abstract overstates the "85%" statistic

**Evidence:** Abstract line 2: "Across 111 submitted VDBMS issues... about 85% are, by our fault-model classification, conformance defects."

**Impact:** This suggests 85% of all VDBMS defects are conformance defects, which is misleading. The 111 issues are not a random sample—they're TestVDB's own outputs, which are biased by design toward conformance. The abstract should clarify this selection bias.

**Suggested fix:** Rephrase to: "Across 111 submitted VDBMS issues (38 acknowledged), about 85% are conformance defects by our classification." This makes the sampling clear.

### [Minor] W5: LLM-as-oracle framing could be clearer

**Evidence:** §3 distinguishes LLM-as-oracle from prior REST-API work, but the boundary is subtle. The paper emphasizes that prior work uses "deterministic extraction" while TestVDB uses "LLM interpretation," yet MASTOR also uses source code.

**Impact:** The precise technical difference is not immediately obvious to readers unfamiliar with this subfield. A clearer contrast would strengthen the novelty argument.

**Suggested fix:** Add a concrete example contrasting AGORA+/SATORI/MASTOR with TestVDB on the same input. Show what each tool would output and where the deterministic vs. LLM-based split occurs.

## Questions for Authors

1. **On scope (W1):** The paper excludes result correctness (ANN recall, ranking). How do you plan to extend this approach to those defects? Would the same source-grounded falsification technique apply, or does that require fundamentally different machinery?

2. **On evaluation scale (W2):** Why include MeiliSearch and Chroma given their negligible contribution? Would this work be stronger as a focused two-system study, or is there a plan to deepen those evaluations?

3. **On RQ3 (W3):** With only 9 clauses, how do you justify the strong claim about task-intrinsic errors? What would it take to expand this to a statistically sound sample size, and is that planned for future work?

## Scores

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| **Soundness** | 4/5 | The methodology is technically sound, with proper ablations and threat discussions. The RQ2 evaluation is solid. Points lost only for the small RQ3 sample. |
| **Significance** | 3/5 | The problem is timely and the results are real (38 acknowledged defects), but the scope is narrow (conformance only) and the evaluation is skewed toward two systems. Feels like a strong specialized contribution rather than a broad breakthrough. |
| **Novelty** | 4/5 | Source-grounded falsification is genuinely new. The two-layer error model (family-specific + task-intrinsic) is insightful. Points lost for some conceptual overlap with MASTOR's use of source, though the directionality is different. |
| **Presentation** | 4/5 | Well-structured and clearly written. Good use of tables to visualize results. Some abstract phrasing could be tightened (W4), but overall above average for the field. |
| **Overall** | **Weak Accept** | **Rationale:** This is solid work with a genuine contribution and real-world impact (38 defects). However, the narrow scope (conformance only) and modest evaluation scale (really 2 systems, not 5) keep it from reaching Accept strength. If the authors address W1-W3, this could become a solid Accept. The current state is publishable but not compelling for a top-tier venue without revision. |
| **Confidence** | 4/5 | I'm familiar with database testing, LLM-as-judge literature, and the REST-API oracle space. I understand the technical contributions and have reviewed similar work. The only uncertainty is in the VDBMS domain specifics, which I've inferred from the paper's context. |

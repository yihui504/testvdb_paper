## Reviewer 3: General Reviewer

**Overall Recommendation:** Weak Accept

### Summary

The paper presents TestVDB, a system for detecting documentation-implementation defects in Vector Database Management Systems (VDBMSs)—a defect class where systems silently accept inputs that violate their API documentation. The authors argue that because API documentation is natural-language prose rather than structured specifications, existing deterministic oracles (crash-based fuzzing, differential testing, metamorphic relations) cannot adjudicate accept/reject decisions, leaving LLMs as the practical oracle. TestVDB instantiates a four-stage pipeline using LLMs for claim extraction, test generation, sandboxed execution, and defect confirmation. To address LLM false positives from hallucination and self-preference bias, they introduce a "dev-reviewer" agent that falsifies claims against implementation source. They evaluate on three VDBMSs (Milvus, Qdrant, Weaviate), reporting 49 maintainer-acknowledged true-positive defects from 107 submitted issues, with a dev-reviewer retrospective achieving 67% precision and 74% recall versus 37% recall without source grounding. A bidirectional probe against VDBFuzz shows complementary coverage.

### Core Strengths

- **S1:** Clear articulation of the oracle problem and why existing deterministic approaches miss the documentation-implementation residual — see 1.1, 1.2.
- **S2:** Systematic oracle-exclusion argument (Table 1) that structurally motivates LLM-derived oracles as the necessary approach for this defect class — see 1.3.
- **S3:** Well-motivated dev-reviewer design addressing two specific false-positive failure modes (hallucination, self-preference) with a falsification architecture — see 3.1, 3.2.
- **S4:** Substantial real-world impact: 15 merged-PR fixes across three production VDBMSs — see 4.1.

### Core Weaknesses

- **W1:** Novelty relative to REST-API oracle literature is unclear — the paper claims TestVDB targets "ambiguous-prose documentation" but doesn't systematically differentiate from prior work's "low-ambiguity structured sources" regime — see 2.1.
- **W2:** Statistical rigor on the dev-reviewer operating point is insufficient — the 3-run union ensemble is a post-hoc selection without pre-registration, and Wilson CIs don't account for selection across four operating points — see 4.2 [major, fixable].
- **W3:** External validation beyond VDBMSs is absent, limiting confidence in transferability claims — see 4.3.

### Detailed Assessment

1. **Significance** — Adequate
   - **1.1** The paper targets a real and impactful problem: VDBMS defects that silently corrupt query semantics without crashing. The bug study they cite (Section 1) attributes 43% of VDBMS bugs to incorrect behavior, making this a substantive target. The 15 merged-PR fixes across production systems demonstrate practical impact beyond toy examples.
   - **1.2** However, the scope is narrower than the framing suggests. The paper explicitly limits itself to "documentation-implementation consistency" and explicitly excludes "result correctness" (ANN recall, ranking) as out of scope. This focused scope is defensible but limits significance to a subset of VDBMS correctness issues. The impact on the broader VDBMS testing agenda is therefore partial.
   - **1.3 [minor, fixable]** The contribution statement (Section 1, last paragraph) would benefit from explicitly stating what is NOT claimed (result correctness, closed-source systems) to set precise expectations for readers unfamiliar with the VDBMS testing roadmap.

2. **Novelty** — Provisional Adequate
   - **2.1 [major, fixable]** The novelty positioning relative to REST-API oracle tools (AGORA+, SATORI, MASTOR) needs clarification. The paper claims these tools "extract from low-ambiguity structured sources" and that TestVDB enters the "ambiguous-prose regime," but the boundary is not demonstrated. Are there examples where AGORA+ or SATORI *attempted* to extract from natural-language documentation and failed? Or is this a theoretical exclusion argument? Without concrete comparison cases, the "ambiguous-prose" regime reads as a post-hoc distinction rather than a demonstrated delta.
   - **2.2** Within the LLM-as-judge reliability line, the contribution of source-grounded falsification to break self-preference bias (Section 5) appears novel. Prior work (Toradocu, Doc2OracLL, ChatAssert) uses runtime feedback or iterative prompt repair, not implementation source as an independent falsifier. This is a clear methodological delta.
   - **2.3 [minor, fixable]** The Related Work section (Section 7) should explicitly state whether Toradocu, Doc2OracLL, or ChatAssert were evaluated on VDBMS-like natural-language API documentation. If they were tested on Javadoc (structured) and failed on prose, that would strengthen the novelty claim. If they were never evaluated on prose, the delta is untested.

3. **Soundness** — Adequate
   - **3.1** The oracle-exclusion argument (Table 1) is structurally sound: each deterministic oracle candidate is ruled out for a documented reason (crash oracles miss silent accepts; differential testing cannot adjudicate accept/reject; metamorphic relations address output not input; property-based testing requires machine-checkable properties; REST-API tools require structured sources). The logical chain that leaves LLMs as the residual follows from these exclusions.
   - **3.2** The dev-reviewer three-check falsification design (Section 5, Figure 3) is sound: independently reproducible, evidence-sufficient, and falsifiable checks directly address the failure modes diagnosed in Section 4 (hallucination, self-preference). The cross-model check (DeepSeek agreeing on 20 candidates, Cohen's κ=1.0) provides evidence that the verdict is not strongly family-specific when source evidence is explicit.
   - **3.3 [major, unfixable]** The implementation-as-correct assumption (acknowledged in Section 8) is a structural limitation: an implementation bug can wrongly falsify a correct clause. The authors report observing "maintainer-rejected confirmed TPs where the documentation itself was wrong" but do not quantify this failure mode. Without knowing the false-negative rate from this assumption, the precision/recall estimates are biased upward. This is inherent to the approach and cannot be fixed without a ground-truth defect catalog.

4. **Verifiability** — Adequate
   - **4.1** The paper provides sufficient methodological detail to reproduce the pipeline: the four-stage architecture (Section 3), the dev-reviewer three checks (Section 5), and the LLM runtime configuration (Section 3, "LLM automation"). The authors state that "full prompts, target versions, and per-token accounting are in the artifact" and commit to releasing it at a persistent URL upon acceptance, which satisfies the verifiability bar for a technical paper.
   - **4.2 [major, fixable]** The statistical reporting on the dev-reviewer operating point is insufficient. The 3-run union ensemble is selected as the "headline" from four operating points (single run, 3-run union, 5-run union, 5-run majority), and the authors explicitly flag this as "post-hoc." However, the Wilson 95% CIs in Table 2 do not account for selection across operating points. A pre-registered analysis plan or a correction for multiple comparisons would strengthen verifiability. As written, the recall gain (37%→74%) may be partially attributable to cherry-picking the operating point.
   - **4.3** The bidirectional VDBFuzz probe (Section 6, RQ3) provides two concrete case studies (Qdrant v1.4.0 integer-overflow crash, Qdrant v1.18.0 empty-vector accept) that demonstrate complementary coverage. The authors correctly note that "each direction is n=1" and treat these as "hypothesis-generating controlled cases rather than a generalized result," which is an appropriate limitation statement. The root-cause analysis of #9045 (debug_assert conditional, wait=true vs wait=false path divergence) is detailed and verifiable.
   - **4.4 [minor, fixable]** The paper reports "single-run recall varies widely (15–78%)" but does not show the distribution of per-run recall or quantify the variance (e.g., standard deviation, interquartile range). Reporting these metrics would improve verifiability of the LLM judge's high-variance claim.

5. **Presentation** — Adequate
   - **5.1** The paper is well-structured: Introduction → Problem Setup → Approach → False-Positive Problem → Dev-Reviewer → Evaluation → Related Work → Discussion → Conclusion. The narrative flow is logical, and each section builds on the previous. The figures (Figure 1 pipeline, Figure 3 dev-reviewer checks) are clear and support the text.
   - **5.2** The writing is generally clear, with precise terminology (e.g., "documentation-implementation consistency" vs "result correctness," "accept/reject" vs "crash"). The example case studies (Milvus #49823, Qdrant #9255, Qdrant #9045) are well-chosen and illustrative.
   - **5.3 [minor, fixable]** Table 2 (operating points) uses "---" for accuracy on the "5-run majority" configuration, which is unclear. Is this missing data, or is accuracy undefined for majority voting? A footnote or explicit "N/A" would clarify.
   - **5.4 [minor, fixable]** The Related Work section (Section 7) is dense and would benefit from sub-paragraph breaks to separate the four threads (VDBMS testing, REST-API oracles, LLM-as-judge, documentation-derived oracles) for readability.

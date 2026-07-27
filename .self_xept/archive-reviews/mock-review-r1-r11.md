# Mock Review: TestVDB (Round 11) — Reviewer 1 (Objective)

**Scores (ISSTA/FSE/ICSE criteria):**
- Soundness: 4/5
- Significance: 3/5
- Novelty: 4/5
- Presentation: 4/5
- Overall: 3.8/5 (Weak Accept)
- Confidence: 4/5

## Summary

This paper introduces TestVDB, a source-grounded falsification approach for API conformance testing of vector databases. The core insight is that when documentation is natural-language prose (unlike structured specifications), LLMs produce unreliable behavioral claims that split into family-specific errors (mitigated by cross-model validation) and task-intrinsic errors (requiring source as ground truth). The authors demonstrate this on five VDBMSs, surfacing 111 candidate issues with 38 maintainer-acknowledged defects, and show that source-grounded falsification suppresses 81% of false positives on Milvus/Qdrant while retaining 96.7% of true positives.

**Round 11 improvement:** The within-vendor contrast on Qdrant (search parameters with optional defaults vs. collection parameters with explicit minimums) is a **meaningful methodological advance** over Round 10. The falsifiable prediction that "optional default + no explicit bound → over-strict candidate, whereas explicit minimum → not" provides a concrete operationalization that moves the distribution finding toward evidence-backed from post-hoc. This addresses the primary concern from Round 10 about pattern-hunting without a priori framing.

## Strengths

1. **Problem characterization is crisp.** The separation of conformance from correctness, and the mapping of why differential/metamorphic/property-based oracles cannot reach the accept/reject residual (Table 1), is clear and technically sound. The framing of source ambiguity as the gap from prior REST-API oracle work (AGORA+, SATORI, MASTOR) is well-positioned.

2. **Two-layer reliability model is solid.** The family-specific vs. task-intrinsic split is theoretically grounded. Cross-model validation addresses the first; source addresses the second. This is a clean contribution that clarifies *when* LLMs enter the testing pipeline and *why* they become unreliable.

3. **Within-vendor contrast is now evidence-backed.** The Qdrant comparison (search vs. collection parameters) provides a falsifiable prediction that documentation style (optional default vs. explicit minimum) drives over-formalization risk. This is a substantial methodological improvement over Round 10's exploratory observation, turning the distribution finding from post-hoc pattern-spotting into a testable hypothesis.

4. **Empirical evaluation is reasonable for an exploratory probe.** The 12-clause pilot (Milvus 9, Qdrant 3) with TI rate 5/12 (Wilson 95% CI [19%, 68%]) is appropriately cautious. The authors acknowledge this is a pilot and flag a larger head-to-head study as ongoing, which is honest about limitations.

5. **Related work is thorough.** The positioning against AGORA+, SATORI, MASTOR, Toradocu, and ChatAssert is precise. The distinction that MASTOR tests what the implementation does (with source as reference) while TestVDB tests what the documentation prescribes (with source as reference for actual behavior) is a key differentiator.

## Weaknesses

### Major

1. **Statistical generalization remains underspecified.** The 85% residual composition is the *composition of TestVDB's findings*, not an estimate of the true defect distribution. The paper acknowledges this in RQ1 ("biased toward conformance by design"), but the threat-to-validity discussion could be more explicit about what would be required to turn this into a population estimate: capture-recapture analysis, or an unbiased defect sample via manual inspection of a random parameter subset.

2. **External validity on Weaviate/MeiliSearch/Chroma is breadth-only.** The abstract claims "five VDBMSs," but the statistical claims (85% residual, 5/12 TI rate, 81% FP suppression) rest on Milvus and Qdrant only. Weaviate contributes 30 submissions but only 3 acknowledgments; MeiliSearch and Chroma are effectively negative controls. The paper should be clearer that statistical power is Milvus/Qdrant-bounded and that the other three systems demonstrate applicability rather than statistical weight.

3. **Cross-model κ is promising but small.** The DeepSeek re-run on 6 candidates (κ=1.0) is suggestive that the verdict is not family-specific when source evidence is explicit, but n=6 is a pilot. The paper flags a larger ablation as ongoing, which is appropriate, but the current state is preliminary.

4. **RQ3 probe design is post-hoc constrained.** The 12-clause set is "Milvus-heavy" because the phenomenon itself concentrates in optional-default APIs (Milvus, Qdrant search params) and is absent in explicit-bound systems (Weaviate). While the within-vendor contrast helps, the clause selection remains driven by where GLM found over-strict claims, not by a pre-specified sampling frame. A stronger design would enumerate *all* optional-default parameters across Milvus/Qdrant a priori, then test whether over-strictness correlates with documentation style.

### Minor

1. **Presentation: The abstract is dense.** The second paragraph (lines 20-22) packs the two-layer error model, the exploratory pilot, and the concentration in optional-default APIs into 3 sentences. This could be split for clarity.

2. **Presentation: Table 2 (RQ3) could be clearer.** The three Qdrant parameters at bottom could be labeled more explicitly as "Qdrant v1.18.2 search parameters" to reinforce the within-vendor contrast.

3. **Writing: Some sentences are long.** Example: line 89-91, "When the documentation itself is ambiguous..." runs 3 lines and could be split.

4. **Terminology: "task-intrinsic" vs. "documentation-intrinsic".** The paper uses "task-intrinsic" for errors rooted in the shared documentation. This is technically correct but "documentation-intrinsic" might be more transparent. This is minor and not a blocker.

## Questions

1. **On the falsifiable prediction:** You predict that "optional default + no explicit bound → over-strict candidate." Have you tested this prediction on a *new* VDBMS (not Milvus/Qdrant) to see if it holds? For example, if Weaviate added an optional-default parameter with no explicit bound, would you expect over-formalization?

2. **On sampling for the larger head-to-head study:** You flag a larger study as ongoing. What is the planned sampling frame? Will it be (a) all optional-default parameters across Milvus/Qdrant, (b) a stratified random sample of parameters across all five VDBMSs, or (c) a new VDBMS not in the current set?

3. **On the 85% residual:** You state this is the composition of *your* findings, not a population estimate. If you were to estimate the true conformance-defect proportion, what method would you use? Capture-recapture? Manual audit of a random parameter subset?

4. **On Weaviate's role:** You note Weaviate documents explicit bounds ("Must be >= 1"), so its doc-code gaps are conformance bugs rather than over-formalized clauses. This is a useful contrast, but Weaviate only contributes 3 acknowledgments to 30 submissions. Is there a systematic difference in how maintainers treat conformance bugs vs. over-formalized clauses?

## Detailed Comments by Section

### Introduction (§1)
- Strong opening. The 85% figure is prominent, though the caveat that this is *composition* not *prevalence* could be highlighted more.
- Paragraph 3 (LLM errors split) is much clearer in Round 11. The within-vendor contrast foreshadowing is well-placed.

### Background (§2)
- Clean separation of conformance vs. correctness. The placement of conformance as a subset of the broader oracle problem (Barr et al.) is solid.

### The Role of the LLM (§3)
- The two-layer error model is the theoretical core. This is well-written and technically precise.
- The distinction from AGORA+/SATORI/MASTOR (source ambiguity, not extraction mechanism) is a key contribution.
- The probe description (12 clauses, GLM vs. DeepSeek) is now more clearly framed as exploratory, which is appropriate.

### Design (§4)
- The falsification rule is concrete: "dev-reviewer examines source, accepts value → clause over-strict."
- Good contrast with MASTOR (tests what implementation does vs. what documentation prescribes).

### Implementation (§5)
- Reasonable detail on the pipeline. The cost estimate (~$10 per target) is useful context.

### Evaluation (§6)
- **RQ1:** Good caveats about the 85% being composition, not prevalence. The threat-to-validity discussion should repeat this explicitly.
- **RQ2:** The 81% FP suppression (up from 31%) is a strong result. The ablation (single-LLM 25.5%, single-source 45.6%, full 69.2%) is well-structured.
- **RQ3:** The within-vendor contrast is the key improvement. The falsifiable prediction is clearly stated. The CI [19%, 68%] is appropriately wide for n=12.
- **RQ4:** The model-free invariant subclass is a useful contribution but less central to the main narrative.

### Related Work (§7)
- Thorough and well-positioned. The distinction from Toradocu, ChatAssert, and Testora is precise.

### Discussion (§8)
- Generalizability to other systems (REST without OpenAPI, config validation) is well-stated.
- Limitations are honest: requires source, treats implementation as correct, 85% is composition not prevalence.

### Conclusion (§9)
- Solid summary. The boundary drawing (structured sources vs. natural-language docs) is a forward-looking framing.

## Recommendation

This paper has improved significantly from Round 10. The within-vendor contrast on Qdrant, combined with the falsifiable prediction about documentation style driving over-formalization risk, moves the distribution finding from post-hoc pattern-spotting to evidence-backed hypothesis testing. This addresses the core methodological concern from Round 10.

**The paper is now methodologically sound for an exploratory probe.** The authors are appropriately cautious about statistical generalization, acknowledge the small probe size, and flag larger studies as ongoing. The two-layer reliability model is a solid theoretical contribution, and the 81% FP suppression with source anchor is a strong empirical result.

**Weaknesses are real but not fatal.** The 85% composition is not a prevalence estimate, and Weaviate/MeiliSearch/Chroma are breadth-only. These are limitations, not flaws, provided the paper is explicit about them—which it mostly is, though the threat-to-validity section could be strengthened.

**Minor revisions would tighten the presentation.** The abstract is dense in places, and some sentences are long. Table 2 could be clearer. These are cosmetic.

**Recommendation:** Weak Accept (3.8/5). The paper makes a solid contribution to LLM-as-judge reliability in testing, introduces a practical falsification approach, and has improved its methodological framing substantially. With minor revisions to clarify statistical scope and tighten presentation, this would be a respectable addition to ISSTA/FSE/ICSE.

---

**Verdict:** Weak Accept (3.8/5)
**Condition:** Minor revisions to clarify (a) that 85% is composition not prevalence, (b) that statistical power is Milvus/Qdrant-bounded, (c) that Weaviate/MeiliSearch/Chroma demonstrate breadth not statistical weight. No re-review needed.

**Next steps for authors:**
1. Add 1-2 sentences to abstract clarifying "this is the composition of our findings, not a population estimate."
2. Add a bullet to Threats to Validity: "External validity: statistical claims rest on Milvus/Qdrant; other systems demonstrate applicability."
3. Split the dense abstract sentence about the exploratory pilot (lines 20-22).
4. Label Qdrant rows in Table 2 as "Qdrant v1.18.2 search parameters" to reinforce within-vendor contrast.

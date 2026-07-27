# Mock Review: TestVDB (Round 12) — Reviewer 1 (Objective)

**Scores (ISSTA/FSE/ICSE criteria):**
- Soundness: 5/5
- Significance: 4/5
- Novelty: 4.5/5
- Presentation: 4/5
- Overall: 4.4/5 (Accept)
- Confidence: 4/5

## Summary

This paper introduces TestVDB, a source-grounded falsification approach for API conformance testing of vector databases. The core insight is that when documentation is natural-language prose (unlike structured specifications), LLMs produce unreliable behavioral claims that split into family-specific errors (mitigated by cross-model validation) and task-intrinsic errors (requiring source as ground truth). The authors demonstrate this on five VDBMSs, surfacing 111 candidate issues with 38 maintainer-acknowledged defects, and show that source-grounded falsification suppresses 81% of false positives on Milvus/Qdrant while retaining 96.7% of true positives.

**Round 12 improvement:** The paper has substantially strengthened its evidentiary base. RQ3, which I characterized as an "exploratory pilot" in Round 11 (n=12, Wilson CI [19%, 68%]), is now backed by a 29-clause probe across three subtypes (parameter over-strict 5/12, behavior 4/4, explicit-bound negative 0/13) with a falsifiable prediction validated both positively (task-intrinsic concentrates in optional-default APIs) and negatively (absent where documentation states explicit bounds). Cross-model validation, which I flagged as "promising but small" at n=6, now extends to n=20 candidates spanning five subtypes with Cohen's κ=1.0, substantially reducing the family-specific concern. The §3 clarification distinguishing task-intrinsic (extraction-level across-families) from Haldar's judgment-level across-runs noise strengthens the theoretical foundation, and four added references (AugmenTest, Actual-vs-Expected Konstantinou, Wataoka, Rating Roulette Haldar) improve related work coverage.

## Strengths

1. **Task-intrinsic claim is now evidence-backed, not exploratory.** The expansion from n=12 to n=29 (parameter over-strict 5/12, by-design behavior 4/4, explicit-bound negative 0/13), combined with the within-vendor contrast (Qdrant: search parameters with optional defaults vs. collection parameters with explicit minimums), provides both positive and negative validation of the falsifiable prediction. The pooled task-intrinsic rate of 9/16 (Wilson 95% CI [33%, 77%]) with 0/13 on explicit bounds (CI [0%, 23%]) constitutes a controlled finding. This addresses the primary Round 11 concern about "post-hoc pattern-spotting" by turning the distribution finding into a testable hypothesis with empirical support.

2. **Cross-model reliability is now convincingly demonstrated.** The expansion from n=6 to n=20 candidates (spanning input-validation, upsert-semantics, idempotent-drop, correct-reject, and dynamic-field subtypes) with Cohen's κ=1.0 (blind to GLM-5.2's rationale) provides strong evidence that the source-grounded verdict is not family-specific when source evidence is explicit. This addresses the Round 11 concern that "cross-model κ is promising but small."

3. **Theoretical clarification on task-intrinsic vs. Rating Roulette.** §3 now explicitly scopes the stability claim: task-intrinsic stability is extraction-level (across model families) and distinct from Haldar et al.'s judgment-level across-runs inconsistency. This clarifies the threat model and positions the work more precisely in the LLM-as-judge reliability landscape.

4. **Related work is more complete.** The addition of AugmenTest, Actual-vs-Expected (Konstantinou et al.), Wataoka & Takahashi, and Rating Roulette (Haldar et al.) fills gaps in LLM-as-judge reliability and documentation-derived oracle literature. The positioning against these works is now tighter.

5. **Within-vendor contrast is now quantified with negative control.** The Qdrant comparison (search parameters with optional defaults: 3/3 over-strict; collection parameters with explicit minimums: 0/6) provides a falsifiable prediction validated in both directions. The 13-parameter explicit-bound probe (Qdrant shard_number/replication_factor/write_consistency_factor/full_scan_threshold, Weaviate ef/dynamicEfMin/dynamicEfMax/efConstruction/maxConnections/vectorIndexType/replicationConfig.factor, Milvus dimension/num_partitions) with 0/13 over-formalization (Wilson 95% CI [0%, 23%]) strengthens the claim that the phenomenon concentrates in ambiguous optional-default APIs.

6. **Cross-model validation's scope is clarified.** The W3 study now explicitly distinguishes what cross-model validation can and cannot resolve: it catches family-specific self-preference but not task-intrinsic errors (catches 7/12 over-strict clauses but misses 2/5 task-intrinsic ones). This clarifies the complementary roles of cross-model validation and source-grounded falsification.

## Weaknesses

### Major

1. **Statistical generalization remains underspecified (persistent from Round 11).** The 85% residual composition is still the *composition of TestVDB's findings*, not an estimate of the true defect distribution. The paper acknowledges this in RQ1 ("biased toward conformance by design"), but the threat-to-validity discussion could be more explicit about what would be required to turn this into a population estimate: capture-recapture analysis, or an unbiased defect sample via manual inspection of a random parameter subset. This is a limitation, not a flaw, provided the paper is explicit—which it is, though the threats section could be strengthened.

2. **External validity on Weaviate/MeiliSearch/Chroma is breadth-only (persistent from Round 11).** The abstract claims "five VDBMSs," but the statistical claims (85% residual, 9/16 TI rate, 81% FP suppression) rest on Milvus and Qdrant only. Weaviate contributes 30 submissions but only 3 acknowledgments; MeiliSearch and Chroma are effectively negative controls. The paper should be clearer that statistical power is Milvus/Qdrant-bounded and that the other three systems demonstrate applicability rather than statistical weight. Round 12 has not changed this.

### Minor

1. **Presentation: The abstract remains dense.** The second paragraph (lines 20-22) still packs the two-layer error model, the exploratory pilot, and the concentration in optional-default APIs into 3 sentences. This could be split for clarity (persistent from Round 11).

2. **Presentation: Table 2 (RQ3) could be clearer.** The three Qdrant parameters at bottom could be labeled more explicitly as "Qdrant v1.18.2 search parameters" to reinforce the within-vendor contrast (persistent from Round 11).

3. **Writing: Some sentences are long.** Example: line 89-91, "When the documentation itself is ambiguous..." runs 3 lines and could be split (persistent from Round 11).

## Questions

1. **On the falsifiable prediction:** You predict that "optional default + no explicit bound → over-strict candidate." Have you tested this prediction on a *new* VDBMS (not Milvus/Qdrant) to see if it holds? For example, if Weaviate added an optional-default parameter with no explicit bound, would you expect over-formalization? (Persistent from Round 11, now more pressing given the stronger evidence.)

2. **On sampling for the larger head-to-head study:** You flag a larger study as ongoing. What is the planned sampling frame? Will it be (a) all optional-default parameters across Milvus/Qdrant, (b) a stratified random sample of parameters across all five VDBMSs, or (c) a new VDBMS not in the current set? (Persistent from Round 11.)

3. **On the 85% residual:** You state this is the composition of *your* findings, not a population estimate. If you were to estimate the true conformance-defect proportion, what method would you use? Capture-recapture? Manual audit of a random parameter subset? (Persistent from Round 11.)

4. **On Weaviate's role:** You note Weaviate documents explicit bounds ("Must be >= 1"), so its doc-code gaps are conformance bugs rather than over-formalized clauses. This is a useful contrast, but Weaviate only contributes 3 acknowledgments to 30 submissions. Is there a systematic difference in how maintainers treat conformance bugs vs. over-formalized clauses? (Persistent from Round 11.)

5. **On the 13-parameter explicit-bound probe:** The 0/13 result (Wilson CI [0%, 23%]) is a strong negative control. Did you pre-specify these 13 parameters, or were they selected post-hoc from a larger set? The strength of the negative control depends on whether the sampling was a priori or data-driven.

## Detailed Comments by Section

### Introduction (§1)
- Strong opening. The 85% figure is prominent, though the caveat that this is *composition* not *prevalence* could be highlighted more (persistent from Round 11).
- Paragraph 3 (LLM errors split) is much clearer in Round 11 and remains clear in Round 12.
- The task-intrinsic distinction now foreshadows the §3 clarification.

### Background (§2)
- Clean separation of conformance vs. correctness. The placement of conformance as a subset of the broader oracle problem (Barr et al.) is solid (unchanged).

### The Role of the LLM (§3)
- **Key improvement:** The explicit scoping of task-intrinsic stability (extraction-level across-families) vs. Haldar's judgment-level across-runs inconsistency. This clarifies the theoretical contribution.
- The two-layer error model is the theoretical core. This is well-written and technically precise (unchanged).
- The distinction from AGORA+/SATORI/MASTOR (source ambiguity, not extraction mechanism) is a key contribution (unchanged).
- The probe description (29 clauses: 12 over-strict parameters + 4 by-design behaviors + 13 explicit-bound negatives) is now more clearly framed as evidence-backed rather than exploratory, which is appropriate.

### Design (§4)
- The falsification rule is concrete: "dev-reviewer examines source, accepts value → clause over-strict." (unchanged)
- Good contrast with MASTOR (tests what implementation does vs. what documentation prescribes) (unchanged).

### Implementation (§5)
- Reasonable detail on the pipeline. The cost estimate (~$10 per target) is useful context (unchanged).

### Evaluation (§6)
- **RQ1:** Good caveats about the 85% being composition, not prevalence. The threat-to-validity discussion should repeat this explicitly (persistent from Round 11).
- **RQ2:** The 81% FP suppression (up from 31%) is a strong result. The ablation (single-LLM 25.5%, single-source 45.6%, full 69.2%) is well-structured (unchanged).
- **RQ3:** **Major improvement.** The within-vendor contrast is now quantified with both positive (3/3 over-strict on search parameters) and negative (0/6 on collection parameters) validation. The falsifiable prediction is clearly stated and empirically supported. The pooled task-intrinsic rate of 9/16 (Wilson 95% CI [33%, 77%]) with 0/13 on explicit bounds (CI [0%, 23%]) is a controlled finding. The 13-parameter explicit-bound probe is a strong negative control. The CI for the 9/16 rate ([33%, 77%]) is appropriately wide for n=16.
- **RQ3 (cross-model):** **Major improvement.** The expansion from n=6 to n=20 candidates spanning five subtypes with Cohen's κ=1.0 provides strong evidence that the source-grounded verdict is not family-specific when source evidence is explicit. This addresses the Round 11 concern about "promising but small."
- **RQ4:** The model-free invariant subclass is a useful contribution but less central to the main narrative (unchanged).

### Related Work (§7)
- **Major improvement:** The addition of AugmenTest, Actual-vs-Expected (Konstantinou et al.), Wataoka & Takahashi, and Rating Roulette (Haldar et al.) fills gaps. The positioning against these works is now tighter. The distinction from Toradocu, ChatAssert, and Testora remains precise.

### Discussion (§8)
- Generalizability to other systems (REST without OpenAPI, config validation) is well-stated (unchanged).
- Limitations are honest: requires source, treats implementation as correct, 85% is composition not prevalence (unchanged).

### Conclusion (§9)
- Solid summary. The boundary drawing (structured sources vs. natural-language docs) is a forward-looking framing (unchanged).

## Comparison to Round 11 Concerns

| Round 11 Concern | Round 12 Response | Assessment |
|------------------|-------------------|------------|
| Statistical generalization (85% is composition, not prevalence) | Unchanged | Persistent limitation, not fatal |
| External validity (Weaviate/MeiliSearch/Chroma breadth-only) | Unchanged | Persistent limitation, not fatal |
| Cross-model κ small (n=6) | Expanded to n=20, κ=1.0 | **Resolved** |
| RQ3 probe design post-hoc constrained (12-clause Milvus-heavy) | Expanded to n=29 with negative control (13 explicit-bound 0/13) | **Largely resolved** |
| Presentation issues (dense abstract, long sentences) | Unchanged | Cosmetic, can be fixed in camera-ready |

## Recommendation

This paper has improved significantly from Round 11. The expansion of RQ3 from n=12 to n=29 (with three subtypes: parameter over-strict, by-design behavior, explicit-bound negative) and the quantification of the within-vendor contrast (Qdrant search vs. collection parameters) provide both positive and negative validation of the falsifiable prediction. This moves the task-intrinsic claim from "exploratory pilot" to "evidence-backed hypothesis." The expansion of W3 from n=6 to n=20 with Cohen's κ=1.0 substantially reduces the cross-model family-specific concern. The §3 clarification distinguishing task-intrinsic from Haldar's Rating Roulette strengthens the theoretical foundation, and four added references improve related work coverage.

**The paper is now methodologically sound for an evidence-backed probe.** The authors have appropriately responded to the Round 11 concerns about exploratory status and cross-model κ. The two-layer reliability model is a solid theoretical contribution, and the 81% FP suppression with source anchor is a strong empirical result.

**Weaknesses are real but not fatal.** The 85% composition is not a prevalence estimate, and Weaviate/MeiliSearch/Chroma are breadth-only. These are limitations, not flaws, provided the paper is explicit about them—which it is, though the threat-to-validity section could be strengthened.

**Minor revisions would tighten the presentation.** The abstract is dense in places, and some sentences are long. Table 2 could be clearer. These are cosmetic.

**Recommendation:** Accept (4.4/5). The paper makes a solid contribution to LLM-as-judge reliability in testing, introduces a practical falsification approach, and has substantially improved its methodological framing and evidentiary base from Round 11. With minor revisions to clarify statistical scope and tighten presentation, this would be a strong addition to ISSTA/FSE/ICSE.

---

**Verdict:** Accept (4.4/5)

**Condition:** Minor revisions to clarify (a) that 85% is composition not prevalence, (b) that statistical power is Milvus/Qdrant-bounded, (c) that Weaviate/MeiliSearch/Chroma demonstrate breadth not statistical weight. No re-review needed.

**Key improvements from Round 11:**
1. RQ3: n=12 → n=29 (with negative control 0/13 on explicit bounds), moving from exploratory to evidence-backed.
2. W3: n=6 → n=20 (κ=1.0), substantially reducing cross-model family-specific concern.
3. §3: Clarification of task-intrinsic (extraction-level) vs. Rating Roulette (judgment-level), strengthening theoretical foundation.
4. Related work: 4 added references (AugmenTest, Actual-vs-Expected, Wataoka, Rating Roulette) improving coverage.

**Next steps for authors:**
1. Add 1-2 sentences to abstract clarifying "this is the composition of our findings, not a population estimate" (persistent from Round 11).
2. Add a bullet to Threats to Validity: "External validity: statistical claims rest on Milvus/Qdrant; other systems demonstrate applicability" (persistent from Round 11).
3. Split the dense abstract sentence about the exploratory pilot (lines 20-22) (persistent from Round 11).
4. Label Qdrant rows in Table 2 as "Qdrant v1.18.2 search parameters" to reinforce within-vendor contrast (persistent from Round 11).
5. Consider addressing Question 5 (whether the 13-parameter explicit-bound probe was pre-specified or post-hoc) in the threats section or appendix.

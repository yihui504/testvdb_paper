# Mock Review: TestVDB (Round 1)

## Summary

This paper presents TestVDB, a source-grounded falsification approach for detecting API conformance defects in Vector Database Management Systems (VDBMSs). The core observation is that many VDBMS defects involve violations of natural-language API documentation (e.g., accepting `nprobe=0` when the docs prescribe rejection) that cannot be mechanically checked by classical oracles (differential, metamorphic, property-based). The authors argue this forces an LLM into both extraction and judgment roles, creating a two-layer reliability problem: family-specific self-preference (mitigated by cross-model validation) and task-intrinsic errors arising from ambiguous documentation (requiring source grounding). TestVDB addresses this by falsifying LLM-derived behavioral claims against source code. Across five VDBMSs, TestVDB surfaced 111 issues (38 maintainer-acknowledged defects), with source-grounded falsification suppressing 81% of false positives while retaining 96.7% of true positives.

## Strengths

1. **Clear problem framing and novelty** - The paper identifies a genuine gap: API conformance defects where the only reference is natural-language documentation, and classical oracles structurally cannot reach. The 85% residual quantification is compelling evidence that this is a substantial, non-trivial subset.

2. **Honest two-layer reliability analysis** - Section 3's separation of family-specific vs. task-intrinsic documentation-interpretation errors is thoughtful and well-motivated. The admission that cross-model validation cannot fix task-intrinsic errors (because the ambiguity lives in the documentation, not the model) is intellectually honest and sets up the source-grounded contribution properly.

3. **Concrete evaluation with maintainer validation** - Submitting 111 issues to real VDBMS maintainers and receiving 38 acknowledgments (31 fixed) is substantive evidence that TestVDB finds real bugs. The precision analysis (69.2% Wilson CI [55.7%, 80.1%]) is appropriately cautious with intervals.

4. **Terminology consistency is largely achieved** - The paper systematically uses "behavioral claims" and "documentation" throughout, avoiding the previous "contract/assertion" and "specification" terminology that caused confusion. This is a significant improvement in clarity.

5. **Structural complementarity demonstrated** - The VDBFuzz head-to-head on Qdrant v1.18.2 (0 crashes vs. TestVDB's conformance defects) and the classical-oracle suite (metamorphic relations found 0 violations by construction) convincingly show that TestVDB targets a disjoint defect class.

## Weaknesses

### [Major]

**W1. E2 experiment scope is critically small for the central claim.** The RQ3 probe (N=9 clauses, single VDBMS) is the primary evidence for the paper's most distinctive claim—that task-intrinsic documentation-interpretation errors exist and cross-model validation cannot catch them. This is treated as a "pilot" awaiting a larger study, but the entire paper's novelty hinges on this distinction. Without a larger, multi-vendor validation, the task-intrinsic layer remains speculative. The paper over-weights this tiny probe in the contribution list and abstract.

**Evidence:** §6.3, Table 2: "The probes are small, nine Milvus clauses, and we treat them as a pilot pending a larger study." Yet §7 lists this as a core contribution: "Task-intrinsic documentation-interpretation errors and the source-grounded counter."

**Fix:** Either scale the E2 probe (across multiple VDBMSs, N≥30) OR demote the task-intrinsic claim from a contribution to a hypothesis/discussion point. As is, it's a strong claim on weak evidence.

**W2. The "source reliability vs. checking mechanism" framing is not fully convincing.** The paper argues the distinction from AGORA+/SATORI/MASTOR is about source reliability (structured/ trustworthy vs. ambiguous/unreliable), not checking mechanism. But Table 1 shows AGORA+ uses "execution traces" and SATORI uses "OpenAPI spec"—both of which can be noisy or incomplete. The claim that their assertions are "trustworthy" by construction is too strong; OpenAPI specs often under-specify or mis-specify behavior. The contrast is real but overstated.

**Evidence:** §3: "AGORA+, SATORI, and MASTOR extract oracles from structured sources... where the constraints are explicit and the resulting assertions are reliable." Table 1 row 4: "extracted from structured sources (trustworthy); no falsification needed."

**Fix:** Qualify the claim. AGORA+/SATORI/MASTOR operate in a setting where the source is *more* structured, not perfectly reliable. The distinction is a continuum, not a binary.

**W3. Logical gap in the classical-oracle exclusion argument.** §2 claims metamorphic relations cannot reach conformance defects because "an MR is an output relation, not an input-acceptance transform." This is technically true but ignores the possibility of MRs over accept/reject decisions themselves (e.g., "input A rejected ⇔ input B rejected" under some transformation). The paper rules this out without justification. Similarly, property-based testing's "needs machine-checkable property" is not inherent to the approach—you could use PBT to test documentation-derived properties directly; the paper's framing makes this sound impossible when it's just what TestVDB does with an LLM.

**Evidence:** §2, Table 1 row 3: "an MR is an output relation; conformance is an input accept/reject decision, and no transform preserves it." Row 4: "needs a machine-checkable property and an OpenAPI schema."

**Fix:** Acknowledge that MRs/PBT *could* be adapted to conformance but require an intermediate semantic interpretation step (which is what TestVDB's LLM provides). The exclusion is pragmatic, not absolute.

### [Minor]

**W4. The conformance vs. correctness separation could be sharper.** §2.3 separates conformance (accept/reject matches docs) from correctness (mathematical result quality). But the abstract says "These defects corrupt query semantics"—which sounds like correctness. Conformance defects *enable* incorrect semantics, but the defect itself is about API boundaries, not query results. This conflation risks overclaiming.

**Evidence:** Abstract: "These defects corrupt query semantics and can return data the documentation intended to exclude." §2.3: "Conformance asks whether the API's accept/reject behavior matches its documentation. Correctness asks whether a returned result is mathematically right."

**Fix:** Clarify that conformance defects *allow* incorrect semantics but the defect itself is about input validation, not output correctness.

**W5. Threats to validity undersell construct validity concerns.** §6.4 lists construct validity as "All source-anchor results use a single model family (GLM-5.2), a full cross-model ablation of the dev-reviewer is open." But the bigger construct issue is that the entire approach assumes the implementation is correct for falsification. §7 acknowledges this but doesn't quantify it—how many of the 81% suppressed false positives might actually be clauses where the implementation is wrong, not the LLM?

**Evidence:** §6.4: "we do not estimate recall because there is no public ground-truth defect catalog for VDBMSs." §7: "it treats the implementation as correct, so an implementation bug can wrongly falsify a clause whose documentation is right."

**Fix:** Add a brief analysis of the 81% suppressed FPs: categorize how many were falsified due to implementation bugs vs. doc ambiguity. Even a small manual audit (N=20) would help.

**W6. Terminology inconsistency in one spot.** §6.2 mentions "over-strict clauses" but doesn't define them until §6.3. Earlier use of "over-formalized" (§3) creates two terms for the same phenomenon. This is minor but shows terminology hasn't fully settled.

**Evidence:** §3: "the extraction may over-formalize the documented intent." §6.2: "over-strict clauses." §6.3: "GLM-derived over-strict clauses."

**Fix:** Standardize on one term (prefer "over-formalized clauses" since it captures the root cause—extraction from informal docs).

**W7. Cross-vendor Qdrant probe is under-discussed.** §6.3 mentions a "cross-vendor check on Qdrant" showing that "over-strict phenomenon is largely confined to APIs with many optional-default parameters such as Milvus." This is an important generalization but gets one sentence. More detail would strengthen the external validity.

**Evidence:** §6.3: "A cross-vendor check on Qdrant... shows where the pattern concentrates."

**Fix:** Expand to 2-3 sentences with a concrete example from Qdrant.

## Questions

1. **Could the E2 probe be expanded within the page limit?** If N=9 is too small, could you add Qdrant/Weaviate to reach N=20-30 while keeping the table manageable? The task-intrinsic claim is central enough to warrant more evidence.

2. **How would you respond to a reviewer who says "just use PBT with LLM-derived properties" is not novel?** The philosophical novelty is source-grounded falsification of unreliable LLM assertions, but a reviewer might see this as "PBT + LLM for property generation." The paper could foreground the falsification aspect more explicitly.

3. **What fraction of the 81% suppressed false positives are due to implementation bugs vs. doc ambiguity?** Even a rough estimate from manual inspection of a sample would help address the "implementation as correct" assumption.

## Scores

**Soundness: 4/5** - The methodology is solid and the evaluation is substantive, but the E2 probe is critically underpowered for the central task-intrinsic claim. The classical-oracle exclusion argument has a minor logical gap.

**Significance: 4/5** - API conformance defects in VDBMSs are a real problem, and the 85% residual is compelling. The approach likely generalizes to other systems with NL documentation. Source-grounded falsification is a valuable conceptual contribution.

**Novelty: 4/5** - The two-layer reliability analysis (family-specific + task-intrinsic) is new, and source-grounded falsification of LLM-derived assertions is a distinct approach from prior REST-oracle work. The overall "LLM-as-oracle regime" framing is forward-looking.

**Presentation: 4/5** - The writing is clear, the terminology is largely consistent (good improvement from "contract/specification"), and the structure is logical. Minor issues: some terminology drift (over-formalized vs. over-strict), and a few conflation risks (conformance vs. correctness semantics).

**Overall: Strong Accept** - The paper addresses a real problem with a thoughtful approach, substantive evaluation (111 issues submitted, 38 acknowledged), and honest reliability analysis. The E2 experiment is underpowered but doesn't invalidate the core claims. The distinction from prior REST-oracle work is genuine, if slightly overstated. With minor revisions to address W1-W7, this would be a solid addition to ICSE/FSE/ISSTA.

**Confidence: 4/5** - I am familiar with VDBMSs, REST-API testing, and LLM-as-judge literature. The claims are accessible, though implementation details of the 20-agent pipeline are necessarily outsourced to the artifact.

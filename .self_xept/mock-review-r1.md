# Mock Review — TestVDB (ACM SIGCONF format)

**Summary:**  
TestVDB targets API conformance defects in vector databases by treating an LLM-derived contract as a hypothesis and falsifying it against source code. The work introduces the "LLM-as-oracle setting" to demarcate problems that lack a deterministic oracle, and validates source-grounded falsification on five systems, reporting 38 acknowledged defects from 111 submissions with an 81% false-positive suppression rate.

---

## Strengths

- **Clear problem articulation.** The paper cleanly distinguishes conformance (accept/reject vs. documented contract) from correctness (result quality), and quantifies the residual left by classical oracles (≈85% unreachable by differential/metamorphic/property-based approaches). Table 1 effectively maps where each classical oracle fails.

- **Honest scoping.** The work explicitly bounds its claims: conformance only, not result correctness of vector search. The threat-to-validity section is direct about the limitations (RQ3 is a nine-clause pilot; Weaviate/MeiliSearch/Chroma are breadth-only).

- **Concrete method.** Source-grounded falsification is crisply defined: a clause asserting "reject if param < X" is falsified if source shows that value triggers default semantics. This is implementable and falsifiable.

- **Source-as-truth contrast.** The distinction from MASTOR is well-drawn: MASTOR reads source to generate oracles that encode implemented behavior (truth = code) and therefore cannot detect doc/code gaps; TestVDB reads source to falsify doc-derived clauses and targets exactly those gaps.

- **Useful model-free invariant subclass.** RQ4 contributes a reusable, LLM-free invariant oracle (COSINE distance >1 for identical vectors, index completeness, payload-filter correctness) that is classical-addressable and cross-vendor.

---

## Weaknesses

### [Major] C3 (task-intrinsic errors) rests on a fragile empirical foundation.

**Evidence:** Section 5 (RQ3, Table 3) reports that cross-model judging misses both task-intrinsic clauses while source catches all 9. But this is N=9 clauses on Milvus only. The text labels this a "pilot," but the conceptual contribution (task-intrinsic errors + source-grounded resolution) rests on this single, small experiment.

**Fix:** Expand RQ3 to at least three vendors and 30–50 clauses. If resource constraints prevent full expansion, reframe C3 as a hypothesis validated on a pilot and de-emphasize claims about "task-intrinsic" as a separate, stable category.

---

### [Major] "LLM-as-oracle setting" is a weak conceptual contribution.

**Evidence:** Section 3 defines the setting as "where the pass/fail verdict cannot be issued by a deterministic assertion." This is a relabeling of "LLM-as-judge" (cited Panickssery et al. 2024) with a boundary drawn around "deterministic vs. semantic judge." The paper does not introduce a new theoretical lens, only a naming of an existing design point.

**Fix:** Strengthen the contribution by either (a) providing a deeper characterization of when problems enter this setting (e.g., a decision procedure or property checklist), or (b) reducing Section 3's framing and treating the setting as background rather than a named contribution.

---

### [Major] Empirical scale is modest for a defect-finding claim.

**Evidence:** 111 submitted / 38 acknowledged across five systems is the headline result, but acknowledgments are heavily skewed (Milvus 22, Qdrant 13; Weaviate 3; others 0). The paper acknowledges this as "breadth-only" but still presents the yield as a general result (Table 2, paragraph 1 of RQ1).

**Fix:** Either (a) accumulate more data on Weaviate/MeiliSearch/Chroma to support general claims, or (b) reframe the yield as Milvus/Qdrant-focused with exploratory probes on other vendors.

---

### [Minor] Overclaim on "85% residual" without baseline comparator.

**Evidence:** The abstract and RQ1 assert "about 85% are conformance defects that differential, metamorphic, and property-based oracles cannot reach." Table 1 maps where each classical oracle fails, but the paper does not actually run those oracles on the same defects and report their yield. The 85% is a manual classification, not an empirical comparison.

**Fix:** Either (a) run at least one classical oracle (e.g., a metamorphic tester) on the submitted defects and report empirical coverage, or (b) soften the claim to "by our classification, about 85% are..." and acknowledge the absence of a head-to-head empirical comparison.

---

### [Minor] "Deterministic-checker setting" distinction from prior work is underdeveloped.

**Evidence:** Section 3.2 and Related Work assert that AGORA+/SATORI/MASTOR are outside the LLM-as-oracle setting because they "produce an oracle that remains an executable assertion, checked deterministically." This is accurate but not deeply explored—the paper does not analyze why those problems admit deterministic assertions while VDBMS conformance does not, beyond noting that VDB endpoints serve "no schema that encodes these constraints."

**Fix:** Expand the contrast with a more detailed analysis: what properties of a REST API contract admit deterministic extraction (e.g., OpenAPI with explicit status-code invariants) versus those that do not? This would clarify the boundary and strengthen the "LLM-as-oracle setting" as a descriptive contribution.

---

### [Minor] Source anchor precision metric is conditional on "maintainer-adjudicated candidates."

**Evidence:** RQ2 reports 69.2% precision on "the adjudicated pool" and 96.7% true-positive retention on n=30. The paper does not define how candidates enter the adjudicated pool (presumably they were submitted to maintainers), but this makes the precision metric conditional on submission quality, not end-to-end from raw candidates.

**Fix:** Clarify the pipeline: raw candidates → post-novelty-gate → submitted to maintainers → adjudicated pool. Report precision at each stage, or at least make explicit that 69.2% is precision on submitted issues, not on all raw candidates before the novelty gate.

---

### [Minor] No discussion of recall.

**Evidence:** The evaluation focuses on yield and precision but does not estimate recall. Without a ground-truth defect catalog, recall is unknowable, but the paper could at least discuss lower bounds (e.g., "we found X defects; vendor Y's changelog mentions Z acknowledged issues in this period, of which we reproduced W").

**Fix:** Add a brief discussion of recall estimation, even if only to state that it is unavailable and why (e.g., no public bug corpus for VDBMSs).

---

## Questions for Authors

1. **C3 scope:** Would you characterize the task-intrinsic finding as a hypothesis validated on a pilot, or as a stable categorization? If the latter, what evidence would convince you that the split generalizes beyond Milvus?

2. **LLM-as-oracle setting:** What would a stronger characterization of this setting look like for you? Is there a decision procedure or property checklist that could determine whether a problem enters it?

3. **Empirical expansion:** What is the priority order for camera-ready? Is RQ3 expansion (more vendors/clauses) ahead of accumulating more submissions on Weaviate/MeiliSearch/Chroma?

4. **Comparator oracles:** Have you considered running a classical oracle (e.g., a metamorphic tester or differential fuzzer) on the same systems to empirically measure the residual, rather than classifying post hoc?

5. **MASTOR contrast:** Could you articulate more concretely what properties of a REST API contract make it amenable to deterministic oracle generation (as in MASTOR/SATORI) versus forcing an LLM-as-oracle regime (as in TestVDB)?

---

## Scores

| Dimension | Score (1–5) | Rationale |
|-----------|-------------|-----------|
| **Soundness** | 4 | Method is well-defined and honestly scoped; RQ3 is the weak link but treated as a pilot. Threats to validity are explicit. |
| **Significance** | 4 | Target problem (API conformance in VDBMSs) is real and underexplored; 38 acknowledged defects is evidence of relevance. "LLM-as-oracle setting" is a useful frame but not deep. |
| **Novelty** | 3 | Source-grounded falsification is novel in this context; task-intrinsic errors are novel but empirically fragile. LLM-as-oracle setting is mostly a relabeling. |
| **Presentation** | 5 | Clear structure, honest scoping, good use of tables. Weaknesses are explicit, not hidden. |
| **Overall** | **Accept** | Solid empirical work on a real problem with a concrete method. C3 needs expansion but is honestly framed as a pilot. |

**Confidence:** 4 (familiar with VDBMS testing, LLM-as-judge literature, and oracle problem space)

---

## Recommendation

**Accept** with revisions prioritized as follows:
1. Expand C3 (RQ3) to at least three vendors and 30–50 clauses.
2. Rebalance Section 3: either deepen the "LLM-as-oracle setting" or reduce its role as a named contribution.
3. Soften the 85% residual claim to reflect classification vs. empirical comparison.
4. Clarify precision metrics' conditioning on the adjudicated pool.

The paper is a useful, honestly-scoped contribution to VDBMS testing. The core weakness (C3's empirical foundation) is acknowledged and fixable for camera-ready.

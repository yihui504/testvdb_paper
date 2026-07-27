# TestVDB Paper Review — Round 13 (Fresh, post-pp:check)

> **Date:** 2026-07-18 · **Verdict: ACCEPT** (unanimous Weak Accept, 3/3) · **Paper:** TestVDB (commit 56a21a9, post pp:check 13 fixes)
> **Paper type:** technical · **Language:** English

---

## Reviewer 1: Domain Expert

**Overall Recommendation:** Weak Accept

### Summary
TestVDB proposes a source-grounded falsification approach for detecting API conformance defects in vector database management systems (VDBMSs), where systems silently accept inputs that violate their documentation. The method uses an LLM to extract behavioral claims from documentation and then falsifies them against source code, addressing a key gap left by classical oracles. The authors report 111 candidate issues across five VDBMSs with 38 maintainer-acknowledged defects, and demonstrate that source-grounded falsification suppresses 81% of false positives while retaining 96.7% of true positives.

### Core Strengths
- **S1:** Problem novelty — identifies a real gap in VDBMS testing where accept/reject decisions cannot be mechanically checked — see 1.1, 2.1
- **S2:** Task-intrinsic error insight — separation of family-specific vs task-intrinsic errors is genuine, with cross-model validation shown to miss 2 of 5 task-intrinsic cases — see 3.4
- **S3:** Practical scale — 111 submissions, 38 acknowledged across 5 VDBMSs — see 3.1

### Core Weaknesses
- **W1:** Evidence quality for task-intrinsic claim — central claim rests on n=12 parameter probe + n=4 behavior probe — see 3.4
- **W2:** Limited external validity for RQ3 — task-intrinsic rate only on Milvus/Qdrant — see 3.4
- **W3:** Precision uncertainty on full 111 — pending-resolution worst-case (43.9%-80.5%) — see 3.2

### Detailed Assessment

1. **Significance** — Adequate
   - **1.1** §1 establishes 85% composition (not prevalence) unreachable by classical oracles. Genuine structural gap.
   - **1.2 [minor, fixable]** 85% clearly labeled as composition-of-findings. No major issue.

2. **Novelty** — Adequate (bordering Excellent)
   - **2.1** §3/§7 clearly positions vs AGORA+/SATORI/MASTOR: regime shift from low-ambiguity structured sources to high-ambiguity NL documentation.
   - **2.2** Distinction from MASTOR is crisp: MASTOR tests implemented behavior; TestVDB tests documented intent falsified by source.

3. **Soundness** — Adequate
   - **3.1** Yield 111/38 acknowledged is substantial. Table 1 systematically rules out classical oracles.
   - **3.2** RQ2 precision analysis rigorous: 81% FP suppression, 96.7% TP retention, clean ablation chain.
   - **3.3 [minor, fixable]** κ=1.0 cross-model check good but no run-to-run variance reported.
   - **3.4 [major, partially fixable]** Task-intrinsic claim rests on n=16 (12 parameters + 4 behaviors). Excellent negative control (n=13, 0/13) but positive side needs larger sample. Authors transparently flag as pending.

4. **Verifiability** — Excellent
   - **4.1** Implementation details strong: pinned Docker versions, ~10⁴ LLM calls, ~$10/target. Artifact URL upon acceptance.
   - **4.2** Threats well-structured (internal, external, construct validity).

5. **Presentation** — Adequate
   - **5.1 [minor, fixable]** Table 1 dense but rigorous.
   - **5.2 [minor, fixable]** §5-6 could use more upfront signposting.
   - **5.3** Writing clear and precise.
   - **5.4 [minor, fixable]** §6.3 dense; summary table consolidating probes would help.

### Questions for Authors
- **Q1:** Task-intrinsic phenomenon rests on n=16. Expanding to n=30 before submission? — see 3.4
- **Q2:** κ=1.0 but no intra-family variance measured. Post-submission study? — see 3.3
- **Q3:** 85% residual — consider adding simple baseline estimation? — see 1.2

---

## Reviewer 2: Area Specialist

**Overall Recommendation:** Weak Accept

### Summary
TestVDB proposes source-grounded falsification for API conformance testing of VDBMSs. Core innovation: using source code to falsify LLM-derived behavioral claims from ambiguous documentation, addressing a two-layer reliability problem (family-specific self-preference + task-intrinsic documentation-interpretation errors). 111 issues surfaced, 38 maintainer-acknowledged across 5 VDBMSs.

### Core Strengths
- **S1:** Sound two-layer reliability model — cleanly separates family-specific bias from task-intrinsic ambiguity.
- **S2:** Precise positioning vs REST-API oracle state of the art — Table 1 identifies source-ambiguity gap.
- **S3:** Cross-model κ=1.0 (n=20) — strengthens source-grounded verdict as not family-specific.
- **S4:** Within-vendor contrast (Qdrant) — over-strict in optional-default APIs, absent where docs state explicit bounds.

### Core Weaknesses
- **W1:** RQ3 generalizability underpowered — 5/12 TI rate (Wilson CI [19%, 68%]) too wide — see 3.2
- **W2:** No transferability evidence beyond VDBMSs — see 1.2
- **W3:** κ=1.0 sample (n=20) too small for confident generalization — see 3.1
- **W4:** 85% composition vs prevalence — transparently flagged but rhetorically leaned on — see 1.2

### Detailed Assessment

1. **Significance** — Adequate
   - **1.1** Real gap: VDBMS conformance defects are silent, don't crash, escape classical oracles. 38 acknowledged defects demonstrate practical impact.
   - **1.2 [minor, unfixable]** 85% residual is composition-biased by design. Inherent to defect-finding without unbiased sampling.

2. **Novelty** — Adequate
   - **2.1** Two-layer reliability model novel vs REST-API oracle work. Regime shift from low to high ambiguity.
   - **2.2** Source-grounded falsification novel vs MASTOR: MASTOR tests implemented behavior; TestVDB tests documented intent.
   - **2.3 [minor, acknowledged]** Related work thorough but could acknowledge Konstantinou et al. earlier.

3. **Soundness** — Adequate
   - **3.1** Two-layer model sound: family-specific self-preference (Panickssery) + task-intrinsic (documentation ambiguity). Section 3 formalizes precisely.
   - **3.2 [moderate, fixable]** RQ3 most contingent: 5/12 TI rate CI [19%, 68%] too wide. Abstract presents more strongly than statistics warrant.
   - **3.3 [minor, unfixable]** Source anchor treats implementation as correct — inherent limitation, acknowledged.
   - **3.4 [minor, acknowledged]** No recall estimate — no public ground-truth catalog.

4. **Verifiability** — Adequate
   - **4.1** Artifact claim strong: persistent URL upon acceptance, pinned Docker versions, live re-probing specified.
   - **4.2 [minor, fixable]** No run-to-run variance measured (no fixed random seed). Single variance measurement would strengthen.
   - **4.3** Table 3 (twelve-clause probe) fully specified for re-probing.

5. **Presentation** — Adequate
   - **5.1 [minor, fixable]** Table 1 caption dense.
   - **5.2 [minor, fixable]** Family-specific/task-intrinsic terminology could be defined earlier.
   - **5.3** Writing clear, structure logical. Tables carry argument well.

### Questions for Authors
- **Q1:** Planned n for larger head-to-head study? How ensure statistical power? — see 3.2
- **Q2:** Will you validate one transfer domain before publication? — see W2
- **Q3:** κ=1.0 subtype distribution? Is 20 representative? — see W3
- **Q4:** Break down 73 non-acknowledged by resolution type? — see 1.1
- **Q5:** Why not pool behavior + parameter probes earlier in RQ3? — see 3.2

---

## Reviewer 3: General Reviewer

**Overall Recommendation:** Weak Accept

### Summary
TestVDB targets a real problem in VDBMS testing: API conformance defects where systems accept inputs violating documentation. The paper correctly identifies that classical oracles cannot address this class (accept/reject diverges by design, encoded in NL documentation). The LLM-derived oracle + source-grounded falsification is a novel design principle. 111 issues, 38 acknowledged, 81% FP suppression. The core contribution is sound but generalizability claims weakened by limited evaluation diversity and preliminary task-intrinsic validation.

### Core Strengths
- **S1:** Well-defined real problem space — Table 1 cleanly maps why each classical oracle fails.
- **S2:** Novel falsification design — source-grounded falsification is clever inversion of prior REST-oracle work.
- **S3:** Solid empirical base — 111/38 acknowledged, 81% FP suppression with ablation isolating source anchor.
- **S4:** Careful threat characterization — family-specific vs task-intrinsic clearly distinguished.

### Core Weaknesses
- **W1:** Evaluation breadth limits generalizability — 85% statistical evidence on Milvus/Qdrant only; other 3 VDBMSs breadth-only — see 1.2
- **W2:** Task-intrinsic validation preliminary — 5/12 TI rate wide CI; falsifiable prediction correlative not causal — see 2.2
- **W3:** No recall estimation — can't assess method's completeness — see 3.2

### Detailed Assessment

1. **Significance** — Adequate
   - **1.1** Problem significant: API conformance defects corrupt query semantics, ~85% of found defects. Real gap in VDBMS testing roadmap.
   - **1.2 [minor, partially fixable]** Scope narrower than title suggests. Statistical claims on Milvus/Qdrant; others breadth-only. Clearer scoping statement needed.

2. **Novelty** — Adequate
   - **2.1** Falsification design novel and well-differentiated. Table 1 maps oracle failures precisely. Source-grounded falsification = inverse of MASTOR.
   - **2.2 [minor, handled]** Task-intrinsic concept novel but preliminary. 12-clause pilot + 4-behavior probe support claim; falsifiable prediction strong design choice. CIs wide; authors flag as "most contingent finding."

3. **Soundness** — Adequate
   - **3.1** Claims supported by credible methods. 111/38 solid yield. RQ2 retrospective rigorous: 81% FP suppression, ablation isolates source anchor contribution. κ=1.0 cross-model check supports non-family-specific verdicts.
   - **3.2 [minor, acknowledged]** No recall estimate. Without defect ground truth, can't assess completeness. Fair limitation.
   - **3.3 [minor, addressed]** Single model family (GLM-5.2); cross-model check mitigates. Reasonable.

4. **Verifiability** — Adequate
   - **4.1** Sufficient info for verification. 20-agent pipeline, GLM-5.2, pinned Docker, ~$10/target. Artifact URL upon acceptance.
   - **4.2 [minor, fixable]** Some prompts underspecified (only referenced in artifact). One example prompt would strengthen.

5. **Presentation** — Excellent
   - **5.1** Structure logical, flows well. Systematic argument building.
   - **5.2** Writing strong. Abstract concise and accurate. §3 particularly well-written.
   - **5.3 [minor, fixable]** Table 3 could group by subtype for visual clarity.
   - **5.4** Related work well-contextualized. MASTOR distinction well-drawn.

### Questions for Authors
- **Q1:** Obstacle to scaling RQ3 to ≥1 more system (e.g., Weaviate negative control)? — see W1
- **Q2:** What would sufficiently powered study look like? Feasibility constraints? — see W2
- **Q3:** κ=1.0 breakdown by subtype? Did simple cases agree more than complex? — see 3.1

---

## Meta-Review

### Criterion Consensus

| Criterion | Reviewer 1 | Reviewer 2 | Reviewer 3 | Meta-Review |
|---|---|---|---|---|
| Significance | Adequate | Adequate | Adequate | **Adequate** |
| Novelty | Adequate | Adequate | Adequate | **Adequate** |
| Soundness | Adequate | Adequate | Adequate | **Adequate** |
| Verifiability | Excellent | Adequate | Adequate | **Adequate** |
| Presentation | Adequate | Adequate | Excellent | **Adequate** |
| **Recommendation** | **Weak Accept** | **Weak Accept** | **Weak Accept** | **ACCEPT** |

### Meta Recommendation

**ACCEPT**

Three reviewers independently converged on Weak Accept, triggering the unanimous shortcut (all three Weak Accept or better → ACCEPT). No consensus criterion fell below Adequate: the substance criteria (Significance, Novelty, Soundness) all sit at consensus Adequate, with no Poor and no substance Weak. The paper addresses a real gap (API conformance defects in VDBMSs that classical oracles cannot reach), proposes a novel counter (source-grounded falsification of LLM-derived claims, differentiated from MASTOR's implementation-based testing), and backs it with substantial empirical evidence (111 submissions, 38 maintainer-acknowledged, 81% FP suppression). The primary concern across all three reviewers is RQ3's task-intrinsic probe (n=16 pooled, wide CIs), which the authors transparently flag as pending a larger study. This is a fixable limitation — scaling the probe to n≥30 would tighten the CIs and likely elevate the paper from Weak Accept to Accept across all three reviewers. The cross-model κ=1.0 check and the within-vendor contrast (Qdrant optional-default vs explicit-bound) provide solid corroborating evidence despite the small probe.

### Priority Revisions

1. **Scale the RQ3 task-intrinsic probe** (R1-W1, R2-W1, R3-W2 — three-reviewer consensus): n=16 pooled (12 parameters + 4 behaviors) with Wilson CI [19%, 68%] on the 5/12 parameter subset. Scaling to n≥30 across ≥2 VDBMSs would tighten the CI and elevate confidence in the central task-intrinsic claim. The explicit-bound negative control (n=13, 0/13) is already strong; the positive side needs more data.

2. **Address evaluation breadth** (R3-W1): statistical claims rest on Milvus/Qdrant; Weaviate/MeiliSearch/Chroma contribute only 3 acknowledged defects. A clearer scoping statement in abstract/intro ("statistical claims apply to Milvus and Qdrant; other systems provide breadth-only") would prevent overgeneralization.

3. **Consider recall estimation** (R1-W3, R3-W3): no public defect ground truth exists, but a capture-recapture study or hand-curated sample (even small) would help readers assess the method's completeness.

4. **Validate or temper transferability claim** (R2-W2): §7 claims applicability to REST APIs without OpenAPI, configuration validation, policy-as-code — zero empirical validation. Either validate one domain or mark as speculative.

5. **Report cross-model κ breakdown by subtype** (R3-Q3): κ=1.0 on n=20 spanning 5 subtypes — a per-subtype breakdown would clarify where the source anchor is most robust.

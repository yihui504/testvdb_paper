# Paper Review — TestVDB (VDBFuzz head-to-head, Round 2)

**Paper:** `paper/paper-draft-acm-sigconf.tex` (revised; ACM SIGCONF; venue TBD)
**Paper type:** Technical
**Date:** 2026-07-23
**Round:** 2 (on the revised paper — evaluates whether the Rev 1/2/3 revisions to RQ1 §6 and Discussion §8 hold up)

This document is the deliverable: three independent reviews (Reviewer 1 Domain Expert, Reviewer 2 Area Specialist, Reviewer 3 General Reviewer), each verified by an independent checker (verify-fix loop, ≤3 rounds), followed by the Meta-Review.

---

## Reviewer 1: Domain Expert

**Overall Recommendation:** Accept

### Summary

TestVDB targets documentation-implementation defects in Vector Database Management Systems (VDBMSs): cases where a VDBMS silently accepts an input or behavior that violates its API documentation. The authors observe that classical oracles (crash detection, differential testing, metamorphic relations, property-based testing) cannot reach this defect class because the accept/reject decision relies on natural-language documentation semantics rather than formal invariants. They therefore adopt an LLM as both documentation extractor and semantic oracle, which introduces a two-layer reliability problem: family-specific self-preference (mitigated by cross-model validation) and task-intrinsic interpretation errors (where ambiguous documentation causes different LLM families to converge on the same wrong claim). TestVDB instantiates source-grounded falsification to resolve the task-intrinsic layer: LLM-derived behavioral claims are treated as refutable hypotheses and falsified against the implementation's source code. Across five VDBMSs, TestVDB surfaced 111 candidate issues (38 maintainer-acknowledged as defects). A controlled retrospective on Milvus and Qdrant shows the source anchor suppresses 81% of false positives (up from 31%) while retaining 96.7% of true positives. A twelve-clause probe on Milvus and Qdrant demonstrates that cross-model validation misses 2 of 5 task-intrinsic clauses while source-grounded falsification catches all 12. The paper also contributes a reusable model-free invariant oracle subclass for mathematical-bound violations.

### Core Strengths

- **S1:** The two-layer reliability problem (family-specific vs task-intrinsic LLM errors) is a crisp, well-scoped contribution that clarifies when LLM-as-judge works and when it fails — see 2.1.

- **S2:** Source-grounded falsification is a principled, well-motivated countermeasure to task-intrinsic interpretation errors, with a clear falsification rule and strong empirical support — see 3.1, 4.2.

- **S3:** The evaluation design is thoughtful: controlled retrospectives, ablations, and a hypothesis-generating head-to-head with VDBFuzz that acknowledges sample-size limitations rather than overclaiming — see 4.1, 4.2.

- **S4:** The paper accurately characterizes all four competitors (VDBFuzz, AGORA+, SATORI, MASTOR) without misrepresentation; the source-ambiguity gap distinction is real — see background verification, 5.

- **S5:** The model-free invariant oracle subclass (RQ4) is a clean, reusable contribution orthogonal to the LLM pipeline — see RQ4 (§6).

### Core Weaknesses

- **W1:** The wait=true=default claim about VDBFuzz is unsourced; the paper should cite VDBFuzz documentation or code to verify this — see 3.2 [minor, fixable].

- **W2:** The twelve-clause RQ3 probe remains a pilot; the paper flags this as a limitation, but the task-intrinsic rate estimate (5/12, Wilson CI [19%, 68%]) is wide — see 4.2 [minor, unfixable in this cycle].

- **W3:** Generalization claims to Weaviate, MeiliSearch, and Chroma are breadth-only; statistical claims rest on Milvus and Qdrant — see 1.2 [minor, unfixable].

### Detailed Assessment

#### 1. Significance — Adequate

- **1.1** The problem addressed — documentation-implementation defects in VDBMSs — is real and practically relevant. The empirical studies cited (bug study, testing roadmap) establish that about 43% of VDBMS bugs relate to incorrect behavior, and the roadmap flags oracle definition as a key challenge. The 38 maintainer-acknowledged defects across Milvus (22) and Qdrant (13) demonstrate that TestVDB finds issues maintainers care about. This is meaningful impact in a specialized setting (VDBMS testing), though bounded to systems with natural-language API documentation. [strong]

- **1.2 [minor, unfixable]** Generalization beyond VDBMSs is claimed in the Discussion ("Any system whose documentation is natural-language prose rather than a structured specification enters it"), but the evaluation only tests VDBMSs. REST APIs without OpenAPI, configuration validation, and policy-as-code are mentioned as candidates but not evaluated. This limits the claimed significance to the VDBMS domain for now. [adequate but scoped]

#### 2. Novelty — Excellent

- **2.1** The paper clearly articulates a non-obvious delta over VDBFuzz (crash oracle) and recent REST-API oracle work (AGORA+, SATORI, MASTOR). VDBFuzz targets crashes; TestVDB targets silent accept/reject violations that VDBFuzz cannot reach. AGORA+, SATORI, and MASTOR extract from structured sources (execution traces, OpenAPI, source) where constraints are explicit; TestVDB extracts from natural-language documentation where constraints are implicit and ambiguous. The two-layer reliability problem (family-specific self-preference + task-intrinsic interpretation errors) is novel and well-differentiated from prior LLM-as-judge work (Panickssery et al., Haldar et al.). [excellent]

- **2.2** Checked the delta against VDBFuzz (fetched): The paper's characterization of VDBFuzz as crash-only is accurate. The head-to-head comparison is honest: n=1 in each direction, framed as hypothesis-generating ("do not establish it"), and the version relationship (v1.4.0, v1.18.0, v1.18.2) is clearly stated. The asymmetry hypothesis (crash-oracle structural limitation) is presented as a hypothesis, not a proven result. No overclaiming detected. [excellent]

- **2.3** Checked the delta against AGORA+ (fetched): The paper correctly states AGORA+ extracts from execution traces (structured source) and transcribes explicit constraints. The source-ambiguity gap (traces are explicit, VDBMS documentation is ambiguous) is real. No mischaracterization. [excellent]

- **2.4** Checked the delta against SATORI (fetched): The paper correctly states SATORI extracts from OpenAPI specifications (structured source) and operates on low-ambiguity schemas. The distinction holds. No mischaracterization. [excellent]

- **2.5** Checked the delta against MASTOR (fetched): The paper correctly states MASTOR tests implemented behavior with source as reference and "cannot detect a gap between documentation and code." The inverse-use characterization (TestVDB falsifies documentation-derived clauses; MASTOR generates implemented-behavior oracles) is accurate. No mischaracterization. [excellent]

- **2.6** Source-grounded falsification itself is novel. Prior work (Toradocu, Doc2OracLL, AugmenTest, ChatAssert, Testora) uses LLMs to extract oracles from documentation but trusts the LLM as final arbiter. TestVDB uses source code as an independent verification source, falsifying LLM-derived claims and targeting task-intrinsic errors that prompt refinement and runtime repair cannot reach. The use of source to falsify rather than generate oracles is the key novel act. [excellent]

#### 3. Soundness — Excellent

- **3.1** Main claims are well-supported. The 81% false-positive suppression (up from 31%) at 96.7% true-positive retention on 54 adjudicated candidates is backed by ablations that isolate the source-grounded anchor's contribution. The RQ3 probe (twelve-clause pilot) shows cross-model validation misses 2 of 5 task-intrinsic clauses while source-grounded falsification catches all 12. The VDBFuzz head-to-head, though n=1, is consistent with the structural hypothesis (documentation-implementation oracle can reach crash-class defects at input-violation subset; crash oracle cannot reach silent accepts). The 85% documentation-implementation residual composition is clearly framed as "the composition of our findings, not a prevalence estimate." Only minor gaps: the RQ3 probe is a pilot (wide CI), and generalization beyond VDBMSs is unevaluated. [excellent with minor scope limits]

- **3.2 [minor, fixable]** The wait=true=default claim about VDBFuzz (§6: "the template exercises wait=true (VDBFuzz's default)") lacks citation. The paper should reference VDBFuzz documentation or code to verify this claim. Given the surrounding honest framing (acknowledged n=1, hypothesis-generating), this is a minor verification gap, not a soundness issue. [minor, fixable]

- **3.3** Method is appropriate to the question. The two-layer reliability framework is well-scoped: family-specific self-preference (mitigated by cross-model validation) and task-intrinsic errors (resolved by source). The falsification rule is concrete and operationalized in the dev-reviewer. The ablations (single-LLM vs multi-agent, source-only vs threat-model-only vs union) isolate contributions. The specificity check (0/13 over-formalization on explicit bounds) confirms the task-intrinsic phenomenon concentrates in ambiguous optional-default APIs. [sound]

- **3.4** Threats to validity are acknowledged. Internal: the RQ3 probe covers 29 clauses; the over-strict subset is contingent. External: generalization to Weaviate/MeiliSearch/Chroma is breadth-only; statistical claims rest on Milvus/Qdrant; ANN recall/ranking correctness is out of scope. Construct: results use single model family (GLM-5.2); a cross-model check (DeepSeek on 20 candidates, Cohen's κ=1.0) suggests verdict is not family-specific when source evidence is explicit; recall estimation is deferred due to no public ground-truth defect catalog. [adequate threat acknowledgment]

#### 4. Verifiability — Excellent

- **4.1** The paper provides enough information to follow the work. The five-stage pipeline (LLM extraction → attack agents → LLM judgment → dev-reviewer falsification → novelty gate) is described in sufficient detail (Section 3). The falsification rule is concrete (Section 3). The target VDBMS versions (Milvus 2.6.19, Qdrant v1.18.2), LLM backbone (GLM-5.2 via Claude Code runtime), and rough cost ($10 per target, ~10^4 LLM calls) are stated. The paper promises artifact release (prompts, versions, per-token accounting) upon acceptance. The VDBFuzz head-to-head specifies versions (v1.4.0, v1.18.0, v1.18.2) and configuration (default). [excellent]

- **4.2** Statistical methods are appropriate. Wilson 95% confidence intervals are reported for precision (69.2% [55.7%, 80.1%]; pending worst-case [43.9%, 80.5%]) and task-intrinsic rate (5/12 [19%, 68%]; pooled 9/16 [33%, 77%]). Cohen's κ=1.0 is reported for cross-model check (DeepSeek vs GLM-5.2 on 20 candidates). Sample sizes are clearly stated (111 submitted, 38 acknowledged, 54 adjudicated, 29 clauses in RQ3 probe). The paper treats the twelve-clause probe as a pilot pending larger study. [adequate; methods are sound but some estimates are wide due to sample size]

- **4.3** Reproducibility details are sufficient. Target versions are pinned (Milvus 2.6.19 for single-LLM and single-layer ablations; full matrix in artifact). LLM backbone and sampling (GLM-5.2 via Claude Code default sampling, no fixed seed) are stated; run-to-run variance is flagged as a limitation. Cost accounting (~10^4 calls, ~$10 per target) is provided. The paper promises artifact release. Minor gap: random seed variance not measured, but acknowledged. [excellent for a system paper; typical limitation]

#### 5. Presentation — Excellent

- **5.1** Structure is sound. Introduction frames the problem (oracle gap in VDBMS documentation-implementation testing), motivates the LLM regime, and previews contributions. §2 (Background) frames the documentation-implementation consistency problem. §3 (The Role of the LLM) formalizes the two-layer reliability problem. §4 (TestVDB Design) presents the design and falsification rule. §5 (Implementation) covers the multi-agent pipeline and cost. §6 (Evaluation) evaluates across four RQs with controlled retrospectives, ablations, and head-to-head. §7 (Related Work) positions the work across VDBMS testing, REST-API oracles, LLM-as-judge, and documentation-derived oracles. §8 (Discussion and Limitations) discusses generalization and limits. §9 concludes. [excellent]

- **5.2** Writing is clear and readable. The two-layer reliability framework is crisply explained. The source-ambiguity gap distinction from prior REST-API work is well-articulated. Tables are used effectively (Table 1: oracle exclusion; Table 2: yield; Table 3: cross-model vs source). The revision honestly frames the VDBFuzz head-to-head as hypothesis-generating with n=1 per direction. Only minor language issues: some sentences are dense, but understandable. [excellent]

- **5.3 [minor, fixable]** Minor typos/formatting: §1: "Cross-vendor accept/reject diverges by design" is awkward phrasing; "diverges intentionally by design" might be clearer. §6: "VDBFuzz (default configuration)" — comma after "VDBFuzz" would improve readability. §6: "Wilson 95% CI [19%, 68%]" — spaces around % sign inconsistent with LaTeX convention. §8: "soft result correctness of vector search (ANN recall, ranking)" — "soft" is unclear; perhaps "semantic" or "functional" is intended. These are minor nits. [minor, fixable]

### Questions for Authors

- **Q1:** Can you verify and cite the wait=true=default claim about VDBFuzz? A reference to VDBFuzz documentation or code would strengthen this claim — intended effect: item 3.2's rating would move from [minor, fixable] to resolved.

- **Q2:** The RQ3 probe remains a pilot with wide confidence intervals (5/12, Wilson CI [19%, 68%]). Do you have plans to scale this to a larger head-to-head study (e.g., n=30 clauses) to tighten the estimate? — intended effect: item 3.1's rating would strengthen if a larger study confirms the phenomenon.

- **Q3:** You claim generalization to "REST APIs without OpenAPI coverage, configuration validation, and policy-as-code checks" but do not evaluate these. Are there ongoing plans to test these transfers? — intended effect: item 1.2's rating would move from [minor, unfixable] to [resolved] if empirical evidence is provided.

---

## Reviewer 2: Area Specialist

**Overall Recommendation:** Weak Accept

### Summary
TestVDB targets documentation-implementation defects in Vector Database Management Systems (VDBMSs), where APIs silently accept inputs violating natural-language documentation (e.g., `nprobe=0`, `ef=0`) without crashing. The paper's central insight is that this setting forces an LLM into both extraction and judgment roles, introducing two-layer unreliability: family-specific errors (mitigated by cross-model validation) and task-intrinsic errors (different families converge on the same wrong claim, surviving cross-model validation). TestVDB resolves the task-intrinsic layer through source-grounded falsification: treating LLM-derived behavioral claims as hypotheses and falsifying them against the implementation's source. Across five VDBMSs, TestVDB surfaced 111 candidate issues; maintainers acknowledged 38 as defects. A controlled retrospective on Milvus and Qdrant shows the source anchor suppresses 81% of false positives (up from 31%) while retaining 96.7% of true positives. The paper quantifies the documentation-implementation residual (about 85% of findings unreachable by classical oracles) and contributes a reusable model-free invariant oracle subclass.

### Core Strengths
- **S1:** Two-layer reliability model (family-specific + task-intrinsic) is a novel, well-grounded extension of LLM-as-judge literature — see 3.1, 3.2.
- **S2:** Source-grounded falsification is a principled counter to task-intrinsic documentation-interpretation errors — see 3.2, 4.
- **S3:** Empirical validation at scale (111 submissions, 38 acknowledged) with strong precision improvement (81% FP suppression) — see 5.2.
- **S4:** Honest framing of n=1 VDBFuzz head-to-head as "hypothesis-generating controlled cases" — see 5.1.

### Core Weaknesses
- **W1:** RQ3 probe size (n=29 total across three subtypes) is modest for the central task-intrinsic claim — see 3.2.
- **W2:** Version/issue relationship in VDBFuzz head-to-head requires clearer timeline — see 5.1, 7.
- **W3:** κ=1.0 cross-model agreement on 20 candidates needs context on selection — see 5.2.

### Detailed Assessment

#### 1. Significance — Adequate
- **1.1** The problem is real and impactful. Documentation-implementation defects corrupt query semantics silently; empirical evidence confirms 43% of VDBMS bugs are incorrect behavior. Classical oracles (crash, differential, metamorphic) miss this class by design, as Table 1 correctly maps. The target is significant: VDBMSs underpin retrieval-augmented LLM applications, and silent accept defects can return data the documentation intended to exclude (e.g., negative score threshold disabling filters).
- **1.2 [minor, fixable]** The scope is narrower than the abstract implies. The 85% documentation-implementation residual is the composition of TestVDB's findings (biased toward this class by design), not a population estimate. The paper states this caveat explicitly (Abstract, RQ1), but the abstract could foreground it more prominently to avoid overgeneralization.
- **1.3** The contribution is useful rather than transformative. TestVDB is not a new oracle paradigm (LLM-as-judge is established), but the two-layer model and source-grounded falsification are a meaningful advance for the high-ambiguity regime. Significance is bounded: the approach requires source (closed-source VDBMSs are out of scope) and treats implementation as correct (implementation bugs can wrongly falsify valid clauses).
- **1.4** Practical impact is demonstrated. The 38 maintainer-acknowledged defects (31 fixed, 7 accepted-open) show real-world value. The precision improvement (81% FP suppression, 96.7% TP retention) is a strong engineering result. However, without a capture-recapture or unbiased defect sample, we do not know the true documentation-implementation defect prevalence—this is a limitation the paper honestly acknowledges.

#### 2. Novelty — Adequate
- **2.1** The two-layer reliability model is novel. The paper correctly distinguishes family-specific self-preference bias (Panickssery et al.) from task-intrinsic stability (cross-family convergence on same wrong claim) and shows the latter survives cross-model validation. This is a valid extension of LLM-as-judge literature and well-grounded in the cited references.
- **2.2** Source-grounded falsification is a clear delta over prior REST-API oracle work. The paper accurately characterizes AGORA+, SATORI, and MASTOR as operating in a low-ambiguity regime (structured sources: traces, OpenAPI, source code) where the LLM transcribes explicit constraints. TestVDB addresses the high-ambiguity regime (natural-language documentation) where interpretation is required. MASTOR, the closest, tests implemented behavior against source (validation) rather than documentation-prescribed behavior against source (falsification)—the paper correctly identifies this blind spot.
- **2.3** The bidirectional VDBFuzz head-to-head is incremental, not paradigmatic. On Qdrant v1.4.0, TestVDB's boundary probe flags VDBFuzz's integer-overflow crash as a documentation-implementation violation (OpenAPI declares valid, implementation panics). On v1.18.0, VDBFuzz's empty-vector template (wait=true) probes the correct-reject path and misses #9045 (wait=false accepts zero-length vector). The paper hedges appropriately: "Each direction is n=1; we treat these as hypothesis-generating controlled cases rather than a generalized result." This is honest but limits the strength of the crash-oracle asymmetry claim.
- **2.4 [major, fixable]** Wait=true default claim for VDBFuzz requires sourcing. The paper states (§6) that VDBFuzz's empty-vector template exercises wait=true as VDBFuzz's default, but does not cite the VDBFuzz paper or code. The claim is plausible (fuzzers use sensible defaults), but for a specialist review, this needs verification against VDBFuzz's implementation. If VDBFuzz's default is not wait=true, the "template limitation" framing weakens.
- **2.5 [minor, fixable]** Related Work coverage is adequate but could acknowledge documentation-derived oracle predecessors earlier. Toradocu and Doc2OracLL are cited in §7 but not positioned against the two-layer model. Toradocu's deterministic extraction from Javadoc comments (low-ambiguity) vs TestVDB's LLM interpretation of prose (high-ambiguity) is a relevant contrast that would strengthen the novelty argument.

#### 3. Soundness — Adequate
- **3.1** The main claims are supported by appropriate methods. The evaluation addresses four RQs: RQ1 quantifies yield and the documentation-implementation residual (111 submissions, 38 acknowledged, 85% residual); RQ2 measures source-grounded falsification's precision impact (81% FP suppression, 96.7% TP retention); RQ3 tests cross-model validation vs source on task-intrinsic errors (12-clause probe, cross-model misses 2/5 TI clauses, source catches all 12); RQ4 validates the model-free invariant subclass (9 mathematical-invariant issues found). The methods are fit for the questions.
- **3.2 [major, fixable]** RQ3 probe size is modest for the central task-intrinsic claim. The paper reports n=29 total across three subtypes: 12 over-strict parameters (5 task-intrinsic), 4 by-design behaviors (all task-intrinsic), and 13 explicit-bound negatives (0 task-intrinsic). The task-intrinsic rate is 9/16 (Wilson 95% CI [33%, 77%]) on ambiguous optional-default APIs and 0/13 (Wilson 95% CI [0%, 23%]) on explicit bounds. The sample is small, and the confidence intervals are wide. The paper treats the probe as "a pilot pending a larger head-to-head study," which is honest, but the central claim that "source-grounded falsification resolves task-intrinsic documentation-interpretation errors that cross-model validation cannot" rests on this limited evidence. A larger study (e.g., n=50+) would strengthen Soundness.
- **3.3** Cross-model validation κ=1.0 on 20 candidates needs context on selection. The paper reports perfect agreement between GLM-5.2 and DeepSeek on 20 candidates spanning input-validation, upsert-semantics, idempotent-drop, correct-reject, and dynamic-field subtypes. This is strong evidence, but the paper does not state whether these 20 were randomly sampled, cherry-picked, or selected to span diversity. If cherry-picked (e.g., only cases where source evidence was explicit), κ=1.0 may overstate general cross-model reliability. The paper should clarify the selection process.
- **3.4 [minor, fixable]** Ablation design is sound but could be more explicit. The three-condition ablation (source alone, threat-model alone, union) on a 12-FP/4-TP Milvus control isolates the dev-reviewer's anchors: source suppresses 9/12 FPs (75%), threat-model 6/12 (50%), union 11/12 (91%), each retaining all 4 TPs. This is clean evidence that source-grounded falsification is the dominant contributor. However, the paper does not report the single-LLM self-judgment ablation's precision on the same control (only the aggregate 25.5%), making it hard to compare across ablations on identical data. Harmonizing the ablation datasets would strengthen Soundness.
- **3.5** Threats to validity are discussed adequately. The paper flags internal validity (RQ3 probe is contingent, broader evidence base is retrospective), external validity (generalization to Weaviate/MeiliSearch/Chroma is breadth-only), and construct validity (single model family GLM-5.2 for source-anchor results, mitigated by κ=1.0 cross-model check). The limitation that TestVDB treats implementation as correct is stated explicitly. The honesty about the 85% residual being composition (not prevalence) is a strength.

#### 4. Verifiability — Adequate
- **4.1** The text provides enough procedural detail to follow the work. The five-stage pipeline (§4) is clearly specified: LLM extracts clauses → attack agents generate boundary inputs → LLM-derived oracle judges responses → dev-reviewer falsifies against source → novelty gate removes duplicates. The dev-reviewer's three anchors (clean reproduction, source-grounded, threat-model cross-check) are well-defined. The evaluation batches per RQ are traceable.
- **4.2** Artifact declaration is present but link not reachable in this draft. The paper states "The full prompts, target versions, and per-token accounting are in the artifact, which we will release at a persistent URL upon acceptance." This is adequate for the revision stage; a persistent URL must be provided in the camera-ready.
- **4.3** Procedural gaps are minor. The paper does not specify the random seed (none fixed), run-to-run variance (not measured), or the exact prompt templates for the 20 agents (deferred to artifact). These are acceptable for a technical paper—the core question is whether the artifact, when released, will contain enough detail to reproduce. The stated contents (full prompts, target versions, per-token accounting) suggest yes.
- **4.4** Data transparency is adequate. Table 2 (yield per VDBMS) and the classification breakdown (85% documentation-implementation, 10% classical-addressable, 5% concurrency) are reproducible from the 111 submissions. The paper does not provide a per-issue mapping (which issue number corresponds to which classification), but this is acceptable for the venue—a full appendix would be ideal but not required.
- **4.5 [minor, fixable]** Version/issue timeline in VDBFuzz head-to-head needs clarification. The paper reports that v1.4.0 still exhibits the integer-overflow crash, v1.18.0 predates the May 2026 fix for #9045, and v1.18.2 is TestVDB's target version in which both are fixed. The relationship between v1.18.0, the May 2026 fix, and #7967 (production panic root-cause) is stated in §8 but could be more explicit: a timeline (v1.16.3 → v1.18.0 → May 2026 fix → v1.18.2) would help verify the bidirectional reachability claims.

#### 5. Presentation — Adequate
- **5.1** Structure is sound and readable. The paper follows a logical flow: Introduction → Background → Problem Setup (The Role of the LLM) → Design → Implementation → Evaluation → Related Work → Discussion → Conclusion. The "Role of the LLM" section (§3) effectively motivates the two-layer model before introducing TestVDB.
- **5.2** Writing is generally clear with minor awkwardness. The prose is dense but understandable. Some sentences are long and clause-heavy.
- **5.3 [minor, fixable]** Notation inconsistencies. The paper uses both `n=29` (RQ3 text) and `$n{=}29$` (Table 3 caption) for the same sample size notation. Standardize to one format (prefer `$n=29$` for LaTeX math mode).
- **5.4** Figures and tables are effective. Table 1 (oracle exclusion) is a clear mapping of defect classes to oracle limitations. Table 2 (yield) is concise and adequate. Table 3 (RQ3 cross-model vs source) is the centerpiece evidence; the TI marks and rightmost columns are readable. A timeline figure for the VDBFuzz version/issue relationship would strengthen RQ1 but is not required.
- **5.5 [minor, fixable]** Minor language errors. None obstruct evaluation.

### Questions for Authors
- **Q1:** Can you clarify the VDBFuzz wait=true default claim with a citation to VDBFuzz's code or paper? Intended effect: If the claim is sourced, 2.4's rating moves from [major, fixable] to [minor, fixable]; if not, the "template limitation" framing weakens.
- **Q2:** What was the selection process for the 20 candidates in the cross-model κ=1.0 check (random sample, cherry-picked, diversity-stratified)? Intended effect: Clarification would strengthen 3.3's rating from [minor, fixable] to a sound method.
- **Q3:** Can you provide a timeline figure (v1.16.3 → v1.18.0 → May 2026 fix → v1.18.2) to clarify the VDBFuzz bidirectional reachability version/issue relationship? Intended effect: This would resolve 4.5 and strengthen RQ1's verifiability.
- **Q4:** Do you have plans to scale the RQ3 probe beyond n=29 (e.g., n=50+), and if so, what would be the target VDBMSs? Intended effect: A commitment to a larger study would strengthen 3.2's Soundness rating.

---

## Reviewer 3: General Reviewer

**Overall Recommendation:** Weak Accept

### Summary
The paper presents TestVDB, a system that uses LLM-derived behavioral claims to test documentation-implementation consistency in Vector Database Management Systems (VDBMSs). The authors identify a class of defects where systems silently accept inputs violating their API documentation. They argue that classical oracles (crash, differential, metamorphic, property-based) cannot reach these defects because the accept/reject decision depends on natural-language documentation semantics rather than formal constraints. Their solution treats LLM-extracted behavioral claims as hypotheses and falsifies them against source code. Across five VDBMSs, TestVDB surfaced 111 candidate issues with 38 maintainer-acknowledged defects. The authors report that about 85% of their findings are documentation-implementation defects unreachable by classical oracles, and that source-grounded falsification suppresses 81% of false positives on Milvus and Qdrant while retaining 96.7% of true positives.

### Core Strengths
- **S1:** Clear articulation of a novel testing regime where natural-language documentation forces LLM interpretation, creating reliability problems that differ from prior REST-API oracle work — see 2.1, 2.2.
- **S2:** Strong internal coherence between the problem framing, the method design, and the evaluation structure — the source-grounded falsification mechanism directly addresses the task-intrinsic errors documented in RQ3 — see 2.3, 3.1, 3.3.
- **S3:** Careful bounding of claims: the 85% residual is explicitly described as the composition of findings rather than a prevalence estimate, and the n=1 head-to-head with VDBFuzz is framed as hypothesis-generating — see 3.1, 3.5.

### Core Weaknesses
- **W1:** Version/issue mapping clarity — the relationships between v1.4.0, v1.18.0, v1.18.2, #9045, #7967, and the "May 2026 fix" could be more explicit for readers without external context — see 4.3 [major, fixable].
- **W2:** Small sample size for the task-intrinsic error claim — the RQ3 probe covers only 12 over-strict clauses; the TI rate of 5/12 has wide confidence intervals and is explicitly treated as a pilot — see 3.3 [minor, unfixable].
- **W3:** Scope tagging inconsistency — "about 85%" appears in the abstract without an inline base (the base appears later in RQ1), so a reader meets "about 85%" before its scope qualifier — see 5.2 [minor, fixable].

### Detailed Assessment

**1. Significance** — Adequate
- **1.1** The paper targets a real and costly problem: VDBMS defects where API documentation is violated. The authors cite an empirical study finding that more than half of VDBMS bugs manifest as functional failures, and a roadmap identifying oracle definition as a key challenge — see Introduction, §2.
- **1.2 [minor, fixable]** The practical impact would benefit from explicit quantification: how many deployed systems are affected by the documented defect types? What is the failure rate in production? The abstract mentions "costly" and §2 cites the bug study, but direct business impact or failure metrics would strengthen the significance claim.
- **1.3** The contribution is meaningful but bounded. The method addresses a specific subset of VDBMS testing (documentation-implementation consistency) and requires source access, which limits transfer to closed-source systems. The authors acknowledge this in §8 (Discussion and Limitations), but it bounds the applicability.

**2. Novelty** — Adequate
- **2.1** The paper clearly distinguishes its setting from prior REST-API oracle work. AGORA+, SATORI, and MASTOR extract from structured sources (OpenAPI, traces, source) where constraints are explicit, whereas TestVDB extracts from natural-language documentation where interpretation is required. This is a non-obvious delta: prior work avoids LLM semantic judgment precisely because of reliability concerns, while TestVDB enters that regime and introduces a counter (source-grounded falsification).
- **2.2** The separation of LLM reliability into two layers (family-specific vs task-intrinsic) is a real conceptual contribution. Family-specific bias (self-preference) is known in LLM-as-judge literature, but task-intrinsic stability—where different model families converge on the same wrong claim due to shared ambiguous input—is a precise and useful distinction.
- **2.3 [minor, unfixable]** The novelty is incremental in that documentation-derived oracles have precedents (Toradocu, Doc2OracLL, AugmenTest). What is new is the source-grounded falsification mechanism, which targets a failure mode (stable misinterpretation) that prior documentation-oracle work does not explicitly address. The positioning against this prior work is clear in §7 (Related Work), but the delta is evolutionary rather than revolutionary.

**3. Soundness** — Adequate
- **3.1** The core claim—that source-grounded falsification resolves task-intrinsic documentation-interpretation errors—is supported by a controlled probe on twelve over-strict clauses. DeepSeek independently formalized 5 of the 12 as over-strict (the task-intrinsic subset), cross-model judging missed 2 of these 5, and source-grounded falsification caught all 12. The probe design is sound: it isolates the variable (cross-model vs source) on the same clauses — see RQ3, Table 3.
- **3.2** The yield results (111 submissions, 38 acknowledged) are presented with appropriate caution. The paper reports "about 85%" of submitted issues (and 89% of the 38 acknowledged), explicitly framed as the composition of its findings rather than a prevalence estimate; it does not give an exact numerator/denominator for the 85%. The authors do not claim recall because no ground-truth defect catalog exists — see RQ1.
- **3.3 [minor, unfixable]** The RQ3 probe has a small sample size (n=12 over-strict clauses, extended to n=29 with behavior and explicit-bound subtypes). The task-intrinsic rate of 5/12 (Wilson 95% CI [19%, 68%]) has wide intervals. The authors explicitly treat this as a pilot pending a larger study, which is appropriate given the uncertainty, but it limits the strength of the task-intrinsic claim.
- **3.4 [major, fixable]** The version/issue relationships in the VDBFuzz head-to-head comparison could be more explicit. The discussion mentions v1.4.0, v1.18.0, v1.18.2, #9045, #7967, and a "May 2026 fix," but the mapping between versions and issue states is not immediately clear for a reader without external context. A timeline figure or a table clarifying which issues are live in which versions would strengthen verifiability — see RQ1 (§6) and §8 (Discussion).
- **3.5** The "n=1 per direction" framing is careful. The authors state explicitly that the bidirectional reachability probe treats the cases as hypothesis-generating controlled cases rather than a generalized result, and the structural hypothesis (documentation-implementation oracles can reach crash defects when input violates a documented bound, but crash oracles under current templates do not reach silent accepts) is framed as a hypothesis, not an established fact. This bounding is appropriate for the evidence level — see RQ1 (§6) and §8 (Discussion).

**4. Verifiability** — Adequate
- **4.1** The paper gives enough detail to follow the overall pipeline flow. The five stages (LLM extraction, attack generation, LLM judgment, dev-reviewer falsification, novelty gate) are clearly described in §4. The falsification rule is concrete: for a clause asserting "parameter ≥ 1," the dev-reviewer examines source and falsifies if "parameter = 0" selects a default — see §4.
- **4.2** Key evaluation details are present: the LLM backbone (GLM-5.2 via bigmodel API), the runtime (Claude Code), the Docker-pinned target versions, the approximate cost ($10 per target), and the order of magnitude of LLM calls ($10^4$). The authors state that full prompts and per-token accounting are in the artifact — see §5.
- **4.3 [major, fixable]** The version/issue mapping in the VDBFuzz head-to-head comparison is insufficient for a reader to fully reconstruct the experimental setup without external context. The text mentions:
  - v1.4.0 reproduces an integer-overflow crash
  - v1.18.0 predates the "May 2026 fix" that resolves #9045
  - v1.18.2 is the version TestVDB targeted, where both crashes are fixed
  - #9045 is an empty-vector defect (acknowledged)
  - #7967 is a production panic root-caused by #9045

  The relationships between these versions, issues, and fixes are implicit. A table clarifying "Issue #9045: live in v1.18.0, fixed in May 2026; Issue #7967: recurred from v1.16.3 through v1.18.0, resolved by the same fix" would make the mapping explicit — see RQ1 (§6) and §8 (Discussion).
- **4.4** The scope tagging of quantitative claims is mostly clear but occasionally inconsistent. The paper reports "about 85%" of submitted issues (and 89% of the 38 acknowledged), explicitly framed as the composition of its findings rather than a prevalence estimate; it does not give an exact numerator/denominator for the 85%. However, the abstract and introduction use "about 85%" and "roughly 10%" where exact counts would be clearer. Consistent use of exact counts with confidence intervals would improve precision — see Abstract, RQ1.

**5. Presentation** — Adequate
- **5.1** The structure is sound and logical: problem framing (§2), LLM regime analysis (§3), method design (§4), implementation (§5), evaluation (§6), related work (§7), discussion and limitations (§8), conclusion (§9). The abstract matches the contributions listed in the introduction.
- **5.2** Table 1 (oracle exclusion) is internally consistent with the prose. Each row correctly maps an oracle type to the defect class it reaches and explains why it misses the documentation-implementation residual. The framing of LLM-derived oracle as the residual is clear.
- **5.3 [minor, fixable]** Table 3 (tab:e2) presents the cross-model vs source comparison clearly, but the "TI" marking could be more explicit in the caption or a footnote about what TI denotes (task-intrinsic) for readers who missed the definition in §3 — see Table 3.
- **5.4** The language is generally clear, with minor awkwardness. Some sentences are dense and could be split for readability. For example, the first sentence of the abstract packs the problem definition, defect class, and stakes into one clause; splitting this would improve accessibility — see Abstract.
- **5.5 [minor, fixable]** The notation is consistent but occasionally sparse. The "85%" residual is introduced without an explicit denominator in the abstract (it appears later in RQ1). Stating the base inline when "about 85%" first appears (e.g., "about 85% of the 111 submitted issues") would reduce ambiguity — see Abstract.

### Questions for Authors
- **Q1:** Could you make the version/issue mapping in the VDBFuzz head-to-head comparison explicit in a table or timeline? This would clarify the relationships between v1.4.0, v1.18.0, v1.18.2, #9045, #7967, and the "May 2026 fix" for readers without external context — intended effect: item 4.3's rating would move from Adequate to Excellent.
- **Q2:** The RQ3 probe treats 12 over-strict clauses as a pilot. Do you have plans or preliminary results for a larger head-to-head study (e.g., n=30)? If so, how would the TI rate estimate change — intended effect: clarify whether item 3.3's "pilot" status is a temporary limitation or a methodological boundary.
- **Q3:** You state that the "about 85%" residual is the composition of findings, not a prevalence estimate. Could you explicitly frame the "about 10%" classical-addressable and "about 5%" concurrency portions in the same way to avoid reader misinterpretation — intended effect: item 4.4's scope tagging consistency would improve.

---

## Meta-Review

### Criterion Consensus

| Criterion | Reviewer 1 | Reviewer 2 | Reviewer 3 | Meta-Review |
|---|---|---|---|---|
| Significance | Adequate | Adequate | Adequate | **Adequate** |
| Novelty | Excellent | Adequate | Adequate | **Adequate** |
| Soundness | Excellent | Adequate | Adequate | **Adequate** |
| Verifiability | Excellent | Adequate | Adequate | **Adequate** |
| Presentation | Excellent | Adequate | Adequate | **Adequate** |
| **Recommendation** | **Accept** | **Weak Accept** | **Weak Accept** | **ACCEPT** |

### Meta Recommendation
**ACCEPT**

All three reviewers leaned in (Accept, Weak Accept, Weak Accept — every recommendation at Weak Accept or better), which is the unanimous-shortcut ACCEPT; the consensus-tier count agrees, since there is no consensus Poor and no consensus substance Weak (every substance criterion sits at Adequate or Excellent). The verdict is stronger than Round 1: Reviewer 1, who verified VDBFuzz, AGORA+, SATORI, and MASTOR against their full-text PDFs, confirmed all four competitor characterizations are accurate and found the n=1 head-to-head honestly framed as hypothesis-generating — upgrading Novelty, Soundness, Verifiability, and Presentation to Excellent. Reviewers 2 and 3 held those four at Adequate, their reservation resting on two recurring points: the RQ3 task-intrinsic probe sample (n=29; TI rate 9/16, Wilson [33%, 77%]) that underpins the central conceptual contribution, and the version/issue exposition of the VDBFuzz comparison. Both reservations are revision-addressable (explicit pilot scoping; a version/issue timeline), and neither threatens a substance tier — the consensus substance tier is Adequate across the board. The two `[major, fixable]` items (source the wait=true default; add a version/issue timeline) are the must-fix revisions; the `[minor, unfixable]` items (pilot sample size; breadth-only generalization beyond Milvus/Qdrant) bound how far the claims can be pushed and explain why R2/R3 stayed at Adequate rather than following R1 to Excellent.

### Priority Revisions
1. **Source the VDBFuzz `wait=true` default claim** (R2 2.4 [major, fixable]; R1 3.2 [minor, fixable]). Cite VDBFuzz's paper/code/template confirming `wait=true` is the default; if it is not, the "template-coverage limitation, not a fundamental oracle property" framing weakens. This is the fairness hinge of the head-to-head — R1 read the VDBFuzz PDF and found the claim plausible but unsourced.
2. **Add an explicit version/issue timeline (or small table) for the VDBFuzz head-to-head** (R3 3.4 & 4.3 [major, fixable]; R2 4.5 [minor, fixable]). Map v1.4.0 / v1.18.0 / v1.18.2 ↔ #9045 / #7967 / May-2026 fix so a reader without external context can verify the bidirectional reachability — the single most repeated verifiability ask across all three reviewers.
3. **Make the RQ3 task-intrinsic pilot scoping unmistakable** (R2 3.2 [major, fixable]; R1 4.2/W2; R3 3.3 [minor, unfixable]). n=29 (9/16 TI) underpins the central conceptual contribution, yet the title/abstract give the task-intrinsic layer high weight; either expand the probe or carry an explicit "pilot" qualifier through title/abstract/intro. This is the main reviewer divergence — R1 rated Soundness Excellent finding the pilot honest, while R2/R3 rated Adequate wanting stronger evidence — so the fix is to make the pilot framing visible enough that R2/R3 read it as R1 did.
4. **Clarify the κ=1.0 cross-model candidate selection** (R2 3.3; R1 4.2). State whether the 20 candidates were random / diversity-stratified / purposive, so perfect agreement is not read as cherry-picked.
5. **Minor framing/presentation nits**: tag the "about 85%" base inline at first appearance (R3 5.5/W3); harmonize the ablation datasets so the single-LLM 25.5% is comparable on the same 12-FP/4-TP control (R2 3.4); standardize `n=29` vs `$n{=}29$` notation (R2 5.3); position Toradocu/Doc2OracLL against the two-layer model earlier (R2 2.5); reword "soft result correctness" and align `%` spacing (R1 5.3).

The `[major, unfixable]` ceiling — why this is ACCEPT rather than a stronger consensus — is that the RQ3 task-intrinsic sample (n=29) and the breadth-only Weaviate/MeiliSearch/Chroma generalization inhere in the current data; all three reviewers flagged these as the reason the substance criteria sit at Adequate for R2/R3. They bound the claims but do not undermine the verdict.

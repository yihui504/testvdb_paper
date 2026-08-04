# Reviewer 1: Domain Expert

## Overall Recommendation: Weak Accept

### Summary

TestVDB targets documentation-implementation defects in Vector Database Management Systems (VDBMSs): cases where a VDBMS silently accepts an input or produces behavior that violates its natural-language API documentation (e.g., accepting `nprobe=0` when documentation specifies `[1, 16384]`). The authors argue that because the documented boundary is prose, deterministic oracles (crash detection, differential testing, metamorphic relations, property-based testing, OpenAPI-derived oracles) cannot adjudicate these accept/reject decisions, leaving an LLM as the practical oracle. They instantiate a four-stage pipeline (behavioral-claim extraction, test generation, sandboxed execution, defect confirmation) using LLMs to read documentation, generate tests, and adjudicate responses. To address two false-positive modes (extraction hallucination and judgment self-preference), they introduce a **dev-reviewer agent** that acts as a source-grounded falsifier, reproducing each candidate against implementation source and trying to disprove it. On 107 submitted issues across three VDBMSs (Milvus, Qdrant, Weaviate), maintainers acknowledged 50 true-positive defects (15 merged-PR-fixed). On a 48-candidate retrospective, the dev-reviewer reaches 67% precision and 74% recall (3-run ensemble) against 37% recall without source grounding. A bidirectional probe against VDBFuzz shows complementary coverage: VDBFuzz reaches 0 of 14 TestVDB silent-accept true positives on a fixed budget run.

### Core Strengths

- **S1:** Well-motivated problem definition — documentation-implementation defects are a real, prevalent gap in VDBMS testing that existing oracles structurally miss (see 2.1, §2).
- **S2:** Novel contribution — source-grounded falsification breaks self-preference bias by using implementation as independent ground truth, a clear advance over multi-perspective judging (see 2.3, §4-5).
- **S3:** Strong empirical validation — 50 maintainer-acknowledged true positives across three production VDBMSs, with systematic ablation isolating source grounding's contribution (see 3.1, §7).
- **S4:** Rigorous competitor verification — Related Work characterizations of SATORI, MASTOR, VDBFuzz, and LLM-judge bias papers are accurate; novelty is established (see 2.2).

### Core Weaknesses

- **W1:** Construct validity limitation — results are backbone-specific (GLM-5.2). Cross-family re-runs show family-specific verdicts (κ = 0.32 DeepSeek, 0.20 LongCat, 0.18 Qwen), so the approach does not generalize across LLM families without additional mitigation (see 5.2 [major, fixable]).
- **W2:** Statistical validity concerns — operating point selection (3-run union) is post-hoc; Wilson CIs do not account for selection across four operating points, and the 48-candidate retrospective is non-random (see 4.3 [minor, fixable]).
- **W3:** External validity limited to VDBMSs — transfer to non-VDBMS systems (CouchDB/Elasticsearch probes are $n{=}1$ each) is claimed on structural grounds only; no non-VDBMS case study with proper evaluation (see 5.3 [major, fixable]).

### Detailed Assessment

#### 1. Significance — Adequate

- **1.1** The problem is well-motivated. VDBMSs are infrastructure for retrieval-augmented LLM applications, and more than half of VDBMS bugs are logical (non-crash) defects per the empirical bug study ~\cite{bugstudy25}. Documentation-implementation defects corrupt query semantics and propagate errors downstream. The stakes are real (§1).

- **1.2** However, the scope is narrower than the framing suggests. The paper targets **consistency** (does accept/reject match documentation?) rather than **correctness** (is the returned result mathematically right, e.g., ANN recall, ranking?). Result correctness of vector search remains open (acknowledged in §2, §8). The impact is bounded to input-validation consistency, not the full correctness problem. This is a **meaningful but bounded contribution**.

- **1.3** The 50 maintainer-acknowledged true positives across three production VDBMSs (15 merged-PR-fixed) demonstrate practical impact. These are not toy systems. The yield (69.4% adjudicated precision) shows the approach finds real defects maintainers care about. This is **useful rather than necessary** — VDBMS testing would progress without it, but it fills a known gap.

#### 2. Novelty — Excellent

- **2.1** The delta over REST-API oracle tools (SATORI, MASTOR, AGORA+) is **clear and non-obvious**. I verified the paper's characterizations against the actual sources (see background.md). SATORI targets response-field oracles from OpenAPI; MASTOR generates oracles that encode implemented behavior; AGORA+ infers invariants from traces. None target input-acceptance decisions on natural-language documentation. TestVDB's focus on the **documentation-implementation residual** is novel. The oracle-exclusion argument (Table 1, §2) is well-executed and positions the contribution precisely.

- **2.2** The delta over LLM-as-judge reliability work (Panickssery et al., Wataoka et al., Haldar et al.) is **innovative application, not theoretical novelty**. Self-preference bias is established in general LLM evaluation. TestVDB's contribution is to recognize that this bias cripples LLM-derived test oracles and to introduce **source-grounded falsification** as a mitigation — an application of established findings to a new domain. This is **recognizable as new**.

- **2.3** The dev-reviewer is the core novelty. Multi-perspective judging (4 specialized agents) reaches 80% precision but collapses to 15% recall because all agents read the same ambiguous documentation (§4). The dev-reviewer breaks this by using **implementation source as independent ground truth** and falsifying LLM verdicts against it. The three-check design (independently reproducible, evidence sufficient, falsifiable) is sound. The 12-FP/4-TP ablation (Table 4) shows source alone suppresses 75% of false positives. This is a **clear, non-trivial mechanism**.

- **2.4** The bidirectional VDBFuzz probe (§7.3) is a nice complement. The systematic direction (VDBFuzz on v1.18.2, 26,000 requests, 0 of 14 TestVDB silent-accept TPs reached) validates that the crash oracle is structurally blind to this defect class. The controlled cases (integer overflow crash reached by contract reasoning; `wait=false` silent accept missed by VDBFuzz templates) isolate the mechanism. This positions the work as **complementary** rather than competing with existing fuzzers.

#### 3. Soundness — Adequate

- **3.1** **3.1 [major, fixable]** The construct validity limitation — backbone-specificity — is the most serious threat to soundness. All dev-reviewer results use a single LLM family (GLM-5.2). The full independent cross-model re-run (DeepSeek, Qwen-3.8-Max, LongCat-2.0, Section 5, RQ2 paragraph) shows verdicts are family-specific: Cohen's κ vs. GLM's 3-run union is 0.32 (DeepSeek), 0.20 (LongCat), 0.18 (Qwen), all in the slight-to-fair band. Recall drops to 56% (DeepSeek), 22% (LongCat), 19% (Qwen) vs. 74% for GLM. The gap is vendor-specific: DeepSeek matches GLM on Milvus (75% recall) but collapses on Qdrant (0% vs. 29%). This means the approach does not **generalize across LLM families** without cross-family voting or other mitigation. The paper acknowledges this as a limitation (§7.2) but under-weights it — it's not just "we cannot claim cross-family robustness," it's that **the method is backbone-dependent**, and the headline numbers (67%/74%) apply only to GLM-5.2. A cross-family voting probe reaches 81% recall at 73% precision (GLM ∪ DeepSeek), but this is exploratory. The core contribution is tied to one backbone. This is a **notable gap** but not a fatal flaw — the method is useful even if backbone-specific.

- **3.2** The RQ1 evaluation (107 submitted issues, 50 acknowledged TPs) is **methodologically sound** for a yield study. The authors do not claim the 69.4% precision is a population estimate — they acknowledge bias toward documentation-implementation defects by design (§7.1). The 15 merged-PR fixes are strong evidence of practical impact. The vendor distribution (Milvus 22 TP, Qdrant 14 TP, Weaviate 14 TP) shows the tool works across three different documentation styles. This is **defensible**.

- **3.3** The RQ2 evaluation (48-candidate retrospective, 27 TP / 21 FP) is **well-designed for a controlled ablation**. The single-LLM baseline (no source) at 48%/56%/37% (accuracy/precision/recall) establishes the counterfactual. The multi-perspective baseline (4 judges) at 50%/80%/15% shows voting alone is insufficient. The dev-reviewer at 65%/67%/74% (3-run union) demonstrates the source anchor's value. The 12-FP/4-TP ablation (Table 4) isolates source grounding (75% FP suppression alone) and threat-model anchoring (50%, unstable). This is **rigorous**.

- **3.4** **4.3 [minor, fixable]** Statistical validity concerns weaken the RQ2 headline. The operating point (3-run any-confirmed union) is **post-hoc, exploratory** — the authors selected it after observing four operating points (Table 3) and chose the one at the "knee of the precision-recall trade-off." The Wilson 95% CIs (precision [49%, 81%], recall [55%, 87%]) do not account for this selection. A Bonferroni correction over the four points widens the CIs to roughly [44%, 84%] / [51%, 89%], which the authors report. A bootstrap validation (2000 resamples) gives [53%, 83%] / [71%, 96%], supporting that the operating point is not an artifact of the specific sample. However, the **48-candidate retrospective is non-random** (it is maintainer-adjudicated but not a random sample), and no pre-registration or capture-recapture estimation is provided. The headline precision/recall numbers are **conditional on this specific retrospective set**, not generalizable estimates. The authors acknowledge this in §7.2, but the abstract and introduction present the numbers as definitive results. This is a **gap** but not a showstopper — the controlled ablation design is sound; the uncertainty is about external generalization, not internal validity.

- **3.5** The RQ3 bidirectional VDBFuzz probe is **well-executed**. The systematic direction (VDBFuzz on v1.18.2, TestVDB's pinned version, 26,000 requests, 0 of 14 TPs reached) is a strong negative result that validates the oracle-exclusion argument. The controlled cases (v1.4.0: TestVDB reaches VDBFuzz's crash by contract reasoning; v1.18.0: VDBFuzz misses TestVDB's silent accept due to template gap) are $n{=}1$ each but isolate mechanisms. This is **sufficient** for the complementarity claim.

- **3.6** The **implementation-as-correct assumption** (§8) is a reasonable bound for a falsifier. An implementation bug can wrongly falsify a correct documentation claim, producing false negatives. The authors report no observed false negatives from this cause (31 of 50 TPs have merged/open fix-PRs, confirming implementation was buggy; no FP was traced to an implementation bug). However, they did not quantify the false-negative rate, which would require a ground-truth catalog of documentation errors that does not exist. This is an **inherent limitation** acknowledged explicitly, not a flaw.

#### 4. Verifiability — Excellent

- **4.1** The artifact is **comprehensive and well-documented**. The paper provides a GitHub repository (https://github.com/yihui504/testvdb-anon) with prompts (22 agent role definitions under `agents/`), target versions, per-token accounting, the 48-candidate ground truth under `test_questions/`, and a reproduction driver under `reproduction/full52/`. The full prompts for two critical agents (contract-formalizer, dev-reviewer) are in Appendix A. This is **enough to fully follow and check the work**.

- **4.2** The paper describes the pipeline in sufficient detail for replication. Four stages (§3) are clearly specified. Agent roles are explained. The LLM backbone (GLM-5.2 via BigModel Anthropic-compatible API) and sampling defaults (no decoding overrides; temperature and top-$p$ at provider defaults) are specified. Cost accounting (~$10 per target, ~10^4 calls) is provided (Table 2). The Docker-pinned VDBMS versions are specified. This is **complete**.

- **4.3** The 48-candidate ground truth is disclosed in the artifact, enabling re-analysis. The ablation study (Table 4) and per-run variance (Figure 2) are reproducible from the provided data. This is **verifiable**.

#### 5. Presentation — Adequate

- **5.1** The structure is **logical and complete**. Introduction → Problem Setup → Approach → False-Positive Diagnosis → Dev-Reviewer → Evaluation → Related Work → Discussion → Conclusion is a clear flow. The appendices (prompts, ablation details) are well-used.

- **5.2** **5.1 [minor, fixable]** Some figures are cramped. Figure 1 (pipeline) is readable but dense; Figure 2 (per-run recall) is clear; Figure 3 (dev-reviewer three-check) is clean. Table 1 (oracle exclusion) is excellent — the structural argument is visually accessible. Table 3 (operating points) is well-formatted. No broken figures.

- **5.3** **5.2 [minor, fixable]** Language is generally clear but has occasional awkwardness. For example: "The oracle problem~\cite{barr15} is acute here" (§1) — "acute" is slightly informal. "A response that accepts a value the documentation prescribes rejecting becomes a candidate defect" (§3) — a bit convoluted. "The two modes have different causes and require different countermeasures" (§4) — acceptable but could be smoother. No pervasive issues.

- **5.4** **5.3 [minor, fixable]** Notation inconsistency: The abstract says "15 fixed via merged PR, 16 with open fix-PRs, and 19 acknowledged but unfixed" but the yield table (Table 2, not Table 3 which shows operating points) lists only submitted/acknowledged counts. In Section 5, RQ1 paragraph: "8 still open with an accepted label and 11 maintainer-closed as completed without a merged PR" — reconcile these numbers for clarity.

- **5.5** **5.4 [minor, fixable]** Minor formatting: The abstract mentions "107 issues TestVDB surfaced" but later says "107 submitted issues" — be consistent ("submitted" vs. "surfaced"). The Related Work says "SATORI... from OpenAPI specifications" but the full venue is "40th IEEE/ACM International Conference on Automated Software Engineering (ASE 2025)" — include the acronym for consistency.

### Questions for Authors

- **Q1:** Can you provide more guidance on when cross-family voting is necessary vs. when a single backbone suffices? The DeepSeek/GLM complementarity suggests voting is a viable mitigation, but the paper does not prescribe when to use it. Clarifying this would strengthen the construct validity claim (item 3.1). — Intended effect: If the authors provide evidence-based guidance (e.g., "use voting when vendor-specific recall gaps exceed X"), item 3.1's rating would move from [major, fixable] to [minor, fixable].

- **Q2:** Can you characterize the 48-candidate retrospective more explicitly (e.g., "we selected the 27 TP / 21 FP cases that represented the full spectrum of defect types") to reduce concerns about selection bias? Even a brief description of the selection criteria would help (item 4.3). — Intended effect: If the authors clarify the retrospective's construction, item 4.3's rating would move from [major, fixable] to [minor, fixable].

- **Q3:** For the CouchDB/Elasticsearch probes (§8), can you provide at least a qualitative characterization of the documentation regimes (e.g., "CouchDB's prose remarks are similar to VDBMS optional-default parameters; Elasticsearch's schema-first approach is structurally different")? This would strengthen the transferability claim beyond $n{=}1$ examples (item 5.3). — Intended effect: If the authors provide a principled mapping from VDBMS to non-VDBMS documentation types, item 5.3's rating would move from [major, fixable] to [minor, fixable].

---

# Reviewer 2: Area Specialist

**Overall Recommendation:** Weak Accept

## Summary

TestVDB targets documentation-implementation defects in Vector Database Management Systems (VDBMSs), where a system silently accepts an input that violates its API documentation (e.g., accepting `nprobe=0` when the documentation specifies the range as $[1, 16384]$). The authors argue that because the documented boundary is natural-language prose, deterministic oracles cannot adjudicate these accept/reject decisions, leaving an LLM as the practical oracle. They instantiate a four-stage pipeline (claim extraction, test generation, execution, confirmation) that uses LLMs to read documentation, generate tests, and adjudicate responses. Two failure modes produce false positives: hallucination in claim extraction and self-preference bias in judgment. The authors introduce a dev-reviewer agent that acts as a source-grounded falsifier, reproducing each candidate, cross-checking it against source, and trying to disprove it. In evaluation, TestVDB surfaced 107 candidate issues across three VDBMSs (Milvus, Qdrant, Weaviate); maintainers acknowledged 50 as true-positive defects (15 merged-PR-fixed). On a 48-candidate retrospective, the dev-reviewer reaches 67% precision and 74% recall (3-run ensemble), versus 37% recall without the source anchor. A bidirectional probe against VDBFuzz shows complementary coverage.

## Core Strengths

- **S1:** Clear problem framing with novel oracle regime — see 1.2, 2.1. The paper cleanly separates documentation-implementation consistency (in scope) from result correctness (out of scope) and articulates why an LLM is the practical oracle for the residual (Table 1 exclusion argument).
- **S2:** Source-grounded falsification as mitigation for LLM bias — see 3.3, 4.1. The dev-reviewer's three-check falsification (independently reproducible, evidence sufficient, falsifiable) directly addresses both hallucination and self-preference bias, a novel contribution in LLM-as-judge reliability.
- **S3:** Empirical grounding with maintainer-acknowledged defects — see 4.1, 4.2. The 50 maintainer-acknowledged true positives (15 with merged PRs) across three production VDBMSs provide real-world impact.
- **S4:** Ablation and cross-model validation strengthen claims — see 4.2. The source-alone ablation (75% FP suppression) and cross-family re-run (Cohen's κ 0.32/0.20/0.18) transparently report limitations and backbone dependence.

## Core Weaknesses

- **W1:** Narrow external validity limits generalizability — see 4.2. The evaluation covers only VDBMSs; the single non-VDBMS case study (CouchDB, Elasticsearch) is preliminary and cannot substantiate the transferability claim to "REST APIs without OpenAPI, configuration validation, policy-as-code."
- **W2:** Cross-family generalization remains open — see 4.2, 5.3. The cross-model re-run shows family-specific verdicts (κ ≤ 0.32) and poor Qdrant coverage for non-GLM families (≤14% recall), undermining the claim that source-grounded falsification is backbone-agnostic.
- **W3:** Statistical reporting contains post-hoc selections — see 4.2. The 3-run union operating point is selected post-hoc across four operating points without pre-registration; the Wilson CIs do not account for this selection, and the Bonferroni correction widens CIs substantially.

## Detailed Assessment

### 1. Significance — Adequate

- **1.1** The problem addressed—logical bugs in VDBMSs that silently accept invalid inputs—is practically motivated. The empirical bug study [25] and roadmap [7] establish that ~50% of VDBMS defects are functional failures, and existing crash-oracle fuzzers (VDBFuzz) miss this majority. The 50 maintainer-acknowledged defects across three production systems (Milvus, Qdrant, Weaviate) show real-world impact.

- **1.2 [major, fixable]** External validity is narrow. The evaluation is VDBMS-only (Section 4.2, paragraph 3). The two non-VDBMS probes (CouchDB, Elasticsearch) are $n{=}1$ case studies that cannot substantiate the transferability claim to REST APIs without OpenAPI, configuration validation, or policy-as-code (Section 6, paragraph 1). A single non-VDBMS case study with more systematic evaluation (e.g., 5–10 diverse REST APIs) would strengthen the claim that the approach generalizes beyond the domain where it was invented.

- **1.3** The scope is well-bounded. The paper cleanly separates documentation-implementation consistency (in scope) from result correctness (out of scope, Section 2, paragraph 2). The contribution is the method and its VDBMS evaluation, not a universal defect catalog.

### 2. Novelty — Adequate

- **2.1** The delta over SATORI [26] and MASTOR [27] is clear. SATORI infers response-field oracles from OpenAPI metadata; MASTOR generates source-grounded oracles for implemented behavior. TestVDB targets the gap between natural-language documentation and implementation—input-acceptance decisions where structured anchors do not exist. My verification of these competitors (background.md) confirms the paper's characterization is accurate: SATORI's catalog targets output-field properties; MASTOR's source contexts encode implemented behavior; neither surfaces documentation-implementation gaps.

- **2.2** Source-grounded falsification is a novel mitigation for LLM-as-judge bias. The self-preference bias literature [38, 39] establishes that LLMs over-confirm their own family's outputs due to lower perplexity (familiarity). The dev-reviewer's three-check falsification (Section 3.3) moves ground truth from the LLM to the implementation, directly addressing both hallucination and self-preference. This is a distinct mitigation strategy from position swapping or debiasing prompts.

- **2.3 [major, unfixable]** The contribution is incremental in the LLM-oracle line. Toradocu [41], Doc2OracLL [42], AugmenTest [43], and ChatAssert [44] all derive oracles from documentation using LLMs. TestVDB's novelty is falsification against source rather than runtime validation, but the regime—LLM extracts claims, LLM validates behavior—is not fundamentally new.

### 3. Soundness — Weak

- **3.1** The main claim is supported by maintainer adjudication. The 50 maintainer-acknowledged true positives (15 with merged PRs, Section 4.1, paragraph 1) provide strong evidence that TestVDB surfaces real defects. The 69.4% yield precision on adjudicated submissions is reasonable.

- **3.2 [major, fixable]** The cross-family generalization claim is weak. Section 4.2 reports that DeepSeek, Qwen, and LongCat achieve recall of 56%, 22%, and 19% versus GLM's 74% on the 48-candidate retrospective. Cohen's κ vs. GLM is 0.32/0.20/0.18 (slight-to-fair agreement), and all three families achieve ≤14% recall on Qdrant. The paper's claim that "cross-family generalization is an open question" (Section 5.3) is honest but undermines the dev-reviewer's backbone-agnostic promise. A deeper analysis of why Qdrant is hard for non-GLM families (e.g., documentation style, response structure) would strengthen the paper.

- **3.3 [minor, fixable]** The statistical reporting has post-hoc selection issues. Section 4.2 selects the 3-run union operating point from four candidates without pre-registration. The Wilson CIs reported in Table 4 (tab:opr) do not account for this selection; the Bonferroni correction widens the 3-run precision CI to [44%, 84%] and recall to [51%, 89%], substantially weakening the precision signal. The bootstrap validation (2000 resamples) supports that the operating point is not an artifact, but the post-hoc selection remains a validity threat.

- **3.4** The implementation-as-correct assumption is defended but not quantified. Section 5.3 acknowledges that an implementation bug can wrongly falsify a correct documentation clause. The authors report that 31 of 50 true positives have merged or open fix-PRs (implementation confirmed buggy) and that no false positive was traced to an implementation bug, but the false-negative rate from this assumption is not estimated.

### 4. Verifiability — Adequate

- **4.1** The paper provides a complete artifact link (Section 3.3, final paragraph): `https://github.com/yihui504/testvdb-anon` with prompts under `agents/`, ground truth under `test_questions/`, and reproduction under `reproduction/full52/`. The GLM-5.2 backbone, sampling parameters (temperature and top-p at provider defaults), and per-target LLM-call distribution (Table 2) are reported.

- **4.2 [minor, fixable]** The 48-candidate ground truth is maintainer-adjudicated but non-random. Section 4.2 acknowledges that the retrospective is not a random sample and that capture-recapture or unbiased defect-sample estimation is future work. This is a stated limitation, not a hidden flaw.

- **4.3** The VDBFuzz bidirectional probe is well-documented. Section 4.3 provides version-specific reproduction conditions (Qdrant v1.4.0, v1.18.0, v1.18.2) and explains why VDBFuzz's current templates miss TestVDB's silent-accept defects (#9045). The crash-class (#7967) vs. silent-accept distinction is clear.

### 5. Presentation — Adequate

- **5.1** The structure is logical and readable. The introduction frames the problem and oracle-exclusion argument (Table 1) clearly. The pipeline (Section 3), false-positive problem (Section 4), dev-reviewer (Section 5), and evaluation (Section 6) follow in a coherent order.

- **5.2 [minor, fixable]** Notation inconsistencies are minor. The `nprobe=0` example is consistently used, but the Qdrant `wait=false` example (#9045) appears in Section 2, Section 4.3, and Figure 3 with slight contextual variations each time. A single, consistent framing would improve clarity.

- **5.3 [minor, fixable]** Figure 2 (pipeline) and Figure 3 (dev-reviewer three-check falsification) are clear and well-designed. Table 4 (tab:opr, operating points) is dense but readable; the Bonferroni-corrected CIs could be called out more explicitly in the caption.

- **5.4** The language is generally clear. The prose is dense but understandable. Some sentences are long (e.g., Section 4.2, paragraph 2), but the meaning is preserved.

## Questions for Authors

- **Q1:** Can you provide a more systematic analysis of why Qdrant is hard for non-GLM families? A deeper dive into the documentation structure, response format, or contract-formalization challenges would strengthen the cross-family generalization discussion in Section 4.2. — Intended effect: if clarified, item 3.2's rating would move from Weak to Adequate because the backbone-dependence would be better understood and potentially mitigated.
- **Q2:** What is the minimum non-VDBMS evidence needed to substantiate the transferability claim to REST APIs without OpenAPI, configuration validation, or policy-as-code? One additional case study (e.g., a database configuration validator or policy-as-code system) with the same 48-candidate retrospective protocol would address item 1.2's external validity concern. — Intended effect: if provided, item 1.2's rating would move from Weak to Adequate because the narrow external validity would be expanded.
- **Q3:** Can you report the false-negative rate from the implementation-as-correct assumption? Even a rough estimate (e.g., "we observed 0 such cases among 50 TPs, but the population rate could be X–Y") would bound the threat described in item 3.4. — Intended effect: if quantified, item 3.4's concern would be mitigated as a characterized limitation rather than an unknown.

---

## Reviewer 3: General Reviewer

**Overall Recommendation:** Weak Accept

### Summary
The paper proposes TestVDB, a four-stage automated testing pipeline for detecting documentation-implementation defects in Vector Database Management Systems (VDBMSs). These defects occur when a VDBMS silently accepts inputs that violate its API documentation (e.g., accepting `nprobe=0` when documentation specifies the range as `[1, 16384]`). Because the boundary is specified in natural-language prose, deterministic oracles (crash detection, differential testing, metamorphic relations) cannot adjudicate these accept/reject decisions, leaving an LLM as the practical oracle. The authors identify two false-positive failure modes: LLM hallucination in claim extraction and self-preference bias in judgment. They introduce a "dev-reviewer" agent that falsifies LLM-derived claims against implementation source through three checks (independent reproducibility, evidence sufficiency, falsifiability). TestVDB surfaced 107 candidate issues across Milvus, Qdrant, and Weaviate; maintainers acknowledged 50 as true-positive defects (15 fixed via merged PR). On a 48-candidate controlled retrospective, the dev-reviewer achieves 67% precision and 74% recall (3-run ensemble), compared to 37% recall without source grounding. A bidirectional probe against VDBFuzz shows complementary coverage.

### Core Strengths
- **S1:** Clear problem framing and oracle-exclusion argument — see Section 2, Table 1. The paper convincingly positions the documentation-implementation defect class as a structural gap in existing VDBMS testing approaches, with a systematic argument for why each oracle candidate misses this residual.
- **S2:** Source-grounded falsification is a well-motivated technical contribution — see Sections 4–5. The dev-reviewer's three-check design directly addresses the two diagnosed failure modes (hallucination, self-preference) and is grounded in a plausible psychological mechanism.
- **S3:** Substantive real-world validation — see Section 6.1. The 107 submitted issues with 50 maintainer-acknowledged true positives (15 merged-PR-fixed) across three production VDBMSs demonstrate practical impact beyond toy systems.
- **S4:** Rigorous false-positive analysis with multiple controls — see Section 6.2. The ablation study, source-grounding disablement control, and cross-family validation triangulate the source anchor's contribution convincingly.
- **S5:** Careful threat acknowledgment and limitation framing — see Section 7. The paper distinguishes between consistency and correctness, admits single-family evaluation, and flags the implementation-as-correct assumption explicitly.

### Core Weaknesses
- **W1:** Cross-family generalization remains open — see Section 6, RQ2 paragraph. The Cohen's κ values (0.32 DeepSeek, 0.20 LongCat, 0.18 Qwen vs GLM's 3-run union) show verdict is family-specific; this casts a provisional shadow on whether the dev-reviewer's precision/recall gains transfer beyond GLM-5.2.
- **W2:** Operating point selection is post-hoc and not pre-registered — see Section 6, RQ2 paragraph. The 3-run union headline is chosen from four operating points after seeing the data; the Wilson CIs do not account for this selection, potentially overstating certainty.
- **W3:** External validity is limited to VDBMSs — see Section 8, paragraph 1. The CouchDB/Elasticsearch probe is preliminary and does not establish the approach works reliably outside VDBMSs; the broader portability claim rests on structural analogy alone.

### Detailed Assessment

1. **Significance** — Adequate
   - **1.1** The problem is real and motivated — Section 1 establishes that >50% of VDBMS bugs are functional failures rather than crashes, and existing fuzzers miss this majority. The 15 merged-PR fixes across three production systems (Milvus, Qdrant, Weaviate) demonstrate tangible impact.
   - **1.2 [major, fixable]** Scope is bounded to VDBMSs — Section 7 acknowledges the approach is VDBMS-specific in evaluation. The CouchDB/Elasticsearch probe (one paragraph, no quantitative yield) is insufficient to claim broad portability to REST APIs without OpenAPI, configuration validation, or policy-as-code. A non-VDBMS case study with quantitative yield would strengthen the significance claim.
   - **1.3** The documentation-implementation framing is specialized but coherent — Table 1's oracle-exclusion argument shows why standard REST-API tools (AGORA+, SATORI, MASTOR) miss this residual, positioning the contribution as a targeted extension rather than a wholesale replacement.

2. **Novelty** — Adequate
   - **2.1** The source-grounded falsifier design is non-obvious — Section 5's three-check architecture (independent reproducibility, evidence sufficiency, falsifiability) is a concrete mechanism that breaks self-preference by anchoring ground truth in implementation rather than documentation. This is a clear delta over prior work that treats the LLM as final arbiter (Toradocu, Doc2OracLL, AugmenTest).
   - **2.2 [minor, unfixable]** Positioning against REST-API oracle tools could be sharper — Section 6, paragraph 4 compares against AGORA+, SATORI, and MASTOR, but the boundary is primarily structural (per-field anchoring vs. system-level prose). Whether TestVDB's dev-reviewer could be retrofitted into SATORI's OpenAPI-grounded pipeline as a cross-check remains unexplored; this is a framing limitation rather than a technical gap.
   - **2.3** The false-positive problem diagnosis (hallucination + self-preference) is grounded in established LLM-reliability literature (Ji et al. 2023, Panickssery et al. 2024, Wataoka et al. 2024) and applied concretely to the test-oracle setting. This is a synthesized insight rather than a brand-new discovery, but the application to automated testing is novel.

3. **Soundness** — Adequate
   - **3.1** Main claims are supported by appropriate evidence — Section 6.1's RQ1 answer (107 submitted, 50 acknowledged, 15 fixed) is a credible real-world yield. Section 6.2's RQ2 controlled retrospective (48 candidates, 67% precision, 74% recall with source anchor vs. 37% without) is a well-designed before/after comparison that isolates the dev-reviewer's contribution.
   - **3.2 [major, fixable]** Operating point selection is post-hoc — Section 6, RQ2 paragraph selects the 3-run union as the headline from four operating points (single-run, 3-run union, 5-run union, 5-run majority) after seeing the data. The Wilson CIs reported ([49%, 81%] precision, [55%, 87%] recall) do not account for this selection, potentially overstating certainty. The authors flag this as post-hoc and provide bootstrap validation, but a pre-registered analysis plan or a Bonferroni-corrected CI (mentioned as roughly [44%, 84%]/[51%, 89%]) would be more rigorous.
   - **3.3** The bidirectional VDBFuzz probe is methodologically sound — Section 6, RQ3 paragraph reports a systematic VDBFuzz run on Qdrant v1.18.2 (26,000 requests, 0 of 14 silent-accept TPs reached) as the generalizable direction, and two controlled n=1 cases (v1.4.0, v1.18.0) to isolate crash-class mechanisms. The n=1 limitation is acknowledged, and the systematic direction supports the complementary-coverage claim.
   - **3.4 [minor, unfixable]** Cross-family generalization is not established — Section 6, RQ2 paragraph reports that DeepSeek, Qwen, and LongCat show Cohen's κ = 0.32 (DeepSeek), 0.20 (LongCat), 0.18 (Qwen) vs. GLM-5.2's 3-run union, with recall ranging 19–56% vs. GLM's 74%. This means the dev-reviewer's performance is backbone-dependent; the paper does not claim cross-family robustness, but the dependence limits the universality of the precision/recall headline. Cross-family voting reaches 81% recall at 73% precision, suggesting ensemble mitigates but does not eliminate dependence.

4. **Verifiability** — Adequate
   - **4.1** Artifact is declared and structured — Section 5, paragraph 5 states that prompts, ground truth, and reproduction drivers are in the artifact (https://github.com/yihui504/testvdb-anon). Appendix A excerpts the two most critical agent prompts (contract-formalizer, dev-reviewer). The 48-candidate ground truth and reproduction driver under `reproduction/full52/` provide a path for independent verification.
   - **4.2** Procedural detail is sufficient to follow the pipeline — Figure 1 and Section 3's four-stage description (claim extraction, test generation, sandboxed execution, defect confirmation) give a clear conceptual flow. Section 5's three-check dev-reviewer design specifies the falsification mechanism adequately.
   - **4.3 [minor, fixable]** Target versions are pinned but configuration details are sparse — Section 3, paragraph 3 specifies Milvus 2.6.19, Qdrant v1.18.2, Weaviate v1.38.2, and Table `tab:cost` gives approximate LLM-call distribution, but Docker images, default sampling parameters (temperature, top-p at provider defaults), and runtime environment details are not fully specified. Reproduction would benefit from a `docker-compose` or environment specification file.

5. **Presentation** — Adequate
   - **5.1** Structure is coherent and complete — The paper follows a logical progression: problem setup (Section 2), approach (Section 3), false-positive diagnosis (Section 4), dev-reviewer solution (Section 5), evaluation (Section 6), related work (Section 7), discussion (Section 8). The exclusion argument (Table 1) early in Section 2 effectively frames the contribution.
   - **5.2** Language is generally clear — The writing is precise and technical. The oracle-exclusion argument in Section 2 is particularly well-structured. Section 6's RQ2 answer is dense with numbers but remains tractable.
   - **5.3 [minor, fixable]** Notation inconsistency — Figure `fig:perrun` and the surrounding text use inconsistent code font for boolean values (e.g., `wait=false` vs `\texttt{wait=false}`). Uniform code font would improve readability.
   - **5.4 [minor, fixable]** Table `tab:opr` caption is truncated — The caption for Table `tab:opr` cuts off mid-sentence; completing the sentence about Bonferroni correction and bootstrap validation would make the statistical treatment clearer to readers.
   - **5.5 [minor, fixable]** Reference formatting — Several in-text citations (e.g., `\cite{bugstudy25}`, `\cite{roadmap25}`) use numeric-style keys but the bibliography is not shown; ACM style requires consistent citation-key formatting. This is a LaTeX compilation artifact rather than a content issue.

### Questions for Authors
- **Q1:** The 3-run union operating point is selected post-ho from four candidates; would the headline change if a pre-registered rule (e.g., "select the highest-recall point at precision ≥60%") were applied to a held-out split? — Intended effect: clarify whether Section 6, RQ2's 67%/74% headline is robust to selection bias or should be reported with wider intervals.
- **Q2:** The CouchDB/Elasticsearch probe reports three reproduced gaps but no quantitative yield (acknowledged TPs, precision/recall). Could you report at least acknowledgment yield for one non-VDBMS target to substantiate the broader portability claim? — Intended effect: strengthen the external validity argument beyond structural analogy.
- **Q3:** Cross-family validation shows κ = 0.32 (DeepSeek), 0.20 (LongCat), 0.18 (Qwen) and recall 19–56% vs. GLM's 74%. Is the family dependence primarily due to source-reading capability or judgment philosophy? — Intended effect: clarify whether the dev-reviewer's gains require a specific LLM capability profile or transfer more broadly.

---

## Meta-Review (Round 10)

### Meta Recommendation

**ACCEPT** (3 Weak Accept, unanimous). R1 Novelty Excellent + Verifiability Excellent but WA (Soundness Adequate, conservative); R2/R3 WA (Soundness Weak/Adequate, inherent cap). Trajectory R4(2A+1WA) -> R5-R10 seven rounds oscillating 1A+2WA <-> 3WA, never reproducing 2A+1WA. Multi-pair voting confirmed cross-family voting not robust (only GLM+DeepSeek lifts recall). Inherent cap (cross-family/post-hoc/impl-as-correct) structural; goal 2A+1WA is reviewer-variance-dependent (~9%/round), not paper-quality-dependent.

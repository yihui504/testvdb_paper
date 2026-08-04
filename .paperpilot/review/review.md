# Peer Review - TestVDB: Detecting API Compliance Defects in Vector Database Systems via Contract-Truth Separation

> Three independent reviewers (Domain Expert / Area Specialist / General Reviewer), each filled the same five-criteria template against the same rubric. Paper type: **technical**. Each draft passed an independent checker (verify-fix loop). Date: 2026-08-04.

---

## Reviewer 1: Domain Expert

**Overall Recommendation:** Weak Accept

### Summary
TestVDB targets documentation-implementation defects in Vector Database Management Systems (VDBMSs), where systems silently accept inputs that violate their API documentation. The paper argues that because documentation is natural-language prose, deterministic oracles cannot adjudicate these accept/reject decisions, leaving LLMs as the practical oracle. TestVDB instantiates a four-stage pipeline: behavioral-claim extraction (LLM reads documentation), test-script generation (boundary probes), sandboxed execution, and defect confirmation. The key contribution is a dev-reviewer agent that falsifies LLM-derived claims against implementation source, addressing two false-positive modes: hallucination in extraction and self-preference in judgment (where same-family LLMs over-confirm their own claims). On three VDBMSs (Milvus, Qdrant, Weaviate), TestVDB surfaced 107 candidate issues with 49 maintainer-acknowledged true-positive defects (15 merged-PR fixes). A controlled 48-candidate retrospective shows source-grounded falsification achieves 67% precision and 74% recall vs. 37% recall without source. A bidirectional probe against VDBFuzz demonstrates complementary coverage: VDBFuzz reached 0 of 14 silent-accept TPs on Qdrant v1.18.2 (structural limitation of crash oracles), while TestVDB reached VDBFuzz's integer-overflow crash via contract reasoning on v1.4.0.

### Core Strengths
- **S1:** Well-motivated problem and clear oracle-exclusion argument — see 1.2, 2.1
- **S2:** Source-grounded falsification is a genuine delta over prior work — see 2.1, 2.2, 2.3
- **S3:** Rigorous bidirectional comparison with VDBFuzz on Qdrant — see 3.3
- **S4:** Maintainer-acknowledged ground truth (49 TPs) provides real-world validation — see 4.1

### Core Weaknesses
- **W1:** Post-hoc operating point selection without pre-registration — see 3.2, Table 5
- **W2:** Limited external validity (single LLM family; non-random retrospective) — see 3.4, 3.5
- **W3:** Missing precision context from AugmenTest baseline — see 2.2

### Detailed Assessment

1. **Significance** — Adequate
   - **1.1** The problem is well-motivated and has real-world impact. Section 2 clearly establishes the defect class (silent-accept documentation violations) with concrete examples (Milvus #49823: nprobe=0 accepted despite documentation declaring range [1, 16384]). The empirical bug study (43% of VDBMS bugs from incorrect behavior) and testing roadmap citation provide domain context. The yield (49 acknowledged TPs, 15 merged-PR fixes across three production VDBMSs) demonstrates practical impact.
   - **1.2 [major, fixable]** The oracle-exclusion argument in Table 1 is conceptually sound but empirically under-substantiated. The table walks through deterministic oracle candidates (crash, differential testing, metamorphic relations, property-based testing, REST-API tools) and argues why each misses the documentation-implementation residual. However, the paper does not empirically demonstrate that these alternatives would fail on VDBMSs. For example, could differential testing catch nprobe=0 violations if the comparison reference implements the documented range? The structural argument is plausible, but experimental validation (even on 1-2 cases) would strengthen the claim that LLM-oracle is necessary rather than merely convenient.
   - **1.3** The significance is bounded by scope. The paper targets documentation-implementation consistency, not result correctness (ANN recall, ranking). Section 2 explicitly bounds this, and RQ3's bidirectional probe focuses on crash vs. silent-accept oracles. The contribution is significant within this boundary but does not address the full correctness problem identified in the VDBMS roadmap.

2. **Novelty** — Adequate
   - **2.1** The novelty claim over REST-API oracle tools is valid. I verified against MASTOR (cached summary read) and SATORI (first 100 lines of full text read). MASTOR reads source to generate oracles encoding implemented behavior — it tests what the code does, not whether documentation matches implementation. SATORI requires OpenAPI schemas; VDBMS documentation carries constraints in prose without schema fields, so SATORI's extraction has no input. The paper correctly characterizes both (Section 7, Related Work). The source-grounded falsifier (dev-reviewer) is a genuine delta: prior tools treat LLM as final arbiter; TestVDB falsifies LLM claims against source.
   - **2.2 [minor, fixable]** The paper cites AugmenTest (Section 7, Related Work) as treating LLM as final arbiter, which is accurate, but does not engage with AugmenTest's reported precision (30% Extended Prompt vs. TestVDB's 67%). AugmenTest's 8.2% TOGA baseline and 18.2% RAG performance would provide useful competitive context for TestVDB's precision claims. The delta exists (source falsification), but the quantitative comparison is missing.
   - **2.3** The novelty over VDBFuzz is well-established. The bidirectional probe (RQ3, Section 6) shows structural complementarity: VDBFuzz's crash oracle cannot detect silent accepts by construction. On Qdrant v1.18.2, VDBFuzz ran 26,000 requests and reached 0 of 14 TestVDB TPs (all silent accepts). This is a systematic direction, not an n=1 case. TestVDB reached VDBFuzz's integer-overflow crash on v1.4.0 via contract reasoning. The #9045 example (wait=false accepts zero-length vector, VDBFuzz's templates don't probe this path) further isolates the limitation to current templates, not crash oracles as a class.
   - **2.4** The LLM-reliability contribution (diagnosing hallucination + self-preference, introducing source anchor) is incremental but meaningful. Panickssery et al. (Section 7, Related Work) established self-preference; Haldar et al. showed judge inconsistency. TestVDB applies these insights to design a falsifier that breaks both biases. The multi-perspective judging baseline (80% precision, 15% recall) validates that voting alone is insufficient.

3. **Soundness** — Adequate
   - **3.1** The main claims are supported with appropriate evidence. RQ1 (yield: 107 candidates, 49 TPs) uses maintainer adjudication as ground truth, which is reasonable. RQ2 (precision/recall on 48-candidate retrospective) uses controlled comparison (single-LLM baseline, multi-perspective baseline, dev-reviewer with ablations). The three-condition ablation (Table 6: source alone 75% FP suppression, threat-model 50%, union 91%) triangulates source grounding's contribution. The source-disabled control (74% → 19% recall) further isolates the effect.
   - **3.2 [major, fixable]** Operating point selection is post-hoc and not pre-registered. Table 5 reports four operating points (single-run, 3-run union, 5-run union, 5-run majority) and selects 3-run union as the headline. The paper acknowledges this is "post-hoc" and notes Wilson CIs don't account for selection (Section 6, RQ2). A Bonferroni correction would widen 3-run precision to roughly [44%, 84%]. This does not change the qualitative claim (source grounding lifts recall above 37% baseline), but the headline numbers (67% / 74%) should be flagged as exploratory. A pre-registered selection rule (e.g., "highest F1" or "recall ≥ 70% at precision ≥ 60%") would strengthen causal inference.
   - **3.3** The VDBFuzz comparison is methodologically sound. The systematic direction (VDBFuzz on TestVDB's pinned version with 26,000 requests, 0 of 14 TPs reached) provides generalizable evidence for crash-oracle limitations. The controlled cases (v1.4.0 crash reached by TestVDB, v1.18.0 #9045 missed by VDBFuzz templates) isolate mechanisms without overgeneralizing from n=1 examples.
   - **3.4 [minor, unfixable]** External validity is limited by single-LLM-family evaluation. The cross-model re-run (DeepSeek, Qwen, LongCat; κ = 0.14/0.37/0.51 vs. GLM) shows family-specific verdicts, so cross-family robustness cannot be claimed. The paper acknowledges this (Section 6, RQ2 / Threats to validity). This is inherent to the current evaluation scope and would require additional resources to fix.
   - **3.5** Construct validity: The 48-candidate retrospective is maintainer-adjudicated but non-random, and the paper does not claim it's representative. The threat-to-validity discussion (Section 6, Threats to validity) is honest about this limitation. "Implementation-as-correct" assumption bounds the approach (implementation bug could wrongly falsify correct documentation); the 15 merged-PR fixes suggest this holds often enough to be useful.

4. **Verifiability** — Excellent
   - **4.1** The paper provides sufficient detail to follow the work. Section 3 describes the four-stage pipeline with concrete examples (Milvus #49823 path). Appendix excerpts key agent prompts (contract-formalizer, dev-reviewer). The artifact (https://github.com/yihui504/testvdb-anon) includes 22 agent definitions, target versions, per-token accounting, 48-candidate ground truth, and reproduction driver. Cost breakdown (~$10 per target, ~10^4 LLM calls) is transparent.
   - **4.2** The links are declared and reachable. The GitHub URL is provided. The paper does not claim to have executed the artifact for this review (per rubric instructions), but the text describes the procedure well enough to replicate conceptually.

5. **Presentation** — Adequate
   - **5.1** The structure is logical and complete. Problem → Background → Approach → False-Positive Analysis → Dev-Reviewer → Evaluation → Related Work → Discussion. The 9-page length is appropriate for the contribution.
   - **5.2 [minor, fixable]** Some figures could be clearer. Figure 1 (pipeline sketch) is readable but dense; a simplified version highlighting the three dev-reviewer checks would improve accessibility. Table 5 (operating points) is dense with CIs and footnotes; the main takeaway (3-run union at knee of precision-recall trade-off) could be called out more explicitly in the caption.
   - **5.3 [minor, fixable]** Language is generally clear with occasional awkwardness. Example: "The oracle problem is acute here" (Section 2) could specify what "acute" means (e.g., "no deterministic oracle applies"). "Silent-accept defect does not surface as a crash" (Section 1) could explicitly state the consequence (corrupted query semantics without error signal).
   - **5.4** Notation is consistent. LLM agents are clearly named. VDBMS versions are pinned (Milvus 2.6.19, Qdrant v1.18.2, Weaviate v1.38.2). Statistical reporting (Wilson CIs, Bonferroni, bootstrap) is appropriate for the scale.

### Questions for Authors
- **Q1:** Could you provide empirical validation of the oracle-exclusion argument in Table 1? For example, run differential testing on nprobe=0 across Milvus/Qdrant/Weaviate to show cross-vendor accept/reject diverges, or apply SATORI/AGORA+ to a VDBMS with OpenAPI to demonstrate they miss silent-accept defects? Even 1-2 concrete cases would strengthen the claim that LLM-oracle is necessary rather than convenient. — Intended effect: if added, item 1.2's rating would move from Adequate toward Excellent.
- **Q2:** What was the decision process for selecting 3-run union as the headline operating point? Was there a pre-registered rule (e.g., "knee of precision-recall curve"), or was the selection informed by observing the results? — Intended effect: clarify whether 3.2's [major, fixable] tag should be downgraded to [minor] if a principled (though post-hoc) rule was applied.


---

## Reviewer 2: Area Specialist

**Overall Recommendation:** Weak Accept

### Summary

TestVDB targets documentation-implementation defects in Vector Database Management Systems (VDBMSs)—cases where a VDBMS silently accepts inputs that violate its API documentation (e.g., accepting `nprobe=0` when documentation specifies `[1, 16384]`). Because the boundary is natural-language prose, deterministic oracles cannot adjudicate these accept/reject decisions, leaving LLMs as the practical oracle. The LLM introduces two false-positive failure modes: hallucination in claim extraction and self-preference in judgment. The paper introduces a **dev-reviewer agent** that acts as a source-grounded falsifier, reproducing each candidate, cross-checking it against implementation source, and trying to disprove it. TestVDB surfaced 107 issues across three VDBMSs (Milvus, Qdrant, Weaviate) with 49 maintainer-acknowledged true-positive defects (15 fixed via merged PR). On a controlled retrospective over 48 maintainer-adjudicated candidates, the dev-reviewer reaches 67% precision and 74% recall (3-run ensemble) versus 37% recall without the source anchor. A bidirectional probe against VDBFuzz shows TestVDB reaches a crash-class defect by contract reasoning while VDBFuzz misses a TestVDB silent-accept defect under current templates.

### Core Strengths

- **S1:** Clear problem definition and oracle-exclusion argument (Table 1) — see 1.1
- **S2:** Rigorously maintained ground truth through developer adjudication — see 3.1
- **S3:** Source-grounded falsifier is a well-motivated response to LLM self-preference — see 2.3
- **S4:** Strong empirical signal: 37% → 74% recall gain from source grounding — see 3.2

### Core Weaknesses

- **W1:** Single LLM family (GLM-5.2) used throughout; cross-family generalization explicitly left open with weak preliminary evidence — see 3.3 [major, fixable]
- **W2:** Operating point selection (3-run union) is post-hoc without pre-registration; statistical claims do not account for this selection — see 3.2 [major, fixable]
- **W3:** RQ3 bidirectional probe has asymmetric depth: systematic VDBFuzz-on-v1.18.2 (26K requests, 0/14) vs. two isolated $n=1$ cases in reverse direction — see 3.4 [minor, fixable]
- **W4:** Related Work characterizes SATORI's limitations without independent verification against the actual SATORI paper — see 2.2 [minor, fixable]

### Detailed Assessment

#### 1. Significance — Adequate

- **1.1** [Strength] The paper identifies a real problem: VDBMS defects that corrupt query semantics without crashing. The bug study citation (roadmap25, 43% functional failures) and the 49 maintainer-acknowledged defects across three production VDBMSs demonstrate practical impact. The 15 merged-PR fixes show the defects matter to maintainers.

- **1.2 [major, fixable]** The contribution is bounded in three ways that limit significance. First, the approach is VDBMS-specific; the generalization claim to other domains (REST APIs without OpenAPI, configuration validation, policy-as-code) is structural-only with only a single CouchDB probe showing portability. Second, the single-LLM-family evaluation (GLM-5.2) means the source-grounded falsifier's effectiveness is backbone-dependent; the cross-family re-run (κ = 0.14–0.51) shows the verdict is family-specific, so we cannot claim the falsifier works generally across LLMs. Third, the target defect class (documentation-implementation consistency) is a subset of VDBMS bugs; the paper acknowledges result correctness (ANN recall, ranking) is out of scope. The significance is real but narrow.

- **1.3 [minor, fixable]** The RQ3 bidirectional probe against VDBFuzz has asymmetric strength. The systematic direction (VDBFuzz on v1.18.2, 26K requests, 0 of 14 silent-accept TPs reached) is compelling evidence that crash oracles miss this defect class. The reverse direction is weaker: only two controlled $n=1$ cases showing TestVDB reaching crash-class defects that VDBFuzz templates missed. While the paper correctly identifies this as a template limitation rather than a crash-oracle property, the asymmetry means the "complementary coverage" claim is stronger in one direction than the other.

#### 2. Novelty — Adequate

- **2.1 [major, fixable]** The source-grounded falsifier is a plausible but not definitively new contribution. The paper positions it as novel relative to documentation-derived oracles (Toradocu, AugmenTest, Doc2OracLL) that keep the LLM as final arbiter. However, the falsification mechanism itself—cross-checking LLM verdicts against an independent ground truth—is conceptually similar to how MASTOR uses source to generate oracles, just applied in reverse (MASTOR: source → oracle; TestVDB: doc → claim, then source as falsifier). The paper acknowledges this in Related Work but the novelty claim rests on the *direction* of source usage (falsification vs. generation) rather than the mechanism itself. Given that MASTOR already used source as a reference for oracle generation, the incremental novelty is real but thinner than the paper's framing suggests.

- **2.2 [minor, fixable]** The Related Work characterization of SATORI cites its dependence on low-ambiguity structured sources (OpenAPI schema elements) and argues "SATORI's extraction step has no input to work from" for prose documentation. The structural exclusion argument (Table 1) is logically sound—the documentation-implementation residual does leave an LLM as the practical oracle—but the paper characterizes SATORI from its own framing rather than independently verifying the SATORI paper's actual capabilities (e.g., whether SATORI can leverage natural-language descriptions in OpenAPI fields). This is a minor weakness because the core exclusion argument (Table 1) stands independently; a revision could sharpen it by directly citing what SATORI's own paper confirms it cannot handle.

- **2.3 [Strength]** The two-mode failure analysis (hallucination in extraction, self-preference in judgment) is well-motivated and the falsifier design directly targets both. The multi-perspective judging baseline (80% precision, 15% recall) establishes that voting cannot break the documentation-ambiguity agreement, which strongly motivates the need for an independent ground truth. This is a solid novelty contribution: identifying why multi-agent voting fails in this regime and proposing source as the solution.

#### 3. Soundness — Weak

- **3.1 [Strength]** The evaluation uses maintainer adjudication as ground truth, which is a high standard. Of 107 submitted issues, 72 were adjudicated (49 true-positive, 23 by-design or rejected) and 35 remain pending. The paper is transparent about worst-case bounds (45.8% precision if all pending are false positives) and acknowledges the 48-candidate retrospective is non-random. The 15 merged-PR fixes provide strong evidence that the defects are real, not just artifacts of the LLM oracle.

- **3.2 [major, fixable]** The operating point selection for the dev-reviewer is post-hoc without pre-registration. The paper reports four operating points (single-run band, 3-run union, 5-run union, 5-run majority) and selects the 3-run union as the headline because it "sits at the knee of the precision-recall trade-off." However, the Wilson CIs reported for the 3-run union (precision [49, 81], recall [55, 87]) do not account for this selection across four points. The paper provides a Bonferroni correction (widening to roughly [44, 84]/[51, 89]) and a bootstrap validation ([53, 83]/[71, 96]), which mitigates but does not eliminate the concern. This is fixable by either (a) pre-registering the operating point or (b) clearly labeling all numbers as post-hoc exploratory results rather than headline claims.

- **3.3 [major, fixable]** The cross-family generalization experiment is methodologically sound but weakly reported. The paper ran three additional families (DeepSeek, Qwen-3.8-Max, LongCat-2.0) with "one full SOP run each" and reports κ agreement against GLM-5.2 (0.14, 0.37, 0.51) and recall ranges (18–56% vs. 85% for GLM's 5-run union). This is better than nothing, but "one full SOP run each" is minimal statistical evidence. Given that the backbone-dependence is a major limitation (W1), this experiment should be stronger: multiple runs per family, pre-registered comparison protocol, and a clearer statement of whether source grounding benefits generalize beyond GLM-5.2.

- **3.4 [minor, fixable]** The RQ3 bidirectional probe interpretation is slightly overstated. The paper claims VDBFuzz "reached 0" of 14 silent-accept TPs on v1.18.2, which is technically accurate but omits that this is on a *fixed budget* of 26K requests, not an exhaustive search. If VDBFuzz's templates have low probability coverage of the silent-accept paths, a budget of 26K may simply be insufficient. The structural interpretation (crash oracles cannot detect non-crashing accepts) is sound, but the "VDBFuzz reached 0" phrasing suggests exhaustiveness that the budget does not guarantee.

#### 4. Verifiability — Adequate

- **4.1 [Strength]** The paper provides a complete artifact: prompts (22 agent role definitions), target versions, per-token accounting, the 48-candidate ground truth, and a reproduction driver at `https://github.com/yihui504/testvdb-anon`. The prompts are excerpted in Appendix A. This is well above the minimum for reproducibility.

- **4.2 [minor, fixable]** The paper could improve verifiability by clarifying two procedural details in the evaluation. First, the 48-candidate retrospective selection: are these the *first* 48 adjudicated candidates? A random subset? Or selected for diversity? The paper calls it "non-random" but does not specify the selection mechanism, which matters for external validity. Second, the CouchDB and Elasticsearch portability probes (Section 8, Discussion) lack detail on how the contract-formalizer was adapted to non-VDBMS documentation. Given that generalization is a claimed contribution, a fuller method description would help others replicate the portability claim.

#### 5. Presentation — Adequate

- **5.1 [minor, fixable]** The paper structure is clear and readable. Figures (pipeline diagram, dev-reviewer three-check diagram) are helpful. However, some notation is inconsistent: the abstract uses "dev-reviewer" while the body uses "dev-reviewer agent" interchangeably. Table 5's "Operating point" column formatting could be clearer (the per-run band spans two lines but is a single row).

- **5.2 [minor, fixable]** Several typos and language errors appear throughout:
  - The introduction: "we introduce a dev-reviewer agent" → inconsistent capitalization of dev-reviewer
  - Section 2: "correctness of vector search remains open and is not our claim~\cite{roadmap25}" → should be "is not our claim to establish" or similar
  - Table 2: "Share of calls" → should be "Share of LLM calls" for clarity
  - Table 5 caption: "any-confirmed" hyphenation is inconsistent with later usage (sometimes hyphenated, sometimes not)

These are minor but collectively suggest one more proofreading pass would improve readability.

### Questions for Authors

- **Q1:** The 3-run union operating point is selected post-hoc across four candidates. If you had pre-registered a different operating point (e.g., 5-run majority or a precision-constrained selection), how would the headline numbers change? This affects item 3.2's rating.

- **Q2:** The cross-family generalization experiment uses only one SOP run per family. What would the precision/recall ranges look like with a 3-run union for each family, matching the GLM-5.2 protocol? This affects item W1's severity—if source grounding helps uniformly across families, the single-family limitation is less concerning.

- **Q3:** The Related Work claims SATORI cannot handle prose documentation because "SATORI's extraction step has no input to work from." Have you verified this claim against the SATORI paper? If SATORI can handle some prose constraints (e.g., natural-language descriptions in OpenAPI fields), how would that change Table 1's exclusion argument? This affects item 2.2's assessment.

- **Q4:** The CouchDB/Elasticsearch portability probes show extraction and probing work but find no silent-accept defects. Is this because mature non-VDBMS APIs validate strictly (as the paper suggests), or because the contract-formalizer's prompts are tuned to VDBMS documentation patterns and miss non-VDBMS ambiguity? This affects the generalization claim's strength.


---

## Reviewer 3: General Reviewer

**Overall Recommendation:** Weak Accept

### Summary
TestVDB targets documentation-implementation defects in Vector Database Management Systems (VDBMSs)—cases where a system silently accepts inputs that violate its API documentation, such as accepting nprobe=0 when the documentation specifies the range as [1, 16384]. Because the documented boundary is natural-language prose, deterministic oracles (crash detection, differential testing, metamorphic relations, property-based testing, or REST-API tools that extract from structured sources) cannot adjudicate these accept/reject decisions, leaving an LLM as the practical oracle. The authors instantiate TestVDB as a four-stage pipeline (behavioral-claim extraction, test generation, sandboxed execution, defect confirmation) that uses LLMs to read documentation, generate tests, and adjudicate responses. Two failure modes produce false positives: hallucination in extraction (the LLM invents constraints the documentation does not state) and self-preference bias in judgment (the same family that extracts a claim tends to confirm it). A multi-perspective judging baseline reaches high precision but collapses recall, so the authors introduce a dev-reviewer agent that acts as a source-grounded falsifier, reproducing each candidate, cross-checking it against implementation source, and trying to disprove it. TestVDB surfaced 107 candidate issues across three VDBMSs (Milvus, Qdrant, Weaviate); maintainers acknowledged 49 as true-positive defects (15 fixed via merged PR). On a controlled retrospective over 48 maintainer-adjudicated candidates, the dev-reviewer reaches 67% precision and 74% recall (3-run any-confirmed ensemble), against 37% recall without the source anchor. A bidirectional probe against VDBFuzz shows TestVDB reaches a crash-class defect by contract reasoning, while VDBFuzz misses a silent-accept defect under its current templates.

### Core Strengths
- **S1:** Clear problem formulation with strong motivation — see 1.1, 1.2. The authors convincingly establish documentation-implementation defects as a prevalent, costly class that existing fuzzers miss, and the oracle-exclusion argument (Table 1) cleanly positions why LLMs are the practical option.
- **S2:** Well-structured false-positive diagnosis — see 2.2. The separation of hallucination (extraction) and self-preference (judgment) failure modes, with empirical demonstration that multi-perspective judging is structurally insufficient, is a strong contribution.
- **S3:** Grounded evaluation with maintainer adjudication — see 4.1. The 107 submitted issues with 49 maintainer-acknowledged true positives (15 merged-PR-fixed) across three production VDBMSs provides convincing real-world impact evidence.
- **S4:** Thorough ablation and cross-family analysis — see 3.4, 4.2. The three-condition ablation (Table 6), source-grounding removal control, and independent cross-model re-run (DeepSeek/Qwen/LongCat) establish the source anchor's contribution and document backbone-dependence honestly.

### Core Weaknesses
- **W1:** Post-hoc operating point selection — see 3.2 [major, fixable]. The 3-run union headline is selected post-hoc from four operating points without pre-registration; the Wilson CIs in Table 5 do not account for this selection, and the Bonferroni-corrected intervals are not used as the primary reporting format.
- **W2:** Single-backbone evaluation limits cross-family generalization claims — see 3.4 [major, fixable]. All dev-reviewer results use GLM-5.2; the cross-model re-run shows family-specific verdicts (κ = 0.14/0.37/0.51), so the 74% recall claim does not generalize across model families without qualification.
- **W3:** External validity weak on transfer beyond VDBMSs — see 1.3 [major, fixable]. The CouchDB/Elasticsearch probes are shallow (5 claims on _all_docs, method portability rather than defect detection), and no non-VDBMS case study surfaced silent-accept defects, leaving the transferability claim preliminary.

### Detailed Assessment

1. **Significance** — Adequate
   - **1.1** Strong problem motivation with real-world impact — The Introduction (Section 1) and Background (Section 2) convincingly establish documentation-implementation defects as a prevalent, costly defect class in VDBMSs. The 107 submitted issues with 49 maintainer-acknowledged true positives (15 merged-PR-fixed) across three production systems demonstrates practical impact that matters to system maintainers and downstream LLM applications.
   - **1.2** Clear value proposition over existing approaches — The oracle-exclusion argument (Table 1) is a strong structural contribution: it systematically walks through why deterministic oracles (crash detection, differential testing, metamorphic relations, property-based testing, REST-API tools from structured sources) miss the documentation-implementation residual, leaving LLMs as the practical option. This framing clarifies the problem space and TestVDB's positioning.
   - **1.3 [major, fixable]** Scope bounded by VDBMS-specific evaluation — The contribution is positioned as VDBMS-specific, but the Discussion (Section 8) claims transferability to structurally similar documentation regimes (REST APIs without OpenAPI, configuration validation, policy-as-code) on structural grounds only, with only shallow portability probes (CouchDB/Elasticsearch probed 5 claims each, method validation rather than defect detection). This limits the claimed generalization scope; a revision could strengthen it by adding at least one non-VDBMS case study that surfaces a real silent-accept defect.

2. **Novelty** — Adequate
   - **2.1** Clear delta over REST-API oracle tools that avoid the ambiguous-prose regime — The Related Work (Section 7) positions TestVDB against AGORA+ (traces), SATORI (OpenAPI), and MASTOR (source) by emphasizing that those tools extract from low-ambiguity structured sources and explicitly avoid the regime where documentation is natural-language prose. The boundary is concrete: SATORI assumes every constraint has an OpenAPI field (type, format, minimum, maximum); VDBMS documentation carries these in prose with no schema anchor, so SATORI's extraction step has no input. (Assessed from the paper's own characterization; not independently verified against the SATORI paper.)
   - **2.2** Source-grounded falsification as a novel countermeasure to LLM false-positive modes — The dev-reviewer (Section 5) introduces a distinct approach: instead of adding more judge agents (multi-perspective judging), it grounds the falsifier in implementation source, breaking both hallucination (by not depending on documentation) and self-preference (by not coming from the same family). The three-check design (independently reproducible, evidence sufficient, falsifiable) and the falsifier semantics are a novel contribution to LLM-as-judge reliability.
   - **2.3 [minor, fixable]** Delta over documentation-derived oracle lines needs sharper positioning — The Related Work discusses Toradocu, Doc2OracLL, AugmenTest, ChatAssert, and Testora, but the delta is stated as "all treat the LLM as the final arbiter, verifying through runtime behavior; TestVDB instead falsifies against implementation source." This is accurate but could be sharper: what specific limitation of each prior approach does TestVDB overcome, and is the delta a methodological advance or an application-domain adaptation?

3. **Soundness** — Adequate
   - **3.1** Well-supported main claims with controlled evaluation — RQ1 (107 submitted, 49 acknowledged TP, 15 merged-PR fixed) provides real-world impact evidence. RQ2 (48-candidate retrospective, 67% precision/74% recall vs. 56%/37% baseline) is controlled with maintainer adjudication ground truth. The bidirectional VDBFuzz probe (RQ3) isolates complementary coverage mechanistically (Table 8: systematic direction VDBFuzz → 0/14 TPs on v1.18.2; two controlled crash-class cases on older versions).
   - **3.2 [major, fixable]** Post-hoc operating point selection without pre-registration — Section 6 (RQ2) reports four operating points (3-run union, 5-run union, 5-run majority, single-run band) and selects the 3-run union as the headline. The authors flag it as "post-hoc" and provide Bonferroni-corrected CIs, but the Wilson CIs in Table 5 (the primary reporting format) do not account for selection across the four points. A pre-registered analysis plan or a single primary operating point would have strengthened this.
   - **3.3 [minor, fixable]** 48-candidate retrospective is maintainer-adjudicated but non-random — The Threats-to-validity paragraph (Section 6) acknowledges the 48-candidate set is non-random and not pre-registered, and the authors flag that capture-recapture or unbiased defect-sample estimation is future work. This is a limitation clearly stated, but it bounds the generalizability of the 74% recall estimate.
   - **3.4** Honest limitation discussion on backbone-dependence — The cross-model re-run (DeepSeek, Qwen-3.8-Max, LongCat-2.0) showing family-specific verdicts (κ = 0.14/0.37/0.51) is thoroughly reported, and the authors explicitly state they cannot claim cross-family robustness. This transparency is a strength, though the family-specific verdicts are also a material limitation (see W2).

4. **Verifiability** — Excellent
   - **4.1** Comprehensive artifact availability — The paper declares an artifact link (https://github.com/yihui504/testvdb-anon) and specifies its contents: 22 agent role definitions (agents/), 48-candidate ground truth (test_questions/), reproduction driver (reproduction/full52/), target versions, and per-token accounting. The text (Section 3) describes the LLM backbone (GLM-5.2 via BigModel Anthropic-compatible API, default sampling, temperature/top-p at provider defaults) and per-stage call distribution (Table 2). For a reader with API access, this should be sufficient to reproduce the pipeline.
   - **4.2** Clear reproduction specifications for controlled experiments — The ablation (Table 6, 12-FP/4-TP Milvus control) and the VDBFuzz bidirectional probe (Table 8, specific versions and request counts) are specified in enough detail to trace the methodology. The source-grounding removal control ("disabling Step 3.5") is described, though a more explicit pointer to the implementation component would help.
   - **4.3 [minor, fixable]** Appendix prompts are excerpts, not full reproductions — Appendix A excerpts two agent prompts (contract-formalizer and dev-reviewer) but notes "the full 22 agent definitions are in the artifact." This is acceptable for space, but a reader cannot verify the exact multi-perspective judging baseline (Table 3) or the attack agents' logic from the paper alone; they must clone the artifact.
   - **4.4** No broken links or unreproducible claims detected — The artifact URL is declared as reachable, and no methodological dead-ends are apparent from the text.

5. **Presentation** — Adequate
   - **5.1** Sound structure and readable flow — The paper follows a clear structure: Introduction → Problem Setup (oracle exclusion) → Approach (4-stage pipeline) → False-Positive Diagnosis → Dev-Reviewer Solution → Evaluation (3 RQs) → Related Work → Discussion/Limitation → Conclusion. The figures (Figure 1 pipeline, Figure 2 dev-reviewer checks, Figure 3 per-run recall) and tables (Table 1 oracle exclusion, Table 5 operating points, Table 6 ablation, Table 8 VDBFuzz versions) are well-placed and support the text.
   - **5.2 [minor, fixable]** Dense technical material in some sections — Section 6 (RQ2) packs four operating points, Wilson CIs, Bonferroni correction, bootstrap validation, and a three-condition ablation into two paragraphs. The information is all there, but a reader must slow down to extract the primary claim (3-run union at 67%/74%) from the alternatives. A slight restructuring to foreground the headline before the operating-point exploration would improve readability.
   - **5.3 [minor, fixable]** Minor notation inconsistency — Table 2 caption says "Approximate per-target LLM-call distribution" but the body uses "~50%" notation; the "~" symbol is not defined. The text mixes "~10^4 calls" and "~$10$" approximation styles in the same context.
   - **5.4 [minor, fixable]** One LaTeX formatting nit — The RQ2 paragraph uses "0.05/4" inline without math-mode formatting; should be "$0.05/4$".
   - **5.5** No pervasive language or clarity issues — The paper is readable throughout, and the core ideas (oracle exclusion, false-positive modes, source-grounded falsification) are explained clearly. No structural gaps or obstructive ambiguities.

### Questions for Authors
- **Q1:** On the post-hoc operating point selection (item 3.2) — If the authors had pre-registered a single primary operating point (e.g., 3-run union) and reported Wilson CIs only for that point, would the qualitative claim "source grounding lifts recall above the 37% baseline" still hold? Would the Bonferroni-corrected intervals change the interpretation?
- **Q2:** On cross-family generalization (item 3.4) — The cross-model re-run shows family-specific verdicts. If a future evaluation on a different LLM family (beyond GLM-5.2, DeepSeek, Qwen, LongCat) achieved similar performance (e.g., >70% recall with source grounding), would the authors revise the claim to "source grounding is effective when the backbone has X property"? What would that property be?
- **Q3:** On transfer beyond VDBMSs (item 1.3) — The CouchDB/Elasticsearch probes validate method portability but found no silent-accept defects. Did the authors consider probing targets where documentation is known to be ambiguous (e.g., a newer REST API without mature validation, or configuration languages)? A single non-VDBMS case study where TestVDB surfaces a silent-accept defect would strengthen the transferability claim.


---

## Meta-Review

### Criterion Consensus

| Criterion | Reviewer 1 | Reviewer 2 | Reviewer 3 | Meta-Review |
|---|---|---|---|---|
| Significance | Adequate | Adequate | Adequate | **Adequate** |
| Novelty | Adequate | Adequate | Adequate | **Adequate** |
| Soundness | Adequate | Weak | Adequate | **Adequate** |
| Verifiability | Excellent | Adequate | Excellent | **Excellent** |
| Presentation | Adequate | Adequate | Adequate | **Adequate** |
| **Recommendation** | **Weak Accept** | **Weak Accept** | **Weak Accept** | **ACCEPT** |

### Meta Recommendation
**ACCEPT**

All three independent reviewers returned Weak Accept (unanimous shortcut). Across the five criteria there is no consensus Poor and no consensus substance Weak: Soundness reaches consensus Adequate by majority (R2 is the lone Weak; R1 and R3 both Adequate), Verifiability reaches consensus Excellent by majority (R1/R3 Excellent, R2 Adequate), and the remaining three criteria are unanimous Adequate. No `[major, unfixable]` item survives in any verified draft, so nothing inherent blocks acceptance.

The two deepest consensus weaknesses are both `[major, fixable]` and both already mitigated in the text: (i) post-hoc operating-point selection (all three reviewers flag Section 6 / RQ2) — the paper already supplies Bonferroni-corrected CIs and a bootstrap validation; the residual is a framing fix (label headline numbers as exploratory, or pre-register a single operating point); (ii) single-backbone / cross-family generalization (all three reviewers flag the GLM-5.2-only evaluation) — the paper already runs DeepSeek/Qwen/LongCat and honestly reports κ = 0.14–0.51; the residual is more runs per family. R2 is the strictest reviewer (the only Soundness Weak) precisely on these two points; the divergence with R1/R3 is on severity, not on the facts, and both items are fixable in a revision cycle.

Three inherent limitations recur (post-hoc operating point, single LLM family, external portability beyond VDBMSs). They bound the paper's ceiling — which is why the verdict is ACCEPT rather than a higher commendation — but each is disclosed honestly (Bonferroni + bootstrap; κ data; CouchDB/Elasticsearch probes) and none rises to `[major, unfixable]`. The core contribution — source-grounded falsification as a countermeasure to LLM hallucination + self-preference in the documentation/implementation residual — is sound, novel against verified competitors (MASTOR/SATORI fetched), and supported by 49 maintainer-acknowledged TPs.

### Priority Revisions
1. **[consensus, major, fixable]** Post-hoc operating-point selection (R1 3.2 / R2 3.2 / R3 3.2). Either pre-register a single primary operating point or explicitly label the 3-run-union headline numbers (67%/74%) as exploratory, with the Bonferroni-corrected intervals ([44,84]/[51,89]) as the primary reporting format.
2. **[consensus, major, fixable]** Cross-family generalization (R1 3.4 / R2 W1+3.3 / R3 W2+3.4). Run at least one non-GLM family under the 3-run union protocol matching GLM-5.2, and report precision/recall ranges; the current "one full SOP run each" is minimal evidence.
3. **[R2/R3, minor→major, fixable]** RQ3 reverse-direction asymmetry (R2 3.4 / R3 implied). The systematic VDBFuzz→TestVDB direction (26K requests, 0/14) is strong; the reverse TestVDB→VDBFuzz direction rests on two controlled n=1 cases. A fixed-budget systematic reverse run would make "complementary coverage" symmetric.
4. **[R2, minor, fixable]** SATORI characterization (R2 2.2/W4). Fetch and verify the SATORI paper's actual capabilities against the paper's exclusion argument; either confirm "no input for prose" from SATORI's own text or soften the claim to a structural-positioning argument.
5. **[R3, major, fixable]** External portability (R3 W3/1.3). Add at least one non-VDBMS case study that surfaces a real silent-accept defect, or explicitly weaken the transferability claim to "method-portable, defect-detection unverified beyond VDBMSs."

**Inherent limitations (not revision-blocking, disclosed honestly):** post-hoc operating point (needs pre-registration); single LLM family (needs substantial re-runs); external portability (CouchDB/Elasticsearch returned 0 defects). These cap the verdict at ACCEPT rather than a higher tier.


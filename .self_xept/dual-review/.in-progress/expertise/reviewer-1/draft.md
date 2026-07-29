## Reviewer 1: Domain Expert

**Overall Recommendation:** Weak Accept

### Summary

TestVDB targets documentation-implementation defects in Vector Database Management Systems (VDBMSs) — a class of logical bugs where a VDBMS silently accepts inputs or behaviors that violate its API documentation (e.g., accepting `nprobe=0` when documentation specifies range `[1, 16384]`). Because the boundary is specified in natural-language prose, deterministic oracles (crash detection, differential testing, metamorphic relations, property-based testing, REST-API tools that rely on structured sources) cannot adjudicate these accept/reject decisions. The paper instantiates a four-stage LLM pipeline (claim extraction, test generation, sandboxed execution, defect confirmation) that uses LLMs to read documentation, generate tests, and judge conformance. Two failure modes produce false positives: hallucination in extraction (LLM invents constraints the documentation doesn't state) and self-preference bias in judgment (same-family LLM confirms its own extracted claims). A multi-perspective judging baseline raises precision but collapses recall. The paper introduces a dev-reviewer agent that acts as a source-grounded falsifier, reproducing each candidate independently and cross-checking against implementation source to suppress false positives. TestVDB surfaced 107 issues across three VDBMSs (Milvus, Qdrant, Weaviate); maintainers acknowledged 49 as true-positive defects, with 15 fixed via merged PR. On a 48-candidate retrospective, the dev-reviewer reaches 67% precision and 74% recall (3-run ensemble) against 37% recall without the source anchor. A bidirectional probe against VDBFuzz on Qdrant shows complementary coverage.

### Core Strengths

- **S1:** Well-motivated problem — documentation-implementation defects are a prevalent, impactful defect class that existing VDBMS fuzzers miss (44 of 49 true positives in this paper's results do not crash).  — see 2.1, 3
- **S2:** Sound exclusion argument — Table 1 shows principled reasons why each deterministic oracle class cannot reach the documentation-implementation residual, making the LLM-as-oracle choice well-justified.  — see 2, 7
- **S3:** Demonstrated practical impact — 49 maintainer-acknowledged defects across three production VDBMSs, with 15 already fixed via merged PR, shows the approach finds real bugs.  — see 6
- **S4:** Source-grounded falsification contribution — The dev-reviewer's three-check design (independent reproducibility, evidence sufficiency, falsifiability) is a genuine technical advance over single-LLM and multi-perspective baselines.  — see 5

### Core Weaknesses

- **W1:** Single-backbone evaluation — All dev-reviewer results use only GLM-5.2; cross-model re-run shows verdict is family-specific (κ = 0.14–0.51 vs. other families), so the headline 67%/74% precision/recall may not generalize.  — see 6.2
- **W2:** Limited external validity — Controlled retrospective covers only Milvus and Qdrant (48 candidates); Weaviate results are yield-only without controlled analysis. Non-VDBMS transferability (CouchDB, Elasticsearch) is exploratory only.  — see 6.3, 8
- **W3:** Operating point selection — The 3-run union ensemble is selected post-hoc from four operating points; Wilson CIs don't account for this selection, and no pre-registered rule justifies the choice.  — see 6.2
- **W4:** No false-negative quantification — Paper acknowledges dev-reviewer can wrongly suppress true defects when implementation is buggy but documentation is right; false-negative rate is not estimated.  — see 8

### Detailed Assessment

1. **Significance** — Adequate

- **1.1** **Well-motivated problem.** Documentation-implementation defects are a logical-bug majority that crash-oracle fuzzers miss. The paper grounds the problem in an empirical bug study (bugstudy25) and VDBMS testing roadmap (roadmap25), showing 43% of VDBMS bugs stem from incorrect behavior and >50% manifest as functional failures. The 49 maintainer-acknowledged defects across three production systems demonstrate practical relevance.

- **1.2** **Clear impact.** The 15 merged-PR fixes (plus 16 open fix-PRs) across Milvus, Qdrant, and Weaviate represent tangible impact. These are not hypothetical findings — maintainers applied patches, confirming the defects are real and worth fixing.

- **1.3 [major, fixable]** **Unclear scope boundaries.** The paper focuses on "documentation-implementation defects" but does not clearly delimit what counts as documentation (API docs? README? comments?) versus what counts as implementation (HTTP handlers? storage layer?). §2 separates consistency from correctness, but the boundary between "accept/reject behavior" (consistency) and "returned result correctness" is fuzzy in practice. For example, if a VDBMS silently accepts an invalid `ef` parameter and returns wrong recall due to it, is this a consistency defect (accepted invalid input) or a correctness defect (wrong ANN result)? The paper treats it as consistency, but the root cause may be correctness-focused (bad index parameters affect search quality). This conceptual blurring undermines clarity of the defect class.

- **1.4 [minor, fixable]** **Limited generalization evidence.** §8 claims transferability to "structurally similar documentation regimes" (REST APIs without OpenAPI, config validation, policy-as-code), but the only non-VDBMS probes (CouchDB, Elasticsearch) are exploratory method-portability tests, not defect-detection evaluations. Both systems rejected all invalid probes with 400 errors; the only silent-accepts (`limit=0`, `size=0`) returned empty result sets, which the paper calls "graceful behavior rather than a defect." This suggests mature non-VDBMS APIs validate strictly, so the defect class may be VDBMS-specific (immature tooling, rapid development) rather than documentation-regime-general. A single non-VDBMS case study where the tool actually finds defects would strengthen the generalization claim.

2. **Novelty** — Adequate

- **2.1** **Clear delta from VDBFuzz.** VDBFuzz (vdbfuzz26) is the closest VDBMS testing work; it uses crash as its oracle via template-based input mutation. TestVDB's novelty is well-differentiated: it targets silent-accept defects (non-crashing), uses an LLM-derived oracle for natural-language documentation semantics, and introduces source-grounded falsification. The bidirectional probe (RQ3, §6.3) concretely demonstrates complementarity: TestVDB reaches VDBFuzz's integer-overflow crash by contract reasoning (size=2^63 is documented-valid yet panics), while VDBFuzz misses TestVDB's #9045 (wait=false accepts zero-length vector) under current templates. This is a strong bidirectional reachability result that shows neither approach subsumes the other.

- **2.2** **Well-positioned against REST-API oracle tools.** The paper's characterization of MASTOR (mastor26), SATORI (satori25), and AGORA+ (agoraplus25) in §7.2 and Table 1 is structurally sound on first principles:
- MASTOR reads source to encode *implemented* behavior → by construction cannot detect documentation-implementation gaps (it would encode the implementation as oracle, missing the violation)
- SATORI reads OpenAPI schema fields (type, format, min, max) → VDBMS documentation carries these constraints in prose without schema fields, so SATORI's extraction has no input
- AGORA+ infers from traffic → limited to exercised inputs; novel boundary probes (e.g., nprobe=0) don't appear in typical traffic

The paper's claim that TestVDB "reads source as a falsifier of documentation-derived claims and targets exactly that gap" is a genuine delta over MASTOR's "source-as-oracle" approach. The three-check design (independent reproducibility, evidence sufficiency, falsifiability) is novel relative to the REST-oracle line.

- **2.3 [minor, fixable]** **Limited coverage of LLM-as-oracle prior work.** §7.3 cites self-preference bias (panickssery24, wataoka24), hallucination (ji23hall), and intra-judge inconsistency (haldar25), but misses several highly relevant works on LLM-as-judge reliability that strengthen the problem framing:
- **Liu et al., "LLM-as-a-Judge" (various venues, 2023-2024):** Established the self-preference bias the paper builds on; more precise citation would strengthen motivation.
- **Zheng et al., "Large Language Models as Judges for Evaluating Alignment" (ICLR 2024):** Shows LLM judges correlate poorly with human judges on nuanced semantic tasks, which directly motivates the dev-reviewer's source-grounding.
- **LLM-as-judge calibration work (e.g., "Judging LLM-as-a-Judge," various 2024 workshops):** Shows that LLM judges are high-variance and benefit from external grounding, which aligns with the dev-reviewer design.
These are not missing per se (the paper cites the core phenomenon), but more precise citation of the LLM-as-judge reliability literature would strengthen the problem motivation. The current citations (panickssery24, wataoka24, haldar25) are sufficient but not maximally authoritative.

- **2.4** **Clear delta from documentation-derived oracle line.** §7.4 cites Toradocu (toradocu16), Doc2OracLL (doc2oracll25), AugmenTest (augmentest25), ChatAssert (chatassert24), and Testora (testora26). TestVDB's novelty is well-differentiated:
- Toradocu uses deterministic NLP for Javadoc @throws → handles simple patterns but acknowledges false positives without correction
- AugmenTest/ChatAssert verify via runtime behavior (compilation, differential execution) → still treat LLM as final semantic arbiter
- Testora uses PR descriptions as regression oracle → 55% precision even with multi-question classifier
TestVDB differs by using *implementation source* (not runtime behavior) as independent verification, breaking self-preference. The dev-reviewer's falsifier semantics (survives all three checks → defect; fails any → suppress) is a clear contribution over "LLM + runtime feedback" approaches.

3. **Soundness** — Adequate

- **3.1** **RQ1 evaluation sound.** The 107-submission yield with 49 maintainer-acknowledged true positives (68.1% precision on adjudicated set; 45.8% worst-case bound treating all pending as false positives) is reasonable. The paper correctly reports both the adjudicated-only precision (68.1%) and a conservative worst-case bound (45.8%), acknowledging uncertainty around the 35 still-pending submissions. The 15 merged-PR fixes are strong evidence that findings are real.

- **3.2** **RQ2 evaluation generally sound but with notable limitations.** The 48-candidate retrospective (27 TP, 21 by-design/rejected) is a reasonable controlled dataset. The dev-reviewer's headline 67% precision / 74% recall (3-run union) is meaningfully above the single-LLM baseline (56%/37%). The ablation (Table 4) on 12-FP/4-TP control shows source grounding suppresses 75% of false positives while retaining all TPs, and the source-disabled collapse (74% → 19% recall) triangulates source grounding's contribution. These controls are adequate to support the claim that source grounding lifts recall above baseline.

- **3.3 [major, fixable]** **Single-backbone evaluation limits generalizability.** All dev-reviewer results use GLM-5.2. The cross-model re-run (DeepSeek, Qwen-3.8-Max, LongCat-2.0) shows verdict is family-specific (κ = 0.14–0.51 vs. GLM single-run), and all three families recall fewer defects (18–56% vs. GLM's 85% single-run, though the paper reports 74% for 3-run union). This is a significant limitation: the headline precision/recall numbers are GLM-5.2-specific, not properties of the dev-reviewer design itself. The paper acknowledges this ("we cannot claim cross-family robustness") but does not quantify how much variance is due to architecture vs. sampling. A sensitivity analysis showing precision/recall variance across (say) 5 families would clarify whether the dev-reviewer reliably improves over single-LLM regardless of backbone, or whether GLM-5.2 is uniquely good at this task. As stated, the 67%/74% headline may mislead readers into thinking these are properties of the method rather than of GLM-5.2.

- **3.4 [major, fixable]** **Post-hoc operating point selection without pre-registration.** The paper reports four operating points (single run, 3-run union, 5-run union, 5-run majority) and selects the 3-run union as the headline because it "sits at the knee of the precision-recall trade-off." This selection is post-hoc, and the Wilson CIs reported ([49%, 81%] for precision, [55%, 87%] for recall) do not account for selection across the four operating points. The paper acknowledges this ("the Wilson CIs... do not account for this selection") and provides a Bonferroni correction that widens CIs to roughly [44%, 84%] and [51%, 89%], plus a bootstrap validation (2000 resamples, 2000 candidates) giving [53%, 83%] and [71%, 96%]. These corrective analyses are commendable but feel patched-on. A stronger design would pre-register the operating-point selection rule (e.g., "we will use any-confirmed ensemble as the operating point because falsifier semantics imply under-confirmation is costlier than forwarding false positives") and report CIs that do not require post-hoc correction. The current analysis is adequate but not ideal.

- **3.5 [minor, fixable]** **Per-vendor analysis shallow.** The paper reports per-vendor yield (Table 3: Milvus 22 TP / 51 submitted, Weaviate 13/30, Qdrant 14/26) and per-vendor retrospective performance (Milvus 69%/73%/80% accuracy/precision/recall; Qdrant 56%/50%/57%), but does not analyze *why* performance differs. Milvus's lower precision (73% vs 80% overall) and higher recall (80% vs 74%) may reflect documentation style (Milvus concentrates defects in optional-default parameters where documentation omits explicit bounds). A deeper per-vendor analysis linking documentation style to dev-reviewer performance would strengthen understanding of when the approach works best.

- **3.6 [minor, fixable]** **Limited analysis of remaining false positives.** On the 48-candidate retrospective, the dev-reviewer still produces ~16% false positives (8 of 48, assuming 67% precision on 27 TP → ~40 total confirmed, meaning ~8 false positives escaped suppression). The paper does not characterize these remaining FPs: are they hallucination failures? Source-grounding failures? Threat-model coverage gaps? Understanding the residual FP mode would clarify the method's boundaries.

4. **Verifiability** — Adequate

- **4.1** **Sufficient method description.** §4 (TestVDB Approach) describes the four-stage pipeline in sufficient detail to understand the method: claim extraction (contract-formalizer agent reads docs, emits JSON claims), test generation (attack agents generate probes), sandboxed execution (Docker-pinned instances), defect confirmation (judge compares documented expectation vs. actual response). The dev-reviewer's three-check design (Figure 4) is clearly explained. Reproduction would require access to the agent prompts and target versions, which the paper states are in the artifact to be released.

- **4.2 [minor, fixable]** **Limited artifact availability at review time.** The paper states "artifact... we will release at a persistent URL upon acceptance," which means reviewers cannot verify the implementation now. The LLM prompts, per-token accounting, and target versions are described in text but not provided in the paper. For full verifiability, the artifact (or at minimum: representative prompts, the 20 agent role definitions, and a reproduction script for the 48-candidate retrospective) should be available during review. The paper's claim of "~10^4 LLM calls, ~$10 per target" is credible but not verifiable without artifact access.

- **4.3** **Sufficient evaluation reporting.** RQ1 (Table 3), RQ2 (Tables 4–6, Figure 6), and RQ3 (Table 7) report sufficient statistics to follow the analysis. The Wilson CIs, bootstrap validation, and Bonferroni correction are appropriate statistical rigor. The per-vendor breakdowns and threat-model anchor analysis are adequate to trace the results.

- **4.4 [minor, fixable]** **Incomplete ground-truth reporting.** The paper reports 27 TP / 21 by-design-rejected on the 48-candidate retrospective, but does not list which specific issues are in each category. Without this list, a reviewer cannot verify the precision/recall calculation or identify patterns in the remaining FPs/FNs. Providing the 48-issue IDs with ground-truth labels in an appendix would strengthen verifiability.

5. **Presentation** — Weak

- **5.1** **Generally clear structure.** The paper follows a logical flow: motivation → problem setup → method → false-positive analysis → dev-reviewer → evaluation → related work → discussion. The four-stage pipeline (Figure 1) and dev-reviewer three-check design (Figure 4) are visually clear. Table 1 (oracle exclusion argument) is effective.

- **5.2 [minor, fixable]** **Dense writing in key sections.** §6 (Evaluation) packs many results into limited space. The RQ2 subsection in particular toggles between the 48-candidate retrospective, the 12-FP/4-TP ablation, the source-disabled collapse, the cross-model re-run, per-vendor analysis, and multi-perspective comparison without clear visual signposting. A table or figure summarizing the relationship between these different analyses (which is main result vs. which is control) would help readers navigate.

- **5.3 [minor, fixable]** **Inconsistent notation.** The paper uses Wilson CIs in some places (Table 6) and bootstrap CIs in others (Table 6 text, §6.2). The relationship between these is explained but could be clearer. Figure 6's "per-run band" for single-run results (15–78% recall) is not defined — does it show min-max across 5 runs? A figure caption or footnote would clarify.

- **5.4 [minor, fixable]** **Missing definitions.** §6.2 introduces "any-confirmed ensemble" and "majority voting" without defining them precisely. From context, any-confirmed = union across runs (candidate confirmed if any run confirms it), majority = candidate confirmed if ≥3 of 5 runs confirm it. A formal definition would avoid ambiguity.

- **5.5 [minor, fixable]** **Typos and minor issues.**
- Abstract: "future work" phrasing is vague ("cross-family generalization is an open question" is stated without framing what work remains)
- Table 6: Wilson CI brackets are inconsistent with text (text reports [55, 87] for recall, table shows [55, 87] — these match, but precision shows [49, 81] in table vs. [49, 81] in text; redundant check needed)
- §6.3: "Each direction is n=1" appears twice; consolidate
- Figure 6 caption: Could explicitly state that the 3-run union is the headline operating point

### Questions

- **Q1 (relates to 3.3):** What is the minimum cross-family performance required to claim the dev-reviewer's benefits are backbone-independent? If GLM-5.2 achieves 67%/74% and DeepSeek achieves 18%/56%, is the dev-reviewer design robust or backbone-specific? A sensitivity analysis across more families would clarify.

- **Q2 (relates to 3.4):** If the 3-run union were pre-registered as the operating point (justified by falsifier semantics: "under-confirmation is costlier than forwarding false positives for human triage"), would the Bonferroni correction be unnecessary? Can you reformulate the operating-point selection as a pre-registered rule rather than a post-hoc choice?

- **Q3 (relates to 2.3):** Can you cite the most authoritative LLM-as-judge reliability papers (e.g., Zheng et al. ICLR 2024) to strengthen the problem motivation? The current citations are sufficient but not maximally precise.

- **Q4 (relates to 3.6):** Can you characterize the ~8 remaining false positives (out of 48 candidates) that the dev-reviewer fails to suppress? Which of the three checks (reproducibility, evidence sufficiency, falsifiability) failed for each? This would clarify the residual failure modes.

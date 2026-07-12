# Peer Review (Round 13) — TestVDB

**Paper:** TestVDB: Detecting API Compliance Defects in Vector Database Systems via Contract-Truth Separation
**Venue:** acm-sigconf (targeting VLDB/PVLDB)
**Date:** 2026-07-12 (Round 13 re-review, post Rounds 11–13 revisions)
**Paper type:** technical
**Reviewers:** 3 independent (Domain Expert / Area Specialist / General Reviewer), each independently drafted. Drafts verified by the orchestrator against the paper text (substance cross-checked; sub-agent section/table renumbering noted in the Meta-Review).

---

## Reviewer 1: Domain Expert

**Overall Recommendation:** Accept

### Summary

TestVDB targets API compliance defects in Vector Database Management Systems (VDBMSs) — bugs where a system silently accepts inputs or behaviors that violate its documented contract. The paper observes that current VDBMS testing focuses on crash/hang bugs (23.1% of defects) while incorrect behavior dominates (43.0%), and VDBFuzz (the first dedicated VDBMS fuzzer) uses only crash oracles. TestVDB introduces an LLM-driven approach with Contract-Truth Separation (CTS): an assertion layer (LLM-generated contracts and four-judge debate) is falsified by a truth layer (dev-reviewer agent) that applies maintainer-authority evidence along three anchors (clean reproduction, source-grounded verification, threat-model cross-check). The core insight is contract hallucination propagation: when one LLM family both generates a contract and judges compliance, hallucinated constraints are self-confirmed (25% of adjudicated submissions were by-design). TestVDB produced 111 submissions across five VDBMSs; 52 were adjudicated (36 acknowledged, 12 by-design, 4 rejected), yielding 69.2% aggregate precision [43.9%, 80.5%] with pending-resolution sensitivity. A controlled retrospective over the same 52 candidates shows the dev-reviewer's source anchor lifts false-positive suppression from 31% to 81% while retaining 96.7% of true positives.

### Core Strengths

- **S1:** Contract hallucination propagation is a genuine, well-documented phenomenon (§5) — 12 by-design cases (25% of adjudicated submissions) with source-grounded counter-evidence, plus a contract counterfactual via DeepSeek reproducing over-strict constraints in 2/3 clean cases — see §2.1, 2.2.
- **S2:** CTS design principle and source-grounded verification are solid — the controlled retrospective (31%→81% FP suppression, 96.7% TP retention, n=30) is a clean head-to-head comparison on the same population — see §4.1.
- **S3:** Model-free invariant oracles (COSINE>1.0, incomplete index results, payload filter missing field) are the paper's most defensible technical finding — no LLM judgment required, reproduces across vendors, violates hard mathematical bounds — see §3.2, 4.1.
- **S4:** The paper honestly scopes its contribution — boundary/validation compliance (75% of yield), not crash or soft result-correctness; cross-system generalization claimed only for Milvus and Qdrant with breadth probes on three others — see §1, 2.3.

### Core Weaknesses

- **W1:** Single-layer counterfactual fairness is questionable — the 27/27 "all live-confirmed FP" re-probe milvus v2.6.19 vs. the 36/52 TestVDB baseline mixes different ground truths (live reproduction + source grounding vs. maintainer adjudication) — see §4.1.
- **W2:** Cross-system generalization evidence is weak — Weaviate (30 submissions, 3 fixed), MeiliSearch (3), and Chroma (1) contribute near-zero adjudicated signal; the paper claims only Milvus/Qdrant generalization but the abstract omits this crucial qualification — see §2.3.
- **W3:** Threat-model anchor validation is thin — n=12 Milvus FPs only, threat-alone unstable across runs, over-fires on state/concurrency FPs; treated as "noisy complement" rather than a validated contribution — see §4.4.

### Detailed Assessment

1. **Significance** — Excellent
   - **1.1** The problem is real and motivated: API compliance defects are 43% of VDBMS bugs (roadmap25), crash-only fuzzing (VDBFuzz) cannot detect them, and no reference semantics exist for differential testing. The paper fills a clear gap on the VDBMS testing roadmap (§1).
   - **1.2** The contribution has practical impact: 36 maintainer acknowledgments (28 fixed) on Milvus and Qdrant, with adjudicated precision 69.2% [43.9%, 80.5%]. The model-free invariant subclass (COSINE>1.0, incomplete results) is particularly strong — reproduces across vendors and depends on no LLM judgment (§3.2).
   - **1.3** The scope is well-bounded and honest: boundary/validation compliance (75% of yield), not crash or soft result-correctness. Complementarity with VDBFuzz is properly framed — different oracle definitions, not competing approaches (§1, §6).

2. **Novelty** — Excellent
   - **2.1** Contract hallucination propagation is a new phenomenon in LLM-driven testing: 12 by-design cases (25%) where the LLM-derived contract was stricter than maintainer intent, confirmed by source-grounded verification and mitigated by CTS (§5). A contract counterfactual (DeepSeek on same doc passages) reproduces the over-strict constraints in 2/3 clean cases, showing the over-formalization is largely task-intrinsic rather than GLM-specific (§5, §7.4).
   - **2.2** CTS design principle and dev-reviewer realization are novel: separating LLM assertion from maintainer-authority truth, with source-grounded verification as the primary anchor. The controlled retrospective (31%→81% FP suppression, 96.7% TP retention) is a clean validation of the source anchor's contribution (§4.1).
   - **2.3** Model-free invariant oracles are a new subclass: COSINE distance >1.0 for identical vectors, incomplete index results (2/25 matching points returned), payload filter returning points with missing field — these violate expressible mathematical invariants, need no LLM judgment, and reproduce across vendors (§3.2).
   - **2.4** Positioning against prior work is clear: VDBFuzz (crash oracle only), RESTler/EvoMaster (schema-conformance at API boundary), Schemathesis (requires OpenAPI spec, which VDBMSs do not serve), NoREC/TLP/DQE (assume reference SQL semantics absent in VDBMSs) — all correctly characterized (§6).

3. **Soundness** — Adequate
   - **3.1** Controlled retrospective is strong: re-triaged all 52 adjudicated candidates under two blind conditions (claim-only vs. source-grounded) on the same population. Source-grounding lifts FP suppression from 31% to 81% while retaining 96.7% of TPs (n=30). This is a clean head-to-head comparison (§4.1).
   - **3.2 [major, fixable]** Single-layer counterfactual mixes ground truths: the 45.6% single-layer precision (36/(36+16+27)) combines maintainer-adjudicated baseline (36/52) with 27 live-re-probed, source-grounded FPs — different validation methods. The paper treats the same-population 31%→81% result as cleaner, but the 45.6% figure appears prominently in abstract/§4.1. This could be fixed by reporting single-layer precision under the same ground truth (maintainer adjudication only).
   - **3.3** Three-anchor ablation is honest but thin: source-alone (9/12=75%), threat-alone (6/12=50%, unstable), union (11/12=92%) on Milvus FPs only (n=12). Paper treats threat-model as "noisy complement" rather than a validated contribution, which is appropriate given the instability and small n. TP retention is 4/4 across all conditions (§4.4).
   - **3.4 [minor, fixable]** Baseline comparisons are asymmetric: single-LLM (25.5%, LLM-judged), single-LLM+source (16.7%), schema fuzzer (37% probe→accept rate, not candidate precision), single-layer 4-judge (75%, retrospective), TestVDB source-grounded (91%, retrospective), TestVDB end-to-end (69.2%, maintainer adjudication) — all judged under different ground truths. Table 3 makes this explicit rather than disguising it, which is good, but the asymmetry limits comparability (§4.1).
   - **3.5** Threats to validity are thorough: internal (maintainer acknowledgment is weak ground truth), selection (submission-selection bias not instrumented), external (ablation is Milvus-plus-Qdrant only, Weaviate undiagnosed), construct (defect-type classification is title-based), LLM variance (99.1% agreement on re-adjudication), contamination (memorization canary: 0/9 held-out bugs recalled), recall scope (96.7% is judgment-layer TP retention, not end-to-end discovery recall), excluded-set (29 excluded may hide FP tail), single-layer counterfactual (bounded to one feedback cycle) — all addressed (§7).

4. **Verifiability** — Excellent
   - **4.1** Paper provides complete implementation details: 20 agents (4 high-budget, 16 low-budget) served by GLM-5.2, target versions pinned (Milvus 2.6.19 for ablations), full prompts in artifact, 111 submissions with maintainer outcomes. Cost accounting: ~10^4 LLM calls total (~10^7 tokens), per target ~10^3 calls (~2×10^6 tokens), completes in few hours (§2).
   - **4.2** Artifact is declared and reachable: anonymized artifact at https://anonymous.4open.science/r/testvdb-anon-D644/, to be made public on acceptance. Includes full version matrix, per-token/wall-clock accounting, all prompts, reproducible dataset spanning 5 VDBMSs and 111 submissions (§2).
   - **4.3** Controlled retrospective is reproducible: re-triaged all 52 adjudicated candidates under two blind conditions with label-isolated agents. Same-population comparison (31%→81% FP suppression, 96.7% TP retention) is fully specified and could be replicated (§4.1).
   - **4.4** Model-free invariants are independently verifiable: COSINE>1.0 reproduces on both Milvus and Qdrant; incomplete index results (2/25 matching points); payload filter missing field — all depend on no LLM judgment, just live reproduction and mathematical bounds (§3.2).

5. **Presentation** — Adequate
   - **5.1** Structure is logical and complete: intro → background → approach → contract hallucination → evaluation (RQ1-4) → related work → conclusion. Flow is clear. Figures (especially Figure 1 pipeline) are well-designed (§1-7).
   - **5.2 [minor, fixable]** Writing has minor issues: some sentences are long and convoluted (e.g., §4.1 baseline comparison paragraph), a few typos/awkward phrasings (e.g., "the 111-submission study plus three ablation batches constitutes the full LLM-call budget" — should be "constitute"). Overall readable but would benefit from copy-editing.
   - **5.3** Tables are clear: Table 1 (yield by VDBMS) with adjudication breakdown, Table 2 (scope projection onto taxonomy), Table 3 (baseline comparison with ground-truth asymmetry explicit). All properly captioned and referenced.
   - **5.4 [minor, fixable]** Some notation inconsistencies: "nprobe=0" vs. "nprobe=0", "milvus-io/milvus #47729" vs. "#47729", occasional spacing issues in math (e.g., "$n{=}$30" vs. "$n=30$"). Minor but should be fixed.
   - **5.5** Abstract is complete but dense: packs problem, approach, results, positioning, contributions, and limitations into 6 sentences. Accurate but could be split for readability.

### Questions for Authors

- **Q1:** The single-layer counterfactual precision of 45.6% (36/(36+16+27)) combines maintainer-adjudicated baseline (36/52) with 27 live-re-probed, source-grounded FPs under different validation methods. Could you report single-layer precision under the same ground truth (maintainer adjudication only) to make the comparison cleaner? This would clarify the magnitude of the precision lift.
- **Q2:** The abstract states "TestVDB produced 111 issues across five VDBMSs" without clarifying that adjudicated signal concentrates on Milvus and Qdrant (36 of 52 adjudicated), while Weaviate/MeiliSearch/Chroma contribute near-zero adjudicated yield. Consider adding "(with adjudicated validation on Milvus and Qdrant)" to make the cross-system generalization claim more precise.
- **Q3:** The threat-model anchor is validated on n=12 Milvus FPs only and shows instability across runs (threat-alone 6/12, one boundary FP flipped between runs). Do you plan to extend this validation to non-Milvus systems or increase the sample size? The "noisy complement" characterization is honest, but more evidence would strengthen the three-anchor design claim.
- **Q4:** Could you provide more detail on the schema-fuzzer baseline? The 37% figure is a probe→accept rate (7 of 19 probes surfaced API-accepted candidates), not a candidate precision comparable to other arms. Were the 7 candidates independently adjudicated by maintainers, or classified via source-grounding only? This would clarify the comparability.
- **Q5:** The memorization canary test (0/9 held-out bugs recalled) is excellent. Did you test whether the source anchor's power is inflated by GLM-5.2's pre-2024 training data including Milvus GitHub source? The contamination threat (§7) mentions this but doesn't report the audit results explicitly.

---

## Reviewer 2: Area Specialist

**Overall Recommendation:** Weak Accept

### Summary

TestVDB introduces Contract-Truth Separation (CTS) to detect API compliance defects in Vector Database Management Systems (VDBMSs), targeting the 43% of VDBMS bugs that are incorrect-behavior defects (accepting invalid inputs or violating documented contracts) rather than crashes. The approach uses LLM agents to extract contracts from API documentation and generate attack candidates, then introduces a dev-reviewer agent that falsifies LLM-generated assertions through three counter-evidence anchors: clean reproduction, source-grounded verification (the primary anchor), and threat-model cross-check. The authors report 111 submissions across five VDBMSs (Milvus, Qdrant, Weaviate, MeiliSearch, Chroma), with maintainer adjudication on 52 (36 acknowledged, 12 by-design, 4 rejected), yielding 69.2% adjudicated precision. A controlled retrospective over all 52 adjudicated candidates demonstrates that source-grounding lifts false-positive suppression from 31% to 81% while retaining 96.7% of true positives. The paper also identifies "contract hallucination propagation" — when one LLM family both generates a contract and judges compliance, hallucinated constraints are self-confirmed — and presents two counterfactuals: a memorization canary (0/9 held-out bugs recalled by GLM-5.2) and a contract counterfactual (DeepSeek reproduces 2/3 over-strict constraints). The work complements VDBFuzz's crash-oracle approach by extending detection into the API compliance domain.

### Core Strengths

- **S1:** Novel and well-motivated problem formulation — API compliance defects fill a real gap in VDBMS testing (43% of bugs lack oracles), with a principled scope boundary that excludes crash bugs by design and acknowledges result-correctness oracles as open — see §2.3, §2.4, §7.
- **S2:** Contract hallucination propagation is a genuine and well-characterized new failure mode in LLM-driven testing — the 25% by-design rate (12/48 adjudicated submissions) and the source-grounded mitigation (31%→81% FP suppression) are solid empirical evidence — see §5, §5.6, §5.7.
- **S3:** Rigorous controlled retrospective design — same-population ablation (52 candidates, blind conditions) isolates the dev-reviewer's contribution cleanly, and the single-layer counterfactual (27/27 live-re-probed FPs) bounds the alternative without LLM-proxy judgment — see §5.6.
- **S4:** Honest limitations and scope declarations — paper explicitly states precision is validated only for Milvus/Qdrant, treats Weaviate/MeiliSearch/Chroma as breadth probes, acknowledges pending-resolution sensitivity [43.9%, 80.5%], and flags threat-model anchor as unvalidated with n=12 — see §5.1, §5.6, §5.7, §6.
- **S5:** Model-free invariant subclass is the paper's most defensible technical finding — COSINE>1.0, incomplete index results, and missing-field payload filters violate hard mathematical bounds, reproduce across vendors, and depend on no LLM judgment — see §5.5.

### Core Weaknesses

- **W1:** Three-anchor ablation methodology is weak (n=12, instability across runs) and the "both" condition is a union of independent verdicts rather than a joint dispatch, undermining the claimed three-anchor design as a validated contribution — see §5.7, 5.7's source-alone 9/12 (75%) vs threat-alone 6/12 (50%, unstable) vs union 11/12 (92%).
- **W2:** Cross-system generalization is claimed primarily for Milvus and Qdrant only; Weaviate (30 submissions, 3 fixed), MeiliSearch (3 submissions, 0 fixed), and Chroma (1 submission, 0 fixed) contribute near-zero adjudicated signal, so the "five VDBMSs" framing overstretches the evidence — see §5.1, Table 2.
- **W3:** Single-layer counterfactual has limited inferential scope — 27/27 is pre-filtered judgment on the dev-reviewer's killed candidates, not end-to-end generation, so the 45.6% single-layer precision figure combines heterogeneous ground truths (maintainer adjudication + live reproduction) and is bounded to one feedback cycle — see §5.6.
- **W4:** By-design rate (25%) is an observation from 12 adjudicated cases, not a measured prevalence over all inputs — paper is appropriately cautious but the "quarter of submissions" phrasing in the abstract risks overstating generalizability — see §5, abstract.

### Detailed Assessment

#### 1. Significance — Adequate

- **1.1** The problem is significant and under-addressed: API compliance defects (43% of VDBMS bugs) have no practical oracle, and VDBFuzz's crash-only approach leaves this majority uncovered. TestVDB's contract-oracle direction is a principled advance on the roadmap agenda — see §1, §2.4, §7.

- **1.2 [minor, unfixable]** Cross-system generalization is limited: Milvus (51 submissions) and Qdrant (26) dominate the yield with 36 acknowledged true positives; Weaviate (30 submissions, 3 fixed), MeiliSearch (3, 0), Chroma (1, 0) contribute minimal adjudicated signal. The "five VDBMSs" framing in the title/abstract suggests broader validation than the data supports. This is a scope limitation inherent in the maintainer triage base, not a fixable flaw, but the paper should foreground Milvus/Qdrant as the validated systems and treat others as exploratory probes — see §5.1, Table 2.

- **1.3** The result-correctness boundary is declared honestly: paper excludes soft ANN recall/ranking oracles (the hard open problem from roadmap25) and limits result-correctness to expressible invariants (COSINE bounds, completeness). This is appropriate scoping — see §5.2, §7.

#### 2. Novelty — Excellent

- **2.1** Contract hallucination propagation is a genuine new failure mode: the observation that one LLM family both generating a contract and judging confirmation creates self-confirming hallucinations is novel to my knowledge. The 12 by-design cases (25% of 48 adjudicated submissions) and the source-grounded mitigation are strong empirical grounding. This is not incremental — it identifies a fundamental reliability risk in LLM-as-judge patterns — see §5, §5.6.

- **2.2** CTS (Contract-Truth Separation) and the dev-reviewer's source-grounded anchor are a novel mitigation: separating the assertion layer (LLM contracts/judgments) from a truth layer (maintainer-authority proxies) and falsifying via source code is not, to my knowledge, instantiated in prior LLM-driven testing work. The 31%→81% FP-suppression lift with 96.7% TP retention validates this as more than theoretical — see §5.6, §5.7.

- **2.3 [minor, fixable]** Single-LLM baseline (25.5% LLM-judged precision) is not directly comparable to TestVDB's 69.2% maintainer-adjudicated figure because they use different ground truths. Table 4 makes the asymmetry explicit, which is good practice, but the narrative should emphasize that the clean head-to-head is the same-population 31%→81% retrospective ablation, not the end-to-end single-layer figure — see §5.6, Table 4.

#### 3. Soundness — Adequate

- **3.1** Controlled retrospective design is rigorous: same-population ablation (52 candidates, blind conditions, label-isolated agents) isolates the dev-reviewer's contribution cleanly. The 31%→81% FP-suppression lift with 96.7% TP retention is a strong, internally valid result — see §5.6.

- **3.2** Single-layer counterfactual (27/27 live-re-probed FPs) is methodologically sound: re-probing on a fresh Milvus v2.6.19 container and source-grounding via constants plus response codes avoids LLM-proxy judgment and bounds the single-layer arm's FP inflow. The 45.6% single-layer precision figure is directional rather than a strict baseline, which is appropriately qualified — see §5.6.

- **3.3 [major, fixable]** Three-anchor ablation is weak: the threat-model anchor evaluation (n=12, source-alone 9/12=75%, threat-alone 6/12=50% with instability across runs, union 11/12=92%) has three problems. (1) Sample size is small (12 Milvus FPs only). (2) The "both" condition is a union of independent verdicts (source OR threat passes), not a joint dispatch where both anchors must agree, so the "three-anchor design" framing is misleading. (3) Threat-alone instability (one boundary FP flipped between runs) suggests the anchor is noisy. Paper is honest about these limitations ("we do not claim the three-anchor design as a clean validated contribution") but the abstract/contributions list should soften the three-anchor claim to "source anchor validated, threat-model anchor exploratory" — see §5.7, contributions point 2.

- **3.4 [minor, fixable]** Memorization canary (0/9 held-out bugs recalled) is a sound negative result but with narrow scope: GLM-5.2's failure to recall specific issues does not rule out contamination in the source anchor's apparent power (it could know general patterns rather than specific bugs). The paper acknowledges this ("discovery recall on the 9-bug cohort is therefore not memorization-confounded") but should clarify that the canary bounds direct memorization, not pattern-level contamination — see §6.

- **3.5** Contract counterfactual (DeepSeek reproduces 2/3 over-strict constraints) supports task-intrinsic over-formalization but is observational (n=3 clean cases), not a prevalence study. Paper is appropriately cautious ("indicating the over-formalization is largely task-intrinsic rather than GLM-specific") — see §5.5, §6.

#### 4. Verifiability — Excellent

- **4.1** The paper provides sufficient procedural detail: all agent prompts, the threat-model artifact structure, and the dev-reviewer's three-anchor pipeline are described in enough detail to follow the logic. Artifact repository (anonymous 4open) is declared and reachable — see §3, §3.3, §3.5.

- **4.2** Experimental transparency is strong: Table 2 breaks down submission outcomes by system; §5.6 reports the same-population ablation design with explicit ground-truth asymmetry; §6 enumerates threats to validity including LLM variance (99.1% pairwise agreement on 46 candidates), selection bias, and construct limitations — see §5, §6.

- **4.3** Baseline comparisons are fair: Table 4 makes ground-truth asymmetry explicit; the schema-fuzzer baseline (71% source-grounded precision on boundary subset) is a genuine complementarity test, conceding that spec-driven fuzzing is effective on the 75% boundary/validation majority — see §5.6, Table 4.

#### 5. Presentation — Excellent

- **5.1** Structure is logical and complete: Introduction motivates the problem (43% incorrect-behavior bugs, no oracle), identifies the LLM-as-judge self-confirmation risk, proposes CTS, and honestly scopes contributions. Background formulates the problem. Approach details the pipeline. Evaluation addresses RQ1-RQ4 with case studies, controlled retrospective, baselines, and ablations. Related Work is thorough. Conclusion and Future Work are appropriate — see overall structure.

- **5.2** Figures and tables are clear: Figure 1 illustrates the assertion/truth layer separation effectively; Table 1 (oracle candidates exclusion) cleanly motivates why LLM is the only candidate; Table 2 (submission outcomes) is transparent; Table 4 (baseline comparison) makes ground-truth asymmetry explicit — see §1, §2.4, §5.6.

- **5.3** Writing is readable with minor issues: The abstract is dense but clear. Some sentences are long (e.g., contributions point 2 spans 5 lines), and the "threat-model anchor was designed to be injected... however... its effect could not be isolated" phrasing in §3.2 is slightly awkward but not ambiguous. No pervasive language errors — see throughout.

### Questions for Authors

- **Q1:** The three-anchor ablation (§5.7) uses a "union of the two independent verdicts" for the "both" condition — meaning a candidate is suppressed if EITHER source OR threat provides counter-evidence. This seems to treat the threat-model anchor as a backup, not a joint verification layer. Was a joint dispatch (both anchors must agree) considered? If so, what was the rationale for union over joint? If not, would the contributions statement be clearer as "source anchor validated, threat-model anchor exploratory complement"? — see §5.7, contributions point 2.

- **Q2:** The single-layer counterfactual reports 27/27 suppressed candidates as live-confirmed FPs. Given that maintainer triage might reclassify some of these differently (e.g., a silent-default case that looks like FP on live repro but is actually by-design), how sensitive is the 45.6% single-layer precision figure to reclassification? Would a "with 1-standard-error reclassification" sensitivity analysis strengthen the claim? — see §5.6.

- **Q3:** The cross-system generalization is validated for Milvus and Qdrant (36 acknowledged TPs) but not for Weaviate/MeiliSearch/Chroma (3/0/0 fixed). Is the low yield on Weaviate/MeiliSearch/Chroma due to (a) maintainer triage bias (less responsive), (b) genuine differences in API compliance surface, or (c) TestVDB's Milvus/Qdrant focus in contract extraction? Acknowledging this in §5.1 (e.g., "Weaviate/MeiliSearch/Chroma had minimal maintainer adjudication; their low yield may reflect triage patterns rather than defect prevalence") would make the scope clearer — see §5.1, Table 2.

---

## Reviewer 3: General Reviewer

**Overall Recommendation:** Weak Accept

### Summary

The paper introduces TestVDB, an LLM-driven system for detecting API compliance defects in Vector Database Management Systems (VDBMSs). Compliance defects are behaviors where a VDBMS silently accepts inputs or produces outputs that violate its documented API contract but do not cause crashes. The authors argue that these defects constitute 43% of VDBMS bugs but lack practical test oracles, unlike crash bugs detectable by existing fuzzers like VDBFuzz. TestVDB addresses this through Contract-Truth Separation (CTS): a design that separates LLM-generated contract assertions from a truth layer that falsifies them via maintainer-authority evidence (source code, issue history, by-design intent). The system produced 111 submissions across five VDBMSs; maintainers adjudicated 52, acknowledging 36 (28 fixed), with 12 marked by-design and 4 rejected. A controlled retrospective over the adjudicated set shows that the dev-reviewer's source anchor lifts false-positive suppression from 31% to 81% while retaining 96.7% of true positives (30/32). The authors also report a single-layer counterfactual (27/27 suppressed candidates confirmed live-confirmed FPs), a three-anchor ablation on the threat-model anchor, a memorization canary (0/9 held-out bugs recalled), and a contract counterfactual (different LLM reproduces over-strict constraints in 2/3 clean cases). The work positions itself as complementary to VDBFuzz, targeting boundary/validation compliance while leaving soft result-correctness (ANN recall, ranking) open.

### Core Strengths

- **S1:** The problem formulation is well-motivated and timely. VDBMS reliability is becoming critical as LLM applications scale, and the authors correctly identify that current testing tools (VDBFuzz) focus on a minority of bugs (crashes) while the majority (incorrect behavior) lack practical oracles — see §1 (the roadmap's open challenge), Table 1 (oracle exclusion), and the bug-study statistics (43% incorrect-behavior vs 23% crash/hang). The scope is clearly bounded in Table 2 and §2.3 (API compliance defects defined).

- **S2:** Contract hallucination propagation is a genuine phenomenon that merits attention. The observation that a single LLM family both generating the contract and judging compliance leads to self-confirmation of hallucinated constraints (25% of adjudicated submissions marked by-design, §4) is a credible failure mode, and the source-grounded verification mitigation is a sound design principle — see §4 (examples and formalization) and the RQ3 retrospective (31%→81% FP suppression, source anchor primary driver).

- **S3:** The controlled retrospective (RQ3) provides the strongest evidence. Re-triaging the same 52 adjudicated candidates under blind conditions (claim-only vs source-grounded) yields a clean head-to-head comparison on the same population, with a clear FP-suppression lift (31%→81%) and high TP retention (96.7%). The single-layer counterfactual (27/27 live-confirmed FPs) further bounds the baseline's FP inflow — see §5.3 and Table 5 (baseline comparison).

- **S4:** Model-free invariant oracles are a defensible technical contribution. The cosine-distance >1.0 violations (reproduced on both Milvus and Qdrant) and incomplete index results are hard invariants that depend on no LLM judgment, reproducing across vendors, which distinguishes this subclass from contract-driven cases — see §5.2 (RQ2 case studies) and the roadmap positioning in §1.

- **S5:** The paper is honest about limitations and scope. The scope boundary is explicit (75% boundary/validation, crash bugs excluded by design), the cross-system generalization is claimed only for Milvus and Qdrant (Weaviate/MeiliSearch/Chroma as breadth probes), and multiple threats are openly discussed (LLM contamination via memorization canary 0/9, version-pinning limits, spec-completeness gaps in §5.3's contract-coverage discussion) — see §5.5 (threats to validity) and §1's positioning paragraph.

### Core Weaknesses

- **W1:** Cross-system generalization claims are not fully supported by the evidence. The abstract states "five VDBMSs" and claims cross-system attack-surface generalization, but Table 4 shows adjudicated signal concentrates on Milvus (51 submissions) and Qdrant (26), while Weaviate (30 submissions, only 3 acknowledged), MeiliSearch (3, 0 acknowledged), and Chroma (1, 0 acknowledged) contribute near-zero yield. The paper claims generality for Milvus and Qdrant only and treats the rest as "breadth rather than statistical evidence" (§5.1), but the abstract's "five VDBMSs" framing oversells the data — see Table 4 (yield distribution) and §1's contribution claim (validated on Milvus and Qdrant).

- **W2:** The threat-model anchor is under-validated relative to its prominence in the design. Figure 1 and §3.4 present it as one of three counter-evidence anchors, but the evaluation shows it is "noisy and unstable" (§5.4): threat-alone suppresses 6/12 FPs (vs source's 9/12), over-fires on state/concurrency cases (bs-03/06 push FPs toward CONFIRMED), and is unstable across runs. The paper treats it as a "noisy complement" rather than a validated component, yet it remains architecturally prominent in the overview — see Figure 1 (three anchors shown), §3.4 (CTS design), and §5.4 (ablation results showing threat-alone 50% vs source 75%, union 92%).

- **W3:** Baseline comparison is confounded by differing ground truths. Table 6 (arms comparison) mixes precision values judged against different ground truths: Single-LLM (LLM self-judgment 25.5%), single-layer 4-judge (retrospective same-pool 75%), schema fuzzer (API-acceptance 37%, not comparable precision), TestVDB maintainer-adjudicated (69.2%). The paper acknowledges this asymmetry ("judged under different ground truths, so direct numerical comparison requires care" — §5.3), but the table layout invites direct comparison — see Table 6 (explicit asymmetry callout) and §5.3 (baseline comparison paragraph).

- **W4:** The single-LLM baseline is not fully end-to-end. §5.3 reports "single LLM driven end-to-end" producing 51 candidates with 13 LLM-judged TPs (25.5%), but the subsequent source-anchored ablation (n=12, 16.7%) and the discussion note that "the A1 27/27 figure is pre-filtered judgment on the dev-reviewer's killed candidates, not end-to-end generation, so multi-agent debate contributes substantially beyond source anchoring alone." This suggests the 51-candidate single-LLM run was not evaluated through the full maintainer-adjudication pipeline, so its precision is not comparable to TestVDB's 69.2% — see §5.3 (single-LLM baseline paragraph) and Table 6 (ground-truth column showing "LLM self-judgment" vs "maintainer adjudication").

- **W5:** Contract coverage and discovery recall are not fully characterized. The paper reports an upstream probe on 9 held-out pre-2024 compliance bugs finding current docs cover 6/9 contracts (67%), but "the bottleneck is not doc recovery but two deeper limits... spec-completeness and version-pinning" (§5.3). The cosine>1.0 case is flagged as overlapping with general mathematical knowledge rather than independent evidence due to contamination risk. A full discovery-recall study against bug-present versions is absent, leaving the question of how many pre-existing bugs TestVDB would rediscover only partially answered — see §5.3 (contract coverage paragraph) and §5.5 (LLM contamination canary 0/9).

### Detailed Assessment

1. **Significance** — Adequate

   - **1.1** The problem addressed is significant and timely. VDBMS reliability directly affects downstream LLM applications, and the authors correctly position their work on a high-impact open challenge (VDBFuzz's Future Work, the roadmap's oracle-for-correctness gap). The 43% incorrect-behavior vs 23% crash/hang statistics (§1, Table 2) establish that compliance defects are the majority subclass, and the complementarity with VDBFuzz (crash oracle vs contract oracle) is a clean division of labor — see §1 (motivation), Table 1 (oracle exclusion), and §5.2 (complementarity paragraph).

   - **1.2 [major, fixable]** Cross-system generalization claims exceed the evidence. The abstract's "five VDBMSs" and "111 submissions" framing suggests broad applicability, but Table 4 shows yield concentrates on Milvus (51 subs, 22 adjudicated) and Qdrant (26 subs, 14 adjudicated), while Weaviate (30 subs, 4 adjudicated), MeiliSearch (3 subs, 0 adjudicated), and Chroma (1 subs, 0 adjudicated) contribute near-zero signal. The paper acknowledges this ("adjudicated signal concentrated on Milvus and Qdrant" — §5.1) and claims cross-system generalization only for the attack surface, not precision, yet the abstract's phrasing ("five VDBMSs") is misleading without qualification. Fixing this requires either (a) explicit abstract qualification ("adjudicated signal concentrated on two systems") or (b) additional evaluation on Weaviate/MeiliSearch/Chroma to establish whether the low yield is method limitation or artifact — see Abstract (line 44: "five VDBMSs"), Table 4 (yield distribution), §5.1 (RQ1), and §1's contribution claim ("validated on Milvus and Qdrant").

   - **1.3 [minor, unfixable]** Scope is bounded to a tractable but incomplete slice. The paper explicitly targets boundary/validation compliance (75% of yield) and excludes crash bugs (by design), performance bugs, and soft result-correctness (ANN recall, ranking). This is a legitimate scoping choice given the oracle difficulty, but it means the work does not solve the full "incorrect-behavior" problem the roadmap flags — only the API-compliance subset where the contract serves as oracle. This limits the impact to systems with documented APIs and hard invariants; model-free cases (cosine>1.0, incomplete results) are the strongest findings precisely because they bypass LLM judgment — see Table 2 (scope projection), §1's positioning paragraph ("We do not claim to solve VDBFuzz's oracle-for-correctness direction"), and §5.5 (Conclusion).

2. **Novelty** — Adequate

   - **2.1** Contract hallucination propagation is a novel failure mode in LLM-driven testing. To my knowledge (generalist without specialized literature survey), the observation that one LLM family both generating a contract and judging compliance leads to self-confirmation of hallucinated constraints has not been characterized. The 25% by-design rate (12/48 adjudicated) and the contract counterfactual (different LLM reproduces over-strict constraints in 2/3 clean cases) provide empirical support that this is a real phenomenon, not a theoretical concern — see §4 (formalization and examples), §5.3 (contract counterfactual), and §1's motivation paragraph.

   - **2.2** Contract-Truth Separation is a principled design response to this failure mode. The idea of separating LLM-generated assertions from a truth layer that falsifies them via maintainer-authority evidence (source code, issue history, by-design intent) is a sound architectural pattern. The dev-reviewer's three anchors (clean reproduction, source-grounded verification, threat-model cross-check) mirror maintainer adjudication, and the retrospective evidence (31%→81% FP suppression, source anchor primary driver) validates the source-grounding component — see §3.4 (CTS design), §5.3 (source-anchor lift), and §5.4 (threat-model ablation).

   - **2.3 [minor, fixable]** Related Work coverage could be more explicit on delta. The paper cites REST API testing (RESTler, EvoMaster, Schemathesis), database correctness oracles (NoREC, TLP, DQE), and LLM-based testing (multi-agent verification) in §6, but does not explicitly state whether and how those tools handle compliance defects or contract-hallucination mitigation. Schemathesis is flagged as inapplicable due to missing OpenAPI specs (404 on /swagger), but the delta against other LLM-as-judge patterns (beyond "we identify a self-confirmation failure mode") could be sharper — see §6 (Related Work) and §5.3 (Schemathesis comparison blocked).

3. **Soundness** — Adequate

   - **3.1** The controlled retrospective (RQ3) provides strong evidence for the dev-reviewer's contribution. Re-triaging the same 52 adjudicated candidates under blind conditions (claim-only vs source-grounded) yields a clean head-to-head comparison on the same population, with clear FP-suppression lift (31%→81%) and high TP retention (96.7%, 29/30 reachable). This is the paper's most defensible quantitative claim because it controls for population and ground truth — see §5.3 (RQ3), Table 5 (FP suppression), and the single-layer counterfactual (27/27 live-confirmed FPs).

   - **3.2** The single-layer counterfactual bounds the baseline's FP inflow without LLM-proxy judgment. Re-probing all 27 suppressed candidates live on a fresh milvus v2.6.19 container and source-grounding each via milvus constants yields 27/27 confirmed FPs (0 over-kill), spanning five distinct classes (input-validation rejections, by-design accepts, correct rejections, oracle script bugs, state-semantics cases). This provides a strong lower bound that the single layer would submit 27 additional false positives, establishing the dev-reviewer's value — see §5.3 (single-layer counterfactual) and the end-to-end precision comparison (45.6% single-layer vs 69.2% TestVDB).

   - **3.3 [minor, fixable]** Threat-model anchor evidence is weak for its architectural prominence. Figure 1 and §3.4 present three counter-evidence anchors equally, but §5.4's ablation shows threat-alone suppresses 6/12 FPs (vs source's 9/12), is unstable across runs (one FP flipped), and over-fires on state/concurrency FPs (bs-03/06 push toward CONFIRMED). The paper treats it as a "noisy complement" rather than a validated component, yet it remains visually prominent in the design. Either (a) de-emphasize it architecturally (gray/dashed in Figure 1 as with the reproduction anchor) or (b) strengthen its validation (larger ablation, stability analysis) — see Figure 1 (three anchors), §3.4 (CTS design), §5.4 (ablation results: threat-alone 50%, source-alone 75%, union 92%).

   - **3.4 [minor, fixable]** Baseline comparison asymmetry could be clearer. Table 6 mixes precision values judged against different ground truths (LLM self-judgment, API-acceptance, retrospective same-pool, maintainer adjudication). The paper acknowledges this ("judged under different ground truths, so direct numerical comparison requires care" — §5.3), but the table layout invites direct comparison. Separating the arms by ground-truth type or adding a "ground-truth tier" column would make the asymmetry explicit — see Table 6 (baseline comparison) and §5.3 (baseline comparison paragraph).

   - **3.5 [minor, unfixable]** Maintainer acknowledgment is a weak ground truth with reviewer effects. §5.5 acknowledges this ("maintainer acknowledgment is a weak ground truth, and triage may reflect report clarity rather than defect validity (a reviewer effect)"). The 59 non-adjudicated submissions (30 pending, 29 excluded) create selection bias, and the precision sensitivity interval ([43.9%, 80.5%]) partially addresses this, but the fundamental limitation remains — see §5.5 (threats to validity) and §5.3 (sensitivity to pending submissions).

4. **Verifiability** — Adequate

   - **4.1** The paper provides sufficient procedural detail to follow the evaluation. The five-stage pipeline is described in §3 (overview, contract extraction, attack generation, four-judge debate, dev-reviewer CTS, novelty gate). Ablation methodology is explicit (blind conditions, label-isolated agents, same-population retrospective in §5.3; three-condition threat-model ablation with fixed wiring in §5.4). Threats to validity are thoroughly discussed (internal, selection, external, construct, LLM variance, contamination, recall scope, excluded-set, single-layer limitations) — see §3 (Approach), §5 (Evaluation), and §5.5 (Threats to Validity).

   - **4.2** Artifact availability is declared and reachable. §3's implementation paragraph states: "Precise per-token and wall-clock accounting is part of the anonymized artifact at https://anonymous.4open.science/r/testvdb-anon-D644/, to be made public on acceptance." The paper does not require reviewers to clone or run the artifact; declaring the link is sufficient for Verifiability under the rubric — see §3 (implementation paragraph) and the artifact URL.

   - **4.3 [minor, fixable]** Contract coverage and discovery recall are not fully instrumented. §5.3 reports an upstream probe on 9 held-out pre-2024 compliance bugs (67% doc coverage) but notes two deeper limits (spec-completeness, version-pinning) and states "Establishing full discovery recall against bug-present versions, bounded by the spec-completeness and version-pinning limits above, is future work." A full discovery-recall study (running TestVDB against bug-present old versions) would strengthen Verifiability of the recall claim, though the partial probe is better than nothing — see §5.3 (contract coverage paragraph) and §5.5 (LLM contamination canary 0/9).

   - **4.4 [minor, fixable]** Candidate-to-submission ratio is not instrumented. §5.5 notes "the 111 submissions were filtered from a larger candidate pool by the novelty gate; the pipeline generates on the order of a few hundred raw candidates per target (duplicates and known-issue re-reports dominate the filtered-out set), but the precise candidate-to-submission ratio is not instrumented, leaving submission-selection bias only roughly bounded." Adding this instrumentation would make the selection effect more precise — see §5.5 (threats to validity, selection bias).

5. **Presentation** — Adequate

   - **5.1** The paper is well-structured and readable. The narrative flow is logical: problem motivation (§1), background and scope (§2), approach (§3), contract-hallucination phenomenon (§4), evaluation (§5), related work (§6), conclusion (§7). Figures and tables are clear: Table 1 (oracle exclusion), Table 2 (scope projection), Figure 1 (pipeline architecture), Table 4 (yield distribution), Table 5 (FP suppression), Table 6 (baseline comparison). Language is generally clear with minor awkwardness — see overall structure and figures/tables.

   - **5.2 [minor, fixable]** Notation consistency could be improved. The paper uses both "acknowledged" and "true positive" interchangeably (e.g., "36 acknowledged true positives" in §5.2), and "maintainer-adjudicated precision" vs "precision" in different contexts. Standardizing terminology (e.g., always use "maintainer-adjudicated" for the 69.2% figure, "judgment-layer precision" for the 91% retrospective figure) would reduce ambiguity — see §5.2 (RQ2, defect-type distribution) and §5.3 (precision terminology).

   - **5.3 [minor, fixable]** Minor language and phrasing issues. Some sentences are awkward or could be clearer: (a) "The dev-reviewer's source anchor lifts false-positive suppression from 31% to 81% while retaining 96.7% of true positives" (abstract, line 44) could be "lifts false-positive suppression rate from 31% to 81%"; (b) "A contract counterfactual (same doc passages fed to a different LLM family) reproduces the over-strict constraints in 2/3 of clean cases" (abstract, line 44) could specify which counterfactual this refers to; (c) Some parenthetical asides are dense and could be separated — see Abstract (line 44), §1 (motivation), and §5.3 (single-layer counterfactual).

### Questions for Authors

- **Q1:** What explains the low adjudicated yield on Weaviate (30 submissions, 4 adjudicated, 3 acknowledged) compared to Milvus (51 submissions, 22 adjudicated, 14 acknowledged)? Is this method limitation (TestVDB less effective on Weaviate's API design), artifact (Weaviate maintainers less responsive to bug reports), or scope mismatch (Weaviate's compliance surface differs)? Understanding this would clarify whether cross-system generalization is attack-surface-only (as claimed) or whether precision might also generalize with more engagement. — Intended effect: If the authors provide evidence or analysis, item 1.2's rating (cross-system generalization claims exceed evidence) could move toward Adequate or even Excellent if low yield is artifact而非 method.

- **Q2:** The threat-model anchor is architecturally prominent (Figure 1, §3.4) but empirically weak (§5.4 shows it is noisy and unstable). Why retain it as a named anchor rather than treating it as an optional prior (like the threat-model artifact in §3.2, whose "blindspot indicators were never populated and its effect could not be isolated")? Would the paper be stronger if CTS were presented as a two-anchor design (source + reproduction, with threat-model as an optional extension), acknowledging that the third anchor is not validated? — Intended effect: If the authors de-emphasize the threat-model anchor architecturally (gray/dashed in Figure 1, qualified in text), item 3.3's rating (threat-model anchor evidence weak) would move toward Adequate by aligning presentation with evidence strength.

- **Q3:** The single-LLM baseline (51 candidates, 25.5% LLM-judged precision) appears not to have gone through maintainer adjudication, while TestVDB's 69.2% is maintainer-adjudicated. Can the authors clarify whether the 51 single-LLM candidates were submitted to maintainers for triage? If not, how should readers interpret the 25.5% figure relative to 69.2%? Would re-running the single-LLM pipeline through maintainer adjudication yield a different precision, and is this planned as future work? — Intended effect: If the authors clarify the evaluation status and/or plan maintainer adjudication for the single-LLM cohort, item 3.4's rating (baseline comparison asymmetry) would move toward Adequate by reducing ground-truth confusion.

- **Q4:** The contract-coverage probe (6/9 held-out bugs, 67% doc coverage) suggests spec-completeness is a limiting factor. Have the authors considered a hybrid approach that augments documentation-derived contracts with automatically inferred invariants (e.g., from source code static analysis or runtime trace collection) to close spec-gap bugs like the qdrant dimension-mismatch silent-drop? Could this extend TestVDB's recall beyond the current 67% contract-coverage bound? — Intended effect: If the authors discuss hybrid contract inference and/or report preliminary results, item 4.3's rating (contract coverage not fully instrumented) would move toward Adequate by showing a path to full discovery-recall evaluation.

- **Q5:** The memorization canary (0/9 held-out bugs recalled at specificity) suggests GLM-5.2 did not regurgitate pre-2024 bugs through the pipeline, but the authors flag the cosine>1.0 case as overlapping with general mathematical knowledge. Are there other potential overlaps where general knowledge (e.g., "vectors should have matching dimensions," "distance metrics must satisfy triangle inequality") could coincide with held-out bugs, inflating apparent independence? How did the authors distinguish genuine discovery from knowledge overlap in the 9-bug cohort? — Intended effect: If the authors provide a systematic breakdown of the 9-bug cohort (which are knowledge-overlap vs genuinely novel), item 3.5's rating (maintainer acknowledgment weak ground truth) and item 4.3's rating (contract coverage) would both benefit from clearer contamination bounds.

---

## Meta-Review

### Criterion Consensus

| Criterion | Reviewer 1 | Reviewer 2 | Reviewer 3 | Meta-Review |
|---|---|---|---|---|
| Significance | Excellent | Adequate | Adequate | **Adequate** |
| Novelty | Excellent | Excellent | Adequate | **Excellent** |
| Soundness | Adequate | Adequate | Adequate | **Adequate** |
| Verifiability | Excellent | Excellent | Adequate | **Excellent** |
| Presentation | Adequate | Excellent | Adequate | **Adequate** |
| **Recommendation** | **Accept** | **Weak Accept** | **Weak Accept** | **ACCEPT** |

### Meta Recommendation
**ACCEPT**

All five criteria sit at consensus Adequate or above — Novelty and Verifiability at **Excellent** (2/3 each), Significance/Soundness/Presentation at **Adequate**. No criterion is Poor, no substance criterion is Weak, and fewer than three criteria are below Adequate (in fact none are below Adequate). With Novelty Excellent as a substance anchor, the verdict follows the "no criterion below Adequate with at least one substance Excellent → Accept" path.

The improvement over the prior round (which returned Accept with a Reviewer 2 Weak Reject dissent) is real and traceable. Reviewer 2's two prior [major, fixable] items — the single-layer counterfactual's mixed ground truth and the three-anchor design being unvalidated — have both been addressed: the 27 suppressed candidates are now live-confirmed on a fresh milvus v2.6.19 container (27/27, no LLM-proxy component), and the threat-model anchor was wired and ablated across three conditions (source-alone 9/12, threat-alone 6/12, union 11/12, TP retention 4/4), with the wiring gap diagnosed honestly. Reviewer 2 accordingly lifted from Weak Reject to Weak Accept, and Reviewer 1 from Weak Accept to Accept. The remaining items below are fixable blemishes, not tier-lowering flaws.

The agreement is meaningful, not a rubber stamp. All three reviewers independently converged on the same core merit — the controlled retrospective (31%→81% FP suppression at 96.7% TP retention), the model-free invariant oracles (cosine>1.0 reproducing across Milvus and Qdrant), and the now-live-grounded single-layer counterfactual — and on the same two residual presentation issues: the cross-system generalization framing still outruns the adjudicated evidence, and the threat-model anchor's architectural prominence outruns its validation.

### Priority Revisions
The main problems the author should fix, ranked by impact. Items 1–2 are each flagged by all three reviewers (cross-reviewer consensus); items 3–5 are single- or double-reviewer flags that still warrant attention.

1. **Qualify the cross-system generalization claim in the abstract.** All three reviewers flag that the abstract's "111 issues across five VDBMSs" overstates the validated base: Milvus and Qdrant account for 77/111 submissions and 36/52 adjudicated issues, while Weaviate (3 acknowledged), MeiliSearch (0), and Chroma (0) contribute near-zero adjudicated signal. The body already claims precision generalization only for Milvus and Qdrant (§1, §5.1), but the abstract omits this. Add a one-clause qualifier ("adjudicated signal concentrated on Milvus and Qdrant") to the abstract's yield sentence. (R1 W2/Q2, R2 1.2, R3 1.2 — unanimous [major, fixable].)

2. **Align the threat-model anchor's architectural prominence with its evaluated strength.** Figure 1 and the contribution statement present three counter-evidence anchors symmetrically, but the §5.4 ablation shows the threat-model anchor is a noisy complement (threat-alone 6/12=50%, unstable, over-fires on state/concurrency FPs via BS-03/06) while source-grounding is the primary validated anchor (9/12=75%, union 11/12=92%). The text now says this honestly, but Figure 1 still draws the three anchors equally. Either visually de-emphasize the threat-model anchor (dashed/gray, as already done for the unvalidated reproduction anchor) or re-caption Figure 1 to mark which anchors are source-validated vs design-level. (R1 W3, R2 W1/3.3, R3 W2/3.3 — consensus [major, fixable].)

3. **Make the baseline table's ground-truth asymmetry structural, not just footnote-deep.** Table 4 (precision/ground-truth comparison) mixes four ground truths (LLM self-judgment, API-acceptance, retrospective same-pool, maintainer adjudication). The footnote flags this, but the column layout invites direct numeric comparison. Adding a "ground-truth tier" column or grouping rows by ground-truth type would make the asymmetry structural. (R1 3.4, R3 W3/3.4 — [minor, fixable].)

4. **Bound or complete the end-to-end discovery-recall study.** The upstream probe (6/9 held-out pre-2024 bugs have recoverable contracts, 67%) and the memorization canary (0/9 recalled at issue-specificity) bound the gap from two sides, but a full rediscovery study on bug-present old versions remains future work. The canary already converts the contamination concern from an unbounded threat to a measured low quantity; state this explicitly as the recall claim's positive control rather than only as a contamination footnote. (R3 W5/4.3, R2 3.4 — [minor, fixable].)

5. **Soften or verify the "three-anchor" contribution wording against the n=12 ablation.** Reviewer 2 notes the "both" condition is a union of independent verdicts, not a joint dispatch where both anchors must agree — so "three-anchor design" slightly overstates a setup where threat-model acts as an offline backup. The contribution statement already softens this ("noisy complement"), but a one-line note that the union is an OR of independent anchors (not a joint AND) would make the ablation's logic explicit. (R2 W1/Q1 — [minor, fixable].)

**Bottom line:** the paper clears the Accept bar on the strength of its controlled retrospective, model-free invariants, and now-live-grounded single-layer counterfactual. The two unanimous revisions (abstract cross-system qualification + Figure 1 anchor de-emphasis) are presentational fixes that bring the framing in line with the evidence the paper already reports honestly in the body; neither requires new experiments.

---

*Orchestrator note on verification:* All three reviewer drafts were read in full and their substantive claims (111 submissions, 52 adjudicated, 36 acknowledged, 31%→81% FP suppression at 96.7% TP retention, 27/27 live-confirmed single-layer FPs, three-anchor 9/12/6/12/11/12 with 4/4 TP retention, canary 0/9, DeepSeek 2/3 over-strict reproduced) were cross-checked against the paper text and match. The reviewers use their own internal section/table numbering (renumbered by reading order) rather than the paper's LaTeX labels; this is a sub-agent citation artifact that does not affect the verdict and is marked here rather than patched, per the 3-round verify-fix cap. The drafts are preserved under `.paperpilot/review/.in-progress/reviewer-{1,2,3}/draft.md` for inspection.

# Paper Review — TestVDB (Round 14 re-review)

**Paper:** TestVDB: Detecting API Compliance Defects in Vector Database Systems via Contract-Truth Separation
**Venue:** VLDB/PVLDB (acm-sigconf)
**Date:** 2026-07-12 (Round 14)
**Paper type:** technical

This round re-reviews the state of the paper after the Round 13 follow-up (commit `85366a6`) that addressed the five Priority Revisions from Round 13's ACCEPT verdict. Three independent reviewers (Domain Expert / Area Specialist / General Reviewer) reviewed the full stripped source in parallel; each draft passed an independent checker (verify-fix artifacts kept under `.paperpilot/review/.in-progress/`).

---

## Reviewer 1: Domain Expert

**Overall Recommendation:** Weak Accept

### Summary
This paper presents TestVDB, an LLM-driven system for detecting API compliance defects in Vector Database Management Systems (VDBMSs). The problem is real and significant: 43% of VDBMS bugs are "incorrect behavior" but lack practical oracles, as current fuzzers like VDBFuzz detect only crashes. TestVDB targets API compliance defects (bugs where a VDBMS silently accepts inputs or behaviors that violate its documented contract) using Contract-Truth Separation (CTS): an assertion layer (LLM-generated contracts and four-judge debate) falsified by a truth layer (a dev-reviewer agent that applies maintainer-authority counter-evidence via three anchors: clean reproduction, source-grounded verification, and threat-model cross-check). CTS is motivated by the observation of contract hallucination propagation (when one LLM family both generates a contract and judges compliance, hallucinated constraints are self-confirmed; 25% of adjudicated submissions were by-design). The authors ran TestVDB against five VDBMSs, producing 111 submissions; 52 were adjudicated by maintainers (36 acknowledged, 28 fixed), concentrated on Milvus and Qdrant. A controlled retrospective over the 52 adjudicated candidates shows the dev-reviewer's source anchor lifts false-positive suppression from 31% to 81% while retaining 96.7% of true positives. End-to-end maintainer-adjudicated precision is 69.2% (interval [43.9%, 80.5%] under pending resolution sensitivity). The contribution is positioned as complementary to crash-focused fuzzing and scoped to boundary/validation compliance (75% of yield), not result-correctness oracles.

### Core Strengths
- **S1:** Real problem scope — addresses the incorrect-behavior gap (43% of VDBMS bugs) that crash-focused fuzzers like VDBFuzz miss, with a practical oracle (the API contract itself) — see 1.1, 1.2.
- **S2:** First LLM-driven VDBMS compliance detector — the paper delivers on this agenda item from the VDBMS testing roadmap — see 2.1, 2.2.
- **S3:** Contract-Truth Separation is a principled design — identifying contract hallucination propagation (25% by-design rate) and isolating LLM assertions from a maintainer-authority truth layer is a solid contribution — see 2.3.
- **S4:** Rigorous controlled retrospective — the same-population blind re-triage (52 candidates, two conditions) is methodologically sound and provides clean evidence for the dev-reviewer's contribution — see 3.1.
- **S5:** Honest scope boundary — the paper explicitly reports what TestVDB does not solve (result-correctness oracles) and where precision is validated (Milvus/Qdrant only, not all five systems) — see 3.3.

### Core Weaknesses
- **W1:** Cross-system generalization overclaimed — contribution 1 claims "first end-to-end realization... with adjudicated precision validated on Milvus and Qdrant AND breadth probes on three further VDBMSs," but the precision data supports only Milvus and Qdrant; Weaviate, MeiliSearch, and Chroma have minimal adjudicated signal — see 2.3 [major, fixable].
- **W2:** Schema-fuzzer baseline concedes effectiveness on boundary subset — the hand-written fuzzer achieves 71% precision on the boundary/validation subset (75% of acknowledged true positives) without any LLM stack, raising questions about TestVDB's marginal value on its dominant yield class — see 2.4 [major, fixable].
- **W3:** Novelty delta against competitors under-evaluated — the paper positions against RESTler, EvoMaster, and Schemathesis, but provides no empirical comparison on identical targets; the delta is real (semantic compliance vs schema-conformance/crash) but unvalidated — see 2.5 [major, fixable].
- **W4:** Three-anchor design under-validated — the threat-model anchor is reported as "noisy complement" and the reproduction anchor is "not exercised"; only source is validated, so the three-anchor contribution is incomplete — see 3.2 [minor, fixable].
- **W5:** Recall scope not measured — the 96.7% figure is judgment-layer TP retention, not end-to-end discovery recall; the paper acknowledges this gap but the contribution is therefore partial — see 3.4 [minor, fixable].

### Detailed Assessment

1. **Significance** — Adequate

- **1.1** **Real problem addressed.** The paper targets a genuine gap: VDBMS incorrect-behavior bugs (43% of defects, per the bug study) lack practical oracles. Crash-focused fuzzers like VDBFuzz detect only crashes, leaving the majority without an oracle. API compliance defects admit an oracle where general result-correctness does not: the documented contract itself. This is a meaningful, tractable slice of the VDBMS testing problem. The problem scope is well-bounded and practically significant.

- **1.2** **Practical impact but limited scope.** TestVDB found 111 issues across five VDBMSs; maintainers acknowledged 36 (28 fixed). This is real impact. However, the impact is concentrated on two systems (Milvus and Qdrant), and the yield is 75% boundary/validation compliance—a subset of incorrect behavior. The paper does not claim to solve result-correctness oracles (ANN recall, ranking), which remains open. The impact is therefore significant within its scoped boundary but not a complete solution to the incorrect-behavior problem.

- **1.3** **Clear positioning within the agenda.** The paper responds directly to the VDBMS testing roadmap's future work (an oracle for correctness, LLM-based methods that stay updated with evolving APIs). The judgment-side contribution (contract oracle) extends detection beyond crash into API-compliance. This is a clear, practical contribution to the VDBMS testing agenda.

2. **Novelty** — Weak

- **2.1** **First LLM-driven VDBMS compliance detector.** The paper delivers the first end-to-end LLM-driven system for VDBMS API compliance defects. This is a clear novelty claim. The multi-agent design (20 agents), four-judge debate, and dev-reviewer with Contract-Truth Separation are non-trivial and not previously instantiated for VDBMSs. The contract hallucination propagation observation (25% by-design rate) is also new to my knowledge.

- **2.2** **Contract-Truth Separation is a real design contribution.** The core reversal—isolating LLM-generated assertions from a maintainer-authority truth layer and falsifying them via source-grounded verification—is a principled design pattern. Identifying contract hallucination propagation as a self-confirmation failure mode (when one LLM family both generates the contract and judges) is novel. The dev-reviewer's three-anchor architecture (reproduction, source, threat-model) is a concrete instantiation. This is a solid contribution beyond applying LLMs to testing.

- **2.3 [major, fixable]** **Cross-system generalization overclaimed.** Contribution 1 claims "the first end-to-end realization... with adjudicated precision validated on Milvus and Qdrant AND breadth probes on three further VDBMSs (Weaviate, MeiliSearch, Chroma) that probe generality of the attack surface without adjudicated precision." However, Table 2 shows the adjudicated precision data supports only Milvus and Qdrant: Milvus (51 submissions, 22 acknowledged), Qdrant (26 submissions, 11 acknowledged). Weaviate has 30 submissions but only 4 adjudicated (3 acknowledged, 1 rejected; 0 by-design). MeiliSearch (3 submissions) and Chroma (1 submission) have near-zero adjudicated signal. The contribution text should clarify that cross-system generalization is claimed for the attack surface, not for precision. Currently, the phrasing implies broader validation than the data supports.

- **2.4 [major, fixable]** **Schema-fuzzer baseline concedes effectiveness on boundary subset.** In Section 4.3, the paper reports a hand-written boundary-value fuzzer (19 probes derived from documented constraints) that surfaced 7 API-accepted candidates, 5 classified as genuine violations (71% precision) and 2 as by-design defaults. This concedes that on the boundary/validation subset (75% of acknowledged true positives), a spec-driven fuzzer is genuinely effective. TestVDB's marginal value lies where the fuzzer cannot reach: (a) state/logic, diagnostic, and result-correctness probes (8/36 TPs are non-boundary), (b) CTS FP-suppression (the fuzzer has no source-grounded layer), and (c) spec-gap bugs. The paper acknowledges this, but the dominance of boundary bugs in the yield (75%) raises questions about TestVDB's marginal value on its primary yield class. The contribution would be stronger if the paper quantified TestVDB's unique non-boundary yield (8/36 = 22%) and positioned it as the primary delta over schema fuzzing.

- **2.5 [major, fixable]** **Novelty delta against competitors under-evaluated.** The Related Work section positions against RESTler (stateful REST API fuzzer), EvoMaster (evolutionary REST API test generator), and Schemathesis (property-based testing on OpenAPI schemas). The paper correctly characterizes the delta: TestVDB extends to "semantic compliance (does the response honor the documented contract?)" while these tools target schema-conformance and crash at the API boundary. However, there is no empirical comparison on identical targets. The complementarity with VDBFuzz (crash vs compliance) is claimed but not demonstrated. The novelty is real—semantic compliance is a clear conceptual extension—but the evaluation is siloed. Without a head-to-head comparison on the same VDBMSs, the delta remains conceptual rather than empirically validated.

- **2.6** **LLM multi-agent instantiation is incremental.** The use of multi-agent debate (du2023improving) and the He et al. 2025 survey as foundational background are appropriate, but the multi-agent design itself is incremental. The novelty is in the specific instantiation (four-judge debate + dev-reviewer) and the Contract-Truth Separation principle, not in the multi-agent paradigm per se.

3. **Soundness** — Adequate

- **3.1** **Rigorous controlled retrospective (same-population ablation).** The paper's strongest evidence is the controlled retrospective over all 52 maintainer-adjudicated candidates under two blind conditions: claim-only (four-judge layer) vs source-grounded (dev-reviewer's source anchor). Source-grounding lifts FP suppression from 5/16 (31%) to 13/16 (81%, 2.6×) while retaining 29/30 TPs (96.7%, n=30). This is a clean, same-population comparison that directly validates the dev-reviewer's contribution. The methodological design (blind re-triage, label-isolated agents) is sound.

- **3.2 [minor, fixable]** **Three-anchor design under-validated.** The dev-reviewer has three counter-evidence anchors (clean reproduction, source-grounded verification, threat-model cross-check). The paper validates only the source anchor comprehensively. The threat-model anchor is ablated in Section 4.4 and reported as "noisy complement" (source-alone 9/12 FPs, threat-alone 6/12, union 11/12), with the reproduction anchor "not exercised" in the retrospective. The three-anchor design is thus incompletely validated. The contribution claims a three-anchor pipeline, but the evidence supports primarily a one-anchor (source) solution with two optional complements. The paper should clarify the validated scope.

- **3.3** **Honest reporting of precision uncertainty.** The paper reports maintainer-adjudicated precision as 69.2% (36/52) and explicitly bounds the sensitivity to pending submissions: resolving all 30 pending as valid gives 80.5%; resolving all as invalid gives 43.9%. This interval [43.9%, 80.5%] is honestly reported rather than relying on a point estimate alone. The excluded set (29 closed-no-label or duplicate) is also explicitly discussed. This transparency is a strength.

- **3.4 [minor, fixable]** **Recall scope not measured.** The 96.7% figure is judgment-layer TP retention, not end-to-end discovery recall. The paper acknowledges this gap and reports a pilot on 9 held-out pre-2024 bugs, noting that full recall is bounded by spec-completeness and version-pinning limits. However, the contribution is therefore partial: TestVDB is validated for precision but not for recall. The paper would be stronger if it reported at least a lower bound on discovery recall (e.g., "TestVDB rediscovered X of the 9 held-out bugs when run against bug-present versions").

- **3.5** **LLM variance and contamination checks.** The paper reports re-adjudicating 46 source-grounded candidates five times with independent agents, yielding 99.1% pairwise agreement and 45/46 unanimous verdicts. It also audits GLM-5.2 contamination with a memorization canary (0/9 issues recalled at specificity). These are rigorous checks that strengthen the Soundness of the LLM-dependent components.

4. **Verifiability** — Adequate

- **4.1** **Sufficient methodological detail.** The paper provides enough detail to understand the method: the five-stage pipeline (contract extraction, attack generation, four-judge debate, dev-reviewer, novelty gate), the 20 agents (4 high-budget, 16 low-budget), and the LLM configuration (GLM-5.2, default sampling). The cost and reproducibility section (Section 3.2) reports on the order of 10⁴ LLM calls total and ~10³ calls per target, with wall-clock dominated by dev-reviewer's source-grounding step. This is sufficient for a research prototype.

- **4.2** **Artifact declared and reachable.** The paper declares an anonymized artifact at https://anonymous.4open.science/r/testvdb-anon-D644/ to be made public on acceptance. The description includes the five VDBMSs, all 111 submissions with outcomes, and the full prompts. The artifact is declared and reachable (the URL format is standard for anonymous review). The paper notes that precise per-token and wall-clock accounting is part of the anonymized artifact. This meets the Verifiability bar.

- **4.3** **Data and results reproducible in concept.** The main flow (contract extraction → attack generation → four-judge debate → dev-reviewer) is reproducible in concept. The controlled retrospective (Section 4.3) provides enough detail to understand the ablation methodology (blind re-triage, label-isolated agents). Some detail is missing (e.g., exact prompt templates for all 20 agents), but the artifact is declared to contain these. The text itself is sufficient to follow the work.

- **4.4** **Version pinning documented.** Target VDBMS versions are pinned (Milvus 2.6.19 for ablations; full version matrix in artifact). This is critical for reproducibility and is properly reported.

5. **Presentation** — Adequate

- **5.1 [minor, fixable]** **Minor writing issues.** The writing is generally clear but has some verbosity and repetition. For example, the contract hallucination propagation phenomenon is explained in both Section 2 (paragraph 2) and Section 4 (intro and formalization). Some sentences are long and could be split for clarity (e.g., the first sentence of the abstract is 76 words). These are minor and do not impede understanding.

- **5.2** **Structure is sound.** The paper follows a logical structure: Introduction → Background → Approach → Contract Hallucination → Evaluation → Related Work → Conclusion. The flow is clear. The evaluation section is well-organized by research question (RQ1–RQ4). The case studies (RQ2) concretely illustrate the TP/FP boundary. The structure is sound and complete.

- **5.3** **Figures and tables are effective.** Figure 1 (pipeline diagram) clearly illustrates the assertion layer vs truth layer separation. Table 2 (yield and outcomes) is readable and comprehensive. Table 3 (baseline comparison) is a strength: it explicitly groups arms by ground-truth tier (LLM-judged, API-acceptance, retrospective, maintainer-adjudicated) and notes the asymmetry, making the comparison clear rather than disguising it.

- **5.4 [minor, fixable]** **Notation inconsistencies.** Some notation could be more consistent. For example, the paper uses both "nprobe=0" and "\texttt{nprobe}=0" for parameter values. The contract hallucination formalization uses C_LLM and C_true, which is clear, but could be introduced earlier. These are minor issues.

- **5.5 [minor, fixable]** **Typos and minor edits needed.** A few minor issues: (1) Section 4.3 paragraph 1: "milvus-io/milvus \,\#47729" has extra spacing. (2) Section 4.4: "\textsc{bs-}03" and "\textsc{bs-}06" use inconsistent small caps. (3) References section: some entries have "% VERIFY" comments indicating the authors need to verify details. These are easily fixable.

### Questions for Authors

- **Q1:** Can you clarify the cross-system generalization claim in Contribution 1? Currently, the text suggests adjudicated precision is validated on all five VDBMSs, but the data supports only Milvus and Qdrant. Would rephrasing as "adjudicated precision validated on Milvus and Qdrant, with breadth probes on Weaviate, MeiliSearch, and Chroma that probe generality of the attack surface" accurately reflect your intent? — Intended effect: If yes, this would resolve the overclaim in W1 (2.3).

- **Q2:** Given that the schema fuzzer achieves 71% precision on the boundary/validation subset (75% of acknowledged TPs), can you quantify TestVDB's unique value on the non-boundary subset? You report 8/36 TPs as non-boundary (22%). If TestVDB's unique contribution is the non-boundary yield plus FP-suppression, could you position this more explicitly as the primary delta over schema fuzzing? — Intended effect: This would address W2 (2.4) by clarifying TestVDB's marginal value.

- **Q3:** Can you provide at least a conceptual head-to-head comparison with RESTler or EvoMaster on the same VDBMS targets? Even if not a full empirical study, a small pilot (e.g., running RESTler on Milvus and comparing the yield) would strengthen the novelty delta. — Intended effect: This would address W3 (2.5) by providing some empirical validation of the conceptual delta.

- **Q4:** Can you clarify the validated scope of the three-anchor design? Is the claim that source is primary and validated, threat-model is a noisy complement (validated only on n=12), and reproduction is future work? — Intended effect: This would clarify W4 (3.2) by explicitly stating what is validated vs what remains exploratory.

- **Q5:** Can you report at least a lower bound on discovery recall from your 9 held-out bug pilot? Even a qualitative statement (e.g., "TestVDB rediscovered X of 9 bugs when run against bug-present versions, bounded by spec-completeness and version-pinning") would complete the precision-only picture. — Intended effect: This would address W5 (3.4) by providing some recall evidence.

---

## Reviewer 2: Area Specialist

**Overall Recommendation:** Weak Accept

**Specialty areas chosen:** (1) LLM-driven testing / LLM-as-oracle / multi-agent debate, (2) Database/API testing (REST fuzzing, metamorphic testing, differential testing).

### Summary

The paper addresses API compliance defects in Vector Database Management Systems (VDBMSs), a problem where a VDBMS silently accepts inputs or produces behaviors that violate its documented contract without crashing. The authors propose TestVDB, an LLM-driven system that auto-derives a contract oracle from API documentation and applies Contract-Truth Separation (CTS) to isolate LLM-generated assertions from a truth layer that falsifies them via maintainer-authority evidence (source code, issue history, by-design intent). CTS is motivated by the observation that when one LLM family both generates a contract and judges compliance, hallucinated constraints are self-confirmed (contract hallucination propagation), evidenced by 25% of adjudicated submissions being marked by-design. TestVDB produced 111 issues across five VDBMSs; maintainers acknowledged 36 (28 fixed). On a controlled retrospective over 52 adjudicated candidates, the dev-reviewer's source anchor lifts false-positive suppression from 31% to 81% while retaining 96.7% of true positives. The paper claims cross-system generalization of the attack surface (not precision) validated on Milvus and Qdrant, with breadth probes on Weaviate, MeiliSearch, and Chroma.

### Core Strengths

- **S1:** Clear problem motivation grounded in empirical VDBMS bug study — see 1.1, 1.1.
- **S2:** Contract hallucination propagation observation is a credible, well-documented phenomenon — see 2.1, 2.3.
- **S3:** Controlled retrospective (same-population ablation) provides clean evidence for CTS contribution — see 3.2.
- **S4:** Honest boundary reporting: cross-system precision limited to Milvus/Qdrant; 75% yield is boundary/validation — see 1.4, 1.
- **S5:** Complementarity with VDBFuzz well-argued from oracle definitions — see 1.1, 1.1.

### Core Weaknesses

- **W1:** Cross-system precision overclaim — paper claims generalization only for attack surface, but Related Work and abstract language blur this — see 2.1, 5.4.
- **W2:** Evaluation scope narrow: no head-to-head comparison with schema-driven fuzzing on identical targets — see 5.3.
- **W3:** Three-anchor design claimed but only one (source) validated; threat-model anchor shown noisy, reproduction unevaluated — see 3.6, 5.4.
- **W4:** LLM contamination threat (GLM-5.2 may have seen pre-2024 source) mitigated only by canary, not systematic exclusion — see 3.7.
- **W5:** Single-layer counterfactual conflates LLM-judgment with maintainer-adjudicated ground truth in precision comparison — see 3.5.

### Detailed Assessment

1. **Significance** — Adequate

- **1.1** The problem is well-motivated by empirical data: 43% of VDBMS bugs are incorrect behavior vs 23% crash/hang, and current testing (VDBFuzz) only targets the minority. This establishes practical importance.
- **1.2** API compliance defects are a credible threat model: they corrupt query semantics, lower recall, and expand attack surface without triggering crashes. The stakes are real for production VDBMS deployments.
- **1.3 [minor, fixable]** The scope is narrower than the abstract suggests: TestVDB targets boundary/validation compliance (75% of yield) and excludes soft result-correctness (ANN recall, ranking), which remains open. The abstract should foreground this boundary.
- **1.4** The impact is bounded by evaluation scope: maintainer-adjudicated precision is validated only on Milvus and Qdrant (69.2% on 52 adjudicated submissions); Weaviate, MeiliSearch, and Chroma are breadth probes without adjudicated precision. The paper is honest about this, but it limits generalizability claims.

2. **Novelty** — Adequate

- **2.1** Contract hallucination propagation is a clear, non-obvious observation: when one LLM family both generates the contract and judges compliance, hallucinated constraints are self-confirmed, evidenced by 12 by-design cases (25% of adjudicated submissions). This is the paper's most original insight and motivates CTS.
- **2.2** Contract-Truth Separation (CTS) is a real delta over single-layer LLM judgment: the dev-reviewer's source anchor lifts FP suppression from 31% to 81% while retaining 96.7% TPs in a controlled retrospective. The design principle (assertion layer falsified by truth layer) is sound.
- **2.3** Checked delta against RESTler (stateful REST API fuzzing): RESTler targets spec-conformance and crash bugs; TestVDB extends to semantic compliance (does response honor documented contract?). RESTler requires standard OpenAPI spec; TestVDB handles VDBMS endpoints lacking compliant specs (we probed `/swagger`, `/openapi.json`, all 404). This is a genuine extension.
- **2.4** Checked delta against TLP (query partitioning for SQL logic bugs): TLP assumes reference SQL semantics; VDBMS APIs lack agreed reference semantics (vendors diverge; results approximate), so differential testing is unsuitable. TestVDB replaces reference semantics with documentation-derived contracts, a different oracle class. The positioning is fair.
- **2.5** Checked delta against Schemathesis (property-based testing for OpenAPI): Schemathesis requires standards-compliant spec; VDBMS REST endpoints don't serve one, so off-the-shelf application is blocked. TestVDB's doc-derived contracts bridge this gap. Schemathesis validates schema-conformance; TestVDB validates semantic compliance.
- **2.6 [major, fixable]** Related work positioning overreaches in one instance: the paper states Schemathesis "cannot be applied off-the-shelf" because VDBMSs lack OpenAPI specs — this is accurate, but the broader implication (that schema-driven fuzzers are ineffective) is not empirically tested. The hand-written schema-fuzzer baseline concedes that on the boundary/validation subset, a spec-driven fuzzer is genuinely effective (71% source-grounded precision). The paper should clarify: Schemathesis is blocked by spec absence, not by fundamental incompatibility; TestVDB's marginal value is state/logic probes + FP-suppression, not boundary-finding per se.
- **2.7** The multi-agent debate contribution is incremental rather than novel: TestVDB applies existing multi-agent verification patterns to the VDBMS domain, adding the CTS layer. The novel insight is the failure mode (contract hallucination propagation) and its mitigation (source-grounded falsification), not multi-agent debate itself.

3. **Soundness** — Adequate

- **3.1** RQ1 (detection capability) is supported by maintainer acknowledgment: 111 submissions across 5 VDBMSs; 36 acknowledged (28 fixed, 8 accepted-open); adjudicated signal concentrated on Milvus (51) and Qdrant (26).
- **3.2** The controlled retrospective (RQ3, same-population ablation) provides the strongest evidence: re-triaging 52 adjudicated candidates under claim-only vs source-grounded conditions shows FP suppression lift from 31% to 81% with 96.7% TP retention. This cleanly isolates the dev-reviewer's contribution.
- **3.3** RQ2 case studies are well-chosen to span TP/FP boundary: True positives (Milvus #47729 invalid nprobe=0, #49844 empty-filter full scan); false positive correctly suppressed (#50193 get_stats rowCount=0 eventual consistency). The traces are concrete.
- **3.4** Baseline comparisons are extensive but asymmetric: single-layer counterfactual, single-LLM end-to-end, schema-aware fuzzer, and single-LLM arms are compared. However, the ground truths differ (LLM self-judgment vs LLM+source vs maintainer adjudication), so numerical comparison requires care. The paper acknowledges this asymmetry (Table 3 explicitly groups by truth tier), which is good.
- **3.5 [major, fixable]** The single-layer counterfactual precision figure (45.6%) conflates weak-proxy ground truth (live reproduction + source grounding for 27 suppressed candidates) with maintainer-adjudicated ground truth (36/52 baseline). The 27 suppressed candidates were confirmed via live probe + source grounding, not maintainer triage. While live reproduction is a strong proxy, it's not equivalent to maintainer adjudication. The paper should present this as a directional lift at zero recall cost with a weaker ground truth caveat, not as a clean precision comparison.
- **3.6 [minor, fixable]** The three-anchor design (clean reproduction, source-grounding, threat-model cross-check) is claimed in the abstract but only source is validated; threat-model is ablated as noisy, and reproduction is "design-level and not yet evaluated". The contribution statement should reflect this: CTS with source anchor is validated; threat-model is exploratory; reproduction is future work.
- **3.7** Threats to validity are discussed thoroughly: internal (maintainer acknowledgment is weak ground truth), selection (submission-selection bias), external (same-population ablation is Milvus+Qdrant only), construct (defect-type classification is title-based), LLM variance (near-zero on judgment layer), contamination (GLM-5.2 memorization canary shows 0/9 issues recalled), recall scope (96.7% is judgment-layer TP retention, not end-to-end discovery recall). The discussion is honest and detailed.
- **3.8 [minor, unfixable]** Maintainer acknowledgment as ground truth is inherently weak: triage may reflect report clarity rather than defect validity (a reviewer effect). The paper acknowledges this but cannot fix it — it's a limitation of the empirical method. This is a known issue in bug-report studies and doesn't invalidate the results, but it bounds the confidence in precision estimates.

4. **Verifiability** — Adequate

- **4.1** The paper describes the pipeline clearly enough to follow: five stages (contract extraction, attack generation, four-judge debate, dev-reviewer, novelty gate) with agent roles and configuration.
- **4.2** Ablation methodology is well-specified: controlled retrospective uses label-isolated agents with outcomes hidden; single-layer counterfactual re-runs generation + four-judge debate; threat-model ablation uses three conditions (source-alone, threat-alone, both).
- **4.3** Implementation details are sufficient: all agents are GLM-5.2; 20 agents with 4 on high-budget config, 16 on low-budget; Claude Code runtime default sampling; target VDBMS versions pinned (Milvus 2.6.19 for ablations); prompts in artifact.
- **4.4 [minor, fixable]** Cost and scale reporting is approximate: "on the order of 10^4 LLM calls (~10^7 tokens) aggregate; per target, ~10^3 calls (~2×10^6 tokens) in a few hours". The paper should provide exact accounting in the anonymized artifact.
- **4.5** Artifact availability is declared: anonymized artifact at https://anonymous.4open.science/r/testvdb-anon-D644/, to be made public on acceptance. This meets the verifiability bar.
- **4.6 [minor, fixable]** The schema-fuzzer baseline description lacks reproducibility details: "19 probes derived directly from Milvus's documented parameter constraints" — which parameters? Which constraints? The paper should list the 19 probes or provide the fuzzer script in the artifact.

5. **Presentation** — Adequate

- **5.1** Structure is logical and follows the problem-approach-evaluation pattern: Introduction (problem + motivation), Approach (pipeline + CTS), Contract Hallucination (phenomenon), Evaluation (RQ1-4), Related Work, Conclusion.
- **5.2** Figures and tables are effective: Figure 1 (pipeline) visually separates assertion/truth layers; Table 2 (yield) cleanly breaks down outcomes by system; Table 3 (baselines) explicitly groups by truth tier to avoid misleading comparison.
- **5.3** Writing is generally readable with minor awkwardness: some sentences are long and densely packed. The prose is understandable but could be tightened.
- **5.4 [minor, fixable]** Abstract language overclaims cross-system generalization: "produced 111 issues across five VDBMSs; maintainers acknowledged 36" without clarifying that adjudicated precision is validated only on two systems (Milvus, Qdrant). The abstract should foreground the honest boundary: "adjudicated signal concentrated on Milvus and Qdrant; breadth probes on three further VDBMSs probed generality without adjudicated precision."
- **5.5 [minor, fixable]** Related Work positioning is slightly uneven: Schemathesis is cited as "cannot be applied off-the-shelf" but the paper's own schema-fuzzer baseline shows spec-driven fuzzing is effective on boundary/validation. The distinction should be clarified: Schemathesis is blocked by spec absence, not by fundamental incompatibility; TestVDB's marginal value is CTS FP-suppression and state/logic probes, not boundary-finding.
- **5.6 [minor, fixable]** Terminology inconsistency: "model-free invariant oracles" are introduced as a subclass but not clearly distinguished from contract oracles in the approach section. The paper should explicitly position mathematical-invariant oracles (cosine similarity ∈ [-1,1]) as a separate oracle class earlier.
- **5.7 [minor, fixable]** Typo/formatting: Table 3 caption runs long; consider splitting the "truth tier" grouping into a separate sentence. Some acronyms are first-used without definition (CTS appears in abstract before "Contract-Truth Separation" is introduced).

### Questions for Authors

- **Q1:** The single-layer counterfactual precision (45.6%) combines maintainer-adjudicated baseline (36/52) with live-reproduced, source-grounded FPs (27 candidates). How many of those 27 do you expect would be reclassified by maintainer triage? This would bound the residual gap between live-reproduction and maintainer adjudication — see 3.5.
- **Q2:** The three-anchor design claims source + threat-model + reproduction, but only source is validated; threat-model is noisy; reproduction is unevaluated. For the camera-ready, consider stating the contribution as "CTS with source anchor validated; threat-model anchor explored as noisy complement; reproduction anchor as future work" — see 3.6.
- **Q3:** The schema-fuzzer baseline found 5/7 genuine violations after source-grounded filtering. Did these overlap with TestVDB's acknowledged boundary TPs? If ~1-2 overlap and 3-4 are new variants, this strengthens the complementarity claim. Consider reporting the overlap explicitly — see 2.6.
- **Q4:** For the abstract, consider foregrounding the evaluation scope: "adjudicated precision validated on Milvus and Qdrant (69.2%); breadth probes on Weaviate, MeiliSearch, and Chroma probed generality without adjudicated precision" — see 1.4, 5.4.
- **Q5:** The paper identifies COSINE distance >1.0 for identical vectors as a "model-free invariant oracle". Are there other mathematical invariants applicable to VDBMSs (e.g., triangle inequality for distance metrics)? This could expand the expressible invariant subclass beyond the three cases reported — see 5.6.

---

## Reviewer 3: General Reviewer

**Overall Recommendation:** Weak Accept

### Summary
This paper introduces TestVDB, an LLM-driven system for detecting API compliance defects in Vector Database Management Systems (VDBMSs). The authors define API compliance defects as bugs where a system silently accepts inputs or behaviors that violate its documented contract. Their core contribution is Contract-Truth Separation (CTS), which isolates LLM-generated assertions from a "truth layer" that falsifies them using maintainer-authority evidence (source code, prior PRs, issue history). The system produced 111 candidate issues across five VDBMSs, with 36 acknowledged by maintainers (28 fixed). On a controlled retrospective over 52 adjudicated candidates, the dev-reviewer's source anchor improved false-positive suppression from 31% to 81% while retaining 96.7% of true positives.

### Core Strengths
- **S1:** The Contract-Truth Separation principle identifies a real failure mode—contract hallucination propagation—where LLMs both generate contracts and judge compliance, leading to self-confirmation of hallucinated constraints — see 3.1, 3.2, 4.1
- **S2:** The controlled retrospective (RQ3) provides strong evidence for the dev-reviewer's source anchor as the primary FP-suppression mechanism, with a clean 31%→81% lift on the same 52-candidate population — see 3.3
- **S3:** The paper honestly scopes its claims—boundary/validation compliance (75% of yield), excluding crash bugs (complementary to VDBFuzz) and soft result-correctness (ANN recall/ranking) — see 1.1, 2.3, 5.1
- **S4:** The COSINE distance >1.0 invariant cases demonstrate a model-free oracle subclass that depends on no LLM judgment and reproduces across vendors — see 3.2

### Core Weaknesses
- **W1:** The paper claims cross-system generalization from five VDBMSs, but adjudicated signal concentrates on Milvus and Qdrant (77/111 submissions, 36/52 adjudicated TPs); Weaviate, MeiliSearch, and Chroma contribute near-zero adjudicated signal — see 1.2
- **W2:** Related Work coverage is thin—RESTler and EvoMaster are mentioned but not positioned against TestVDB's novelty delta; the schema-fuzzer baseline is acknowledged as effective but no systematic comparison is presented — see 2.3, 3.5
- **W3:** The threat-model anchor evaluation (RQ4) is underpowered (n=12) and reports a noisy, unstable complement; the paper does not claim it as a validated contribution, but it remains part of the system design without clear validation — see 3.4, 3.5
- **W4:** The single-layer counterfactual (45.6% vs. 69.2%) mixes ground truths and has limited feedback cycles, making it a directional rather than definitive comparison — see 3.6

### Detailed Assessment

1. **Significance** — Adequate
   - **1.1** The problem scope is real and well-motivated: 43% of VDBMS bugs are incorrect-behavior, but current testing (VDBFuzz) targets only the 23% crash/hang minority. API compliance defects are a tractable subset where the documented contract provides an oracle.
   - **1.2 [major, fixable]** The cross-system generalization claim is overstated. The abstract and contributions claim "five VDBMSs" but the body acknowledges adjudicated signal concentrates on Milvus and Qdrant (77 submissions, 36 acknowledged TPs). Weaviate, MeiliSearch, and Chroma contribute near-zero acknowledged TPs. The paper should claim generality of the attack surface, not precision, across all five systems.
   - **1.3 [minor, fixable]** The positioning paragraph correctly disclaims the result-correctness oracle direction (ANN recall, ranking) as remaining open, but the paper would be stronger if it articulated a clearer roadmap for that direction given its prominence in the roadmap's Future Work.

2. **Novelty** — Adequate
   - **2.1** Contract-Truth Separation (CTS) is a clear design principle: isolate LLM-generated assertions from a truth layer and falsify them via maintainer-authority evidence (source, history, prior PRs). The dev-reviewer's three-anchor realization (clean reproduction, source-grounding, threat-model) is a concrete instantiation.
   - **2.2** The contract hallucination propagation observation is well-documented: when one LLM family both generates a contract and judges compliance, hallucinated constraints are self-confirmed. The 12 by-design cases (25% of adjudicated submissions) are direct evidence.
   - **2.3 [major, fixable]** Related Work coverage on REST API testing tools (RESTler, EvoMaster, Schemathesis) is superficial. These tools target schema-conformance and stateful fuzzing of REST APIs, which is adjacent to TestVDB's semantic compliance checking. The paper should position TestVDB's novelty delta more explicitly: CTS provides a semantic oracle that goes beyond schema validation to documented intent, whereas RESTler/EvoMaster lack both the LLM-driven semantic layer and the source-grounded falsification mechanism. The schema-fuzzer baseline concedes that spec-driven fuzzers are effective on the boundary subset; the paper should articulate TestVDB's marginal value over these tools more clearly.
   - **2.4 [minor, fixable]** The abstract and introduction frame TestVDB as "the first LLM-driven detector" for API compliance defects, but the Related Work section shows a broader landscape of LLM-based testing and multi-agent verification. The framing should be more precise: first LLM-driven detector for VDBMS API compliance, or first application of CTS to this problem.

3. **Soundness** — Adequate
   - **3.1** The controlled retrospective (RQ3) is methodologically sound: the same 52-candidate pool re-triaged under blind conditions (claim-only vs. source-grounded), with outcomes hidden via label-isolated agents. The 31%→81% FP-suppression lift and 96.7% TP retention are strong evidence for the dev-reviewer's source anchor as the primary validated mechanism.
   - **3.2** The single-layer counterfactual (27/27 suppressed candidates re-probed as live FPs, zero over-kill) provides additional evidence that the FP-suppression chain is not simply discarding bugs. The mix of five FP classes (input-validation rejections, by-design accepts, correct rejections, oracle script bugs, state-semantics cases) shows diversity.
   - **3.3** The COSINE distance >1.0 invariant cases are the paper's strongest technical finding: they violate a hard mathematical bound, reproduce across vendors (Milvus and Qdrant), and depend on no LLM judgment. This is a defensible, model-free oracle subclass.
   - **3.4 [major, unfixable]** The threat-model anchor evaluation (RQ4) is underpowered (n=12) and reports an exploratory negative. The paper honestly diagnoses the wiring gap and re-runs with fixed wiring, showing threat-alone as unstable across runs (one FP flipped) and over-firing on state/concurrency cases. However, the design remains part of the system without clear validation—the paper treats it as a "noisy complement" whose union with source is the practical configuration, but this is not claimed as a validated contribution. This is a design-level gap that a revision cannot fully resolve without additional data.
   - **3.5 [minor, fixable]** The schema-fuzzer baseline (19 probes, 7 API-accepted, 5/7 genuine violations after source-grounding) concedes that spec-driven fuzzers are effective on the boundary subset. The paper acknowledges TestVDB's marginal value lies in state/semantic probes, FP-suppression, and spec-gap bugs, but a systematic comparison against Schemathesis is blocked by Milvus's non-compliant OpenAPI. The paper should articulate this comparison more clearly and explain why CTS adds value beyond schema fuzzing even on the boundary subset.
   - **3.6 [minor, fixable]** The single-layer counterfactual end-to-end figure (45.6% vs. 69.2%) combines maintainer-adjudicated 36/52 with 27 live-reprobed, source-grounded FPs. The paper acknowledges the residual gap (maintainer triage might reclassify a few) and bounds it to one feedback cycle, but the comparison remains directional rather than definitive.

4. **Verifiability** — Adequate
   - **4.1** The paper provides sufficient implementation detail to follow the five-stage pipeline (Fig. 1): contract extraction, attack generation, four-judge debate, dev-reviewer with three anchors, novelty gate. The threat-model artifact and agent prompts are referenced as part of the anonymized artifact.
   - **4.2** The controlled retrospective methodology is clearly described: same 52-candidate pool, blind re-triage under two conditions (claim-only vs. source-grounded), outcomes hidden via label-isolated agents. The statistics (31%→81% FP suppression, 96.7% TP retention, n=30 reachable TPs) are reproducible from the text.
   - **4.3 [minor, fixable]** The threat-model anchor evaluation (RQ4) describes the wiring gap diagnosis and the re-run with fixed wiring, but the exact prompt changes and the three-condition ablation procedure (source-alone, threat-alone, both) could be more detailed. The instability across runs (one FP flipped) should be quantified more precisely.
   - **4.4 [minor, fixable]** The schema-fuzzer baseline describes the 19 probes and 7 API-accepted candidates but does not list the exact probe list. Reproducing the 5/7 genuine vs. 2/7 by-design classification would require more detail.

5. **Presentation** — Adequate
   - **5.1** The paper is well-structured: introduction with clear problem formulation, approach overview with figure, evaluation with RQ1–RQ4, honest scoping in positioning and conclusion. The abstract is concise and accurate.
   - **5.2** Figure 1 clearly shows the five-stage pipeline and the separation between assertion layer (LLM contract + 4-judge) and truth layer (three anchors). The visual distinction between primary (source), secondary (threat-model), and unmeasured (reproduction) anchors is helpful.
   - **5.3** Tables 2 and 3 (yield, baselines) present the data clearly. Table 3's grouping by truth tier (LLM-judged proxy → API-acceptance proxy → retrospective → maintainer adjudication gold) makes the asymmetry explicit rather than disguising it.
   - **5.4 [minor, fixable]** The abstract is dense and could be split more cleanly. The positioning paragraph is also dense with caveats and could be restructured for readability.
   - **5.5 [minor, fixable]** The notation in the threat-model anchor section is sometimes dense (e.g., bs-03/06) and could be explained more clearly for readers unfamiliar with the blindspot notation.
   - **5.6 [minor, fixable]** The Related Work section is organized by subfield but the REST API testing tools (RESTler, EvoMaster, Schemathesis) are not positioned against TestVDB's novelty delta as clearly as they could be.

### Questions for Authors
- **Q1:** Can you clarify the adjudication status of the 30 pending submissions across the five VDBMSs? Specifically, how many are Milvus vs. Qdrant vs. Weaviate vs. others? This would clarify whether the pending pool might significantly shift the precision interval or whether it is concentrated on systems that already have strong adjudicated signal — intended effect: would help assess the robustness of the 69.2% point estimate and the [43.9%, 80.5%] interval (3.3).
- **Q2:** For the three VDBMSs with near-zero adjudicated signal (Weaviate, MeiliSearch, Chroma), can you provide more detail on why they yielded so little? Was it a coverage issue (docs were sparse, API endpoints limited), a detection-scope mismatch (their compliance defects are outside TestVDB's attack surface), or a maintainer triage difference (they triage differently than Milvus/Qdrant)? This would clarify whether the cross-system generalization claim should be reconceptualized — intended effect: would help refine the overgeneralization in 1.2 (cross-system claim).
- **Q3:** The threat-model anchor is evaluated as a noisy complement (6/12 vs. 9/12 on Milvus FPs, union 11/12). Given the instability across runs and the over-firing on state/concurrency cases, would you consider de-emphasizing it in the system design (e.g., presenting CTS primarily as the source anchor with threat-model as an optional, unvalidated prior) or providing a stronger validation (e.g., a larger-scale ablation on multiple VDBMSs)? — intended effect: would address the design-validation gap in 3.4.
- **Q4:** The schema-fuzzer baseline shows that spec-driven fuzzers are effective on the boundary subset (75% of yield). Can you articulate TestVDB's marginal value over these tools more clearly, particularly on the boundary subset itself? Is it primarily the FP-suppression layer (catching by-design defaults that the fuzzer would miss), the semantic layer (catching spec-gap bugs), or the state/logic probes? — intended effect: would help position against Related Work (2.3) and the overgeneralization in 1.2.
- **Q5:** The single-layer counterfactual (45.6% vs. 69.2%) is a directional comparison with limited feedback cycles. Do you plan to run a full end-to-end single-layer arm with independent maintainer triage in future work? What would be required to make that comparison definitive? — intended effect: would clarify the strength of the baseline comparison in 3.6.

---

## Meta-Review

### Criterion Consensus

| Criterion | Reviewer 1 | Reviewer 2 | Reviewer 3 | Meta-Review |
|---|---|---|---|---|
| Significance | Adequate | Adequate | Adequate | **Adequate** |
| Novelty | Weak | Adequate | Adequate | **Adequate** |
| Soundness | Adequate | Adequate | Adequate | **Adequate** |
| Verifiability | Adequate | Adequate | Adequate | **Adequate** |
| Presentation | Adequate | Adequate | Adequate | **Adequate** |
| **Recommendation** | **Weak Accept** | **Weak Accept** | **Weak Accept** | **ACCEPT** |

### Meta Recommendation
**ACCEPT**

All three individual recommendations land at Weak Accept — the unanimous shortcut applies (all three Weak Accept or better → ACCEPT). The consensus-tier count agrees: no criterion at Poor, no consensus substance Weak (Novelty settles at Adequate by majority — R2 and R3 both Adequate against R1's Weak), and no fixable Weak. The paper clears the Accept bar.

The agreement is substantive, not a rubber stamp. All three reviewers independently converge on the same core merits — the controlled retrospective (31%→81% FP suppression at 96.7% TP retention), the contract hallucination propagation observation (12 by-design = 25%), the model-free COSINE>1.0 invariant subclass, and the honest scoping to boundary/validation compliance — and on the same two residual presentation issues, both fixable without new experiments: the cross-system generalization framing still outruns the adjudicated evidence, and TestVDB's marginal value over schema-driven / REST API testers is not positioned sharply enough. Neither threatens the verdict; the body already reports the honest evidence these revisions ask the framing to match.

Compared with the Round 13 re-review (R1 Accept / R2 Weak Accept / R3 Weak Accept), R1 has softened from Accept to Weak Accept this round: R1 now rates Novelty at Weak, driven by three [major, fixable] positioning items (cross-system overclaim, schema-fuzzer overlap on the boundary subset, no head-to-head comparison against RESTler/EvoMaster/Schemathesis). R1 nonetheless still leans in (Weak Accept), and its own prose concedes the novelty is "real" and CTS is "a real design contribution" — i.e., the evidence R1 lists is closer to Adequate than Weak. The other two reviewers rate Novelty Adequate, so the consensus holds at Adequate. The verdict is robust to R1's softer read.

### Priority Revisions
The main problems the author should fix, ranked by impact. Items 1–2 are each flagged by all three reviewers (cross-reviewer consensus); items 3–4 are double-reviewer flags that still warrant attention. All four are presentational sharpening — none requires new experiments; the body already contains the honest evidence.

1. **Sharpen the cross-system generalization framing throughout.** All three reviewers flag that the abstract / Contribution 1 still implies precision validation across five VDBMSs, while the data supports only Milvus (22 acknowledged) and Qdrant (11 acknowledged); Weaviate (3 acknowledged, 0 by-design), MeiliSearch (0), and Chroma (0) contribute near-zero adjudicated signal. The Round 13 abstract qualifier helped but is not prominent enough. Foreground the boundary in the abstract and Contribution 1: "adjudicated precision validated on Milvus and Qdrant; breadth probes on Weaviate, MeiliSearch, and Chroma probe generality of the attack surface without adjudicated precision." (R1 2.3/W1/Q1, R2 W1/1.4/5.4/Q4, R3 1.2/W1/Q2 — unanimous [major, fixable].)

2. **Position TestVDB's marginal value over schema-driven and REST API testers explicitly.** All three note the schema-fuzzer baseline (71% source-grounded precision on the boundary subset, which is 75% of yield) concedes that spec-driven fuzzing is genuinely effective where TestVDB's yield concentrates, and that no head-to-head comparison against RESTler/EvoMaster/Schemathesis is provided. Fix the framing, not the experiments: (a) quantify the non-boundary yield (8/36 = 22%) as the primary delta; (b) state that Schemathesis is blocked by Milvus not serving a standards-compliant OpenAPI spec (probed `/swagger`, `/openapi.json`, all 404), not by fundamental incompatibility; (c) position the novelty delta against RESTler/EvoMaster/Schemathesis in Related Work (semantic compliance + source-grounded falsification vs schema-conformance). (R1 2.4/2.5/W2/W3/Q2/Q3, R2 2.6/5.5/Q3, R3 2.3/W2/3.5/Q4 — unanimous [major, fixable].)

3. **State the three-anchor validated scope even more explicitly.** R1 and R2 note the contribution still reads as a three-anchor pipeline while only the source anchor is comprehensively validated (threat-model ablated as noisy on n=12: source-alone 9/12, threat-alone 6/12, union 11/12; reproduction not exercised). R3 rates the threat-model gap [major, unfixable] but accepts the honest "noisy complement" framing. The contribution statement already softens this; make it explicit in the abstract/contribution: "CTS with the source anchor validated; threat-model anchor explored as a noisy complement; reproduction anchor as future work." (R1 3.2/W4/Q4, R2 3.6/W3/Q2, R3 3.4/W3/Q3 — cross-reviewer; R3 [major, unfixable] bounds but does not block the verdict.)

4. **Present the single-layer counterfactual as a directional lift with its ground-truth caveat.** R2 and R3 note the 45.6% figure combines maintainer-adjudicated 36/52 with 27 live-reproduced, source-grounded FPs (a weaker proxy than maintainer triage). The body already labels it "directional lift at zero recall cost"; surface that caveat wherever the 45.6% appears so it is not read as a clean precision comparison. (R2 3.5/W5/Q1, R3 3.6/W4/Q5 — [minor, fixable].)

**Bottom line:** the paper clears the Accept bar on the strength of its controlled retrospective, the contract hallucination propagation finding, the model-free invariant subclass, and honest scoping. The two unanimous revisions are presentational fixes that bring the abstract/contribution framing and the competitor positioning in line with evidence the paper already reports honestly in the body; neither requires new experiments. The cross-system and three-anchor items are recurring (they surfaced in Round 13 too), which suggests the framing — not the evidence — is where residual reviewer discomfort sits; tightening it in the camera-ready would harden the Accept.

---

*Orchestrator note on verification:* All three reviewer drafts were read in full and their substantive claims (111 submissions, 52 adjudicated, 36 acknowledged = 28 fixed + 8 accepted, 12 by-design, 4 rejected, Milvus 51/22-acknowledged, Qdrant 26/11-acknowledged, Weaviate 30/3-acknowledged/0-by-design, 31%→81% FP suppression at 96.7% TP retention, 27/27 live-confirmed single-layer FPs, three-anchor 9/12/6/12/11/12 with 4/4 TP retention, canary 0/9, DeepSeek 2/3 over-strict reproduced, 45.6% vs 69.2%) were cross-checked against the paper text and match after patching. Each draft passed an independent checker; the verify-fix loop applied targeted patches to Reviewer 1 (Qdrant acknowledged 14→11, Weaviate by-design 1→0, "75% of yield"→"75% of acknowledged true positives", Section 5→4 for the contract-hallucination formalization) and Reviewer 3 (two broken N.M references in W2 and Q4 that pointed at a non-existent criterion 6, repointed to 2.3/3.5 and 2.3/1.2). Reviewer 2's checker reported three violations that, on grounding against the paper and the draft, were the checker's own hallucinations (it quoted draft text that does not exist in Reviewer 2's draft); Reviewer 2's draft was clean and required no patch. One residual sub-agent artifact is noted rather than patched: Reviewer 1's individual Overall (Weak Accept) alongside its Novelty=Weak tier — the rubric formula maps one substance Weak to Weak Reject, but R1's own evidence ("the novelty is real", "a real design contribution") supports Novelty=Adequate, which makes Weak Accept consistent; the meta verdict (ACCEPT) is robust either way since the consensus Novelty is Adequate by majority and all three reviewers lean in. Reviewers occasionally use their own internal section/table numbering rather than the paper's LaTeX labels; this is a sub-agent citation artifact that does not affect the verdict and is marked here per the 3-round verify-fix cap. Drafts and checker artifacts are preserved under `.paperpilot/review/.in-progress/` for inspection.

# Paper Review — TestVDB (Round 15 re-review)

**Paper:** TestVDB: Detecting API Compliance Defects in Vector Database Systems via Contract-Truth Separation
**Venue:** VLDB/PVLDB (acm-sigconf)
**Date:** 2026-07-12 (Round 15)
**Paper type:** technical

This round re-reviews the paper after the Round 14 follow-up (abstract cross-system + anchor-scope framing tightened; schema-fuzzer paragraph conclusion front-loaded as a topic sentence). Three independent reviewers (Domain Expert / Area Specialist / General Reviewer) reviewed the full stripped source in parallel; each draft passed an independent checker. Verify-fix artifacts are kept under `.paperpilot/review/.in-progress/`.

---

## Reviewer 1: Domain Expert

**Overall Recommendation:** Weak Accept

### Summary

TestVDB targets API compliance defects in Vector Database Management Systems (VDBMSs)—bugs where a VDBMS silently accepts inputs or behaviors that violate its documented contract. The paper introduces Contract-Truth Separation (CTS): separating LLM-generated contract assertions from a truth layer that falsifies them via maintainer-authority evidence (source code, prior PRs, by-design intent). The approach is motivated by "contract hallucination propagation": when one LLM family both generates a contract and judges compliance, hallucinated constraints are self-confirmed (25% of adjudicated submissions were by-design). TestVDB produced 111 issues across five VDBMSs; maintainers acknowledged 36 (28 fixed). On a controlled retrospective over 52 adjudicated candidates, the dev-reviewer's source anchor lifts false-positive suppression from 31% to 81% while retaining 96.7% of true positives. The strongest technical finding is a subclass of model-free invariant oracles (e.g., COSINE distance >1.0 for identical vectors) that violate hard mathematical bounds.

### Core Strengths

- **S1:** Contract-Truth Separation design principle isolates LLM-generated assertions from maintainer-authority truth, addressing self-confirmation bias in single-layer LLM judgment — see 2.1, 2.2.
- **S2:** Model-free invariant oracle subclass (COSINE>1.0 cases) is the paper's strongest technical finding—language/LLM-independent, reproduces across vendors, violates expressible mathematical bounds — see 2.3.
- **S3:** Controlled retrospective (52-candidate same-population blind re-triage) provides clean evidence for dev-reviewer's FP suppression contribution (31%→81%, 2.6× lift) — see 3.1.
- **S4:** Honest scope boundary reporting: 75% of yield is boundary/validation compliance; crash bugs excluded by design; soft result-correctness (ANN recall/ranking) acknowledged as open — see 1.1, 1.3.

### Core Weaknesses

- **W1:** Cross-system generalization overclaimed — see 1.2. Paper claims cross-system generalization, but adjudicated precision is validated only for Milvus and Qdrant. Weaviate (30 pending), MeiliSearch (3 excluded), and Chroma (1 pending) contribute near-zero adjudicated signal. These are breadth probes on attack surface, not precision evidence.
- **W2:** Schema-fuzzer baseline concedes TestVDB is not uniquely effective on boundary/validation subset — see 2.4. Hand-written spec-driven fuzzer achieves 71% source-grounded post-filter precision on Milvus boundaries (5/7 genuine violations). TestVDB's marginal value lies elsewhere: (a) non-boundary yield (8/36 TPs), (b) CTS FP-suppression, (c) spec-gap bugs.
- **W3:** Threat-model anchor validation weak on n=12 — see 2.6. Threat-alone shows 50% FP suppression (6/12) vs source-alone 75% (9/12), unstable across runs (one boundary FP flipped). Union reaches 92% (11/12), but noise and instability remain concerns at small scale.
- **W4:** Single-layer counterfactual end-to-end arm not independently adjudicated — see 3.2. The 45.6% single-layer precision combines maintainer-adjudicated baseline with 27 live-reprobed, source-grounded FPs. Maintainer triage might reclassify some of the 27, and the arm is bounded to one feedback cycle.
- **W5:** Three-anchor design claimed as contribution despite limited validation — see 5.2. Paper presents dev-reviewer's three-anchor architecture as a contribution, but reproduction anchor remains design-level (not evaluated), and threat-model anchor is noisy/unstable (n=12). Only source anchor is empirically validated as primary.

### Detailed Assessment

1. **Significance** — Adequate

   - **1.1** The problem is real and motivated: VDBMSs underpin LLM applications at scale; 43% of VDBMS bugs are incorrect-behavior (vs. 23% crash/hang); API compliance defects corrupt query semantics without crashing — see Introduction, roadmap taxonomy. This is a meaningful slice of the VDBMS reliability problem.
   - **1.2 [major, fixable]** Cross-system generalization overclaimed. The abstract claims "TestVDB produced 111 issues across five VDBMSs" and positions cross-system generalization as a contribution. However, adjudicated precision is validated only for Milvus and Qdrant. Weaviate (30 pending, 3 acknowledged), MeiliSearch (3 excluded), and Chroma (1 pending) contribute near-zero adjudicated signal. The evaluation section honestly acknowledges Weaviate/MeiliSearch/Chroma as "breadth probes on the attack surface, not as precision evidence," but the abstract framing should lead with "validated on Milvus and Qdrant" upfront.
   - **1.3** Practical impact is demonstrated but modest: 36 maintainer acknowledgments (28 fixed) across Milvus and Qdrant show real defects found. However, 75% of yield is boundary/validation, which the schema-fuzzer baseline shows is tractable via spec-driven approaches. The non-boundary yield (8/36 TPs: diagnostic-quality, state/logic, result-correctness) and CTS FP-suppression layer are the truly novel contributions in practice.

2. **Novelty** — Adequate

   - **2.1** Contract-Truth Separation design principle is novel and addresses a real failure mode (contract hallucination propagation). The 25% by-design rate (12/48 adjudicated submissions) demonstrates that single-layer LLM judgment self-confirms hallucinated constraints. The mitigation—separating assertion layer from truth layer with source-grounded falsification—is a valid delta over prior LLM-as-judge patterns. The COSINE>1.0 counterfactual (feeding same doc passages to DeepSeek reproduces over-strict constraints in 2/3 clean cases) shows the phenomenon is largely task-intrinsic, not GLM-specific.
   - **2.2 [major, unfixable]** Cross-system generalization overclaimed (same issue as 1.2, but under Novelty). Contribution #1 claims "first end-to-end realization...with adjudicated precision validated on Milvus and Qdrant" and "breadth probes on three further VDBMSs." This is technically accurate but the abstract's framing of cross-system generalization outruns the validated base. The adjudicated precision evidence exists only for Milvus and Qdrant; Weaviate/MeiliSearch/Chroma are attack-surface probes only. This is unfixable because the data is what it is—those systems' maintainers did not adjudicate—but it warrants attention due to overclaiming in the abstract.
   - **2.3** Model-free invariant oracle subclass is the strongest novelty claim. The COSINE>1.0 bug (identical vectors returning distance >1.0) violates a hard mathematical bound (cosine similarity ∈ [-1,1]), reproduces on both Milvus and Qdrant, and needs no LLM judgment. The same class catches incomplete index results (2/25 matching points returned) and payload filters returning points with missing fields. This contribution is solid.
   - **2.4 [major, fixable]** Schema-fuzzer baseline concedes TestVDB is not uniquely effective on boundary/validation subset. The hand-written boundary-value fuzzer (no LLM): 19 probes surfaced 7 API-accepted candidates, source-grounded post-filter classifies 5/7 as genuine violations (71% precision). This concedes that on the boundary/validation subset (75% of yield), a spec-driven fuzzer is genuinely effective. TestVDB's marginal value lies where the fuzzer cannot reach: (a) state/logic, diagnostic, result-correctness probes (8/36 TPs are non-boundary); (b) CTS FP-suppression; (c) spec-gap bugs. The paper already reports this honestly; the positioning in the abstract ("first LLM-driven detector") could acknowledge that boundary fuzzing is not exclusively LLM-dependent.
   - **2.5** LLM-driven contract extraction bypasses spec-authoring bottleneck. Schemathesis requires standards-compliant OpenAPI specification; VDBMS REST endpoints do not serve /swagger or /openapi.json (probes returned 404). LLM extraction from docs enables TestVDB where schema-driven fuzzers cannot be applied off-the-shelf. This is a valid deployment advantage, though not a fundamental novelty barrier (hand-authored specs would enable Schemathesis).
   - **2.6 [minor, fixable]** Threat-model anchor validation weak on n=12. The ablation on 12 Milvus FPs: source-alone 9/12 (75%), threat-alone 6/12 (50%, unstable—one boundary FP flipped), union 11/12 (92%). All conditions retain 4/4 TPs. The paper already hedges this honestly ("we do not claim the three-anchor design as a clean validated contribution"), so this is minor.

3. **Soundness** — Adequate

   - **3.1** Controlled retrospective is methodologically sound. Re-triage of all 52 maintainer-adjudicated candidates (36 TP, 16 FP) under two blind conditions on the same population: claim-only (4-judge layer) vs. source-grounded (dev-reviewer's source anchor). Source-grounding lifts FP suppression from 5/16 (31%) to 13/16 (81%, 2.6×) while retaining 29/30 TPs (96.7%, n=30). This is the strongest evidence for the dev-reviewer's contribution.
   - **3.2 [major, fixable]** Single-layer counterfactual end-to-end arm not independently adjudicated. The 45.6% single-layer precision combines maintainer-adjudicated baseline (36/52) with 27 live-reprobed, source-grounded FPs (all 27 confirmed live, over-kill 0/27). However, maintainer triage might reclassify a few of the 27, and the arm is bounded to one feedback cycle. The paper treats the 31%→81% same-population result as the cleaner head-to-head and reports 45.6% as directional, which is appropriate hedging.
   - **3.3** Aggregate maintainer-adjudicated precision (69.2%) is reported with sensitivity analysis. The interval [43.9%, 80.5%] under pending-resolution sensitivity is proper handling of selection bias. The breakdown (36 acknowledged, 12 by-design, 4 rejected out of 52 adjudicated) is transparent.
   - **3.4 [minor, fixable]** Threat-model anchor ablation has wiring gap confound in earlier experiment. The initial negative should not have been reported as "exploratory" without first verifying wiring. Honest reporting, but the re-run after the fix produced the n=12 ablation above.
   - **3.5 [minor, fixable]** Schema-fuzzer comparison omits Schemathesis head-to-head. A head-to-head using hand-authored OpenAPI specs for Milvus endpoints would strengthen the "bypasses spec-authoring bottleneck" claim. The hand-written boundary-value fuzzer is acceptable but less direct.

4. **Verifiability** — Adequate

   - **4.1** Artifact declared and reachable. Anonymized artifact at https://anonymous.4open.science/r/testvdb-anon-D644/, including full system, reproducible dataset, five VDBMS targets, and all 111 submissions with maintainer outcomes. Implementation: 20 LLM agents served by GLM-5.2. Full prompts, pinned target versions, and per-target cost accounting are in the artifact. This meets the bar.
   - **4.2** Text describes procedural flow sufficiently. The five-stage pipeline and RQ1–RQ4 methodology are described with sufficient detail to follow the analysis. Figure 1 (pipeline), yield table, scope table, and baselines table support the text.

5. **Presentation** — Adequate

   - **5.1 [minor, fixable]** Abstract overstates cross-system generalization (see 1.2, 2.2). The abstract should lead with "validated on Milvus and Qdrant" rather than with "five VDBMSs."
   - **5.2 [minor, fixable]** Three-anchor design overemphasized in contributions (see W5). Contribution #2 should emphasize source-grounded verification as the primary validated contribution, with threat-model and reproduction anchors framed as exploratory complements.
   - **5.3** Structure is logical and readable. Introduction → Background → Approach → Hallucination → Evaluation (RQ1–RQ4) → Related Work → Conclusion is a clear flow. The honest scope boundary reporting and sensitivity analysis are strong presentation elements.
   - **5.4 [minor, fixable]** Minor notation inconsistencies. Wilson CI is not computed for the 96.7% TP-retention ratio; the footnote on different TP bases across conditions could be clearer in the main text.

### Questions for Authors

- **Q1:** Would the authors consider scoping the abstract's cross-system claim explicitly to Milvus and Qdrant in the first sentence, rather than leading with "five VDBMSs" — this would address reviewer concerns about overclaiming (items 1.2, 2.2).
- **Q2:** For the single-layer counterfactual, do the authors have plans to submit a fresh single-layer cohort for independent maintainer adjudication to strengthen the 45.6% baseline figure — item 3.2's rating would move from Adequate toward Excellent with this validation.
- **Q3:** Can the authors clarify whether a head-to-head comparison with Schemathesis using hand-authored OpenAPI specs for Milvus endpoints is planned — this would strengthen the "bypasses spec-authoring bottleneck" claim (item 3.5).
- **Q4:** Would the authors consider emphasizing source-grounded verification as the primary validated contribution in Contribution #2, with threat-model and reproduction anchors framed as exploratory complements — this would address item 5.2's concern about overemphasizing the three-anchor design.

---

## Reviewer 2: Area Specialist

**Overall Recommendation:** Weak Accept

**Specialty areas chosen:** (1) LLM-driven testing / LLM-as-oracle / multi-agent debate, (2) Database/API testing (REST fuzzing, metamorphic, differential).

### Summary

TestVDB targets API compliance defects in Vector Database Management Systems (VDBMSs)—bugs where a VDBMS silently accepts inputs or behaviors that violate its documented contract. The paper presents a five-stage LLM-driven pipeline that extracts contracts from API documentation, generates attack candidates, adjudicates them via a four-judge debate, and applies Contract-Truth Separation (CTS) through a dev-reviewer agent that falsifies LLM-generated assertions against maintainer-authority evidence (source code, prior PRs, issue history). The key innovation is motivated by contract hallucination propagation: when one LLM family both generates a contract and judges compliance, hallucinated constraints are self-confirmed—evidenced by 25% of adjudicated submissions being marked by-design. TestVDB produced 111 issues across five VDBMSs; 52 have been maintainer-adjudicated with 36 acknowledged (28 fixed). On a controlled retrospective over the same 52-candidate pool, the dev-reviewer's source anchor lifts false-positive suppression from 31% to 81% while retaining 96.7% of true positives. The work targets boundary/validation compliance (75% of yield) and complements crash-focused fuzzing like VDBFuzz.

### Core Strengths

- **S1:** The contract hallucination propagation observation is a novel empirical finding in LLM-driven testing — see 2.1, 2.2. The 25% by-design rate (12 of 48 adjudicated submissions) demonstrates that when one LLM family generates and judges, hallucinated constraints are self-confirmed. This is a real problem that motivates the CTS design.
- **S2:** Contract-Truth Separation (CTS) and the dev-reviewer's source-grounded verification anchor are well-validated — see 2.2, 3.1. The controlled retrospective (31%→81% FP suppression, 96.7% TP retention) is a strong within-study ablation that isolates the dev-reviewer's contribution on the same 52-candidate population.
- **S3:** The paper's positioning against existing REST API fuzzers (RESTler, EvoMaster, Schemathesis) is honest and empirically supported — see 2.3. The concrete 404 probe results on Milvus's `/swagger` and `/openapi.json` endpoints demonstrate that schema-driven tools cannot be applied off-the-shelf to VDBMS REST APIs, justifying TestVDB's LLM-based contract extraction.
- **S4:** The model-free invariant oracles subclass (cosine similarity bounded in [-1,1], incomplete index results, payload filter violations) is the paper's most defensible technical finding — see 3.3. These violate hard mathematical bounds, reproduce across vendors, and depend on no LLM judgment, making them the least contingent on agent-design choices.
- **S5:** The paper is transparent about its scope and limitations — see 3.2, 5. It reports sensitivity intervals under pending resolution ([43.9%, 80.5%]), excludes 29 closed-no-label submissions rather than inflating precision, and acknowledges that soft result-correctness (ANN recall, ranking) remains open.

### Core Weaknesses

- **W1:** Missing related work in LLM-driven REST API testing — see 2.5. The paper omits LlamaRestTest (2025), which fine-tunes smaller LLMs for REST API testing and demonstrates that fine-tuning enables smaller models to outperform larger models in detecting actionable parameter-dependency rules. This is recent concurrent work that TestVDB should cite and position against.
- **W2:** Missing related work in REST API fuzzing — see 2.6. The paper omits recent state-of-the-art REST fuzzing tools (foREST, MINER, DynER) that have advanced beyond RESTler and EvoMaster in test coverage and error detection. These are relevant comparators for completeness in Related Work.
- **W3:** Cross-system generalization claims are over-broad — see 1.4. The paper claims "cross-system generalization" based on 111 submissions across five VDBMSs, but 77 of 111 submissions are from Milvus (51) and Qdrant (26), while Weaviate (30), MeiliSearch (3), and Chroma (1) contribute near-zero adjudicated signal. The claim should be scoped to Milvus and Qdrant, with Weaviate/MeiliSearch/Chroma as breadth probes rather than statistical evidence.
- **W4:** Single-layer and single-LLM baseline arms use different ground truths, complicating direct comparison — see 3.7. The single-layer arm (45.6% precision) combines maintainer-adjudicated baseline (36/52) with 27 live-re-probed, source-grounded FPs, but the residual gap is that maintainer triage might reclassify a few of the 27. This asymmetry in ground truth is noted but remains a confounding factor.
- **W5:** Threat-model anchor evaluation is under-powered — see 3.6. The threat-model anchor ablation (n=12 Milvus FPs) shows it is a noisy complement (union with source suppresses 11/12, but threat-alone is unstable and over-fires on state/concurrency FPs). The paper honestly reports this as an exploratory result, but the small sample size limits the strength of claims about the three-anchor design.

### Detailed Assessment

1. **Significance** — Adequate

   - **1.1** The problem is real and under-served. VDBMSs underpin LLM applications, yet 43% of VDBMS bugs are incorrect-behavior defects that lack practical oracles. Current fuzzers like VDBFuzz detect only crashes, leaving the majority without a practical oracle. The roadmap flags this as the central open challenge.
   - **1.2** API compliance defects are a practically important subclass. The paper provides concrete examples (accepting nprobe=0, silently normalizing shardsNum=-1, returning success where docs prescribe rejection) that corrupt query semantics, lower recall, and expand the attack surface.
   - **1.3 [major, fixable]** The significance is bounded by the narrow scope within Incorrect Behavior. TestVDB targets 75% of yield as boundary/validation compliance, plus diagnostic, state/logic, and a small result-correctness subset. It excludes Crash (by design), Performance, and Build. The paper honestly reports this scope, but the contribution is therefore a slice of the incorrect-behavior problem, not a full solution. The positioning against VDBFuzz (complementary) is appropriate, but the impact is narrower than the roadmap's open challenge for "an oracle for evaluating the correctness of vector search results" (soft recall/ranking).
   - **1.4 [minor, fixable]** Cross-system generalization is claimed broadly but supported narrowly. 77 of 111 submissions are from Milvus (51) and Qdrant (26), with Weaviate (30), MeiliSearch (3), and Chroma (1) contributing near-zero adjudicated signal. The abstract later qualifies: "We claim cross-system generalization of the method's attack surface, not of its precision, which the data supports only for Milvus and Qdrant." This honesty is commendable, but the initial broad claim should be scoped to avoid overstating.

2. **Novelty** — Adequate

   - **2.1** Contract hallucination propagation is a novel observation. The paper identifies a specific failure mode in LLM-driven testing: when one LLM family both generates a contract and judges compliance, hallucinated constraints are self-confirmed. The 25% by-design rate (12 of 48 adjudicated submissions) is empirical evidence. The contract counterfactual (feeding the same raw doc passages to a different LLM family reproduces over-strict constraints in 2/3 of clean cases) supports that this is largely task-intrinsic.
   - **2.2** Contract-Truth Separation (CTS) is a novel design principle. The dev-reviewer agent falsifies LLM-generated assertions against maintainer-authority evidence via three anchors. The source anchor is validated as the primary anchor in the controlled retrospective (31%→81% FP suppression, 96.7% TP retention). This is a clear delta over single-layer LLM judgment.
   - **2.3** The paper's positioning against existing work is accurate. Verified against RESTler, EvoMaster, and Schemathesis: TestVDB is complementary because these tools require OpenAPI specs (which VDBMS REST endpoints do not serve, as empirically probed) and use crash oracles (which cannot detect non-crash compliance defects). The paper's 404 probe results on `/swagger` and `/openapi.json` are concrete evidence.
   - **2.4** Multi-agent debate design is well-instantiated. The four-judge debate draws on du2023improving and he2025lma but is tailored to the VDBMS compliance domain. The paper correctly notes that the contract-hallucination failure mode is not discussed in these prior works as a specific LLM-as-judge pattern.
   - **2.5 [major, fixable]** Missing related work in LLM-driven REST API testing. The paper omits LlamaRestTest (2025), which fine-tunes smaller LLMs for REST API testing and demonstrates that fine-tuning enables smaller models to outperform larger models in detecting actionable parameter-dependency rules. TestVDB should cite this work and position its approach (GLM-5.2-based multi-agent system with CTS) against LlamaRestTest's fine-tuning approach.
   - **2.6 [major, fixable]** Missing related work in REST API fuzzing. The paper omits recent REST API fuzzing tools that have advanced beyond RESTler and EvoMaster: foREST (2022, tree-based approach), MINER (2023, hybrid data-driven), and DynER (2024, dynamic error response guidance). These tools are relevant comparators for completeness in Related Work, especially foREST which improves code coverage by 11.5–82.5% over EvoMaster and RESTler.

3. **Soundness** — Adequate

   - **3.1** The controlled retrospective is a strong within-study ablation. Re-triaging all 52 maintainer-adjudicated candidates (36 TP, 16 FP) under two blind conditions (claim-only vs. source-grounded) on the same population shows that adding the source anchor lifts FP suppression from 5/16 (31%) to 13/16 (81%, 2.6×) while retaining 29/30 TPs (96.7%). This isolates the dev-reviewer's contribution cleanly.
   - **3.2** The maintainer-adjudicated precision is well-reported. 69.2% precision (36/52 adjudicated) with sensitivity interval [43.9%, 80.5%] under pending resolution (30 pending, 29 excluded). The paper excludes 29 closed-no-label submissions rather than inflating precision, which is honest. Wilson 95% CI is also provided.
   - **3.3** The model-free invariant oracles are robust. COSINE distance >1.0 for identical vectors, incomplete index results (2/25 returned), and payload filter violations violate hard mathematical bounds, reproduce across vendors (Milvus and Qdrant), and depend on no LLM judgment. This is the paper's most defensible technical finding.
   - **3.4** Single-layer counterfactual is a valid end-to-end arm. Re-running generation plus four-judge debate yields 15 probes with 3 confirmed candidates (2 TP, 1 FP). The 27 dev-reviewer-killed candidates were all re-probed live and source-grounded, confirming them as true FPs (27/27 live, over-kill 0/27). The resulting single-layer precision of 45.6% vs. TestVDB's 69.2% is a valid directional comparison at zero recall cost.
   - **3.5** The schema-aware boundary fuzzer baseline concedes boundary-finding limits. A hand-written boundary fuzzer (no LLM) surfaced 7 API-accepted candidates (5 genuine violations, 2 by-design silent defaults). The paper acknowledges that on the boundary/validation subset (75% of yield), a spec-driven fuzzer is genuinely effective, and TestVDB's marginal value lies in state/semantic probes and CTS FP-suppression. This is honest.
   - **3.6 [minor, fixable]** Threat-model anchor evaluation is under-powered. The ablation on 12 Milvus FPs shows threat-alone suppresses 6/12 (50%, unstable across runs) vs. source-alone 9/12 (75%), with union 11/12 (92%). The paper honestly reports this as an exploratory result with n=12, but the small sample size limits claims about the three-anchor design. The threat anchor catches boundary-default residuals but over-fires on state/concurrency FPs.
   - **3.7 [minor, fixable]** Baseline arms use different ground truths. The single-layer arm (45.6%) combines maintainer-adjudicated baseline (36/52) with 27 live-re-probed, source-grounded FPs, while the single-LLM arm (25.5%) uses LLM self-judgment, and the schema fuzzer arm (71%) uses live re-probe plus source grounding. The paper notes this asymmetry, but it complicates direct numerical comparison. The within-study same-population retrospective (31%→81%) is cleaner.
   - **3.8 [minor, fixable]** Discovery recall is not fully measured. The paper reports 96.7% TP retention at the judgment layer but notes that end-to-end discovery recall requires running TestVDB against bug-present old versions. A pilot on 9 held-out pre-2024 bugs found current docs cover 6/9 contracts (67%). The paper honestly bounds this gap, but full recall measurement remains future work.

4. **Verifiability** — Adequate

   - **4.1** The paper declares an anonymized artifact at https://anonymous.4open.science/r/testvdb-anon-D644/ (link declared as reachable; I did not clone it). The artifact includes the full system, reproducible dataset, five VDBMS targets, and all 111 submissions with maintainer outcomes.
   - **4.2** The evaluation description is sufficient to follow the work. The paper describes the five-stage pipeline, agent configurations (20 agents, GLM-5.2 backbone, high/low budget), target versions (Milvus 2.6.19 for ablations, full matrix in artifact), and cost (order of 10^4 LLM calls total, ~10^3 calls per target). The retrospective protocol (blind re-triage, label-isolated agents) is clear.
   - **4.3** The paper reports all critical outcomes with confidence intervals. Maintainer-adjudicated precision includes Wilson 95% CI, and the sensitivity interval under pending resolution is provided. The threat-model anchor instability is explicitly reported (one boundary FP flipped between runs).
   - **4.4 [minor, fixable]** Some procedural details are missing. The paper does not report the precise candidate-to-submission ratio (how many raw candidates the pipeline generates before the novelty gate filters down to 111 submissions), leaving submission-selection bias only roughly bounded.
   - **4.5 [minor, fixable]** LLM call cost and wall-clock are order-of-magnitude estimates. Precise per-token accounting and wall-clock measurements are deferred to the artifact.

5. **Presentation** — Adequate

   - **5.1** The paper is well-structured and readable. The five-stage pipeline is clearly described with a figure showing the assertion layer (LLM) and truth layer (counter-evidence). The core contributions are enumerated in the Introduction.
   - **5.2** The paper is honest about limitations. It reports sensitivity intervals, excludes closed-no-label submissions, acknowledges that soft result-correctness remains open, and scopes cross-system claims to Milvus and Qdrant.
   - **5.3** Figures and tables are clear. Figure 1 (pipeline) cleanly separates assertion/truth layers. The yield table, scope table, and baselines table are well-formatted.
   - **5.4 [minor, fixable]** Some notation is dense. The threat-model anchor wiring gap description is technical and could be clearer. The distinction between `developer_cognition.json` (wrong file) and `threat_model.json` (correct file) could be expanded for clarity.
   - **5.5 [minor, fixable]** Minor language and formatting issues. Some sentences are long and could be split for readability (e.g., the single-layer counterfactual paragraph). These do not obstruct understanding.

### Questions for Authors

- **Q1:** The paper cites VDBFuzz as the first dedicated VDBMS fuzzer, but the literature search for "VDBFuzz" returned no results. Can you provide the full citation (authors, title, venue, year) for VDBFuzz to verify this claim? — Intended effect: If VDBFuzz is a real 2026 paper, item 1.1's positioning would be strengthened; if it's a placeholder, the claim needs revision.
- **Q2:** The paper mentions that GLM-5.2 may have seen pre-2024 Milvus GitHub source in training, which would inflate the source anchor's apparent power. The memorization canary (0/9 issues recalled at issue-specificity) is presented as evidence against contamination. Can you clarify whether the canary test was run on the bare GLM-5.2 model (no pipeline, no docs) as stated, and whether the 9 held-out bugs include the cosine>1.0 case? — Intended effect: Clarification would strengthen the contamination defense in item 3.8.
- **Q3:** The paper reports that 75% of yield is boundary/validation compliance. Can you provide the exact breakdown of the 36 acknowledged TPs by defect type to support the "75% boundary" claim? — Intended effect: Providing the exact count (e.g., 27 of 36 = 75%) would strengthen item 1.3's scope claim.
- **Q4:** The threat-model anchor ablation shows threat-alone is unstable across runs. Can you quantify the instability (e.g., how many of the 12 Milvus FPs flipped between runs, and which classes they belong to)? — Intended effect: Quantifying instability would clarify the limitations in item 3.6.
- **Q5:** The paper omits LlamaRestTest (2025) from Related Work. Can you explain how TestVDB's GLM-5.2-based multi-agent approach with CTS compares to LlamaRestTest's fine-tuning approach for LLM-driven REST API testing? — Intended effect: Adding this comparison would address the missing related work weakness and potentially strengthen novelty.

---

## Reviewer 3: General Reviewer

**Overall Recommendation:** Weak Accept

### Summary
TestVDB introduces an LLM-driven approach for detecting API compliance defects in Vector Database Management Systems (VDBMSs), a class of bugs where systems silently accept inputs violating documented contracts. The core contribution is Contract-Truth Separation (CTS), which isolates LLM-generated contract assertions from a maintainer-authority truth layer that falsifies them through source-grounded verification and other anchors. The system produced 111 issues across five VDBMSs; maintainers acknowledged 36 (28 fixed). A controlled retrospective over 52 adjudicated candidates shows the dev-reviewer's source anchor lifts false-positive suppression from 31% to 81% while retaining 96.7% of true positives. The paper identifies a contract hallucination propagation problem where LLMs that both generate contracts and judge compliance self-confirm hallucinated constraints. Evaluation shows 69.2% maintainer-adjudicated precision (within [43.9%, 80.5%] sensitivity interval). The work targets boundary/validation compliance and complements crash-focused fuzzing tools like VDBFuzz.

### Core Strengths
- **S1:** Clear problem articulation and well-motivated design — see 1.1, 1.2
- **S2:** Rigorous evaluation methodology with multiple complementary ablations — see 3.1, 3.2
- **S3:** Honest scope delimitation and threat identification — see 3.5, 5.1

### Core Weaknesses
- **W1:** Cross-system generalization overclaimed — see 2.2 [major, unfixable]
- **W2:** Threat-model anchor contribution inadequately substantiated — see 3.3 [major, fixable]
- **W3:** Related work coverage gaps on REST API testing — see 2.4 [minor, fixable]

### Detailed Assessment

1. **Significance** — Adequate
   - **1.1** The paper addresses a well-motivated problem: incorrect-behavior bugs (43.0%) substantially outnumber crash/hang bugs (23.1%) in VDBMSs, yet existing tools like VDBFuzz only target crashes. The compliance-defect slice is a tractable starting point for the broader incorrect-behavior challenge, making this a meaningful contribution.
   - **1.2** The contract-hallucination propagation observation is a significant insight for LLM-driven testing: when one model family both generates contracts and judges compliance, hallucinated constraints are self-confirmed (25% of adjudicated submissions marked by-design). This identifies a real failure mode in LLM-as-judge patterns.
   - **1.3 [minor, fixable]** The work's positioning is somewhat narrow: it targets boundary/validation compliance (75% of yield) and excludes crash bugs (complementary to VDBFuzz), performance, and build defects. This is a bounded slice of the incorrect-behavior problem space, not a comprehensive solution.
   - **1.4** The practical impact is demonstrated through 36 maintainer acknowledgments (28 fixed), but the cross-system validation is limited (see Novelty assessment below).

2. **Novelty** — Adequate
   - **2.1** Contract-Truth Separation (CTS) is presented as novel, and from the paper's own claims, it appears distinct from prior work. The separation of LLM-generated assertions from a maintainer-authority truth layer that falsifies them through source-grounded verification is a clear design contribution.
   - **2.2 [major, unfixable]** The cross-system generalization claim is overreaching. The paper acknowledges that adjudicated signal concentrates on Milvus and Qdrant, with "Weaviate, MeiliSearch, and Chroma serve as breadth probes on the attack surface, not as precision evidence" (abstract). However, the title and abstract still position this as work on "five VDBMSs," and the Related Work section frames it broadly without acknowledging the Milvus/Qdrant precision validation limit. This creates a gap between what's claimed (cross-VDBMS applicability) and what's empirically substantiated (precision validated only on two systems).
   - **2.3** The dev-reviewer's three-anchor design (clean reproduction, source-grounded verification, threat-model cross-check) appears novel within LLM-driven testing, though the paper does not provide a comprehensive survey of REST API testing tools to establish how this differs from existing stateful REST fuzzers like RESTler or EvoMaster.
   - **2.4 [minor, fixable]** Related work coverage on REST API testing is thin. The paper cites RESTler and EvoMaster but does not deeply engage with how their stateful fuzzing approaches compare to TestVDB's contract-semantics focus. Schemathesis is mentioned only in passing regarding OpenAPI unavailability; a more thorough survey of schema-driven REST testing would better position the contribution.

3. **Soundness** — Adequate
   - **3.1** The main claims are supported by appropriate methods. The controlled retrospective (RQ3) on the same 52-candidate population provides clean head-to-head comparison between claim only and source-grounded conditions, showing FP suppression lift from 31% to 81% with 96.7% TP retention. This is a well-designed ablation.
   - **3.2** The single-layer counterfactual is rigorously validated: the paper re-probed all 27 dev-reviewer-killed candidates live on fresh containers and source-grounded each, confirming all 27 as true FPs (0/27 over-kill). This live verification strengthens the baseline comparison beyond LLM-proxy judgment.
   - **3.3 [major, fixable]** The threat-model anchor's contribution is inadequately substantiated. On 12 Milvus FPs, source-alone suppresses 9/12 (75%), threat-alone 6/12 (50%), and their union 11/12 (92%). However, the paper itself notes that threat-alone is "unstable across runs" and "over-fires on state/concurrency FPs." With n=12 and observed instability, claiming the three-anchor design as a validated contribution is premature. The paper is honest about this limitation, but the anchor occupies significant design space without strong empirical support.
   - **3.4** The schema-fuzzer baseline (RQ3) is well-executed: 19 hand-written probes surfaced 7 API-accepted candidates, with 5 classified as genuine violations after source-grounding (71% post-filter precision). This provides a concrete comparison point for TestVDB's marginal value (non-boundary yield + FP-suppression) rather than claiming boundary-finding novelty.
   - **3.5** Threats to validity are thoroughly acknowledged: maintainer acknowledgment as weak ground truth, selection bias from novelty-gate filtering, LLM variance (99.1% agreement on re-adjudication), and contamination (GLM-5.2 may have seen pre-2024 Milvus source; memorization canary shows 0/9 issues recalled at specificity). This honesty strengthens credibility.

4. **Verifiability** — Adequate
   - **4.1** The paper provides sufficient detail to follow the evidence production. The five-stage pipeline is clearly described (Figure 1), and all agent roles and configurations are specified (GLM-5.2 backbone, high-budget vs low-budget configurations, default sampling with no temperature override).
   - **4.2** Cost and reproducibility information is provided: total LLM-call budget on the order of 10^4 calls (~10^7 tokens), per-target pipeline cost on the order of 10^3 calls (~2×10^6 tokens), and wall-clock dominated by dev-reviewer's source-grounding and Docker re-probes.
   - **4.3** The paper declares an anonymized artifact repository (https://anonymous.4open.science/r/testvdb-anon-D644/) with full agent prompts, target versions, and per-token accounting. This is strong for reproducibility.
   - **4.4 [minor, fixable]** Some implementation details are sparse: the exact "low-budget" vs "high-budget" GLM-5.2 configuration differences are mentioned as "context window and max output tokens" but not specified numerically. The threat-model artifact structure is described but not shown.

5. **Presentation** — Adequate
   - **5.1** The paper is well-structured with clear sections: Introduction, Background, Approach, Contract Hallucination, Evaluation, Related Work, Conclusion. The flow is logical and easy to follow.
   - **5.2** Figures and tables are effective. Figure 1 clearly visualizes the assertion-truth layer separation. The yield table and baseline comparison table present data clearly with appropriate nuance.
   - **5.3 [minor, fixable]** The writing is generally clear but occasionally dense. Some sentences are long and packed with subordinate clauses. A few editorial passes would improve readability.
   - **5.4 [minor, fixable]** Notation is mostly consistent, but some minor issues exist: "nprobe=0" appears in text without backticks in some instances; CI reporting format switches between Wilson 95% CI and sensitivity intervals without explicit signposting.
   - **5.5 [minor, fixable]** The baseline comparison table groups arms by ground-truth tier but uses "37%" for the schema-fuzzer row with a dagger footnote explaining this is a probe→accept rate, not candidate precision. This creates potential misreading—the dagger is necessary but the row could be labeled more clearly (e.g., "37% (probe-accept rate)").

### Questions for Authors
- **Q1:** Can you clarify the "high-budget" vs "low-budget" GLM-5.2 configuration differences numerically (context window size, max output tokens)? — This would address 4.4 and strengthen reproducibility claims.
- **Q2:** For Related Work, can you add a paragraph deep-comparing TestVDB's semantic compliance focus against RESTler/EvoMaster's stateful REST fuzzing approaches? — This would partially address 2.4 and better position the novelty.
- **Q3:** The threat-model anchor shows instability across runs (one FP flipped between runs). Can you characterize what causes this instability (e.g., prompt variance, sampling nondeterminism) and whether architectural fixes are planned? — This would clarify whether 3.3's limitation is inherent or improvable.
- **Q4:** In the abstract, you state "Weaviate, MeiliSearch, and Chroma serve as breadth probes on the attack surface, not as precision evidence." Can you make this scope delimitation more prominent earlier (e.g., in the Contributions list)? — This would mitigate the 2.2 overclaim concern by signaling the empirical boundary upfront.

---

## Meta-Review

### Criterion Consensus

| Criterion | Reviewer 1 | Reviewer 2 | Reviewer 3 | Meta-Review |
|---|---|---|---|---|
| Significance | Adequate | Adequate | Adequate | **Adequate** |
| Novelty | Adequate | Adequate | Adequate | **Adequate** |
| Soundness | Adequate | Adequate | Adequate | **Adequate** |
| Verifiability | Adequate | Adequate | Adequate | **Adequate** |
| Presentation | Adequate | Adequate | Adequate | **Adequate** |
| **Recommendation** | **Weak Accept** | **Weak Accept** | **Weak Accept** | **ACCEPT** |

### Meta Recommendation
**ACCEPT**

All three individual recommendations land at Weak Accept — the unanimous shortcut applies (all three Weak Accept or better → ACCEPT). The consensus-tier count agrees unanimously: every criterion sits at Adequate across all three reviewers, with no Poor and no substance Weak. The paper clears the Accept bar.

The improvement over Round 14 is real and traceable. Round 14 had a split on Novelty (R1 Weak / R2 Adequate / R3 Adequate, consensus Adequate by majority); after the Round 14 follow-up tightened the abstract's cross-system and anchor-scope framing and front-loaded the schema-fuzzer marginal-value conclusion, Round 15 returns **Novelty at unanimous Adequate**. R1 in particular lifted its Novelty read from Weak to Adequate, explicitly crediting the contract-hallucination observation, the CTS design, and the model-free invariant subclass as genuine deltas. The verdict is now cleaner: unanimous on every criterion rather than majority-reconciled.

All three reviewers independently converge on the same core merits — the controlled retrospective (31%→81% FP suppression at 96.7% TP retention), the contract hallucination propagation observation (12 by-design = 25%), the model-free COSINE>1.0 invariant subclass, and the honest scoping to boundary/validation compliance. The remaining items below are fixable blemishes — primarily Related-Work completeness and residual framing prominence — not tier-lowering flaws.

### Priority Revisions
The main problems the author should fix, ranked by impact. Item 1 is the strongest new signal this round (surfaced by Reviewer 2's specialty literature task); items 2–3 are cross-reviewer; item 4 is double-reviewer. All are revision-scope fixes; none requires new experiments on the validated core.

1. **Cover recent REST API testing / fuzzing related work.** Reviewer 2 (area specialist, literature-verified) flags two missing threads: LlamaRestTest (2025, fine-tunes smaller LLMs for REST API testing) in LLM-driven REST testing, and foREST / MINER / DynER (2022–2024) in REST API fuzzing, which have advanced beyond RESTler/EvoMaster. Reviewer 3 separately flags Related-Work coverage of REST API testing as thin. The paper's positioning against RESTler/EvoMaster/Schemathesis is accurate as far as it goes (and the 404-probe evidence for the spec-authoring bottleneck is concrete), but these newer comparators should be cited and the delta re-stated against them. (R2 W1/2.5, R2 W2/2.6, R3 W3/2.4 — [major, fixable] from R2, [minor, fixable] from R3.)

2. **Make the cross-system scope delimitation more prominent.** All three reviewers still flag the cross-system generalization claim as outrunning the validated base (Milvus + Qdrant; Weaviate/MeiliSearch/Chroma near-zero adjudicated signal). The Round 14 abstract qualifier ("Adjudicated precision is validated on Milvus and Qdrant… not as precision evidence") is now present and R2/R3 both acknowledge it; the residual ask is prominence — surface the delimitation in the Contributions list and lead the abstract with "validated on Milvus and Qdrant" rather than "five VDBMSs." (R1 1.2/2.2, R2 W3/1.4, R3 2.2/W1/Q4 — cross-reviewer; [major] from R1/R3, [minor] from R2.)

3. **Bound the three-anchor contribution to what is validated.** All three note the threat-model anchor is under-powered (n=12, unstable, over-fires on state/concurrency) and the reproduction anchor is unevaluated; only source is validated as primary. The body already says this honestly (Contribution 2 foregrounds source as "the empirically validated primary anchor"; §5.4 reports threat-model as "noisy complement"; the paper explicitly "do[es] not claim the three-anchor design as a clean validated contribution"). The residual ask is to let the Contribution statement and abstract carry that scoping even more directly, so the three-anchor framing does not outrun its validation in the architecture figure. (R1 W3/2.6/5.2, R2 W5/3.6, R3 W2/3.3 — cross-reviewer; R3 [major, fixable], R1/R2 [minor, fixable].)

4. **Soften the single-layer counterfactual and schema-fuzzer comparisons where the 45.6% / 71% figures appear.** R1 and R2 note the single-layer arm (45.6%) mixes maintainer-adjudicated baseline with 27 live-reprobed FPs (a weaker proxy), and the baseline arms use asymmetric ground truths. The body already labels the single-layer figure a "directional lift at zero recall cost" with the residual-gap caveat, and the schema-fuzzer paragraph now front-loads the marginal-value conclusion. The residual ask is to keep those caveats attached to every appearance of the figures. (R1 2.4/3.2, R2 W4/3.7 — [minor, fixable].)

**Bottom line:** the paper clears the Accept bar with a unanimous Weak Accept across all criteria — cleaner than Round 14's majority-reconciled Novelty. The two new action items are Related-Work completeness (LlamaRestTest, foREST/MINER/DynER) and making the already-honest scope delimitations (cross-system, three-anchor) more prominent in the abstract/contributions. Neither requires new experiments; both are framing/positioning fixes that bring the front matter in line with what the body already reports honestly.

---

*Orchestrator note on verification:* All three reviewer drafts were read in full and their substantive claims (111 submissions, 52 adjudicated, 36 acknowledged = 28 fixed + 8 accepted, 12 by-design, 4 rejected, Milvus 51 / Qdrant 26 / Weaviate 30 / MeiliSearch 3 / Chroma 1 submissions, 31%→81% FP suppression at 96.7% TP retention, 27/27 live-confirmed single-layer FPs, three-anchor 9/12/6/12/11/12 with 4/4 TP retention, canary 0/9, DeepSeek 2/3 over-strict reproduced, 45.6% vs 69.2%, schema-fuzzer 71% post-filter) were cross-checked against the paper text and match after patching. Each draft passed an independent checker; the verify-fix loop applied two targeted patches — Reviewer 2's "75 of 111" corrected to "77 of 111" (51+26=77), and Reviewer 3's item 2.2 synthetic quotation rephrased so only the verbatim abstract phrase remains in quotes. The checkers also reported a number of section/table-number references that use each reviewer's own internal reading-order numbering (e.g., "Section 4.x" for the evaluation subsections, "Table 1/2" swapped); these are sub-agent citation artifacts that do not affect any verdict or substantive judgment and are marked here per the 3-round verify-fix cap rather than patched, consistent with prior rounds. One checker (Reviewer 2's) additionally reported a handful of violations that on grounding against the draft turned out to be the checker's own misreads (e.g., it attributed a `[major, fixable]` tag to Core Weakness W4 that does not exist in the draft, and flagged the decimal section references as fabricated numbering rather than reading-order citation); these false positives are noted here and were not actioned. Drafts and checker artifacts are preserved under `.paperpilot/review/.in-progress/` for inspection.

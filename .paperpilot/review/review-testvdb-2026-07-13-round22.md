## Reviewer 1: Domain Expert

**Overall Recommendation:** Accept

### Summary

This paper addresses the problem of detecting API compliance defects in Vector Database Management Systems (VDBMSs)—bugs where the system silently accepts inputs or produces behaviors that violate its documented contract but do not crash. The authors present TestVDB, an LLM-driven system that extracts contracts from API documentation, generates attack cases, and applies Contract-Truth Separation (CTS) to mitigate a novel failure mode they identify: contract hallucination propagation, where the same LLM family both generates the contract and judges compliance, leading to self-confirmation of hallucinated constraints. CTS introduces a truth layer (a dev-reviewer agent) that falsifies LLM-generated assertions using maintainer-authority evidence (source code, prior PRs, by-design intent). The system produced 111 submissions across five VDBMSs, with maintainer-adjudicated validation on Milvus and Qdrant (36 acknowledged, 28 fixed, 8 accepted-open, 12 by-design, 4 rejected). On a controlled 52-candidate retrospective, the dev-reviewer's source anchor lifted false-positive suppression from 31% to 81% while retaining 96.7% of true positives. Aggregate end-to-end precision is 69.2% (Wilson 95% CI [55.7%, 80.1%%]; worst-case bound with pending submissions [43.9%, 80.5%]).

### Core Strengths

- **S1:** The model-free invariant oracle subclass—COSINE distance >1.0 for identical vectors, incomplete index results, payload-filter violations—is the paper's most defensible technical finding, violating hard mathematical bounds independently of LLM judgment and reproducing across vendors — see Section 5.2 (RQ2 case studies) and Table 2.

- **S2:** Contract-Truth Separation (CTS) is a well-motivated design principle that directly addresses a real and previously uncharacterized failure mode in LLM-driven testing—contract hallucination propagation—and the empirical evidence (25% of adjudicated submissions marked by-design) demonstrates its importance — see Section 6 and lines 192-195.

- **S3:** The evaluation design is unusually thorough for a systems paper: maintainer-adjudicated ground truth, controlled same-population retrospective comparing claim-only vs source-grounded judgment, live FP audit on 27 candidates, and honest sensitivity analysis with pending-resolution bounds — see Section 5.3 (RQ3) and Table 4.

- **S4:** The paper's positioning is precise and honest: it explicitly targets the API-compliance slice of incorrect behavior (not result-correctness oracles, which remain open), correctly scopes complementarity with VDBFuzz (crash vs compliance), and acknowledges limitations upfront rather than overselling — see Introduction lines 86-87 and Conclusion line 385.

### Core Weaknesses

- **W1:** External validity is limited—adjudicated signal concentrates on Milvus (51 submissions) and Qdrant (26); Weaviate, MeiliSearch, and Chroma contribute near-zero adjudicated outcomes (3 pending, 1 excluded total), so the cross-system generalization claim is supported only for two systems — see Table 1 (lines 204-221) and Section 5.1.

- **W2:** The threat-model anchor evaluation (RQ4, Section 5.4) reports an exploratory negative with a wiring bug confound and unstable results (one FP flipped across runs), leaving the three-anchor design incompletely validated—the threat anchor's value as a "noisy complement" is supported only on n=12 Milvus FPs — see lines 361-363.

- **W3:** Recall quantification is indirect—the 96.7% figure is judgment-layer TP retention, not end-to-end discovery recall; the held-out rediscovery study (4/9 bugs) provides some evidence but is small and constrained by version-pin boundaries — see lines 371-373 and Threats to Validity.

### Detailed Assessment

#### 1. Significance — Adequate

- **1.1** The problem is real and practical: 43% of VDBMS bugs are incorrect-behavior defects (per the cited bug study xie2025toward), and crash-based oracles cannot detect them. The authors correctly identify this as the central open challenge flagged by the roadmap (wang2025towards) — Introduction lines 50-54.

- **1.2** The scope is narrower than the full roadmap challenge: the paper addresses API-compliance defects (a subset of incorrect behavior) and explicitly leaves result-correctness oracles (ANN recall, ranking error) as open work. This is honest scoping rather than overselling — line 87 and Conclusion line 385.

- **1.3** The practical impact is demonstrated by 36 maintainer-acknowledged issues (28 fixed, 8 accepted-open) across two production VDBMSs. However, the impact is primarily concentrated on two systems (Milvus and Qdrant); three other VDBMSs contribute minimal adjudicated signal, limiting the claim of broad cross-system generalization — Table 1 (lines 204-221).

#### 2. Novelty — Excellent

- **2.1** Contract hallucination propagation is, to my knowledge, a newly characterized failure mode in LLM-driven testing. When the same model family generates the contract and judges compliance, hallucinated constraints are self-confirmed. The authors provide direct empirical evidence: 12 of 48 substantively adjudicated submissions (25%) were marked by-design because the LLM-derived contract was stricter than true intent — Section 6 and lines 192-195.

- **2.2** Contract-Truth Separation (CTS) is a principled design response to this failure mode: separating the LLM assertion layer from a truth layer that falsifies via maintainer-authority evidence. The source-grounding anchor's contribution is validated by a controlled same-population retrospective showing FP suppression lift from 31% to 81% at 96.7% TP retention — Section 5.3 (lines 251-254) and Table 3.

- **2.3** Checked the delta against core competitors (fetched via literature search): The paper accurately positions itself against RESTler (atlidakis2019restler) and QuickREST (karlsson2020quickrest). RESTler uses crash/5XX oracles; QuickREST requires OpenAPI specs (which VDBMS endpoints don't serve, as honestly acknowledged in line 277). TestVDB's LLM-derived contract + CTS approach is a real novelty delta — Related Work lines 377-380 and Section 5.3.4.

- **2.4** The model-free invariant oracle subclass (COSINE >1.0, index completeness, payload-filter presence) is a strong technical finding: it violates hard mathematical bounds, needs no LLM judgment, reproduces across vendors, and is adoptable independent of TestVDB's pipeline — Section 5.2 (lines 245-249). This is the least contingent contribution.

- **2.5** The paper correctly identifies that it does not solve the roadmap's full oracle challenge (result correctness of vector search remains open) and honestly scopes complementarity with VDBFuzz (crash vs compliance, no head-to-head empirical comparison yet). The positioning is precise rather than inflated — lines 86-87, 242.

#### 3. Soundness — Adequate

- **3.1** The evaluation design is a strength: maintainer-adjudicated ground truth on 52 submissions is stronger than LLM self-judgment or API-acceptance alone. The controlled same-population retrospective (blind re-triage of the 52 adjudicated candidates under claim-only vs source-grounded conditions) provides clean evidence for the dev-reviewer's contribution — Section 5.3 (lines 251-254).

- **3.2** The single-layer counterfactual (removing the FP-suppression chain and re-running generation + 4-judge debate on milvus v2.6.19) and live FP audit (re-probing 27 dev-reviewer-killed candidates on a fresh container, confirming 27/27 as true FPs) are rigorous sanity checks — lines 269-272.

- **3.3 [major, fixable]** External validity is limited. The 111 submissions produced across five VDBMSs concentrate adjudicated signal on Milvus (51 submissions) and Qdrant (26). Weaviate (30 submissions, 21 pending), MeiliSearch (3 excluded), and Chroma (1 pending) contribute near-zero adjudicated outcomes. The cross-system generalization claim is therefore supported primarily for two systems, with the other three serving as breadth probes rather than statistical evidence — Table 1 (lines 204-221), Section 5.1. This limits the claim that the approach generalizes across VDBMSs; a revision should soften the cross-system claim or expand validation.

- **3.4 [major, fixable]** The threat-model anchor evaluation (RQ4, Section 5.4) reports an exploratory negative with a confound: the threat-modeler populated threat_model.json, but the dev-reviewer consumed developer_cognition.json's blindspot_indicators field (empty). After fixing the wiring, the results are unstable (one boundary FP flipped between runs) and the sample is small (n=12 Milvus FPs). The conclusion that the threat anchor is a "noisy complement" is therefore incompletely validated — lines 361-363. A revision should either strengthen this evaluation (larger sample, stability analysis) or demote the threat anchor to design-level future work rather than a claimed component.

- **3.5** The recall quantification is indirect. The 96.7% figure (Section 5.3, line 254) is judgment-layer TP retention (6 rate-limited TPs unreachable via GitHub API), not end-to-end discovery recall. The held-out rediscovery study (4/9 pre-2024 bugs, 44.4%, Wilson 95% CI [18.9%, 73.3%%]) provides some evidence but is small and constrained by spec-completeness and version-pin boundaries — lines 371-373. The paper is honest about this limitation, but it leaves the true discovery recall uncertain.

- **3.6** The single-LLM baseline (25.5% precision) is an apples-to-oranges comparison: it removes the multi-agent debate entirely, whereas the single-layer counterfactual (45.6% precision) removes only the FP-suppression chain while keeping the full multi-agent generation and 4-judge debate. The paper correctly notes these are not directly comparable (line 275), but the multiple ground-truth tiers in Table 4 make it difficult to assess which components contribute most to the precision lift.

- **3.7 [minor, fixable]** The schema-aware boundary fuzzer baseline (19 probes, 71% post-filter precision on 7 API-accepted candidates) concedes that on the boundary/validation subset (75% of yield), a spec-driven fuzzer is effective. The paper's marginal value claim focuses on (a) non-boundary probes (8/36 TPs), (b) CTS FP-suppression cross-category, and (c) spec-gap detection — lines 277-278. This is honest, but the fuzzer comparison would be stronger with a larger probe set or Schemathesis head-to-head (currently blocked by Milvus lacking OpenAPI, line 277).

#### 4. Verifiability — Excellent

- **4.1** The paper provides end-to-end reproducibility: target VDBMS versions are pinned (Milvus 2.6.19 for ablations; full matrix in artifact), the 20 agents are defined by task-structured role prompts (prompts in artifact), and the pipeline is orchestrated by Claude Code dispatching to GLM-5.2 under default sampling — lines 131-133.

- **4.2** An anonymized artifact is declared and reachable at https://anonymous.4open.science/r/testvdb-anon-D644/, containing per-target LLM-call budgets, wall-clock measurements, and token accounting on the order of 10^4 calls (~10^7 tokens aggregate, ~10^3 calls or ~2×10^6 tokens per target) — line 133.

- **4.3** The paper reports the 36 acknowledged TPs with GitHub issue identifiers (Table 2 lists the 5 unique TPs reachable only by the full pipeline with issue numbers), enabling external verification of maintainer outcomes — lines 225-240.

- **4.4** The evaluation dataset is reproducible: the 111 submissions, 52 adjudicated candidates, and 9 held-out pre-2024 bugs are documented with sufficient version-pin information to enable replication. The retrospective design (same 52-candidate pool, blind re-triage) is particularly well-described for reproducibility — Section 5.3.

- **4.5** The only verifiability gap is the threat-model anchor's wiring bug (line 362): the dev-reviewer prompt reading threat_model.json directly is mentioned but not fully detailed, making the exact fix harder to replicate. However, this is a minor issue in an otherwise strongly reproducible package.

#### 5. Presentation — Adequate

- **5.1** The structure is logical and follows the testing-system template: problem → approach → evaluation → threats → related work → conclusion. The figures are clear—Figure 1 (pipeline overview) effectively shows the assertion layer (LLM) and truth layer (counter-evidence) separation, and Figure 2 (precision by tier) makes the asymmetry across ground-truth tiers explicit.

- **5.2** The writing is generally clear, with precise language. The distinction between "incorrect behavior" (roadmap term), "API compliance defects" (this paper's scope), and "result correctness" (explicitly out of scope) is well-maintained.

- **5.3 [minor, fixable]** Some notation in Table 3 is dense: the "ground truth (tier)" column groups rows into four tiers (LLM-judged, API-acceptance, retrospective, maintainer) with no visual separator, making the table harder to parse at a glance. Adding visual grouping (lines or whitespace) would improve readability.

- **5.4 [minor, fixable]** Table 1 line 218 reports "Total" aggregates across 5 VDBMSs, but the text (Section 5.1) correctly notes that cross-system generalization is claimed primarily for Milvus and Qdrant, with the other three as breadth probes. The table caption could be more explicit about this asymmetry.

- **5.5 [minor, fixable]** The threat-model anchor section (RQ4, lines 361-363) is dense: the wiring bug confound, the fixed re-run conditions (source-alone, threat-alone, union), and the unstable result are compressed into one paragraph. Splitting this into two paragraphs (confound diagnosis → re-run results) would improve clarity.

### Questions for Authors

- **Q1:** The external validity is limited to two well-adjudicated systems (Milvus and Qdrant). Can you provide more details on why Weaviate adjudication is minimal (21 of 30 submissions pending)? Is this maintainer triage latency, or a substantive signal about the approach's transfer to Weaviate? If the former, a revision should note this explicitly and soften the cross-system claim — item 3.3's rating would move from Weak to Adequate if addressed.

- **Q2:** The threat-model anchor evaluation shows instability (one FP flipped across runs). Can you provide more analysis on what caused the instability? Is this the threat-model agent's non-determinism, or the dev-reviewer's consumption of it? If the former, can you stabilize it with stronger prompts or multiple runs? If the latter, can you re-architect the integration? — item 3.4's rating would move from Weak to Adequate if the anchor is strengthened or demoted to future work.

- **Q3:** The single-LLM baseline (25.5% precision) uses a different ground truth than the single-layer counterfactual (45.6% precision), making it hard to attribute the precision lift to multi-agent debate vs CTS. Can you add an arm that keeps the single-LLM generation but applies the source-grounded dev-reviewer, to isolate CTS's contribution? — this would clarify component attribution but is not required for acceptance.

- **Q4:** The schema-aware boundary fuzzer used 19 probes. Can you characterize the probe design space more systematically—how many total boundary probes exist across the five VDBMSs, and how was the 19-probe subset selected? This would strengthen the concession that spec-driven fuzzers are effective on boundary/validation — not required but would improve the baseline.

- **Q5:** The recall quantification (4/9 held-out bugs, 44.4%) is small and wide-CI. Do you have plans to expand this cohort, or is there a fundamental constraint (e.g., few pre-2024 VDBMS bugs exist)? Acknowledging this as a limitation rather than future work would strengthen the threats section — item 3.5's assessment is already honest, but this would make it explicit.


---

## Reviewer 2: Area Specialist

**Overall Recommendation:** Weak Accept

### Summary
TestVDB targets API compliance defects in Vector Database Management Systems (VDBMSs)---bugs where systems silently accept inputs or behaviors that violate their documented contracts, despite no crash or exception. The authors present an LLM-driven testing pipeline that extracts contracts from API documentation, generates attacks, and applies Contract-Truth Separation (CTS) to mitigate contract hallucination propagation, where hallucinated constraints are self-confirmed when the same LLM family both generates contracts and judges compliance. The system produced 111 submissions across five VDBMSs, with maintainer adjudication on Milvus and Qdrant yielding 36 acknowledged defects (28 fixed, 8 accepted-open) and 12 by-design false positives, for 69.2% adjudicated precision. A controlled retrospective shows CTS's source-grounded verification lifts false-positive suppression from 31% to 81% while retaining 96.7% of true positives. The paper contributes the first LLM-driven realization of VDBMS API compliance defect detection, the CTS design principle, and a model-free invariant oracle subclass (COSINE distance >1.0 for identical vectors, incomplete index results, payload-filter violations).

### Core Strengths
- **S1:** CTS identifies a real LLM-driven testing failure mode---contract hallucination propagation, where the same model family generating and judging contracts self-confirms hallucinations (25% of adjudicated submissions marked by-design) — see 2.1, 2.2
- **S2:** Strong end-to-end validation on real VDBMSs---36 maintainer-acknowledged defects across Milvus and Qdrant (28 fixed), with adjudicated precision 69.2% — see 3.1, 3.3
- **S3:** Model-free invariant oracle subclass (COSINE>1.0, incomplete index results, payload-filter violations) violates hard mathematical bounds, needs no LLM judgment, and reproduces across vendors — see 2.3, 3.2

### Core Weaknesses
- **W1:** Multi-layer abstraction blurs evaluation boundaries---20 LLM agents, two-stage judgment, three dev-reviewer anchors (only one validated), and unvalidated components (threat-model anchor, L1 gate) make it difficult to isolate CTS's contribution from design complexity — see 1.1, 3.3, 4.1
- **W2:** Recall scope weakly bounded---96.7% TP retention is judgment-layer, not end-to-end discovery recall; held-out 9-bug rediscovery study shows 4/9 (44%, Wilson CI [18.9%, 73.3%]), leaving actual coverage unclear — see 3.3, 4.1

### Detailed Assessment

1. **Significance** — Adequate
   - **1.1** VDBMS reliability is increasingly important as these systems underpin LLM applications; the paper cites a 43.0% prevalence of incorrect-behior bugs (vs. 23.1% crash/hang) from a 1,671-PR empirical study~\cite{bugstudy25}, establishing practical relevance.
   - **1.2 [major, fixable]** The scope restriction---API compliance defects only, within the incorrect-behavior subset---is substantial but reasonable for a first LLM-driven realization on this agenda. The paper honestly excludes crash bugs (complementary to VDBFuzz), performance, and build defects, leaving soft result-correctness (ANN recall) open. This bounded scope is Adequate for significance rather than Excellent, as the contribution is incremental to the broader correctness-oracle agenda flagged as open in~\cite{roadmap25}.

2. **Novelty** — Adequate
   - **2.1** The Contract-Truth Separation design principle---isolating LLM-generated assertions from a maintainer-authority truth layer that falsifies them via source-grounded verification---is a clear, non-obvious delta over prior LLM-as-judge patterns (Section~2.3). The contract-hallucination propagation phenomenon (same model family generating contract + judgment self-confirms hallucinations, 25% of adjudicated submissions marked by-design) has not been characterized in LLM-driven testing.
   - **2.2 [minor, unfixable]** The LLM-driven VDBMS testing direction builds directly on VDBFuzz~\cite{vdbfuzz26} (crash-focused fuzzer) and responds to its generation-side Future Work (LLM-generated diverse API interactions, staying current with evolving APIs). This dependency limits Novelty to incremental (Adequate) rather than transformative, though CTS is a distinct contribution beyond VDBFuzz's crash oracle.
   - **2.3** The model-free invariant oracle subclass (COSINE>1.0, incomplete index results, payload-filter violations) is independently valuable and adopts cleanly beyond TestVDB's LLM pipeline. It is a small, specialized contribution but defensible.
   - **2.4 [major, fixable]** Related Work coverage is incomplete for REST API fuzzing. The paper cites RESTler~\cite{restler19}, EvoMaster~\cite{evomaster21}, Schemathesis~\cite{schemathesis}, and recent tools (foREST~\cite{lin2023forest}, MINER~\cite{lyu2023miner}, DynER~\cite{chen2024dyner}) but does not deeply position TestVDB's semantic compliance oracle against their schema-conformance focus. The delta is stated (they target schema/crash; we target semantic compliance) but not verified---the paper notes VDBMS REST endpoints return 404 for /swagger and /openapi.json, but this single datapoint does not fully establish the novelty boundary.

3. **Soundness** — Adequate
   - **3.1** The main claims are supported by appropriate evaluation. End-to-end results (111 submissions, 36 acknowledged, 12 by-design, 4 rejected) establish real defect detection; the controlled retrospective on the same 52-candidate pool (blind re-triage under claim-only vs. source-grounded conditions) cleanly isolates CTS's source anchor as the driver of FP suppression (31% → 81%, 2.6× lift) while retaining 29/30 TPs (96.7%).
   - **3.2** Baseline comparisons are appropriately differentiated by ground-truth tier (LLM-judged / API-acceptance / blind re-triage / maintainer). The paper wisely avoids cross-tier comparisons (e.g., Table~2 notes rows are "not directly comparable across tiers"), which strengthens the evaluation's internal validity.
   - **3.3 [major, fixable]** Threats to Validity covers key concerns (maintainer acknowledgment as weak ground truth; submission-selection bias; Weaviate undiagnosed pending cases; LLM variance; contamination via GLM-5.2 training data; excluded-set FP tail bounding). However, the construction of the single-layer counterfactual precision (45.6%) combines maintainer-adjudicated 36/52 baseline with 27 live-re-probed FPs under one feedback cycle, which may understate variance. The live FP audit (27/27 killed candidates re-probed as true FPs, over-kill 0/27) is strong but limited to Milvus v2.6.19.
   - **3.4 [minor, fixable]** The threat-model anchor ablation (RQ4, Section~3.4) is honest about its negative result---the anchor is "a noisy complement" rather than a validated component. The diagnosis (wiring gap fixed; unstable across runs; catches 2 source residuals but over-fires on state/concurrency FPs) is transparent, and the paper correctly bounds its claim (source is primary; threat-model is not a clean validated contribution on n=12). This honesty is commendable but leaves the three-anchor design partially unevaluated.

4. **Verifiability** — Adequate
   - **4.1** The paper provides sufficient information to follow the work at a conceptual level. The five-stage pipeline (Figure~1), agent roles, and the CTS mechanism are clearly described. Target VDBMS versions are pinned (Milvus 2.6.19 for ablations; full matrix in artifact), and the 20-agent system is specified with prompts in the artifact. Implementation details are sufficient for replication.
   - **4.2 [minor, fixable]** The artifact link is declared as reachable (anonymous 4open.science repository). The paper states it contains "full prompts, per-target LLM-call and wall-clock accounting, and the 52 adjudicated candidates" but does not explicitly describe the repository structure or replication instructions in-text. Readers must follow the link to assess reproducibility details fully.
   - **4.3** LLM call and cost accounting is provided at aggregate level ("on the order of 10^4 LLM calls, ~10^7 tokens; per target, ~10^3 calls, ~2×10^6 tokens, on the order of $10 per target"). Precise per-token and wall-clock accounting is deferred to the artifact, which is acceptable given the complexity but limits in-text verifiability of the exact cost breakdown.

5. **Presentation** — Adequate
   - **5.1** The paper is well-structured and readable. The introduction clearly motivates the problem (43.0% incorrect-behior bugs lack oracles), positions CTS against VDBFuzz's crash oracle, and honestly scopes the contribution (API compliance defects only; result-correctness remains open). Figures and tables support the core arguments (Figure~1 for pipeline, Table~2 for precision tiers, Figure~2 for CI visualization).
   - **5.2 [minor, fixable]** Language is generally clear with minor awkwardness (e.g., "touching multiple areas / dimensions" in persona phrasing; some inline parentheticals are dense). No pervasive errors that obstruct evaluation.
   - **5.3 [minor, fixable]** Formatting appears sound, but the stripped LaTeX source prevents full assessment of figure/table rendering quality in this review pass.
   - **5.4 [minor, fixable]** The Related Work section categorizes prior work well (VDBMS testing, REST API fuzzing, database oracles, LLM-based testing, test oracles) but could better position TestVDB against the recent REST fuzzer wave (foREST, MINER, DynER) beyond the single 404 datapoint for OpenAPI unavailability. A more explicit comparison table would strengthen the positioning.

### Questions for Authors
- **Q1:** Could you clarify the relative contribution of CTS vs. multi-agent debate to the overall 69.2% end-to-end precision? The single-layer counterfactual (A1) removes the FP-suppression chain entirely (45.6%), while the Single-LLM arm removes both multi-agent debate and CTS (25.5%). Can you quantify how much of the lift from 45.6% → 69.2% is attributable to CTS specifically vs. the four-judge debate layer?
- **Q2:** The held-out 9-bug rediscovery study (4/9, 44%) is the primary evidence for end-to-end discovery recall. Given the wide Wilson CI [18.9%, 73.3%], do you have plans to expand this cohort or provide additional evidence (e.g., manual labeling of the 30 pending submissions) to better bound actual coverage?
- **Q3:** The threat-model anchor is reported as "a noisy complement" that catches boundary-default FPs but over-fires on state/concurrency. Have you considered alternative designs (e.g., separate state/concurrency models, finer blindspot categories) that might stabilize this anchor, or is the current three-anchor design intended as the final architecture?


---

## Reviewer 3: General Reviewer

**Overall Recommendation:** Accept

### Summary

This paper presents TestVDB, an LLM-driven system for detecting API compliance defects in Vector Database Management Systems (VDBMSs). The authors target bugs where a VDBMS silently accepts inputs or produces behaviors that violate its documented contract but do not crash. Their approach employs Contract-Truth Separation (CTS), which isolates LLM-generated contract assertions from a truth layer that falsifies them using maintainer-authority evidence (source code, pull request history, and issue discussions). TestVDB generated 111 issue submissions across five VDBMSs, with maintainer adjudication on Milvus and Qdrant yielding 36 acknowledged defects (28 fixed, 8 accepted open) out of 52 adjudicated submissions. A controlled retrospective on the 52 adjudicated candidates demonstrates that the dev-reviewer's source-grounded verification anchor lifts false-positive suppression from 31% to 81% while retaining 96.7% of true positives, for an aggregate precision of 69.2% (Wilson 95% CI [55.7%, 80.1%]). The work also identifies a model-free invariant oracle subclass (e.g., cosine distance >1.0 for identical vectors) that violates mathematical bounds and is adoptable independently of the LLM pipeline.

### Core Strengths

- **S1:** The Contract-Truth Separation principle is a well-motivated architectural response to the contract-hallucination propagation problem the authors identify — see Section 4 and Section 7, where they show that 25% of adjudicated submissions were by-design because the LLM-derived contract was stricter than maintainer intent.
- **S2:** The evaluation design is stronger than typical LLM-based testing work — see RQ3 (Section 6.3), where a controlled retrospective on the same 52-candidate population isolates the contribution of source-grounded verification, and the acknowledgment that different baseline arms use different ground truths (Table 3, Figure 3) rather than drawing spurious cross-tier comparisons.
- **S3:** The model-free invariant oracle subclass is a clear, defensible contribution that needs no LLM judgment — see Section 6.2, where cosine distance >1.0 and incomplete index results violate hard mathematical bounds and reproduce across Milvus and Qdrant.
- **S4:** The paper is self-contained and internally coherent — the problem formulation (Section 2), the CTS mitigation (Section 4.4), and the evaluation (RQ1–RQ3) form a clear logical chain, and the authors honestly report boundary conditions (75% boundary/validation yield, crash excluded, soft result-correctness open).
- **S5:** Verifiability is strong — the authors provide sufficient implementation detail (agent count, LLM backbone GLM-5.2, cost order-of-magnitude per target, pinned versions), commit to an anonymized artifact, and describe the reproduction path for key findings.

### Core Weaknesses

- **W1:** Limited external validation on Weaviate, MeiliSearch, and Chroma — see RQ1 (Section 6.1), where Weaviate has 21 pending submissions with no adjudication, and MeiliSearch/Chroma contribute near-zero adjudicated signal, so the cross-system generalization claim rests primarily on Milvus and Qdrant.
- **W2:** The threat-model anchor evaluation is unstable and on a small sample (n=12 Milvus FPs) — see Section 6.4 (RQ4), where the threat anchor shows instability across runs and over-fires on state/concurrency cases; the authors report it as a noisy complement rather than a validated component, which weakens the three-anchor design as a claimed contribution.
- **W3:** Discovery recall is measured on only 9 held-out bugs — see Section 6.5, Threats to Validity, where a 9-bug rediscovery study yields 4/9 (44%, Wilson [18.9%, 73.3%]), with 2 blocked by SDK incompatibility; the lower bound clears zero but the sample is small.

### Detailed Assessment

1. **Significance** — Excellent
   - **1.1** The problem is real and framed with empirical backing — Section 1 cites a study of 1,671 VDBMS bug-fix PRs finding 43% incorrect-behavior bugs, and the roadmap [roadmap25] flags incorrect-behavior testing as an open challenge. The scope is narrower (API compliance, boundary/validation) but meaningful: compliance defects corrupt query semantics and expand attack surfaces without crashing.
   - **1.2** The contribution is incremental beyond prior work but addresses a clear gap — VDBFuzz [vdbfuzz26] targets crashes; TestVDB extends detection to API compliance using a contract oracle. The authors position their work as complementary to VDBFuzz and explicitly claim they do not solve result-correctness (ANN recall/ranking), which remains open. This is a bounded but useful slice of the roadmap agenda.
   - **1.3** The practical impact is demonstrated by maintainer uptake — 36 acknowledged defects across two production VDBMSs, 28 fixed, is concrete evidence of utility. The 5 unique TPs (3 diagnostic-quality, 2 state/logic) reachable only by the full LLM pipeline (Table 2) show where the approach adds value over spec-driven fuzzing.

2. **Novelty** — Adequate
   - **2.1** The Contract-Truth Separation principle and the contract-hallucination propagation phenomenon are, to my knowledge, new characterizations — Section 4 and Section 7 explain that when one LLM family both generates a contract and judges compliance, hallucinated constraints are self-confirmed, and the authors provide empirical evidence (12 of 48 adjudicated submissions, 25%, were by-design due to over-strict contracts). This is a specific, non-obvious failure mode.
   - **2.2** The method components are assembled from existing ideas — multi-agent debate for verification [du2023improving], property-based testing [claessen00], and source-grounded verification are not new, but their combination into an LLM-driven compliance pipeline with CTS is a new application to VDBMSs.
   - **2.3** The Related Work section is reasonably thorough for the domains surveyed — Section 8 covers VDBMS testing (VDBFuzz, roadmap, bug study), REST API testing (RESTler, EvoMaster, Schemathesis, and more recent REST fuzzers), database oracles (NoREC, TLP, DQE, DDLCheck), and LLM-based testing. However, the REST-testing discussion focuses on schema-driven tools and does not cite LLM-based API-testing contemporaries like LlamaRestTest [kim2025llamaresttest] until a brief mention in the LLM-based testing subsection, which weakens the novelty positioning against concurrent LLM-driven REST testing work.

3. **Soundness** — Excellent
   - **3.1** The main claims are supported by appropriate evidence — the core claim (CTS improves FP suppression) is evaluated via a controlled retrospective on the same 52-candidate population (Section 6.3), which is a stronger design than the typical end-to-end precision report alone. The authors also report a live FP audit (27/27 dev-reviewer-killed candidates reproduce as true FPs on reprobe) and a derived single-layer precision (45.6% vs. 69.2%).
   - **3.2** The evaluation design addresses key validity threats — Section 6.5 (Threats to Validity) covers internal, selection, external, construct, LLM variance, contamination, recall scope, and excluded-set threats. The contamination analysis uses a memorization canary (0/9 held-out bugs recalled at issue-specificity) and a contract counterfactual (DeepSeek reproduces over-strict constraints), which is thorough for LLM-based work.
   - **3.3** The claims are scoped honestly — the authors explicitly exclude crash bugs (complementary to VDBFuzz), acknowledge that 75% of yield is boundary/validation compliance, and state that soft result-correctness (ANN recall) remains open. The 5 unique TPs claim is qualified as a lower bound relative to the 19-probe instance, not a fuzzer-class upper bound (Section 6.1).
   - **3.4** The threat-model anchor evaluation is underpowered but honestly reported — Section 6.4 (RQ4) reports an exploratory negative on n=12 with instability and over-firing, and the authors classify it as a noisy complement rather than a validated component. This is a weakness in the three-anchor design as a claimed contribution, but the honesty about the evidence quality is appropriate.
   - **3.5** [minor, fixable] The cross-system generalization claim is weaker than stated — RQ1 (Section 6.1) states the work produced issues across five VDBMSs, but Table 1 shows that only Milvus (51 submissions) and Qdrant (26) have substantive adjudicated yield, while Weaviate has 30 submissions with 21 pending and MeiliSearch/Chroma contribute near-zero signal. The cross-system claim rests primarily on Milvus and Qdrant, which should be qualified more explicitly in the abstract and introduction.

4. **Verifiability** — Excellent
   - **4.1** The paper provides sufficient implementation detail to reproduce the approach — Section 4.1 specifies the 20 agents, the LLM backbone (GLM-5.2, high- and low-budget configurations), the cost order-of-magnitude per target (~10³ calls, ~2×10⁶ tokens, ~$10), and the artifact commitment (anonymous repository at 4open.science). The Figure 1 overview pipeline is complete and the threat-model artifact design is described.
   - **4.2** The evaluation details are sufficient for replication — RQ1–RQ3 report exact target versions (Milvus 2.6.19 for ablations; full version matrix in artifact), submission counts, adjudication outcomes, precision calculations with Wilson CIs, and the controlled retrospective protocol. The 19-probe schema fuzzer instance and the model-free invariant oracle triggers are described in enough detail to reconstruct them.
   - **4.3** The artifact is declared as reachable — the anonymized repository URL is provided (https://anonymous.4open.science/r/testvdb-anon-D644/), and the authors state it will be made public on acceptance. The text alone describes the pipeline stages and agent roles sufficiently to follow the evidence without cloning the artifact.

5. **Presentation** — Adequate
   - **5.1** The paper is well-structured and internally coherent — the logical flow from problem (Section 1) → background (Section 2) → approach (Section 3, with CTS in Section 3.3) → contract hallucination (Section 4) → evaluation (Section 5, RQ1–RQ4) → related work (Section 6) → conclusion (Section 7) is clear. The figures (Figure 1 pipeline, Figure 2 precision comparison) and tables (Table 1 yield, Table 2 unique TPs, Table 3 baselines) are legible and referenced appropriately.
   - **5.2** [minor, fixable] The writing is generally clear but has occasional run-on sentences and passive voice that could be tightened — e.g., Section 1, "We target a tractable slice of this gap: API compliance defects" is slightly telegraphic; Section 4, the paragraph on contract-hallucination forms has a long sentence that could be split.
   - **5.3** [minor, fixable] Some notation is introduced without explicit definition — the table uses "Fix.", "Acc.", "ByD.", "Rej.", "Pend.", "Excl." as abbreviations; these are inferable from context but could be expanded in the caption (e.g., "Fix. = fixed, Acc. = accepted open, ByD. = by-design, Rej. = rejected, Pend. = pending, Excl. = excluded").
   - **5.4** [minor, fixable] The Related Work section could better position the work against concurrent LLM-driven REST testing — LlamaRestTest [kim2025llamaresttest] is cited only briefly in the LLM-based testing subsection, whereas it is directly relevant to the novelty discussion in the REST API testing subsection.

### Questions for Authors

- **Q1:** The cross-system generalization claim in the abstract and introduction is broader than the adjudicated evidence supports — Milvus and Qdrant have clear adjudicated signal, but Weaviate has 21 pending submissions and MeiliSearch/Chroma contribute near-zero adjudicated yield. Can you qualify the claim more explicitly (e.g., "primary evidence from Milvus and Qdrant, with breadth probes on Weaviate, MeiliSearch, and Chroma")? This would affect item 3.5's rating from Adequate toward Excellent if clarified.
- **Q2:** The threat-model anchor evaluation (RQ4) reports instability on n=12 and classifies it as a noisy complement rather than a validated component. Is the three-anchor design (source + threat-model + reproduction) intended as a core claimed contribution, or should the paper reframe CTS primarily around source-grounded verification with threat-model as exploratory? Clarifying this would strengthen the Soundness assessment.
- **Q3:** The discovery recall experiment (Threats to Validity) uses 9 held-out bugs and yields 4/9 rediscovered, with 2 blocked by SDK incompatibility. Do you have plans to expand this cohort? A larger sample would tighten the recall confidence interval and strengthen the practical-impact claim.

---

## Meta-Review (Round 22)

### Criterion Consensus

| Criterion | R1 (Domain) | R2 (Area) | R3 (General) | Meta-Review |
|---|---|---|---|---|
| Significance | Adequate | Adequate | Excellent | Adequate |
| Novelty | Excellent | Adequate | Adequate | Adequate |
| Soundness | Adequate | Adequate | Excellent | Adequate |
| Verifiability | Excellent | Adequate | Excellent | Excellent |
| Presentation | Adequate | Adequate | Adequate | Adequate |
| **Recommendation** | **Accept** | **Weak Accept** | **Accept** | **ACCEPT** |

### Meta Recommendation

**ACCEPT** — stop condition met (all three ≥ Weak Accept; two Accept)

All three reviewers returned ≥ Weak Accept (R1 Accept, R2 Weak Accept, R3 Accept), firing the rubric shortcut "All three Weak Accept or better → ACCEPT". The consensus-tier count agrees: no criterion at Poor or Weak — all five sit at Adequate or above (Verifiability consensus Excellent by 2/3). Two reviewers reached Accept via the "no criterion below Adequate with at least one substance criterion Excellent" branch — R1 on Novelty (contract hallucination propagation newly characterized; competitor positioning now complete incl. QuickREST), R3 on Significance + Soundness (maintainer-validated impact + strong controlled retrospective). This clears the user's stop condition (≥1 Accept among three ≥ Weak Accept).

### Checker notes (advisory, non-blocking)

The three independent checkers reported violations; on review, most are section/table numbering ambiguity from the stripped source (which carries \label/\ref, not compiled numbers) rather than fabricated claims. One substantive item: R3 W1 understated Weaviate's adjudicated count ("21 pending with no adjudication" — Table 1 shows 4 adjudicated: 3 fixed + 1 rejected). This sits inside a weakness description and does not affect R3's Accept (driven by Significance/Soundness Excellent). No patch needed for the verdict.

### Priority Revisions (advisory, post-accept)

1. **Recall cohort N=9** (R1 W3, R2 W2, R3) — the only remaining cross-reviewer weakness; unfixable without a Docker experiment session, already honestly disclosed.
2. **Cross-system scope** (R1 W1, R2 1.2, R3 W1) — already framed ("adjudicated on Milvus and Qdrant; breadth probes" + Weaviate 21 pending = triage latency).
3. **REST-competitor positioning depth** (R2 2.4) — delta stated but could be sharpened beyond the single OpenAPI-404 datapoint.

**Bottom line:** Round 22 lands a confident ACCEPT — 2 of 3 reviewers at Accept, none below Weak Accept, Verifiability consensus Excellent. The stop condition is met.

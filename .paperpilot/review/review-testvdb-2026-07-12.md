# Peer Review — TestVDB

**Paper:** TestVDB: Detecting API Compliance Defects in Vector Database Systems via Contract-Truth Separation
**Venue:** acm-sigconf (targeting VLDB/PVLDB)
**Date:** 2026-07-12
**Paper type:** technical
**Reviewers:** 3 independent (Domain Expert / Area Specialist / General Reviewer), each independently drafted then independently fact-checked.

---

## Reviewer 1: Domain Expert

**Overall Recommendation:** Weak Accept

### Summary

TestVDB targets API compliance defects in Vector Database Management Systems (VDBMSs)—bugs where a VDBMS silently accepts inputs or behaviors that violate its documented contract. The paper proposes Contract-Truth Separation (CTS), which isolates LLM-generated contract assertions from a truth layer that falsifies them via maintainer-authority evidence (source code, issue history, by-design intent). The approach is motivated by contract hallucination propagation: when one LLM family both generates a contract and judges compliance, hallucinated constraints are self-confirmed (25% of adjudicated submissions were by-design false positives from over-strict contracts). TestVDB produced 111 issues across five VDBMSs; maintainers acknowledged 36 (28 fixed), with adjudicated signal concentrated on Milvus and Qdrant. On a controlled retrospective over 52 adjudicated candidates, the dev-reviewer's source anchor lifts false-positive suppression from 31% to 81% while retaining 96.7% of true positives. The work addresses the incorrect-behavior subset of VDBMS bugs (43% of defects, per the roadmap) and complements crash-focused fuzzing (VDBFuzz).

### Core Strengths

- **S1:** The model-free invariant oracles (cosine similarity > 1.0, incomplete index results, payload filter violations) are the most defensible technical finding—they reproduce across vendors, violate hard mathematical bounds, and depend on no LLM judgment — see 3.7.
- **S2:** The controlled retrospective on the same 52-candidate population provides credible evidence that source-grounding substantially reduces false positives (31% → 81% suppression, 2.6× lift) with negligible true-positive loss — see 3.1.
- **S3:** The problem formulation—API compliance defects as a tractable subset of incorrect-behavior bugs that admit a contract oracle—is well-motivated by the VDBMS bug taxonomy (43% incorrect-behavior vs 23% crash) — see 1.1.
- **S4:** The contract hallucination propagation observation is a genuine phenomenon that matters for LLM-driven testing systems; the 12 by-design cases (25% of adjudicated submissions) provide concrete qualitative evidence — see 2.3.
- **S5:** The honest scope boundary (75% of yield is boundary/validation; crash bugs excluded by design; soft result-correctness remains open) is appropriately claimed — see 1.3.

### Core Weaknesses

- **W1:** Cross-system generalization is overclaimed—Milvus and Qdrant account for 77 of 111 submissions (69%) and 36 of 52 adjudicated issues (69%), while MeiliSearch (3), Chroma (1), and Weaviate (30 submissions, 3 acknowledged) contribute near-zero adjudicated signal — see 1.2, Table 3.
- **W2:** The threat-model prior is presented as a component but its evaluation (RQ4) is explicitly labeled "exploratory, not a contribution" with negative results (blindspot indicators never populated, unstable dev-reviewer, n=5 below significance) — see 3.4.
- **W3:** The single-LLM and schema-fuzzer baseline comparisons use different ground truths (LLM self-judgment, API-acceptance, maintainer adjudication) and populations, making direct numerical comparison problematic — see 3.5, Table 4.
- **W4:** End-to-end discovery recall is not established—pilots on held-out bugs reveal spec-completeness and version-pinning limits, and the paper does not run TestVDB against bug-present old versions — see 3.6.
- **W5:** Related Work coverage has gaps in LLM-as-oracle and REST API compliance testing literature that would strengthen novelty positioning — see 2.4.

### Detailed Assessment

#### 1. Significance — Adequate

- **1.1** The problem is real: the roadmap study establishes that incorrect-behavior bugs (43%) substantially outnumber crash/hang bugs (23%) in VDBMSs, and current fuzzers (VDBFuzz) target only the minority crash subset — see 1, 2.2. API compliance defects are a tractable slice of this gap that admit a contract oracle where general result-correctness does not.
- **1.2** The practical impact is bounded but meaningful: 36 acknowledged bugs across five VDBMSs (28 fixed) shows the approach finds real issues, but the yield is heavily concentrated on Milvus (51 submissions, 22 acknowledged) and Qdrant (26 submissions, 11 acknowledged) — see Table 3. MeiliSearch (3 submissions, 0 acknowledged), Chroma (1 submission, 0 acknowledged), and Weaviate (30 submissions, 3 acknowledged) contribute minimal adjudicated signal, so cross-system generalization is claimed primarily for two systems rather than five.
- **1.3 [minor, fixable]** The scope is appropriately positioned as complementary to crash-focused fuzzing (VDBFuzz) and not claiming to solve the harder result-correctness oracle problem (ANN recall, ranking) — see 1, 5. The paper is honest that 75% of yield is boundary/validation compliance and that soft result-correctness remains open.

#### 2. Novelty — Adequate

- **2.1** TestVDB is the first LLM-driven realization of VDBMS API compliance defect detection—the roadmap flags this as an open direction, and VDBFuzz (crash-oracle-based) does not target this defect class — see 1, 6.
- **2.2** Contract-Truth Separation (CTS) is a clear design principle contribution: separating the LLM assertion layer from a truth layer that falsifies via maintainer-authority evidence (source, issue history, by-design intent) is not present in VDBFuzz, RESTler, EvoMaster, NoREC, TLP, or DQE — see 3.3, 6. The dev-reviewer's three-anchor design (reproduction, source-grounding, threat-model) instantiates this principle.
- **2.3** The contract hallucination propagation observation is novel: when one LLM family both generates a contract and judges compliance, hallucinated constraints are self-confirmed — see 4. The 12 by-design cases (25% of 48 adjudicated submissions) provide qualitative evidence. The mitigation (source-grounded falsification) is instantiated in CTS.
- **2.4 [major, fixable]** Related Work coverage has gaps that weaken novelty positioning: the paper cites RESTler and EvoMaster for REST API fuzzing but does not cite LLM-as-oracle papers (e.g., LLM-based test oracle generation, LLM-driven metamorphic testing) that would clarify the delta from prior LLM-oracle work. Similarly, schema fuzzers like Schemathesis are mentioned only in the evaluation footnote but not positioned in Related Work, and LLM-based API testing (beyond fuzzing) is absent — see 6.
- **2.5 [minor, fixable]** The multi-system empirical study is a novelty contribution but is weakened by the signal concentration on two systems (Milvus and Qdrant) — see 3.1. The breadth probes on Weaviate, MeiliSearch, and Chroma do not provide statistical evidence of cross-system generalization.

#### 3. Soundness — Adequate

- **3.1** The controlled retrospective on the same 52-candidate population is the strongest evidence: comparing claim-only (4-judge layer) vs source-grounded (dev-reviewer's source anchor) shows FP suppression lifts from 31% to 81% (2.6×) while retaining 96.7% of TPs (n=30) — see 3.3. The blind re-adjudication design (label-isolated agents, outcomes hidden) mitigates bias.
- **3.2** The maintainer-adjudicated precision (69.2%, 36/52) is an honest end-to-end operating point, with the sensitivity interval [43.9%, 80.5%] explicitly accounting for the 30 pending submissions — see 3.3.
- **3.3** The single-layer counterfactual analysis provides credible evidence that the dev-reviewer does not trade away recall: all 27 candidates killed by the suppression layer were verified as true FPs (7 via live re-probe on v2.6.19, 20 via blind LLM adjudication), giving dev-reviewer precision 27/27 — see 3.3. The end-to-end precision lift (45.6% → 69.2%, +23.7 pp) is claimed without recall cost.
- **3.4 [major, fixable]** The threat-model prior evaluation (RQ4) is explicitly labeled "exploratory, not a contribution" with negative results (blindspot indicators never populated, dev-reviewer unstable across runs, n=5 below significance) — see 3.4. This component is presented in the approach (§3.3) and Figure 1 but its evaluation does not support its claimed role.
- **3.5 [minor, fixable]** The single-LLM and schema-fuzzer baseline comparisons are methodologically sound but use different ground truths and populations, making direct numerical comparison difficult — see 3.3, Table 4. Single-LLM uses LLM self-judgment (25.5%), schema fuzzer uses API-acceptance (37%), while TestVDB uses maintainer adjudication (69.2%).
- **3.6 [minor, fixable]** End-to-end discovery recall is not established: pilots on held-out bugs reveal two fundamental limits (spec-completeness: OpenAPI does not describe dimension-mismatch handling; version-pinning: bug-present versions must be pinned to exact dev/patch, not major release) — see 3.3. The paper does not run TestVDB against bug-present old versions to measure full discovery recall.
- **3.7** The model-free invariant oracles are the most defensible technical finding: cosine similarity > 1.0, incomplete index results (2/25 matching points returned), and payload filter violations depend on no LLM judgment, reproduce across vendors, and violate hard mathematical bounds — see 3.2. This subclass is well-distinguished from contract oracles.

#### 4. Verifiability — Adequate

- **4.1** The paper provides sufficient methodological detail to follow the work: the five-stage pipeline (contract extraction, attack generation, four-judge debate, dev-reviewer with three anchors, novelty gate) is described in §3 with implementation details (20 agents, GLM-5.2 backbone, high/low budget configurations) — see 3.1, Figure 1.
- **4.2** Artifact availability is declared: an anonymized repository (https://anonymous.4open.science/r/testvdb-anon-D644/) is promised with full prompts, target versions, and LLM-call budget — see 3.1. The link is declared but reachability cannot be verified pre-publication.
- **4.3** The evaluation protocols are adequately described: the controlled retrospective design (blind re-adjudication, label-isolated agents), the maintainer-adjudicated outcome categorization (acknowledged/by-design/rejected/pending/excluded), and the sensitivity interval construction are all disclosed — see 3.3.
- **4.4 [minor, fixable]** Reproducibility has minor gaps: exact candidate-to-submission ratios are not instrumented (the paper reports "on the order of a few hundred raw candidates per target" but not precise numbers), and LLM sampling configuration is described as "default Claude Code runtime with no explicit temperature override" rather than specifying parameters — see 3.1.
- **4.5 [minor, fixable]** Threats to Validity is comprehensive and honest (internal validity: maintainer acknowledgment as weak ground truth; selection bias: submission filtering not fully instrumented; external validity: same-population ablation is Milvus-plus-Qdrant only; construct validity: defect classification is title-based; LLM variance: 99.1% pairwise agreement reported; contamination: GLM-5.2 may have seen pre-2024 Milvus source; recall scope: 96.7% is judgment-layer retention, not end-to-end discovery recall; excluded-set: 17 of 29 excluded are Milvus) — see 3.5.

#### 5. Presentation — Adequate

- **5.1** The structure is logical and complete: Introduction motivates the problem, Background defines the scope, Approach describes the pipeline and CTS, Contract Hallucination motivates the design, Evaluation addresses RQ1-RQ3 plus exploratory RQ4, Related Work positions against competitors, Conclusion summarizes.
- **5.2** The figures are clear: Figure 1 shows the assertion layer (LLM contract + 4-judge) falsified by the truth layer (dev-reviewer with three anchors) — the validated source anchor is solid, the unvalidated reproduction and threat-model anchors are dashed-gray, making the evaluated vs unevaluated boundary explicit — see Figure 1.
- **5.3** The tables are well-designed: Table 3 (yield and maintainer outcomes) is clear; Table 4 (precision/ground-truth comparison) makes the asymmetry explicit rather than disguising it — see 3.1, 3.3.
- **5.4 [minor, fixable]** The writing has minor language issues: some sentences are long and could be clearer (e.g., the opening sentence of §3.1), and a few typos remain (e.g., "by-design" vs "by design" inconsistency).
- **5.5 [minor, fixable]** Notation consistency: the paper uses both "by-design" and "by design" (hyphenated vs unhyphenated), and both "maintainer-adjudicated" and "maintainer adjudicated".

### Questions for Authors

- **Q1:** Can you clarify the status of the threat-model prior? It is presented as a component in §3.2 and Figure 1 but its evaluation (RQ4) is labeled "exploratory, not a contribution" with negative results. Should this be removed from the core contribution list, or is it included as a design-level component whose evaluation is future work?
- **Q2:** For Related Work, can you discuss LLM-as-oracle papers (LLM-based test oracle generation, LLM-driven metamorphic testing) to clarify the delta from prior LLM-oracle work? Similarly, can you position schema fuzzers like Schemathesis in Related Work rather than only in the evaluation footnote?
- **Q3:** The cross-system generalization is claimed for five VDBMSs, but 69% of submissions and 69% of adjudicated issues come from Milvus and Qdrant. Can you clarify whether the contribution is "multi-system" (five systems with breadth probes) or "two-system + breadth probes" — and how this should be interpreted for generalization?
- **Q4:** For the baseline comparison, can you make explicit which arms use which ground truths and why direct numerical comparison is problematic? The current presentation in Table 4 and §5.3 is honest about the asymmetry but could be clearer.
- **Q5:** Can you provide more detail on the candidate-to-submission ratio? The paper reports "on the order of a few hundred raw candidates per target" but not precise numbers. How many raw candidates were generated vs submitted for each VDBMS?

---

## Reviewer 2: Area Specialist

**Overall Recommendation:** Weak Reject

### Summary

The paper proposes TestVDB, an LLM-driven system for detecting API compliance defects in Vector Database Management Systems (VDBMSs). API compliance defects are behaviors where a VDBMS silently accepts inputs or produces outputs that violate its documented contract (e.g., accepting `nprobe=0` that should be rejected, or returning incorrect status codes). The core technical contribution is Contract-Truth Separation (CTS), a design principle that isolates LLM-generated contract assertions from a "truth layer" that falsifies them using maintainer-authority evidence (source code, issue history, by-design intent). TestVDB implements CTS via a 20-agent pipeline: contract extraction from docs, attack generation by specialized agents, a four-judge debate producing Stage-2 candidates, a dev-reviewer applying CTS counter-evidence (three anchors: clean reproduction, source-grounded verification, threat-model cross-check), and a novelty gate. The authors report 111 submissions across five VDBMSs (Milvus, Qdrant, Weaviate, MeiliSearch, Chroma), with 36 maintainer acknowledgments (28 fixed, 8 accepted-open). On a controlled retrospective over 52 adjudicated candidates, the dev-reviewer's source anchor improves false-positive suppression from 31% to 81% while retaining 96.7% of true positives. The paper identifies "contract hallucination propagation"—where one LLM family generating the contract and judging compliance self-confirms hallucinated constraints—and positions CTS as the mitigation. The work addresses the VDBMS testing roadmap's call for compliance oracles and complements crash-focused fuzzing (VDBFuzz).

### Core Strengths

- **S1:** Contract hallucination propagation is a real, under-studied problem in LLM-driven testing — see 2.1. The 12 by-design cases (25% of adjudicated submissions) provide concrete evidence that single-layer LLM judgment self-confirms fabricated constraints.
- **S2:** Controlled retrospective design (same-population, blind re-adjudication) credibly isolates the dev-reviewer's contribution — see 3.1. The 31%→81% FP suppression lift at 96.7% TP retention on the same 52-candidate pool is the paper's strongest quantitative evidence.
- **S3:** Model-free invariant oracle subclass (cosine distance >1.0 for identical vectors, incomplete index results) is the most defensible technical finding — see 2.4. It violates hard mathematical bounds, reproduces across vendors, and requires no LLM judgment.
- **S4:** Honest boundary reporting. The paper explicitly scopes to 75% boundary/validation yield, acknowledges crash bugs are excluded by design, and admits result-correctness (ANN recall, ranking) remains open — see 1, 3.1, 5.

### Core Weaknesses

- **W1:** Unvalidated threat-model anchor weakens the claimed three-anchor design — see 3.3. Only the source anchor is measured; reproduction and threat-model anchors are "design-level and not yet evaluated," yet the contribution statement treats CTS as a validated three-anchor system.
- **W2:** Single-layer counterfactual mixes ground truths, undermining the 45.6% precision claim — see 3.2. The 27 suppressed candidates use live re-probes (7) plus LLM-adjudicated proxy (20), not maintainer adjudication, so the end-to-end single-layer arm is on a different ground truth than the TestVDB baseline.
- **W3:** Cross-system generalization claimed primarily for Milvus and Qdrant; Weaviate, MeiliSearch, and Chroma contribute near-zero adjudicated signal — see 1.2. The title's "multi-system empirical study" overstates the breadth of validated evidence.

### Detailed Assessment

1. **Significance** — Adequate
   - **1.1** The problem is real and important: incorrect-behavior bugs (43%) substantially outnumber crash/hang bugs (23%) in VDBMSs per the cited roadmap study, and current fuzzers (VDBFuzz) detect only crashes, leaving the majority without a practical oracle — see 1, 2.1.
   - **1.2** The contribution is meaningful but bounded: TestVDB targets a tractable subset (boundary/validation compliance, 75% of yield) and complements rather than replaces crash-focused fuzzing. It does not solve result-correctness oracles (ANN recall, ranking), which the roadmap flags as the central open challenge — see 1, 5. This is useful but not necessary impact.

2. **Novelty** — Adequate
   - **2.1** Contract-Truth Separation (CTS) is a new design principle for LLM-driven testing. The problem it addresses—contract hallucination propagation—is not characterized in prior LLM-based testing literature (checked via Taipalus 2024 roadmap and abstract search for multi-agent debate; du2023improving could not be fetched for full verification). The dev-reviewer's source-grounded falsification anchor is a concrete mitigation — see 2.3, 4.
   - **2.2** Multi-agent debate design is consistent with emerging patterns (du2023improving; Hegazy 2024 on diversity-of-thought debate; SWE-Debate 2025 on competitive debate for software issues) but adapted to API compliance with a novel falsification layer. The adaptation (four-judge debate + dev-reviewer) is recognizable as new within VDBMS testing — see 2.2, 2.3.
   - **2.3 [major, fixable]** Missing related work: SWE-Debate (2025) "Competitive Multi-Agent Debate for Software Issue Resolution" uses multi-agent debate for fault localization and patch generation, conceptually similar to the paper's multi-agent verification approach. Positioning against this work would clarify novelty. See background.md for details.
   - **2.4** Model-free invariant subclass (cosine-bounded, completeness) is an instance of the "derivable" oracle class and is novel in VDBMS context — see 2.2, 3.2.

3. **Soundness** — Weak
   - **3.1** Controlled retrospective (RQ3) is the paper's strongest evidence. On the same 52 adjudicated candidates, source-grounded judgment lifts FP suppression from 31% to 81% while retaining 96.7% of TPs. This isolates the dev-reviewer's contribution credibly — see 3.3.
   - **3.2 [major, fixable]** Single-layer counterfactual precision (45.6%) mixes ground truths: 7/27 suppressed candidates verified by live re-probes (strong ground truth) plus 20/27 by LLM-adjudicated proxy (weak ground truth). The end-to-end single-layer arm therefore combines maintainer-adjudicated baseline (36/52) with mixed-ground-truth suppression, making the 45.6% vs 69.2% comparison unsound. The paper acknowledges the asymmetry in Table 4 but should not present this as an end-to-end precision lift without a common ground truth — see 3.3, Table 4.
   - **3.3 [major, fixable]** Threat-model anchor is unvalidated. The contribution statement presents CTS as a three-anchor design (reproduction, source, threat-model), but only source is measured; reproduction is not exercised in the retrospective, and threat-model blindspot indicators "were never populated" (RQ4). Thus the claimed three-anchor counter-evidence design is not evaluated — see 2.3, 3.4, 3.6.
   - **3.4** Aggregate maintainer-adjudicated precision (69.2%) is reported as an end-to-end operating point, not as the "after" arm of an ablation. The paper correctly notes this is measured on a different population (five libraries, adjudicated submissions only) and provides a sensitivity interval [43.9%, 80.5%] for pending submissions — see 3.3. This is honest but limits the strength of the end-to-end claim.
   - **3.5** RQ4 (threat-model prior) is reported as an "exploratory negative result" with n=5 TPs below significance. The paper correctly emphasizes this is not a stable estimate of dev-reviewer TP recall (the controlled retrospective measures that at 96.7%) — see 3.4. This is appropriate caveat-leaving.
   - **3.6 [minor, fixable]** Schema fuzzer baseline is hand-written with 19 probes; while it demonstrates boundary violations are catchable by spec-driven fuzzing (conceding TestVDB's marginal value is state/semantic + FP-suppression), the comparison is limited by scale. The paper acknowledges this limitation — see 3.3.

4. **Verifiability** — Adequate
   - **4.1** Artifact declaration: The paper promises an anonymized artifact at anonymous.4open.science with "full LLM-call budget," per-target cost, and all 111 submissions with maintainer outcomes — see 2.1, 5. Link is declared as reachable (do not verify by cloning). If delivered as promised, this supports reproduction.
   - **4.2** Textual description of method is sufficient to follow the pipeline: five stages, 20 agents (4 heavy-reasoning on high-budget GLM-5.2, 16 low-budget on low-budget GLM-5.2), per-target cost (~10^3 calls, ~2×10^6 tokens). Key design choices (threat-model prior, four-judge debate, three anchors) are described — see 2.1-2.4.
   - **4.3 [minor, fixable]** Threats to validity section is thorough but should explicitly flag the ground-truth asymmetry in the single-layer counterfactual (3.2) as a construct validity threat. It mentions "mixed proxy ground truth" for the 27 suppressed candidates but does not categorize it as a threat — see 3.6.

5. **Presentation** — Adequate
   - **5.1** Structure is logical: intro/motivation → approach (CTS + pipeline) → evaluation (RQ1-4) → related work → conclusion. Case studies (RQ2) effectively trace TP/FP boundary and model-free invariants — see 1-4.
   - **5.2 [minor, fixable]** Notation inconsistency: Table 4 column headers mix "Precision" (a ratio) with probe→accept rates for schema fuzzer (37% is 7/19 probes, not candidate precision). The footnote clarifies but the column label is inconsistent — see Table 4.
   - **5.3 [minor, fixable]** Figure 1 (overview) is clear but the threat-model anchor is gray/dashed with "not yet evaluated" in caption, while the contribution statement (Introduction) presents CTS as a validated three-anchor design. This discrepancy should be reconciled — see Figure 1 vs 1.
   - **5.4** Writing is generally clear but some sentences are dense (e.g., "Single-layer counterfactual: precision lift without recall cost" paragraph). Minor language polishing would help — see 3.3.

### Questions for Authors

- **Q1:** Can you re-run the single-layer counterfactual with maintainer adjudication on the suppressed candidates (or at least the 7 live-reprobed) to establish a common ground truth? This would resolve the mixed-ground-truth threat and strengthen the 45.6% precision claim — intended effect: upgrade 3.2 [major, fixable] if resolved.
- **Q2:** Can you report the reproduction anchor's performance (even if on a smaller cohort) so the three-anchor design is partially validated rather than entirely design-level? Or reframe CTS as "source-anchored falsification" with reproduction/threat-model as future work — intended effect: resolve 3.3 [major, fixable] and align contribution statement with evaluated components.
- **Q3:** Can you position against SWE-Debate (2025) or similar multi-agent software debugging work in Related Work? This would clarify the novelty delta in the multi-agent design space — intended effect: resolve 2.3 [major, fixable].

---

## Reviewer 3: General Reviewer

**Overall Recommendation:** Weak Accept

### Summary
The paper presents TestVDB, an LLM-driven system for detecting API compliance defects in vector database management systems (VDBMSs). API compliance defects are bugs where a system silently accepts inputs or behaviors that violate its documented contract (e.g., accepting invalid parameter values like nprobe=0, or returning success where rejection is prescribed). The authors identify a key problem—contract hallucination propagation, where the same LLM family both generates a contract from documentation and judges compliance, leading to self-confirmation of hallucinated constraints. Their solution is Contract-Truth Separation (CTS), which introduces a dev-reviewer agent that falsifies LLM-generated assertions using maintainer-authority evidence (source code, reproduction, and threat-model cross-checks). Across five VDBMSs, TestVDB produced 111 submissions; 52 have been adjudicated by maintainers, with 36 acknowledged (28 fixed, 8 accepted-open), yielding 69.2% adjudicated precision. A controlled retrospective on the same 52 candidates shows that the dev-reviewer's source-grounded verification anchor improves false-positive suppression from 31% to 81% while retaining 96.7% of true positives.

### Core Strengths
- **S1:** The contract-hallucination propagation observation is a well-argued, technically sound insight that directly motivates the CTS design and is grounded in concrete evidence from the submission adjudication. — see 1.1, 1.2
- **S2:** The controlled retrospective experiment (same-population ablation) provides convincing within-system evidence for the dev-reviewer's source anchor contribution on the 52 adjudicated candidates. — see 3.1, 3.2
- **S3:** The paper is exceptionally well-structured and honest about scope and limitations, with clear positioning against VDBFuzz and explicit boundaries on what is not solved (soft result-correctness). — see 5.1, 5.2
- **S4:** The model-free invariant oracle subclass (cosine similarity bounded in [-1,1], 200-success implies data stored) is a robust, LLM-independent finding that reproduces across vendors. — see 2.3

### Core Weaknesses
- **W1:** Aggregate end-to-end precision (69.2%) rests on a narrow adjudicated base: 52 adjudicated out of 111 submissions, with signal concentrated on two systems (Milvus and Qdrant), leaving cross-system generalization provisional. — see 1.1, 1.3
- **W2:** The 25% by-design rate is presented as evidence of contract-hallucination propagation, but the paper does not establish that this rate is higher than a counterfactual baseline (e.g., human-written contracts). — see 2.1, 2.2

### Detailed Assessment

1. **Significance** — Adequate
   - **1.1** The problem addressed—API compliance defects in VDBMSs—is real and under-served by existing tools (VDBFuzz targets only crashes), and the authors convincingly show that incorrect-behavior bugs (43%) substantially outnumber crash/hang bugs (23%) using their cited studies~\cite{roadmap25,bugstudy25}. The contribution is the first end-to-end realization of non-crash compliance detection for this domain.
   - **1.2 [major, unfixable]** However, the impact is bounded by concentration on two systems (Milvus and Qdrant) and a narrow adjudicated base (52/111 submissions). Table 3 shows that MeiliSearch (3 submissions, 0 adjudicated signal), Chroma (1 submission, 0 adjudicated signal), and Weaviate (30 submissions, 3 acknowledged, 21 pending) contribute near-zero or unvalidated signal. The paper explicitly claims cross-system generalization "primarily for Milvus and Qdrant" (Introduction), which limits the claimed significance to two systems rather than the five-VDBMS scope implied by the aggregate statistics.
   - **1.3** The authors position TestVDB as complementary to VDBFuzz (crash-focused) and as not solving the general result-correctness oracle problem (ANN recall, ranking), which is honest but also bounds the contribution to the API-compliance slice of incorrect behavior.

2. **Novelty** — Adequate
   - **2.1** The contract-hallucination propagation observation is presented as a new characterization of a failure mode in LLM-driven testing: when one LLM family both generates a contract and judges compliance, hallucinated constraints are self-confirmed. The authors provide qualitative evidence (12 by-design cases, 25% of 48 adjudicated submissions) and a concrete example (formalizer's "complexity requirement" from constant.go, shown by source grounding to be a guard against a historical performance regression rather than a behavioral constraint). This is a credible insight that motivates CTS.
   - **2.2 [major, unfixable]** The 25% by-design rate is used to substantiate the prevalence of contract hallucination propagation, but the paper does not compare this against a baseline (e.g., contracts written by human experts, or contracts from a different LLM family). Without a counterfactual, we cannot assess whether 25% is high, low, or expected for this task. The authors acknowledge this as a "qualitative finding" and flag a "frequency study" as future work, which is appropriate, but the reliance on this rate to motivate CTS limits the strength of the novelty claim.
   - **2.3** The Contract-Truth Separation design principle (isolating LLM assertions from a maintainer-authority truth layer) is presented as novel, and the instantiation (dev-reviewer with three anchors: clean reproduction, source-grounded verification, threat-model cross-check) is a concrete contribution. The source anchor is validated; the reproduction and threat-model anchors are "designed but not yet evaluated" (Introduction, Section 3.3), which limits the evaluated portion of the novelty to the source anchor alone.

3. **Soundness** — Adequate
   - **3.1** The main claims are supported by appropriate methods. The 111-submission multi-system study (RQ1) provides the end-to-end evidence; the controlled retrospective (RQ3, same 52 adjudicated candidates) provides strong within-system evidence for the dev-reviewer's source anchor contribution; and the single-layer counterfactual (RQ3, removing the FP-suppression chain) shows precision lift without recall cost. The case studies (RQ2) illustrate the TP/FP boundary concretely.
   - **3.2 [major, fixable]** The single-layer counterfactual precision figure (45.6%) is computed by combining the maintainer-adjudicated baseline (36/52) with the 27 killed candidates, but the 27 are validated under mixed ground truth: 7 by live re-probe on v2.6.19, and 20 by 5-batch blind LLM adjudication. The paper states "over-kill 0/27" (all confirmed FP), but the text does not clearly separate which of the 27 were validated under which ground truth. This makes the 45.6% figure harder to assess, as it mixes proxy ground truth (LLM adjudication) with maintainer adjudication. Separating the two arms would strengthen the claim.
   - **3.3 [minor, fixable]** The schema-fuzzer baseline (Section 5.3, schema-aware boundary fuzzer baseline paragraph) reports a 37% "probe→accept" rate (7 of 19 probes surfaced API-accepted candidates), but this is not directly comparable to the other precision rates, which are candidate-level precisions after filtering. The paper flags this with a dagger (†) in Table 4, but the text does not explicitly state that 7 of 19 is a generation-level acceptance rate, not a post-filter precision. This creates a risk of misinterpretation when readers compare arms in the table.
   - **3.4** The threat-model prior ablation (RQ4) is appropriately reported as an exploratory negative result with small n (=5 TP, 7 FP), and the authors emphasize that the 20%/60% TP recall figures are the control/experiment split, not a stable estimate of dev-reviewer TP recall. The controlled retrospective (96.7% TP retention) is the authoritative figure for the source anchor's TP retention, so the RQ4 negative result does not undermine the main claims.

4. **Verifiability** — Adequate
   - **4.1** The paper provides sufficient detail to follow the work. The five-stage pipeline is clearly explained (Section 3), implementation details (agent count, budget configurations, LLM backbone) are specified, and the full prompts are promised to be in the anonymized artifact. The evaluation sections describe the RQs, datasets, and methods in enough detail to understand how the results were produced.
   - **4.2 [minor, fixable]** The paper declares an anonymized artifact URL (https://anonymous.4open.science/r/testvdb-anon-D644/) but states it will be "made public on acceptance." The URL is not verified as reachable in the paper itself, so the verifiability rests on the text rather than the artifact. This is consistent with the rubric (judge from the text whether the link is declared and reachable; we cannot verify reachability until post-publication), but the paper should explicitly state that the artifact was not verified at submission time if that is the case.
   - **4.3** The internal coherence is strong. The abstract/intro/eval/conclusion numbers agree: 111 submissions, 52 adjudicated (36 acknowledged, 12 by-design, 4 rejected), 69.2% adjudicated precision, 31%→81% FP suppression lift, 96.7% TP retention on the same 52-candidate retrospective. The precision interval [43.9%, 80.5%] correctly reflects the 30 pending sensitivity analysis. The self-consistency checks (Section 5.5, LLM variance) show 99.1% pairwise agreement, which supports the reliability of the judgment layer.

5. **Presentation** — Adequate
   - **5.1** The paper is well-structured, with a logical flow from problem formulation → approach → hallucination motivation → evaluation → related work → conclusion. The figures are clear: Table 1 (oracle-candidate exclusion) justifies the LLM choice; Figure 1 (pipeline overview) effectively visualizes the assertion/truth layer separation; the tables (Table 3 yield, Table 4 baselines) are legible and informative.
   - **5.2 [minor, fixable]** The writing is generally clear, but there are occasional densely packed sentences that could be simplified for readability. Example: Section 5.1, defect-type-distribution paragraph ("Of the 36 acknowledged true positives, 27 (75%) are boundary/validation...") packs defect-type distribution, complementarity with VDBFuzz, and the model-free invariant subclass into one long block. Splitting this into separate paragraphs would improve readability.
   - **5.3** The language is professional and appropriate for a technical paper. The notation is consistent (C_LLM, C_true), and the figures use clear color coding (blue for assertion layer, red for truth layer). The formatting follows ACM style correctly.

### Questions for Authors
- **Q1:** The 25% by-design rate (12 of 48 adjudicated submissions) is central evidence for contract-hallucination propagation. Can you provide any comparison point—even if qualitative—to help readers assess whether this rate is high or low? For example, do you have any anecdotal evidence from prior VDBMS bug reports about how often human-written contracts would flag by-design behaviors as violations? — This would strengthen the motivation for CTS by showing that the LLM's self-confirmation is worse than a human baseline.
- **Q2:** In the single-layer counterfactual (Section 5.3, single-layer counterfactual paragraph), the 27 killed candidates were validated under mixed ground truth (7 by live re-probe, 20 by 5-batch LLM adjudication). Can you separately report the single-layer precision if only the 7 live-reprobed FPs are counted, versus if all 27 are counted? — This would clarify whether the 45.6% figure is robust to the choice of proxy ground truth.
- **Q3:** The schema-fuzzer baseline (Section 5.3, schema-aware boundary fuzzer baseline paragraph) surfaced 7 API-accepted candidates from 19 probes, which you note is a generation-level acceptance rate rather than a post-filter precision. Do you have any estimate of what the post-filter precision would be if these 7 candidates were run through your four-judge debate and dev-reviewer? — This would enable a more direct comparison to TestVDB's candidate precision.
- **Q4:** The threat-model anchor (Section 3.3) is designed to catch the 3 residual false positives that the source anchor misses (silent-absent cases where no validation code exists to cite). Can you provide any concrete examples of such silent-absent cases from your 16 FP corpus, even if hypothetical, to illustrate what this anchor would target? — This would help readers understand the gap that the threat-model anchor is intended to fill.

---

## Meta-Review

### Criterion Consensus

| Criterion | Reviewer 1 | Reviewer 2 | Reviewer 3 | Meta-Review |
|---|---|---|---|---|
| Significance | Adequate | Adequate | Adequate | **Adequate** |
| Novelty | Adequate | Adequate | Adequate | **Adequate** |
| Soundness | Adequate | Weak | Adequate | **Adequate** |
| Verifiability | Adequate | Adequate | Adequate | **Adequate** |
| Presentation | Adequate | Adequate | Adequate | **Adequate** |
| **Recommendation** | **Weak Accept** | **Weak Reject** | **Weak Accept** | **ACCEPT** |

### Meta Recommendation
**ACCEPT**

All five criteria reach consensus **Adequate** — four unanimously (Significance, Novelty, Verifiability, Presentation), and Soundness by majority (R1 and R3 at Adequate vs R2 at Weak). With no consensus Poor and no consensus substance Weak, the verdict follows the no-substance-Weak path to ACCEPT.

The agreement is meaningful, not a rubber stamp. All three reviewers independently converged on the same core technical merit — the controlled retrospective on 52 candidates (31%→81% FP suppression at 96.7% TP retention) and the model-free invariant oracles (cosine > 1.0 reproducing across Milvus and Qdrant) — and on the same central scope concern that the cross-system claim rests on two systems, not five.

R2's dissent to Weak Reject is the signal the author must take seriously. Its Soundness Weak is driven by two [major, fixable] items that R1 and R3 *also* flagged (as fixable blemishes rather than tier-lowering): the single-layer counterfactual mixes maintainer-adjudicated ground truth with LLM-proxy judgment (7 live + 20 LLM out of the 27 suppressed), so the 45.6%→69.2% "lift" is not an apples-to-apples comparison; and the three-anchor CTS design is only validated on the source anchor (reproduction not exercised; threat-model blindspots never populated). These do not sink the paper because the same-population controlled retrospective (RQ3) stands on its own as the core evidence — but the framing oversells what was measured. R3 additionally carries two [major, unfixable] items (the 25% by-design rate has no counterfactual baseline; the two-system concentration is inherent in the data) that bound the contribution's strength rather than its validity. None of these is a [major, unfixable] consensus — they do not block acceptance — but together they define the revision workload below.

### Priority Revisions
The main problems the author must fix, ranked by impact on the verdict. Items 1-4 are each flagged [major, fixable] by two or more reviewers (cross-reviewer consensus on the fix, even where tiers diverge); items 5-6 are single-reviewer flags that still warrant attention.

1. **Re-run or reframe the single-layer counterfactual on a common ground truth.** The 27 suppressed candidates use 7 live re-probes (strong) + 20 LLM-adjudicated proxy (weak), combined with the maintainer-adjudicated 36/52 baseline — so the 45.6% vs 69.2% "precision lift without recall cost" (§5.3) is not an end-to-end comparison on one ground truth. Either re-adjudicate the suppressed set under maintainer triage (at least the 7 live-reprobed), or explicitly relabel the 45.6% as a mixed-ground-truth estimate and stop presenting it as a clean e2e lift. (R2 3.2, R3 3.2 — both [major, fixable]; this is the primary driver of R2's Weak.)

2. **Align the CTS contribution claim with what was evaluated.** The contribution statement and Figure 1 present CTS as a three-anchor counter-evidence design, but only the source anchor is measured; reproduction is not exercised in the retrospective and the threat-model anchor's blindspot indicators were never populated (RQ4 negative). Reframe the validated contribution as "source-grounded falsification" and demote reproduction + threat-model to design-level / future work — or partially evaluate them on a smaller cohort. (R2 3.3 + R1 3.4 / W2 — both [major, fixable]; R3 2.3 concurs on the evaluated-vs-claimed gap.)

3. **Soften the cross-system generalization claim.** Milvus and Qdrant account for 77/111 submissions (69%) and 36/52 adjudicated issues (69%); MeiliSearch (3 submissions) and Chroma (1) contribute near-zero adjudicated signal, and Weaviate's 30 submissions are mostly pending (21). This is unanimous across all three reviewers. Reframe the title/contribution's "multi-system empirical study" as "two-system validated + three-system breadth probes," matching the paper's own honest admission in the intro.

4. **Add the missing Related Work.** Position against SWE-Debate (competitive multi-agent debate for software issues) in the multi-agent design space, LLM-as-oracle / LLM-driven metamorphic testing to clarify the novelty delta from prior LLM-oracle work, and Schemathesis (schema fuzzers) in Related Work rather than only in the evaluation footnote. (R1 2.4 + R2 2.3 — both [major, fixable].)

5. **Bound or complete end-to-end discovery recall.** The pilot already surfaces two structural limits (spec-completeness — OpenAPI does not describe dimension-mismatch handling; version-pinning — bug-present versions must be pinned to exact dev/patch, not the major release). State these as the recall ceiling explicitly and either run a held-out old-version cohort or position full recall as bounded future work. (R1 3.6 / W4 [minor, fixable].)

6. **Acknowledge the 25% by-design rate has no counterfactual baseline.** The rate motivates CTS but readers cannot judge whether 25% is high or low without a comparison (e.g., human-written contracts, or a different LLM family). A qualitative comparison point or a clearer "this is an observation, not a measured prevalence" framing would resolve it. (R3 2.2 [major, unfixable] — single-reviewer; bounds contribution strength, not validity.)

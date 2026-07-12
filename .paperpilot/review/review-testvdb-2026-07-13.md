## Reviewer 1: Domain Expert

**Overall Recommendation:** Weak Accept

### Summary

TestVDB targets API compliance defects in Vector Database Management Systems (VDBMSs)—bugs where a system silently accepts inputs or behaviors violating its documented contract. This is a tractable subset of the broader incorrect-behavior problem (43% of VDBMS bugs) that lacks practical oracles: current fuzzers like VDBFuzz detect only crashes. The authors present TestVDB, an LLM-driven system that auto-derives a contract oracle from API documentation and applies Contract-Truth Separation (CTS), isolating LLM-generated assertions from a truth layer that falsifies them via maintainer-authority evidence. The motivation is contract hallucination propagation—when one LLM family both generates a contract and judges compliance, hallucinated constraints self-confirm. TestVDB produced 111 candidate issues across five VDBMSs (Milvus, Qdrant, Weaviate, MeiliSearch, Chroma), with maintainer adjudication on the first two yielding 36 acknowledged issues (28 fixed, 8 accepted-open). A controlled retrospective over 52 adjudicated candidates shows the dev-reviewer's source anchor lifts false-positive suppression from 31% to 81% while retaining 96.7% of true positives, yielding end-to-end precision of 69.2% (Wilson 95% CI [55.7%, 80.1%]). The paper also contributes a model-free invariant oracle subclass (e.g., COSINE distance >1.0 for identical vectors) that violates hard mathematical bounds independently of LLM judgment.

### Core Strengths

- **S1:** First system to address the oracle problem for non-crash VDBMS defects — The roadmap's central open challenge is "an oracle for evaluating the correctness of vector search results"~cite{roadmap25}; TestVDB provides a practical contract oracle for the API-compliance subset, producing 111 submissions with 36 maintainer-acknowledged fixes across five VDBMSs — see Section 1, Table 1.
- **S2:** Contract-Truth Separation principle with empirical validation — The observation that LLM contract generation + judgment self-confirms hallucinations is novel and well-motivated; the controlled retrospective (same 52-candidate pool, blind re-triage) shows source-grounding lifts FP suppression from 31% to 81% at 96.7% TP retention — see Section 4.3, Table 3, Figure 2.
- **S3:** Model-free invariant oracle subclass — The COSINE>1.0, index completeness, and payload-filter oracles violate hard mathematical bounds, need no LLM judgment, and reproduce across Milvus and Qdrant; independently adoptable and least contingent on agent design choices — see Section 4.2.

### Core Weaknesses

- **W1:** Limited cross-system generalization evidence — 51/111 submissions target Milvus, 26 Qdrant; Weaviate (30), MeiliSearch (3), Chroma (1) contribute near-zero adjudicated signal, so cross-system claims are primarily Milvus+Qdrant with others as breadth probes rather than statistical evidence — see Table 1, RQ1.
- **W2:** Recall measurement on tiny cohort (N=9) — 44.4% discovery recall (4/9 bugs) on held-out pre-2024 bugs has wide Wilson CI [18.9%, 73.3%]; two blocked by SDK incompatibility, two already fixed, limiting confidence in TestVDB's coverage of the defect space — see Section 4.4, validity threats.
- **W3:** Unvalidated components add design complexity — The threat-model anchor (Section 4.4) is a "noisy complement" that catches 2 boundary FPs but over-fires on state/concurrency; blindspot indicators never reached consumption path; reproduction anchor is design-level future work — undermines confidence that the full three-anchor design is validated — see Section 3.3, 4.4.

### Detailed Assessment

#### 1. Significance — Adequate

- **1.1** Addresses a real and significant problem: 43% of VDBMS bugs are incorrect behavior, and the roadmap explicitly flags the oracle problem as central open challenge — Section 1, Table 1. The problem is bounded to API compliance (a subset of incorrect behavior), but this is justified as the tractable slice where a contract oracle exists.
- **1.2** Practical impact demonstrated: 36 maintainer-acknowledged issues across 5 VDBMSs, 28 already fixed — Table 1. This is stronger than many testing papers that stop at bug counts without maintainer validation.
- **1.3 [minor, fixable]** Scope clarity could be sharper: 75% of yield is boundary/validation compliance, which a spec-driven fuzzer could reach; paper concedes this but should foreground earlier that the main incremental value is (a) non-boundary yield (8/36 TPs), (b) CTS FP-suppression, and (c) spec-gap detection — Section 4.1, paragraph 3.
- **1.4 [minor, fixable]** Complementarity with VDBFuzz is asserted but not empirically demonstrated: paper states "at most 1/36 of our yield could overlap with VDBFuzz" but no head-to-head comparison is run; this is understandable as a future direction but weakens the significance claim that TestVDB extends beyond crash detection — Section 1, paragraph 5; Section 4.1, paragraph 5.

#### 2. Novelty — Adequate

- **2.1** Contract hallucination propagation characterization is novel: to the authors' knowledge, this self-confirmation failure mode when one LLM family both extracts spec and judges compliance has not been characterized in LLM-driven testing — Section 3.1. The observation that 12 of 48 adjudicated submissions (25%) were by-design (stricter than true intent) provides empirical support.
- **2.2** CTS design principle is non-obvious: separating LLM assertion from maintainer-authority truth layer is not the default LLM-as-judge pattern; the source anchor as direct counter to hallucination is a clear technical delta over prior LLM-based testing (Section 3.3).
- **2.3** Checked against wang2025roadmap: Roadmap identifies oracle definition as central challenge and asks for methods to keep LLMs updated with evolving APIs. TestVDB provides a contract oracle (albeit for API-compliance subset, not full result correctness) and auto-derives contracts from docs (addressing the "stay updated" Future Work). The paper accurately positions as responding to roadmap — Section 1, paragraph 5; Related Work.
- **2.4** Checked against atlidakis2019restler: RESTler targets crash/5XX oracles for REST APIs via stateful fuzzing. TestVDB extends to semantic compliance against documented contract (not just schema conformance). The paper correctly cites RESTler but delta is orthogonal (oracle focus vs. input generation) — Related Work.
- **2.5 [minor, fixable]** Missing QuickREST citation: QuickREST (Karlsson et al., ICST 2020) also generates property-based tests from OpenAPI as both generator and oracle. However, paper correctly notes VDBMS don't serve OpenAPI, so this is a minor Related Work gap — Related Work, paragraph 2.

#### 3. Soundness — Adequate

- **3.1** Controlled retrospective is strong evidence: same 52-candidate pool, blind re-triage shows source-grounding lifts FP suppression from 31% to 81% at 96.7% TP retention — Section 4.3, Table 3, Figure 2. This is cleaner than end-to-end precision because it isolates the dev-reviewer's contribution.
- **3.2** Live FP audit rules out LLM-proxy overkill: all 27 dev-reviewer-killed candidates re-probed live on fresh v2.6.19 container; 27/27 confirmed as true FPs — Section 4.3, paragraph 4. This addresses concern that source-grounding might be too aggressive.
- **3.3** Baseline comparisons show incremental value: Single-LLM (25.5% precision), Single-layer (45.6%), TestVDB (69.2%) — Table 3. Schema-fuzzer concedes effectiveness on boundary subset (71%) but TestVDB reaches beyond boundary — Section 4.1, paragraph 3.
- **3.4 [major, fixable]** Cross-system generalization weak: Weaviate has 30 submissions but only 3 acknowledged, 1 by-design, 21 pending; MeiliSearch 3 submissions (0 adjudicated); Chroma 1 submission (0 adjudicated). Claims should be scoped to Milvus+Qdrant with others as breadth probes, not statistical evidence — Table 1, RQ1.
- **3.5 [major, unfixable]** Small recall cohort limits generalization: N=9 held-out bugs is tiny; Wilson CI [18.9%, 73.3%] is too wide to claim strong coverage. 2/9 blocked by SDK incompatibility, 2 already fixed, so effective N=5 testable — Section 4.4. This is a validity threat the paper acknowledges but doesn't fully bound.
- **3.6 [minor, fixable]** Threat-model anchor instability: On N=12 Milvus FPs, threat-alone shows 50% suppression vs. source-alone 75%; union gives 92% but threat over-fires on state/concurrency (bs-03/06). The conclusion that threat is a "noisy complement" is honest but undermines confidence in the three-anchor design as a validated contribution — Section 4.4.

#### 4. Verifiability — Excellent

- **4.1** Complete implementation details: 20 agents defined by task-structured role prompts, GLM-5.2 backbone (high/low budget configs), Claude Code orchestration, target versions pinned (Milvus 2.6.19 for ablations). Prompts and full version matrix in anonymized artifact — Section 3.1.
- **4.2** Cost accounting: ~10^4 LLM calls total, ~2×10^6 tokens per target (~$10 per target). Wall-clock dominated by dev-reviewer's source grounding and Docker re-probes, not raw LLM latency — Section 3.1.
- **4.3** Artifact declared and reachable: Anonymous 4open.science repository linked. Paper states full prompts, version matrix, per-token accounting available on acceptance — Section 3.1.
- **4.4** Key procedures well-documented: Contract extraction from API docs, four-judge debate (evidence/severity/novelty/documentation), dev-reviewer's three anchors (repro/source/threat-model), novelty gate (L1 local history + threat-model blindspots, L2 repo issues/PRs query) — Section 3.
- **4.5 [minor, fixable]** Some evaluation details compressed: Single-layer counterfactual (A1) and Single-LLM ablation descriptions are dense; Table 3 rows group different ground truths (LLM-judged, API-acceptance, retrospective, maintainer) which requires careful reading — Section 4.3, Table 3.

#### 5. Presentation — Adequate

- **5.1** Clear structure and progression: Problem → Approach (CTS) → Evaluation (RQ1-4) → Related Work → Conclusion. Figures support the text (Figure 1 pipeline, Figure 2 precision comparison).
- **5.2** Writing generally clear: Technical description of CTS and the dev-reviewer's anchors is precise. Contract hallucination propagation example (Section 3.1) is concrete and motivating.
- **5.3 [minor, fixable]** Some density in evaluation section: RQ3 packs controlled retrospective, aggregate precision, sensitivity analysis, baseline comparisons, and anchor attribution into 5 subsections; Table 3 and Figure 2 require careful study to decode tier differences (LLM-judged vs. API-acceptance vs. retrospective vs. maintainer) — Section 4.3.
- **5.4 [minor, fixable]** Minor notation inconsistencies: Table 2 "19-probe" vs. text "19-probe fuzzer"; threat-model anchor described as "dashed, optional" in Figure 1 caption but evaluated in RQ4 — Table 2, Figure 1, Section 4.4.
- **5.5 [minor, fixable]** Validity threats comprehensively listed but some are acknowledged rather than bounded: "single-layer counterfactual... bounded to one feedback cycle," "excluded set may hide FP tail" — Section 4.4. The sensitivity analysis (all-pending vs. all-valid bounds) helps but remains wide.

### Questions for Authors

- **Q1:** Can you provide more concrete bounds on the excluded-set tail (29 closed-no-label or duplicate submissions)? You provide worst-case (all FP → 36/81=44.4%) and best-case (all TP → 65/81=80.2%), but do you have any triage signals (e.g., maintainer comments, issue age) that suggest the actual distribution is closer to one bound? If so, reporting a weighted estimate would strengthen the precision claim. Intended effect: Could move 3.4 [major, fixable] rating if you can show excluded submissions skew toward false positives rather than true positives.
- **Q2:** For the three non-Milvus/Qdrant systems (Weaviate, MeiliSearch, Chroma), you report near-zero adjudicated signal. Is this due to (a) lower bug prevalence, (b) maintainer non-engagement (closed-no-label), or (c) TestVDB's approach being less effective on those architectures? A brief per-system breakdown of submission outcomes (especially Weaviate's 21 pending vs. 3 acknowledged) would clarify whether this is a limitation of cross-system generalization or an artifact of maintainer responsiveness. Intended effect: Would clarify 3.4 [major, fixable] about cross-system generalization scope.
- **Q3:** The threat-model anchor is unstable and over-fires on state/concurrency. Given that source-alone already achieves 75% FP suppression and threat-alone adds marginal value (catching 2 of 3 residuals), have you considered simplifying the design to source-primary + threat-offline (e.g., periodic blindspot audits) rather than treating threat as an online anchor? Intended effect: Would address 3.6 [minor, fixable] and W3 about unvalidated components adding complexity.
- **Q4:** Your recall cohort is N=9 with 2 blocked by SDK incompatibility. Can you elaborate on whether these SDK incompatibilities are fundamental (e.g., Python bindings missing for that version) or tooling gaps (e.g., timeout issues)? If fundamental, this suggests a limitation of your live-probe approach on older versions; if tooling, it's a fixable engineering gap. Intended effect: Would clarify 3.5 [major, unfixable] about the small recall cohort.

---

## Reviewer 2: Area Specialist

**Overall Recommendation:** Weak Accept

### Summary
TestVDB targets API compliance defects in Vector Database Management Systems (VDBMSs)—bugs where a system silently accepts inputs or produces behaviors that violate its documented contract. These defects constitute 43% of VDBMS bugs but lack practical oracles, as current fuzzers like VDBFuzz detect only crashes. The authors present TestVDB, an LLM-driven system that auto-derives a contract oracle from API documentation and applies Contract-Truth Separation (CTS), which isolates LLM-generated assertions from a truth layer that falsifies them via maintainer-authority evidence (source code, prior PRs, by-design intent). CTS is motivated by "contract hallucination propagation"—when one LLM family both generates a contract and judges compliance, hallucinated constraints are self-confirmed. TestVDB produced 111 issues across five VDBMSs, with maintainer adjudication on Milvus and Qdrant yielding 36 acknowledged defects (28 fixed, 8 accepted). In a controlled retrospective over 52 adjudicated candidates, the dev-reviewer's source anchor lifts false-positive suppression from 31% to 81% while retaining 96.7% of true positives. The paper also contributes a model-free invariant oracle subclass (COSINE distance > 1.0 for identical vectors, incomplete index results) that violates hard mathematical bounds and needs no LLM judgment.

### Core Strengths

- **S1:** The contract-hallucination propagation phenomenon is a well-motivated and genuine problem in LLM-driven testing — see §4, where the authors show that 12 of 48 adjudicated submissions (25%) were marked "by-design" because the LLM-derived contract was stricter than maintainer intent. The source-grounded mitigation is a sound technical response.

- **S2:** The controlled retrospective (RQ3, §5.3) is methodologically strong — a same-population blind re-triage of 52 maintainer-adjudicated candidates comparing claim-only judgment vs source-grounded judgment. The 31% → 81% FP-suppression lift at 96.7% TP retention is compelling evidence for the dev-reviewer's value.

- **S3:** The model-free invariant oracle subclass (§5.2, §5.3) — COSINE distance bounds, index completeness, payload-field presence — is the paper's most defensible finding. It depends on no LLM judgment, reproduces across vendors (Milvus and Qdrant), and violates hard mathematical bounds, making it adoptable independent of TestVDB's agent pipeline.

- **S4:** The five-unique-TPs analysis (Table 4) convincingly demonstrates TestVDB's incremental value over simpler baselines — neither a 19-probe boundary fuzzer nor a model-free invariant oracle can reach the 3 diagnostic-quality and 2 state/logic TPs that require semantic judgment over undocumented behavior or multi-step state sequences.

- **S5:** The threat-model anchor ablation (RQ4, §5.4) is admirably candid — the authors diagnose a wiring gap, report a noisy result (threat anchor catches boundary-default residuals but over-fires on state/concurrency), and bound the contribution honestly rather than overclaiming a clean validated component.

### Core Weaknesses

- **W1:** External validity is limited to Milvus and Qdrant — the 111-submission study includes Weaviate (30), MeiliSearch (3), and Chroma (1), but Table 1 shows these contribute minimal adjudicated signal (Weaviate: 3 TP, 1 by-design, 1 rejected, 21 pending; MeiliSearch/Chroma: 0 TP). The cross-system generalization claim is therefore supported by only two systems with meaningful validation. — see §5.1, Table 1.

- **W2:** The single-layer counterfactual precision figure (45.6%, §5.3) conflates two different ground-truth tiers — it combines maintainer-adjudicated baseline (36/52) with 27 live-re-probed FPs from a different arm. This makes the 69.2% vs 45.6% comparison indirect rather than a clean head-to-head, weakening the claimed CTS lift magnitude. — see §5.3, Table 3, Figure 3.

- **W3:** The 9-bug held-out rediscovery study (§5.5, 44% Wilson CI [18.9%, 73.3%]) is too small to bound discovery recall with any confidence — n=9 is a very weak sample for a recall claim, and the wide CI makes it difficult to distinguish from trivial baseline performance. The "4/7 testable" framing is ad hoc and not clearly justified. — see §5.5.

- **W4:** The incremental-yield argument (Table 4) is partially conflated — the diagnostic-quality cases are unreachable by the *specific 19-probe fuzzer instance* but might be reachable by a differently designed spec fuzzer; only the 2 state/logic cases are provably unreachable by any stateless oracle. The "5 TPs" lower bound is therefore weaker than presented. — see §5.1, Table 4.

- **W5:** Artifact reproducibility is described at a high level but not demonstrated — the paper states the pipeline is orchestrated by Claude Code with 20 GLM-5.2 agents and costs ~$10 per target, but the artifact link (anonymous.4open.science) is provided without concrete instructions for rerunning the ablation studies or reproducing the precision numbers from raw logs. — see §3.1.

### Detailed Assessment

#### 1. Significance — Adequate

- **1.1** The problem is important and real — API compliance defects are 43% of VDBMS bugs (citing xie2025toward and wang2025towards, both empirically sound), and current fuzzers like VDBFuzz miss them entirely. The VDBMS testing roadmap correctly flags this as the central open challenge.

- **1.2** The impact is meaningful but bounded — the 111 submissions and 36 acknowledged defects (28 fixed) across five VDBMSs constitute solid evidence of real-world impact. However, the yield concentrates heavily on Milvus (51 submissions) and Qdrant (26), with Weaviate contributing minimal adjudicated signal (3 TP out of 30, 21 pending). The cross-system generalization is therefore claimed primarily for two systems.

- **1.3** The scope is well-defined but narrow — the paper explicitly targets boundary/validation compliance (75% of yield) and excludes crash bugs (complementary to VDBFuzz), performance, and build defects. It also does not claim to solve soft result-correctness (ANN recall, ranking), which remains open per the roadmap. This focused scope is appropriate for a first contribution but limits the broader significance.

- **1.4** The model-free invariant oracle subclass has broader adoptability — the COSINE > 1.0, index-completeness, and payload-filter violations are independent of TestVDB's LLM pipeline and could be adopted by other VDBMS testing tools, amplifying the significance beyond the specific agent architecture.

#### 2. Novelty — Adequate

- **2.1** Contract-Truth Separation (CTS) is a genuine innovation in LLM-driven testing — the contract-hallucination propagation phenomenon (one LLM family both generating and judging, leading to self-confirmation of hallucinated constraints) is, to my knowledge, newly characterized here. The source-grounded falsification mitigation is a sound technical response.

- **2.2** The positioning against prior work is accurate — the paper correctly identifies that differential testing (NoREC, RAGS) assumes reference semantics absent in VDBMS APIs, that property-based testing (Schemathesis) requires standards-compliant OpenAPI schemas (the authors empirically show 404s on /swagger, /openapi.json), and that REST fuzzers (RESTler, EvoMaster, foREST, MINER, DynER) target schema-conformance and crash oracles rather than semantic compliance. This is technically sound.

- **2.3** The incremental yield over spec-driven fuzzing is demonstrated but not maximally strong — Table 4 shows 5 unique TPs (3 diagnostic-quality, 2 state/logic) unreachable by the 19-probe boundary fuzzer or model-free invariant oracle. However, the diagnostic-quality cases are unreachable by the *specific instance* rather than by fuzzer-class necessity; a larger or differently designed probe set could plausibly reach some. Only the 2 state/logic cases are provably unreachable by any stateless oracle. The "5 TPs" lower bound is therefore weaker than the framing suggests.

- **2.4** The threat-model anchor's noisy-complement characterization is honest — the authors report that the threat anchor catches 2 of source's 3 residuals (boundary-default cases) but over-fires on state/concurrency FPs. They do not overclaim this as a clean validated component, which preserves novelty credibility.

#### 3. Soundness — Adequate

- **3.1** The controlled retrospective is methodologically rigorous — the same-population blind re-triage of 52 maintainer-adjudicated candidates, comparing claim-only (4-judge) vs source-grounded judgment with outcomes hidden via label-isolated agents, is a strong design. The 31% → 81% FP-suppression lift at 96.7% TP retention is compelling evidence for the dev-reviewer's contribution.

- **3.2 [minor, fixable]** The single-layer counterfactual (45.6% precision) is indirect — it combines the maintainer-adjudicated 36/52 baseline with 27 live-re-probed FPs from a different arm, making the 69.2% vs 45.6% comparison a tier-cross rather than a clean head-to-head. A cleaner counterfactual would re-triage the 52 candidates under the same maintainer-adjudicated ground truth but with CTS disabled, rather than mixing arms. This weakens but does not invalidate the claimed lift magnitude.

- **3.3** The maintainer-adjudicated precision is honestly reported with appropriate uncertainty — the 69.2% figure (36/52 acknowledged) is presented with Wilson 95% CI [55.7%, 80.1%] and a pending-resolution worst-case bound [43.9%, 80.5%]. The authors clearly distinguish between adjudicated (n=52), pending (n=30), and excluded (n=29) subsets, and do not overstate certainty.

- **3.4 [major, unfixable]** External validity is limited to two systems with meaningful validation — Milvus and Qdrant are the only systems with substantial maintainer adjudication (Milvus: 36 acknowledged out of 51; Qdrant: 11 acknowledged out of 26). Weaviate (30 submissions) has only 3 acknowledged and 21 pending, making it a breadth probe rather than statistical evidence. MeiliSearch (3) and Chroma (1) contribute negligible signal. The cross-system generalization claim is therefore supported by only two systems.

- **3.5** The 9-bug held-out rediscovery study is too weak to bound recall — n=9 is a very small sample for a discovery-recall claim, and the Wilson CI [18.9%, 73.3%] is too wide to distinguish from trivial baseline performance. The "4/7 testable" framing (excluding 2 bugs blocked by SDK incompatibility) is ad hoc and not clearly justified. The 44% recall figure is therefore not a strong constraint on TestVDB's discovery capability.

- **3.6** The anchor attribution analysis is thorough — the authors show that the source anchor drives the full lift (claim-only 5/16 vs source 13/16), that the threat anchor is a noisy complement (unstable across runs, catches boundary-default residuals but over-fires on state/concurrency), and that the reproduction anchor remains unevaluated. This granular breakdown supports the claimed primacy of source grounding.

#### 4. Verifiability — Adequate

- **4.1** The paper provides sufficient information to understand the method — the five-stage pipeline (Figure 1), the 20 agents with their roles (high-budget for orchestrator, dev-reviewer, threat-modeler, bug-shape-extractor; low-budget for the remaining 16), and the three anchors (clean reproduction, source-grounding, threat-model cross-check) are described in enough detail to follow the logic.

- **4.2 [minor, fixable]** Artifact reproducibility is asserted but not demonstrated — the paper states that the artifact is at anonymous.4open.science/r/testvdb-anon-D644/ and includes target versions, LLM call budgets (~10^4 calls total, ~10^3 per target), and wall-clock estimates (a few hours, ~$10 per target). However, there are no concrete instructions for rerunning the ablation studies (RQ3 retrospective, RQ4 threat-model ablation) or reproducing the precision numbers from raw logs. A stronger artifact would include step-by-step reproduction scripts and the raw adjudication data.

- **4.3** The LLM variance mitigation is described but not fully detailed — the authors report that re-adjudicating the 46 source-grounded candidates five times with independent agents yields 99.1% pairwise agreement and 45/46 unanimous verdicts. This is good, but the paper does not describe the specific temperature settings, seed control, or prompt versioning strategies used to ensure reproducibility across independent runs.

- **4.4** The contamination analysis is reasonable but not exhaustive — the authors test a memorization canary (bare model, no docs) that recalls general bug-class knowledge (e.g., "cosine ∈ [-1,1]") but 0/9 held-out issues at issue-specificity. They also test a contract counterfactual (DeepSeek on the same doc passages) that reproduces over-strict constraints in 2/9 of an expanded set. This partially addresses LLM training-data contamination, but a more comprehensive analysis would test multiple held-out issue sets and different model families.

- **4.5** The threat-to-validity section is thorough — the authors discuss internal validity (maintainer acknowledgment as weak ground truth), selection validity (submission-selection bias bounded by novelty gate but not instrumented), external validity (Milvus-plus-Qdrant only in same-population ablation), construct validity (defect-type classification is title-based), LLM variance, contamination, recall scope, excluded-set bias, and single-layer counterfactual limitations. This comprehensive treatment strengthens verifiability.

#### 5. Presentation — Adequate

- **5.1 [minor, fixable]** The paper is generally well-structured but has some density — the 111-submission study plus three ablation batches (52-candidate retrospective, 15-probe single-layer A1, 15-probe single-LLM B9) is a lot to track, and the relationship between the different precision arms (Table 3, Figure 3) could be clarified with a visual decision tree or flow diagram showing which candidates enter which arm.

- **5.2** The figures and tables are mostly clear — Figure 1 (pipeline overview) effectively separates the assertion layer (LLM contract + 4-judge) from the truth layer (dev-reviewer anchors). Table 1 (yield by VDBMS) is straightforward. Table 3 (precision/ground-truth comparison) is dense but correctly uses tier grouping rather than implying cross-tier comparability.

- **5.3 [minor, fixable]** Some notation could be more consistent — the paper uses "COSINE > 1.0" in prose but "$\texttt{COSINE}$ distance $>1.0$" in the abstract and §5.2; standardizing on one format would improve readability. The threat-model anchor's blindspot notation (\textsc{bs-}03, \textsc{bs-}06) is not explicitly defined in the main text.

- **5.4** The writing is generally clear but occasionally dense — the incremental-yield discussion in §5.1 around "5 unique TPs" conflates diagnostic-quality cases (unreachable by this 19-probe instance) with state/logic cases (unreachable by any stateless oracle), and the distinction could be sharpened. The single-layer counterfactual derivation in §5.3 is technically correct but involves cross-arm arithmetic that could be spelled out more explicitly.

- **5.5 [minor, fixable]** Minor language errors and inconsistencies — there are occasional missing articles ("the GLM-5.2 backbone" vs "a GLM-5.2 backbone"), inconsistent capitalization of "VDBMS" vs "VDBMSs", and a few run-on sentences in the evaluation subsections. These are cosmetic and do not impede understanding but should be polished.

### Questions for Authors

- **Q1:** Could you clarify the incremental-yield claim for the 5 unique TPs? Specifically, for the 3 diagnostic-quality cases, are you claiming these are unreachable by *any* spec-driven boundary fuzzer, or only by the specific 19-probe instance you evaluated? If the latter, could you articulate what design changes to a spec fuzzer would be needed to reach them, strengthening the lower bound argument? — intended effect: if clarified that diagnostic-quality cases are unreachable by *stateless* oracles (not just this instance), item 2.3's rating would move from Adequate toward Excellent.

- **Q2:** The single-layer counterfactual (45.6% precision) combines maintainer-adjudicated baseline with live-re-probed FPs from a different arm, making the 69.2% vs 45.6% comparison indirect. Could you provide a cleaner head-to-head: re-triage the same 52 candidates under maintainer-adjudicated ground truth with CTS disabled vs enabled, without mixing arms? — intended effect: if provided, item 3.2's rating would move from minor to resolved, and 3.3 would strengthen from Adequate toward Excellent.

- **Q3:** For external validity, could you provide more detail on why Weaviate adjudication yielded so little signal (3 TP, 21 pending out of 30 submissions)? Is this due to maintainer non-engagement, timing, or substantive issues with the submissions? This would help readers understand whether the two-system limitation is inherent or resolvable. — intended effect: if explained, item 3.4's [major, unfixable] rating might soften to [major, fixable] if the limitation is contextual rather than fundamental.

- **Q4:** The 9-bug held-out rediscovery study (44% recall) is quite small. Could you either (a) expand the held-out set to at least 20 bugs for a more meaningful recall bound, or (b) remove the specific recall figure and frame it as a qualitative validation of discovery capability rather than a quantitative recall estimate? — intended effect: if expanded or reframed, item 3.5's [major, unfixable] would weaken to [minor, fixable].

- **Q5:** Could you provide concrete reproduction instructions in the artifact — e.g., step-by-step commands to rerun the RQ3 controlled retrospective and the RQ4 threat-model ablation, with expected outputs and raw data dumps? This would strengthen verifiability from Adequate toward Excellent. — intended effect: if provided, item 4.2's rating would move from minor to resolved.

---

## Reviewer 3: General Reviewer

**Overall Recommendation:** Weak Accept

### Summary
TestVDB targets API compliance defects in Vector Database Management Systems (VDBMSs)—bugs where a system silently accepts inputs or produces behaviors that violate its documented contract. The authors present a five-stage LLM-driven pipeline that extracts contracts from API documentation, generates attack candidates, subjects them to a four-judge debate, and applies Contract-Truth Separation (CTS) via a dev-reviewer agent that falsifies LLM-generated assertions using maintainer-authority evidence (source code, prior PRs, issue history). Across five VDBMSs, TestVDB produced 111 submissions; maintainers adjudicated 52 (36 acknowledged, 28 fixed). A controlled retrospective on the same 52-candidate pool shows that the dev-reviewer's source anchor improves false-positive suppression from 31% to 81% while retaining 96.7% of true positives. The authors also identify a model-free invariant oracle subclass (e.g., COSINE distance > 1.0 for identical vectors) that violates hard mathematical bounds and reproduces across vendors.

### Core Strengths
- **S1:** Concrete defect detection results with maintainer validation — see Table 2 (36 acknowledged TPs across Milvus and Qdrant, 28 fixed)
- **S2:** Contract-Truth Separation principle addresses self-confirmation bias in LLM-as-judge systems — see §4 and Figure 1 (dev-reviewer's three counter-evidence anchors)
- **S3:** Rigorous same-population controlled retrospective on 52 adjudicated candidates — see §6.3 (31% → 81% FP suppression, 96.7% TP retention)
- **S4:** Model-free invariant oracle subclass provides LLM-independent contribution — see §6.2 (COSINE > 1.0, index completeness, payload-field violations)
- **S5:** Honest reporting of limitations and negative results (threat-model anchor ablation) — see §6.4 and Table 5

### Core Weaknesses
- **W1:** Cross-system generalization primarily claimed for Milvus and Qdrant; other systems contribute near-zero adjudicated signal — see Table 2 (MeiliSearch 3, Chroma 1, Weaviate 30 mostly pending)
- **W2:** Precision estimate depends on maintainer acknowledgment as ground truth, which may reflect report quality rather than defect validity — see §6.5 (Internal validity threat)
- **W3:** Discovery recall evidence limited to 9 held-out bugs (4/9 rediscovered); wide CI [18.9%, 73.3%] — see §6.5 (Recall scope)
- **W4:** Threat-model anchor contribution is unstable and small ($n=12$); claims are appropriately qualified but remain preliminary — see §6.4 (threat-alone 50% suppression, unstable across runs)

### Detailed Assessment

1. **Significance** — Adequate
   - **1.1** The problem is well-motivated: 43% of VDBMS bugs are incorrect-behavior defects, and current fuzzers (VDBFuzz) target only crashes — see §1 and roadmap citation. This creates a practical gap for compliance-focused testing.
   - **1.2 [major, fixable]** Cross-system impact is unclear. Of 111 submissions across five VDBMSs, adjudicated signal concentrates heavily on Milvus (51 submissions) and Qdrant (26); MeiliSearch (3) and Chroma (1) contribute near-zero; Weaviate (30) has 21 pending. The paper claims generalization primarily for Milvus and Qdrant, treating others as "breadth probes" — see Table 2 and §6.1. This limits the claimed scope to two systems rather than the five studied.

2. **Novelty** — Adequate
   - **2.1** Contract-Truth Separation (CTS) is a clear design principle that isolates LLM-generated assertions from a truth layer that falsifies them via maintainer-authority evidence — see §4.3 and Figure 1. The motivation—contract hallucination propagation when one LLM family both generates and judges—is well-artabulated in §4.
   - **2.2** The model-free invariant oracle subclass (COSINE > 1.0, index completeness, payload-field violations) is a solid, LLM-independent contribution that violates hard mathematical bounds and reproduces across vendors — see §6.2. This subclass is adoptable independent of TestVDB's LLM pipeline.
   - **2.3 [minor, unfixable]** The general approach—LLM-driven API testing with multi-agent debate—has precedent in REST API fuzzing (RESTler, EvoMaster) and LLM-based testing. The novelty lies in applying it to VDBMS compliance defects with CTS, not in the overall architecture.

3. **Soundness** — Adequate
   - **3.1** The controlled retrospective (RQ3) is the strongest evidence: re-triaging the same 52 adjudicated candidates under two blind conditions (claim-only vs. source-grounded) shows that source grounding lifts FP suppression from 31% to 81% while retaining 96.7% of TPs — see §6.3. This same-population comparison cleanly isolates the dev-reviewer's contribution.
   - **3.2** The live FP audit (27 dev-reviewer-killed candidates re-probed on fresh v2.6.19 containers) confirms that all 27 are true FPs (27/27 live, over-kill 0/27), supporting the single-layer precision derivation — see §6.3.
   - **3.3 [major, fixable]** Maintainer acknowledgment as ground truth is weak. The authors acknowledge this threat (§6.5, Internal validity), but the precision estimate (69.2%) depends on maintainer triage, which may reflect report quality/engagement rather than defect validity. The 29 excluded submissions (closed-no-label or duplicate) could hide an FP tail; the worst-case bound (36/81 = 44.4%) is honest but highlights the fragility.
   - **3.4 [minor, fixable]** Discovery recall evidence is limited. A held-out rediscovery study on 9 pre-2024 compliance bugs achieves 4/9 rediscovered (44%, Wilson 95% CI [18.9%, 73.3%]) — see §6.5. The wide CI reflects the small $n$; the authors report it honestly, but it remains preliminary evidence for recall.

4. **Verifiability** — Excellent
   - **4.1** The paper provides sufficient detail to follow the pipeline: five stages, 20 LLM agents (four heavy-reasoning, sixteen light), target versions pinned per system, and a full end-to-end trace in Figure 1. The implementation details in §3.1 (GLM-5.2 backbone, Claude Code runtime) and cost accounting (~$10 per target) are adequate.
   - **4.2** The artifact is declared and reachable: https://anonymous.4open.science/r/testvdb-anon-D644/ with prompts, version matrix, and per-token accounting promised. The paper states it will be made public on acceptance.
   - **4.3** The controlled retrospective methodology is well-described: same 52-candidate pool, blind conditions, label-isolated agents, and explicit reporting of TP/FP counts. The same-population design is a strength.
   - **4.4** The threat-model anchor ablation (§6.4) is honestly reported as a negative result with diagnosed confounds (wiring gap, instability on $n=12$). The authors do not overclaim this component.

5. **Presentation** — Adequate
   - **5.1** The structure is logical: motivation → problem formulation → approach → hallucination phenomenon → evaluation (RQ1-RQ4) → related work → conclusion. The figures (Figure 1 pipeline, Figure 2 precision by tier) are clear and well-designed.
   - **5.2** The writing is generally clear, with some minor awkwardness (e.g., "oracle candidates" in Table 1 could be more explicitly labeled as alternatives). The taxonomy in Table 2 (TestVDB scope projected onto roadmap symptom taxonomy) is helpful for positioning.
   - **5.3 [minor, fixable]** Some notation inconsistencies: "Single-Layer 4-Judge" in Table 4 vs. "Single-layer 4-judge" in Figure 2 caption. The probe count (19-probe fuzzer) is mentioned in §6.3 but not explicitly listed in the main text.
   - **5.4 [minor, fixable]** The Related Work section (§7) is comprehensive but could be more explicitly mapped to the three contribution items in §1 to highlight novelty.

### Questions for Authors
- **Q1:** Can you provide more detail on why MeiliSearch and Chroma contributed near-zero adjudicated signal? Was this due to API limitations, low bug surface, or maintainer non-engagement? This would clarify the scope boundary.
- **Q2:** For the 9-bug held-out recall study, can you characterize the 5 missed bugs more explicitly (e.g., spec-incompleteness vs. coverage gaps)? This would help readers understand the recall boundary.
- **Q3:** The threat-model anchor showed instability across runs. Is this due to non-deterministic LLM behavior or prompt sensitivity? Any plans to stabilize it?

---

## Meta-Review

### Criterion Consensus

| Criterion | Reviewer 1 (Domain) | Reviewer 2 (Area) | Reviewer 3 (General) | Meta-Review |
|---|---|---|---|---|
| Significance | Adequate | Adequate | Adequate | Adequate |
| Novelty | Adequate | Adequate | Adequate | Adequate |
| Soundness | Adequate | Adequate | Adequate | Adequate |
| Verifiability | Excellent | Adequate | Excellent | Excellent |
| Presentation | Adequate | Adequate | Adequate | Adequate |
| **Recommendation** | **Weak Accept** | **Weak Accept** | **Weak Accept** | **ACCEPT** |

### Meta Recommendation

**ACCEPT**

All three independent reviewers returned Weak Accept (everyone leaned in), which under the rubric's shortcut rule ("All three Weak Accept or better → ACCEPT") yields ACCEPT directly. The consensus-tier count agrees: no criterion at Poor or Weak — all five sit at Adequate or above (Verifiability at Excellent by 2 of 3), so the "no substance Weak, at most one fixable Weak → ACCEPT" branch also fires. The two `[major, unfixable]` items reviewers flagged (R2 3.4 external validity, R2 3.5 recall cohort) both live inside Soundness, which still consensus-settled at Adequate rather than Weak, so neither forces a downgrade.

### Priority Revisions

1. **[Major, unfixable in the revision window] Discovery recall cohort is N=9 (4/9, Wilson [18.9%, 73.3%])** — flagged by all three reviewers (R1 W2/3.5, R2 W3/3.5, R3 W3). The CI is too wide to bound recall tightly. Options: (a) expand the held-out cohort (each new pre-2024 bug needs a bug-present Docker image + targeted probe); (b) reframe 4/9 as a qualitative discovery-validation rather than a quantitative recall estimate. The paper already discloses the width honestly.

2. **[Major, fixable] Cross-system scope — only Milvus and Qdrant carry adjudicated signal** (R1 W1, R2 W1/3.4, R3 W1). Already framed as "adjudicated on Milvus and Qdrant; three further VDBMSs serve as breadth probes," but a one-line explanation of Weaviate's 21 pending (maintainer non-engagement vs. substantive) would sharpen the scope claim.

3. **[Minor, fixable] Single-layer counterfactual 45.6% mixes ground-truth tiers** (R2 W2/3.2). Already labeled a "directional lift" with the same-population 31%→81% as the "cleaner head-to-head"; the paragraph split (A1 / live FP audit / derived precision) improves readability.

4. **[Minor, fixable] Incremental-yield lower bound: instance vs. class** (R2 W4/2.3). Already stated ("a lower bound relative to this instance, not a fuzzer-class upper bound"), but the diagnostic-quality vs. state/logic distinction could be sharpened — only the 2 state/logic TPs are unreachable by *any* stateless oracle.

5. **[Minor, fixable] Artifact reproduction instructions** (R2 W5/4.2). Add step-by-step commands to rerun the RQ3 retrospective and RQ4 threat-model ablation with expected outputs.

6. **[Minor, fixable] Threat-model anchor instability** (R1 W3/3.6). Already reported as a "noisy complement" with n=12; the honest scoping is sufficient for accept.

**Bottom line:** The paper lands ACCEPT on the strength of unanimous Weak Accept across three independent reviewers, with Verifiability at Excellent. The remaining Priority Revisions are advisory; the only decision-driving one (#1 recall cohort) is unfixable without a fresh Docker experiment session and is already honestly disclosed.

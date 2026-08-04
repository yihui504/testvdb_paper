# Peer Review v3 (post-v7) — TestVDB

> Three independent reviewers re-evaluated the paper after v7 revisions (SATORI two-axis reframe + cross-family 3-run union + structured-failure-mode diagnosis + symmetric kappa vs GLM 3-run union + GLM per-vendor recall + kappa consistency fix + CONFIRMED notation). Same rubric, independent of Rounds 1-2. Each draft passed an independent checker. Date: 2026-08-04.

---

## Reviewer 1: Domain Expert

**Overall Recommendation:** Weak Accept

### Summary

TestVDB targets documentation-implementation defects in Vector Database Management Systems (VDBMSs), where systems silently accept inputs that violate their API documentation. Because the documented boundary is natural-language prose rather than structured specifications, deterministic oracles (crash, differential, metamorphic, property-based, REST-API spec-derived) cannot adjudicate these accept/reject decisions, leaving an LLM as the practical oracle. The LLM introduces two false-positive failure modes: hallucination in claim extraction (inventing constraints the documentation does not state) and self-preference bias in judgment (same-family LLMs confirm their own extracted claims). The authors show multi-perspective judging raises precision but collapses recall. They introduce a dev-reviewer agent that acts as a source-grounded falsifier, reproducing candidates, cross-checking against implementation source, and trying to disprove them. TestVDB surfaced 107 candidate issues across three VDBMSs (Milvus, Qdrant, Weaviate); maintainers acknowledged 49 as true-positive defects (15 merged-PR-fixed). On a 48-candidate retrospective, the dev-reviewer reaches 67% precision and 74% recall (3-run ensemble), versus 37% recall without source grounding. A bidirectional probe against VDBFuzz explores complementary coverage.

### Core Strengths

- **S1:** Clear problem formulation and novelty delta — see 1.1, 1.2. The documentation-implementation defect class is well-characterized, and the exclusion argument (Table 2) convincingly shows why deterministic oracles cannot reach this residual.

- **S2:** Source-grounded falsification effectively addresses LLM reliability — see 2.1, 2.3. The dev-reviewer design breaks both hallucination (by falsifying against source rather than documentation) and self-preference bias (by using implementation as independent ground truth).

- **S3:** Empirical evaluation demonstrates practical impact — see 3.1, 3.2. 107 submitted issues with 49 maintainer-acknowledged true-positive defects (15 merged-PR-fixed) across three production VDBMSs is strong evidence of real-world impact.

- **S4:** Bidirectional VDBFuzz probe establishes complementary coverage — see 3.3. The systematic direction (26,000 requests, 0 of 14 silent-accept TPs reached) empirically validates the oracle complementarity claim.

### Core Weaknesses

- **W1:** Cross-family generalization is an open question — see 2.4. The full independent cross-model re-run shows the verdict is family-specific (κ = 0.14-0.51 vs. GLM), and the paper's headline results use only GLM-5.2. This limits the claim that source-grounded falsification reliably breaks self-preference bias.

- **W2:** Construct validity: "implementation-as-correct" assumption unaddressed — see 2.5. The dev-reviewer treats the implementation as correct to falsify documentation claims, but implementation bugs can wrongly falsify correct documentation. The 15 merged-PR fixes suggest the assumption often holds, but no analysis quantifies this false-negative rate.

- **W3:** External validity limited to VDBMS setting — see 3.4. Weaviate evaluation is yield-only (no controlled retrospective), and non-VDBMS portability claims are structural only, not empirically validated. One non-VDBMS case study would strengthen the transferability argument.

- **W4:** Operating point selection post-hoc — see 3.2. The 3-run union headline is selected post-hoc from four operating points without pre-registration, and Wilson CIs do not account for this selection. A Bonferroni correction widens CIs considerably.

### Detailed Assessment

1. **Significance** — Adequate

   - **1.1** [strength] The problem is well-motivated. More than half of VDBMS bugs manifest as functional failures (bug study cited), and the crash-oracle approach (VDBFuzz) structurally misses silent-accept defects (44 of 49 true positives do not crash). The economic cost of corrupted vector search results in retrieval-augmented LLM applications is clear. The defect class characterization is precise and the impact is bounded but real.

   - **1.2** [strength] The yield demonstrates practical impact. 107 submitted issues with 49 maintainer-acknowledged true-positive defects (15 merged-PR-fixed) across three production VDBMSs is meaningful evidence. The vendor distribution (Milvus 22 TP, Qdrant 14, Weaviate 13) shows the problem exists across systems, not a single target artifact. This is a "useful rather than necessary" contribution—practical impact in a specialized setting.

2. **Novelty** — Adequate

   - **2.1** [strength] Novelty delta over REST-API oracle tools is clear. I verified MASTOR (cached summary) and SATORI (cached full text). MASTOR generates oracles from source encoding implemented behavior; it cannot detect documentation-implementation gaps. SATORI generates response-field oracles from OpenAPI specifications; input-acceptance decisions on system-level prose are out of scope. The paper correctly characterizes both. TestVDB's source-grounded falsification targets exactly this gap, which is a non-obvious delta over the prior art.

   - **2.2** [strength] Novelty delta over documentation-derived oracles (AugmenTest, ChatAssert, Doc2OracLL) is clear. These tools treat the LLM as the final semantic arbiter, validating through runtime behavior. TestVDB falsifies against implementation source, which is what breaks self-preference bias. The bidirectional probe (RQ3) empirically validates this difference.

   - **2.3** [strength] Source-grounded falsification is a non-trivial mechanism. The dev-reviewer's three-check design (independently reproducible, evidence sufficient, falsifiable) and three anchors (clean-reproduction, source-grounded, threat-model) are novel contributions that address the specific LLM reliability failure modes diagnosed in Section 4. This is "real but incremental originality"—the LLM-as-judge framing is known, but the source-grounded falsifier application is new.

   - **2.4 [major, fixable]** Cross-family generalization is open. The full independent cross-model re-run (DeepSeek, Qwen, LongCat) shows the verdict is family-specific (κ = 0.14-0.51 vs. GLM). The paper acknowledges this (Section 5, "we cannot claim cross-family robustness"), but the headline results and claims are based on GLM-5.2 only. This limits the generalization of the self-preference bias mitigation. Fixability: A future revision could report cross-family median performance, or explicitly qualify claims as "GLM-5.2-specific." The fix requires additional experiments, not just text revision.

3. **Soundness** — Adequate

   - **3.1** [strength] RQ1 evaluation is sound. 107 submitted issues with 49 maintainer-acknowledged true-positive defects (15 merged-PR-fixed) is strong evidence of detection capability. The 68.1% yield precision on adjudicated submissions (Wilson 95% CI [56.6%, 77.7%]) is well-reported with appropriate confidence intervals. The vendor breakdown and defect-type characterization (optional-default parameters, search parameters, state operations) are thoughtful analysis.

   - **3.2** [strength] RQ2 evaluation on the 48-candidate retrospective is methodologically sound. The maintainer-adjudicated ground truth (27 TP, 21 FP) is appropriate. The single-LLM baseline (48%/56%/37%) provides a meaningful comparison. The source-grounding contribution isolation (disabling Step 3.5 drops recall from 74% to 19%) is a strong control showing the mechanism's effect. The per-run variance analysis (recall 15-78%) and the rationale for the any-confirmed ensemble are well-reasoned.

   - **3.3** [strength] RQ3 bidirectional probe is well-designed. The systematic direction (VDBFuzz on v1.18.2, 26,000 requests, 0 of 14 TPs reached) is generalizable evidence of complementarity. The two controlled cases (v1.4.0 crash-class, v1.18.0 silent-accept) isolate mechanisms (n=1 each) but are labeled appropriately. The #9045 root cause analysis (debug_assert vs. release build) is insightful and explains why crash-focused patching misses the residual.

   - **3.4 [major, unfixable]** External validity is limited to the VDBMS setting. Weaviate evaluation is yield-only (no controlled retrospective), so the 48-candidate retrospective covers only Milvus and Qdrant. Non-VDBMS portability claims (CouchDB, Elasticsearch) are structural only, not empirically validated—the paper acknowledges this explicitly. Result correctness of vector search is out of scope. This is a bounded scope: the contribution is proven in VDBMSs, and generalization beyond is claimed only on structural grounds, which is honest but limits the work's reach. This inheres in the contribution design and cannot be fixed without expanding the empirical scope, which is a new study.

   - **3.5 [minor, fixable]** Construct validity: "implementation-as-correct" assumption. The dev-reviewer treats the implementation as correct to falsify documentation claims, but implementation bugs can wrongly falsify correct documentation. The 15 merged-PR fixes suggest the assumption often holds, but the paper does not quantify this false-negative rate (acknowledged in limitations). Fixability: Add a brief analysis of the 23 by-design/rejected cases to characterize how many might be implementation bugs rather than documentation violations. This is text revision plus existing data analysis.

   - **3.6 [minor, fixable]** Internal validity: operating point selection post-hoc. The 3-run union headline is selected from four operating points without pre-registration. The Wilson CIs in Table 4 do not account for selection across operating points. The paper acknowledges this ("post-hoc, exploratory") and reports Bonferroni-corrected CIs (roughly [44,84]/[51,89]), plus bootstrap validation ([53,83]/[71,96]). Fixability: Report both the uncorrected CIs (current) and Bonferroni-corrected CIs more prominently, and explicitly state the operating point was selected post-hoc in the RQ2 prose. This is text revision.

4. **Verifiability** — Excellent

   - **4.1** [strength] The artifact is comprehensive. GitHub repository (https://github.com/yihui504/testvdb-anon) with 22 agent role definitions, target versions, per-token accounting, 48-candidate ground truth, and reproduction driver. The paper describes the pipeline cost (10^4 LLM calls, ~$10 per target) and the distribution across stages (Table 3). All agents run on GLM-5.2 via BigModel Anthropic-compatible API under default sampling.

   - **4.2** [strength] The dev-reviewer design is fully specified. Appendix excerpts role prompts for contract-formalizer and dev-reviewer (full 22 in artifact). The three-check falsification logic, three anchors, and evidence-sufficiency standards are described in detail. Figure 3 provides a clear visual summary.

   - **4.3** [strength] Experimental protocols are reproducible. Docker-pinned VDBMS versions (Milvus 2.6.19, Qdrant v1.18.2, Weaviate v1.38.2). The 48-candidate retrospective is fully specified. The bidirectional VDBFuzz probe versions and budgets are documented. An independent researcher could reproduce the main results.

5. **Presentation** — Excellent

   - **5.1** [strength] Structure is logical and complete. Introduction → Background/Problem Setup → TestVDB Approach → False-Positive Problem → Dev-Reviewer → Evaluation → Related Work → Discussion/Limitations → Conclusion. Table 2 (exclusion argument) is early and clearly positions the LLM-derived oracle residual. The pipeline figure (Figure 1) and dev-reviewer falsification (Figure 3) are clear.

   - **5.2** [strength] Writing is clear and precise. The oracle exclusion argument (Table 2) is well-articulated. The false-positive mode diagnosis (Section 4) distinguishes hallucination from self-preference clearly. The threat model discussion (Section 6, three-check design) is thorough. No pervasive language errors or ambiguity.

   - **5.3** [strength] Figures and tables are effective. Table 2 (exclusion argument) is a strong conceptual contribution. Figure 1 (pipeline) and Figure 3 (dev-reviewer falsification) are clear. Figure 4 (per-run recall) visualizes variance well. Tables are well-labeled with appropriate confidence intervals.

   - **5.4 [minor, fixable]** Two minor LaTeX issues. Line 389: `\emph{static test oracle generation}` should be `\texttt{static test oracle generation}` for consistency with other tool names. Table 4 caption: "\emph{Per-run band}" and "\emph{any-confirmed}" should use `\textit{}` for italics in captions rather than `\emph{}`.

### Questions for Authors

- **Q1:** On the cross-family generalization limitation (2.4), you report κ = 0.14-0.51 vs. GLM. Beyond acknowledging the limitation, have you explored any cross-family ensemble strategies (e.g., majority voting across DeepSeek+GLM+Qwen) that might improve robustness? If not, would this be a promising direction for future work, or does the family-specific verdict pattern suggest ensemble would not help?

- **Q2:** On the "implementation-as-correct" assumption (3.5), you note the 15 merged-PR fixes suggest the assumption often holds. Have you analyzed the 23 by-design/rejected cases to estimate how many might be implementation bugs rather than documentation violations? Even a rough characterization (e.g., "most appear to be silent accepts of invalid input per maintainer rationale") would help bound the false-negative rate.

- **Q3:** On the external validity limitation (3.4), you report CouchDB and Elasticsearch probes that validate portability but find no defects (both APIs validate strictly). Do you view this as evidence that mature non-VDBMS APIs have stronger validation, or as insufficient probe coverage? Would one additional non-VDBMS case study (e.g., a system with known documentation-implementation defects) be feasible to strengthen the transferability claim?


---

## Reviewer 2: Area Specialist

**Overall Recommendation:** Accept

### Summary

TestVDB targets documentation-implementation defects in Vector Database Management Systems (VDBMSs), where a system silently accepts inputs or behaviors that violate its natural-language API documentation. Because the boundary is prose rather than structured specification, classical oracles (crash detection, differential testing, property-based testing) cannot adjudicate these accept/reject decisions, leaving an LLM as the practical oracle. The authors instantiate a four-stage pipeline (claim extraction, test generation, execution, confirmation) that uses LLMs to read documentation, generate tests, and adjudicate responses. Two failure modes produce false positives: hallucination in extraction and self-preference bias in judgment. A multi-perspective judging baseline raises precision but collapses recall, so the authors introduce a dev-reviewer agent that acts as a source-grounded falsifier, reproducing each candidate and cross-checking against implementation source. TestVDB surfaced 107 submitted issues across Milvus, Qdrant, and Weaviate, with 49 maintainer-acknowledged true-positive defects (15 fixed via merged PR). On a 48-candidate retrospective, the source-grounded dev-reviewer reaches 67% precision and 74% recall against 37% recall without source anchoring. A bidirectional probe against VDBFuzz shows complementary coverage: TestVDB reaches a crash-class defect by contract reasoning, while VDBFuzz misses TestVDB silent-accept defects under its current templates.

### Core Strengths

- **S1:** Clear articulation of the documentation-implementation defect class and why it eludes existing oracles (Table 1, §2) — see 1.1, 1.2
- **S2:** Well-motivated source-grounded falsification as a countermeasure to LLM self-preference bias, with both theoretical rationale (§2.4, §3) and experimental validation (§4.2, Table 7) — see 2.3, 3.2
- **S3:** Strong empirical grounding: 107 real-world submissions with 49 maintainer-adjudicated true positives, plus controlled retrospectives isolating the dev-reviewer's contribution (§4) — see 3.1, 3.3

### Core Weaknesses

- **W1:** Limited cross-family validation (single LLM backbone GLM-5.2; DeepSeek/Qwen/LongCat show family-specific verdicts with κ ≤ 0.32) — see 3.4 [major, unfixable]
- **W2:** External validity threats: Weaviate evaluation is yield-only (no controlled retrospective), and transfer beyond VDBMSs is claimed only on structural grounds with minimal probe evidence (§5, §6) — see 3.5 [major, fixable]

### Detailed Assessment

#### 1. Significance — Adequate

- **1.1** **Defining a real, costly problem.** The paper targets a prevalent defect class: 49 maintainer-acknowledged true positives across three production VDBMSs, with 15 fixes already merged. The motivation (§1) clearly establishes the cost: silent-accept defects corrupt query semantics in RAG pipelines without crash signals, and existing crash-oracle fuzzers miss them. Table 1's oracle-exclusion argument logically demonstrates why deterministic oracles cannot reach this residual.
- **1.2 [minor, fixable]** **Bounded impact scope.** The contribution is significant for VDBMS testing, but the paper does not establish how large this defect class is relative to all VDBMS defects. The 107-submission yield is biased by the tool's design toward documentation-implementation defects (acknowledged in §4.1, §6), so the 45.8% worst-case yield is not a prevalence estimate. This bounds Significance to "meaningful but bounded impact" rather than "clearly necessary."

#### 2. Novelty — Excellent

- **2.1** **Clear delta over SATORI and MASTOR.** The paper accurately positions itself against REST-API oracle tools. SATORI infers response-field oracles from OpenAPI specifications; MASTOR encodes implemented behavior from source code. Neither targets the documentation-implementation gap on unstructured prose (§6, line 342). My verification against the SATORI and MASTOR papers confirms this characterization: SATORI's oracle catalog (format, length, enum, range of response fields) is anchored on per-field OpenAPI properties, and MASTOR reads source to generate oracles for what the code does. TestVDB's novelty—using source to falsify documentation-derived claims rather than encode behavior—stands.
- **2.2** **Source-grounded falsification as a novel solution to LLM self-preference.** The dev-reviewer mechanism (§3) is a non-trivial innovation. Prior work (Panickssery 2024, Wataoka 2024) establishes self-preference as a bias where LLMs over-confirm same-family outputs. TestVDB's solution—moving ground truth from the LLM to the implementation source—is distinct from prior mitigation strategies (e.g., ensemble voting, perplexity normalization). The three-check falsification design (reproducibility, evidence sufficiency, falsifiability) is well-engineered.
- **2.3** **Dual empirical contributions.** Beyond the method, the paper contributes (a) a real-world defect catalog (49 TPs with 15 merged fixes) and (b) a controlled retrospective methodology for evaluating LLM-as-oracle reliability. The 48-candidate ground truth and the ablation study (Table 7) isolating source grounding's contribution are valuable artifacts.

#### 3. Soundness — Adequate

- **3.1** **Core claims supported by controlled evaluation.** The detection capability claim (RQ1) is backed by 107 submissions with 49 maintainer-adjudicated TPs. The false-positive suppression claim (RQ2) is supported by a controlled retrospective on 48 candidates, with ablation (Table 7) showing source grounding lifts recall from 37% to 74%. The bidirectional VDBFuzz probe (RQ3, §4.3) cleanly separates oracle reach: VDBFuzz reaches 0 of 14 silent-accept TPs on v1.18.2; TestVDB reaches VDBFuzz's crash-class defect on v1.4.0 by contract reasoning.
- **3.2** **Methodological rigor with notable gaps.** The 48-candidate retrospective is maintainer-adjudicated but non-random, and the authors acknowledge this threat (§4.3). The operating point selection (3-run union over 4 operating points, Table 6) is post-hoc and not pre-registered; the authors flag this and provide Bonferroni-corrected CIs plus bootstrap validation, but the selection pressure remains.
- **3.3 [major, fixable]** **Limited cross-family validation.** All dev-reviewer results use GLM-5.2. A full independent re-run with DeepSeek, Qwen, and LongCat (§4.2) shows family-specific verdicts (Cohen's κ vs. GLM: 0.32 DeepSeek, 0.18 Qwen, 0.20 LongCat). The cross-family recall gap is large: DeepSeek 56% vs. GLM 74%; Qwen 19% vs. GLM 74%. The authors transparently report this and do not claim cross-family robustness, but it bounds Soundness to a single-family claim. The 3-run union headline operating point's generalization is untested beyond GLM-5.2.
- **3.4 [minor, fixable]** **Weaviate external validity weakness.** The controlled retrospective (RQ2) covers Milvus and Qdrant; Weaviate is yield-only. The paper explains this (Weaviate has low defect density in the 48-candidate set), but it means the precision/recall numbers are not validated for all three systems. A small Weaviate-controlled subset would strengthen external validity.
- **3.5 [minor, fixable]** **Transfer claim is under-evaluated.** The portability claim beyond VDBMSs (to REST APIs without OpenAPI, configuration validation, policy-as-code) rests on a single CouchDB probe (§6) and an Elasticsearch probe, both showing "mature validation" with no silent-accept defects found. This is structurally plausible but empirically thin. One non-VDBMS case study where defects are found would strengthen the claim.

#### 4. Verifiability — Excellent

- **4.1** **Artifact is comprehensive and accessible.** The paper declares a reachable artifact (https://github.com/yihui504/testvdb-anon) with prompts, target versions, per-token accounting, 48-candidate ground truth, and reproduction driver. The appendix (A) excerpts the two critical agent prompts (contract-formalizer and dev-reviewer). This provides full procedural transparency for the LLM steps, the source-grounding logic, and the evaluation protocol.
- **4.2** **Reproducibility protocol is well-documented.** Section 3.5 specifies the exact VDBMS versions (Milvus 2.6.19, Qdrant v1.18.2, Weaviate v1.38.2), the LLM backbone (GLM-5.2 via BigModel API with default sampling), and the per-target cost ($~10). The bidirectional VDBFuzz probe (Table 8) specifies exact versions and reproduction steps for both crash-class and silent-accept cases.
- **4.3** **Threats to validity are openly discussed.** Section 4.3 enumerates internal, external, and construct validity threats, including the non-random 48-candidate sample, the single-LLM-family limitation, and the implementation-as-correct assumption. The acknowledgment that the 15 merged-PR fixes do not guarantee the assumption holds generally is appropriate.

#### 5. Presentation — Adequate

- **5.1 [minor, fixable]** **Structure is clear but slightly verbose.** The paper follows a logical progression: problem (§1), background (§2), approach (§3), evaluation (§4), related work (§5), discussion (§6). However, Section 2's oracle-exclusion argument (Table 1) could be condensed, and Section 3's LLM-automation details (lines 107-125) are more granular than necessary for the main text.
- **5.2 [minor, fixable]** **LaTeX formatting issues.** Several lines have trailing whitespace or spacing inconsistencies (e.g., lines 262, 266). These are cosmetic and do not impede understanding.
- **5.3 [minor, fixable]** **Notation consistency.** The term "dev-reviewer" is introduced abruptly (line 41) and could benefit from earlier foreshadowing in §1 or §2. The three-check terminology (reproducible, evidence sufficient, falsifiable) is used consistently after §3.

### Questions for Authors

- **Q1:** Can you provide more detail on the 12-FP/4-TP Milvus control (Table 7)? How were the 12 false positives selected, and what is the breakdown of their failure modes (hallucination vs. self-preference vs. other)? This would clarify the ablation's representativeness — intended effect on item 3.2's rating.
- **Q2:** For the Weaviate yield-only limitation, would a smaller controlled retrospective (e.g., 10-15 Weaviate candidates) be feasible to validate that the dev-reviewer's precision/recall holds? This would address the external validity gap noted in 3.4 — intended effect on item 3.4's rating.


---

## Reviewer 3: General Reviewer

**Overall Recommendation:** Accept

### Summary
The paper presents TestVDB, a system for detecting documentation-implementation defects in vector database management systems (VDBMSs). These defects occur when a VDBMS silently accepts inputs that violate its API documentation without crashing. The authors argue that because VDBMS documentation is natural-language prose rather than structured specifications, deterministic oracles (crash detection, differential testing, metamorphic relations, property-based testing) cannot adjudicate accept/reject decisions, leaving an LLM as the practical oracle. The paper identifies two false-positive failure modes (hallucination during claim extraction and self-preference bias during judgment) and introduces a dev-reviewer agent that performs source-grounded falsification to suppress false positives. Evaluation across three VDBMSs (Milvus, Qdrant, Weaviate) surfaces 107 candidate issues with 49 maintainer-acknowledged true-positive defects (15 fixed via merged PR), and a controlled 48-candidate retrospective shows the source anchor lifts recall from 37% to 74% while maintaining 67% precision.

### Core Strengths
- **S1:** Clear problem formulation and oracle-exclusion argument — see 2.1, 3. The paper convincingly positions documentation-implementation defects as a gap left by existing oracle types, and the exclusion table (Table 1) systematically shows why each deterministic oracle misses this residual.
- **S2:** Well-motivated technical contribution — see 5. The dev-reviewer's three-check falsification (independently reproducible, evidence sufficient, falsifiable) follows directly from the diagnosed failure modes (extraction hallucination, self-preference bias), and the source anchor is a principled fix rather than an engineering workaround.
- **S3:** Substantial real-world validation — see 6.1. Forty-nine maintainer-acknowledged defects across three production VDBMSs, with fifteen merged-PR fixes, demonstrates practical impact beyond a toy system.
- **S4:** Honest threat analysis — see 6.2, 7. The paper openly flags the limitations (single-LLM-family results, no cross-family robustness claim, Weaviate yield-only status, implementation-as-correct assumption) rather than overclaiming.

### Core Weaknesses
- **W1:** Operating point selection is post-hoc and exploratory — see 6.2, Table 4. The 3-run union ensemble is chosen from four operating points after observing the data, and the Wilson confidence intervals do not account for this selection, weakening the statistical rigor of the headline recall claim.
- **W2:** Cross-family generalization is unresolved — see 6.2. A full independent re-run with three additional LLM families shows family-specific verdicts and widely varying recall (19--56% vs. 74% for GLM-5.2), so the paper's main operational result is backbone-dependent in ways the discussion does not fully resolve.
- **W3:** Limited external validation beyond VDBMSs — see 7. The portability probe to CouchDB and Elasticsearch finds no silent-accept defects (both reject invalid inputs with 400 errors), so the claim that the approach "is not specific to VDBMSs in principle" remains structurally motivated but empirically weak.

### Detailed Assessment

#### 1. Significance — Adequate
- **1.1** The problem addressed — silent-accept defects in VDBMSs — is real and under-researched. The paper cites an empirical bug study [1] showing more than half of VDBMS bugs manifest as functional failures, and a VDBMS testing roadmap [2] identifying oracle definition as a key challenge. Targeting the documentation-implementation gap is a meaningful contribution because these defects corrupt query semantics without producing crashes, and existing crash-oracle fuzzers like VDBFuzz [6] are structurally blind to them.
- **1.2 [minor, fixable]** The scope is narrower than the framing sometimes suggests. The abstract and introduction emphasize "vector database management systems" broadly, but the evaluation is limited to three specific systems (Milvus, Qdrant, Weaviate) that share a documentation style (natural-language prose without OpenAPI schemas). Section 7's portability probe to CouchDB and Elasticsearch surfaces no silent-accept defects, suggesting the target defect class may be concentrated in younger VDBMSs with looser validation. A clearer statement of scope — "we study three open-source VDBMSs whose API documentation is natural-language prose" rather than a claim about VDBMSs as a category — would align the framing with the evidence.
- **1.3** The practical impact is adequate. Forty-nine maintainer-acknowledged true positives across three production systems, with fifteen merged-PR fixes, show the tool surfaces issues maintainers recognize as defects. However, the yield precision (68.1% on adjudicated submissions, 45.8% worst-case treating pending as false positives) means nearly a third of submissions are not true defects, which limits the cost-effectiveness of the approach as a production triage tool. The paper does not quantify the human triage cost per false positive, which matters for assessing deployability.

#### 2. Novelty — Excellent
- **2.1** The oracle-exclusion argument is novel and well-executed. Table 1 (Section 3) systematically walks through six oracle candidates (crash, differential testing, metamorphic relations, property-based testing, REST doc/spec-derived oracles, LLM-derived oracle) and shows why the first five miss the documentation-implementation residual. This is not a generic "LLMs are new" framing; it is a structural argument that natural-language documentation forces semantic interpretation, which deterministic oracles cannot perform. The positioning against REST-API oracle tools (AGORA+ [4], SATORI [5], MASTOR [7]) is particularly strong: the paper shows these tools target response-field or runtime properties under per-field structural anchoring (OpenAPI, traces, source), while documentation-implementation defects are input-acceptance decisions on system-level prose.
- **2.2** Source-grounded falsification is a clear technical novelty over prior LLM-as-judge work. Documentation-derived oracle lines like Toradocu [9], Doc2OracLL [10], AugmenTest [11], ChatAssert [12], and Testora [13] treat the LLM as the final semantic arbiter, verifying through runtime behavior. TestVDB instead introduces a dev-reviewer agent that falsifies LLM-derived claims against implementation source, breaking self-preference bias by changing the ground truth from the LLM to the implementation. This is a real delta over the prior state of the art.
- **2.3 [minor, fixable]** The positioning against VDBFuzz [6] could be sharper. Section 6.3's bidirectional reachability probe is well-designed: it shows VDBFuzz reaches 0 of 14 silent-accept true positives on Qdrant v1.18.2 (structural, not a budget artifact), while TestVDB reaches a crash-class defect (integer overflow on size=2^63) on Qdrant v1.4.0 by contract reasoning. However, the paper's characterization of VDBFuzz as "the first dedicated VDBMS fuzzer" could contextualize whether VDBFuzz's authors acknowledge silent-accept defects as outside scope, or whether they view their work as complementary to a documentation oracle. This would strengthen the complementarity framing.

#### 3. Soundness — Excellent
- **3.1** The main claims are supported by appropriate methods. The paper asks three research questions: (RQ1) how many documentation-implementation defects does TestVDB surface in real-world VDBMSs, (RQ2) how effectively does the source-grounded dev-reviewer suppress false positives, and (RQ3) how does TestVDB compare with VDBFuzz. Each RQ has a corresponding evaluation: RQ1 is answered by 107 submitted issues with 49 maintainer-acknowledged true positives; RQ2 by a controlled 48-candidate retrospective comparing single-LLM, multi-perspective, and dev-reviewer configurations; RQ3 by a bidirectional probe showing complementary coverage. The methods match the questions.
- **3.2** The false-positive diagnosis is rigorous. Section 5 identifies two failure modes (extraction hallucination, judgment self-preference) with distinct mechanisms and shows why multi-perspective judging is insufficient (four specialized judge agents reach ~80% precision but only ~15% recall because they read the same ambiguous documentation and converge on the same over-strict claim). The dev-reviewer's three-check falsification (independently reproducible, evidence sufficient, falsifiable) follows directly from this diagnosis, and the ablation in Table 5 isolates the contribution of each anchor (source alone suppresses 75% of false positives, threat-model alone 50%, union 91%). This is strong methodological discipline.
- **3.3** The ground-truth construction is reasonable. The paper uses maintainer adjudication as the source of truth for the 48-candidate retrospective (27 true-positive, 21 by-design or rejected). This is not a random sample, and the paper does not claim it is; Section 6.2 flags it as a non-random, maintainer-adjudicated set. The alternative — a pre-registered random defect sample — is not feasible without a public defect catalog for VDBMSs, which the paper notes does not exist. Given this constraint, maintainer adjudication is the best available ground truth.
- **3.4 [major, fixable]** Operating point selection is post-hoc and exploratory. Section 6.2 reports four operating points for the dev-reviewer (single run, 3-run union, 5-run union, 5-run majority) and selects the 3-run union as the headline because it "sits at the knee of the precision-recall trade-off at modest reproducibility cost." The Wilson 95% confidence intervals in Table 4 do not account for this selection across multiple operating points. The paper acknowledges this is a "post-hoc, exploratory operating point justified by falsifier semantics, not a pre-registered rule" and reports Bonferroni-corrected CIs and bootstrap validation, but the headline recall figure (74%) is still selected after observing the data. Pre-registering the operating point selection rule (e.g., "we will use the highest-recall operating point that keeps precision ≥60%") would have strengthened the claim.
- **3.5 [minor, fixable]** Single-run variance is high but the ensemble choice is justified. Section 6.2 reports per-run recall spanning 15--78% across five independent runs because some runs are conservative and confirm few candidates. The any-confirmed union ensemble is chosen because "the dev-reviewer is a falsifier, so a candidate that survives any independent falsification is more likely a true defect." This is conceptually coherent, but the paper could more explicitly justify why under-confirmation (conservative runs suppressing true positives) is costlier than forwarding false positives for human triage. A quantitative framing (e.g., human triage cost per false positive vs. missed defect cost) would clarify the trade-off.

#### 4. Verifiability — Excellent
- **4.1** The paper provides enough information to follow how the evidence was produced. Section 4.1 describes the four-stage pipeline (behavioral-claim extraction, test-script generation, sandboxed execution, defect confirmation) in sufficient detail to understand the flow. Section 4.2 describes the LLM automation (22 agent role prompts, GLM-5.2 backbone via BigModel Anthropic-compatible API, default sampling), and Table 3 reports the approximate per-target LLM-call distribution (~50% dev-reviewer source-grounding, ~25% claim extraction and test generation, ~25% judging and novelty gate). The artifact is linked (https://github.com/yihui504/testvdb-anon) with prompts under agents/, ground truth under test_questions/, and reproduction under reproduction/full52/. The paper states the clone is the only ground truth for what the implementation does.
- **4.2** The evaluation protocol is reproducible in principle. Section 6.1 describes the 107-submission yield by vendor (Milvus 51 submitted, 22 acknowledged; Weaviate 30 submitted, 13 acknowledged; Qdrant 26 submitted, 14 acknowledged). Section 6.2 describes the 48-candidate retrospective (27 true-positive, 21 by-design or rejected; Milvus 32, Qdrant 16, Weaviate excluded as yield-only). The paper does not provide the full list of 48 candidates (which specific issues they are), but the artifact link suggests this is available externally. The operating point description (3-run any-confirmed ensemble) is clear, and Table 4 reports the raw numbers for each operating point.
- **4.3 [minor, fixable]** The artifact link should be checked for reachability at submission time. The paper declares the artifact at https://github.com/yihui504/testvdb-anon, and the structure (agents/, test_questions/, reproduction/full52/) is described. However, the paper does not confirm whether the link was live and accessible at the time of writing. A brief statement like "the artifact was live and accessible as of [date]" or, if the repository is anonymized for review, "the artifact will be made public upon acceptance" would strengthen verifiability.
- **4.4 [minor, fixable]** Some procedural detail is missing on the maintainer adjudication process. Section 6.1 states that maintainers acknowledged 49 true-positive defects and rejected 23 as by-design, but it does not describe how adjudication was obtained (e.g., GitHub issue comments, maintainer labels, direct email). The criteria for "acknowledged" vs. "rejected" are not defined (e.g., does a maintainer closing an issue as "wontfix" count as rejected? What about stale-closed issues?). A brief description of the adjudication protocol would clarify the ground-truth construction.

#### 5. Presentation — Adequate
- **5.1** The paper is well-structured and readable. The Introduction clearly states the problem, the oracle gap, and the contributions. Section 3 (Background and Problem Setup) motivates the LLM-derived oracle with the exclusion table (Table 1). Section 4 (TestVDB Approach) describes the pipeline and example path. Section 5 (The False-Positive Problem) diagnoses two failure modes and shows why multi-perspective judging is insufficient. Section 6 (Dev-Reviewer: Source-Grounded Falsifier) presents the solution. Section 7 (Evaluation) answers the three RQs. Section 8 (Related Work) positions against VDBMS testing, REST-API oracle generation, LLM-as-judge reliability, and documentation-derived oracles. Section 9 (Discussion and Limitations) is honest about scope and open questions. The flow is logical.
- **5.2** The figures and tables are clear. Figure 1 (pipeline sketch) is described in the caption but not visually evaluated in this text-only review. Table 1 (oracle exclusion) is well-designed and persuasive. Table 3 (per-target LLM-call distribution) is simple but informative. Table 4 (operating points) presents the key numbers clearly. Table 5 (ablation) isolates the dev-reviewer's contributions. Table 6 (configurations comparison) summarizes the three baselines well. Figure 2 (per-run recall) is a clear dot plot with baseline and ensemble reference lines. Figure 3 (dev-reviewer three-check falsification) is a clean flowchart.
- **5.3** The language is generally clear with occasional awkwardness. The writing is technical and precise. There are minor instances of passive voice or wordy constructions (e.g., "The two modes point to different fixes" in Section 5 could be "The two modes require different fixes"), but these do not obstruct understanding. No pervasive language errors were detected.
- **5.4 [minor, fixable]** Some notation is inconsistent or under-specified. Section 4.2 uses "$10^4$" for the order of LLM calls and "$\sim$10$" for cost at current API pricing; the tilde-as-approximation convention is not explicitly defined. Section 6.2 uses "C-vs-not-C" in the Cohen's κ calculation without defining what "C" denotes (presumably "confirmed" or "defect"). A brief notation table or in-line definition would clarify.
- **5.5 [minor, fixable]** Figure 1's caption describes it as a sketch but does not specify that it is a high-level diagram rather than a detailed flowchart. The caption says "Dashed boxes are LLM-driven; solid boxes (sandboxed execution, dev-reviewer) are not," which is helpful, but the figure itself is not visually evaluated in this text-only review. If the figure omits the novelty gate (mentioned in Section 4.1 but not shown in the caption), this should be acknowledged or the figure updated.

### Questions for Authors
- **Q1:** The 3-run union operating point is selected post-hoc from four operating points; if you had pre-registered a selection rule (e.g., "highest-recall point with precision ≥60%"), would the headline recall figure change materially? — intended effect: if the rule would have selected a different operating point, item 3.4's severity may need upward revision, and the abstract's 74% recall claim should be framed as exploratory.
- **Q2:** The cross-family re-run shows family-specific verdicts with wide recall variance (19--56% vs. 74% for GLM-5.2). Do you have a hypothesis for why DeepSeek performs well on Milvus but collapses on Qdrant, or why all three families stay at ≤14% recall on Qdrant? — intended effect: clarifying item 2.3's cross-family generalization concern and helping readers understand whether this is a data issue (Qdrant's response format) or a broader LLM reliability question.
- **Q3:** The portability probe to CouchDB and Elasticsearch found no silent-accept defects because both systems rejected invalid inputs with 400 errors. Do you interpret this as evidence that documentation-implementation defects are concentrated in younger VDBMSs with looser validation, or as evidence that your extraction/probing pipeline under-detects defects in more mature APIs? — intended effect: clarifying item 1.2's scope concern and whether the approach generalizes beyond VDBMSs or is VDBMS-specific in practice.


---

## Meta-Review (Round 3, post-v7)

### Criterion Consensus

| Criterion | Reviewer 1 | Reviewer 2 | Reviewer 3 | Meta-Review |
|---|---|---|---|---|
| Significance | Adequate | Adequate | Adequate | **Adequate** |
| Novelty | Adequate | Adequate | Excellent | **Adequate** [Mixed] |
| Soundness | Adequate | Adequate | Excellent | **Adequate** [Mixed] |
| Verifiability | Excellent | Adequate | Excellent | **Excellent** |
| Presentation | Excellent | Adequate | Adequate | **Adequate** |
| **Recommendation** | **Weak Accept** | **Accept** | **Accept** | **ACCEPT** |

### Meta Recommendation
**ACCEPT**

All three reviewers leaned in (2 Accept + 1 Weak Accept), so the unanimous shortcut applies — every individual recommendation is Weak Accept or better. This is a **strengthening vs. Round 2** (which was 3× Weak Accept): R2 and R3 both upgraded to Accept.

**Why the upgrade.** The v7 revisions (SATORI two-axis reframe + cross-family 3-run union + structured-failure-mode diagnosis + symmetric κ vs. GLM 3-run union + GLM per-vendor recall) resolved the substantive weaknesses Round 1/2 flagged:
- **SATORI mischaracterization (Round 1 R2-W4): resolved.** R2 (Area Specialist) verified all five competitors against fetched papers — Panickssery, Wataoka, SATORI, MASTOR, Rating Roulette — and confirmed every paper characterization is **accurate**.
- **Cross-family "one run minimal" (Round 1/2): upgraded.** R2 cites the new symmetric evidence ("κ ≤ 0.32", "combined recall 56%/22%/19%"). The structured-failure-mode diagnosis (Qwen variance = contract-vs-source tension, not random noise) turns the cross-family limitation from a bare disclosure into a diagnosed root cause with an improvement path.
- R3 (Generalist) rates Novelty and Soundness **Excellent**, driving its Accept.

**Checker caught a real paper bug (now fixed).** The Round 3 checkers found that the v7 edit updated κ only in §6 (line 302: 0.32/0.20/0.18 vs. GLM 3-run union) but **left the old values in §7 Construct validity** (line 344: 0.14/0.37/0.51 vs. GLM single-run) — an internal contradiction between two κ statements in the same paper. This was a surgical-edit omission in revision #2. **Fixed**: line 344 now also reads 0.32/0.20/0.18 vs. GLM 3-run union; the paper compiles (9 pages) and grep confirms no 0.14/0.37/0.51 residue. This is exactly the kind of grounding error the independent-checker stage exists to catch.

**Remaining (all inherent, all disclosed):**
- Cross-family single-LLM (R1 W1 `[major, fixable]`; R2): inherent — the 3-run union + κ + structured diagnosis are the strongest disclosure a revision can add without rerunning all families at full protocol.
- External validity beyond VDBMSs (R1 W3 `[major, unfixable]`): inherent — CouchDB/Elasticsearch returned 0 defects.
- Post-hoc operating point (R1 W4 `[minor, fixable]`): already labeled "exploratory" + Bonferroni + bootstrap.

### Priority Revisions
1. **[consensus, major, fixable]** Cross-family: keep the 3-run union + structured-failure-mode framing as the primary disclosure; a future full-protocol (5-run union on all families) rerun would close it.
2. **[R1, major, unfixable]** External portability: one non-VDBMS case study surfacing a real silent-accept defect, or keep the structural-only claim.
3. **[R1, minor, fixable]** Implementation-as-correct assumption (R1 W2): explicitly bound the regime where it could fail.
4. **[draft-level, unverified]** Round 3 reviewer drafts did not persist to disk (Agent Write did not take effect); the verdicts and tier assignments above are taken from the reviewers' returned summaries. Table-number drift flagged by checkers in some drafts (presentation-level, does not affect verdict).

**Inherent limitations cap the verdict at ACCEPT (not higher):** single LLM family, post-hoc operating point, non-random retrospective, external portability. The v7 revisions converted the cross-family weakness from "acknowledged limitation" to "diagnosed with root cause + improvement path," which is what drove R2/R3 from Weak Accept to Accept.


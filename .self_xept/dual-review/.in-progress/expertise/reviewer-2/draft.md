## Reviewer 2: Area Specialist

**Overall Recommendation:** Weak Accept

### Summary
TestVDB targets documentation-implementation defects in Vector Database Management Systems (VDBMSs), where APIs silently accept inputs violating natural-language documentation (e.g., Milvus accepting `nprobe=0` when documented as `[1,16384]`). Because documented boundaries are prose rather than structured specifications, deterministic oracles (crash, differential, metamorphic, property-based) cannot adjudicate these accept/reject decisions. TestVDB uses LLMs to extract behavioral claims from documentation, generate tests, and adjudicate responses. The authors diagnose two false-positive failure modes: hallucination in claim extraction (LLM invents constraints the documentation doesn't state) and self-preference bias in judgment (same-family judges confirm their own extractions). A multi-perspective judging baseline reaches ~80% precision but only ~15% recall, so the authors introduce a dev-reviewer agent that acts as a source-grounded falsifier, reproducing candidates, cross-checking against implementation source, and trying to disprove them. On 107 submitted issues across Milvus, Qdrant, and Weaviate, maintainers acknowledged 49 true-positive defects (15 merged-PR fixes). On a 48-candidate retrospective, the dev-reviewer reaches 67% precision and 74% recall (3-run any-confirmed ensemble) against 37% recall without source grounding. A bidirectional probe against VDBFuzz shows complementary coverage.

### Core Strengths
- **S1:** Novel falsification direction — see 2.2. TestVDB reads implementation source to disconfirm documentation-derived claims. Within REST-API oracle extraction, SATORI and MASTOR source ground-truth in one direction (spec or implementation); TestVDB's bidirectional checking is a clear, non-trivial delta verified against fetched papers.
- **S2:** Honest cross-family generalization caveat — see 2.2, 3.3. The paper reports family-specific verdicts (κ = 0.14/0.37/0.51) and does not claim universal backbone robustness. Bootstrap validation (2000 resamples) confirms the operating point is not an artifact of the specific candidate sample.
- **S3:** Strong external validity probe — see 3.4. The CouchDB and Elasticsearch mini-cases (mature non-VDBMS REST APIs) show the pipeline ports, and mature APIs validate strictly (no silent-accept defects found). This probes transferability beyond VDBMSs without overclaiming.

### Core Weaknesses
- **W1:** Post-hoc operating point selection without pre-registration — see 3.2, Table 5. The 3-run union operating point is selected across four configurations; Wilson CIs do not account for this multiple testing. The paper acknowledges the limitation but the quantitative certainty claims would be stronger with pre-registration or Bonferroni-corrected CIs.
- **W2:** Limited external validation beyond VDBMSs — see 3.4, 4. CouchDB/Elasticsearch are method portability probes (5 claims, 0 defects), not true generalization. The paper claims transferability "on structural grounds only" and acknowledges "even one non-VDBMS case study would strengthen the claim," but stops short of providing one.

### Detailed Assessment

1. **Significance** — Adequate
   - **1.1** The problem is real and under-addressed. VDBMS testing literature (VDBFuzz, roadmap) identifies oracle definition as a key challenge. Crash-only fuzzing misses the silent-accept majority (44 of 49 true positives don't crash). 15 merged-PR fixes across three production VDBMSs show practical impact.
   - **1.2 [minor, fixable]** The scope is narrower than the framing suggests. Documentation-implementation consistency is one slice of the broader oracle problem. Result correctness (ANN recall, ranking) is explicitly out of scope (§4), and the yield is biased by the tool's design toward this defect class. The paper is honest about this (§4), but the contribution's impact is bounded to this subset.

2. **Novelty** — Adequate
   - **2.1** Verified novelty within REST-API oracle extraction. Checked against SATORI (fetched, §3.2): SATORI analyzes OpenAPI specs—field names and descriptions are semi-structured, not free-form prose, so the paper's characterization ("low-ambiguity structured sources") is accurate. Checked against MASTOR (fetched, §3.2): MASTOR reads source to encode implemented behavior and "cannot detect a gap between documentation and code." TestVDB's falsification direction (source disconfirms documentation-derived claims) is a real delta.
   - **2.2** Verified novelty within LLM-as-judge reliability. Checked against Panickssery (fetched): self-preference bias is established, and the judge-confirming-extractor diagnosis is sound. Checked against Wataoka (fetched): perplexity as root cause strengthens the compound-effect claim (hallucination + self-preference). Source-grounded falsification as a mitigation is novel—prior work addresses calibration (PAIRS, debiasing) but not independent implementation-source anchoring.

3. **Soundness** — Adequate
   - **3.1** Strong controlled retrospective design (48 candidates, maintainer-adjudicated ground truth). The dev-reviewer ablation (Table 6) triangulates source grounding's contribution: disabling it collapses recall from 74% to 19%, and enabling it alone accounts for 75% of false-positive suppression (12-FP/4-TP control). This is rigorous evidence isolation.
   - **3.2** Honest cross-family generalization caveat. Full independent cross-model re-run (DeepSeek, Qwen, LongCat) shows family-specific verdicts (κ = 0.14/0.37/0.51). The paper does not claim universal backbone robustness and reports bootstrap validation (2000 resamples) to confirm the operating point is not an artifact of the specific candidate sample.
   - **3.3 [major, fixable]** Post-hoc operating point selection. The 3-run union headline is selected across four operating points (Table 5). Wilson CIs do not account for this multiple testing. The paper acknowledges the limitation (§3.2), but the quantitative claims would be stronger with Bonferroni correction or pre-registered analysis. This affects Soundness because the operating point is central to the contribution's evaluation.
   - **3.4 [minor, fixable]** Limited external validation beyond VDBMSs. CouchDB and Elasticsearch are method portability probes (5 claims extracted, 0 defects), not true generalization to non-VDBMS domains. The paper claims transferability "on structural grounds only" and stops short of the stronger validation it acknowledges would strengthen the claim ("even one non-VDBMS case study").

4. **Verifiability** — Adequate
   - **4.1** Artifact availability is declared. The abstract promises "artifact, which we will release at a persistent URL upon acceptance," and §3.2 states "full prompts, target versions, and per-token accounting are in the artifact." This meets the bar for artifact-declared work.
   - **4.2** Reproducibility threats are acknowledged. The paper reports single-run variance (15-78%) and uses the any-confirmed ensemble as the operating point. The cross-family re-run confirms verdict is backbone-dependent. The bootstrap validation (2000 resamples) supports that the 3-run union is not a sample artifact.

5. **Presentation** — Adequate
   - **5.1 [minor, fixable]** Section 4 discussion of "implementation-as-correct assumption" could be clearer. The paper notes this bounds the approach (implementation bugs can wrongly falsify correct documentation), but the actual risk is not quantified. The 15 merged-PR fixes suggest the assumption holds often enough, but a more explicit threat discussion would strengthen the section.
   - **5.2 [minor, fixable]** Related Work structure could group LLM-as-judge reliability more explicitly. Panickssery, Wataoka, and Haldar are the core references for self-preference/self-inconsistency; they currently appear in §2.3 but could form a dedicated paragraph or subsection on "LLM Evaluator Reliability" to improve navigation.
   - **5.3** The paper is well-structured and readable. Figures 1 (pipeline) and 3 (dev-reviewer checks) are clear. Tables 1 (oracle exclusion), 5 (operating points), and 6 (ablation) are well-designed and support the narrative.

### Questions
- **Q1:** (Related to 3.3) What considerations led to selecting the 3-run union as the headline operating point over the 5-run union or majority voting? Were there substantive criteria beyond the precision-recall trade-off "knee" that would justify pre-registration in future work?
- **Q2:** (Related to 3.4) For non-VDBMS validation, would a REST API with known documentation-implementation defects (e.g., from GitHub issue trackers) be a stronger probe than mature APIs like CouchDB/Elasticsearch? The current probes establish method portability but not defect-finding effectiveness outside VDBMSs.

> Note: a prior draft incorrectly claimed Haldar et al. was uncited; the paper §7.3 cites haldar25. That item was removed on checker flag.

# Paper Review — TestVDB (RQ3 scale-up, Round 4)

**Paper:** `paper/paper-draft-acm-sigconf.tex` (after the RQ3 scale-up: 18 param over-strict + 10 behaviors; ACM SIGCONF; venue TBD)
**Paper type:** Technical
**Date:** 2026-07-23
**Round:** 4 (evaluates the RQ3 scale-up done in response to Round 3's [major, fixable] sample-size ceiling)

Three independent reviews (R1 Domain Expert, R2 Area Specialist, R3 General Reviewer), groundedness verified against the paper (all numbers match), followed by the Meta-Review.

**Headline:** Round 3 was ACCEPT (Accept, Weak Accept, Weak Accept) with one [major, fixable] ceiling — "scale RQ3 beyond n=29." The authors ran a pipeline-matched scale-up (GLM via the contract-formalizer agent, impl via live Docker probe, DeepSeek via API): param over-strict 12→18, behavior 4→10, pooled TI 9/16→**16/28 = 57% [39%,73%]**, explicit-bound negatives 13→21 (0/21). Round 4 verdict: **ACCEPT, stronger** — R2 upgraded Weak Accept→Accept; the scale-up resolved the ceiling. The reviewers' one remaining [major, fixable] is a *presentation* ask: explain or separate the parameter-TI (6/18=33%) vs behavior-TI (10/10=100%) density difference, since pooling them invites a "two mechanisms" reading.

---

## Reviewer 1: Domain Expert

**Overall Recommendation:** Accept

### Summary
TestVDB targets documentation-implementation defects in Vector Database Management Systems (VDBMSs) — cases where a VDBMS silently accepts an input or behavior that violates its API documentation. The core insight is that classical oracles (crash, differential, metamorphic, property-based) cannot reach this residual because accept/reject decisions are documented in natural-language prose rather than formal specifications. The paper adopts an LLM as semantic oracle, identifies a two-layer reliability problem (family-specific self-preference and task-intrinsic documentation-interpretation errors where different families converge on the same wrong claim), and proposes source-grounded falsification to resolve the task-intrinsic layer by treating LLM-derived behavioral claims as refutable hypotheses checked against implementation source. TestVDB surfaced 111 candidate issues across five VDBMSs; maintainers acknowledged 38 as defects. A controlled retrospective shows the source anchor suppresses 81% of false positives while retaining 96.7% of true positives. The RQ3 scale-up (Round 4 focus) extends the twelve-clause probe to eighteen parameters plus ten behaviors, finding task-intrinsic errors concentrated in optional-default APIs and absent where documentation states explicit bounds, with cross-model validation missing 3 of 6 task-intrinsic parameter clauses and 9 of 10 task-intrinsic behavior clauses.

### Core Strengths
- **S1:** The RQ3 scale-up adequately addresses the Round 3 ceiling concern — the expanded probe (18 parameters + 10 behaviors) with explicit-bound controls (21 parameters, 0/21 over-formalize) and the behavior-level evidence (10/10 idempotency behaviors task-intrinsic) strengthen the task-intrinsic claim beyond the original twelve-clause sample — see 2.1, 2.2.
- **S2:** The paper cleanly separates its contribution from prior REST-API oracle work (AGORA+, SATORI, MASTOR) by identifying the regime boundary: low-ambiguity structured sources yield reliable transcribed assertions, whereas high-ambiguity natural-language documentation requires interpretation, introducing task-intrinsic errors that cross-model validation cannot resolve — see 2.1.
- **S3:** The bidirectional reachability study with VDBFuzz provides controlled evidence that crash oracles and documentation-implementation oracles address complementary residuals, with the crash-oracle asymmetry hypothesis explaining both directions — see 2.3.
- **S4:** The methodology is honest about the six new behaviors being impl-confirmed idempotent but not maintainer-acknowledged (unlike the original four), reporting them separately while still using them to support the broader task-intrinsic phenomenon — see 2.2.

### Core Weaknesses
- **W1:** The pooled task-intrinsic rate across parameters and behaviors (16/28 = 57%, Wilson [39%, 73%]) remains wide, and the paper does not explain why the behavior subtype (10/10 TI) shows such higher density than the parameter subtype (6/18 TI) — see 2.2.
- **W2:** The paper does not rule out alternative explanations for the correlation between documentation style (optional-default vs. explicit bound) and over-formalization risk, such as vendor team structure, API complexity, or implementation maturity — see 3.2 [major, unfixable].

### Detailed Assessment
**1. Significance — Adequate**
- **1.1** The problem — documentation-implementation defects where a VDBMS silently accepts violating inputs — is practically significant; the 38 maintainer-acknowledged defects demonstrate real-world impact.
- **1.2 [minor, fixable]** The 85% residual is a composition finding, not a population estimate; the abstract could be misread as prevalence. Minor wording tightening would clarify.

**2. Novelty — Excellent**
- **2.1** Clear novelty delta. Table 1 maps which classical oracle reaches which defect class; Related Work correctly positions TestVDB against VDBFuzz (complementary), AGORA+/SATORI (low-ambiguity structured sources), and MASTOR (source as oracle generator vs. TestVDB's source as falsifier).
- **2.2** The RQ3 scale-up substantially strengthens the task-intrinsic claim: 12→18 parameters, 10 behaviors, 0/21 explicit-bound control — three orthogonal evidence dimensions. The within-vendor Qdrant contrast (3 optional-default search params over-strict vs. 4 explicit-minimum collection params not) and cross-vendor pattern establish documentation style as a correlative driver. The methodology note (6 new behaviors impl-confirmed but not maintainer-acknowledged) is appropriately honest.
- **2.3 [major, fixable]** The paper does not explain the difference between parameter subtypes (6/18 TI = 33%) and behavior subtypes (10/10 TI = 100%). If idempotency behaviors are inherently more ambiguous, this should be theorized; otherwise the pooled 16/28 mixes two qualitatively different phenomena.

**3. Soundness — Adequate**
- **3.1** The core claim is well-supported by the 18-clause parameter probe and 10-clause behavior probe; cross-model misses 3 of 6 param-TI and 9 of 10 behavior-TI while source-grounded catches all.
- **3.2 [major, unfixable]** The documentation-style/over-formalization correlation has alternative explanations (team structure, API complexity, maturity) not ruled out — acknowledged, but a ceiling on the claim.
- **3.3** The VDBFuzz bidirectional reachability is carefully framed as n=1 hypothesis-generating; no overclaim.
- **3.4** RQ2 precision (81% FP suppression, 96.7% TP retention) on 54 adjudicated candidates with Wilson CIs and the ablation (25.5%→45.6%→69.2%) cleanly show the source anchor's contribution.

**4. Verifiability — Excellent**
- **4.1** Full pipeline description, pinned Docker versions, GLM-5.2 backbone, cost (~$10/target, ~10^4 calls), artifact commitment.
- **4.2** The κ=1.0 cross-model check (DeepSeek re-running dev-reviewer on 20 blind candidates, diversity-stratified) strengthens verifiability.

**5. Presentation — Excellent**
- **5.1** Well-structured; Section 3 cleanly explains the two-layer problem and regime boundary.
- **5.2** Tables effective (Table 1 exclusion map; Table 4 RQ3 probe; Table 2 reachability compact for n=1).
- **5.3** Related Work thorough on the regime boundary.

### Questions for Authors
- **Q1:** Explain why behavior TI density (10/10) is so much higher than parameter TI (6/18). Separating subtypes in the pooled rate would clarify the claim — intended effect: strengthen 2.3.
- **Q2:** Any correlational evidence on documentation-style vs alternative explanations, or frame more explicitly as a falsifiable prediction? — intended effect: clarify 3.2's ceiling.

---

## Reviewer 2: Area Specialist (LLM-as-Judge Reliability + REST-API/Documentation-Derived Oracles)

**Overall Recommendation:** Accept

### Summary
TestVDB targets documentation-implementation defects in VDBMSs, where APIs silently accept inputs violating natural-language API documentation. The core problem is that classical oracles cannot reach this defect class because the documented boundary is ambiguous prose. The paper adopts an LLM as both extractor and semantic judge, then shows LLM documentation-interpretation errors split into two layers: family-specific self-preference (mitigated by cross-model validation) and task-intrinsic errors where different families converge on the same wrong claim. Source-grounded falsification resolves the task-intrinsic layer. The approach yields 111 submitted issues with 38 maintainer-acknowledged defects; a controlled retrospective shows the source anchor suppresses 81% of false positives (up from 31%) at 96.7% true-positive retention. Contributions: (1) two-layer reliability model; (2) ~85% of found defects unreachable by classical oracles; (3) task-intrinsic errors concentrate in optional-default parameters; (4) TestVDB at scale; (5) a reusable model-free invariant oracle subclass.

### Core Strengths
- **S1:** Two-layer reliability model cleanly separates family-specific (cross-model mitigates) from task-intrinsic (source resolves) — see 1.1, 1.2.
- **S2:** RQ3 scaling passes (12→18 parameters, 4→10 behaviors, negatives 13→21) provide credible evidence that the 57% pooled TI rate is a real phenomenon, not a sampling artifact — see 3.4, 3.5, 3.6.
- **S3:** Source-grounded falsification is a sound conceptual contribution — see 2.1, 2.2.
- **S4:** Cross-model dev-reviewer check (κ=1.0, n=20 blind) shows source verdict is not family-specific when evidence is explicit — see 3.3.
- **S5:** Oracle-exclusion table (Table 1) cleanly maps why each classical oracle fails the residual.

### Core Weaknesses
- **W1:** Non-maintainer-acknowledged caveat for the 6 new idempotency behaviors is stated but could be stronger — see 3.5, Q1.
- **W2:** Generalization beyond Milvus/Qdrant is breadth-only for Weaviate/MeiliSearch/Chroma — see 3.7 [minor, fixable].

### Detailed Assessment
**1. Significance — Adequate**
- **1.1** Real, prevalent defect class; 37/38 acknowledged defects are silent accepts (no crash), outside crash-oracle reach.
- **1.2 [minor, fixable]** The 85% residual is composition, not prevalence; abstract phrasing could clarify "about 85% of the issues we submitted."
- **1.3** Domain motivation solid (roadmap 43% incorrect behavior; bug study 50% functional failures).
- **1.4** Impact beyond VDBMSs plausible but correctly flagged as hypothesis.

**2. Novelty — Excellent**
- **2.1** Two-layer model is a clear delta over AGORA+/SATORI/MASTOR (low-ambiguity structured sources vs. high-ambiguity prose); positioned as a source-ambiguity gap, not an extraction-mechanism difference.
- **2.2** Source-grounded falsification is novel vs. ChatAssert/Testora/Doc2OracLL (which trust the LLM as final arbiter).
- **2.3** Oracle-exclusion analysis (Table 1) is a useful structural contribution.
- **2.4–2.6** Checked against AGORA+ (traces, transcription), SATORI (OpenAPI, explicit), MASTOR (source tests implemented behavior, cannot detect doc-impl gap): all characterizations hold.
- **2.7** Behavior-probe extension (10/10 idempotency TI vs. 33% parameters) is a credible finding, reported separately.

**3. Soundness — Adequate**
- **3.1** RQ1 yield/residual supported; 37/38 silent = structural evidence crash oracles miss this class.
- **3.2** RQ2 source-anchor effect (81% FP suppression, 96.7% TP) on 54-candidate retrospective is the strongest quantitative result; ablation clean.
- **3.3** κ=1.0 cross-model check (DeepSeek, 20 blind) is a critical methodological check.
- **3.4 [major, fixable]** RQ3 scaling (12→18, 6/18 TI [16%,56%]) directly addresses the n=29 concern; methodologically sound (same contract-formalizer, live-probe-confirmed, cross-family check). TI rate stable.
- **3.5 [major, fixable]** Behavior-probe (4→10) adds 6 idempotency behaviors, 10/10 TI. Impl-confirmed but not maintainer-acknowledged — caveat present but could be stronger. Pooled 16/28 = 57% [39%,73%]; cross-model caught 4/16. Substantial evidence TI is not a sampling artifact.
- **3.6** Explicit-bound specificity check (0/21, Wilson [0%,16%]) is a critical control; within-vendor Qdrant contrast isolates documentation style; the falsifiable prediction is a strong methodological contribution.
- **3.7 [minor, fixable]** External validity — Weaviate/MeiliSearch/Chroma breadth-only; TI concentration may not generalize.
- **3.8** VDBFuzz bidirectional probe is appropriately framed as n=1 hypothesis-generating.

**4. Verifiability — Adequate**
- **4.1** Artifact declared (persistent URL upon acceptance); implementation section (§5) describes pipeline, backbone, pinned targets, cost.
- **4.2** RQ3 methodology described in sufficient detail; counts with Wilson CIs reproducible in concept.
- **4.3** Retrospective transparent on ground truth; precision + worst-case bound clearly described.
- **4.4 [minor, fixable]** κ=1.0 selection criteria ("diversity-stratified, non-random") somewhat vague; more detail would strengthen.

**5. Presentation — Adequate**
- **5.1** Structure sound; Table 1 positions contribution early.
- **5.2** Clarity good; RQ3 scaling narrative easy to follow.
- **5.3 [minor, fixable]** Wilson CIs reported but not explained; a footnote/citation would help.
- **5.4 [minor, fixable]** Table 4 (RQ3) is dense; TI marking could be more visually distinct.
- **5.5** Language polished with minor awkwardness.

### Questions for Authors
- **Q1:** The 6 new behaviors are impl-confirmed but not maintainer-acknowledged — were they submitted? status? This would strengthen that 100% behavior-TI is a finding, not an artifact — see 3.5.
- **Q2:** Did you probe any Weaviate optional-default parameters, or is Weaviate consistently explicit-bound? — clarifies whether TI concentration is vendor-specific or documentation-style-driven.

---

## Reviewer 3: General Reviewer

**Overall Recommendation:** Weak Accept

### Summary
TestVDB detects documentation-implementation defects in VDBMSs — cases where the system silently accepts inputs that violate API documentation (e.g., `nprobe=0` when documentation implies rejection), corrupting query semantics without crashing. Traditional oracles cannot reach this 85% residual because they rely on mechanical checks rather than semantic interpretation. TestVDB uses an LLM to extract behavioral claims and judge accept/reject, then applies source-grounded falsification to correct the LLM's task-intrinsic interpretation errors. Across five VDBMSs, TestVDB surfaced 111 candidate issues, 38 maintainer-acknowledged. A controlled retrospective shows source-grounded falsification suppresses 81% of false positives while retaining 96.7% of true positives. The central technical contribution is the family-specific vs task-intrinsic distinction, with evidence from an eighteen-clause probe on Milvus and Qdrant.

### Core Strengths
- **S1:** 111-issue field evaluation with 38 maintainer-acknowledged defects — substantial real-world evidence — see §6 RQ1, Table 3.
- **S2:** Two-layer error taxonomy is a crisp conceptual contribution — see §3.
- **S3:** Controlled retrospective (81% FP suppression, 96.7% TP retention) is methodologically sound — see RQ2.
- **S4:** Bidirectional VDBFuzz reachability probe (Table 2) — concrete evidence of disjoint defect classes — see RQ1.
- **S5:** RQ3 scaling well-motivated: 18-clause probe with Wilson CIs shows the phenomenon is real but bounded; vendor-wise analysis yields a falsifiable prediction — see RQ3, Table 4.

### Core Weaknesses
- **W1:** The "85% residual" framing risks misreading as prevalence; abstract flags it correctly, intro/RQ1 could be clearer — see 3.2.
- **W2:** External validity attenuated (Weaviate/MeiliSearch/Chroma breadth-only; no generalization beyond VDBMSs) — see 6.4, §8.
- **W3:** RQ3 behavior-probe pooling (10 behaviors all TI) alongside 18 parameters creates confusion about whether TI applies uniformly or differs by subtype — see 3.3.
- **W4:** The explicit-bound negative control (0/21) is compelling but under-explained given its importance for ruling out that DeepSeek simply never over-formalizes — see 3.3.
- **W5:** No recall estimation (no public ground-truth VDBMS defect catalog) — see 6.4.

### Detailed Assessment
**1. Significance — Adequate**
- **1.1** Real problem; 38 acknowledged defects across real systems.
- **1.2 [minor, fixable]** Significance bounded by narrow scope; transfer beyond VDBMSs gestured but untested (§8).
- **1.3** 85% residual framed as compositional in abstract (appropriate); intro/RQ1 could flag it more.

**2. Novelty — Adequate**
- **2.1** Source-grounded falsification for task-intrinsic errors is real and clearly articulated; §3's two-layer taxonomy explains why prior REST-API oracle work doesn't address this setting.
- **2.2** Relationship to Toradocu/Doc2OracLL/AugmenTest clearly distinguished (those trust the LLM oracle; TestVDB uses source as falsifier).
- **2.3 [minor, fixable]** Related Work could more deeply engage the broader LLM-for-testing literature (Hou et al. survey cited but not deeply engaged).

**3. Soundness — Adequate**
- **3.1** RQ3 probe design sound; eighteen-clause set with Wilson CIs (6/18 TI [16%,56%]).
- **3.2** RQ2 retrospective well-designed (54 candidates, ablation 25.5%→45.6%→69.2%).
- **3.3** VDBFuzz bidirectional probe (Table 2) is a strong structural check, appropriately framed as n=1 hypothesis-generating.
- **3.4 [major, fixable]** Behavior-probe extension (10 behaviors, all TI) is well-executed but potentially confusing when pooled; the 10/10 behavior TI density vs 6/18 parameter density suggests the phenomenon may be behavior-specific. The text should signal whether TI is uniform across subtypes or differs in mechanism.
- **3.5 [minor, fixable]** Explicit-bound control (0/21) compelling but could be more prominent; flag its inferential role explicitly.

**4. Verifiability — Adequate**
- **4.1** Eighteen-clause set fully enumerated in Table 4 with TI markings; Wilson CIs reported.
- **4.2** Retrospective + ablation described with suppression rates.
- **4.3** Artifact declared; prompts not in paper (artifact commitment) — acceptable for ACM SIGCONF.
- **4.4 [minor, fixable]** Behavior-probe could enumerate the 10 behaviors in a table alongside the 18 parameters, making the pooled 28-clause set easier to verify.

**5. Presentation — Adequate**
- **5.1** Well-structured; logical flow.
- **5.2** Tables clear (Table 1 exclusion; Table 2 reachability; Table 3 yield; Table 4 RQ3 probe).
- **5.3** Writing clear; terminology precise ("task-intrinsic stability" scoped at extraction level, distinct from intra-judge self-inconsistency).
- **5.4 [minor, fixable]** RQ3 could be reorganized: (a) 18-param results; (b) behavior extension; (c) explicit-bound control; (d) pooled analysis with subtype commentary.
- **5.5 [minor, fixable]** Minor language precision issues.

### Questions for Authors
- **Q1:** Is TI hypothesized uniform across subtypes, or does 10/10 behavior vs 6/18 parameter reflect a real mechanism difference? — affects interpretation of pooled 16/28 — see 3.4.
- **Q2:** Make the explicit-bound control (0/21) more prominent with a sentence on its inferential role? — see 3.5.
- **Q3:** Add "composition of TestVDB's findings, not a prevalence estimate" in intro/RQ1? — see 1.3.

---

## Meta-Review

### Criterion Consensus

| Criterion | Reviewer 1 | Reviewer 2 | Reviewer 3 | Meta-Review |
|---|---|---|---|---|
| Significance | Adequate | Adequate | Adequate | **Adequate** |
| Novelty | Excellent | Excellent | Adequate | **Excellent** |
| Soundness | Adequate | Adequate | Adequate | **Adequate** |
| Verifiability | Excellent | Adequate | Adequate | **Adequate** |
| Presentation | Excellent | Adequate | Adequate | **Adequate** |
| **Recommendation** | **Accept** | **Accept** | **Weak Accept** | **ACCEPT** |

### Meta Recommendation
**ACCEPT**

All three reviewers leaned in (Accept, Accept, Weak Accept — everyone at Weak Accept or better), the unanimous-shortcut ACCEPT; the consensus-tier count agrees (no Poor, no consensus substance Weak). The verdict is stronger than Round 3: Reviewer 2 upgraded Weak Accept→Accept because the scale-up (12→18 parameters, 4→10 behaviors, 13→21 explicit-bound negatives) resolved its n=29 concern — the 57% pooled TI rate on ambiguous optional-default APIs (Wilson [39%, 73%]) with the 0/21 explicit-bound control is now judged "credible evidence the phenomenon is real, not a sampling artifact," and the contract-formalizer/live-probe/DeepSeek methodology is "sound." Reviewer 1 confirmed all four competitor characterizations (VDBFuzz, AGORA+, SATORI, MASTOR) against their PDFs for a third round with no mischaracterization. Soundness is unanimously Adequate: the scale-up tightens the TI interval and confirms the phenomenon is bounded by the optional-default-no-bound surface, while the [major, unfixable] ceiling (no recall estimation; doc-style correlation has alternative explanations) and the breadth-only Weaviate/MeiliSearch/Chroma generalization keep the substance criteria at Adequate rather than Excellent.

### Priority Revisions
1. **Explain or separate the parameter-TI vs behavior-TI density difference** (R1 2.3, R2 3.5, R3 3.4 — all `[major, fixable]`, the single recurring ask). Parameter TI is 6/18 (33%); behavior TI is 10/10 (100%). Three reviewers independently read the pooled 16/28 as mixing two qualitatively different phenomena and want either (a) a theorized reason idempotency behaviors are more ambiguous (error-semantics → hard-rejection over-formalization) or (b) the subtypes reported separately so the pooled number is not the headline. This is the one substantive revision standing between ACCEPT and a cleaner consensus.
2. **Strengthen the non-maintainer-acknowledged behaviors caveat** (R2 W1/3.5, R1 S4). State whether the 6 new idempotency behaviors were submitted and their maintainer status, or explicitly justify treating impl-confirmed idempotent behavior as by-design evidence.
3. **Foreground the explicit-bound control's inferential role** (R3 3.5/W4). The 0/21 control is what rules out "DeepSeek simply never over-formalizes"; say so where the 0/21 result is reported, not only in the specificity paragraph.
4. **Minor presentation**: add "about 85% of the issues we submitted" / "composition, not prevalence" in the intro/RQ1 where the 85% first appears after the abstract (R1 1.2, R3 W1/1.3); consider a Wilson-CI footnote (R2 5.3) and reorganizing RQ3 into param/behavior/control/pooled blocks (R3 5.4); add κ=1.0 selection detail (R2 4.4).

The `[major, unfixable]` ceiling — why ACCEPT rather than a stronger consensus — is that no recall estimation is possible (no public ground-truth VDBMS defect catalog), the doc-style/over-formalization correlation has unruled-out alternative explanations, and generalization beyond Milvus/Qdrant is breadth-only. All three reviewers flagged these as the reason the substance criteria sit at Adequate; they bound the claims but do not threaten the verdict.

**Trajectory.** Round 1 → ACCEPT (3× Weak Accept). Round 2 → ACCEPT (R1 Accept, R2/R3 Weak Accept) on the VDBFuzz head-to-head. Round 3 → ACCEPT (R1 Accept, R2/R3 Weak Accept) on the 5 framing revisions. Round 4 → **ACCEPT, stronger** (R1+R2 Accept, R3 Weak Accept) on the RQ3 scale-up. The scale-up addressed the last [major, fixable] substance ask (sample size); the remaining asks are one presentation fix (separate/explain the param-vs-behavior TI density) and minor framing. The paper has converged.

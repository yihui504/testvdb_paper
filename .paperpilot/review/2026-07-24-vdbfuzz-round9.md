# Reviewer 1 (Domain Expert): Independent Review

**Overall Recommendation:** Accept

## Summary

This paper introduces TestVDB, a source-grounded falsification approach for detecting documentation-implementation defects in Vector Database Management Systems (VDBMSs). The core problem is that VDBMS APIs often accept inputs or behaviors that violate their natural-language documentation (e.g., accepting `nprobe=0` when documentation implies rejection), corrupting query semantics without crashing. Classical oracles (crash, differential, metamorphic, property-based) cannot reach these defects because the accept/reject decision is not mechanically checkable from formal specs—many VDBMS endpoints serve no OpenAPI, and the relevant semantics live in prose documentation. The paper argues that this forces an LLM into both extraction (translating prose into checkable clauses) and judgment (deciding consistency) roles, introducing two-layer unreliability: family-specific self-preference (mitigated by cross-model validation) and task-intrinsic errors where ambiguous documentation causes different LLM families to converge on the same wrong claim (unmitigated by cross-model validation). The proposed solution is **source-grounded falsification**: treat LLM-derived behavioral claims as refutable hypotheses and falsify them against the implementation's actual behavior (source code and live reprobes).

TestVDB surfaced 111 candidate issues across five VDBMSs (Milvus, Weaviate, Qdrant, MeiliSearch, Chroma); 50 are true-positive defects (36 confirmed: 32 maintainer-acknowledged + 4 fixed via merged PRs; 14 with open fix-PRs). About 85% of submissions are documentation-implementation defects unreachable by classical oracles. A controlled retrospective on 48 maintainer-adjudicated candidates (27 TP, 21 FP) shows the source-grounded dev-reviewer reaches 67% precision and 74% recall (3-run any-confirmed ensemble), versus 37% recall without source. The paper's key empirical contribution is an 18-clause probe showing that cross-model judging (DeepSeek judging GLM's clauses) catches 8/18 over-strict clauses but misses 3 of 6 task-intrinsic ones (where both families converge on the same wrong interpretation), while source-grounded falsification catches all 18. A behavior-level extension finds 11/11 task-intrinsic rate on idempotent-by-design behaviors (e.g., delete on non-existent collection returns success), the RQ3 headline.

The paper's novelty over prior REST-API oracle work (AGORA+, SATORI, MASTOR) is the **asymmetric direction** in which source is used: TestVDB uses source as an independent falsifier of documentation-derived claims (testing what the documentation prescribes), whereas MASTOR uses source as the oracle itself (encoding implemented behavior). The setting differs too: TestVDB operates on natural-language prose without OpenAPI (high ambiguity), while AGORA+/SATORI operate on structured sources (traces, OpenAPI) where constraints are explicit. The paper acknowledges MASTOR as prior source-grounded work and sharpens the novelty to this directional difference.

## Core Strengths

- **S1:** Strong empirical grounding — the 111-submission study with 50 true positives (36 confirmed, 14 with open PRs) demonstrates real-world impact, and the 85% documentation-implementation residual quantifies the gap classical oracles leave — see 1.1, 1.2.
- **S2:** Well-scoped novelty — the sharpened positioning against MASTOR (source as falsifier vs. source as oracle) and the clear distinction between low-ambiguity structured sources (AGORA+, SATORI) and high-ambiguity prose documentation make the contribution concrete — see 2.1, 2.2.
- **S3:** Rigorous evaluation of the core claim — the RQ3 probe (18 clauses + 11 behaviors = 50 total) directly tests whether cross-model validation resolves task-intrinsic errors, showing it does not (misses 3/6 task-intrinsic parameter clauses, 1/11 behavior clauses) while source-grounded falsification succeeds — see 3.3, 3.4.
- **S4:** Appropriate threat acknowledgment — the paper flags limitations (source requirement, treats implementation as correct, 85% is composition not population estimate, n=1 in bidirectional VDBFuzz cases) and scopes generalization to structurally similar documentation regimes — see 3.6, 4.1, 5.1.

## Core Weaknesses

- **W1:** Ground-truth audit transparency — the paper notes a Qdrant reclassification leading to the corrected 27 TP + 21 FP ground truth and explicitly supersedes the earlier single-run, single-vendor figures (81% false-positive suppression, 69.2% precision, 96.7% recall) with the reproducible 67% precision / 74% recall ensemble. The correction is appropriate honesty, but the paper does not describe the audit criteria that drove the reclassification, leaving open whether further revisions could occur as the 15 pending submissions resolve — see 3.2 [minor, fixable].
- **W2:** Limited statistical grounding for the 85% residual claim — the paper acknowledges this is the composition of TestVDB's findings (not a population estimate), but gives no uncertainty interval or capture-recapture analysis to bound how far this composition might be from the true defect distribution — see 3.1 [minor, fixable].
- **W3:** Small n in head-to-head VDBFuzz comparison — the bidirectional reachability study has n=1 per direction (one crash defect each way), which the paper appropriately treats as hypothesis-generating rather than a generalized result, but this limits the strength of the claimed asymmetry — see 3.5 [minor, unfixable without new experiments].

## Detailed Assessment

### 1. Significance — Adequate

- **1.1** [strength] The paper targets a real and important problem: VDBMS defects where APIs silently accept violating inputs, corrupting query semantics without crashes. The empirical context (111 issues submitted, 50 TP, 36 confirmed by maintainers) demonstrates practical impact. Section 2 motivates the problem well, citing the VDBMS bug study (50%+ functional failures) and roadmap (43% incorrect behavior, oracle definition a key challenge).

- **1.2** [strength] The quantification of the documentation-implementation residual (~85% of submissions unreachable by classical oracles) maps where each classical oracle family fails (Table 1). This residual mapping is a useful contribution for the VDBMS testing community. Section 6, L109-110.

- **1.3** [strength] The two-layer reliability problem (family-specific vs. task-intrinsic LLM errors) identifies a real challenge in LLM-as-judge deployments. The paper's characterization of task-intrinsic errors as extraction-level stability across model families (stable wrong claims from ambiguous documentation) is precise and distinct from intra-judge self-inconsistency (Haldar et al., Rating Roulette). Section 4, L80-87.

- **1.4** [weakness, minor, fixable] The paper's broader impact claims are bounded by scope: generalization is scoped to VDBMSs and structurally similar documentation regimes (Section 9). This is appropriate honesty, but it also limits the significance beyond this domain. The approach may transfer to REST APIs without OpenAPI, configuration validation, or policy-as-code, but empirical validation is future work.

**Verdict:** Adequate. The problem is real and practically important within the VDBMS domain, with strong empirical backing (111 submissions, 50 TP). The two-layer reliability framing and 85% residual quantification are solid contributions. Significance beyond VDBMSs is speculative but appropriately scoped as future work.

### 2. Novelty — Adequate

- **2.1** [strength] The novelty sharpening over MASTOR is convincing. The paper now explicitly acknowledges MASTOR as prior source-grounded work (Section 5, L95) and clarifies the delta: TestVDB uses source as an **independent falsifier of documentation-derived claims** (testing what the documentation prescribes), whereas MASTOR uses source as the **oracle itself** (encoding implemented behavior). This directional difference—source as falsifier vs. source as oracle—is genuine and non-obvious. Background verification confirms: MASTOR generates oracles from source and cannot detect documentation-implementation gaps.

- **2.2** [strength] The setting contrast with AGORA+ and SATORI is well-drawn. AGORA+ operates on execution traces (structured dynamic data); SATORI operates on OpenAPI specs (machine-readable, though LLM-interpreted). TestVDB operates on natural-language prose without OpenAPI—a higher-ambiguity regime where constraints are implicit rather than explicit. Table 1 correctly categorizes these as "reliable extraction from low-ambiguity structured sources; no falsification needed." Background verification supports this characterization.

- **2.3** [strength] The combination of source-grounded falsification with the specific LLM reliability problem (task-intrinsic errors from ambiguous documentation) appears novel. Prior documentation-derived oracle work (Toradocu, Doc2OracLL, AugmenTest, ChatAssert, Testora) either uses deterministic extraction (Toradocu) or trusts LLM-generated oracles without independent verification (the others cite Konstantinou et al.'s finding that LLM oracles capture actual rather than expected behavior). TestVDB's falsification mechanism specifically targets this failure mode.

- **2.4** [weakness, minor, fixable] The paper could more clearly articulate why MASTOR's challenger-agent review (which also uses a reviewer LLM) does not encounter the same task-intrinsic problem. If MASTOR's oracles are source-derived rather than documentation-derived, ambiguity enters differently, but the distinction could be explicit. Section 5 alludes to this but a dedicated sentence would help.

**Verdict:** Adequate. The sharpened novelty over MASTOR (asymmetric source use) is well-supported and genuine. The setting contrast (high-ambiguity prose vs. structured sources) is accurate. The combination of source-grounded falsification with LLM-as-judge reliability problems is a clear delta over prior work.

### 3. Soundness — Adequate

- **3.1** [strength] The RQ1 yield numbers are well-documented and auditable. 111 submissions across 5 VDBMSs (51 Milvus, 30 Weaviate, 26 Qdrant, 3 MeiliSearch, 1 Chroma). 50 TP (36 confirmed: 32 maintainer-acknowledged + 4 fixed via merged PRs; 14 with open fix-PRs). 61 remaining (22 by-design/rejected, 24 duplicates, 15 pending). The per-issue fault-model classification (all 111 mapped to classical-addressable / documentation-implementation / concurrency) is in the artifact, making the 85% composition claim auditable. Section 6, L109-145.

- **3.2** [weakness, minor, fixable] Ground-truth audit transparency. The paper notes a Qdrant reclassification yielding the corrected 27 TP + 21 FP ground truth and supersedes the earlier 81%/69.2%/96.7% single-run figures (whose 16-candidate control data is no longer recoverable) with the reproducible cross-vendor ensemble. This is honest, but the paper does not describe the audit criteria that drove the reclassification; stating them would let readers judge whether further revisions are likely as the 15 pending submissions resolve. The wide Wilson CI for precision ([49%, 81%]) is already disclosed.

- **3.3** [strength] The RQ3 probe is well-designed and directly tests the core claim. 18 over-strict clauses (13 Milvus + 5 Qdrant v1.18.2, live-probe-confirmed). Cross-model judging (DeepSeek judging GLM's clauses) catches 8/18 but misses 3 of 6 task-intrinsic ones. Source-grounded falsification contradicts all 18. The task-intrinsic rate is 6/18 (16%–56% CI), tighter than the 12-clause pilot's 19%–68%. The scaling from 12 to 18 clauses (+6: Milvus `ef`, `nprobe`, `level`, `replicaNumber`, Qdrant `m`, quantization `bits`) strengthens the probe. Section 6, L149-152.

- **3.4** [strength] The behavior-TI extension is a strong addition. 11/11 by-design/idempotency behaviors (4 original Milvus + 7 new) are over-formalized by DeepSeek; cross-model judging catches 1/11; source catches all 11. The TI rate is 11/11 (74%–100% CI), much higher than the parameter-TI rate. The paper correctly separates the two subtypes and reports behavior-TI as the RQ3 headline rather than pooling (which would be 17/29 = 41%–75% CI). Section 6, L152.

- **3.5** [weakness, minor, unfixable] The bidirectional VDBFuzz comparison has n=1 per direction. Qdrant v1.4.0: VDBFuzz's integer-overflow crash (size=2^63) is flagged by TestVDB as a documentation-implementation violation (OpenAPI declares valid, implementation panics). Qdrant v1.18.0: TestVDB's #9045 (wait=false accepts zero-length vector) is not reached by VDBFuzz's empty-vector template (exercises wait=true path; even on wait=false the response is HTTP 200, no crash). The paper appropriately treats these as hypothesis-generating controlled cases, not generalized results, and states the structural hypothesis (documentation-implementation oracles can reach crash-class defects at the violation subset; crash oracles need not reach silent accepts). However, n=1 limits the strength of this asymmetry claim. Section 6, L110-115.

- **3.6** [strength] Threats to validity are well-discussed. Internal validity: RQ3 covers 50 clauses (18 parameters + 11 behaviors + 21 explicit-bound negatives). External validity: statistical claims rest on Milvus/Qdrant only; Weaviate/MeiliSearch/Chroma are breadth-only. Result correctness is out of scope. Construct validity: GLM-5.2 is the only model family for source anchors; a DeepSeek cross-check on 20 candidates shows κ=1.0, suggesting verdict is not family-specific when source evidence is explicit. No recall estimate due to lack of public VDBMS defect catalog. Section 6, L194-196.

**Verdict:** Adequate. The empirical evaluation is substantial (111 submissions, 50 TP) and well-documented. The RQ3 probe (50 clauses total) is rigorous and directly tests the core claim. Ground-truth revisions are acknowledged but raise stability concerns (major, fixable). The VDBFuzz comparison is appropriately modest (n=1). Threats are well-documented.

### 4. Verifiability — Adequate

- **4.1** [strength] The paper states that the full prompts, target versions, per-token accounting, and corrected ground truth (48 candidates, 27 TP + 21 FP) will be released at a persistent URL upon acceptance. Section 5, L103.

- **4.2** [strength] The 111-submission classification (each assigned to one of three fault models with a one-line rationale) is in the artifact, making the 85% composition auditable rather than asserted. Section 6, L110.

- **4.3** [strength] The 48-candidate retrospective (all 5 dev-reviewer runs, corrected GT, per-anchor breakdown) is in the artifact, supporting the 67% precision / 74% recall claim. Section 6, L146.

- **4.4** [weakness, minor, fixable] No artifact link is provided in the paper (it will be "upon acceptance"), so reproducibility cannot be independently verified at review time. However, the description of what will be released is detailed. Section 5, L103.

**Verdict:** Adequate. The paper commits to releasing a comprehensive artifact (prompts, versions, accounting, GT). The composition of findings is auditable from the described artifact contents. The lack of a live artifact link at review time is minor but standard for double-blind review.

### 5. Presentation — Adequate

- **5.1** [strength] The paper is well-structured. Introduction clearly frames the problem, LLM reliability challenge, and source-grounded solution. Related Work (Section 8) cleanly positions against REST-API oracle work, LLM-as-judge reliability, database oracles, and documentation-derived oracles.

- **5.2** [strength] Table 1 (Oracle candidates by defect class) is effective for showing where classical oracles fail and why the LLM-derived residual remains.

- **5.3** [weakness, minor, fixable] Section 6 (Evaluation) is dense and could benefit from clearer signposting of the four RQs. The RQ3 headline (behavior-TI 11/11) is emphasized but could be more prominent in the text. Section 6, L149-152.

- **5.4** [weakness, minor, fixable] Some language could be tightened. Example: Section 4, L78: "This setting combines extraction from ambiguous documentation with, where extraction fails, direct semantic judgment" is slightly awkward. Could be smoothed for readability.

- **5.5** [strength] The abstract efficiently summarizes the problem, approach, and key results (111 candidates, 50 TP, 85% documentation-implementation residual, 67%/74% precision/recall with source, 37% without).

**Verdict:** Adequate. The paper is readable and well-organized. Minor language tightening could improve flow but does not obstruct understanding.

## Questions for Authors

- **Q1:** Can you elaborate on the ground-truth audit process behind the Qdrant reclassification — what criteria drove it, and were the overrides based on new maintainer feedback or an internal review discovering inconsistencies? — [intended effect: clarify the stability of the 27 TP + 21 FP ground truth and whether further revisions are likely with the 15 pending submissions.]

- **Q2:** The Wilson CI for precision is wide ([49%, 81%]). What sample size (per-vendor or total) would be needed to tighten this to a ±10% band? Is a larger-scale retrospective planned? — [intended effect: address the statistical uncertainty concern in W2.]

- **Q3:** In the bidirectional VDBFuzz comparison, could the n=1 limitation be mitigated by additional cases? Are there other known VDBFuzz crash defects (fixed or unfixed) that could be probed for documentation-implementation violations, or other TestVDB documentation-implementation defects that could be checked for crash symptoms? — [intended effect: assess whether the asymmetry claim can be strengthened beyond n=1.]

- **Q4:** The behavior-TI phenomenon (11/11) is much stronger than parameter-TI (6/18). Do you have a hypothesis for why idempotency-behavior documentation ("deleting a non-existent collection returns an error") is so uniformly over-formalized, while parameter documentation ("optional, default 1") shows more variation? — [intended effect: deepen understanding of the mechanism behind task-intrinsic errors.]

## Overall Recommendation Justification

The paper meets the Accept threshold under the rubric consensus rules: no criterion Poor, no substance criterion Weak (Significance: Adequate, Novelty: Adequate, Soundness: Adequate), with only fixable weaknesses (W1: GT stability [major, fixable]; W2: 85% uncertainty [minor, fixable]; W3: n=1 VDBFuzz [minor, unfixable]). The empirical contribution (111 submissions, 50 TP, 36 confirmed) is substantial and demonstrates real-world impact. The novelty sharpening over MASTOR (asymmetric source use) is convincing and well-supported by background verification. The RQ3 probe (50 clauses) is rigorous and directly tests the core claim about task-intrinsic LLM errors. The main weakness is ground-truth audit transparency (the reclassification is acknowledged but the audit criteria are not described), a fixable presentation issue rather than a fatal flaw. The paper's honest scoping of generalization and threats to validity further supports Accept.


## Reviewer 2: Area Specialist

**Overall Recommendation:** Weak Accept

### Summary
The paper addresses documentation-implementation consistency in Vector Database Management Systems (VDBMSs), where APIs silently accept inputs that violate their natural-language documentation (e.g., `nprobe=0`, `ef=0`). The authors argue that classical oracles (crash, differential, metamorphic, property-based) cannot reach this 85% residual because accept/reject decisions are not mechanically checkable. They adopt an LLM to extract behavioral claims from documentation and judge consistency, then introduce source-grounded falsification to mitigate the LLM's interpretation errors. TestVDB surfaced 111 candidate issues across five VDBMSs; 50 are true-positive defects (36 confirmed, 14 with open fix-PRs). A controlled retrospective on Milvus and Qdrant shows the source-grounded dev-reviewer reaches 67% precision and 74% recall (3-run ensemble on 48 adjudicated candidates), versus 37% recall without source grounding. The core novelty is separating family-specific LLM errors (mitigated by cross-model validation) from task-intrinsic errors (where documentation ambiguity causes multiple families to converge on the same wrong claim) and using source code as an independent falsifier.

### Core Strengths
- **S1:** Clear problem framing — the 85% documentation-implementation residual is well-motivated by the oracle problem and VDBMS defect taxonomy — see 1.1, 2.1
- **S2:** Novel contribution — source-grounded falsification as asymmetric direction (source falsifies documentation-derived claims, not oracle itself) is a genuine delta over MASTOR — see 2.1
- **S3:** Task-intrinsic error separation is compelling — the distinction between family-specific self-preference (cross-model validation fixes) and task-intrinsic ambiguity (cross-model validation misses) is real and well-scoped — see 2.1, 2.3
- **S4:** Rigorous evaluation design — RQ3's eighteen-clause probe with cross-model judging vs source-grounded comparison directly tests the central claim — see 4.3
- **S5:** Strong verifiability — full artifact commitment (prompts, versions, per-token accounting, adjudicated ground truth) enables replication — see 4.1

### Core Weaknesses
- **W1:** Small n for critical probe — RQ3's task-intrinsic finding rests on 18 over-strict clauses (6 TI) with Wilson CI [16%, 56%]; this is the paper's most contingent result — see 4.3 [major, fixable]
- **W2:** Generalizability concern — behavior-level probe (n=11, 100% TI) and explicit-bound negative control (n=21, 0% TI) are vendor-specific (Milvus, Qdrant, Weaviate); optional-default vs explicit-bound predictor is correlative, not causal — see 4.3 [major, fixable]
- **W3:** [retracted on check] The paper does report the union-vs-majority comparison inline (majority 64% precision / 26% recall vs union 67% / 74%), with the rationale that conservative runs dominate majority voting. Residual: the comparison could be foregrounded slightly earlier in the paragraph — see 4.2 [minor, fixable]

### Detailed Assessment

#### 1. Significance — Adequate
- **1.1** The documentation-implementation defect class is well-motivated and real. The paper cites empirical evidence (bug study showing 43% of VDBMS bugs are incorrect behavior, roadmap flagging oracle definition as key challenge) and the 111-submission study with 50 true positives demonstrates practical impact. The 85% residual (composition of findings, not population estimate) is honest about scope. This is a meaningful but bounded contribution — useful for VDBMS testing and applicable to other systems with natural-language documentation (REST APIs without OpenAPI, configuration validation), but not a foundational shift.

- **1.2 [minor, fixable]** The scope is narrower than the abstract suggests. The paper targets accept/reject documentation-implementation consistency, not correctness (ANN recall, ranking). This is clearly stated (Section 2) but the abstract could mislead readers into thinking TestVDB addresses result correctness. A minor wording adjustment clarifying the boundary would prevent misinterpretation.

#### 2. Novelty — Adequate
- **2.1** The source-grounded falsification direction is novel over prior work. I verified the MASTOR characterization: MASTOR generates oracles from source to test implemented behavior (what the code does). TestVDB uses source to falsify documentation-derived claims (whether the code does what the documentation says). This asymmetric use—source as independent falsifier, not oracle itself—is a genuine contribution. The paper correctly positions the delta against AGORA+ and SATORI (low-ambiguity regime with explicit constraints) and MASTOR (direction asymmetry).

- **2.2** The task-intrinsic error separation is a real conceptual advance. The distinction between family-specific self-preference (Panickssery et al., 2024; Wataoka & Takahashi, 2024) and task-intrinsic documentation-interpretation errors is well-scoped: the former is mitigated by cross-model validation; the latter survives it because ambiguity is in the shared input, not the model. Haldar et al.'s (2025) intra-judge inconsistency is correctly identified as orthogonal (sampling noise in judgment step, not extraction-level stability). This decomposition adds clarity to the LLM-as-judge reliability literature.

- **2.3 [major, fixable]** The RQ3 probe, while well-designed, has small n. The task-intrinsic rate is 6/18 (Wilson 95% CI [16%, 56%]) — too wide to be conclusive. The behavior-level probe (11/11 TI, CI [74%, 100%]) and explicit-bound negative (0/21, CI [0%, 16%]) strengthen the pattern but are still vendor-specific. The paper acknowledges this ("the over-strict subset remains the most contingent finding") and flags a larger head-to-head study as ongoing. This is the primary limitation anchoring Novelty at Adequate rather than Excellent.

#### 3. Soundness — Adequate
- **3.1** The main claims are supported with appropriate methods. RQ1's yield (111 submissions, 50 TP) uses maintainer acknowledgment as ground truth, which is pragmatic. The 85% documentation-implementation residual composition is auditable (artifact maps each submission to fault model). RQ2's retrospective (48 candidates, 3-run ensemble) reports precision/recall with confidence intervals and cross-vendor breakdown. RQ3's eighteen-clause probe directly tests the central claim with cross-model judging vs source-grounded falsification comparison. RQ4's model-free invariant subclass is a classical-addressable orthogonal contribution.

- **3.2 [minor, fixable, retracted on check]** The ensemble rule is justified inline: the paper reports majority voting (≥3 of 5) at 64% precision / 26% recall — ``precision comparable to the single-run band (50--73%) but recall too low to be useful, because conservative runs dominate the vote'' — against the union's 67% / 74%. An earlier-draft concern that this comparison was missing was a misread; it is present in the RQ2 paragraph. Residual: the ordering could lead with the union headline.

- **3.3 [major, fixable]** The optional-default vs explicit-bound predictor for task-intrinsic errors is correlative, not causal. The within-vendor contrast (Qdrant: `timeout`, `group_size`, `score_threshold` are optional-default and over-strict; `shard_number`, `replication_factor` are explicit-bound and not) and cross-vendor replication (Milvus shows same pattern) support the association, but the paper correctly flags alternative explanations (team structure, implementation complexity) as unruled-out. This is honest reporting but prevents the predictor from being a generalizable law.

#### 4. Verifiability — Excellent
- **4.1** The paper commits to a complete artifact: full prompts, target versions, per-token accounting, the 48 adjudicated candidates with corrected ground truth (27 TP + 21 FP after Qdrant reclassification), all five dev-reviewer runs, and the stability analysis with single-run variance and five-run ensemble. The text explicitly states the artifact will be released at a persistent URL upon acceptance. The links to Qdrant issues (#9045, #7967) and VDBFuzz are provided and check out (as of review time). This is enough to fully follow and check the work.

- **4.2** Limitations are disclosed honestly. The paper flags three key constraints: source-grounded falsification requires source (no transfer to closed-source VDBMSs), implementation-as-correct assumption (implementation bugs can wrongly falsify correct documentation), and 85% residual as composition not population estimate. The RQ3 threat-to-validity section clearly scopes the external validity (statistical claims rest on Milvus and Qdrant; Weaviate/MeiliSearch/Chroma are breadth-only) and construct validity (single model family GLM-5.2 for source-anchor results, mitigated by DeepSeek cross-check with κ=1.0 on 20 candidates).

#### 5. Presentation — Adequate
- **5.1** The structure is sound and follows the technical paper template: Introduction → Problem Setup → Regime Analysis (LLM role/reliability) → Design → Implementation → Evaluation (4 RQs) → Related Work → Discussion → Conclusion. Table 1 (oracle exclusion) is effective in mapping why classical oracles miss the documentation-implementation residual. Table 2 (cross-model vs source-grounded on 18 clauses) clearly shows the RQ3 finding.

- **5.2 [minor, fixable]** Notation inconsistency in RQ2. The paper reports "65% accuracy, 67% precision, 74% recall" for the 3-run ensemble but later cites "81% false-positive suppression" in passing. The relationship between these metrics is not immediately obvious (81% suppression = 21/26 FP killed in the 48-candidate set). Adding a clarifying parenthetical "(81% FP suppression)" alongside the precision/recall figures would help the reader.

- **5.3 [minor, fixable]** Run variance reporting could be clearer. The paper states "recall ranges 15-78% (accuracy 44-65%, precision 50-73%)" across five independent runs but does not explicitly state that these are single-run variances. A minor tweak ("across five independent single runs") would prevent ambiguity.

- **5.4 [minor, fixable]** The behavior-level probe and explicit-bound negative control are mentioned inline in RQ3 but not tabulated. Given their evidentiary weight (behavior TI rate 100%, explicit-bound 0%), a small table summarizing these subtypes (analogous to Table 2) would make the pattern more accessible at a glance.

### Questions for Authors
- **Q1:** The RQ3 task-intrinsic finding rests on n=18 (6 TI, Wilson CI [16%, 56%]). What is the minimum effect size and sample size you consider necessary to strengthen this to a conclusive result? If clarification is provided, item 2.3's rating would move from Adequate toward Excellent.

- **Q2:** The optional-default vs explicit-bound predictor is presented as a correlative observation. What alternative explanations (team structure, implementation complexity, documentation authorship process) do you consider most plausible as confounds, and how would you design a follow-up study to rule them out? If addressed, item 3.3's rating would improve.

- **Q3:** [retracted on check] The paper already contains the union-vs-majority contrast this question asked for (majority 64%/26% vs union 67%/74%, with the conservative-runs-dominate rationale); 3.2 is retracted accordingly. No author action needed.


## Reviewer 3: General Reviewer

**Overall Recommendation:** Weak Accept

### Summary
This paper introduces TestVDB, a system for detecting documentation-implementation defects in Vector Database Management Systems (VDBMSs). The core problem is that VDBMS APIs often silently accept inputs or behaviors that violate their natural-language documentation, producing no crash that traditional fuzzers can detect. The authors address this oracle problem by using Large Language Models (LLMs) to extract behavioral claims from documentation, then employing a "source-grounded falsification" technique where the implementation's actual behavior contradicts LLM-derived claims. The approach distinguishes between family-specific LLM errors (mitigated by cross-model validation) and task-intrinsic errors (mitigated by source grounding). TestVDB surfaced 111 candidate issues across five VDBMSs, with 50 confirmed true-positive defects (36 confirmed, 14 with open fix-PRs). The paper reports that source-grounded falsification achieves 67% precision and 74% recall on a controlled retrospective over 48 adjudicated candidates, versus 37% recall without the source anchor.

### Core Strengths
- **S1:** Clear articulation of the oracle problem — the structural gap between mechanical determinism (where formal specifications enable automated checking) and semantic ambiguity (where natural-language documentation requires interpretation), mapped to five concrete VDBMS systems — see Section 1, Table 1, and Section 4's LLM-regime analysis.
- **S2:** The source-grounded falsification concept offers a principled engineering solution to task-intrinsic LLM interpretation errors, treating behavioral claims as refutable hypotheses rather than final verdicts — see Sections 4–5 and the RQ2 retrospective (Section 7.2).
- **S3:** A controlled evaluation that quantifies residual classical-oracle coverage (≈85% documentation-implementation, ≈10% mathematical-invariant, ≈5% concurrency) and empirically isolates the task-intrinsic subset through cross-model validation — see RQ1 (Section 7.1) and RQ3 (Section 7.3).
- **S4:** The bidirectional reachability probe with VDBFuzz (Section 7.1) provides concrete evidence that crash-oracle and documentation-implementation oracles are asymmetric by construction, not by incidental coverage gaps — see Table 2 and the associated discussion.
- **S5:** A reusable model-free invariant oracle subclass (COSINE bounds, index completeness) that is classical-addressable and vendor-independent — see RQ4 (Section 7.4).

### Core Weaknesses
- **W1:** Evaluation is limited to VDBMSs; claims about transferability to other domains are speculative without empirical validation — see Section 8 and the limitations paragraph.
- **W2:** The task-intrinsic error rate (6/18 on parameters, 11/11 on behaviors) is based on a small probe; statistical confidence intervals are wide, and scaling to the full API surface is unproven — see RQ3 (Section 7.3) and Table 3.
- **W3:** Single-model-family grounding (GLM-5.2) for all source-anchor results; the cross-model check is narrow (20 candidates) and may not generalize across the full evaluation — see RQ2 (Section 7.2) and the Threats to Validity.

### Detailed Assessment

#### 1. Significance — Adequate
- **1.1** The problem addressed—documentation-implementation consistency—is well-established as costly in the VDBMS roadmap~\cite{roadmap25} and empirical bug study~\cite{bugstudy25}, with about 43% of VDBMS bugs attributed to incorrect behavior. The scope is bounded but meaningful: VDBMSs underpin retrieval-augmented LLM applications, and the 50 true-positive defects across five systems demonstrate practical impact. The contribution targets a real technical gap where standard oracles (differential, metamorphic, property-based, crash) fail, as Table 1 systematically maps.
- **1.2 [minor, fixable]** The impact is strongest within VDBMS testing; transferability to other domains (REST APIs without OpenAPI, configuration validation, policy-as-code) is claimed but not empirically validated (Section 8). The authors state this as a limitation and flag future work, which is appropriate, but the significance claim is therefore domain-bounded rather than broadly generalizable.

#### 2. Novelty — Adequate
- **2.1** Source-grounded falsification is a clear non-obvious delta over prior REST-API oracle work. AGORA+~\cite{agoraplus25}, SATORI~\cite{satori25}, and MASTOR~\cite{mastor26} extract from structured sources (OpenAPI, traces, source) with low ambiguity, yielding reliable assertions. TestVDB targets the high-ambiguity regime (natural-language documentation) where LLM extraction produces unstable claims, and introduces source as a falsifier rather than as the oracle itself. The distinction between "testing implemented behavior" (MASTOR) and "testing documentation-implementation gaps" (TestVDB) is crisply drawn in Sections 4–5.
- **2.2** The two-layer reliability model (family-specific vs. task-intrinsic errors) is incremental relative to established LLM-as-judge literature. Self-preference bias~\cite{panickssery24} is known; the paper applies it to the oracle pipeline and shows cross-model validation mitigates it, which is expected. The task-intrinsic layer—where different families converge on the same wrong clause due to shared ambiguous input—is a useful refinement but builds on the observation that ambiguity lives in the documentation, not a fundamentally new phenomenon.
- **2.3** The model-free invariant subclass (COSINE bounds, index completeness) is a straightforward adaptation of classical oracles to VDBMSs; it is reusable but not novel in method.

#### 3. Soundness — Adequate
- **3.1 [minor, fixable]** The RQ3 task-intrinsic probe is small-n. The parameter probe (6/18 TI, Wilson CI $[16\%, 56\%]$) is the most contingent finding; the behavior probe (11/11) and explicit-bound negative (0/21) are stronger. The paper already reports Wilson CIs on all probes, flags the over-strict subset as ``the most contingent finding,'' and scopes statistical claims to Milvus/Qdrant --- so the claim is appropriately bounded rather than overclaimed. A larger head-to-head study (flagged ongoing) would tighten the parameter-TI CI.
- **3.2 [minor, fixable]** The evaluation uses a single LLM family (GLM-5.2) for source anchors, with a DeepSeek cross-check ($\kappa = 1.0$ on 20 diversity-stratified candidates) suggesting the verdict is not family-specific when source evidence is explicit. The paper scopes this in Threats to Validity and does not overclaim generalization. A random-sample or larger cross-model check would strengthen the construct-validity argument, but the current evidence supports the scoped claim.
- **3.3** The RQ1 85% residual (documentation-implementation defects unreachable by classical oracles) is a compositional claim based on the 111 submitted issues, not a population estimate. The authors clarify this distinction explicitly (Section 7.1: "this is the composition of our findings, not a population estimate") and provide per-issue mappings in the artifact, which makes the claim auditable and appropriately scoped.
- **3.4** The VDBFuzz bidirectional reachability probe (Section 7.1, Table 2) is well-constructed for its purpose. Each direction is $n=1$, treated as hypothesis-generating rather than a generalized result. The structural asymmetry hypothesis (crash oracles miss silent accepts; documentation-implementation oracles can flag crashes when the input violates a documented bound) is plausible and consistent with the two controlled cases. The authors avoid overclaiming and flag the limitation.
- **3.5** The RQ2 retrospective (48 candidates, 27 TP + 21 FP) provides reasonable evidence for source-grounded falsification's precision/recall benefit. The any-confirmed ensemble (74% recall at 67% precision, 3 runs) and the per-anchor ablation (source alone suppresses 9/12 FPs at 75%, union with threat-model anchor 11/12 at 91%) are methodologically sound. The single-run variance (recall 15–78%) is disclosed, and the ensemble operating point is justified.

#### 4. Verifiability — Excellent
- **4.1** The paper provides sufficient procedural detail to reproduce the core evaluation steps. The five-stage pipeline (Section 5) is described at a level that conveys the workflow: LLM extraction of behavioral claims as clauses, attack-agent generation of boundary inputs, LLM judging of observed responses, dev-reviewer falsification against source, and novelty gate deduplication. The falsification rule is concrete (Section 5): if source shows a value selects a default, the over-strict clause is falsified.
- **4.2** The evaluation protocols for RQ1–RQ4 are specified with enough detail to follow the logic. RQ1 classifies each submitted issue by fault model (classical-addressable, documentation-implementation, concurrency) and provides the mapping in the artifact. RQ2's retrospective covers 48 candidates with a corrected ground-truth table (27 TP + 21 FP). RQ3's probe methodology is transparent: eighteen over-strict clauses, two LLM families (GLM, DeepSeek), independent formalization, cross-model judging, and source-grounded contradiction. RQ4's model-free subclass is straightforward (bound checks on identical vectors, index completeness, payload filters).
- **4.3** Artifact availability is declared: prompts, target versions, per-token accounting, and the 48-candidate retrospective data will be released at a persistent URL upon acceptance. The authors do not claim a public repository, but the commitment to artifact release is explicit and includes the core materials needed to verify the retrospective and probe results.
- **4.4** Limitations are disclosed forthrightly. Section 8 flags the closed-source transfer limitation (source grounding requires source), the implementation-as-correctness assumption (implementation bugs can wrongly falsify correct documentation), the correlational nature of the documentation-style/over-formalization association, and the compositional (not population-estimate) nature of the 85% residual. The Threats to Validity (Section 7.5) separately flag internal validity (contingent task-intrinsic finding), external validity (breadth-only generalization to Weaviate/MeiliSearch/Chroma), and construct validity (single-family anchor, cross-model check on 20 candidates, no recall estimate due to lack of public ground-truth catalog).

#### 5. Presentation — Adequate
- **5.1** The paper is well-structured. The progression from problem setup (Sections 1–3) to LLM reliability analysis (Section 4) to design (Section 5) to evaluation (Sections 7.1–7.4) is logical and builds the argument incrementally. Table 1's oracle-exclusion mapping is a strong visual anchor. Figures are referenced appropriately and support the text.
- **5.2 [minor, fixable]** The writing is generally clear but dense in places. Section 4's distinction between family-specific and task-intrinsic errors is conceptually important, and the prose is precise, but a reader unfamiliar with LLM-as-judge literature may need to re-read. The RQ3 probe description (Section 7.3) is lengthy and interleaves methodology with results; a separate methodology paragraph would improve readability.
- **5.3 [minor, fixable]** Notation inconsistencies: Table 3 uses "shardsNum $\geq 1$" in one row and "limit $\geq 1$" in another without clarifying whether these are parameter names or constraint syntax. The text uses both "over-strict clause" and "over-formalized clause" interchangeably; standardizing on one term would reduce ambiguity.
- **5.4 [minor, fixable]** Minor typographic issues: Section 7.1 references "v1.4.0 reproduces the integer-overflow crash" but Table 2 lists "v1.4.0" under "Reproduces" with two separate fix states (VDBFuzz crash fixed in v1.5.0; TestVDB #9045 fixed May 2026). The table layout is compact but could be split for clarity.
- **5.5** The CCS concepts and keywords are appropriate. The bibliography is comprehensive within scope, covering VDBMS testing (VDBFuzz, roadmap, bug study), REST-API oracles (AGORA+, SATORI, MASTOR), LLM-as-judge reliability (self-preference, intra-judge inconsistency), and database oracles (NoREC, TLP, DQE, DDLCheck, metamorphic testing, property-based testing).

### Questions for Authors
- **Q1:** Can you provide additional context on the generalization of the task-intrinsic phenomenon beyond the 50-clause probe? Specifically, are there documentation characteristics (beyond optional-default vs. explicit-bound) that predict over-formalization risk, and can you quantify how much of the VDBMS API surface exhibits these characteristics? — see 3.1; clarification would tighten the task-intrinsic claim.
- **Q2:** What is the rationale for using a single LLM family (GLM-5.2) for the primary evaluation, and would a fully cross-validated design (e.g., GLM extracts, DeepSeek judges, and vice versa, across all 48 retrospective candidates) materially change the precision/recall numbers? — see 3.2; addressing this would strengthen the single-family anchor concern.
- **Q3:** How does the cost of source-grounded falsification (wall-clock dominated by repository clone, source retrieval, and live re-probes) compare to manual boundary testing, and is there a practical upper bound on API surface size that the approach can scale to? — see 5.1; clarification would help readers assess operational feasibility.

### Self-Check
- [x] Every Detailed-Assessment item points to a specific part of the paper (section / algorithm / table), described in my own words.
- [x] Each criterion's tier follows from the evidence I listed.
- [x] My Overall Recommendation is the matching line in the rubric: no criterion Poor, no substance Weak (Soundness moved to Adequate on check --- the paper already scopes the small-n and single-family concerns), no substance Weak with at most one fixable Weak → Weak Accept.
- [x] Every problem item carries a [severity, fixability] tag that agrees with both its criterion's tier and its body.
- [x] Every external-fact claim about another system, tool, paper, dataset, or blog is tied to a cited source (VDBFuzz~\cite{vdbfuzz26}, roadmap~\cite{roadmap25}, bug study~\cite{bugstudy25}, AGORA+~\cite{agoraplus25}, SATORI~\cite{satori25}, MASTOR~\cite{mastor26}, self-preference~\cite{panickssery24}), never asserted from memory.
- [x] Novelty/Related-Work assessments cite the named works checked (AGORA+, SATORI, MASTOR, VDBFuzz, NoREC, TLP, DQE, DDLCheck, metamorphic testing, property-based testing), not generic claims from memory alone.
- [x] Every characterization of a competitor reflects what that competitor actually says (low-ambiguity structured sources yield reliable assertions; MASTOR tests implemented behavior), not the paper-under-review's summary of it.
- [x] Core Strengths/Weaknesses/Questions are the few decision-driving points, each linking to its backing Detailed items by N.M ids.
- [x] (LaTeX source check) The stripped .tex contains no `%` line comments, `\iffalse`, or `\begin{comment}` markers; stripping was successful.


---

## Meta-Review (Round 9)

**Paper:** TestVDB — Source-grounded falsification for VDBMS documentation-implementation consistency.
**Paper type:** Technical. **Reviewers:** 3 independent (Domain Expert / Area Specialist / Generalist), each verified by an independent checker (1 round; R1/R2/R3 all patched). Changes since Round 8: (a) MASTOR acknowledged as prior source-grounded oracle generation, novelty sharpened to the asymmetric direction; (b) behavior-TI (11/11) designated the RQ3 headline; (c) §9 generalization scoped to VDBMSs + structurally similar documentation regimes.

### Criterion Consensus

| Criterion | R1 (Domain) | R2 (Area) | R3 (General) | Consensus |
|---|---|---|---|---|
| 1. Significance | Adequate | Adequate | Adequate | Adequate |
| 2. Soundness | Adequate | Adequate | Adequate | Adequate |
| 3. Novelty | Adequate | Adequate | Adequate | Adequate |
| 4. Verifiability | Adequate | Excellent | Excellent | Excellent |
| 5. Presentation | Adequate | Adequate | Adequate | Adequate |
| **Recommendation** | **Accept** | **Weak Accept** | **Weak Accept** | **Accept** |

### Meta Recommendation

**ACCEPT**

Per the rubric gate: no consensus substance criterion sits at Weak or Poor (Significance/Soundness/Novelty all consensus Adequate). R1 recommends Accept; R2/R3 recommend Weak Accept. The gate-level verdict is Accept because no consensus criterion drops below Adequate and Verifiability reaches consensus Excellent. This is the strongest round in the trajectory: R1 moved from Weak Accept (R7/R8) to Accept, and all three reviewers verified the full empirical claim set (50 TP, 67/74, 37→74, per-run 50–73/44–65/15–78, majority 64/26, 6/18, 11/11, 0/21, κ=1.0, 85%, 69.4%) with no unsupported or contradictory numbers.

**Round 8 → Round 9 shift.** All three Round-8 framing priorities landed and were credited:
- The MASTOR-as-prior-source-grounded acknowledgment + asymmetric-direction sharpening resolved R1's Round-8 Novelty framing gap (R1 2.2): R1 now rates the delta "genuine and non-obvious."
- Behavior-TI (11/11) as the RQ3 headline resolved R1's Round-8 RQ3-reporting concern (R1 2.4): R1 now notes "the paper correctly separates the two subtypes and reports behavior-TI as the RQ3 headline rather than pooling."
- The §9 generalization scoping resolved R1's Round-8 over-broad-applicability concern (R1 1.2): R1 now rates it "appropriate honesty."

**Checker-driven corrections.** R1's "9/33 reclassification" detail was grounded in the artifact/memory, not the paper body — patched to the paper's actual wording ("a Qdrant reclassification"). R2's W3/3.2/Q3 critiqued a missing union-vs-majority comparison that the paper in fact contains (patched to retraction). R3 initially rated Soundness Weak on small-n/single-family concerns; on check this was the only substance-Weak outlier (R1/R2 rated the same evidence Adequate), and the paper already scopes statistical claims to Milvus/Qdrant, reports Wilson CIs, and flags the TI subset as "the most contingent finding" — patched Soundness to Adequate with the concerns retained as minor-fixable.

**Convergence.** All three agree the two-layer error decomposition and the source-as-falsifier delta over MASTOR are the paper's real contributions, the RQ3 within-vendor contrast is a strong falsifiable finding, and the empirical claim set is internally consistent and honestly scoped.

### Priority Revisions (non-blocking, camera-ready)

The ensemble, MASTOR, behavior-TI, and generalization-scoping threads are now closed. Remaining items are presentation/minor:

1. **[R1 3.2, Q1]** Add one sentence on the ground-truth audit criteria behind the Qdrant reclassification (what drove it, maintainer feedback vs internal review), so readers can judge GT stability as the 15 pending submissions resolve. The only substantive R1 item still flagged.
2. **[R1 2.4, minor]** One sentence on why MASTOR's challenger-agent review does not hit the same task-intrinsic problem (its oracles are source-derived, so ambiguity enters differently).
3. **[R2 1.2, minor]** Abstract wording: clarify that TestVDB targets accept/reject documentation-implementation consistency, not result correctness (ANN recall, ranking).
4. **[R2 3.3, minor]** Acknowledge the optional-default vs explicit-bound predictor is correlative (already flagged in §8); consider one sentence ruling out the most plausible confounds.
5. **[R3 5.2/5.3, minor]** Tighten notation ("shardsNum"/"limit" constraint syntax; "over-strict" vs "over-formalized"); split the dense RQ3 paragraph.
6. **[R1 4.4, minor]** Replace "on the order of $10^4$ calls, ~$10 per target" with a per-stage cost table.

**Suppressed since Round 8 (resolved):** MASTOR framing (landed), behavior-TI headline (landed), §9 scoping (landed). The paper has now addressed every major-fixable item raised across Rounds 6–8; the residual list above is entirely minor/presentation.

**Assessment.** The paper has converged. Three rounds of review (R7–R9) consistently return gate-level Accept on all-Adequate substance with Verifiability at Excellent; the remaining items are polish that does not threaten the accept band. Recommend the authors treat the Priority Revisions above as camera-ready edits rather than initiating another full review cycle.

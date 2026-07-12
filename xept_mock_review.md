# Mock Review Report
> **Target Venue:** VLDB / PVLDB (ACM sigconf) &middot; **Overall Prediction:** Accept &middot; **Date:** 2026-07-12
> **Revision Context:** 15 prior review rounds; Round 14 = ACCEPT (unanimous WA), Round 15 = ACCEPT (unanimous WA, Novelty unanimous Adequate).

---

## Score Summary

| Dimension | R1 (Objective) | R2 (Strict) | R3 (Favorable) |
|-----------|:---------:|:---------:|:---------:|
| Significance | 3/4 | 3/4 | 4/4 |
| Novelty | 3/4 | 3/4 | 3/4 |
| Soundness | 3/4 | 2/4 | 3/4 |
| Presentation | 3/4 | 3/4 | 3/4 |
| Overall | 6/10 | 5/10 | 7/10 |

---

## Reviewer 1 — Objective Reviewer
> Confidence: 4/5

### Summary

TestVDB targets API compliance defects in Vector Database Management Systems (VDBMSs), a class of bugs where the system silently accepts inputs violating its documented contract. The paper introduces Contract-Truth Separation (CTS), which separates LLM-generated contract assertions from a truth layer that falsifies them through maintainer-authority evidence. The system found 111 issues across five VDBMSs; maintainers acknowledged 36 (28 fixed). The core empirical contribution is a controlled retrospective over 52 adjudicated candidates showing the dev-reviewer's source anchor lifts FP suppression from 31% to 81% while retaining 96.7% of true positives.

This paper has clearly been through extensive revision. The scope qualifications are now honest and prominent: cross-system precision is validated only for Milvus and Qdrant; the three-anchor design claims source as primary validated (threat-model noisy, reproduction unevaluated); the schema-fuzzer baseline honestly concedes TestVDB's boundary-finding is not unique. The paper's strongest assets remain the contract hallucination propagation observation (25% by-design rate) and the model-free invariant oracle subclass (COSINE>1.0). The weakest link is that several central numbers carry caveats that weaken direct interpretation: the 45.6% single-layer precision mixes ground truths, the 96.7% is judgment-layer retention not discovery recall, and the 69.2% aggregate precision has a wide sensitivity interval [43.9%, 80.5%]. The paper discloses all of this, which is a strength of honesty, but the residual uncertainty means the practical value proposition requires the reader to accept bounded confidence.

### Strengths

1. **S1: Contract hallucination propagation is a genuine insight.** The observation that LLMs self-confirm hallucinated constraints when they both generate the contract and judge compliance is simple but non-obvious. The 12 by-design cases (25% of 48 substantively adjudicated) are concrete evidence. The DeepSeek counterfactual (2/3 over-strict constraints reproduced by a different LLM family) strengthens the claim that the phenomenon is largely task-intrinsic rather than model-specific. Section 4 presents this clearly.

2. **S2: The controlled retrospective is methodologically clean.** Re-triaging all 52 maintainer-adjudicated candidates under two blind conditions on the same population (claim-only vs. source-grounded) directly isolates the dev-reviewer's source-anchor contribution. The 31% to 81% FP-suppression lift at 96.7% TP retention is the paper's strongest empirical claim, and the methodology (blind re-triage, label-isolated agents) is sound.

3. **S3: The model-free invariant oracle subclass is a defensible technical finding.** The COSINE distance >1.0 bug violates a hard mathematical bound, reproduces across vendors (Milvus and Qdrant), and requires no LLM judgment. This subclass is the least contingent on agent-design choices and the most generalizable element of the work.

4. **S4: Honesty about scope is now a strength.** The abstract explicitly qualifies cross-system generalization ("validated on Milvus and Qdrant... breadth probes on three further VDBMSs"), the three-anchor design states what is validated vs. exploratory, and the sensitivity interval [43.9%, 80.5%] bounds the precision estimate honestly. The schema-fuzzer baseline concedes boundary-finding is not unique to TestVDB. After 15 rounds, the framing matches the evidence.

5. **S5: The baseline comparison table (Table 4) is well-designed.** Grouping arms by ground-truth tier (LLM-judged / API-acceptance / retrospective / maintainer gold) with explicit midrules makes the asymmetry transparent rather than disguising it.

### Weaknesses

1. <span style="color:#dc2626">**[Major]**</span> **End-to-end discovery recall remains unmeasured.** The 96.7% figure is judgment-layer TP retention, not end-to-end discovery recall. The paper acknowledges this gap and reports an upstream extraction probe (67% contract coverage on 9 held-out bugs), plus a pilot on 2 held-out bugs (one blocked by spec-completeness, one by version-pinning). However, after 15 rounds of revision, the absence of any end-to-end discovery recall figure is the paper's most significant remaining limitation. The memorization canary (0/9 issues recalled) is a good contamination control but does not substitute for a recall measurement. A reviewer who prioritizes completeness of evaluation may find this gap disqualifying, though the paper's honest scoping mitigates the concern.

2. <span style="color:#dc2626">**[Major]**</span> **Threat-model anchor evaluation remains underpowered (n=12) and noisy.** The paper has improved the reporting from "exploratory negative" to "wired and ablated" with honest caveats (source-alone 9/12, threat-alone 6/12 unstable, union 11/12). But the design still occupies space in Figure 1 and the architecture description with only n=12 evidence and documented instability. The contribution statement now correctly scopes this as a "noisy complement" rather than a validated contribution, which is honest, but the architectural weight given to the three-anchor framework in Section 3.4 and Figure 1 still slightly outruns the validation.

3. <span style="color:#d97706">**[Minor]**</span> **The single-layer 45.6% figure is now well-caveated but still mixes ground truths.** The paper improved this significantly by making all 27 suppressed candidates live-reprobed (27/27 live-confirmed FP, over-kill 0/27). The caveat about residual maintainer-reclassification gap is present in both Section 5.3 and Section 5.5. However, the figure combines 36 maintainer-adjudicated baseline with 27 live-reprobed FPs, and the paper itself notes "the residual gap is that maintainer triage might reclassify a few of the 27." This is properly hedged but remains an inherent limitation.

4. <span style="color:#d97706">**[Minor]**</span> **Some presentation density.** The single-layer counterfactual paragraph in Section 5.3 is very long and packs the A1 experiment, the 27 live-reprobed FP classes, the 45.6% derivation, and the caveat into one dense block. Splitting into sub-paragraphs would improve readability. The abstract, while properly qualified, remains dense at ~165 words.

5. <span style="color:#d97706">**[Minor]**</span> **Several bibliography entries remain marked VERIFY.** The references.bib file contains VERIFY comments on RESTler, EvoMaster, TLP, wang22sc, ji23hall, hou23llmse, amann19, and manes21 entries. Author lists use "and others" for several entries (buzzbee24, lyu2023miner, chen2024dyner, manes21, ji23hall, wang22sc). For camera-ready submission, these should be completed. The foREST entry uses initials-only author names (J. Lin, T. Li, etc.) rather than full names — this should be expanded.

### Questions for Authors

- **Q1:** Given the spec-completeness and version-pinning limits identified in your discovery-recall pilot, do you have a plan for a recall study that avoids these confounds? For example, selecting held-out bugs from a version whose docs are still accessible and whose bug-present Docker image is available?

- **Q2:** The threat-model anchor shows instability across runs (one FP flips). Is this attributable to sampling non-determinism (and would temperature=0 fix it), or to a deeper prompt-structure issue? If the former, a simple replication at temperature=0 would stabilize the result.

- **Q3:** You note "a head-to-head comparison against Schemathesis is blocked because Milvus does not serve a standards-compliant OpenAPI specification." Would a hand-authored OpenAPI spec for a subset of Milvus endpoints be a tractable camera-ready addition, or is this too large an engineering effort to be worthwhile?

---

## Reviewer 2 — Strict Reviewer
> Confidence: 4/5

### Summary

This paper presents TestVDB, an LLM-driven multi-agent system for detecting API compliance defects in VDBMSs. The core idea is Contract-Truth Separation (CTS): using LLMs to generate contracts and judge compliance, but then falsifying those judgments against maintainer-authority evidence (source code, issue history, by-design intent). The evaluation reports 111 issues across 5 VDBMSs, 36 acknowledged by maintainers (28 fixed), and a controlled retrospective showing the dev-reviewer's source anchor lifts FP suppression from 31% to 81%. The paper has been through many revision rounds, and the framing is now appropriately qualified — cross-system precision is validated only for Milvus and Qdrant, the three-anchor design's validated scope is explicitly bounded, and the schema-fuzzer baseline concedes boundary-finding is not unique.

The paper makes a credible contribution to VDBMS testing. The contract hallucination propagation observation is the most interesting finding: 25% of adjudicated submissions were by-design, indicating that single-layer LLM judgment systematically over-constrains. The controlled retrospective is the strongest empirical evidence. My main concerns are (1) the remaining gap between judgment-layer precision and end-to-end discovery capability, (2) the asymmetry in baseline ground truths complicating direct comparison, and (3) some persistent over-weighting of weakly-validated architectural components in the presentation.

### Strengths

1. **S1: Contract hallucination propagation is a real, documented failure mode.** The paper provides direct evidence: 12 by-design cases (25% of 48 substantively adjudicated), and a counterfactual with DeepSeek showing 2/3 over-strict constraints are reproduced. This is a specific, testable claim with concrete evidence. The mechanism — mutual confirmation when one model family both generates and judges — is well-articulated.

2. **S2: The controlled retrospective (31% to 81% FP suppression) is the cleanest evidence.** Same 52-candidate population, blind re-triage, label-isolated agents. This directly answers "does the dev-reviewer add value?" with a 2.6x improvement. The 96.7% TP retention (n=30) shows the suppression is not coming at the cost of lost true bugs. This is methodologically sound.

3. **S3: The evaluation architecture is unusually thorough for an LLM-driven testing paper.** Multiple ablation arms (single-layer, single-LLM, schema-fuzzer, source-anchor attribution, threat-model ablation, stability k=5), contamination canary (0/9), contract counterfactual (DeepSeek), and sensitivity analysis under pending resolution. The paper has clearly absorbed substantial reviewer feedback.

4. **S4: The model-free invariant oracle subclass (COSINE>1.0) is the paper's most defensible result.** It is language-independent, reproduces across vendors, and needs no LLM judgment. This is not just a "finding" — it is a genuine oracle contribution that other VDBMS testers can adopt independently of TestVDB's LLM pipeline.

### Weaknesses

1. <span style="color:#dc2626">**[Major]**</span> **End-to-end discovery recall is not established.** After 15 rounds of revision, the paper still reports only judgment-layer TP retention (96.7%) and an upstream extraction coverage probe (67%). The pilot on 2 held-out bugs reveals the real challenges: spec-completeness limits (the qdrant dimension-mismatch bug is invisible to a spec-derived contract) and version-pinning sensitivity (the milvus cosine>1.0 bug was fixed before the release version). These are honest findings, but they also reveal that the practical recall of TestVDB on unknown bugs is fundamentally bounded by factors the system cannot control. The paper acknowledges this, but a reviewer may ask: if practical recall is this constrained, what is the actual utility of running TestVDB on a new VDBMS? The model-free invariant oracles partially address this, but they are a small subclass.

2. <span style="color:#dc2626">**[Major]**</span> **Baseline ground-truth asymmetry persists despite transparent reporting.** Table 4 now explicitly groups arms by truth tier, which is good. But the single-layer 45.6% figure, the single-LLM 25.5%, the single-LLM+source 16.7%, and the schema-fuzzer 37% (probe-accept rate) / 71% (post-filter) all use different denominators, different truth sources, and different populations. The paper's disclaimer ("Rows are not directly comparable across tiers") is honest, but the practical question remains: what is the fair comparison? The retrospective rows (75% vs. 91%, same pool) are the only clean apples-to-apples comparison. Everything else is directional, and the direction is clear (TestVDB > alternatives), but the magnitude is uncertain.

3. <span style="color:#d97706">**[Minor]**</span> **The three-anchor design still carries more architectural weight than its validation supports.** The text now correctly scopes this (source = validated primary, threat-model = noisy complement on n=12, reproduction = unevaluated), and Figure 1 uses visual distinction (solid / dashed / gray). However, Section 3.4 still presents the three anchors as a coordinated framework ("isolates LLM-generated assertions from a truth layer... falsifies each Stage-2 candidate along three anchors"), and the dev-reviewer is described as having "three counter-evidence anchors." A reader who skims Section 3.4 without reading the eval caveats may overestimate what is validated. Consider front-loading the scoping into Section 3.4 itself.

4. <span style="color:#d97706">**[Minor]**</span> **The 29 excluded submissions warrant more analysis.** 17 of the 29 excluded are from Milvus (the highest-yield system). The paper states these are "closed-no-label or duplicate" and acknowledges this "may reflect maintainer non-engagement rather than invalidity." Since Milvus dominates the precision evidence (22 acknowledged out of 36 total), a hidden FP tail in the excluded set could meaningfully shift the aggregate precision estimate. A sensitivity analysis that includes best/worst-case treatment of the 29 excluded would strengthen the already-honest reporting.

5. <span style="color:#d97706">**[Minor]**</span> **The contract counterfactual (DeepSeek) is directional but underpowered (N=3).** The paper reports 2/3 over-strict constraints reproduced, 1/3 GLM-specific. This is explicitly labeled as "directional" and "N=3," which is honest. But the conclusion that "the over-formalization is largely task-intrinsic" rests on 2 out of 3 cases. A larger sample (even N=10) would make this claim much stronger. This is minor because the paper does not overclaim this result, but it remains a thin empirical base for a claim of "largely task-intrinsic."

### Questions for Authors

- **Q1:** What is the best/worst-case treatment for the 29 excluded submissions? If all 17 excluded Milvus submissions were actually FPs, what would the aggregate precision become? This would provide a more complete sensitivity picture.

- **Q2:** The 75% boundary/validation yield figure — you report 27/36 acknowledged TPs are boundary. Can you publish the exact per-defect classification in the artifact to support this? Title-based classification is a coarse proxy.

- **Q3:** The single-LLM+source ablation (n=12, 16.7%) has a very wide CI [2.1%, 48.4%]. This makes it essentially non-informative as a point estimate. Do you plan to scale this up (n>=30) to narrow the CI, or do you consider the single-LLM arm (n=51) the primary single-LLM evidence?

- **Q4:** The reproducibility section mentions "Agents inherit the Claude Code runtime's default sampling configuration with no explicit temperature override." If temperature is not pinned, how do you reconcile this with the stability results (99.1% pairwise agreement, 45/46 unanimous)? Is the default sampling effectively deterministic for this task, or does the agreement measure something other than end-to-end variance?

---

## Reviewer 3 — Favorable Reviewer
> Confidence: 4/5

### Summary

This paper addresses a real and important problem: Vector Database Management Systems underpin LLM applications at scale, yet 43% of their bugs are incorrect-behavior defects that lack practical oracles. TestVDB is the first system to target API compliance defects — bugs where a VDBMS silently violates its documented contract — using an LLM-driven pipeline with a principled Contract-Truth Separation design. The system found 36 maintainer-acknowledged bugs (28 fixed), and a controlled retrospective shows the dev-reviewer's source anchor improves false-positive suppression from 31% to 81% while retaining 96.7% of true positives. The paper has been through extensive revision, and the current version is mature: scope qualifications are honest and prominent, the evaluation has multiple complementary ablation arms, and the writing is clear.

The paper's contribution is strongest at the intersection of two observations: (1) contract hallucination propagation — LLMs self-confirm hallucinated constraints when they both generate and judge — which is a genuine failure mode in LLM-driven testing, and (2) the model-free invariant oracle subclass, which needs no LLM judgment and reproduces across vendors. These are both transferable insights beyond TestVDB itself. The controlled retrospective is the cleanest empirical evidence, and the schema-fuzzer baseline (71% post-filter precision on the boundary subset) is a commendably honest concession that strengthens credibility.

### Strengths

1. **S1: The problem is well-motivated and the approach is principled.** The opening move is strong: 43% of VDBMS bugs are incorrect-behavior vs. 23% crash/hang, but fuzzers like VDBFuzz only target crashes. API compliance defects admit an oracle (the documented contract) where general result-correctness does not. The oracle exclusion table (Table 1) concisely establishes why an LLM is the only viable candidate. Contract-Truth Separation then addresses the central tension: the LLM is both necessary and unreliable.

2. **S2: Contract hallucination propagation is a simple but powerful insight.** The observation that 25% of adjudicated submissions were by-design — meaning the LLM-derived contract was stricter than maintainer intent — is compelling. The formalization (C_LLM vs. C_true, with the judge sharing the generator's bias) is clear. This is the kind of observation that, once made, seems obvious in retrospect — the mark of a good contribution.

3. **S3: The controlled retrospective is the paper's evidentiary backbone and is well-executed.** Same 52-candidate population, blind re-triage, label-isolated agents, two conditions. The 31% to 81% FP-suppression lift at 96.7% TP retention is a clean result that directly answers the central question: does the dev-reviewer add value beyond single-layer LLM judgment? The answer is a clear yes.

4. **S4: The evaluation is unusually honest and self-critical for an LLM-driven testing paper.** The schema-fuzzer baseline concedes boundary-finding effectiveness; the three-anchor design admits the threat-model is noisy and the reproduction anchor is unevaluated; the cross-system claim is qualified to Milvus and Qdrant; the sensitivity interval [43.9%, 80.5%] bounds precision honestly; the 29 excluded submissions are disclosed rather than hidden. This level of transparency is rare and praiseworthy.

5. **S5: The model-free invariant oracle subclass is elegant.** COSINE distance >1.0 for identical vectors is a hard mathematical violation. The fact that it reproduces on both Milvus and Qdrant, is language- and LLM-independent, and generalizes to other invariants (incomplete index results, payload filter violations) makes this the most transferable contribution. I would like to see this subclass elevated further — it is arguably the paper's most important technical insight.

### Weaknesses

1. <span style="color:#d97706">**[Minor]**</span> **The model-free invariant oracle subclass deserves more prominence.** Currently, it appears in Section 5.2 as a paragraph under RQ2. Given that this is the paper's most defensible, language-independent, and transferable finding, it could anchor its own subsection or even be highlighted in the abstract. The abstract mentions "TestVDB targets boundary/validation compliance" but does not mention the invariant oracle subclass. A sentence like "A model-free invariant oracle subclass (e.g., COSINE distance bounded in [-1,1]) surfaces hard mathematical violations without LLM judgment" would strengthen the abstract's technical contribution.

2. <span style="color:#d97706">**[Minor]**</span> **The discovery-recall pilot findings are interesting but buried.** The two held-out bug pilots reveal important system boundaries: the spec-completeness limit (qdrant dimension-mismatch silent-drop is invisible to a spec-derived contract) and the version-pinning limit (milvus cosine>1.0 was fixed before the release version). These are more than limitations — they are design insights about when TestVDB works and when it does not. They currently appear late in Section 5.3 and could be elevated to inform the reader's understanding of the system's applicability conditions.

3. <span style="color:#d97706">**[Minor]**</span> **The paper does not fully exploit the contract hallucination propagation insight's generality.** Section 4 characterizes the phenomenon well, but the conclusion only briefly mentions that it "generalizes beyond VDBMSs — any system where one LLM family both extracts a spec and checks compliance is susceptible." This is a strong claim with broad implications for the LLM-driven testing field. A paragraph or two in the conclusion sketching the implications for REST API testing, configuration validation, or policy compliance checking would strengthen the paper's impact narrative.

4. <span style="color:#d97706">**[Minor]**</span> **Minor bibliography issues for camera-ready.** The foREST entry uses initials rather than full author names. Several entries still carry VERIFY comments. The buzzbee24 entry uses "and others." These are easily fixable but should be addressed before submission.

5. <span style="color:#6b7280">**[Optional]**</span> **A summary figure showing the precision chain would help readers.** The paper reports many precision figures across different arms and tiers: 25.5%, 16.7%, 37%/71%, 75%, 91%, 45.6%, 69.2%, [43.9%, 80.5%]. A visual summary (e.g., a horizontal bar chart with CI whiskers, grouped by truth tier) would make the comparative picture immediately clear without requiring the reader to parse Table 4 and the surrounding text.

### Questions for Authors

- **Q1:** Have you considered making the model-free invariant oracle subclass a named contribution in the abstract and introduction? I believe it is the paper's most transferable insight and deserves more prominence than a paragraph in RQ2.

- **Q2:** The contract hallucination propagation insight has clear implications for any LLM-driven testing pipeline. Do you plan to study this phenomenon in other domains (REST API testing, configuration validation) to establish its generality beyond VDBMSs?

- **Q3:** For the discovery-recall pilot, the spec-completeness limit is particularly interesting: if the contract does not cover a behavior, TestVDB cannot detect its violation. Do you have thoughts on hybrid approaches that combine spec-derived contracts with model-free invariants to expand coverage? This seems like the natural next step.

---

## Verification

| # | Source | Claim | Verdict | Note |
|---|--------|-------|---------|------|
| 1 | R1-W1 | "End-to-end discovery recall remains unmeasured" | <span style="color:#16a34a">**Valid**</span> | Paper reports 96.7% judgment-layer TP retention and 67% upstream extraction coverage; Section 5.3 explicitly states full discovery recall is "future work." The gap is real and acknowledged. |
| 2 | R1-W2 | "Threat-model anchor evaluation underpowered (n=12)" | <span style="color:#16a34a">**Valid**</span> | Section 5.4 reports n=12 Milvus FPs with instability noted. Paper acknowledges "we do not claim the three-anchor design as a clean validated contribution on the strength of n=12." |
| 3 | R1-W3 | "Single-layer 45.6% mixes ground truths" | <span style="color:#16a34a">**Valid**</span> | Section 5.3 and 5.5 both acknowledge this. The 27 suppressed are all live-reprobed (27/27), but the paper notes "the residual gap is that maintainer triage might reclassify a few." |
| 4 | R1-W4 | "Single-layer counterfactual paragraph is dense" | <span style="color:#16a34a">**Valid**</span> | The paragraph in Section 5.3 is approximately 15 lines of continuous text covering the A1 experiment, 27 live-reprobes, five FP classes, 45.6% derivation, and caveats. |
| 5 | R1-W5 | "Bibliography VERIFY entries incomplete" | <span style="color:#16a34a">**Valid**</span> | references.bib has VERIFY comments on 8+ entries. Several use "and others" or initials. FoREST authors are initials-only. |
| 6 | R2-W1 | "End-to-end discovery recall not established" | <span style="color:#16a34a">**Valid**</span> | Same as R1-W1. Paper is explicit about this gap. |
| 7 | R2-W2 | "Baseline ground-truth asymmetry persists" | <span style="color:#16a34a">**Valid**</span> | Table 4 groups by truth tier but the paper acknowledges rows are not directly comparable. The 45.6%, 25.5%, 16.7%, and 37%/71% figures use different denominators and truth sources. |
| 8 | R2-W3 | "Three-anchor design carries more weight than validation supports" | <span style="color:#d97706">**Misleading**</span> | Section 3.4 presents three anchors as a framework, but the paper already scopes this in multiple places: Abstract ("source is the validated primary anchor, threat-model a noisy complement, reproduction future work"), Contribution 2, Section 5.3 anchor attribution, and Figure 1 caption. The presentation is nearly as qualified as it can be. A reader who skims might misread, but the qualifications are there. |
| 9 | R2-W4 | "29 excluded submissions warrant more analysis" | <span style="color:#16a34a">**Valid**</span> | The paper notes 17/29 excluded are Milvus and acknowledges this "may reflect maintainer non-engagement." A sensitivity analysis treating them as FP would complete the picture. |
| 10 | R2-W5 | "Contract counterfactual (DeepSeek) underpowered (N=3)" | <span style="color:#16a34a">**Valid**</span> | Paper labels it "directional" and "N=3." The conclusion "largely task-intrinsic" rests on 2/3 cases. A larger sample would strengthen it. |
| 11 | R3-W1 | "Model-free invariant oracle subclass deserves more prominence" | <span style="color:#16a34a">**Valid**</span> | Currently a paragraph in Section 5.2 (RQ2). The abstract does not mention it. Given its LLM-independence and cross-vendor reproducibility, it could be elevated. |
| 12 | R3-W2 | "Discovery-recall pilot findings are buried" | <span style="color:#16a34a">**Valid**</span> | The spec-completeness and version-pinning limits appear late in a dense Section 5.3 paragraph. These are design insights that could be foregrounded. |
| 13 | R3-W3 | "Contract hallucination generality not fully exploited" | <span style="color:#16a34a">**Valid**</span> | The conclusion mentions generality in one sentence. Broader implications for LLM-driven testing beyond VDBMSs could be developed. |
| 14 | R3-W5 | "Summary figure would help readers" | <span style="color:#6b7280">**Optional**</span> | Table 4 exists and is well-designed. A visual summary would complement it but is not essential. |

---

## Action Plan

<span style="color:#dc2626">**Must Fix**</span> — issues that could lower reviewer confidence or affect acceptance

- [ ] **Clean up bibliography before submission.** Complete full author names for foREST (initials-only currently), expand "and others" entries (buzzbee24, lyu2023miner, chen2024dyner, manes21, ji23hall, wang22sc), and resolve all VERIFY comments. This is mechanical but a sloppy bibliography is a red flag for camera-ready. (R1-W5)

- [ ] **Add a sensitivity analysis for the 29 excluded submissions.** The paper already reports sensitivity for the 30 pending [43.9%, 80.5%]. Adding a parallel treatment for the 29 excluded (particularly the 17 Milvus excluded) would close a remaining uncertainty. Even a simple statement: "If all 29 excluded were true FPs, aggregate precision would drop to X%; if all were duplicate TPs, it would rise to Y%." (R2-W4)

<span style="color:#d97706">**Should Fix**</span> — improvements that strengthen the paper's impact and readability

- [ ] **Elevate the model-free invariant oracle subclass.** Currently buried in RQ2. Consider: (a) adding a sentence to the abstract ("A model-free invariant oracle subclass surfaces hard mathematical violations without LLM judgment"), (b) giving it a dedicated subsubsection in the evaluation, (c) referencing it in the contributions list. This is the paper's most transferable and least contingent finding. (R3-W1)

- [ ] **Split the dense single-layer counterfactual paragraph.** The current paragraph in Section 5.3 (~15 lines) packs the A1 experiment, 27 live-reprobes, five FP classes, 45.6% derivation, and caveats. Breaking it into labeled sub-paragraphs (e.g., "A1: Single-layer arm", "Live re-probe of suppressed candidates", "End-to-end precision comparison") would improve readability. (R1-W4)

- [ ] **Foreground the discovery-recall pilot's design insights.** The spec-completeness limit and version-pinning limit are more than limitations — they are lessons about when TestVDB works. Consider a dedicated paragraph: "When TestVDB applies and when it does not." (R3-W2)

- [ ] **Front-load the three-anchor scoping into Section 3.4.** Currently the qualifications appear in the abstract, contributions, and evaluation, but Section 3.4 still reads as a three-anchor framework without scoping. Adding one sentence: "Of these, we validate the source anchor in the controlled retrospective (Section 5.3); the threat-model anchor is ablated as a noisy complement in Section 5.4; the reproduction anchor remains design-level future work." (R2-W3)

- [ ] **Develop the contract hallucination propagation insight's generality in the conclusion.** The current one-sentence mention could be expanded to a paragraph sketching implications for REST API testing, configuration validation, and policy compliance — any domain where LLMs might both extract a spec and check compliance. (R3-W3)

<span style="color:#6b7280">**Optional**</span> — nice-to-have improvements

- [ ] **Expand the DeepSeek counterfactual from N=3 to N=10+.** The paper labels it "directional" and "N=3," which is honest. A larger sample would make the "largely task-intrinsic" claim stronger. Can be done without additional experiments by selecting more over-strict constraints from the 12 by-design cases. (R2-W5)

- [ ] **Add a visual precision-chain summary figure.** A horizontal bar chart with CI whiskers, grouped by truth tier, showing all the precision figures (25.5%, 16.7%, 37%/71%, 75%, 91%, 45.6%, 69.2%) would make the comparative picture immediately clear. (R3-W5)

- [ ] **Scale up the single-LLM+source ablation from n=12 to n>=30.** The current CI [2.1%, 48.4%] is too wide to be informative. This would strengthen the multi-agent-debate necessity claim. (R2-Q3, R2-W2)

---

## Meta-Review

### Criterion Consensus

| Criterion | R1 (Objective) | R2 (Strict) | R3 (Favorable) | Meta |
|---|---|---|---|---|
| Significance | Adequate (3/4) | Adequate (3/4) | Adequate (4/4) | **Adequate** |
| Novelty | Adequate (3/4) | Adequate (3/4) | Adequate (3/4) | **Adequate** |
| Soundness | Adequate (3/4) | Weak (2/4) | Adequate (3/4) | **Adequate (by majority)** |
| Presentation | Adequate (3/4) | Adequate (3/4) | Adequate (3/4) | **Adequate** |
| **Overall** | **Weak Accept (6/10)** | **Borderline (5/10)** | **Weak Accept (7/10)** | **ACCEPT** |

### Meta Recommendation
**ACCEPT**

This paper has been through 15 rounds of revision and it shows. The current version is mature, honest, and well-qualified. The contribution is real: Contract-Truth Separation addresses a genuine failure mode in LLM-driven testing (contract hallucination propagation, 25% by-design rate), and the controlled retrospective (31% to 81% FP suppression at 96.7% TP retention) provides clean evidence for the dev-reviewer's value. The model-free invariant oracle subclass (COSINE>1.0) is the paper's most transferable insight.

R2's Soundness at Weak (2/4) is the only criterion below Adequate, and it reflects genuine concerns about end-to-end discovery recall remaining unmeasured and baseline ground-truth asymmetry. However, these are acknowledged limitations that the paper honestly scopes — they are not hidden flaws. The majority (R1 and R3) rate Soundness Adequate, so the consensus holds.

Compared with Rounds 14 and 15 (both ACCEPT), the paper's fundamentals are unchanged. The remaining issues (bibliography cleanup, excluded-submission sensitivity, invariant-oracle prominence, paragraph density) are all <span style="color:#d97706">Should Fix</span> or <span style="color:#6b7280">Optional</span>. None requires new experiments. The "Must Fix" items are mechanical (bibliography) and one additional sensitivity analysis (excluded submissions) that can be done with existing data.

**Bottom line:** The paper clears the Accept bar on the strength of its controlled retrospective, the contract hallucination propagation insight, the model-free invariant oracle subclass, and its unusual level of evaluative honesty. The remaining issues are presentation refinements that strengthen an already-solid paper.

### Comparison with Historical Rounds

Compared to Round 15 (also ACCEPT, unanimous WA, Novelty unanimous Adequate), this review finds:
- **Same overall verdict (ACCEPT)** with the same score distribution (R1 WA, R2 Borderline/WA, R3 WA)
- **Novelty remains unanimous Adequate** — the contract hallucination propagation + CTS + invariant oracle subclass continue to be sufficient
- **Soundness is majority Adequate** (R2 at Weak is consistent with historical R2 positioning; Round 15 R2 was also the most critical)
- **The four new references** (foREST, MINER, DynER, LlamaRestTest) adequately address the Related Work gap identified in Round 15
- **New action items** (bibliography cleanup, excluded-submission sensitivity, invariant-oracle prominence) are refinements rather than structural issues
- **No new experimental demands** — the paper's evidence base is stable and sufficient

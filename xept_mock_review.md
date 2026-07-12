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

---
---

# Independent Mock Review (Round 16)
> **Target Venue:** Top-tier SE/DB conference (ICSE / FSE / VLDB) &middot; **Overall Prediction:** Borderline (Weak Accept / Weak Reject) &middot; **Date:** 2026-07-12
> **Note:** This is an independent re-review with a more critical lens than Rounds 14-15. The previous rounds gave ACCEPT (unanimous WA); this round downgrades Presentation and Soundness based on persistent readability and marginal-value concerns.

---

## Score Summary

| Dimension | R1 (Objective) | R2 (Strict) | R3 (Favorable) |
|-----------|:---------:|:---------:|:---------:|
| Significance | 3/4 | 3/4 | 4/4 |
| Novelty | 3/4 | 2/4 | 3/4 |
| Soundness | 2/4 | 2/4 | 3/4 |
| Presentation | 2/4 | 1/4 | 2/4 |
| Overall | 5/10 | 4/10 | 6/10 |

---

## Core Issues (Cross-Reviewer Consensus)

### Consensus Issue 1: Readability Is Severely Lacking
All three reviewers flag this. Specific evidence:
- **Abstract:** ~200 words with 15+ numeric values and inline caveats ("validated on Milvus and Qdrant; Weaviate, MeiliSearch, and Chroma serve as breadth probes..."). Cannot be parsed in one reading.
- **Section 5.3 (RQ3):** ~1500 words of continuous text with 9 `\paragraph` pseudo-sections, each packing multiple experiments, sensitivity analyses, and cross-references into 200+ word blocks.
- **Threats to Validity:** ~450 words covering 9 distinct threat categories in a single undivided block.
- **Sentence length:** Multiple sentences exceed 50-60 words with nested parenthetical qualifications.

### Consensus Issue 2: Marginal Value of the LLM Pipeline Is Unclear
- 75% of acknowledged bugs (27/36) are boundary/validation.
- The paper concedes a hand-written spec fuzzer (19 probes, no LLM) achieves 71% source-grounded precision on the same target.
- Only ~6 TPs are exclusive to the LLM pipeline (after removing boundary and model-free invariant cases).
- No cost-effectiveness analysis (~10^7 tokens/target vs. manual testing effort).

### Consensus Issue 3: Ground-Truth Inconsistency in Evaluation
Table 4 groups arms by truth tier (LLM self-judgment / API-acceptance / blind re-triage / maintainer adjudication), but the surrounding text draws cross-tier directional conclusions ("Both arms remain far below TestVDB's 69.2%") that violate the paper's own caveat that "rows are not directly comparable across tiers."

---

## Reviewer 1 -- Objective Reviewer
> Confidence: 4/5

### Summary

TestVDB targets API compliance defects in VDBMSs -- non-crash bugs where the system silently accepts inputs or behaviors violating its documented contract. The paper introduces Contract-Truth Separation (CTS), separating LLM-generated contract assertions from a truth layer that falsifies them via maintainer-authority evidence. The system produced 111 issues across five VDBMSs; maintainers acknowledged 36 (28 fixed). A controlled retrospective over 52 adjudicated candidates shows the dev-reviewer's source anchor lifts FP suppression from 31% to 81% while retaining 96.7% of true positives.

The paper attacks a real gap and delivers real bugs. The contract hallucination propagation observation is a genuine insight. However, the paper suffers from severe presentation density, an evaluation that conflates multiple ground truths, and a cost-effectiveness gap: 75% of yield consists of boundary/validation bugs that a hand-written spec fuzzer can find at a fraction of the cost.

### Strengths

1. **S1: Well-motivated problem with real-world validation.** 36 maintainer-acknowledged bugs (28 fixed) across production VDBMSs is concrete evidence. The bug taxonomy grounding (43% incorrect-behavior vs. 23% crash/hang) effectively motivates why crash-focused fuzzers are insufficient.

2. **S2: Contract hallucination propagation is a transferable insight.** The observation that LLMs self-confirm hallucinated constraints when the same model family generates and judges is simple, well-evidenced (12 by-design cases, 25% of adjudicated), and applies beyond VDBMSs.

3. **S3: The controlled retrospective is the cleanest empirical evidence.** Same 52-candidate population, blind re-triage, two conditions. The 31% to 81% FP-suppression lift directly isolates the dev-reviewer's contribution.

4. **S4: Model-free invariant oracle subclass is the most defensible contribution.** COSINE distance >1.0 for identical vectors, incomplete index results, payload filter violations. These violate hard mathematical or logical bounds, need no LLM judgment, reproduce across vendors, and are adoptable independently.

5. **S5: Unusually honest scoping.** The paper qualifies almost every claim with appropriate caveats, reports sensitivity intervals, and concedes the schema-fuzzer overlap. Commendable transparency.

### Weaknesses

1. <span style="color:#dc2626">**[Major]**</span> **The paper is extremely difficult to read.** The abstract alone contains ~200 words with 15+ numeric values and reads like a compressed results section. Section 5.3 (RQ3) is a wall of text with `\paragraph` breaks as pseudo-subsections, each paragraph often exceeding 200 words of continuous, parenthetically-qualified prose. The Threats to Validity section is ~450 words of continuous text that reads more like a preemptive rebuttal. A reviewer who cannot follow the argument will not champion the paper.

2. <span style="color:#dc2626">**[Major]**</span> **75% of acknowledged bugs are boundary/validation, which a simple spec fuzzer can find.** The paper concedes this: a hand-written boundary fuzzer with 19 probes achieved 5/7 = 71% source-grounded precision. The remaining 25% of yield (9 TPs: 3 diagnostic, 2 state/logic, 1 crash, 3 result-correctness) is the only slice where the full 20-agent LLM pipeline demonstrates unique value. For ~10^4 LLM calls and ~10^7 tokens per target, the marginal value over boundary fuzzing is thin. No cost-effectiveness analysis is provided.

3. <span style="color:#dc2626">**[Major]**</span> **End-to-end discovery recall is unmeasured, and pilots suggest fundamental limits.** The 96.7% figure is judgment-layer TP retention, not discovery recall. The two held-out-bug pilots reveal structural ceilings: the qdrant dimension-mismatch bug is invisible because the spec does not describe it (spec-completeness limit), and the milvus cosine>1.0 bug was fixed before the release version (version-pinning limit). These are not just limitations -- they suggest TestVDB's practical recall on unknown bugs may be fundamentally constrained.

4. <span style="color:#dc2626">**[Major]**</span> **The "5 VDBMSs" framing overstates cross-system evidence.** Milvus contributes 22 acknowledged bugs, Qdrant 11. Together: 33/36 = 92%. MeiliSearch (0), Chroma (0), and Weaviate (3 fixed, 21 still pending) provide negligible signal. The breadth-probe qualification is present but insufficient: claiming "5 VDBMSs" in the abstract and contributions while 92% of evidence comes from two systems is misleading.

5. <span style="color:#d97706">**[Minor]**</span> **The Contributions list is overloaded.** Five contributions with sub-clauses and parenthetical statistics. Contribution 2 alone is ~100 words. A reader cannot quickly grasp the claims.

6. <span style="color:#d97706">**[Minor]**</span> **The controlled retrospective is on the development population.** The 52 candidates were produced by TestVDB during iterative development. Re-running "blind" on the same population does not fully control for the system having been tuned to perform well on exactly these cases.

### Questions for Authors

- **Q1:** What is the actual dollar cost per pipeline run? How does this compare to a human tester spending one day on boundary testing of the same API?

- **Q2:** Of the 9 non-boundary TPs, how many could a competent human tester have found from reading the same documentation?

- **Q3:** Have you considered a prospective evaluation on a fresh (sixth) VDBMS not used during development?

---

## Reviewer 2 -- Strict Reviewer
> Confidence: 4/5

### Summary

This paper presents TestVDB, a multi-agent LLM system for detecting API compliance defects in vector databases. The core mechanism, Contract-Truth Separation (CTS), uses a dev-reviewer agent to falsify LLM-generated contract assertions against maintainer-authority evidence. Results: 111 issues filed, 36 acknowledged (28 fixed), controlled retrospective showing source anchor lifts FP suppression from 31% to 81%.

I see a genuine problem identification and a real engineering contribution. But the paper has fundamental issues. The evaluation conflates multiple incompatible ground truths. The practical marginal value over simple spec fuzzing is unclear for 75% of the yield. The writing quality is below the bar: the evaluation is impenetrably dense, the abstract is overloaded, and the threats section is a defensive wall. The paper reads as if it has been revised many times to address every possible objection, and in doing so has lost clarity of narrative.

### Strengths

1. **S1: Contract hallucination propagation is the paper's most interesting contribution.** Clean observation, concrete evidence (12 by-design cases, 25%), simple formalization. This alone could justify a publication if presented clearly.

2. **S2: Model-free invariant oracle subclass is technically sound.** COSINE bounded in [-1,1] is a mathematical fact. Violations are unambiguous, LLM-independent, cross-vendor, reproducible.

3. **S3: 28 bugs fixed across production VDBMSs.** Not toy targets. Real practical impact.

4. **S4: Controlled retrospective methodology is well-designed.** Blind re-triage, label-isolated agents, same population.

### Weaknesses

1. <span style="color:#dc2626">**[Major]**</span> **The evaluation conflates incompatible ground truths.** Table 4 groups by "truth tier," but the paper draws cross-tier conclusions that are not valid. Single-LLM (25.5%) uses LLM self-judgment; schema fuzzer (37%) uses API-acceptance; retrospective (75%, 91%) uses blind re-triage; end-to-end (69.2%) uses maintainer adjudication. These numbers cannot establish TestVDB's superiority because they measure different things. The only valid comparison is the retrospective tier (75% vs. 91%), and even that uses slightly different TP denominators (36 vs. 30).

2. <span style="color:#dc2626">**[Major]**</span> **Writing quality is below the bar for a top venue.** (a) Abstract: ~200 words, 15+ numbers, multiple inline caveats. (b) Section 5.3: ~1500 words in a continuous block with `\paragraph` pseudo-sections. (c) Threats to Validity: ~450 words, 9 threat categories in one undivided block. (d) Sentences routinely exceed 50 words with nested parentheticals. These are readability barriers that make the arguments hard to evaluate.

3. <span style="color:#dc2626">**[Major]**</span> **Marginal value of LLM pipeline over spec fuzzing is not justified.** 27/36 TPs are boundary/validation. A hand-written fuzzer finds 5 genuine violations at 71% precision. The model-free invariant cases (3 TPs) need no LLM. This leaves ~6 TPs as the exclusive domain of the 20-agent pipeline. For ~10^7 tokens per target, finding 6 bugs a simpler tool cannot is a weak value proposition.

4. <span style="color:#dc2626">**[Major]**</span> **GLM-5.2 monoculture raises generalizability concerns.** All 20 agents use GLM-5.2. The DeepSeek counterfactual covers only contract generation (N=10), not the full pipeline. Would CTS still be necessary with a model that hallucinates less?

5. <span style="color:#d97706">**[Minor]**</span> **20-agent architecture lacks design rationale.** Why 4 judges instead of 3 or 5? Why separate boundary/semantic/state agents? No component-level ablation. "Full prompts in the artifact" does not substitute for in-paper justification.

6. <span style="color:#d97706">**[Minor]**</span> **Bibliography has incomplete entries.** Multiple "and others," initials-only names, VERIFY comments. Placeholder ACM metadata.

7. <span style="color:#d97706">**[Minor]**</span> **Template mismatch.** ACM sigconf template but filename indicates VLDB target.

### Questions for Authors

- **Q1:** If you remove boundary/validation TPs and model-free invariant TPs, how many unique bugs does the LLM pipeline contribute? Is ~6 bugs sufficient to justify 20 agents and ~10^7 tokens?

- **Q2:** Have you tried replacing GLM-5.2 with a different model family for the entire pipeline?

- **Q3:** The text mentions both "Claude Code runtime" and "GLM-5.2 backbone." Please clarify: is Claude Code the orchestration framework and GLM-5.2 the model backend?

- **Q4:** The Threats section mentions possible pre-training contamination with Milvus source code. The memorization canary tests recall of specific issues. How do you rule out that the source anchor's effectiveness comes partly from pre-training familiarity with Milvus's codebase patterns?

---

## Reviewer 3 -- Favorable Reviewer
> Confidence: 3/5

### Summary

TestVDB addresses a genuine gap: 43% of VDBMS bugs are incorrect-behavior, but existing tools only detect crashes. The paper introduces API compliance defects as a tractable formulation, proposes Contract-Truth Separation to address LLM oracle unreliability, and delivers 36 maintainer-acknowledged bugs (28 fixed). The controlled retrospective cleanly demonstrates the dev-reviewer's value. The contract hallucination propagation observation and model-free invariant oracle subclass are both transferable insights.

The paper's main weakness is presentation: it reads as if every possible objection has been preemptively addressed, resulting in text that is thorough but exhausting. Despite this, the paper makes genuine contributions to an important problem.

### Strengths

1. **S1: The problem formulation is excellent.** API compliance defects as a tractable slice, with the API contract as the oracle. The exclusion table (Table 1) concisely justifies why an LLM is the only viable candidate.

2. **S2: Real-world impact is demonstrated.** 28 bugs fixed. The case studies (nprobe=0, empty filter, get_stats) trace the system's reasoning end-to-end.

3. **S3: Contract hallucination propagation is broadly applicable.** Simple, well-evidenced, relevant beyond VDBMSs to any LLM-driven spec-checking pipeline.

4. **S4: Model-free invariant oracle subclass is elegant and independently valuable.** No LLM needed, cross-vendor, hard mathematical bounds. This is the paper's strongest technical finding.

5. **S5: Controlled retrospective is rigorous.** Blind conditions, label-isolated agents, same population. The 2.6x FP-suppression lift is clean.

### Weaknesses

1. <span style="color:#dc2626">**[Major]**</span> **Presentation density undermines the paper's strengths.** Each revision round has added qualifications rather than clarity. Concrete recommendations: (a) Cut abstract to 150 words with at most 5 key numbers. (b) Break Section 5.3 into proper subsections. (c) Split Threats into labeled sub-paragraphs. (d) Consider moving some sensitivity/ablation details to an appendix.

2. <span style="color:#d97706">**[Minor]**</span> **Model-free invariant oracle subclass deserves much more prominence.** Currently a paragraph in RQ2. Should anchor its own subsection, appear in the abstract, and be discussed in the conclusion as the starting point for future invariant-based VDBMS oracles.

3. <span style="color:#d97706">**[Minor]**</span> **System contributions vs. empirical observations are not clearly separated.** CTS is a system contribution. Contract hallucination is an observation. The 36 bugs are practical impact. Mixing them in the contributions list makes it harder to evaluate what is being claimed.

4. <span style="color:#d97706">**[Minor]**</span> **Cost-effectiveness is not discussed.** For practical adoption, knowing cost per bug matters. ~10^4 LLM calls and ~10^7 tokens per target is stated but not translated to dollars or compared with manual effort.

5. <span style="color:#6b7280">**[Optional]**</span> **DeepSeek counterfactual could be expanded.** N=3 original + N=10 expanded is directional but thin. Testing 2-3 model families on all 12 by-design cases would strengthen the "predominantly model-specific" conclusion.

### Questions for Authors

- **Q1:** Could you provide a "one-paragraph elevator pitch" for TestVDB that a non-specialist PC member could understand?

- **Q2:** For the model-free invariant oracle subclass, do you have a catalog of all identified invariants? A table of (invariant, VDBMSs where violated, evidence) would be a valuable standalone artifact.

- **Q3:** What would a "TestVDB Lite" look like: model-free invariant oracles + spec-driven boundary fuzzer + source-grounded filter, without the full 20-agent pipeline? Would this capture 80% of the value at 10% of the cost?

---

## Verification

| # | Source | Claim | Verdict | Note |
|---|--------|-------|---------|------|
| 1 | R1-W2 | "75% of yield is boundary/validation" | <span style="color:#16a34a">**Valid**</span> | Section 5.1: "27 (75%) are boundary/validation." Schema fuzzer achieves 71% precision on the same target. Paper concedes: "a spec-driven fuzzer is genuinely effective." |
| 2 | R1-W4 | "92% of acknowledged bugs from Milvus+Qdrant" | <span style="color:#16a34a">**Valid**</span> | Table 2: Milvus 22 + Qdrant 11 = 33/36 = 91.7%. |
| 3 | R2-W1 | "Cross-tier comparisons not valid" | <span style="color:#d97706">**Misleading**</span> | Paper warns "not directly comparable" and groups with midrules, but still draws cross-tier directional conclusions in the text. Partially valid. |
| 4 | R2-W3 | "Only ~6 TPs exclusive to LLM pipeline" | <span style="color:#d97706">**Misleading**</span> | Arithmetic correct (36-27-3=6), but ignores that the LLM pipeline found boundary bugs first (the fuzzer rediscovered them), and CTS FP-suppression applies across all categories. Directionally fair but oversimplified. |
| 5 | R2-Q3 | "Claude Code vs GLM-5.2 confusion" | <span style="color:#16a34a">**Valid**</span> | Paper mentions both "served by GLM-5.2" and "Claude Code runtime's default sampling configuration" without explaining the relationship. |
| 6 | R3-W4 | "Cost-effectiveness not discussed" | <span style="color:#16a34a">**Valid**</span> | Paper states ~10^4 calls, ~10^7 tokens but provides no dollar cost or comparison to manual testing. |

---

## Action Plan

<span style="color:#dc2626">**Must Fix**</span> -- not fixing risks rejection

- [ ] **Rewrite the abstract (~150 words, at most 5 key numbers).** Remove all inline caveats and breadth-probe qualifications. Core message: problem, method, main result. Save qualifications for the body.
- [ ] **Restructure Section 5.3 (RQ3) into proper subsections.** Replace 9 `\paragraph` blocks with: (a) Controlled Retrospective, (b) Aggregate Precision, (c) Sensitivity Analysis, (d) Baseline Comparisons (single-layer, single-LLM, schema-fuzzer as sub-paragraphs), (e) Anchor Attribution. Each self-contained and scannable.
- [ ] **Trim Contributions list from 5 to 3.** Each 1-2 sentences max. Suggested: (1) First VDBMS API compliance defect detection system + empirical study, (2) Contract-Truth Separation design principle, (3) Model-free invariant oracle subclass. Move contract hallucination observation and threat-model details into the body.
- [ ] **Split Threats to Validity into labeled sub-paragraphs.** Internal / Selection / External / Construct / LLM Variance / Contamination / Excluded Set.
- [ ] **Complete bibliography.** Full author names, resolve VERIFY comments, fix template metadata.

<span style="color:#d97706">**Should Fix**</span> -- significantly improves competitiveness

- [ ] **Add cost-effectiveness analysis.** Dollar cost per pipeline run, comparison to "human tester + spec fuzzer" baseline.
- [ ] **Elevate model-free invariant oracle.** Dedicated subsection, invariant catalog table, mention in abstract.
- [ ] **Articulate LLM pipeline marginal value clearly.** Acknowledge 75% overlap, then quantify three unique sources: (a) non-boundary bugs, (b) CTS FP-suppression across categories, (c) spec-gap detection.
- [ ] **Clarify Claude Code vs GLM-5.2 relationship.**
- [ ] **Front-load three-anchor scoping into Section 3.4.**

<span style="color:#6b7280">**Optional**</span> -- nice-to-have

- [ ] Prospective evaluation on a fresh (sixth) VDBMS
- [ ] Cross-model full-pipeline evaluation (GPT-4 or Claude replacing GLM-5.2)
- [ ] Expand DeepSeek counterfactual to all 12 by-design cases
- [ ] Design "TestVDB Lite" (invariants + spec fuzzer + source filter) and compare cost/effectiveness

---

## Meta-Review

### Criterion Consensus

| Criterion | R1 (Objective) | R2 (Strict) | R3 (Favorable) | Meta |
|---|---|---|---|---|
| Significance | Adequate (3/4) | Adequate (3/4) | Strong (4/4) | **Adequate** |
| Novelty | Adequate (3/4) | Weak (2/4) | Adequate (3/4) | **Adequate (by majority)** |
| Soundness | Weak (2/4) | Weak (2/4) | Adequate (3/4) | **Weak (by majority)** |
| Presentation | Weak (2/4) | Poor (1/4) | Weak (2/4) | **Weak** |
| **Overall** | **Borderline (5/10)** | **Weak Reject (4/10)** | **Weak Accept (6/10)** | **BORDERLINE** |

### Meta Recommendation
**BORDERLINE (Weak Accept / Weak Reject)**

The paper's technical foundations are sound: CTS addresses a real failure mode, contract hallucination propagation is a valuable observation, model-free invariant oracle is a clean contribution, and 36 real bugs demonstrate practical impact.

Two issues prevent a clear Accept:

**1. Presentation is a major barrier.** All three reviewers flag this. The paper has absorbed extensive revision feedback, but each round added qualifications rather than clarity. The net effect is thorough and honest but exhausting. A paper that cannot be understood will not be championed.

**2. Marginal value of the LLM pipeline is unclear.** 75% of yield overlaps with spec fuzzing. Model-free invariants need no LLM. The remaining ~6 unique bugs at ~10^7 tokens per target face a cost-effectiveness challenge the paper does not address.

**Path to acceptance:** No new experiments needed. Focus on: (a) presentation overhaul (rewrite abstract, restructure evaluation, trim contributions), (b) cost-effectiveness analysis, (c) clearer marginal-value articulation. These are writing tasks. Completing them should move this to Accept.

### Comparison with Historical Rounds (14-15)

This round diverges from Rounds 14-15 (both ACCEPT, unanimous WA) on two dimensions:
- **Presentation**: Rounds 14-15 rated Presentation as Adequate (3/4). This round downgrades to Weak/Poor (1-2/4). The difference: I weigh readability as a gating factor for acceptance at a top venue. A paper this dense will lose reviewers under time pressure.
- **Soundness**: Rounds 14-15 rated Soundness as majority Adequate. This round downgrades to majority Weak (2/4). The difference: I give more weight to the marginal-value gap (75% overlap with spec fuzzing) and the unmeasured discovery recall, treating them as substantive rather than acknowledged-and-therefore-mitigated limitations.
- **Technical content is unchanged**: the same experiments, same numbers, same contributions. The disagreement is about how much weight presentation quality and marginal-value justification carry in the accept/reject decision.

---
---

# Mock Review Report — Round 17 (post-overhaul re-review)
> **Target Venue:** Top-tier SE/DB conference (ICSE / FSE / VLDB) &middot; **Overall Prediction:** Weak Accept &middot; **Date:** 2026-07-12
> **Context:** Re-review after the author addressed Round 16 must-fixes. This round evaluates the *current* text independently, then diffs against Round 16.

---

## What Changed Since Round 16

Round 16 raised two blockers (presentation, marginal-value justification) and a must-fix list. Verified against the current `.tex`:

| Round 16 Must-Fix | Status | Evidence |
|---|---|---|
| Rewrite abstract (≤ ~150 words, ≤5 numbers) | <span style="color:#d97706">**Partial**</span> | Now ~165 words, 7 numeric tokens (43%, 111, 36, 28, 31%, 81%, 96.7%). Far tighter than the old 15+, but still above target. |
| Trim contributions to 3 | <span style="color:#16a34a">**Done**</span> | Intro enumerate now has exactly 3 items. |
| Restructure Section 5.3 into subsections | <span style="color:#16a34a">**Done**</span> | Five subsubsections: Controlled Retrospective / Aggregate / Sensitivity / Baselines / Anchor Attribution. |
| Split Threats into labeled sub-paragraphs | <span style="color:#16a34a">**Done**</span> | Itemized with bold labels (Internal, Selection, External, Construct, LLM variance, Contamination, Recall scope, Excluded set, Single-layer CF). |
| Add cost-benefit analysis | <span style="color:#16a34a">**Done**</span> | "Reproducibility and cost" paragraph: ~$10/target, ~10^3 calls/target, marginal value stated as threefold. |
| Elevate model-free invariant oracle | <span style="color:#16a34a">**Done**</span> | Now Contribution 3 + dedicated RQ2 paragraph framing it as "most defensible technical finding." |
| Complete bibliography | <span style="color:#dc2626">**Not done**</span> | `references.bib` still carries the "Round 6 additions (VERIFY)" block and "and others" author lists (wang22sc, ji23hall, hou23llmse, manes21, lin2023forest, lyu2023miner, chen2024dyner). |

**Net effect:** Round 16's presentation blocker is substantially resolved; the marginal-value blocker is now *addressed in text* (cost paragraph + Contribution-3 elevation) even if not fully *resolved in evidence*. This moves my recommendation from BORDERLINE to **Weak Accept**.

---

## Score Summary

| Dimension | R1 (Objective) | R2 (Strict) | R3 (Favorable) |
|-----------|:---------:|:---------:|:---------:|
| Significance | 3/4 | 3/4 | 4/4 |
| Novelty | 3/4 | 2/4 | 3/4 |
| Soundness | 3/4 | 2/4 | 3/4 |
| Presentation | 3/4 | 2/4 | 3/4 |
| **Overall** | **6/10** | **5/10** | **7/10** |

Change vs. Round 16: Presentation +1 across the board (structural fixes landed); Soundness R1 +1 (cost/marginal-value now argued). R2 (strict) holds Novelty and Soundness at 2/4 for the reasons below.

---

## Reviewer 1 — Objective Reviewer
> Confidence: 4/5

**Summary.** The revised paper reads markedly better. The contribution list is now three tight claims, the evaluation is navigable by subsection, and a cost paragraph finally quantifies the pipeline's price ($\sim$$10/target) against its threefold marginal value. The two strongest assets are unchanged and remain strong: contract hallucination propagation (25% by-design rate, corroborated by a DeepSeek counterfactual) and the model-free invariant oracle subclass (COSINE>1.0, cross-vendor, no LLM). The honesty scaffolding (sensitivity interval, tiered baseline table, scope caveats) is now paired with enough structure that a reviewer can actually follow it.

**Strengths**
1. The controlled retrospective (52 candidates, blind, same population) cleanly isolates the source anchor: 31%→81% FP suppression at 96.7% TP retention. This is the paper's load-bearing result and it is methodologically sound.
2. The model-free invariant oracle is now first-class (Contribution 3 + RQ2). It is the least model-contingent finding and the most portable.
3. Table 4's tiered grouping (LLM-judged / API-acceptance / retrospective / maintainer-gold) makes cross-arm incomparability explicit instead of hiding it.

**Weaknesses**
1. <span style="color:#dc2626">**[Major]**</span> **End-to-end discovery recall is still unmeasured.** 96.7% is judgment-layer retention. The upstream 67% contract-coverage probe and the 2-bug pilot bound the problem but do not measure recall. After this many rounds, the absence of any recall number is the single largest remaining gap.
2. <span style="color:#d97706">**[Minor]**</span> **Abstract is still above the target density.** 7 numeric tokens in ~165 words. Dropping the 31%/81%/96.7% triple to a single headline number would help a first-pass reader.
3. <span style="color:#d97706">**[Minor]**</span> **Bibliography not camera-ready.** VERIFY block and "and others" author lists remain; foREST uses initials-only names. Cosmetic, but a diligent reviewer will notice.

**Questions**
- Q1: Can you produce even a small (n≈5) end-to-end rediscovery number on version-pinned bug-present images, to replace the retention-vs-recall hedge?

---

## Reviewer 2 — Strict Reviewer
> Confidence: 3/5

**Summary.** Presentation improved; the underlying value proposition did not. The paper now *states* marginal value (cost paragraph, three-fold claim) but the arithmetic still undercuts the LLM pipeline. 75% of yield is boundary/validation, which the authors' own 19-probe spec fuzzer reaches at 71% precision. The model-free invariants need no LLM. What remains uniquely attributable to the full multi-agent + CTS machinery is a handful of state/logic + diagnostic + spec-gap bugs (8/36 TPs by their own count), purchased at ~10^7 tokens in aggregate.

**Weaknesses**
1. <span style="color:#dc2626">**[Major]**</span> **Marginal value is asserted, not demonstrated.** The "threefold" claim (non-boundary yield, FP-suppression, spec-gap) is qualitative. There is no experiment isolating the *incremental* bugs found by the full pipeline that the spec-fuzzer + model-free oracle could not. Until that delta is measured, cost-effectiveness is an unfalsified assertion.
2. <span style="color:#dc2626">**[Major]**</span> **The threat-model anchor still occupies architectural real estate it has not earned.** n=12, unstable (a boundary FP flips between runs), rescued only as a "noisy complement." It is a full node in Figure 1 and a subsection in Section 3 for what is, empirically, a diagnosed negative.
3. <span style="color:#d97706">**[Minor]**</span> **The 45.6% single-layer number still mixes ground truths** (36 maintainer-adjudicated + 27 live-reprobed). Live-confirmation helps, but it is not the maintainer-gold tier it is compared against.

**Questions**
- Q1: Report the incremental-yield delta directly: of 36 TPs, how many are reachable *only* by the full pipeline (not spec-fuzzer, not model-free oracle)? Name them.
- Q2: If the threat anchor is a noisy complement at n=12, why keep it as a co-equal node in Figure 1 rather than a footnote?

---

## Reviewer 3 — Favorable Reviewer
> Confidence: 4/5

**Summary.** This is a mature, honest systems-and-measurement paper on a real and underserved problem. VDBMS incorrect-behavior bugs (43%) lack oracles; TestVDB delivers a working contract oracle, 36 acknowledged real bugs (28 fixed), and a genuinely novel failure-mode characterization (contract hallucination propagation). The revision fixed the readability complaints and added the cost accounting reviewers asked for. The work will be used and cited.

**Strengths**
1. 36 maintainer-acknowledged, 28 fixed bugs in production systems — undeniable practical impact.
2. Contract hallucination propagation is a transferable insight beyond VDBMSs (REST contract testing, policy-as-code). The generalization paragraph in the conclusion lands.
3. The paper is unusually honest: sensitivity intervals, contamination canary (0/9), tiered baselines. This is the kind of rigor reviewers should reward, not punish.

**Weaknesses**
1. <span style="color:#d97706">**[Minor]**</span> Discovery recall unmeasured — but the scope is honestly drawn and future work is explicit.
2. <span style="color:#d97706">**[Minor]**</span> Bibliography VERIFY tags should be cleared for camera-ready.

**Questions**
- Q1: Would you consider promoting the model-free invariant oracle to its own short section? It is your most portable result and currently lives inside RQ2.

---

## Verification

| # | Source | Claim | Verdict | Note |
|---|--------|-------|---------|------|
| 1 | R1 | "Contributions trimmed to 3" | <span style="color:#16a34a">**Valid**</span> | Intro enumerate = 3 items. |
| 2 | R1 | "Section 5.3 restructured" | <span style="color:#16a34a">**Valid**</span> | 5 subsubsections present. |
| 3 | R1 | "Cost paragraph added" | <span style="color:#16a34a">**Valid**</span> | "Reproducibility and cost", ~$10/target. |
| 4 | R1/R3 | "Bibliography still has VERIFY / 'and others'" | <span style="color:#16a34a">**Valid**</span> | `references.bib` L64 + multiple entries. |
| 5 | R1 | "Abstract still >5 numbers" | <span style="color:#16a34a">**Valid**</span> | 7 numeric tokens counted. |
| 6 | R2 | "75% yield reachable by spec fuzzer" | <span style="color:#16a34a">**Valid**</span> | Sec 5.1 (27/36) + Sec 5.3 fuzzer 71% concession. |
| 7 | R2 | "Marginal value asserted, not measured" | <span style="color:#16a34a">**Valid**</span> | Cost paragraph is qualitative; no incremental-delta experiment. |
| 8 | R2 | "Threat anchor n=12, unstable" | <span style="color:#16a34a">**Valid**</span> | Sec 5.4 (RQ4) states exactly this. |
| 9 | R1/R2 | "Discovery recall unmeasured" | <span style="color:#16a34a">**Valid**</span> | 96.7% is retention; recall probe only bounds. |
| 10 | (mine) | "Template mismatch: sigconf acmart vs. PVLDB" | <span style="color:#d97706">**Misleading**</span> | Class is `[sigconf]{acmart}`; if VLDB is the true target, PVLDB uses its own `vldb.cls`, not acmart. Confirm venue before submission. |

---

## Action Plan

<span style="color:#dc2626">**Must Fix**</span> — gating for a clear Accept
- [ ] **Measure the incremental yield delta (R2-Q1).** Of the 36 TPs, list those reachable *only* by the full pipeline (not the 19-probe spec fuzzer, not the model-free oracle). This single table converts the "threefold marginal value" assertion into evidence and neutralizes R2's core objection. No new bug-hunting needed — reclassify existing 36.
- [ ] **Clear the bibliography.** Remove VERIFY tags, expand every "and others" to full author lists, expand foREST initials. Purely mechanical; leaving it signals unfinished work.

<span style="color:#d97706">**Should Fix**</span> — reduces reviewer friction
- [ ] **Tighten the abstract to ≤5 numbers.** Keep 36-acknowledged + 31%→81%; drop the 43%, 111, 28, and 96.7% to the body.
- [ ] **Demote the threat-model anchor in Figure 1** to a dashed/optional node with a one-line caption note, matching its "noisy complement, n=12" status in the text (addresses R2-W2).
- [ ] **Confirm the target venue and fix the template** if it is PVLDB (acmart sigconf ≠ vldb.cls). If the target is truly an ACM sigconf venue, rename the file to stop implying VLDB.

<span style="color:#6b7280">**Optional**</span> — polish
- [ ] Promote the model-free invariant oracle to a short standalone subsection (R3-Q1).
- [ ] Split the single-layer counterfactual paragraph (Sec 5.3) into two sub-paragraphs for readability.

---

## Meta Recommendation: **WEAK ACCEPT**

The overhaul did what Round 16 asked. Presentation is no longer a blocker: the contribution list, evaluation structure, and Threats section are now navigable, and the cost paragraph directly answers the "why pay for the LLM" question at the argument level. The technical core — CTS, contract hallucination propagation, and the model-free invariant oracle — was always sound and is now framed to match its evidence.

One substantive gap keeps this at Weak rather than clear Accept: **marginal value is argued but not measured.** The fastest path to a confident Accept is the incremental-yield table (Must-Fix #1), which requires zero new experiments — only reclassification of the 36 existing TPs. Pair that with a clean bibliography and the paper clears the bar.

### Comparison with Round 16
- **Presentation: Weak/Poor → Adequate.** The structural must-fixes (abstract, contributions, Section 5.3, Threats) all landed. This is the decisive change.
- **Soundness (R1): Weak → Adequate.** The cost paragraph and Contribution-3 elevation address the marginal-value argument enough for the objective reviewer, though the strict reviewer still withholds (evidence vs. assertion).
- **Overall: BORDERLINE → Weak Accept.** Same experiments and numbers as Round 16; the improvement is entirely presentational and rhetorical, which is exactly what Round 16 said was needed.

---
---

# Mock Review Report — Round 19
> **Target Venue:** VLDB / PVLDB &middot; **Overall Prediction:** Accept (borderline) &middot; **Date:** 2026-07-12
> **Revision Context:** Round 18 = Weak Accept, leaning Accept. Since then the last remaining Major (end-to-end discovery recall) was addressed with a held-out rediscovery study (L370, 4/9). Independent re-read of current text.

---

## Score Summary

| Dimension | R1 (Objective) | R2 (Strict) | R3 (Favorable) |
|-----------|:---------:|:---------:|:---------:|
| Significance | 3/4 | 3/4 | 4/4 |
| Novelty | 3/4 | 3/4 | 4/4 |
| Soundness | 3/4 | 2/4 | 3/4 |
| Presentation | 4/4 | 3/4 | 4/4 |
| Overall | 7/10 | 5/10 | 8/10 |

---

## Reviewer 1 — Objective Reviewer
> Confidence: 4/5

### Summary
TestVDB detects API compliance defects in VDBMSs via Contract-Truth Separation (CTS): LLM-generated contract assertions are falsified by a dev-reviewer truth layer grounded in maintainer authority. 111 submissions across five systems, 36 acknowledged (28 fixed). The evidence spine is (a) a same-population retrospective (source anchor lifts FP suppression 31%→81% at 96.7% TP retention), (b) an incremental-yield decomposition isolating 5 TPs reachable only by the full pipeline, and (c) a new held-out rediscovery study (4/9 pre-2024 bugs).

Compared with the prior round, the paper now closes the recall gap that dominated three earlier rounds. The held-out study (L370) converts the single largest evaluation void into a bounded positive number, and the contamination canary (0/9 at issue-specificity) makes the recall claim credibly non-memorized. The paper is now internally complete: every headline number has a scope caveat, and the caveats are honest rather than defensive.

### Strengths
1. **Recall is now measured, not deferred.** The 4/9 held-out rediscovery, with the 0/9 canary and the two named confounds (spec-completeness, version-pinning), turns "future work" into a real, defensible data point.
2. **Marginal value is now decomposed by oracle class (L231).** The "5 TPs reachable only by the full pipeline" plus the cross-category FP-suppression lift (45.6%→69.2%) gives a concrete answer to "what does the LLM buy beyond a spec fuzzer."
3. **Honest scoping throughout.** Cross-system claims restricted to Milvus+Qdrant; threat-model anchor reported as a diagnosed negative; sensitivity band on precision made explicit.

### Weaknesses
1. **[Minor]** The recall number is honest but modest: 4/9 (really 4/7 testable) means the system misses more than half of known compliance bugs. This is fine to report, but the abstract/intro should not let the retrospective's 96.7% overshadow it — a reader skimming will conflate the two.
2. **[Minor]** The 69.2% precision still carries a [43.9%, 80.5%] band driven by 30 pending + 29 excluded. The point estimate rests on 52/111 adjudicated. This is disclosed but remains the widest uncertainty in the paper.
3. **[Minor]** Model/runtime description is confusing: "served by GLM-5.2" but "inherit the Claude Code runtime's default sampling." A reviewer cannot tell what the actual inference stack is or how determinism is controlled.

### Questions for Authors
1. Of the 4/9 rediscovered, how many required the full 20-agent pipeline vs. contract-derivation + probe alone (which is what you actually ran)?
2. Can you give a single number for the effective adjudication rate you expect the 30 pending to resolve at, to narrow the precision band?

---

## Reviewer 2 — Strict Reviewer
> Confidence: 4/5

### Summary
The paper is well-written and honest, and the phenomenon (contract hallucination propagation) is a real contribution. My concern is unchanged in kind from prior rounds though smaller in degree: the positive empirical case rests on a stack of small, heterogeneous samples, and the central "marginal value" claim is still established by author-assigned reachability rather than by running the competing oracle.

### Strengths
1. Contract hallucination propagation is a genuine, transferable insight, and the DeepSeek counterfactual gives it cross-model support.
2. The model-free invariant oracle subclass is the one finding with no LLM dependency — correctly identified as the most defensible.
3. The negative results (threat-model anchor, single-LLM) are reported rather than buried.

### Weaknesses
1. **[Major]** *The whole positive case is underpowered.* Recall n=9 (4/7 testable), threat-model ablation n=12, single-layer live re-probe n=27, schema fuzzer 19 probes, retrospective 52. None of the decisive numbers has a sample large enough to survive a hostile reading, and the 4/9 recall has no interval. The paper is honest about this, but honesty does not add statistical power.
2. **[Major]** *"5 TPs reachable only by the full pipeline" is still analytical, not demonstrated.* You argue the spec fuzzer and model-free oracle cannot reach the 3 diagnostic + 2 state/logic TPs; you did not run them against those five and show they miss. Until you do, the core marginal-value claim is a reclassification, not a measurement — the same objection as Round 18, only relabeled.
3. **[Major]** *CTS is a three-anchor design of which only one anchor is validated.* Source is validated; threat-model is a diagnosed noisy complement (n=12); reproduction is design-only. So the headline contribution effectively reduces to "source-grounded falsification." That is still worthwhile, but the paper is sold as a three-anchor architecture and two-thirds of it is unproven.
4. **[Minor]** "Five VDBMSs" recurs in abstract/intro/contributions, but adjudicated signal is essentially two systems; MeiliSearch and Chroma contribute 0 adjudicated. This is disclosed in Sec 5.1 but oversold up front.

### Questions for Authors
1. Run the 19-probe spec fuzzer and the model-free oracle against the specific 5 "unique" TPs and report that they miss. Can you?
2. What is a 95% interval on the 4/9 recall, and does its lower bound stay above a trivial baseline?

---

## Reviewer 3 — Favorable Reviewer
> Confidence: 3/5

### Summary
A mature, unusually honest systems paper that opens a new problem (non-crash VDBMS compliance defects), ships 28 maintainer-fixed bugs, and contributes a genuinely novel failure mode (contract hallucination propagation) plus a clean mitigation (CTS). The revision history shows every reviewer ask has been answered, including the recall study that was the last outstanding item.

### Strengths
1. Real-world impact: 28 fixed bugs across production VDBMSs is strong external validation few LLM-testing papers match.
2. Contract hallucination propagation + CTS is a conceptual contribution that generalizes beyond VDBMSs (REST contracts, policy-as-code), and the Conclusion frames this transfer well.
3. The paper now has both a controlled retrospective AND a held-out recall study AND an ablation stack — the evaluation is broad for the page budget.
4. Presentation is polished: tight abstract, decomposed Sec 5.3, figure/text consistency on the threat-model anchor.

### Weaknesses
1. **[Minor]** The single-layer counterfactual paragraph (Sec 5.3) is dense; splitting it would help.
2. **[Minor]** No head-to-head with VDBFuzz — complementarity is argued from oracle definitions. Convincing, but a small empirical confirmation would remove all doubt.

### Questions for Authors
1. Would a short table listing the 5 unique-yield TPs by ID (with why each competing oracle misses) strengthen the marginal-value claim at near-zero cost?

---

## Verification

| # | Source | Claim | Verdict | Note |
|---|--------|-------|---------|------|
| 1 | R1 | "Recall now measured (4/9 held-out, canary 0/9)" | <span style="color:#16a34a">**Valid**</span> | L370 present; confounds named; canary at issue-specificity |
| 2 | R2-W2 | "5 unique TPs argued not demonstrated" | <span style="color:#16a34a">**Valid**</span> | L231 assigns reachability by inspection; fuzzer not run against those 5 |
| 3 | R2-W3 | "Only 1 of 3 CTS anchors validated" | <span style="color:#16a34a">**Valid**</span> | Source validated (5.3); threat-model diagnosed negative (5.4, n=12); reproduction design-only (L189) |
| 4 | R2-W1 | "Positive case underpowered (small n)" | <span style="color:#16a34a">**Valid**</span> | recall 9, TM 12, single-layer 27, fuzzer 19 — all small; disclosed but real |
| 5 | R2-W4 | "'Five VDBMSs' oversold" | <span style="color:#d97706">**Misleading**</span> | Genuinely disclosed at L210 and in contributions; front-matter phrasing is optimistic, not false |
| 6 | R1-W3 | "Model/runtime stack unclear (GLM-5.2 + Claude Code runtime)" | <span style="color:#16a34a">**Valid**</span> | L137/L139 mix backbone and runtime; determinism control ambiguous |
| 7 | R1-W1 | "4/9 recall risks being overshadowed by 96.7%" | <span style="color:#d97706">**Misleading**</span> | Both numbers are correctly distinguished in text (L370); risk is reader conflation, not author error |
| 8 | R3-W2 | "No VDBFuzz head-to-head" | <span style="color:#16a34a">**Valid**</span> | L233 concedes empirical comparison is future work |

---

## Action Plan

<span style="color:#dc2626">**Must Fix**</span> — none content-blocking on scientific merit; the two below are the strict reviewer's ceiling-raisers
- [ ] **Demonstrate the 5 unique TPs (R2-W2).** Run the 19-probe spec fuzzer + model-free oracle against those specific 5 TPs and report they miss; add a small by-ID table (also answers R3-Q1). Converts the last analytical claim into measurement. Low effort — the tools already exist.
- [ ] **Confirm target venue and align template (administrative).** Still `\documentclass[sigconf]{acmart}` while filename/target say VLDB; PVLDB uses `vldb.cls`. Gating for submission, affects page/format compliance. *Excluded from the scientific rating below per request.*

<span style="color:#d97706">**Should Fix**</span> — reduce misread risk / strict-reviewer friction
- [ ] Add a 95% interval (or explicit "n too small for CI") to the 4/9 recall so it is not read as a point claim (R2-Q2).
- [ ] Reframe "five VDBMSs" → "five probed, two adjudicated (Milvus, Qdrant)" in abstract + contribution 1 (R2-W4).
- [ ] Clarify the inference stack in one sentence: what GLM-5.2 vs. Claude Code runtime each mean, and how determinism is handled (R1-W3).

<span style="color:#6b7280">**Optional**</span> — polish
- [ ] Split the single-layer counterfactual paragraph (Sec 5.3) into two (R3-W1).
- [ ] One-line note in intro that 4/9 recall is a floor (simplified 2-stage probe, not full 20-agent pipeline) so the number is not read as the system's ceiling.

---

## Meta Recommendation: **ACCEPT (borderline)** — content-wise up from Round 18's Weak Accept

The recall study is the decisive change. Three rounds running, "no end-to-end discovery number" was the one Major every strict reviewer fell back on; it is now a bounded, contamination-controlled 4/9. With that filled, no reviewer has a *Major* that maps to a missing experiment — R2's remaining three Majors are all "underpowered / argued not measured," which lower the ceiling but do not, on their own, justify rejection given the 28 fixed real bugs.

### Excluding the venue/template issue — the rating you asked for
The template/venue mismatch is **purely administrative** and carries **zero weight** on scientific merit. Setting it aside entirely:
- **Content rating: Weak Accept solidly tipping into Accept** (mean overall 6.7/10 across the three reviewers; R1 7, R2 5, R3 8).
- The paper would clear a real PVLDB/ICSE-class bar on the strength of impact (28 fixed bugs), a novel and transferable failure mode (contract hallucination propagation), and a now-complete evaluation (retrospective + recall + ablation stack).
- What still separates it from a **clear/strong Accept** is not a missing experiment but *statistical weight*: every positive number rests on small n, and the "unique 5 TPs" marginal-value claim is still analytical. The single highest-leverage, near-zero-cost move is running the two baselines against those 5 TPs (Must-Fix #1) — that alone would likely push R2 from 5 to 6-7 and make the accept unanimous.

### Comparison with Round 18
- **Soundness (overall): improved.** The last evaluation void (recall) is closed; R1 moves Weak→Adequate (7/10).
- **The strict reviewer's objection changed shape.** Round 18: "marginal value asserted, recall missing." Round 19: recall is present, so R2 retreats to "underpowered + reachability still analytical" — a weaker, ceiling-lowering critique, not a gate.
- **Overall: Weak Accept → Accept (borderline).** The move is now evidence-driven, not presentational.

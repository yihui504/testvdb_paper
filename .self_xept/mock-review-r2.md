# Reviewer 2: Mock Review for PVLDB/VLDB

## Summary

TestVDB targets API compliance defects in Vector Database Management Systems (VDBMSs) using an LLM-driven pipeline with Contract-Truth Separation (CTS). The core idea is that LLMs both extract contracts from documentation and judge compliance, creating a self-confirmation problem when the same model family performs both roles. The system introduces a dev-reviewer agent that falsifies LLM-generated assertions against maintainer-authority evidence (source code, history, intent). Across five VDBMSs, TestVDB produced 111 submissions with 52 adjudicated on Milvus and Qdrant, yielding 36 acknowledged true positives (28 fixed, 8 accepted-open). Aggregate precision is 69.2% (Wilson CI [55.7%, 80.1%] on n=52). A controlled retrospective shows source-grounded FP suppression improves from 31% to 81% while retaining 96.7% of TPs. The paper claims that 5 unique TPs are only reachable by the full LLM pipeline.

## Strengths

1. **Contract-hallucination phenomenon identification.** The observation that one LLM family both generating contracts and judging compliance creates self-confirmation of hallucinated constraints is well-motivated and supported by concrete examples (12 of 48 adjudicated submissions, 25%, marked by-design). The formalization $C_{\text{LLM}} \supset C_{\text{true}}$ clarifies the failure mode.

2. **Model-free invariant oracle subclass.** The identification of COSINE distance >1.0 for identical vectors, incomplete index results, and payload-filter violations as a mathematically grounded subclass that needs no LLM judgment is a defensible, reproducible contribution. These violate hard bounds and reproduce across Milvus and Qdrant.

3. **Controlled retrospective methodology.** The same-population comparison (31% → 81% FP suppression, 96.7% TP retention) uses label-isolated agents and is the paper's strongest methodological claim. The 27 live-re-probed FPs (0 over-kills) provide strong evidence that the source anchor truly eliminates false positives.

4. **Honest threat reporting.** The threat-model anchor ablation (n=12) is reported as a negative result: the anchor is unstable and over-fires on state/concurrency FPs. The paper admits it is "noisy complement" rather than claiming it as a validated contribution.

## Weaknesses

### [Major] Methodological conflation in the 31%→81% retrospective claim

The retrospective comparison (Section 5.3) is presented as a clean head-to-head: "source-grounded lifts FP suppression from 5/16 (31%) to 13/16 (81%). However, this comparison masks three different denominators that are not reconciled:

- **Baseline 31%**: Derived from 16 FPs among 52 adjudicated candidates (36 TP + 16 FP)
- **Improved 81%**: Derived from the same 16 FPs, but the paper states "6 TPs were unreachable via API rate limits" during source-grounding, meaning the comparison is actually 16 FPs out of 52-6=46 reachable candidates, not 52
- **96.7% TP retention**: 29/30 TPs retained, but this 30 TP denominator is different from the 36 TP baseline (6 rate-limited)

The paper does not provide a single, consistent denominator that reconciles all three numbers. The 31%→81% improvement is presented as if the same population is used throughout, but the actual populations differ. The paper states "slightly different TP denominators (claim-only scored all 36; source-grounding scored 30 reachable via the GitHub API)" but this critical footnote is buried in Table 2 discussion rather than being the headline constraint.

**Fix:** Recalculate the retrospective using a consistent denominator. Either (a) report the improvement only on the 30 reachable TPs, explicitly acknowledging 6 are lost, or (b) re-run the comparison on a fully reachable subset. The current presentation conflates three incompatible denominators.

### [Major] The "5 unique TPs only the full LLM pipeline reaches" claim is weakly defended

The paper's strongest technical claim is that 5 acknowledged TPs (3 diagnostic-quality, 2 state/logic) are reachable *only* by the full LLM pipeline, not by a 19-probe schema fuzzer or model-free invariant oracle. However, the evidence is mixed:

1. **For the 2 state/logic TPs (Milvus #47635, #50323):** The argument that these require multi-step state sequences and are unreachable by *any* stateless oracle is convincing by construction. These are genuinely unique.

2. **For the 3 diagnostic-quality TPs (Milvus #47636, Qdrant #9039, Weaviate #12041):** The paper states "a larger or differently designed probe set could plausibly reach some" but treats the 19-probe instance as a lower bound. Table 2 shows the 19-probe fuzzer was run *only on Milvus v2.6.19*, and the paper admits "the fuzzer is milvus-only so the two non-milvus TPs are out of scope." This means for 2 of the 3 diagnostic TPs, the claim is defended by *argument* (probe set design limitation), not *execution*.

3. **Table 2 footnote acknowledges this is a lower bound:** The paper states "The '5' is therefore a lower bound relative to this instance, not a fuzzer-class upper bound." This is honest but weakens the claim's strength. A reader cannot tell whether a better-designed probe set would reach all 3 diagnostic TPs.

**Fix:** Either (a) run the 19-probe fuzzer on Qdrant and Weaviate to provide execution evidence for all 5 TPs, or (b) reframe the claim as "2 state/logic TPs provably unreachable by any stateless oracle; 3 diagnostic TPs not reached by this 19-probe instance (possibly reachable by better designs)." The current presentation conflates proven uniqueness with probe-set limitations.

### [Major] Single-layer counterfactual (45.6%) combines incomparable ground truths

The 45.6% single-layer precision figure is presented as a directional comparison: "derived single-layer precision = 36/(36+16+27) = 45.6% vs TestVDB's 69.2%." However, this combines:

- **36/52:** Maintainer-adjudicated TPs from the full pipeline
- **16/52:** Maintainer-adjudicated FPs from the full pipeline
- **27/27:** Dev-reviewer-killed candidates, re-probed live and source-grounded

The 27 killed candidates were *never adjudicated by maintainers*. They were classified as FPs by live re-probing on a fresh v2.6.19 container plus source grounding. This is a *different ground truth tier* than maintainer adjudication. The paper admits this in Section 5.3 ("triage might reclassify a few of the 27") but still presents 45.6% as a clean comparison.

Table 2 and Figure 1 group rows by "ground truth tier" (LLM-judged, API-acceptance, retrospective, maintainer) but the 45.6% figure spans tiers: it mixes maintainer-adjudicated (36/52) with live-re-probed (27/27). This is apples-to-oranges.

**Fix:** Either (a) remove the 45.6% single-layer counterfactual from the precision comparison (it's not the same tier), or (b) clearly mark it as "mixed-tier estimate, not directly comparable to maintainer-adjudicated 69.2%." The current presentation in Figure 1 suggests a direct comparison that is methodologically invalid.

### [Major] Generalizability rests on weak statistical foundation

The headline precision is 69.2% (36/52) with Wilson 95% CI [55.7%, 80.1%]. However:

1. **Small effective n:** n=52 is small, and the CI is wide. The lower bound (55.7%) is not strong evidence.

2. **Pending submissions dominate:** 30 of 111 submissions are pending, 29 excluded. The worst-case bound [43.9%, 80.5%] is honest but spans nearly the full possible range.

3. **Weaviate signal is minimal:** 21 of 30 Weaviate submissions are pending, giving almost no adjudicated signal. The paper claims generalization primarily for Milvus and Qdrant, but this reduces the effective generalization claim from 5 VDBMSs to 2.

4. **Excluded set may hide FPs:** 17 of 29 excluded are Milvus closed-no-label. The paper bounds this (36/81=44.4% if all FPs) but admits "excluding them could hide an FP tail."

**Fix:** Acknowledge that the 69.2% figure is essentially a Milvus+Qdrant estimate (n=52) and that Weaviate/MeiliSearch/Chroma provide only breadth, not statistical evidence. The current abstract presents the 69.2% as if it generalizes across all 5 VDBMSs, which is misleading.

### [Major] Recall study (4/9 = 44%) is weak evidence but framed strongly

The held-out rediscovery study found 4/9 pre-2024 bugs rediscovered (44%, Wilson CI [18.9%, 73.3%]). The paper claims this "genuine discovery recall, not memorization" (0/9 canary recall at issue-specificity). However:

1. **CI is massive:** [18.9%, 73.3%] spans from very weak to strong. This is not strong evidence either way.

2. **2 blocked by SDK incompatibility:** 2 of 9 bugs were blocked by milvus/pymilvus incompatibility, reducing the testable set to 7. The paper reports 4/7 testable but presents 4/9 headline, which understates the 57% (4/7) on the actually testable set.

3. **Spec-completeness limit:** One bug was invisible to spec-derived contract (qdrant dimension-mismatch). This is a fundamental limit of the approach but not quantified.

**Fix:** Present recall as 4/7 = 57% on the testable subset, with the 2 incompatibility-blocked bugs reported separately. Acknowledge that 4/9 = 44% is a lower bound if incompatibility is resolved. The current framing presents 44% as if all 9 were testable.

### [Major] LLM contamination defense is incomplete

The contamination defense (GLM-5.2 canary test: 0/9 issue-specificity recall) is good but incomplete:

1. **Only GLM-5.2 tested:** The paper uses only GLM-5.2 throughout. A canary on a *different* model (e.g., Claude, GPT-4) would strengthen the claim that the phenomenon is model-agnostic, not GLM-specific.

2. **Cosine>1.0 overlap with general knowledge:** The paper flags "cosine > 1.0 invariant as the one overlap with general mathematical knowledge rather than count it as independent evidence." But this invariant is central to the model-free oracle claim. If it's overlapping with general knowledge, it's not *independent* evidence of LLM discovery capability.

3. **DeepSeek counterfactual is limited:** The paper reports "DeepSeek on the same doc passages reproduces over-strict constraints in 2/9 of an expanded N=10 set." This is directional but N=10 is tiny, and the paper doesn't report whether DeepSeek also hallucinates the *same* constraints as GLM-5.2 or *different* ones.

**Fix:** Either (a) test a second LLM family to show contract-hallucination is not GLM-5.2 specific, or (b) explicitly acknowledge that all results are GLM-5.2-specific and generalization to other models is future work. The current presentation implies generalizability without evidence.

### [Minor] Threat-model anchor ablation is underpowered

The threat-model anchor ablation (Section 5.4, n=12 Milvus FPs) is honestly reported as unstable, but:

1. **Tiny n:** n=12 is too small to conclude anything about the threat anchor's utility. The "noisy complement" characterization is based on 2 FPs caught by threat but not source.

2. **Wiring gap confounds earlier runs:** The paper admits an earlier ablation was confounded by a wiring gap (threat_model.json vs developer_cognition.json). This raises questions about experimental hygiene.

3. **No reproduction:** The ablation is not reproduced on non-Milvus data (Qdrant, Weaviate), so we don't know if the "noisy complement" finding generalizes.

**Fix:** Either (a) increase n to at least 30 FPs across Milvus+Qdrant, or (b) remove the threat-model anchor from the main architectural diagram and relegate it to "failed explorations." The current presentation presents it as a working component when it's barely validated.

### [Minor] Cost claims lack verification

The paper reports "~$10 per target" and "~10^4 LLM calls" for the full study. However:

1. **No artifact-linked accounting:** The paper states "precise per-token and wall-clock accounting is part of the anonymized artifact" but does not provide even a single example breakdown (e.g., Milvus pipeline: 1500 calls, $8.50). The reader cannot verify the order of magnitude.

2. **Pipeline description is vague:** Section 3.1 states "O(10-50) generated attack candidates" but doesn't give an actual distribution. How many candidates per VDBMS? How many candidates reached Stage-2? How many reached the dev-reviewer?

**Fix:** Provide a concrete breakdown for one VDBMS (e.g., Milvus): X candidates generated → Y Stage-2 → Z submitted → A agents invoked → B tokens → $C cost. The current "order of 10^4 calls" and "order of $10" is too vague to verify.

### [Minor] Model-free invariant oracle is underdeveloped

The model-free invariant oracle (COSINE>1.0, incomplete results, payload-filter violations) is a strong contribution but is only briefly discussed in Section 5.2 (RQ2 case studies) and not integrated into the main evaluation:

1. **No quantitative yield:** How many of the 36 TPs were caught by the model-free oracle? The paper states "3 result-correctness by the model-free invariant oracle" but doesn't break out which of the 36 these are.

2. **No precision comparison:** Does the model-free oracle have better precision than the LLM pipeline? The paper doesn't report its standalone FP rate.

3. **Not integrated into RQ3:** Table 2 and Figure 1 don't report model-free oracle precision, so we can't compare it to CTS or single-layer.

**Fix:** Add a row to Table 2 for "model-free invariant oracle (math-bounds only)" with its own precision/FP rate. The current treatment buries a strong technical contribution in a case study.

### [Minor] Reproducibility: pinned versions and prompts

The paper states "target VDBMS versions are pinned per system" and "full prompts in the artifact." However:

1. **No version table:** The paper doesn't provide a table of which versions were tested (e.g., Milvus 2.6.19 for ablations, but what about the main study? Weaviate v1.19 for recall, but what about yield generation?).

2. **No prompt examples:** Even a single example prompt (e.g., the dev-reviewer's source anchor prompt) would help readers understand the LLM's reasoning. The "full prompts in artifact" claim is opaque without a sample.

**Fix:** Add a table with pinned versions for all 5 VDBMSs in both yield generation and ablation studies. Provide 1-2 example prompts in an appendix. The current artifact-only approach makes it hard to evaluate LLM quality.

## Questions for Authors

1. **Retrospective denominators:** Can you reconcile the 31%→81% improvement using a single, consistent denominator? Either report the improvement only on the 30 reachable TPs (acknowledging 6 lost), or re-run the comparison on a fully reachable subset. The current numbers conflate three incompatible denominators.

2. **"5 unique TPs" claim strength:** Can you run the 19-probe fuzzer on Qdrant and Weaviate to provide execution evidence for all 5 TPs, or reframe the claim as "2 state/logic TPs provably unique; 3 diagnostic TPs not reached by this 19-probe instance"? The current presentation mixes proven uniqueness with probe-set limitations.

3. **Generalizability evidence:** Do you have evidence (even preliminary) that contract-hallucination propagation occurs in other LLM families beyond GLM-5.2? If not, can you explicitly state that all results are GLM-5.2-specific and generalization is future work?

## Scores

- **Originality / Novelty:** 4/5 — Contract-hallucination propagation is a new characterization of LLM-as-judge failure modes; CTS is a principled mitigation; model-free invariant oracle is a clean, reproducible contribution.
- **Significance / Impact:** 3/5 — VDBMS compliance defects are a real but narrow slice of incorrect behavior; complementarity with VDBFuzz is clear but head-to-head comparison is future work; generalizability beyond VDBMSs is claimed but not tested.
- **Presentation / Clarity:** 3/5 — Structure is logical, but key claims (31%→81%, 5 unique TPs, 45.6% single-layer) are buried in footnotes or caveats rather than being headline constraints; figures are helpful but dense.
- **Soundness / Technical correctness:** 3/5 — Methodology is mostly sound but critical comparisons (retrospective, single-layer counterfactual) mix incomparable ground truths; generalizability rests on small n (52) with wide CIs; recall study is underpowered (n=9).
- **Overall:** **Weak Accept** — The contract-hallucination phenomenon and CTS mitigation are genuine contributions with strong mechanistic evidence, but the evaluation's methodological conflation (denominators, ground-truth tiers) and weak statistical foundation (small n, wide CIs) undermine the headline claims. The model-free invariant oracle is independently valuable. I recommend acceptance with revisions that: (1) reconcile the retrospective denominators, (2) qualify the "5 unique TPs" claim, (3) separate single-layer counterfactual from maintainer-adjudicated precision, and (4) acknowledge that generalizability is primarily Milvus+Qdrant, not all 5 VDBMSs.
- **Reviewer Confidence:** 4/5 — I read the full paper carefully, traced the evaluation methodology, and identified specific numerical inconsistencies. I did not inspect the artifact or reproduce experiments.

---

**Top 3 Major Weaknesses:**
1. Methodological conflation in the 31%→81% retrospective claim (three incompatible denominators)
2. The "5 unique TPs only the full LLM pipeline reaches" claim is weakly defended (argument vs execution)
3. Single-layer counterfactual (45.6%) combines incomparable ground truths (maintainer-adjudicated + live-re-probed)

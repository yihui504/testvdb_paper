# Mock Review Report
> **Target Venue:** PVLDB / VLDB · **Overall Prediction:** Weak Accept (leaning Accept) · **Date:** 2026-07-14
> **Paper:** TestVDB — Detecting API Compliance Defects in VDBMSs via Contract-Truth Separation
> **Note:** This is a camera-ready of an already-accepted paper (Round 22, 2/3 Accept per project memory). Science is fixed; most "fixes" below are framing/polish, with one open future-work item.

## Score Summary

| Dimension | R1 (Objective) | R2 (Strict) | R3 (Friendly) | Median |
|-----------|:--------------:|:-----------:|:-------------:|:------:|
| Originality / Novelty | 4/5 | 4/5 | 4/5 | 4/5 |
| Significance / Impact | 3/5 | 3/5 | 4/5 | 3/5 |
| Presentation / Clarity | 4/5 | 3/5 | 5/5 | 4/5 |
| Soundness / Technical | 3/5 | 3/5 | 4/5 | 3/5 |
| **Overall** | **Weak Accept** | **Weak Accept** | **Accept** | — |
| Confidence | 4/5 | 4/5 | 4/5 | 4/5 |

Consensus on Originality (4/4/4) is strong; the spread is on Soundness/Significance (strict vs friendly). Net: **two Weak Accept + one Accept**, matching the real outcome.

---

## Reviewer 1 — Objective
> Confidence: 4/5
**Summary** TestVDB is an LLM-driven detector for API compliance defects in VDBMSs, targeting the 43% "incorrect-behavior" slice that crash-focused fuzzers miss. Core idea: Contract-Truth Separation (CTS) isolates LLM-generated contracts from a source-grounded truth layer that falsifies them, countering "contract hallucination propagation" (12/48 adjudicated = 25% by-design). 36 maintainer-acknowledged issues across 5 VDBMSs; retrospective shows source anchor lifts FP suppression 31%→81% at 96.7% TP retention; aggregate precision 69.2% (n=52).
**Strengths** (with evidence): (1) well-motivated scope via Table 1 exclusion reasoning; (2) CTS is a principled response to the concrete `constant.go` hallucination example; (3) the same-52-candidate retrospective is methodologically sound; (4) thorough, honest Threats-to-Validity; (5) model-free invariant oracles (COSINE>1.0) are the least-contingent contribution.
**Weaknesses** 1. **[Major]** Maintainer acknowledgment is weak ground truth. 2. **[Major]** n=52 small, dominated by Milvus (51) + Qdrant (26). 3. **[Major]** "5 unique TPs" claim not defended against a *general* stateful fuzzer. 4. **[Major]** Single-LLM-family (GLM-5.2 throughout) limits generalizability. 5. **[Major]** 31%→81% conflates source-grounding with having a second layer. 6. **[Minor]** 45.6% figure methodologically indirect. 7. **[Minor]** threat-model ablation n=12 underpowered. 8. **[Minor]** 4/9 recall CI too wide to cite as headline.
**Questions** (1) Of the 12 by-design, how many did the dev-reviewer catch pre-adjudication vs maintainers? (2) Could a general stateful fuzzer (RESTler/EvoMaster) reach the 3 diagnostic TPs? (3) Does contract-hallucination occur in other model families?

## Reviewer 2 — Strict
> Confidence: 4/5
**Summary** (as above). The contract-hallucination phenomenon, CTS mitigation, and model-free oracle are genuine contributions, but the evaluation's headline comparisons rest on small n with wide CIs and several comparisons the reviewer judges to mix incomparable denominators/ground-truth tiers.
**Strengths**: (1) hallucination phenomenon + $C_{\mathrm{LLM}} \supset C_{\mathrm{true}}$ formalization; (2) model-free oracle; (3) same-population retrospective + 27/27 live re-probe; (4) honest negative-result reporting.
**Weaknesses** 1. **[Major]** 31%→81% retrospective conflates three incompatible denominators. 2. **[Major]** "5 unique TPs" weakly defended (argument vs execution). 3. **[Major]** 45.6% single-layer counterfactual mixes maintainer-adjudicated + live-re-probed tiers. 4. **[Major]** Generalizability rests on weak stats (n=52, wide CI, Weaviate minimal, excluded FP tail). 5. **[Major]** Recall 4/9 weak; should present 4/7=57%. 6. **[Major]** Contamination defense incomplete (GLM-5.2 only; cosine overlap; DeepSeek N=10). 7. **[Minor]** threat-model n=12 + wiring gap. 8. **[Minor]** cost claims unverifiable. 9. **[Minor]** model-free oracle underdeveloped (no standalone precision row). 10. **[Minor]** no version table / prompt sample.
**Questions** (1) Reconcile the 31%→81% denominators. (2) Run fuzzer on Qdrant/Weaviate or reframe "5 unique TPs". (3) Cross-model evidence?

## Reviewer 3 — Friendly
> Confidence: 4/5
**Summary** Timely problem (43% of VDBMS bugs lack oracles); CTS + contract-hallucination propagation is a transferable insight; model-free oracle is the most defensible finding; evaluation is honest and well-structured.
**Strengths** (longest section): real gap; transferable hallucination insight; cross-vendor COSINE>1.0; honest negative-result reporting; right retrospective method; clear incremental-value articulation; clean VDBFuzz complementarity positioning; clear writing.
**Weaknesses / Suggestions** 1. **[Major]** recall cohort small (4/9). 2. **[Major]** breadth systems give little adjudicated signal. 3. **[Major]** threat-model confounded/noisy. 4. **[Minor]** reproduction anchor is future work. 5. **[Minor]** ground-truth tiers asymmetric across baselines. 6. **[Minor]** 45.6% heterogeneous triage. 7. **[Minor]** excluded set may hide FP tail.
**Questions** (1) Plans to expand recall cohort? (2) Re-adjudicate Weaviate once triage completes? (3) Refine threat-model blindspot mechanism?
**Scores** Originality 4, Significance 4, Presentation 5, Soundness 4 — **Accept**.

---

## Verification

Claims re-checked against the paper source (`paper/paper-draft-vldb-final.tex`). **The paper is unusually well-disclosed** — most "weaknesses" are already stated in Threats-to-Validity (§5.6) or the evaluation footnotes; several strict-reviewer claims misread the tables.

| # | Source | Claim | Verdict | Note |
|---|--------|-------|---------|------|
| 1 | R2-W1 | "31%→81% retrospective conflates three incompatible denominators / methodologically invalid" | **False** | The headline metric (FP suppression) is 5/16→13/16 — **same 16 FPs**, consistent denominator. The TP *retention* denominator differs (36 vs 30, 6 rate-limited) but is disclosed in the footnote at L276. R2 confused the FP denominator with the total candidate count. The "apples-to-oranges" charge does not hold for the FP comparison the headline rests on. Only nit: the TP-retention caveat could be more prominent. |
| 2 | R1-W2 / R2-W4 / R3-W2 | n=52 small; "across five systems" but effectively Milvus+Qdrant; Weaviate 21/30 pending | **Valid** | Numbers confirmed: Milvus 22/34=64.7%, Qdrant 11/14=78.6%. Paper concedes "generalization claimed primarily for Milvus and Qdrant" (L211) and Weaviate undiagnosed (L389). The **abstract** (L88) still says "aggregated over the five systems" — the one place that overstates 5-system generalization. |
| 3 | R1-W3 / R2-W2 | "5 unique TPs" weakly defended; 2 of 3 diagnostic TPs (qdrant #9039, weaviate #12041) by argument not execution (fuzzer is milvus-only) | **Misleading** | Body is honest: L232 states it is "a lower bound relative to this instance, not a fuzzer-class upper bound"; Table 2 caption notes the fuzzer is milvus-only. Execution covers 3/5 (the 2 state/logic + 1 milvus diagnostic, 0/19 triggers). The **abstract/intro headline** (L140: "only the full pipeline reaches") states all 5 uniformly — that is the real, fixable framing gap. |
| 4 | R1-W4 / R2-W6 | Single-LLM-family (GLM-5.2 throughout) → CTS generalization untested across model families | **Valid** | Real gap. Partial mitigation exists: canary 0/9 (L392), DeepSeek contract counterfactual 2/9 of N=10 (L392). But cross-model *CTS effectiveness* is not tested, while the conclusion (L408) claims CTS generalizes. This is the one genuinely open scientific item — appropriately future work for camera-ready. |
| 5 | R1-W6 / R2-W3 / R3-W6 | 45.6% single-layer figure mixes maintainer-adjudicated (36/52) + live-re-probed (27/27) tiers — apples-to-oranges | **Misleading** | Already disclosed: L282 calls it "a directional lift," L288 warns rows are "not directly comparable across tiers." The real nit: Figure 1 (L339) plots the 45.6% bar visually adjacent to the 69.2% gold bar, which invites a direct comparison the text warns against. Fix is labeling, not content. |
| 6 | R1-W5 | 31%→81% conflates source-grounding with "having any second layer" | **Misleading** | Plausible confound in principle, but the 27/27 live re-probe audit (L280) independently confirms the killed candidates are genuine FPs — so the suppression is real FP removal, not second-pass harshness. Clean isolation (source vs non-source second layer) is absent but the practical claim holds. |
| 7 | R1-W8 / R2-W5 / R3-W1 | Recall 4/9 too small; CI [18.9%, 73.3%]; R2 says present 4/7=57% instead | **Misleading** | Paper already reports **both** 4/9 and 4/7 (L393). Choosing 4/9 (conservative) as headline is the *more* honest option; R2's suggestion (4/7) would make the paper look better. The "genuine, not memorization" claim (L393) refers to the 0/9 canary, not the precision of the 44% — supported. |
| 8 | R1-W7 / R2-W7 / R3-W3 | Threat-model anchor ablation n=12 tiny + wiring-gap confound | **Valid** | But already heavily qualified: L383 reports n=12, instability, the wiring gap, and explicitly "we do not claim the three-anchor design as a clean validated contribution on the strength of n=12." Disclosed and bounded. |
| 9 | R1-W1 | Maintainer acknowledgment is weak ground truth | **Valid** | Acknowledged verbatim at L387. The improvement (independent re-validation) is good practice but out of scope for camera-ready. |
| 10 | R2-W8 | Cost claims (~$10/target, ~10^4 calls) unverifiable | **Misleading** | Order-of-magnitude given at L140; precise accounting deferred to artifact (pinned URL). A one-system concrete breakdown is a reasonable addition but not an error. |
| 11 | R2-W9 | Model-free oracle underdeveloped — no standalone precision row in Table 4 | **Valid** | Paper says "3 result-correctness by the model-free invariant oracle" (L232) but no standalone row. A genuine, cheap-to-add improvement (Minor). |
| 12 | R2-W10 | No version table / no prompt sample | **Misleading** | Versions "in artifact" (L140), prompts "in artifact." A compact version table + one example prompt in an appendix is a reasonable Minor addition. |
| 13 | R3-W4 | Reproduction anchor is future work | **False** | Already stated at L190 ("the reproduction anchor remains design-level future work"). R3's suggestion is already in the paper. |
| 14 | R3-W5 | Ground-truth tiers asymmetric across baselines | **False** | Already made explicit at L288. R3 acknowledges the paper handles it; suggestion is a one-line clarification only. |
| 15 | R3-W7 | Excluded set may hide FP tail (17/29 Milvus closed-no-label) | **Misleading** | Already bounded at L394 (worst case 36/81=44.4%). Disclosed. |

**Stage-2 takeaway:** Of 15 distinct weakness claims, **3 are False / misreadings** (R2-W1 denominator conflation is the headline catch; R3-W4, R3-W5 already in paper), **8 are Misleading** (disclosed in body but framed/headlined sub-optimally), and **4 are Valid** (cross-model gap, model-free-oracle row, n=52 abstract framing, ground-truth weakness). The strict reviewer (R2) over-claimed severity on items 1, 5, 7 by reading disclosures as absences.

---

## Action Plan

### **Must Fix** — multi-reviewer consensus on a Valid framing issue; cheap, high-value for camera-ready
- [ ] **Abstract/intro: narrow the "5 systems" + "5 unique TPs" framing.** (R1-W2, R2-W4, R3-W2, R1-W3, R2-W2 — 2 consensus clusters, 5 reviewers-weight.)
  - L88 abstract "aggregated over the five systems" → state precision rests on Milvus+Qdrant (n=52), with Weaviate/MeiliSearch/Chroma as breadth probes.
  - L140 intro "5 unique TPs... only the full pipeline reaches" → "2 state/logic TPs provably unreachable by any stateless oracle, plus 3 diagnostic-quality TPs not reached by our 19-probe fuzzer instance (a lower bound, not a fuzzer-class upper bound)." Body already supports this; only the headline needs to match.

### **Should Fix** — disclosed but presentation invites misreading
- [ ] **Figure 1 (fig:precision): stop inviting cross-tier comparison of 45.6% vs 69.2%.** (R2-W3, R1-W6, R3-W6 — 3 reviewers.) Add an explicit "different ground-truth tier — not directly comparable" annotation on the Single-layer CF bar, or visually separate the tiers with a divider. Text at L288 is correct; the figure undermines it.
- [ ] **Make the TP-retention denominator caveat (36 vs 30) prominent.** (R2-W1.) Promote the L276 footnote into the main text of §5.3.1 so no reviewer misreads the 96.7% denominator. (The FP comparison 5/16→13/16 is already clean — no recalculation needed; do **not** let R2's "three denominators" framing trigger unnecessary re-analysis.)
- [ ] **Add a standalone row for the model-free invariant oracle in Table 4.** (R2-W9.) Its own precision / FP rate makes the "most defensible finding" quantitatively visible rather than buried in RQ2 prose. Cheap and strengthens the paper.
- [ ] **Cross-model scope statement.** (R1-W4, R2-W6 — Valid, consensus.) Add one sentence in §5.6 or the conclusion: all CTS results are GLM-5.2; the DeepSeek contract counterfactual (2/9) is partial evidence; cross-model CTS effectiveness is the primary future-work direction. The conclusion already gestures at future work (L408) — make the model-family limitation explicit there.

### **Optional** — individual Minor; nice but not necessary for camera-ready
- [ ] Recall cohort: optionally add "(4/7 of the testable; 2 blocked by SDK incompatibility)" next to the headline 4/9 so the 57% testable-subset figure is visible (L393). (R2-W5.)
- [ ] One concrete per-target cost/token breakdown for Milvus in a footnote (L140) — e.g., "Milvus: ~X calls, ~Y tokens, ~$Z." (R2-W8.)
- [ ] Compact version-pinning table for all 5 VDBMSs + one example dev-reviewer prompt in an appendix. (R2-W10.)
- [ ] If space permits, note the 31%→81% "source vs any-second-layer" isolation as a acknowledged limitation, citing the 27/27 live audit as the mitigating evidence. (R1-W5.)

---

## Predicted Overall Decision

**Weak Accept (leaning Accept).** Two Weak Accept (R1, R2) + one Accept (R3), unanimous Originality 4/5, unanimous Confidence 4/5. The contract-hallucination-propagation framing, the CTS principle, and the cross-vendor model-free COSINE>1.0 oracle are genuine, defensible contributions; the same-52-candidate retrospective with a 27/27 live re-probe audit is solid evidence the source anchor removes real FPs. The weaknesses that survive verification are (a) small-n statistics and a single-LLM-family evaluation — both openly disclosed and typical of a first system paper — and (b) a handful of headline/framing mismatches where the abstract overstates what the body carefully qualifies. None of the verified weaknesses are blocking; the strict reviewer's most severe charge (denominator conflation) does not survive fact-checking. **For camera-ready: execute the Must-Fix framing changes and the Table-4 / Figure-1 presentation fixes; treat cross-model CTS as the explicit future-work item.**

### What a rebuttal should pre-empt (if a future reviewer echoes R2)
1. "Denominator conflation in 31%→81%" → FP comparison is 5/16→13/16, same 16 FPs; only TP retention uses 30 (disclosed). Do not concede the invalid-methodology framing.
2. "5 unique TPs unsupported" → 2 state/logic are provably unique (no stateless oracle can reach them); 3 diagnostic are bounded against the specific 19-probe instance (0/19 execution on milvus); paper states this is a lower bound.
3. "45.6% vs 69.2% unfair comparison" → different ground-truth tiers, explicitly labeled directional; Figure 1 groups by tier.
4. "Single LLM family" → acknowledged; canary (0/9) + DeepSeek partial counterfactual provided; cross-model is future work.

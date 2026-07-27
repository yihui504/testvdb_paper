# Attitude-Half Report（dual-review 态度半边，复用 mock-review）

> Paper: TestVDB · Target Venue: TBD → fallback SE 顶会（ICSE/FSE/ISSTA/ASE）通用标准
> Overall Prediction: **Weak Accept / Borderline**（5.7/10，分歧大）· Date: 2026-07-26

## Score Summary

| Dimension | R1 客观 | R2 严格 | R3 友好 | mean |
|---|:---:|:---:|:---:|:---:|
| Soundness | 3 | 3 | 4 | 3.3 |
| Significance | 4 | 3 | 4 | 3.7 |
| Novelty | 4 | 4 | 5 | 4.3 |
| Presentation | 4 | 3 | 4 | 3.7 |
| **Overall** | **6/10** | **4/10** | **7/10** | **5.7** |
| Confidence | 4/5 | 4/5 | 4/5 | 4/5 |

**Overall Prediction: Weak Accept / Borderline**（5.7/10）。R1 weak-accept（6/10）、R2 lean-reject（4/10）、R3 lean-accept（7/10）——borderline paper。三人都认可贡献真实（15 merged PR + novelty delta vs MASTOR），分歧在方法论 gaps 是否致命。修订一轮（解决 W1-W3）可拉到 weak-accept 共识。

## Reviewer 1 — Objective

**Venue:** TBD → fallback SE top conference (ICSE/FSE/ISSTA/ASE)
**Stance:** Independent, evidence-driven. Scores reflect conference norms; not calibrated to any other reviewer.

---

## Summary

The paper studies **documentation-implementation defects** in Vector Database Management Systems (VDBMSs): cases where the API silently accepts an input or behavior that its natural-language API documentation prescribes rejecting (e.g., `nprobe=0`, `ef=0`, idempotent drops returning success where the doc promises an error). The authors argue, via a structural exclusion argument (Table 1), that ~85% of these defects are unreachable by differential, metamorphic, property-based, and crash oracles because the relevant boundary is natural-language prose, not a machine-checkable spec. This forces an LLM into both the extraction and the judgment roles, creating two reliability layers: family-specific self-preference (mitigated by cross-model judging) and a deeper **task-intrinsic** layer, where ambiguous documentation causes multiple LLM families to converge on the same wrong clause. The proposed counter is **source-grounded falsification**: the implementation's source code is read by a `dev-reviewer` agent that tries to disprove each LLM-derived behavioral claim. The tool, TestVDB, is a 20-agent pipeline built on Claude Code + GLM-5.2.

The empirical evaluation reports 107 candidate issues submitted across Milvus, Qdrant, and Weaviate (49 true-positive, 15 merged-PR-fixed), a controlled retrospective over 48 adjudicated candidates (67% precision / 74% recall, vs. 37% recall without source grounding, 3-run union ensemble), and an 18-clause task-intrinsic probe plus a behavior/idempotency extension (n=29 ambiguous, n=21 explicit-bound negatives) showing cross-model judging misses 3 of 6 TI clauses while source-grounded falsification catches all 18. A bidirectional VDBFuzz reachability probe on Qdrant v1.4.0/v1.18.0/v1.18.2 (n=1 per direction) illustrates an asymmetric-reachability hypothesis.

---

## Strengths

1. **The reliability decomposition is clearly scoped and falsifiable.** Section 3 separates family-specific from task-intrinsic errors and gives an operational definition at the parameter level ("a clause is task-intrinsic when a second family's independent formalization of the same documentation is also over-strict on the same parameter"). The scoping paragraph distinguishing this from Haldar et al.'s intra-judge self-inconsistency is the right kind of precision for an SE venue — it pre-empts the most common misreading of the claim.

2. **The exclusion table (Table 1) does real work.** Rather than asserting the residual is uncovered, the table maps each classical oracle class to the specific defect subclass it reaches and the structural reason it fails on the residual. Pairing it with a within-vendor contrast (Qdrant optional-default vs. explicit-minimum parameters; Milvus search-default vs. explicit-range parameters; Section 6, RQ3) gives a falsifiable prediction: "optional-default with no explicit bound → over-formalization candidate." The specificity check (0/21 on explicit bounds, Wilson [0%, 16%]) is the right negative control.

3. **The artifact-yield accounting is unusually transparent about pending adjudication.** Section 6 (RQ1) reports both the point estimate (68.1% yield precision, Wilson [56.6%, 77.7%] on 72 adjudicated) and a worst-case bound that treats all 35 pending submissions as false positives (45.8%, Wilson [36.7%, 55.2%]). The honest handling of the 10 stale-closed TPs and the explicit statement that 85% is a composition, not a population estimate, are strengths; many testing papers collapse this distinction.

4. **The MASTOR distinction is well-motivated.** Section 5 isolates the actual novelty — not source grounding per se but the *asymmetric direction* (source falsifies documentation-derived claims rather than encoding implemented behavior) — and the related-work paragraph (Section 7) extends this to Toradocu/Doc2OracLL/AugmenTest/ChatAssert/Testora, identifying precisely which subset of LLM-as-oracle work TestVDB differs from and why prompt refinement cannot reach task-intrinsic errors. The positioning is sharper than typical REST-API-oracle papers.

5. **The controlled VDBFuzz head-to-head is reported with appropriate caveats.** Rather than claiming a "win," the authors disclose VDBFuzz's template-suite gap (`wait=true` hardcoded on every points-upsert), explicitly read the reverse direction as a template-coverage limitation rather than a fundamental crash-oracle property, and present the structural asymmetry hypothesis as n=1-per-direction, hypothesis-generating. This is the honest framing of a controlled case study.

---

## Weaknesses

1. **[major, fixable] The RQ3 task-intrinsic probe is the headline finding and rests on a two-LLM-family pair (GLM + DeepSeek), n=18 clauses plus an idempotency extension, with no third family to break a tie.**
   The paper's central claim — task-intrinsic errors survive cross-model validation — is established by observing that *DeepSeek* reproduces *GLM*'s over-strict clause on 6 of 18 parameters. With only two families, the "convergence" evidence is structurally limited: a third family could break the tie, and the RQ3 probe is run only once per family pair (no within-pair repetition to estimate extraction-level variance). This is distinct from the *separate* single-family threat on the RQ2 source-anchor (dev-reviewer uses GLM-5.2 only; Threats-to-Validity concedes "all source-anchor results use a single model family," mitigated by a κ=1.0 DeepSeek cross-check on 20 candidates) — that threat is about source-anchor falsification, not about task-intrinsic extraction. The 3-missed-of-6-TI count from cross-model judging is a within-pair observation, not a population-level estimate. **Position:** Section 6 RQ3, Table 4. **Suggested improvement:** add at least one further LLM family (e.g., a Llama or Mistral variant, or GPT-family) on the 18-clause probe — even n=3 families on the existing 18 clauses would materially strengthen the task-intrinsic claim and turn a binary "DeepSeek agrees with GLM" into a family-set convergence statistic.

2. **[major, fixable] The RQ2 recall headline (74% recall, 67% precision) rests on a 48-candidate retrospective with a 5-run recall band of 15–78%, and the any-confirmed union rule is selected post hoc.**
   Section 6 RQ2 reports the 3-run any-confirmed ensemble reaches 74% recall / 67% precision, and notes single-run recall ranges 15–78%. The justification for the union operating point — "the dev-reviewer is a falsifier, so under-confirmation is costlier" — is plausible but offered after observing the data, and the same data shows majority voting collapses to 26% recall. The retrospective is also confined to Milvus (32) + Qdrant (16); Weaviate is excluded from RQ2. **Position:** Section 6 RQ2, footnote on the 48 candidates. **Suggested improvement:** (a) pre-register the any-confirmed rule on a held-out batch (e.g., Weaviate or a future-version Milvus) and report whether the operating point transfers; (b) add a power analysis on the Wilson intervals — the 67% precision CI [49%, 81%] is wide, and a 48-candidate n is small for a recall claim that drives the abstract headline.

3. **[major, fixable] The 85% "documentation-implementation residual" composition is reported as the central framing number but its denominator is TestVDB's own yield, not a defect sample.**
   Section 1 and Section 6 state ~85% of the 107 submitted issues (89% on the 49-TP subset) are documentation-implementation defects unreachable by classical oracles. The authors are careful to say "this is the composition of our findings, not a population estimate" (abstract, Section 6, Section 8), but the Introduction and Contributions list use 85% as a load-bearing framing for the whole approach. Since TestVDB is by design biased toward documentation-implementation defects, using its own yield as evidence for the size of the residual is partly circular. **Position:** Section 1 first paragraph, Section 6 RQ1 first paragraph, Contributions bullet 2. **Suggested improvement:** add an independent estimate — e.g., (i) a capture-recapture estimate on a known historical issue corpus (Milvus GitHub pre-2025), or (ii) classify a random sample of 100 historical VDBMS issues with the bugstudy25 taxonomy, and report the documentation-implementation fraction. Without this, the 85% framing should be moved out of the Contributions list and explicitly labeled "composition of TestVDB's yield" everywhere it appears.

4. **[minor, fixable] Single-LLM backbone without seed control is under-specified for reproducibility.**
   Section 5 (Implementation) discloses "no fixed random seed; we have not measured run-to-run variance and flag this as a limitation." Combined with the reported 15–78% single-run recall range, this means a reader cannot reproduce a specific TestVDB run, and the headline numbers depend on an unreported sampling distribution. **Position:** Section 5. **Suggested improvement:** report the seed used for at least one of the five retrospective runs, or commit to publishing all five run logs (the footnote promises the artifact will contain them — make this explicit in the main text, with a checksummed release plan).

5. **[minor, fixable] The behavior-idempotency extension (Section 6 RQ3, n=11, "not separately maintainer-acknowledged") mixes confirmed and unconfirmed ground truth.**
   The 11/11 TI rate on idempotency behaviors is reported as the "headline finding of this probe," but seven of the eleven are "impl-confirmed idempotent but not separately maintainer-acknowledged, which we flag." The within-vendor parameter contrast is preserved by reporting subtypes separately, but the pooled 17/29 aggregate in the next sentence dilutes the contrast. **Position:** Section 6 RQ3 paragraph 2. **Suggested improvement:** either (a) commit to maintainer-adjudicating the seven new behaviors before camera-ready, or (b) drop the pooled 17/29 number from the main text and relegate it to a clearly-labeled upper-bound computation in the appendix.

6. **[minor, fixable] The Discussion (Section 8) overreaches on generalization claims without evidence.**
   The paper claims transferability to "REST APIs without OpenAPI coverage, configuration validation, and policy-as-code checks" but concedes "we have not tested these transfers." For a paper whose central methodological move is *distinguishing tested from untested claims* (the explicit-bound vs. optional-default contrast), an unbacked generalization paragraph undercuts that discipline. **Position:** Section 8 paragraph 1. **Suggested improvement:** either add one minimal transferability probe (e.g., a 10-clause run on a documented but non-OpenAPI REST endpoint) or shrink the generalization paragraph to one sentence noting that the structural setting (natural-language documentation, source-available) is not unique to VDBMSs, with explicit "future work" framing.

7. **[minor, unfixable] The n=1-per-direction VDBFuzz reachability probe cannot support the asymmetric-reachability hypothesis, and the paper says so but still elevates it in the Discussion.**
   Section 6 RQ1 reports the bidirectional probe as "hypothesis-generating controlled cases rather than a generalized result," which is correct. But Section 8 ("Crash-oracle asymmetry and incomplete fixes") then uses the #9045↔#7967 root-cause case as evidence that "crash-focused fuzzing surfaces symptoms whose fixes can leave the documentation-implementation residual intact." The single root-cause story is illustrative; the structural asymmetry claim is not established. **Position:** Section 8 final paragraph. **Suggested improvement:** either run the asymmetric-reachability probe on a third pair (a second VDBMS where both tool's target defects reproduce) to push n≥2 per direction, or move the asymmetric-reachability hypothesis from Discussion framing to an explicit "future work" sentence.

---

## Questions for Authors

1. **On the task-intrinsic claim.** If a third LLM family (e.g., Llama 3 or Mistral) were run on the 18-clause probe, what would your prediction be for how many of the 6 current TI clauses it would also over-formalize? Is the prediction sharp enough that a single disagreement would weaken the claim, or is the claim robust to one family disagreeing?

2. **On the operating-point selection.** The any-confirmed union rule gives 74% recall / 67% precision at 3 runs and 85% recall / 62% precision at 5 runs. Did you select the 3-run operating point before or after observing the 5-run data? If the 5-run point were selected instead, would the recall headline change materially, and would the precision drop to a level that would change the abstract claim?

3. **On the source-grounded anchor's failure modes.** Section 5 and Threats-to-Validity (Section 6) concede that "an implementation bug can wrongly falsify a clause whose documentation is right." In the 48-candidate retrospective, did any of the 27 TPs involve an implementation bug that the dev-reviewer initially mis-classified as over-strict? If so, how many, and how were they caught?

---

## Scores

| Dimension | Score (1–5) | Notes |
|-----------|-------------|-------|
| Soundness | 3 | The structural exclusion argument (Table 1) is sound; the task-intrinsic claim and the RQ2 operating point are under-evidenced given the n=2-family and 48-candidate limitations. Honest uncertainty reporting is a plus. |
| Significance | 4 | The documentation-implementation defect class is real, the residual framing is novel, and 15 merged-PR fixes on production VDBMSs demonstrate practical impact. |
| Novelty | 4 | The source-grounded *falsification* direction (source as falsifier of documentation-derived claims, not as oracle of implemented behavior) is a genuine conceptual move over MASTOR and the Toradocu/Doc2OracLL line. The task-intrinsic vs. family-specific decomposition is original. |
| Presentation | 4 | Clearly written, well-structured; the within-vendor contrast and the explicit-bound negative control are exemplary. Minor overreach in Discussion generalization paragraph. |
| **Overall** | **6 / 10** | A solid contribution with a real tool (15 merged fixes), a well-scoped reliability decomposition, and an honest limitations section. The central claims (task-intrinsic layer, 74% recall source-grounded) need either an additional LLM family or a pre-registered operating point before they are conference-grade. With one revision cycle addressing Weaknesses 1–3, this lands in the weak-accept band. |
| Confidence | 4 / 5 | I read the paper end-to-end and traced the evaluation back to the claims. I am not deeply expert on LLM-as-judge self-preference mechanisms beyond Panickssery et al. and Haldar et al., which is where my residual uncertainty lies. |

## Reviewer 2 — Strict / Critical

**Paper:** TestVDB: Source-Grounded Falsification of LLM-Derived Behavioral Claims for Documentation-Implementation Consistency Testing of Vector Databases

---

## Summary

The paper studies documentation-implementation defects in Vector Database Management Systems (VDBMSs): cases where the API silently accepts inputs that violate its own natural-language documentation (e.g., `nprobe=0`, `ef=0`, `wait=false` on a zero-length vector). Because the documented boundary is natural-language prose rather than a formal schema, the authors argue the standard oracle families (crash, differential, metamorphic, property-based) cannot adjudicate these accept/reject decisions, leaving an LLM as the practical oracle. They identify a two-layer reliability problem in the LLM-as-oracle: a family-specific layer (mitigated by cross-model validation) and a *task-intrinsic* layer (different LLM families extract the same wrong clause from ambiguous text), and propose **source-grounded falsification** — using the implementation's source code to refute LLM-derived behavioral clauses — as a counter to the task-intrinsic layer. The TestVDB pipeline is evaluated on Milvus, Qdrant, and Weaviate, yielding 107 submitted issues and 49 maintainer-acknowledged true-positive defects, plus a retrospective over 48 adjudicated candidates reporting 67% precision / 74% recall for the source-grounded dev-reviewer and a probe of 18 over-strict clauses where source catches all 18 while cross-model judging misses 3 of 6 task-intrinsic ones.

The core idea — treating LLM-derived claims as refutable hypotheses and using source as the independent falsifier — is reasonable and the writing is mostly clear. However, several experimental design choices, small sample sizes, and a small number of conflated or under-supported claims prevent me from recommending acceptance in the current state.

---

## Strengths

- **S1. The source-ambiguity framing is genuinely clarifying.** The distinction between low-ambiguity structured sources (where AGORA+/SATORI/MASTOR extract reliable assertions) and high-ambiguity natural-language documentation (where the LLM must interpret intent) cleanly separates TestVDB from prior REST-API oracle work and explains *why* those tools' low FP rates do not transfer. The MASTOR direction-of-use contrast (source as oracle vs. source as falsifier of documentation-derived claims) is precise and well-articulated.

- **S2. The task-intrinsic vs. family-specific split is well-motivated and the operationalization is non-trivial.** Defining task-intrinsic at the parameter level (a second family independently over-formalizes the *same* parameter) rather than verbatim, and showing the phenomenon concentrates in optional-default APIs and is absent on explicit-bound parameters via within-vendor contrast (Qdrant search params vs. collection params; Milvus search params vs. `M`/`nlist`/`dimension`), is a real piece of evidence rather than a slogan.

- **S3. Honest retrospective reporting.** The authors supersede their earlier single-vendor numbers (81% FP suppression / 96.7% recall on 16 candidates), disclose that the underlying data is "no longer recoverable," and replace them with a reproducible cross-vendor ensemble. They also disclose single-run variance (recall 15–78%) and the worst-case precision bound (45.8% if all 35 pending submissions are FP). This is more honest than the typical SE paper.

- **S4. Real maintainer-acknowledged defects.** 15 merged-PR fixes plus 16 open fix-PRs is a tangible artifact contribution that exceeds many testing papers' yield.

---

## Weaknesses

- **W1. [Major, fixable] The headline precision/recall numbers (67%/74%) rest on a small, non-random, retrospective sample and a single operating point chosen post hoc.**
  The RQ2 retrospective uses N=48 (27 TP, 21 FP), drawn from Milvus (32) and Qdrant (16) only, with no Weaviate representation. Within this sample the authors evaluate five runs and then *select* the 3-run any-confirmed union as the reported operating point because it "restores recall," explicitly justifying the union rule on the grounds that "under-confirmation is costlier than forwarding a false positive." This is a post-hoc choice of metric on data the authors also used to develop the method, and the paper does not report what the precision/recall would be at the *a priori* obvious alternatives (single run, any-confirmed at 2 runs, 4 runs, 5 runs) as a clean curve — they only give three isolated points (single, 3-run union @ 67%/74%, 5-run union @ 62%/85%, 5-run majority @ 64%/26%). The reader cannot tell whether the 3-run choice was the operating point the authors would have committed to *before* seeing the data. Combined with single-run recall swinging from 15% to 78% across five runs, the 74% figure has a defensible but narrow CI (Wilson 95% on the recall denominator: n=27, 20 hits → roughly [55%, 87%]) — not the clean "74%" headline the abstract implies.
  *Fix:* (a) commit to the operating-point rule *before* the retrospective and state the rule in the protocol; (b) report precision/recall at each k-run threshold (k=1..5) as a curve so the reader can see the trade-off rather than three cherry-picked points; (c) acknowledge the absence of Weaviate from RQ2 in the abstract, not only in the body.

- **W2. [Major, fixable] RQ3 sample sizes are too small for the claims made, and the most striking rate (behavior TI 11/11, CI [74%, 100%]) is on unstated ground truth.**
  The 18-clause parameter probe gives a TI rate of 6/18 with Wilson 95% CI [16%, 56%] — a 40-point span that does not support a precise quantitative claim, yet the text treats the rate as a finding ("the phenomenon concentrates in default-based parameters"). The behavior probe (n=11) reports 11/11 TI with Wilson CI [74%, 100%], which is presented as "the headline finding of this probe," but seven of the eleven behaviors are *not* maintainer-acknowledged — the authors themselves flag this ("The seven new behaviors are impl-confirmed idempotent but not separately maintainer-acknowledged"), yet the headline rate uses them. The "ground truth" for whether a behavior is task-intrinsic is *whether DeepSeek independently over-formalizes it*, which makes the rate partly definitional rather than empirical.
  *Fix:* (a) frame the 6/18 and 11/11 rates as point estimates with their CIs, not as established population parameters; (b) split the behavior headline into maintainer-acknowledged (4/4) and newly-probed (7/7) and present the 7/7 as a hypothesis-generating extension rather than pooling; (c) explicitly state the construct of "over-strict" relies on the authors' (or DeepSeek's) reading of the implementation as correct.

- **W3. [Major, partially fixable] The κ=1.0 cross-model check is on n=20 non-random, diversity-stratified candidates chosen by the authors.**
  The claim that the source-grounded verdict "does not appear family-specific when source evidence is explicit" rests on DeepSeek agreeing with GLM-5.2 on all twenty candidates, but the twenty are described as "diversity-stratified, non-random sample chosen to span input-validation, upsert-semantics, idempotent-drop, correct-reject, and dynamic-field subtypes." A non-random sample chosen to span subtypes cannot support a general claim about family-independence; it can only rule out family-specificity *on the strata the authors chose to sample*. Cohen's κ=1.0 on n=20 is also a single high-magnitude point estimate — the appropriate Wilson-style interval on the agreement proportion (20/20 → [83%, 100%] at 95%) already includes the possibility of substantial disagreement in the broader population.
  *Fix:* (a) state the claim as "no family-specific disagreement on these twenty strata" rather than as a general statement; (b) report the Wilson CI on the agreement proportion; (c) describe the sampling frame and how the strata were chosen (was the choice made before or after seeing GLM-5.2's verdicts?).

- **W4. [Major, not fixable without new experiments] The VDBFuzz head-to-head is n=1 per direction and cannot support even a directional claim.**
  The paper is admirably explicit that "Each direction is n=1; we treat these as hypothesis-generating controlled cases rather than a generalized result" — but then in the Discussion (§7) proposes a *structural hypothesis* ("a documentation-implementation oracle can reach a crash-class defect whose input violates a documented bound, while a crash oracle... does not reach a documentation-implementation defect that manifests as a silent accept") supported by these two n=1 cases. A structural hypothesis needs either a representative sample of crash-class/documentation-class pairs across versions and vendors, or a formal argument; two hand-picked versions where each tool's pet defect happens to reproduce cannot carry the claim. The reverse direction is also weakened by the authors' own observation that the failure is in VDBFuzz's *template suite* (`wait=true` hardcoded), not in the crash-oracle concept — making the asymmetry an artifact of VDBFuzz's current implementation rather than of crash oracles as a class.
  *Fix:* (a) tone the §7 hypothesis down to "we observe a directional pattern in two controlled cases and a structural explanation that we cannot establish at n=1; the VDBFuzz reverse-direction miss is also attributable to template coverage rather than to the crash-oracle concept per se, and disentangling the two requires a larger head-to-head that we leave to future work"; (b) make the template-coverage caveat as prominent as the structural hypothesis.

- **W5. [Medium, fixable] The 10 stale-closed "acknowledged but unfixed" TPs are counted as true defects on a weak criterion.**
  The paper counts the 10 stale-closed issues as true positives because "the maintainer acknowledged the issue rather than rejecting it, even though no merged-PR fix exists." This is a generous criterion: maintainers often acknowledge a report to be polite or to keep it on record without confirming the defect, and a stale close without a merged PR is, in many open-source projects, indistinguishable from a soft wont-fix. With these 10 included, the headline TP count is 49; excluding them it is 39. The abstract should report both.
  *Fix:* (a) report 39 fixed/open-PR + a separate line for "10 stale-closed with maintainer acknowledgement but no merged fix"; (b) report yield precision under both inclusions (the current 68.1% assumes all 10 are TP; excluding them as ambiguous would lower the rate).

- **W6. [Medium, fixable] The precision/recall gains over the "single-LLM baseline" are not on a like-for-like setup.**
  The baseline (48%/56%/37%) is "no source-grounded anchor," but the dev-reviewer with source also has the threat-model anchor and clean-reproduction anchor active. The three-condition ablation (source alone 9/12, threat-model alone 6/12, union 11/12) is on a *different, smaller* control (12-FP/4-TP, Milvus v2.6.19) than the 48-candidate retrospective used for the headline 67%/74%. So the headline recall gain (37%→74%) cannot be cleanly attributed to source grounding specifically — the gain is "dev-reviewer with all anchors" vs. "dev-reviewer with none," which is a comparison of pipelines rather than of the source-grounding contribution in isolation.
  *Fix:* run the 48-candidate retrospective with (a) dev-reviewer minus source anchor and (b) dev-reviewer minus all anchors, and report precision/recall for each, so the marginal contribution of source grounding is visible on the same data the headline uses.

- **W7. [Minor, fixable] Random-seed variance is acknowledged as a limitation but not bounded.**
  The paper states the dev-reviewer uses "default sampling, with no fixed random seed; we have not measured run-to-run variance and flag this as a limitation." Five-run recall swings from 15% to 78% — a 5× range — and the abstract reports 74% without that range. This is a substantial source of irreproducibility: a reader running TestVDB once could see recall anywhere in that band. The five runs that *are* reported also appear to have been conducted on the same retrospective data, so the band is conditional on that data and the true population band could be wider.
  *Fix:* (a) include the [15%, 78%] range alongside the 74% in the abstract; (b) discuss whether the union rule's 85% recall at 5 runs also comes with a comparable worst-case bound; (c) consider reporting the median single-run recall rather than only the union, since a single run is what a practitioner would actually perform.

- **W8. [Minor, fixable] Generalization claim to three VDBMSs is overstated given statistical claims rest on two.**
  The abstract leads with "across three VDBMSs" and "TestVDB demonstrates the approach at scale," but the threats-to-validity section concedes "statistical claims rest on Milvus and Qdrant." Weaviate contributes 13/30 acknowledged TPs but no source-grounded dev-reviewer numbers and only one over-strict probe (zero over-strict, attributed to explicit-bound documentation). The within-vendor contrast for Weaviate is also n=1 (delete on non-existent class).
  *Fix:* either run the RQ2 retrospective on Weaviate too, or rephrase "across three VDBMSs" as "across three VDBMSs for yield, with the controlled retrospective conducted on Milvus and Qdrant."

- **W9. [Minor, fixable] The "task-intrinsic" definition is partly circular.**
  Task-intrinsic is defined as "a second family's independent formalization of the same documentation is also over-strict on the same parameter." This means task-intrinsic status is established by DeepSeek's behavior, then used to evaluate DeepSeek's behavior (cross-model judging misses 3 of 6 TI clauses). The same model's outputs appear on both sides of the evaluation. The authors are aware that "the over-strict phenomenon concentrates in optional-default APIs" is a *separate* empirical signal, but the TI status itself is defined by the cross-model convergence they then evaluate.
  *Fix:* acknowledge explicitly that TI status is operationally defined by cross-model convergence and that this introduces a circularity; lean on the within-vendor contrast (default-based vs. explicit-bound) and the explicit-bound negative control (0/21) as the *independent* evidence that the phenomenon is real, not the 6/18 rate alone.

---

## Questions

1. **Operating-point selection.** Was the 3-run any-confirmed union rule committed to *before* the 48-candidate retrospective was unblinded, or after seeing the five single-run results? If after, please describe what rule you would have committed to ex ante and report the corresponding number. This is the central methodological question for RQ2.

2. **Cost of the dev-reviewer's source grounding.** The paper says wall-clock is "dominated by the dev-reviewer's source-grounding step, repository clone and source retrieval, and live Docker re-probes." Please report the wall-clock and token cost breakdown for a single target run, and specifically the marginal cost of the source-grounding step vs. the rest of the pipeline — readers cannot currently assess whether source grounding is practically affordable.

3. **The 21 explicit-bound negative control.** How were these 21 parameters sampled? Were they all the explicit-bound parameters in the three VDBMSs' documentation, a random subset, or chosen by the authors? If the latter, the 0/21 result is a stratum-level finding (no over-formalization where bounds are explicit) rather than a population finding, and the sampling frame should be described.

---

## Scores

| Dimension        | Score (1–5) | Notes |
|------------------|:-----------:|-------|
| Soundness        | **3**       | Method is reasonable and results are honestly reported, but headline precision/recall rest on a small retrospective with a post-hoc operating point, RQ3 CIs are wide, the κ=1.0 check is on n=20 non-random candidates, and the n=1 VDBFuzz head-to-head is over-interpreted in the Discussion. |
| Significance     | **3**       | 49 acknowledged defects and a clear framing of the source-ambiguity gap are real contributions; the method's reach is bounded to open-source VDBMSs and the headline effect sizes are too noisy to be the last word. |
| Novelty          | **4**       | The task-intrinsic vs. family-specific decomposition, the falsification (not oracle) use of source, and the documentation-style predictor (optional-default vs. explicit-bound) are genuinely novel contributions to the LLM-as-oracle literature. |
| Presentation     | **3**       | Mostly clear and well-organized, but the abstract overstates precision (no CI, no seed-variance range, no Weaviate caveat), and the n=1 VDBFuzz cases are foregrounded more than their evidentiary weight supports. |

**Overall: 4 / 10** (borderline — weak accept at best, lean reject without W1/W2/W4 addressed)

**Confidence: 4 / 5** (familiar with LLM-as-judge reliability and REST-API oracle literature; limited direct experience with the three target VDBMSs' internals)

## Reviewer 3 — Friendly

**Paper:** TestVDB: Source-Grounded Falsification of LLM-Derived Behavioral Claims for Documentation-Implementation Consistency Testing of Vector Databases

---

## Summary

The paper studies documentation-implementation consistency defects in Vector Database Management Systems (VDBMSs) — cases where the API silently accepts inputs that violate its own natural-language documentation (e.g., accepting `nprobe=0` or `ef=0` when the documentation implies a positive lower bound). These defects are argued to be largely invisible to crash, differential, metamorphic, and property-based oracles, because the documented boundary is natural-language prose rather than a formal contract.

The central conceptual contribution is a two-layer decomposition of the LLM-as-judge reliability problem: (1) a **family-specific** layer (self-preference) mitigated by cross-model validation, and (2) a deeper **task-intrinsic** layer, where ambiguous documentation causes different LLM families to converge on the same wrong clause, which cross-model validation cannot break. The paper then proposes **source-grounded falsification** (TestVDB): LLM-derived behavioral claims are treated as refutable hypotheses, and the implementation's actual behavior is used as an independent reference to falsify them — the opposite direction from MASTOR, which reads source as the oracle itself.

Empirically, TestVDB surfaced 107 issues across Milvus, Qdrant, and Weaviate, with 49 true-positive defects (15 merged-PR-fixed, 16 open fix-PRs, 18 maintainer-acknowledged). A controlled retrospective on 48 adjudicated candidates reports 67% precision / 74% recall (3-run ensemble) for the source-grounded dev-reviewer versus 37% recall without the source anchor. A probe over 18 over-strict clauses shows cross-model judging misses 3 of 6 task-intrinsic clauses while source-grounded falsification catches all 18, plus a behavior-level extension to 11 idempotency behaviors where the TI rate is much higher. A bidirectional VDBFuzz head-to-head is reported honestly as n=1 per direction, hypothesis-generating.

---

## Strengths

**S1. Genuinely novel framing: source-grounded *falsification* (not source as oracle).**
The most valuable conceptual move in this paper is the asymmetric direction in which source is used. MASTOR reads source to *generate* oracles encoding implemented behavior, which by construction cannot detect a gap between documentation and code. TestVDB reads source to *falsify* documentation-derived claims, targeting exactly that gap. This is a precise, defensible novelty claim that the paper makes carefully (§4, §6). The falsification framing — treating LLM-derived claims as refutable hypotheses — is elegant and connects to a much older Popperian tradition, which makes the idea feel principled rather than ad-hoc. It also yields a clean operational rule: a clause is over-strict iff the implementation accepts the value the clause rejects. This is the kind of crisp, mechanistic insight that makes the paper's core claim falsifiable and the contribution separable from the particular pipeline.

**S2. The task-intrinsic / family-specific distinction is a real analytical insight, well-scoped and well-tested.**
The decomposition of LLM-as-judge unreliability into a family-specific layer (self-preference, addressable by cross-model validation) and a task-intrinsic layer (shared ambiguity in the input, *not* addressable by cross-model validation) is, to my knowledge, novel in the testing literature. The paper is careful to scope it as an *extraction-level* property (a clause is task-intrinsic when a second family's independent formalization is also over-strict on the same parameter), and explicitly distinguishes it from the intra-judge self-inconsistency of Haldar et al. — a nuance many papers would blur. The eighteen-clause probe is well-designed: GLM and DeepSeek independently formalize, and the comparison is at the parameter level rather than verbatim, which is the right unit. The within-vendor contrast (Qdrant's default-based search parameters over-strict while its explicit-minimum collection parameters are not, with the same pattern reproduced independently on Milvus) is a strong piece of internal validity evidence that the phenomenon is driven by *documentation style* rather than vendor identity.

**S3. Honest, well-instrumented empirical work, including a bidirectional head-to-head and a falsifiable prediction.**
The paper does several things that friendly reviewers admire but rarely see done well: (a) the VDBFuzz comparison is bidirectional and runs on the version where *each* tool's target defect reproduces, not just the version favorable to TestVDB — the n=1-per-direction caveat is stated explicitly and the asymmetry hypothesis is reserved for the Discussion; (b) the 5-run variance (recall 15–78%) is disclosed rather than buried, and the union-vs-majority operating-point analysis (3-run union at 74% recall vs. 5-run majority at 26% recall) is a genuinely useful empirical contribution for anyone deploying LLM-based falsifiers; (c) the explicit-bound negative control (0/21 over-formalization on parameters documented with explicit bounds, with a tightened Wilson CI) is exactly the kind of negative result that turns a positive claim into a *predictive* one — the paper even states the falsifiable prediction: "optional-default + no explicit bound ⇒ over-formalization candidate." The cross-model κ=1.0 on the dev-reviewer verdicts across 20 diversity-stratified candidates is reassuring evidence that the *source-grounded verdict itself* is not family-specific, which closes a natural objection to the design.

**S4. Real-world impact: 15 merged-PR-fixed defects.**
15 merged fixes across Milvus, Qdrant, and Weaviate is a strong impact claim for a testing paper. The 16 open fix-PRs and 18 maintainer-acknowledged-but-unfixed further demonstrate that the findings are not paper-only. The Qdrant #9045 / #7967 root-cause case study (boundary fix resolving a recurring production panic that previous crash-site patches had not) is a compelling narrative for the Discussion.

---

## Weaknesses

**W1. `**[major, fixable]** Single-model backbone with no fixed seed; variance magnitude threatens reproducibility of headline numbers.**
The paper uses GLM-5.2 as the sole backbone for both extraction and the dev-reviewer, under default sampling with no fixed seed (§5). The 5-run variance on recall (15–78%) is substantial — a nearly 5x range — and while the union ensemble at 3 runs (74%) and 5 runs (85%) restores recall, the *precision* of those operating points rests on a thin per-run band (50–73%). The κ=1.0 cross-model check on the *verdicts* (DeepSeek vs. GLM-5.2 on 20 candidates) is reassuring for verdict stability, but it does not cover *extraction* stability, which is where the task-intrinsic claim lives. A friendly suggestion: report extraction-level stability across ≥3 GLM-5.2 runs and/or seed variation (the paper already flags "we have not measured run-to-run variance" — adding a small extraction-stability table, even on a subset, would meaningfully strengthen the headline TI rate). At minimum, the paper should clarify whether the RQ3 probe (n=18, n=11, n=21) was a single run or an ensemble, since the CIs hinge on it.

**W2. `**[Major, Fixable]** The 85% "residual" is a composition of TestVDB's findings, not a population estimate — but is sometimes read as the latter.**
The paper is mostly careful about this (the abstract says "this is the composition of our findings, not a population estimate"; §7 repeats the caveat). However, the Introduction and Contributions still feature "about 85% of the documentation-implementation defects we found are unreachable by differential, metamorphic, or property-based oracles" as a headline contribution, and the per-issue mapping is in the artifact rather than the paper. A friendly reviewer will want the *fault-model distribution table* in the main paper (or at minimum, a Table summarizing how many of the 107 fall into each classical class, with a one-line rationale per category aggregated to counts). This converts a verbal claim into something a reviewer can audit without fetching the artifact, and it strengthens rather than weakens the contribution. The "capture-recapture or unbiased defect sample" future-work note is appreciated.

**W3. `**[major, fixable]** The behavior-level TI probe (11/11) is the strongest result but rests on impl-confirmed rather than maintainer-acknowledged behaviors.**
The behavior-TI rate of 11/11 (Wilson 95% CI [74%, 100%]) is the most striking single number in RQ3, and the paper flags it as "the headline finding of this probe." Yet seven of the eleven behaviors are "impl-confirmed idempotent but not separately maintainer-acknowledged, which we flag to preserve the within-vendor parameter contrast." This is honest, but the asymmetry is worth sharpening: the parameter-TI finding (6/18) rests on maintainer-adjudicated cases, while the behavior-TI finding (11/11) rests on the authors' own impl-confirmation. A reader could reasonably worry that "idempotent API returns success where documentation implies an error" reflects a different (possibly by-design) category than "parameter accepts value documentation rejects." The paper's separate-reporting decision is correct; a short note in §7 clarifying that behavior-TI and parameter-TI are mechanistically distinct (the paper already says this) and should not be pooled for that reason would further insulate the claim. (The pooled 17/29 is reported "as an aggregate only," which is the right framing.)

**W4. `**[major, fixable]** Construct validity of "task-intrinsic" depends on a single second family (DeepSeek); a third family would materially harden the claim.**
The task-intrinsic-vs-family-specific distinction rests on two families (GLM, DeepSeek). A clause counts as task-intrinsic when DeepSeek *also* over-formalizes on the same parameter. But if a third family (say, Llama or a Qwen variant) disagreed, would that re-classify the clause as family-specific rather than task-intrinsic? The paper acknowledges "all source-anchor results use a single model family" but the TI definition itself uses only two. A friendly suggestion: run a third family on a *subset* of the 18 clauses (say, the 6 currently classified TI), to verify the stability of the TI classification. Even n=6 with a third family would be a large marginal evidence gain. If a third family is infeasible, the paper should add one sentence acknowledging this and noting it as the most valuable next experiment.

**W5. `**[Minor, Fixable]** The MASTOR-asymmetry novelty claim is crisp but compressed; a small concrete example would help.**
The claim "MASTOR reads source to generate oracles that encode implemented behavior, and so cannot detect a gap between documentation and code; TestVDB reads source to falsify documentation-derived claims" is the paper's sharpest differentiation. It is currently made in prose in §3, §4, and §7. A 2–3-line worked example (e.g., "if documentation says `nprobe ≥ 1` but source accepts `nprobe=0`, MASTOR encodes `nprobe ∈ ℕ` from source and reports no bug; TestVDB contradicts the doc-derived clause and reports a real defect") would make the asymmetry tangible to a reader who is not already familiar with MASTOR.

**W6. `**[minor, fixable]** Conclusion reports precision 67% / recall 74% without the 37% recall-without-source baseline that the Abstract already carries.**
The 67/74 operating point is reasonable but not eye-catching in isolation; the *differential* (37% → 74% recall when source grounding is added) is the result that actually sells the contribution. The Abstract already states this differential ("…versus 37\% recall without the source anchor"), and the Introduction mentions it once; the Conclusion (§9) reports only the absolute operating point. A one-phrase addition ("…versus 37% recall without the source anchor") in the Conclusion would bring its first/last-impression framing in line with the Abstract and materially strengthen the paper's closing.

---

## Questions

**Q1.** For the behavior-TI probe (11/11), were the 11 behaviors selected based on a pre-registered list of idempotency patterns, or chosen post-hoc from observed successes? If the latter, is there a risk that the 100% rate reflects selection of behaviors where over-formalization was already visible? A one-sentence answer about selection protocol would suffice.

**Q2.** The κ=1.0 cross-model check on verdicts uses 20 diversity-stratified candidates chosen to span 5 subtypes. Was the diversity stratification done before or after observing GLM's verdicts? (i.e., is the sample diverse on *inputs* or on *observed agreement*?) The paper says "diversity-stratified, non-random" — a half-sentence clarifying whether the subtypes were defined a priori would close a small but real construct-validity concern.

**Q3.** On the falsifiable prediction (optional-default + no explicit bound ⇒ over-formalization candidate): is this being used to *generate* new clauses in ongoing work? If the paper can show the predictor is being used prospectively (rather than only retrospectively validated on the existing 18), that would convert a strong correlative observation into a validated tool. The paper mentions a "larger head-to-head study is ongoing" — any prospective-deployment result from that would be valuable.

---

## Scores

| Dimension         | Score |
|-------------------|-------|
| Soundness         | 4     |
| Significance      | 4     |
| Novelty           | 5     |
| Presentation      | 4     |
| **Overall**       | **7** |
| Confidence        | 4     |

---

## Constructive Closing

This is a paper I would like to see accepted. The source-grounded *falsification* framing is a genuine and crisp conceptual contribution that separates the work cleanly from MASTOR and the broader REST-API oracle line. The task-intrinsic / family-specific distinction is, in my view, the right analytical lens for LLM-derived oracles on ambiguous documentation, and the within-vendor contrast plus the explicit-bound negative control are exactly the internal-validity checks one would ask for. The empirical work is honest about variance, honest about n=1 per direction in the VDBFuzz comparison, and honest about the 85% residual being a composition rather than a population estimate. The weaknesses above are all addressable in revision without new experiments in most cases; the one that would most improve the paper (third family on the TI subset, §W4) is a small, high-marginal-value follow-up. I lean accept.


## Verification

主 agent 回剥注释后论文逐条核实三份 review 的 weakness 批评是否成立（Valid/Misleading/False）：

| # | Source | Claim（weakness 摘要） | Verdict | Note |
|---|---|---|---|---|
| 1 | R1-W2/R2-W1/R3-W1 | 67%/74% 基于 N=48 + post-hoc 操作点 | **Valid** | 论文 §6 RQ2 line 144 确认 N=48；单 run 15-78%；union 最大化 recall |
| 2 | R1-W3/R3-W2 | 85% framing 分母是 TestVDB yield（circular） | **Valid** | 摘要 line 16 有 qualifier，但 Contributions bullet 2 + Intro 仍 headline framing |
| 3 | R1-W1/R2-W9/R3-W4 | RQ3 6/18 CI 宽 + TI 定义循环 | **Valid** | line 147 确认 6/18 CI；line 82/149 TI 由 DeepSeek 定义 |
| 4 | R1-W5/R2-W2 | 11/11 behavior TI 含 7 个非 maintainer-ack | **Valid** | line 149 自承认 |
| 5 | R1-W7/R2-W4 | VDBFuzz n=1 不能支撑 §8 hypothesis | **Valid** | §6 line 109 诚实；§8 line 209 overreach |
| 6 | R1-W1/R2-W3/R3-W1 | 单 LLM family (GLM-5.2) for source-anchor | **Valid** | line 189 自承认 |
| 7 | R2-W3/R3-W1 | κ=1.0 on n=20 非随机 | **Valid** | line 144/189 确认 stratified |
| 8 | R1-W2/R2-W7 | 单 run 方差来源未分析 | **Valid** | 论文披露方差未分析来源 |
| 9 | R2-W5(patched) | 10 stale-closed TP 计数宽松 | **Valid** (minor) | manual_fix tier 已说明 |
| 10 | R2-W8 | Weaviate 从 RQ2 缺失 | **Valid** | RQ2 仅 Milvus+Qdrant |
| 11 | R1-W6/R3-W3 | §8 generalization 未测试 | **Misleading** | §8 line 205 已标 future work |
| 12 | R2-W6(patched) | baseline vs headline 非 like-for-like | **Valid** | baseline 无 anchor，dev-reviewer 含 3 anchor |
| 13 | R3-W6(patched) | Conclusion 缺 37% baseline | **Valid** (minor) | 摘要有，结论缺 |

**核实结论**：绝大多数 **Valid**。1 条 Misleading。0 条 False（patch 后虚假 claim 已修正）。三份 review 事实基础扎实。

## Action Plan

**Must Fix**（多人共识 / Valid Major，不改大概率被拒）

- **[major, fixable]** RQ2 操作点：报告 k=1..5 PR 曲线 + 预注册规则 + 分析方差来源
- **[major, fixable]** 85% framing：重构摘要 + 贡献点；或补独立估计
- **[major, fixable]** RQ3 小样本：拆 maintainer-ack vs newly-probed；不 pool 17/29
- **[major, fixable]** VDBFuzz §8 overreach：scope §8；foreground template caveat
- **[major, fixable]** 第三 LLM family on TI subset（高 marginal value）

**Should Fix**（Misleading 或 minor-major）

- **[major, unfixable]** 单 family inherent limitation：标边界 + 补 κ Wilson CI
- **[major, fixable]** baseline like-for-like：48-candidate 上跑 minus source anchor
- **[minor, fixable]** Weaviate from RQ2：或跑 retrospective，或改摘要
- **[minor, fixable]** Conclusion 补 37% baseline
- **[minor, fixable]** 10 stale-closed 敏感性分析

**Optional**（个别 minor）

- **[minor, fixable]** §6 RQ1 段落拆分 / Table caption 49 vs 50 / notation / artifact link / MASTOR worked example

## Notes

态度半边（borderline 5.7）与 expertise 半边（ACCEPT）的张力是 dual-review 设计预期：态度用严格方法论视角看到拒稿信号；expertise 用深读+cache 看到 novelty delta 真实 + fixable。R2 的 4/10 是 swing vote——其拒稿信号全 fixable，解决后大概率升 weak-accept。

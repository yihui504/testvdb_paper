# Mock Review: TestVDB (ACM SIGCONF format)

**Reviewer:** Senior software-engineering reviewer (SE top-tier bar)
**Venue Target:** ICSE/FSE/ISSTA
**Confidence:** 4/5 (familiar with VDBMS testing, LLM-as-judge literature; implementation details not fully audited)
**Submission:** TestVDB: Source-Grounded Falsification of LLM-Derived Contracts for API-Conformance Testing of Vector Databases

---

## Summary

This paper introduces TestVDB, a tool for detecting API conformance defects in Vector Database Management Systems (VDBMSs). The authors argue that existing oracles (differential, metamorphic, property-based) cannot reach ~85% of conformance defects because accept/reject decisions against natural-language contracts do not compile to deterministic assertions. They propose an "LLM-as-oracle setting" where a language model serves as semantic judge, and identify a two-layer reliability problem: family-specific self-preference (mitigated by cross-model validation) and "task-intrinsic" contract errors where ambiguous documentation causes different LLM families to infer the same wrong contract (cross-model fails here). Their solution is "source-grounded falsification": treat LLM-derived contracts as refutable hypotheses and falsify them against source code, treating the implementation as ground truth. Across 5 VDBMSs, TestVDB surfaced 111 issues; maintainers acknowledged 38 as defects. A controlled retrospective shows the source anchor suppresses 81% of false positives (up from 31%) while retaining 96.7% true positives.

---

## Strengths

1. **Problem relevance and significance.** API conformance defects in VDBMSs are a real and costly problem. The connection to LLM-augmented applications (RAG depends on VDBMS correctness) is timely and significant. The roadmap and bug study citations establish this as an open challenge.

2. **Useful problem framing.** The "LLM-as-oracle setting" cleanly distinguishes problems requiring semantic judgment from those addressable by deterministic oracles. The boundary drawn against prior REST-API oracle work (AGORA+, SATORI, MASTOR) is conceptually sound and clearly explained in Section 4 and Table 1.

3. **Empirical grounding.** 111 submitted issues and 38 maintainer-acknowledged defects across 5 systems represent non-trivial real-world testing. The precision analysis (Wilson CI) and controlled retrospective design are methodologically stronger than typical "we found X bugs" papers.

4. **Novel insight on task-intrinsic errors.** The split between family-specific self-preference and task-intrinsic contract errors (ambiguous documentation shared across families) is a genuine contribution. The distinction that cross-model validation covers the former but not the latter is both intuitive and empirically motivated.

5. **Reproducibility artifacts.** The paper promises detailed prompts, target versions, per-token accounting, and Docker-pinned environments. This is above-average artifacting for a 5-page format.

---

## Weaknesses

### **[Major] M1: RQ3 experimental scale undermines the central C3 claim**

The paper's central novel claim (C3: task-intrinsic contract errors require source-grounded falsification; cross-model validation cannot resolve them) rests on a **single, small experiment**: 9 clauses from one VDBMS (Milvus), comparing GLM vs. DeepSeek. The paper itself acknowledges this as a "pilot" (Section 7, RQ3; §9), but the abstract and contributions present it as a core finding.

**Evidence:** Abstract line 19-20: "The natural automated ground truth that resolves task-intrinsic errors is the implementation." Section 4, line 91-93: "Cross-model judging missed both of the task-intrinsic subset, where DeepSeek read the ambiguous documentation as GLM had." Table 2 shows 9 clauses total.

**Why this is problematic:**
- **Sample size:** N=9 clauses is tiny. With only 2 task-intrinsic cases identified, the "2/2 missed by cross-model" observation is statistically anecdotal. A single different clause would change the rate to 50%.
- **Single-vendor scope:** All clauses are from Milvus. No evidence is provided that task-intrinsic errors exist in Qdrant, Weaviate, or other systems, nor that the DeepSeek/GLM pattern generalizes.
- **Model selection rationale:** The paper provides no justification for choosing GLM-5.2 and DeepSeek specifically. Are these families representative? Would GPT-4/Claude-3 show different patterns?
- **No statistical analysis:** No confidence intervals, significance tests, or power analysis for RQ3. Yet this is the primary novel contribution separating this work from prior cross-model validation approaches.

**Concrete fix required for camera-ready:**
1. **Expand RQ3 to minimum N=30 clauses** across at least 3 VDBMSs (Milvus, Qdrant, Weaviate) with 3+ LLM family pairs.
2. **Report with confidence:** Provide binomial CI or Bayesian posterior on "cross-model catch rate" for task-intrinsic subset. Current "2/2 missed" is anecdotal.
3. **Justify model selection:** Explain why GLM-5.2 and DeepSeek were chosen and discuss the space of LLM families.
4. **Qualify the claim in abstract/intro:** If RQ3 cannot be expanded, reframe C3 as "initial evidence on Milvus suggests..." rather than the universal claim currently presented.

Until RQ3 is expanded, the paper's central novelty claim is unsupported beyond the Milvus/GLM/DeepSeek corner of the space.

---

### **[Major] M2: "85% conformance residual" overstates classical oracle reach**

The abstract and intro claim that "about 85% of the conformance defects we found are unreachable by differential, metamorphic, or property-based oracles" (Abstract line 18-19; §1 line 40). This suggests that 85% of *all* VDBMS conformance defects fall into this residual. However, the evidence base is **111 submitted issues from one tool (TestVDB) on 5 systems**, not a systematic, unbiased sample of the defect space.

**Evidence:** Section 7, RQ1 line 120-122: "About 85% of the issues are conformance defects that classical oracles cannot reach." No population estimate, no capture-recapture, no discussion of selection bias.

**Why this is problematic:**
- **Selection bias:** TestVDB was *designed* to find LLM-oracle-reachable defects (conformance). The 111 issues are the tool's output, not a random sample from the ground-truth defect population. The "85%" is a conditional probability P(conformance | TestVDB-finds), not P(conformance | all-defects).
- **No ground truth denominator:** We do not know how many defects classical oracles *would* find on the same systems because TestVDB is not compared head-to-head against a metamorphic or differential testing baseline on identical targets.
- **Overclaim to "residual":** The paper uses "residual" to imply "what remains after classical methods are exhausted." But without a controlled comparison (classical oracle on same targets, same inputs), we cannot claim TestVDB reaches a *residual*—only that it found defects classified as conformance.
- **Inflated by design:** The 38 acknowledged defects include 31 fixed + 7 accepted-open, but the "85%" figure is on *submitted* issues (111). This includes issues that might be false positives, duplicates, or out-of-scope. Table 1 shows MeiliSearch contributed 0 acknowledged but 3 submitted.

**Concrete fix required:**
1. **Controlled baseline comparison:** Run a metamorphic testing baseline (e.g., MeTMaP-style) and differential testing on the same 5 VDBMSs with comparable test budget. Report overlap and unique yield. This is necessary to support "residual" claims.
2. **Reframe 85% as conditional:** "85% of the *issues TestVDB submitted* were classified as conformance defects not reachable by classical oracles" rather than "85% of conformance defects are unreachable."
3. **Report on acknowledged defects only:** Provide the breakdown on the 38 acknowledged defects (currently only in text: "89% on the 38 maintainer-acknowledged subset"). Acknowledged defects are a more reliable denominator than submitted.
4. **Discuss selection bias:** Add a threats-to-validity paragraph on selection bias in the 111-issue sample and how TestVDB's design influences the defect mix.

Without a controlled baseline, the "85% conformance residual" is an observation about one tool's output, not a claim about the defect space.

---

### **[Major] M3: Missing direct comparison against MASTOR/SATORI on same targets**

The Related Work section (§8) draws a sharp boundary between TestVDB and prior REST-API oracle work (AGORA+, SATORI, MASTOR), arguing they are "not in our setting" because they produce deterministic assertions (Section 4 line 88-89; §8 line 182). However, there is **no empirical comparison** against these tools on shared VDBMS targets to demonstrate that (a) they cannot find conformance defects, and (b) TestVDB finds defects they miss.

**Evidence:** Section 4 line 88-89: "each produces an oracle that remains an executable assertion, checked deterministically, so the LLM never issues a test verdict." Section 8 line 182: "MASTOR is the closest... but it reads source to generate oracles that encode implemented behavior and treats source as the truth, so by construction it cannot detect a gap between the documentation and the code."

**Why this is problematic:**
- **Unsubstantiated boundary claim:** The paper argues that prior work is "outside the LLM-as-oracle setting" by construction. But unless tested empirically, we do not know if MASTOR/SATORI *could* be applied to VDBMS conformance, perhaps with extensions. The claim rests on a theoretical distinction, not evidence.
- **No "cannot find" evidence:** No experiment shows MASTOR/SATORI on Milvus/Qdrant producing zero conformance defects. The theoretical argument ("they use deterministic assertions") is not a substitute for a controlled comparison.
- **Weakens novelty:** Without a comparison, reviewers cannot assess whether TestVDB's "LLM-as-oracle setting" is a fundamental distinction or a methodological choice that could be addressed within prior frameworks.
- **MASTOR contrast incomplete:** The paper contrasts MASTOR's source use ("generate oracles encoding implemented behavior") with TestVDB's ("falsify documentation-derived clauses"). But MASTOR could potentially add a documentation-read step to detect gaps. The paper does not explore this middle ground.

**Concrete fix required:**
1. **Run MASTOR/SATORI on Milvus/Qdrant:** Apply at least one prior tool to the same VDBMS endpoints. Report yield. If they find zero conformance defects, this *empirically* supports the setting-boundary claim.
2. **If direct comparison infeasible, expand discussion:** Explain *why* prior tools cannot be applied (e.g., "MASTOR requires OpenAPI spec; Milvus serves none") rather than assuming the theoretical distinction is sufficient.
3. **Qualify the "by construction" claim:** Add "to the best of our knowledge, prior tools in this line..." and acknowledge that extensions could bridge the gap.

A single controlled baseline (even N=1 system) would substantially strengthen the setting-boundary claim.

---

### **[Major] M4: Source-grounded falsification lacks ablation of anchor components**

The paper claims "the dev-reviewer's source anchor suppresses 81% of false positives, up from 31% without it" (Section 7, RQ2 line 142-143). However, the dev-reviewer applies **three anchors** (Section 5 line 108-109): "clean reproduction that re-probes the live API," "source-grounded verification," and "optional threat-model cross-check." It is unclear what "without it" means—is it no anchors at all, or only the source anchor removed?

**Evidence:** Section 5 line 108-109: "the dev-reviewer applies three anchors." Section 7, RQ2 line 142-143: "the dev-reviewer's source anchor suppresses 81% of false positives, up from 31% without it." No breakdown of anchor contributions.

**Why this is problematic:**
- **Attribution ambiguity:** Does "81% suppression" mean the source anchor *alone* achieves 81%, or that the three-anchor *system* achieves 81% and removing source drops it to 31%? The paper does not specify.
- **No individual anchor ablation:** Without per-anchor ablation, we cannot assess whether source-grounded falsification is the primary contributor or whether clean reproduction (live API re-probe) does most of the work.
- **Threat-model anchor unexplained:** The "optional threat-model cross-check" is never described or ablated. Is it used in the evaluation? If optional, when is it applied?

**Concrete fix required:**
1. **Report per-anchor ablation:** Provide precision/recall for (a) no anchors, (b) clean reproduction only, (c) source only, (d) all three. This isolates the source anchor's contribution.
2. **Clarify "without it":** Replace "up from 31% without it" with "up from 31% when only the clean-reproduction anchor is applied" (or whatever the baseline actually was).
3. **Explain threat-model anchor:** Describe what the threat-model cross-check is, when it's used, and ablate it.
4. **Artifact should include:** Full ablation data to enable reproducibility.

Without this, the "source anchor suppresses 81%" claim is not interpretable.

---

### **[Major] M5: Retrospective design unclear on adjudication pool and "pending-resolution" sensitivity**

The precision analysis reports "69.2% (Wilson 95% CI [55.7%, 80.1%])" and adds a "pending-resolution sensitivity" that widens the bound to "[43.9%, 80.5%]" (Section 7, RQ2 line 143). The paper does not explain: (a) what constitutes the adjudicated pool, (b) why "pending-resolution" exists (are some issues unresolved?), (c) how the worst-case bound is computed.

**Evidence:** Section 7, RQ2 line 142-143: "under pending-resolution sensitivity the worst-case bound widens to [43.9%, 80.5%]." No further explanation.

**Why this is problematic:**
- **Non-transparent adjudication:** Reviewers cannot assess selection bias in the adjudicated pool without knowing its size, composition, and adjudication criteria.
- **Pending-resolution ambiguity:** Does this mean issues are still awaiting maintainer response? If so, how many? How does this affect the denominator (is it 111 submitted - X pending)?
- **Worst-case bound derivation:** How is [43.9%, 80.5%] computed? If all pending are false positives, precision drops to 43.9%—this implies a large pending pool. But the paper provides no numbers.

**Concrete fix required:**
1. **Report adjudication stats:** How many issues were adjudicated? How many are pending? What are the adjudication criteria?
2. **Explain pending-resolution sensitivity:** Provide the formula/assumptions behind the worst-case bound. Is it "all pending are false positives"?
3. **Clarify denominators:** In Table 2 and RQ2, specify whether percentages are over submitted issues, acknowledged defects, or adjudicated pool.
4. **Artifact:** Include the adjudication log to enable reproducibility.

---

### **[Minor] m1: "Natural automated ground truth" is an overstatement**

The abstract calls the implementation "the natural automated ground truth" (line 19). This overstates. Source code expresses *actual* behavior, not *correct* behavior. If the implementation has a bug, treating it as ground truth will incorrectly falsify a correct LLM-derived clause.

**Evidence:** Abstract line 19: "The natural automated ground truth that resolves task-intrinsic errors is the implementation."

**Concrete fix:** Rephrase to "the automated proxy for ground truth" or "the practical ground truth." Add a sentence in §5 acknowledging that implementation bugs are a limitation and that the source anchor treats code *as if* it were correct. This weakens the "natural" claim while preserving the method's validity.

---

### **[Minor] m2: Model-free invariant oracle lacks methodological detail**

RQ4 (Section 7, line 171-172) describes a "model-free invariant oracle subclass" that detects "COSINE distance above 1 for identical vectors" and other mathematical violations. However, the paper does not explain how this oracle is implemented, how test inputs are generated, or how its results are validated.

**Evidence:** Section 7, RQ4 line 171-172: "a model-free invariant subclass detects violations of hard mathematical bounds." No methodology description.

**Concrete fix:** Add a 2-3 sentence description of the model-free oracle's implementation, test generation strategy, and validation. This is the "least design-contingent part of the evaluation" but currently lacks enough detail to assess its rigor.

---

### **[Minor] m3: LLM-as-oracle setting boundary could be sharper with a decision tree**

The LLM-as-oracle setting is defined textually in Section 4. A formal decision tree or flowchart would clarify the boundary and help readers classify other problems into/outside the setting.

**Evidence:** Section 4, line 86-87: "A testing problem belongs to the LLM-as-oracle setting when the pass/fail verdict cannot be issued by a deterministic assertion."

**Concrete fix:** Add a figure with a decision tree: "Is there a deterministic oracle? (Yes → classical setting; No → LLM-as-oracle setting)." This would strengthen the conceptual contribution.

---

### **[Minor] m4: Threats to validity conflate scope with statistical validity**

Section 7, "Threats to validity" (line 174-175) correctly notes that "generalization to Weaviate, MeiliSearch, and Chroma is breadth-only." However, it does not address statistical validity threats beyond RQ3's small sample, nor construct validity (e.g., are conformance defects actually distinct from correctness defects in ground truth?).

**Evidence:** Section 7, line 174-175: "Generalization to Weaviate, MeiliSearch, and Chroma is breadth-only."

**Concrete fix:** Expand the threats section to include:
- **Construct validity:** Are conformance defects correctly classified? Could some be correctness defects?
- **Statistical validity:** No power analysis for any RQ. Discuss this as a limitation.
- **Reliability:** Are LLM calls deterministic? Prompt reproducibility?

---

### **[Minor] m5: "111 submitted issues" includes by-design rejected cases**

The 111 submitted issues include cases that are "by-design" (intentional behavior) or "rejected" by maintainers. The paper does not break down how many of the 111 fall into these categories vs. acknowledged defects.

**Evidence:** Abstract line 21: "111 candidate issues across five VDBMSs; maintainers acknowledged 38 as defects." No breakdown of the remaining 73.

**Concrete fix:** Add a breakdown: of 111 submitted, X acknowledged defects, Y by-design, Z duplicates, W pending. This helps readers assess the 85% residual claim (is it inflated by by-design cases?).

---

### **[Minor] m6: Single-model evaluation for source anchor**

Section 7, "Threats to validity" notes that "All source-anchor results use a single model family (GLM-5.2)" (line 175). However, the cross-model ablation promise ("a full cross-model ablation of the dev-reviewer is open") is not scoped or prioritized.

**Evidence:** Section 7, line 175: "a full cross-model ablation of the dev-reviewer is open."

**Concrete fix:** Specify what a "full cross-model ablation" would entail (e.g., "run dev-reviewer with GPT-4, Claude-3, and DeepSeek on N adjudicated issues"). Without this, the limitation statement is vague.

---

### **[Minor] m7: No discussion of cost-effectiveness vs. manual testing**

The paper reports ~$10 per target and "comparable to a few hours of manual boundary testing" (Section 6, line 113). However, there is no cost-benefit analysis: is TestVDB more cost-effective than hiring a QA engineer for manual boundary testing?

**Evidence:** Section 6, line 113: "roughly $10 per target at current pricing, comparable to a few hours of manual boundary testing."

**Concrete fix:** Add 1-2 sentences comparing TestVDB's yield/cost to manual testing baselines (even rough estimates). This would strengthen the significance argument.

---

### **[Minor] m8: LLM-as-judge self-preference citation is tangential**

The paper cites Panickssery et al. (2024) for LLM-as-judge self-preference. That work studies "LLM evaluators recognize and favor their own generations" in text generation, not test oracle contexts. While the phenomenon is analogous, the direct link to VDBMS conformance is unstudied.

**Evidence:** Section 4, line 91-92: "This is the LLM-as-judge self-preference phenomenon (Panickssery et al.)."

**Concrete fix:** Add a clarifying sentence: "While Panickssery et al. study text generation evaluation, we observe an analogous bias in the test-oracle pipeline." This acknowledges the domain gap.

---

### **[Minor] m9: Abstract conflates "submitted" with "found"**

The abstract states "TestVDB surfaced 111 candidate issues" (line 21). However, 111 is the *submitted* count. The number of issues *surfaced internally* (pre-filtering) could be higher. The paper should clarify whether 111 is the raw output or post-novelty-gate.

**Evidence:** Abstract line 21: "TestVDB surfaced 111 candidate issues." Section 5 line 106 mentions a "novelty gate that removes duplicates and known issues."

**Concrete fix:** Specify whether 111 is pre- or post-novelty-gate. If post-gate, report the pre-gate count to give readers a sense of false-positive load.

---

## Questions for Authors

1. **On RQ3 scale:** The central C3 claim rests on N=9 clauses from Milvus. What was the rationale for stopping at 9? Can you commit to expanding to N=30+ across 3 VDBMSs for camera-ready? If not, how will you reframe the task-intrinsic claim to avoid overstatement?

2. **On classical oracle comparison:** Can you provide a controlled baseline comparing TestVDB against a metamorphic testing tool (e.g., MeTMaP-style) on the same VDBMSs? If not in scope for this venue, can you at least run MASTOR/SATORI on Milvus to empirically demonstrate they find zero conformance defects?

3. **On the 85% residual:** Is "85% of submitted issues" the same as "85% of all conformance defects"? If not, can you reframe the claim to be conditional ("85% of the defects TestVDB submitted were conformance defects") and discuss selection bias in the 111-issue sample?

4. **On anchor ablation:** What exactly does "31% without it" mean in the source anchor suppression claim? Is this no anchors, or only clean reproduction? Can you provide per-anchor ablation data?

5. **On adjudication:** How many issues are in the adjudicated pool? How many are pending-resolution? What is the derivation of the worst-case [43.9%, 80.5%] bound?

---

## Scores

| Dimension | Score (1-5) | Rationale |
|-----------|-------------|-----------|
| **Soundness** | 3/5 | Methodology is generally sound (controlled retrospective, precision CI), but RQ3's small sample (N=9) undermines the central C3 claim, and the "85% residual" overstates classical oracle reach without controlled comparison. |
| **Significance** | 4/5 | VDBMS conformance is a real and timely problem given RAG's dependence on VDBMS correctness. The problem is significant, but the "85% residual" is inflated and the generalizability beyond Milvus/Qdrant is breadth-only. |
| **Novelty** | 4/5 | The LLM-as-oracle setting framing and the task-intrinsic vs. family-specific split are novel contributions. However, the empirical support for task-intrinsic errors is thin (N=9). The source-grounded falsification concept is novel but not yet rigorously validated. |
| **Presentation** | 4/5 | Writing is clear and well-structured. Table 1 is excellent. The abstract/intro are concise. Minor presentation issues: some overclaims ("natural ground truth"), unclear adjudication details, missing baseline description in RQ4. |
| **Overall** | **Weak Accept** | The paper addresses a significant problem with a novel conceptual framing (LLM-as-oracle setting) and useful empirical grounding (111 issues, 38 acknowledged). However, the central novelty claim (task-intrinsic errors require source) is supported by only N=9 clauses from one system, and the "85% residual" overstates classical oracle reach without controlled baseline. The method is promising but needs larger-scale validation of RQ3 and a classical-oracle comparison to support the "residual" claim. If authors commit to expanding RQ3 and adding a baseline for camera-ready, this would be a solid **Accept**. |

---

## Meta-Review Notes

- **Top weakness:** RQ3's N=9 sample undermines the central task-intrinsic claim.
- **Secondary weakness:** "85% residual" overstates classical oracle reach without controlled comparison.
- **Overall band:** Weak Accept (borderline Accept pending major revisions to RQ3).

The paper is well-positioned for a top-tier venue if the authors address M1 (expand RQ3) and M2 (add classical oracle baseline). The conceptual contributions are solid; the empirical validation needs strengthening to match the venue bar.

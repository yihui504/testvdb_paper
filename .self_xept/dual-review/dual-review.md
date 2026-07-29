# Dual-Review Report — TestVDB v4（第四版）

> Paper: TestVDB v4（commit c26ed22：3-family cross-model κ + bootstrap CI + minus-source ablation + CouchDB/ES external validity + 20-agent 架构 + per-vendor 分析）
> Date: 2026-07-29 · 6 reviewer（3 态度 + 3 expertise）· **评分不合并**

## 顶层摘要

| 半边 | Verdict | vs v3 | vs v2 | vs v1 |
|---|---|---|---|---|
| **态度** | ~6.75/10，Weak Accept/Accept band（R1 客观 7.2 Accept / R2 严格 6 WA / R3 友好 7 Accept）| ≈（~7→6.75）| ↑ | ≈ |
| **expertise** | **ACCEPT**（unanimous Weak Accept × 3）| = | = | = |

**核心 framing 第四次确认站得住**（无 reviewer 质疑 doc-impl defect class + dev-reviewer source-grounded falsification 的基本贡献）。

**共识点**（[both] inherent limitation，文字已尽）：
1. post-hoc 操作点 selection-aware CI（6 reviewer 共识）—— 已 Bonferroni + bootstrap
2. cross-family / single-backbone —— 已 abstract caveat + 3-family κ
3. external validation 仅 portability —— 已 CouchDB/ES framing

**分歧点**（两半边视角不同，非合并）：
- VDBFuzz n=1 probe：态度 R2 批 underpowered（Valid minor）vs expertise R1 称 "strong reachability result" —— 同一证据两视角
- ensemble fairness：态度 R2 批 3-run vs single-run 不公平（核实 Misleading，ablation 已隔离 source 贡献）vs expertise 未提

## 四版对比（v1 → v2 → v3 → v4）

| | v1（初版）| v2（κ 修正+minus-source）| v3（abstract caveat+CouchDB）| **v4（3-family+bootstrap+ES+arch）** |
|---|---|---|---|---|
| 态度 | ~7 | ~6.5 | ~7 | **~6.75**（R1 升 Accept 7.2，R2 降 6，R3 7）|
| expertise Meta | ACCEPT（R1 Accept）| ACCEPT（全 WA，R1 Novelty Weak）| ACCEPT（全 WA，R1 Novelty Adequate）| **ACCEPT**（全 WA，五准则 consensus 全 Adequate）|
| R1 Domain Novelty | Excellent | Weak | Adequate | **Adequate**（stable，3-family + cache 核实后）|
| Verifiability | Adequate | Adequate | Excellent | **Adequate**（R3 denominator 误报 patch 后稳）|
| 核心 framing | 站得住 | 站得住 | 站得住 | **站得住** |
| 最强 weakness | post-hoc / κ=1.0 | cross-family / post-hoc | post-hoc / cross-family | **post-hoc / cross-family / external validation**（均 inherent）|

## Score Summary

| Dimension | 态度 R1 | 态度 R2 | 态度 R3 | exp R1 | exp R2 | exp R3 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Soundness | 4/5 | 3/5 | 4/5 | Adequate | Adequate | Adequate |
| Significance | 4/5 | 4/5 | 4/5 | Adequate | Adequate | Adequate |
| Novelty | 3/5 | 4/5 | 4/5 | Adequate | Adequate | Adequate |
| Verifiability | — | — | — | Adequate | Adequate | Adequate |
| Presentation | 4/5 | 4/5 | 4/5 | Weak | Adequate | Excellent |
| **Overall** | **Accept (7.2)** | **WA (6)** | **Accept (7)** | **Weak Accept** | **Weak Accept** | **Weak Accept** |

## Attitude Half

# Attitude Half — TestVDB v4（第三版 dual-review 态度半边）

> Target Venue: SE conference（ISSTA/ICSE/FSE tier）· Overall Prediction: Weak Accept · Date: 2026-07-29 · 3 reviewer（客观/严格/友好），评分不合并

## Score Summary

| Dimension | R1 (客观) | R2 (严格) | R3 (友好) |
|---|:---:|:---:|:---:|
| Soundness | 4/5 | 3/5 | 4/5 |
| Significance | 4/5 | 4/5 | 4/5 |
| Novelty | 3/5 | 4/5 | 4/5 |
| Presentation | 4/5 | 4/5 | 4/5 |
| **Overall** | **Accept (7.2/10)** | **Weak Accept (6/10)** | **Accept (7/10)** |

3 份完整 review：[r1.md](r1.md) / [r2.md](r2.md) / [r3.md](r3.md)

## Reviewer 1 — 客观审稿人
> Confidence: 4/5 · Overall: Accept (7.2/10)

**Strengths** — (1) 清晰 problem framing + Table 1 oracle-exclusion；(2) 49 maintainer-acknowledged TP 跨 3 VDBMS 的实证 grounding；(3) 两模式 FP diagnosis + multi-perspective baseline recall 崩塌（~80% precision → ~15% recall）；(4) source grounding 经 ablation（74→19%）+ 12-FP/4-TP triangulation 验证；(5) bidirectional VDBFuzz probe 方法论 sound。

**Weaknesses**
1. **[major, fixable]** Cross-family generalization 未充分 address（abstract framing 暗示广适用，但 κ=0.14–0.51 + recall 18–56% 显示 backbone-dependent）
2. **[major, fixable]** Post-hoc operating-point selection 无 pre-registration（Wilson CI 未校正四操作点选择）
3. **[minor, fixable]** Construct validity："implementation-as-correct" 假设未量化（23 rejected 中多少是 doc error）
4. **[minor, fixable]** External validity overstated（CouchDB/ES 0 defect，portability 非 generalization）
5. **[minor, unfixable]** Recall estimation absent（无 GT catalog，74% 是相对非绝对）

**Questions for Authors** — (1) 给定 κ，practitioner 如何选 backbone？(2) 何时用 5-run union？(3) 48-candidate non-random 的 bias？(4) CouchDB/ES mature API 严格校验是 maturity 还是 architecture 差异？

## Reviewer 2 — 严格审稿人
> Confidence: 4/5 · Overall: Weak Accept (6/10)

**Strengths** — (1) well-motivated problem（silent-accept 缺失）；(2) source-grounded falsification sound；(3) 49 TP + 15 merged-PR practical impact；(4) honest threat disclosure。

**Weaknesses**
1. **[major, fixable]** Post-hoc selection bias（48-candidate 是 tool-surfaced 后 adjudicated，非随机样本）
2. **[major, fixable]** Single-backbone（GLM-5.2）undercuts generalization（κ=0.14/0.37/0.51）
3. **[major, fixable]** 3-run ensemble vs single-run baseline 不公平比较（混淆 source grounding 与 ensemble）
4. **[minor, fixable]** VDBFuzz probe n=1 underpowered
5. **[minor, fixable]** CI 未含 post-hoc selection（abstract 引用未校正 67%/74%）
6. **[minor, unfixable]** 无 full defect space recall estimate
7. **[minor, fixable]** External mini-case observational 非 experimental

**Questions for Authors** — (1) selection bias mitigation（stratification）？(2) 3-run single-LLM baseline？(3) backbone property 与 performance 相关？(4) VDBFuzz fixed budget？(5) capture-recapture proxy？

## Reviewer 3 — 友好审稿人
> Confidence: 4/5 · Overall: Accept (7/10)

**Strengths** — (1) clear problem definition（crash vs doc-impl）；(2) dev-reviewer 是 LLM reliability 的 substantial contribution；(3) rigorous comparative evaluation（ablation + operating-point + cross-model）；(4) concrete artifacts + per-vendor nuance；(5) honest limitation。

**Weaknesses**
1. **[minor, fixable]** Cross-family under-explored（建议 pre-register cross-family validation set）
2. **[minor, fixable]** Post-hoc operating point（建议 Bonferroni CI 可视化）
3. **[minor, fixable]** RQ3 framing 应显式 "complementarity" 而非 "superiority"
4. **[minor, fixable]** Threat-model anchor under-specification

**Questions for Authors** — (1) mature REST API 严格校验 hypothesis？(2) κ variance 来自 extraction 还是 judgment？(3) confirmed TP 中有 doc bug 吗？

## Verification

主代理回剥注释论文逐条核实 weakness（三态 Valid / Misleading / False）：

| # | Source | Claim | Verdict | Note |
|---|---|---|---|---|
| 1 | R1-W1 / R3-W1 | "Cross-family generalization unaddressed / under-explored" | **Misleading** | abstract + §8 有 "single LLM backbone (GLM-5.2); cross-family generalization is an open question" caveat，§6 有 3-family κ（0.14/0.37/0.51）+ recall 18–56%；已探索非完全未 address，但 framing 可更紧 |
| 2 | R1-W2 / R2-W1 / R2-W5 / R3-W2 | "Post-hoc operating-point selection inflates uncertainty / CI 未校正" | **Valid** | 论文 §6 承认 + Bonferroni（[44,84]/[51,89]）+ bootstrap 2000（[53,83]/[71,96]）；residual 是 inherent（需 pre-registration） |
| 3 | R2-W3 | "3-run ensemble vs single-run baseline 不公平比较" | **Misleading** | 12-FP/4-TP ablation 隔离了 source grounding 贡献（source alone 抑制 75% FP + 保留全部 TP），minus-source 74→19% 证明 gain 主来自 source 非 ensemble；但补 3-run single-LLM baseline 对照表会更显式 |
| 4 | R2-W2 | "Single-backbone undercuts generalization" | **Valid** | inherent，论文标 open question + 3-family 数据 |
| 5 | R1-W4 / R2-W7 | "External validity overstated（CouchDB/ES portability only）" | **Valid** | 两个 non-VDBMS 均 0 defect（mature API 严格校验），论文已标 portability framing；Discussion transfer claim 可更 hedge |
| 6 | R2-W4 | "VDBFuzz probe n=1 underpowered" | **Valid** | 论文已标 "hypothesis-generating controlled cases"；abstract "complementary coverage" 与 n=1 略不平衡 |
| 7 | R1-W5 / R2-W6 | "Recall estimation absent" | **Valid** | inherent（无 public GT catalog），论文诚实承认；74% 是相对 37% baseline 非绝对 |
| 8 | R1-W3 | "Implementation-as-correct 未量化" | **Valid** | §8 提 limitation 但未量化 23 rejected 中 doc-error 比例；minor |
| 9 | R3-W3 | "RQ3 应 framing 为 complementarity" | **Misleading** | 论文 §6 已 frame 为 bidirectional reachability + complementarity，非 superiority；个别措辞可调 |

## Action Plan

**Must Fix** — 多人共识 Valid major
- post-hoc operating-point selection（R1/R2/R3 + expertise 共识）：论文已有 Bonferroni + bootstrap，**residual 是 inherent limitation**——根本解决需 pre-registered 选择规则，非文字修改能消除。文字层面已尽。

**Should Fix** — Misleading（表述/对照可改进）
- cross-family framing（R1-W1 / R3-W1）：abstract caveat 已有，§6 可更显式标 "backbone-specific"（与 expertise R1 3.3 一致）
- ensemble fairness（R2-W3）：补 3-run single-LLM baseline 对照表（ablation 已实质做了，显式化更清楚）
- RQ3 措辞（R3-W3）：确保 §6 一致用 "complementary" 而非 "superiority"

**Optional** — 个别 minor / 锦上添花
- residual FP 分类（~8/48，与 expertise R1 3.6 一致）
- implementation-as-correct 量化（audit 23 rejected）
- VDBFuzz fixed-budget run（强化 complementarity）
- threat-model anchor 细节附录

## Overall Prediction
**Weak Accept / Accept band**（2 Accept + 1 Weak Accept，均分 ~6.75/10；vs v3 ~7 持平）。核心 framing 第三次确认站得住，最强 weakness（post-hoc）是 inherent limitation 且文字已尽（Bonferroni + bootstrap + open question + portability framing）。比 v3 改善点：R1 Objective 从 ~7 升 Accept 7.2（minus-source ablation + 3-family + bootstrap 提升信任）；R2 Strict 的 unfair-ensemble 批评经核实为 Misleading（ablation 已隔离 source 贡献）。

---

## Expertise Half

# Expertise Half — TestVDB v4（第三版 dual-review expertise 半边）

> 3 expertise reviewer（Domain Expert / Area Specialist / General）+ Meta-Review。checker 已过：R2 Haldar-fabricated、R3 denominator 误报已 patch。

## Reviewer 1: Domain Expert

**Overall Recommendation:** Weak Accept

### Summary

TestVDB targets documentation-implementation defects in Vector Database Management Systems (VDBMSs) — a class of logical bugs where a VDBMS silently accepts inputs or behaviors that violate its API documentation (e.g., accepting `nprobe=0` when documentation specifies range `[1, 16384]`). Because the boundary is specified in natural-language prose, deterministic oracles (crash detection, differential testing, metamorphic relations, property-based testing, REST-API tools that rely on structured sources) cannot adjudicate these accept/reject decisions. The paper instantiates a four-stage LLM pipeline (claim extraction, test generation, sandboxed execution, defect confirmation) that uses LLMs to read documentation, generate tests, and judge conformance. Two failure modes produce false positives: hallucination in extraction (LLM invents constraints the documentation doesn't state) and self-preference bias in judgment (same-family LLM confirms its own extracted claims). A multi-perspective judging baseline raises precision but collapses recall. The paper introduces a dev-reviewer agent that acts as a source-grounded falsifier, reproducing each candidate independently and cross-checking against implementation source to suppress false positives. TestVDB surfaced 107 issues across three VDBMSs (Milvus, Qdrant, Weaviate); maintainers acknowledged 49 as true-positive defects, with 15 fixed via merged PR. On a 48-candidate retrospective, the dev-reviewer reaches 67% precision and 74% recall (3-run ensemble) against 37% recall without the source anchor. A bidirectional probe against VDBFuzz on Qdrant shows complementary coverage.

### Core Strengths

- **S1:** Well-motivated problem — documentation-implementation defects are a prevalent, impactful defect class that existing VDBMS fuzzers miss (44 of 49 true positives in this paper's results do not crash).  — see 2.1, 3
- **S2:** Sound exclusion argument — Table 1 shows principled reasons why each deterministic oracle class cannot reach the documentation-implementation residual, making the LLM-as-oracle choice well-justified.  — see 2, 7
- **S3:** Demonstrated practical impact — 49 maintainer-acknowledged defects across three production VDBMSs, with 15 already fixed via merged PR, shows the approach finds real bugs.  — see 6
- **S4:** Source-grounded falsification contribution — The dev-reviewer's three-check design (independent reproducibility, evidence sufficiency, falsifiability) is a genuine technical advance over single-LLM and multi-perspective baselines.  — see 5

### Core Weaknesses

- **W1:** Single-backbone evaluation — All dev-reviewer results use only GLM-5.2; cross-model re-run shows verdict is family-specific (κ = 0.14–0.51 vs. other families), so the headline 67%/74% precision/recall may not generalize.  — see 6.2
- **W2:** Limited external validity — Controlled retrospective covers only Milvus and Qdrant (48 candidates); Weaviate results are yield-only without controlled analysis. Non-VDBMS transferability (CouchDB, Elasticsearch) is exploratory only.  — see 6.3, 8
- **W3:** Operating point selection — The 3-run union ensemble is selected post-hoc from four operating points; Wilson CIs don't account for this selection, and no pre-registered rule justifies the choice.  — see 6.2
- **W4:** No false-negative quantification — Paper acknowledges dev-reviewer can wrongly suppress true defects when implementation is buggy but documentation is right; false-negative rate is not estimated.  — see 8

### Detailed Assessment

1. **Significance** — Adequate

- **1.1** **Well-motivated problem.** Documentation-implementation defects are a logical-bug majority that crash-oracle fuzzers miss. The paper grounds the problem in an empirical bug study (bugstudy25) and VDBMS testing roadmap (roadmap25), showing 43% of VDBMS bugs stem from incorrect behavior and >50% manifest as functional failures. The 49 maintainer-acknowledged defects across three production systems demonstrate practical relevance.

- **1.2** **Clear impact.** The 15 merged-PR fixes (plus 16 open fix-PRs) across Milvus, Qdrant, and Weaviate represent tangible impact. These are not hypothetical findings — maintainers applied patches, confirming the defects are real and worth fixing.

- **1.3 [major, fixable]** **Unclear scope boundaries.** The paper focuses on "documentation-implementation defects" but does not clearly delimit what counts as documentation (API docs? README? comments?) versus what counts as implementation (HTTP handlers? storage layer?). §2 separates consistency from correctness, but the boundary between "accept/reject behavior" (consistency) and "returned result correctness" is fuzzy in practice. For example, if a VDBMS silently accepts an invalid `ef` parameter and returns wrong recall due to it, is this a consistency defect (accepted invalid input) or a correctness defect (wrong ANN result)? The paper treats it as consistency, but the root cause may be correctness-focused (bad index parameters affect search quality). This conceptual blurring undermines clarity of the defect class.

- **1.4 [minor, fixable]** **Limited generalization evidence.** §8 claims transferability to "structurally similar documentation regimes" (REST APIs without OpenAPI, config validation, policy-as-code), but the only non-VDBMS probes (CouchDB, Elasticsearch) are exploratory method-portability tests, not defect-detection evaluations. Both systems rejected all invalid probes with 400 errors; the only silent-accepts (`limit=0`, `size=0`) returned empty result sets, which the paper calls "graceful behavior rather than a defect." This suggests mature non-VDBMS APIs validate strictly, so the defect class may be VDBMS-specific (immature tooling, rapid development) rather than documentation-regime-general. A single non-VDBMS case study where the tool actually finds defects would strengthen the generalization claim.

2. **Novelty** — Adequate

- **2.1** **Clear delta from VDBFuzz.** VDBFuzz (vdbfuzz26) is the closest VDBMS testing work; it uses crash as its oracle via template-based input mutation. TestVDB's novelty is well-differentiated: it targets silent-accept defects (non-crashing), uses an LLM-derived oracle for natural-language documentation semantics, and introduces source-grounded falsification. The bidirectional probe (RQ3, §6.3) concretely demonstrates complementarity: TestVDB reaches VDBFuzz's integer-overflow crash by contract reasoning (size=2^63 is documented-valid yet panics), while VDBFuzz misses TestVDB's #9045 (wait=false accepts zero-length vector) under current templates. This is a strong bidirectional reachability result that shows neither approach subsumes the other.

- **2.2** **Well-positioned against REST-API oracle tools.** The paper's characterization of MASTOR (mastor26), SATORI (satori25), and AGORA+ (agoraplus25) in §7.2 and Table 1 is structurally sound on first principles:
- MASTOR reads source to encode *implemented* behavior → by construction cannot detect documentation-implementation gaps (it would encode the implementation as oracle, missing the violation)
- SATORI reads OpenAPI schema fields (type, format, min, max) → VDBMS documentation carries these constraints in prose without schema fields, so SATORI's extraction has no input
- AGORA+ infers from traffic → limited to exercised inputs; novel boundary probes (e.g., nprobe=0) don't appear in typical traffic

The paper's claim that TestVDB "reads source as a falsifier of documentation-derived claims and targets exactly that gap" is a genuine delta over MASTOR's "source-as-oracle" approach. The three-check design (independent reproducibility, evidence sufficiency, falsifiability) is novel relative to the REST-oracle line.

- **2.3 [minor, fixable]** **Limited coverage of LLM-as-oracle prior work.** §7.3 cites self-preference bias (panickssery24, wataoka24), hallucination (ji23hall), and intra-judge inconsistency (haldar25), but misses several highly relevant works on LLM-as-judge reliability that strengthen the problem framing:
- **Liu et al., "LLM-as-a-Judge" (various venues, 2023-2024):** Established the self-preference bias the paper builds on; more precise citation would strengthen motivation.
- **Zheng et al., "Large Language Models as Judges for Evaluating Alignment" (ICLR 2024):** Shows LLM judges correlate poorly with human judges on nuanced semantic tasks, which directly motivates the dev-reviewer's source-grounding.
- **LLM-as-judge calibration work (e.g., "Judging LLM-as-a-Judge," various 2024 workshops):** Shows that LLM judges are high-variance and benefit from external grounding, which aligns with the dev-reviewer design.
These are not missing per se (the paper cites the core phenomenon), but more precise citation of the LLM-as-judge reliability literature would strengthen the problem motivation. The current citations (panickssery24, wataoka24, haldar25) are sufficient but not maximally authoritative.

- **2.4** **Clear delta from documentation-derived oracle line.** §7.4 cites Toradocu (toradocu16), Doc2OracLL (doc2oracll25), AugmenTest (augmentest25), ChatAssert (chatassert24), and Testora (testora26). TestVDB's novelty is well-differentiated:
- Toradocu uses deterministic NLP for Javadoc @throws → handles simple patterns but acknowledges false positives without correction
- AugmenTest/ChatAssert verify via runtime behavior (compilation, differential execution) → still treat LLM as final semantic arbiter
- Testora uses PR descriptions as regression oracle → 55% precision even with multi-question classifier
TestVDB differs by using *implementation source* (not runtime behavior) as independent verification, breaking self-preference. The dev-reviewer's falsifier semantics (survives all three checks → defect; fails any → suppress) is a clear contribution over "LLM + runtime feedback" approaches.

3. **Soundness** — Adequate

- **3.1** **RQ1 evaluation sound.** The 107-submission yield with 49 maintainer-acknowledged true positives (68.1% precision on adjudicated set; 45.8% worst-case bound treating all pending as false positives) is reasonable. The paper correctly reports both the adjudicated-only precision (68.1%) and a conservative worst-case bound (45.8%), acknowledging uncertainty around the 35 still-pending submissions. The 15 merged-PR fixes are strong evidence that findings are real.

- **3.2** **RQ2 evaluation generally sound but with notable limitations.** The 48-candidate retrospective (27 TP, 21 by-design/rejected) is a reasonable controlled dataset. The dev-reviewer's headline 67% precision / 74% recall (3-run union) is meaningfully above the single-LLM baseline (56%/37%). The ablation (Table 4) on 12-FP/4-TP control shows source grounding suppresses 75% of false positives while retaining all TPs, and the source-disabled collapse (74% → 19% recall) triangulates source grounding's contribution. These controls are adequate to support the claim that source grounding lifts recall above baseline.

- **3.3 [major, fixable]** **Single-backbone evaluation limits generalizability.** All dev-reviewer results use GLM-5.2. The cross-model re-run (DeepSeek, Qwen-3.8-Max, LongCat-2.0) shows verdict is family-specific (κ = 0.14–0.51 vs. GLM single-run), and all three families recall fewer defects (18–56% vs. GLM's 85% single-run, though the paper reports 74% for 3-run union). This is a significant limitation: the headline precision/recall numbers are GLM-5.2-specific, not properties of the dev-reviewer design itself. The paper acknowledges this ("we cannot claim cross-family robustness") but does not quantify how much variance is due to architecture vs. sampling. A sensitivity analysis showing precision/recall variance across (say) 5 families would clarify whether the dev-reviewer reliably improves over single-LLM regardless of backbone, or whether GLM-5.2 is uniquely good at this task. As stated, the 67%/74% headline may mislead readers into thinking these are properties of the method rather than of GLM-5.2.

- **3.4 [major, fixable]** **Post-hoc operating point selection without pre-registration.** The paper reports four operating points (single run, 3-run union, 5-run union, 5-run majority) and selects the 3-run union as the headline because it "sits at the knee of the precision-recall trade-off." This selection is post-hoc, and the Wilson CIs reported ([49%, 81%] for precision, [55%, 87%] for recall) do not account for selection across the four operating points. The paper acknowledges this ("the Wilson CIs... do not account for this selection") and provides a Bonferroni correction that widens CIs to roughly [44%, 84%] and [51%, 89%], plus a bootstrap validation (2000 resamples, 2000 candidates) giving [53%, 83%] and [71%, 96%]. These corrective analyses are commendable but feel patched-on. A stronger design would pre-register the operating-point selection rule (e.g., "we will use any-confirmed ensemble as the operating point because falsifier semantics imply under-confirmation is costlier than forwarding false positives") and report CIs that do not require post-hoc correction. The current analysis is adequate but not ideal.

- **3.5 [minor, fixable]** **Per-vendor analysis shallow.** The paper reports per-vendor yield (Table 3: Milvus 22 TP / 51 submitted, Weaviate 13/30, Qdrant 14/26) and per-vendor retrospective performance (Milvus 69%/73%/80% accuracy/precision/recall; Qdrant 56%/50%/57%), but does not analyze *why* performance differs. Milvus's lower precision (73% vs 80% overall) and higher recall (80% vs 74%) may reflect documentation style (Milvus concentrates defects in optional-default parameters where documentation omits explicit bounds). A deeper per-vendor analysis linking documentation style to dev-reviewer performance would strengthen understanding of when the approach works best.

- **3.6 [minor, fixable]** **Limited analysis of remaining false positives.** On the 48-candidate retrospective, the dev-reviewer still produces ~16% false positives (8 of 48, assuming 67% precision on 27 TP → ~40 total confirmed, meaning ~8 false positives escaped suppression). The paper does not characterize these remaining FPs: are they hallucination failures? Source-grounding failures? Threat-model coverage gaps? Understanding the residual FP mode would clarify the method's boundaries.

4. **Verifiability** — Adequate

- **4.1** **Sufficient method description.** §4 (TestVDB Approach) describes the four-stage pipeline in sufficient detail to understand the method: claim extraction (contract-formalizer agent reads docs, emits JSON claims), test generation (attack agents generate probes), sandboxed execution (Docker-pinned instances), defect confirmation (judge compares documented expectation vs. actual response). The dev-reviewer's three-check design (Figure 4) is clearly explained. Reproduction would require access to the agent prompts and target versions, which the paper states are in the artifact to be released.

- **4.2 [minor, fixable]** **Limited artifact availability at review time.** The paper states "artifact... we will release at a persistent URL upon acceptance," which means reviewers cannot verify the implementation now. The LLM prompts, per-token accounting, and target versions are described in text but not provided in the paper. For full verifiability, the artifact (or at minimum: representative prompts, the 20 agent role definitions, and a reproduction script for the 48-candidate retrospective) should be available during review. The paper's claim of "~10^4 LLM calls, ~$10 per target" is credible but not verifiable without artifact access.

- **4.3** **Sufficient evaluation reporting.** RQ1 (Table 3), RQ2 (Tables 4–6, Figure 6), and RQ3 (Table 7) report sufficient statistics to follow the analysis. The Wilson CIs, bootstrap validation, and Bonferroni correction are appropriate statistical rigor. The per-vendor breakdowns and threat-model anchor analysis are adequate to trace the results.

- **4.4 [minor, fixable]** **Incomplete ground-truth reporting.** The paper reports 27 TP / 21 by-design-rejected on the 48-candidate retrospective, but does not list which specific issues are in each category. Without this list, a reviewer cannot verify the precision/recall calculation or identify patterns in the remaining FPs/FNs. Providing the 48-issue IDs with ground-truth labels in an appendix would strengthen verifiability.

5. **Presentation** — Weak

- **5.1** **Generally clear structure.** The paper follows a logical flow: motivation → problem setup → method → false-positive analysis → dev-reviewer → evaluation → related work → discussion. The four-stage pipeline (Figure 1) and dev-reviewer three-check design (Figure 4) are visually clear. Table 1 (oracle exclusion argument) is effective.

- **5.2 [minor, fixable]** **Dense writing in key sections.** §6 (Evaluation) packs many results into limited space. The RQ2 subsection in particular toggles between the 48-candidate retrospective, the 12-FP/4-TP ablation, the source-disabled collapse, the cross-model re-run, per-vendor analysis, and multi-perspective comparison without clear visual signposting. A table or figure summarizing the relationship between these different analyses (which is main result vs. which is control) would help readers navigate.

- **5.3 [minor, fixable]** **Inconsistent notation.** The paper uses Wilson CIs in some places (Table 6) and bootstrap CIs in others (Table 6 text, §6.2). The relationship between these is explained but could be clearer. Figure 6's "per-run band" for single-run results (15–78% recall) is not defined — does it show min-max across 5 runs? A figure caption or footnote would clarify.

- **5.4 [minor, fixable]** **Missing definitions.** §6.2 introduces "any-confirmed ensemble" and "majority voting" without defining them precisely. From context, any-confirmed = union across runs (candidate confirmed if any run confirms it), majority = candidate confirmed if ≥3 of 5 runs confirm it. A formal definition would avoid ambiguity.

- **5.5 [minor, fixable]** **Typos and minor issues.**
- Abstract: "future work" phrasing is vague ("cross-family generalization is an open question" is stated without framing what work remains)
- Table 6: Wilson CI brackets are inconsistent with text (text reports [55, 87] for recall, table shows [55, 87] — these match, but precision shows [49, 81] in table vs. [49, 81] in text; redundant check needed)
- §6.3: "Each direction is n=1" appears twice; consolidate
- Figure 6 caption: Could explicitly state that the 3-run union is the headline operating point

### Questions

- **Q1 (relates to 3.3):** What is the minimum cross-family performance required to claim the dev-reviewer's benefits are backbone-independent? If GLM-5.2 achieves 67%/74% and DeepSeek achieves 18%/56%, is the dev-reviewer design robust or backbone-specific? A sensitivity analysis across more families would clarify.

- **Q2 (relates to 3.4):** If the 3-run union were pre-registered as the operating point (justified by falsifier semantics: "under-confirmation is costlier than forwarding false positives for human triage"), would the Bonferroni correction be unnecessary? Can you reformulate the operating-point selection as a pre-registered rule rather than a post-hoc choice?

- **Q3 (relates to 2.3):** Can you cite the most authoritative LLM-as-judge reliability papers (e.g., Zheng et al. ICLR 2024) to strengthen the problem motivation? The current citations are sufficient but not maximally precise.

- **Q4 (relates to 3.6):** Can you characterize the ~8 remaining false positives (out of 48 candidates) that the dev-reviewer fails to suppress? Which of the three checks (reproducibility, evidence sufficiency, falsifiability) failed for each? This would clarify the residual failure modes.

---

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

---

## Reviewer 3: General Reviewer

**Overall Recommendation:** Weak Accept

### Summary
TestVDB targets documentation-implementation defects in Vector Database Management Systems (VDBMSs)—cases where a VDBMS silently accepts inputs that violate its API documentation. Because documentation boundaries are expressed in natural-language prose rather than structured schemas, deterministic oracles (crash detection, differential testing, metamorphic relations) cannot adjudicate these accept/reject decisions, leaving an LLM-derived oracle as the practical option. The paper presents TestVDB, a four-stage pipeline (claim extraction, test generation, execution, defect confirmation) that uses LLMs to read documentation, generate tests, and adjudicate responses. The key technical contribution is a dev-reviewer agent that acts as a source-grounded falsifier, reproducing each candidate defect against implementation source to suppress two LLM failure modes: hallucination in claim extraction and self-preference bias in judgment.

The paper reports 107 submitted issues across three VDBMSs (Milvus, Qdrant, Weaviate) with 49 maintainer-acknowledged true-positive defects (15 fixed via merged PR). On a controlled retrospective of 48 maintainer-adjudicated candidates, the dev-reviewer reaches 67% precision and 74% recall (3-run ensemble), versus 37% recall without the source anchor. A bidirectional probe against VDBFuzz explores complementary coverage: TestVDB reaches a crash-class defect by contract reasoning, while VDBFuzz misses a TestVDB silent-accept defect under its current templates.

### Core Strengths
- **S1:** Well-motivated problem with clear structural reasoning for why deterministic oracles miss the documentation-implementation residual (Section 2, Table 1) — see 1.1, 2.1
- **S2:** Coherent four-stage pipeline design with clear role separation and a falsifier architecture that addresses both identified failure modes (Section 3, Figure 1) — see 3.1, 3.2
- **S3:** Rigorous ablation design that triangulates the source anchor's contribution through multiple configurations (Section 6, Tables 4–6) — see 3.3, 4.1
- **S4:** Candid threat disclosure that flags the post-hoc operating point selection and cross-family generalization gap (Section 6) — see 4.2

### Core Weaknesses
- **W1:** Novelty positioning has a gap — Related Work cites AGORA+, SATORI, MASTOR as REST-API oracle tools from structured sources, but AugmenTest (the most directly comparable work) uses LLMs to infer oracles from available documentation and is buried late in Section 7 rather than upfront in positioning; the paper's "LLM-derived oracle" framing should acknowledge this closer lineage earlier — see 2.2 [major, fixable]
- **W2:** External validation claim overreach — Section 6 claims transfer to Apache CouchDB and Elasticsearch based on a single end-to-end run each, yet both mature APIs strictly rejected invalid probes (only silent-accept was limit=0 returning empty sets), which the paper interprets as "probing method portability rather than defect detection"; this is insufficient evidence for the broad transferability claim in Discussion — see 4.3 [major, fixable]
- **W3:** Worst-case-bound labeling in the abstract — the abstract states 49/107 (45.8%) alongside the 49 acknowledged count; the 45.8% is a worst-case bound (treating 35 pending as false positives) that the body (line 232) labels as such, but the abstract does not carry the "worst-case bound" label, so a casual reader may conflate it with adjudicated precision (49/72 = 68.1%). Surfacing the label in the abstract would remove the conflation — see 4.1 [minor, fixable]

### Detailed Assessment

1. **Significance** — Adequate
- **1.1** The problem is well-motivated with clear practical impact: Section 1 establishes that more than half of VDBMS bugs manifest as functional failures (cite bugstudy25) and that crash-oracle fuzzers miss the silent-accept majority (44 of 49 true positives). The framing of documentation-implementation defects as a distinct class with real consequences (wrong context reaching LLMs) establishes significance.
- **1.2** The scope is limited to VDBMSs, which constrains impact. The paper claims structural transferability to other natural-language documentation regimes (REST APIs without OpenAPI, configuration validation, policy-as-code) in Section 8, but the evaluation is VDBMS-only, and the CouchDB/Elasticsearch probes are too weak to substantiate broad generalization. The contribution is meaningful but narrow.

2. **Novelty** — Adequate
- **2.1** The paper clearly positions TestVDB within a well-mapped space. Table 1 is a strong exclusion argument that walks through why standard oracles (crash, differential, metamorphic, property-based) miss the documentation-implementation residual, leaving an LLM-derived oracle as the structural residual. This is a well-executed novelty framing.
- **2.2 [major, fixable]** Related Work positioning has a gap. Section 7 cites AGORA+, SATORI, MASTOR as structured-source REST-API oracle tools, then discusses LLM-as-judge reliability and documentation-derived oracles (Toradocu, Doc2OracLL, ChatAssert, Testora), but AugmenTest—the most directly comparable work that "infers oracles from the available documentation" using LLMs—is buried late in the documentation-derived paragraph rather than upfront. AugmenTest should be surfaced earlier to clarify TestVDB's delta (source-grounded falsification) over prior LLM-derived oracle work. The current placement obscures the precise novelty boundary.
- **2.3** The source-grounded falsifier mechanism itself is a clear delta: prior LLM-as-judge work (Panickssery et al., Wataoka et al., Haldar et al.) addresses self-preference and self-inconsistency in general text evaluation, but TestVDB's application to test-oracle pipelines with implementation source as the independent falsifier is a distinct contribution. The multi-perspective judging baseline (Table 2) isolates the gap well.

3. **Soundness** — Adequate
- **3.1** The core claim that source-grounded falsification suppresses false positives is well-supported by triangulated evidence. Section 6 presents three complementary controls: (1) a 12-FP/4-TP ablation showing source alone suppresses 75% of FPs (Table 4), (2) a full 48-candidate retrospective showing disabling source collapses recall from 74% to 19% (line 272), and (3) per-vendor breakdowns isolating where source grounding adds value (Milvus recall 80%→5% without source). This is rigorous ablation design.
- **3.2** The methodology is sound on paper: the four-stage pipeline (Section 3) cleanly separates extraction, generation, execution, and confirmation, with the dev-reviewer as a falsifier that independently reproduces, cross-checks evidence, and falsifies against source. The three-check design (Figure 2) is well-specified.
- **3.3** The choice of operating points is statistically grounded. The paper flags the 3-run union as a post-hoc selection (line 252) and reports Wilson 95% CIs that do not account for this selection, then validates with bootstrap resampling (2000 resamples) and Bonferroni correction, which is appropriate transparency about the selection bias.
- **3.4** Threats to validity (Section 6) are candid, calling out internal validity (post-hoc operating point, non-random 48-candidate set), external validity (Weaviate yield-only, no capture-recapture), and construct validity (single-family GLM-5.2, κ-scores showing family-specific verdicts). This is thorough self-disclosure.

4. **Verifiability** — Adequate
- **4.1 [minor, fixable]** The abstract's yield accounting is correct but could be labeled more explicitly. The paper reports two distinct denominators: 49/107 = 45.8% as a worst-case bound (all 35 pending treated as false positives, line 232) and 49/72 = 68.1% as the adjudicated precision (49 TP + 23 by-design/rejected). The body distinguishes these clearly; carrying the "worst-case bound" qualifier into the abstract would help a casual reader avoid conflating the two.
- **4.2 [minor, fixable]** Information about the 20-agent architecture (Section 3, line 126) is sparse. The paper lists five stage-aligned roles (contract-formalizer, four attack agents, judge quartet, dev-reviewer, reporter) but does not specify the prompts, the dispatch mechanism, or how JSON outputs are collected. The artifact note (line 143) says "full prompts" will be released; from the paper alone, a reader cannot assess whether the 20-agent design is minimal or over-engineered. The main flow is conceptually reproducible, but the agent layer needs the artifact for full verification.
- **4.3 [major, fixable]** The CouchDB/Elasticsearch external validation probe (Section 8) is too weak to support the transferability claim. The paper reports "the pipeline ran end-to-end" with CouchDB extracting five claims and probing each boundary, and Elasticsearch similarly rejecting all invalid probes except size=0. However, both cases yielded zero silent-accept defects—both mature APIs strictly rejected invalid inputs. The paper interprets this as "probing method portability rather than defect detection," but this is insufficient evidence for the broad transferability claim to "REST APIs without OpenAPI, configuration validation, and policy-as-code" that follows. At minimum, the claim should be hedged as "preliminary portability demonstration" rather than implied generalization.
- **4.4** Artifact availability is declared (line 143—"will release at a persistent URL upon acceptance"), which satisfies Verifiability for the paper type. The paper should clarify what the artifact contains: prompts? per-token accounting? the 48-candidate set? The current statement is vague on completeness.

5. **Presentation** — Excellent
- **5.1** Structure is strong: Introduction (problem → oracle gap → LLM solution → false-positive modes), Background (exclusion argument), Approach (four-stage pipeline), False-Positive Problem (two modes), Dev-Reviewer (three-check design), Evaluation (three RQs), Related Work, Discussion/Threats, Conclusion. This is logical flow.
- **5.2** Visuals are effective: Figure 1 (four-stage pipeline with dev-reviewer as falsifier) clearly shows the LLM-driven stages and the source-grounded anchor; Figure 2 (three-check falsification) visualizes the suppression logic; Table 1 (oracle exclusion) is an excellent at-a-glance argument for why LLM is the practical oracle.
- **5.3 [minor, fixable]** Inconsistent capitalization of "OpenAPI" vs "openapi": line 60 uses "OpenAPI" (correct trademark), but line 346 writes "openapi coverage" (lowercase). Should be uniform. (The testora26 citation key could not be verified from the stripped source alone—the .tex uses `\bibliography{references}`, so the .bib is out of scope; confirm the entry resolves in the final build.)
- **5.4 [minor, fixable]** Line 143's "The full prompts, target versions, and per-token accounting are in the artifact, which we will release at a persistent URL upon acceptance" is slightly awkward phrasing. Better: "The artifact (to be released at a persistent URL upon acceptance) contains full prompts, target versions, and per-token accounting."

### Self-Check
- [x] Every Detailed Assessment item points to paper specifics (section/table/line)
- [x] Each tier is grounded in cited evidence
- [x] Overall recommendation matches rubric: no Poor, no substance Weak (Significance/Novelty/Soundness all Adequate), Verifiability Adequate (patched: the denominator is not an inconsistency, only a label-clarity point), Presentation Excellent → per rubric, no substance Excellent keeps this at Weak Accept (not Accept)
- [x] Every problem item has [severity, fixability] tag consistent with tier
- [x] No external fact claims without sources or provisional flags
- [x] Novelty assessment cites specific competitors from paper's own Related Work
- [x] Core Strengths/Weaknesses are decision-driving, linked to N.M ids

> Note: a prior draft framed the 45.8%/68.1% two-denominator reporting as an internal inconsistency; on re-read the paper distinguishes them clearly (line 232 labels 45.8% a worst-case bound), so this was downgraded to a minor abstract-labeling point.

## Meta-Review

### Criterion Consensus

| Criterion | Reviewer 1 | Reviewer 2 | Reviewer 3 | Meta-Review |
|---|---|---|---|---|
| Significance | Adequate | Adequate | Adequate | **Adequate** |
| Novelty | Adequate | Adequate | Adequate | **Adequate** |
| Soundness | Adequate | Adequate | Adequate | **Adequate** |
| Verifiability | Adequate | Adequate | Adequate | **Adequate** |
| Presentation | Weak | Adequate | Excellent | **Adequate** *(Mixed)* |
| **Recommendation** | **Weak Accept** | **Weak Accept** | **Weak Accept** | **ACCEPT** |

### Meta Recommendation
**ACCEPT**

三位 expertise reviewer 一致给出 Weak Accept，触发 unanimous shortcut 直接判 **ACCEPT**。无任何 consensus Poor，无 substance 准则 consensus Weak——五准则 consensus 均为 Adequate（Presentation 三票分散 Weak / Adequate / Excellent，中位 Adequate，标 [Mixed] 但不驱动 verdict）。最接近危险信号的是 R1 的 Presentation Weak（§6 密度 + Wilson/bootstrap 记号不一致），但属 fixable 且单票，不影响 consensus。

核心 framing（doc-impl defect class + deterministic oracle 的结构性 exclusion + LLM-as-practical-oracle + dev-reviewer source-grounded falsification）经三位独立核实站得住：R1 从全领域确认对 VDBFuzz / MASTOR / SATORI / AGORA+ 的 delta（first-principles，2025-2026 竞品未入学术库故 provisional）；R2 经 fetched cache（SATORI / MASTOR / Panickssery / Wataoka）确认 characterization 准确、falsification direction 是真实 delta；R3 从内部 coherence 确认 ablation triangulation（12-FP/4-TP + source-disabled 74→19% + per-vendor）严谨。

residual weakness（post-hoc 操作点、single-backbone、external validation 仅 portability）三位均判为 fixable 或 inherent limitation 而非致命——这些是修订周期可解或需后续工作的问题，不阻止接收。与 v3 相比，R1 Novelty 从 Weak 恢复为 Adequate（3-family cross-model + cache 核实后 delta 站得住），R2/R3 Verifiability 因 minus-source + bootstrap 升 Adequate。

### Priority Revisions
1. **Post-hoc operating-point CI（R1 3.4, R2 W1/3.3）[major, fixable]** — 3-run union 是四操作点中事后选的，Wilson CI 未校正多重比较。论文已有 Bonferroni + bootstrap（2000 resamples）CI [53%,83%] / [71%,96%]；residual 需 pre-registered 选择规则（如 falsifier 语义：under-confirmation 成本高于 forwarding FP）才能根本消除。
2. **External validation 扩展（R1 1.4, R2 W2/3.4, R3 W2/4.3）[major, fixable]** — CouchDB / Elasticsearch 是 method-portability 探测（0 defect），非 generalization 证据。Discussion 的 "REST API / config / policy-as-code" transfer claim 应显式 hedged 为 preliminary portability；一个 non-VDBMS defect case 会显著加强。
3. **AugmenTest 前置定位（R3 W1/2.2）[major, fixable]** — 最直接可比的 LLM-derived-from-documentation oracle 工作被埋在 §7 末尾，应前置到 positioning 处澄清 TestVDB 的 source-grounded falsification delta。
4. **Single-backbone generalization（R1 W1/3.3）[major, partially fixable]** — headline 67% / 74% 是 GLM-5.2 的。已有 abstract caveat + 3-family κ（0.14 / 0.37 / 0.51）+ recall 18–56%，但 R1 指出读者仍可能误读为 method 属性而非 backbone 属性。§6 显著标注 "backbone-specific" 可缓。
5. **Residual FP characterization（R1 3.6）[minor, fixable]** — ~8/48 residual FP 未分类（hallucination vs source-grounding 失败 vs threat-model 漏覆盖）。附录分类表会澄清边界。
6. **20-agent 架构细节（R3 4.2）[minor, fixable]** — §3 仅列 5 stage-aligned 角色，prompts / dispatch / JSON 收集未述，artifact 需补。
7. **§6 记号与 density（R1 5.2–5.4）[minor, fixable]** — Wilson vs bootstrap CI 关系、"any-confirmed" / "majority" 定义、Figure 6 per-run band 含义应加 caption / footnote。

---

## Unified Action Plan

# Unified Action Plan（v4 第四版 dual-review weakness 去重）

> 6 reviewer（3 态度 + 3 expertise）。评分不合并，仅 weakness 语义聚类去重。
> 来源标：`[both]`（两半边都点到，最强信号）/ `[attitude-only]`（方法论/三态视角）/ `[expertise-only]`（novelty/cache 视角）。
> severity 跟原 reviewer tag；态度三态核实结果（Valid/Misleading/False）折入描述。

## [both] + major（两半边共识，优先）

- **[both] [major, fixable]** post-hoc 操作点 selection-aware CI — 见态度 R1-W2 / R2-W1 / R2-W5 / R3-W2（均 Valid）/ 见 expertise R1-3.4 / R2-W1/3.3 / Meta-1
  **6 reviewer 共识（最强信号）**。3-run union 是四操作点中事后选的，Wilson CI 未校正多重比较。论文已有 Bonferroni（[44,84]/[51,89]）+ bootstrap 2000（[53,83]/[71,96]）+ selection rationale；residual 是 **inherent limitation**（需 pre-registered 选择规则才能根本消除），文字层面已尽。

- **[both] [major, fixable]** cross-family / single-backbone generalization — 见态度 R1-W1（Misleading）/ R2-W2（Valid）/ R3-W1（Misleading）/ 见 expertise R1-W1/3.3 / Meta-4
  headline 67%/74% 是 GLM-5.2 的；3-family κ=0.14/0.37/0.51 + recall 18–56% 显示 backbone-dependent。论文 abstract + §8 已标 open question，§6 有 3-family 数据。两半边分歧在定性：态度 R1/R3 称"未充分 address"（Misleading，因已有 caveat），R2 称"undercuts"（Valid，inherent）。**residual inherent**——§6 可更显式标 "backbone-specific"。

- **[both] [major, fixable]** external validation 仅 portability — 见态度 R1-W4（Valid）/ R2-W7（Valid）/ 见 expertise R1-1.4 / R2-W2/3.4 / R3-W2/4.3 / Meta-2
  CouchDB / Elasticsearch 各 1 次 end-to-end（0 defect，mature API 严格校验），是 method-portability 非 generalization 证据。论文已标 portability framing；Discussion 的 "REST API / config / policy-as-code" transfer claim 可显式 hedge 为 "preliminary portability"；一个 non-VDBMS defect case 会显著加强。

## [expertise-only] + major

- **[expertise-only] [major, fixable]** AugmenTest 前置定位 — 见 expertise R3-W1/2.2 / Meta-3
  最直接可比的 LLM-derived-from-documentation oracle 工作被埋在 §7 末尾，应前置到 positioning 处澄清 TestVDB 的 source-grounded falsification delta。态度半边未提（其视角偏方法论/novelty-delta 不重叠）。

- **[expertise-only] [major, fixable]** defect-class scope boundary 模糊 — 见 expertise R1-1.3
  "documentation-implementation defect" 与 result-correctness 的边界在实践模糊（如 invalid `ef` 被接受导致 wrong recall：是 consistency 还是 correctness？）。§2 分了 consistency/correctness 但实践边界不清。态度半边未单独提（R1-W3 的 implementation-as-correct 是相邻但不同的点）。

## [attitude-only] + major

- **[attitude-only] [major, fixable]** ensemble fairness（3-run dev-reviewer vs single-run baseline）— 见态度 R2-W3（Misleading）
  R2-严格 批比较不公平（混淆 source grounding 与 ensemble 贡献）。**核实为 Misleading**：12-FP/4-TP ablation 已隔离 source grounding 贡献（source alone 抑制 75% FP + 保留全部 TP），minus-source 74→19% 证明 gain 主来自 source 非 ensemble。expertise 半边未提此批评（R1-3.2 反而肯定 ablation triangulation 严谨）。补 3-run single-LLM baseline 对照表会更显式。

## [both] + minor

- **[both] [minor, unfixable]** recall estimation absent — 见态度 R1-W5（Valid）/ R2-W6（Valid）/ 见 expertise R1-W4
  无 public GT catalog，74% 是相对 37% baseline 非绝对。**inherent**——论文诚实承认；capture-recapture 是 future work。

- **[both] [minor, fixable]** implementation-as-correct 假设未量化 — 见态度 R1-W3（Valid）/ 见 expertise R2-5.1
  §8 提 limitation（implementation bug 可错误 falsify 正确 doc）但未量化 23 rejected 中 doc-error 比例。audit 23 rejected（"wont-fix, docs will update" vs "behavior correct"）会加强。

## [expertise-only] + minor

- **[expertise-only] [minor, fixable]** residual FP 未分类 — 见 expertise R1-3.6 / Meta-5
  ~8/48 residual FP（hallucination vs source-grounding 失败 vs threat-model 漏覆盖）未分类。附录分类表会澄清边界。

- **[expertise-only] [minor, fixable]** 20-agent 架构细节稀疏 — 见 expertise R3-4.2 / Meta-6
  §3 仅列 5 stage-aligned 角色，prompts/dispatch/JSON 收集未述。artifact 需补。

- **[expertise-only] [minor, fixable]** §6 记号与 density — 见 expertise R1-5.2/5.3/5.4 / Meta-7
  Wilson vs bootstrap CI 关系、"any-confirmed"/"majority" 定义、Figure 6 per-run band 含义应加 caption/footnote。R1 Presentation Weak 的主因。

## [attitude-only] + minor

- **[attitude-only] [minor, fixable]** VDBFuzz probe n=1 underpowered — 见态度 R2-W4（Valid）
  每方向 n=1，论文已标 "hypothesis-generating"。**两半边分歧**：态度 R2 批 underpowered，expertise R1-2.1 称 bidirectional probe "strong reachability result"。VDBFuzz fixed-budget run 会强化（即使 negative 结果 VDBFuzz reaches 0/49 也比 n=1 强）。

- **[attitude-only] [minor, fixable]** RQ3 complementarity framing 措辞 — 见态度 R3-W3（Misleading）
  §6 已 frame 为 bidirectional reachability + complementarity，R3 建议确保一致用 "complementary" 而非 "superiority"。

## 结论

residual weakness 集中在 3 个 **[both] major inherent limitation**（post-hoc / cross-family / external validation）——文字层面已尽（Bonferroni + bootstrap + caveat + open question + portability framing），根本解决需实际改进（pre-registration / 更多 family / non-VDBMS defect case），非文字修改能消除。其余为显式化/补细节/措辞性 minor。论文已诚实面对 inherent limitation，适合投稿。

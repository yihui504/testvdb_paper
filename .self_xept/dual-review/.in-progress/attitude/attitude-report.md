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

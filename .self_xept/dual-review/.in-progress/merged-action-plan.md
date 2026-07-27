# Unified Action Plan（Stage C weakness 去重合并）

> 来源：态度半边（attitude-report.md）+ expertise 半边（3 份 expertise review + Meta Priority Revisions）。
> **评分不合并**——两 verdict 各自保留（态度 5.7/10 borderline vs expertise ACCEPT）。仅 weakness 语义聚类、去重、标来源。

<!-- verify_merged_plan: 以下每条 bullet 须以 **[source] [severity]** 开头；描述用缩进段落 -->

## [both] + major（两半边共识，must-fix）

- **[both] [major, fixable]** RQ2 操作点 post-hoc + 单 run 方差未解释 — 见态度 R1-W2 / R2-W1 / R3-W1 / 见 expertise R1-3.3 / R2-1.3 / R3-3.2

  6 reviewer 全提（最强共识）。67%/74% 基于 N=48（Milvus32+Qdrant16，无 Weaviate），3-run any-confirmed union 是看到数据后选的（maximizes recall by construction），单 run recall 15-78%（5x range）。方差来源未分析。**修**：报告完整 k=1..5 PR 曲线 + 预注册/明确 post-hoc justification + 分析方差来源（temperature/retrieval）。R2 拒稿信号 + R3 Soundness Weak 主因。

- **[both] [major, fixable]** 85% residual framing 循环分母 — 见态度 R1-W3 / R3-W2 / 见 expertise R1-1.3 / R3-3.3

  摘要（line 16）已有 qualifier "composition of our findings, not a population estimate"（R2 原 W5 因此删除），但 Intro + Contributions bullet 2（line 61）仍作 headline framing，分母是 TestVDB 自己 yield（partly circular）。**修**：重构为"of TestVDB's surfaced defects"；或补独立估计（capture-recapture / 随机 100 历史 issue 用 bugstudy25 分类）。

- **[both] [major, fixable]** RQ3 小样本 + 11/11 behavior TI 含 7 个非 maintainer-acknowledged + TI 定义循环 — 见态度 R1-W1/W5 / R2-W2/W9 / R3-W3/W4 / 见 expertise R2-2.3/3.2 / R3-2.4

  6/18 Wilson CI [16%,56%] 40-point span 太宽；11/11 中 7 个 impl-confirmed 非 maintainer-ack（论文 line 149 自承认）；TI 由 DeepSeek over-formalize 定义再评 DeepSeek。**修**：拆 maintainer-ack(4/4) vs newly-probed(7/7) 分开报告；正文不 pool 17/29；承诺 maintainer 裁决 7 个；lean on within-vendor contrast + 0/21 负对照作 independent evidence。

- **[both] [major, fixable]** VDBFuzz n=1/direction + §8 structural hypothesis overreach — 见态度 R1-W7 / R2-W4 / 见 expertise R1-3.4 / R2-1.4

  §6（line 109）诚实说 hypothesis-generating，但 §8（line 209）从 2 个 hand-picked case 推 structural claim。reverse-direction miss 归因 VDBFuzz `wait=true` template 覆盖（非 crash-oracle 本质）。**修**：scope §8 为"observed in 2 cases"；foreground template-coverage caveat；或跑第三对（n≥2/direction）。

- **[both] [major, fixable]** 第三 LLM family on TI subset（高 marginal value）— 见态度 R1-W1/Q1 / R3-W4 / 见 expertise R3-2.4

  task-intrinsic claim 只用 GLM+DeepSeek 2 family。第三 family（Llama/Qwen/GPT）即使 n=6 on TI 子集也大幅加固 convergence claim。**修**：跑第三 family on 6 TI clauses；若不可行标 next experiment。

- **[both] [major, unfixable]** 单 LLM family (GLM-5.2) for source-anchor + κ=1.0 on n=20 非随机 — 见态度 R1-W1(patch) / R2-W3 / R3-W1/W4 / 见 expertise R2-1.5 / R3-3.4

  source-anchor 全用 GLM-5.2（line 189 自承认）；κ=1.0 的 20 candidate diversity-stratified 非随机 → Wilson on agreement [83%,100%] 含 substantial disagreement。contribution 边界（unfixable），但"标注边界 + 补 Wilson CI + 明确 scope"是 fixable。态度 R2/R3 视为降分主因，expertise R1/R2 视为已充分承认。

## [both] + minor

- **[both] [minor, fixable]** 10 stale-closed TP 计数 + 敏感性分析 — 见态度 R2-W5(patched) / 见 expertise R1-3.5

  manual_fix tier 是"acknowledged but unfixed"。论文已披露但计数宽松。**修**：报告排除 10 个后 yield（49→39 TP）。

- **[both] [minor, fixable]** Generalization（REST API/config/policy）未测试 — 见态度 R1-W6 / 见 expertise R3-1.3

  §8 列 transfer targets 但"we have not tested these transfers"。三态 Misleading（已标 future work）。**修**：缩 §8 段为一句 + 显式 future work；或 10-clause probe。

- **[both] [minor, fixable]** Presentation（段落/notation/Table caption/artifact link） — 见态度 R1/R2/R3 各 minor / 见 expertise R1-5.* / R2-5.* / R3-5.*

  §6 RQ1 大段落拆分；Table caption 50 vs 49 一致；notation 标准化；artifact preview link；prompt skeleton；Conclusion 补 37% baseline。

## [attitude-only] + major

- **[attitude-only] [major, fixable]** baseline like-for-like（dev-reviewer 全 anchor vs baseline 无） — 见态度 R2-W6(patched)

  baseline 48/56/37% = "no source anchor"，但 dev-reviewer 含 source+threat-model+clean-repro 三 anchor；3-condition ablation 在 12-FP/4-TP 不同对照组。headline recall gain（37→74%）不能干净归因 source grounding。**修**：48-candidate 上跑 dev-reviewer minus source anchor + minus all anchors。

## [expertise-only] + major

- **[expertise-only] [major, fixable]** Novelty dichotomy 不完全 clean + RESTGPT 线未引 — 见 expertise R1-2.6 / R2-2.5 / R3-2.3

  structured/NL 二分边界模糊：SATORI 也读 OpenAPI NL field descriptions；RESTGPT/LlamaRestTest/Kim et al. LLM-rule-extraction-from-OpenAPI-NL 线未引。**修**：补 positioning（source-ambiguity spectrum：OAS→Javadoc→NL prose）。

## [attitude-only] + minor

- **[attitude-only] [minor, fixable]** Weaviate from RQ2 + "三 VDBMS"泛化 — 见态度 R2-W8

  RQ2 仅 Milvus+Qdrant；Weaviate 仅 yield。**修**：或跑 Weaviate retrospective；或摘要改"across three VDBMSs for yield, retrospective on Milvus and Qdrant"。

## 统计

[both] 8 簇（6 major + 2 minor + 1 mixed unfixable）—— 两半边共识，优先修。[attitude-only] 2 簇。[expertise-only] 1 簇。互补率 [both] 8/11 ≈ 73% 共识 + 27% 互补（≥30% 阈值，验证双套非冗余且高度收敛）。

# Unified Action Plan（dual-review weakness 去重合并）

> 6 reviewer（3 态度 + 3 expertise）weakness 语义聚类、去重、标来源。**评分不合并**——态度 ~7/10 weak-accept vs expertise ACCEPT。

## [both] + major（两半边共识，最强信号）

- **[both] [major, fixable]** RQ2 post-hoc 操作点 selection bias — 见态度 R1-W1 / R2-W1 / 见 expertise R1-3.5 / R2-3.2 / R3-4.2
  5 reviewer 共识（最强信号）。论文已加 selection rationale（"precision ≥60% 下最高 recall"）+ 标 post-hoc，但 Wilson CI 未含 selection uncertainty（统计本质）。**修**：报告 selection-aware CI（如 Bonferroni 或显式标"CI conditional on selected operating point"），或更显 limitation。

- **[both] [major, fixable]** External validity / VDBMS 外泛化无证据 — 见态度 R1-W2 / R3-W2 / 见 expertise R1-1.2 / R2-3.4 / R3-W3
  5 reviewer 共识。§8 已标 future work（REST API/config/policy），但无 case study。**修**：1 个 non-VDBMS mini case（10-clause run on documented REST without OpenAPI）或更显式 future work 框架。

- **[both] [major, fixable]** Single LLM backbone (GLM-5.2) + κ=1.0 on 20 统计力 — 见态度 / 见 expertise R1-W1 / R2 / R3-3.2
  论文已加 Wilson [83,100] + "measures agreement not recall"。**修**：更显 limitation（"moderate family-specificity 统计兼容"已加；可补"running a third family on a subset is the highest-value next experiment"）。

- **[both] [major, unfixable]** impl-as-correct false negative — 见 expertise R2-W3 / R3-3.3
  inherent limitation。论文已加 false negative 讨论（§8）。**修**：已较充分，可补"false-negative rate 未量化"的更显 limitation。

## [both] + minor

- **[both] [minor, fixable]** VDBFuzz n=1 降调 — 见态度 R2-W3 / 见 expertise R3
  论文已标 hypothesis-generating + abstract 降调（"explores complementary coverage"）。**修**：基本 done，可更显式。

- **[both] [minor, fixable]** Novelty vs REST-API 位置 — 见 expertise R3-W1
  论文 §7 有 MASTOR/SATORI/AGORA+ 比较 + Table 1 排除论证。R3 觉得"ambiguous-prose regime"边界不清。**修**：加 1 句"AGORA+/SATORI 假设 OpenAPI/schema 存在；VDBMS documentation 无此结构"强化边界。

## [attitude-only] + minor

- **[attitude-only] [minor, fixable]** multi-perspective baseline 加表 — 见态度 R2-W2
  论文已展开 voting rule + operating point（§4）。R2 仍觉得不够。**修**：可加小表（4 judge 角色 + voting threshold sweep），但边际价值低。

- **[attitude-only] [minor, fixable]** yield selection bias — 见态度 R1-W3
  yield 68.1% 基于 adjudicated subset（有 selection bias）。论文 §8 已说"biased by design"。**修**：可补 stratified precision（by defect class）。

## [expertise-only] + minor

- **[expertise-only] [minor, fixable]** cost breakdown 加表 — 见 expertise R2-4.2
  论文已加 token 分布文字（§3 LLM automation）。**修**：可加 cost 表（claim extraction / generation / dev-reviewer breakdown）。

## [expertise-only] — False（reviewer 误读，论文有）

**漏 AugmenTest（R2 标，False）** —— 论文 §7 有 cite（augmentest25+chatassert24），reviewer 漏看。不需改。原 bullet: [expertise-only] 漏 AugmenTest/ChatAssert** — 见 expertise R2-2.3 / R2-5.4。**False**：论文 §7 Documentation-derived oracles 段已 cite augmentest25 + chatassert24（line 311-313 区）。reviewer 漏看。不需改。

## 统计

[both] 6 簇（4 major + 2 minor，两半边共识优先修）；[attitude-only] 2 簇（minor）；[expertise-only] 1 簇（minor）+ 1 False（误读）。互补率 [both] 6/9 ≈ 67% 共识 + 33% 互补（≥30% 阈值）。

**最强 must-fix**：post-hoc 操作点 selection-aware CI（5 reviewer 共识，统计本质，文字可改）+ external validity mini case（5 reviewer 共识，需小实验或更显 limitation）。

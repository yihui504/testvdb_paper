# Unified Action Plan（v5 第五版 dual-review weakness 去重）

> 6 reviewer（3 态度 + 3 expertise）。评分不合并，仅 weakness 语义聚类。
> **独立性 caveat**：v5 expertise R1/R2 Detailed Assessment 大量雷同（论文+cache 相同→措辞趋同，仅 1.2/2.4 specialty 不同），R3 为独立确认。共识强度按此加权。

## [both] + major（两半边共识，优先 — inherent）

- **[both] [major, fixable]** post-hoc 操作点 selection-aware CI — 态度 R1-W2/R2-W1/R3-W2 + expertise R1-3.2/R2-W4/R3-3.2
  6 reviewer 共识。已有 Bonferroni（[44,84]/[51,89]）+ bootstrap（[53,83]/[71,96]）。**v5 新具体建议（R1）：Bonferroni CI 进 Table 5**（cheap，显式化）。residual inherent（需 pre-registration）。

- **[both] [major, fixable]** cross-family / single-backbone — 态度 R1-W1/R2-W3 + expertise R1-W1/1.2/R3-W2
  inherent。v4 加 backbone 标注，但 R1 1.2 仍说 headline "67%/74%" 未 fully qualify "on GLM-5.2"（abstract/intro/RQ2 header）。

- **[both] [major, fixable]** external validation 仅 portability — 态度 R1/R2/R3 + expertise R1-W4/R2-W3/R3-1.2
  inherent（需 non-VDBMS defect case）。

## [expertise-only] + major（v5 新抓，fixable）

- **[expertise-only] [major, fixable]** Verifiability: prompts / sampling / 48-candidate catalog — expertise R3-4.1/4.2
  **v5 新**（v4 R3 patch 后 Adequate，v5 R3 更严格 bar）。R3 要求关键 prompts（contract-formalizer/attack/judge/dev-reviewer）+ sampling 参数 + 48-candidate issue ID 移入 appendix（不只 artifact promise）。修订周期可解。

- **[expertise-only] [major, fixable]** LLM-as-judge bias 未独立测量 — expertise R2-W1/1.2/2.4
  **v5 新**（R2 specialty 独特）。R2 指出论文 cite Panickssery/Wataoka 作 motivation 但未 apply 其 bias metric（Wataoka Equal Opportunity / Panickssery self-recognition）测 TestVDB judge 是否真降 bias。建议报 single-LLM / multi-perspective / dev-reviewer 三配置的 bias metric。这是新 experimental 建议（中等工作）。

## [attitude-only] + major（Misleading — v4 reframe 后仍被漏读）

- **[attitude-only] [major, fixable]** VDBFuzz crash baseline on v1.18.2 — 态度 R2-W2（**Misleading**）
  R2 称"0/14 incomparable without baseline"，但论文 §6.3 已有"26k requests, 0 crash"baseline。v4 reframe（systematic vs controlled）未让 R2 读到。**fix：§6.3 更显著标 'crash baseline'**（一句明确"this 26k-request run is the crash baseline; 0 crashes means VDBFuzz detects none, not that it was not run"）。

## [expertise-only] + minor（v5 新抓）

- **[expertise-only] [minor, fixable]** §6.2 cross-model "85%" 口径 — expertise R3-4.3
  **v5 新**。"18-56% vs. 85%" 中 85% 是 GLM 5-run union recall，但 κ 比较的是 vs GLM single-run；比较 basis 应显式（R3 抓的 valid coherence 点）。

- **[both] [minor, fixable]** worst-case-bound framing — expertise R1-W3/5.1/R2-W2/5.1
  abstract 应 lead with adjudicated 68%，worst-case 46% 作 sensitivity。v4 加了 68%/46%，但 R1/R2 认为仍偏保守。

## 结论

v5 验证 v4 修订**部分成功**：
✓ Presentation consensus 升（v4 R1 Weak → v5 全 Adequate，Table 5 caption 起效）
✓ R3 internal coherence 确认（abstract/§6.1/§6.3/Table 5 一致）
✓ AugmenTest §2 positioning（R1 2.2 确认 delta 准确）
⚠ backbone 标注（v4 加了，但 R1 1.2 仍说未 fully qualify headline）
⚠ VDBFuzz systematic framing（v4 reframe，但 R2 漏读，需更显式标 "crash baseline"）

**v5 新增 fixable 项**（非 inherent）：① Verifiability prompts/catalog appendix；② LLM-as-judge bias metric 测量；③ 85% 口径澄清；④ Bonferroni CI 进表；⑤ §6.3 显式 "crash baseline"。这些都是修订周期可解，不需重实验。

3 个 [both] major inherent limitation（post-hoc / cross-family / external）仍文字已尽。论文适合投稿。

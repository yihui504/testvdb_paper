# Unified Action Plan（v6 第六版 dual-review weakness 去重）

> 6 reviewer（3 态度 + 3 expertise）。评分不合并，仅 weakness 语义聚类。

## [both] + major（两半边共识 — inherent）

- **[both] [major, fixable]** post-hoc 操作点 selection-aware CI — 态度 R1-W2/R2-W1 + expertise R1-3.2/R2-W2/3.2/R3-W1
  6 reviewer 共识。已有 Bonferroni（[44,84]/[51,89]）+ bootstrap（[53,83]/[71,96]）。residual inherent（需 pre-registration）。

- **[both] [major, fixable]** cross-family / single-backbone — 态度 R1-W1/R2-W3 + expertise R1-W1/3.4/R2-W3/3.6
  inherent（κ=0.14-0.51 + recall 18-56% vs GLM 85%）。

- **[both] [major, fixable]** external validation 仅 portability — 态度 R1-W4/R2-W5 + expertise R1-W3/R2-1.2/R3-1.2
  inherent（CouchDB/ES 0 defect）。

## [attitude-only] + major（Misleading）

- **[attitude-only] [major, fixable]** RQ3 VDBFuzz n=1 / asymmetry — 态度 R2-W4（**Misleading**）
  R2 称"n=1 underpowered, conflates template gaps with oracle limits"，但论文 §6.3 已区分 systematic（v1.18.2, 26k requests, 0/14）vs controlled（n=1 mechanism）。fix：§6.3 systematic direction 首句更显著标 "crash baseline" 让 strict reviewer 不漏读。

## [expertise-only] + minor（v6 新抓，fixable）

- **[expertise-only] [minor, fixable]** self-preference mechanistic discussion — expertise R2-W1/2.3
  论文 cite Panickssery + Wataoka both，但 §4 没区分两机制（self-recognition vs perplexity/familiarity）。一句区分可 sharpen dev-reviewer 的 mechanistic justification。

- **[expertise-only] [minor, fixable]** significance prevalence — expertise R1-1.2
  43% incorrect-behavior 中 doc-impl 占比未量化。

- **[expertise-only] [minor, fixable]** prompts excerpt in appendix — expertise R2-4.4
  artifact 有 22 prompts，paper appendix 可 excerpt 1-2（contract-formalizer/dev-reviewer）。

- **[expertise-only] [minor, fixable]** 48-candidate construction process — expertise R2-4.5
  27 TP + 21 FP 的 selection criteria（从 72 adjudicated）未述。

## 结论

v6 验证 v5 polish **全部 clean**——approach.png Figure 1（icon 风格 + dev-reviewer from Stage 4 + LLM dashed/solid）、judge→judge agent 术语统一、PBT 句清晰化、feedback loop 删除、reduce-ai L4 soften、Figure 3 per-run variation——**未引入新真 issue**。R3 expertise 提的 3 个 v6-specific 点（judge/agent 不一致、Figure 1 caption、PBT obscure）经独立 checker 核实全是 reviewer 误读（论文实际 consistent），不进 Meta。

3 个 [both] major inherent limitation（post-hoc / cross-family / external）仍文字已尽。v6 新增 4 个 [expertise-only] minor（mechanistic discussion / prevalence / prompts excerpt / 48-candidate construction）+ 1 个 [attitude-only] Misleading（RQ3 framing 让 strict reviewer 漏读）。这些都是修订周期可解，不需重实验。

论文适合投稿（6 版 dual-review expertise 全 ACCEPT，core framing 第六次确认）。

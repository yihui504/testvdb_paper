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

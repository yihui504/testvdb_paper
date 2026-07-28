# Unified Action Plan（v3 第二版 dual-review weakness 去重）

> 6 reviewer（3 态度 + 3 expertise）。评分不合并。

## [both] + major（两半边共识，must-fix）

- **[both] [major, fixable]** post-hoc 操作点 selection-aware CI — 见态度 R1-W1 / R2-W2 / 见 expertise R1 / R2
  4 reviewer 共识（最强信号）。论文已加 Bonferroni 估算 + selection rationale，但 reviewer 仍觉 headline CI 未充分 caveat selection。

- **[both] [major, fixable]** cross-family κ 在 abstract/contributions 显式 caveat — 见态度 R1-W2 / R2-W3 / 见 expertise R1 / R2
  论文 §6 已诚实报告 κ=0.14/0.51，但 abstract/contributions 仍 claim "LLM-derived oracle" 广义。reviewer 要更显式标 single-backbone limitation。

- **[both] [major, fixable]** external validity 扩展（CouchDB 只 1 个 non-VDBMS）— 见态度 R1-W3 / 见 expertise R1
  CouchDB mini case 只测了 1 个 + 无 defect found。reviewer 要 ≥2 个 non-VDBMS 或更显式 framing。

## [attitude-only] + major

- **[attitude-only] [major, fixable]** minus-source fully crossed ablation — 见态度 R2-W1
  R2 指出 minus-source 仍含 clean-repro + threat-model anchor，没完全隔离 source 的贡献。要 fully crossed（source only vs no-source vs full）在同一 48-candidate 上。

## [attitude-only] + minor

- **[attitude-only] [minor, fixable]** no recall catalog — 见态度 R1-W3
  recall 74% 缺 ground-truth catalog denominator context。

## [expertise-only]

- **[expertise-only] [minor, fixable]** Novelty positioning 分歧 — 见 expertise R1（Weak）vs R2（Excellent）
  R1 觉得 source-grounded falsification 是 known technique；R2 觉得 domain-specific application is novel。论文可强化"source as falsifier（非 oracle）的方向性不对称"framing。

互补率：[both] 3/5 ≈ 60% 共识。

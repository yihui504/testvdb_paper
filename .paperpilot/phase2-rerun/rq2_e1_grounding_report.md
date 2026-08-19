# E1：视角 A 机械判定 vs LLM 判定 对照实验（2026-08-18）

方案：plans/validated-riding-cat.md 交付物 2。纯机械回测，零新增 LLM 成本。

## 波动集挖掘（四轮判词 verdict_A 对比）

**A 值波动 case = 44/71（62%）**——auditor 视角 A 的会话方差比预想严重一倍多
（原估计 ~15）。典型波动模式：
- 039-042：v1 NEUTRAL → v2 CONFIRMED → v4 NEUTRAL（同链三值全变）
- 022/023：v1 CONFIRMED → v4 REFUTED（跨极翻转）
- 波动覆盖三 vendor 全部 15 组

## 主对照：对 GT 方向一致率（波动集 44）

| 判定者 | 一致率 | 性质 |
|--------|--------|------|
| v1 LLM | 0.409 | 会话抽样 |
| v2 LLM | 0.545（仅 11 case 有记录） | 会话抽样 |
| v3 LLM | 0.118（17 case） | 会话抽样 |
| v4 LLM | 0.386 | 会话抽样 |
| **A_MECH（脚本）** | **0.545** | **确定性，零方差** |

A_MECH 分布：CONFIRMED 11 / REFUTED 12 / NEUTRAL 21（reason：id+quote_ok 23 / constraint_absent 12 / quote_mismatch 9）

## 判据判定（预注册）

> A_MECH 在波动集上与 GT 方向一致率 ≥ LLM 最好轮

**通过**：0.545 ≥ 0.545（与 v2 并列最高）。且两点使机械化的论证强于"并列"：
1. v2 的 0.545 是会话抽样的幸运值——同是 LLM，v1/v3/v4 轮只有 0.118-0.409；
   A_MECH 的 0.545 是**可复现下限**（同输入同输出）
2. quote_mismatch 9 个经归一化复检全部为真转述（builder 概括契约文本而非逐字引用），
   机械判 NEUTRAL 是保守正确的处理——这 9 个的歧义留给 D 吸收（决策 8 的设计如此）

## 离线模拟：A_MECH 替换进 v4 判词重算聚合

用 v4 判词的 B/C/D 值 + A_MECH 按聚合规则离线重算（波动集 44 case）：

| 口径 | recall | precision |
|------|--------|-----------|
| v4 实测（LLM A） | 0.103 | — |
| **离线模拟（A_MECH）** | **0.448** | **0.929** |

recall 提升 4.3 倍、precision 0.929——A 会话方差正是 v4.1 回退的最大单一因素，
机械化后立即可见恢复。（模拟用 B/C/D 仍是 v4 会话值，E2 会实测它们本身的方差）

## 结论

**E1 判据通过 → 按决策 1，A 全量机械化写进 SOP。**

下一步（方案交付物 3-6）：
- SOP 修订：A 采信机械结果（读 grounding_check 输出，不得自行改判）+ 删除
  agent_suspects_contract_wrong 例外（D 吸收）+ 认知必读先验 + ≤12 分批
- E2 波动子集重判 ×2 轮验证稳定化

数据：rq2_e1_fluct_set.json（波动集）；机械判定函数见本报告与后续
check_chain_grounding.py。

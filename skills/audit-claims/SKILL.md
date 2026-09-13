---
name: audit-claims
description: 审计论文里「有数字/统计主张但无支撑锚点」的句子——每个数字或统计主张必须挂 \cite 或 \ref/\eqref 或 Table/Figure 引用，找不到支撑就标红给作者、绝不编造。用于投稿前、跨节大改后、或用户问"这些数字哪来的/这句话有出处吗"时调用。区分：数字前后不一致用 xept:consistency-check；引用真实存在用 xept:check-references；补真实引用用 xept:add-citation。
---

# Audit Claims（主张-证据绑定审计）

找出论文里**没有支撑锚点**的数字/统计主张，逐个绑定证据或标红。轻量化 K-Dense scientific-writing 的 evidence binding（xept 面向 CS 论文，不需要 E/C/N/M/O 全量 manifest——退化为：数字/统计主张句必须挂锚点）。

> 核心规则：**每个数字或统计主张都要能指到证据。** 指不到的——加锚点、或标红给作者核实；**绝不**为了"补上支撑"而编造引用/数字/结果。

## 何时用

- 投稿前、跨节大改后、多作者合并后
- 用户问"这些数字哪来的""这句话有出处吗""结果有没有支撑"

## 何时不用（真实边界）

- 数字前后**不一致**（同一指标两处值不同）→ `xept:consistency-check`
- 引用是否**真实存在/格式正确** → `xept:check-references`
- 补**真实**引用 → `xept:add-citation`
- 方法陈述里的数字（"我们训练 50 epochs"）**不算**主张，跳过

## 工作流

> 本质行：**扫 → 读 unbound → 分类 → 修复 → 重跑**。

### Step 1: 扫描
`python scripts/audit_claims.py <main.tex>` —— 输出数字主张总数、无锚点行、其中统计强信号（%/p 值/±/×/n=）子集。

### Step 2: 逐条读 unbound
对每个无锚点行，在**上下文**里判断它属于哪类：
1. **应挂引用**（别人的结果/事实）→ 加 `\cite{}`（先用 `xept:add-citation` 找真引用，绝不编）
2. **应挂表/图**（自己实验的结果）→ 加 `\ref{tab:...}` / `\ref{fig:...}` 指到承载该数字的表图
3. **方法陈述**（"我们训练 50 epochs"）→ 不是主张，跳过
4. **无法支撑**（既无引用也无表图，作者也没给数据）→ 标红给作者核实，不硬造

### Step 3: 修复并重跑
改完重跑脚本，`stat_unbound` 应降到 0 或只剩已标红的待核实项（明确列给作者）。

## 锚点优先级

- 自己的实验结果 → `\ref{tab}` / `\ref{fig}`（数据落进表图，数字从表图来）
- 别人的结果 → `\cite`（且经 `xept:check-references` 核实真实）
- 公式推导 → `\eqref`

## 集成

- **上游**：`xept:write-paper` / `xept:write-revision` 产出后跑本技能。
- **下游**：标红项 → `xept:add-citation`（补引用）或 `xept:consistency-check`（若数字对不上）。
- **协同**：与 `xept:check-submission`（投稿前总查）互补——本技能专挖"主张无锚点"这一轴。
- **脚本**：确定性扫描 `scripts/audit_claims.py`（启发式，误报交本技能判断层过滤）。

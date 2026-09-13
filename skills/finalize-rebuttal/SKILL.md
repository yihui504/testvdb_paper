---
name: finalize-rebuttal
description: 把 rebuttal 草稿打磨成可提交定稿——统一格式与语气、去冗余、核实主张、控字数、跨回复一致。读项目根 rebuttal.md + review.md + main.tex，写 rebuttal_final.md。rebuttal 流水线收尾。
---

# Finalize Rebuttal（打磨 rebuttal 定稿）

把草稿 rebuttal 转成打磨过的、可提交文档。

## 目的
取工作版 `rebuttal.md`（可能有粗糙回复、格式不一、语气参差），产出干净、专业的 `rebuttal_final.md`。

## 工作流
1. `read` 项目根 `rebuttal.md` — 含所有回复的草稿
2. `read` 项目根 `review.md`（或 `reviews.md`）— 理解审稿人上下文与分数
3. `read` 项目根 `main.tex` — 核实主张与引用
4. 通篇**分析**一致性问题
5. 生成打磨版
6. `write` 到项目根 `rebuttal_final.md`

## 定稿清单

### 1. 结构与格式
- 每条回复标题格式一致
- markdown 格式正确
- 回复间视觉分隔清晰

### 2. 语气一致
- 全文专业语气
- 无防御性语言
- 一致用 "we"（非 "I" 或混用）

### 3. 去冗余
- 去重复 "Thank you"（每审稿人最多一次）
- 合并重复解释
- 删填充与对冲语言

### 4. 内容打磨
- 所有论文引用具体（Section X、Table Y、Line Z）
- 主张有证据支撑
- 承诺现实且具体
- 技术准确性对照 main.tex 核实

### 5. 字数优化
- 每条回复在字数限内
- 删冗长短语
- 收紧句子但不丢义

### 6. 跨回复一致
- 同问题多审稿人提及时，回复一致
- 修订主张跨回复一致
- 回复间无矛盾

## 输出格式
```markdown
# Author Response to Reviewer Comments

We thank all reviewers for their constructive feedback. Below we address each comment in detail. **Bold text** indicates revisions made to the manuscript.

---

## Reviewer A (Overall Merit: X)

### Response to Comment 1 [Q1]

> [Original comment]

[Polished response]

---

## Summary of Revisions

- **Section 2.3**: Added clarification on methodology (addresses R1-Q2, R2-Q1)
- **Table 3**: Added new baseline comparison (addresses R1-Q3)
- ...
```

## 打磨指南

### 收紧语言

| 改前 | 改后 |
|------|------|
| "We would like to thank the reviewer for this very insightful comment" | "We thank the reviewer for this insight" |
| "It should be noted that" | [删] |
| "In order to" | "To" |
| "Due to the fact that" | "Because" |

### 强化软弱语言

| 改前 | 改后 |
|------|------|
| "We think this might help" | "This addresses the concern" |
| "We tried to improve" | "We improved" |
| "We hope this clarifies" | "This clarifies" |

### 去对冲（有把握时）

| 改前 | 改后 |
|------|------|
| "It seems that" | [直接陈述] |
| "Perhaps" | [直接陈述或删] |
| "We feel that" | [陈述事实] |

## 输出前质量检查
1. **无孤立回复** — 每条意见都有回复
2. **无占位** — 无 "[TODO]"、"[FILL IN]"
3. **审稿人命名一致** — 全文 "Reviewer A/B/C" 或 "Reviewer 1/2/3"
4. **引用格式一致** — 所有原意见用 blockquote
5. **字数合理** — 总文档典型 2000-4000 词
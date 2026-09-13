---
name: ideation
description: "写论文前评估研究想法——SWOT + 5 维评分（Novelty/Feasibility/Impact/Research Gap/Clarity）+ ≥5 篇相关工作对比矩阵 + PROCEED-class 判决。只用 web_search/fetch_bib 元数据做对比，**禁下载竞品全文**。用户要\"这想法值得写吗\"/\"评估研究想法\"/\"值不值得投稿\"（写论文前）时调用。已有 draft 用 xept:mock-review；只要文献用 xept:add-citation。"
---

# Ideation（研究想法评估 · 写论文前）

> **实现**：companion `evaluation-framework.md`（5 维量表）+ `output-guide.md`（输出模板）（见 §配套）。设计依据：[docs/improvement-plan.md](../../docs/improvement-plan.md) P4-1 + 路线 B plan（范围限定：不引入 competitor cache，§6）。

## 核心原则

**没有对比矩阵的创新性断言 = 未经验证的假设。**

每个想法都走完整评估：SWOT + 5 维评分 + ≥5 篇相关工作对比。verdict 由证据推出，不由"这想法明显新"推出。

**Iron Law**：

```
NO NOVELTY CLAIM WITHOUT ≥5-PAPER COMPARISON.
无对比矩阵的创新性断言无效。
```

<HARD-GATE>
用户**必须**提供 problem + approach 的研究想法（非模糊主题）。只给模糊主题 → 问澄清再进。不评估没有具体 problem-solution 对的想法。
</HARD-GATE>

## 何时用 / 何时不用

**用**：
- 有研究想法（problem + approach），要 go/no-go 评估
- 想对比 state of the art 再决定写不写
- 要结构化的发表计划
- 已有 PROCEED-class verdict 且想更新计划 → 跳过 Step 1-5，直接 Step 6-7

**不用**：
- 已有完整 draft → [xept:mock-review](../mock-review/SKILL.md)
- 只要文献检索 → [xept:add-citation](../add-citation/SKILL.md)
- 要初始化论文项目 → [xept:setup-venue](../setup-venue/SKILL.md)（新）或 [xept:configure](../configure/SKILL.md)（存量）

## 范围限定（红线 · improvement-plan §6）

<HARD-GATE>
对比矩阵**只用元数据+摘要**：标题 / 作者 / 年份 / venue / DOI / 链接 + [fetch_bib](../../scripts/fetch_bib.py) 返回的 abstract。

**红线**：
- 不下载竞品 PDF
- 不缓存竞品全文 / summary（competitor cache）
- 不读竞品正文

本 skill 只做"想法 vs 已有工作的 delta 定位"，**不做** novelty 的 full verification。要深度核实某条引用是否真实存在 → [xept:check-references](../check-references/SKILL.md)（只验存在性，不读全文）。
</HARD-GATE>

## 流程

### Step 1: 结构化想法
把原始想法重述为 Problem-Solution 声明，scope 清晰。

### Step 2: SWOT
Strengths / Weaknesses / Opportunities / Threats。每点指向具体想法（非通用观察）。

### Step 3: 搜相关工作
[web_search](../../docs/tool-mapping.md) + [xept:add-citation](../add-citation/SKILL.md)（走 [fetch_bib](../../scripts/fetch_bib.py) 四源）找 **5-15 篇直接相关工作（优先最相关 5 篇）**。只用返回的元数据（标题/摘要/作者/年份）——**不下载全文**。

### Step 4: 对比矩阵
把想法 vs 找到的 5-15 篇，沿关键维度（novelty / approach / evaluation / scalability / limitations）列表对照。

```markdown
| 维度 | 你的想法 | 竞品 1 | 竞品 2 | 竞品 3 | 竞品 4 | 竞品 5 |
|---|---|---|---|---|---|---|
| **Novelty** | [1-2 句] | [1-2 句] | [1-2 句] | [1-2 句] | [1-2 句] | [1-2 句] |
| **Approach** | [1-2 句] | [1-2 句] | [1-2 句] | [1-2 句] | [1-2 句] | [1-2 句] |
| **Evaluation** | [1-2 句] | [1-2 句] | [1-2 句] | [1-2 句] | [1-2 句] | [1-2 句] |
| **Scalability** | [1-2 句] | [1-2 句] | [1-2 句] | [1-2 句] | [1-2 句] | [1-2 句] |
| **Limitations** | [1-2 句] | [1-2 句] | [1-2 句] | [1-2 句] | [1-2 句] | [1-2 句] |
```

### Step 5: 5 维评分
按 [evaluation-framework.md](evaluation-framework.md)（实现阶段补）量表打分，每维 1-5 + 1-2 句 justification 引用量表档位：

| 维度 | 问什么 | 1 vs 5 含义 |
|---|---|---|
| **Novelty** | 相对已有工作的原创程度 | 1=重复 / 5=突破 |
| **Feasibility** | 资源范围内能否实现并评估 | 1=不可实现 / 5=直接可做 |
| **Impact** | 对目标社区的潜在贡献 | 1=无影响 / 5=领域变革 |
| **Research Gap** | 填补文献空白的程度 | 1=无gap / 5=关键未填 |
| **Clarity** | 此阶段想法的定义清晰度 | 1=模糊 / 5=清晰 |

### Step 6: 判决
综合 SWOT + 5 维 + 对比矩阵，给四级 verdict：

| verdict | 含义 | 下游 |
|---|---|---|
| **STRONG PROCEED** | 强证据支持 | → [xept:setup-venue](../setup-venue/SKILL.md)（新论文）或 [xept:configure](../configure/SKILL.md)（存量） |
| **PROCEED WITH CAUTION** | 可做，记风险 | 同上，风险写进 `.self_xept/project.yml` 的 `ideation.risk_assessment` |
| **RECONSIDER** | 证据不足或有威胁 | 停；回 Step 1 重构想法或换题 |
| **DO NOT PROCEED** | 根本缺陷（无新意/不可行/无 gap） | 停 |

**硬规则**：5 维平均 <3 不得 PROCEED-class。

### Step 7: Paper Plan + Research Roadmap（已有 PROCEED-class verdict 跳过 Step 1-5 时只做此步 + Step 8）
按 [output-guide.md](output-guide.md)（实现阶段补）模板写发表计划（target venue / research questions / contributions / method / experiment design / outline）+ 4 阶段 roadmap（含里程碑）。

### Step 8: 自检
- 分数和 verdict 一致？（全 <3 不能 PROCEED-class）
- 对比矩阵 ≥5 篇？
- 每个 SWOT 点指向具体想法？
- verdict 由证据推出，非 aspiration？
- 若跳过 Step 1-5：是否已有 PROCEED-class verdict？

## 输出

写到 `.self_xept/ideation/`：
- `idea-analysis.md` — SWOT + 5 维分 + 对比矩阵 + 风险 + verdict
- `paper-plan.md` — 发表计划（供 [xept:write-paper](../write-paper/SKILL.md) 读）
- `research-roadmap.md` — 4 阶段里程碑

verdict 同步进 `.self_xept/project.yml` 的 `ideation.status`（PROCEED-class / RECONSIDER / DO NOT PROCEED）——**每次覆写（幂等，新覆盖旧）**。

## Red Flags — STOP

- 这想法明显新
- SWOT 没必要
- 分数低但兴奋
- 4 篇够了
- 下份 PDF 深读
- 跳过风险评估

**以上任一 = 跑完整评估。**

## 借口表

| 借口 | 现实 |
|---|---|
| "我对这领域够熟" | 你不知道上月发了什么。搜。 |
| "5 篇太多" | <5 = 不可靠的创新性评估。每次。 |
| "明显新" | 无对比 = 未验证假设。 |
| "SWOT 对简单想法过头" | 简单想法有隐藏威胁。SWOT 5 分钟。 |
| "下全文核实更稳" | competitor cache 工程过重（§6 排除）。元数据足够定位 delta。 |
| "用户只要快速 verdict" | 无证据的快 verdict 是伤害。做完整评估。 |

## 配套（实现阶段补）

- 5 维量表：`skills/ideation/evaluation-framework.md`（每维 1-5 档 anchor 描述；借鉴成熟量表，案例换 xept 领域）
- 输出模板：`skills/ideation/output-guide.md`（Idea Analysis / Paper Plan / Research Roadmap 三模板）

## Integration

- **上游**：用户的研究想法（problem + approach）
- **PROCEED-class 下游**：[xept:setup-venue](../setup-venue/SKILL.md)（新论文）或 [xept:configure](../configure/SKILL.md)（存量）→ [xept:write-paper](../write-paper/SKILL.md)
- **扩展对比矩阵**：[xept:add-citation](../add-citation/SKILL.md)（继续找文献）
- **深度核实单条引用**：[xept:check-references](../check-references/SKILL.md)（只验存在性）

---

## 立项验收清单（review 用）

- [ ] discipline 三件套（Iron Law + 借口表 + Red Flags），符合 [B1-1 writing-skills](../writing-skills/SKILL.md) §6（3-8 词触发短语标准）+ HARD-GATE（结构门）
- [ ] **范围限定**写死（只用元数据、禁下载全文/competitor cache，呼应 improvement-plan §6）
- [ ] 5 维框架名称 + 硬规则（平均 <3 不 PROCEED）写明（量表细节留 companion）
- [ ] verdict 四级 + 下游接 xept 链（setup-venue / configure）
- [ ] 输出位置 `.self_xept/ideation/`（不挪动工作产物，写元状态）
- [ ] 与 mock-review / add-citation / check-references / setup-venue / configure 边界清晰
- [ ] 方言合规（`xept:` 引用、`.self_xept/`、中文正文、无平台工具残留）

---
name: doc-check
description: "派独立 fresh auditor 审计任意 prose 文档（SKILL.md / README / design doc / API doc / 指南）——查结构、内部矛盾、事实漂移、遗漏、冗余。Iron Law: 不自我审计（派新 subagent，不粘 session history）。用户要\"审一下这个文档\"/\"检查文档质量\"/\"这文档有没有矛盾或漂移\"时调用。审论文内容用 xept:mock-review 或 xept:dual-review；审代码逻辑用 code-reviewer agent；改写/降 AI 味用 xept:paraphrase 或 xept:reduce-ai。"
---

# Document Check（文档审计 · 独立 auditor）

> 移植自 PaperPilot `doc-check`（路线 D）。实现：派一个 fresh auditor subagent 读全文 + 跑固定 checklist（5 维 18 子项）+ 自标 severity，呈现报告。**不自我审计、不粘 session history、不自己 apply 改动**——作者据 Findings 自决改不改。

## 核心原则

**Iron Law: NO SELF-AUDIT.**

```
NO SELF-AUDIT.
你对自己刚写/刚读的文档有确认偏误——派一个 fresh auditor 读全文跑 checklist，
才能抓到你自省漏掉的。违反字面 = 违反精神。
```

<HARD-GATE>
审计**必须**派一个 fresh auditor subagent（Task/Agent 工具，general-purpose），**绝不**自己跑 checklist、**绝不**把 session history 粘进 dispatch。fresh auditor 的独立性是全部意义——它要文档 + 四字段 audit context，不要你的读后感。
</HARD-GATE>

## 何时用 / 何时不用

**用**：
- 审任意 prose 文档：SKILL.md / README / design doc / API doc / 指南 / 教程
- 查：结构/排序问题、内部矛盾/不清措辞、事实不准/漂离代码或相关文档、遗漏/未完成标记、冗余/该在别处的内容
- 写完文档发布前独立核查

**不用**：
- 审论文内容 → [xept:mock-review](../mock-review/SKILL.md) 或 [xept:dual-review](../dual-review/SKILL.md)
- 审代码逻辑 → code-reviewer agent
- 审参考文献 → [xept:check-references](../check-references/SKILL.md)
- 改写/降 AI 味 → [xept:paraphrase](../paraphrase/SKILL.md) / [xept:reduce-ai](../reduce-ai/SKILL.md)
- 查论文一致性 → [xept:consistency-check](../consistency-check/SKILL.md)

## 流程

### Step 1 — 审计上下文

1. `read` 文档全文。
2. 写审计上下文——**恰好**四字段，按序，无其他：
   - **Type**——文档类型（API guide / README / design doc / SKILL.md / …）
   - **Purpose**——文档用途
   - **Intended audience**——读者
   - **Related documents**——auditor 要读来核实 Correctness（漂移/准确性）的文件路径；"none" 若文档独立

### Step 2 — 派一个 auditor

用 Task/Agent 工具派 fresh auditor subagent（general-purpose），payload 见 [auditor-prompt.md](auditor-prompt.md)：
1. auditor prompt 模板——[auditor-prompt.md](auditor-prompt.md)
2. 文档**路径**（长文档传路径，不内联粘贴）
3. 审计上下文（Step 1 四字段，inline）
4. （可选）**scope**（标题/锚点/行范围；省略审全文）

auditor 读全文（+ Related documents 核实 Correctness）→ 跑固定 checklist（5 维 18 子项）→ 自标 severity（HIGH/MEDIUM/LOW）→ 返回 Findings。报告可落 `.self_xept/doc-check/audit-report.md`（若用户要留存）。

### Step 3 — 核实 finding + 呈现报告

**auditor 也可能 hallucinate 引用**（报不存在的 location/issue——真实使用验证：审一份 SKILL 报 9 finding，核实后 5 个误报，都是"JSON 有 venue 字段"但实际文件没有）。呈现前**必须核实**：

1. **核实每条 finding**——`read` finding 引用的 location（行/锚点），确认 issue 真实存在（文件该处确实有所描述的内容/矛盾）。剔除 hallucinate 的（location 引用的内容不存在 / issue 与文件实际矛盾 / 引用了想象的字段）。
2. 呈现**核实后**的 Findings（severity 排序）+ 标注剔除情况（"auditor 报 X 条，核实剔除 Y 条 hallucinate：[简述]"），让作者信任呈现的内容。
3. **STOP**——呈现发现；apply 改动是人的 gate（你不编辑/提交/推送）。

**核实的 Red Flag**：呈现未核实的 finding = 放任 auditor hallucinate 误导作者改不存在的问题。核实是 orchestrator 的 gate，不可跳过。

## Red Flags — STOP

- "我自己跑 checklist 省事" — STOP. Iron Law：派 fresh auditor。
- "粘 session history 给 auditor 了解背景" — STOP. fresh auditor 要文档 + 四字段，你的读后感会污染它。
- "预评 finding 的 severity，或引导 auditor 偏离某 finding" — STOP.
- "给报告注水显得详尽" — STOP.
- "silently 扣下某些 finding" — STOP. 呈现 auditor 返回的原样。
- "自己 apply finding（编辑/提交/推送）" — STOP. 改不改是作者的 gate。
- "加四字段以外的 audit context" — STOP.

**以上任一 = 撤销违反，重派 fresh auditor。**

## 借口表

| 借口 | 现实 |
|---|---|
| "我刚写的，自己清楚" | 确认偏置——你自省漏的，fresh auditor 才抓得到。Iron Law。 |
| "粘 session history 让 auditor 了解背景" | fresh auditor 的独立性是全部意义——你的读后感会污染它。只给文档 + 四字段。 |
| "文档短，我自己扫一遍" | 短文档也派 auditor——Iron Law 无长度豁免。 |
| "我自己改完再派 auditor 验" | STOP. 先派 auditor 呈现 Findings，改不改是你的 gate，不绕过审计。 |
| "code-reviewer 能审文档" | code-reviewer 偏代码逻辑；doc-check 的 5 维 18 子项 checklist 专攻 prose（结构/矛盾/漂移/遗漏/冗余）。正交。 |

## 配套

- auditor dispatch 模板 + checklist：[auditor-prompt.md](auditor-prompt.md)（5 维 18 子项 + Calibration + Severity + Output Format）
- 设计 rationale：[docs/doc-check-design.md](../../docs/doc-check-design.md)

## Integration

- **审论文**：[xept:mock-review](../mock-review/SKILL.md) / [xept:dual-review](../dual-review/SKILL.md)
- **审代码**：code-reviewer agent
- **下游**：作者据 Findings 决定改不改（doc-check 不 apply）；改后可再跑 doc-check 复审
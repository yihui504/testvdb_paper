---
name: mock-review
description: 模拟目标会议/期刊的真实审稿流程——派 3 个独立子代理（客观/严格/友好）各出一份 review，主代理逐条核实 weakness（Valid/Misleading/False），输出行动清单与预测决定。投稿前自检。输出写到项目根 mock-review.md。
---

# Mock Review（模拟审稿）

模拟目标会议/期刊的真实审稿流程。用 subagent 工具派 3 个独立子代理各出一份 review，主代理核实后输出行动清单。

输出文件：项目根 `mock-review.md`

---

## 工作流
```
Stage 0 — 会议研究：确定目标会议，获取评审标准
Stage 0.5 — 输入净化：剥注释（dispatch 前物理删 %/iffalse/comment，防 reviewer 引用草稿注释）
Stage 1 — 三视角审稿：派 3 个独立子代理，各自读**剥注释后**的论文、独立写 review
Stage 1.5 — 独立事实核查：每份 draft 过独立 checker 子代理核实 claim 是否 grounded，原 reviewer patch，≤3 轮，兜底 [unverified]
Stage 2 — 验证：主代理逐条核实三份 review 的 weakness，判 Valid / Misleading / False
Stage 3 — 行动清单：综合三份 review + 验证，输出修改建议
```

---

## Stage 0 — 会议研究（获取审稿标准）

确定目标会议，从三层获取评审标准：

### 第一层：项目配置（结构化元数据）
`read` `.self_xept/project.yml`，拿：
- Page limit、Anonymity（单盲/双盲）、Review process type、Deadline、CFP URL

这些是形式约束，不含评分维度与量表。

### 第二层：CFP / Reviewer Guidelines 页面抓取
用 `.self_xept/project.yml` 的 CFP URL，`web fetch` 会议官网 Reviewer Guidelines，提取：
- 评分维度（如 Soundness / Novelty / Clarity / Significance）
- 量表范围（1-4？1-10？每维含义？）
- 每个分数段描述（如 "3 = technically solid, 4 = exceptional"）
- Review 文本格式要求（有无模板？要写哪些部分？）

### 第三层：已知会议惯例（fallback）
抓不到完整标准时，用常见会议已知格式：

| 会议 | 评分维度 | 量表 |
|------|----------|------|
| NeurIPS | Soundness, Presentation, Contribution, Overall | 1-4 / 1-4 / 1-4 / 4-10 |
| ICML | Quality, Clarity, Originality, Significance | 1-5 each |
| ACL/EMNLP | Soundness, Novelty, Clarity, Overall | 1-5 each |
| ICSE/ASE | Soundness, Importance, Novelty, Presentation | -2 to +2 或 1-5 |
| USENIX Security | Scientific novelty, Technical depth, Presentation, Overall | 1-5 each |

---

## Stage 0.5 — 输入净化（剥注释）

dispatch 前物理删除 LaTeX 注释，让草稿注释、`\iffalse` 备选内容、`% TODO` 根本
不进入 reviewer 视野——口头"别看注释"是模型能绕过的软约束。

用 `pwsh` 跑（论文的所有 .tex，含 `\input` 的子文件）：

```
python scripts/strip_comments.py -o .self_xept/mock-review-stripped/ <main.tex 及其 \input 子文件>
```

- 非零退出（`\iffalse` / `\begin{comment}` / verbatim 不平衡）→ **中止审稿**，让用户修源码后重跑；绝不回退到原始文件 dispatch。
- 之后 Stage 1 的子代理一律读 `.self_xept/mock-review-stripped/` 下的 stripped .tex，不读项目根裸 .tex。
- 若 stripped 文件里仍出现 `%` 行注释 / `\iffalse` / `\begin{comment}` 标记，说明剥除失败——中止并排查。

---

## Stage 1: 三视角审稿

用 subagent 工具派 3 个独立子代理，每个各自读论文、独立写一份 review。子代理之间互不可见，也不受主代理对话上下文影响。

### 启动方式
对每个 reviewer，用 subagent 工具派发，传入：
- **剥注释后的论文路径**（`.self_xept/mock-review-stripped/` 下，Stage 0.5 产出；不传项目根裸 .tex）
- Stage 0 获取的会议评审标准（打分维度、范围、格式）
- 该 reviewer 的人设与立场

三份 review 分别存到：
- `.self_xept/mock-review-r1.md`
- `.self_xept/mock-review-r2.md`
- `.self_xept/mock-review-r3.md`

### Reviewer 1 — 客观审稿人（Objective）
**人设**：领域内有经验的研究者，实事求是，不偏接收也不偏拒绝。
- 优点问题都直说；打分居中偏上（若论文确实还行）；Confidence 通常 3-4/5
- **要求**：严格按会议 review 格式；每维单独打分；Strengths 带具体证据（引论文段落/数据）；Weaknesses 每条带改进建议；提 2-3 个 Questions for Authors

### Reviewer 2 — 严格审稿人（Critical）
**人设**：对质量要求很高的资深研究者，倾向找问题，但不捏造。
- **关注**：方法论严谨性、实验设计充分性（baseline 够不够新？ablation 够不够？random seed？）、Claim 是否被实验充分支撑
- 打分偏低但有理有据；每个 weakness 必须有论文具体证据
- **注意**：严格 ≠ 恶意。所有批评基于论文实际内容，不凭空编造。

### Reviewer 3 — 友好审稿人（Friendly）
**人设**：认为该研究方向有价值的研究者，倾向看到贡献。
- 强调创新点与贡献；Strengths 更详细；也指出问题但语气建设性；打分偏高但不盲目；问题以"建议改进"方式提

### 写作要求
1. 三个子代理完全独立，不互相参考
2. 不要三份都说同样优缺点——不同视角应注意到不同方面
3. 每份都要有：Summary → Strengths → Weaknesses（每条带 **[severity, fixability]** tag，见标记规则）→ Questions → 各维度打分
4. 格式严格按目标会议
5. Review 语言跟着投递地方——国际会议/期刊（EMNLP、NeurIPS、ICSE）用英文，中文会议/期刊（计算机学报、软件学报）用中文

---

## Stage 1.5: 独立事实核查（checker 循环）

<HARD-GATE>
Stage 1 的每份 draft 必须过独立 checker 核查后才能进 Stage 2。checker 是**新的独立
子代理**，只看自己那一份 draft + stripped 论文，**不碰其余两份**（跨份比较是 Stage 2/3
主代理的活）。跳过 checker 直接进 Stage 2 不可接受。
</HARD-GATE>

### 流程（三份 draft 各自独立、可并行）

1. 对每份 draft（`.self_xept/mock-review-rN.md`），派 checker 子代理，传入：该份 draft、stripped 论文路径（`.self_xept/mock-review-stripped/`）、核查指令（下述）
2. checker 重读 stripped 论文，逐条核实 draft 的**事实性 claim**（引用的数据/节/公式/baseline/figure/定理），判：
   - **grounded**：claim 在论文里成立
   - **fabrication**：claim 不在论文（编造的数据、不存在的节、张冠李戴的 baseline）
3. checker 返回 `VERDICT: CLEAN` 或 `VIOLATIONS:` 后跟编号清单：`[编号] <draft 原文> — fabrication. 论文: <位置+短引文 或 "not found in paper">`
4. 若 VIOLATIONS：用 SendMessage **继续原 reviewer 子代理**（保留其读论文的上下文），把 checker 清单给它，让它**只改被标项**（删/修正 fabricated claim，不重写整份），覆盖写回 `.self_xept/mock-review-rN.md`
5. 重新派 checker 核查 patch 后的 draft → 循环
6. **上限 3 轮**；到上限仍有 violations → 在 draft 对应项标 `[unverified: <原因>]`，**绝不冒充 clean**，照常进 Stage 2。Stage 2 对 `[unverified]` 项**照常做三态核实**（其事实基础未确认，反而更需主代理回论文查），最终报告保留 `[unverified]` 标记让作者看到

### checker 与 Stage 2 三态的分工（保留 xept 差异化）

- **checker（本阶段）**：查**事实**——claim 是否在论文里。二元 grounded/fabrication。**去 hallucination**。
- **Stage 2（下阶段）**：评**判断**——weakness 的批评是否成立。三态 Valid/Misleading/False。**保留 xept 的 Misleading 中间态**。

两层互补：checker 净化 draft 的事实基础（去掉编造的数据/节），Stage 2 再评估 weakness 真实性（Valid/Misleading/False）。不互相替换——checker 不评 weakness 是否成立，Stage 2 不重复查 claim 是否在论文（checker 已查）。

### checker 纪律
- 只看自己那份 draft，不比较三份
- 只报 fabrication（claim 不在论文的 grounded 核查未过项），**不写 review 内容、不给改进建议、不评论文好坏**
- 一个"感觉不对"但无论文依据的怀疑不是 violation——不报

---

## Stage 2: 验证

### 目的
评估 weakness 批评是否成立（三态）。此时 draft 已过 Stage 1.5 checker 去除编造的**事实 claim**，但仍可能存在"批评本身不成立"（论文其实没问题）或"表述误导"——这两类由本阶段判。主代理回到论文原文，逐条核实每条 weakness。

### 步骤
1. `read` `.self_xept/mock-review-r1.md`、`mock-review-r2.md`、`mock-review-r3.md`
2. 提取所有待验证 claim（Weaknesses + 有事实依据的 Strengths），格式化如：
   ```
   [R2-W1] "The paper lacks ablation studies to justify each component."
   [R1-W3] "The comparison with method X is missing."
   [R3-S2] "The theoretical analysis in Section 3 is rigorous."
   ```
3. 回到**剥注释后**的论文（`.self_xept/mock-review-stripped/`）逐条核实（重读相关章节含 appendix），判断是否正确、相关内容在哪章
4. 汇总验证结果

### Verdict 定义

| 判决 | 含义 | 行动 |
|------|------|------|
| **Valid** | 论文确实有此问题 | 必须修改 |
| **Misleading** | 有相关内容但表述不够清晰，易被误解 | 改写相关段落 |
| **False** | 论文有明确内容反驳此意见 | 不需改内容，但可让相关内容更醒目 |

---

## Stage 3: 行动清单

1. **综合分析三份 review**
   - 多人都提？→ Must Fix
   - 验证为 Misleading？→ Should Fix（改表述）
   - 验证为 False？→ 不改内容，但 Action Plan 注明原因
   - 只被严格 reviewer 提？→ Optional，但要准备 rebuttal

2. **生成 Action Plan**

| 优先级 | 触发条件 | 含义 |
|--------|----------|------|
| **Must Fix** | 多人共识 或 Valid 的 Major weakness | 不改大概率被拒 |
| **Should Fix** | Misleading 意见 | 内容没错但表述需改进 |
| **Optional** | 个别 reviewer 的 Minor 问题 | 锦上添花 |

每条 Action 要**具体**：指明改哪章、怎么改、按影响力排序。

3. **预测 Overall Decision**：据三 reviewer 评分与内容给 Strong Accept / Accept / Weak Accept / Borderline / Weak Reject / Reject + 简短理由（1-2 句）

4. `write` 完整报告到项目根 `mock-review.md`

---

## 输出格式

写入项目根 `mock-review.md`：
```markdown
# Mock Review Report
> **Target Venue:** NeurIPS 2026 · **Overall Prediction:** Weak Accept · **Date:** 2026-07-14

## Score Summary
| Dimension | R1 (客观) | R2 (严格) | R3 (友好) |
|-----------|:---------:|:---------:|:---------:|
| Soundness | 3/4 | 2/4 | 3/4 |
| Novelty | 3/4 | 2/4 | 4/4 |
| Overall | 6/10 | 4/10 | 7/10 |

## Reviewer 1 — 客观审稿人
> Confidence: 4/5
**Summary** ...
**Strengths** 1. ...
**Weaknesses** 1. **[major, fixable]** ... 2. **[minor, fixable]** ...
**Questions for Authors** 1. ...

## Reviewer 2 — 严格审稿人
> Confidence: 3/5
（同样格式，立场更严格）

## Reviewer 3 — 友好审稿人
> Confidence: 4/5
（同样格式，立场更积极）

## Verification
| # | Source | Claim | Verdict | Note |
|---|--------|-------|---------|------|
| 1 | R2-W1 | "实验缺少 ablation study" | **Valid** | 确实缺少 |
| 2 | R2-W3 | "没有和 XX 方法对比" | **Misleading** | 4.2 节有提及但表述不清，建议改写 |
| 3 | R1-W2 | "缺乏理论分析" | **False** | Appendix A 有完整证明 |

## Action Plan
**Must Fix** — 多人共识，不改大概率被拒
- [ ] ...
**Should Fix** — 表述不清易被误解
- [ ] ...
**Optional** — 锦上添花
- [ ] ...
```

---

## 标记规则（markdown 粗体，无 emoji，无 HTML 色彩）

| 用途 | 写法 |
|------|------|
| Verdict: Valid | `**Valid**` |
| Verdict: Misleading | `**Misleading**` |
| Verdict: False | `**False**` |
| Must Fix | `**Must Fix**` |
| Should Fix | `**Should Fix**` |
| Optional | `**Optional**` |
weakness 每条带 **[severity, fixability]** tag（四组合之一，`scripts/verify_review.py` 校验合法性）：

| tag | 含义 | Action Plan 映射 |
|------|------|------|
| `**[major, fixable]**` | 严重且可修（缺 baseline、实验漏洞） | Must Fix |
| `**[major, unfixable]**` | 严重且不可修（核心方法根本缺陷） | 影响 Overall Decision（拒稿信号） |
| `**[minor, fixable]**` | 小问题可修（typo、表述） | Should Fix / Optional |
| `**[minor, unfixable]**` | 小问题不可修（罕见） | Optional |

---

## 重要规则
- 三个 reviewer 必须由独立子代理完成，确保各自独立、不互相参考、不受主代理对话上下文影响
- **dispatch 前必剥注释**（Stage 0.5）：reviewer 只读 `.self_xept/mock-review-stripped/`，不读裸 .tex；若 reviewer 引用了注释 / `\iffalse` 草稿内容，说明剥除失败，中止重跑
- 验证环节由主代理自己做，回到**剥注释后**的论文逐条核实（同样不读裸 .tex）
- **每份 draft 必过独立 checker**（Stage 1.5）：checker 只看自己那份、只报 fabrication（claim 不在论文）、原 reviewer patch、≤3 轮、超限标 `[unverified]` 不冒充 clean——未经 checker 的 draft 不进 Stage 2
- checker 查事实（grounded/fabrication），Stage 2 三态评判断（Valid/Misleading/False），两层分工不替换
- 每个 reviewer 格式严格按目标会议真实 review 格式
- 打分维度与范围从目标会议获取，不用通用 1-5 分
- Review 语言跟着投递地方——国际会议/期刊用英文，中文会议/期刊用中文
- Action Plan 按紧急度排序，每条具体说改哪、怎么改
- **不要用 emoji**
- 用上面的粗体标记规则让报告易读
- 写完 `mock-review.md` 后跑 `python scripts/verify_review.py mock-review.md` 自检：退出 1（缺段 / 非法 tag）必须修后才交付

## 配套
- review 模板见本技能 `refs/review_template.md`
- 注释剥离器 `scripts/strip_comments.py`（Stage 0.5 用，纯标准库、fail-closed）
- 输出校验器 `scripts/verify_review.py`（写完 mock-review.md 后跑，校验段标题 verbatim + tag 合法性）
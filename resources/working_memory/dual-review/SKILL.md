---
name: dual-review
description: "双套 reviewer 并行深度审稿——态度三审（复用 xept:mock-review：客观/严格/友好 + Valid/Misleading/False 三态 + 会议动态量表）+ expertise 三审（domain-expert/area-specialist/generalist + competitor cache，固定四档 rubric + Meta ACCEPT/REVISION/REJECT）。**两套评分不合并**，各出一份报告，最后 weakness 去重合并标 [both]/[attitude-only]/[expertise-only]。用户要\"深度审稿\"/\"既抓方法论又抓 novelty delta\"/\"双套 review\"时调用。只要态度三审用 xept:mock-review；轻量自检用 mock-review。"
---

# Dual-Review（双套 reviewer · 评分不合并 · weakness 去重）

> **实现**：复用 [xept:mock-review](../mock-review/SKILL.md)（态度半边）+ 本 skill 新增 expertise 半边（[rubric-expertise.md](rubric-expertise.md) + 3 expertise persona + [search_literature](../../scripts/search_literature.py)/[fetch_literature](../../scripts/fetch_literature.py) cache）+ weakness 去重合并层。设计依据：[docs/improvement-plan.md](../../docs/improvement-plan.md) §5.2/§6（路线 C，competitor cache 解禁）。

## 核心原则

**两套评分系统独立运行、绝不合并分数。** 态度半边（会议动态量表 + Valid/Misleading/False 三态）和 expertise 半边（固定四档 Excellent/Adequate/Weak/Poor + Meta ACCEPT/REVISION/REJECT）各有各的 verdict，仅 weakness 在最后去重合并。

**Iron Law**：

```
NO SCORE MERGING BETWEEN THE TWO HALVES.
两套评分不合并——各有 verdict，仅 weakness 去重。
```

**态度半边不带 cache**（保投稿前自检的轻量定位）；**competitor cache 仅 expertise 半边的 R1/R2 用**（§6 解禁，限定范围）。

<HARD-GATE>
两半边各自的三 reviewer 都**必须**并行独立 sub-agent。态度半边按 [xept:mock-review](../mock-review/SKILL.md) 的 HARD-GATE；expertise 半边见下方 Stage B 的 HARD-GATE。**跨半边不共享 reviewer、不共享评分**——两套独立产出，Stage C 才读两份报告做 weakness 去重。
</HARD-GATE>

**违反字面 = 违反精神。**

## 何时用 / 何时不用

**用**：
- 想要既抓方法论（态度三审的 Valid/Misleading/False）又抓 novelty delta（expertise + competitor cache）的深度 review
- 投稿前想双重交叉验证（两套视角非冗余，C1 验证互补 ≥30%）
- 论文所在领域有大量竞品，novelty 定位需要 full-read 核实

**不用**：
- 只要态度三审 → [xept:mock-review](../mock-review/SKILL.md)（更轻、无 cache 开销）
- 只要单篇快速反馈 → mock-review（dual-review 跑 6 reviewer + cache，重 2-3 倍）
- 论文未编译 / LaTeX 不通过 → 先 [xept:fix-latex](../fix-latex/SKILL.md) 或编译
- 只想标 review 发现到论文 → mock-review + [xept:annotate](../annotate/SKILL.md)

## 流程

### Stage 0 — 准备（两半边共用）

1. **读** `.self_xept/project.yml`（venue / language / main_file / page_limit / anonymity）。
2. **剥注释**（一次，两半边共用）：
   ```
   python scripts/strip_comments.py -o .self_xept/dual-review/.in-progress/paper/ <main.tex 及其 \input 子文件>
   ```
   非零退出 → **中止**，让用户修源码重跑；绝不回退裸 .tex dispatch。
3. **会议研究**（服务态度半边，按 [mock-review Stage 0](../mock-review/SKILL.md) 三层获取评审标准：project.yml → CFP/guidelines → 已知会议惯例 fallback）。

### Stage A — 态度半边（复用 mock-review）

按 [xept:mock-review](../mock-review/SKILL.md) 的 **Stage 1-3** 跑态度三审，**三处覆盖默认**：

1. **跳过 mock-review 的 Stage 0.5**（剥注释）——用 Stage 0 已剥好的 `.self_xept/dual-review/.in-progress/paper/`（非 `.self_xept/mock-review-stripped/`）。
2. **会议标准**用 Stage 0.3 的产出（非重跑）。
3. **产出根目录**改为 `.self_xept/dual-review/.in-progress/attitude/`（非项目根）：
   - 三份 review：`.self_xept/dual-review/.in-progress/attitude/r1.md` / `r2.md` / `r3.md`
   - 最终态度报告：`.self_xept/dual-review/.in-progress/attitude/attitude-report.md`（含 Overall Prediction + 三态 Action Plan + severity tag）

跑完后 `python scripts/verify_review.py .self_xept/dual-review/.in-progress/attitude/attitude-report.md` 自检（退出 1 必须修后才进 Stage C）。

### Stage B — expertise 半边（本 skill 核心）

<HARD-GATE>
三位 expertise reviewer **必须**并行独立 sub-agent。无 reviewer 可见他人输出（含态度半边的 review）。

每个 expertise reviewer sub-agent 的 prompt **必须**含：
1. 其 persona 文件——[./reviewer-domain-expert.md](reviewer-domain-expert.md)（R1）/ [./reviewer-area-specialist.md](reviewer-area-specialist.md)（R2）/ [./reviewer-generalist.md](reviewer-generalist.md)（R3），
2. 共享模板与准则——[./rubric-expertise.md](rubric-expertise.md)，
3. 论文**全文**——`.self_xept/dual-review/.in-progress/paper/` 下剥注释后的每个 `.tex`，reviewer **`read` 全文**（非原始、非摘要），
4. **paper type**（technical / experience，Stage B.0 判定），
5. 输出语言（`.self_xept/project.yml` 的 `paper-review.language`，默认英文），
6. **（仅 R1 & R2）** 其私有 workdir `.self_xept/dual-review/.in-progress/expertise/reviewer-N/`（orchestrator 先建）的绝对路径，以及跑 **competitor-cache 脚本**（`scripts/search_literature.py` + `scripts/fetch_literature.py`）的指令——cache 落 `.self_xept/literature/`。R1/R2 在 sub-agent **内**（非 orchestrator）跑 cache 任务，再起草。

每位 reviewer 的 draft 随后由**独立 checker sub-agent** 核实后才进 Meta-Review。checker prompt **必须**含：[./review-checker.md](review-checker.md)（见下）、**这一份** draft（不含其他）、[./rubric-expertise.md](rubric-expertise.md)、剥注释后论文全文。checker 只报 grounded violations；**原 reviewer sub-agent**（非新 agent）patch 自己的 draft。verify-fix 循环**至多 3 轮**；到顶则 orchestrator 给每条未决项标 `[unverified: <reason>]` 再进 Meta——绝不静默放过未决 review，绝不循环超 3 轮。
</HARD-GATE>

**B.0 判 paper type**——读论文后分 technical（提 method/model/algorithm/system/theory）或 experience（empirical study / 数据分析 / case study）。选 [rubric-expertise.md](rubric-expertise.md) 的准则 1-3（准则 4-5 共享）。三位 reviewer 用你判的这套。

**B.1 并行派 3 expertise reviewer**——用 subagent 工具，三个 sub-agent，payload 见 HARD-GATE。对 R1 & R2，先建 workdir（`mkdir -p .self_xept/dual-review/.in-progress/expertise/reviewer-N`）并传绝对路径——它们在 sub-agent 内跑 cache（persona: "Build background from the paper's competitors"）+ Write `background.md`，再起草。每个 reviewer Write draft 到 `.self_xept/dual-review/.in-progress/expertise/reviewer-N/draft.md` 并返回文本。**保留每个 reviewer sub-agent 的 handle**——B.2 继续它 patch。勿等一个 reviewer 完成才派下一个。

**B.2 verify-fix 每个 review（HARD-GATE 循环，≤3 轮）**——reviewer 返回 draft 后即跑循环；三份的循环各自独立并行。派独立 checker sub-agent（payload 见 HARD-GATE：[./review-checker.md](review-checker.md)、**这一份** draft、[./rubric-expertise.md](rubric-expertise.md)、剥注释 `.tex` 路径——checker 全 `read`，只看这一份 draft）。`VERDICT: CLEAN` 结束该 review。`VIOLATIONS` 则用 `send_message` 发原 reviewer sub-agent（保留其读竞品的上下文）做**针对性 patch**（只改标项，不重写），覆盖 `.self_xept/dual-review/.in-progress/expertise/reviewer-N/draft.md`。HARD-GATE 限 3 轮，未决项标 `[unverified: <reason>]` 再合成。

**B.3 合成 Meta-Review**——三份 verified（或 marked）后，逐准则比三份 review，按 [rubric-expertise.md](rubric-expertise.md) 的 Meta-Review Recommendation 逻辑判 ACCEPT / REVISION / REJECT。**verbatim 用 Meta-Review Template 的三个 `###` 标题**（`### Criterion Consensus` / `### Meta Recommendation` / `### Priority Revisions`）、consensus 表的 `**Recommendation**` 行、`### Meta Recommendation` 下直接 `**ACCEPT/REVISION/REJECT**`——[verify_expertise_review.py](../../scripts/verify_expertise_review.py) 会匹配这些精确字符串（4 段顺序 / 3 Overall 4-tier / Meta 三标题 + ACCEPT/REVISION/REJECT / shortcut 一致性），勿改写/加子节；收敛/分歧折入 Priority Revisions。

**B.4 写 expertise 报告**——按 Reviewer 1/2/3 + Meta-Review 顺序拼成单文件，`write` 到 `.self_xept/dual-review/.in-progress/expertise/expertise-report.md`。三份 review 保持完整独立；Meta-Review 在末尾整合。跑 `python scripts/verify_expertise_review.py .self_xept/dual-review/.in-progress/expertise/expertise-report.md` 自检（退出 1 必须修后才进 Stage C）。

> **Stage A 与 Stage B 并行**——两半边都只依赖 Stage 0（剥注释 + 会议标准），互不依赖。同一消息里派 6 reviewer（3 态度 + 3 expertise），两半边的 checker 循环也各自独立并行。Stage C 等**两份报告都交付**才启动。

### Stage C — weakness 去重合并（评分不合并）

**只合并 weakness，不合并分数。** 收两份报告的 weakness：

- **态度半边**：attitude-report.md 的 Action Plan 项（带 severity tag `[major/minor, fixable/unfixable]` + Valid/Misleading/False 三态）
- **expertise 半边**：三份 review 的 Core Weaknesses（`W`）+ Meta-Review 的 Priority Revisions（带 `[severity, fixability]` tag）

1. **语义聚类**——把两份报告里**指同一问题**的 weakness（不同表述、不同角度）归一簇。聚类是判断（prompt），不下沉脚本。例：态度"ablation 缺组件隔离"+ expertise R1"ablation bundles variables (Novelty/Soundness)"→ 同簇。
2. **每簇标来源**：
   - `[both]`——两半边都点到（最强信号，优先修）
   - `[attitude-only]`——仅态度半边（方法论/三态视角）
   - `[expertise-only]`——仅 expertise 半边（novelty delta/cache 视角）
3. **排序**——`[both]` + major 最先（must-fix），后 `[both]` + minor，再 `[xxx-only]` + major，最后 `[xxx-only]` + minor。同档保态度/expertise 各自的 severity。
4. **产出 unified Action Plan**——`write` 到 `.self_xept/dual-review/.in-progress/merged-action-plan.md`，每条格式：
   ```
   - **[来源] [severity] weakness 摘要** — 见态度 N.M / 见 expertise Reviewer-N N.M
     [1-2 句合并描述；若两半边表述分歧，注分歧]
   ```
   跑 `python scripts/verify_merged_plan.py .self_xept/dual-review/.in-progress/merged-action-plan.md` 自检（每条有来源标 + severity tag；退出 1 必须修后才交付）。

### Stage D — 交付

拼装 `.self_xept/dual-review/dual-review.md`（这一文件——非回复文本——是交付物）：

1. **Attitude Half**（态度半边）——直接内嵌 `.self_xept/dual-review/.in-progress/attitude/attitude-report.md`（Overall Prediction + 三态 Action Plan）
2. **Expertise Half**（expertise 半边）——直接内嵌 `.self_xept/dual-review/.in-progress/expertise/expertise-report.md`（3 review + Meta-Review）
3. **Unified Action Plan**——Stage C 的 merged-action-plan.md（`[both]`/`[attitude-only]`/`[expertise-only]` 去重后）

文件开头加一段顶层摘要：两半边各自的 verdict（态度 Overall Prediction + expertise Meta）+ 共识点 / 分歧点（非合并分数，是并列陈述）。

保留 `.self_xept/dual-review/.in-progress/` + `.self_xept/literature/` 在位供 post-run 检查；下次跑 Stage 0 的剥注释会 wipe `.in-progress/paper/`（cache `.self_xept/literature/` 保留——跨轮共享）。

## Reviewer Personas

### 态度半边（[xept:mock-review](../mock-review/SKILL.md)）

| Reviewer | 态度 | lit task |
|---|---|---|
| 1 | 客观（Objective） | 无 |
| 2 | 严格（Strict） | 无 |
| 3 | 友好（Friendly） | 无 |

态度三审带 Valid/Misleading/False 三态核实 + 会议动态量表——见 mock-review SKILL。

### Expertise 半边

| Reviewer | Expertise | Pre-review lit task |
|---|---|---|
| 1: Domain Expert | whole research area | 论文自有核心竞品 ≤5 全文（全领域） |
| 2: Area Specialist | 1–2 chosen areas | 论文自有核心竞品 ≤5 全文（专项内） |
| 3: General Reviewer | none（paper + own knowledge） | 无 |

R1/R2 跑 cache 脚本（`search_literature` + `fetch_literature`）后起草；R3 无 cache。

## Red Flags — STOP

- "把两套分数平均一下" — STOP. Iron Law：评分不合并。两 verdict 并列陈述。
- "只跑一套省时间" — STOP. 两套都跑（互补 ≥30%，C1 验证）。
- "态度 reviewer 也跑 cache" — STOP. cache 仅 expertise R1/R2（§6 限定范围）。
- "expertise R3 也要读竞品" — STOP. R3 无 cache，凭论文 + 自身知识。
- "两半边共享 reviewer" — STOP. 6 个独立 reviewer，跨半边不共享。
- "Stage C 合并分数" — STOP. Stage C 只合并 weakness，分数各自保留。
- "expertise review 看起来没问题，跳 checker" — STOP. 每 draft 过 checker 才进 Meta。
- "checker 能看其他 review 对比" — STOP. 每 checker 只看自己那份；跨 reviewer 对比是 Meta 的活。
- "loop 到 clean" — STOP. 限 3 轮，未决项标 `[unverified]` 再进 Meta。
- "用会议量表给 expertise 打分" — STOP. expertise 用固定四档（[rubric-expertise.md](rubric-expertise.md)）；会议量表只服务态度半边。

**以上任一 = 撤销违反，重跑。**

## 借口表

| 借口 | 现实 |
|---|---|
| "平均分更客观" | Iron Law：评分不合并。两套设计不同（动态 vs 固定、三态 vs cache-delta），平均无意义。 |
| "态度 + cache 更强" | 态度半边保轻量（投稿前自检）；cache 仅 expertise（§6 限定）。混用破设计。 |
| "一套够" | C1 验证互补 ≥30%（verdict 差异自证非冗余）。两套都跑。 |
| "Stage C 太繁，直接交两份报告" | Unified Action Plan 是 dual-review 的核心增值——去重后作者一份清单。 |
| "expertise R3 没 cache 评不准 novelty" | R3 定位就是"凭论文自证"的通才视角；novelty 的 cache-delta 由 R1/R2 担。 |

## 配套

- expertise 准则：[rubric-expertise.md](rubric-expertise.md)（5 维四档 + paper type + Meta-Review）
- expertise persona：[reviewer-domain-expert.md](reviewer-domain-expert.md) / [reviewer-area-specialist.md](reviewer-area-specialist.md) / [reviewer-generalist.md](reviewer-generalist.md)
- expertise checker：[review-checker.md](review-checker.md)（实现阶段补，参考 mock-review checker + [rubric-expertise.md](rubric-expertise.md) 的 Self-Check）
- cache 基建：[search_literature.py](../../scripts/search_literature.py) + [fetch_literature.py](../../scripts/fetch_literature.py)（must-be-correct，配单测）
- 合并层校验：[verify_merged_plan.py](../../scripts/verify_merged_plan.py)（must-be-correct，配单测）
- 剥注释 + review 校验：复用 [strip_comments.py](../../scripts/strip_comments.py) + [verify_review.py](../../scripts/verify_review.py)（态度半边 mock-review 格式）+ [verify_expertise_review.py](../../scripts/verify_expertise_review.py)（expertise 半边四档+Meta 格式）

## Integration

- **复用**：[xept:mock-review](../mock-review/SKILL.md)（态度半边 Stage 1-3）、[strip_comments.py](../../scripts/strip_comments.py)、[verify_review.py](../../scripts/verify_review.py)
- **新增**：[rubric-expertise.md](rubric-expertise.md) + 3 expertise persona + review-checker.md + [search_literature](../../scripts/search_literature.py)/[fetch_literature](../../scripts/fetch_literature.py) cache + [verify_merged_plan.py](../../scripts/verify_merged_plan.py) + [verify_expertise_review.py](../../scripts/verify_expertise_review.py)
- **前置**：论文须编译（[xept:fix-latex](../fix-latex/SKILL.md) 或 pdflatex）
- **下游**：[xept:annotate](../annotate/SKILL.md)（把 merged Action Plan 标进论文不改原文）/ [xept:write-revision](../write-revision/SKILL.md)（按 plan 改论文带 `\revadd`/`\revdel`）

---

## 立项验收清单（review 用）

- [ ] discipline 三件套（Iron Law 评分不合并 + HARD-GATE 6 reviewer 并行独立 + 借口表 + Red Flags），符合 [B1-1 writing-skills](../writing-skills/SKILL.md) 分类
- [ ] Stage A 复用 mock-review（不复制态度三审逻辑，DRY），三处覆盖默认写明（剥注释 / 会议标准 / 产出根）
- [ ] Stage B expertise 半边 HARD-GATE 完整（3 persona payload + checker 循环 ≤3 轮 + cache 仅 R1/R2）
- [ ] Stage A/B 并行写明（同一消息派 6 reviewer）
- [ ] Stage C 只合并 weakness 不合并分数（语义聚类 + `[both]`/`[attitude-only]`/`[expertise-only]` + 排序）
- [ ] Stage D 交付单文件 dual-review.md（两份报告 + Unified Action Plan），开头并列两 verdict（非合并）
- [ ] cache 仅 expertise R1/R2、态度不带 cache（§6 限定范围，呼应 [improvement-plan §6](../../docs/improvement-plan.md)）
- [ ] 方言合规（`xept:` 引用、`.self_xept/dual-review/` 元状态、中文正文、无 `pp:`/平台工具残留）
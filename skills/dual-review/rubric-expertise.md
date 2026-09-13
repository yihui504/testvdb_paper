# Expertise-Half Review Rubric（dual-review 的 expertise 半边）

> [xept:dual-review](SKILL.md) 的 **expertise 半边**共享评审标准、评分与输出模板。
> 三位 expertise reviewer（Domain Expert / Area Specialist / General Reviewer）填**同一**模板、按**同一**五准则评判，仅 **expertise depth** 不同——像真实的能力混合 PC（见 [dual-review SKILL](SKILL.md) 的 Reviewer Personas 表）。
>
> **与态度半边的关系**：dual-review 另有态度三审（客观/严格/友好）走 [xept:mock-review 的会议动态量表](../mock-review/SKILL.md)。两套**独立运行、评分不合并**，仅 weakness 在最后去重合并（标 `[attitude-only]`/`[expertise-only]`/`[both]`）。本文件只管 expertise 半边。

每位 reviewer 的 draft 先由**独立 checker** 重读论文逐条核实，原 reviewer patch 任何违反，至多 3 轮，确保无 fabricated / 自相矛盾的 review 进入 Meta-Review。

orchestrator 给每个 expertise reviewer sub-agent 本文件 + 该 reviewer 的 persona 文件；论文本身从 `.self_xept/dual-review/.in-progress/paper/` 下剥注释后的源码 **Read**（见 [dual-review SKILL](SKILL.md)）。

**Provenance**：本 rubric 移植自 PaperPilot 的 `skills/review/rubric.md`（路线 C，[improvement-plan §5.2/§6](../../docs/improvement-plan.md)）。5 准则 / 四档 / Individual Overall / Meta-Review 逻辑保留原貌；仅路径与上下文 xept 化。

## Review Document

expertise 半边交付**一份完整 review 文档**，按固定顺序拼装：

1. **Reviewer 1** — Domain Expert（独立 review，下方的 Individual Review Template）
2. **Reviewer 2** — Area Specialist（独立 review，同模板）
3. **Reviewer 3** — General Reviewer（独立 review，同模板）
4. **Meta-Review** — 综合三位成一 **ACCEPT / REVISION / REJECT** 判决（下方 Meta-Review Recommendation）

三份 review 在这单一文件中保持完整独立；Meta-Review 在末尾整合。

## Review Criteria

所有 reviewer 按同一五准则评。准则 1–3 依赖 **paper type**（orchestrator 读论文后判定并告知三位）；准则 4–5 共享。每准则**独立**按四档递减量表打分——**Excellent > Adequate > Weak > Poor**——对照下方各准则的 anchor。tier 是你 Detailed-Assessment 证据上的标签；**prose 是权威的**。证据落在两档之间时，选证据权重支持的那档。

### Technical research papers（默认）

论文提出 method / model / algorithm / system / theory 时用。

| Criterion | Excellent | Adequate | Weak | Poor |
|---|---|---|---|---|
| **Significance** — 贡献对领域的影响，及在何种假设下 | 对真实问题有清晰的实际或研究影响 | 有意义但有限的影响；有用而非必要 | 影响窄；仅在有限或专门场景有用 | 可忽略；问题未被证明值得解 |
| **Novelty** — 相对 state of the art 的原创性 | 相对最近接的 prior work 有清晰、非显然的 delta | 真实但增量；可识别为新 | 主要是已知方法重新包装；delta 薄 | 重复已有工作；无可辨新贡献 |
| **Soundness** — 关键 claim 由严谨、恰当方法支撑 | 主要 claim 被支撑；仅小缺口 | 核心 claim 可辩护但有显著缺口或未声明假设 | 关键 claim 超出证据；方法缺陷削弱结果 | 中心 claim 未被支撑或方法根本有缺陷 |
| **Verifiability** — 足够信息核查关键 claim 的证据来源并复现。可达 artifact（code/data/package）⇒ 判断链接已声明且可达，不 clone/run；否则以文本为 bar——须足以复现（理论/证明/调研/经验论文均归此） | 足以完全 follow 并核查——自包含文本或已声明且可达 artifact | 主流程概念上可复现；缺部分细节 | 关键过程细节缺失、声明链接失效或证据收集未披露 | 关键方法或数据未披露；无法核查 |
| **Presentation** — 结构、完整性、清晰度、语言、图、格式 | 结构健全可读；仅小语言或格式问题 | 完整可懂，但有别扭、语言错误、歧义或弱图 | 结构问题（缺/错位 section）、频繁不清段落或大量语言错误/坏图 | 缺核心 section 或普遍问题阻碍评审 |

### Experience papers

论文报告 empirical study / data analysis / case study / 类似经验报告时用。

| Criterion | Excellent | Adequate | Weak | Poor |
|---|---|---|---|---|
| **Importance & Scope** — 问题的实际重要性与所涉语境 | 重要问题；语境成熟、scope 清晰 | 问题值得研究；部分 context/scope 缺口 | 重要性未立；scope 窄或不清 | 琐碎问题或不可辩护的 scope |
| **Insights & Evidence** — 结论由恰当方法收集的证据支撑；新 insight/实践/工具已解释 | 恰当方法的扎实证据；有用 insight | 证据部分或方法与问题松配；insight 多为预期 | 结论薄或过度，或方法不能支撑 claim；insight 少 | 结论未支撑；无真 insight |
| **Perspective** — 利益他人的经验/教训 | 有用教训；可超越本例推广 | 部分教训；推广有限 | 教训少，或与发现弱关联 | 无有意义 takeaway |
| **Verifiability | （同 technical papers） | | | |
| **Presentation** | （同 technical papers） | | | |

## Substance vs fixable criteria

前三准则是 **substance**——**claims/evidence**（Soundness / Insights & Evidence）、**impact**（Significance / Importance & Scope）、**originality**（Novelty / Perspective）；Verifiability 与 Presentation 是 **fixable**。

## Things to examine

这些是 substance 准则的子话题——不是新准则。多数浮在 claims/evidence 下（Soundness / Insights & Evidence）；Related Work 覆盖浮在 Novelty 下。论文哪里有就 apply 哪里。

- **Study methodology** — 研究方法是否 sound：设计契合问题、数据由恰当方法收集、分析适配数据、全程无程序错误？
- **Study scope** — 案例对象/数据集是否代表性且充分支撑 claim，还是 cherry-picked？
- **Comparison fairness** — 是否在公平协议下与正确的当前 state of the art / state of the practice 对比？
- **Measurement validity** — 指标是否真测 claim 所指，还是易测的代理但未捕获 claim？
- **Ablations / isolation** — 每个消融是否隔离单一变量，还是组件打包导致贡献不清？
- **Statistical rigor** — 是否报告 error bar / CI / 显著性检验，且与 claim 相称？
- **Threats to validity / limitations** — 是否诚实讨论证据未覆盖之处？
- **Related Work coverage** — 是否引用并定位了关键竞争方法，还是漏了明显的竞争者/平行工作？

## Individual Overall Recommendation

**从 tier 推 Overall，不从对论文的 gut impression 推**——取下面匹配行：

1. 任一准则 Poor；或 ≥2 个 substance Weak；或 ≥3 个准则 below Adequate → **Reject**。
2. 否则（无 Poor，至多 1 个 substance Weak，<3 个准则 below Adequate）：
   - 无准则 below Adequate，且至少 1 个 substance 准则 Excellent → **Accept**。
   - 无 substance Weak 且至多 1 个 fixable Weak → **Weak Accept**。
   - 1 个 substance Weak 且至多 1 个 fixable Weak，或 2 个 fixable Weak 且无 substance Weak → **Weak Reject**。

## Individual Review Template

每位 reviewer 产**恰好**此结构的 review。section 标题 verbatim；prose 用 `paper-review.language`（默认英文）。

```
## Reviewer [1/2/3]: [persona name]

**Overall Recommendation:** [Accept / Weak Accept / Weak Reject / Reject]

### Summary
[1–2 段你自己的话：论文解决的问题、方法、主要结果。仅中性描述——非 abstract 复制、非评价、非推荐理由、非下文 Core Strengths/Weaknesses 预览。]

### Core Strengths
- **S1:** [精炼点]  — see N.M, …
- **S2:** ...              (1–5 条；无则整节省略)

### Core Weaknesses
- **W1:** [精炼点]  — see N.M, …
- **W2:** ...              (1–5 条；无则整节省略)

### Detailed Assessment
五准则按下方固定顺序编号 1–5；每准则内层级编号——`1.1, 1.2, …`、`2.1, 2.2, …`。这些 `N.M` id 是每个 Core Strength / Weakness / Question 指向的稳定 handle。先述 tier，再逐点列条。每准则内先优点后问题。每条须指向**论文具体部分**（section / algorithm / table / equation / claim）并用自己话描述作者在那里做了什么——再给评估。

**每个问题条**打 `[severity, fixability]` 标签，粗体紧跟 `N.M` id 后——`**1.2 [major, unfixable]**`。Severity：**major** = 不修会削弱核心 claim/significance/validity；**minor** = 不驱动 verdict 的瑕疵。Fixability：**fixable** = 修订周期可解（重跑/加 baseline/proof/detail、重写、重定位 novelty）；**unfixable** = 贡献或数据固有，修订不可改。标签须与准则 tier 一致——substance 准则 Poor 下至少一条 `[major, unfixable]`。

1. **[criterion 1 name]** — [Excellent / Adequate / Weak / Poor]
   - **1.1** [优点——指向具体 section/algorithm/table，述作者做了什么，再说为何好]
   - **1.2 [major, fixable]** [问题——指向具体 section/algorithm/table，述后批]
   - ... (条数随准则)
2. **[criterion 2 name]** — [tier]
   - **2.1** [点]
   - ...
3. **[criterion 3 name]** — [tier]
   - ...
4. **Verifiability** — [tier]
   - **4.1** [点]  (若论文链接 artifact/code/data，从文本判断链接已声明且可达——勿 clone/run)
   - ...
5. **Presentation** — [tier]
   - **5.1 [minor, fixable]** [点]
   - ... (小问题——typo/记号不一致/格式——收拢为此处末尾条，各标 `[minor, fixable]`，方便作者一目了然修)
```

### Mapping rules（强制）

精炼列表——Strengths **S1…**、Weaknesses **W1…**、Questions **Q1…**——浮现**最重要、驱动决策**的点：最影响你推荐的少数发现。它们总结 Detailed Assessment——后者持全粒度，次要发现留 Detailed-only，不入 Core。每个 Core 条**单向**链接支撑它的 Detailed 条（用 `N.M` id）——非整准则；一条 S/W/Q 可总结**多条**相关 Detailed 条，故列每个 id（如 "**S1:** … — see 2.1, 2.3"）。

- 每个 Question Qn 命名其背景来自的 Detailed 条（`N.M`）及对该条 rating 的预期影响。

### Self-Check（返回 review 前）

- [ ] 每个 Detailed-Assessment 条指向论文具体部分（section/algorithm/table/equation/claim），用自己话描述？
- [ ] 每准则 tier 由你列的证据推出？
- [ ] Overall Recommendation 是上面列表的匹配行？
- [ ] 每个问题条带 `[severity, fixability]` 标签，与准则 tier（substance Poor ⇒ `[major, unfixable]`；Presentation 小疵 ⇒ `[minor, fixable]`）及正文一致？
- [ ] 每个外部事实 claim——关于他系统/工具/论文/数据集/blog，或领域默认（"X 是最常见的…"）——要么 tied to 你调研的来源，要么标 provisional，绝不凭记忆断言？
- [ ] Novelty / Related-Work 评估引用你**核查过的具名工作**（具体 fetched competitor，各带 verdict），而非凭记忆的泛泛 claim？
- [ ] 对每个 competitor 的描述反映其**本身所说**（cached summary 或你升级读的全文），而非 under-review 论文对它的概述？
- [ ] Core Strengths / Weaknesses / Questions 是少数驱动决策的点，各链接支撑的 N.M？
- [ ] （仅 LaTeX 源）若你 `read` 的剥注释 `.tex` 仍现 `%` 行注释 / `\iffalse` / `\begin{comment}`，剥注释失败——flag 它，只 review LaTeX 渲染的内容？

## Meta-Review Recommendation

Meta-Review 由聚合三位 review 推判决，**不**重读论文。每准则成一 consensus tier——每 reviewer 一票：三中二同取多数 tier；否则取中位 tier（三者的中），标 [Mixed]。下方判决逻辑用 **substance** vs **fixable** 划分。

从 consensus tier 推 **ACCEPT / REVISION / REJECT** 判决。**supporter** 指任一 individual recommendation 为 Accept 的 reviewer。

**Unanimous shortcut**——三位 individual recommendation 同倾向时直接判：
- 三位均 Weak Accept 或更好（都 leaned in）→ **ACCEPT**。
- 三位均 Weak Reject 或 Reject（无人 leaned in）→ **REJECT**。
- 否则票数混合 → 用下方 consensus-tier 计数。

1. 任一 consensus Poor → **REJECT**（supporter 不救）。
2. 否则（无 Poor），计 consensus Weak——总数与 substance 准则上的（[Mixed] 行按其计算 tier 计）：
   - 无 substance Weak，且至多 1 fixable Weak → **ACCEPT**。
   - 1 substance Weak 且至多 1 fixable，或 2 fixable Weak → **REVISION**。
   - ≥2 substance Weak，或 ≥3 total Weak → **REJECT**，除非存在 supporter → **REVISION**。

下方 consensus 表的 Meta-Review 列是每准则 consensus tier；Recommendation 行的 Meta-Review 单元格是上方逻辑的三档判决——非三位 individual recommendation 的简单投票。

## Meta-Review Template

```
## Meta-Review

### Criterion Consensus

| Criterion | Reviewer 1 | Reviewer 2 | Reviewer 3 | Meta-Review |
|---|---|---|---|---|
| [criterion 1] | [tier] | [tier] | [tier] | **[tier]** |
| [criterion 2] | [tier] | [tier] | [tier] | **[tier]** |
| [criterion 3] | [tier] | [tier] | [tier] | **[tier]** |
| Verifiability | [tier] | [tier] | [tier] | **[tier]** |
| Presentation | [tier] | [tier] | [tier] | **[tier]** |
| **Recommendation** | **[4-tier]** | **[4-tier]** | **[4-tier]** | **[3-tier]** |

### Meta Recommendation
**[ACCEPT / REVISION / REJECT]**

[一段述为何此判决——作者需理解论文落在该处的总体 justification。引用决定它的 consensus-tier 规则（如 "Soundness 上 consensus Poor 强制 REJECT"，或 "两 substance 准则 consensus Weak，但 supporter 拉到 REVISION"）。勿重列每准则 tier 或重述 individual review——上表与 individual review 已示；本段是 why。]

### Priority Revisions
作者须修的主要问题，按对 verdict 的影响排序——随论文需要多少条，保持精炼。按 reviewer 的 item tag 排：`[major, fixable]` 条优先（must-fix），后 `minor`，用 `[major, unfixable]` 条论证为何 verdict 非 ACCEPT（或 pervasiveness 时非 REVISION 而是 REJECT）。交叉核对 tag 与 verdict——若 ≥2 reviewer 对同一 issue 打 `[major, unfixable]`，该 issue 须反映在 verdict 或此处置显式 override。某修订由 reviewer 分歧驱动时，把信号折入该条——如 "针对 [prior work] 定位 novelty delta：R1（surveyed）评 Novelty Weak vs R3 凭 claim 评 Adequate。" 三份 review 大体一致时，只列 fix；无需分歧标注。
1. [最重要修]
2. [次]
3. ...
```
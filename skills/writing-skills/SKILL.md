---
name: writing-skills
description: 创建/修改/审计 xept 任何 skill 时使用——RED-GREEN-REFACTOR 方法论（先看无 skill 怎么失败→写最小 skill 堵那个失败→堵漏洞）、失败类型→正确形态映射、discipline/technique/reference 三类划分、gate 必须是脚本的规则、SDO description 陷阱。改 skills/ 下任何 SKILL.md 前先读本技能 + [CLAUDE.md](../../CLAUDE.md) 方言。
---

# Writing Skills（写 / 改 skill 方法论）

> **与 [CLAUDE.md](../../CLAUDE.md) skill 方言互补**：CLAUDE.md 管**格式方言**（slug 连字符、frontmatter、`xept:<slug>` 引用、平台工具映射、`<HARD-GATE>` 写法、平台残留零容忍）；本技能管**内容结构**（怎么决定 skill 长什么样、怎么验证它有效）。冲突以 CLAUDE.md 为准；工程规范（脚本/测试/提交）见 [docs/conventions.md](../../docs/conventions.md)。

## 核心原则

**写 skill = 针对一个观察到的失败，写最小的、能堵住那个失败的文档。**

不是"把我知道的写下来"，是"堵一个具体的、看过的失败"。没看过失败就写 skill = 写没有测试的代码。

**Iron Law**（改 `skills/` 下任何文件前）：

```
NO SKILL EDIT WITHOUT EVIDENCE OF FAILURE.
```

"failure evidence" = 要么跑过一次无 skill 的 baseline 看到 agent 怎么偏离，要么有具体的、已知的、可描述的失败 case（如路线 A 的真实事故："reviewer 引用 `\iffalse` 草稿表格"——口头'别看注释'被绕过）。凭"我觉得该加一节"不构成 evidence。

> **务实例外（路线 A/B 场景）**：借鉴成熟外部设计（如路线 A 移植的 strip_comments / checker / verify_revision）时，外部设计已有的测试证据可作 evidence；但移植后**必须在 xept 跑 GREEN**——真跑 skill 确认行为没在移植中漂移。form 可借，behaviour 必须自证。

## 何时该做 skill / 不该做

**做**：判断性方法（打分、评级、改写、审稿）；跨项目复用的技术；需要 discipline 约束的流程。

**不做**（[conventions.md](../../docs/conventions.md) §1 务实混合）：
- **确定性算法** → 写脚本（剥注释、投影验证、去重合并、检索 I/O、配置字段反推）
- **机械约束**（能用正则/校验器强制）→ 脚本（`verify_review.py` 校验 tag 合法性，而非 prompt 提醒）
- **一次性方案 / 项目特定约定** → 写进 CLAUDE.md / AGENTS.md
- **已有 skill 覆盖** → 扩展现有 skill，不新建

## skill 三类（决定要不要 discipline 装置）

| 类型 | 定义 | 需要 | xept 案例 |
|---|---|---|---|
| **discipline**（纪律） | agent 知道规则但压力下会违反 | Iron Law + Red Flags + 借口表（§discipline 三件套） | [xept:mock-review](../mock-review/SKILL.md)（三审独立 / 剥注释 / checker 循环）、[xept:write-revision](../write-revision/SKILL.md)（round-trip 验证不过不交付） |
| **technique**（技法） | 具体 how-to 方法 | recipe / Process（步骤序列） | [xept:write-paper](../write-paper/SKILL.md) 各阶段、[xept:add-citation](../add-citation/SKILL.md)、[xept:paraphrase](../paraphrase/SKILL.md) |
| **reference**（参考） | API/格式/命令/路由文档 | 可检索结构，**无** discipline 装置 | [xept:setup-venue](../setup-venue/SKILL.md)（venue 元数据）、[xept:using-xept](../using-xept/SKILL.md)（意图→技能路由表） |

**关键**：reference skill 不需要 Iron Law / Red Flags——加了是噪声。discipline skill 必须有三件套，否则压力下会被绕过。

## Match the Form to the Failure（写规则前先分类失败）

同一规则，针对不同失败类型，对的形态不同。选错形态会**反向恶化**。

| baseline 失败 | 对的形态 | 错的形态 |
|---|---|---|
| 压力下违反规则（知道却做不到） | 禁令 + 借口表 + Red Flags（discipline 三件套） | 软引导（"prefer..."、"consider..."） |
| 遵守了但输出形状错（冗长、buried、restated） | **正面 recipe / 契约**：说输出**是什么**（其部件、按顺序） | 禁令列表（"don't restate"、"never narrate"） |
| 漏掉本该有的元素 | **结构**：模板里 REQUIRED 槽（校验脚本精确匹配） | 模板旁的散文提醒 |
| 行为依赖条件 | **可观测谓词键控**（"若 `.self_xept/project.yml` 的 `state=revision`，则..."） | 无条件规则 + 豁免条款 |

**两条硬规则**（选了任何形态都适用）：
- **不要 nuance 子句**："除非重要的别 X" 会重开谈判——把真正例外写成独立的、可观测谓词条件。
- **豁免条款不 scope**："本限制不适用于代码块"仍会压制代码块——若部分输出需豁免，重构让规则够不着它。

完整对照与测试证据见 [writing-a-skill.md](writing-a-skill.md) §4。

## discipline 三件套（discipline skill 专属）

三件是流水线 **Rule → Rebuttal → Detection**，各自独立挣得，不是固定模板：

1. **Iron Law**（Rule）：单一 ALL-CAPS 行，`code fence` 包裹，内嵌补救动作。仅当违反 = 根本性崩溃时携带（如"不过验证不交付"）。
2. **借口表**（Rebuttal）：`| 借口 | 现实 |` 表。**每一行必须是 baseline 测试里逐字抓到的真实借口**，不发明。只抓到一个借口 → 折进 Iron Law 散文，不要单行 thin 表。
3. **Red Flags**（Detection）：触发短语列表，让 agent 实时自 catch。每条 3-8 词，TDD 风格（如 `"我只改了一个 typo"` / `Code before test`）。

参考 [xept:mock-review](../mock-review/SKILL.md) 的 Stage 1.5 `<HARD-GATE>` + "checker 纪律"段 = 完整三件套样例。

## gate 必须是脚本（不是 prompt 自检）

<HARD-GATE>
若一个 gate 要**证明一个结构不变量**（标记 round-trip、注释纯插入、tag 合法性），它**必须是确定性脚本**，不能是 prompt 驱动的启发式自检。
</HARD-GATE>

**为什么**：prompt 自检"我只加了 note 没改原文"会放过 agent "顺手改了个 typo" 的案例——它注意到的 case 过，没注意到的 case 静默漏。git-diff + grep 让就地原文编辑溜过去。要证明结构性质，只能用脚本投影比对。

**xept 已有的 gate 脚本**（must-be-correct，[conventions.md](../../docs/conventions.md) §3.3）：
- [verify_revision.py](../../scripts/verify_revision.py)：`accept(marked)==new ∧ reject(marked)==old`（round-trip）
- [verify_review.py](../../scripts/verify_review.py)：tag 合法性 + 段标题 verbatim
- [strip_comments.py](../../scripts/strip_comments.py)：剥注释物理去除（fail-closed，不平衡退出 1）

**规则**：新 skill 若带 gate，照此模式——写 must-be-correct 脚本 + 配 pytest 单测（覆盖率 ≥90%）+ SKILL 里写 emit→verify→repair 循环（≤5 轮，不过不交付）。样例：[xept:write-revision](../write-revision/SKILL.md) Part 2。

## RED-GREEN-REFACTOR（skill 的 TDD）

| TDD | 写 skill |
|---|---|
| 测试用例 | 压力场景（discipline）/ 应用场景（technique）/ 检索场景（reference） |
| **RED** | 跑无 skill 的 baseline，**逐字记录** agent 怎么偏离、用什么借口 |
| **GREEN** | 写最小 skill 堵那些**具体**偏离（不为假设 case 加内容）；跑同一场景确认遵守 |
| **REFACTOR** | 找新借口 → 加显式反驳 → 重测到 bulletproof |

**Micro-test 先于全场景**（措辞验证，便宜）：
1. 每次一个 fresh-context 样本；system prompt = 指导将真实生存的上下文（完整 skill，非孤立指导）；user = 诱发该失败的任务。
2. **总要含无指导对照组**。对照组没出现该失败 → 没东西可修，停。
3. 每变体 ≥5 次（单样本会撒谎）。
4. 手读每个命中（模板回声 / 引用反例会冒充命中）。
5. **方差是指标**：指导生效时多次 rep 收敛到同一形状；5 次 5 种解读 = 措辞没约束力，先收紧形态再加词。

完整执行手册（压力场景写法、Phase 0-6、plant-one-signal-per-defect、open-scan vs closed-taxonomy、subagent dispatch 纪律）见 [writing-a-skill.md](writing-a-skill.md)。

## SKILL.md 结构（逐节）

```
frontmatter（name + description：中文开头 + 触发条件 + 边界声明）
# English Title（中文标题）
## Overview（verb-sequence 开场或一句 what+why + 一句核心原则）
## 何时用 / 何时不用（和 description 互补，不重述；何时不用只写真实边界）
## Iron Law（discipline 才有）
## Process / 工作流（recipe：### Step N: Name + 一行祈使句）
## Quick Reference（表/紧列表，reference 材料拉出 Process）
## Red Flags / 借口表（discipline 才有）
## Integration（上下游 skill 链）
```

**Process 写法**（细节 [writing-a-skill.md](writing-a-skill.md) §5）：
- 本质行：一句、3-4 个动词、telegraph 全流程。
- `### Step N: Name` 作 H3，不折进第一条 numbered item。
- 祈使密度 ~100%，每条一行；禁 "You should..." / "建议..."。
- reference 材料按重量摆：≤3 项内联；~4 项放 Quick Reference；5+ 项放专门 `##` 节（表）；长形进 companion 文件。
- **三层分离**：step 写 **what**；why 在 Overview/Iron Law；how（重型 reference）在 companion / Quick Reference。三层混进一个 step 是最常见的清晰杀手。

## Skill Discovery Optimization（被发现的概率）

**description 陷阱**（最关键）：description **只写何时用**，**绝不**总结 workflow。

测试发现：description 一旦总结 workflow，agent 会跟着 description 走、不读 skill 正文。一份说"派 subagent + 中间 review"的 description 导致 agent 只做**一次** review，尽管正文要求两阶段。

```yaml
# 错：总结了 workflow
description: 模拟审稿——派 3 个子代理各出 review，主代理逐条核实 weakness

# 对（xept 方言：中文开头 + 触发条件 + 边界）
description: 投稿前模拟目标会议/期刊审稿流程自检。用户要"模拟审稿"/"投稿前自检"/"我这论文能投吗"时调用。已投稿改稿用 xept:write-revision；逐条回复审稿人用 xept:write-response。
```

**keyword 覆盖**：用 agent 会搜的词——错误信息、症状、工具名、同义词。

**token 效率**：skill 加载进上下文，每个 token 都算。频繁加载的（如 using-xept）<200 词；其余 <500。重型 reference（100+ 行）和可复用工具进 companion 文件，相对路径链接，**绝不**用 `@` force-load（烧 200k+ 上下文）。

## 改 skill 后必做（对齐 [CLAUDE.md](../../CLAUDE.md)）

1. `grep` 旧下划线 slug 与平台工具名（`get_knowledge`/`compile_latex`/`live_edit`/`confirm_plan`/`search_venue_db`/`manage_files`/`paper_state`/HTML `<span>`）→ 归零
2. frontmatter 齐全（首行 `---`，name 连字符、description 中文开头）
3. must-be-correct 脚本改动 → **先改/先跑测试**（[§3.3](../../docs/conventions.md)）
4. 输出契约 verbatim（改标题同步改校验脚本）

## 借口表（跳过测试的常见合理化）

| 借口 | 现实 |
|---|---|
| "skill 写得很清楚，不用测" | 你觉得清楚 ≠ agent 觉得清楚。测。 |
| "只是个 reference skill" | reference 也有缺口。测检索场景。 |
| "测一下太慢" | 15 分钟测试省几小时线上 debug。 |
| "出了问题再测" | 问题 = agent 用不了 skill。部署前测。 |
| "借鉴的成熟设计，不用测" | 移植后行为会漂移。至少跑 GREEN。 |
| "改一节小调整，不用 RED" | 编辑 = 新行为 = 新测试义务。看过失败再改。 |

**以上任一 = 先跑测试再动手。**

## Integration

**链外 meta-skill**：本技能**不在** xept 的论文生产链（`setup-venue → write-paper → ... → mock-review`）里。它是**开发和审计** `skills/` 下任何 skill 的方法。创建/修改任何 skill 前用它。

- 格式方言：[CLAUDE.md](../../CLAUDE.md) + [docs/tool-mapping.md](../../docs/tool-mapping.md)
- 工程规范：[docs/conventions.md](../../docs/conventions.md)
- 执行手册（RED-GREEN-REFACTOR 细节、压力场景、subagent dispatch 纪律、好坏表达对照）：[writing-a-skill.md](writing-a-skill.md)

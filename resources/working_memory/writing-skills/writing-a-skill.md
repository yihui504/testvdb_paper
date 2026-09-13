# Writing a Skill — 执行手册

> 本文档是 [SKILL.md](SKILL.md) 的 companion：SKILL.md 给方法论核心，本文档给**怎么执行**——完整 RED-GREEN-REFACTOR 流程、压力场景写法、Process 写法细节、好坏表达对照、subagent dispatch 纪律。
>
> 权威方法在 [SKILL.md](SKILL.md)；每个 skill 自己的 SKILL.md 是该 skill 行为的唯一真相。本文档持"好 skill 长什么样"的标准。

## 1. 这文档何时用

- **新建 skill**：从 Phase 0 走到 Phase 6。
- **改现有 skill**：先跑 Phase 1（characterize 当前失败）再改；改完跑 Phase 4（GREEN）。
- **审计 skill**：用 §2-§5 的标准逐项过。

## 2. creation flow（新建 skill 的 6 阶段）

### Phase 0 — Worth making?
过 [SKILL.md](SKILL.md) "何时该做 / 不该做"门：不是确定性算法、不是机械约束、不是一次性、不是已有 skill 覆盖。确认通过再进 Phase 1。

### Phase 1 — Characterize the failure（RED）
看 agent 在**没有这个 skill** 时怎么失败。两条路：
- **跑 baseline**：给一个 subagent 任务（不带 skill），逐字记录它怎么偏离、用什么借口。压力格式见 §3。
- **已有证据**：路线 A/B 的真实事故、用户 bug 报告、code-review 发现的偏离——这些**就是** RED 证据。

**没有具体失败在手 → 停**。你在为想象的问题造 skill。

### Phase 2 — Type → form
分类失败（discipline / technique / reference，见 [SKILL.md](SKILL.md) 三类表），读出形态：
- discipline → Iron Law + Red Flags + 借口表
- 技形错（输出形状）→ recipe
- 漏元素 → REQUIRED 槽
- 条件依赖 → 可观测谓词

**形态层**（apparatus、layout、opener）从类型 + 样例 skill 读出，不需 RED。

### Phase 3 — Behaviour from the failure
填每条禁令、每个 Red Flag、每行借口表——都从 Phase 1 的失败来，**不发明**。这是形态/行为分离里需要 characterized failure 的那层。

### Phase 4 — GREEN
真跑 skill。**形态过 ≠ 工作**——只有 GREEN（带 skill 跑真实任务、确认行为对）才算。xept 的 GREEN 手段：
- 脚本层 skill：跑 pytest 单测（[conventions.md](../../docs/conventions.md) §3.3）
- LLM 编排 skill：跑 `tests/skill-triggering/`（naive prompt 触发）+ `tests/review-eval/`（植入缺陷 recall）
- 手动：装 xept 插件真跑一次

### Phase 5 — REFACTOR
堵 GREEN 里冒出的新借口/漏洞；只为你**实际观察到**的合理化加反驳。

### Phase 6 — Commit
对齐 [conventions.md](../../docs/conventions.md) §7：Conventional Commits、一次一改、正文含测试证据、改 must-be-correct 脚本的提交须含"跑了什么 + 结果"。

## 3. 压力场景设计（discipline 测试）

discipline skill 必须在**压力下**测——agent 知道规则但会找借口绕过。

### 压力类型（组合使用）
- **时间压力**："deadline 前必须交"
- **沉没成本**："已经写了 2000 字了，别推翻"
- **权威压力**："审稿人是资深专家，他说删就删"
- ** exhaustion**："这是第 8 轮 repair 了，差不多就行"

### Plant one signal per defect（测试 fixture 纪律）
一个证明"某维度/某 gate 会 fire"的 fixture，**只触发被测的那个信号**。
- 反例：一个植入的"语域 shift"**同时**是技术错误（把 GCN 描述成 autoregressive）→ fire 了 HIGH，但 HIGH 骑在准确性错误上，**不能**证明语域维度工作。
- 正例：净化到"只语域 shift"（口语化但技术正确）→ 稳定 fire MEDIUM，且只 fire 语域维度。

**堆叠的缺陷只能证明'有东西被抓住了'，证明不了'哪个信号抓住的'。**

### Open scan vs closed taxonomy
finder skill 建在固定维度表上（如 grammar 8 维、doc-check 18 维）时，两件事要解耦：
- **filing enum**（`dimension:` 字段，下游 merge 按它）→ **CLOSED**（固定集合，输出从中选）
- **scan scope**（扫什么）→ **OPEN**（列出的维度是 required 核心，**非天花板**）——列表外的真缺陷也要报，归到最近维度。

测过：closed-scan framing（"只跑固定 checklist"）系统性漏掉列表外错误；open-scan（"report every defect, listed or not, under closest dimension"）把 off-list recall 从 ~7/11 提到 10/11，无 precision 损失。

### Zero hits 不代表死维度
某维度在某个 corpus 上 0 次 fire，**不**说明该维度没用——可能 corpus 太干净。砍维度前先植入它该抓的缺陷，看它（而非邻居）fire。低 base-rate 维度（如 bias）是便宜的安全网。

## 4. Match-the-Form 完整（SKILL.md §的展开）

[SKILL.md](SKILL.md) 给了 4 行表。这里补测试证据和复合案例。

**为什么禁令在 shaping 问题上反向恶化**：竞争激励下（"让 prompt 自包含"），agent 会和 "don't X" 谈判。recipe 不留谈判空间——输出要么匹配声明形状，要么不匹配。

**两层失败可复合**：一个 recipe 看着对（形状），但仍漏（行为）。例：recipe 说"exactly these fields, nothing else"，agent 在成本压力下读了 closure 还是加了第五块，合理化为"必要 scope"。这是 **discipline 失败穿 recipe 衣服**——cure 是加 Red Flag 点名该合理化并 reframe（"context 描述文档，不描述忽略什么"），不是强化 closure 措辞（重开谈判）也不是丢 recipe（形状对）。

**诊断**：agent 读了 closure 还加内容 + 合理化语言 → discipline；单纯产出错形状 → shaping。

## 5. Process 写法细节

### 本质行（essence line）
一句、3-4 个动词、telegraph 全流程：*"读意见 → 定 new → 标 marked → round-trip 验证 → 交付"*。所有 telegraph（Overview 开场、本质行、"分 N 步"引导）必须 phase 数一致——可压缩子步，**绝不**显示和你声称不同的 count。

### Step headers
`### Step N: Name` 或 `### Phase N:` 作 H3。**不要**折进第一条编号项作 `1. **Step name** —`。读者按标题导航。

### 祈使密度 ~100%
每条一行祈使句（"Read plan file"、"派一个 finder per..."）。禁 "You should..." / "建议..." / "It is recommended that..."。真密度项拆 sub-bullet，不写 run-on 段。

### reference 摆放（按重量）
- ≤3 项某 step 用 → 内联
- ~4 项 recap phases → `## Quick Reference`（Process 后）
- 5+ 定义项（维度、状态、flag 值）→ 专门 `##` 节（表），放 Process **后**（catalog 跟在 recipe 后），绝不放 Process 前
- 长形技巧 / 可复用模板 → companion 文件，一行指针节引出

把重型 reference 拉出 step 是让多步流程可扫的最高杠杆手段。

### Objections quarantine
每个"但万一..."进尾部借口表（discipline）或 FAQ，**不**在 step 内跑题。step 保持干净——对冲的话住在别处。

### 三层分离
每条 step 写 **what**；**why** 在 Overview/Iron Law；**how**（重型 reference、skeleton）在 companion/Quick Reference。三层混进一条 step = 最常见清晰杀手。

## 6. 表达 — 好 vs 坏

| 好 | 坏 |
|---|---|
| `每改跑一测。` | `建议适当的时候为每次改动跑测试。` |
| Recipe："输出是：summary, findings, severity, 按此序" | 禁令："别冗长、别 bury 结果" |
| `若 brief 存在，引用它。` | `引用 brief，除非不重要。`（nuance 子句） |
| 一个优秀可跑例子 | 五个平庸的同模式例子 |
| `Delete it. Start over.` | `也许删了它会比较好。` |

**语气**：祈使、绝对、第二人称。命令的动词，不是许可。

**闭集 token 慎命名**：闭集值（verdict、state、severity）被字面理解。若日常义 invites 误用——`PLAUSIBLE` 读作"probable"当置信度 hedge——改名指向 intended act（`JUDGMENT-CALL`）。**别**在两个 crisp 反义词间夹 fuzzy 选项（`CONFIRMED / PLAUSIBLE / REFUTED`）：中间槽读作梯度。把不可判状态放最后。

## 7. Skills that dispatch subagents（mock-review 式）

有些 skill 的 Process fan out subagents（一个 per role/task/unit）。xept 样例：[xept:mock-review](../mock-review/SKILL.md) Stage 1 派 3 个独立 reviewer、Stage 1.5 派 checker。

**三个关注点分离**：
1. **template = lean dispatch skeleton**（每角色一个）。Purpose / Dispatch-after / `Subagent:` 块 / 返回什么。父 SKILL.md **不**内联 prompt——指向 template 或在 SKILL 内描述清楚。
2. **dispatch-site wayfinding**：派发的 Process step 处点名 template/输入路径；别把文件列表藏在和 step 脱节的 intro 里。
3. **usage discipline**：怎么填 dispatch（输入递路径不递粘贴历史；scope 经 finder 的 lens；不预判其发现）住在自己的节，带它防的失败。

**关键纪律**（xept 已落实）：
- **输入递路径，不递粘贴历史**——粘贴内容膨胀每轮且过时；fresh subagent 拿任务 + lens + 路径，仅此。
- **merge 从持久化文件，不从对话记忆**——fan-out 的 merge 是 union 组装处，context 压缩会静默缩 union。每源**返回时写自己的文件**，merge **只读那些文件**。文件抗压缩，记忆不抗。（[xept:mock-review](../mock-review/SKILL.md) 的 `.self_xept/mock-review-rN.md` = 此模式。）
- **independence 保护 proposal，不限制 context 访问**："独立"指每 agent 不看别人的 output / controller 的预判答案，**不**指扣留共享事实。给每个 fan-out agent 全部共享事实；只扣留**偏置源**（会话历史、兄弟 draft、你的预判 verdict）。
- **Fan out diverse lenses, not copies**：N 个 agent 抓 blind spot 靠**union**——给每个**不同 lens**（不同 assignment/angle/scope）。相同 prompt 收敛到同一 obvious 核心，union 几乎不增。

完整样例：[xept:mock-review](../mock-review/SKILL.md) Stage 1（三视角独立）+ Stage 1.5（checker 循环）。

## 8. 去哪深挖

- 方法论核心：[SKILL.md](SKILL.md)（Iron Law、三类划分、Match-the-Form、gate=script、SDO）
- 格式方言：[CLAUDE.md](../../CLAUDE.md)（frontmatter、`xept:<slug>`、平台工具映射、HARD-GATE 写法）
- 工程规范：[docs/conventions.md](../../docs/conventions.md)（脚本/测试/提交/分层配置/行为评估）
- xept 的 gate 脚本样例（must-be-correct，证明结构不变量）：[verify_revision.py](../../scripts/verify_revision.py)（round-trip）、[verify_review.py](../../scripts/verify_review.py)（tag 合法性）、[strip_comments.py](../../scripts/strip_comments.py)（剥注释 fail-closed）。区别：[fetch_bib.py](../../scripts/fetch_bib.py) / [compress_images.py](../../scripts/compress_images.py) 是确定性 I/O 工具，**非** gate——它们不证明结构不变量，只做检索/压缩
- discipline skill 完整样例：[xept:mock-review](../mock-review/SKILL.md)（三件套 + HARD-GATE + 借口表）
- technique skill 样例：[xept:write-paper](../write-paper/SKILL.md)
- reference skill 样例：[xept:using-xept](../using-xept/SKILL.md)

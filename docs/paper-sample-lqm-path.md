# 样本 v10

**v9 送审结果**（首份完整稿）：三票 **Weak Accept / CONDITIONAL**。
**每一项准则都离开了 Adequate**（round-18 是五项 Adequate）：
Importance / Insights / Perspective / Verifiability / Presentation 全部 **Good**，
其中 R1 给 Perspective、R3 给 Verifiability 各一个 **Excellent**——但**无共识 Excellent**，
按 rubric 仍不够 ACCEPT。元评审：`.paperpilot/review/.in-progress-sample9/meta-review.md`。

**三审一致确认的正面**：round-18 头号沉船点（复现包落后一代）**不复现**——R1 逐文件比对
发货包与冻结研究树在 **452 个文件上零差异**；R3 把五个脚本全部就地跑通、逐条对上论文。
§2/§3/§7/§8 四节被认为关闭了结构性缺口（此前八轮反复提的那条），R3 的判断是
「emphasis 终于移到主张本身上了」。

## v10 处置

**① §4.5 的 identification 段——我上一轮写错，重写。** R1、R2 各自独立算出、与我逐格重算一致：
不是「18 格引注释 + 1 格引校验规则」，而是 **15 格引注释/文档字符串 / 2 格引校验规则
（milvus_026 的两个 run）/ 2 格引代码结构（milvus_011、milvus_012 各自的第三个 run）**。
更重的是 R2 挖出的第三条：这两案的**另两个 run 都记 WEAK_REFUTED 并写明理由**——
`milvus_011` run2「无注释静默行为」、`milvus_012` run2「兜底链结构示设计但**无注释/quote 明文
（红线3 不构成 REFUTED）**」，而 run3 却按同一份结构判了 REFUTED。
→ 所以「C 是唯一要求逐字意图证据的条款」这一命题，在它自己的 19 格里有 4 格没守住。
已于 §4.5 如实写出，并说明**合规重算抓不到它**（那重量的是聚合规则，不是视角的证据要求）。
教训：我上轮用关键词匹配（源码/注释/文档字符串）把"提到源码"当成了"引注释"——又一次全称断言未证伪。

**② §8 层次错配（三人全中）**：把召回层费率配了确认集层的配对与 p。已改为
`0.588→0.765` 配 `9/0, p=0.0039`、`0.529→0.804` 配 `14/0, p=0.0001`，确认集层另述。
这正是我本轮在 §4.4 修好的同类错，上一批没传播到 §8。

**③ Holm 家族是循环定义（R1、R2）**：我把家族定义成"那四个显著值本身"。已重写为
**m=10（正文印出的十个召回层检验）**，非循环：留 0.0001 / 0.0034 / 0.0039 / 0.0039 四个
（对 α/10…α/7），**停在第 5 个 0.0225**——即部署臂自己 vs flat 的召回层优势应作描述性读。
配套：§4.4 补印了捆绑对比两骨干的召回层配对与 p（§4.1 承诺"每个对比两个层次都报"，缺的正是这个）。

**④ 重判方向按 convention 口径是 15/0/4，不是 18/1（R1，我复现）**：我按三级序
（Confirmed > Human-Review > False-Positive）算的；convention 是二值口径，HR↔Confirmed 是**无操作**。
已改。方向仍全对我们不利。

**⑤ 多数票平局规则未定义（R3，我复现）**：81 案中 **3 案三次运行给出三个不同判定**
（milvus_021 / milvus_038 / qdrant_027）。原文 "a case confirmed on a majority" 已改为
「至少两次把该案算作确认」，并写明换严格多数则 39/51 → **37/51**。

**⑥ §4.2 的 26/20 —— 三人全中，撤断言。** 按 (vendor, reported_version) join 发货台账与
`rq1-fullrun` 的十二个版本目录给 **49/30**（前缀归一 50/31）；R2 重建给 27/21；论文印 26/20。
数值随"覆盖"的定义而变，我定不了代际，故**正文改为不带数的表述**，账挂在自检表。

**⑦ 我本轮新写的三处过强（R2）**：§3.1 "holding everything else fixed" 与 §4.1/§6 冲突；
§2 "**none** takes its expectation from untagged, system-level API prose" 对 RESTInfer/ICON 过强；
§4.4 九臂描述"主骨干非 core 的六个"实为七个（含 source-only）——已逐条改准。

**⑧ 工具盲区**：`107_rejudge_coverage_audit.py` 此前只扫 `rerun_v3`，**整个 contract core 漏掉**——
这正是 R1 找到 core 三条前代归档缺失的原因。已扩到 `rerun_v2/run{1,2,3}`，现报 3 处 GAP。

**⚠️ 未结**：复现包的三项（匿名化声明不实 254 文件 / core 前代归档 / README 的 RQ3 双计数表）
**需你拍板**；§4.2 的 crash 计数与台账两处措辞（R1 小项）留待下轮。

---

## 沿革（v8 处置）

**v8 送审结果**：R1 **Weak Accept** / R2 **Weak Accept** / R3 **Weak Accept**——三票全 CONDITIONAL。
R2 明确把自己的 Verifiability 从 **Excellent 降到 Adequate**，理由是"机械的、不是科学的"：
**发货的复现包比论文落后一代**。三人**独立**把这一条列为头号沉船点。

### v9 处置（按三审收敛顺序）

**① 复现包同步（三人共同头号项，已落盘）。** 复现包对 `run_fullnosrc*` / `run_noscopic*`
既无 `verdicts_coganchor_rejudge.jsonl` 也无 override 行，`recompute_paper_numbers.py`
就地跑出**已撤回的旧数**（supp 0.467/0.933、对比 18/2 p=0.0004）——正是论文"每个率都可从包重算"
所依赖的两条臂。同一类缺陷还波及：6 条控制臂的派发词承诺了一份目录里不存在的
`_pre_coganchor.jsonl`；第一轮修复的 `_pre_cogstrip_merge/` 有 10 条臂只在开发树里。
现已全部补齐并提交复现包 `91da092`，五脚本就地跑通、打印论文的数。另：`clause_tally.py`
扩了 `primary|second` 参数（Qwen 普查此前只存在于评审期临时脚本里），新增
`bootstrap_net_f1.py`（论文要印区间，包里得有脚本）。

**② 四处算术/记号（R1/R2/R3 各自独立抓到，我逐条重算）。** 三处陈数系补漏后只更新了
convention 侧、没更新 forced 侧：强制召回 27→**31**（milvus_006）、九臂强制跨度 [23,30]→**[23,31]**、
"九真 bug 换**七**次拦截"→换**九**次（同句自己印的 21/30→12/30 就是九）。另两处是标题党式
错印：`33 vs 30, 6/4, p=0.7539` 把**召回层**的差值配了**确认集层**的配对（正确写法见 §4.4）；
部署臂 vs flat 的确认集印成 flat 在前（34 vs 48），与同句召回对的部署臂在前矛盾。

**③ 范围限定传播（R1 Q4 / R2 1.2+3.2 / R3 5.2）。** v8 把范围只写在 §4.5，题名第三条腿、
摘要、贡献 3、§5 教训、§6 仍按"协议属性"讲。现已补进摘要与贡献 3、§5 加"on the deployment we
audited"并说明第二骨干上误差质量会移动、§6 Backbone 单独一段。§1 ¶5 的 "controlled
configuration study" 改为 "twelve-configuration study"（§4.1 自己说臂是中途加的、三个对比多于一个变量）。

**④ identification gap（R2 W5 / R3 2.4，R3 称之为"最大的结构性漏洞"）。** 论文用 C/D 互换这个
自身缺陷去限定跨骨干比较，却从没说**主骨干**的字母凭什么算数。v9 实测补齐：主骨干 D 格 145 用认知
词表、98 用源码词表。
⚠️ **同一段对 C 行的分布断言当时写错了**（"18 明写源码注释 + 1 引校验规则"），
v10 已按逐格重读改正为 **15 / 2 / 2**，见上方 ①。

**⑤ 新增证据。** net/F1 配对 bootstrap 区间（R2 已用仓库自带脚本算过，我复现一致）：
无源码 − full 的 net **0 [−8,+8]**、F1 **+0.033 [−0.044,+0.115]**，两者都跨零 → "leads on F1"
改写为"未被分开"。重判效果首次披露：6 个重判文件改 19 个判定，**18 朝确认、1 反向**，
两臂 TP 集合不变。§4.1 的 Holm 家族点名（四值 0.0001/0.0034/0.0039/0.0039，m=4）。§4.6 补
"审计零时会遇到的 152 条伪告警行"（分布 119/205 个模板日志）。§6 的"每个臂都记分"改为 11/12。
§7 数据可用性删掉包代际的空头承诺，改为如实描述发货内容。

**⑥ 已核实为真、无需改的**：§4.1 的 "the artifact says so"（README 新增 script-coverage 节后为真）、
"both raw generations ship"（补 10 个 `_pre_cogstrip_merge/` + 6 个 `_pre_coganchor.jsonl` 后为真）、
§4.6 的"探针脚本发货"（`rq3/analyses/vdbfuzz_oracle_probe.py` 确在，R3 引的旧审计结论过时）。

**⚠️ 未结（进 v9 送审可见）**：§4.2 的"26 案（20 确认）在实验覆盖版本上"**复现不出**——
按 (vendor, reported_version) 匹配现行台账给 49/30，R2 重建给 27/21，论文印 26/20；
差异源头是台账代际（工作区 xlsx 已是 52-TP 口径）。**未改数、未写映射规则**，留待定代际。

---

## 沿革（v7→v8）

**v7 送审结果**：R1 **Accept** / R2 **Weak Accept** / R3 **Weak Accept**——三票全 CONDITIONAL。
三份都核实了 v6 的两条条件关闭、每一个数复现（R2 说 "Everything below was checked against the
frozen verdicts"）。**但两位置审稿人各自独立挖出两处测量级问题**，都不是文字：

**① 泄漏修复漏了两条臂（R1 发现；我逐条验证）。** `run_fullnosrc*` 与 `run_noscopic*` 派发词指向
**未清洗**的 `developer_cognition.json`，**没有** coganchor 重判文件，而理由里引着泄漏的 issue 号
（`run_fullnosrc1/milvus_006` 引 `#47766`；`run_noscopic1` 引 `#50192`×2、`#50193`、`#50319`、
`#50351`×2）。**无源码臂（48/51）正是证据通道那条结论的承重臂。**
→ **已生成 6 个补漏派发**（`results/extraction-audit/106_gen_coganchor_arms.py`，2 臂 × 3 run × 7 案），
说明见 `rerun_v3/COGANCHOR_MISSED_ARMS_NOTE.md`。**待你在 GLM 会话执行。**

**② 条款普查是单骨干的，且第二骨干不复现（R1 与 R2 各自独立算出，我复现）。**

| | GLM | Qwen |
|---|---|---|
| A=Refuted 关闭 | 50（24 真 bug） | 56（24 真 bug） |
| C=Refuted 准确率 | **0.89** | **0.56** |
| 错误关闭中 A 的占比 | **80%** | **50%** |
| A=Refuted&B=Confirmed 格 | 0 | **3** |

→ v8 在 §4.5 开头如实写出范围与第二骨干的不复现，并给出**为什么不能直接读成骨干效应**：D 词表在
两骨干是 98/243 vs **217/243**，而论文自己报告的缺陷 3 正是"C/D 被定义两遍且互换"——**字母可能
在两边不是同一个意思**。

**其余 v8 修正**：泄露修复范围改为五个配置（不是四个）；milvus_001 那句 "every arm but two" 改为
**11/12**（只有 contract core 从不转）；a/b 记号改为与用法一致；§5 的 "our headline effect" 与 §4.4
的 "the routing change" 归位；条款普查计数**随第二次修复变动**如实披露（pre-repair 是 47/20）；
**RQ3 给出单份口径的真值**（R2 查明主日志是 205 个模板日志的逐字回声，单份 = 11,270 变异 / 11,629
响应 / 1,127 阶段）；§4.5 标题改为 "The clause census"。

**⚠️ 依赖**：①的 6 个派发跑完后，`fullnosrc` 与 `noscopic` 的数字可能移动——**交付前需重聚合**。

---

**③ 补漏后的数据更新（2026-09-15，6 个派发已执行）。** 逐项重算后：

| 臂 | TP/FP | supp | prec | net | F1 |
|---|---|---|---|---|---|
| full | 39/9 | 0.700 | 0.812 | **30** | 0.788 |
| **full, no source** | 48/18 | 0.467→**0.400** | 0.750→**0.727** | 32→**30** | 0.835→**0.821** |
| **full, no aggregation** | 33/3 | 0.933→**0.900** | 0.943→**0.917** | **30** | 0.759 |

**四条后果**：① 两条臂的**召回不变**（48/51、33/51，TP 集合逐案相同）；② **承重对比变强**——
full vs 无源码从确认集 18/2 (p=0.0004) 到 **18/0 (p<0.0001)**；③ **net 上三条臂全持平在 30**，
所以"无源码臂在论文自己的指标上更强"**不再成立**，改为"**net 持平、F1 领先（0.821 vs 0.788）**"；
④ 召回层对比**不变**（0/9，p=0.0039）——变的只有抑制侧与确认集检验。

---
---

## Title

**Detecting Documentation–Implementation Bugs in Vector Database Management Systems: A Mining
Campaign, an Evidence-Package Audit, and a Clause-Level Error Census**

（第三条从 "a Controlled Study of What Confirmation Buys" 换成 "a Clause-Level Error Census"——
那才是撑得住的第三条。）

---

## Abstract（~360 词，已写全）

> Vector Database Management Systems (VDBMSs) fail mostly without crashing, and the one dedicated
> VDBMS fuzzer is crash-oracle by construction, so the silent documentation–implementation bugs they
> admit are out of its reach by design. We report a mining campaign, an audit of the evidence its
> confirmation stage reads, and a census of that stage's errors.
>
> **The campaign.** Across Milvus, Qdrant, and Weaviate, maintainers confirmed 51 of 81 adjudicated
> submissions as real bugs and fixed 23 through merged PRs. The ledger records 132 rows for these
> three systems — 81 adjudicated, 49 awaiting a maintainer, 2 withdrawn by us — and covers 19
> versions, of which the 81 span 16. It is a record of submissions and adjudication, **not a
> per-run detection rate**: the runs that would have measured detection ability were voided for
> dispatch-discipline violations and nothing here depends on them.
>
> **The audit.** The packages that stage reads are distilled from vendor documentation, and we
> audited every one of their 134 (constraint, cited-page) pairs against the page it cites:
> **18 are supported as cited, 58 cite a source file or an API landing page rather than the page
> that documents the constraint and were re-anchored, and 58 have no support on their cited page** —
> 43.3%. On the 12 case-level main assertions, a separate object, the audit recorded 5 supported,
> 3 unsupported, 2 weak-evidence and 2 over-strong, and acted on all 12. Two leak repairs followed
> from the same audit and are load-bearing: ten rebuilt packages carried an embedded
> maintainer-cognition section their dispatches forbid reading, and the runtime cognition files
> referenced seven of the candidates' own issue numbers; both were stripped and the affected cases
> re-judged, and **every rate below is computed on the cleaned pool**.
>
> **The census.** Classifying the deployed stage's 243 judgments by the clause that closes them
> locates the error budget in the one refuting clause its protocol does not guard — measured on the
> primary backbone, where the perspectives are identified by their content, and not reproduced on
> the second. Contract refutation, which
> carries no evidence requirement, closes 50 judgments and 24 of them are maintainer-confirmed
> bugs; by-design refutation, which the protocol requires be backed by verbatim intent evidence,
> closes 19 and is right 17 times. **80% of the stage's incorrect closures to False-Positive come
> from the unguarded clause.** Routing contract refutation instead of closing on it recovers seven true bugs for nine
> false-positive interceptions under the deployment's convention, and nothing under the forced
> reading. Four defects in our own dispatches were found by reviewers reading what we shipped.

---

## 1 Introduction（~950 词，已写全）

**¶1 问题。** VDBMSs such as Milvus, Qdrant, and Weaviate store the embeddings that
retrieval-augmented LLM applications depend on. When a VDBMS query is buggy the wrong context
reaches the model — a disabled filter returns all matches, a zero-length vector corrupts an index —
and the error propagates with no crash and no error code to log. Empirical studies agree this is the
dominant shape: most VDBMS bugs are functional failures that keep the service up while returning
wrong results, and the one dedicated VDBMS fuzzer is crash-oracle by construction.

**¶2 目标类。** We target a prevalent subset: *documentation–implementation bugs*, where a VDBMS
silently accepts an input or produces a behavior that violates its API documentation. A canonical
instance: Milvus documents `nprobe` as an integer in $[1, 16384]$, yet the search API accepts
`nprobe=0` with HTTP 200 and returns results (issue #49823).

**¶3 为什么需要 LLM，以及它带来什么。** Detecting such bugs requires an expectation derived from
the documentation prose, and no deterministic-oracle family we analyze anchors its expectation
there. Reading prose is a semantic-interpretation step only an LLM currently performs at scale —
which imports the LLM's false-positive problem, because the same model family that misreads an
ambiguous sentence into an over-strong constraint later judges whether the observed behavior
violates it. **Both halves of that sentence are measurable, and we measure both**: what the
distillation keeps from the documentation, and where the confirmation stage makes its errors.

**¶4 三条结果。**

- **产出。** Maintainers confirmed 51 of 81 adjudicated submissions (Milvus 29, Qdrant 14,
  Weaviate 8) and fixed 23 through merged PRs. The ledger covers 19 versions, of which the 81
  span 16. It carries our own screening and submission decisions, and the runs that would have
  measured per-version detection ability were voided for dispatch-discipline violations; nothing
  here depends on them.
- **审计。** Of the 134 (constraint, cited-page) pairs the confirmation stage's packages carry,
  **18 are supported as cited, 58 cite a source file or an API landing page and were re-anchored,
  and 58 have no support on their cited page**; on the 12 case-level main assertions, a separate
  object, the audit acted on all 12. Two leak repairs followed, and every rate below is computed
  on the cleaned pool.
- **错误普查。** Classifying the deployed stage's 243 judgments by closing clause: contract
  refutation carries no evidence requirement, closes 50 judgments, and **24 of them are real bugs**;
  the verbatim-guarded by-design clause closes 19 and is right 17 times. **80% of the stage's
  incorrect closures to False-Positive come from the unguarded clause**, and routing it instead of closing on it
  recovers seven true bugs for nine interceptions under the deployment's convention. The census is
  measured on the primary backbone, where the two refuting clauses are identified by the evidence
  their cells cite; on the second backbone the pattern does not reproduce and, because our own
  dispatch defines the four perspectives twice with C and D exchanged, we cannot rule out the letters
  meaning different things there.

**¶5 贡献。**

1. **A mining campaign with maintainer-validated yield** across three production VDBMSs: 51
   confirmed bugs, 23 merged fixes, with the ledger's provenance and its limits stated.
2. **An audit-and-rebuild discipline for documentation-derived oracle material**, with the first
   quantitative pair-level measurement we know of for how much of it is unsupported by its own
   citations (58 of 134) and how much was mis-anchored (a further 58), the two leak repairs the
   same audit forced, and the packages it produced.
3. **A clause-level error census** of the confirmation stage, locating the evidence guard on the
   wrong clause, with the counterfactual priced at both readings — supported by a twelve-configuration
   study that supplies the 243 judgments and prices the counting convention by hand. The census is
   measured on the primary backbone and does not reproduce on the second; §4.5 states that scope and
   identifies the two refuting clauses by the evidence their cells carry.

**¶6 也报告我们自己仪器里的缺陷。** Four defects in our own dispatches were found by reviewers
reading the shipped texts, not by us: eight of twelve declare an output field that contradicts their
own verdict vocabulary; the deployed dispatch prints two aggregation rules with opposite defaults
and defines the four perspectives twice with C and D exchanged; and its output schema declares the
source vocabulary for a perspective the text calls maintainer cognition, which 98 of 243 recorded
cells use. We report them because the paper's methodological claim is that this pipeline is
auditable, and an audit that only reports what it finds in the target is not one.

---

## 2 Preliminaries（~740 词，已写全）

**The non-crashing majority.** Studies of VDBMS defects converge on one structural fact: most do not
crash. The systematic bug study attributes the dominant share to functional failures — the service
stays up and silently returns wrong results — with crash-producing defects a minority class
\cite{bugstudy25,roadmap25}. The one dedicated VDBMS fuzzer, VDBFuzz, reaches exactly that minority:
its oracle fires on a 5xx response or a failed request induced by template-driven input mutation,
not on the silent misbehaviour at issue here \cite{vdbfuzz26}. The
community roadmap names oracle definition as the open problem for what is left \cite{roadmap25},
and that residual is where this paper works.

**What we target.** The subset we study is *documentation–implementation inconsistency*: the
system silently accepts an input, errors where it documented success, returns a shape its API
reference does not describe, or leaves state the documentation says cannot arise. We separate this
from *correctness*. Consistency asks whether observable behavior matches what the API documentation
prescribes — what is accepted, what is rejected, what is returned, how state evolves. Correctness
asks whether a returned result is right in the mathematical sense, such as whether an approximate
nearest-neighbour search returns the true top-$k$. Vector-search correctness is not what this paper
measures; a documentation-conformant query that returns the documented (approximate) answer is out
of scope here, and the distinction matters because the two are checked by different means.

The reverse shape of inconsistency also occurs and is harder to see: an operation the documentation
describes as all-or-nothing applies partially, or a transition — delete, recreate, restore — leaves
behavior the documentation does not allow. These are the silent majority's own subclass, and none of
them produces a signal a crash oracle can fire on.

**Why the expectation has to be read from prose.** Every testing oracle needs an expectation, and
oracle families differ in where they get one. The candidates relevant here, and the structural
reason each anchors somewhere other than system-level API prose:

| Candidate oracle | Expectation anchored in | Why it misses this residual |
|---|---|---|
| crash signal (VDBFuzz) | process death or 5xx | the bugs here do not crash |
| differential testing (NoREC, TLP, DQE) | another evaluation of the same engine, or another vendor | intra-system variants compare an engine with itself and derive nothing from documentation; cross-vendor behavior diverges by design |
| metamorphic relations | a relation the tester already poses | deriving *which* relation the prose prescribes is the semantic step non-LLM tooling does not perform |
| property-based testing, schemas | field types, declared ranges, enum sets | a schema bounds fields; it does not carry cross-request or state-coupling behaviour, and where a schema declares a minimum it may omit the maximum that matters |
| structured-source oracles (AGORA+, SATORI, MASTOR, MASTEST) | OpenAPI fields, execution traces, or the implementation source | anchored in structured sources; source-anchored oracles encode implemented behaviour and so cannot report a documentation–code gap as a defect |
| documentation-derived oracles (@tComment, JDoctor, DocTer, RBCTest, RESTInfer) | tagged or method-/parameter-level prose | prose-derived, but the derived oracle stays the final arbiter and the granularity sits below system-level behavioural prose |

Each of these reaches something real. The point of the table is narrower: the families that read
prose at all read it at field, parameter or method granularity, and often from tagged sources; none
of them takes its expectation from **untagged, system-level behavioural prose**, which is where the
VDBMS documentation states the constraints that matter here — "the other collection should have the same vector size as the current
one", an `nprobe` bound, a password length. Those constraints are prose: implicit, ambiguous, spread
across pages, and rarely stated as a machine-checkable value. "Optional, default 1" may or may not
admit zero, and the documentation usually does not say. The systems also diverge by design — each
VDBMS standardizes its own parameter semantics, error codes, and state model — so no cross-vendor
reference adjudicates which of two behaviours is the bug.

**The consequence, and what it costs.** Reading that prose is a semantic-interpretation step, which
makes an LLM the practical oracle for this residual — and imports the LLM's false-positive problem,
because the same class of model that reads an ambiguous sentence into an over-strong constraint
later judges whether an observation violates it. That import is not a defect of a particular
pipeline; it is the price of the only oracle family that anchors where the residual lives. The rest
of this paper measures what that price buys, where inside a judge the errors concentrate, and which
parts of the judge change the answer.

## 3 Approach（~1,840 词，已写全）

### 3.1 Overview

The pipeline this paper measures has four stages, and it is worth stating what each is *for* in the
measurement rather than only what it does. (i) **Behavioral-specification extraction** turns a
vendor's natural-language API documentation into structured constraint records, each with a citation
to the page it came from. (ii) **Test-script generation** turns each constraint into executable
probes, assigning every probe to a strategy that was registered before it ran. (iii) **Sandboxed
execution** runs the probes against a pinned instance of the target and records raw HTTP traffic.
(iv) **Bug confirmation** decides, per candidate, whether the observation is a defect — and this
stage is the object of study for most of what follows: §4.4 and §4.5 vary its internal organization
and its evidence access against one common set of frozen packages, and §4.1 states which of the
resulting contrasts change more than one thing.

Two features of the design make it measurable rather than merely usable. First, each stage writes a
structured artifact — a constraint record, a probe with an inline oracle line, a request/response
log, an evidence chain — so a claim about a stage can be traced to the file that grounds it.
Second, the confirmation stage's evidence is *frozen* per case: a candidate's package (observation
plus documented contract) is fixed once built, and the judge configurations in §4 read the same
packages. Whatever a configuration concludes, it concluded from the same material as the others.

We carry two real candidates through the description. Milvus issue \#49823 documents `nprobe` as an
integer in $[1, 16384]$; the REST search API accepts `nprobe=0`, returns HTTP 200, and answers the
query. That is a boundary violation visible in one response. Qdrant issue \#10369 documents that a
collection referenced through `lookup_from` must have the same vector size as the target; the
`recommend` API bypasses that check for negative examples and returns silently wrong scores. That
one needs a state transition — delete the lookup collection, recreate it at a different size — to
become observable at all. The two differ in which generation path they take in stage (ii), and both
were confirmed by maintainers.

### 3.2 Behavioral-specification extraction

**Knowledge extraction.** A *knowledge extractor* crawls the vendor's documentation for the target
and its version and writes a per-endpoint knowledge file: method, path, source URL, parameters,
constraints, expected responses, plus a table tracking each page's documentation version. Two
self-checks gate the output — an endpoint-coverage check against the vendor's published API surface,
and a version-alignment check requiring the documentation version to match the target's
major.minor, because a specification read from the wrong documentation version tests the wrong
system. Version alignment is a precondition, not a post-hoc filter: where a crawled artifact
disagrees with the pinned version, the versioned documentation stays authoritative.

**Specification extraction.** A *specification extractor* reads that file and emits one record per
constraint: a unique identifier, the endpoint, a natural-language description, a checkable assertion
(for \#49823's family, `nprobe >= 1 && nprobe <= 16384`), a type, an evidence tier, and a source URL
with a verification flag. Three mechanisms discipline the model here. *Categorization* types every
constraint as range, type, state, behavioural, or other, which downstream decides which attack agent
owns it. *Evidence tiering* records how directly the page supports the constraint — stated verbatim,
inferred from an example, inferred from behaviour, or convention — so that test strength can be
graded by its support. *Source verification* fetches the cited page and confirms it actually carries
the asserted semantics; constraints that fail are marked and excluded from downstream reporting as
bug evidence. A judge's package is not the extractor's output alone — it also carries contract rows
matched to the parameters a candidate probes and appended when the package was rebuilt — and §4.3
audits every citation that reaches a package against the page it names and at the version the row
claims, independently of this or any earlier verification step.

**Two levels, decided observationally.** Each constraint is endpoint-level or system-level, and the
criterion is what would prove a violation rather than how hard it is to construct: a constraint
violated by a single request/response pair is endpoint-level even where elaborate setup is needed to
reach the violating request, and a constraint violated only by relating observations across requests
or against evolved state is system-level. \#49823 is endpoint-level; \#10369 is system-level because
the coupling it describes becomes visible only after a transition.

### 3.3 Test-script generation

Three attack agents — boundary, state, and semantic — turn constraint records into executable
Python probes, each bound to strategies registered before generation with trigger conditions and
oracle templates. Boundary strategies probe at and beyond documented bounds, wrong JSON types, and
the same resource addressed through two key forms. State strategies build multi-request scenarios:
partial application of an operation the documentation describes as all-or-nothing, deletion
concurrent with use, and cross-object references left dangling by a transition. Semantic strategies
check the documented meaning of a response rather than its shape — a right status code with a
misleading message, or the accept/reject semantics of a documented parameter.

*Strategy selection is not left to the model at generation time.* Strategies are bound to
constraints deterministically by a registry of (strategy, trigger predicate) entries matched against
the constraint's type, level, and assertion surface; a constraint may trigger several and the agent
generates for each, and one that triggers none falls through to scenario construction. Because the
mapping is a function of the constraint record alone, the (constraint, strategy) pairs are
reproducible from the specification file, and each generated probe carries an inline oracle line —
a machine-checkable assertion about the expected response — which removes a degree of freedom in
which the model could drift.

Generation splits on the constraint's level. An endpoint-level constraint with a bound strategy is
instantiated directly against its violation surface. A system-level constraint always goes through
scenario construction: the agent must first build the state in which the constraint binds, then
evaluate the assertion against that live state in both directions of any transition. For \#10369,
that means a size-4 lookup collection answering `recommend` with 200, then a delete and recreate at
size 8 after which the same request must be rejected with a dimension-mismatch error.

Every probe passes five gates before it may execute: it must compile; its constraint must exist in
the structured contract; it must avoid registered risky patterns (a request path with no safe
wrapper, a swallowed exception); it must not carry helper code fingerprinted to another vendor's
environment; and its oracle line must match the response shape the endpoint actually returns. A
failing probe is regenerated; only passing ones reach the sandbox.

### 3.4 Sandboxed execution

An executor runs each passing probe from the host runtime against a Docker-pinned instance of the
target at the tested version — nothing but the database itself executes inside the container. Each
probe writes its raw request/response pair to a log and, only after the log is flushed, a completion
marker; per-batch marker counts are reconciled, so an interrupted batch is detectable and
re-runnable. The sandbox is what lets a candidate reproduce under a clean probe, and the raw records
are the behavioural evidence every later stage consumes. §4.3 describes what an audit of that
evidence found.

### 3.5 Bug confirmation

The last stage decides whether a candidate is a defect. It is not a single judgment. An *evidence
builder* assembles evidence and a *chain auditor* cross-examines it, with an explicit rebuild loop —
a builder/judge split whose purpose is to keep the falsification separate from the claim.

**Assembly.** The builder first checks the observation against the specification and re-verifies the
citation independently of the extractor's own check, then traces the chain `contract → doc → script
→ log` and flags broken links. It then greps a local clone of the implementation *at the pinned
version* — the only authority for what the implementation does — for the parameter and error-code
keywords, follows the relevant call chain, and records an outcome: the validation the documentation
promises is absent, present, the behaviour is by design in the source, the code could not be
located, or the search was shallow. The result is a five-section evidence chain — document
verification, execution evidence, contract grounding, chain trace, source grounding — each section
labelled with the kind of evidence it rests on.

**Cross-examination.** The auditor first applies four mechanical checks: that all five sections are
non-empty, that contract, documentation, log and source agree, that nothing inside the chain
contradicts anything else, and that the primary observation matches the specification. A chain that
fails goes back for rebuild, at most three times. Surviving chains are then read from four
perspectives:

- **A — contract.** Does the quoted contract text actually ground the assertion? Run as a mechanical
  containment check.
- **B — objective constraints.** Seven classes that constitute violations without any contract
  endorsement: numeric lower bounds on count-, size- and limit-class parameters, closed enum sets,
  mutually exclusive parameters, type tautologies, same-family inconsistency, interface asymmetry
  across a system's REST, gRPC and SDK faces, and (heavily qualified) HTTP response semantics. An
  `ef`/`nprobe`-class carve-out applies where the source documents a negative-sentinel convention.
- **C — behavioural elegance.** May the implementation refuse the bug reading? Only an *explicit*
  by-design may refute: the source excerpt must contain intent evidence — a comment or docstring
  saying the behaviour is intended — or a maintainer quote must declare the same class of phenomenon
  intended. Bare structural inference ("no validation is present") is recorded as a weak refutation
  and routed to human review rather than closing the case. This is the clause §4.5 audits.
- **D — maintainer cognition.** Does a corpus distilled from the target's historical issues and
  merged PRs support either reading? Hits must match at the level of phenomenon, never by word
  overlap. Cognition states a maintainer's attitude; it may decide a contract-neutral case but may
  not supply a missing observation.

**Aggregation, and the verdict space.** The verdict is three-valued: Confirmed, False-Positive, or
Human-Review. Aggregation is fixed, and the order in which its clauses are tried is part of the
design: a contract confirmation decides the case; a contract refutation *with* the objective-constraint
perspective confirmed routes rather than closing; otherwise a contract refutation closes to
False-Positive; an objective-constraint confirmation decides a contract-neutral case; a cognition hit
on either side decides a case the earlier clauses left open; an explicit by-design refutation closes;
and everything else routes to human review. The order is not a detail — **the clause that closes a
judgment is the first in this sequence that decides it**, and which clause that is is exactly what
§4.5 counts. The rule is
deliberately asymmetric — only explicit intent evidence may refute, and anything unsettled goes to a
person rather than closing — and that asymmetry is a design position rather than a claim of
precision. An LLM-derived oracle is expected to over-report; the protocol keeps the over-reporting
visible in a review queue instead of suppressing it at the cost of discarding real defects. §4
measures what the asymmetry costs and what it buys, and §4.5 shows where the errors it does not
catch actually land.

**Implementation.** The pipeline runs as a multi-agent system on an agentic coding runtime, one role
prompt per agent, all agents on a single model backbone under vendor-default sampling. Each stage's
artifact is versioned, and the §4 study reads frozen copies of them rather than re-running the
pipeline.

## 4 Evaluation

### 4.1 Methodology（~1,055 词，已写全）

**The pool.** Eighty-one candidates from Milvus, Qdrant, and Weaviate: 51 maintainer-confirmed bugs
and 30 adjudicated false positives. Ground truth is maintainer adjudication for the 51 (labels,
closures, merged fix PRs); the 30 negatives are adjudicated by us against the maintainers'
disposition where available. There is no inter-annotator study. The shipped ledger holds 132 rows
for these three systems: 81 adjudicated and 51 unadjudicated, of which 49 carry no maintainer
verdict and 2 are our own withdrawn submissions. **One of the 81, `milvus_001`, is unjudgeable** —
its observation was never captured and its version's documentation segment is retired. Under the
deployment's convention, which credits a routed case, **eleven of the twelve configurations route
it to Human-Review in at least two of their three runs** — only the contract core never does — so
eleven are **credited a point for a case nobody could judge**; under the forced and joint readings
it is a guaranteed miss.

**Two leak repairs, and why they are load-bearing.** The audit in §4.3 exposed two channels through
which material the confirmation stage was forbidden to read had reached it. First, **ten of the 81
rebuilt packages carried an embedded maintainer-cognition section**, which the core, flat and
source-only dispatches forbid; the section was stripped and all ten cases re-judged. The re-judged
runs span **five configurations**: contract core, flat judge and source-only on the primary
backbone at three runs each (nine), the second backbone's source-only arm at three, and its flat
judge at one — that arm's other two runs were dispatched after the strip and read the cleaned
packages from the start. The re-judged cells were merged into those runs and the pool reduced as
before. Second,
**the runtime cognition files referenced seven of the 81 candidates' own issue numbers**; the
entries were removed and those seven cases re-judged. That repair was applied to the deployed stage
on both backbones at the time and, we found later, **not to the two full-family controls**, which
were dispatched around the same time and whose recorded rationales still cite the removed entries by
issue number; those six runs have since been re-judged on the same terms, and the two controls'
numbers below are computed on the cleaned pool as the rest are. **Every number this paper reports is computed on the cleaned pool**, and the
second repair is not cosmetic: without it the deployed configuration would read 41/51 with
a confirmed set of 41+6 rather than the 39/51 and 39+9 we report. It does not move the two controls in our favour either: of the
nineteen verdicts the six re-judge files rewrite, fifteen move a case toward confirmation under the
convention, four move between Confirmed and Human-Review, which the convention counts alike, and
none moves away; the arms' true-positive sets are unchanged
(48 and 33) while their false-positive counts rise by two and one — suppression $0.467\to0.400$
and $0.933\to0.900$ — and on the forced reading the no-source arm's recall rises by one, to 31.
Both raw generations ship
alongside the cleaned one, so a reader can reconstruct either.

**The counting convention, and its price.** A verdict is Confirmed, False-Positive, or Human-Review;
Human-Review is the deployment's escalation channel. We count a routed case as confirmed, because
that is what the deployment's ledger counts — and the convention is not free, because a
configuration that routes more scores higher on recall. So we report the forced-verdict reading
beside it for every contrast, and we price the convention at **two** places: the arms' levels, and
the headline contrast itself. The rulings come from one author-executed non-blind pass; an
independent adjudicator on the same materials agrees with it on 4, 5 and 6 of the 20 commonly ruled
cases under the pack-only, pack-plus-source and full-protocol statements respectively
($\kappa = -0.01$, $0.08$, $0.11$), so we report the joint reading as a bound rather than a
measurement. **Two of the three independent passes land at the forced floor.**

**The twelve configurations.** Each re-adjudicates all 81 cases three times. A case counts as
confirmed when **at least two of its three runs recorded it as confirmed** — under the convention,
either Confirmed or Human-Review — which is not the same as requiring two runs to agree on a
verdict: three of the 81 cases split three ways, and under a rule that demanded two identical
verdicts the deployed stage's recall would be 37/51 rather than the 39/51 we report. Both backbones
are serving aliases without pinned weights.

| # | configuration | perspectives | rule | source | backbone |
|---|---|---|---|---|---|
| 1 | contract core | — | — | — | GLM-5.3-Flash |
| 2 | flat judge | — | — | ✓ | GLM-5.3-Flash |
| 3 | flat + schema fix | — | — | ✓ | GLM-5.3-Flash |
| 4 | flat + aggregation | — | ✓ | ✓ | GLM-5.3-Flash |
| 5 | full, no aggregation | ✓ | — | ✓ | GLM-5.3-Flash |
| 6 | source-only | — | — | ✓ | GLM-5.3-Flash |
| 7 | full stage | ✓ | ✓ | ✓ | GLM-5.3-Flash |
| 8 | full, no source | ✓ | ✓ | — | GLM-5.3-Flash |
| 9 | flat judge | — | — | ✓ | Qwen3.8-Flash |
| 10 | flat + aggregation | — | ✓ | ✓ | Qwen3.8-Flash |
| 11 | source-only | — | — | ✓ | Qwen3.8-Flash |
| 12 | full stage | ✓ | ✓ | ✓ | Qwen3.8-Flash |

We added them during the study rather than pre-registering them, and **three contrasts change more
than one thing**: contract-core-to-flat (any judgment at all, against a binary-only core), the
deployed change (verdict space plus routing rule, decomposable only on the primary backbone), and
the four-perspective contrast (five things, listed in §4.4).

**A defect we report rather than repair.** Eight of the twelve dispatches declare a binary `verdict`
field while their own text mandates three values. It is part of the baseline on those eight; the
declared field was not binding in practice — the flat judge recorded Human-Review on 21 of 243
judgments against a binary schema.

**Statistics.** Paired exact McNemar at both the confirmed-set level (81 cases) and the recall level
(51 true bugs); they disagree and **both are reported for every contrast**, including the isolation
steps. Matched-pairs Wald intervals on recall differences. Discordant pairs are written *a/b*, where *a* is the arm whose
count is printed first in the comparison being reported. **The p-values we print are unadjusted.**
Sixteen paired tests appear below, ten of them at the recall level. Read as a family of ten, a Holm
correction leaves the four smallest significant — the bundled contrast on the second backbone
($0.0001$), that backbone's perspective contrast ($0.0034$), the bundled contrast on the primary
backbone ($0.0039$) and the evidence-access contrast ($0.0039$), tested against $\alpha/10$,
$\alpha/9$, $\alpha/8$ and $\alpha/7$ — and stops at the fifth
($0.0225$), so the deployed stage's own recall-level advantage over the flat judge, and everything
larger than it, should be read descriptively. All rates, the census on both backbones, both replays, the net and $F_1$
intervals and the pair audit are recomputable from the artifact
(`rq2/analyses/{recompute_paper_numbers,clause_tally,convention_pricing,bootstrap_net_f1}.py` and
`rq2/analyses/audit/pair_audit.py`; `clause_tally.py second` gives the second backbone's census);
the joint prices, the catch-all composition and the expectation-framing check are printed but not
yet scripted, and the artifact's script-coverage note says so.

### 4.2 Mining yield（~450 词，已写全）

Maintainers confirmed 51 of the 81 adjudicated submissions; 23 are fixed by merged PRs. The 51 break
down as 23 fixed, 18 acknowledged-open, 7 closed without a fix, and 3 tracked as duplicates.
Per system: Milvus 43 adjudicated (29 confirmed / 11 fixed / 14 false positives), Qdrant 28
(14 / 9 / 14), Weaviate 10 (8 / 3 / 2). One of the 51 is a crash-or-panic defect; the other 50 are
silent accepts, wrong results, or poor diagnostics. A separate analysis in our development tree
records that all 23 merged fixes modify implementation code, 15 also add a regression test, and none
is documentation-only; **that table is not part of the shipped artifact and we mark the claim
accordingly**.

**Attribution, and what was voided.** The ledger records 132 rows across 19 versions of the three
systems; the 81 adjudicated submissions span 16 of those versions and the 51 confirmed bugs span 15.
It is **not a per-run detection rate, and we cannot supply one**: the RQ1 *detection-ability*
experiment — 15 versions run to measure per-version detection — was **voided in full on 2026-08-23**
because its attack dispatches carried source-clone paths and cross-round experience, violating our
own information-boundary rules, with quality gates missed on the versions that were clean. Those
runs measure nothing. **A substantial share of the 81 adjudicated submissions sits on versions that
experiment covered**, so the distinction matters and we state it: the voided object is
the *measurement*, and the adjudication survives because maintainers are external to the violated
protocol — they confirmed the candidates and merged the fixes. We report the ledger for that reason
and no other. The void record ships with the artifact.

### 4.3 Auditing the evidence packages（~750 词，已写全）

*How much of what the confirmation stage reads is actually in the documentation?*

The stage reads a per-case package: the candidate's observation, and constraint rows distilled from
vendor documentation with a citation on each. We audited every cited pair against the page it cites,
at the version the row claims.

**Pair level: 134 (constraint, cited-page) pairs**, deduplicated from the surviving row instances.

| Verdict | n | share | meaning |
|---|---|---|---|
| supported as cited | **18** | 13.4\% | the cited page documents the constraint |
| re-anchored | **58** | 43.3\% | the cited anchor was a **source file** (a `constant.go` path) or an **API landing page** carrying no endpoint documentation; the constraint was re-anchored to version-pinned documentation or the pinned API specification |
| no support on the cited page | **58** | **43.3\%** | the cited page does not support the constraint, and for many no page does |

The two 43.3\% shares are each of 134, not a combined 86.6\%.

**Case level: 12 main assertions** — a different object, the case's own headline claim rather than
its citations. Five were supported (recorded by quoting the page verbatim, or — for three cases
whose assertion was the same schema-match sentence — by replaying the observation against the
operator's page), **three were dropped as unsupported** (no constraint entry on the pages checked),
**two were over-strong** and were respectively rewritten to the page's own claim and weakened to a
descriptive statement, and two were recorded as weak-evidence rows with the page's own normative-free
wording. All twelve were acted on.

**The two dominant mechanisms.** *Version drift*: the augmentation script drew every vendor's
constraints from one fixed version's contract, so rows for one release carried another release's
endpoints and shapes. *Conceptual-only documentation*: constraints such as `nprobe ∈ [1, nlist]`,
`M ∈ [4, 64]` or a password length bound exist as prose descriptions but not as documented values,
so a distiller that states them asserts more than the page does.

Every package was then rebuilt against version-pinned documentation and all rows re-anchored, and we
checked the rebuilt set for the failure this class of work invites: **zero of 81 packages contain a
sentence framed as an expectation** — the 19 hits for such phrasing were each inspected and are all
verbatim server responses, quoted as observations.

**What it means.** This measures a step every "distil a specification from documentation, then judge
against it" pipeline performs and that, to our knowledge, none reports. **We are not claiming these
rates as properties of LLM distillation in general** — they are this distiller on these three
vendors' documentation, classified by a single reader without a second coder — but they are high
enough that the next pipeline in this line should measure its own numbers before attributing a
confirmation rate to its judge.

### 4.4 What the confirmation stage buys（~1,200 词，已写全）

*Which part of the stage's structure changes what it confirms, under which reading?*

This section supplies the instrument; §4.5 carries the paper's claim.

**Levels.** At its deployed configuration the stage confirms 39 of 51 true bugs and intercepts 21 of
30 false positives under the deployment's convention; forced, 27/51 at suppression 27/30; under the
hand-adjudicated joint reading, 33/51. The contract-only core suppresses 29/30 but recalls 8/51; the no-aggregation arm confirms 33
with 3 leaked false positives (suppression 0.900, precision 0.917).

**The headline contrast, priced.** The flat judge differs from the deployed stage in several things,
so we added the missing pieces to the flat judge in turn. The schema-line repair alone moves recall
30→35 (recall level 0/5, $p{=}0.0625$; confirmed-set level 34→39, 1/6, $p{=}0.1250$) and forced
recall 25→29; adding the routing rule on top moves recall 35→39 at the recall level (2/6,
$p{=}0.2891$; confirmed-set 39→51, 2/14, $p{=}0.0042$) and, forced, the other way (29→27, 3/1).
**The bundled contrast — flat judge to rule-bearing judge — moves 30→39** at the recall level (0/9,
$p{=}0.0039$) and 34→51 on the confirmed set (0/17, $p{<}0.0001$), and it replicates on the second
backbone: 27→41 at the recall level (0/14, $p{=}0.0001$) and 32→51 on the confirmed set (0/19,
$p{<}0.0001$).
**The two levels disagree for the rule step, and we privilege neither**: it is significant at the
confirmed-set level and not at the recall level. For reference, the deployed stage against the flat
judge is 48 vs 34 on the confirmed set (16/2, $p{=}0.0013$) and 39 vs 30 at recall (11/2,
$p{=}0.0225$).

**Under our own hand-priced reading the change is worth three, and that is a floor.** Applying the
same hand-adjudication of the routed queue to this contrast gives the **rule-bearing control** —
which is not the deployed stage — 32/51 against the flat judge's 29: **+3**. The deployed stage
itself is 33/51 against the same 29 — **+4**. The control has 22 decisive routed cases, of which 9
were never ruled, one of them a true bug; the flat judge has 8, of which 2 were never ruled, none a
true bug. Crediting every unruled case on **both** arms symmetrically gives 33 against 29 — **+4**;
crediting the control's unruled *and* return-ruled cases while leaving the flat judge strict gives
+5. **At the reading this paper considers honest, the deployed change is suggested, not
established**, and on the second backbone there is no schema-repaired control, so the split is
unmeasured there.

**The four-perspective contrast.** It changes **five things** against the rule-bearing flat judge:
the perspectives; the aggregation rule text, since a perspective-free judge cannot carry an A/B/C/D
clause table; the red-line set; the declared verdict field; and access to the cognition corpus.
With that label: 39 vs.\ 39 on the primary backbone (4/4, $p{=}1.0$; interval $\pm0.11$, so the
data exclude an effect larger than about eleven points but do not establish equivalence), and
**$-11$ true bugs on the second** (41 vs.\ 30, 12/1, $p{=}0.0034$). Under forced verdicts the two
are equal on both backbones (27 vs.\ 27; 26 vs.\ 26); equal, but not the same decisions — their
forced true-bug sets intersect in 22 of 27 and 23 of 26. At the recall level against the rule-free
flat judge the perspectives are $+3$ (33 vs.\ 30, 5/2, $p{=}0.4531$) and against the
schema-corrected control $-2$ (33 vs.\ 35, 1/3, $p{=}0.6250$), neither significant.

**The readings reorder the arms.** Across the nine judging arms this section contrasts — the flat
judge, flat $+$ schema, flat $+$ aggregation, full-no-aggregation, full stage and full-no-source on
the primary backbone, and the second backbone's flat, flat $+$ aggregation and full — forced
recall spans [23, 31] of 51 against a convention span of [27, 48]; the contract-only core, a blind
baseline, reaches 8 forced and 8 convention, and the two source-only configurations 20 and 19
forced (36 and 37 convention, the two recall figures quoted below).

**What evidence access costs.** Withholding the implementation source raises recall 39→48
(discordant 0/9 at the recall level, $p{=}0.0039$; forced 27→31) and cuts suppression from 21/30 to
12/30, so it buys nine true bugs for nine false-positive interceptions. On the confirmed set the same
contrast is 48 vs 66 (discordant 0/18, $p{<}0.0001$). **The deployment's summary metrics do not
separate the two configurations**: net true positives minus leaked false positives is 30 either way —
a difference of 0, paired case-level bootstrap 95\% CI $[-8,+8]$ — and $F_1$ is 0.821 without the
source against 0.788 with it, a difference of $+0.033$ whose interval also spans zero
($[-0.044,+0.115]$). A configuration that drops its most
trusted evidence channel therefore matches the deployed stage on net and is not separated from it on
$F_1$ either — the
price of the falsification anchor, stated as a tie rather than as a defeat. Two caveats: the arm is
not source-access-only (it also
redirects the by-design clause to the cognition materials and drops the objective-constraint
perspective's negative-sentinel exemption), and the two source-only configurations (0.706 and 0.725
recall) are shipped but outside this section's contrasts.

### 4.5 The clause census: where the confirmation stage closes wrong（~1,150 词，已写全）

*Where does the confirmation stage's error come from?*

The census covers **the deployed stage on the primary backbone** — 81 cases, three runs each, 243
judgments. We state the scope because it is narrower than the claim sounds and because we can check
it: the same census on the second backbone does not reproduce the pattern. There, contract refutation
closes 56 judgments and by-design refutation closes 50, of which 22 are wrong — so by-design is not
the accurate clause on that backbone — and the unguarded clause supplies 24 of 48 incorrect closures
to False-Positive, **50% rather than 80%**. That comparison is itself bounded: the deployed dispatch
defines the four perspectives twice with C and D exchanged (our own defect 3, reported in §1 ¶6 and
§5), and
the recorded D cells use the source vocabulary in **217 of 243 judgments on the second backbone
against 98 of 243 on the primary**, so the letters may not denote the same perspective on the two
backbones and the two censuses may not be comparable.

**On the primary backbone the letters are identified by their content rather than assumed.** The
nineteen judgments this census closes by C=Refuted record what they rest on, and reading them
separates three kinds of evidence rather than one: **fifteen** cite a comment or docstring in the
implementation; **two** (`milvus_026`, in two of its three runs) cite the server's own
name-validation rule, whose code and error message those runs name; and **two** (`milvus_011` and
`milvus_012`, each in its third run) rest on code structure — a default expression, a fallback
chain. None rests on observed behaviour alone, which is the property the legend requires of this
clause. But the last two are the weaker kind, and the same two cases show why the distinction is
not academic: in both, the case's *other* runs recorded a weak refutation and gave their reason —
`milvus_011`'s second run notes that a silent behaviour has no comment behind it, and
`milvus_012`'s second run states that the fallback-chain structure shows design but carries no
comment or quote, so the red line governing this perspective does not admit it. The
verbatim-evidence requirement is therefore not applied uniformly by the judge that recorded these
cells — a departure the compliance recount below does not catch, because that recount measures
compliance with the *aggregation* rule, and this is a requirement of the perspective itself. The
primary's D cells likewise carry the cognition vocabulary in 145 of 243 judgments against the source
vocabulary's 98, which is the split that puts the latter in the catch-all below. The ambiguity
between the two printed definitions therefore bounds the cross-backbone comparison without voiding
the census on the backbone we claim. What we claim is the primary-backbone
result; what we can say about the second is that it does not reproduce and that we cannot rule out
the letters meaning different things there.

The clause legend, in firing order:
**A** the contract perspective (Confirmed, or Refuted where the contract assertion is contradicted,
with the exception that Refuted plus B Confirmed routes); **B** the objective-constraint perspective;
**D** maintainer cognition; **C** behavioral elegance, refuting only on verbatim intent evidence —
an in-source comment or docstring, or a maintainer quote; then the catch-all. "Accuracy" is agreement
with the maintainers' adjudication. The table is grouped by the outcome each clause assigns.

| Clause | assigns | n | right | wrong | accuracy |
|---|---|---|---|---|---|
| B = Confirmed | Confirmed | 61 | 56 | 5 | **0.92** |
| A = Confirmed | Confirmed | 21 | 17 | 4 | 0.81 |
| D = Supports-Defect | Confirmed | 7 | 5 | 2 | 0.71 |
| **A = Refuted** | False-Positive | **50** | 26 | **24** | **0.52** |
| **C = Refuted** | False-Positive | 19 | 17 | 2 | **0.89** |
| D = Supports-Not-Defect | False-Positive | 16 | 12 | 4 | 0.75 |
| catch-all | **Human-Review** | 69 | *45 bugs* | *24 FPs* | — |

**The protocol guards the clause that is already clean.** By-design refutation must rest on verbatim
intent evidence and perspective C enforces that. C is the most accurate refuting clause measured
(17 of 19) and the least often fired of the two refuting clauses — **the middle of the three clauses
that assign False-Positive** (19 judgments, against cognition's 16 and contract refutation's 50); it
closes 2 of the 243 judgments that rest on true
bugs. Contract refutation carries no such requirement, closes two and a half times as many, and is
wrong about half the time: **24 of its 50 closures fall on confirmed bugs, and of the stage's 30
incorrect closures to False-Positive this one clause supplies 24 — 80%**. Three facts make this
count the census's most robust, all of them about how it is constructed rather than how far it
travels — the scope above bounds the latter — with one disclosure: the counts above are post-repair, and the archived
pre-repair cells would give contract refutation 47 closures and by-design 20, so "by-design is the
middle of the three" holds of the cleaned pool. The load-bearing 24 is invariant either way. **It is invariant across the two aggregation rules our dispatch prints**,
whose last steps disagree about the insufficient-evidence default, because contract refutation
assigns False-Positive under both — and no recorded cell **on this backbone** carries the
A=Refuted-with-B=Confirmed pair that the other rule would route (the second backbone records three).
**Its load-bearing count is computed on maintainer-confirmed
labels** (the 24 closures that fall on true bugs), so it does not rest on the 30 negatives we
adjudicated ourselves. And it survives the two leak repairs above, which were applied before these
judgments were recorded.

**The counterfactual, at both readings.** Routing contract refutation to human review, everything
else held at the recorded perspective values, moves recall 39/51 → **46/51** and suppression 21/30 →
**12/30** under the convention — seven true bugs for nine interceptions. **Forced, the same replay
changes nothing** (27/51, 27/30, and the confirmed sets are identical), because an abstention and a
closure score the same there. Fifteen cases are closed by this clause in at least two of three runs,
seven of them true bugs, and all seven are unconfirmed — so seven is the case-level maximum. The
prescription is a replay rather than a re-adjudication; **what cannot be computed from frozen data
is whether a judge re-adjudicating those refutations under a verbatim-evidence guard would reach the
same place**, and the gain it shows is a property of the convention rather than of the stage's
decisions.

**The escalation channel, restricted to the cells the rule defines.** The catch-all routes 69
judgments. **Thirty-seven of them (54%) carry the source vocabulary in their D cell** — a vocabulary
the operative rule has no clause for, so they fall through by classification rather than by the
judge's substantive reasoning; those 37 rest on 28 true bugs. On the **32 catch-all judgments whose D
cell the rule does define**, **17 rest on true bugs (53.1%) against a pool base rate of 63.0%** — if
anything below it, at about one standard error, so we could not detect enrichment. The honest
reading of this channel is the composition, not a rate.

**The judge departs from the appended rule in 22 of 243 judgments forward and one in reverse** —
17 forced to False-Positive, which the red lines forbid, and 5 to Confirmed; **10 of the 17 rest on
true bugs**. Replaying with the rule enforced moves 39/51 → 43/51 and 21/30 → 19/30 under the
convention, and nothing under the forced reading. One caveat bounds the paragraph: the dispatch
prints an earlier rule whose last step commands exactly those closures, so they are deviations from
the appended rule and compliance with the earlier one.

### 4.6 Comparison with the crash-oracle baseline（~200 词，已写全）

Run to natural completion against the Qdrant instance where our silent-accept defects are live, the
released VDBFuzz template set (205 templates; 50.8 minutes wall time; the per-template logs record
every mutation loop and every response) produces **0 oracle anomalies**. The per-template logs record 1,127 mutation stages and 11,629 response-status lines, with no 5xx
anywhere; the runner's master log is a verbatim echo of them, so any total taken over the shipped
directory doubles. We report the single-copy figures. The per-template oracle fires on 5xx rather than on
service death, and the released mutation vocabulary tops out below the values some crash classes
need, so the zero is a bound on **the released configuration's** reach into the silent majority
rather than on the crash-oracle family. A hand-guided probe built on the pipeline's boundary
reasoning submits a value that vocabulary cannot reach; the probe script ships and its output was
not retained, so no execution result is claimed.

One artefact of the released tool meets a reader who opens the logs to audit the zero: 152 lines,
across 119 of the 205 per-template logs, report three anomalies apiece. They come from the
baseline's own no-mutable-fields path, which returns a three-key dictionary where its caller counts
failures, so a dictionary reads as a count. They are not oracle decisions — every stage-completion
line in those same logs records zero — but they look like anomaly reports, and we say so here
rather than leave them to be found.

---

## 5 Discussion（~650 词，已写全）

**Audit what your oracle reads, not only what it concludes.** Thirteen per cent of the
constraint-page pairs our stage read were supported by the page they cited; another 43% cited the
wrong kind of anchor, and 43% had no support at all. Every pipeline in this line distils
documentation and judges against the distillation, and the distillation is the step nobody measures.
It is cheap to measure: a sample of pairs against their cited pages suffices to know whether your
confirmation rate is a property of your judge or of your materials.

**Put the evidence guard where the error mass is.** On the deployment we audited, the protocol
requires verbatim intent evidence
for the refutation it makes least often and gets most right, and requires nothing for the one that
closes the most judgments and is wrong half the time. The counterfactual prices the fix at seven
true bugs for nine interceptions under the convention — and at nothing under the forced reading,
which is the cleanest demonstration that it is the convention, not the judge, that pays for
abstention. The prescription is bounded by what we measured: the error mass moved on the second
backbone, where the guarded clause closes 50 judgments and is wrong 22 times, so the rule is
advice about where to look rather than a property of the protocol.

**Price the deferral channel, and price the contrast, not just the level.** The routing change
(the flat judge to the rule-bearing judge) is worth nine under the convention and falls by two
thirds — to three — when the routed queue is hand-adjudicated
rather than credited by convention; the deployed stage's own price against the same baseline is
four. The pricing is still a floor: at the reading this paper considers
honest, the routing change is suggested, not established.

**Check the dispatch before you re-architect the judge.** Our own dispatches contained four defects:
a declared output field contradicting the prompt's verdict vocabulary (in eight of twelve arms); a
prompt printing two aggregation rules with opposite defaults; two complete perspective definitions
with C and D exchanged; and an output schema declaring the source vocabulary for the perspective the
text calls maintainer cognition, which 98 of 243 recorded cells use. A one-line schema repair moved
five of the headline nine bugs. **None of the four was found by our own audit**; all were found by
reviewers reading the shipped texts. That is the limit of self-audit and it is why the paper reports
them rather than repairing them quietly.

**Self-auditing a stage against its own rules is cheap and informative.** Replaying the printed rule
over the judge's own recorded values showed 22 forward departures, 17 in the direction the red lines
forbid, 10 of those on real bugs. That is a five-line script.

## 6 Threats to validity（~800 词，已写全）

**Yield.** A record of submissions and adjudication, not a per-run rate; the detection-ability runs
were voided and we supply no such rate. The 81 span 16 versions and the 51 span 15, against the
ledger's 19. The fix-PR characterisation is outside the shipped artifact.

**Pool.** Submission-filtered subset of one pipeline's output; maintainer adjudication without an
inter-annotator study, and the 30 negatives adjudicated by us. Recall levels are contrasts on a
common pool, not operating performance. One case is unjudgeable and, under the convention, credited
to eleven of the twelve configurations — every one but the contract core routes it.

**Materials.** Two leak repairs were applied and every number here is computed on the cleaned pool;
the raw generations ship so a reader can reconstruct either. The pair audit is a single-reader
classification without a second coder; the re-anchored and unsupported rates are this distiller on
these three vendors' documentation, and we do not generalise them. The row-level accounting of the
rebuild does not fully reconcile in our own report and we flag it as an open item; the rates we
print are the pair-level ones, which do reconcile.

**Design.** The twelve configurations were added during the study, not pre-registered. Three
contrasts change more than one thing; the four-perspective contrast changes five. The two steps of
the deployed change are individually under-powered at the recall level — the rule step is
significant at the confirmed-set level and not at the recall level, and we report both. The bundled
effect is a third of its convention-level size under hand-pricing, itself a floor; the joint prices,
the catch-all composition and the expectation-framing check are printed but not scripted.

**Backbone.** Two backbones, three systems, one domain, one task; the second varies with the
dispatching session rather than being randomized, both are serving aliases without pinned weights,
and it has no schema-repaired control. **The clause census is scoped to the primary backbone for the
same reason**: its pattern does not reproduce on the second, and the deployed dispatch defines the
four perspectives twice with C and D exchanged, so the two censuses may not be comparable. On the
primary the letters are identified by their content (§4.5).

**Counting.** Headline rates use the deployment's convention; the joint reading is author-executed
and non-blind, an independent pass bounds it rather than confirming it, and two of three protocol
statements put it at the forced floor. Both §4.5 replays are no-ops under the forced reading.

**Instrument.** Four dispatch defects are reported rather than repaired, and §4.5's departure count
and its catch-all composition both depend on treating the appended aggregation as operative.

## 7 Related work（~790 词，已写全）

**Oracles derived from documentation.** Deriving test oracles from documentation is an old idea:
tabular specifications (Peters and Parnas \cite{peters98}) and natural-language resource
specifications (Zhong et al. \cite{zhong09}) predate LLMs, and the comment–code inconsistency
literature (\cite{icomment07,docref13}) and its LLM-era successors (\cite{docchecker24,c4rllama25})
share this paper's premise that a prose artifact is the statement of intent. The tagged-Javadoc and
dependency-grammar tools — @tComment, JDoctor, DocTer, Toradocu \cite{tcomment12,jdoctor18,docter22,toradocu16}
— and the REST-side constraint miners (RESTInfer, ICON, RBCTest
\cite{restinfer22,icon16,rbctest26}) derive checkable expectations from prose, but at method or
parameter granularity, and they keep the derived oracle as the final arbiter, validating it through
runtime behaviour. Konstantinou et al. \cite{konstantinou24} document the gap this produces: such
oracles tend to capture actual rather than expected behaviour. The line we are closest to
operationally is Metamon \cite{metamon25}, which asks an LLM whether a generated regression oracle
agrees with the method's documented specification and then stabilises that same LLM judge; its
falsifier is another LLM question, which is the self-reference this pipeline's source grounding
exists to break. Its published profile (precision 0.722 at recall 0.480) is the same tradeoff
measured on a different pool and ground truth, not a head-to-head baseline. Structured-source
oracles — AGORA+ from traces, SATORI from OpenAPI fields, MASTOR from source, MASTEST from a
specification composed into executed tests \cite{agoraplus25,satori25,mastor26,mastest26} — anchor
their expectations in something other than system-level prose; MASTOR in particular takes the
implementation as its authority, whereas here the implementation can only refute a claim the prose
supplied, never supply one. What this paper adds to the line is not a new oracle but an audit of the
oracle's *input*: §4.3 measures how much of the distilled specification the judge reads is supported
by the pages it cites.

**LLM judges, and what a multi-perspective organization does.** That LLM evaluators prefer their own
output is established \cite{zheng23judge,panickssery24,wataoka24}, as is intra-judge
inconsistency — one judge's ratings on the same input varying across runs \cite{haldar25}. The
closest work to ours is Ma et al. \cite{manyminds25}, who measure multi-agent judging for *bias*
rather than for accuracy and find that debate amplifies judge biases after an initial round while a
meta-judge resists them; they establish that adding perspectives is not a uniform correction, which
is the premise our four-perspective stage is built on and, on this pool, the finding we reproduce in
a different currency: the organization changes *which* cases are decided, not how many, and on a
second backbone it costs recall rather than buying it. Two further results shape our design.
Bodicoat et al. \cite{bodicoat25} find in a controlled study that prompting technique and supplied
context dominate model choice in oracle accuracy — which is why our flat-judge comparison holds the
materials fixed and varies the organization instead. Molinelli et al. \cite{molinelli25} show on a
leakage-free benchmark that LLM oracles reach near-human mutation scores on average while remaining
unreliable per-subject, and that training-data contamination is a first-order validity threat; §6
carries that threat here rather than claiming to have excluded it. TRACE \cite{trace26} is adjacent
in spirit: it measures where LLM judgment breaks down on conflicting artifacts and finds a
systematic blind spot when the implementation drifts while the documentation stays plausible — the
asymmetry a source-anchored falsifier is built for.

**Non-crashing bugs in database systems.** The DBMS-side literature targets wrong-result bugs
without documentation: NoREC, TLP, DQE, PQS and DDLCheck \cite{norec20,tlp20,dqe23,pqs20,ddlcheck25}
compare an engine against its own alternative evaluations or schemas, BUZZBEE \cite{buzzbee24}
fuzzes DBMSs generically, and ACME \cite{acme26} and Argus \cite{argus25} bring LLMs in to derive
clause mappings or query-equivalence oracles — Argus validating them with a formal prover, the
DBMS-side instance of grounding oracle authority outside the model. All of these anchor in the
implementation's own semantics and so expose optimization and internal-consistency bugs rather than
violations of external documentation; the roles are inverted here, with the prose supplying the
expectation and the implementation serving only as the falsifier. LogicHunter \cite{logichunter26}
is a near neighbour in an adjacent domain, and its oracle is a telling contrast: it treats retrieved
documentation as the statement of intent but consults and executes the implementation freely before
returning a verdict, where here the implementation is never the statement of intent.

**Testing vector databases.** VDBFuzz \cite{vdbfuzz26} is the first dedicated VDBMS fuzzer and is
crash-oracle by construction; §4.6 runs its released configuration and prices what that oracle
reaches. The roadmap \cite{roadmap25} identifies oracle definition as the field's open problem, and
the empirical bug study \cite{bugstudy25} supplies the taxonomy that motivates the focus on
non-crashing defects. To our knowledge no prior work measures the reliability of a
documentation-derived oracle on an adjudicated pool of VDBMS cases, which is what the pool and the
twelve frozen configurations below are for.

## 8 Conclusion（~430 词，已写全）

We set out to measure what determines which candidate defects an LLM confirmation judge confirms,
and the answer on this pool is not the judge's internal organization. Two configurations that differ
in whether they carry a four-perspective decomposition confirm the same number of true bugs under
forced verdicts on both backbones — 27 of 51 and 26 of 51 — while agreeing on only 22 and 23 of
those cases: the organization changes which cases are decided, not how many. What moves the outcome
is how often the judge declines to decide. Adding an aggregation rule that lets it route a case to
human review rather than close it raises recall on both backbones (0.588 to 0.765, 9/0 at the recall
level, $p{=}0.0039$; 0.529 to 0.804, 14/0, $p{=}0.0001$) — and on the confirmed set the same two
contrasts are 17/0 and 19/0, both $p{<}0.0001$. Almost all of that is deferral: forced-verdict
recall moves only 25 to 27 and 23 to 26. Under the deployment's convention, where a routed case
counts as confirmed, the rule's effect and the routing rate are the same quantity, and we say so
rather than presenting the difference as the rule getting better at deciding.

Two measurements bound what a judge is worth even when it is right about the evidence. An audit of
the specifications it reads found 43.3\% of their cited (constraint, page) pairs unsupported by the
pages they cite, so a confirmation rate can be a property of the materials rather than of the judge.
And the clause that closes the most judgments is the one the protocol guards least: contract
refutation carries no evidence requirement, closes 50 of 243 judgments and is wrong about half the
time, while the guarded by-design clause closes 19 and is right 17 times. The guard protects the
clause that was already clean. Fixing that is a replay rather than a re-adjudication, and its gain
exists only under the counting convention — which is itself the finding: on this pool, what an
LLM judge confirms is decided less by how it is organized than by how it accounts for the cases it
refuses to decide.

**Data availability.** The replication package is at [anonymized URL]: the pool, the frozen per-run
verdicts of all twelve configurations, the packages the study read (the post-rebuild,
cognition-stripped generation the dispatches name; the earlier rebuilt generations are archived
separately and do not ship), the dispatch texts, the pair-audit verdicts, the adjudication worksheet
and the blind passes, and the five analysis scripts named in §4.1. Where a run was re-judged after
either leak repair, the re-judged cases and the pre-repair state both ship beside the untouched
batches, so either pool can be reconstructed from the package alone.

---

## 数值自检（每条注明来源）

| 断言 | 值 | 来源 |
|---|---|---|
| yield | 81 = 51(29/14/8) + 30；23 fixed；**台账 132 行覆盖 19 版，81 案跨 16 版，51 案跨 15 版** | ledger |
| void | 15 版本 RQ1 检测能力实验全作废（2026-08-23）；**81 案中 26 案（20 确认）在其版本上** | `VOIDED-ALL-15.md` |
| **⚠️ 未结** | 上一条的 join 复现不出：按 (vendor, reported_version) ∈ `rq1-fullrun/` 的 12 个版本目录匹配，现行台账给 **49 案（30 确认）**；R2 独立重建给 27/21；论文印 26/20。差异源于**台账代际**（工作区 xlsx 已是 52-TP 口径，见 [[phase1-xlsx-and-tp-strategy]]），需先定"以哪一代台账 + 哪一套版本集为准"再改数或删数 | 本人三法对比 |
| **泄漏修复** | **10 包内嵌认知节被剥（13 run 重判）；7 案认知锚点被清除（两骨干重判）** | `CLEAN_POOL_FINAL.md`；**去掉后部署臂为 41/51** |
| 审计对级 | 134 = **18 / 58 / 58**（两个 43.3% 各占 134，非合计 86.6%） | `pair_audit.py` |
| 审计案级 | 12 = 5 / 3 / 2 / **2**；动作 7 改写弱化 / 3 丢弃 / 2 恢复 | `pair_audit.py` + `verify_verdicts_main.jsonl` |
| 部署变更（捆绑） | 30→39（召回 0/9 p=0.0039；确认集 34→51，0/17，p<0.0001）；forced 25→27 | artifact 脚本 |
| 部署臂 vs flat | 召回 39 vs 30（11/2，p=0.0225）；**确认集 48 vs 34，16/2，p=0.0013**（部署臂在前） | artifact 脚本 |
| schema 步 | 召回 0/5 (p=0.0625)；确认集 34→39，1/6，p=0.1250 | artifact 脚本 |
| 规则隔离步 | 召回 2/6 (p=0.2891)；**确认集 39→51，2/14，p=0.0042** | artifact 脚本 |
| **joint 定价** | 规则臂 29→32 = **+3**；部署臂 29→33 = **+4**；**对称计满 = +4**（不对称才是 +5） | 本人重算 |
| **源码臂（补漏后）** | 48+18；supp **0.400**、prec 0.727；**net 30（与 full 持平）**、F1 **0.821**；**forced 31**（原 30，milvus_006） | 本人重算 |
| **重判效果** | 6 个重判文件改 19 个判定：**15 朝确认、4 无操作、0 反向**（convention 二值口径；三级序口径才是 18/1/0，v10 修正）；两臂 TP 集合不变（48/33）、FP +2/+1 | 本人重算 |
| **无聚合臂（补漏后）** | 33+3；supp **0.900**、prec 0.917；**net 30**、F1 0.759；vs flat **确认集 36 vs 34，6/4，p=0.7539** | 本人重算 |
| **源码对比** | 召回层 0/9 p=0.0039（**不变**）；**确认集 48 vs 66，0/18，p<0.0001**；supp 21/30→**12/30** | 本人重算 |
| **net/F1 区间** | 无源码 − full：net 0 **[−8,+8]**、F1 +0.033 **[−0.044,+0.115]**（配对 bootstrap 20k，seed 20260914） | `bootstrap_net_f1.py` |
| Qwen | 捆绑 27→41 (0/14, p=0.0001) | artifact 脚本 |
| 视角（五变量） | 39 vs 39 (4/4, p=1.0, ±0.11)；Qwen 41 vs 30 (12/1, p=0.0034, forced 26 vs 26) | artifact 脚本 |
| 强制跨度 | 九臂 **[23,31]**/[27,48]（6 主骨干 + 3 Qwen，不含两个 core）；core 8；source-only 20、19 | 本人重算 |
| **identification** | 主骨干 19 个 C=Refuted 关闭格：**15 引注释/文档字符串、2 引服务端校验规则（milvus_026 的两个 run）、2 引代码结构**（milvus_011、milvus_012 各 run3；这两案的另两 run 均记 WEAK_REFUTED 并写明「无注释/quote 明文」）；D 词表 145 认知 / 98 源码 | 本人逐格读 rationale（v10 修正） |
| **多数票规则** | 「至少两次算作确认」（convention 二值）→ 39/51；严格多数（两次须记同一判定）→ **37/51**；**3 案三向分裂**（milvus_021/038、qdrant_027） | 本人重算 |
| **Holm 家族** | 正文印 **16 个配对检验（召回层 10 个）**；m=10 下 Holm 留 4 个（0.0001/0.0034/0.0039/0.0039，对 α/10…α/7），**停在第 5 个 0.0225** | 本人重算（v10 修正，原为循环定义） |
| 条款表 | 243 = 61+21+7+50+19+16+69；A 24/50；C 17/19（**三个 FP 条款的中间**）；错误关闭 30，A 占 24 = 80% | `clause_tally.py` |
| catch-all 构成 | 69 中 37 用源码词表（**54%**，28 真 bug）；32 可定义，17 真 bug = 53.1% vs 63.0%（**−1.12 SE**，SE 取观测比口径；取基准率口径为 −1.16） | 本人重算 |
| 重放 | 严格 43/51·19/30；反事实 46/51·12/30；**两条 forced 均 no-op** | `clause_tally.py` |
| 定价 | 0.765 / 0.529 / 0.647；独立 30·27·27（两个落强制地板） | `convention_pricing.py` |
| 派发缺陷 | **4**：8 臂二值 vs 三值散文；2 张聚合表；2 套视角定义；D 词表 98/243 | 本人逐文件审计 |
| RQ3 | 205 模板 / 50.8 min / 0 异常；**11,629 响应状态行 + 1,127 阶段完成行**（主日志是逐字回声，全目录口径正好 2×） | artifact rq3 逐日志计数 |

**⚠️ 不印的**：重建行级漏斗（不闭合）。**已解决、不再挂账**：RQ3 变异/响应总数此前记作"三种数法不一致（2,254 / 1,910 / 22,540）"——那是主日志回声未扣除造成的假象；扣除后单份 = 11,629 响应 / 1,127 阶段，§4.6 印的就是这两个数。

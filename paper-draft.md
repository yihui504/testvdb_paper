# TestVDB 论文正文底稿

> **标题候选**：TestVDB: Detecting API Compliance Defects in Vector DBMSs via Contract-Truth Separation
> **对标**：DDLCheck (VLDB 2025) *"Detecting Schema-Related Logic Bugs in Relational DBMSs via Equivalent Database Construction"*
> **目标会议候选**：VLDB / SIGMOD（数据库）；ICSE / FSE / ESEC（SE）；ISSTA（测试）
> **状态**：摘要 + §1 引言 + §3 方法 已成稿；§2/§4/§5/§6 草稿 + 待扩。配套 [paper-draft-v3.pptx](paper-draft-v3.pptx)（24 slides）。
> **一句话故事**：分离断言层（contract）与真相层（维护者权威），用真相层反证断言层，把 LLM 判定改造为可反证、可纠错的链式 oracle，从而可靠挖掘向量库 API 合规性缺陷。

---

## 摘要

向量数据库管理系统（VDBMS）已成为现代 AI 应用的核心基础设施，支撑语义检索、检索增强生成（RAG）和推荐系统的大规模落地。与关系型数据库不同，VDBMS 暴露的是复杂且快速演进的 REST/gRPC API，其参数合法性校验主要由非形式化的官方文档界定，而非严格规范。这一空白催生了 **API 合规性缺陷（API compliance defects）**——数据库静默接受了文档明令禁止的输入（如 `nprobe=0`、`shardsNum=-1`、空查询向量），导致数据损坏、性能退化和安全风险。一项最新的实证研究在两年内统计了 15 个开源 VDBMS 的 **1671 个 bug-fix PR** [arXiv:2506.02617]，其中 API 校验与参数处理类缺陷占据相当比例。

现有测试方法无法可靠检测这一类以 Type-1 为主、覆盖 Type-2/3/4 形态的 API 合规缺陷家族。差分与元变态测试技术（NoREC、DQP、Radar）针对 SQL 优化 bug，难以迁移到向量 API 合规场景。直接用大语言模型（LLM）作 oracle 同样不可靠：LLM 判定存在幻觉、缺版本上下文，且**无反证机制**。更严重的是，文档化的 contract 本身常常过时或含糊，因此即便 LLM 判定正确，对抗错误的 contract 仍会产出假阳性。

我们提出 **TestVDB**，一个基于单一设计原则的多 Agent 缺陷挖掘框架：**将断言层（contract / threat model / LLM 判定）与真相层（维护者权威——源码、PR、issue 跟踪器）分离，用后者反证前者**。TestVDB 把这一原则落实为四层 oracle 链——contract 检查、4-Judge 辩论、dev-reviewer 在 Docker 沙箱中反证、双层 Novelty Gate——每一层都是独立的反证机会。

我们在 5 个主流 VDBMS（Milvus、Qdrant、Weaviate、Meilisearch、Chroma）上应用 TestVDB，提交 **108 个 issue**，其中 **32 个被维护者明确承认（24 个已修复、8 个已接受）**，**12 个被标记为 by-design**——这实证了 contract 层不可靠，也证明真相层的反证在干活。跨层消融实验显示，单独的 4-Judge LLM 辩论仅取得 **12.9% precision**，而 dev-reviewer 反证层独自剔除 **80.6% 的假阳性**，把全链 precision 提升到 **72.7%（5.6 倍）**。作为副产物，TestVDB 还发现了一个数学上不可能的精度缺陷（相同向量的 cosine 距离 > 1.0），该 bug 在 Milvus 和 Qdrant 两个独立系统中均被修复。

---

## 1. 引言

### 1.1 动机：VDBMS 已成为承重 AI 基础设施

向量数据库管理系统（VDBMS）已成为生成式 AI 时代的数据骨架。通过存储与检索高维向量，VDBMS 支撑了语义检索 [ref]、检索增强生成 [ref]、个性化推荐以及日益增多的 agentic 工作流。主流开源 VDBMS——Milvus、Qdrant、Weaviate、Chroma——已在生产环境大规模部署，一项最新的实证研究在两年内统计了 15 个开源 VDBMS 的 **1671 个 bug-fix PR** [arXiv:2506.02617]。随着 VDBMS 成为承重基础设施，其正确性缺陷的代价也相应放大。

### 1.2 问题：API 合规性缺陷

在 VDBMS 已观察到的缺陷类别中，有一类尤其普遍但未被充分研究：**API 合规性缺陷**。它发生在 VDBMS 静默接受了文档明令禁止的输入时。这类缺陷的形态分布很广：

- **Type-1（非法成功，最普遍）**：最常见的形态是参数边界违规——`hnsw_ef=0`（Qdrant [#9017]）、`nprobe=0`（Milvus [#49823]）、`flatSearchCutoff` 接受负值（Weaviate [#11396]）。更隐蔽的形态包括**静默归一化**（`replicationFactor=-1` 被静默改成 1，Weaviate [#11397]）和**静默截断**（int64 上界 `9223372036854775807` 被截成 `92233720368547760`，Weaviate [#11735]）——这类缺陷**返回成功但语义已 corrupt**。
- **Type-2（诊断不足）**：服务失败但错误信息暴露内部实现，例如 Qdrant 的 serde 反序列化错误直接把 Rust 内部类型名透出给用户（[#9525]），既泄露实现细节又无法定位真因。
- **Type-3（运行时稳定性，副产物）**：对抗输入触发 panic 或数据丢失，例如空向量 upsert 触发 Qdrant 服务崩溃（[#9045]），或 `shard_number=INT_MAX` 触发崩溃（[#9520]）。
- **Type-4（精度，亮点）**：违反数学性质，例如相同向量的 cosine 距离超过 1.0 这一数学上不可能的现象，我们独立地在 Milvus [#49059] 和 Qdrant [#8688] 中都发现了它，两个系统都已/将修复。

API 合规性缺陷（Type-1）很少导致服务崩溃，而是 corrupt 查询语义、降低 recall 或暴露安全面，且只通过下游模型行为间接显现。

### 1.3 为什么重要

API 合规性缺陷之所以阴险，是因为它违反了*文档化的 contract*——这是绝大多数开发者唯一阅读的"规范"。集成 Milvus 的开发者依赖文档中"nprobe 必须为正"的约束；若服务静默接受 `nprobe=0`，下游检索流水线会产出静默错误的结果，且没有任何可观察的错误可供追溯。这一缺陷类别在数值上也很显著：[arXiv:2506.02617] 统计的 1671 个 VDBMS bug 中，API 校验与参数处理类别占据相当比例。

### 1.4 现有方法及其失败原因

既有的 DBMS 测试技术无法迁移到这一问题。**NoREC** [Rigger2020]、**DQP** [Ba2024]、**Radar** [Song2025] 通过差分与元变态 oracle 检测 SQL SELECT 执行中的优化 bug，它们要求 SQL 形态的查询与明确定义的等价变换——VDBMS 的 REST/gRPC 接口并不暴露这些。**通用 fuzzing** 产出的是在表层就被拒绝的语法非法输入，且没有 oracle 判断一个*未被拒绝*的输入是否本应被拒绝。自然的替代方案——用大语言模型以文档 contract 为提示作 oracle——则以另一种方式不可靠：LLM 判定存在幻觉、缺失版本特定上下文，且最关键的，**没有反证机制**。更糟糕的是，文档 contract 本身常常过时、含糊或不完整；我们在实验中观察到约 **30% 的 contract 层结论被维护者权威反证**（见 §4）。一个 LLM oracle 对着错误 contract 做判定，从构造上就是错的。

### 1.5 核心 insight：断言/真相分层

我们的核心观察是：向量库合规测试中不可靠的组件*并非 LLM 本身*，而是**两个本应被分离的角色被混淆**了：

- **断言层（assertion layer）**：关于系统*应该*做什么的主张——contract、threat model、LLM 判定。
- **真相层（truth layer）**：系统*由其维护者定义*的实际行为——源码、已合并 PR、by-design 注释、既有 issue。

基于 LLM 的测试框架把这两者混淆，把 LLM 判定既当断言又当真相。我们提出 **contract-truth separation**：用断言层*生成*候选，用真相层*反证*候选。每一个反证机会对应流水线中独立的一个阶段，每一个被拒绝的候选都让最终 precision 更锐利。

### 1.6 方法：TestVDB

我们将这一原则落实为 **TestVDB**——一个具有四层反证机制的多 Agent 缺陷挖掘流水线：

1. **Threat model 构建**：从目标 VDBMS 的历史 issue、PR、commit 中提炼反复出现的缺陷模式、文档化的 by-design 行为，以及维护者的认知盲点（cognitive blindspot）。Threat model 同时注入攻击生成与下游判定。
2. **Attack agents**：boundary、semantic、state 三类攻击 Agent 针对生成候选缺陷，分别覆盖 Type-1/2/3/4。
3. **4-Judge 辩论**：四个独立 judge（evidence、severity、novelty triage、documentation）对每个候选投票，产出仍可能出错的 Debate-Confirmed 集合。
4. **Dev-reviewer 反证**：一个模拟目标 VDBMS 维护者的 Agent 阅读源码、在 Docker 沙箱中复现候选，独立地确认或证伪——这是"是否真缺陷"的*唯一出口闸门*。

最后的**双层 Novelty Gate**（本地 threat model + corpora，以及 GitHub Search API）过滤已知与已被覆盖的缺陷，产出可提交的 Gate-Endorsed 集合。Issue 提交始终是人工动作。

### 1.7 结果

我们在 **5 个主流 VDBMS**——Milvus、Qdrant、Weaviate、Meilisearch、Chroma——上应用 TestVDB，覆盖专用向量库与搜索引擎扩展两类形态。TestVDB 提交了 **108 个 issue**，维护者明确承认 **32 个（24 个已修复、8 个已接受）**，**12 个被标记为 by-design**——这实证了 contract 层不可靠，也证明真相层的反证做了实事。在 Milvus v2.6.19 上的跨层消融实验显示，4-Judge LLM 辩论单独只取得 **12.9% precision**，而 dev-reviewer 反证层独自剔除 **80.6%** 的假阳性，把端到端 precision 提升到 **72.7%——5.6 倍改善**。作为副产物，TestVDB 还发现了两个稳定性崩溃缺陷与一个数学上不可能的精度缺陷（cosine > 1.0），后者在 Milvus [#49059] 和 Qdrant [#8688] 两个独立系统中均被修复。

### 1.8 贡献

本工作在**理论、方法论、技术、原创增量、实证、工程**六个层面做出贡献，每一项都建立在我们前期提出的理论框架（[AI-DB-QC 理论框架报告 v2.0]）之上，并明确针对既有工作的真实局限。需要说明：本工作相对 v2.0 框架做了一次有意识的方法论收敛——**放弃以 LLM 语义打分作为 oracle（v2.0 创新点 2）**，转而以维护者权威为核心 oracle——这一演化及其证据见 §4。

**贡献 1（理论）——VDBMS 四型缺陷分类法的形式化与实证校准**
我们提出针对 VDBMS 的四型缺陷分类（Type-1 非法成功 / 合法拒收、Type-2 诊断不足、Type-3 运行时崩溃、Type-4 状态/逻辑违规），决策树见 §3.2。我们设计**双层反证闸门**作为前置条件类（PF）假阳性的过滤机制：**L1 Mechanical Gate**（[verify_live_l1.py](TestVDB/scripts/verify_live_l1.py)，零 LLM，12 个 Check 类）实测覆盖 **~90% 历史假阳性模式**（HTTP 层混淆、脚本语法错、缺索引等 PF 形态）；**L2 Semantic Gate**（[verify-live-l2.md](TestVDB/agents/verify-live-l2.md)，Docker 实测）覆盖 L1 无法裁决的 **~10% 语义残余**。TestVDB 不再使用 v2.0 框架的"抽象合法性 × 运行时就绪性"分类（v2.0 的 Type-2.PF 已删，由 L1 机械闸门 REFUTE）。与 IEEE 1044、ODC 等通用 8 维分类不同，本分类法专门面向 VDBMS 的 API 形态。我们用 [arXiv:2506.02617] 的 1671 个真实 bug 校准了该分类法的覆盖度，并在 §4 给出跨 5 个 VDBMS、108 个新缺陷的实证分布。**对比既有工作**：[arXiv:2502.20812] 提出 VDBMS 测试路线图但未给出缺陷分类法；[arXiv:2506.02617] 给出缺陷分布统计但未形式化分类。

**贡献 2（方法论）——Contract-Truth 分层作为可信 LLM-oracle 的设计原则**
我们识别出 LLM 驱动测试不可靠的根因——**断言层（contract / LLM 判定）与真相层（维护者权威：源码、PR、issue）被混淆**——并提出 contract-truth separation 作为可信 oracle 设计的一般原则：用断言层*生成*候选、用真相层*逐级反证*，每一级反证都是独立的、可审计的、可证伪的。**对比既有工作**：NoREC/Radar 用等价 SQL 变换作 oracle（要求 SQL 形态），元变态测试要求预定义关系（RENE 等），纯 LLM-as-oracle（[arXiv:2505.02012] 的 SQL 合成）无反证机制，contract-based testing 把 contract 当真相而非断言。本原则**首次把"维护者权威"显式建模为 oracle 的真相层**，并允许 contract 本身被反标。

**贡献 3（技术）——四层可反证 oracle 链与 dev-reviewer Agent**
我们将 contract-truth separation 落实为四层 oracle 链（contract → 4-Judge 辩论 → dev-reviewer 反证 → 双层 Novelty Gate），其中 **dev-reviewer Agent** 是核心技术贡献：它通过阅读目标 VDBMS 源码 + Docker 沙箱复现，模拟维护者对每个候选缺陷独立证伪。消融实验（§4）显示该层独自剔除 **80.6% 假阳性**，是整个 pipeline 的 workhorse，把端到端 precision 从 12.9% 提升到 72.7%（5.6 倍）。**对比既有工作**：既有 LLM 多 Agent 测试工具（CodaMosa、AutoGRML 等）聚焦于代码生成 + 执行反馈，没有显式的"维护者代理反证"层；既有差分测试工具依赖参考实现，VDBMS 不存在可用的参考实现。

**贡献 4（原创增量）——历史驱动的 Threat Model 与维护者认知盲点建模**
我们从目标 VDBMS 的历史 issue、PR、commit 中自动提炼三类情报：(a) 反复出现的缺陷模式、(b) 文档化的 by-design 行为、(c) **维护者认知盲点（cognitive blindspot）**——历史上反复被外部报告但被维护者判定为 by-design 的边界行为。该 threat model 同时注入攻击生成（指导挖掘方向）与下游判定（指导反证）。**这是本工作相对 v2.0 框架的真正原创增量**——v2.0 用静态三层 contract，TestVDB 用历史驱动 + 认知盲点建模。**对比既有工作**：既有 LLM 测试工具用静态 prompt 或 RAG 检索，没有显式的历史驱动 threat model；既有 fuzzing 用覆盖率引导，不利用维护者历史认知；这一组件让我们能在维护者未回应前就预判哪些"看似 bug"实际是 by-design。

**贡献 5（实证）——5 个主流 VDBMS 上发现 108 个先前未知缺陷**
我们在 Milvus、Qdrant、Weaviate、Meilisearch、Chroma 5 个主流 VDBMS 上发现 108 个先前未知缺陷，提交后维护者明确承认 **32 个（24 fixed + 8 accepted）**，12 个被标 by-design；其中包含数学上不可能的精度缺陷（cosine > 1.0）在两个独立系统中的复现。**对比既有工作**：这是迄今规模最大的 VDBMS API 合规缺陷*工具自动发现*数据集；[arXiv:2506.02617] 的 1671 bug 是从历史 PR 中挖掘的，不是工具实时发现的；既有 VDB 评测工作（vector-db-benchmark 等）关注性能而非正确性。

**贡献 6（工程）——开源 TestVDB 框架与可复用反证数据集**
我们将 TestVDB 框架、5 个 VDBMS 的 threat model、缺陷 issue 草稿，以及一份 31 条规模的**维护者代理反证标注集**（dev-review verdict，含 root_cause 分类）完全开源（[GitHub URL，论文 camera-ready 后公开]）。后者尤其有价值——它是 LLM 测试研究少见的人工可审计中间层数据集，可作为未来 VDBMS 测试研究的弱 ground truth。我们也承诺在论文发表后维护该项目，接受社区贡献的新 threat model 与新 VDBMS 适配器。

---

## 2. 背景（草稿，待扩）

### 2.1 向量数据库的查询语义

[ref 待补：ANN 算法基础、HNSW/IVF/PQ 索引家族、近似性 vs 精确性的权衡。]

### 2.2 主流 VDBMS 的 API 形态

| 系统 | 接口 | 索引家族 | 状态模型 |
|---|---|---|---|
| Milvus | REST v2 + gRPC + PyMilvus | HNSW/IVF/DiskANN | collection / partition / segment |
| Qdrant | REST + gRPC | HNSW | collection / point |
| Weaviate | REST + GraphQL | HNSW | class / object |
| Chroma | Python SDK | HNSW | collection |
| Meilisearch | REST | LMDB | index / document |

### 2.3 VDBMS 与关系库的差异（决定测试方法不可迁移）

[ref 待补：数据类型 / 查询语义 / 算法确定性 / 状态管理 / 错误诊断 五维差异。]

---

## 3. 方法

### 3.0 概述（Overview）

TestVDB 把 contract-truth separation（§1.5）落实为一条**粗到细的漏斗流水线**，每个候选缺陷要依次穿过四个独立的反证闸门。每个闸门都有权拒绝候选，**没有任何一层能单独让候选"成为真缺陷"**——成为真缺陷必须穿过全部四层。

```
[目标 VDBMS]
     ↓ (a) 历史驱动情报
[Threat Model] ──────────────┐
     ↓ b 注入                  │ c 注入
[Attack Agents]              │
   boundary / semantic / state│
     ↓ 生成候选缺陷脚本        │
[Docker 沙箱执行]             │
     ↓ 行为观测                │
[4-Judge 辩论] ◄──────────────┘
   evidence / severity / novelty / doc
     ↓ 通过 → Debate-Confirmed
[Dev-Reviewer 反证] ◄── 读源码 + Docker 复现
     ↓ 通过 → Dev-Endorsed
[双层 Novelty Gate]
   L1 Consumer / L2 Corrector
     ↓ NOVEL → Gate-Endorsed
[人工选择性提交 issue]
```

四个反证层的角色分工：

| 层 | 反证什么 | 用什么反证 | 输出 |
|---|---|---|---|
| **3.2 Attack Agents** | contract 是不是真被违反 | 边界/语义/状态攻击脚本 + Docker 实测行为 | 候选缺陷（~1834/库/run）|
| **3.3 4-Judge 辩论** | 候选是否同时满足证据、严重性、新颖、文档四视角 | 4 个独立 LLM judge 投票 | Debate-Confirmed（~33/库/run）|
| **3.4 Dev-Reviewer 反证** | Debate-Confirmed 是不是真 bug | 模拟维护者读源码 + Docker 复现 | Dev-Endorsed（~4/库/run）|
| **3.5 Novelty Gate** | Dev-Endorsed 是不是已知 / 已覆盖 / by-design | 威胁模型 + 本地语料 + GitHub API | Gate-Endorsed（NOVEL 子集）|

漏斗形态**不是装饰，而是经济学**：3.4 的 Docker 复现 + 源码阅读最贵（每个候选几分钟），不能跑 1834 个；3.2/3.3 用便宜的方法先收敛。漏斗的累积 precision 见 §4 RQ3。

### 3.1 Threat Model 构建（历史驱动情报）

TestVDB 不用静态 prompt 测试，而是从**目标 VDBMS 自身的历史**中提炼威胁模型（Threat Model），再注入攻击与判定。这是本工作相对前作 [v2.0 报告] 与既有 LLM 测试工具的主要原创增量（§1.8 贡献 4）。

#### 3.1.1 三类历史情报

Threat Model 模块（`threat-modeler` Agent）抓取目标 VDBMS 仓库的历史 issue、已合并 PR、commit，提炼三类结构化情报：

1. **缺陷模式（defect pattern）**：反复出现的 bug 形态。例如，Milvus 历史上多次出现 "REST API v2 接受空字符串参数" 类 bug（#50018 及相关），这成为攻击生成的高优先级方向。
2. **文档化 by-design 行为**：维护者明确判定为 by-design 的边界。例如，weaviate 的 `ef=-1` 是 documented sentinel（表示"自动选择 ef"），不是非法值。把这些录入 Threat Model 可避免流水线反复产出"ef=-1 被接受"的假阳性候选。
3. **维护者认知盲点（cognitive blindspot）**：历史上**反复被外部用户报告但被维护者判定为 by-design** 的行为。这是最有价值的一类——它预测了"哪些看似 bug 的报告实际是浪费维护者时间"。例如，Milvus 的"search on unloaded collection returns code=0"在 #50305/#50319 等多个 issue 中被反复报告，但维护者判定为 by-design；这类盲点一旦录入 Threat Model，下游 Judge 与 Dev-Reviewer 就能在维护者回应前主动反证。

#### 3.1.2 双重注入

Threat Model 同时注入两个下游环节（上图标 b 和 c）：

- **注入 Attack Agents（标 b）**：作为攻击生成的"提示词地图"，让攻击优先朝历史缺陷模式方向倾斜，提高 candidate 的 recall。
- **注入 Judge 与 Dev-Reviewer（标 c）**：作为判定的"反证词典"，让 Judge 在投票时主动核对"这个候选是不是命中了某个 by-design / cognitive blindspot"。这一注入是 §3.4 dev-reviewer 反证能力的来源——没有它，dev-reviewer 只能凭通用 LLM 知识反证，错失目标系统特定的 by-design 行为。

#### 3.1.3 与既有工作的对比

既有 LLM 测试工具多用**静态提示**或**通用 RAG 检索**（如 CodaMosa、AutoGRML）。Threat Model 与它们的关键差异：
- 静态提示不知道目标系统的 by-design 行为，会反复产出已知 wontfix 的候选；
- 通用 RAG 检索按语义相似度返回文档片段，**不区分"这是 bug"和"这是 by-design 注释"**；
- Threat Model 显式区分这两类，且把认知盲点作为一等公民，使反证能在维护者回应**之前**完成。

### 3.2 Attack Agents（候选生成）

Attack Agents 把 Threat Model + contract 转成具体的攻击脚本，在 Docker 沙箱里执行，产出**候选缺陷**。每个候选的形态是 `(endpoint, illegal_param, observed_behavior, contract_clause_violated)`。

#### 3.2.1 三类攻击 Agent

按 v2.0 的四型缺陷分类（§1.8 贡献 1），TestVDB 配置三类攻击 Agent：

| Agent | 攻击方向 | 对应缺陷类型 | 示例攻击 |
|---|---|---|---|
| **attack-boundary** | 参数边界违规 | Type-1 非法成功 | `nprobe=0`, `ef=-1`, `dimension=4097`, `limit=0`, int64 上界 |
| **attack-semantic** | 类型/语义混淆 | Type-1（语义形态）+ Type-2 诊断 | 字符串传 int 字段、空向量、null filter |
| **attack-state** | 状态/序列违规 | Type-3 稳定性 + Type-4 状态/逻辑 | 未 loaded collection 上 search、并发 rename + create、upsert 在 autoID=true 时传 id |

三类 Agent 共享同一个 contract（断言层），但**生成策略不同**——boundary 用边界值表 + 等价类划分，semantic 用类型混淆矩阵 + LLM 生成对抗样本，state 用状态机遍历 + 并发序列。

#### 3.2.2 contract 作为断言来源

contract 来自目标 VDBMS 的官方文档（由 `contract-formalizer` Agent 从 OpenAPI / Markdown 提炼为结构化断言）。每条断言形如 `(endpoint, parameter, constraint, severity)`，例如：

```
(POST /collections, "shardsNum", "int > 0 and <= 32", HIGH)
(POST /collections, "metricType", "in {COSINE, L2, IP}", MEDIUM)
```

contract 是断言层，不是真相层——它会被 Threat Model 中的 by-design / cognitive blindspot **覆盖**（§3.1.2）。这是 contract-truth separation 在生成阶段的体现：Attack Agents **同时**遵守 contract 与 Threat Model 的覆盖，避免反复产出已知 wontfix 的候选。

#### 3.2.3 Docker 沙箱执行

每个攻击脚本在独立的 Docker 容器里跑（`docker-executor` Agent），目标 VDBMS 的版本精确匹配用户指定（不允许用缓存的近似版本替代——这是生产环境约束）。脚本输出 `(request, response, container_log)`，由后续 Judge 审阅。

#### 3.2.4 L1 机械闸门（设计存在，Check 库待扩展）

TestVDB 的 pipeline 在 EXECUTION 与 DEBATE_S2 之间设有 `VERIFY_LIVE` 阶段，包含 **L1 机械闸门**（`scripts/verify_live_l1.py`，零 LLM）+ **L2 语义闸门**（`verify-live-l2` Agent）的双层设计。设计意图是 L1 纯脚本覆盖约 90% 历史假阳性模式（如 HTTP 404 与 DEFECT_FOUND 自相矛盾、脚本从未创建所测的 index、`transaction is aborted` 连接污染等 PF 形态），L2 轻量 Agent 覆盖剩余约 10% 语义微妙情况。

**诚实说明**：当前 L1 的 12 个 Check 类是 v2.0 时代为 pgvector/Postgres 设计的（如 `PostgresAbortedCheck` 检测 "current transaction is aborted"、`FloatFormatCheck` 检测 Postgres `::text` CAST、`VECTOR_TYPE_DIMS` 用 pgvector 类型），对 Milvus/Qdrant/Weaviate/Chroma 等非 Postgres 库匹配度低。在本工作的 5 库实测中，L1 阶段未产出有效过滤（`verify_live_l1.json` 候选数为 0）。**向量库 native 的 Check 扩展**（如 milvus code=0+空结果、qdrant 404+SUCCESS 矛盾检测）**列为 §6 future work**。当前 PF 形态的实际过滤由 §3.4 Dev-Reviewer 兜底完成。

### 3.3 4-Judge 辩论（多视角反证）

Debate-Confirmed 是反证链的第一个收敛点。4-Judge 辩论让 4 个独立的 LLM judge 从四个正交视角各自投票，任一视角反对都阻止候选晋级。

#### 3.3.1 四个 Judge

| Judge | 评判什么 | 反证什么 |
|---|---|---|
| **judge-evidence** | 攻击脚本的实际响应**是否真的**违反了 contract | 反证"脚本/工具自身有 bug 误判响应" |
| **judge-severity** | 违规的严重性（HIGH/MEDIUM/LOW）是否值得报告 | 反证"轻微到不值得占用维护者时间" |
| **judge-novelty** | 是否与已知 issue / Threat Model 重合（5 级标注）| 反证"已知缺陷或 by-design"——但**不 kill**，只标注（Novelty Gate 才做最终 kill）|
| **judge-doc** | 是否有文档证据支撑 contract 断言 | 反证"contract 本身含糊或被误读"——这是 contract-truth separation 在辩论层的入口 |

四个 Judge 独立投票，最终聚合（`stage2_aggregation`）决定是否晋级为 Debate-Confirmed。这一层用便宜的方法（LLM 推理）从 ~1834 个候选筛到 ~33 个，**精度低（12.9%，§4 RQ3）但 recall 高**——这正是漏斗设计要的。

#### 3.3.2 辩论不解决 contract 错误

4-Judge 辩论**不能反标 contract**——它只判断"contract 是不是被违反了"。如果 contract 本身错了（例如文档说"必须 >0"但实际 -1 是 documented sentinel），judge-doc 会标"contract 含糊"但不会主动反标。"contract 反标"以 Dev-Reviewer 的 `root_cause` 分类（contract_misread / contract_formalizer_hallucination / approximate_by_design）落地，回写 `experience_handoff.json.rejection_patterns` 指导下轮 attack 改进（见 §3.4.2）。

### 3.4 Dev-Reviewer 反证（workhorse）

Dev-Reviewer（`dev-reviewer` Agent）是 TestVDB 的核心技术贡献（§1.8 贡献 3）。它模拟目标 VDBMS 的维护者，对每个 Debate-Confirmed 候选独立反证，**是"是否真缺陷"的唯一出口**。

#### 3.4.1 反证流程

每个 Debate-Confirmed 候选经过：

1. **干净复现（clean repro）**：抛开 Attack Agent 的原始脚本，Dev-Reviewer **重新构造最小复现脚本**，在 Docker 沙箱里跑。这一步直接反证"是不是 Attack Agent 脚本自身的工具 bug"。例如 §4 case study：`state_001_count_consistency` 候选声称 Milvus 在 autoID=true 时返回 rowCount=0 是 bug；Dev-Reviewer 重构脚本时发现**原始脚本违反了 autoID 约束（在 autoID=true 时传了显式 id），导致 insert 失败、rowCount=0 是正确行为**——候选被反证为 FALSE_POSITIVE，root_cause = `request_param_typo`。
2. **假设审计（assumption audit）**：Dev-Reviewer 列出候选隐含的所有假设（"假设 autoID 不影响 insert"、"假设 collection 已 loaded"），逐一在源码或文档里核对。
3. **源码锚定（source-grounded）**：Dev-Reviewer 阅读目标 VDBMS 的源码（用 grep + 阅读关键函数），找出实际行为与候选断言的不一致。例如，候选说"`nprobe=0` 应被拒绝"，Dev-Reviewer 在 Milvus 源码里搜 nprobe 校验逻辑，发现确实缺失 → 确认；或者发现校验在 v2.6.19 已加 → 反证为"already fixed"。
4. **Threat Model 核对**：Dev-Reviewer 拿候选对比 Threat Model 的 by-design 行为与认知盲点（§3.1），命中即反证。

#### 3.4.2 输出与影响

Dev-Reviewer 输出结构化 verdict：

```json
{
  "defect_id": "state_001_count_consistency",
  "verdict": "FALSE_POSITIVE",
  "root_cause_if_fp": "request_param_typo",
  "steps": { "clean_repro": {...}, "assumption_audit": {...} },
  "severity_after_review": null,
  "confidence": 0.92,
  "rationale": "..."
}
```

Dev-Reviewer 的反证在 §4 RQ3 实测中剔除了 **80.6%** 的 Debate-Confirmed 候选（milvus v2.6.19，31 进 4 出）。这是漏斗里**单个层级贡献最大**的反证。

#### 3.4.3 为什么 Dev-Reviewer 有效

Dev-Reviewer 有效的关键不在 LLM 本身，而在 **contract-truth separation**：
- Dev-Reviewer **不信任 Debate-Confirmed 的隐含假设**，把它当成新的断言层，要求源码与 Docker 实测作为真相层来反证；
- 它**显式调用 Threat Model**，因此能用目标系统特定的 by-design 行为反证，而不是只用通用 LLM 知识；
- 它**重新构造脚本**，因此能发现 Attack Agent 脚本自身的工具 bug（state_001 案例的 root_cause = request_param_typo 就是这一类）。

这三条加起来让 Dev-Reviewer 成为"维护者代理"——它做的事和真实维护者收到 issue 后做的事一样（读源码 + 重构 MRE + 核对 by-design），只是在维护者回应之前。

#### 3.4.4 PF 形态的反证兜底

v2.0 把 Precondition Failure（PF，脚本前置条件未满足——如搜不存在的 collection、数据未注入、索引未建）列为独立类目 Type-2.PF。TestVDB 删除了这一类目，因为 PF 本质是**脚本 bug 不是 DB bug**，提交给维护者会被 wontfix。PF 的过滤在架构上有两层设计（§3.2.4 的 L1 机械闸门 + L2 语义闸门），但如 §3.2.4 所述，当前 L1 的 Check 库是 pgvector 风味，对 5 个非 Postgres 库未实际生效。

**实际的 PF 过滤由 Dev-Reviewer 兜底**。Dev-Reviewer 的 clean repro 步骤（§3.4.1 第 1 步）天然识别 PF 形态——它抛开原脚本重构 MRE 时，会暴露"原脚本假设了未满足的前置条件"。§4.5.2 的 state_001 案例就是典型 PF：原脚本声称 "Milvus 在 autoID=true 时 rowCount=0 是 bug"，Dev-Reviewer 重构时发现**脚本违反 autoID 约束在先（在 autoID=true 时传了显式 id），insert 失败导致 rowCount=0 是正确行为**——root_cause = `request_param_typo`，正是 PF 形态（脚本前置条件违反）。

**PF 边界形态**（真 bug 伪装成 PF）仍归 Type 2/3：
- PF + 500/crash（合法请求触发 5xx）→ **Type 3 Runtime Failure**
- PF + stack trace 泄露内部类型 → **Type 2 Poor Diagnostics**
- PF + 静默接受未就绪状态 → **Type 1 Illegal Success**

这一分流让 TestVDB 既不漏 PF 边界里的真 bug，又不污染提交队列。

### 3.5 Novelty Gate（双层查重）

Dev-Reviewer 通过的候选进入 Novelty Gate（`scripts/novelty_gate.py`），做最后一道反证：是不是已知 / 已覆盖 / 已修复 / by-design。这是 contract-truth separation 在查重层的体现——**已知的 by-design 与已覆盖的 PR 都是真相层**，可反标候选。

#### 3.5.1 双层架构

| 层 | 数据源 | 用途 |
|---|---|---|
| **L1 Consumer** | Threat Model + 本地语料（含自家历史 issue 草稿存档）| 快速过滤：命中威胁模型的 by-design 行为或自家曾报过的 dup |
| **L2 Corrector** | GitHub Search API（精确到 PR / commit）| 精确反证：命中覆盖该参数校验的 open/merged PR |

L1 便宜（本地查询），L2 贵（API 限流）。L1 命中即可决断，L1 模糊时升级 L2。

#### 3.5.2 六级分级

Novelty Gate 输出六级：

| 分级 | 含义 | 处理 |
|---|---|---|
| **NOVEL** | 无已知命中 | 升级为 Gate-Endorsed，进入可提交列表 |
| **KNOWN_OPEN** | 精确命中某个 open issue | 内部存档，不提交 |
| **COVERED_BY_PR** | 命中覆盖该参数校验的 PR | 内部存档，不提交 |
| **BY_DESIGN** | 源码/文档显示"非法值"实际合法 | 内部存档，不提交（与 KNOWN_OPEN / COVERED_BY_PR 同级）|
| **POSSIBLY_FIXED** | 命中已 merged PR，需复验当前版本 | 标记，进入 Dev-Reviewer 重测队列 |
| **UNVERIFIED** | 查询失败（限流/断网） | 不背书，但不 kill——fail-closed 不丢数据 |

**关键设计**：仅 NOVEL 进可提交列表，但 **fail-closed 不丢数据**——UNVERIFIED 不 kill 候选，只不背书。"学习"机制在 Dev-Reviewer（§3.4.2）：`root_cause` 分类回写 `experience_handoff.json.rejection_patterns`，下轮 Attack Agent 据此改进断言质量。**注**：直接反标 `structured_contract.json`（标 stale / patch 修正）作为 future work——见 [ADR-0001](TestVDB/docs/adr/0001-novelty-gate-over-judge-recall.md)（原计划实现，但因 Phase 0 重生成覆盖 + 无实证需求而暂缓）。

#### 3.5.3 Gate 不产生"提交许可"

Gate-Endorsed 是**可提交背书**，不是**提交许可**。提交始终是人工动作（§1.6）。这一约束让 Gate 的 fail-closed 不丢数据——查不清只是不背书，缺陷报告仍生成供人工核。

### 3.6 章节小结

TestVDB 的方法层把 contract-truth separation 落实为四层反证闸门，每层用更贵的真相源反证更便宜的断言：3.2 用 Docker 实测反证 contract 断言；3.3 用四视角辩论反证候选的完整性与重要性；3.4 用源码 + 沙箱复现反证 Debate-Confirmed；3.5 用历史与维护者权威反证 Dev-Endorsed。**任何一层单独都不够**——§4 RQ3 将给出每层 precision 的实测，显示 Dev-Reviewer 单层剔除 80.6% 假阳性、全链 precision 72.7% 的 5.6 倍累积提升。Threat Model（§3.1）作为唯一原创增量，让反证能在维护者回应**之前**完成，是 contract-truth separation 在向量库合规测试场景下的关键工程化。

---

## 4. 评估（草稿，待扩）

### 4.1 实验设置

**被测系统**：5 个主流 VDBMS——Milvus、Qdrant、Weaviate（专用向量库）+ Meilisearch、Chroma（搜索引擎扩展）。其中 Milvus 和 Qdrant 为主战场（深度测试），其余为探索性测试。每个系统锁定具体版本（容器版本精确匹配用户指定，不允许近似替代）。

**执行环境**：Docker 沙箱隔离部署，多轮自适应迭代。

**Ground Truth 双层设计**：
- **Tier 1（强真值，小集合）**：维护者反馈。对**提交层**算 precision = acknowledged / (acknowledged + by_design + rejected) = 32/48 = 66.7%，或排除 wontfix = 32/44 = 72.7%。
- **Tier 2（弱真值，大集合）**：Dev-Reviewer verdict。对**Stage 2 输出**算 precision = confirmed / reviewed = 4/31 = 12.9%。
- **跨层贡献**：每层的 FP 拒绝率（Dev-Reviewer = 80.6%）。

### 4.2 RQ1：缺陷检测能力

TestVDB 在 5 个 VDBMS 上发现 108 个先前未知缺陷，提交后维护者明确承认 **32 个（24 fixed + 8 accepted）**，12 个被标 by-design，4 个 wontfix/not_planned。

| DB | submitted | fixed | accepted | by-design |
|---|---|---|---|---|
| Milvus | 49 | 12 | 8 | 12 |
| Qdrant | 26 | 11 | 0 | 0 |
| Weaviate | 29 | 1 | 0 | 0 |
| Meilisearch | 3 | 0 | 0 | 0 |
| Chroma | 1 | 0 | 0 | 0 |
| **Total** | **108** | **24** | **8** | **12** |

对比 DDLCheck（VLDB 2025）的 "34 submitted / 29 confirmed / 9 fixed"——TestVDB 数量级相当甚至更优（24 fixed > 9 fixed）。

### 4.3 RQ2：Contract 反标频率（验证 insight）

总反标事件 ~23 次：
- Pipeline 内：11 次（final_verdict 中 BY_DESIGN + COVERED_BY_PR + KNOWN_OPEN）
- 提交层：12 次（维护者标 by-design）

反标率 ~30%（每 3-4 个候选就有 1 个被真相层反标）。**这证明 truth layer 不是装饰，是做了实事**。

BY_DESIGN 案例展示：
- Milvus #47767：empty query vector accepted（实为 documented 行为）
- Milvus #49928：maxDimension=32768（实为文档化上限）

### 4.4 RQ3：跨层 Precision 消融

**漏斗**（Milvus v2.6.19）：1834 raw → 33 Stage-2-confirmed → 31 Dev-reviewed → 4 confirmed。

| 层 | precision | 备注 |
|---|---|---|
| Stage 2 辩论（单独）| **12.9%** | 4/31，vs Dev-Reviewer verdict |
| Dev-Reviewer 单层贡献 | **抓 80.6% FP** | 25/31 FP 被剔除 |
| 全链 | **72.7%** | 32/(32+12)，vs maintainer |
| **5.6× precision 提升** | | from Stage 2 单层到全链 |

**限制**：跨库 RQ3 数据只 milvus 单库（其他库待补 dev_review 数据）。

### 4.5 Case Studies

#### 4.5.1 Hook 案例：cosine > 1.0 for identical vectors

相同向量的 cosine 距离 ∈ [0, 2]，但 TestVDB 发现 Milvus 和 Qdrant 都返回过 > 1.0 的距离值（数学上不可能）。该缺陷在 Milvus [#49059] 已修复，在 Qdrant [#8688] 已确认。这是一个数学不可能的事件被工具自动发现的有力案例。

#### 4.5.2 机制案例：Dev-Reviewer 反证 state_001 contract_misread

候选 `state_001_count_consistency` 声称 Milvus 在 autoID=true 时返回 rowCount=0 是 bug。Stage 2 辩论判为 CONFIRMED。Dev-Reviewer 重构脚本时发现**原始脚本违反了 autoID 约束（在 autoID=true 时传了显式 id），导致 insert 失败、rowCount=0 是正确行为**——候选被反证为 FALSE_POSITIVE，root_cause = `request_param_typo`。这证明 Dev-Reviewer 的 clean repro 步骤在干活。

### 4.6 RQ4：对比现有方法

| 现有方法 | 适用性 | 原因 |
|---|---|---|
| NoREC / DQP / Radar | 结构不适用 | 针对关系库 SELECT 优化，要求等价 SQL 变换，VDBMS API 不暴露 |
| 纯 LLM-as-oracle | 等价于 Stage 2 单层 | precision = 12.9%，不可接受 |
| 传统 fuzzing | 无 oracle | 不理解 contract，无法判断"应否被拒" |
| 既有 VDB benchmark | 测性能非正确性 | vector-db-benchmark 等只测 QPS / recall，不测合规 |

**主张**：vector DB API compliance 是新赛道，本工作是首个系统方法。

### 4.7 Threats to Validity

- **LLM 非确定性**：多 judge + 多轮迭代缓解
- **标注偏差**：用维护者反馈作弱 ground truth
- **跨库 RQ3 数据只 milvus 单库**：承认 limitation，待补
- **Weaviate 22 open issue 仅 community 标签**：维护者未分诊；用硬口径 32 acknowledged 报数，软口径 63 labeled-bug 附录
- **重复提交**（milvus #50305-18 vs #50319+）：论文统计已去重

---

## 5. 相关工作（草稿，待扩）

### 5.1 关系库测试

NoREC [Rigger2020]（differential testing for DBMS）、DQP [Ba2024]、Radar [Song2025]、Troc [Sun2020] —— 均针对 SELECT 优化 bug，结构上不适用于 VDBMS API。

### 5.2 LLM 驱动测试

[arXiv:2505.02012]（LLM 合成 SQL 测试）、CodaMosa、AutoGRML —— 聚焦代码生成 + 执行反馈，无显式维护者代理反证层。

### 5.3 VDBMS 测试与评测

[arXiv:2502.20812]（VDBMS 测试路线图）、[arXiv:2506.02617]（1671 VDBMS bug 实证）、vector-db-benchmark（性能评测）—— 路线图与统计，无工具实时发现。

### 5.4 多 Agent 系统

[ref 待补] —— 与 LLM 多 Agent 框架的关系，TestVDB 的反证链设计可迁移到其他需要可信判定的 agent 系统。

---

## 6. 结论与未来工作

我们提出 **contract-truth separation** 作为向量库合规测试的可信 oracle 设计原则，并把它落实为 TestVDB 的四层反证 oracle 链。核心实验结论：Dev-Reviewer 反证层独自剔除 80.6% 假阳性，把全链 precision 从 12.9% 提升到 72.7%（5.6 倍）。我们在 5 个 VDBMS 上发现 108 个先前未知缺陷，32 个被维护者明确承认。

**未来工作**：
- 跨库补 Dev-Reviewer 数据（让 RQ3 不只 milvus 单库）
- Type-4 语义缺陷检测（需更扎实的语义 oracle）
- 自动 patch 生成（基于 Dev-Reviewer 的源码锚定）
- 把 contract-truth separation 迁移到其他需要可信 LLM 判定的领域（agent 系统、代码评审）

---

## 附录 A · PPT 24-Slide Outline（与 [paper-draft-v3.pptx](paper-draft-v3.pptx) 对应）

### 第一幕 · 背景与问题（Slides 1-7）

| # | 标题 | 要点 |
|---|---|---|
| **1** | Title | TestVDB: ...via Contract-Truth Separation |
| **2** | VDBMS are critical infrastructure | 1671 VDBMS bug [arXiv:2506.02617] |
| **3** | VDBMS fundamentally different | 5 维差异表 |
| **4** | Type 1: API Compliance | nprobe=0 / shardsNum=-1 / cosine 截断 |
| **5** | Type 2/3: Diagnostic + Stability | qdrant #9525 serde / #9045 panic |
| **6** | Type 4: State/Logic | INSERT 3 rows COUNT 返 2 / cosine > 1.0 |

### 第二幕 · Gap + Insight（Slides 7-9）

| # | 标题 | 要点 |
|---|---|---|
| **7** | Existing approaches fail | NoREC/DQP/Radar 不适用 / LLM 无反证 / fuzzing 无 oracle |
| **8** | Insight 1: assertion layer unreliable | ~30% contract 反标率 |
| **9** | Insight 2: Contract-Truth separation | 分层 + 反证 + 累积可信度 |

### 第三幕 · 方法（Slides 10-14）

| # | 标题 |
|---|---|
| **10** | Offline Intelligence Layer（/mine + /intel + /contract）|
| **11** | Online Attack Pipeline Overview |
| **12** | Threat Model（三类情报 + 双重注入）|
| **13** | 4-Judge 辩论 + Dev-Reviewer 反证 |
| **14** | Novelty Gate 双层查重 |

### 第四幕 · 评估（Slides 15-21）

| # | 标题 |
|---|---|
| **15** | RQ Overview（4 个 RQ）|
| **16** | Setup（5 库分层）|
| **17** | RQ1: 108 submitted / 32 acknowledged |
| **18** | RQ2: 30% contract 反标率 |
| **19** | RQ3: 跨层 precision（12.9% → 72.7%）|
| **20** | Case Studies（cosine > 1.0 + state_001）|
| **21** | RQ4: 对比现有方法 |

### 第五幕 · 结论（Slides 22-24）

| # | 标题 |
|---|---|
| **22** | Threats to Validity |
| **23** | Conclusion |
| **24** | Future Work |

---

## 附录 B · 写作备忘（非论文内容，给作者参考）

### B.1 待确认判断点

1. **§1.1 引用**：[ref] 占位需补 RAG / 语义检索经典论文（Lewis 2008 RAG + kNN 文献）
2. **§1.2 issue 号**：用了 #49823 / #11397 / #9017 / #9525 / #9045 / #49059 / #8688。有更想推的明星 issue 可替换
3. **§1.5 术语**：lock "contract-truth separation"
4. **§1.6 threat model 篇幅**：cognitive blindspot 是否单独成亮点（已纳入贡献 4）
5. **§1.8 工件开源**：已确定真开源，URL 待 camera-ready 公开

### B.2 已知短板（论文写作要正视）

- **跨库 RQ3 数据只 milvus 单库**：§4.4 只能写 "on Milvus v2.6.19"
- **Type-4 仅 2 个案例**：cosine > 1.0 是 by-product，需在 §1.2 末尾明确
- **Weaviate 22 open 未分诊**：分布表会暴露维护者响应冷淡，§4.2 已诚实写

### B.3 已修正的关键事实

- **TestVDB 实际 4 型分类**（非 v2.0 五型）：Type-2.PF 已删（L1 机械闸门 REFUTE），Type 4 是 State/Logic 不是 precision。详见 memory `testvdb-defect-taxonomy-actual`
- **yihui504 issue 统计**：108 issue / 32 维护者承认 / 12 BY_DESIGN / pgvector 空白。详见 memory `yihui504-vector-db-issue-submissions`
- **AIDBQC_flow → TestVDB 演化**：原始单体 LangGraph → Claude Code 插件。详见 memory `aidbqc-to-testvdb-evolution`

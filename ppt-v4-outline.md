# TestVDB PPT V4 大纲（问题导向式，24 页）

> **基础**：[paper-narrative-skeleton.md](paper-narrative-skeleton.md)（叙事骨架定稿）
> **取代**：[ppt-draft-v3-archived.pptx](ppt-draft-v3-archived.pptx)（旧 V3 已存档）
> **结构**：开场（1-2）→ 问题立 + roadmap（3-5）→ 5 步链条（6-13）→ 评估（14-20）→ 对比结论（21-24）
> **核心**：第 5 页骨架图是全篇 roadmap；第 8-10 页是核心反转（insight 高潮）

---

## 第一幕 · 开场（Slides 1-2）

### Slide 1 · Title
- **标题**：TestVDB: Detecting API Compliance Defects in Vector DBMSs via Contract-Truth Separation
- **副标题**：When the oracle itself may be wrong —代理维护者权威作为语义真相层
- 作者 / 机构 / 会议候选（VLDB/SIGMOD/ICSE）

### Slide 2 · 动机：VDBMS 支撑关键应用，合规缺陷普遍
- VDBMS 支撑 RAG / 推荐 / agentic workflow（1671 bug 实证 [arXiv:2506.02617]）
- **API 合规缺陷**：VDBMS 静默接受文档禁止的输入
- 代表性案例（2 个，配代码片段）：
  - `nprobe=0` 接受（Milvus）→ 静默 recall=0
  - `shardsNum=-1` 静默归一化为 1（Weaviate #11397）→ 查询语义被破坏
- **系统身份**：**边界/校验合规检测器**（兼诊断/状态）——36 TP 实测：边界 75% / 诊断 8% / 状态 6% / 崩溃 3% / 结果正确性 8%
- **目标缺陷类型**（主参考 [arXiv:2502.20812] symptom 分类 + [arXiv:2506.02617] pattern 词汇，详见 §2）：
  - Type 1 边界违反（**核心目标**，占产出 75%，boundary attack）
  - Type 2 诊断质量（延伸，semantic attack）
  - Type 4 状态/逻辑不一致（延伸，含 cosine>1.0，state attack）
  - Type 3 合法输入崩溃（**非目标**，L1 前置过滤——与 vdbfuzz 设计性互补）
- **后果**：不崩，但破坏查询语义、降低 recall、暴露攻击面

---

## 第二幕 · 问题立 + Roadmap（Slides 3-5）

### Slide 3 · 锚点 0：vdbfuzz Discussion 列出的两条 future work
- vdbfuzz (ICSE'26) 用 **crash oracle** 在 8 个 VDBMS 上挖出 19 个 crash bug
- **但它的 Discussion 主动承认两条 future work**（大字引用）：
  > 1. *"future work should explore the development of an oracle for evaluating the correctness of vector search results, as the inherent fuzziness ... makes traditional differential testing unsuitable"*
  > 2. *"Another promising direction is the generation of more diverse and comprehensive seed inputs ... LLMs could play a significant role in generating diverse API interactions ... methods must be devised to ensure that LLMs can stay updated with the latest syntax and functionalities"*
- **TestVDB 的回应（精确口径，2026-07-09 修订）**：
  - 生成面（attack agents + knowledge-extractor）← **方向 ②**（LLM 生成 diverse interactions + 爬文档保持更新）
  - 判定面（CTS + dev-reviewer）= **contract oracle，把可检测边界从 crash 扩展到 API 合规子集（超越 crash）**；**不声称填方向 ①**（结果正确性 oracle：ANN 精度/ranking 仍 open，见 [arXiv:2502.20812]）
- **叙事递进**：开题从方向 ② 起步（LLM 生成）→ 发现非崩溃缺陷的判定才是核心 → 判定面是"超越 crash 的 contract oracle"（非"结果正确性 oracle"）

### Slide 4 · 问题 1：排除法 → LLM（总 gap）
- 合规缺陷没有可观察信号，oracle 该用什么？
- **排除法表**（直接放 slide）：

| 候选 oracle | 为什么不行 |
|---|---|
| crash（vdbfuzz）| 合规缺陷不崩 |
| PoC 复现（Anthropic harness）| 无可观察的失效信号（如 crash/异常退出）|
| 差分测试（NoREC）| VDBMS 无可作差分基准的参考实现 |
| 等价变换（Radar）| VDBMS 无可等价变换的查询形态 |
| **LLM** | **无参考实现前提下，唯一能对语义合规做弹性判定的候选** → 但不可靠 |

- **总 gap（红字）**：LLM 在【生成】和【判定】两个角色都不可靠
- **角色**：一次性回应所有"为什么不直接用 X"

### Slide 5 · Roadmap：5 步链条骨架图 ⭐ 重点页
- **视觉**：纵向链条，每个节点是"问题 | 解"双色块，★ 标在问题 3
- threat model 用一条**贯穿四层的竖线**标出（视觉立住"贯穿各层的经验先验"身份）
- 配文一句话：
  > 每个组件由前一个 gap 论证；所有"问题→解"都是 contract-truth separation 在不同层的实例化

**图内容**（见 [paper-narrative-skeleton.md §5](paper-narrative-skeleton.md) 骨架表）：
```
[锚点 0] vdbfuzz future work
   ↓
问题 1 → LLM（排除法）         总 gap: LLM 两角色不可靠
   ↓ 拆面
问题 2 → threat model          生成面: 方向平庸
   ↓
问题 3 ★ → dev-reviewer + CTS   判定面: contract 可能错  [核心反转]
   ↓
问题 4 → 三层反证锚点           dev-reviewer 凭何可信
   ↓
问题 5 → 双层 novelty gate      查重
   ↓
[收束] threat model 横跨四层
```
- **角色**：让读者一开始就看到全貌；后续 8 页按此图逐步展开

---

## 第三幕 · 5 步链条（Slides 6-13）

### Slide 6 · 问题 2：LLM 生成缺乏先验 + 经济学
- 单给 contract，LLM 倾向生成**常见边界测试**（`nprobe=0`、`limit=0` 这类表面值）
- 真正的 bug 藏在 **by-design 边界附近的语义微妙处**（如 `ef=-1` 是 sentinel 还是非法？）
- **经济学对比**（柱状图）：
  - vdbfuzz：120 min → 10M+ test cases（覆盖率导向）
  - TestVDB：单轮 → ~1834 候选（LLM 生成成本远高于 fuzzing，语义攻击 vs 覆盖率导向）
- **结论**：覆盖率不再是好目标，**precision-per-generation** 才是

### Slide 7 · 解 2：Threat Model（⚠️ exploratory pilot——ablation 降级，详见 skeleton §12）
- 从目标 VDBMS **历史 issue / PR / commit** 提炼三类先验信息：
  1. **bug pattern**（反复出现的缺陷形态）
  2. **documented by-design**（`ef=-1` 是 sentinel）
  3. **cognitive blindspot**（历史上反复被报但被判 by-design）
- 注入 attack agents → 引导生成到历史上反复出现的缺陷方向
- **借鉴边界**（小字）：借 Anthropic threat model 的**架构位置**；替换其内容（focus_areas → 认知盲点）和动机（scope → 生成经济性）

### Slide 8 · 问题 3：contract 本身可能错 ⭐ 核心反转开始
- 即便 LLM 判定正确，**它判的 contract 可能本身是错的**
- 实测 **30% contract 反标率**（约每 3 个候选中有 1 个被真相层反标）
- contract 不可靠的两种根因：
  - **文档化 by-design**：Milvus #47767 empty query vector accepted（documented 行为）；Weaviate `ef=-1`（sentinel，不是非法值）
  - **契约幻觉**：#50354 complexity requirements 源自 constant.go——formalizer 造的约束，源码里没有；LLM 既生成契约又判定合规 → 幻觉被自我确认
- **结论**：contract 是**断言**不是**真相**——这是 paper 的核心洞察入口

### Slide 9 · 第二层排除法 → 维护者权威
- contract 不可靠时，谁是真相源？
- **第二层排除法表**：

| 候选真相源 | 为什么不行 |
|---|---|
| 另一个 LLM（多 judge）| 同源盲点 |
| PoC 复现（Anthropic）| 合规缺陷无可观察的失效信号 |
| **维护者权威**（源码 + PR + by-design + 历史）| **唯一能权威回答"应否被拒"** → 但稀缺 |

- 维护者权威稀缺：维护者不可能实时回应每个候选
- **必须代理** → dev-reviewer

### Slide 10 · Insight：Contract-Truth Separation
- **Contract-Truth Separation**（大字定义）：
  > 断言层（contract / threat model / LLM 判定）与真相层（维护者权威代理）分离，用后者逐级反证前者
- 落地为 **dev-reviewer Agent**：代理维护者，读源码 + Docker 沙箱复现
- 与既有工作的分界（一句话）：
  - vdbfuzz：contract 当真相（违反 = crash bug）
  - Anthropic：crash 当真相（PoC 复现）
  - **TestVDB：contract 是断言，维护者权威才是真相**
- **角色**：立单一原则，使所有组件收敛到 CTS

### Slide 11 · 问题 4：dev-reviewer 凭何比 4-Judge 可信？
- dev-reviewer 与 4-judge 同为 LLM，差异在反证机制
- 答案：**三层"非 LLM"的反证锚点**：

| 锚点 | 反证什么 | 机制 |
|---|---|---|
| clean repro | attack agent 的工具 bug | 重构 MRE，反证脚本自身错 |
| source-grounded | **契约幻觉**（contract 是 LLM 造的）| 读源码锚定（grep + 关键函数），反证约束是否真实存在 |
| threat model 核对 | contract 误判 by-design | 查历史上的 by-design 行为 |

- 4-Judge 无独立反证锚点，主要依赖 LLM 推理 → precision 12.9%
- dev-reviewer 三层锚点 → 剔除 80.6% FP

### Slide 12 · 解 4 实测 + Case Study（state_001）
- state_001 案例（机制演示）：
  - 候选声称："Milvus autoID=true 时 rowCount=0 是 bug"
  - 4-Judge 判 CONFIRMED
  - dev-reviewer **重构 MRE** 发现：原脚本违反 autoID 约束（传了显式 id）→ insert 失败 → rowCount=0 是**正确行为**
  - root_cause = `request_param_typo`，反证为 FALSE_POSITIVE
- **结论**：clean repro 起实际作用——这是"维护者代理"的具体实例

### Slide 13 · 问题 5：双层 Novelty Gate
- dev-reviewer 通过的还可能是已知的 / 已覆盖的 / by-design
- **双层查重**：

| 层 | 数据源 | 用途 |
|---|---|---|
| L1 Consumer | threat model + 本地语料 | 快速过滤 by-design / 本地历史重复 |
| L2 Corrector | GitHub Search API | 精确反证（命中覆盖 PR）|

- 六级分级（NOVEL / KNOWN_OPEN / COVERED_BY_PR / BY_DESIGN / POSSIBLY_FIXED / UNVERIFIED）
- **关键设计**：仅 NOVEL 进可提交列表；**fail-closed 不丢数据**（UNVERIFIED 不 kill）
- 提交始终是人工动作（Gate 是背书，不是许可）

---

## 第四幕 · 评估（Slides 14-20）

### Slide 14 · RQ Overview
- **RQ1**：缺陷检测能力（111 issue / 36 承认）
- **RQ2**：Contract 反标频率（验证 insight，30%）
- **RQ3**：跨层 Precision 消融（12.9% → 69.2%，反证链有效？）
- **RQ4**：对比现有方法（vdbfuzz / Anthropic / NoREC）

### Slide 15 · Setup
- **5 库分层**：Milvus / Qdrant（主要测试对象）+ Weaviate / Meilisearch / Chroma（探索）
- Docker 沙箱隔离，多轮自适应迭代
- **Ground Truth 双层**：Tier 1 维护者反馈（强）/ Tier 2 dev-reviewer verdict（弱）

### Slide 16 · RQ1：111 缺陷，36 维护者承认
- 分库表：

| DB | submitted | fixed | accepted | by-design |
|---|---|---|---|---|
| Milvus | 49 | 12 | 8 | 12 |
| Qdrant | 26 | 11 | 0 | 0 |
| Weaviate | 29 | 1 | 0 | 0 |
| Meilisearch | 3 | 0 | 0 | 0 |
| Chroma | 1 | 0 | 0 | 0 |
| **Total** | **111** | **28** | **8** | **12** |

- 对比 DDLCheck (VLDB'25)：34 submitted / 29 confirmed / 9 fixed —— TestVDB 28 fixed，数量级相当

### Slide 17 · RQ2：30% Contract 反标率 + 契约幻觉（验证 insight）
- 总反标事件 ~23 次：
  - Pipeline 内：11 次（BY_DESIGN + COVERED_BY_PR + KNOWN_OPEN）
  - 提交层：12 次（维护者标 by-design）
- 反标率 ~30%——**证明 truth layer 起实际判定作用**
- **契约幻觉实例**（#50354）：formalizer 从 constant.go "提取" complexity requirements（源码无此约束）→ attack 测 → judge-doc 确认违规 → 只有 dev-reviewer source-grounded 反证才发现
- 这是 contract-truth separation 的可验证预测：如果 truth layer 不干活，反标率应接近 0

### Slide 18 · RQ3：跨层 Precision 消融 ⭐ 主结果
- 漏斗图（Milvus v2.6.19）：1834 raw → 33 Stage-2 → 31 dev-reviewed → 4 confirmed

| 层 | precision | 备注 |
|---|---|---|
| 4-Judge 辩论（单独）| **12.9%** | 4/31 |
| Dev-Reviewer 单层贡献 | **剔除 80.6% FP** | 25/31 FP 被剔除 |
| 全链 | **69.2%** | 36/(36+12+4) |
| **5.4× precision 提升** | | Stage-2 → 全链 |

- **限制**（诚实写）：跨库 RQ3 数据只 milvus 单库

### Slide 19 · Case 1：cosine 极值违反（双库复现）
- 相同向量的 cosine 应返回极值（distance=0 / similarity=1），但两系统均违反，形式不同：
  - **Milvus #49059**（已修复）：cosine **distance** >1.0（如 1.0000001192）——相同向量应=0，返回 >1.0 意味 similarity<0，对相同向量荒谬
  - **Qdrant #8688**（已确认）：cosine **similarity** >1.0——超出 [-1,1] 上界，数学不可能
- **价值**：工具自动发现极值违反，且在两独立系统中以不同形式复现
- 配图：距离/相似度分布直方图（显示越界 cluster）

### Slide 20 · Case 2：state_001（机制演示）
- 见 Slide 12 的 case，这里展开 dev-reviewer 的反证流程图：
  - clean repro → assumption audit → source-grounded → threat model 核对
- 输出结构化 verdict（JSON 片段）

---

## 第五幕 · 对比 + 结论（Slides 21-24）

### Slide 21 · RQ4：对比现有方法
- **对比表**：

| 方法 | 适用性 | 原因 |
|---|---|---|
| vdbfuzz (ICSE'26) | 互补 | 测 crash，TestVDB 测合规——oracle 不同 |
| Anthropic harness | 不适用 | PoC 复现要求可观察的失效信号 |
| NoREC / DQP / Radar | 查询结构不适用 | 要求 SQL 等价变换 |
| 纯 LLM-as-oracle | 等价于 Stage-2 单层 | precision = 12.9%，不可接受 |
| 传统 fuzzing | 无 oracle | 不理解 contract |

- **主张**：上述对比表明，VDBMS API 合规缺陷的检测此前无适用方法

### Slide 22 · Threats to Validity
- LLM 非确定性 → 多 judge + 多轮迭代缓解
- 标注偏差 → 维护者反馈作弱 ground truth
- 跨库 RQ3 数据只 milvus 单库 → 承认 limitation，列为 future work
- Weaviate 22 open 未分诊 → 用保守口径 36 acknowledged 报数

### Slide 23 · Conclusion
- 核心：**contract-truth separation** 作为可信 oracle 设计原则
- 实测：dev-reviewer 反证层独自剔除 80.6% FP，全链 precision 12.9% → 69.2%（5.4×）
- 发现：契约幻觉传播（LLM 造约束被自我确认），反证层是对抗机制
- 实证：5 库 111 缺陷，36 维护者承认（28 fixed + 8 accepted）；系统定位=**边界/校验合规检测器**

### Slide 24 · Future Work + 贡献
- **Future work**：
  - 跨库补 dev-reviewer 数据（让 RQ3 不只 milvus 单库）
  - 把 CTS 迁移到其他需要可信 LLM 判定的领域（代码评审、合规审计）
  - 自动 patch 生成（基于 dev-reviewer 的源码锚定）
- **6 条贡献**（缩略列表）：**首个 LLM 驱动的 VDBMS API 合规检测实现 + 大规模实证**（非"赛道界定"——赛道已被 [arXiv:2502.20812] 界定）/ 方法论 CTS / dev-reviewer 反证机制（三层锚点，TP recall 限制诚实标注）/ **契约幻觉传播发现**（12 BY_DESIGN 实锤：25% 提交被判"契约过严"；反证层是对抗机制）/ TM exploratory pilot / 实证 111 缺陷 + 工程开源

---

## 制作备注

### 视觉一致性
- **配色**：建议深色背景（学术风），accent 色标 ★ 核心反转
- **字体**：标题 sans-serif，代码 mono，引用 italic
- **图表**：Slide 5（骨架图）、Slide 6（经济学柱状图）、Slide 18（漏斗图）、Slide 19（距离直方图）是 4 个关键视觉

### 与旧 V3 的关键差异
- 旧 V3 按"组件介绍"组织（Slide 10-14 是组件）→ V4 按"问题→解链条"组织
- 旧 V3 没有 roadmap 骨架图 → V4 Slide 5 是加强点
- 旧 V3 的 insight 分散 → V4 集中在 Slide 8-10（核心反转三连）
- 旧 V3 借鉴边界模糊 → V4 Slide 7/21 精确引用 vdbfuzz §4.1 / Anthropic `/threat-model`

### 生成 .pptx 的下一步
确认大纲后，用 python-pptx 生成实际 .pptx（参考 2025-vldb-ddlcheck.pptx 的视觉风格）。

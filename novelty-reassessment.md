# Novelty Reassessment — 论文修订/重构的基础（活文档）

> 起点 2026-07-15。这是一份**活文档**：在四篇经典 + 文献威胁的 grilling 过程里持续追加。
> 最终用途：驱动论文（TestVDB）的修订，甚至重新构思。
> **铁律：区分证据等级。** ✅=原文摘要核实；🟡=搜索摘要/二手，待全文核实；❓=推测。
> 投稿：venue 未定（软目标 ISSTA 2027，~2027-01）。见 memory `paper-submission-status`。

---

## 0. 这份文档要回答的根本问题

**在"从文档推导 test oracle"这条已被 AGORA/SATORI/MASTOR 占据的研究线上，TestVDB 到底还剩什么 delta？够不够撑一篇？卖法要不要从"方法创新"转向"新领域实证 + 一个被命名的失败模式"？**

这个问题是 grilling 第 1 篇（Barr）跑到一半、被用户一句"后续有没有人做从文档推 oracle"逼出来的。下面是目前的全部认知。

---

## 1. Grilling 进度（四篇经典）

来源：用户读完我指定的四篇，逐篇讨论。

| # | 文献 | 对应 oracle taxonomy 的一格 | 状态 |
|---|---|---|---|
| 1 | Barr et al. 2015, *The Oracle Problem in Software Testing: A Survey* (ICST) | 框架本身（specified/derivable/implicit/none）| **进行中**——串讲到"从文档推 oracle"，引出文献威胁（§3）|
| 2 | Slutz 1998, *Massive Stochastic Testing of SQL* (VLDB) | differential（差分）| 待开始 |
| 3 | Chen et al. 2018, *Metamorphic Testing: A Review of Challenges and Opportunities* (CSUR) | implicit / metamorphic（蜕变）| 待开始 |
| 4 | Claessen & Hughes 2000, *QuickCheck* (ICFP) | property-based | 待开始 |

---

## 2. 从 Barr 串讲里沉淀的概念（已对齐）

**A. oracle 是否必须？**
- oracle = 判断"这次行为可不可接受"的谓词。能下判决 = 有某种 oracle（哪怕极弱）。
- **partial vs total**：total 对所有输入都能判；partial 只覆盖一个子集。Barr 的精确说法是"没有 full spec 时，去构造 partial oracle"，不是躺平。
- **crash 是退化的 implicit oracle**——正因为是它，fuzzing 只能找 crash，找不到不崩的错。metamorphic relation 也是堂堂正正的 partial/implicit oracle（修正早前"偷偷塞"的轻佻措辞）。
- **两件事别混**：①"没 oracle 就不能下判决"是定义层面的事实；②"oracle problem"是实践困境——需要 oracle 但常常没有好的/买得起的。我们站在 ② 这侧。

**B. Barr 早已点名"从文档推 oracle"——对我们是威胁。**
- ✅ Barr 原文：no full spec 时可构造 partial oracle，方法之一是"deriving oracular information from execution or **documentation**"。
- 推论：**"我们用 API 文档当 oracle 来源"作为一种来源类型，不新**。Barr 2015 已列。论文 related work 必须自己先 cite 这句点破，别留给审稿人。

**C. 我们 vs Barr 的认识论翻转（delta 的种子，但见 §4 被威胁）。**
- Barr：从文档推出来的 oracle = **答案**（拿去判决）。
- 我们：当 deriver 是 LLM，推出来的 oracle 是**会幻觉的假设**（contract hallucination propagation）；source-grounded falsification 拿源码去**证伪**它。
- 应然/实然之分：documentation = 应然（会错/幻觉）；source = 实然（事实）。源码**不是** Barr 说的 documentation 那一类。

---

## 3. 文献威胁：AGORA / SATORI / MASTOR 这条线（核心）

**一句话**：我们声称的几个机制卖点，被这条 2022→2026 的活跃线大量预置。我们 Related Work 现在零引用，是会被当场抓的死洞。

### 3.1 三篇核实摘要（✅ 来自原文摘要）

**AGORA+** — Alonso, Ernst, Segura, Ruiz-Cortés; *TOSEM* 2025.
- oracle：**invariants**（"output properties that should always hold"），通过分析 API **requests + responses** 动态学习预期行为。
- 机制：增强 **Daikon** 做动态 likely-invariant 检测；前端 **Beet** 把任意 OpenAPI spec + 一组请求/响应转成 Daikon 输入；**106 种**不变量类型；**PostmanAssertify** 把不变量转成可执行 JS 断言。
- 效果：**precision 80%**（20 个工业 API 的 25 个 operation）；检出 **48%** 系统植入错误；在 Amadeus/Deutschebahn/GitHub/Marvel/NYTimesBooks/YouTube 等 **发现 32 个 bug**，促成修复与文档更新。
- 关键：**依赖 OpenAPI 结构化规约 + 实际执行**；**不用 LLM**（Daikon 动态）。
- 🟡 搜索摘要称 AGORA+ 有"针对算术比较类 FP 的启发式"——**摘要里没提，待全文核实**。

**SATORI** — Alonso, Martin-Lopez, Segura, Bavota, Ruiz-Cortés; *ASE* 2025; arXiv 2508.16318.
- oracle：**黑盒、静态**，分析 **OpenAPI Specification**；用 **LLM** 推断预期行为，依据是 response fields 的**属性（名字 + 描述）**。
- 机制：PostmanAssertify 转 executable assertions。
- 效果：12 个工业 API 的 17 个 operation，每个 operation 可生成上百条有效 oracle；**F1 = 74.3%**，在可比 oracle 类型上反超 AGORA+（69.3%）；静/动互补，**两者合计找到 90%** ground-truth oracle。
- 18 个 bug（Amadeus Hotel/Deutschebahn/FDIC/GitLab/Marvel/OMDb/Vimeo）→ 文档更新。

**MASTOR** — Deng, Huang, Yang, Zhang, Xie, Wang; arXiv 2606.10465（submitted 2026-06-09，未标会议）.
- oracle：**基于 implementation source code** 的多 agent 语义 oracle；两类——单操作（status + field oracle）+ 多操作（behavioral consistency oracle，跨操作语义关联）。
- 机制：①source extraction agent 从 source files 的 transitive import closure 建上下文；②两条并行生成路径；③**challenger-agent review**（reviewer 挑弱点、给改进提示→定向重生成）；④**oracle normalization** 过滤结构无效的 oracle。
- 效果：13 个开源 REST 项目（296 operations，251,303 LOC，WFD+PRAB 数据集）；**平均 mutation score 75.4%**，生成 10,022 条 oracle；ToJUnit / ToPostmanAssertify / ToReadable 转译。
- 基线对比（50 ops）：比 Direct Prompting 高 **30.1pp**（69.9% vs 39.8%），比 SATORI 高 **49.4pp**（69.9% vs 20.5%）。
- ⚠️ 注意：MASTOR 报 SATORI 在它自己的 50-op 子集上只有 20.5%，而 SATORI 自己报 F1 74.3%（在自己数据集）——**评测设置不同，引用时不能混**。

### 3.2 五个问题 × 答案

1. **后续有人做吗？** 有，活跃一条线（Sevilla Alonso/Segura/Ruiz-Cortés + UW Ernst；工具族 AGORA）。综述 Golmohammadi et al. 2022 *Testing RESTful APIs: A Survey*（190+ 引）把 REST oracle generation 列为成长方向。
2. **最前沿效果？** AGORA+ 80% precision / 32 bug；SATORI F1 74.3% / 18 bug；MASTOR mutation 75.4% / 超 SATORI 49.4pp。
3. **怎么做？** 三范式：动态不变量（Daikon）/ LLM 读 OpenAPI 静态推 / 多 agent 读源码 + challenger 审稿。
4. **提 FP 吗？** 提，且是核心指标（precision/F1 < 100%）。
5. **有解决方案吗？** 有：AGORA+（🟡 统计过滤 + 算术启发式，待核实）；SATORI（更好 prompting + 静动互补）；**MASTOR（源码 + challenger-agent 审稿过滤）——和我们的 source-grounded falsification + dev-reviewer 撞最狠**。

### 3.3 逐条对照（我们声称 vs 已被做）

| 我们声称的卖点 | 这条线已做 | 剩余 |
|---|---|---|
| "LLM 从文档推 oracle" | SATORI | ❌ 基本不剩 |
| "doc 推的 oracle 会错、有 FP" | AGORA+ / SATORI 量化 | ❌ 不剩 |
| "用源码 + 审稿 agent 过滤坏 oracle" | MASTOR（源码 + challenger）| 🟡 撞最狠 |
| "多 agent 语义 oracle" | MASTOR | 🟡 撞 |

---

## 4. 可能还剩的 delta（诚实，待 grilling 夯实）

1. **领域迁移**：VDBMS API（Milvus/Qdrant/Weaviate）**非标准 REST、无 OpenAPI**（试过 /swagger 404）。AGORA+/SATORI 依赖 OpenAPI，不能直接迁移。真，但"换领域"单独是弱 novelty。
2. **失败模式的形式化——contract hallucination *propagation***：SATORI/MASTOR 把 LLM oracle 当"质量问题"用 prompting/审稿改；**没人形式化"生成端与判定端同一 LLM 家族→共享偏见→幻觉自我确认"**。可能仍独有的概念贡献——但**必须与"通用 LLM oracle 不可靠"严格切开**。
3. **source 的角色不同（要死磕的点）**：MASTOR 用源码**生成** oracle（源码=真相）；我们用源码**证伪** doc 推出的契约（doc=应然可能错，source=实然）。方向相反——但审稿人会看成“都是 LLM 读源码 + reviewer 提升 oracle 可靠性”，差异在 framing。
   - ⚠️ **新威胁点（Barr §4.3.1 推导，2026-07-15）**：VDB（Milvus/Qdrant/Weaviate）是**开源**的，所以 MASTOR 式"读源码生成 oracle"**原则上能迁移到 VDB**。区分必须更狠：MASTOR 把源码当真相→导出"代码做什么"→**抓不到代码违反意图**的情况；我们测的是 **doc(应然) vs code(实然) 的合规缺口**。这才是与 MASTOR 的机制级区别候选。
4. **实证体量**：5 库 111 缺陷、36 个维护者承认。AGORA+ 32 bug / SATORI 18 bug，我们量级更大，但领域不同不可直比。

---

## 5. 必须的动作（不管投哪；优先级排序）

- [ ] **P0 堵漏**：Related Work 补 AGORA+ / SATORI / MASTOR（+ 综述 Golmohammadi 2022、AGORA ISSTA'23）。现在是零引用。
- [ ] **P0 重做 Table 1 排除法**：当前写"合规缺陷只剩 LLM 一种 oracle"——被 SATORI/MASTOR 证伪（人家证明 LLM-from-docs 是 viable oracle，不是"无 oracle"）。改成"这些 oracle 范式为何**迁移不到 VDBMS compliance**"。
- [ ] **P1 delta 重新措辞**：从"提出 source-grounded falsification"（被 MASTOR 撞）→ 收到"形式化 contract hallucination propagation + 在无 OpenAPI 的 VDBMS 上实证"。与 B2（卖点重心从方法移到现象）吻合。
- [ ] **P1 核实 MASTOR 是否会议/正式发表、时间线**（2026-06 arXiv；若投 ISSTA 2027-01 则属 prior art，必须 cite + 区分）。
- [ ] **P2 全文核实 AGORA+ 的 FP 启发式细节**（算术比较类），以精确划界。

---

## 6. 当前未决的 grilling 问题（下次接着答）

> **既然 MASTOR 已是"多 agent + 源码 + challenger 审稿过滤坏 oracle"——我们和 MASTOR 的区别，是机制层面的真区别，还是同一个机制换了领域 + 换讲法？**

我的垫底答案（用户可反驳）：**机制层面大概率同族**；真正区别只有两处且都不在机制上——(a) 形式化 hallucination propagation（概念层），(b) 迁移到无 OpenAPI 的 VDBMS（实证层）。若这两处也站不住 → 机制上被 scoop → 卖法彻底转向"新领域实证 + 被命名的失败模式"。**待用户回应。**

---

## 7. 追加记录（按日期倒序，最新在上）

- **2026-07-15** 建档。完成 Barr 串讲概念沉淀（§2）+ 文献威胁核实（§3）+ delta 初判（§4）+ 动作清单（§5）。Slutz/Chen/QuickCheck 三篇待讨论。
- **2026-07-15（续）** Barr §4 *Specified Test Oracles* 串讲完成。
  - **四词关系**：Specification(伞) ⊃ {形式规约 / 状态转移+协议一致性 / 断言+契约 / 代数}；Contract⊂Assertion⊂Specification；演化箭头 = 抽象形式规约 → 具体 → 断言 → 契约。**我们属 Section 5+ 的 semi-formal / API-docs 分支，不在 §4。**
  - **四类路线现状**：①形式规约——学术为主，存活者 Alloy/Event-B/SPARK；🔥[LLM 自动生成 formal spec](https://dl.acm.org/doi/10.1109/ICSE55347.2025.00129)（SpecGen, ICSE'25, 162 引），且公认"生成的规约不可靠"。②状态转移/MBT/IOCO——成熟工业落地（embedded/汽车/电信），LLM+MBT 新兴未定型。③断言/契约——[OpenJML](https://www.openjml.org/)/[icontract](https://github.com/Parquery/icontract)/Racket 小众活跃；🔥LLM-gen contracts（Greiner 2024）。④代数规约——基本退场，精神被 property-based(QuickCheck)+metamorphic 吸收。
  - **Barr §4.3.1 三挑战 → 三个判断**：**A**：§4 因 VDB 无 formal spec 而全废，真威胁在 §5+（AGORA/SATORI/MASTOR）——Table 1 逻辑理顺。**B**：MASTOR 用 source + VDB 开源 → 原则上可迁移（已并入 §4-3）。**C**：🔥 LLM-gen-spec 线承认规约不可靠 → **从威胁变弹药**：cite 它支撑"LLM-derived oracle 不可信"前提，我们再进一步指出"judge 同族时不可靠会自我确认=propagation"。
- **2026-07-15（续2）** Barr §5 *Derived Test Oracles* 串讲完成（**我们的家**）。
  - **TestVDB 流水线对位**：Stage1 抽 contract = **5.5.1**（text→spec，converter=LLM）；Stage3 判合规 = 用 derived oracle 判定，但 checker **也是 LLM**（边界语义不可执行成断言）；Stage4 source-falsification = 用源码（5.4 artifact）**反向证伪** derived oracle；C3 reproduction = **5.4**（从执行推导行为）的实例。
  - **整章路线 × 现状**：5.1 pseudo/N-version→差分（CSmith/SQLancer=Slutz 现代后裔，VDB 无 reference 堵死）；5.2 蜕变→🔥LLM 大举进入（[LLMORPH ASE'25](https://arxiv.org/abs/2603.23611)/[Cho ICSMI'25](https://valerio-terragni.github.io/assets/pdf/cho-icsmi-2025.pdf)），VDB 无可变换形式堵死；5.3 回归→assertion amplification（弱相关）；5.4.1 不变量→**Barr 自认"学出来的 oracle 不可靠"(Daikon 一半误分类)**，🔥[LLM 推断不变量神经符号线](https://chentaolue.github.io/pub-papers/ASE24.pdf)（Wu ASE'24,60 引：LLM 候选+验证器检查）；5.4.2 规约挖掘→LearnLib/DSM/MINES；5.5 文档→**AGORA/SATORI/MASTOR/SpecGen 与我们的共同祖先**（5.5.1 用神经 converter 重做）。
  - **判断 D（钉死 novelty）**：①"LLM 从文档推 oracle"❌(5.5.1+SATORI) ②"derived oracle 会错"❌(**Barr 5.4.1 自认**) ③"独立检查过滤坏 oracle"❌(neuro-symbolic+MASTOR) → **仅剩 propagation（同族生成+判定→自我确认），且只是对已知现象的锐化**。但 propagation **只咬我们**有硬结构原因：VDB 合规语义 accept/reject **不可执行成断言→checker 被迫也是 LLM→两端同族**；AGORA/SATORI 的 oracle 能确定性执行，deriver 错了 checker 还能兜。**"为什么是我们"的论证 > 单纯命名现象。**
  - **判断 E（镜像，必须区分）**：neuro-symbolic（LLM 候选+数学验证器）与 dev-reviewer（LLM 契约+source falsifier）**结构同构**。区分=验证器的 ground truth：他们=数学真理（可证伪），我们=源码（by-design 实现意图，非形式化真理）。→ 收敛到 §4-3 的"测 doc-vs-code 合规缺口"。
  - **判断 F（定位补全）**：reproduction anchor 归 **5.4**（spec mining/invariant detection 实例），非独立第四 anchor。三 anchor 按 FP 成因分工的叙述里补这个学术坐标。
  - **卖法（记录非决策）**：实证系统 + 被锐化命名的失败模式（propagation）；与 B2 吻合，现由 Barr taxonomy 钉死。Slutz(differential=5.1)/Chen(metamorphic=5.2)/QuickCheck 待讨论。
- **2026-07-15（续3）** Barr §7 *The Human Oracle Problem* 串讲完成。
  - **判断 G（动机锚点，非 novelty）**：§7 = taxonomy 终点 "none"=人类是 oracle；2015 的三条对策（quant 砍规模 / qual 提可读真实 / crowdsource 外包）**全是降低人类成本，没替换人类**。**LLM(2023+) 是首个能规模化替代人类语义判断的技术 → LLM-as-oracle = Human Oracle Problem 的自然终点**。→ **"为什么用 LLM"最硬的文献锚点**：所有 artefact oracle 失效后，人类是唯一剩下的格，LLM 是其可规模化实现。⚠️ 只增加动机，不增加 novelty（"LLM 当 oracle" 已烂大街）。
  - **🔥 主线叙事链（动机→问题→贡献焊成一条）**：①人类 oracle 天然有**独立性(dissent)**——判 bug 的 ≠ 写文档的大脑；②用 LLM 替换人类时，若生成契约与判定合规**同族**，独立性丢失 → **propagation 是"替换人类"这个动作本身制造的新问题**（人类 oracle 时代不存在）；③**source-grounded falsification = 把人类 oracle 本有的"独立证伪"重新装回去**。这条链把 §7 直接焊到 propagation 上，组会/intro/rebuttal 通用。
  - **§7 现状**：7.1 quant→SBST(EvoSuite 后裔)+LLM 测试；7.2 qual→**Afshan 2013 的 language model 是 LLM-in-testing 先声**，现代=LLM 生成语义真实输入=我们 attack agents；7.3 crowd→LLM 替代众包做语义判断（"可规模化合成众包"）。
  - **金句（记录）**：§7 是**讲故事的金子**，§5 是**守 novelty 的底线**——别混。
- **2026-07-15（续4）** 差分测试深挖（用户反驳"完全做不了"过头，成立）。
  - **判断 H（差分 scope 修正，必改 Table 1）**：差分**不是整体失效**。能做：**数学定义不变量**（距离度量 `COSINE≤1` 等）——**我们的 model-free invariant 子类本质就是差分/数学检测**，跨 Milvus/Qdrant 复现（论文已有，只是没叫差分）；基本 CRUD 计数；小规模 ANN vs 暴力精确。**不能做**：①API compliance（跨厂商 accept/reject 按设计分叉，无权威 reference）；②最强现代差分 TLP/NoREC 迁移不到向量搜索（ANN 近似，无可证明等价改写）。**差分恰好失效在 compliance 这一格 = 需要 LLM 的地方。**
  - **差分两条轴**：比什么（两系统/同系统等价形式/优化vs参考/换引擎/模型vs实现/版本）× 在哪比（查询/操作/内部组件/状态）。**现代主力=单系统等价形式差分**（SQLancer TLP/NoREC/DQP），靠 SQL 可证明等价改写。
  - **最新进展**：[SQLancer](https://github.com/sqlancer/sqlancer) 族（OSDI'20，450+ bug，TLP/NoREC/DQP/PQS/TQS）；[SQLancer++](https://arxiv.org/html/2503.21424v2)(2025 泛化)、[THANOS](http://www.wingtecher.com/themes/WingTecherResearch/assets/papers/paper_from_25/Thanos_ICSE25.pdf)(ICSE'25 存储引擎轮换)、[Enhanced Diff in Emerging DBs](https://arxiv.org/html/2501.01236v1)(2025)。
  - ⚠️ **待核实**：[arXiv 2502.20812](https://arxiv.org/html/2502.20812v1) *Towards Reliable VDBMS: A Software Testing Perspective* 极可能 = 我们引的 `roadmap25`。它原话差分"**may face challenges**"——谨慎。**我们论文简化成"unsuitable"，比出处还武断，须照原口径修正。**
  - **Table 1 改法（记录非决策）**：旧"Differential testing is unsuitable…"→ 新"差分对数学不变量有效（我们采用），但对 compliance 失效（跨厂商语义分叉 + ANN 无等价改写）——恰好失效在需要 LLM 的一格"。
- **2026-07-15（续5）** 蜕变测试深挖（Chen 2018；四点）。
  - **判断 I（蜕变 scope，扩写非收窄）**：蜕变对 VDB **能用**——result correctness（排序单调性 top-k⊆top-(k+1)、增大 ef 不降 recall、自相似 d(v,v)≈0、距离对称 d(a,b)=d(b,a)、过滤一致性、CRUD 状态单调），[MeTMaP (FSE'24)=metmap24](https://dl.acm.org/doi/10.1145/3650105.3652297) 即此实例。**不能用于 compliance**：MR=输出关系，compliance=输入接受决策，**形式不匹配**（无保持 accept/reject 的输入变换）。比差分那个"跨厂商分叉"更硬。
  - **最新进展**：[Datalog MR 测试 FSE'21/ISSTA'23](https://mariachris.github.io/Pubs/FSE-2021.pdf)（蜕变测 DB 引擎）；搜索 MR（Zhou）；🔥自动发现 MR 解历史瓶颈——[MR-Scout TOSEM'24](https://valerio-terragni.github.io/assets/pdf/xu-tosem-2024.pdf)/MR-Coupler/Metamon + LLM-gen MR（LLMORPH ASE'25/Cho ICSMI'25）。
  - **🔥 关键驳斥（写进论文很值钱）**："LLM 现能自动生成 MR→能给 compliance 造 MR 吧？"→ **不**：自动发现解的是"**发现成本**"，compliance 的问题是"**根本不存在有效 MR**"（无输入变换保持 accept/reject）。**排除对 LLM-MR 进展鲁棒，时间对我们有利。**
  - **对原表述影响**：现句"metamorphic serve result correctness but not API-acceptance"——**对且比差分那句更稳**（点出结构 mismatch），但**太亏**。修法=**扩写**（显式承认 result-correctness 适用 + 结构理由 + 诚实承认 result correctness 是 open、我们不解），方向与差分（收窄）相反，目的同：精确 scope + 显懂边界。
  - **对照**：差分=过声称→收窄；蜕变=说亏了→扩写。两处都改成"懂边界"更可信。
- **2026-07-15（续6）** Property-based testing 深挖（QuickCheck；四点）。
  - **最新进展**：Hypothesis/[Schemathesis](https://schemathesis.readthedocs.io/)(stateful+targeted PBT)；[QuickREST](https://arxiv.org/abs/1912.09686)(OpenAPI→PBT，已 cite)；🔥**LLM+PBT 2024–25 热浪**——LLM 生成 property（AIWare'25/CPS'25）、[PBT 验 LLM 合成 spec (2026)](https://proofsandintuitions.net/2026/05/18/property-based-testing-specifications/)（结构像我们 falsification）、OOPSLA'25 PBT 找 mutant ~50× 单测。**模式=LLM 当 property 来源，PBT 查——TestVDB 正在做。**
  - **判断 J（PBT 重新框定，借力非收窄）**：经典 PBT 在 VDB **数学子集能用**（距离对称/三角/COSINE∈[-1,1]；**我们的 model-free invariant 子类本质就是 PBT property**）；在 **compliance 够不到**（无机器表达 property + 无 OpenAPI schema）。**但 TestVDB 的 LLM-contract = 人造 property → 结构上 PBT-inspired**（偏离三处：property LLM 从 NL 造 / check LLM 语义非确定 / input gen threat 引导）。→ **卖法从"PBT 不行"→"把 PBT 推进到经典够不到的 compliance，代价=propagation"**。check 非确定性 = propagation 的结构性原因（接 §7 链）。⚠️别直自称 PBT（规范是确定 check），用 PBT-inspired。
  - **驳斥**：①"PBT 测不了 VDB"❌(数学 property 能) ②"PBT 当 compliance oracle"被卡(无 property+无 schema=TestVDB LLM-contract 所填) ③🔥"LLM-gen property 热浪→你能 PBT/不新"半对不驳：确定性 check 仍不可→propagation，且热浪验数学/schema 非未文档化边界，是**我们在的趋势非反证**；但"LLM 造 property"本身不够新 ④"PBT 验 LLM-spec(2026)=你 falsification"结构像但 ground truth 不同(数学/Lean vs 源码)。
  - **🔥 统一三类（收束全排除表）**：差分/蜕变/PBT **三者都能测 VDB 数学子集**（距离不变量=model-free invariant 子类，三者共同能处理），**三者都在 compliance 失效** → 数学子集=经典可测(我们用)，compliance 子集=经典全废→LLM。propagation=用 LLM 替代人类 oracle 的副作用(§7 链)。

- **2026-07-15（续7）** 反驳 1：传播不是结构强制的（用户戳中，concede）。
  - 原 forcing 两步：(a) checker 必须是 LLM（compliance 不可编译成确定性断言）；(b) 同族→传播。**(a) 成立，(b) 是设计选择不是强制**——换异家族能（部分）打破传播。
  - 校准（非救场）：异家族≠完全独立（都自回归、训练语料重叠）→ 独立性光谱：确定性断言(满) > 异家族 LLM(部分) > 同家族(零)。VDB compliance 锁在 LLM-judge 区，够不到确定性断言端。
  - **降级**：支柱①从"结构强制的概念新发现"→"单家族实践漏洞 + 可能更优 countermeasure"，立不立看 E2。

- **2026-07-15（续8）** 反驳 2：classical 没废（用户对，"废了"过头）。
  - 111 bug 非纯 compliance：数学根/crash/状态计数的 classical 能找。classical 真够不到的是**纯 compliance 残差**（accept/reject 违文档但不崩/不违数学/无 MR）。
  - 贡献大小 = 残差占比 → **新增 E1（bug 分类）**，自家数据能答，未答。⚠️ 分类不干净（bug 可能"靠 compliance 发现但根是数学"，需人工裁）。

- **2026-07-15（续9）** Task 3 术语审计（Web 核实）。
  - **oracle** ✅ Barr 2015 对齐。**falsification** ✅ 形式方法成熟术语（找反例推翻性质），"source-grounded falsification"站得住。
  - **compliance** 🟡：NIST 权威 **conformance testing**="测实现忠实满足规约"几乎就是我们的定义；compliance 偏法规。重构考虑 conformance/契约一致性。中文：conformance=一致性测试(ISO/GB-T)，compliance=合规(强联想法规)。
  - **hallucination propagation** ❓：精确短语零命中=造词。近邻 self-consistency/LLM-as-judge/HSP。

- **2026-07-15（续10）** 🔥 Task 2-A MASTOR 全文（arXiv 2606.10465，✅原文）→ **两 hinge 解决，比预期更有利**。
  - **Hinge 1（challenger vs 我们 falsification）→ 不是一回事，forcing 上移到更干净的一层。** ✅ MASTOR 判定全程确定性：PITest/JUnit 执行 oracle 断言判 mutant（§5.2.2）；challenger（Qwen3.6-Plus，**异模型**）只在生成阶段审 oracle 质量（Table 5）发 hint 引导一次重生成（§4.4.1）。**MASTOR 不用 LLM 当 checker** → 传播对它不适用。✅ 默认 DeepSeek V4 Pro 主 + Qwen challenger=故意异模型。**→ 真正 forcing 是"compliance 不可编译成确定性断言 → checker 被迫是 LLM（LLM-as-checker 区）"**；MASTOR/SATORI/AGORA+ 的 oracle 是可执行断言、checker 确定性，**根本不进此区**。反驳1的"换异族"只在区内缓解、出不了区。
  - **Hinge 2（MASTOR 源码用法 vs 我们）→ 被证不同 fault model，非 framing。** ✅ §7.4.2 原文："MASTOR infers semantics from implementation behavior. **It cannot detect violations of intended requirements that are not reflected in code.**" MASTOR 参考系=代码（mutation 范式），我们=文档（compliance 范式）。不同 fault model，MASTOR 明确排除我们的类。
  - ✅ §4.3.2 MASTOR 用 OAS 当 endpoint 权威来源 + 仅 Java → 需 OpenAPI+源码，VDBMS 无标准 OpenAPI 不能直迁（支柱③确认）。

- **2026-07-15（续11）** 🔥 Task 2-B 传播检索 → **支柱①再降级 + 最终重构（关键）**。
  - ✅ 我们说的"同族生成+判定→自我确认"**已有成熟学名 = self-preference bias / LLM-as-judge self-preference**：[Panickssery et al. 2024 (arXiv 2404.13076)](https://arxiv.org/html/2404.13076v1)"LLM Evaluators Recognize and Favor Their Own Generations"——LLM 评估器给自家输出打高分，有人类标注为证。配套 [Self-Preference Bias in LLM-as-a-Judge (2410.21819)](https://arxiv.org/html/2410.21819v1)。**标准缓解=换异族当 judge / 人类抽检 / 盲测 A-B**（正是反驳1说的"换不同家族"）。
  - ✅ 跨模型验证是教科书缓解：Chain-of-Verification (Meta)、REVERSE、CCVP。⚠️ 但 Yale'25/Nature'26([s41586-026-10549-w](https://www.nature.com/articles/s41586-026-10549-w))指出 LLM 自/交叉验证有**根本可靠性上限**。
  - **→ 支柱①最终定位（诚实）**：**不是"我们发现/命名了同族偏差"**（Panickssery 已做），而是三件事：(a) **结构性 forcing 论证**——VDB compliance 不可编译成确定性断言，被迫进 LLM-as-checker 区，而 AGORA/SATORI/MASTOR 靠确定性 checker 逃出该区、self-preference 咬不到他们；这是"为什么是我们"的硬理由。(b) **source-grounded falsification** 作为该区的领域专用 countermeasure（区别于通用"换异族"）。(c) **test-oracle/compliance 域的实证**（self-preference 文献都在通用文本评估，没人测过 oracle 合规管线）。
  - **E2 现在有文献锚定的假设**：self-preference bias 预测同族 contract+checker 自我确认；测 source-falsification 是否比 cross-family 更降假确认。

---

## 8. 修订后的贡献地图（post-rebuttal + post-MASTOR + post-propagation，2026-07-15）

**一句话**：MASTOR 把两个最怕的碰撞都化解（checker 确定性→不进 LLM-as-checker 区；参考系是代码→不测 doc-vs-code）；propagation 检索把"同族偏差"从我们的发明降格为已有学名 self-preference bias，但留下"结构性 forcing + 领域专用 countermeasure + 域实证"三件套。我们占"LLM-as-checker 区 × doc-vs-code fault model"这个交集。

| 支柱 | 最终状态 |
|---|---|
| ① 传播/self-preference | **非新概念**（Panickssery 2024 已命名）。我们贡献=forcing 论证（compliance 不可编译→LLM-as-checker 区，AGORA/SATORI/MASTOR 逃出该区）+ source-falsification countermeasure + 域实证。立不立看 E2。 |
| ② 源码方向 | **最干净的区别**。MASTOR §7.4.2 明确排除 doc-vs-code；参考系代码(mutation) vs 文档(compliance)，不同 fault model。 |
| ③ 领域+实证 | 确认（MASTOR/SATORI 需 OpenAPI；VDBMS 无）。 |
| ④ 统一排除 | classical 覆盖数学/crash 子集，compliance 残差只有 LLM-as-checker 够（非"全废"）。 |

**最干净的结构叙事**（intro/rebuttal 通用）：
> AGORA+/SATORI/MASTOR 把 LLM 留在生成道、用**确定性断言**判定。VDB compliance 的 accept/reject 语义**不可编译成确定性断言**，LLM 被迫进入判定道——这正是 self-preference bias（Panickssery 2024）所在、且 AGORA/SATORI/MASTOR 因确定性 checker 而免疫的区。我们不是重新发现这个 bias，而是：(1) 论证 VDB compliance 把你**锁死**在这个区（结构性，不可像 REST+OpenAPI 那样逃出）；(2) 提 source-grounded falsification 作为领域专用 countermeasure；(3) 实证测它 vs cross-family。而 falsification 测的是 **doc(应然) vs code(实然) 的 compliance 缺口**——MASTOR 把代码当真相、明确抓不到这一类（§7.4.2）。

**待 E1/E2 验证**：
- E1：111 bug 里 doc-vs-code compliance 残差占比（体量 + 验证 bug 真属 MASTOR 够不到的类）。
- E2：同族 vs 异族 vs +source-falsification 三组（文献锚定：self-preference 预测同族自我确认）。

---

## 9. E2 深挖结果（2026-07-15）：t25 已跑跨家族检验 → 支柱①再重构（更诚实、更强）

**发现 1｜51-probe 集（p1_single_llm_50）对 judge-level E2 无效。** 38 FP 全是 `response_code≠0`（API 正确拒绝），**0 个 hard FP**（accepted-but-by-design）。GLM 的 25.5%（=13/51）是"HTTP200 当接受"的方法学 bug，**非 self-preference**。→ 不能用它测 self-preference；在它上面跑 DeepSeek 必然 ~100%，是"会读 body code"，误导。

**发现 2｜t25_contract_counterfactual（Round 13）已跑正确的跨家族检验。** 同一份**原始文档**喂 GLM vs DeepSeek，看异族是否复现 GLM 的"过严契约"（导致 by-design FP 的约束）。结果（9 过严案例）：DeepSeek 复现 **≈2-4/9**（脚本 marker 严格计 2；语义读 ~4）。
- 异族**修对了**（task-intrinsic 不成立，是 GLM 特异）：`limit>=0`、`offset>=0`、`roundDecimal==-1||>=0`、`dbName==null||"default"`。
- 异族**也错**（task-intrinsic，文档歧义）：`shardsNum>=1`、metricType/consistencyLevel 严枚举、`data` 非空——两家都从"default:1"推 ≥1。
- → **过严偏差约一半 family-specific（异族能修），约一半 task-intrinsic（异族也复现，源码才能解）。**

**🔥 支柱①再重构（数据驱动，比"传播"框架更强）：**
- **旧**："source-falsification 打破同族传播"——弱（异族也能部分修；传播是 Panickssery 已占的域；反驳1 已削弱"同族强制"）。
- **新**：source-falsification 的真价值 = 解决 **task-intrinsic 契约错误**（同族+异族都从歧义文档犯同样错的那些）。这是 cross-family **结构性修不了**的：文档说"default:1"时，GLM 和 DeepSeek 都推 ≥1，只有**源码**知道 0=用默认。
- → **source 与 cross-family 互补不冗余**：异族补 family-specific 子集，source 补全部（family-specific **+** task-intrinsic）。source 覆盖的正是 cross-family 的盲区。例：shardsNum=0=default、limit=0=no-limit、roundDecimal=-1=no-rounding。
- **为什么比旧框架强**：不撞 Panickssery（self-preference 是 family-specific 子集，我们承认并细分）；不依赖被反驳1削弱的"同族强制"；把"为何需要源码"从"打破同族"升级为"解 task-intrinsic"——后者 cross-family 永远做不到，是结构性。

**对论文影响**：支柱①从"同族传播"转向 **"task-intrinsic 契约错误 + 源码是唯一 ground truth + 与 cross-family 互补"**。E2 核心已由 t25 回答（generation level）。judge-level hard-case 测试可选（需新建 accepted-but-by-design probe 集）。⚠️ t25 N=9 pilot，发表需扩到 ~30-50 跨 5 DB。
- 🔥 **更新版结构叙事**：cross-family（DeepSeek/Panickssery 式）只能消除 family-specific 的契约偏差；当文档本身歧义（default 值、optional 语义），所有 LLM 家族都会犯同样的"过严"推断——这一类只有源码（实然）能裁决。TestVDB 的 source-grounded falsification 因此不是"又一个 LLM 审",而是**唯一能解 task-intrinsic 类的 ground truth 通道**。

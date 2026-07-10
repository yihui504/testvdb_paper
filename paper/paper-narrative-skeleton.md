# TestVDB 论文叙事骨架

> **来源**：2026-07-07 grilling session 达成的叙事决策。
> **用途**：指导论文写作（§1/§3）与 PPT V4 制作。取代 [paper-draft.md](paper-draft.md) 附录 A 的旧 24-slide outline。
> **状态**：骨架定稿。旧 [ppt-draft-v3-archived.pptx](ppt-draft-v3-archived.pptx) 已存档，新 PPT 基于 V4 大纲（[ppt-v4-outline.md](ppt-v4-outline.md)）。

---

## 1. 核心问题（已定：A）

> **当「契约」本身可能错、crash 这个机械 oracle 不再适用、且 LLM 判定无反证机制时，如何可靠挖掘 VDBMS 的 API 合规性缺陷？**

三 gap 合一：
- **G1 crash 失效**：合规缺陷不崩（vdbfuzz 的 oracle 不适用）
- **G2 contract 不可靠**：文档化 contract 有 30% 反标率；根因之一是**契约幻觉**——LLM 既生成契约又判定合规，幻觉约束被自我确认（#50354 complexity requirements 源自 constant.go 是 formalizer 造的）
- **G3 LLM 无反证**：LLM 判定既当断言又当真相

## 2. Key Insight（已定：A）

> **当机械 oracle（crash / PoC 复现）失效时，唯一可用的真相源是维护者权威（源码 + PR + by-design + 历史）；它稀缺，故必须被 agent 代理（dev-reviewer）。**

**Design Principle**（落地形式）：**Contract-Truth Separation**——断言层（contract / threat model / LLM 判定）与真相层（维护者权威代理）分离，用后者逐级反证前者。

三层关系：insight（为什么必须用维护者权威）→ 原则（如何组织进 oracle 设计）→ 实现（四层反证链）。

**三层嵌套（故事线结构，2026-07-09 修订）**：外层（**非崩溃缺陷缺可用 oracle**——crash 仅覆盖 23.1%，incorrect behavior 43% 是 oracle 难题，被 [arXiv:2502.20812] roadmap 背书的问题立论）→ 中层（CTS + dev-reviewer = **超越 crash 的 contract oracle**，吃 incorrect behavior 的 API 合规子集；**非** vdbfuzz 方向① 要的"结果正确性 oracle"，后者仍 open）→ 内层（契约幻觉传播，方式揭示的新风险，反证层是对抗机制）。

## 3. Thesis Statement（暂搁置）

用户暂未定。候选 T1（problem-centric，VLDB 风）：
> 向量库 API 合规缺陷普遍但不可测；通过 agent 代理维护者权威作为语义真相层、逐级反证断言层，可将 LLM 驱动测试的 precision 从 12.9% 提升到 69.2%，并在 5 个主流 VDBMS 上发现 111 个先前未知缺陷。

## 4. 借鉴边界（已定：A，三层口径）

### vdbfuzz (ICSE'26) — 借生成手段，换 oracle

| 借 | 不借 |
|---|---|
| API 约束形式化（§4.1 `C_a` 谓词）| Oracle = crash（核心差异）|
| 边界违反生成（§4.3 Pattern 1）| 覆盖率引导（§5.3）|
| 三类攻击方向（data/indexing/query）| Seed Collection（从合法用法）|

**定位**（精确口径，2026-07-09 修订）：vdbfuzz crash-only（ICSE'26 标题钉死），Discussion 列两条 future work——① oracle for correctness；② LLM 生成 diverse API interactions + 保持更新。**TestVDB 的回应**：生成面（attack agents + knowledge-extractor）**正面回应 ②**；判定面（CTS + dev-reviewer）= **超越 crash 的 contract oracle**（把可检测边界从 crash 扩展到 API 合规子集）——**不声称填 ①**（① 要的是结果正确性 oracle，ANN 精度/ranking 仍 open，见 [arXiv:2502.20812]）。**非"双向背书"**——生成侧被 ② 背书；判定侧是独立贡献，不是对 ① 的回应。叙事递进：开题从方向 ② 起步（LLM 生成）→ 发现非崩溃缺陷判定才是核心 → 判定面定位为"超越 crash 的 contract oracle"。

### Anthropic harness — 借架构位置，换内容

| 借 | 不借 |
|---|---|
| threat model 作前置 scope 工件 | Verify = PoC 复现（机械）|
| 两容器独立验证的**思想**（非容器隔离）| Dedupe judge（ASAN signature）|
| bootstrap-then-interview 形态（半借，全自动）| Patch ladder |

**定位**：Anthropic 的机械验证在无 crash 场景失效，TestVDB 换成语义真相代理。

### TestVDB 原创（两份参考都没有）

1. **Contract-Truth Separation 作为设计原则**
2. **Dev-reviewer 作为维护者代理**（核心技术贡献）
3. **认知盲点（cognitive blindspot）建模**——历史上反复被报但被判 by-design 的行为
4. **4-Judge 多视角辩论**（evidence/severity/novelty/doc）
5. **Threat model 双重注入**（生成 + 判定，Anthropic 只 scope 扫描）

---

## 5. 叙事结构（已定：版本 A + §1.4 骨架图）

**§1 走 3 环节**（紧凑，标准 problem-driven）：
- 锚点 0（vdbfuzz future work）+ 问题 1（总 gap）
- 问题 3（核心反转）+ insight
- §1.4 放骨架图（完整 5 步链条的形状）

**§3 走完整 5 步链条**（逐步展开论证）。

### 5 步链条骨架图

| 链条 | 问题（gap）| 解（组件）| 借鉴 / 原创 |
|---|---|---|---|
| **锚点 0** | vdbfuzz crash-only + [arXiv:2502.20812] 点名 incorrect 43% 缺 oracle | 生成面**回应 ②**（LLM 生成）；判定面=**超越 crash 的 contract oracle**（非结果正确性 oracle，不声称填①） | 生成侧背书②；判定侧独立贡献 |
| **问题 1** | 合规缺陷无信号，oracle 是什么 | **LLM**（排除法）| 起点 |
| *拆总 gap* | LLM 两角色都不可靠 | | |
| **问题 2** | 生成面：LLM 方向平庸 | **threat model**（生成层先验）| 借 Anthropic 架构 + 自有内容 |
| *升级* | 方向对了 ≠ 判定对了 | | |
| **问题 3 ★** | 判定面：contract 可能错（含**契约幻觉**）| **dev-reviewer + contract-truth separation** | **原创（核心反转）** |
| *升级* | dev-reviewer 也是 LLM | | |
| **问题 4** | dev-reviewer 凭何比 4-judge 可信 | **三层反证锚点** | 原创 |
| *升级* | 通过的还可能已知 | | |
| **问题 5** | 查重 | **双层 novelty gate** | 自有 |
| **收束** | — | threat model 横跨四层（经验先验中枢）；契约幻觉是反证层揭示的风险；所有解 = CTS 的实例化 | 设计意图 |

### Threat model 的四重注入（横跨四层，只在问题 2 当主角）

| 层 | threat model 角色 | 主角/辅助 |
|---|---|---|
| 问题 2（生成）| 语义先验引导方向 | **主角** |
| 问题 3（判定）| 反证词典（让 dev-reviewer 知 by-design）| 辅助 |
| 问题 4（dev-reviewer 内部）| 三层反证机制之一 | 辅助 |
| 问题 5（查重）| Novelty Gate L1 数据源 | 辅助 |

**收束句**：与 Anthropic 的 threat model（一次性 scope 工件）不同，TestVDB 的 threat model 是贯穿生成-判定-查重的经验先验中枢——这是 LLM-driven testing 的经济性决定的（生成贵 → 必须复用先验）。

---

## 6. §1 Introduction 结构（6 段，~2 页）

| 段 | 内容 | 关键证据 |
|---|---|---|
| §1.1 动机 | VDBMS 承重基础设施，合规缺陷普遍 | 1671 bug [arXiv:2506.02617]；nprobe=0/shardsNum=-1/cosine>1.0 |
| §1.2 锚点 0 + 问题 1 | vdbfuzz crash-only + [arXiv:2502.20812] incorrect 43% 缺 oracle → 排除法 → LLM；总 gap：两角色不可靠（回应 ②，不填 ①）| 排除法表；vdbfuzz Discussion ② 引 |
| §1.3 问题 3 核心反转 + insight | contract 可能错（含契约幻觉 #50354）→ 维护者权威 → 必须代理 → CTS | 30% 反标率；#50354 幻觉实例；第二层排除法 |
| §1.4 方法概览 + **骨架图** | 四层反证链 + 5 步链条骨架图 | threat model 横跨四层 |
| §1.5 结果 | 111 issue / 36 承认 / 12.9%→69.2% | cosine>1.0 双库复现 |
| §1.6 贡献 | 6 条（理论/方法/技术/原创/实证/工程）| 每条标注"对比既有工作" |

## 7. §3 Method 结构（4 节，~5-6 页）

| 节 | 对应链条 | 内容 |
|---|---|---|
| §3.0 Overview | 全链条 | 复用 §1.4 骨架图，说"逐步展开" |
| §3.1 Threat Model | 问题 2 | LLM 方向平庸 + 经济学（10M vs 1834）+ 三类情报 + 双重注入 |
| §3.2 Attack + 4-Judge | 生成面延续 | 三类 agent + 4-judge + 漏斗经济学 |
| §3.3 Dev-Reviewer | 问题 3+4 | CTS + 三层反证锚点（clean repro / **source-grounded 反幻觉** / threat model 核对）+ 80.6% FP |
| §3.4 Novelty Gate | 问题 5 | 双层查重（L1 threat model + 本地 / L2 GitHub API）|

---

## 8. 三个硬约束（必须守住）

1. **链条必须收敛到 contract-truth separation**——所有"问题→解"对子都是它的实例化，不是 5 个独立改进。
2. **原创组件必须占核心反转位置**（问题 3）——dev-reviewer 和 CTS 不能写成借鉴链条中的一环。
3. **借鉴必须精确引用原文锚点**——vdbfuzz §4.1/§4.3、Anthropic `/threat-model` skill。

## 9. 风险与对冲

| 风险 | 对冲 |
|---|---|
| 5 步链条在 §1 太长 | 版本 A：§1 走 3 环节，5 步留 §3.0 |
| 单一原则被判"naming trick" | §1.3 把"为什么断言/真相必须分离"讲到骨头；§4 RQ3 的 12.9%→69.2% 证伪"不干活" |
| "维护者权威"不够学术 | 80.6% FP 剔除率是证据；类比"代理专家权威"在代码评审/合规审计的先例 |
| 问题 2 的 threat model 论证弱 | 诚实标注"缓解生成面"，不背"解决可靠性"的锅；经济学（precision-per-generation）补强 |
| 跨库 RQ3 数据只 milvus 单库 | §4.4 诚实写 limitation；列为 future work |

## 10. 关键事实清单（数字必须一致）

- **111 issue / 36 维护者承认（28 fixed + 8 accepted）/ 12 by-design**
- **跨层消融（Milvus v2.6.19）**：1834 raw → 33 Stage-2 → 31 dev-reviewed → 4 confirmed
- **4-judge 单层 precision 12.9%（4/31）**；**dev-reviewer 剔除 80.6% FP（25/31）**；**全链 69.2%（36/52）**；**5.4× 提升**
- **contract 反标率 ~30%**（23 次反标 / pipeline 11 + 提交层 12）
- **5 库**：Milvus / Qdrant / Weaviate / Meilisearch / Chroma
- **明星 case**：cosine>1.0（Milvus #49059 + Qdrant #8688，双库复现）；state_001 contract_misread（dev-reviewer 反证）；**#50354 契约幻觉**（complexity requirements 源自 constant.go 是 formalizer 造的，dev-reviewer source-grounded 反证）

---

## 11. 分类法定位（G：目标声明版，已定）

**决策**：4 型分类法**不作理论贡献**，降为**目标声明**（非"形态学描述"，非"分类法"）。

**理由**：分类法灵感来自 [arXiv:2506.02617] 的 VDBMS bug 统计——硬 claim 理论贡献会被审稿人质疑"和 arXiv 统计重叠"。降为目标声明既诚实，又避开"分类法/taxonomy"框架的误判风险。

### 推荐措辞（直接采用）

> 我们从 [arXiv:2506.02617] 的 VDBMS bug 统计中识别出 4 类高发缺陷形态。**TestVDB 聚焦其中 3 类作为攻击目标**——边界违反（Type 1，对应 boundary attack）、诊断质量（Type 2，semantic attack）、状态/逻辑不一致（Type 4，state attack）；**Type 3（合法输入触发崩溃）由 L1 机械闸门前置过滤**，因为此类缺陷大多 wontfix，过滤是符合维护者真实偏好的设计意图，而非能力局限。

### 4 类与 attack agents 的对齐（设计证据）

| Type | 名称 | 是否目标 | 对应 attack agent |
|---|---|---|---|
| Type 1 | Illegal Success / Rejection（边界违反）| **核心目标** | boundary |
| Type 2 | Poor Diagnostics（诊断质量）| 延伸目标 | semantic |
| Type 4 | State/Logic Violation（状态不一致）| 延伸目标 | state（+ semantic）|
| Type 3 | Runtime Failure（合法输入崩溃）| **非目标**（L1 过滤，设计意图）| — |

### 实测分布（诚实标注）

`Type1:27(75%) / Type2:3(8%) / Type4:2(6%) / Type3:1(3%) / 结果正确性:3(8%)`——36 TP 的 title-based 分类（待 TestVDB 实际 type 标签核对）。

**系统真实身份**：**边界/校验合规检测器（兼及诊断/状态）**，**不是均衡四型检测器**。75% 产出是参数/枚举/上限校验缺失。Crash 仅 1/36 = **设计性排除**（L1 gate 滤掉 Type3），与 vdbfuzz 近零重叠是设计使然 → "互补"叙事成立。结果正确性 3/36(8%)——含数学不变量违反（cosine 相同向量距离>1.0）、索引召回不全（2/25）、查询语义错误（filter 返错点）；软结果正确性（ANN 召回/ranking 误差）仍 open。

### 标题与措辞（G 框架）

- **标题保持 "API Compliance Defects"**——呼应 contract-truth separation，和 vdbfuzz crash sharp 对比
- **正文用 "correctness" 作上位词**——compliance 是 correctness 的核心子类
- **分类法放 §2 背景**——目标声明段落，不当贡献

### 贡献 1 重排（2026-07-09 二次修订）

旧贡献 1："四型分类法的形式化与实证校准"（站不住，灵感来自 arXiv）
一修订（2026-07-07）："赛道界定"——但 2026-07-09 grilling 发现赛道已被 [arXiv:2502.20812] roadmap 界定，"界定"声称站不住。

新贡献 1（二修，2026-07-09）：
> **首个 LLM 驱动的 VDBMS API 合规缺陷检测实现与大规模实证**
>
> 在已被 [arXiv:2502.20812] roadmap 界定的 VDBMS 测试赛道上，首个用 LLM 端到端实现"非崩溃 API 合规缺陷"的检测与判定（区别于 vdbfuzz crash、NoREC SQL correctness），并产出大规模实证（111 issue / 36 承认）。不作"赛道界定"声称。

**分类法主参考（2026-07-09）**：B=[arXiv:2502.20812](Crash23.1%/Incorrect43%/Perf9.3%/Build9.7%) 主 frame；A=[arXiv:2506.02617](5 症状/31 pattern) 退为印证 + fault-pattern 词汇源。4 类 = 自有 compliance-dimension 轴，投影到 B symptom 轴。**重要**：A、B、VDBFuzz 是同一组（Shenao/Haoyu Wang + Hou/Zhao/Xie），统治 VDB-testing 议程，无已发表 LLM-driven VDB 合规检测系统（niche 开但 scoop 风险最高）。

---

## 12. Threat Model 定位最终调整（已定：降为 exploratory pilot）

**决策**：TM 在判定层的作用**降为 exploratory pilot**，论文不强调 TM，聚焦 CTS 核心。

### Ablation 实验结论（干净双盲 + 对应版本容器）

控制组（cognition: by_design=6, blindspots=0）vs 实验组（空 cognition），v2.6.17 组 n=5 TP + 7 FP：

| 指标 | 控制组（有 TM）| 实验组（无 TM）|
|---|---|---|
| TP recall | 1/5 = 20% | 3/5 = 60% |
| FP 判对率 | 6/7 = 86% | 4/7 = 57% |

趋势：TM 有保守化倾向（precision↑ recall↓），但**不可靠**（见下）。

### 为什么降级（实验设计缺陷）

1. **blindspot_indicators=0**：TM 保护 TP 的机制（blindspot 提升置信度）从未被测试——控制组 cognition 没有 blindspot 数据。实验实际只测了 by_design_patterns 的作用。
2. **dev-reviewer 判定不稳定**：同一候选（#49823）4 次 run 得 2 CONFIRMED / 2 FP（50/50）。单次控制 vs 实验对比受随机性主导。
3. **n=5 TP**：单个候选翻转即改变结论，统计不显著。

### 可靠发现（比 TM 作用更重要）

**dev-reviewer（LLM）的 TP recall 低（20-60%）**——无论有无 TM，dev-reviewer 连真 bug 都难识别。这是 CTS 的核心挑战：LLM 能否可靠代理维护者权威。此发现多次 run 一致，可靠。

### 论文处理

- **TM 定位**：exploratory pilot——§3.1 简述（不作核心声称），ablation 结果放 §4"exploratory analysis"，诚实标注设计局限（blindspots=0 / n=5 / 不稳定）
- **CTS 核心不变**：dev-reviewer 反证断言层（提高 precision）——但诚实标注 TP recall 限制（20-60%）
- **聚焦的实证**：契约幻觉传播（#50354 complexity requirements 是 formalizer 造的）、stats 滞后（#50193 sealed-segment）、误归因（#50351 名字含连字符非 shardsNum）——这些是 dev-reviewer 独立发现的，支撑 CTS 的"反证"价值
- **future work**：更强的 dev-reviewer（多轮辩论 / 更强模型 / 多次 run 取平均）+ 补 blindspot_indicators 重测 TM 保护 TP 机制 + 契约幻觉发生频率统计

---

## 13. 贡献列表（6 条）

1. **首个 LLM 驱动的 VDBMS API 合规缺陷检测实现与大规模实证**——在被 [arXiv:2502.20812] roadmap 界定的 VDBMS 测试赛道上，首个用 LLM 端到端实现"非崩溃 API 合规缺陷"检测与判定（区别于 vdbfuzz 的 crash oracle、NoREC 的 SQL correctness），并产出大规模实证（111 issue / 36 承认）。**不作"赛道界定"声称**（赛道已被该 roadmap 界定）
2. **CTS 设计原则**——Contract-Truth Separation：断言层（contract / LLM 判定）与真相层（维护者权威代理）分离，用后者逐级反证前者
3. **dev-reviewer 反证机制**——三层锚点（clean repro / source-grounded 反幻觉 / threat model 核对），剔除 80.6% FP，precision 12.9% → 69.2%（5.4×）；TP recall 20-60% 诚实标注
4. **契约幻觉传播发现**——LLM 既生成契约又判定合规时，幻觉约束在生成-判定链中被自我确认；反证层（source-grounded）是对抗机制。**实证**：12/48 已裁定提交（25%）被维护者判 BY_DESIGN，均为"LLM 推导契约比真实意图更严"（幂等/最终一致/宽松默认/命名宽容），即契约幻觉的直接观测（案例 #50354 + 12 BY_DESIGN）
5. **TM exploratory pilot**——诚实标注设计局限（blindspots=0 / n=5 / 不稳定）
6. **实证 + 工程开源**——5 库 111 缺陷 / 36 维护者承认；系统开源

---

## 附：grilling 决策日志

| # | 决策点 | 选定 | 关键理由 |
|---|---|---|---|
| 1 | 核心问题 | A（三 gap 合一）| 解落在自研（oracle 层），不被借鉴吃掉 |
| 2 | Key insight | A（维护者权威代理）| 立 vdbfuzz/Anthropic 的本质分界（机械 vs 语义真相）|
| 3 | Thesis | 暂搁置 | 用户未定，候选 T1 |
| 4 | 借鉴边界 | A（三层口径）| vdbfuzz 借生成换 oracle；Anthropic 借架构换内容；用 vdbfuzz Discussion 当跳板 |
| 5 | 叙事结构 | A + 骨架图 | §1 走 3 环节（主流低风险），§3 走 5 步；§1.4 骨架图消除重复感 |
| 6 | threat model 角色 | 生成层主角，判定层辅助 | 解耦"方向平庸"和"判定不可靠"两个 gap；经济学（precision-per-generation）补强 |
| 7 | 问题 1-2 衔接 | 总-分结构 | 问题 1 立"LLM 两角色不可靠"总 gap，问题 2/3 拆面 |
| 8 | 分类法定位 | G（目标声明版）| 降为目标声明（非形态学/非贡献）；4 类来自 arXiv 统计，3 类为攻击目标，Type 3 设计意图排除；贡献 1 换赛道界定 |
| 9 | TM 判定层 ablation | 降为 exploratory pilot | blindspots=0 未测 TP 保护机制 + dev-reviewer 不稳定（同候选 50/50）+ n=5 不显著；可靠发现是 dev-reviewer TP recall 低（20-60%），论文聚焦 CTS 核心 |
| 10 | 分类法主参考 | B(2502.20812 roadmap) 主、A(2506.02617) 辅 | B 给 clean 数字(23.1/43/9.3/9.7)+预背书 oracle gap；A 退为印证+pattern 词汇；4 类为 compliance 维度轴投影到 B symptom 轴；不再说"占绝大部分" |
| 11 | 系统身份 | **边界/校验合规检测器（兼诊断/状态）** | 36 TP title-based 分布：边界75%/诊断8%/状态6%/崩溃3%/结果正确性8%；非均衡四型 |
| 12 | 贡献 #4 契约幻觉 | **复活**（12 BY_DESIGN 实锤） | 12/48=25% 提交被维护者判"契约过严"（幂等/最终一致/宽松默认/命名宽容），即契约幻觉直接观测 |
| 13 | crash 定位 | **设计性排除**（L1 gate），与 vdbfuzz 互补 | 36 TP 仅 1 崩溃；近零重叠是设计使然；不声称"优于"，声称"覆盖它测不到的那类" |
| 14 | 文献格局 | A/B/VDBFuzz **同一组** | Shenao/Haoyu Wang + Hou/Zhao/Xie；统治议程；niche 开但 scoop 风险最高档；投稿前扫该组近 12 月 |
| 15 | 待补实验 | 强模型重跑 48 issue 分诊（**记录，暂不跑**） | 验证去假阳性机制：dev-reviewer TP召回 vs FP抑制；12 BY_DESIGN 多为机制引入前+glm4.7 跑出 |
| 16 | 计数对齐 + precision 重算 | **已完成**：108/32 → 111/36（28 fixed+8 accepted）；precision 分母=acknowledged+by_design+REJECTED=36+12+4=52，36/52=69.2%（原 72.7% 基于 32/44 排 REJECTED），5.4×；12.9%(4/31)/80.6%(25/31) 为 milvus 消融不动 |

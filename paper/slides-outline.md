# TestVDB 汇报 PPT 大纲（审稿版）

> 主参考 **IsoRel (ISSTA'25)**，借 **GEAR (ICSE'25)** 两招。
> 目标：**34 页 / 20 min**。标注 [可裁] 的页可合并以压到 28 页。
> 论文当前 **只有 3 个 Table、无 Figure**——本文末尾列出需新画的图。

---

## 一、设计取向（为什么这样排）

| 论文要素 | PPT 怎么处理 | 仿照 |
|---|---|---|
| Table 1（6 类 oracle 为何 miss documentation-implementation） | **拆成 naive 方案逐一否证**（3-4 页） | GEAR S5-S8 |
| 两层错误（family-specific / task-intrinsic） | **对称分页**（概念页 + 对比页） | IsoRel S17-S22 |
| 29-clause probe, 3 subtypes (Table 3 + text) | **表格驱动**单页 + 详讲 | IsoRel S40-S46 |
| 5-stage pipeline | **渐进式 3 页**长出总览图 | GEAR S10-S12 |
| 4 个 RQ | 每 RQ 1-2 页，RQ3 作决定性证据 | IsoRel S36-S48 |

## 二、贯穿全程的风格规则（来自 IsoRel/GEAR）

1. **标题写结论断言**，不写名词。例：不写 "Differential Testing"，写 "Differential testing cannot adjudicate accept/reject"。
2. **标题里塞数字**。例："37 of 38 defects do not crash"、"source suppresses 81% of false positives (31% → 81%)"。
3. **同类内容固定版式连放**（RQ2 的 ablation、naive 否证、两层错误）。
4. **表格优先于大段文字**；主角大图全场只 1-2 张。
5. **几乎不用截图**，全部 PPT 原生形状自绘（矢量、可改）。
6. 每页右上角放 **页码 + section 标记**（GEAR 风格）。
7. 结尾 **四宫格**回顾核心结果。

---

## 三、逐页大纲

> 列说明：**标题**（英文，结论式）｜**版式**｜**内容要点**｜**论文来源**｜**图**

### 第 0 段：开场（P1-P3）

| 页 | 标题 | 版式 | 内容 | 来源 | 图 |
|---|---|---|---|---|---|
| P1 | (标题页) | 居中 | Title + 作者 + 单位 + 会议(session TBD) | tex L11 | — |
| P2 | VDBMSs store the embeddings that retrieval-augmented LLMs depend on | SHAPE+小图 | RAG 架构里 VDBMS 的位置；DB-Engines/生态规模 | §1 引言 | RAG/VDBMS 架构示意图 [新画 #1] |
| P3 | VDBMS defects are costly, and most are functional | TBL+引用 | bugstudy: >50% functional；roadmap: ~43% 归为 incorrect behavior，oracle 是关键挑战 | §1 | — |

### 第 1 段：问题定义 + 真实案例（P4-P6）

| 页 | 标题 | 版式 | 内容 | 来源 | 图 |
|---|---|---|---|---|---|
| P4 | documentation-implementation defects: the API silently accepts what the docs prescribe rejecting | SHAPE+TBL | 定义 documentation-implementation vs correctness；accept/reject 违反文档 | §1, §2 | — |
| P5 | A negative score threshold disables a filter and returns all matches | **TBL×2 前后对比** | **3 连案例**：`nprobe=0`、`ef=0`、负 score threshold——文档 vs 实际行为对照 | §1, abstract | 案例对照表 [新画 #2] |
| P6 | 37 of 38 acknowledged defects do not crash, so fuzzers miss them | 大字数字 | crash oracle 到不了；motivate 语义 oracle 的必要 | §1, Table 1 row 1 | — |

### 第 2 段：naive oracle 逐一否证（P7-P10）— 核心动机，仿 GEAR

> 把论文 Table 1（tab:exclusion）拆成"每种 oracle 为何到不了 documentation-implementation residual"。每页一种，版式相同：左 oracle 定义、右 为什么 miss。

| 页 | 标题 | 版式 | 内容 | 来源 |
|---|---|---|---|---|
| P7 [可裁] | Differential testing cannot adjudicate accept/reject | 双栏 | cross-vendor accept/reject 设计上就分叉，无 documentation-implementation reference；roadmap 也标 challenging | Table 1 row 2 |
| P8 [可裁] | Metamorphic relations are output relations, not input-acceptance transforms | 双栏 | MR 管 top-k 单调性/recall，不管 accept/reject | Table 1 row 3 |
| P9 [可裁] | Property-based testing needs a schema VDBMSs do not serve | 双栏 | 需要 machine-checkable property + OpenAPI；VDBMS 多数无 schema，部分无 OpenAPI | Table 1 row 4 |
| P10 | The documentation-implementation residual leaves only an LLM as the practical oracle | **Table 1 收尾页** | 6 行 oracle 对照表完整呈现，高亮 row 6 | Table 1 全表 |

### 第 3 段：核心 insight + 两层错误（P11-P15）— 全文最关键，仿 IsoRel 对称分页

| 页 | 标题 | 版式 | 内容 | 来源 | 图 |
|---|---|---|---|---|---|
| P11 | But an LLM oracle is unreliable in two distinct ways | 预告页 | 抛出"两层错误"框架，引出可靠性问题 | §3 | — |
| P12 | The source-ambiguity gap: structured sources yield assertions, ambiguous docs yield claims | **概念图** | 低歧义源（OpenAPI/trace/source）→ 可靠 assertion；自然语言文档 → 可能错的 claim。这是与 REST oracle 工作的分界 | §3 | **source-ambiguity gap 概念图 [新画 #3]** |
| P13 | Family-specific errors: the judge confirms the extractor's biases | 概念页(a) | self-preference；cross-model validation 可解 | §3 | — |
| P14 | Task-intrinsic errors: different families infer the same wrong claim | 概念页(b) | 文档本身歧义；cross-model 解不了。**脚注/小字**：task-intrinsic 是 extraction-level across-families 稳定性，distinct from intra-judge across-runs 噪声（Haldar Rating Roulette）—— 防御审稿 "stable across runs" 误读 | §3 + §7 LLM-judge reliability | **两层错误覆盖图(Venn) [新画 #4]** |
| P15 | Cross-model validation covers family-specific, not task-intrinsic | 对称对比 | 两种解法的覆盖范围对照 | §3 | 同 #4 |

### 第 4 段：决定性证据（P16-P17）— 仿 IsoRel 表格驱动

| 页 | 标题 | 版式 | 内容 | 来源 |
|---|---|---|---|---|
| P16 | On 12 over-strict parameter clauses (9 Milvus + 3 Qdrant): cross-model catches 7, source catches 12 | **Table 3(tab:e2) 主体** | 12 行 clause 表（参数子类），TI 标注，cross-model vs source 两列；高亮 2 个 TI 行被 cross-model 漏掉；页角标注 "extended to n=29 (behavior + explicit-bound, see P29)" | Table 3, §3, §6.3 |
| P17 | The task-intrinsic residual requires a source of actual behavior — the implementation | 文字+小图 | 过渡到方法：source = 实现 | §3 末 | — |

### 第 5 段：方法（P18-P21）— pipeline 仿 GEAR 渐进式

| 页 | 标题 | 版式 | 内容 | 来源 | 图 |
|---|---|---|---|---|---|
| P18 | TestVDB instantiates source-grounded falsification | **总览图 1/3** | pipeline 前 2 步：LLM 提取 claim → attack agent 生成边界输入 | §4 | **pipeline 图(分 3 段画) [新画 #5]** |
| P19 | The dev-reviewer falsifies LLM verdicts against source | 总览图 2/3 | + LLM oracle 判断 → dev-reviewer 用 source 证伪 | §4 | 同 #5 |
| P20 | A novelty gate removes duplicates and known issues | 总览图 3/3 | + novelty gate；完整 5-stage pipeline 亮相 | §4 | 同 #5 |
| P21 | The falsification rule: if source shows `shardsNum=0` selects the default, the over-strict clause is falsified | 代码/TBL | 用 shardsNum 例子讲证伪规则；强调与 MASTOR 反向 (as currently designed) | §4 | — |

### 第 6 段：dev-reviewer 细节（P22）[可裁]

| 页 | 标题 | 版式 | 内容 | 来源 |
|---|---|---|---|---|
| P22 | Three anchors: clean reproduction, source-grounded (primary), threat-model cross-check | 流程图 | dev-reviewer 三 anchor 分工 | §4 | 三 anchor 流程图 [新画 #6] |

### 第 7 段：实验（P23-P31）

| 页 | 标题 | 版式 | 内容 | 来源 |
|---|---|---|---|---|
| P23 | Four research questions | TBL | RQ1 yield/residual、RQ2 source 抑 FP、RQ3 cross-model vs source、RQ4 model-free subclass | §6 开头 |
| P24 | Five VDBMSs; 111 submitted, 38 acknowledged | **Table 2(tab:yield)** | per-VDBMS submitted/acknowledged；Milvus+Qdrant 是统计主力 | Table 2 |
| P25 | ~85% of submitted issues are documentation-implementation defects classical oracles cannot reach | 饼图/条 | fault model 分类：~85% documentation-implementation (**composition, not prevalence**)、~10% classical、~5% concurrency；ack 子集 89% | §6.1 |
| P26 | On Qdrant v1.18.2: We ran VDBFuzz: 26,000 requests, 0 crashes; TestVDB found documentation-implementation defects | **双栏对比** | head-to-head；两工具 oracle 在不相交的 defect class 上 | §6.1 |
| P27 | The source anchor suppresses 81% of false positives (up from 31%) at 96.7% TP | 大字数字+小表 | RQ2 主结果；retrospective n=54 | §6.2 |
| P28 | Precision scales with the source anchor: 25.5% → 45.6% → 69.2% | **柱状图** | ablation：single-LLM → +1 source cycle → full multi-agent+source | §6.2 | ablation 柱状图 [新画 #7] |
| P29 | RQ3 at n=29: source catches all 16 over-strict; 0/13 on explicit bounds; cross-model κ=1.0 on 20 dev-review verdicts | **3-subtype 表 + 双数字** | (1) parameter over-strict 5/12 TI；(2) behavior over-strict 4/4（by-design issues，跨类型）；(3) explicit-bound negative 0/13（specificity）；within-vendor contrast：optional-default 56% vs explicit-bound 0%（DeepSeek 独立验证 falsifiable prediction）；+ W3 cross-model：DeepSeek 双盲审 20 candidates，5 subtypes，Cohen κ=1.0（dev-reviewer 不 family-specific） | §6.3 + Threats, Table 3 |
| P30 | A model-free invariant subclass finds bugs on its own | TBL | RQ4：COSINE bound / index 返回 2/25 / filter miss field；跨 Milvus+Qdrant | §6.4 |

### 第 8 段：定位 + 收尾（P32-P34）

| 页 | 标题 | 版式 | 内容 | 来源 |
|---|---|---|---|---|
| P31 | Prior work stays in low-ambiguity sources; TestVDB enters the ambiguous regime | **定位表** | vs AGORA+/SATORI/MASTOR（REST）、Toradocu/Doc2OracLL/AugmenTest/Konstantinou/ChatAssert/Testora（doc）、NoREC/TLP/DDLCheck（DB correctness）；突出 MASTOR (as currently designed) 反向用 source | §7 |
| P32 | Threats: the over-strict subset (n=16) is the most contingent finding; the mechanism is correlative, not causal | 文字 | 内部效度（over-strict subset 最 contingent）、外部（统计 claim 限 Milvus+Qdrant）、构造（mechanism correlative — within-vendor contrast + falsifiable prediction 验证但非 causal）；诚实标注 | §6 威胁, §8 |
| P33 | The boundary between extractable and interpretable is where LLM-dependent testing is heading | 结论文字 | 总结 + 可迁移性（REST 无 OpenAPI、配置校验等） | §9 |
| P34 | (结论页) | **四宫格 PIC×4** | 4 张结果回顾：85% residual / 81% FP 抑制 / n=29 TI (56% vs 0% contrast) + κ=1.0 cross-model / 111-38 yield + 代码链接 | — | 四宫格 [新画 #8] |

---

## 四、需要新画的图（论文当前 0 figure）

按优先级：

| # | 图 | 用在 | 难度 | 说明 |
|---|---|---|---|---|
| **5** | **5-stage pipeline 总览图**（分 3 段渐进） | P18-P20 | 中 | **最核心**。GEAR S10-S12 风格，分 3 页亮出 |
| **3** | **source-ambiguity gap 概念图** | P12 | 中 | **核心 insight 的可视化**，论文最该有的一张图。横轴=源歧义度，纵轴=claim 可靠性 |
| **4** | **两层错误 Venn/覆盖图** | P14-P15 | 中 | family-specific（cross-model 覆盖）vs task-intrinsic（只有 source 覆盖） |
| 1 | RAG/VDBMS 架构示意 | P2 | 低 | 背景 |
| 2 | 真实案例对照表 | P5 | 低 | nprobe=0 等，做成文档 vs 实际两栏 |
| 6 | dev-reviewer 三 anchor 流程 | P22 | 低 | 可裁 |
| 7 | ablation 柱状图 | P28 | 低 | 3 根柱 |
| 8 | 结尾四宫格 | P34 | 低 | 复用前面结果图 |

### 核心图（#3 / #4 / #5）具体图例（真实 TestVDB parameter，详见 `figures-design-notes.md`）

**#3 source-ambiguity gap**（左右分屏，transcribe vs interpret）
- 左半（冷色蓝绿，LLM **transcribe** → 可靠）：3 张结构源卡 —— OpenAPI `limit: minimum 1` / execution trace / source code → assertion `limit >= 1`
- 右半（暖色橙红，LLM **interpret** → 可能错）：Milvus doc `shardsNum (int, optional, default 1)` → GLM 提取 `shardsNum >= 1`（over-strict）vs 实际 `0` 选 default
- 中间：锯齿裂缝 + 大字 **SOURCE-AMBIGUITY GAP**

**#4 两层错误 Venn**（每圈一个 probe 对比卡，关键：说法不同 vs 说法相同）
- 左圈 **family-specific**（`consistencyLevel`，self-preference）：GLM 判"违规" vs DeepSeek 判"OK" → **说法不同** → cross-model validation 覆盖
- 右圈 **task-intrinsic**（`timeout`，doc ambiguity）：GLM 和 DeepSeek **都提取 `timeout >= 1`（同错）** → cross-model 解不了 → source-grounded falsification 解
- 脚注：task-intrinsic 是 extraction-level across-families 稳定性，distinct from intra-judge across-runs 噪声（Haldar, Rating Roulette）

**#5 pipeline**（用 `shardsNum=0` 一个 candidate 串 5 stage，每 stage 下方挂数据卡）
- S1 doc `shardsNum (optional, default 1)` → clause `shardsNum >= 1`
- S2 attack → boundary input `shardsNum=0`
- S3 LLM judge → API 200 → verdict "违规（should reject）"
- **S4 dev-reviewer（高亮绿）**：source `if shardsNum == 0 { shardsNum = default }` → **FALSIFY over-strict clause → FP killed**
- S5 novelty → dedup
- 视觉反差：S3 红"违规"被 S4 绿"falsified"推翻 —— 这就是 source-grounded falsification 的价值

**配色统一**：蓝（family / structured / transcribe）+ 橙（intrinsic / ambiguous / interpret）+ 绿（source 正解）+ 红（错误 / over-strict）。三张图逻辑：**#3 why**（doc 为何不可靠）→ **#4 what**（两层错误）→ **#5 how**（pipeline 怎么解）。

**#5 和 #3 是必须有的**——它们承载方法和核心 insight，没有图就只能念字。建议下一步先画这两张。

---

## 五、待你拍板的决策点

1. **页数**：34 页够不够？还是要压到 28（裁 P7-P9 之一、P22、合并 P25-P26）？取决于会议时长（ISSTA/FSE 一般 20min）。**注**：P29 已合并 W3 κ + within-vendor contrast evidence，不新增页；RQ3 加强后若需压页，优先裁 P7-P9（naive 否证）之一。
2. **真实案例（P5）**：用 `nprobe=0`/`ef=0`/负 score threshold 这三个？要不要带上具体 GitHub issue 链接？论文里没写 issue 号，需要你确认能不能公开。
3. **~~9-clause probe 的定位~~** ✅ **已解决**（2026-07-18）：probe 已扩到 **n=29（3 subtypes）**，加 within-vendor contrast（optional-default 56% vs explicit-bound 0%）+ specificity check (0/13) + cross-model κ=1.0 (n=20)。**高调当决定性证据**——round 12 mock review R2 正因此升 4，不再有 pilot 风险。P29 已按此重写。
4. **两层错误可视化**：Venn 图（#4）还是纯对称分页？Venn 更直观但要画。
5. **对比页（P31）打谁**：重点对比 MASTOR（最近、都用 source）？还是均匀铺开？
6. **下一步**：审完大纲后，要我 (a) 生成 8 张图的草图（python/matplotlib 或直接描述画法），还是 (b) 用 python-pptx 生成 .pptx 骨架文件（套好 IsoRel 版式，你填内容）？

# Mock Review Report: TestVDB

> **Target Venue:** 未定的 ACM 会议，按顶会 SE 测试类标准评审（ICSE / FSE / ISSTA / ASE 档）
> **Overall Prediction (Round 1, 原稿 `paper-draft-vldb.tex`):** Weak Reject / Major Revision
> **Overall Prediction (Round 2, 修订稿 `paper-draft-vldb-revised.tex`):** Borderline / Major Revision — 三个致命定量问题已消除，剩余为实证成熟度与投稿硬件（bib/图/方法细节）
> **Date:** 2026-07-10（Round 2 更新）

说明：目标会议尚未锁定。若最终投 DB 类会议（SIGMOD / VLDB），评审会更看重与向量检索系统内部机制、召回率量化的对接；若投 SE 测试类会议，则更看重 oracle 设计的新颖性与实证规模。本报告按 SE 测试类会议标准撰写。

---

## Score Summary

| Dimension | R1 (客观) | R2 (严格) | R3 (友好) |
|-----------|:---------:|:---------:|:---------:|
| Soundness | 2/4 | 1/4 | 3/4 |
| Novelty | 3/4 | 2/4 | 3/4 |
| Presentation | 2/4 | 2/4 | 3/4 |
| Overall | 4/10 (Weak Reject) | 3/10 (Reject) | 6/10 (Weak Accept) |

三位审稿人共识：核心想法（用维护者权威作为独立真值层，去证伪 LLM 生成的契约判断）是有价值的，但当前稿件实验未完成、关键对比是跨口径拼接、核心机制召回率偏低且样本量不足。这是一份很有潜力但尚未成熟的草稿。

---

## Round 2 修订核对（against `paper-draft-vldb-revised.tex`, 2026-07-10）

针对 Round 1 的意见逐条核对修订稿的落实情况。**结论：三个会致命的定量问题全部解决，稿件从「结构性硬伤」降级为「实证成熟度不足」，投稿判断由 Weak Reject 上移到 Borderline。** 但仍有两类问题挡在录用线前：一类是写作硬件（bib 空、图占位、方法细节薄），另一类是无法靠改写解决的实证短板（TP 召回 20–60%、无 VDBFuzz 实测对比）。

| # | Round 1 意见 | 状态 | 证据 |
|---|---|---|---|
| P0-1 | 5.4× 跨口径拼接 | ✅ **已解决** | 主对比改为同总体 Milvus v2.6.19：12.9%(4/31)→66.7%(4/6)=5.2×；69.2%(36/52) 单列为五库 aggregate，不再相除（§5.3、abstract、§1、贡献#2、结论联动一致）|
| P0-2 | 精度分母选择偏差 | ✅ **已解决** | §5.3 加 pending 敏感性 [43.9%, 80.5%]，69.2% 标为已裁决点估计；abstract/Threats 同步 |
| P0-3 | 实验未收口 | ✅ **已解决（改为范围限定）** | 删除 in-progress 措辞；Weaviate 未诊断项明确「excluded, not an in-flight claim」，只报已完成测量 |
| P1-a | RQ4 null result 列为贡献 | ✅ **已解决** | RQ4 retitle 为「Exploratory, not a contribution」，明确不作正向主张；贡献从 6 条压到 4 条 |
| P1-b | 贡献/first 过多重叠 | ✅ **已解决** | CTS/counter-evidence/hallucination 三条合并；pilot 那条删除 |
| — | abstract「25% of submitted」口径错误 | ✅ **已修正** | 改为「12 of 48 adjudicated (25%)」，全文统一（12/111=11% 的误导消除）|
| P0-4 | 填充 references.bib | ❌ **未解决** | `references.bib` 仍为空，8 键无法解析；编译时引用显示 `[?]`。已在 tex 内留 TODO，但投稿前必须补 verified BibTeX |
| P0-5 | 方法可复现细节 + 真实框架图 | 🟡 **未解决（留 TODO）** | LLM backbone/版本、四判官与 dev-reviewer 判定规则、端到端样例走查仍缺；Fig.1 仍 `\fbox` 占位 |
| P1-c | VDBFuzz 实证对比 | 🟡 **部分（诚实降级）** | 已明说「head-to-head 对比是 future work」，不再把 near-zero overlap 当实测；但仍无同环境实测数据 |
| R2-W1 | TP 召回 20–60% 偏低、n=5 | ⚠️ **本质短板，无法靠改写解决** | 属机制固有限制，修订稿如实披露，但录用与否仍取决于评审是否接受「牺牲一半召回换精度」|

### Round 2 分维度评估（修订后）

| Dimension | Round 1 共识 | Round 2 修订后 | 变化说明 |
|-----------|:---:|:---:|---|
| Soundness | 2/4 | **3/4** | 致命的跨口径拼接消除，敏感性区间到位，主张限定在已完成子集 |
| Novelty | 3/4 | 3/4 | 未变（CTS 想法本身不受修订影响）|
| Presentation | 2/4 | **2–3/4** | 贡献精简、口径统一提升清晰度；但 bib 空 + 图占位 + 方法薄仍压分 |
| Overall | 4/10 | **5–6/10（Borderline）** | 跨过「结构性击穿」线，但未跨过「实证成熟」线 |

### 现在最挡路的三件事（按 gate 优先级）
1. **[投稿前硬门槛] 填 `references.bib`** — 空 bib 会让任何审稿人第一眼扣印象分；注意核验 venue（norec20 疑为 OOPSLA/PACMPL 而非 OSDI）。
2. **[投稿前硬门槛] 真实框架图 + 方法可复现段** — 至少补 LLM 版本、判定规则、一个端到端样例走查。
3. **[会被反复追问] TP 召回 20–60%** — 无法靠写作解决，但可加一段正面论证「在无 mechanical oracle 的场景下，高精度低召回的运营价值」，把限制转化为设计取舍的论证。

---

## Reviewer 1 — 客观审稿人
> Confidence: 4/5

**Summary**
本文提出 TestVDB，面向向量数据库系统（VDBMS）的 API 契约合规缺陷检测。核心贡献是 Contract-Truth Separation（CTS）：把 LLM 生成的契约与判断（断言层）和一个由维护者权威证据支撑的真值层分离，用后者证伪前者。作者报告在五个 VDBMS 上产出 111 个候选、36 个被维护者确认，端到端精度从 12.9% 提升到 69.2%。

**Strengths**
1. 问题定位准确：incorrect-behavior 缺陷占 43% 却缺少可用 oracle，是一个真实且被 roadmap 文献点名的空白。用「契约本身即 oracle」切入这个子集是合理且可操作的。
2. 作者对系统边界非常诚实：明确排除 crash、result-correctness，公开 TP 召回只有 20 至 60%，这种自我披露在测试论文里少见且值得肯定。
3. Table 1（oracle 候选排除表）逻辑清晰，把「为什么只能用 LLM」论证得干净。

**Weaknesses**
1. <span style="color:#dc2626">**[Major]**</span> **12.9% 与 69.2% 的对比是跨口径拼接。** 12.9% 是 Milvus 单库、Stage-2 原始候选上的 4/31；69.2% 是五库、仅在「已裁决」52 个提交上的 36/52，后者已经排除了 30 个 pending 和 29 个无标签/重复。两个数字的总体、分母、库范围都不同，直接相除得出的 5.4× 不成立。这是全文最核心的定量主张，却建立在不可比的两个数上。
2. <span style="color:#dc2626">**[Major]**</span> **精度分母存在选择偏差。** 精度只在 52 个已裁决样本上算，排除了 30 个 pending。维护者往往优先裁决明显是 bug 的提交，pending 里可能沉淀了大量弱候选；把它们排除会系统性抬高精度。Weaviate 提交 30 个里 21 个 pending，说明结果实际由 Milvus/Qdrant 主导。
3. <span style="color:#dc2626">**[Major]**</span> **实验在投稿时未完成。** RQ3 明文写「the 36-TP source-grounding ... is completing」，Threats 里写「Weaviate has 22 open undiagnosed」。审稿人无法评审一个还在跑的实验。
4. <span style="color:#d97706">**[Minor]**</span> 方法论述过于高层。四判官辩论、三个攻击 agent、novelty gate 都是段落级描述，缺少提示词设计、判定标准、失败模式，复现困难。用了哪些 LLM 只在 RQ3 顺带提了一次 GLM-5.2。
5. <span style="color:#d97706">**[Minor]**</span> 框架图是占位符（`\fbox` 手绘框），references.bib 为空，所有引用无法解析。

**Questions for Authors**
1. 能否在同一总体、同一分母上给出 dev-reviewer 前后的精度对比？例如都在 Milvus v2.6.19 的 31 个 Stage-2 候选上。
2. 30 个 pending 若最终判为无效，精度会掉到多少？给出敏感性区间。
3. 各阶段（4-judge、dev-reviewer、novelty gate）对精度提升各贡献多少？

---

## Reviewer 2 — 严格审稿人
> Confidence: 3/5

**Summary**
一篇 LLM 驱动的 VDBMS 契约合规测试论文，主张一个「真值层证伪断言层」的设计原则。想法不新奇到能自成范式，实证也未收口。

**Strengths**
1. 选题方向有现实意义，五个真实系统上确实拿到了维护者修复。

**Weaknesses**
1. <span style="color:#dc2626">**[Major]**</span> **核心机制召回率过低且样本无意义。** dev-reviewer 的 TP 召回是 20 至 60%，出自 n=5 的 pilot。一个漏掉 40 至 80% 真 bug 的检测器，其「高精度」很大程度是靠丢弃可疑候选换来的，精度-召回是被牺牲了一半的权衡。而且 20 至 60% 这个区间本身在统计上无意义。
2. <span style="color:#dc2626">**[Major]**</span> **RQ4 是一个 null result 却被包装成贡献。** 作者自己承认：blindspot 指标从未填充、机制未被测试、dev-reviewer 跨 run 不稳定、n=5 不显著。既然什么都没证明，为什么它是 contribution #5？这一节反而暴露了系统的不稳定性。
3. <span style="color:#dc2626">**[Major]**</span> **没有与 VDBFuzz 的实证对比。** 全文用「complementary, not competitive」回避对比，「near-zero overlap by design」是断言而非实测。审稿人需要看到在相同目标、相同版本上，TestVDB 找到的 bug 是 VDBFuzz 找不到的，且反之亦然。
4. <span style="color:#d97706">**[Minor]**</span> **概念包装过重。** Contract-Truth Separation 本质上是「用源码/历史去核实 LLM 的判断」；contract hallucination propagation 建立在 12 个 by-design 案例上，作者也承认「quantitative study is future work」，属于轶事级观察。给工程模式起大写术语名容易被质疑 novelty 灌水。
5. <span style="color:#d97706">**[Minor]**</span> 4 页篇幅列 6 条贡献、3 个「first」，其中 CTS 原则、counter-evidence 机制、hallucination finding 三条高度重叠。

**Questions for Authors**
1. 若把 TP 召回作为主指标，本系统相对「单层 LLM + 直接提交」的净收益是什么？
2. contract hallucination propagation 除了 12 个案例，有没有可复现的频率测量？
3. RQ4 既然不能得出结论，为什么不移出正文？

---

## Reviewer 3 — 友好审稿人
> Confidence: 4/5

**Summary**
一个我很想看到成功的方向。把维护者的裁决逻辑（源码定位、干净复现、by-design 意图）编码成一个独立真值 agent 去反驳 LLM 的判断，是对「LLM 自证」失败模式的一个聪明回应，而且拿到了 36 个真实确认，含跨厂商可复现的 COSINE 不变量违背，很有说服力。

**Strengths**
1. 真实世界影响力强：28 个已修复的 bug 是硬通货，跨 Milvus/Qdrant 的 COSINE>1.0 案例是漂亮的、可复现的、违背数学不变量的发现。
2. 诚实是加分项：作者主动划定边界、公开低召回、区分探索性 pilot 与核心主张，这种态度让结果更可信。
3. contract hallucination propagation 这个失败模式（生成契约的模型同时判断合规，幻觉被自我确认）观察得很到位，即使还只是定性的，也对社区有启发。

**Weaknesses**
1. <span style="color:#dc2626">**[Major]**</span> 定量对比口径需要统一（同 R1-W1），否则最亮的 5.4× 主张会被直接击穿，非常可惜。
2. <span style="color:#d97706">**[Minor]**</span> 方法细节太薄，建议补一个真实框架图和一个端到端的具体样例走查（一个 bug 从生成到提交的全链路）。
3. <span style="color:#d97706">**[Minor]**</span> RQ4 建议降级为附录或删除，避免削弱主线。

**Questions for Authors**
1. 能否把 COSINE 案例扩展成一个「可表达不变量」小类别，作为超越纯契约的第二个 oracle 维度？这可能是比 CTS 更有辨识度的贡献。

---

## Verification（回到原文逐条核实）

| # | Source | Claim | Verdict | Note |
|---|--------|-------|---------|------|
| 1 | R1-W1 | 12.9% 与 69.2% 口径不同 | <span style="color:#16a34a">**Valid**</span> | 12.9% = 4/31（Milvus 单库 Stage-2，见 §5.3）；69.2% = 36/52（五库已裁决，见 abstract 与 §5.3）。总体与分母确实不同 |
| 2 | R1-W2 | 精度分母排除 30 pending，存偏 | <span style="color:#16a34a">**Valid**</span> | Table 1 caption 明确「Pending = 30 … Precision computed over adjudicated (52)」，Weaviate 30 提交 21 pending |
| 3 | R1-W3 | 实验未完成 | <span style="color:#16a34a">**Valid**</span> | §5.3 原文「the 36-TP source-grounding … is completing」；Threats「Weaviate has 22 open undiagnosed」 |
| 4 | R2-W1 | TP 召回 20-60% 来自 n=5 | <span style="color:#16a34a">**Valid**</span> | §5.4 原文 n=5 TP、区间 20%/60%，作者自述「below significance」 |
| 5 | R2-W2 | RQ4 是 null result 却列为贡献 | <span style="color:#16a34a">**Valid**</span> | §5.4 与 contribution #5 均在，作者自承机制未测、不稳定 |
| 6 | R2-W3 | 无 VDBFuzz 实证对比 | <span style="color:#16a34a">**Valid**</span> | 全文仅概念性 complementarity（§5.1、§6），无同目标实测 |
| 7 | R1-W5 | references.bib 空、图为占位符 | <span style="color:#16a34a">**Valid**</span> | .bib 当前为空（引用无法解析）；Fig.1 为 `\fbox` 手绘 |
| 8 | R2-W4 | hallucination finding 仅 12 案例 | <span style="color:#d97706">**Misleading**</span> | 属实但表述需平衡：作者本就标注为定性观察且「quantitative study is future work」，并非隐瞒，批评应聚焦「不宜作为独立强贡献」而非「造假」 |
| 9 | 潜在质疑 | 总数对不上 | <span style="color:#dc2626">**False**</span> | 核对一致：提交 111 = 51+26+30+3+1；Fixed 28 + Accepted 8 = 36 确认；52 已裁决 = 36+12(by-design)+4(rejected)；82 已归类 + 29 排除 = 111。数字账目自洽 |

---

## Action Plan

<span style="color:#dc2626">**Must Fix**</span> — 多人共识，不改大概率被拒（勾选状态对应修订稿 `paper-draft-vldb-revised.tex`）
- [x] **统一精度对比口径。** ✅ 已改为同总体 12.9%(4/31)→66.7%(4/6)=5.2×；69.2%(36/52) 单列为五库 aggregate。
- [x] **补精度敏感性。** ✅ §5.3 给出 [43.9%, 80.5%]，69.2% 标为已裁决点估计。
- [x] **收口实验或明确标注范围。** ✅ 删除 in-progress 措辞，Weaviate 未诊断项明确排除，只报已完成测量。
- [ ] **补方法可复现细节。** 🟡 未做，tex 内留 TODO：使用的 LLM 及版本、四判官/dev-reviewer 判定规则、端到端样例走查、替换占位框架图。
- [ ] **填充 references.bib。** ❌ 仍为空，8 键无法解析（编译引用显示 `[?]`），需补 verified BibTeX 后再投。

<span style="color:#d97706">**Should Fix**</span> — 容易被误解或削弱主线
- [x] **处理 RQ4。** ✅ retitle 为「Exploratory, not a contribution」，从贡献列表移除。
- [~] **加一段 VDBFuzz 实证对比或明确说明为何不可比。** 🟡 已诚实降级为 future work，不再当实测；但仍无同环境实测数据（评审会追问）。
- [x] **精简贡献与「first」措辞。** ✅ 6 条压到 4 条，CTS/counter-evidence/hallucination 三条已合并。

<span style="color:#6b7280"> **Optional**</span> — 锦上添花
- [ ] 把 COSINE>1.0 这类「可表达不变量」发展成第二个 oracle 维度的小节，可能比 CTS 更有辨识度。
- [ ] abstract 与 intro 目前数字密度过高，可读性受影响，建议把部分定量细节下沉到正文。
- [ ] 确认目标会议后按其 rubric 复核（DB 会议会追问 ANN 召回/排序的量化，SE 会议会追问 oracle 设计与实证规模）。

---

### 我的整体判断

**Round 1（原稿）：** 核心 idea 站得住，但有三个会直接致命的问题：(1) 头号定量主张 5.4× 是跨口径拼接；(2) 核心机制召回率低且样本量不足；(3) 实验在截稿时未收口。判断 Weak Reject。

**Round 2（修订稿 `paper-draft-vldb-revised.tex`）：** 三个致命问题里，(1) 和 (3) 已通过改写彻底解决——5.4× 换成同总体 5.2×，敏感性区间到位，实验范围明确限定在已完成子集；连带修掉了 abstract「25% of submitted」的口径错误。(2) 是机制固有短板（TP 召回 20–60%），无法靠改写解决，但修订稿如实披露。**净结果：稿件从「结构性击穿」上移到 Borderline / Major Revision。** 现在真正挡在录用线前的，是两件投稿硬件（`references.bib` 仍空、框架图仍占位、方法细节薄）和一个实证短板（无 VDBFuzz 同环境实测）。前者是纯执行、几小时内可清；后者需要一段把「高精度低召回」讲成设计取舍的正面论证，或补一轮实测。把这两块补上，这篇有机会从 borderline 往 accept 一侧走。

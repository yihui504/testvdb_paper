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

## Round 3 详细审阅（against `paper-draft-vldb-final.tex` + `RESPONSE-to-reviewers.md`, 2026-07-10）

**判断：Borderline / Weak Reject（顶会 SE 档），Weak Accept（扎实的二档）。** Round 1–2 那些会致命的「表述硬伤」基本清除；现在卡住的不再是诚实度，而是**评估完整性**——论文能证明「提交的假阳性少」，但没证明「漏了多少真 bug」，且**没有任何外部 baseline**。这个天花板与写作打磨无关。

### [P0] 机械阻断项（仍在文件里，几分钟可修）
1. **Intro 与 abstract 自相矛盾。** abstract/贡献/RQ3/结论已换成新口径（FP 抑制 31%→81%、recall 96.7%），但 Intro 的 Results 段（line 119）仍是旧的「precision 12.9%(4/31)→66.7%(4/6)，5.2×」。同一篇里两个头号数字，审稿人第一页就撞见。
2. **投稿的 tex 指向空 bib。** `paper-draft-vldb-final.tex` 在 `files/` 根目录，`\bibliography{references}` → `files/references.bib` 仍为空；填好的 8 条在 `files/paper/references.bib`。在 tex 所在目录编译，所有 `\cite` 出 `[?]`。回复信「0 undefined」只在 `files/paper/` 内成立。
3. **虚构合著者。** `du2023improving` 多列了第 6 作者「Pieter Abbeel」；原文只有 5 位（Du/Li/Torralba/Tenenbaum/Mordatch）。删。

### [P1] 审稿人不会放过的评估缺口
4. **无端到端 recall——核心科学空洞。** 卖点是 precision，但没估计漏掉多少可发现的合规缺陷。新的 96.7% 是对**已被确认的 36 个 TP** 复判得到的，即「已抓到的 bug 上的召回」。这是判断层稳定性的合理陈述，但回复信称其「消除」召回担忧属**过度声称**：它对「从未被 surface 的 bug」一无所知。需要 recall 分母实验（如喂一批已知已修的合规 bug，测重发现率）。
5. **完全没有外部 baseline。** VDBFuzz 无实测可理解（paywall/无预印本，oracle 定义 + `run.py` 源码自证 crash-only 可作复现替代，保留）；但也没有「单层 LLM 全提交 + 真实维护者裁决」的 baseline，没有人工/启发式 baseline。唯一对照是自家 retrospective ablation。顶会没有任何 pipeline 外 baseline 是硬伤。
6. **precision 头号数字只靠 5 库里的 2 库。** yield：Milvus 51 + Qdrant 26 = 77/111；Weaviate 30 提交里 21 pending，MeiliSearch 3、Chroma 1。「across five VDBMSs」夸大了，已裁决 precision 实质是「Milvus + Qdrant 上的 precision」。[43.9%, 80.5%] 敏感区间已暴露对 Weaviate pending 的依赖。
7. **threat-model prior：架构里承重，评估里被否。** §3.2 说 threat model 注入「generation / judgment / dedup」，写成工作组件；RQ4 又说从未填充、未测、不稳定。§3.2 和 §5.4 描述的是两套系统。要么在 Approach 降级为「一个未能验证的 optional prior」，要么从数据流里拿掉。
8. **`norec20` 是错标引用。** 正文「NoREC tests SQL via pivoted query synthesis」；bib 条目标题是 *Testing Database Engines via Pivoted Query Synthesis* = **PQS**（OSDI 2020，另一篇 Rigger & Su）；NoREC 是 non-optimizing reference engine（ESEC/FSE 2020）。回复信 §2 又说「OOPSLA/PACMPL 2020」，三处互不一致。定一篇，让 key + 正文名 + venue 对齐。另核 `ddlcheck25` 页码（自承估计值）与 `buzzbee24` 的 `and others`。

### [P2] 加分项
9. **COSINE>1.0 是最亮的技术点却被埋。** 跨厂商、与硬件无关、违背数学不变量、Milvus+Qdrant 双库复现——比「CTS 作为原则」更新颖更站得住。建议把「可表达不变量」提升为第二个 oracle 维度小节，区别于「LLM 查 LLM」。
10. **指标切换需明说。** RQ3 从 precision lift 换成 FP 抑制 + recall（更干净，我认可），但跨版本对比的审稿人会注意到，加一句说明即可。
11. **abstract 数字过密。** results 一句塞 5 个统计量，把敏感区间和 n=30 下沉到 §5.3。

### 确实变好的
- 内部账目自洽：52 = 36 TP + 16 FP，16 = 12 by-design + 4 rejected，111 = 52 + 30 pending + 29 excluded。
- Fig.1 换成真 TikZ 图（assertion/truth 双层配色），占位框消除。
- 加了 implementation 段（agent 分层、GLM-5.2、四判官轴），补上可复现缺口。
- 诚实度高（明确边界、披露低产库、RQ4 标为 negative result），审稿人会给分。
- 28 个真实落地修复仍是最强资产。

### 给作者的问题
1. 端到端 recall 的最佳估计是多少？用一批已修合规 bug 做 held-out，报重发现率。
2. 「单层 LLM 全提交」在真实维护者裁决下的 precision 到底是多少（不是回溯，是实际提交）？
3. 去掉 Milvus + Qdrant，其余三库还有信号吗？
4. threat-model prior 到底在不在部署 pipeline 里？未测为何进架构图数据流？

### 下一步（按优先级）
1. 修三个 [P0] 机械项（Intro 数字对齐、bib 放到 tex 旁、删虚构作者），重编译验证 0 undefined。
2. 调和 §3.2 与 §5.4 对 threat model 的口径（纯一致性，无需新实验）。
3. 若截稿前有时间，补 recall 分母实验——这是唯一能真正移动结论的补充。
4. 修 `norec20` 引用身份。

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

---

## Round 4 详细审阅（against `paper-draft-vldb-final.tex` 最新版, 2026-07-11）

**判断：Borderline，偏 Weak Accept（顶会 SE 档 ICSE/FSE/ISSTA/ASE）；次级会议 Weak Accept ~ Accept。** 相比 Round 3 又往上挪小半档。表述硬伤（Round 3 的三个 [P0]）已全部落地修复；现在卡评级的是**评估闭环**（缺外部 baseline、discovery recall 只探到上游）和**几处对不上的账**。本轮重点做了内部数字核实，核出两个 Round 3 未暴露的问题。

### 相比 Round 3 的变化（delta）

| Round 3 问题 | 本轮状态 | 证据 |
|---|---|---|
| [P0] Intro 数字与 abstract 打架 | ✅ 已修 | 全篇统一为「FP 抑制 31%→81%、TP recall 96.7% (n=30)」；旧 5.2× 降级为 §5.3 directional support |
| [P0] 投稿 tex 旁 bib 为空 | ✅ 已修 | 根目录 `references.bib` 现有全部 8 条 |
| [P0] `du2023improving` 虚构作者 Abbeel | ✅ 已修 | 作者列已为 Du/Li/Torralba/Tenenbaum/Mordatch，与 arXiv:2305.14325 一致 |
| [P1] `norec20` 引用身份错标 | ✅ 已修 | bib 改为 Rigger & Su, ESEC/FSE 2020；正文描述从错误的「pivoted query synthesis」改为正确的「non-optimizing reference engine construction」 |
| [P1] 无 recall 分母 | 🟡 部分 | 新增 discovery recall 上游探针（9 个 held-out pre-2024 bug，文档覆盖 6/9=67%），并诚实标注只测抽取上游、非全链路 |
| [P1] 无外部 baseline | 🟡 部分（诚实降级） | 新增 within-system baseline 段，主动把「缺 end-to-end 外部 baseline」标为 threat to validity |
| [P1] threat-model 架构承重却被否 | ✅ 口径统一 | §3.2 改为「designed, not validated，unvalidated optional prior」 |
| [P0] 框架图占位 / 方法细节薄 | ✅ 已修 | Fig.1 换成真 TikZ（assertion/truth 双层）；新增 Implementation 段 |

### Verification（本轮回原文逐条核实的账）

| # | 位置 | 断言 | 判定 | 说明 |
|---|------|------|------|------|
| 1 | Tab.2 caption / §5.3 | 「111 投稿，52 已裁决，30 pending」 | <span style="color:#dc2626">**False（正文不闭合）**</span> | 按正文文字：52 + 30 = 82，111 − 82 = **29 个投稿正文未交代去向**。账可以closed（52 + 30 pending + 29 excluded = 111），但论文正文从未写出这个分解；且「30 pending」无法从 Tab.2 反推（Milvus+Qdrant 的可诊断 pending 由表算是 17+12=**29**，off-by-one），敏感性区间 [43.9%, 80.5%] 的分母 provenance 因此不可验证 |
| 2 | §3 Implementation (l.169) | 「four use the opus tier … sixteen use sonnet; all runs use GLM-5.2」 | <span style="color:#d97706">**Misleading（读起来自相矛盾）**</span> | opus/sonnet 与 GLM-5.2 分属不同模型体系；若 opus/sonnet 是当"能力档位"泛称、GLM-5.2 是真实 backbone，则不矛盾但措辞误导，审稿人会当成复制粘贴没改干净，直接影响可复现性打分。需作者澄清真实模型配置 |
| 3 | §5.5 Within-system (l.280) | claim-only 33/44=75% vs source-grounded 29/32=91%，「same 52-candidate pool」 | <span style="color:#d97706">**Misleading**</span> | 33/44 的 TP 基数是 36（claim-only 无需复现，覆盖全部 TP）；29/32 的 TP 基数是 30（source-grounded 受 rate-limit 只可达 30）。两条件 TP 分母不同（36 vs 30），「same population」措辞站不住，需脚注说明或统一基数 |
| 4 | 摘要 / §1 / §4 | 「12 of 48 substantively adjudicated」vs「52 maintainer-adjudicated」 | <span style="color:#16a34a">**Valid 但易误读**</span> | 48 = 36 ack + 12 by-design（不含 4 rejected）；52 = 48 + 4。定义自洽，但 substantively/maintainer 两词区分太隐蔽 |
| 5 | §5.3 敏感性 | (36+30)/(52+30)=80.5%，36/82=43.9% | <span style="color:#16a34a">**Valid**</span> | 区间算术在「30 pending」前提下自洽（但前提本身见 #1）|
| 6 | §5.1 缺陷分布 | 27+3+2+1+3=36，各百分比 | <span style="color:#16a34a">**Valid**</span> | 求和与百分比均对 |
| 7 | §5.3 回溯 | 5/16→13/16（31%→81%），29/30=96.7% | <span style="color:#16a34a">**Valid**</span> | 自洽 |
| 8 | Tab.2 汇总 | 111=51+26+30+3+1；36=28+8；52=36+12+4 | <span style="color:#16a34a">**Valid**</span> | 表内列和一致 |

### 主要弱点（Round 4，按严重度）

<span style="color:#dc2626">**[Major] W1 — 投稿总数账目在正文里不闭合。**</span> 正文只说 52 已裁决 + 30 pending，剩 29 个凭空消失；且「30 pending」不能从 Tab.2 反推（表算 Milvus+Qdrant pending=29）。审稿人会要一张 per-system `submitted = adjudicated + pending + excluded` 对账表。修法需作者确认真实 pending/excluded 拆分（涉及敏感性分母，不能凭表臆断）。

<span style="color:#dc2626">**[Major] W2 — 模型报告读起来自相矛盾。**</span> opus/sonnet/GLM-5.2 三者并列。需作者统一为真实使用的 backbone 名称+版本，去掉不属于该体系的档位词。直接关系可复现性打分。

<span style="color:#dc2626">**[Major] W3 — 缺端到端外部 baseline。**</span> 作者已诚实自认（§5.5 flag 为 threat）。但顶会需要「单层 LLM 直投 + 真实 maintainer 裁决」的对照，才能证明 dev-reviewer 的净收益。这是评级天花板，与写作打磨无关。

<span style="color:#d97706">**[Minor] W4 — within-system baseline 两条件 TP 分母不一致（核实 #3）。**</span> 加脚注说明或统一到 30 TP 基数重算。

<span style="color:#d97706">**[Minor] W5 — threat-model 是评估中的死重，却仍画在 Fig.1 主架构里。**</span> Fig.1 灰显/虚线标注「designed, not validated」，或从被评估系统剔除只在 future work 提。

<span style="color:#d97706">**[Minor] W6 — 泛化性证据薄。**</span> 聚合 69.2% 的 dev-reviewer 跨库验证只有 Milvus+Qdrant；「non-Milvus 0%→100%」n 极小；MeiliSearch(3)/Chroma(1) 近乎零样本。收敛「five VDBMSs」的泛化措辞。

<span style="color:#6b7280">**[Optional] W7 — COSINE>1.0 仍被埋在 §5.1 一句话里。**</span> 全篇唯一跨厂商复现的数学不变量违规，建议提为第二 oracle 维度或独立 case study。

<span style="color:#6b7280">**[Optional] W8 — 相关工作偏薄（仅 8 篇）。**</span> 顶会需与 LLM-based test oracle / spec mining / API misuse detection 定位对比，以支撑「first」。

### Action Plan（Round 4）

<span style="color:#dc2626">**Must Fix**</span>
- [ ] W1：Tab.2 补 Pending/Excluded 列，正文写出 111 = 52 + pending + excluded 的逐系统分解，明确敏感性「30」的口径（需作者确认真实拆分）
- [ ] W2：统一 §3 Implementation 的模型报告，消除 opus/sonnet 与 GLM-5.2 的矛盾（需作者确认真实配置）
- [ ] W4：给 within-system baseline 的 33/44 vs 29/32 补分母说明或统一基数

<span style="color:#d97706">**Should Fix**</span>
- [ ] W3：把 within-system 回溯讲成 dev-reviewer 净收益的主证据；外部 baseline 做不了则在 limitation 说透「为何现在做不了 + 何时能做」
- [ ] W5：Fig.1 灰显 threat-model 并标注未验证
- [ ] W6：收敛「five VDBMSs」泛化措辞，precision 泛化只 claim 到 Milvus+Qdrant

<span style="color:#6b7280">**Optional**</span>
- [ ] W7：COSINE>1.0 提升为独立 case study / 第二 oracle 维度
- [ ] W8：相关工作补 LLM oracle / API misuse / spec mining 定位

**Round 4 整体判断：** 叙事诚实度已不是短板，这版把 Round 1–3 最致命的口径/机械问题清干净了。评级天花板现在由两件事决定——(a) 能否补上哪怕一个像样的外部/近似 baseline，(b) 能否给 discovery recall 一个真实分母。这两件是「真功夫」，正是下一步补实验要解决的。W1/W2 是投稿前必须闭合的机械账，但都依赖作者的 ground truth，不能由审阅方臆造。

---

# Round 5 评审（against `paper-draft-vldb-final.tex`, 2026-07-11）

> 目标档次：顶会 SE 测试类（ICSE / FSE / ISSTA / ASE）
> **总体预测：Borderline 偏 Weak Reject** — 一个未闭合的账目错误直接动摇了摘要里的头号精度区间，不修会被严格审稿人一票拦下。

## Score Summary

| 维度 | R1（客观） | R2（严格） | R3（友好） |
|------|:--------:|:--------:|:--------:|
| Soundness | 2/4 | 1/4 | 3/4 |
| Novelty/Significance | 3/4 | 2/4 | 4/4 |
| Presentation | 2/4 | 2/4 | 3/4 |
| Overall | 4/10 (Weak Reject) | 3/10 (Reject) | 6/10 (Weak Accept) |

## Reviewer 2 — 严格审稿人（Confidence 4/5）

**Weaknesses**

1. <span style="color:#dc2626">**[Major]**</span> **W1 账目不闭合，头号精度区间用错分母。**

   **涉及位置（5 处联动）：**

   | 位置 | 行号 | 原文 |
   |------|------|------|
   | Table 2 caption | L242 | `"30 remain pending"` |
   | §5.3 敏感性 | L278 | `"30 further submissions remain pending"` |
   | 摘要 | L78 | `"30 pending submissions"` |
   | §1 Results | L119 | `"[43.9%, 80.5%] under pending-resolution sensitivity"` |
   | 结论 | L302 | `"within [43.9%, 80.5%] under pending sensitivity"` |

   Table 2（L245-257）逐行推算 pending（submitted 减去 fixed + accepted + by-design + rejected）：

   | VDBMS | Submitted | Adjudicated | **Pending（逐行推算）** |
   |-------|-----------|-------------|----------------------|
   | Milvus | 51 | 14+8+12+0 = 34 | **17** |
   | Qdrant | 26 | 11+0+0+3 = 14 | **12** |
   | Weaviate | 30 | 3+0+0+1 = 4 | **26** |
   | MeiliSearch | 3 | 0+0+0+0 = 0 | **3** |
   | Chroma | 1 | 0+0+0+0 = 0 | **1** |
   | **Total** | **111** | **52** | **59** |

   Table 2 自身的数据推出 pending = 111 - 52 = **59**，但 caption 和正文四处都写 **30**。这意味着 **29 篇投稿在论文里完全不存在**：既不在 52 个 adjudicated 里，也不在 30 个 pending 里。

   **连锁后果——精度区间全部作废：** L278 的敏感性计算用 30 pending 得到 worst=36/82=43.9%、best=66/82=80.5%。用真实 59 pending 重算：worst=36/111=**32.4%**、best=95/111=**85.6%**。下界从 44% 跌破 1/3，区间宽度从 36.6pp 拉大到 53.2pp。摘要（L78）、Introduction（L119）、结论（L302）四处全错。

   对一篇把「诚实报告选择偏差」当卖点（L278: "We report the interval rather than the point estimate alone to make the selection effect explicit"）的论文，自己的表格和文字对不上，不是 typo，是逻辑链断裂。R2 直接判 reject。

   **修复前提：** 需要作者确认 111 中 59 篇未裁决的真实 `pending / excluded` 拆分。

2. <span style="color:#dc2626">**[Major]**</span> **三个 CTS 锚点只验证了一个。**

   **涉及位置：**

   | 位置 | 行号 | 原文摘引 |
   |------|------|----------|
   | 贡献 #2 | L127 | `"falsifies them via three counter-evidence anchors"` |
   | §3.4 CTS 描述 | L213-217 | 列出三锚点：clean reproduction / source-grounded / threat-model |
   | 图 1 | L185-199 | TikZ 图中 `repro`、`src`、`tm` 三个 truth-layer 节点并列 |
   | §5.3 Anchor attribution | L284 | `"reproduction anchor requires a live VDB container and is not exercised in this retrospective"` |
   | §5.3 Anchor attribution | L284 | `"threat-model ... blindspot indicators were never populated"` |
   | §5.3 归因结论 | L284 | `"We therefore attribute the measured 81%/96.7% to the source anchor alone, treating reproduction and threat-model anchors as unmeasured future components"` |

   实际验证状况：

   | 锚点 | 设计了？ | 验证了？ | 效果数据 |
   |------|---------|---------|---------|
   | Source-grounding | 是 | **是** | FP 抑制 31%→81%，TP 保留 96.7% |
   | Reproduction | 是 | **否** | L284: "not exercised" |
   | Threat-model | 是 | **否** | L284: "never populated"；导致 3/16 FP 漏过 |

   Reproduction 锚点（L214）描述需 "build a minimal reproducer against a live VDBMS"，但回溯实验未启动容器，完全未执行。Threat-model 锚点（L217）描述 "match against known by-design intents"，但 blindspot indicators 从未填入；L284 明确指出 3 个漏过的 FP（"silent-absent cases"）**恰恰是** threat-model 本应拦截的——不仅未验证，还有反面证据表明其缺失直接导致系统性能损失。

   贡献 #2 headline 是「三锚点 CTS」，但实证只支持「source-grounding 有用」。三分之二机制无法验证甚至无法运行，框架层贡献退化为单点 trick 加两个 future work 占位。

3. <span style="color:#dc2626">**[Major]**</span> **无端到端外部 baseline。**

   | 对比 | 类型 | 位置 | 限制 |
   |------|------|------|------|
   | 75%→91% | 内部消融（同候选池两条件） | L280 | 分母不一致（见 R1-W2） |
   | 45.6%→69.2% | single-layer counterfactual | L282 | **跨总体拼接**：27 killed candidates 来自 Milvus dev-reviewer 运行，36/52 来自五库全集；两个总体 ground truth 来源不同（LLM+re-probe vs 维护者） |
   | VDBFuzz 对比 | 未做 | L262 | `"a head-to-head empirical comparison on identical targets is future work"` |

   L282 的 45.6% = 36/(36+16+27)，分母 79 混合了五库维护者裁决的 52 和 Milvus 单库 LLM 裁决的 27。这不是独立运行的 single-layer 结果，而是事后推算。

4. <span style="color:#d97706">**[Minor]**</span> 分母混乱（52/48/44/36/32/30/16）；ground truth 仅靠 maintainer acknowledgment，选择偏差；n=30、n=5、9 held-out、15 probes 样本量偏小。

**判断：Reject（3/10），W1 不修无讨论余地。**

## Reviewer 1 — 客观审稿人（Confidence 4/5）

**Strengths**
1. 问题框定与 contract hallucination propagation 是有价值的观察，12/48 by-design 佐证可信。
2. 真实世界影响过硬：5 个生产级 VDBMS、111 投稿、36 认可、28 修复。
3. Threats to validity 罕见坦诚。

**Weaknesses**

1. <span style="color:#dc2626">**[Major]**</span> 同 R2-W1：pending 与 Table 2 对不上，精度区间分母错误，必须先修。

2. <span style="color:#dc2626">**[Major]**</span> **Within-system baseline 两条件用了不同 TP 基数。**

   位置：L280，§5.3 Within-system baseline。

   原文：`"The claim-only condition ... lets 11/16 FPs through as judged-TPs, for a judgment-layer precision of 33/44 = 75%; the source-grounded condition lets only 3/16 FPs through (29/32 = 91%)."`

   精确拆解：

   | 条件 | FP passed | FP suppressed | TP passed | Total passed | Precision |
   |------|-----------|---------------|-----------|-------------|-----------|
   | Claim-only | 11 | 5 | **33** | 44 | 75% |
   | Source-grounded | 3 | 13 | **29** | 32 | 91% |

   问题在 TP 列：§5.3 开头（L270）明确写全集只有 36 TP，其中 6 TPs unreachable（API rate limits），可达 TP=30。Source-grounded 用 TP=29（可达 30 保留 29），但 claim-only 用 TP=**33 > 30**，数学上不可能——除非 claim-only 没做 rate-limit 过滤，用的是全部 36 TP 中的 33 个。

   如果两条件的 TP 分母不同（一个 36，一个 30），75%→91% 就不是 apple-to-apple 的比较——一边分母 44（36 基准 TP），一边分母 32（30 基准 TP），提升无法直接相减。

3. <span style="color:#d97706">**[Minor]**</span> **§3 Implementation 模型配置自相矛盾。**

   位置：L169。原文：`"four (orchestrator, dev-reviewer, threat-modeler, bug-shape-extractor) use the opus tier and the remaining sixteen use sonnet; all runs reported here use GLM-5.2."`

   这句话包含三个模型标识：opus（Anthropic Claude opus tier）、sonnet（Anthropic Claude sonnet tier）、GLM-5.2（智谱 Zhipu）。前半句 4 agent 用 opus、16 个用 sonnet（Anthropic 体系），后半句 "all runs use GLM-5.2"（智谱体系），三种可能的理解每种都有矛盾：(a) 如果都用 GLM-5.2 则 opus/sonnet 无意义；(b) 如果混用 Claude+GLM 则 "all runs" 与前半句矛盾；(c) 如果 opus/sonnet 是自定义 GLM 配置名则论文未说明。加上 TODO 注释（L31-32）也写 "State the exact LLM backbone + version"，说明作者自知未交代清楚。

4. <span style="color:#d97706">**[Minor]**</span> **Discovery recall 概念偷换。**

   位置：L286。测量的是「当前文档能否覆盖已知 bug 的契约」（6/9=67%），不是端到端召回率。三个额外问题：(a) 使用当前文档而非 bug 存在时版本，修复后措辞变化可能高估覆盖率；(b) 9 个 held-out 选自 pre-2024 但 LLM 训练截止日期未说明，可能有训练泄露；(c) "recall" 在论文中多义使用（§5.3 的 96.7% 是判断层 TP 保留率，这里是上游抽取率），同一术语指代不同概念。

**判断：Weak Reject（4/10），Major Revision。**

## Reviewer 3 — 友好审稿人（Confidence 3/5）

**Strengths**
1. 首个针对 VDBMS 非崩溃合规缺陷的端到端系统，填 roadmap 点名的 oracle 空白。
2. contract hallucination propagation 是可被反复引用的概念贡献。
3. 28 个真实 bug 已被生产系统修复——落地证据罕见。
4. 对边界/召回范围/无外部 baseline 的自我限定诚实。

**Weaknesses（可在 revision 内解决）**
1. <span style="color:#d97706">**[Minor]**</span> pending 数字与表格对不齐，改数即可。
2. <span style="color:#d97706">**[Minor]**</span> 结果呈现太密，摘要塞了约 18 个数字/百分比（43%、23%、12/48、25%、111、36、28、8、52、31%→81%、96.7%、n=30、69.2%、36/52、43.9%、80.5%、30、75%），对比其他 SE 顶会论文（如 NoREC）摘要通常 2-3 个 headline 数字，建议提炼主结果图。
3. <span style="color:#d97706">**[Minor]**</span> threat-model/reproduction 两锚点未跑，坦白说清即可。

**判断：Weak Accept（6/10）。**

## Verification

| # | 来源 | 断言 | 判定 | 说明 |
|---|------|------|------|------|
| 1 | R2-W1 | pending 应为 59 非 30；区间分母错 | <span style="color:#16a34a">**Valid**</span> | Table 2 逐行 pending=17+12+26+3+1=59；111-52=59。正文/caption/敏感性均用 30，[43.9%,80.5%] 应为约 [32.4%,85.6%] |
| 2 | R2-W2 | 三锚点只验证 source 一条 | <span style="color:#16a34a">**Valid**</span> | §5.3 L284 明写 threat-model never populated、reproduction not exercised；3/16 residual FP 恰为 TM 本应拦截的 |
| 3 | R1-W2 | 33/44 与 29/32 TP 分子不一致 | <span style="color:#16a34a">**Valid**</span> | 33 TP > 可达 30 TP（L270 定义），claim-only 可能基于全集 36 而 source-grounded 基于可达 30，两条件分母不同 |
| 4 | R1-W3 | opus/sonnet 与 GLM-5.2 矛盾 | <span style="color:#16a34a">**Valid**</span> | L169 同句并列三个模型标识，读者无法判断实验真实配置 |
| 5 | R2-W3 | 无端到端外部 baseline | <span style="color:#16a34a">**Valid**</span> | L280 自述无 external baseline；L282 的 45.6% 为跨总体事后推算；VDBFuzz 对比 future work |
| 6 | 内部 | "12 of 48" vs "52 adjudicated" 两裁决分母 | <span style="color:#d97706">**Misleading**</span> | 48=acknowledged+by-design（排除 4 rejected），技术自洽但摘要同段并用 48 和 52 易混，建议首次使用时加定义 |
| 7 | 内部 | Threats 中 "46 source-grounded candidates" 来源不明 | <span style="color:#16a34a">**Valid**</span> | L292 出现 46，全文其他地方未解释此数字；可能 52-6(rate-limit)=46，但与 source-grounded 后剩余的 32 不同，加重分母混乱 |
| 8 | 内部 | L282 single-layer 45.6% 样本量不足 | <span style="color:#16a34a">**Valid**</span> | fresh probe n=15 confirmed=3 precision=2/3，95% Wilson CI 约 [9.4%,99.2%]；45.6% 分母混合五库维护者裁决 52 与 Milvus 单库 LLM 裁决 27 |
| 9 | 内部 | §5.2 Case Studies 过薄 | <span style="color:#16a34a">**Valid**</span> | L264-266 全节仅 4 行，两个 case study 各一句话，缺少端到端走查（输入/契约/输出/判定/维护者反馈） |

## Action Plan

<span style="color:#dc2626">**Must Fix**</span>（不改大概率被拦）
- [ ] **P0-1 账目闭合**：确认 111 中 59 篇未裁决的真实 `pending / excluded` 拆分。然后修正 Table 2 caption（L242）、§5.3 敏感性（L278）、摘要（L78）、§1（L119）、结论（L302）共 5 处。需作者真实数字。
- [ ] **P0-2 模型配置**：确认 §3（L169）真实 backbone（opus/sonnet 是 Claude 体系还是 GLM 自定义配置名），统一措辞并补版本号+artifact pointer。需作者确认。
- [ ] **P0-3 CTS 归因诚实化**：贡献 #2（L127）改措辞：主体改为 source-grounding 验证结论，三锚点降级为 "design-level framework, with source anchor validated and the other two designed but not yet evaluated"。图 1（L185-199）threat-model 和 repro 节点灰显并标 "unvalidated"。可直接做。

<span style="color:#d97706">**Should Fix**</span>（表述不清容易被误解）
- [ ] **P1-1**：§5.5（L280）内 33/44 vs 29/32 加脚注说明两条件 TP 分母差异（claim-only 基于全集 36 中保留 33，source-grounded 基于 rate-limit 可达 30 中保留 29）。可直接做。
- [ ] **P1-3**：统一 "48 substantively adjudicated" 与 "52 adjudicated" 口径——首次使用 48 时加括号定义 "acknowledged or by-design; excluding 4 outright rejections"，或统一用 52 并调整 25% 计算（12/52=23.1%）。可直接做。
- [ ] **P1-4**：Threats（L292）中 "46 source-grounded candidates" 加注解释来源（52-6 unreachable=46）。可直接做。
- [ ] **P1-5**：§5.3 discovery recall 段落（L286）区分术语——改用 "contract coverage" 而非 "discovery recall"，并在首次使用 "TP recall"（L270）时加注说明指判断层保留率。可直接做。
- [ ] **P1-6**：L282 的 single-layer counterfactual 加 caveat："the 45.6% combines two populations with different ground-truth sources (maintainer adjudication vs. LLM+re-probe); the fresh probe arm (n=3) is too small for statistical inference and serves as directional evidence only"。可直接做。
- [ ] **P1-2 外部 baseline**：补一个可比的 baseline（如 naive 规则 baseline：关键词匹配文档约束+简单边界检查），或降级声称并在 limitation 说透「为何现在做不了 + 何时能做」。需补实验或改叙事。
- [ ] **Fig.1 灰显**：threat-model 和 repro 节点改为 `fill=gray!15` 并标 `\tiny unvalidated`。可直接做。

<span style="color:#6b7280">**Optional**</span>（锦上添花）
- [ ] 加主结果图给摘要减负（当前 18 个数字/百分比）
- [ ] 截稿允许则补 discovery recall 端到端 held-out 实验（Tier-2 B）
- [ ] §5.2 Case Studies 扩充为端到端走查（输入/契约/系统输出/dev-reviewer 判定/维护者反馈）

**Round 5 整体判断：** 相比 Round 4，本轮将每个问题定位到行号和原文引用，核心风险排序：**(1) P0-1 账目不闭合**（5 处联动错误，精度区间作废）> **(2) P0-2 模型配置矛盾**（可复现性阻断）> **(3) P0-3 CTS over-claiming**（2/3 机制无实证）。P0-1/P0-2 均需作者真实 ground truth，属硬阻断；其余项可直接落地。核心价值（维护者权威作独立真值层 + 28 个真实修复）依旧成立，天花板取决于账目闭合、CTS 归因诚实化、以及能否补一个像样的 baseline。

---

# Round 6 校正审阅（against `paper-draft-vldb-final.tex`, 2026-07-11）

> **重要勘误：** Round 5 的 P0-1（账目不闭合）和 P0-2（模型配置矛盾）基于 `paper-draft-vldb-revised.tex` 的表格结构进行推算，但 `paper-draft-vldb-final.tex` 已修复了这两项。本轮回到原文逐行核实，纠正 Round 5 的误判，并标注真正仍在的问题。
>
> **总体预测：Borderline / Weak Accept（SE 顶会 ICSE/FSE/ISSTA/ASE），Weak Reject（DB 顶会 VLDB/SIGMOD）**
> **Date:** 2026-07-11

## Round 5 勘误

| Round 5 问题 | 本轮判定 | 说明 |
|---|---|---|
| P0-1 账目不闭合（pending=59 vs 30） | <span style="color:#dc2626">**Round 5 误判，final 版已修**</span> | `paper-draft-vldb-final.tex` Table 2 增加了 Pend. 和 Excl. 两列，逐系统拆分清晰：Milvus 0+17、Qdrant 8+4、Weaviate 21+5、MeiliSearch 0+3、Chroma 1+0，合计 30 pending + 29 excluded。111 = 52 + 30 + 29 完全闭合。Table 2 caption 明确写出 "30 are pending ... 29 are excluded"。敏感性区间 [43.9%, 80.5%] 分母正确。 |
| P0-2 模型配置矛盾（opus/sonnet vs GLM-5.2） | <span style="color:#dc2626">**Round 5 误判，final 版已澄清**</span> | L169 明确写 "where opus/sonnet denote prompting-and-budget configurations of the same GLM-5.2 backbone rather than different model families"。三者不矛盾：GLM-5.2 是 backbone，opus/sonnet 是该 backbone 上的预算/提示配置档位。 |
| P1-1 两条件 TP 分母不一致（33/44 vs 29/32） | <span style="color:#d97706">**已加脚注说明**</span> | L281 脚注解释："claim-only scored all 36 TPs (retaining 33), while source-grounding scored the 30 reachable via the GitHub API (retaining 29, with 6 TPs rate-limited)"。措辞仍可再清晰，但信息已披露。 |
| Fig.1 threat-model/repro 未灰显 | <span style="color:#16a34a">**已修**</span> | TikZ 代码中 `truthunval/.style={..., dashed, fill=gray!15}` 已将 repro 和 tm 节点设为灰色虚线。Figure caption 也标注 "gray, dashed ... designed but not yet evaluated"。 |

## Score Summary（Round 6, 基于 final 版准确核实）

| Dimension | R1 (Objective) | R2 (Strict) | R3 (Supportive) |
|-----------|:---------:|:---------:|:---------:|
| Soundness | 3/4 | 2/4 | 3/4 |
| Novelty | 3/4 | 2/4 | 3/4 |
| Presentation | 2/4 | 2/4 | 3/4 |
| Overall | 5/10 (Borderline) | 4/10 (Weak Reject) | 6/10 (Weak Accept) |

相比 Round 5，Soundness 上调（账目闭合、模型配置已澄清），Presentation 不变（摘要仍过密、related work 仍薄），Novelty 不变。

---

## Reviewer 1 -- Objective Reviewer
> Confidence: 4/5

**Summary**
TestVDB 是首个针对 VDBMS API 合规缺陷的 LLM 驱动检测系统。核心设计原则 Contract-Truth Separation (CTS) 将 LLM 生成的契约断言与由维护者权威支撑的真值层分离，用后者证伪前者。跨 5 个 VDBMS 提交 111 个 issue，维护者确认 36 个（28 已修复）。受控回溯实验显示 source-grounding 锚点将 FP 抑制从 31% 提升到 81%，TP 保留率 96.7%。

**Strengths**
1. 问题定位精准：VDBMS 43% 的缺陷是 incorrect-behavior，却没有 oracle，TestVDB 用契约填补这个空白。Table 1 的排除论证干净有力。
2. Contract hallucination propagation 是一个有洞察力的观察：12/48 by-design 案例证明 LLM 自我确认是真实失败模式。
3. 诚实度出色：敏感性区间 [43.9%, 80.5%]、RQ4 标为 negative result、CTS 两个锚点标为 unvalidated，罕见坦诚。
4. 28 个已修复的真实 bug 是硬通货。Table 2 账目完整闭合（52+30+29=111）。
5. Implementation 段补充了代理分层（4 opus + 16 sonnet on GLM-5.2），四判官轴，以及端到端 trace 指引。

**Weaknesses**
1. <span style="color:#dc2626">**[Major]**</span> **模板与投稿目标不匹配。** 文件名含 "vldb"，但使用 `\documentclass[sigconf]{acmart}`（ACM 格式）。PVLDB 有自己的模板格式。会议元数据全为占位符（`Conference'26`、虚构 ISBN/DOI）。投稿前必须换模板。

2. <span style="color:#dc2626">**[Major]**</span> **三锚点 CTS 只有一个被验证。** 贡献 #2 写 "three-anchor counter-evidence framework"，但 §5.3 Anchor Attribution 段明确承认：reproduction 锚点 "not exercised"，threat-model 锚点 "never populated"，且 3/16 漏过的 FP 恰恰是 threat-model 本应拦截的。实际贡献是 "source-grounding verification"，不是 "three-anchor framework"。Fig.1 灰显处理很好，但文字贡献声明仍 over-claiming。

3. <span style="color:#dc2626">**[Major]**</span> **无端到端外部 baseline。** 所有对比均为内部消融。§5.5 的 single-layer counterfactual (45.6%) 混合了五库维护者裁决的 52 个和 Milvus 单库 LLM 裁决的 27 个，且 fresh probe 仅 n=3（precision 2/3，95% CI 极宽）。缺一个真正独立的 pipeline 外对照（如规则 baseline、单 LLM 调用、或人工 baseline）。

4. <span style="color:#dc2626">**[Major]**</span> **无端到端 discovery recall。** 96.7% 是判断层 TP 保留率（已被 surface 的 bug 有多少保留），不是 "从所有存在的合规缺陷中发现了多少"。Contract coverage 上游探针 (6/9=67%) 只测了文档覆盖，未涉及攻击生成和判断。Discovery recall 是评估系统实用性的关键维度，缺失使审稿人无法判断精度收益是否值得。

5. <span style="color:#d97706">**[Minor]**</span> **摘要过长过密。** 约 250 词、含 18+ 个数字/百分比。PVLDB 摘要通常 ~150 词、2-3 个 headline 数字。当前摘要试图预防所有可能的批评，这不是摘要的功能。

6. <span style="color:#d97706">**[Minor]**</span> **RQ2 过薄。** §5.2 全节仅 ~4 行，两个 case study 各一句话。其中 hallucination case 重复了 §4 的内容。建议扩充为端到端走查（输入/契约/输出/判定/维护者反馈）或并入 RQ1。

7. <span style="color:#d97706">**[Minor]**</span> **相关工作仅 8 篇引用。** 缺少对 API 测试工具（RESTler、Schemathesis）、LLM 规约挖掘、test oracle 综述文献（如 Barr et al. 2015）、API misuse detection 的讨论。

8. <span style="color:#d97706">**[Minor]**</span> **过度防御性措辞。** "we report the boundary honestly" / "we state the system's boundary honestly" 出现 3 次。"not a contribution" 出现 3 次。诚实是好的，但措辞可以中性化：用 "Limitations:" 代替 "We bound the system honestly:"。

**Questions for Authors**
1. 能否在现有 held-out bug 基础上，扩大样本量并跑完整 pipeline（包括攻击生成和判断），给出哪怕是粗略的 discovery recall 估计？
2. 贡献 #4 声称 "open-source system and reproducible dataset"，但正文无 artifact link。是否计划提交 artifact evaluation？
3. MeiliSearch (3/111) 和 Chroma (1/111) 提供的评估信号近乎为零，是否考虑将 "five VDBMSs" 的泛化措辞收敛为 "primarily Milvus and Qdrant"？
4. TODO 注释（tex 文件头部）提到 references.bib "currently empty"。如果已填充，请删除过时的 TODO 注释以避免混淆。

---

## Reviewer 2 -- Strict Reviewer
> Confidence: 4/5

**Summary**
一篇用 LLM 从 VDBMS 文档提取 API 契约并检测合规违规的论文。dev-reviewer agent 通过查源码过滤假阳性。论文提出 "contract hallucination propagation" 作为失败模式。

**Strengths**
1. 28 个已修复 bug 是实在的实践影响。
2. 内部数据账目自洽，敏感性区间方法论合理。
3. 受控回溯实验设计（source-grounding 的 FP 抑制从 31% 到 81%、TP 保留 96.7%）在其限定范围内可信。

**Weaknesses**
1. <span style="color:#dc2626">**[Major]**</span> **Novelty 有限。** 核心技术归结为：(a) 用 LLM 从文档提取约束，(b) 生成违反约束的测试输入，(c) 用 LLM 查源码过滤假阳性。"Contract-Truth Separation"、"assertion layer"、"truth layer" 等术语包装提升了感知复杂度，但底层机制是 "用源码验证 LLM 输出"，属于直觉性的工程决策。§4 的形式化 ($C_{\text{LLM}} \supset C_{\text{true}}$) 不增加分析力度，只是重述了 "LLM 提取的约束可能比真实意图更严格" 这个显然的观察。

2. <span style="color:#dc2626">**[Major]**</span> **75% 的发现是浅层边界/验证缺陷。** 如 `nprobe=0`、`shardsNum=-1` 这类简单输入验证 bug，是任何基于契约的方法最容易抓的一类。仅 2 个 state/logic、3 个 result-correctness bug，难以证明系统对复杂缺陷的价值。对于顶会发表，需要在更难的类别上展示优势。

3. <span style="color:#dc2626">**[Major]**</span> **没有与更简单方法的比较。** (a) 规则 API 验证器（如 OpenAPI schema validation）；(b) 单 LLM 调用（一个 prompt 包含文档 + 行为 + 源码，问 "这是 bug 吗？"）；(c) 人工 reviewer baseline。没有任何 pipeline 外对照，无法判断多 agent 架构是否必要。

4. <span style="color:#dc2626">**[Major]**</span> **可复现性仍有缺口。** GLM-5.2 backbone 和 opus/sonnet 配置已说明，但缺：(a) 具体 API 版本号、(b) temperature/sampling 参数、(c) 20 个 agent 的提示词（至少需要摘要）、(d) 成本分析（tokens、API calls、wall-clock time）、(e) artifact link。声称 "open-source system" 但无链接。

5. <span style="color:#d97706">**[Minor]**</span> **§5.5 single-layer counterfactual 跨总体拼接。** 45.6% = 36/(36+16+27)，分母 79 混合了五库维护者裁决 (52) 和 Milvus 单库 LLM 裁决 (27)。正文 Threats (L293) 已自承此限制，但仍作为主要结果呈现在 §5.5 段落标题中。

6. <span style="color:#d97706">**[Minor]**</span> **"48 substantively adjudicated" 与 "52 maintainer-adjudicated" 并用造成混淆。** 48 = 36 acknowledged + 12 by-design（不含 4 rejected），52 = 48 + 4。定义自洽但首次出现时无括号定义，读者需要自行推导。

7. <span style="color:#d97706">**[Minor]**</span> **Threats to Validity 过长（~30 行），比 Related Work 还长。** 部分内容（variance 分析、proxy ground truth 讨论）属于方法论细节，应移至补充材料或附录。

**Questions for Authors**
1. 如果不用多 agent 架构，一个 LLM 调用（文档 + 行为 + 源码 -> 是否是 bug？）能达到什么精度？这是判断架构必要性的最直接实验。
2. L1/L2 novelty gate 的假阴性率是多少？有没有验证过去重没有误杀真 bug？
3. tex 文件头部的 TODO 注释是否都已过时？如果 references.bib 已填充，stale TODO 会造成审稿人困惑。

---

## Reviewer 3 -- Supportive Reviewer
> Confidence: 3/5

**Summary**
TestVDB 填补了 VDBMS 测试中一个真实且被文献点名的空白：43% 的 incorrect-behavior 缺陷没有 oracle，crash fuzzer 无法覆盖。核心洞察是 LLM 自我确认是危险的（contract hallucination propagation），CTS 通过引入独立真值层来缓解这一问题。28 个已修复 bug + 跨厂商 COSINE > 1.0 复现是有说服力的实践证据。

**Strengths**
1. **问题时机好、scope 合理。** 正确聚焦于可解的子问题（API 合规），而非过度声称解决通用结果正确性。
2. **Contract hallucination propagation 是可被广泛引用的概念贡献。** 任何用同一 LLM 家族做规约提取 + 合规判断的系统都易受此影响。
3. **28 个真实修复 + 跨 Milvus/Qdrant 的 COSINE > 1.0。** 后者是违反数学不变量的硬 bug，不依赖 LLM 判断。
4. **方法论上的审慎。** 账目闭合（52+30+29=111）、敏感性区间 [43.9%, 80.5%]、RQ4 标为 negative result、Fig.1 灰显未验证锚点。这种透明度让结果更可信。
5. **受控回溯设计合理。** FP 抑制 31% -> 81%，TP 保留 96.7% (n=30)，在同一 52 候选池上测量，配合脚注说明 TP 基数差异。
6. **Single-layer counterfactual 有说服力。** 27 个被 kill 的候选全部证实为真假阳性（LLM 裁决 + 7 个 live re-probe），零 over-kill。

**Weaknesses**
1. <span style="color:#dc2626">**[Major]**</span> **缺端到端 discovery recall 使评估只看到了一半。** 96.7% 是已被 surface 的 TP 的保留率；contract coverage 探针 (6/9) 只测上游。无法判断系统漏了多少可发现的 bug。这是论文最大的评估缺口。

2. <span style="color:#d97706">**[Minor]**</span> **呈现可大幅精简。** 同一组核心数字（36/52, 69.2%, 43.9%-80.5%）在摘要、引言、RQ3、结论出现 4 次。RQ3 的 7 个子段落可合并为 3 个（主结果、聚合精度、敏感性）。Threats to Validity 比 Related Work 还长，建议压缩。

3. <span style="color:#d97706">**[Minor]**</span> **贡献 #2 声明与实证支撑不匹配。** 标题写 "three-anchor"，但只有 source anchor 有数据。Fig.1 灰显处理已经到位，贡献文字也需对齐：改为 "source-grounded verification, with reproduction and threat-model anchors designed but not yet evaluated"。

4. <span style="color:#d97706">**[Minor]**</span> **Related work 偏薄。** 仅 8 篇引用。建议补：(a) API 测试（RESTler, EvoMaster, Schemathesis）, (b) LLM-based spec mining, (c) test oracle survey (Barr et al. 2015), (d) LLM hallucination/reliability 文献。

5. <span style="color:#d97706">**[Minor]**</span> **COSINE > 1.0 是最亮的技术发现，却被埋在 §5.1 一句话里。** 建议提升为独立 case study 或第二 oracle 维度（可表达数学不变量），区别于纯 "LLM 查 LLM" 模式。

**Questions for Authors**
1. COSINE > 1.0 能否推广为一个 "数学不变量 oracle" 子类？不依赖 LLM 判断，可能比 CTS 更有辨识度。
2. 29 个 excluded（closed-no-label/duplicate）是系统失败还是维护者行为？分类说明有助于理解 TestVDB 的实际失败模式。
3. 端到端延迟（从文档爬取到 issue 提交）大约是多少？成本信息有助于判断可部署性。

---

## Verification (Round 6)

| # | Source | Claim | Verdict | Note |
|---|--------|-------|---------|------|
| 1 | Round 5 P0-1 | "pending=59, 账目不闭合" | <span style="color:#dc2626">**Round 5 误判**</span> | Final 版 Table 2 有 Pend./Excl. 列，30+29=59 拆分清晰；111=52+30+29 闭合。Round 5 基于 revised 版 5 列表推算，final 版已修复。 |
| 2 | Round 5 P0-2 | "opus/sonnet 与 GLM-5.2 矛盾" | <span style="color:#dc2626">**Round 5 误判**</span> | Final 版 L169 明确解释 "opus/sonnet denote prompting-and-budget configurations of the same GLM-5.2 backbone"。不矛盾。 |
| 3 | R1-W2 | "三锚点只验证一个" | <span style="color:#16a34a">**Valid**</span> | §5.3 L284-285 确认 reproduction "not exercised"、threat-model "never populated"。Fig.1 灰显到位，但 Contribution #2 (L127) 仍写 "three-anchor"。 |
| 4 | R2-W1 | "核心技术是直觉性工程" | <span style="color:#d97706">**Misleading**</span> | CTS 分离原则本身非平凡（识别并解决 LLM 自我确认问题），但形式化 (§4) 确实不增加分析力度。评价取决于审稿人是重理论还是重实践。 |
| 5 | R1-W1 | "模板不匹配" | <span style="color:#16a34a">**Valid**</span> | `\documentclass[sigconf]{acmart}` + 占位符元数据，文件名含 "vldb"。投稿前必须换 PVLDB 模板。 |
| 6 | R1-W4 | "无端到端 discovery recall" | <span style="color:#16a34a">**Valid**</span> | §5.3 L286 的 contract coverage (6/9) 只测上游抽取。L292 "establishing true discovery recall ... is future work"。96.7% 是判断层保留率。 |
| 7 | R1-W7 | "仅 8 篇引用" | <span style="color:#16a34a">**Valid**</span> | 全文 8 个 `\cite{}`。无 API testing tools、LLM spec mining、test oracle survey。 |
| 8 | R2-W2 | "75% 浅层 boundary/validation" | <span style="color:#16a34a">**Valid**</span> | §5.1 确认 27/36=75% 是 boundary/validation。仅 2 state/logic + 3 result-correctness。 |
| 9 | R3-W5 | "COSINE>1.0 被埋" | <span style="color:#16a34a">**Valid**</span> | §5.1 一句话、§5.2 一句话。跨厂商复现的数学不变量违规，比 CTS 更 novel，值得提升。 |
| 10 | 内部核实 | Table 2 逐行算术 | <span style="color:#16a34a">**Valid**</span> | 每行 submitted = fixed+accepted+by-design+rejected+pending+excluded 均成立。52+30+29=111。 |
| 11 | 内部核实 | L281 脚注 TP 基数说明 | <span style="color:#16a34a">**Valid**</span> | 脚注已解释 claim-only 基于 36 TP、source-grounded 基于 30 可达 TP。信息已披露。 |

---

## Action Plan (Round 6, 准确版)

<span style="color:#dc2626">**Must Fix**</span> -- 不改大概率被拒

- [ ] **换 VLDB 模板。** 将 `\documentclass[sigconf]{acmart}` 替换为 PVLDB proceedings 模板，更新所有会议元数据。这是格式门槛。如果目标不是 VLDB 而是 SE 会议（ICSE/FSE/ISSTA/ASE），则按对应模板调整。*(R1-W1)*
- [ ] **精简摘要至 ~150 词。** 保留：问题（43% incorrect-behavior 无 oracle）、方法（CTS）、核心结果（36 acknowledged, 28 fixed, FP 抑制 31%->81%）。移除敏感性区间、n=30、48/52 口径等细节。*(R1-W5, R3-W2)*
- [ ] **收窄贡献 #2 措辞。** 将 "three-anchor counter-evidence framework" 改为 "source-grounded verification (validated), within a three-anchor design where reproduction and threat-model anchors are designed but not yet evaluated"。与 Fig.1 的灰显处理保持一致。*(R1-W2, R3-W3)*
- [ ] **扩展 Related Work。** 从 8 篇扩展到至少 20 篇，覆盖：(a) API testing (RESTler, Schemathesis, EvoMaster), (b) LLM-based spec mining / test generation, (c) test oracle survey (Barr et al. 2015), (d) LLM hallucination mitigation, (e) database testing beyond SQL (NoREC, TLP, DQE)。*(R1-W7, R3-W4)*
- [ ] **删除或更新过时的 TODO 注释。** tex 文件头部仍有 "references.bib is currently empty" 等 TODO 注释。如果 bib 已填充，删除这些注释以避免审稿人困惑。*(R2-Q3)*

<span style="color:#d97706">**Should Fix**</span> -- 不改会降分或被误解

- [ ] **补至少一个外部 baseline。** 最可行的选项：单 LLM 调用 baseline（一个 prompt 包含文档 + 行为 + 源码，直接判断 "是否是 bug？"）。如果无法补实验，在 Limitations 中详细说明为何现阶段做不了、计划何时做。*(R1-W3, R2-W3)*
- [ ] **给 discovery recall 一个更好的估计。** 扩大 contract coverage 探针（当前 6/9），或对 held-out 已修 bug 跑完整 pipeline（攻击生成 + 判断）。即使是粗略的估计也比空白好。*(R1-W4, R3-W1)*
- [ ] **减少防御性措辞。** 将 "we report/state the boundary honestly" 替换为中性表述（如 "Limitations include..."）。RQ4 "not a contribution" 说一次即可，不重复。*(R1-W8)*
- [ ] **充实或合并 RQ2。** 当前 ~4 行的两个 case study 无法支撑独立 RQ。建议扩充为端到端走查（输入 -> 契约提取 -> 攻击 -> 四判官 -> dev-reviewer -> 维护者反馈），或并入 RQ1 作为实例。*(R1-W6)*
- [ ] **统一 "48" 与 "52" 口径。** 首次出现 "48 substantively adjudicated" 时加括号定义（= acknowledged + by-design, excluding 4 rejected），避免读者与 52 混淆。*(R2-W6)*
- [ ] **压缩 Threats to Validity。** 当前 ~30 行，比 Related Work 长。将 variance 分析和 proxy ground truth 讨论移至附录。*(R2-W7)*

<span style="color:#6b7280">**Optional**</span> -- 锦上添花

- [ ] **提升 COSINE > 1.0 的位置。** 扩展为独立 case study 或 "可表达不变量 oracle" 子类讨论。这是最亮的技术发现，不依赖 LLM 判断，比 CTS 更有辨识度。*(R3-W5)*
- [ ] **加成本/效率表。** 每个 VDBMS 目标的 token 消耗、API 调用次数、wall-clock time、美元成本。LLM 系统论文中越来越被期望。*(R2-W4)*
- [ ] **讨论 CTS 的泛化性。** Contract hallucination propagation 观察适用于所有 LLM 驱动的规约测试系统。简短讨论 CTS 能否应用于 REST API、云服务等有文档契约的系统。
- [ ] **考虑拆分论文。** 当前同时推进 (a) 工具、(b) 设计原则 (CTS)、(c) 经验观察 (hallucination propagation)、(d) 数据集。一篇聚焦工具 + 数据集、另一篇聚焦 CTS 原则 + 深入分析可能各自更强。

---

## Round 6 Overall Assessment

**已解决的问题（相比 Round 1-5）：**
- [x] 跨口径 5.4x 拼接 -> 改为同总体 FP 抑制 31%->81% + TP 保留 96.7%
- [x] 精度分母选择偏差 -> 敏感性区间 [43.9%, 80.5%]
- [x] 实验未收口 -> Weaviate 明确排除，只报已完成测量
- [x] 账目不闭合 -> Table 2 补 Pend./Excl. 列，111=52+30+29
- [x] 模型配置矛盾 -> opus/sonnet 解释为 GLM-5.2 的配置档位
- [x] Fig.1 占位符 -> 真 TikZ 图，未验证锚点灰显
- [x] Implementation 段缺失 -> 已补
- [x] RQ4 列为贡献 -> 降级为 negative result
- [x] 贡献从 6 条压到 4 条
- [x] norec20 引用身份错标 -> 已修正

**仍需解决的核心问题（按优先级）：**
1. **[格式] 模板不匹配** -- 纯执行，投稿前必须完成
2. **[评估] 无外部 baseline** -- 评级天花板，需补实验或降级声称
3. **[评估] 无 discovery recall** -- 需补实验或扩大探针
4. **[声明] 贡献 #2 三锚点 over-claiming** -- 改措辞即可
5. **[呈现] 摘要过密、Related work 薄、RQ2 薄、过度防御** -- 写作打磨

**核心价值判断：** 论文的核心价值（维护者权威作独立真值层 + 28 个真实修复 + contract hallucination propagation 观察）经过 6 轮审阅始终成立。数据账目自洽，方法论审慎，诚实度出色。天花板不在写作，在评估完整性：缺外部 baseline 和 discovery recall 使审稿人只能看到一半的图景。如果目标是 SE 顶会（ICSE/FSE/ISSTA/ASE），补上最可行的 baseline（单 LLM 调用对照）和粗略的 recall 估计后，有望进入 accept 区间；如果目标是 DB 顶会（VLDB/SIGMOD），还需要更强的与向量检索内部机制的对接。

---

# Round 7 — 三视角独立审稿 + Response Letter 后校正 (2026-07-11)

> **Method:** 三份独立审稿完成后，对照作者回复信 (`RESPONSE-to-reviewers.md`) 和 `paper-draft-vldb-final.tex` 逐条核实回复中声称的修改是否落地。本轮标注每项修改的核实状态（✅ 已落地 / 🟡 部分 / ❌ 未改）。
> **Overall Prediction:** Weak Accept — R1 和 R3 Weak Accept，R2 从 Weak Reject 上移至 Borderline。回复信解决了约 70% 的实质顾虑。
> **Date:** 2026-07-11

## Score Summary（Response Letter 后校正）

| Dimension | R1 (Objective) | R2 (Strict) | R3 (Friendly) |
|-----------|:---------:|:---------:|:---------:|
| Soundness | **3/4** (+1) | **3/4** (+1) | 3/4 |
| Novelty | 3/4 | 2/4 | 3/4 |
| Presentation | **3/4** | **3/4** (+1) | **3/4** |
| **Overall** | **7/10** (+1) | **5/10** (+1) | **7/10** |

**Soundness 上调理由：** 单 LLM 端到端 baseline (6.7%) + A1 单层反事实实验 (27/27 over-kill=0) 是两个实跑实验增量，填补了原先"仅有内部消融"的最大评估缺口。**Presentation 上调理由：** 摘要精简至 ~165 词、RQ2 充实（3 case study）、Related Work 从 8 篇扩至 20 篇、Threats 压缩至 ~10 行、stale TODO 删除、48/52 口径统一。

---

## Response Letter 修正逐条核实

| # | 回复信声称的修改 | 核实状态 | 证据（final.tex 行号） |
|---|---|---|---|
| 1 | 贡献 #2 措辞收敛（三锚点→source-grounded validated + 其余 designed but not yet evaluated） | ✅ 已落地 | L96-97: "source-grounded verification---the validated anchor---within a three-anchor counter-evidence design" |
| 2 | 新增单 LLM 端到端 baseline | ✅ 已落地 | L257-258: Single-LLM 全流程 6.7% (1/15), Wilson CI [0.2%, 31.5%] vs TestVDB 69.2% |
| 3 | A1 单层反事实实验（fresh probes） | ✅ 已落地 | L255-256: 15 fresh probes, 2 TP + 1 FP confirmed; 27/27 killed all FP, over-kill=0 |
| 4 | 摘要精简 | ✅ 已落地 | 从 ~250 词压至 ~165 词，不再塞敏感性区间 |
| 5 | Related Work 扩展 | ✅ 已落地 | 从 8 篇 → 20 个 `\cite{}`: RESTler, EvoMaster, NoREC/TLP/DQE/DDLCheck, LLM for SE, hallucination survey, Barr et al., 等 |
| 6 | RQ2 充实（3 个端到端 case study + COSINE 不变量子类） | ✅ 已落地 | L234-239: TP #47729, TP #49844, FP #50193 全链路走查 + COSINE>1.0 数学不变量子类 |
| 7 | Threats 压缩 | ✅ 已落地 | L266-268: 压缩至 ~10 行 |
| 8 | 删除 stale TODO | ✅ 已落地 | tex 头部注释已清除 |
| 9 | 48/52 口径统一 | ✅ 已落地 | 摘要和正文中定义清晰 |
| 10 | Discovery recall 补实验 | 🟡 标为 future work | L261: "establishing true discovery recall ... is future work"——未补新数据，但标注诚实 |
| 11 | 模板（acmart → 目标会议） | ❌ 未改 | L3: 仍为 `\documentclass[sigconf]{acmart}`，等导师确认目标会议 |
| 12 | 成本/效率信息 | ❌ 未补 | 无 token 消耗、API 调用量、wall-clock time |
| 13 | "large-scale" 措辞 | ❌ 未改 | 贡献 #1 (L95) 仍写 "large-scale empirical study" |

**净结果：13 项声称中有 9 项完全落地、1 项诚实标注 future work、3 项等待外部决策或后续补充。回复信主要增量是两项实跑实验（A1 单层反事实 + B9 单 LLM baseline），这确实改变了评估图景。**

---

---

## Reviewer 1 -- Objective Reviewer (Confidence: 4/5)

**Summary:** TestVDB 用 LLM 从 VDBMS 文档提取 API 契约，通过四判官辩论生成攻击，再用 dev-reviewer agent 的 source-grounded 验证过滤假阳性。111 投稿、36 维护者确认、28 修复。核心概念 CTS 将 LLM 断言层与真值层分离。

**Strengths:**
1. 问题定位精准：43% incorrect-behavior vs 23% crash/hang，VDBFuzz 只覆盖 crash。Table 1 的 oracle 排除论证干净。
2. Contract hallucination propagation 是有洞察力的观察：constant.go 的虚构 provenance + 12/48 by-design 案例支撑其存在性。
3. 诚实度罕见：敏感性区间 [43.9%, 80.5%]、RQ4 标为 negative result、未验证锚点灰显、边界明确。
4. 28 个真实修复是硬通货。COSINE > 1.0 跨厂商复现是漂亮发现。
5. **【新增】** 单 LLM 端到端 baseline (6.7% vs TestVDB 69.2%) 有力地证明了多 agent 架构的端到端必要性——不是只在内部消融中成立。
6. **【新增】** A1 单层反事实 27/27 over-kill=0 直接回应了"高精度是否靠牺牲召回换来的"质疑。

**Weaknesses:**
1. <span style="color:#dc2626">**[Major]**</span> **模板不匹配。** `\documentclass[sigconf]{acmart}` 是 ACM 格式，文件名含 "vldb"。投稿前必须换 PVLDB 或目标会议模板。*(回复信未解决——等导师定会议)*
2. <span style="color:#16a34a">**[Resolved]**</span> ~~三锚点 CTS 仅 source 被验证~~ → 贡献 #2 (L96-97) 已改为 "source-grounded verification---the validated anchor---within a three-anchor design...reproduction and threat-model anchors are designed but not yet evaluated"。与 Fig.1 灰显完全对齐。✅
3. <span style="color:#16a34a">**[Resolved]**</span> ~~缺端到端外部 baseline~~ → L257-258 新增单 LLM 端到端 baseline: 6.7% (1/15), Wilson CI [0.2%, 31.5%] vs TestVDB 69.2%。✅
4. <span style="color:#d97706">**[Minor]**</span> **缺端到端 discovery recall。** 回复信未补新实验，仅标为 future work。96.7% 仍是判断层 TP 保留率。Contract coverage 探针 (6/9=67%) 未扩大。
5. <span style="color:#16a34a">**[Resolved]**</span> ~~摘要过密~~ → 已精简至 ~165 词。✅
6. <span style="color:#16a34a">**[Resolved]**</span> ~~RQ2 过薄~~ → 已补 3 个端到端 case study（TP #47729、TP #49844、FP #50193 全链路）+ COSINE 不变量子类。✅
7. <span style="color:#16a34a">**[Resolved]**</span> ~~Related Work 仅 8 篇~~ → 已扩至 20 篇，覆盖 API testing、LLM for SE、database oracles、hallucination survey。✅

**Unresolved Questions:** (1) Discovery recall 仍是空白——能否扩大 held-out 样本跑完整 pipeline？(2) Artifact link 在哪里？(3) MeiliSearch (3) 和 Chroma (1) 几乎零信号，"five VDBMSs" 泛化措辞是否应收敛为 "primarily Milvus and Qdrant"？

---

## Reviewer 2 -- Strict Reviewer (Confidence: 4/5)

**Summary:** 用 LLM 提取 API 契约并检测合规违规。dev-reviewer 通过查源码过滤假阳性。论文提出 "contract hallucination propagation" 作为失败模式。

**Strengths:**
1. 28 个已修复 bug 是实在的实践影响。
2. 内部数据账目自洽，敏感性区间方法论合理。
3. 受控回溯实验在其限定范围内可信。
4. **【新增】** 单 LLM 端到端 baseline (6.7%) 提供了一个 pipeline 外对照，直接回应了"没有外部 baseline"的批评。6.7% vs 69.2% 的差距是硬的。
5. **【新增】** A1 27/27 over-kill=0 说明精度提升不以牺牲召回为代价——对一篇 precision-focused 的论文至关重要。

**Weaknesses:**
1. <span style="color:#dc2626">**[Major]**</span> **Novelty 有限。** CTS、"assertion layer"、"truth layer" 等术语提升了感知复杂度，但底层机制是"用源码验证 LLM 输出"，属直觉性工程决策。形式化 C_LLM ⊃ C_true 不增加分析力度。*(回复信未改变这一点——这是本质判断，不是能靠加实验改的)*
2. <span style="color:#dc2626">**[Major]**</span> **75% 的发现是浅层边界/验证缺陷。** 如 nprobe=0、shardsNum=-1 这类简单输入验证 bug，是任何基于契约的方法最容易抓的。仅 2 个 state/logic、3 个 result-correctness bug。对顶会需在更难类别上展示价值。*(回复信未改变)*
3. <span style="color:#d97706">**[Minor，从 Major 降级]**</span> **无 pipeline 外对照** ~~→ 已补单 LLM 6.7% baseline。~~ 这是一个实质性的回应。✅ 但缺与规则 API 验证器和人工 reviewer 的对比。
4. <span style="color:#d97706">**[Minor]**</span> **可复现性缺口：** Implementation 段已补 agent 分层架构，但仍缺 API 版本号、temperature/sampling 参数、20 个 agent 的提示词摘要、成本分析、artifact link。
5. <span style="color:#16a34a">**[Resolved]**</span> ~~§5.5 single-layer counterfactual 混合 ground truth~~ → A1 fresh probes + 7/27 live re-probe 已独立验证，不再纯依赖混合推算。✅
6. <span style="color:#16a34a">**[Resolved]**</span> ~~Threats to Validity 30 行 vs Related Work 8 篇~~ → Threats 压缩至 ~10 行，Related Work 扩至 20 篇。比例已正常。✅
7. <span style="color:#16a34a">**[Resolved]**</span> ~~tex 头部 stale TODO~~ → 已清除。✅

**Unresolved Questions:** (1) L1/L2 novelty gate 的假阴性率是多少？(2) 缺 REST API validator / simple rule baseline 的对照。单 LLM 6.7% 确实很低，但更简单的启发式 baseline 可能同样有效。

---

## Reviewer 3 -- Friendly Reviewer (Confidence: 3/5)

**Summary:** TestVDB 填补了 VDBMS 测试中 43% incorrect-behavior 缺陷无 oracle 的真实空白。CTS 通过引入独立真值层缓解 LLM 自我确认问题。28 个已修复 bug + COSINE > 1.0 跨厂商复现有说服力。

**Strengths:**
1. 问题时机好、scope 合理，聚焦可解子问题而不过度声称。
2. Contract hallucination propagation 是可被广泛引用的概念贡献。方法论插曲（opus agent 编造 /mine 产物）反而强化了 CTS 核心论点。
3. 28 个真实修复 + COSINE > 1.0 数学不变量违规。
4. 方法论审慎：账目闭合、敏感性区间、RQ4 negative result、灰显未验证锚点。
5. 受控回溯设计合理 (FP 抑制 31%→81%, TP 保留 96.7%)。
6. Single-layer counterfactual 的 27/27 zero over-kill 有说服力。
7. **【新增】** 单 LLM 端到端 baseline (6.7%) 让 "多 agent 架构是否必要" 有了实证答案。
8. **【新增】** RQ2 的三个 case study（含一个 FP 被正确抑制的走查）让系统行为可理解。

**Weaknesses:**
1. <span style="color:#d97706">**[Minor，从 Major 降级]**</span> **Discovery recall** 仍标为 future work，但回复信已做诚实标注。6/9 contract coverage 探针未扩大。这是论文最明显的剩余缺口，但不再是评级天花板——单 LLM baseline 和 A1 实验已大幅提升了评估完整性。
2. <span style="color:#16a34a">**[Resolved]**</span> ~~呈现冗余~~ → 摘要 165 词、Threats ~10 行、RQ3 段落精简。✅
3. <span style="color:#16a34a">**[Resolved]**</span> ~~贡献 #2 over-claiming~~ → 已对齐。✅
4. <span style="color:#16a34a">**[Resolved]**</span> ~~Related work 偏薄~~ → 已扩至 20 篇。✅
5. <span style="color:#16a34a">**[Resolved]**</span> ~~COSINE>1.0 被埋~~ → 已在 RQ2 提升为"数学不变量 oracle"子类。虽然仍不是独立 case study，但位置已有实质提升。✅

**Unresolved Questions:** (1) 29 个 excluded（closed-no-label/duplicate）是系统失败还是维护者行为？(2) 端到端延迟大约多少？成本信息有助于判断可部署性。(3) COSINE>1.0 能否推广为系统性的"数学不变量 oracle"子类？

---

## Verification（Response Letter 后重新逐条核实）

| # | Source | Claim | Verdict | Note |
|---|--------|-------|---------|------|
| 1 | R1-W1 | 模板不匹配 | <span style="color:#16a34a">**Valid（仍存在）**</span> | `\documentclass[sigconf]{acmart}` + 占位符元数据，文件名含 "vldb"。回复信未解决 |
| 2 | R1-W2 | 三锚点仅 source 验证 | <span style="color:#dc2626">**已修正**</span> | 贡献 #2 (L96-97) 已改为 "source-grounded verification---the validated anchor---within a three-anchor design...reproduction and threat-model anchors are designed but not yet evaluated"。与 Fig.1 灰显完全对齐 |
| 3 | R1-W3 | 无外部 baseline | <span style="color:#dc2626">**已修正**</span> | L257-258 新增单 LLM 端到端 baseline: 6.7% (1/15), Wilson CI [0.2%, 31.5%]。真正独立的 pipeline 外对照 |
| 4 | R1-W4, R3-W1 | 无 discovery recall | <span style="color:#d97706">**仍存在（诚实标 future work）**</span> | 96.7% 仍是判断层 TP 保留率。Contract coverage 探针未扩大。L261 明确标 "future work" |
| 5 | R2-W1 | Novelty 有限 | <span style="color:#d97706">**主观判断，未变**</span> | 属本质性批评，不因加实验而改变 |
| 6 | R2-W2 | 75% 浅层边界 | <span style="color:#16a34a">**Valid（仍存在）**</span> | 27/36=75% boundary/validation。仅 2 state/logic + 3 result-correctness。回复信未改变 |
| 7 | R2-W4 | 可复现性缺口 | <span style="color:#d97706">**部分改善**</span> | Implementation 段已补 agent 分层（4 opus + 16 sonnet on GLM-5.2），但仍缺提示词、温度、成本、artifact link |
| 8 | R3-W5 | COSINE>1.0 被埋 | <span style="color:#dc2626">**已改善**</span> | 在 RQ2 (L239) 提升为 "Model-free mathematical-invariant oracle" 子类，区别于纯 contract oracle |
| 9 | R1-W5 | 摘要过密 | <span style="color:#dc2626">**已修正**</span> | ~165 词，不再塞敏感性区间和 48/52 口径细节 |
| 10 | R1-W5 | Related Work 仅 8 篇 | <span style="color:#dc2626">**已修正**</span> | 20 个 `\cite{}`: RESTler, EvoMaster, NoREC, TLP, DQE, DDLCheck, LLM for SE, hallucination survey, Barr et al., Claessen, Meyer, Amann, Manes |
| 11 | R1-W6 | RQ2 过薄 (~4 行) | <span style="color:#dc2626">**已修正**</span> | L234-239: 3 个端到端 case study（TP #47729, TP #49844, FP #50193）+ COSINE 子类 |
| 12 | R2-W7 | Threats 30 行 vs RW 薄 | <span style="color:#dc2626">**已修正**</span> | Threats (L266-268) ~10 行，RW 扩至 20 篇。比例正常 |
| 13 | 新增 | A1 单层反事实 27/27 over-kill | <span style="color:#16a34a">**Valid**</span> | L255-256: 15 fresh probes (2 TP + 1 FP confirmed); 7/27 live re-probe; 27/27 all FP, over-kill=0 |

---

## Action Plan（Response Letter 后校正版）

### <span style="color:#dc2626">Must Fix</span> -- 不改大概率被拒

- [ ] **换模板。** `\documentclass[sigconf]{acmart}` → 目标会议模板（等导师确认 PVLDB 或 SE 会议）。*(唯一未被回复信解决的格式门槛)*
- [ ] **收敛 "large-scale" 措辞。** 贡献 #1 (L95) 中 "large-scale empirical study" → "multi-system empirical study"。111 个 issue 跨 5 个系统，在 VDBMS 测试领域算规模可观，但 "large-scale" 对 DB/SE 顶会而言有夸大嫌疑——审稿人会拿百万 commit 级别的实证研究做对比。

### <span style="color:#d97706">Should Fix</span> -- 不改会降分

- [ ] **给 discovery recall 一个更好的估计。** B10 Option A（旧容器 + Web Archive 旧文档跑重发现率）如果能在截稿前跑出来，是跨入 Accept 的最后临门一脚。即使只是粗略估计也比空白好。*(唯一剩余的评估完整性缺口)*
- [ ] **加成本/效率信息。** token 消耗、API 调用次数、wall-clock time。LLM 系统论文越来越期望这些。*(新增建议)*
- [ ] **补充可复现信息。** 提示词摘要、温度参数、Artifact link。Implementation 段已有 agent 架构，再补这几点即可满足顶会可复现性标准。
- [ ] **讨论 "five VDBMSs" 泛化是否应收敛。** MeiliSearch (3/111) 和 Chroma (1/111) 信号近乎为零。如不收敛，至少加一句 caveat。

### <span style="color:#6b7280">Optional</span> -- 锦上添花

- [ ] **讨论 29 excluded 的性质。** 是系统失败还是维护者行为？有助于理解实际失败模式。
- [ ] **考虑 CTS 泛化性段落。** Contract hallucination propagation 适用于所有 LLM 驱动的规约测试系统——REST API、云服务等。简短段落即可增加 impact 感。

---

## Round 7 Overall Assessment（Response Letter 后校正）

**预测：Weak Accept。** R1 (7/10) 和 R3 (7/10) 推荐 Weak Accept，R2 (5/10) 从 Weak Reject 上移至 Borderline。这是一个 rebuttal 后大概率接受的分裂。

**回复信效力评估：约 70% 的实质顾虑已解决。** 主要加分项：
1. **A1 单层反事实 + B9 单 LLM baseline 是真正的实验增量，不是只改措辞。** 单 LLM 的 6.7% vs TestVDB 的 69.2% 这个差距是硬的——审稿人会认。27/27 over-kill=0 直接回应了 "高精度是否靠牺牲召回" 的质疑。
2. **贡献 #2 的措辞修改精准到位**，不再把未验证的三个锚点当作已证明贡献。
3. **方法论插曲**（opus agent 编造 /mine 产物）虽然负面，反而强化了 CTS 核心论点——"LLM agent 会编造，需独立锚点核验"。
4. **写作打磨全面落地：** 摘要 165 词、Related Work 20 篇、RQ2 3 个 case study、Threats 10 行、48/52 统一、stale TODO 清除。

**核心资产（经过 7 轮审阅 + 回复信校正始终成立）：**
- 28 个真实修复 → 实践影响无可争议
- Contract hallucination propagation → 可被广泛引用的概念贡献
- 单 LLM 6.7% vs TestVDB 69.2% → 架构必要性的硬证据
- 方法论诚实度出色 → 经过 7 轮审阅，这是论文最一致的加分项

**剩余天花板：**
- **模板**（格式门槛——纯执行，等导师定会议）
- **Discovery recall**（评估完整性天花板——B10 Option A 如果跑出来，是最后一个临门一脚）
- **"large-scale" 措辞**（易被审稿人抓辫子——改词即可）
- **成本/效率信息**（LLM 系统论文的标配——半天可补）

**投稿建议：**
- 如果目标 VLDB：必须换 PVLDB proceedings 模板 + 加强与向量检索内部机制的对接（DB 审稿人对 "浅层 boundary/validation" 批评会更严厉）
- 如果目标 SE 顶会 (ICSE/FSE/ISSTA/ASE)：当前稿件质量已接近 Accept 区间。补上 discovery recall 粗略估计 + 成本信息后，有望跨过 Accept 线
- 不建议再投次级 SE 会议——稿件已超过那个档位

---

# Round 8 — 三视角独立审稿 (against `paper-draft-vldb-final.tex`, 2026-07-11)

> **本轮变化：** 重新启动三个独立子 agent 对最新版 `paper-draft-vldb-final.tex` 进行盲审，主 agent 逐条核实后输出行动清单。相比 Round 7，本轮更聚焦于「仍未被解决的」评估缺口，而非已修复的表述问题。
> **Overall Prediction:** Weak Accept (R1 4/10, R2 4/10, R3 6/10 — 分裂但偏接受)
> **Date:** 2026-07-11

---

## Score Summary

| Dimension | R1 (Objective) | R2 (Strict) | R3 (Supportive) |
|-----------|:---------:|:---------:|:---------:|
| Soundness | 2/4 | 2/4 | 3/4 |
| Novelty | 2/4 | 2/4 | 3/4 |
| Presentation | 3/4 | 3/4 | 2/4 |
| **Overall** | **4/10 (Weak Reject)** | **4/10 (Weak Reject)** | **6/10 (Weak Accept)** |

**共识：** 三方审稿人都认可三个核心资产——(1) 28 个真实修复是硬通货，(2) contract hallucination propagation 是有价值的观察，(3) 方法论诚实度罕见。分歧点在于：(a) 三锚点 CTS 是否 over-claimed（R1/R2 认为严重，R3 认为已在 Remark 中诚实限定），(b) 单 LLM baseline n=15 是否足够支撑架构必要性论证（R2 认为不够，R1 认为统计力不足），(c) 发现集中于 boundary/validation 是否降低 novelty（R2 认为严重，R3 认为可接受）。

---

## Reviewer 1 — Objective Reviewer (Confidence: 4/5)

**Summary**
TestVDB 是首个针对 VDBMS API 合规缺陷的 LLM 驱动检测器。核心设计原则 CTS 将 LLM 生成的契约断言与维护者权威支撑的真值层分离。跨 5 个 VDBMS 提交 111 个 issue，维护者确认 36 个（28 已修复）。受控回溯实验显示 source-grounding 锚点将 FP 抑制从 31% 提升到 81%，TP 保留率 96.7%。问题适时、实证产出非虚，但论文系统性地 over-claims 已验证的内容，"five VDBMSs" 在已裁决信号分布上慷慨，且多项核心贡献依赖作者自身也承认尚不完整或轶事级的证据。

**Strengths**
1. **真实的 bug 产出。** 28 fixed + 8 accepted-open 在真实维护者 tracker 上（Milvus #47729, #49844, #50193）是可独立核实的硬证据。
2. **诚实的边界划定。** Table 2、VDBFuzz complementarity 段落、敏感性区间 [43.9%, 80.5%]、RQ4 negative result——透明度罕见。
3. **Contract hallucination propagation 是有洞察力的观察。** constant.go 的虚构 provenance + 12/48 by-design 案例抓住了 LLM-driven testing 领域欠表达的失败模式。
4. **受控回溯设计合理。** 同一 52-candidate 总体、claim-only vs. source-grounded、label-isolated——这是隔离 source anchor 贡献的正确方法。
5. **与 VDBFuzz 的互补定位干净。** 不声称解决 result-correctness，只是填补 crash oracle 无法覆盖的空白。

**Weaknesses**

1. <span style="color:#dc2626">**[Major]**</span> **"三锚点 counter-evidence design" 作为贡献被 over-claimed。** Contribution #2 (L96) 兜售 "three-anchor counter-evidence design (clean reproduction, source-grounding, threat-model cross-check)"，但论文别处明确只有 source-grounding 被测量：Fig.1 将两个锚点灰显为 "not yet evaluated"，L261 承认 "reproduction and threat-model anchors as unmeasured future components"，§5.4 报告 TM anchor 产生 exploratory negative result (n=5, blindspot indicators never populated)。一个设计原则三分之二的实例化机制未经验证（且其中之一为负结果），不能合理地被推销为 "三锚点设计"——它是 **单锚点已验证设计** 加两个草图扩展。这是论文最严重的 over-claim，实质性膨胀了 novelty。摘要和引言应统一为 "source-grounded falsification" 或 "a design principle with three anchors, of which one is validated"。

2. <span style="color:#dc2626">**[Major]**</span> **"Across five VDBMSs" 在已裁决信号分布下具有误导性。** Table 2 显示 Milvus (51) + Qdrant (26) 供给 77/111 投稿且几乎全部已裁决信号（Milvus: 34 adjudicated, Qdrant: 14; Weaviate: 4; MeiliSearch 全部 pending/excluded; Chroma: 1 pending）。全部 12 个 by-design 案例和全部 28 个修复集中在 Milvus+Qdrant。论文 L211 承认 "cross-system generalization is claimed primarily for Milvus and Qdrant"——但这个让步与摘要的 "Across five VDBMSs" (L47) 和 Contribution #1 的 "validated across five VDBMSs" (L95) 矛盾。声称应收敛为 "two VDBMSs with adjudicated signal, with breadth probes on three more"。

3. <span style="color:#dc2626">**[Major]**</span> **Baseline 对顶会 SE  venues 偏弱。** 论文提供两个 baseline：(a) 单 LLM 端到端 6.7% (n=15, Wilson CI [0.2%, 31.5%], L259)；(b) A1 单层反事实 (L257)。6.7% 的 Wilson CI 上界达到 31.5%——与 claim-only 的 Milvus 内 33% 重叠——6.7-vs-69.2% 的比较在 n=15 下不具统计意义。A1 反事实用 "5-batch LLM adjudication + 7 live re-probes" 作为 proxy ground truth 重新裁决 27 个被 kill 的候选；论文自身在 Threats 中标记了此限制 (L269)。ICSE/FSE/ISSTA/ASE 期望更强的 baseline 集合——如 plain LLM+RAG-over-source pipeline，EvoMaster 或 RESTler 在相同 API surface 上的运行，或重新提交单层 cohort 给维护者裁决。

4. <span style="color:#dc2626">**[Major]**</span> **Discovery recall 完全推迟，75% boundary/validation 集中加剧了顾虑。** 论文承认 "96.7% figure is judgment-layer TP retention, not end-to-end discovery recall (future work)" (L269)，且 contract coverage 段落 (L263) 记录了 pilot 在测得真实 recall 之前就遇到 spec-completeness 和 version-pinning 限制。结合 L232 的发现 27/36 (75%) 确认 TP 是 boundary/validation——正是 schema-based fuzzing 最容易覆盖的子类——读者无法判断 TestVDB 相对更便宜的 schema fuzzer 的 edge 是否有意义，还是 LLM stack 对边界探测而言 over-engineered。

5. <span style="color:#dc2626">**[Major]**</span> **Contract hallucination propagation "观察" 作为贡献仍证据不足。** Contribution #3 (L97) 标为 "qualitative finding"，§4 (L203) 声明 "a quantitative study of hallucination frequency is future work"。这智力上诚实，但意味着贡献退化为 (a) 一个 constant.go 轶事 (L199) 和 (b) 一个 12/48 by-design 计数，其因果归因（hallucination vs. genuine spec ambiguity）未被解耦。by-design 案例可能同样反映合法维护者裁量（幂等 create、最终一致性），任何基于规约的 oracle——LLM 或人工——都会误分类。最低限度的频率研究——如更换生成器 LLM 族并重新测量 by-design 率，或手动审计 12 个是否源于幻觉约束 vs. 维护者裁量——会实质性硬化此 claim。

6. <span style="color:#dc2626">**[Major]**</span> **模板不匹配与投稿就绪度。** 文件名为 `paper-draft-vldb-final.tex` 但使用 `\documentclass[sigconf]{acmart}` (L3) 和占位符 ACM 元数据 ("Conference'26", L9; "978-1-4503-XXXX-X", L10; "Submission #XXX", L37)。VLDB 使用 PVLDB 自己的 class file (`vldb.cls`)，不是 `acmart`。若目标会议是 SE 测试顶会则文件名错；若 VLDB 则 class file 错。任一种情况下，论文都不是 template-ready。

7. <span style="color:#d97706">**[Minor]**</span> **数字一致性：** Abstract 引用 96.7% TP retention；RQ3 (L245) 报告 29/30 = 96.7%, n=30（6 TP 从原始 36 被 rate-limit）。Abstract 未披露此缩减，读者可能合理假定 96.7% 基于 36。L82 说 "12 of the 48 substantively adjudicated" (25%)，Table 2 显示 52 adjudicated (36+12+4)。"48" 来自减去 4 rejected。"48" 与 "52" 两处分母在同一篇中反复切换——首次出现时应加括号定义。

8. <span style="color:#d97706">**[Minor]**</span> **A1 "27/27 dev-reviewer precision, over-kill 0/27" (L257) 使用 proxy oracle 验证了产出候选的同一层。** 27 个 kill 由 "5-batch LLM adjudication + 7 live re-probes" 重新裁决。只有 7 个 live re-probes 是外部真值；其余 20 个依赖 LLM agreement。7 个中有 2 个 "overturned the LLM's initial TP"，推及 20 个 LLM-only kill 预期约 6 个可能有误。27/27 headline 相对自身噪声模型是乐观的。

9. <span style="color:#d97706">**[Minor]**</span> **GLM-5.2 backbone 配 "opus/sonnet" tier 标签 (L138) 造成困惑。** 论文说 "opus/sonnet denote prompting-and-budget configurations of the same GLM-5.2 backbone rather than different model families。" 这是不寻常的术语（opus/sonnet 是 Anthropic 模型名），在 LLM backbone 对幻觉论点重要的段落里引入读者混淆。

10. <span style="color:#d97706">**[Minor]**</span> **Threat-model prior contribution 实质为零。** §5.4 (L266) 报告 TM prior 从未填充且 n=5 不稳定。却仍列在 Fig.1 的三个 anchor 中和 Contribution #2 里。

11. <span style="color:#d97706">**[Minor]**</span> **"First LLM-driven realization" claim (Contribution #1, L95) 需要限定词。** BUZZBEE (L273) 和各类 LLM-based fuzzers 存在；"first" 应收紧为 "first for VDBMS API-compliance defects"。

**Questions for Authors**
1. 若 reproduction 和 threat-model anchor 未测量，为何贡献框架仍为三锚点设计而非 source-anchor 设计加两个推测性扩展？
2. 纯 OpenAPI-fuzzer (RESTler 或 EvoMaster) 在占 75% 产出的 boundary/validation 子类上预期性能如何？缺此比较，如何为 bulk 发现辩护 LLM stack 的必要性？
3. 能否将 12 个 by-design 案例分解为 (a) 幻觉约束维护者从未打算 vs. (b) 真实约束维护者选择放宽？仅 (a) 支持 "contract hallucination propagation" 机制。
4. A1 反事实中，分离 7 live-reprobe 案例与 20 LLM-only 重新裁决的结果？限制为外部 ground truth 时 27/27 还成立吗？
5. 为何在 abstract 中报告 96.7% TP retention over n=30（非完整 36）而不披露 6-case reduction？若审稿人在 worst-case fill-in 下算成 29/36=80.6%，会接受吗？

**Scores**
- Soundness: 2/4 — source-anchor retrospective 是可靠的；三锚点 framing、单 LLM baseline n=15、A1 proxy-ground-truth 论证各有实际方法学缺口
- Novelty: 2/4 — contract hallucination propagation 是新鲜有趣的观察但仍是定性；CTS-as-source-grounding 接近标准 RAG-for-verification
- Presentation: 3/4 — 结构清晰、边界 disciplined、threats-to-validity 诚实；被 acmart/VLDB template mismatch、摘要三锚点 over-claim、数值分母不一致 (48 vs 52, 30 vs 36) 拖累
- Overall: 4/10 — Weak Reject。真实 bug 发现 + 诚实 report + 有趣的 hallucination propagation 观察。但核心方法学贡献相对已验证内容 over-claimed，baselines 对顶会 SE venues 偏薄，discovery recall 完全推迟，template/venue readiness 未定。

---

## Reviewer 2 — Strict Reviewer (Confidence: 4/5)

**Summary**
论文引入 "TestVDB"，一个 LLM-agent pipeline 用于检测向量数据库的 API 合规缺陷，配以一个重新包装的工程原则 ("Contract-Truth Separation")。尽管问题真实且有真实 bug 发现，论文反复 over-claims novelty，将 modest empirical study 错标为 "multi-system"，并提供了一个分散的评估——甚至缺少单个非 LLM baseline。

**Strengths**
- 问题 framing 真实：incorrect-behavior bugs (43%) 确实超过 crash/hang (23%) 且 VDBFuzz 的 crash oracle 确实对其盲。
- "Contract hallucination propagation" 观察配 concrete constant.go 示例 (§4) 是一个不错的、可记忆的定性发现。
- 报告 pending-sensitivity interval [43.9%, 80.5%] 而非仅点估计 69.2% (§5.3) 是 refreshingly candid。
- 论文对其边界 unusually forthcoming（TM prior 从未填充；3 anchors 中 2 个未测量；MeiliSearch 和 Chroma 近乎零信号；27/27 A1 结果部分 undermine 多 agent 架构）。

**Weaknesses**

1. <span style="color:#dc2626">**[Major]**</span> **"Contract-Truth Separation" 原则是重新包装的工程决策，非科学贡献。** 论文反复断言 CTS 为 "design principle" (§1 Contributions #2, §3.4)。剥去命名，机制是："当 LLM 说 X，也查源码。" 形式化 "$C_{\mathrm{LLM}} \supset C_{\mathrm{true}}$" (§4) 重述了 LLM specs 可能 over-strict——一旦接受 LLMs hallucinate 就是 tautology。没有证明、没有复杂度 claim、没有 bound、没有与任何 LLM extractor+verifier 工作流的区分。论文需 (a) 放弃 "principle" claim 呈现为工程 pattern，或 (b) 证明 CTS 非平凡地超越 "consult source" 泛化。

2. <span style="color:#dc2626">**[Major]**</span> **无 rule-based / schema-validation baseline。** 论文承认 75% 真阳性是 boundary/validation (§5.1)——`nprobe=0`, `shardsNum=-1`, empty filter 触发全扫描 (Milvus #49844), `consistencyLevel="INVALID"` 静默接受。这些是教科书级 OpenAPI/JSON-Schema 违规。若 Milvus 自身的 OpenAPI/proto specs 包含 enum 值和整数边界，两行 schema validator 能捕获其中许多。然而论文只与 (i) 单 LLM (n=15) 和 (ii) 自身去 dev-reviewer 版本比较。没有与 `Schemathesis`、RESTler (已引但未比)、或手写 boundary-value fuzzer 的比较。无此 baseline，读者无法知道 TestVDB 是否值得 20-agent、GLM-5.2 驱动的复杂度，或只是一个昂贵的 schema linter。

3. <span style="color:#dc2626">**[Major]**</span> **单 LLM baseline (n=15, precision 6.7%) 统计无力。** §5.3 报告 Wilson 95% CI [0.2%, 31.5%]——区间如此之宽，"baseline" 基本不传达信息。但论文在同一段用其 justify 整个 "multi-agent + CTS is jointly necessary" claim。此外，14 个 FP 中 4 个 "failed on a query-vector dimension mismatch before their target invariant was exercised"——这些是 prompt/execution 失败，不是 judgment 失败，inflate 了 baseline 的 FP 计数。公平比较需要至少 n≈50-100 per arm 并 de-biasing prompt-execution errors。

4. <span style="color:#dc2626">**[Major]**</span> **A1 结果 (single LLM with source: 27/27 precision) 与架构叙事矛盾。** §5.3 自身承认："a single LLM *with extracted source* matches dev-reviewer precision at 27/27。" 这是一个 devastating internal finding：它说多 agent debate、四 judges、novelty gate、20-agent scaffold 在 source grounding 存在时对 **judgment stage 不必要**。作者通过断言 debate 在 probe generation 侧 "jointly necessary end-to-end" 来转移——但从未对单 LLM-with-source 变体做 generation 消融。考虑 §3.1 的 4-opus/16-sonnet 成本 profile，这个省略看起来像保护一个证据不支持的更昂贵设计。保持单 LLM generation 配 source-anchored verification 的消融是 obvious missing arm。

5. <span style="color:#dc2626">**[Major]**</span> **可复现性对 SE 测试 venue 不足。** §3.1 声明 "Agents inherit the Claude Code runtime's default sampling configuration with no explicit temperature override" 和 "full prompts in the artifact。" 论文没有报告 temperature、top-p、per-agent token budgets、美元成本合计、wall-clock、GLM-5.2 version/date、以及 artifact URL（仅 "to be made public on acceptance"）。judgment-layer noise claim ("99.1% pairwise agreement," Threats to Validity) 无 seeds 和版本不可验证。对于 LLM-driven testing paper，这低于 ICSE/FSE/ISSTA/ASE 可复现性指南标准。

6. <span style="color:#dc2626">**[Major]**</span> **"Opus tier" vs "sonnet tier" of GLM-5.2 是非标准命名法，模糊了设置。** §3.1: "opus/sonnet denote prompting-and-budget configurations of the same GLM-5.2 backbone rather than different model families。" 借用 Anthropic 的专有命名标注内部预算 knob 是困惑的，貌似是面向审稿人的障眼法——让读者假定异构 ensemble，实际论文使用单一模型配两个 prompt-length regimes。使用中性名称（如 "high-budget/low-budget agent class"）并 specify 实际差异（context length, max output tokens, system prompt length）。

7. <span style="color:#d97706">**[Minor]**</span> **Related Work (§6) 偏薄且定位不准。** 约 12 citations 跨五段。缺失：LLM-based DBMS testing beyond MeTMaP；LLM-as-judge 批评和自我验证失败文献（这正是 "contract hallucination propagation" 实例化的）；OpenAPI conformance testing (Schemathesis, Dredd)；grammar-based API fuzzing beyond RESTler/EvoMaster。

8. <span style="color:#d97706">**[Minor]**</span> **Threats to Validity (§5.5) 约 10 行且省略严重威胁。** 缺失/欠展开：(a) selection bias in which 111 were submitted out of unstated candidate pool；(b) reviewer-effect: maintainer acknowledgment 与 report clarity 相关，非 defect validity；(c) contamination: GLM-5.2 可能在训练中见过 Milvus GitHub，inflate source-anchor 的 apparent power；(d) 29 "excluded" (closed-no-label/duplicate) 被 dismiss 为 "unresolvable" 但许多 "closed-no-label" 案例是隐式拒绝。

9. <span style="color:#d97706">**[Minor]**</span> **20 agents 的成本合理性缺失。** §3.1 casually mentions 20 agents。Given 27/27 A1 finding，读者需要数字：per-run dollar cost、tokens、latency vs. single-LLM-with-source condition、Pareto analysis (bugs/$)。

10. <span style="color:#d97706">**[Minor]**</span> **Case Studies (§5.2) 全是 Milvus。** 四个案例中三个是 Milvus；第四个是 cosine 跨系统不变量。没有 Qdrant、Weaviate 的端到端走查。

11. <span style="color:#d97706">**[Minor]**</span> **"Contract hallucination propagation" 定量证据弱。** §4 依赖 "12 of 48 (25%)" by-design 案例。但 by-design ≠ 幻觉——也可以意味着维护者意图与文档分歧（文档 bug，非幻觉）。论文混为一谈。正确分析应分类每个 12 为 (a) LLM 发明了文档中不存在的约束，(b) LLM 从文档正确提取但文档与意图分歧，(c) 文档和代码不同。

13. <span style="color:#d97706">**[Minor]**</span> **Excluded-set 处理有疑。** §5.3 断言 29 excluded "lie outside" 敏感性区间因为 "true compliance status is unknowable post-closure。" 但 29 中 17 个是 Milvus——TestVDB 产出最高的同一系统。若 closed-no-label 反映维护者 non-engagement，排除它们可能隐藏大量 FP tail。

**Questions for Authors**
1. 能否展示一个 schema-validation baseline（Schemathesis + Milvus OpenAPI spec）对你的 5 个 VDBMS 运行？27 个 boundary/validation TP 中多少被它检测到？
2. Given A1 finding (single LLM + source = 27/27 judgment precision)，多 agent debate 贡献了什么单 LLM-with-source 做不到的？请加 missing arm: single-LLM generation + source-anchored verification，报告端到端 precision。
3. 具体成本数字（USD, tokens, wall-clock）for TestVDB vs. single-LLM baseline vs. hypothetical schema-validator baseline？
4. 提供 artifact URL（即使 anonymized），包括 prompts、temperature、model versions、seeds、exact dates。
5. For 12 by-design cases underpinning §4: 多少是 LLM 发明的约束 vs. LLM 从文档正确提取但文档与意图分歧？请逐例分类。
6. Selection ratio 是多少：pipeline 生成了多少候选 issues，111 个 submitted 如何从中选择？
7. 有审计 GLM-5.2 训练数据是否 likely 包含 pre-2024 Milvus GitHub source 吗？这对 source-anchor 声称的 generality 有何影响？

**Scores**
- Soundness: 2/4 — 真实 bug 发现，但核心比较 (schema baseline, larger single-LLM baseline, cost accounting) 缺失；内部 27/27 result 部分 contradict 架构 claim
- Novelty: 2/4 — "contract hallucination propagation" observation 是好的定性 framing；"Contract-Truth Separation" 作为原则被 over-claimed
- Presentation: 3/4 — 异常 candid about limits，可读性好；被 "multi-system" 和 "opus/sonnet tier" rhetoric 削弱
- Overall: 4/10 — Weak Reject。有趣问题，诚实报告，真实 bug，但贡献 as-framed 被 oversold 且评估缺少 ICSE/FSE/ISSTA/ASE 期望的 baselines 和 rigor。

---

## Reviewer 3 — Supportive Reviewer (Confidence: 3/5)

**Summary**
这篇论文承接了一个真实 underserved 的问题——向量数据库系统中的非崩溃 API 合规缺陷——并交付了看起来是首个此类 bug 的端到端 LLM 驱动检测器，由 28 个跨生产 VDBMSs (Milvus, Qdrant, Weaviate 等) 的真实修复验证。**Contract-Truth Separation (CTS)** 作为缓解 **contract hallucination propagation** 的 framing 是一个真正有用的概念贡献，我相信会比特定 artifact 活得更久。论文对自身限制 unusually honest，增加了我对报告数字的信心。

**Strengths**
1. **罕见的高信号实证产出。** 111 submissions → 36 maintainer-acknowledged → **28 fixed** 跨五生产 VDBMSs 是 substantial 且难以伪造的结果。真实 upstream patches 是 testing paper 的金标准证据。
2. **Contract hallucination propagation 是可泛化的概念。** 单一 LLM 族生成并判断契约产生相互确认的观察 (§4) 是一个干净、可移植的失败模式。
3. **CTS 是干净的架构原则。** 将断言层与真值层分离，通过 source-grounded verification 实例化真值层，正是那种能存活 implementation churn 的设计抽象。
4. **COSINE > 1.0 是论文最 novel 的技术结果。** 刚性数学不变量违背——余弦相似度应在 [-1,1] 内——在 Milvus 和 Qdrant 独立复现，是 striking 的 model-free oracle result。作者 underselling 这一点。
5. **严谨透明的 RQ3 方法论。** 同总体受控回溯 (31%→81% FP 抑制, 96.7% TP 保留) 是正确的实验设计，报告敏感性区间 [43.9%, 80.5%] 而非 cherry-picking。
6. **A1 单层反事实非常强。** 27/27 dev-reviewer kills 被确认为真 FP，**over-kill = 0**——异常干净地证明 FP-suppression 精度增益不牺牲召回。
7. **B9 单 LLM baseline (6.7% vs. 69.2%) 有说服力。** ~10× gap 加 Wilson CI [0.2%, 31.5%] 使架构贡献 (multi-agent debate + CTS) 在经验上可辩护。
8. **方法学诚实是真实加分项。** RQ4 作为 acknowledged negative result、Fig.1 灰显未验证锚点、"excluded 29" bucket 解释而非隐藏、anchor-attribution 段直言只有 source anchor 被测量——读起来像作者 in good faith。
9. **与 VDBFuzz 的定位精准且不膨胀。** 明确不声称解决 result-correctness oracles，框架为互补而非竞争——成熟姿态。
10. **论文预判自身批评。** Threats-to-validity、discovery recall 明确差距、reproduction/threat-model anchors 标注未测量——显示了 self-aware author。

**Weaknesses**

1. <span style="color:#dc2626">**[Major — 但容易修]**</span> **模板与目标 venue 不匹配。** 论文使用 `\documentclass[sigconf]{acmart}` 配 `\acmConference{Proceedings of the ACM Conference}` 占位符元数据，但文件名提及 VLDB 且评审针对 SE testing venues。投稿前必须解决：选定 venue，使用其模板。

2. <span style="color:#dc2626">**[Major]**</span> **Discovery recall 是最大的剩余证据缺口。** 论文诚实声明 "96.7% figure is judgment-layer TP retention, not end-to-end discovery recall。" 但粗略估计会实质性加强论文。即使在 20-30 个 held-out 合规 bugs 上的 pilot，bound 如 "TestVDB rediscovers k/n of them"，也能让读者推理 false-negative 侧。

3. <span style="color:#dc2626">**[Major]**</span> **"Five VDBMSs" claim 强于数据支持。** MeiliSearch (3 submissions, 0 adjudicated) 和 Chroma (1 submission, 0 acknowledged) 贡献近乎零信号。Abstract、intro、结论应收敛到已在 §5.1 存在的诚实 framing——"primarily Milvus and Qdrant, with the other three as breadth。"

4. <span style="color:#dc2626">**[Major]**</span> **成本/效率信息缺失。** 对于 20 role-prompted agents (4 opus-tier + 16 sonnet-tier) 的 LLM-agent 系统，审稿人会想要 token cost、wall-clock、和 $ per acknowledged bug。Reproducibility 段承诺 "precise per-token and wall-clock accounting is part of the anonymized artifact" 但论文中一个 summary table 会让读者判断实际可部署性。

5. <span style="color:#d97706">**[Minor]**</span> **提升 COSINE > 1.0 的位置。** 这是论文最 striking 的 novel 技术发现，值得比 RQ2 一个段落更多。考虑 dedicated subsection，因为它是 (a) 双系统可复现，(b) 完全独立于 LLM judgment，(c) 打开自然 bridge 到 future property-based work。

6. <span style="color:#d97706">**[Minor]**</span> **REST API 和云服务的泛化性值得多于一整句。** 结论指出 CTS "should extend to REST APIs and cloud services with documented contracts"——这是一个大 claim，§4 或 §7 一个简短段落描绘将 CTS 应用于 S3 或 Kubernetes API 契约的变化，将以最低成本显著提高论文 impact ceiling。

7. <span style="color:#d97706">**[Minor]**</span> **"Single-layer" 和 "single-LLM" baselines 可更显式统一。** A1 (单层反事实) 和 B9 (单 LLM 端到端) 一起提供强证据，但一个 summary table with rows = {single-LLM, single-layer 4-judge, TestVDB (source-grounded), TestVDB (full CTS)} and columns = {precision, TP recall proxy, FP suppression, cost} 会让画面更清晰。

8. <span style="color:#d97706">**[Minor]**</span> **96.7% 的统计 framing 偏薄。** n=30 retained TPs (其中 29 kept)，Wilson 95% CI 下界约 ~83%。与点估计一起报告会 preempt R2-style 关于 small-n retention claims 的异议。

9. <span style="color:#d97706">**[Minor]**</span> **Related-work 对 LLM-as-judge 失败模式的覆盖偏轻。** Given contract hallucination propagation 是中心概念贡献，连接到 LLM-as-judge bias 和自我一致性 (beyond just Wang et al.) 的增长文献体，有助于将观察定位为已知关注的形式实例。

10. <span style="color:#d97706">**[Minor]**</span> **RQ4 可移到 appendix。** "Blindspot indicators never populated" 是 candid but awkward 的承认。可重新框架更 crisp——要么从正文移除 RQ4 移到 appendix 作为 implementation note，要么用作下一篇论文设计的跳板。

**Questions for Authors**
1. 能否提供粗略 discovery-recall 估计——如在 Milvus 和 Qdrant 的已修复 pre-2024 合规 bugs 小集合上重放 TestVDB，报告重新发现的比例？
2. 大致成本 (tokens 和 $) per submission 和 per acknowledged bug？TestVDB 对持续使用是否可行，还是 one-shot audit tool？
3. For 21 pending Weaviate submissions: 有早期 triage 信号 (labels, maintainer comments) 能 tighten 敏感性区间吗？
4. Beyond VDBMSs，是否在小 REST-API case (如 S3-compatible 或 OpenAI-compatible API) 上尝试了 CTS 以验证结论中的泛化性？
5. 是否愿意将 RQ4 移到 appendix 并将 COSINE > 1.0 发现提升为 dedicated section on model-free invariant oracles？
6. CTS 对 backbone LLM 选择有多敏感？所有 agents 共享 GLM-5.2——有初步证据 CTS 在切换后存活 (Claude, GPT-5) 吗？
7. "Over-kill = 0" A1 结果对 re-running with different seed / prompt-order 是否 robust？

**Scores**
- Soundness: 3/4 — RQ3 方法论干净，ablations 强，对未验证锚点和 pending-sensitivity 的诚实度 unusual。Discovery recall 和跨系统 unevenness 阻止了 4。
- Novelty: 3/4 — Contract hallucination propagation + CTS 是真实概念贡献，COSINE > 1.0 model-free invariant finding 是 genuinely novel。不是 4 因为许多 machinery 重组已知成分 (multi-agent debate, retrieval-grounded verification, property-based invariants)。
- Presentation: 2/4 — 模板不匹配，"five VDBMSs" framing 在产量集中下 slightly over-reaches，RQ4 放置 awkward，最强技术发现 (COSINE) 被埋。全部可修复。
- Overall: 6/10 — **Weak Accept**。这是我想在 venue 看到的论文：贡献 genuine，实证产出罕见，方法学姿态诚实。我的保留在 discovery recall、跨系统证据 uneven、presentation polish——无一威胁核心 claims。修好模板、加粗略 recall bound、将 framing rescope 到证据最强的两个系统，我会移到 clear accept。

---

## Verification (Round 8 — 主 agent 逐条核实)

| # | Source | Claim | Verdict | Note |
|---|--------|-------|---------|------|
| 1 | R1-W1, R2-W1, R3 | "Three-anchor" over-claimed | <span style="color:#16a34a">**Valid**</span> | Contribution #2 (L96) headlines "three-anchor counter-evidence design"; Fig.1 灰显 repro/TM 为 "not yet evaluated"; L261 承认 "reproduction and threat-model anchors as unmeasured future components." 贡献声明的 headline 与实证支撑不匹配 |
| 2 | R1-W2, R3 | "Five VDBMSs" 在已裁决信号分布下 misleading | <span style="color:#16a34a">**Valid**</span> | Abstract (L47) "Across five VDBMSs"; L211 承认 "cross-system generalization is claimed primarily for Milvus and Qdrant." 两处不一致 |
| 3 | R1-W3, R2-W3 | 单 LLM baseline n=15 统计力弱 | <span style="color:#16a34a">**Valid**</span> | L259: Wilson CI [0.2%, 31.5%] — CI 上限与 claim-only 33% 重叠。4/14 FP 是 dimension-mismatch 执行失败而非判断失败 |
| 4 | R2-W2 | 无 schema-validation baseline | <span style="color:#16a34a">**Valid**</span> | 全文中无 RESTler/Schemathesis/OpenAPI validator 对比。75% yield 是 boundary/validation (L232) |
| 5 | R2-W4 | A1 27/27 与多 agent 架构叙事矛盾 | <span style="color:#d97706">**Partially valid with nuance**</span> | L259 承认 "single LLM with extracted source matches dev-reviewer precision at 27/27"——这是 judgment 层发现。论文将必要性论证移到 generation 侧。但缺 "single-LLM generation + source-anchored verification" 消融臂 |
| 6 | R2-W1 | CTS 作为重新包装的工程决策 | <span style="color:#d97706">**Subjective but reasonable**</span> | 形式化 C_LLM ⊃ C_true 是描述性而非分析性。评价取决于审稿人重理论还是重实践 |
| 7 | R1, R2, R3 | 模板不匹配 | <span style="color:#16a34a">**Valid**</span> | L3: `\documentclass[sigconf]{acmart}` + 占位符元数据。文件名含 "vldb"。投稿前必须解决 |
| 8 | R1, R3 | Discovery recall 完全推迟 | <span style="color:#16a34a">**Valid**</span> | L269: "96.7% figure is judgment-layer TP retention, not end-to-end discovery recall (future work)." Contract coverage pilot 6/9=67% 未扩大 |
| 9 | R2-W5 | 可复现性缺口 | <span style="color:#16a34a">**Valid**</span> | 缺 temperature, token budgets, dollar cost, artifact URL, GLM-5.2 version/date |
| 10 | R2-W6 | "Opus/sonnet tier" 命名困惑 | <span style="color:#16a34a">**Valid**</span> | L138-139 借用 Anthropic 专有命名标注 GLM 配置。论文解释到位但术语选择仍 confusing |
| 11 | R1-W5, R2-W7 | 48 vs 52 分母不一致 | <span style="color:#16a34a">**Valid**</span> | L82 用 48 (=36+12, excl. 4 rejected); L253 用 52 (=36+12+4). 自洽但首次出现时无括号定义 |
| 12 | R1-W8 | A1 27/27 混用 proxy+live ground truth | <span style="color:#16a34a">**Valid**</span> | L257: 7/27 live re-probes + 20/27 LLM adjudication. 2/7 overturned LLM's TP → ~29% overturn rate, projected to ~6 possible errors in 20 LLM-only |
| 13 | R2-W8 | Threats 省略严重威胁 | <span style="color:#16a34a">**Valid**</span> | 约 10 行，缺 selection bias (submission ratio unreported), contamination (GLM-5.2 training data), excluded-set audit |
| 14 | R3 | "Multi-system" not "large-scale" | <span style="color:#dc2626">**Round 7 已修**</span> | L95 已为 "multi-system empirical study" (非 "large-scale"). R2-W2 的此具体点已过时 |
| 15 | R3 | COSINE>1.0 仍被埋 | <span style="color:#16a34a">**Valid**</span> | L239: "Model-free mathematical-invariant oracle" 在 RQ2 提到，但仍是半段落而非独立 subsection |

---

## Action Plan (Round 8)

### <span style="color:#dc2626">Must Fix</span> — 多人共识，不改大概率被拦

- [ ] **P0-1: 收窄"三锚点"贡献声明。** Contribution #2 (L96) headline 从 "three-anchor counter-evidence design" → "source-grounded verification (validated), within a three-anchor design where reproduction and threat-model anchors are designed but not yet evaluated." 保持 Fig.1 灰显处理一致，但文字 headline 必须对齐实证现实。Abstract 同步修改。
- [ ] **P0-2: 收敛"five VDBMSs" 泛化措辞。** Abstract (L47)、Contribution #1 (L95)、conclusion 的 "across/spanning five VDBMSs" → "across two VDBMSs with adjudicated signal (Milvus and Qdrant), with breadth probes on three more." 或同效的诚实 framing。与 L211 "primarily Milvus and Qdrant" 一致。
- [ ] **P0-3: 换模板。** `\documentclass[sigconf]{acmart}` → 目标会议模板。确认投稿 venue（PVLDB 或 SE 顶会），更新全部元数据。文件名与模板对齐。
- [ ] **P0-4: 加至少一个像样的非 LLM baseline。** 最具可行性：Schemathesis 或 RESTler 在 Milvus API 上运行（利用其 OpenAPI spec），报告 boundary/validation 子类上的 detection+FPs。若无法补实验，需在 Limitations 中详细说透为何做不了 + 何时能做。当前 "单 LLM 6.7%" 不足以支撑架构必要性论证（n=15, CI [0.2%, 31.5%]）。

### <span style="color:#d97706">Should Fix</span> — 不改会被误解或降分

- [ ] **P1-1: 扩大单 LLM baseline 样本量。** n=15 → n≥50，确保 CI 不与 claim-only precision 重叠。同时 de-bias prompt-execution errors（dimension-mismatch 等不是判断失败）。
- [ ] **P1-2: 加 "single-LLM generation + source-anchored verification" 消融臂。** 这是 R2-W4 的 missing arm——直接回应 "A1 27/27 是否使多 agent 架构不必要" 的质疑。
- [ ] **P1-3: 给 discovery recall 一个更好的估计。** 扩大 contract coverage 探针（当前 6/9），或对 held-out 已修 bug 跑完整 pipeline。即使是粗略 bound 也比空白好。B10 Option A pilot 的发现 (spec-completeness + version-pinning limits) 已写进 §5，但数字未扩大。
- [ ] **P1-4: 加成本/效率表。** token 消耗、API 调用次数、wall-clock、$ per acknowledged bug。LLM 系统论文的标配。
- [ ] **P1-5: 补 artifact link。** 即使 anonymized (anonymous.4open.science 或 Zenodo)。Contribution #4 声称 "open-source system" 但正文无链接。
- [ ] **P1-6: 统一 "48" 与 "52" 口径。** L82 首次出现 "48 substantively adjudicated" 时加括号定义 (= acknowledged + by-design, excluding 4 rejected)。避免与 L253 的 52 混淆。
- [ ] **P1-7: 收窄 "opus/sonnet" 命名。** 或用中性名称 "high-budget/low-budget agent class"，或至少加 footnote 解释这不是 Anthropic 模型族。避免审稿人误读。
- [ ] **P1-8: 扩大 Threats to Validity。** 当前 ~10 行省略了关键威胁。至少加：selection bias (submission ratio)、GLM-5.2 training data contamination、excluded-set audit (至少 random sample of 29)。
- [ ] **P1-9: 分离 A1 27/27 中的 live vs. LLM-proxy ground truth。** 报告 7/7 live re-probe result vs. 20/20 LLM-only separately，让读者自行判断 27/27 headline 的稳健性。

### <span style="color:#6b7280">Optional</span> — 锦上添花

- [ ] **提升 COSINE > 1.0 为独立 subsection。** 论文最 novel 的技术发现，不依赖 LLM judgment，值得 "Model-free invariant oracles: a complementary subclass" 独立小节。可能比 CTS 更有辨识度。
- [ ] **讨论 CTS 泛化性。** 一个简短段落将 CTS 应用于 REST API/云服务契约，会增加 impact 感。与 Conclusion 最后一句话呼应。
- [ ] **扩充 §5.2 Case Studies 至少一个 Qdrant 案例。** 当前全 Milvus。至少需要一个 Qdrant 端到端走查支撑 "cross-system" narrative。
- [ ] **Classify 12 by-design cases。** 分解为 hallucinated constraints vs. maintainer-discretion relaxations。Only former supports "contract hallucination propagation" mechanism. 定性分类即可，不需要新实验。
- [ ] **RQ4 移到 appendix 或删除。** 当前是 candid but awkward 的 distraction。保留为 implementation note，不在正文占用评估空间。

---

## Round 8 Overall Assessment

**预测：Weak Accept（分裂票，R1/R2 Weak Reject, R3 Weak Accept）。** 这是 rebuttal 后大概率被接受的分裂模式——R3 的 6/10 通常能说服 AC。

**核心资产（经过 8 轮审阅始终成立）：**
- 28 个真实修复 → 实践影响无可争议
- Contract hallucination propagation → 可被广泛引用的概念贡献
- 方法学诚实度出色 → 8 轮审阅始终是论文最一致的加分项
- A1 27/27 over-kill=0 + 单 LLM 6.7% vs 69.2% → 架构价值有实证支持
- COSINE > 1.0 数学不变量 → 论文最亮技术发现，跨厂商复现

**相比 Round 7 的变化：**
- 贡献措辞收敛 ("multi-system" 已修)、摘要精简、RQ2 充实、Related Work 20 篇、Threats 压缩——写作侧几乎清完。
- **本轮新发现的本质性问题：** (1) "三锚点" headline 与 Fig.1/L261 的诚实自述仍不一致——改词即可；(2) 单 LLM baseline n=15 被三方审稿人同时质疑统计效力——需扩大样本量；(3) Schema-validation baseline 完全缺失——对 75% boundary/validation yield 而言是显著空白。
- **评级天花板：** 模板 (执行项)、discovery recall (实质性 gap)、schema baseline (实质性 gap)。前两项是已知问题，第三项是本轮新暴露的。
- **投稿建议不变：** 若 VLDB → 换 PVLDB 模板 + 加强向量检索内部机制对接；若 SE 顶会 (ICSE/FSE/ISSTA/ASE) → 当前质量接近 Accept 区间，补上 schema baseline + 更大单 LLM baseline + discovery recall 粗略估计后有望跨线。

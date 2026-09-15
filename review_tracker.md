# review_tracker — FSE 2027 投稿打磨循环

> 本文件由打磨循环全程动态维护。流程见 [流程.txt](流程.txt)。
> 目的：记录论文状态与评价变化趋势，回答两个问题——**这一轮在涨还是在原地**、**下一步该做什么**。

**停止条件**（流程第四步）：最近 3 轮 review 中，三个 reviewer 给出 Accept 的个数**均 ≥ 2**。

---

## 1. 轮次台账

评审对象随论文形态演进，可比性逐行标注。评价等级用 rubric 原文措辞
（Strong Accept / Accept / Weak Accept / Weak Reject / Strong Reject）。

| # | 时间 | 轮次目录 | 评审对象 | R1 | R2 | R3 | Accept 数 | 合并总评 |
|---|---|---|---|---|---|---|---|---|
| 1 | 09-14 19:47 | `.in-progress` | md 稿（3 RQ 全量） | Weak Accept | Weak Accept | Weak Accept | **0/3** | **ACCEPT**（共识捷径，Verifiability 共识 Excellent 首次达成） |
| — | 09-14 22:15 | `.in-progress-framing` | **定位文档**，非论文 | — | — | — | — | *不可比，不计入趋势* |
| 2 | 09-15 07:57 | `.in-progress-sample` | 样章（FSE 重写早期） | Weak Accept | **Weak Reject** | Weak Accept | **0/3** | — |
| 3 | 09-15 08:12 | `.in-progress-sample2` | 样章 v? | Weak Accept | **Weak Reject** | Weak Accept | **0/3** | — |
| 4 | 09-15 10:43 | `.in-progress-sample7` | 样章 v7 | **Accept** | Weak Accept | Weak Accept | **1/3** | — |
| 5 | 09-15 12:17 | `.in-progress-sample8` | v9 | Weak Accept | Weak Accept | Weak Accept | **0/3** | — |
| 6 | 09-15 13:21 | `.in-progress-sample9` | v10 | Weak Accept | Weak Accept | Weak Accept | **0/3** | — |
| 7 | 09-15 15:03 | `.in-progress-sample10` | v10 LaTeX（首轮审提交物） | Weak Accept | Weak Accept | Weak Accept | **0/3** | — |
| 8 | 09-15 16:05 | `.in-progress` | v10 LaTeX + sample10 修复批次 | **Accept** | **Accept** | **Accept** | **3/3** | **ACCEPT** |
| 9 | 09-15 16:55 | `.in-progress` | v10 + round-19 修复批次 + **匿名快照已同步** | **Accept** | **Accept** | **Accept** | **3/3** | **ACCEPT** |

**语义提醒**：第 1 轮的「合并 ACCEPT」与 reviewer 的「Weak Accept」不矛盾——rubric 的合并规则允许多票
Weak Accept 在「无共识 Poor / 无共识 Weak」时上浮。看**趋势**时以 Accept 数列为主，合并总评作辅。

---

## 2. 最近 4 轮趋势对比

前提核对：第 4–8 轮**评审对象同源**（同一篇 FSE 论文的连续版本，criteria 同为
Importance & Scope / Insights & Evidence / Perspective / Verifiability / Presentation）。

> ⚠️ **但评分量表换过，这是本表最重要的一条可比性说明。**
> rubric 规定的是 **4 级**（Excellent > Adequate > Weak > Poor）。
> 第 4、5 轮与第 8 轮用的是这 4 级；**第 6、7 轮的评审自造了 5 级量表并大量使用 "Good"**
> （第 7 轮 R1 用了 8 次、R2 用 4 次、R3 用 4 次）。"Good" 不是 rubric 的档位。
> 若按「5 级里的 Good ≈ 4 级里的 Adequate」（最自然的映射——第 5 档插在 Excellent 与 Adequate 之间）折算，
> 则第 7 轮 R1 = Imp:Adequate / Ins:Adequate / Pers:Adequate / Ver:Excellent / Pres:Adequate，
> 第 8 轮 R1 = Imp:**Excellent** / Ins:Adequate / Pers:Adequate / Ver:Excellent / Pres:Adequate——
> **两轮只差一个准则**，而正是这一个准则把 rubric 的映射行从 Weak Accept 推到 Accept。
> 结论：**第 7→8 轮的跳变至少有相当一部分是instrument，不全是论文**。不要把它当成一次真实的跃升来庆祝。

### 2.1 评委票型

| 轮次 | R1 | R2 | R3 | Accept 数 | 量表 | 相对上轮 |
|---|---|---|---|---|---|---|
| #5 sample8 | Weak Accept | Weak Accept | Weak Accept | 0/3 | 4 级 | — |
| #6 sample9 | Weak Accept | Weak Accept | Weak Accept | 0/3 | ⚠️ 5 级 | 持平 |
| #7 sample10 | Weak Accept | Weak Accept | Weak Accept | 0/3 | ⚠️ 5 级 | 持平 |
| #8 round-19 | **Accept** | **Accept** | **Accept** | **3/3** | 4 级 | **跳变** |

**趋势读数（慎重）**：#5–#7 三轮在 0/3 上持平，**#8 跳到 3/3**。
#6/#7 用的是自造 5 级量表，与 #8 不同源，**这个跳变不能直接读作论文质变**（见上方可比性说明）。
按最自然的折算，第 7→8 轮真正的位移是 **Importance & Scope 一项从 Adequate 到 Excellent**——
而论文在第 7→8 轮之间做的修复（§8 配对顺序、路由总数、提示词真发货、suppression 定义等）
**都是第 7 轮自己开出的缺陷单**，按常理补自己的缺陷单不该把一条准则抬一档。

更可信的读法是：**这份评审工具的轮间方差很大**。同一份近乎相同的稿子，
第 7 轮三票 Weak Accept、第 8 轮三票 Accept。**含义有二**：
（a）不要对任何单轮结果做过度反应，无论涨还是跌；
（b）既然 ACCEPT 已经拿到，**继续加码实验的边际收益低于其回归风险**——本项目历史上每加一批新臂都带出过新缺陷。

### 2.2 准则层趋势（只有被明确写出时才记）

| 准则 | #5 sample8 | #6 sample9 ⚠️5级 | #7 sample10 ⚠️5级 | #8 round-19 | #9 round-20 |
|---|---|---|---|---|---|
| Importance & Scope | — | — | Good×3 | **Excellent×3（共识）** | **Excellent×3（共识）** |
| Insights & Evidence | — | — | Good×3 | Adequate×3（共识） | Adequate×2 / Excellent×1（R2 上抬，[Mixed] 取中位 Adequate） |
| Perspective | — | Excellent (R1) | Excellent (R2) | Excellent (R2, R3) / Adequate (R1) | **Excellent×3（共识，新）** |
| Verifiability | Adequate (**R2 降级**) | Good×2 + Excellent (R3) | Excellent (R1, R3) / Good (R2) | Excellent (R1, R3) / Adequate (R2) | **Excellent×3（共识，新）** |
| Presentation | — | Good×3 | Good×3 | Adequate×3 | Adequate×3 |

**三条最重要的读数**：

1. **Verifiability 是最灵敏的指标，且它对"复现包是否同步"高度敏感。** #5 因复现包落后一代被
   R2 从 Excellent 打回 Adequate；#6 补齐后回升；#7 又因两处解不出被 R2 单票压回。
   **#8 它重新升到 R1/R3 双 Excellent，而 R2 仍给 Adequate——原因换了：从"数字解不出"
   变成"匿名快照缺件"**（见 #8 记录）。振幅比任何其它准则都大，且**每一轮都由"读者能不能
   把论文的数字跑出来"驱动**，与文笔无关。→ **Verifiability 是唯一持续有效的杠杆准则。**
2. **Importance & Scope 在 #8 从共识底线升到共识 Excellent**，三家都把它归给"问题本身选得对"
   而不是论文写法。这条是 #8 拿到 ACCEPT 的直接原因（rubric：无 Poor + 至少一个实质性准则
   Excellent → Accept）。**但它也是那条最可疑的位移**——见上方可比性说明。
3. **Insights & Evidence 在 #8 是唯一的共识 Adequate**，且三家独立给出同一理由：
   普查只落在单骨干、唯一复制为负且被自家派发缺陷混淆、处方是重放而非实测。
   **这是唯一还能往上抬的准则，而抬它需要新实验，不是新文字。**

### 2.3 反复出现、始终未清的问题（跨轮收敛名单）

按「几轮独立出现」排序。这些是**结构性**的，不是笔误。

| 问题 | 出现轮次 | 状态 |
|---|---|---|
| **单骨干普查 / 二骨干反向且被自家 C-D 派发缺陷混淆** | #5 #6 **#7（三家）** **#8（三家）** | **未解**，且**连续两轮是三家各自点名的头号沉船点**；#8 三家一致给出同一出路（重派一条修正派发词的臂，或把处方降格为 scope） |
| **复现包与论文不同步** | #5 #6 **#7** **#8** | **每轮都出新形态**：`override=None` 静默跳过 → 缺重判文件 → 代际落后 → **#8 匿名快照缺 5 个提交**。**这是 Verifiability 的根因，且每次都是我自查漏掉的。** |
| 关键量「印在论文里但没脚本」 | #6 #7 **#8** | #8 首次**减项**：材料/协议交叉表已脚本化并发货（`clause_tally.py` + `doc_evidence_layer.json`），未脚本化家族 5 项未增 |
| 主张与 scope 不匹配 | #6 #7 | **#8 已闭合**：三家一致认为 scope 已写在每个受影响数字旁边（R2/R3 只要求标题/摘要也带上） |
| **论文引文缺口（自家 bib 里躺着却从未引用）** | **#8（R1+R2 独立）** | 新条目。#8 补引 4 处，未引用 bib 项 28→25；仍有 25 项未引用（非缺陷，但属 bib 卫生欠账） |

### 2.4 改进路线反思

**已经走过的三条路，效果各不相同：**

- **"补齐披露"路线**（#2→#7 的主线）：把每一个不可复现的点改成显式声明、加上限定词、报两个读法。
  **效果：显著且已完成**。论文的诚实度已到顶——三家评审在 #7 都用 "exemplary" 形容自我审计。
  但这条路**边际收益已见底**：#7 的三票仍然全部 Weak Accept，且三家都明说"不是正确性问题"。
- **"补实验"路线**（2×2 缺格、重判漏洗臂）：**有效**。#4 的 Accept 就是这条路的回报。
  但这条路已经走到**只剩一个格子**——那 ~15 案重判。
- **"改定位"路线**（把基准当贡献、收敛叙事）：**未走**。R1 在 #1 和 #7 两次独立提出同一件事
  （"应该把 81 案基准作为贡献来声称"），我一直没做。**这是唯一一条不需要新实验、且被重复要求的路。**

**当前判断（#8 更新）**：#7 的判断——"论文不再缺诚实，缺的是正向主张"——**#8 被三家自己推翻了**：
他们这次把 Importance & Scope 直接给了共识 Excellent，理由就是论文对问题的定位本身站得住。
所以那条"改定位"的欠账**已经不再欠**。

**#8 之后，唯一还能抬的只剩 Insights & Evidence（共识 Adequate）**，而它的两条出路都是新实验：
（a）重派一条修正派发词的臂（R2 明说"one re-dispatched arm per backbone with the corrected
text"）以解开二骨干混淆；（b）那 ~15 案在 verbatim-evidence guard 下重判。
**两条都被三家标为 fixable，但没有任何一家把判定挂在上面**——这是本轮的 key judgment：
**判定已经拿到 ACCEPT，加做实验的边际收益低于回归风险**（本项目史上每加一批新臂都带出过新缺陷：
漏洗臂、重判覆盖缺口、artifact 代际漂移，三次都发生在新臂批次上）。

**已挂账未决**（证据不足，不阻塞）：
- `agoraplus25` 年份（ACM TOC 路径指向 2026，一手源被网络策略挡下）
- Metamon `0.722/0.480` 第三位小数（无公开一手源）
- **匿名快照 `TestVDB_artifact-EC36` 落后 GitHub 5 个提交**（#8 R2 独立发现，我逐路径复验）

**已挂账未决**（证据不足，不阻塞）：
- `agoraplus25` 年份（ACM TOC 路径指向 2026，一手源被网络策略挡下）
- Metamon `0.722/0.480` 第三位小数（无公开一手源）

---

## 3. 各轮记录

### 3.1 本轮（#9 round-20，2026-09-15 16:55）

**对象**：`TestVDB-v10.tex` + round-19 修复批次；**匿名快照已在开审前同步**。
**产物**：`.paperpilot/review/TestVDB-review-2026-09-15b.md`。
**评价**：**三票 Accept，合并 ACCEPT**。

**本轮最大的结构变化：Verifiability 首次成为共识 Excellent（3/3）。**
它的成因是机械的——上一轮 R2 的 [major] 4.2（匿名快照缺 5 个提交）被**你同步掉了**。
这条准则在本项目里连续四轮都是唯一的杠杆，**每一次的涨跌都由"读者能不能把论文印的东西跑出来"决定**，
与文笔无关。Perspective 也在本轮成为共识（R1 归队）。

**本轮抓到的最硬一条是「可数宣称」：§4.1 写 "Sixteen paired tests appear below"，
实际是 20 个**（我逐条枚举确认，10 个在召回层）。R2 报的，我用列表证伪。
**这是本项目第四次栽在"我写了一个可数的数但没数"上**
（前三次：236≠243、69≠48、§4.4 的 22/8）。**纪律应当升级为：凡写进论文的计数，
先跑一遍把它数出来。**

另有一处 **我上一轮自己引入的缺陷**：§4.5 交叉表只印了 two of the four strata，
R1 与 R3 **独立地**分别反推出 20/60 与 60+3+18=81——**两个人都推错了**（实际 59+3+18+1）。
"给率不给分母"是可复现的公允缺陷，已补全。

**修复**：20 个检验 + Holm 家族理由、交叉表分层与分母、选择性预测线（R1 独立报的**新**缺口，
bib 此前完全没有这条线）、Table 1 对 SATORI 的过头刻画、§5 第一条教训超出设计、§4.6 的读不通句。

### 3.2 上一轮（#8 round-19，2026-09-15 16:05）

**对象**：`TestVDB-v10.tex` + PDF（承接 #7 的修复批次）。
**产物**：`.paperpilot/review/TestVDB-review-2026-09-15.md`（三审 + meta）。
**评价**：**三票 Accept，合并 ACCEPT**。准则：Imp&Scope **Excellent×3**、
Perspective Excellent×2、Verifiability Excellent×2、Insights Adequate×3、Presentation Adequate×3。

**本轮我做的最有价值的一件事不是修，是核实——两条 [major] 一真一伪：**

1. **R1 的 2.4 被我实测证伪，且方向对论文有利。** R1（领域专家）推理：契约否决是机械包含检查，
   而审计发现 58/134 对无依据，所以"80% 误关集中在 A 条款"可能只是**审计结果换了个面孔**；
   若成立，处方应是修材料而非守条款。我算了交叉表：**24 次误关中 20 落在文档依据完备的案子
   （率 0.11），4 落在 weak_evidence，0 落在 18 个依据缺失案（率 0.00）**——条款是在审计判定
   "有依据"的材料上误读的。**普查是协议结果，不是材料结果。** 已写进 §4.5 并发货脚本。
2. **R2 的 4.2 为真，但根因是匿名快照。** 我逐路径探过 `TestVDB_artifact-EC36`：
   `clause_tally.py`、`bootstrap_net_f1.py`、`audit/pair_audit.py`、`pricing/` 工作表、
   `rq2/prompts/` **全部 404**，README 还是旧标题。本地仓与 GitHub 都是对的，
   **快照落后 5 个提交**。这是 Verifiability 未成共识 Excellent 的唯一原因。

**另外两条 [major]（R1 3.3 引文缺口 / R1 2.3 审计代际）已核实为真并修复。**

**教训（与 [[artifact-sync-stale-arms]] 同族，第四次）**：我又一次以为"包已经同步好了"——
本地和 GitHub 确实好了，**但论文里那个 URL 指向的东西没好**。
前三次是开发树 vs 发货包，这次是**发货包 vs 公开快照**。**验证必须验到读者实际会点开的那一层。**

### 3.3 再上一轮（#7 sample10）

**对象**：`TestVDB-v10.tex` + 编译产物 PDF（首次审格式化提交物，不再是 markdown 草稿）。
**产物**：`.paperpilot/review/.in-progress-sample10/`（`meta-review.md` + `FINDINGS_VERIFIED.md` + 三份 `reviewer-*/draft.md`）。

**评价**：三票 Weak Accept / 全 CONDITIONAL，**无共识 Excellent**。
上一轮列的可修项**全被确认已修**；引文抽 18 条无造假；合规全过（0 错 / 0 未定义引用 / 0 overfull /
20 页 / 计页正文 17.31 ≤ 18）。

**本轮新缺陷**（全部已独立复现并修复）：
1. **★ §4.1 称「English renderings of the two judging prompts ship verbatim in the artifact」为假**——
   包内两个模板与全部派发词都是中文，全树无 `*prompt*`；被删附录还自述渲染件「prepared by the authors」，
   即从来只在论文附录里。处置=**真发货**（`rq2/prompts/` 三份），而非改口。
2. **§4.4「22 decisive routed cases … flat judge has 8」复现不出**——按 `convention_pricing.py` 的
   `joint()` 口径实为 **25 / 11**（两个子声称逐字命中锁死口径）；扫十二臂，`22` 在任何口径下都不存在。
3. **§8 头条对比的 discordant 配对四处写反**（`9/0`→`0/9` 等）——R1 曾误判为"上轮已修"，
   以冻结数据裁决 R3 正确。
4. §4.1 承诺 both levels 而三条对比只印召回层；"suppression" 五处承载数值却从未定义；
   §5/§8「closes the most judgments」字面为假；§4.5 catch-all 混淆词表与条款；§7 指代反；
   `\footnotesize` 两处被 form feed 顶掉（PDF 真印出 "ootnotesize"，**而我早先读该文件时见过却漏过**）；
   bib `haldar25` 作者名与 `ddlcheck25` 页末。

**提交**：论文仓 `4809f6d`、复现包仓 `dce0bf5`。

---

## 4. 下一轮（#10）的决策点

**先读 2.3 / 2.4 再决定做什么。** #8 已把候选 A（改定位）与 B（脚本化）部分兑现，
且 #8 的三家把 Importance & Scope 给了共识 Excellent——**写作类路线基本走到头**。

| 候选 | 成本 | 谁要求过 | 是否新实验 | 状态 / 预期 |
|---|---|---|---|---|
| ~~**B'. 未脚本化家族减项**~~ | 低 | #7 R1、#8 三家 | 否 | ✅ **已做两项**（交叉表 + 对比定价），家族 5 → **4** |
| ~~**E. 匿名快照同步**~~ | 极低 | #8 R2 [major] | 否 | ✅ **已做**。#9 Verifiability 升为**共识 Excellent** |
| **F. 描述统计表**（12 臂 × 4 数） | 中 | #8 R2/R3、**#9 三家** | 否 | **仍未做**：需 ~0.24 页，会把余量从 0.20 压没。**须等量删减才可做** |
| **H. 臂/骨干命名表**（×1 行术语表） | 低 | #8 R2/R3、**#9 三家** | 否 | **连续三轮被三家点名**，是当前最廉价的 Presentation 杠杆 |
| **I. 审计第二读者** | 中 | #8 三家、**#9 三家** | 是（小） | 连续两轮三家点名；抬 Insights/Verifiability 的稳健性 |
| **C. ~15 案重判（verbatim-evidence guard）** | **高** | #5 #6 #7 #8 **#9**（R2/R3） | **是** | 唯一能抬 Insights 的动作 |
| **G. 重派一条修正派发词的臂**（解二骨干混淆） | **高** | #8 R2、**#9 R1/R2/R3** | **是** | 同上；R1 2.5 / R3 2.5 / R2 2.4 本轮全部指向它 |

**#9 对 C/G 的判断仍是不做**，理由与 #8 相同，且本轮更明确：三家的 `[major, fixable]`
**全部落在 C/G 上，但没有一家把判定挂在它们上面**。Insights 由 R2 单票抬到 Excellent、
R1/R3 保持 Adequate——**分歧在权重不在事实**，加做实验去消除这个分歧，
收益远小于本项目史上"每加一批新臂必出一次回归"的代价（已发生三次）。

**#10 的优先序**：**H（术语表，等长可做）→ I（审计第二读者，若判官能用）→ F（表，须先删减）**。
三者都不动承重数字。**距离停止条件还差 #10 一轮**（#7:0/3、#8:3/3、#9:3/3，需连续三轮 ≥2）。

**执行纪律**（每一步都要满足）：
1. 先读本文件 2.3/2.4，再动手；
2. 改完必须自检**是否引入新问题**（表述不一致 / 数据不一致）；
3. 时刻守 **FSE 篇幅硬约束**（正文+图 ≤18 页，参考文献 +4 页，**只有 Data Availability 豁免、无附录豁免**）；
4. 涉及新实验（C）先做**小规模探针**验证是否值得，再评估「篇幅 / 成本与风险 / 潜在收获」。

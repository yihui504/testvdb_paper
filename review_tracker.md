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

**语义提醒**：第 1 轮的「合并 ACCEPT」与 reviewer 的「Weak Accept」不矛盾——rubric 的合并规则允许多票
Weak Accept 在「无共识 Poor / 无共识 Weak」时上浮。看**趋势**时以 Accept 数列为主，合并总评作辅。

---

## 2. 最近 4 轮趋势对比

前提核对：第 4–7 轮**评审对象同源可比**（同一篇 FSE 论文的连续版本，criteria 同为
Importance / Insights / Presentation + Perspective / Verifiability 五准则），只差份量与修复批次。

### 2.1 评委票型

| 轮次 | R1 | R2 | R3 | Accept 数 | 相对上轮 |
|---|---|---|---|---|---|
| #4 sample7 | **Accept** | Weak Accept | Weak Accept | 1/3 | 首次出现 Accept |
| #5 sample8 | Weak Accept | Weak Accept | Weak Accept | 0/3 | **回落** |
| #6 sample9 | Weak Accept | Weak Accept | Weak Accept | 0/3 | 持平 |
| #7 sample10 | Weak Accept | Weak Accept | Weak Accept | 0/3 | 持平 |

**趋势读数**：**#4 是峰值，此后三轮在 0/3 上持平**，没有单调上升。
#4 的 Accept 是有条件的（R1 的 CONDITIONAL 判词），条件是「重判两条漏洗臂」，**该条件在 #5–#7 均已兑现**，
但票型没有回来——说明 **R1 当时的 Accept 是对"承诺兑现"的定价，不是对论文本身的定价**；
承诺兑现后，评审的注意力转移到了更下一层的问题（见 2.3）。

### 2.2 准则层趋势（只有被明确写出时才记）

| 准则 | #4 | #5 | #6 | #7 |
|---|---|---|---|---|
| Perspective | Excellent (R1) | — | Excellent (R1) | Excellent (**R2**) |
| Verifiability | Excellent (R1) | Adequate (**R2 降级**) | **Good**×2 + Excellent (R3) | Excellent (R1, R3) / **Good (R2)** |
| Presentation | — | — | Good×3 | Good×3 |

**两条最重要的读数**：

1. **Verifiability 是最灵敏的指标，且它对"复现包是否同步"高度敏感。**
   #5 因复现包落后一代被 R2 从 Excellent 打回 Adequate；#6 补齐后回到 Good/Excellent；
   #7 又因两处解不出（`22/8`、both-levels）被 R2 单票压到 Good——**首次掉出共识 Excellent**。
   这一项的振幅比任何其它准则都大，且**每次都由"数字能不能从 artifact 复现"驱动**，
   与文笔无关。→ 结论：**Verifiability 是当前唯一的杠杆准则**，其它四项已在 Good 上饱和。
2. **Perspective 从 R1 独占变成 R2 给出，说明它不是 R1 的个人偏好**，但始终没有形成共识
   Excellent（R1 在 #6/#7 反而只给 Good）。

### 2.3 反复出现、始终未清的问题（跨轮收敛名单）

按「几轮独立出现」排序。这些是**结构性**的，不是笔误。

| 问题 | 出现轮次 | 状态 |
|---|---|---|
| **普查处方在 forced 读法下为零 / 二骨干不复制**（census 的处方不是实测的） | #5 #6 **#7（三家独立写出）** | **未解**，且是三家各自点名的头号沉船点 |
| 复现包与论文代际不同步（数字复现不出） | #5 #6 **#7** | 每次修，每次新出——**这是 Verifiability 的根因** |
| 关键量「印在论文里但没脚本」 | #6 #7 | #7 改为显式声明「printed but not scripted」，仍未脚本化 |
| 主张与 scope 不匹配（本文以单骨干、约定定价测量，却按通用处方叙述） | #6 #7 | #7 已加 scope 限定，但标题/摘要仍未重述 |

### 2.4 改进路线反思

**已经走过的三条路，效果各不相同：**

- **"补齐披露"路线**（#2→#7 的主线）：把每一个不可复现的点改成显式声明、加上限定词、报两个读法。
  **效果：显著且已完成**。论文的诚实度已到顶——三家评审在 #7 都用 "exemplary" 形容自我审计。
  但这条路**边际收益已见底**：#7 的三票仍然全部 Weak Accept，且三家都明说"不是正确性问题"。
- **"补实验"路线**（2×2 缺格、重判漏洗臂）：**有效**。#4 的 Accept 就是这条路的回报。
  但这条路已经走到**只剩一个格子**——那 ~15 案重判。
- **"改定位"路线**（把基准当贡献、收敛叙事）：**未走**。R1 在 #1 和 #7 两次独立提出同一件事
  （"应该把 81 案基准作为贡献来声称"），我一直没做。**这是唯一一条不需要新实验、且被重复要求的路。**

**当前判断**：#7 的三家评语高度一致地指向同一件事——**论文不再缺诚实，缺的是"我们测到了什么"的
正向主张**。三家各自给出一个"能推到 Accept"的条件，全部落在这两类上：
（a）那 ~15 案重判（新实验）；（b）把已有的联合定价脚本化 / 把基准正面声称（写作）。

**已挂账未决**（证据不足，不阻塞）：
- `agoraplus25` 年份（ACM TOC 路径指向 2026，一手源被网络策略挡下）
- Metamon `0.722/0.480` 第三位小数（无公开一手源）

---

## 3. 本轮（#7 sample10）记录

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

## 4. 下一轮（#8）的决策点

**先读 2.3 / 2.4 再决定做什么。** 本轮不打算再做"补齐披露"类修补——2.4 已论证其边际收益见底，
且 #7 的三家都在说"问题不在诚实度"。候选动作按 [成本 × 是否被重复要求 × 是否新实验] 排列：

| 候选 | 成本 | 谁要求过 | 是否新实验 | 预期 |
|---|---|---|---|---|
| **A. 把基准正面对待**（标题/摘要/贡献清单） | 极低（纯写作） | #1 R1、#7 R1+R3 | 否 | 直接冲 Significance/Importance 一项 |
| **B. 联合定价脚本化**（worksheet 接进发货脚本） | 低（~30 行） | #7 R1 明说"仅此即可到 unconditional Accept" | 否 | 直接冲 Verifiability |
| **C. ~15 案重判（verbatim-evidence guard）** | 高（新实验） | #5 #6 #7 三家各自点名 | **是** | 唯一能把处方从"重放"变"实测"的动作 |
| D. 双骨干 scope 重述（标题/摘要/§8） | 低 | #7 R3 作为 C 的替代给出 | 否 | 与 A 同向，可合并 |

**执行纪律**（每一步都要满足）：
1. 先读本文件 2.3/2.4，再动手；
2. 改完必须自检**是否引入新问题**（表述不一致 / 数据不一致）；
3. 时刻守 **FSE 篇幅硬约束**（正文+图 ≤18 页，参考文献 +4 页，**只有 Data Availability 豁免、无附录豁免**）；
4. 涉及新实验（C）先做**小规模探针**验证是否值得，再评估「篇幅 / 成本与风险 / 潜在收获」。

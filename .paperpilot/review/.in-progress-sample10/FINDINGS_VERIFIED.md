# sample10 — 逐条核实台账

对象：`TestVDB-v10.tex`（LaTeX 提交物）。核实者：主会话，独立于评审员。
纪律：每条都必须能从冻结对象/复现包复现后才列为 CONFIRMED。

---

## R3（General Reviewer）— 已收到草稿，逐条已核

### R3-W2 §8 配对顺序与 §4.4 相反 — **CONFIRMED（真错）**

`grep` 结果：

| 检验 | §4.4 印 | §8 印 |
|---|---|---|
| 捆绑对比 主骨干 召回层 | `0/9` (L626) | `9/0` (L965) |
| 捆绑对比 主骨干 确认集 | `0/17` (L626) | `17/0` (L966) |
| 捆绑对比 二骨干 召回层 | `0/14` (L627) | `14/0` (L966) |
| 捆绑对比 二骨干 确认集 | `0/19` (L628) | `19/0` (L966) |

§4.1 的约定（L510-511）：「Discordant pairs are written *a/b*, where *a* is the arm whose count is
printed first in the comparison being reported.」§8 印的是费率在前（`0.588 to 0.765`），所以
首印臂 = flat judge = a，应为 `0/9`。§8 四处系统性反了，p 值全对 → **纯标签错，非算术错**。
修法：§8 四处对调。

### R3-W3 "suppression" 从未定义 — **CONFIRMED（定义缺口）**

首用 L440（§4.1），此后 L615/L617/L663/L763 共五处承载数值，全文无一处给出定义。
实义 = 30 个真负例中该臂**未**确认的比例（脚本 `recompute_paper_numbers.py` 印
`supp {tn}/{N_F}`）。

同句反向措辞（L439-440）算术复核：no-source 拦 14/30→12/30（0.467→0.400）、
no-aggregation 拦 28/30→27/30（0.933→0.900）；对应**已确认** FP 16→18、2→3。
所以「false-positive counts rise」与「suppression 下降」同向相容，但两词相距三词、
字面反指。修法：首次使用时加一句定义 + 改写该分句。

### R3-W4 复现包是否真发英文提示词 — **CONFIRMED（比 R3 报的更严重）**

论文 §4.1 L500-501：「All dispatch texts, and English renderings of the two judging prompts,
ship verbatim in the artifact.」

实测：

- `rq2/verdicts/` 下两个模板 `dispatch_template.md`（1,343 B）、
  `dispatch_fullstage_template.md`（3,116 B）**均为中文**。
- 全树 `find -iname "*prompt*"` = 0 命中；`grep -i english` 只命中 `pipeline/README.md`
  的语言切换行。
- 逐臂实例化派发词（`run_*/batch*_dispatch.txt`）亦为中文。

**关键证据**——被删附录（`git show bf3e5c6:TestVDB-v10.tex` 附录段）原文自述：

> Both prompts below are English renderings **prepared by the authors** of the dispatch files
> actually used in the re-adjudication; the verbatim Chinese files ship in the artifact and are
> authoritative.

即：英文渲染件**从来只存在于论文附录**，复现包只发中文原件。附录因页数限制被删后，
这句承诺变成了**对复现包内容的错误陈述**，且"the two judging prompts"在正文已无先行词。

这不只是措辞——它是 RQ2 整个装置（判官提示词）的可核验性。修法二选一：
(a) 把三份英文渲染件（全阶段协议 / flat 判官 / 无视角标签版聚合条款）**真的发进复现包**
（`rq2/prompts/`），§4.1 点名路径；(b) 改句子只说中文派发词发货。**（a）明显更好**——
英文渲染件已存在（旧稿 `TestVDB.tex` L474-500 附录），发货零成本，且把 Verifiability
从负债转回资产。

### R3-Q1-3 判官纪律条款已从正文消失 — **CONFIRMED**

`grep -i "no network|network access|same per-case materials|version-pinned source clone|judged independently|own pack"` → **0 命中**。

被删附录原有一句：「Each judge receives the same per-case materials---the frozen evidence pack
and the case's version-pinned source clone---and the discipline clauses (own pack and clone only,
no network access, cases judged independently) are identical.」

对一篇主张"对比在同一池上"的论文，"判官如何被保持可比"是设计事实。修法：§3.5 或 §4.1
补一句。

### R3-W5 §5/§8 "the clause that closes the most judgments" — **CONFIRMED（字面不成立）**

Census 表（`tab:census`，L730-736）：

- `B = Confirmed` → 关 **61** 条
- `A = Refuted`（contract refutation）→ 关 **50** 条

L821（§5）：「requires nothing for the one that closes the most judgments」；
L975（§8）：「the clause that closes the most judgments ... closes 50 of 243」。
字面为假（61 > 50）。§4.5 自己的措辞才是准的（L743-744）：「**the middle of the three clauses
that assign False-Positive** (19 judgments, against cognition's 16 and contract refutation's 50)」。
修法：两处改成 refuting/assign-False-Positive 限定语。数字一个不动。

### R3-W7a §7 "below" 方向错 — **CONFIRMED**

L954：「the twelve frozen configurations **below** are for」。十二配置在 §4.1，位于 §7 之前。
改 "above" 或点名 §4.1。

### R3-W7b C 格 15/2/2 分类未入"未脚本"清单 — **CONFIRMED**

`grep clause_tally.py`：脚本印 C 行准确率，**不印**该证据分类（15 注释/文档字符串、2 服务端
校验规则、2 代码结构）。§4.1 的 printed-but-not-scripted 清单（L523-524）只列了
joint prices / catch-all composition / expectation-framing check，未含此项。
它是普查最自曝其短的数，修法：要么脚本化，要么列入清单。

### R3-W6 句长/密度 — 接受为**建议级**（未逐条复核）

R3 自报口径（自有 splitter）：正文 340 句 ≥5 词、中位 27 词、17 句 ≥70 词；最长句 §7 Ma et al.
90 词。**这是 R3 自己的测量，非冻结数据**，按建议处理。

### R3-W1 普查处方在 forced 下为零 / 二骨干不复制 — **成立但非新发现，且非文字可修**

论文自己在摘要、§4.5、§5、§6、§8 全部披露。出路是跑那 ~15 案的重判
（§4.5 自陈 frozen data 算不出）。**这是唯一能把它从"重放"变成"实测处方"的动作。**

---

## R1（Domain Expert）— 草稿未到
## R2（Area Specialist）— 草稿未到

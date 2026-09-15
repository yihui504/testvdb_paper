# sample10 三角评审 — 综合

**对象**：`TestVDB-v10.tex` + 编译产物 `TestVDB-v10.pdf`（20 页）。**首轮对格式化提交物本身的评审。**
**日期**：2026-09-15　**交付**：本文件 + `FINDINGS_VERIFIED.md`（逐条核实台账）

---

## 判定：三票 Weak Accept / CONDITIONAL

| 准则 | R1 (Domain) | R2 (Area) | R3 (General) | 共识 |
|---|---|---|---|---|
| Importance & Scope | Good | Good | Good | Good |
| Insights & Evidence | Good | Good | Good | Good |
| Perspective | Good | **Excellent** | Good | 无共识 |
| Verifiability | **Excellent** | Good | **Excellent** | 无共识 |
| Presentation | Good | Good | Good | Good |

**与 sample9 同形**：每项准则都离开 Adequate，但**无一项共识 Excellent**。按 rubric 仍不够 ACCEPT。

**Verifiability 首次出现分歧。** R2 把它从 Excellent 降回 Good，理由是本轮新查出的两处
不可复现数（下方 A4、A5）。R1/R3 给 Excellent，两人都把五个脚本就地跑通、逐条对上。

**三审一致确认的正面**：上一轮我列的**每一条可修问题都已修好**（identification 15/2/2 三家
独立核过、§8 层次配对、Holm m=10 非循环、26/20 已删、臂序）；引文抽样 18 条**无造假**；
合规全过（正文 ≈17.4 页 ≤18、参考 ≈2.4 页 ≤4、双盲、Data Availability 位置对）；
R2 独立重建了 paper 自称"未脚本"的两项，数值精确命中。

---

## 本轮新增缺陷（全部经我独立复现）

### A 类 — 提交物可见/可核性硬伤

**A1. §8 把头条对比的 discordant 配对四处写反。`[R3 报，R1 误判为已修]`**
§4.1 定义 "Discordant pairs are written *a/b*, where *a* is the arm whose count is printed first"。
§4.4 印 `0/9`、`0/17`、`0/14`、`0/19`（L626-628）；§8 对**同一批检验**印 `9/0`、`17/0`、`14/0`、`19/0`
（L965-966）。p 值全对 → 纯标签错。
⚠️ **R1 把此项列为"上轮问题已修"，是误判**：R1 核的是**层次配对**（上轮那条，确已修），
没核**配对顺序**（本轮这条）。两票冲突，以冻结数据为准 → R3 对。

**A2. `\footnotesize` 被 form feed 吃掉，PDF 里印着字面串 "ootnotesize"。`[R1+R2 独立命中]`**
`.tex` 的 byte 11267（L166）、33598（L466）各是一个 `0x0c` 后接 `ootnotesize`——全文仅有的两个
控制字符。后果：表 1（p.4）表注下、表 2（p.9）表体内**排版出 "ootnotesize" 一词**，且两表按正文字号
排。**编译 0 错、20 页，日志里看不见**。根因即本项目已记录过的那类转义坑（`\f` → 0x0c）。

**A3. §4.1 关于"英文提示词随包发货"的陈述为假，且比评审员报的更严重。`[三审全中]`**
现文（L500-501）："All dispatch texts, and English renderings of the two judging prompts, ship
verbatim in the artifact."
实测：`rq2/verdicts/` 两个模板（`dispatch_template.md` 1,343 B、`dispatch_fullstage_template.md`
3,116 B）**均为中文**；全树 `find -iname "*prompt*"` 零命中；`grep -i english` 只命中
`pipeline/README.md` 的语言切换行。
**关键**：被删附录（`git show bf3e5c6`）自述「Both prompts below are English renderings
**prepared by the authors** … the verbatim Chinese files ship in the artifact and are
authoritative」——即英文渲染件**从来只存在于论文附录**。附录因页数被删后，这句成了对复现包内容的
**错误陈述**，且 "the two judging prompts" 在正文已无先行词。
**处置选 (a) 实修**：把三份英文渲染件（全阶段协议 / flat 判官 / 无视角标签版聚合条款）真的发进
`rq2/prompts/`，§4.1 点名路径。渲染件本就在旧稿 `TestVDB.tex` L474-500，发货零成本。

### B 类 — 数字不可复现

**A4. §4.4 路由总数 22 / 8 复现不出；正确值是 25 / 11。`[R2 报，我独立复现并锁定口径]`**
现文：「The control has **22** decisive routed cases, of which **9 were never ruled, one of them a
true bug**; the flat judge has **8**, of which **2 were never ruled, none a true bug**.」

我用"≥1/3 run 路由 且 约定多数确认"这一口径：

| 臂 | 路由数 | 未裁 | 未裁中真 bug |
|---|---|---|---|
| flat+aggregation（control） | **25** | **9** | **1** |
| flat judge | **11** | **2** | **0** |

**两个子声称（9/1、2/0）逐字命中**——所以口径就是它，唯独两个**总数**印错。
附加佐证：包内 `routed_unique.json` 的 full=21 / flat=11 也只与这个口径吻合（该文件无 flatagg 项）；
R2 独立算出同样的 25/11。**扫全部十二臂：`22` 在任何口径下都不存在**（`8` 只出现在 flat-Qwen，
是另一条骨干）。
"decisive" 一词**全文无定义**，且 `grep -rn decisive rq2/` 零命中——读者无法自行重建。

**A5. §4.1 承诺"both are reported for every contrast"，四条对比不符。`[R2 报，我复现]`**
脚本在确认集层确实印了四视角对比：`flat + aggregation vs full stage : discordant 9/6, net +3,
p=0.6072`。论文 §4.4 只印了召回层的 `4/4, p=1.0`；`.tex` 里 `grep 9/6|0.6072` 零命中。
两条辅助读数同理（确认集层 6/4 p=0.7539 与 2/5 p=0.4531，均只在脚本里）。
⚠️ **订正 R2 的数值**：R2 写"both confirmed sets are 51"，实为 **full stage 48 vs flat+aggregation 51**
（我已直接算出；net +3 自洽）。**"缺失"这一发现成立，R2 给的数有小误。**

### C 类 — 措辞/限定语

**A6. "suppression" 全文未定义，§4.1 那句反向措辞。`[R3]`**
首用 L440，此后 L615/617/663/763 共五处承载数值，无一处定义。实义 = 30 个真负例中该臂**未**确认的
比例。算术复核：no-source 拦 14/30→12/30、no-aggregation 拦 28/30→27/30，对应**已确认** FP 16→18、2→3
——「false-positive counts rise」与「suppression 下降」同向相容，但两词相距三词、字面反指。

**A7. §5/§8 "closes the most judgments" 字面为假。`[R3 报公式，R2 报缺限定语——同一句]`**
Census 表：`B = Confirmed` 关 **61** 条 > contract refutation 的 **50**。L821（§5）、L975（§8）两处的
无限定说法为假。§4.5 自己的措辞才是准的（L743-744）："the middle of the three clauses that assign
False-Positive"。R2 另指出 §8 是**唯一**一处普查结论不带 scope 的地方（摘要/§1/§4.5/§5/§6 都带）。

**A8. §4.5 catch-all "the rule does define" 混淆词表与条款。`[R2 报，我复现]`**
catch-all 69 条的 D 值实测：`NO_SIGNAL` **32**、`by_design_in_source` 11、`validation_present` 10、
`validation_absent` 9、`not_found` 7 → 源词表恰 **37**（对上论文的 37/54%），认知词表 **32 且全是
NO_SIGNAL**。"the rule does define" 对**词表**成立（视角定义了 NO_SIGNAL），对**条款**不成立
（聚合条款对它同样没有子句）。实质内容（17/32 = 53.1% vs 基准 63.0%）不受影响。

**A9. §1 的识别声明超出 §4.5 实际所做。`[R2 报，我复现]`**
§1 第 3 条称 §4.5 "identifies the two refuting clauses by the evidence their cells carry"。§4.5 对 C
逐格读、对 D 用词表劈分，**对 A 两者都没做**。实测三视角词表**各自 243 条完全纯净**：
A = NEUTRAL 172 / REFUTED 50 / CONFIRMED 21；B = NEUTRAL 146 / CONFIRMED 80 / REFUTED 17；
C = CONFIRMED 72 / NEUTRAL 71 / WEAK_REFUTED 59 / REFUTED 41。补一句即从弱证据变强证据。

**A10. §7 "below" 指反了；C 格 15/2/2 分类不在"未脚本"清单。`[R3]`**
L954 "the twelve frozen configurations **below**"——配置在 §4.1，位于 §7 之前。
`clause_tally.py` 印 C 行准确率但**不印**该证据分类，§4.1 的清单（L523-524）未含此项。

### D 类 — 参考文献

**A11. `haldar25` 作者名错。`[R1 报，我查一手源确认]`**
现为 `Haldar, Reshma and others`；实为 **Rajarshi Haldar and Julia Hockenmaier**
（Findings of EMNLP 2025, 10.18653/v1/2025.findings-emnlp.1361）。名错 + 第二作者被 "and others" 吞掉。

**A12. `ddlcheck25` 页末错。`[R1 报，我查一手源确认]`**
现为 2281--2293；PVLDB 18(7) 实为 **2281–2294**。作者串完全吻合。

**A13. `agoraplus25` 年份 — 未决，不改。`[R1 报，我判证据冲突]`**
现为 2026。R1 称应为 2025（据作者页文件名 `rest-oracle-tosem2025`）；但 ACM 自己的 TOC 路径为
`/tosem/2026/35/1`，且 TOSEM 卷年 1:1 对应（Vol 35 = 2026），配套 RCR 报告为 35(7) July 2026。
一手页（Ernst 主页 / ACM DL）均被网络策略挡下。**证据不足以翻，保留 2026 并挂账。**

**A14. Metamon 第三位小数 — 未证。`[R1 未能证实]`**
论文印 "precision 0.722 at recall 0.480"；R1 能触达的公开源只有 0.72/0.48。可能引的是结果表而摘要取整。
**不动**，挂账待人工确认引的是表。

**A15. 判官纪律条款已从正文消失。`[R3]`**
`grep -i "no network|network access|same per-case materials|version-pinned source clone|judged
independently|own pack"` → **0 命中**。被删附录原有："Each judge receives the same per-case
materials … under identical discipline clauses (own pack and clone only, no network access, cases
judged independently)." 对一篇主张"对比在同一池上"的论文，这是设计事实而非细节。

---

## 非缺陷但需记的决定

- **R2-W6 的 A 视角**：我确认 A/B/C 三视角词表各自纯净（见 A9）。这**加强**而非削弱论文的
  "identified by content" 主张——补印即可。
- **R1 的 Accept 条件**：把 joint pricing 工作表接进发货脚本，R1 明言这会让它升到
  **unconditional Accept**。这是本轮**最便宜的高杠杆动作**（~30 行）。
- **三审共同的"沉船点"**（R1-Q6 / R2-Q6 / R3-Q6 各自独立）：普查处方在 forced 读法下为零、
  二骨干不复制。三家都说论文**自己已充分披露**，非致命；出路只有那 ~15 案重判（新实验）。

---

## 处置顺序（本轮）

1. A2 修字节 + 重编译（唯一提交物可见硬伤）
2. A1 / A4 / A6 / A7 / A8 / A9 / A10 / A15 正文措辞与数字
3. A3 发货三份英文渲染件到 `rq2/prompts/` + §4.1 点名
4. A11 / A12 文献订正；A13 / A14 挂账
5. 重编译、重跑保真核验、重测页数合规

**不采纳**：R3-W6（句长）与 R1-W6（摘要压缩）判为建议级；A13/A14 证据不足不动。

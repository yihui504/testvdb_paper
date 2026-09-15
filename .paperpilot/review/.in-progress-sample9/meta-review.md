# sample9 元评审

对象：`docs/paper-sample-lqm-path.md`（样本 v9，**首份完整稿**——§2/§3/§7/§8 本轮首次写出）
三份评审：`.in-progress-sample9/reviewer-{1,2,3}/draft.md`

---

## 一、准则与判定

| 准则 | R1 | R2 | R3 | 元评审 |
|---|---|---|---|---|
| Importance & Scope | Good | Good | Good | **Good** |
| Insights & Evidence | Good | Good | Good | **Good** |
| Perspective | **Excellent** | Good | Good | Good |
| Verifiability | Good | Good | **Excellent** | Good |
| Presentation | Good | Good | Good | Good |
| 推荐 | Weak Accept | Weak Accept | Weak Accept | **Weak Accept** |
| 判定词 | CONDITIONAL | CONDITIONAL | CONDITIONAL | **CONDITIONAL** |

**与 round-18 相比的位移**：round-18 是「五项 Adequate + Verifiability 共识 Excellent」。
本轮 **每一条准则都离开了 Adequate**，且 R1、R3 各给出一条 Excellent——但**没有共识 Excellent**，
而 rubric 要求实质准则（Sig/Nov/Sound 或经验论文的 Insights）达成共识 Excellent 才够 ACCEPT。
所以判定没动，位置动了：**从"五项合格"变成"五项良好 + 两条各被一人认为优秀"**。

## 二、三人独立收敛的发现（本轮修复的主体）

**C1 · §4.2 的「26 案（20 确认）在实验覆盖版本上」不可复现——三人全中。**
R1 与 R2 各自 join 发货台账与 `rq1-fullrun` 的十二个版本目录，都得 **49/30**（按版本前缀归一 50/31）；
论文印 26/20；R2 另指出「15 versions run」与包里 12 个版本目录冲突。作者自己的笔记已挂账，
但正文仍以断言形式印出。**这是本轮唯一被判 [major] 三次的条目。**

**C2 · §4.5 的 identification 段是错的——R1、R2 各自独立算出，与我的重算逐格一致。**
我上轮新写的那句「19 格中 18 格引源码注释或文档字符串，第 19 格（milvus_026）引名称校验规则」
在两点上错：
- `milvus_026` 贡献**两格**（run1、run2），不是一格
- `milvus_011` run3、`milvus_012` run3 依据的是**代码结构**，不是注释/文档字符串

正确分布是 **15 格引注释或文档字符串 / 2 格引校验规则（milvus_026 的两个 run）/ 2 格引代码结构**。
更重的是 R2 挖出的第三条：`milvus_012` 的 run2 记 **WEAK_REFUTED**，理由原文写着
「兜底链结构示设计但**无注释/quote 明文（红线3 不构成 REFUTED）**」，而 run3 却按**同一份结构**
判了 REFUTED。`milvus_011` 同形（run2「无注释静默行为」→ run3 REFUTED）。

→ 所以「C 是唯一要求逐字意图证据的条款」这一命题，在它自己的 19 格里有 4 格没守住，
且 2 案存在**同案不同 run 对同一证据给出不同强度判定**。原句「none infers intent from behavior
alone」被直接反证。这不是描述问题——它接上 §4.5 自己的规则合规分析（那里量的是聚合规则，
从没量过 C 条款的证据要求），而**恰恰是论文自己的命题的又一个实例**。

**C3 · §8 的层次错配——三人全中。** §8 首段把召回层费率配了确认集层的配对与 p。
实为 `0.588→0.765` 配 `9/0, p=0.0039`、`0.529→0.804` 配 `14/0, p=0.0001`。
这正是我本轮在 §4.4 修好的同类错误，**没有传播到 §8**——R3 的原话是「修复没传播」。

**C4 · §4.1 的 Holm 家族是循环定义——R1、R2 全中。**
我把家族定义成「那四个显著值本身」，然后说它们通过了对该家族的 Holm 校正——同义反复。
另：我本轮在 §4.4 新增了 `p=0.0225`，召回层显著值因此变成 5 个，而家族计数仍是旧的。
实测：正文印出 **13 个配对检验（召回层 8 个）**；而 §4.1 承诺「每个对比两个层次都报」，
但**捆绑对比（flat→flatagg）的召回层配对与 p 值根本没印**——这正是家族数不出来的原因。

**C5 · 复现包的匿名化声明不实——R1、R2 全中。**
README 称 "The archive is anonymized for double-blind review"。
实测 `grep -rl 11428 rq2/` = **254 / 824** 个文件，形态为 241 个派发词 `.txt` + 13 个 `.jsonl`，
含真实账号名与五处机器路径（`testvdb_paper\.paperpilot\phase…` 3,371 次、`.sourcedeps\milvus…` 1,144、
`mftui\TestVDB\.sourcedeps\…` 300、`tvdb_sessions\intelligence\…` 102、`testvdb4exp\.sourcedeps\…` 60）。
R1 另查到树里存在 `.scrub.py`，**从未被应用到 `rq2/verdicts`**——即"洗过别处、漏了这一处"。
**双盲风险，投稿前必修。**

**C6 · §4.1 的重判方向按 convention 口径是 15/0/4，不是 18/1——R1 中，我已复现。**
我按三级序（Confirmed > Human-Review > False-Positive）算的 18/1；convention 是二值口径，
Confirmed 与 Human-Review 都算确认，所以 4 个 HR↔Confirmed 的移动是**无操作**。
正确表述：**15 个朝确认、4 个无操作、0 个反向**。
（方向仍全对我们不利——去掉泄漏后两条控制臂只会更保守。）

**C7 · core 的三条前代归档未发货，§4.1「两代都发货」对 13 条重判臂中的 3 条不成立——R1 中。**
`rerun_v2/run{1,2,3}/_pre_cogstrip_merge/` 在开发树里，复现包的 `rq2/verdicts/run{1,2,3}/` 没有。
我的覆盖审计脚本 `107_rejudge_coverage_audit.py` **只扫了 `rerun_v3`，整个 core 都漏了**——
审计脚本自身有盲区，须一并修。

**C8 · README 的 RQ3 表印双计数——R2 中，我已见。**
README 表列 `full-coverage-v3 | 23,258 | 22,540`，而 §4.6 明确说主日志是 205 个模板日志的逐字回声、
单份应为 `11,629 / 1,127`。README 与论文互相矛盾。

## 三、单人发现（均需处置）

**S1 · 多数票平局规则未定义（R3，我已复现）。** 81 案中 **3 案三次运行给出三个不同判定**
（milvus_021 / milvus_038 / qdrant_027）。论文写的 "a case confirmed on a majority" 实为
「至少两次把该案算作确认（convention 下 HR 计入）」→ 39/51；严格多数（两次须记同一判定）→ **37/51**。

**S2 · 我本轮新写的三处过强（R2）。**
- §3.1 "holding everything else fixed" —— 与 §4.1（臂中途加、三个对比多于一变量）、§6 冲突
- §2 "**none** takes its expectation from untagged, system-level API prose" —— 对 RESTInfer/ICON 过强；
  tex 原文更准（parameter/method granularity；behavioural residual sits above that granularity）。
  ⚠️ 这正是「凡全称与最高级先跑能证伪它的命令」那条教训的又一次复发。
- §4.4 的九臂描述 "the six primary-backbone configurations other than the core" —— 主骨干非 core 实为
  **7** 个（含 source-only）；该九臂不含两个 source-only，须点名。

**S3 · 其余小项**：contract core 的重判文件未被发货脚本应用（数值无影响，R2）；
§4.2「其中一个是 crash-or-panic」无发货出处（R1、R2）；台账两处措辞过强
（"awaiting a maintainer" / "withdrawn"，R1）。

**未能核实、留作已知边界**：§4.3 的 expectation-framing 检查所依据的"19 条命中"（R1：可见部分
一致但不可复现）；R1 观察到的「1,127 完成块 vs 1,279 启动块」（论文未印该数，我实测论文印的
两个数都对，不追）。

## 四、正面结论（本轮真实进展）

- **round-18 的头号沉船点已消**：上轮「复现包落后论文一代」的失效模式**不复现**。
  R1 逐文件比对：发货包与冻结研究树在 **452 个文件上零差异**。
- **Verifiability 上移**（R1/R2 Good、R3 Excellent）：R3 把五个脚本全部就地跑通、逐条对上论文；
  R2 另核 §4.4 每个费率/配对/p 都满足「层次差 = 配对差」与 a=先印臂约定。
- **四节新章被接受**：三人一致认为 §2/§3/§7/§8 关闭了结构性缺口（此前八轮反复提的那条）。
  R1 逐条核了 §7 对既往工作的陈述（Metamon 的 0.722/0.480 精确、TRACE/LogicHunter/Molinelli/缺陷
  分布研究均准确）。
- **R3 的判断**：「emphasis 终于移到主张本身上了」——此前八轮它反复说"作者诚实但重心没跟着移动"。

## 五、修复清单（按影响排序）

| # | 条目 | 谁中 | 性质 |
|---|---|---|---|
| 1 | §4.5 identification 段重写 | R1+R2 | 我上轮引入，且反证了该段自己的论点 |
| 2 | §4.2 的 26/20 —— 定代际或撤断言 | R1+R2+R3 | 三人，历史挂账 |
| 3 | §8 层次配对 | 三人 | 我本轮引入 |
| 4 | §4.1 Holm 家族 + 补印捆绑对比的召回层配对 | R1+R2 | 我上轮引入 |
| 5 | §4.1 重判方向改 15/0/4 | R1 | 我上轮引入 |
| 6 | 复现包：匿名化洗白 + core 前代归档 + README RQ3 表 | R1+R2 | **需用户拍板**（动已发货证据） |
| 7 | §3.1 / §2 / §4.4 九臂 三处过强 | R2 | 我本轮引入 |
| 8 | 多数票平局规则写进 §4.1 | R3 | 定义缺口 |
| 9 | §4.2 crash 计数、台账措辞 | R1 | 小项 |
| 10 | `107_rejudge_coverage_audit.py` 扩到 rerun_v2 | R1 | 工具盲区 |

## 六、流程教训（第四轮同形）

**三位评审的判断全部可靠，自报的计数仍有出入**：R1 的「1,279 启动块」我复现不出（实测 1,694 条
`运行测试 n/m` 行）；R2 的「15 printed paired tests」我实测 13 个（召回层 8 个）。
但**两处出入都不影响他们的结论**，且两人指向的实体都是真的。
另：本轮我自己的三处新错（§8 层次、identification 分布、重判方向）**全都是"分类/计数"类**，
与前三轮评审的自报错同类——**写数字前先跑能证伪它的命令**这条仍然是我最需要执行的。

# sample9 已核实发现（R2/R3 落盘，R1 未回）

本文件只收**我亲自重算过**的条目。R 编号 = 该发现的报告人。

## A. 论文正文

### A1. §4.5 identification 段（我上轮新写）——**错，须重写**（R2 W2）
逐案读 19 个 C=Refuted 关闭格的 rationale 后，实测分布不是「18 引注释 + 1 引校验规则」：

- `milvus_026` 贡献**两格**（run1、run2），依据是「校验代码与错误消息」，非注释/文档字符串
- `milvus_011` run1/run2 = **WEAK_REFUTED**（run2 理由原文：「无注释静默行为」）；run3 升 REFUTED，
  依据是「空表达式映射 trueLiteral」= 代码结构
- `milvus_012` run1/run2 = **WEAK_REFUTED**（run2 理由原文：「兜底链结构示设计但无注释/quote 明文
  （红线3 不构成 REFUTED）」）；run3 却按**同一结构**判 REFUTED

→ 正确分布：**15 格引注释/文档字符串，4 格引代码结构或校验规则**。
→ 且这 2 案存在**同案不同 run 对同一份证据给出不同强度判定**（WEAK_REFUTED vs REFUTED）。
→ 这不是描述问题：它触及「C 是唯一要求逐字意图证据的条款」这一命题本身，也接上 §4.5 自己的
  规则合规分析（那里量的是聚合规则，没量 C 的证据要求）。
→ 我原来的关键词匹配（源码/注释/文档字符串）把「提到源码」当成了「引注释」——是本轮教训。

### A2. §8 层次混用（R2 W4 + R3 W1，**两人独立**）
§8 首段把**召回层费率**配了**确认集层**的配对与 p：
- 应为 0.588→0.765 配 `9/0, p=0.0039`（现印 17/0 p<0.0001 = 确认集层）；
  0.529→0.804 配 `14/0, p=0.0001`（现印 19/0 p<0.0001）。
- 且 §8 写 "p<0.0001" 与 §4.1 自己列的家族值 "0.0001" 冲突。
- 这正是我在 §4.4 刚修好的同类问题，**没传播到 §8**。

### A3. 多数票平局规则未定义（R3 W4）
81 案中 **3 案三次运行给出三个不同判定**（milvus_021 / milvus_038 / qdrant_027）。
论文写的 "a case confirmed on a majority" 实为「至少两次把该案算作确认（convention 下 HR 计入）」→ 39/51。
严格多数（两次须记同一判定）→ **37/51**。定义须写准。

### A4. §4.1 Holm 家族（R2 W3）
我写的「这四个值构成家族，对家族做 Holm 校正」是**循环定义**（家族 = 那四个显著值本身）。
另：我本轮在 §4.4 新增了 `p=0.0225`（部署臂 vs flat 召回层），使召回层显著值变 5 个而非 4 个，
而家族计数仍是旧的 19/10——须重数后重述。

### A5. §4.2 的 26/20（R2 W1，R3 W2）——**已挂账**
按 (vendor, reported_version) join 现行台账给 **49/30**（按前缀 50/31）；R2 重建给 27/21；论文印 26/20。
"15 versions run" 与复现包里 12 个版本目录冲突。差异源头是台账代际。

### A6. 我上轮新写的两处过强（R2）
- §3.1 "§4.4 and §4.5 vary its internal organization and its evidence access, **holding everything
  else fixed**" —— 与 §4.1（臂中途加、三个对比多于一变量）、§6 冲突
- §2 "**none** takes its expectation from untagged, system-level API prose" —— 对 RESTInfer/ICON 过强；
  tex 原文更准确（"parameter/method granularity…the behavioural residual sits above that granularity"）
- §4.4 nine-arm 描述 "the six primary-backbone configurations other than the core" —— 主骨干非 core 实为
  **7** 个（含 source-only）；该九臂不含两个 source-only，须点名

## B. 复现包（**待 R1 收工后再动**，避免搅掉它的核验）

### B1. 匿名化声明不实（R2 W5）——**已实测**
`grep -rl 11428 rq2/` = **254 / 824** 个文件；全仓 255。形态：**241 个派发词 .txt + 13 个 .jsonl**，
含 `11428\Desktop\testvdb_paper\.paperpilot\phase…`（3,371 次）、`.sourcedeps\milvus…`（1,144）、
`11428\Desktop\mftui\TestVDB\.sourcedeps\…`（300）、`11428/Desktop/tvdb_sessions/intelligence/…`（102）、
`11428\Desktop\testvdb4exp\.sourcedeps\weaviat…`（60）。
README §12 却称 "The archive is anonymized for double-blind review"。**双盲风险，投稿前必须洗。**

### B2. README 的 RQ3 表印双计数（R2 W5 后半）——已见
README 表列 `full-coverage-v3 | 23,258 | 22,540`，而 §4.6 明确说主日志是 205 个模板日志的逐字回声、
单份口径应为 11,629 / 1,127。README 与论文互相矛盾。

### B3. contract core 的重判文件未被发货脚本应用（R2，数值无影响）——待核

## C. R3 已复核为真的修复（正面）
- 五个脚本就地跑通、逐条对上论文：`pair_audit.py`(134=18/58/58)、`clause_tally.py`
  (§4.5 表逐格 + 两条重放 + 合规计数)、`clause_tally.py second`(56/50-22/24-of-48/217)、
  `bootstrap_net_f1.py`(net 0 [−8,+8]、F1 +0.033 [−0.044,+0.115])、`convention_pricing.py`、
  `recompute_paper_numbers.py`
- 上轮"包落后论文一代"的失效模式**不复现**
- R2 另核：§4.4 每个费率/配对/p 都满足「层次差 = 配对差」与 a=先印臂约定；强制跨度 [23,31]/[27,48]；
  集合交 22/27、23/26；RQ3 四数在扣回声后全准；重判披露 19/18/1

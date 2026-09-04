# PPT Approach 实例串讲页设计稿(W1-W2,v2 细化版,2026-08-31)

**定位**:approach 章节末尾实例收束页,插在页 11(novelty 与归档)之后、页 12(验证规模)之前。
路径约定同主设计稿 `ppt-approach-redesign.md`:`../../mftui/TestVDB/…` = 主插件仓库;`../../../.claude/plugins/cache/…` = 运行产物。

**实例**:qdrant v1.18.0,`recommend` 接口 `lookup_from` 负例维度校验绕过(上游 issue #10369,已 `accepted`)。
内部标识:`chunk_points+recommend`(R21)/ `state_recommend_02_lookup_dim_recreate` / `qdrant_state_recommend_001`——按页 1 术语声明,展示层不出现。

**与页 8 的分工**:页 8(R22 scroll)= 同一块的两条生成路径(机制对比);本页 = 一条 bug 走完五步(时序串讲)。过渡句见 W1 讲稿。

**红线沿用主设计稿**:bug / behavioral specification / knowledge;不写 novel;多版本与 RQ3 数字不出现。

***

# 页 W1

## 标题

- **主标题(推荐)**:`一条 bug 的五次变形`
- 副标题:`lookup_from 负例维度校验绕过 —— qdrant v1.18.0 · 上游 #10369(accepted)`
- 备选主标题:`从文档一句话到 accepted bug`(叙事向)/ `实例串讲:五步管线端到端`(保守向)
- 选型理由:主标题以"变形"立骨——每步一次形态变换(知识→规约→场景→观测→判定),与版式的箭头标签互为表里;实例名退居副标题做锚。

## 版式(16:9,三层结构)

```
┌────────────────────────────────────────────────────────────┐
│ 标题带(高 12%):主标题左对齐 + 副标题灰字同行右侧            │
├────────────────────────────────────────────────────────────┤
│ 五列流程带(高 70%):①-⑤ 五等列,列间 4 个箭头               │
│ 每列自上而下:步骤徽标 → 步骤名(页 2 同名)→ 实绩卡 → 产物脚注│
│ 列间箭头上方挂形态标签(灰底白字小胶囊)                      │
├────────────────────────────────────────────────────────────┤
│ 信息条(高 18%):浅灰底一行——上游结果 + 全局定位             │
└────────────────────────────────────────────────────────────┘
```

**视觉语义(两套边框,全篇沿用)**:

- **实线边框 = 0-LLM 机械步骤**,虚线边框 = LLM 参与步骤——呼应页 2 讲稿"LLM 只负责 ② 的提取与 ④ 的场景生成,其余全部有确定性脚本/机械门禁"。
- ③ 与 ④ 下半(gate)、⑤ 上半(候选提取/初筛/引文预检)是实线;② ④ 上半 ⑤ 下半(auditor 裁决)是虚线。
- 不引入颜色语义(与现有 49 页风格一致),边框虚实承担全部区分。

## 五列展示内容(逐字稿)

**列①**(徽标 `①`,步骤名 `Knowledge 采集/提取`)

> 卡题:**规格原文(第一锚)**
>
> `openapi.json v1.18.0(按 tag 抓取,版本核对 gate 拦截过污染快照)`
> `RecommendRequest.lookup_from:"the other collection should have the same`
> `vector size as the current collection"`
> `positive / negative 共用同一 RecommendExample schema`

产物脚注(小字):`fetch_openapi_spec.py → openapi.json`

**列②**(徽标 `②`,虚线边框,步骤名 `Specification 提取`)

> 卡题:**一条行为规约**
>
> `"lookup_from collection must have same vector size as`
> &#x20;` target collection vector"`
> `state 类 · endpoint 级 · evidence_tier=explicit`

产物脚注:`contract-formalizer → structured_contract.json`(assertion 为 formalizer 同义提炼;文档逐字原句 = 列① Note 句"the other collection should have the same vector size…"——should→must 升格属提取规范,导师追问"must 是谁说的"时答:承诺语义 + 行为可观测)

**列③**(徽标 `③`,实线边框,步骤名 `分块 + 策略预绑定`)

> 卡题:**0-LLM 分流**
>
> `该规约独占一块(33 块之一)`
> `state 类无内置直绑 → 绑定清单显式置空`
> `→ 三视角各自场景构造(不是参数矩阵)`

产物脚注:`chunk_contract.py + bind_strategies.py`

**列④**(徽标 `④`,虚线边框,步骤名 `三视角攻击 + gate 预验证`)

> 卡题:**三视角 20 脚本,各写各的 oracle**
>
> `boundary:维度矩阵 —— 只扫了 positive 格`
> `semantic:反方向格(lookup4→target8)—— 未命中`
> `state:生命周期 —— 基线 → 删除后 8 维同名重建`
> `→ positive/negative 分路径 → 恢复复测`
>
> `gate 机械预检:0 拦截 / 12 轻量提示,放行`

产物脚注:`attack-*.md → 20 脚本;_preverify(D3b-R4.0)`

**列⑤**(徽标 `⑤`,上下两段,步骤名 `执行 → 证据链双 agent → 终判`)

> 卡题:**非对称即缺陷**
>
> `同一 8 维 lookup 向量:`
> `positive → 400 · negative → 200 带结果`
>
> `证据链 doc6 / exec5 / source9 / 反证2,引文逐字预检全过`
> `终判:bug(高置信)`
> `源码:recommendations.rs —— zip 截断 + 入口检查不可达`

产物脚注:`extract → builder 链 → auditor 判词`

**四个形态标签**(箭头胶囊):`知识→规约` `规约→场景` `场景→观测` `观测→判定`

**信息条(逐字)**:

> 提交上游 2026-08-29 → 48 小时内获得 `bug` + `accepted` + `area/segment` 标签 · 35 bugs 之一(净新发现侧)· 完整链路:20 脚本 → 1 候选 → 1 条证据链 → 1 个 bug

## 讲稿提示

- 开场(回指页 2):"总览页的五步是地图——现在拿一条真 bug 把它走一遍,注意每步它变成什么。"
- 列③(页 6 呼应):"state 类耦合不是参数边界,系统不硬绑——绑确定的,放不确定的,构造权交给视角。"
- 列④(本页最重一句):"缺陷只住在'target 4 维 ← lookup 8 维 × **negative**'这一个格子——boundary 没扫到,semantic 打了反方向,只有 state 视角的生命周期场景踩中它。**三视角不是冗余,是互补。**"
- 收尾(指向列⑤卡题):"文档里的一句话,最后变成源码里一个具体函数的一行 zip。"
- 时间预算:90 秒;若被追问 gate 提示是什么 → "anyOf 分支歧义的轻量提示,不阻塞——下页有 severity 设计的出处"。

## 素材出处

- 契约/分块/绑定:[structured\_contract.json](../../../.claude/plugins/cache/testvdb/testvdb/2.3.0/results/qdrant/v1.18.0/structured_contract.json) + [chunks.json](../../../.claude/plugins/cache/testvdb/testvdb/2.3.0/results/qdrant/v1.18.0/chunks.json)
- 20 脚本与观测:[2026-08-27T20-06-45Z/candidates.jsonl](../../../.claude/plugins/cache/testvdb/testvdb/2.3.0/results/qdrant/v1.18.0/2026-08-27T20-06-45Z/candidates.jsonl)
- gate 结果:[2026-08-27T20-06-45Z/preverify\_findings.json](../../../.claude/plugins/cache/testvdb/testvdb/2.3.0/results/qdrant/v1.18.0/2026-08-27T20-06-45Z/preverify_findings.json)
- 实现脚本:[fetch\_openapi\_spec.py](../../mftui/TestVDB/scripts/fetch_openapi_spec.py) / [bind\_strategies.py](../../mftui/TestVDB/scripts/bind_strategies.py) / [chunk\_contract.py](../../mftui/TestVDB/scripts/chunk_contract.py) / [\_preverify\_spec\_shape.py](../../mftui/TestVDB/scripts/_preverify_spec_shape.py)

***

# 页 W2

## 标题

- **主标题(推荐)**:`从 200 到 bug:三道证据各自关上一扇门`
- 副标题:`同一观测,三种被排除的替代解释 —— 判定可信度的来源`
- 备选:`三张证据卡:排除,而非确证`(方法论向,更贴 auditor 的反证式设计)
- 选型理由:W1 收在"非对称即缺陷"(观测阳性),W2 回答"阳性为什么成立"——标题直接把 200 与 bug 的因果链摆出来;"关上一扇门"呼应每卡排除一类错误结论的结构。

## 版式(16:9,三层结构)

```
┌────────────────────────────────────────────────────────────┐
│ 标题带(高 12%):同 W1 风格                                  │
├────────────────────────────────────────────────────────────┤
│ 三卡带(高 66%):三等宽卡横排                                │
│ 每卡自上而下:卡头编号+名称 → 观测区(等宽字体块)→           │
│   "排除"行(红叉图标×短句)→ 机制锚行(小字,回指页 10)      │
├────────────────────────────────────────────────────────────┤
│ 结果条(高 22%):箭头链一行 + 结论句                          │
└────────────────────────────────────────────────────────────┘
```

- 卡头编号用 `证据 1/2/3`;三卡等宽,卡间距 = 卡宽 1/3(留白大于卡宽的一半,避免三栏均分感)。
- 观测区统一等宽字体浅灰底——三卡中唯一的"数据"元素,视觉上强调"结论从数据来"。
- "排除"行是每卡的情绪重音:红叉 + 一句被排除的解释,字号与观测正文同大。

## 三卡展示内容(逐字稿)

**卡 1|非对称观测**

> 卡头:`证据 1 · 非对称观测`
>
> 观测区(等宽):
> `positive=[100]        → 400  Vector dimension error:`
> &#x20;                             `                              expected dim: 4, got 8`
> `negative=[100]        → 200  {"result": [...], "status": "ok"}`
> `立即重拍 positive     → 仍 400(确定性)`
>
> ✗ 排除:偶发抖动 · 缓存伪象
> 机制锚:候选机械提取(0-LLM)· 脚本自错自动排除 → 页 10 环节 a

**卡 2|区分性探针**

> 卡头:`证据 2 · 区分性探针`
>
> 观测区(等宽):
> `lookup 向量改 [0,0,9,9,9,9,9,9]`
> `zip 截断模型:q = 2·avg(pos) − neg[:4] = [2,0,−9,−9]`
> `预测 id2 = √170 = 13.038405`
> `实测 id2 = 13.038404(Δ ≈ 1e-4)✓`
> `"丢弃负例"假设预测 [1.00, 2.83, 1.41] ✗`
> `恢复 4 维 → 逐位回到基线分数(无脏状态)✓`
>
> ✗ 排除:机制歧义("分数算错")· 持久脏状态
> 机制锚:builder 三证只取证 · 假设-排除式取证 → 页 10 环节 c

**卡 3|义务范围裁决**

> 卡头:`证据 3 · 义务范围裁决`
>
> 观测区(等宽):
> `契约断言主语:lookup_from **collection** must have same`
> &#x20; `  vector size …(无 positive/negative 限定语)`
> `openapi note 同措辞:"the other collection"`
> `实现:正负例走同一解析 helper(convert_to_vectors)`
> `→ 契约 · 规格 · 实现 三方同向`
>
> ✗ 排除:"文档只承诺 positive 路径"窄读抗辩(正面驳回,不留模糊地带)
> ✗ 排除:"源码没写校验=有意为之"——沉默 ≠ 明示 by-design,不得据此筛除
> 机制锚:引文逐字机械比对 + LLM 只裁语义边界 → 页 10 判定规则卡(机械判定给锚,不给判决——语义裁决在固定规则内进行)

**结果条(逐字)**:

> 20 脚本 → 1 候选 → 1 条证据链 → 1 个 bug → 上游 `accepted`(48 小时)
> 观测回答"发生了什么";探针回答"机制是什么";裁决回答"义务是什么"——三问三答,判定闭合。

## 讲稿提示

- 承接 W1:"W1 结尾说非对称即缺陷——但 200 就一定是 bug 吗?三道证据各自关掉一扇'其实不是 bug'的门。"
- 卡 2 是全场最值得慢讲的一张(30 秒):"一个 √170 的预测值,把'服务器算错了'变成'服务器在静默截断你的向量'——从症状到机制的定罪。"
- 卡 3 回马枪(回指 W1 列①):"还记得 ① 里 openapi 那句 'the other collection' 吗?没有写 positive——这个措辞在这里决定了终判方向。**知识层的每个字,都可能成为几百步之后的判定依据。**"
- 主动防御两问:
  - "怎么证明不是你们环境问题?" → 卡 1 重拍 + 卡 2 恢复复测 + 盲重跑(两独立执行同判)三重。
  - "会不会只是文档没写 negative?" → 卡 3 三方同向;契约-规格-实现任何一方单独特指 positive,窄读即成立——恰恰三方都没写。
- 时间预算:2 分钟(卡 2 占 1/3)。

## 素材出处

- 证据链全文:[state\_recommend\_02\_lookup\_dim\_recreate.chain.json](../../../.claude/plugins/cache/testvdb/testvdb/2.3.0/results/qdrant/v1.18.0/2026-08-27T20-06-45Z/evidence_chain/state_recommend_02_lookup_dim_recreate.chain.json)(execution\_evidence\[1] 区分性探针 / counter\_evidence\[0] 窄读抗辩)
- 终判词:[chain\_verdicts.json](../../../.claude/plugins/cache/testvdb/testvdb/2.3.0/results/qdrant/v1.18.0/2026-08-27T20-06-45Z/debate_logs/chain_verdicts.json)(义务范围裁决原文)
- 源码引文:主插件仓 `.sourcedeps/qdrant/v1.18.0/lib/collection/src/recommendations.rs` L110-114、L377-382
- 上游:github.com/qdrant/qdrant/issues/10369

***

# 单页压缩变体(页数紧张时 W1-W2 合一)

- 保留:W1 五列流程带(原样)+ W2 三卡各压成一行三列(卡头+✗行,观测区只留 1 行数据)+ 结果条压成半行。
- 讲稿只留两句:列④"只有 state 视角踩中那个格子";卡 2"√170 定罪"。
- 代价:卡 1/卡 3 的可信度论证退化为文字 → W2 完整版移入 Q\&A 备用页,不删除。

***

# 数字与事实核对表(做页时逐条对)

| 稿中数字/事实                                         | 依据                                                                                  |
| ----------------------------------------------- | ----------------------------------------------------------------------------------- |
| 33 块 / 101 单元                                   | chunks.json;FINAL\_STATS\_RQ1\_v34.md                                               |
| 本块 20 脚本(boundary 7 / semantic 7 / state 6)     | candidates.jsonl 20 条;debate\_logs 计数                                               |
| gate 0 拦截 / 12 轻量提示                             | preverify\_findings.json(REJECT 0 / WARN 12,ambiguous\_branch)                      |
| doc 6 / exec 5 / source 9 / 反证 2                | chain.json 各数组长度                                                                    |
| q = \[2,0,−9,−9];√170 = 13.038405 vs 13.038404  | chain.json execution\_evidence\[1]                                                  |
| "丢弃负例"假设预测 \[1.00, 2.83, 1.41]                  | chain.json execution\_evidence[1](排除句原文)                                            |
| convert\_to\_vectors 同一 helper                  | chain.json counter\_evidence\[0] + source\_evidence(fetch\_vectors.rs 311-320 对称解析) |
| recommendations.rs L110-114 zip / L377-382 合并路径 | chain.json source\_evidence\[0]\[1]                                                 |
| 48 小时 accepted                                  | issue 10369:created 2026-08-29T08:28Z,labels bug+accepted+area/segment              |
| 35 bugs / 净新侧                                   | FINAL\_STATS\_RQ1\_v34.md;页 11 口径                                                   |
| semantic 视角"lookup4→target8 未命中"                | candidates.jsonl:semantic\_recommend\_01 case B rejected 4xx → NO\_DEFECT           |

***

# English Version(W1-EN / W2-EN,slide-facing text + speaker notes)

版式、素材出处与核对表与中文版共用,不重复;本节逐元素镜像 W1/W2。术语与论文一致:bug / behavioral specification / knowledge / net-new findings;红线(不写 novel 等)同样适用。
边框语义英文表述:**solid = LLM-free (mechanical) / dashed = LLM-involved**。

***

## Slide W1-EN

### Title

- **Main (recommended)**: `Five Transformations of One Bug`
- Subtitle: *lookup\_from negative-example dimension-validation bypass — qdrant v1.18.0 · upstream issue #10369 (accepted)*
- Alternatives: `From a Sentence in the Docs to an Accepted Issue`(narrative)/ `The Five-Stage Pipeline, End to End`(conservative)

### The five columns (verbatim)

**Column ①** — badge `①`, stage name `Knowledge acquisition`

> Card title: **The spec sentence (primary anchor)**
>
> `openapi.json v1.18.0 (fetched per tag; the version-check gate once`
> `intercepted a polluted snapshot)`
> `RecommendRequest.lookup_from: "the other collection should have the`
> `same vector size as the current collection"`
> `positive / negative share one RecommendExample schema`

Footnote: `fetch_openapi_spec.py → openapi.json`

**Column ②** — badge `②`, dashed border, stage name `Specification extraction`

> Card title: **One behavioral specification**
>
> `"lookup_from collection must have same vector size as`
> &#x20;` target collection vector"`
> `state category · endpoint-level · evidence tier = explicit`

Footnote: `contract-formalizer → structured_contract.json`

**Column ③** — badge `③`, solid border, stage name `Chunking + strategy pre-binding`

> Card title: **LLM-free routing**
>
> `The specification gets its own chunk (one of 33)`
> `state category: no built-in binding → binding list explicitly empty`
> `→ each perspective constructs its own scenario (not a parameter grid)`

Footnote: `chunk_contract.py + bind_strategies.py`

**Column ④** — badge `④`, dashed border, stage name `Three-perspective attacks + pre-execution gate`

> Card title: **20 scripts, three perspectives, each with its own oracle**
>
> `boundary: dimension grid — scanned positive cells only`
> `semantic: the reverse direction (lookup 4-d → target 8-d) — miss`
> `state: lifecycle — baseline → delete & recreate lookup at 8-d`
> `→ positive/negative paths → restore & re-check`
>
> `gate (mechanical): 0 rejections / 12 soft warnings, all released`

Footnote: `attack-*.md → 20 scripts; _preverify (D3b-R4.0)`

**Column ⑤** — badge `⑤`, two sub-blocks, stage name `Execution → evidence-chain agents → verdict`

> Card title: **Asymmetry is the bug**
>
> `Same 8-d lookup vector:`
> `positive → 400 · negative → 200 with results`
>
> `Evidence chain doc 6 / exec 5 / source 9 / counter 2 —`
> `verbatim quote check fully passed`
> `Verdict: bug (high confidence)`
> `Root cause: recommendations.rs — zip truncation + unreachable entry check`

Footnote: `extract → builder chain → auditor verdict`

**Morph labels**(arrow pills): `knowledge → specification → scenario → observation → verdict`

**Info bar(verbatim)**:

> Submitted upstream 2026-08-29 → `bug` + `accepted` + `area/segment` within 48 hours · one of 35 bugs (net-new findings side) · full trail: 20 scripts → 1 candidate → 1 evidence chain → 1 bug

### Speaker notes (EN)

- Opening (callback to the overview slide): "The five stages you saw are a map — let's walk one real bug through them and watch what it becomes at each step."
- Column ③ (echoes the pre-binding slide): "A cross-collection coupling is not a parameter boundary — the system does not force a binding. **Bind what is certain; free what is not.**"
- Column ④ (the key line): "The bug lives in exactly one cell: target 4-d ← lookup 8-d × **negative**. Boundary never scanned it; semantic probed the reverse direction; only the state perspective's lifecycle scenario steps on it. **Three perspectives are complementary, not redundant.**"
- Close (point at column ⑤): "A sentence from the docs ends up as one zip in one function."
- Timing: 90 seconds; if asked about the gate warnings → "soft anyOf-ambiguity notices, non-blocking — the severity design is on its own slide."

***

## Slide W2-EN

### Title

- **Main (recommended)**: `From a 200 to a Bug: Three Cards, Three Doors Closed`
- Subtitle: *Same observation, three rejected alternatives — where the verdict's credibility comes from*
- Alternative: `Exclusion, Not Confirmation`(methodological)

### Three cards (verbatim)

**Card 1 · Asymmetric observation**

> Observation block (mono):
> `positive=[100]   → 400  Vector dimension error:`
> &#x20;                       `                        expected dim: 4, got 8`
> `negative=[100]   → 200  {"result": [...], "status": "ok"}`
> `re-probe (positive, immediate) → 400 again (deterministic)`
>
> ✗ Rules out: transient flakiness · cache artifacts
> Anchor: mechanical candidate extraction (LLM-free) · script errors auto-excluded → step ⑤-a

**Card 2 · Distinguishing probe**

> Observation block (mono):
> `lookup vector set to [0,0,9,9,9,9,9,9]`
> `zip-truncation model: q = 2·avg(pos) − neg[:4] = [2,0,−9,−9]`
> `predicted id2 = √170 = 13.038405`
> `measured  id2 = 13.038404 (Δ ≈ 1e-4) ✓`
> `"dropped negative" alternative predicts [1.00, 2.83, 1.41] ✗`
> `restore to 4-d → scores return to baseline bit-for-bit ✓`
>
> ✗ Rules out: mechanism ambiguity ("scores computed wrongly") · persistent stale state
> Anchor: builder collects evidence only · hypothesis-exclusion style → step ⑤-c

**Card 3 · Obligation-scope adjudication**

> Observation block (mono):
> `specification subject: "lookup_from collection must have same`
> &#x20; `  vector size …" — no positive/negative qualifier`
> `openapi note, same wording: "the other collection"`
> `implementation: both example lists resolved by one helper`
> &#x20; `  (convert_to_vectors)`
> `→ contract · spec · implementation: three sources converge`
>
> ✗ Rules out: the narrow reading ("the docs only promise the positive path") — rebutted head-on, no gray zone left
> ✗ Rules out: "no validation in source = intended" — silence ≠ an explicit by-design; cannot dismiss on that basis
> Anchor: verbatim quote check (mechanical) + LLM adjudicates semantic scope only → verdict rule card

**Result bar(verbatim)**:

> 20 scripts → 1 candidate → 1 evidence chain → 1 bug → upstream `accepted` (48 hours)
> The observation answers *what happened*; the probe answers *what the mechanism is*; the adjudication answers *what the obligation is* — three questions, three answers, one closed case.

### Speaker notes (EN)

- Bridge from W1: "W1 ended with 'asymmetry is the bug.' But is a 200 always a bug? Three cards close three 'actually not a bug' doors."
- Card 2 deserves 30 slow seconds: "A √170 prediction turns 'the server computed wrong scores' into 'the server silently truncates your vector' — conviction from symptom to mechanism."
- Card 3 callback (point back at W1 column ①): "Remember the openapi wording, 'the other collection'? No 'positive' anywhere. That wording decides the verdict five stages later. **Every word in the knowledge layer can become a verdict hundreds of steps downstream.**"
- Pre-empted questions:
  - "How do we know it's not your environment?" → Card 1 re-probe + Card 2 restore + blind rerun (two independent executions, same verdict).
  - "Maybe the docs just don't cover negatives?" → Card 3: any one of the three sources singling out positive would sustain the narrow reading — none does.
- Timing: 2 minutes (one third on Card 2).

### 单页压缩变体(EN)

- Keep the W1 five-column band as-is; compress each W2 card to header + one ✗ line + one data line; result bar to half a line.
- Keep only two spoken lines: column ④ "only the state perspective steps on that cell"; Card 2 "convicted by √170."
- Full W2-EN moves to the Q\&A backup deck.

***

# 附录:源文件行号索引(按五步组织,全部绝对路径,可直接点击/复制)

> ⚠ **VSCode 点击跳转说明**:Markdown 预览对指向工作区外的文件链接默认拦截,点击无效——这是编辑器安全策略,与路径写法无关。确定性替代:[instance-links.bat](instance-links.bat)(同目录)——双击运行,按 `code --goto "路径:行号"` 逐条在 VSCode 打开并**精确停靠到行**,节与节之间按任意键继续。以下链接仍保留绝对路径供复制。

> ✅ **可点击**:下方所有链接指向工作区内副本 [files/10369-walkthrough/](../files/10369-walkthrough/)(2026-08-31 从原件整文件复制,**行号与原件一致**,VSCode 内可直接点击打开)。链接文本保留原件绝对路径,便于溯源。
> 原件位置:
>
> - 主插件仓库:`C:/Users/11428/Desktop/mftui/TestVDB`
> - 运行产物:`C:/Users/11428/.claude/plugins/cache/testvdb/testvdb/2.3.0/results/qdrant/v1.18.0`
> - 本案 session:`…/v1.18.0/2026-08-27T20-06-45Z`
> - 副本结构:`pipeline/`=机制文件(脚本+agent 规范)、`contract/`=契约与分块、`session/`=运行产物、`qdrant-src-v1.18.3/`=源码
>
> qdrant 源码行号以链内 source\_evidence 与 auditor rationale(亲读逐字核实)为权威,clone 为 v1.18.0(`.qdrant-src-1180`,已清理);本地现存 v1.18.3 行号已漂移(zip 在 L112)。
> 副本为临时快照(勿提交/与原件可能失同步);若原件更新,以原件为准。

## ① Knowledge

- `_fetch_qdrant`:按 tag 抓 `docs/redoc/{minor}.x/openapi.json`(L60 = redoc 目录 v 前缀踩坑注释)
  [C:/Users/11428/Desktop/mftui/TestVDB/scripts/fetch\_openapi\_spec.py#L52-L63](../files/10369-walkthrough/pipeline/fetch_openapi_spec.py#L52-L63)

## ② Behavioral Specification

- `qdrant_state_recommend_001` 完整条目(assertion / type=state\_constraint / level=endpoint / evidence\_tier=explicit / bound\_strategies=\[])
  [C:/Users/11428/.claude/plugins/cache/testvdb/testvdb/2.3.0/results/qdrant/v1.18.0/structured\_contract.json#L7291](../files/10369-walkthrough/contract/structured_contract.json#L7291)

## ③ 分块 + 预绑定

- `UNIT_SOURCES` 四类单元源
  [C:/Users/11428/Desktop/mftui/TestVDB/scripts/chunk\_contract.py#L36](../files/10369-walkthrough/pipeline/chunk_contract.py#L36)
- 单端点块 + `-1of2` 超限切分
  [C:/Users/11428/Desktop/mftui/TestVDB/scripts/chunk\_contract.py#L96-L102](../files/10369-walkthrough/pipeline/chunk_contract.py#L96-L102)
- `BUILTIN_BASELINE`:type/range 直绑,state 起全部空表;L62-63 注释"预绑定的价值在分流,绑一切等于没绑"
  [C:/Users/11428/Desktop/mftui/TestVDB/scripts/bind\_strategies.py#L64-L79](../files/10369-walkthrough/pipeline/bind_strategies.py#L64-L79)
- `chunk_points+recommend`(单单元块)
  [C:/Users/11428/.claude/plugins/cache/testvdb/testvdb/2.3.0/results/qdrant/v1.18.0/chunks.json#L572](../files/10369-walkthrough/contract/chunks.json#L572)
- 预绑定消费(D2 v3.5,2026-09-04 起 A+B 叠加):非空直按清单(路径 A) **+ 全部约束普适 G1-G10 双向(路径 B,含已绑定)**,A/B 独立构造=交叉验证;gate 症状④强制 `_strategy_binding` 在位
  [C:/Users/11428/Desktop/mftui/TestVDB/agents/attack-state.md#L99-L107](../files/10369-walkthrough/pipeline/attack-state.md#L99-L107)

## ④ 攻击生成 + gate

- **本案三视角脚本原件**(docstring 含 Attack:/Oracle:/Constraint: 行):主角 [state\_recommend\_02\_lookup\_dim\_recreate.py(234 行)](../files/10369-walkthrough/session/debate_logs/state_recommend_02_lookup_dim_recreate.py);对照 [boundary\_recommend\_01\_lookup\_dim\_matrix.py](../files/10369-walkthrough/session/debate_logs/boundary_recommend_01_lookup_dim_matrix.py) / [semantic\_recommend\_01\_xdim\_lookup\_bidir.py](../files/10369-walkthrough/session/debate_logs/semantic_recommend_01_xdim_lookup_bidir.py)(原件均在 SESSION/debate_logs/)
- Oracle 行强制(缺 = C3 打回);配套生成 L109-L110
  [C:/Users/11428/Desktop/mftui/TestVDB/agents/attack-state.md#L87](../files/10369-walkthrough/pipeline/attack-state.md#L87)
- 8c 接线(preverify 命令在 L596)
  [C:/Users/11428/Desktop/mftui/TestVDB/commands/mine.md#L577](../files/10369-walkthrough/pipeline/mine.md#L577)
- C 类 `check_shape_conflicts`(断言×响应形状相容矩阵)
  [C:/Users/11428/Desktop/mftui/TestVDB/scripts/\_preverify\_spec\_shape.py#L272](../files/10369-walkthrough/pipeline/_preverify_spec_shape.py#L272)
- D 类 `check_request_required`(必填树/anyOf 消歧)
  [C:/Users/11428/Desktop/mftui/TestVDB/scripts/\_preverify\_spec\_shape.py#L400](../files/10369-walkthrough/pipeline/_preverify_spec_shape.py#L400)
- meta.oracle 单写者物化(调用在 L503)
  [C:/Users/11428/Desktop/mftui/TestVDB/scripts/\_preverify\_spec\_shape.py#L451](../files/10369-walkthrough/pipeline/_preverify_spec_shape.py#L451)
- WARN 边车写出 `{script_id}.preverify_warnings.json`
  [C:/Users/11428/Desktop/mftui/TestVDB/scripts/\_preverify\_spec\_shape.py#L515](../files/10369-walkthrough/pipeline/_preverify_spec_shape.py#L515)
- 本块 gate 结果(REJECT 0 / WARN 12)
  [C:/Users/11428/.claude/plugins/cache/testvdb/testvdb/2.3.0/results/qdrant/v1.18.0/2026-08-27T20-06-45Z/preverify\_findings.json](../files/10369-walkthrough/session/preverify_findings.json)
- 本案 WARN 边车
  [C:/Users/11428/.claude/plugins/cache/testvdb/testvdb/2.3.0/results/qdrant/v1.18.0/2026-08-27T20-06-45Z/state\_recommend\_02\_lookup\_dim\_recreate.preverify\_warnings.json](../files/10369-walkthrough/session/state_recommend_02_lookup_dim_recreate.preverify_warnings.json)
- 本案 oracle(物化键)
  [C:/Users/11428/.claude/plugins/cache/testvdb/testvdb/2.3.0/results/qdrant/v1.18.0/2026-08-27T20-06-45Z/debate\_logs/state\_recommend\_02\_lookup\_dim\_recreate.meta.json#L12](../files/10369-walkthrough/session/debate_logs/state_recommend_02_lookup_dim_recreate.meta.json#L12)

## ⑤ 执行 → 证据链双 agent → 终判

- 8d 执行接线
  [C:/Users/11428/Desktop/mftui/TestVDB/commands/mine.md#L607](../files/10369-walkthrough/pipeline/mine.md#L607)
- 8e:候选提取 L634 / L1 初筛 L640 / 引文逐字预检 L646
  [C:/Users/11428/Desktop/mftui/TestVDB/commands/mine.md#L630-L646](../files/10369-walkthrough/pipeline/mine.md#L630-L646)
- 8e.7 auditor 收口;9a novelty 后置
  [C:/Users/11428/Desktop/mftui/TestVDB/commands/mine.md#L669](../files/10369-walkthrough/pipeline/mine.md#L669) · [C:/Users/11428/Desktop/mftui/TestVDB/commands/mine.md#L750](../files/10369-walkthrough/pipeline/mine.md#L750)
- builder:step1 三段(A 文档 / B 执行取证 / C 链追溯);claim\_alignment L83;对照取证义务 L95;step2 源码搜证 L114;输出 schema L152
  [C:/Users/11428/Desktop/mftui/TestVDB/agents/evidence-builder.md#L55](../files/10369-walkthrough/pipeline/evidence-builder.md#L55)
- auditor:WARN 边车消费(不改机械判定权)
  [C:/Users/11428/Desktop/mftui/TestVDB/agents/chain-auditor.md#L90-L95](../files/10369-walkthrough/pipeline/chain-auditor.md#L90-L95)
- auditor:三视角聚合 + 视角 A 机械判定
  [C:/Users/11428/Desktop/mftui/TestVDB/agents/chain-auditor.md#L97-L99](../files/10369-walkthrough/pipeline/chain-auditor.md#L97-L99)
- auditor:明示 by-design 才可 REFUTED
  [C:/Users/11428/Desktop/mftui/TestVDB/agents/chain-auditor.md#L169-L171](../files/10369-walkthrough/pipeline/chain-auditor.md#L169-L171)
- **本案候选行(四行观测 + DEFECT\_FOUND 全在此行)**
  [C:/Users/11428/.claude/plugins/cache/testvdb/testvdb/2.3.0/results/qdrant/v1.18.0/2026-08-27T20-06-45Z/candidates.jsonl#L16](../files/10369-walkthrough/session/candidates.jsonl#L16)
- **本案执行 log**:L7 baseline / L8-L9 positive+repeat 400 / L10 restore / L11 VERDICT(含 negative 200)
  [C:/Users/11428/.claude/plugins/cache/testvdb/testvdb/2.3.0/results/qdrant/v1.18.0/2026-08-27T20-06-45Z/r21\_exec\_logs/state\_recommend\_02\_lookup\_dim\_recreate.log#L7-L11](../files/10369-walkthrough/session/r21_exec_logs/state_recommend_02_lookup_dim_recreate.log#L7-L11)
- 链:claim\_summary(L4)/ doc\_evidence×6(L5)/ execution\_evidence×5(L37,**探针 √170 在 L49**)/ source\_evidence×9(L64)/ counter\_evidence×2(L120)/ open\_questions(L147)
  [C:/Users/11428/.claude/plugins/cache/testvdb/testvdb/2.3.0/results/qdrant/v1.18.0/2026-08-27T20-06-45Z/evidence\_chain/state\_recommend\_02\_lookup\_dim\_recreate.chain.json#L4](../files/10369-walkthrough/session/evidence_chain/state_recommend_02_lookup_dim_recreate.chain.json#L4)
- **终判:verdict=DEFECT(L10-L12);rationale 全文——三查+义务范围裁决+R19/R20 路径(L17)**
  [C:/Users/11428/.claude/plugins/cache/testvdb/testvdb/2.3.0/results/qdrant/v1.18.0/2026-08-27T20-06-45Z/debate\_logs/chain\_verdicts.json#L10](../files/10369-walkthrough/session/debate_logs/chain_verdicts.json#L10) · [C:/Users/11428/.claude/plugins/cache/testvdb/testvdb/2.3.0/results/qdrant/v1.18.0/2026-08-27T20-06-45Z/debate\_logs/chain\_verdicts.json#L17](../files/10369-walkthrough/session/debate_logs/chain_verdicts.json#L17)

## qdrant 源码(权威行号 = v1.18.0 链内记录;本地现存 v1.18.3 行号有漂移)

- `merge_positive_and_negative_avg` + `.zip(negative.iter())` 截断:v1.18.0 **L110-114**(fn L104-131 起始 104)
  本地现存副本(v1.18.3):[C:/Users/11428/Desktop/mftui/TestVDB/.sourcedeps/qdrant/v1.18.3/lib/collection/src/recommendations.rs#L104](../files/10369-walkthrough/qdrant-src-v1.18.3/recommendations.rs#L104)(fn\@104,zip\@L112)
- `recommend_by_avg_vector`(AverageVector 合并路径,绕过入口检查):v1.18.0 L377-382(fn L131-145)
  v1.18.3:[C:/Users/11428/Desktop/mftui/TestVDB/.sourcedeps/qdrant/v1.18.3/lib/collection/src/recommendations.rs#L339](../files/10369-walkthrough/qdrant-src-v1.18.3/recommendations.rs#L339)(fn\@339)
- segment 入口维度检查(Nearest 单向量):v1.18.0 common/mod.rs L61-69;WrongVectorDimension L195-201
  v1.18.3 结构有变("Check dimensionality" @L194/L206):[C:/Users/11428/Desktop/mftui/TestVDB/.sourcedeps/qdrant/v1.18.3/lib/segment/src/common/mod.rs#L194](../files/10369-walkthrough/qdrant-src-v1.18.3/common-mod.rs#L194)
- 正负例对称解析(同一 helper):v1.18.0 fetch\_vectors.rs L311-320(v1.18.3 中该文件已不在原路径)
- `#[default] AverageVector`:v1.18.0 schema.rs L805-810(未在现存副本核对)


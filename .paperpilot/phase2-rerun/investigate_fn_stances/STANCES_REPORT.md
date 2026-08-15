# 信息不可达 FN 锚点调查报告（fixG 前置调查）

> 日期：2026-08-16。任务来源：用户指令——"严格且深入地去调查并汇总对应数据库历史 PR 与 issues 表态，
> 应该能够提取出一些有效的表态（即便表态不直接源于原 issue 或 PR），这样我们就是否可以
> 名正言顺地将对应锚点引入 intelligence？"
> 调查对象：8 个信息不可达顽固 FN（docs/phase2-status-and-decisions.md §4，milvus_001 除外）
> 判定准绳：实验纪律 §9 锚点三条件（≥2 独立维护者行为 / 无方向冲突 / 现象类普适措辞）。
> 原始数据：本目录 `raw/`（25 个 GitHub issue/PR 完整 dump：detail+comments+timeline，
> 脚本 investigate_r1.py / investigate_r2.py，检索日志 _search_round1.json / _search_reverse.json）。

## 0. 结论速览

| 类 | 现象 | 本体 case | 判定 | 一句话理由 |
|----|------|-----------|------|-----------|
| A | milvus 数值精度/数学边界 | milvus_008 (49059) | **不可注入** | ACK 后修复死链（社区 PR 49264 被 stale 关闭未合并），仅 1 硬行为；另有反向风险（48204 "kind of expected"） |
| B | milvus REST v2 空串/无效参数 | milvus_012 (49889) + 017 (50018) | **不可注入** | GT 内部方向分裂：同簇 3 TP（009/012/017）vs 3 FP（011/027/028）；dbName 空串=TP 而 metricType 空串=FP，条件 2 数学挡死 |
| C | milvus 文档-行为不一致 | milvus_031 (50355) | **✅ 可注入** | 3 个独立修复行为（50355 docs PR 3513/3514；46683 docs PR 3402；46494 foxspy "fixed"）；无反向表态 |
| E | qdrant 无效值静默回退 | qdrant_002 (9017) | **不可注入** | 同一维护者 timvisee 方向分裂：9017 "Fixed via PR 9320" vs 9027 "we don't see this as a problem"（同属输入校验类） |
| F | qdrant 5xx→4xx 错误码 | qdrant_014 (9421) | **不可注入** | 单行为（timvisee "I agree...I like HTTP 405"）；fix PR 9442 open/未合并、无维护者表态 |
| G | weaviate 5xx→4xx 错误码 | weaviate_010 (12041) | **✅ 可注入** | ≥3 个独立 merged 修复（12049 500→422；12040 500→404；11878 "Fix more error codes in REST handler"）+ MEMBER 表态（12262 etiennedi +1）；无反向 |
| — | milvus_001 (47635) 材料空日志 | — | 不调查 | 材料形态边界，锚点无法作用 |

**6 个可调查类：2 类可名正言顺注入（C/G），4 类证据证明结构性不可注入。**

## 1. 死刑四类的证据细节（论文素材：不可达的深层结构）

四个"死刑"不是"没找到证据"，而是**证据证明了维护者态度本身不可收敛**：

### B 类（最典型）：同簇 GT 态度分裂
milvus "REST v2 接受空/无效参数"簇在 case 集内的 GT 分布：

| case | 现象 | GT | 维护者态度 |
|------|------|-----|-----------|
| 009 (49823) | nprobe=0 无校验 | **TP_ACK** | assign 未拒 |
| 012 (49889) | dbName 空串 | **TP_ACK** | assign MrPresent-Han |
| 017 (50018) | collectionName 空串 | **TP_ACK_CLOSED** | yanliang567 "not a big problem, could make an improvement"（弱 ACK） |
| 011 (49844) | null/missing filter 静默返回全部 | **FP_BY_DESIGN** | — |
| 027 (50351) | shardsNum=0/-1/65535 接受 | **FP_BY_DESIGN** | — |
| 028 (50352) | metricType=""/consistencyLevel="None" 接受 | **FP_BY_DESIGN** | — |

**同为"空字符串参数被接受"，dbName 空串=TP 而 metricType 空串=BY_DESIGN**。
任何满足条件 3（不点名字段）的措辞都无法同时翻正 009/012/017 而不卷翻 011/027/028——
锚点集合在数学上不可全翻正（条件 2 的教科书案例）。

### E 类：同一维护者方向分裂
- 9017（hnsw_ef=0 静默回退默认）：timvisee (MEMBER) "**Fixed via** https://github.com/qdrant/qdrant/pull/9320"
- 9027（score_threshold 超 [0,1] 静默接受）：timvisee (MEMBER) "we choose to not set any search
  threshold limits. The user is responsible... **I hope I explained we don't see this as a problem**"

两个都是"无效输入值被静默接受"，同一维护者、两个方向。qdrant 的校验态度是
**per-parameter** 的，不存在现象类级准绳。

### A 类：态度温和 + 修复死链
- 49059 本体：xiaofan-luan (COLLABORATOR) "This is a good suggestion" + assign 流程 = 温和 ACK
- 社区修复 PR 49264（"fix: precision > 1 in similarity search with COSINE metric"）：**未获
  review，被 stale[bot] 关闭**——TP_ACK_CLOSED_NOFIX 的"NOFIX"是真实的
- 48204（FLAT/HNSW cosine 差异）：yanliang567 "I think this is **kind of expected**" + foxspy RCA
  （SIMD 浮点差异）——轻度反向
- 32262（负距离）：多名维护者调查无结论，stale 关闭
- 52338（负自相似度）：有 RCA，open 未修

### F 类：同意但未落地
timvisee "I agree this is a reasonable suggestion. I like HTTP 405" —— 但 fix PR 9442 至今
open/未合并，qdrant 无第二例错误码修正。单行为 + 孤链。

**结构规律（论文论点）**：FN 信息可达性取决于维护者态度在历史中的**收敛程度**——
错误码语义在 weaviate 历史强收敛（批量修复 PR），文档一致性在 milvus 强收敛（docs PR 流程）；
参数校验态度在 milvus/qdrant 内部按参数逐个分裂。锚点三条件不是形式主义，它精确划出了
"态度可泛化"与"态度分裂"的边界。

## 2. 可注入锚点草案（fixG）

### 锚点 C（milvus intel）：文档-行为一致性裁决

**支撑证据链（3 独立行为，全部修复方向）**：
1. **50355**（=milvus_031 本体）：yanliang567 实测确认 autoID upsert 行为后，开 docs PR
   [3513](https://github.com/milvus-io/milvus-docs/pull/3513) + 3514（v2.6.x 与 v3.0.x 双分支）
   修正文档——处置 = 修文档使与行为一致
2. **46683**：xiaofan-luan "I think you are right" + AnthonyTsu1984 "The fix has already been
   merged"（milvus-docs PR 3402，dynamic field upsert 示例文档不符）
3. **46494**：foxspy "fixed" 并关闭（nbits 文档范围与行为不符）

**反向检查**：milvus 历史上文档类报告（43159/40064/39607/41748）全部以修复/更新处理关闭，
无"文档-行为不一致不算 bug"表态。50324（milvus_025）为伪案例——报告者自证 v2 文档并无
100 上限（看错 v1 旧文档）后撤回，维护者 yanliang567 的表态"sounds like a document issue"
反而是修复方向的。

**措辞草案**（满足条件 3，不点名 upsert/autoID/nbits）：
> Documentation-behavior consistency: when official documentation claims a behavior or
> capability that the server does not exhibit (documented X, actual behavior is not-X),
> this is a consistency defect — maintainers' repeated disposition is to fix it (usually by
> correcting the docs to match verified behavior: docs PRs #3402, #3513/#3514; issue #46494
> "fixed"). "The behavior looks reasonable on its own" does not neutralize a documented
> claim that contradicts it.

**预期作用面**：milvus_031（判词明引契约却无视"documentation claiming support"的冲突）。
潜在误伤面：milvus_025（FP）——但 025 现象是"报告者声称文档说 X"，实测文档**没有**说 X，
锚点要求"documented claim 实际存在"，reviewer 核对文档后不会启用；仍列为对照重点。

### 锚点 G（weaviate intel）：错误码语义裁决

**支撑证据链（≥3 merged 修复 + 1 MEMBER 表态，全部同向）**：
1. **12049** (MERGED, dirkkul)：gh-12041 batch delete 缺 match 字段 500→**422**（=weaviate_010 本体修复）
2. **12040** (MERGED, jfrancoa)：non-existing index 500→**404**（"returns 404, not 500"）
3. **11878** (MERGED, dirkkul)："**Fix more error codes in REST handler**"——批量错误码修正
4. **12262**：etiennedi (MEMBER) 多轮 QA +1（reindex 竞态 500→202 NO_OP；open）
5. 11661/11712（limit 超限 500→422，issue+PR 成对，open）——同向待落地

**反向检查**：weaviate 历史无"5xx 用于请求侧错误是 by-design"表态；12262/11661 等 open PR
全部是继续收紧方向。

**措辞草案**（满足条件 3，不点名 batch delete/cluster）：
> HTTP status-code semantics: server-side 5xx responses to request-side detectable errors
> (invalid/missing parameters, non-existent resources, mode-inapplicable operations) are
> treated as defects by maintainers and repeatedly fixed (500→422 #12049, 500→404 #12040,
> batch REST handler error-code fixes #11878, 500→202 with maintainer +1 #12262). 5xx is
> reserved for genuine internal failures; "the validation exists and the message is clear"
> does not make a 5xx status correct.

**预期作用面**：weaviate_010（判词原话"HTTP 500 状态码选择可能值得 UX 讨论，但并非功能性
缺陷"——锚点直接裁决该论证）。潜在误伤面：weaviate_009（11981，FP，现象是空数组被 200
接受——非 5xx 现象，锚点条件不满足，理论不卷入；仍列为对照）。

## 3. 预注册试验设计（fixG，待用户拍板）

- 干预：C 锚点注入 milvus intel + G 锚点注入 weaviate intel（脚本注入，双处顶层+内层，
  备份+MATERIAL_FIXES 留痕，audit 0 FAIL——同 fixD 模式）。
- 子集：**适用 2**（milvus_031、weaviate_010）+ **形态近邻对照 2**（milvus_025、weaviate_009）
  + **稳定对照 4**（每 vendor 取 fixA 三轮全一致 case：如 milvus_004/013、weaviate_002/005，
  实际选择时从三轮一致表挑）= 8 case 单轮。
- 判据（预注册）：
  - 适用 2 全翻正 → 锚点保留；
  - 近邻对照 2 任一翻错（025/009 由对变错）→ 字面 FAIL，判词级因果检查后处置；
  - 稳定对照 4 任一翻错 → 轮方差核查（同 fixD 015 先例）。
- 披露义务：C/G 锚点为 GT-informed 注入（本体 case 行为计入支撑）+ 外部独立行为补充；
  措辞为现象类普适（不含字段/端点名）——论文披露注入方式与三条件检验过程。
- fixG 结果并入最终配置后再跑 fixF 全量快照（fixF 的"最终配置"相应更新）。

## 4. 调查原始数据清单（raw/）

本体 dump：milvus 49059/49889/50018/50355/50324；qdrant 9017/9027/9421；weaviate 12041
候选 dump：milvus 49264/48204/32262/52338/46683/46494；qdrant 9142/9553/9442；
weaviate 12049/12040/11878/11712/12262/11661/5556
检索日志：_search_round1.json（10 查询）、_search_reverse.json（4 反向查询）

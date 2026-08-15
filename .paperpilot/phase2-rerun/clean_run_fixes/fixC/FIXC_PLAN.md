# fixC 预注册计划：证据冲突消解次序显式化（evidence hierarchy explicitization）

> 日期：2026-08-15。Run 标识：**fixC**。干预载体 = **SOP 文件**（testvdb4exp/agents/dev-reviewer.md），
> 派发 prompt 零改动（reviewer 自行读 SOP 即携带新规则）。备份：`dev-reviewer.md.pre-fixC.bak`。

## 1. 动机（来自三轮 fixA 数据的发现）

SOP 有**名义**优先级（视角 A 契约"ground truth 不允许推翻"压倒 C），但：
(a) 可推翻 A 的例外条款模糊（"maintainer 陈述"未定义清单）——run2 多份判词用源码注释违反 SOP 推翻 A
（如 milvus_023），run3 同 case 又按 SOP 判 CONFIRMED——**同对材料、相反消解方向**；
(b) "显式 by-design 证据"认定标准松——无声实现（cast.ToBoolE/json.Unmarshal 直转）被算作 by-design，
而 4 个 FIXED_PR 恰是维护者修掉的无声实现。

32 个三轮 SPLIT case 即此空隙的产物（fixA 三轮多数投票对 21 / 错 11；顽固错 0）。

## 2. 干预内容（SOP patch，三处）

1. **视角 A 例外清单化**：可推翻 verdict_A=CONFIRMED 的证据类型完整清单 = E3/E4，其余（无声实现、
   行为优雅、"源码就这么写的"）一律不可。
2. **新增"证据冲突消解次序"节**（聚合规则前，条件互斥、自上而下）：
   - E1 现场实测 > 历史 raw log（工程规则，非维护者行为泛化——来源如实标注）
   - E2 REST v2 与 gRPC 通道不一致 → CONFIRMED（泛化自 4 个 FIXED_PR，即 fixA 锚点制度化）
   - E3 源码显式意图声明（意图注释/专用命名常量）> 契约 → FALSE_POSITIVE
     （泛化自幂等 create/drop 的 errIgnored* + 注释、SetDefaults，GT 均 BY_DESIGN）
   - E4 认知信号标注 → 按标注方向（泛化自 qdrant HNSW should_report:false）
   - E5 兜底：A=NEUTRAL + B=NEUTRAL + 无 E2/E3/E4 → FALSE_POSITIVE（保守）
3. **视角 C 认定收紧**："显式 by-design"必须为意图注释/专用命名常量，无声实现不算。

**锚点三条件自检**：E2 已验证（fixA 10:3）；E3 在现有 GT 上无反例（FIXED_PR 四例均无声实现），
但支撑样本（≈5 个 BY_DESIGN case）少于 E2；E1 为工程规则、非维护者行为——**已知风险**：
milvus_041 型（实测与 log 冲突、GT=CONFIRMED）会被 E1 推向 FP 错向。

## 3. 子集（38 case，预注册固定）

- **SPLIT 32 全量**（三轮非全一致）：milvus 21（002/004/005/006/007/009/013/016/021/023/024/025/
  028/029/030/032/033/038/039/040/041/042）、qdrant 7（003/004/007/009/010/011/012）、
  weaviate 3（004/006/008）
- **对照 6**（三轮稳定对、灰区敏感类，防止新表劣化稳定项）：milvus_022（幂等 create，E3 类）、
  milvus_035（Int64 强转，E2 类）、milvus_043（strictGroupSize）、qdrant_002（hnsw_ef by-design）、
  qdrant_017（HNSW 分页，E4 类）、weaviate_001

**已知 caveat**：SPLIT 子集 GT=C 占比偏高（~14/32），E5 保守兜底在此子集结构性占优（选择效应），
全量外推需全量轮——本试验只回答"消解次序能否消除漂移 + 是否引入系统性错向"。

## 4. 预注册判据（跑前固定，不可事后改）

- **主指标**：SPLIT 32 上 fixC vs {fixA-r1, r2, r3} 的 κ 中位 ≥ **0.60**
  （对照：fixA 轮间 κ 0.352-0.492，中位 0.354）
- **次指标**：SPLIT 32 上 fixC 对错数 vs 三轮多数投票的 21/32；对照 6 全对
- **判据三支**：
  1. **采纳**（保留 SOP patch）：κ 中位 ≥0.60 且 SPLIT 对错 ≥21/32 且对照 6/6 → 进入全量验证（另行决定）
  2. **负结果**（回滚，记录发现）：κ 中位 ≥0.60 但 SPLIT 对错 <21/32 →
     结论"结构化 rubric 消除方差的同时在灰区固化为系统性偏差"
  3. **无效**（回滚）：κ 中位 <0.60 → 显式化本身不足以稳定消解
- 回滚动作：`cp dev-reviewer.md.pre-fixC.bak` 恢复 + 本文件记录

## 5. 纪律

- 派发 prompt = clean_run/prompts/ 原文（零改动，无 §3.2 风险）；每 case 新会话；
  同容器串行/异容器并行；判词校验+归档走 archive_verdict.py；VOID_LOG 留痕；audit 0 FAIL。
- **披露义务**：E2-E4 从维护者公开行为泛化（GT-informed），论文使用须披露 SOP 干预方式与依据。

## 6. 预判（跑前写定，供事后核对）

κ 中位 ≥0.6（规则消解的确定性）；SPLIT 对错 ≈19-24（E5 兜底在 GT=C 富集子集占优，但 E1/E3 边界
误伤 milvus_024/028/041 等 2-3 个）；对照 5-6/6。最可能落在判据 1 与 2 的边界——若 <21 则为负结果
（与"方差→偏差"预判一致）。

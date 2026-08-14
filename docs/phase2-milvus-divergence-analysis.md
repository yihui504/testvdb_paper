# Phase 2 milvus 板块分歧根因分析

> 日期：2026-08-15。对象：clean_run 中 milvus 43 case 的 24 个分歧 case（正确率 0.44，
> 对照 qdrant 0.72 / weaviate 0.70）。方法：24 份 clean 判词 root_cause/三视角路径/源码接地的
> 逐份提取 + GT 依据（gt_category）对照 + 历史三轮同 case 论证对照 + 三 vendor intelligence
> 态度信号丰富度对照。数据：`clean_run/verdicts/milvus/`、`clean_run/CLEAN_RUN_RESULTS.json`。

## 0. 结论（一句话）

milvus 板块分歧率高的根本原因是**四层因素叠加**：样本现象集中在 REST v2 包装层的语义灰区（层1），
GT 判据是"维护者事后态度"而 reviewer 判据是"源码显式实现"启发式、两者系统性错位（层2），
三视角聚合在灰区退化为视角 C 自由裁量（层3），而 milvus intelligence 态度信号近乎为零、
C 无锚点（层4）——于是同一源码行在不同轮次被论证出相反结论。

## 1. 现象盘点

43 case：对 19、错 24（其中 milvus_001 为空日志已知例外，非语义分歧）→ **真语义分歧 23**：

- **FN 15**（GT=CONFIRMED 判 FP）：root_cause 分布 = mundane_api_semantics ×10、
  contract_misread ×3、by_design_type_coercion ×1、rest_api_parameter_silent_ignore ×1
- **FP 8**（GT=FP 判 CONFIRMED）：全部引契约违反/缺校验为据

## 2. 根因分层

### 层 1 — 样本结构：24 个分歧全部落在 REST v2 包装层"宽松接受"灰区

| 现象簇 | case | 特征 |
|--------|------|------|
| type coercion | 52308/52310/52312/52314/52315（全 FN） | REST 接受字符串标量/字符串向量，源码 `cast.ToBoolE`/`json.Number().Int64()`/`json.Unmarshal` 显式转换 |
| 参数静默忽略/宽松接受 | FN: 47763/49889/49890/50018/50353；FP: 49844/50324/50351/50352 | 空 optional 参数、非法值静默回退默认——**同簇现象 GT 分裂：4 个 ACK、5 个 BY_DESIGN** |
| 幂等/成功码 | FP: 50321/50322；FN: 47755/50323 | 幂等 create/drop 返回 200、互斥参数并存静默取一 |
| 一致性/精度/时序 | 47635/49059/50193/50194 | rowCount 时延、COSINE 精度、stale 读 |
| upsert 语义/字段类型 | 50355/52311（均 FN，A 组 FIXED_PR） | autoID upsert、group_by vector 字段 |

这些现象的共同点：**行为优雅、源码显式、契约模糊或缺席**——没有客观判据可锚定。
qdrant/weaviate 的样本更多落在"客观可判"现象（维度不匹配 422、枚举违约），分歧率自然低。

### 层 2 — 判据错位：GT = 维护者事后态度 vs reviewer = 源码显式启发式

15 个 FN 的 GT 依据**全部**是维护者承认（TP_ACK ×11 / TP_DUP_TRACKED ×3）或修复（TP_FIXED_PR ×4：49890/50355/52311/52315）。
其中 4 个 FIXED_PR 意味着**维护者修掉了自己显式写下的代码**——"源码里写了 = by-design"启发式
在这些 case 上被 GT 直接证伪。clean 判词的典型论证（52315）：

> "源码 utils.go:548 使用 json.Unmarshal 处理 FloatVector……这是 API 设计的灵活性(by-design)"

而 GT 的真实依据（issue 标题明写）："gRPC rejects"——**维护者的判据是 REST v2 与 gRPC 行为一致性**。
这个客观判据 reviewer 没有执行，SOP 也没有这个步骤，intelligence 里也不存在。

反向 8 个 FP 与 FN 同现象带（幂等 create/drop、shardsNum/metricType 静默），GT 却标 BY_DESIGN
——GT 自身对同类现象态度分裂，两类在 reviewer 的判据空间里不可区分，**必然一半错**。

### 层 3 — 裁决机制：三视角在灰区退化为视角 C 自由裁量

15 份 FN 判词的三视角路径：

- **A=NEUTRAL + B=NEUTRAL → C 全权决定 ×8**（004/013/035/037/041/042 及近似）
- A 或 B 直接 REFUTED ×2（005/029）
- **未写三视角字段（SOP 执行衰减）×7**（008/012/017/024/031/038/039——root_cause 仍自洽，但聚合过程缺失）

视角 C 的判据 = "行为优雅 + 源码显式 = by-design"，在层 2 的错位下系统性偏向 REFUTED。

### 层 4 — 锚点缺失：milvus intelligence 态度信号近乎为零

| vendor | by_design | not_bugs | blindspots | clean 正确率 |
|--------|-----------|----------|------------|--------------|
| qdrant | 2 | 0 | **10**（含"Parameter validation on filter/condition APIs"疑 bug 锚点） | 0.72 |
| weaviate | 0 | 0 | 0 | 0.70 |
| milvus | 2（均与 REST v2 无关：Storage V3 snapshot / rollback） | 0 | **0** | **0.44** |

qdrant reviewer 判 9373/9523 FP 时直接引用了 by_design pattern（"HNSW approximation duplicates,
should_report: false"）——有锚点。milvus reviewer 面对灰区时**没有任何维护者态度先验**，
视角 C 只能靠模型直觉。weaviate intel 也空但正确率高，佐证层 4 是放大器而非独立成因：
**灰区 case 多（层1）× 态度锚点空（层4）** 才是 milvus 独有的双重命中。

## 3. 微观实证：同一源码行，四轮相反结论

| case | 源码证据 | run1 | run2 | run3 | clean | GT |
|------|---------|------|------|------|-------|----|
| 52315 vector 字符串 | utils.go json.Unmarshal（**同一处**） | C | C | C | **F**(by-design) | FIXED_PR |
| 52308 Int64 字符串 | utils.go json.Number().Int64() | C | F | C | **F**(mundane) | DUP |
| 50321 幂等 create | create_collection_task.go errIgnored | F(幂等设计) | C | C | **C**(契约压倒) | BY_DESIGN |
| 49890 超时头 | timeout_middleware.go 静默忽略 | C | F* | F* | **F**(by-design) | FIXED_PR |

（*run2/run3 的 rationale 实际在讲 dimension 校验——历史轮 endpoint 错配时期产物）

"源码显式转换"在 run1 被解读为缺陷（"未检查 fieldValue.Type"）、在 clean 被解读为 by-design
（"有意的设计灵活性"）；幂等在 run1/clean-50192 被解读为"分布式标准设计"、在 run2/run3/clean-50321
被"契约压倒"。**判词的源码接地质量四轮都在（551-989 字符 excerpt），分歧不在证据在解读。**

## 4. 可操作结论

1. **intelligence 补态度锚点（最高杠杆）**：把 GT 侧维护者的真实判据写进 milvus
   `developer_cognition.blindspot_indicators`——"REST v2 与 gRPC 行为不一致 → 疑 bug"
   （52308/52312/52315 的 GT 依据全是它）。真实 TestVDB 流程中该信号来自维护者历史 issue，
   补齐是贴近真实形态而非注入特权信息。
2. **SOP 加 REST/gRPC 双通道对照步骤**：对 REST v2 候选，证伪阶段显式检查 gRPC 端行为是否相反
   （现 SOP 第 4 步只有"独立通道取证"且未点名此对照）。
3. **视角 C 判据收紧**："源码显式实现"不得单独构成 by_design 证据（TP_FIXED_PR 4 例证伪了
   该启发式），需引用 maintainer 文档/commit/issue 态度。
4. **论文层面**：23 个语义分歧 case + 四轮同源码行相反结论，是"LLM-as-dev-judge 在语义灰区
   缺乏态度锚点"的直接论据——支持 RQ2 的"判定语义欠定性"论点，也解释了 κ 0.30-0.38 的微观来源。

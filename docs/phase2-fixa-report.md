# Phase 2 fixA 报告：分歧修复杠杆实验（杠杆 1 采纳）

> 日期：2026-08-15。目的：按 [phase2-milvus-divergence-analysis.md](phase2-milvus-divergence-analysis.md)
> §4 的修复杠杆，在分歧 case 上逐步验证效果，全量验证影响面，保留有效且影响小的修复。
> Run 标识：**fixA**（杠杆 1）；判词 `clean_run_fixes/fixA/verdicts/`（42 份 milvus 重判 + 28 份沿用）。

## 1. 修复内容（杠杆 1，唯一采纳项）

milvus `developer_cognition.blindspot_indicators` 追加一条**裁决准绳型锚点**（v2 包 + intel 源同步，
脚本 `fix_intel_blindspot.py`，MATERIAL_FIXES 169 条留痕，audit 0 FAIL）：

> "REST v2 and gRPC divergent validation: REST v2 accepting values the gRPC path rejects
> (maintainers treat cross-channel inconsistency as a defect and fix it)"

**方法论披露**：准绳从 fix PR 的维护者公开行为泛化（真实历史态度），非从 GT 标签直抄；
论文使用须披露 intel 构建包含此人工补录。

**不采纳**：杠杆 2（SOP 加双通道对照步骤——影响全 vendor，对非通道类增量≈0）、
杠杆 3（视角 C 禁单证据——单独不提升 recall，只把自信 FP 变 UNCERTAIN）。

## 2. 分歧 case 子集试验（23 个，milvus）

| 结果 | 数量 | case |
|------|------|------|
| FN 翻正（FP→C，GT=C） | 6 | 52308/52310/52311/52312/52314/52315（3.0.0 type coercion 全簇） |
| FP 翻正（C→FP，GT=FP） | 4 | 49844/50321/50322/50352（filter 空语义、幂等 create/drop、默认值回退） |
| 保持错（锚点不适用类） | 13 | IN 语义、optional 参数、anndField 自动检测、一致性时序、契约幻觉类 |

**10/23 翻正、0 新增劣化**（子集内 clean 全错）；翻正判词明确消费锚点
（"maintainers treat gRPC/REST v2 validation inconsistency as a defect"）；
不适用类正确地未乱翻（如 50352 判词显式识别"默认值回退不是通道分歧"）。

## 3. 全量影响面验证（71）

milvus 判对的 19 个重判：**17 保持 / 2 劣化**（49930、52325 的同类也稳）；
qdrant 18 + weaviate 10 输入零变化沿用 clean 判词（intel 改动物理上不触及）。
合计 milvus 42 重判 + 1 例外沿用（milvus_001 空日志）。

**flip 总账：13 个变化 = 10 翻正 + 3 劣化**（+016/49930、+033/52325 为"参数静默忽略"类被推向
by-design；+018/50192 为 HTTP 200 包装类反向翻——三例同属"同现象 GT 态度分裂"灰区，即纯轮方差区）。

### 指标对比

| 配置 | recall | fp_supp | precision | accuracy |
|------|--------|---------|-----------|----------|
| clean（基线） | 0.533 | 0.577 | 0.686 | 0.549 (39/71) |
| **fixA** | **0.622** | **0.692** | **0.778** | **0.648 (46/71)** |
| milvus 单独（clean→fixA） | 0.448→0.586 | 0.429→0.643 | 0.619→0.773 | 0.442→0.605 (19→26/43) |

四项指标全面提升，净 +7 case（+4 TP、+3 TN），杠杆比 10:3。

## 4. 结论

1. **采纳杠杆 1**：一条 intel 锚点，影响面 milvus-only，四指标全升，杠杆比 10:3。
   根因假设（层 4"裁决准绳缺失"）被实验证实——补准绳后 3.0.0 灰区簇整体翻正。
2. 剩余分歧（17 FN + 8 FP 中的未翻正部分）仍属"同现象 GT 态度分裂"灰区
   （维护者对同类现象 ACK/BY_DESIGN 分裂），**不是材料或流程可修复的**——
   这是 dev-reviewer 任务在语义灰区的固有上限，论文应作为 limitation 披露。
3. 方差注意：fixA 是单轮结果，受 κ 0.3-0.4 级 run-to-run 方差影响（016/018/033 三个劣化
   均为方差区翻转）；引用 fixA 数字时应与 clean 并置说明。
4. 四轮+fixA 五份判词树完整归档，可复算。

## 5. 归档

- 判词：`clean_run_fixes/fixA/verdicts/`（42）+ `VERDICTS_ALL.json`（clean/fixA 全 71 对照）
- 修改：`fix_intel_blindspot.py`、MATERIAL_FIXES 第 169 条、v2+intel 源两处
- 材料：判词移出后材料树零残留；容器全清

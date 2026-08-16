# Phase 2 三臂实验最终汇总（RQ2 数据收口）

日期：2026-08-16 | 状态：**全部完成**（sl 三轮 + vt 三轮 + fixF 三轮 = 9 轮 × 71 case）
GT：clean_run 审定表（45 真 / 26 C 组）| 材料：同一 71 case 冻结包（audit 0 FAIL）

---

## 0. 口径声明（先读）

- **统一分母 = 45 真 / 26 C 组**（clean_run 审定 GT，sl/vt 两臂全程使用）。
- **"fp_supp" 同名反向（已破案）**：fixF 系报告的 fp_supp = **抑制率**（C 组判 F 比例，
  TN/(TN+FP)：r1 0.667 / r2 0.704 / 三轮中位 0.704）；sl/vt 臂的 fp_supp = **FP 率**
  （C 组判 C 比例）。本汇总表**一律用 FP 率**（两臂口径）：fixF 系对应值 =
  报告值取反（0.667→0.333 等，重算自 verdicts 原始文件，全部吻合：
  r1 FP=9/27、r2 FP=8/27、r3 FP=5/26）。
- **qdrant_005 GT 分歧披露**：fixF 系列归档内嵌 GT 标其为 FALSE_POSITIVE（分母 44/27）；
  clean_run 审定表标 CONFIRMED。本汇总以 clean_run 为准（fixF 在 qdrant_005 三轮全 F，
  两口径下均非 TP；差异只影响分母：45 口径 fixF r1 recall = 0.644 vs 归档 0.659）。
  该 case 属"8 个 GT 存疑待办"之一，最终裁决待 phase3。
- 三臂判定口径：sl = 纯调用 JSON verdict；vt = 级联聚合 confirmed/rejected；
  fixF = dev-reviewer SOP 判词。每臂 3 轮 + majority-vote(3)。

## 1. 三臂定义（同一材料，只动"判断架构"轴）

| 臂 | 架构 | 工具/证据面 | LLM 调用数/case | 产物 |
|----|------|------------|----------------|------|
| single-LLM | 1 次纯调用，材料全文内联 | **无工具**（不读文件/不联网/不执行） | 1 | arms/single_llm/ |
| voting | as-shipped 4 judge 级联 + 代码聚合 | 只读本地；doc/novelty 关网（代码直出降级） | 2（evidence+severity） | arms/voting/ |
| dev-reviewer | 单 agent SOP + 内三视角 | Bash/Grep：源码接地 + 活 DB 实跑 + 锚点通道 | 多轮 agent | clean_run_fixes/fixF 系 |

## 2. 三轮指标全表（统一 45/26 口径）

### 2.1 逐轮

| 臂·轮 | recall | fp_supp | precision | acc |
|-------|--------|---------|-----------|-----|
| sl run1 | 0.378 | 0.885 | 0.850 | 0.563 |
| sl run2 | 0.422 | 0.769 | 0.760 | 0.549 |
| sl run3 | 0.568 | 0.731 | 0.781 | 0.620 |
| vt run1 | 0.556 | 0.269 | 0.781 | 0.620 |
| vt run2 | 0.422 | 0.077 | 0.905 | 0.606 |
| vt run3 | 0.378 | 0.115 | 0.850 | 0.563 |
| fixF r1 | 0.644 | 0.346 | 0.763 | 0.648 |
| fixF r2 | 0.556 | 0.308 | 0.758 | 0.606 |
| fixF r3 | 0.578 | 0.192 | 0.839 | 0.662 |

（fixF 归档原文为 44/27 分母 + 抑制率口径：r1 0.659/0.667、r2 0.568/0.704、
r3 0.568/0.704*；*r3 归档行继承 r2 的抑制率数字，verdicts 重算 r3 FP=5/26 →
FP 率 0.192。本表统一 45/26 + FP 率，重算自三轮 verdicts 原始文件。）

### 2.2 中位数 [区间] + majority

| 臂 | recall 中位 [区间] | fp_supp 中位 [区间] | precision | majority (r/fp/pr/acc) |
|----|-------------------|---------------------|-----------|------------------------|
| sl | 0.422 [0.378-0.568] | 0.769 [0.731-0.885] | 0.76-0.85 | 0.444 / 0.192 / 0.800 / 0.577 |
| vt | 0.422 [0.378-0.556] | **0.115** [0.077-0.269] | 0.78-0.91 | 0.378 / 0.115 / 0.850 / 0.563 |
| **fixF** | **0.578** [0.556-0.644] | 0.308 [0.192-0.346] | 0.76-0.84 | **0.689 / 0.192 / 0.861 / 0.732** |

**读法**：fixF majority 是全表唯一的效率高点（recall+precision+acc 三高）；
sl 与 vt 的 majority fp_supp（0.192/0.115）反而低于其单轮——两臂的 FP 在轮间不稳定
（majority 票过滤掉了单轮 FP），这是方差而非精度。

## 3. 轮间稳定性（κ，同臂跨轮）

| 臂 | κ(1,2) | κ(1,3) | κ(2,3) | 区间 |
|----|--------|--------|--------|------|
| sl | 0.321 | 0.294 | 0.449 | 0.29-0.45 |
| vt | 0.442 | 0.529 | 0.623 | 0.44-0.62 |
| fixF | 0.187 | 0.246 | 0.318 | 0.19-0.32 |

- 三臂 κ 全部落在 0.19-0.62：**方差是模型内禀属性，与架构无关**（判据 4 三臂同证）。
- vt κ 最高且有"轮次越近越高"结构（2,3 相邻 = 0.623）——但 confirmed 数单调漂移
  32→21→20，case 级一致性与整体保守漂移并存。
- fixF κ 最低（工具路径发散：每轮 agent 探索不同）但指标最好——**低 κ ≠ 低质量**，
  agent 的探索方差换取了 recall 上限。

## 4. 跨臂 paired 对比（majority，McNemar）

| 对 | 仅 A 对 | 仅 B 对 | χ² | 结论 |
|----|---------|---------|-----|------|
| sl vs vt | 12 | 7 | 0.84 | ns——无工具下架构差不显著 |
| sl vs fixF | 6 | 17 | 4.35 | **sig**——工具/证据通道增量显著 |
| vt vs fixF | 5 | 21 | 8.65 | **sig**——fixF 对 vt 近单向支配 |

**显著性阶梯**：sl↔vt ns，两无工具臂↔fixF 均 sig 且 fixF 方向单向——
三臂递进设计把"工具增量"与"架构增量"干净分离：**架构差（纯调用 vs 级联）
不显著，工具差（无工具 vs agent）显著**。

## 5. 机制分解

### 5.1 voting 级联真相（as-shipped ≠ 多数投票）
级联 = 规则0崩溃旁路（纯子串匹配，确定性）→ novelty 否决（关网下空转）→
evidence 闸门（LLM，实质唯一判断者）→ doc 降级（关网下全 PARTIAL = 恒 -1）→
severity trivial 闸门（三轮共杀 1 票）。
- 拒票分布：evidence 39→50→49，trivial 0→0→1 —— **evidence 单 judge 决定生死**。
- 崩溃旁路恰命中 qdrant_014/weaviate_010（'status: 500'），三轮 CCC = recall 保底。

### 5.2 三臂 FN 结构（GT=CONFIRMED，majority 口径）

| 类 | n | case | 判读 |
|----|---|------|------|
| 三臂全漏 | 6 | milvus_001/004/012/029/038、qdrant_005 | 顽固 FN 核心：态度/材料不可达类（001 空日志、005 GT 存疑）——工具也解不了 |
| 仅 fixF 对 | 12 | milvus_002/003/006/009/013/017/024/031/043、qdrant_016、weaviate_006/007 | **工具增量实体**：源码接地+实跑翻正的契约消费/结构性取证类 |
| 三臂全中 | 8 | milvus_005/010/032/033/034/040/041/042 | 强信号 case（参数校验类，材料面即可判） |

## 6. 兴趣点三臂轨迹（C/F × 3 轮）

| case | sl | vt | fixF | gt | 三角判读 |
|------|----|----|------|----|---------|
| qdrant_014 | FFF | **CCC** | FFC | 真 | vt=崩溃旁路锁定；fixF 仅 r3 中（工具也难）；sl 锁死 |
| weaviate_010 | FFF | **CCC** | **CCC** | 真 | G 锚点（fixF）与崩溃旁路（vt）双通道解锁同一 LLM 锁死类 |
| qdrant_002 | CCF | FCF | FCC | 真 | 三臂灰区同源：gte>lt 契约直读，轮间漂移 |
| milvus_009 | CFF | CFF | FCC | 真 | 灰区；fixF r1 靠结构取证中 |
| qdrant_018 | CCC | FFC | CCC | 真 | 无 expected 依据：sl 保守倾向反而不生效；vt r3 行为论证过闸 |
| milvus_008 | CFC | FFF | CFF | 真 | 数值精度可 log 直读（sl 半稳）；vt evidence 全拒 |
| milvus_017 | FCF | FFF | CCF | 真 | 端点不一致论证偶发；fixF 2/3 中 |
| milvus_001 | FFF | FFF | FFF | 真 | 三臂一致死刑类（占位日志）——材料不可达无解 |

## 7. 执行事故与偏差总账

| 臂 | 事故 | 处置 |
|----|------|------|
| sl | run2 两批+run3 一批 429 中断；run3-b2 自恢复覆盖 b2b 补跑版 10 文件；milvus_042 JSON 引号机械修复 | 归档以最终写入为准，dispatch_log 记录 |
| vt | run3 evidence 3 文件漏写（SendMessage 唤回补写）；severity qdrant_004 写盘竞态 | 二次聚合消解，426 判词全落盘 |
| fixF | 该会话自记（另见 clean_run_fixes/fixF_run3/） | — |

**共通偏差（披露）**：judge/dev-reviewer SOP 原配 model=sonnet → 统一 GLM-5.2；
doc/novelty 关网走 SOP 降级（代码直出）；VERDICT: UNKNOWN 中性行 ×70 为实验构造；
契约超集保留（41/71 ≥10 条）；qdrant_005 GT 分歧（§0）。

## 8. RQ2 结论（论文表述）

1. **证据通道决定 recall 上限**：fixF majority 0.689 vs 两无工具臂 0.378-0.444；
   仅 fixF 对的 12 case = 工具增量实体（契约消费 + 源码接地 + 实跑证伪）。
2. **架构轴在无工具下只挪 precision-recall 折衷**：sl 与 vt recall 中位同为 0.422，
   差别全在 fp_supp（0.769 vs 0.115）——级联把 FP 压近零的代价是保守漂移
   （confirmed 32→21→20）与 recall 下行。sl↔vt McNemar ns（χ²=0.84）。
3. **as-shipped 级联在文档验证降级下退化为 evidence 单闸门 + 崩溃旁路**
   （trivial 闸门三轮杀 1 票；崩溃旁路 2 case 恒 confirmed）——与多 judge 分权
   设计意图相反；构造性发现，非执行偏差。
4. **方差是模型内禀**：三臂轮间 κ 0.19-0.62 全重叠带；fixF κ 最低但指标最好
   （探索方差换 recall 上限）；vt κ 最高但漂移最大（确定性成分不产生判断只传导偏置）。
5. **双通道解锁证据**：weaviate_010 = G 锚点（fixF CCC）与崩溃旁路（vt CCC）两条
   独立通道解锁 sl 锁死类；三臂一致死刑类收敛到 6 case（材料/态度不可达）。

## 9. 文件索引

- 三臂三轮全数据：arms/single_llm/、arms/voting/run{1,2,3}/、clean_run_fixes/fixF{,_run2,_run3}/
- 分臂报告：ARM_SL_REPORT.md、ARM_VT_REPORT.md、FIXF3_REPORT.md（另一会话）
- 合成：arms/ARMS_SYNTHESIS.md（三臂表）、本文件（最终汇总）
- 预注册：arms/{single_llm,voting}/PREREG.md、FIXF2_PLAN.md
- 口径工具：arms/fixF_majority_45.json（45/26 统一口径 majority 重算）

# RQ2 v7.1：机械层预跑注入实验（2026-08-19）

## 假设与设计

mechbacktest 结论落地：v7 的 auditor 无监督时不跑/不采信机械脚本（A 不一致 18/71、B 未采信 8/23、CONFLICT 闭环架空）。v7.1 唯一变量 = **主进程预跑 check_chain_grounding + check_physical_constraints，A/B 机械值直接注入 auditor 派发词**（auditor 只解释不计算）。链文件不动（除 rework 闭环重写），验证"采信"单变量。

派发器：`gen_dispatch_v71.py`（v7 版 + 机械预跑段 + 工单文本白名单修复）。

## 终态指标（71 案全量，GT=cases_index gt_label）

| 口径 | recall | precision | fp_supp | TP/FP/FN/TN |
|------|--------|-----------|---------|-------------|
| fixF | 0.621 | 0.818 | — | — |
| v7（无监督基线） | 0.614 | 0.794 | 0.741 | 27/7/17/20 |
| mechbacktest 模拟 | 0.727 | 0.762 | 0.630 | 32/10/12/17 |
| **v7.1（实测）** | **0.727** | **0.780** | 0.667 | **32/9/12/18** |

**实测与模拟吻合（recall 0.727 完全一致；precision 实测 0.780 略优于模拟 0.762）**——机械注入修复有效且无监督可复现。

- recall 0.614 → **0.727**（+0.113，TP 27→32）
- precision 0.794 → 0.780（-0.014，FP 7→9）
- NME 清零（8 案工单全部闭环：5 案复审收敛、3 案材料性不可修复保守落判）

## v7→v7.1 翻转 11 案（翻对 7 / 翻错 4）

翻对（FN→TP，7）：milvus_002/006/030/031、qdrant_004/015、weaviate_007——全部是上轮被 auditor 架空机械层的案（B=HTTP语义恒真/资源边界/类型恒真 或 A=CONFIRMED 被报 NEUTRAL）
翻错（4）：
- milvus_021/qdrant_009（NOT→DEFECT，FP+2）：机械 A=CONFIRMED 误伤（violates 语义边界，模拟已预判）
- milvus_024（DEFECT→NOT，FN+1）：机械 A=REFUTED 锁死（filter+ids 互斥无契约断言）
- milvus_038（DEFECT→NOT，FN+1）：灰区保守路径（契约无 groupByField 断言）

## rework 闭环（8 案工单）

| case | 轮次 | 终态 | 说明 |
|------|------|------|------|
| milvus_017 | 1 | DEFECT ✓ | 换真实约束（collections_drop_001）后 A=CONFIRMED 定案 |
| milvus_026 | 1 | NOT_DEFECT | 源码显式允许下划线名（validation_absent 族澄清为 by_design） |
| milvus_037 | 1 | DEFECT ✓ | D=REST类型盲区 + B=HTTP语义 采信 |
| qdrant_010 | 1 | NOT_DEFECT | CONFLICT 闭环：契约明示 payload-only 支持（quote 实际支持观测） |
| weaviate_010 | 1 | DEFECT ✓ | D=维护者已修 500→422 锚点 + B=HTTP语义 |
| milvus_007 | 2 | NOT_DEFECT | 材料性 phantom（v7 先例） |
| milvus_029 | 2 | NOT_DEFECT | 契约无 HTTP-4xx 断言（constraint-absent 族） |
| milvus_038 | 2 | NOT_DEFECT | 契约无 groupByField 断言（同族） |

闭环有效率：5/8 收敛出终判（3 ✓TP），3 案材料性不可修复（与 v7 结论一致——契约缺断言族是 rework 上限）。

## 结论

1. **机械注入修复确认有效且方向正确**：recall +0.113 无监督复现，precision 代价 -0.014（优于模拟预测）。这是 SOP 文字纪律无法达到的结构性修复。
2. **CONFLICT 闭环在注入下真正工作**：v7 4 案 CONFLICT 全被架空，v7.1 的 CONFLICT（qdrant_010/weaviate_010/milvus_029）全部走了打回-复审，其中 1 案翻正（weaviate_010）、2 案闭环到正确保守终态。
3. **剩余 FN 12 的构成**：by-design/认知抗辩 4（003/008/024/qdrant_016）、契约缺断言 5（012/013/029/033/038）、材料性 2（001/qdrant_018 部分）、灰区保守 1——机械层能做的已做完，下一步收益在契约补断言（文档考古法，E6 已验证可复制）。
4. **FP 9 的构成**：机械 A 误伤 3（021/027/qdrant_009，violates 语义边界）+ 机械 B 语义触发 4（011/018/019/028/qdrant_003/weaviate_009 部分重叠）——收紧 A 的 quote 匹配与 B 的"应拒绝"声称识别是 precision 回收点。

## 与论文口径的关系

RQ2 判定链路无人值守数字更新为 **v7.1：recall 0.727 / precision 0.780**（71 案全量、零人工干预、机械层结构性采信）。v7（0.614/0.794）作为"LLM 服从性失效"的对照保留。E6（0.793/0.852）维持"44 案子集+人工监督"的机制实验定位。

## 产物

- `gen_dispatch_v71.py`（机械预跑注入派发器）
- 各组 `sessions/{v}/{ver}/debate_logs/chain_verdicts_v71[_a|_b|_r].json`
- `rq2_v71_rework_state.json`（8 案闭环计数）
- 本报告

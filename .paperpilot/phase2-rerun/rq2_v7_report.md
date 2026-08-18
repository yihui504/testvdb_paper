# RQ2 v7：E6 判定链路完整复测（71 case / 15 组，2026-08-19）

## 运行协议

- builder：`testvdb:evidence-builder` ×71（gen_dispatch_v7.py 派发，claim 锚程序化注入 packet raw_observation 原文；18 个空 ro 用 issue title 原文兜底——任务书口径）
- auditor：`testvdb:chain-auditor` 15 组（>12 链的组拆两批：milvus 2.6.16/2.6.17/3.0.0、qdrant 1.18.2；批判词合并为 chain_verdicts_v7.json）
- rework 闭环：3 轮上限主进程执行（rq2_v7_rework_state.json 计数），超限保守 NOT_DEFECT
- 泄漏扫描：全部派发词 0 命中（R2 硬门禁）

## 终态指标（71 case 全量，GT=cases_index.json gt_label）

| 口径 | recall | precision | fp_supp |
|------|--------|-----------|---------|
| fixF（Phase 2 终值） | 0.621 | 0.818 | — |
| E6（44 案子集终态） | 0.793 | 0.852 | — |
| **v7（本轮全量复测）** | **0.614** | **0.794** | **0.741** |

**TP 27 / FP 7 / FN 17 / TN 20 / NME 0**（E6 机制下的 NME 全部走完 rework 闭环收敛，无悬置）。

⚠️ **口径警示**：E6 的 0.793/0.852 是 44 案子集（E 系列实验只跑 GT=TP 的挖掘产物侧），v7 是 71 案全量。两者分母不同，直接比会高估 v7 的退步幅度。同为全量 71 案的对照是 fixF（0.621/0.818）——v7 recall 0.614 与之持平（-0.007），precision 0.794 略降（-0.024）。

## E6→v7 逐 case 翻转（∩44 案）

same 29 / ↑2 / ↓13：

**翻正方向（↑，2 案）**
- milvus_043：NME→DEFECT，GT=CONFIRMED ✓（strictGroupSize HTTP 语义机械 B）
- milvus_018：NOT_DEFECT→DEFECT，GT=FALSE_POSITIVE ✗（TOCTOU race 判定，翻错）

**翻负方向（↓，13 案，7✓ 6✗）**
- 翻对的（FP 侧收紧，7）：milvus_014/021、qdrant_009/010（GT=FALSE_POSITIVE）
- 翻错的（TP 丢失，6）：milvus_029/030/031、qdrant_004/015/016、weaviate_007（GT=CONFIRMED）

## FN 17 全名单（GT=CONFIRMED 判 NOT_DEFECT）

milvus_001/002/003/004/006/008/012/013/029/030/031/033、qdrant_004/015/016/018、weaviate_007

按机制归因（主进程事后，不进 prompt）：
1. **近似算法 by_design 抗辩过强**（002/003/006/008/029）：auditor 采信"自动替换/float 精度/宽松解析是设计"的 C=REFUTED + D=SUPPORTS_NOT_DEFECT 组合——E6 里这些靠机械 B/CONFLICT 闭环保住的 TP，本轮 builder 的 violates 声明偏保守（violates=False）使机械层不触发
2. **rework 保守落判吞掉**（030/008）：3 轮上限走满保守 NOT_DEFECT（030 复杂度约束确实不在契约中——契约缺断言族；008 材料性不可修复：log 无 count 操作）
3. **契约缺正约束族**（012/013/018/031/033/qdrant_016）：A=NEUTRAL(constraint_absent) 后灰区 B/C/D 未给信号
4. **by-design 认知锚点翻案**（qdrant_004/015、weaviate_007、milvus_021）：D=SUPPORTS_NOT_DEFECT + 源码 by_design——GT 是维护者后来修了的（blindspot 在认知材料里没有对应锚点）

## FP 7 全名单（GT=FALSE_POSITIVE 判 DEFECT）

milvus_011/018/019/027/028、qdrant_003、weaviate_009

- milvus_011（filter=null 全表返回）、027（shardsNum 边界）、028（枚举空值）、qdrant_003（score_threshold 越界）、weaviate_009（batch 空向量）：机械 B 数值下界/枚举/类型恒真触发——GT 侧维护者不接受为缺陷
- milvus_019（同名 rename）、018（TOCTOU）：灰区 B/C/D 聚合判 DEFECT

## 与 E6 差距解剖（0.793 → 0.614，44 案同口径重算见下方注意）

E6 的 4 案 CONFLICT 闭环（009/014/030/qdrant_016）本轮结果：009 DEFECT 保持 ✓、030 保守 NOT_DEFECT ✗、qdrant_016 NOT_DEFECT ✗（E6 判 DEFECT）。E6 的翻正依赖**人工挑选的 conflict batch + 定向 builder 复核**（violates 复核条款在 E6 是逐案监督执行）；v7 是无人干预全流程，builder 的 violates 自检条款触发率不足——E5 引入的"violates 声明自检"在无监督下明显退化。

## rework 统计

| case | 轮次 | 终态 | 备注 |
|------|------|------|------|
| milvus_001 | 2 | NOT_DEFECT | 材料性不可修复（gRPC 无 trace） |
| milvus_007 | 3 | NOT_DEFECT（保守） | claim 为 phantom（log 无该现象） |
| milvus_020 | 1 | NOT_DEFECT | 闭环收敛（换真实约束后 A=REFUTED） |
| milvus_030 | 3 | NOT_DEFECT（保守） | 复杂度约束不在契约 |
| qdrant_008 | 3 | NOT_DEFECT（保守） | 材料性不可修复（log 无 count 操作） |
| qdrant_016 | 2 | NOT_DEFECT | 闭环收敛（lookup_from 条件性 by-design） |

工单类型：PHENOMENON_MISMATCH×4、EVIDENCE_GAP×2。6/6 走完闭环，无 CONFLICT 悬置。

## 结论

1. v7 全量指标与 fixF 持平（recall -0.007 / precision -0.024，71 案同口径），未复现 E6 子集上的 0.793/0.852
2. E6→v7 的差距主因：E6 的定向 violates 复核与 CONFLICT 批是**人工挑选的监督干预**，全流程无人值守时该机制退化；builder violates 自检在源头的触发不足是首要改进点
3. rework 闭环本身按设计工作（6/6 收敛，保守路径无误判 DEFECT），但其上限被材料质量锁死（2/6 是材料性不可修复）
4. NME 清零达成——71 案全部有终判，可审计链完整

## 产物清单

- 判词：`rq2_v7_verdicts.json`（71 case 汇总）+ 各组 `sessions/{v}/{ver}/debate_logs/chain_verdicts_v7[_a|_b].json`
- rework 计数：`rq2_v7_rework_state.json`
- 派发器：`gen_dispatch_v7.py`（v4 纪律 + title 兜底 + rework 参数修复）
- 链文件：71 case evidence_chain/*.json（v7 重建，少数 E6 后已合格链保留）

# RQ2 v9 实验链总结（2026-08-19）

## 一句话

最新版判定链路（机械 A/B 注入 + 7 考古契约断言 + 4 认知锚点 + rework 闭环）在 71 案
全量、四轮复测下终态 **recall 0.909 / precision 0.889 / f1 0.899 / fp_supp 0.815**
（TP40/FP5/FN4/TN22），四轮逐案 71/71 一致；注入口径按 in-sample 定位，论文 headline
仍为无注入 v7.x 三轮中位 0.705 [0.682, 0.727] / 0.775。

## 实验矩阵

| 实验 | 口径 | 结果 | 位置 |
|------|------|------|------|
| v9 首轮全量+闭环 | 最新版材料 71 案 | 0.909/0.889；7 NME 全闭环（6 TN+1 TP） | rq2_v9_run1_report.md |
| v9b/v9c/v9d 复测 | 同协议三轮 | 终态逐案一致；r3/r4 严格同链 i.i.d. 对 0 差异 | rq2_v9_three_runs_report.md |
| gates-only 基线 | 纯机械层无 LLM | 0.907/0.886 + 9 悬置；LLM 补全 9 案全对（+1TP+8TN） | 同上 |
| 8 案 LLM 子集 | 裁量空间 32 判定 | 0 翻转，翻转率 95% 上界 p≤0.089 | 同上 |
| 独立评审 | pp:review 三 reviewer | R1 Weak Accept / R2 Accept / R3 Weak Reject → Meta ACCEPT | ../review/rq2_v9_experiment_review.md |

## 关键结论（论文可引用表述）

1. **分层方差**：verdict 层零漂移是机械化的结果（89% 案在 auditor 会话前定案），
   不是 LLM 变稳定——LLM 方差被挤压到归因标签层（root_cause 15/71、fp_src 18/71
   漂移）和过程层（NME 7→1→0）。论文写方差节须用此三层结构，禁写"LLM 零方差"。
2. **LLM 边际贡献有界**：gates-only 对照显示 LLM 不修正机械层错误、不引入新错误，
   只补全确定性证据主导的悬置案。
3. **注入口径循环性**：7 断言+4 锚点源自 GT 同源材料，0.909/0.889 是 in-sample
   校准口径，非独立检测强度；headline 纪律见 rq2_v9_three_runs_report.md 论文口径节。
4. **B 规则2 FP 边界**（已拍板接受现状）：milvus_014/028 与 029 现象同族、GT 相反，
   precision 0.889 含 2 个同族错判，论文须如实携带。

## 产物清单

- 派发词：dispatch_v9/（v9/v9b/v9c/v9d ×15 组 + rework 工单 11 份）
- 判词：tvdb_sessions（实验数据树，非本仓库）/sessions/*/*/debate_logs/
  chain_verdicts_v9{.json,_r,_r2,_v9b(+_r),_v9c,_v9d}
- 材料源：.paperpilot/phase2-rerun/{cases_index.json, defect_id_map.json, packets/}
- 判定器源码：mftui/TestVDB/scripts/（check_chain_grounding / check_physical_constraints
  / check_anchor_conflict）+ agents/chain-auditor.md（主仓库，插件 cache 2.3.0 同步）

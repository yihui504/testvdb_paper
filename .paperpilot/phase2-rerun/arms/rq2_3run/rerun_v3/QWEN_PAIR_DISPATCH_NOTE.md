# Qwen full/flat 双臂派发指引（单 run 试探版）

**前置**：本会话必须运行在 Qwen 上（/model 切换后新开会话）。agent 继承会话模型——这是 backbone 切换的实现机制（与当年 run_donlyq 相同）。

**任务**：12 个 dispatch 文件，逐个派发 sub-agent。每个 agent 的指令相同：

> Read 文件 `<dispatch 路径>`，严格按其内容执行（读取材料、判定、Write verdicts JSONL 到指定路径、返回一行摘要）。除此之外不读任何其他文件，不联网。

**文件清单**（派发时替换路径）：

full 臂（四视角协议，6 批）：
- .paperpilot/phase2-rerun/arms/rq2_3run/rerun_v3/run_fullq1/batch1_dispatch.txt … batch6_dispatch.txt
- 产出：run_fullq1/verdicts_batch1..6.jsonl

flat 臂（单提示，6 批）：
- .paperpilot/phase2-rerun/arms/rq2_3run/rerun_v3/run_flatq1/batch1_dispatch.txt … batch6_dispatch.txt
- 产出：run_flatq1/verdicts_batch1..6.jsonl

**派发纪律**（历史教训：12 批并发会触发 429 静默死亡）：
- 分 2-3 波，每波 4-6 个 agent 并行；每波结束**逐个确认 verdicts 文件已落盘**再发下一波
- 每个 agent 完成的判据 = 对应 verdicts_batchN.jsonl 存在且行数 13-14
- 全部完成后抽查 2 个 rationale 确认判定语言/协议符合 dispatch

**完成后**：回主会话（GLM）做聚合分析（Qwen-full vs Qwen-flat 同家族 McNemar）并写入论文。

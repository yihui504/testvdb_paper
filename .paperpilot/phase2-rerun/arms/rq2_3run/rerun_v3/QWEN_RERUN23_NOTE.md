# Qwen full/flat 补轮（run 2/3）派发指引

**前置**：本会话必须运行在 Qwen 上（与 run_donlyq/fullq1 相同机制）。目的：把 full-vs-flat 第二家族配对从单轮补成三轮同口径——R1 3.1 "properly bounded negative" 或机制复制，二选一收口。

**任务**：24 个 dispatch，逐个派发 sub-agent。每个 agent 的指令相同：

> Read 文件 `<dispatch 路径>`，严格按其内容执行（读取材料、判定、Write verdicts JSONL 到指定路径、返回一行摘要）。除此之外不读任何其他文件，不联网。

**文件清单**（派发时替换路径；均为 6 批）：
- .paperpilot/phase2-rerun/arms/rq2_3run/rerun_v3/run_fullq2/batch1..6_dispatch.txt → run_fullq2/verdicts_batch1..6.jsonl
- .paperpilot/phase2-rerun/arms/rq2_3run/rerun_v3/run_fullq3/batch1..6_dispatch.txt → run_fullq3/verdicts_batch1..6.jsonl
- .paperpilot/phase2-rerun/arms/rq2_3run/rerun_v3/run_flatq2/batch1..6_dispatch.txt → run_flatq2/verdicts_batch1..6.jsonl
- .paperpilot/phase2-rerun/arms/rq2_3run/rerun_v3/run_flatq3/batch1..6_dispatch.txt → run_flatq3/verdicts_batch1..6.jsonl

**派发纪律**（429 教训）：
- 分 4 波（每波一个 run 的 6 批，或每波 6 个），每波结束逐个确认 verdicts 文件落盘（每文件 13-14 行）再发下一波
- full 臂注意：逐行单次工具调用写 JSONL（6000 token 上限曾截断成段写入）
- 若单 agent 挂（ECONNRESET/429），确认无残留文件后重派该批

**完成后**：回 GLM 主会话聚合（full/flat Qwen 三轮 majority + full-vs-flat 同家族 McNemar + 论文 backbone 段终稿）。

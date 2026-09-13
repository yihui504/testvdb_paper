# Qwen 侧认知锚定重判（run_fullq1/2/3）派发指引

**背景**：2026-09-13 发现运行时认知文件含 81 池候选自身条目（milvus 6 编号→4 条 FP 侧 by_design_patterns + 1 条 TP 侧 blindspot 对；qdrant #9523→1 条 by_design_patterns），而清理版（milvus 2026-09-10 / qdrant 2026-09-13 生成）未被重判 dispatch 引用。7 个受影响案：milvus_004/006/018/019/021/027、qdrant_017。GLM 侧 run_full1-3 已重判完毕；**Qwen 侧 run_fullq1-3 需在 Qwen 会话派发**（本会话为 GLM，无法代跑）。

**任务**：Qwen 会话逐个派发 3 个 sub-agent，每个的指令相同：

> Read 文件 `<dispatch 路径>`，严格按其内容执行（读取材料、判定、Write verdicts JSONL 到指定路径、返回一行摘要）。除此之外不读任何其他文件，不联网。

dispatch 路径（均已生成、已验证 7 案材料 + cleaned 认知路径 + 输出路径）：
- `.paperpilot/phase2-rerun/arms/rq2_3run/rerun_v3/run_fullq1/coganchor_rejudge_dispatch.txt` → `run_fullq1/verdicts_coganchor_rejudge.jsonl`
- `.paperpilot/phase2-rerun/arms/rq2_3run/rerun_v3/run_fullq2/coganchor_rejudge_dispatch.txt` → `run_fullq2/verdicts_coganchor_rejudge.jsonl`
- `.paperpilot/phase2-rerun/arms/rq2_3run/rerun_v3/run_fullq3/coganchor_rejudge_dispatch.txt` → `run_fullq3/verdicts_coganchor_rejudge.jsonl`

**纪律**：
- 3 个 agent 逐个派发（或一波 3 个），每个完成后确认 `verdicts_coganchor_rejudge.jsonl` 落盘且恰 7 行
- 若单 agent 挂（ECONNRESET/429），确认无残留文件后重派
- 判前 verdicts 已备份在各自目录 `_pre_coganchor.jsonl`

**完成后回 GLM 主会话**：跑合并重算（把 6 个 rejudge 文件替换进全链聚合，重出 headline/族敏感性/strata 全部数字），再落论文修订。

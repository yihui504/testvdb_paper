# Qwen 侧认知剥离重判指引（4 个 agent）

**前置**：本会话必须运行在 Qwen 上（/model 切换后新开会话，与 run_donlyq 同机制）。

**背景**：10 个包（milvus_010/014/018/019/022/026/027/028/032/033）内嵌的维护者认知节已从包中剥除（原包归档于 `_v9_archive/packs_pre_cogstrip/`）。需要在这些臂上按剥除后的包重判这 10 案。

**任务**：派发 4 个 sub-agent，每个的指令相同：

> Read 文件 `<dispatch 路径>`，严格按其内容执行（读包/源码取证/判定/Write JSONL 到指定路径/返回一行摘要）。除此之外不读任何文件，不联网。

**dispatch 清单**：
- .paperpilot/phase2-rerun/arms/rq2_3run/rerun_v3/run_donlyq1/rejudge_cog_dispatch.txt
- .paperpilot/phase2-rerun/arms/rq2_3run/rerun_v3/run_donlyq2/rejudge_cog_dispatch.txt
- .paperpilot/phase2-rerun/arms/rq2_3run/rerun_v3/run_donlyq3/rejudge_cog_dispatch.txt
- .paperpilot/phase2-rerun/arms/rq2_3run/rerun_v3/run_flatq1/rejudge_cog_dispatch.txt

产出各 run 目录下 `verdicts_rejudge_cog.jsonl`（每文件 10 行）。

**纪律**：4 个可一次并行（量小）；每个完成的判据 = 对应 jsonl 存在且 10 行。注意 CLAUDE_CODE_MAX_OUTPUT_TOKENS 若为 6000：flatq 的行小无碍，donlyq 行含 d_evidence 也小；若 Write 被截则逐行写。

**完成后**：回 GLM 主会话说"Qwen 重判落盘"，由主会话合并 verdicts、重聚合、更新论文。

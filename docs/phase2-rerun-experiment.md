# Phase 2 重做 = 跑真 dev-reviewer 判 71 样本 TP/FP

> 样本是 issue。dev-reviewer 正常运行时读一组固定文件（见 `testvdb4exp/agents/dev-reviewer.md` + `commands/mine.md` 的 Output 布局）。
> 实验 = **把每个样本还原成 dev-reviewer 会去读的那些文件 → 派 `Agent(subagent_type="testvdb:dev-reviewer")` → 收 `dev_review.json` 的 verdict**。
> 不自定义 judge/packet 脚本；用插件真 agent + 它真读的文件布局。

## dev-reviewer 读的文件（还原目标）

```
results/{target}/{version}/{timestamp}/          ← SESSION_DIR
├── output_*.log                                 ← 探针执行输出（raw 证据）
├── .srcdir                                      ← 一行：该版本源码 clone 路径
└── debate_logs/stage2_aggregation.json          ← 候选清单（defect_id/endpoint/defect_type，剔 rationale/GT）
results/{target}/{version}/
├── structured_contract.json                     ← 版本契约
└── api_templates.md                             ← 版本 API 模板
intelligence/{target}/
├── developer_cognition.json
└── bug_shapes.json
+ 活容器（TESTVDB_DB_URL）— dev-reviewer Step1/4 复现/证伪用
```

派发：`Agent(subagent_type="testvdb:dev-reviewer", prompt="session_dir=..., target=..., version=..., 候选=...")` → 产出 `SESSION_DIR/debate_logs/dev_review.json`（含每候选 verdict + source_grounding + steps）。

---

## 准备（不起容器，现在可做）

把已有产物摆进上面布局 + 补两个缺失件：

| 要摆的 | 来源 | 去向 |
|--------|------|------|
| structured_contract.json | `contracts/{target}/{ver}.json`（7 真 + 9 派生） | `results/{target}/{version}/` |
| developer_cognition/bug_shapes.json | `intel/{target}/` | `intelligence/{target}/` |
| .srcdir | 一行 `C:/Users/11428/Desktop/vdb_src/{target}/{tag}` | 每个 session 根 |
| **api_templates.md**（缺） | 从契约 `api_endpoints` 生成，每版本一份 | `results/{target}/{version}/` |
| **stage2_aggregation.json**（缺） | 把该版本样本列为 confirmed 候选（defect_id/endpoint/defect_type，**无 GT/无 rationale**） | `SESSION_DIR/debate_logs/` |

→ `layout_inputs.py`（摆文件 + 生成 `api_templates.md`/`stage2_aggregation.json`/`.srcdir`）+ `fill_endpoints.py`（从探针脚本抽 endpoint 补 stage2_aggregation）。**无自定义判官脚本。**
> ✅ 已完成（2026-08-14）：71/71 session 还原到 `run/` 下 dev-reviewer 真实布局，endpoint 71/71（milvus 43/qdrant 18/weaviate 10），`.srcdir`→clone 71/71，版本契约+api_templates+intelligence 齐全。唯一缺 `output_*.log`（实验期跑探针才有）。

## 实验（等"开始"，要容器）

按版本：起容器 → 跑该版本探针（`orchestrate.py`，probe_common 已会写 output）→ `output_*.log` 入 session → 派 dev-reviewer agent（**容器常驻**供其 Step1/4 复现/证伪）→ 收 `dev_review.json` → 停容器。
- GLM-5.2 先（harness 主模型即 GLM-5.2，派出 agent 即 GLM-5.2 dev-reviewer）；DeepSeek 后。
- 不复现 case：dev-reviewer 自己会记，入结果如实。

## 收集 + 分析

`dev_review.json` 每候选 `verdict`（CONFIRMED/FALSE_POSITIVE）→ vs GT（cases_index group/gt_label）→ recall / precision / FP-suppression + flippers + 按 defect_type/vendor 分组 + 对比旧 oracle；DeepSeek 到位后加 inter-model κ。
> κ 语义（主动模式）：full-task agreement（含探索路径差），论文按此写。

## 决策

- D1 milvus SDK raw：dev-reviewer 读 output_*.log（探针 emit 观察），SDK 探针所见即此——1:1，无需额外抓 gRPC。
- D2 轮数：默认 3（量化采样方差），GLM 可先单跑 1 轮验流程。
- D3 DeepSeek：后做（agent 模型 or API，待定）。
- D7 dev-reviewer 模式：**主动**（带工具 + clone + 活容器，跑完整 SOP）。

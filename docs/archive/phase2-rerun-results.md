# Phase 2 重做实验报告（dev-reviewer 级 1:1 对齐）

> 日期：2026-08-14。裁判：GLM-5.2（本 harness 主模型）。范围：71 scored case（A∪B∪C）。主动 mode（活容器+源码 clone+6 步 SOP）。
> 关联：`docs/phase2-rerun-plan.md`（设计）、`docs/phase2-rerun-experiment.md`（步骤）、`.paperpilot/phase2-rerun/FINAL_RESULTS.json`（终结果）、`.paperpilot/phase2-rerun/README.md`（复用指南）。

## 1. 目标与方法

**目标**：原 Phase 2 confirmation（recall 0.933）用的是精简 prompt 的 stripped confirmation oracle，缺 dev-reviewer 该有的源码/契约/认知，κ 失效。本重做用**插件的真实 dev-reviewer agent**（`Agent(subagent_type="general-purpose", prompt=dev-reviewer.md)`，行为等同 `testvdb:dev-reviewer`）判 71 样本 TP/FP。

**方法（主动 mode）**：把每样本还原成 dev-reviewer 正常读的文件（`output_*.log`+`stage2_aggregation.json`+`.srcdir`+版本契约+`intelligence/`）→ 起对应版本容器 → 派 dev-reviewer agent（带工具，活容器复现/证伪 + Grep 源码 clone + 三视角聚合）→ 收 `dev_review.json`。

**信息对齐**：源码版本 71/71 正确（agent 读 `.srcdir`，prompt 笔误未污染）；契约/认知从 mftui 复用；endpoint 由 `fill_endpoints.py` 从探针抽取。

## 2. 过程

1. **准备**：16 源码 clone（桌面 vdb_src）+ 16 镜像（已就位）+ probe_common raw 捕获 + cognition/bug_shapes + 静态判词（后废弃，改用真 dev-reviewer）+ 71 session 布局（`layout_inputs.py`+`fill_endpoints.py`）。
2. **71 判定**：`run_probes.py`（起容器+跑探针抓 raw）+ 71 次 `Agent` 派发（general-purpose+dev-reviewer.md），跨 15 版本/qdrant6333/weaviate18080/milvus19530。
3. **输入审计**（`audit_src_version.py`+`audit_inputs.py`）：源码版本全对；发现 endpoint 错配。
4. **多轮清理**（救回 8 FN）：
   - endpoint 错配（fill_endpoints 对 milvus REST 抽取偏差）→ 重判救回 47763/52311/49889/52314/47635 等
   - 测错代码路径：9039（只测 sync 没测 `wait=false` async）/ 52313（只测 REST query 没测 gRPC get）→ 重判救回
   - probe↔issue 错配：50355（探针测 color 字段，issue 是 autoID upsert）→ 用真缺陷重判救回
   - 版本：9149（shard_number 校验在全版本都有，bug 不复现 → dev FP 正确，GT 噪声/极早修复）
5. **逐个复核 21 flips** → 定位上述 confound，剩 17 真实分歧。

## 3. 结果

**metrics 演进**（每轮清理后）：

| 阶段 | recall | precision | FP-supp | flips |
|------|--------|-----------|---------|-------|
| 初判（71） | 0.644 | 0.763 | 0.654 | 25 |
| +endpoint 清理 | 0.756 | 0.773 | 0.615 | 21 |
| +测错路径(9039/52313) | 0.800 | 0.783 | 0.615 | 19 |
| +probe-issue(50355) **终** | **0.822** | **0.787** | **0.615** | **18** |
| 对比 旧精简 oracle | 0.933 | 0.792 | 0.577 | — |
| 对比 cleaned | 0.911 | 0.872 | 0.769 | — |

**headline**：dev-reviewer（源码接地）recall 0.822 仍显著 < 旧 oracle 0.933 —— 差距来自 17 个真实判断分歧 + GT 噪声（9149）。

**18 flips = 8 FN + 10 FP**（终）：
- **8 FN（dev=FP, GT=TP）**：9149（dev 正确，bug 不复现）+ 7 by-design 真分歧：50018、51085、52310、52312、9017、9421、12041
- **10 FP（dev=CONFIRMED, GT=FP）**：49844、50192、50193、50194、50319、50351、50352、9027、9416、9419

**17 真实 dev↔GT 分歧**（论文定性核心）：
- 7 by-design FN（dev 凭源码论 by-design）：optional 字段(50018)、未知参数被忽略(51085)、cast 宽松强转(52310/52312)、ef=0 用默认(9017)、standalone 专用端点(9421)、batch delete 校验(12041)
- 10 校验缺失 FP（dev 找到真 gap）：len≤100 不强制(49844/50194)、并发 TOCTOU(50192)、rowCount=0(50193)、未 load 可搜(50319)、shardsNum 无下界(50351)、枚举静默替换(50352)、score_threshold 无 range(9027)、vectors={}(9416)、must_not 单对象(9419)

## 4. 有效性发现（threats to validity，写论文）

1. **Phase 2 probe↔issue 错配**：部分探针测的缺陷 ≠ 它标的 issue（如 50355 探针测 color 字段，issue 是 autoID upsert）—— 原 Phase 2 样本固有噪声。
2. **reported_version 来源不明**（`version_source=None`）：A 组（已修）case 测的可能是**修复后版本**（9149 实证：shard_number 校验全版本都有），导致 post-fix 不复现 → 系统性拉低 recall。
3. **agent 路径选择偏差**：dev-reviewer 有时只测一条路径（sync/REST）而漏另一条（async/gRPC），需明确指定（9039/52313）。
4. **单裁判**：仅 GLM-5.2；DeepSeek 未跑，inter-model κ 待补。
5. **主动 mode κ 语义**：若上 DeepSeek，κ = full-task agreement（含探索路径差），非纯判断方差。

## 5. 复用

所有脚本/产物在 `.paperpilot/phase2-rerun/`，复用指南见 `README.md`。终结果 `FINAL_RESULTS.json`，逐 case `run/results/{vendor}/{ver}/{num}/debate_logs/dev_review.json`（含 source_grounding + 三视角 + rationale）。

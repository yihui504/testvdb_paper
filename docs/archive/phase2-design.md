# Phase 2 设计：controlled detection capability 实验

日期：2026-08-13 | 状态：设计稿，待确认后执行

## 1. 目标

在 Phase 1 的 126 条（124 issues + 2 PRs）known-ground-truth candidate 上，用**当前版 TestVDB 判定逻辑**（机械 L1 gate + GLM 语义判定 + 真实验证）重新判定每条 candidate，产出：

- **controlled precision / recall**（论文新 RQ2 的核心指标）
- **FP-still-false / FP-now-correct**（历史 26 个 FP 在最新版下还误报吗——导师关注点）
- **53 个 unadjudicated 的当前 verdict**（辅助信息）

## 2. 术语（清晰口径，修正 redesign 文档的混用）

每条 candidate 有两个标签：

| 标签 | 含义 | 来源 |
|---|---|---|
| **GT**（ground truth） | 真 bug（45）/ 非 bug（26）/ 未决（53）/ 自提 PR（2） | Phase 1 人工核对 |
| **verdict**（最新版判定） | CONFIRMED / FALSE_POSITIVE | Phase 2 重跑 |

四格：

| GT \ verdict | CONFIRMED | FALSE_POSITIVE |
|---|---|---|
| 真 bug | **TP-caught**（recall 分子） | **FN-missed**（漏检） |
| 非 bug | **FP-still-false**（误报仍在） | **FP-now-correct**（误报消除） |

## 3. 重跑集（全量 126，按 GT 分 4 组）

**容器版本：历史版本**（每条 candidate 在其被报告时的 DB 版本上重跑，2026-08-13 用户确认）。理由：28 个已修的 bug 在报告时版本上 probe 可复现 → 全部进入 recall 分子，detection 分母 = 全部 71 条 GT 已知集，口径最干净。

| 组 | 条数 | 历史版本重跑的意义 |
|---|---|---|
| A. TP_FIXED_PR（已修） | 28 | probe 在报告时版本应**复现** bug → verdict CONFIRMED → recall 分子 |
| B. TP ack-unfixed（8 open + 6 closed-nofix + 3 dup） | 17 | bug 未修 → probe 应复现 → verdict CONFIRMED → recall 分子 |
| C. FP（16 BY_DESIGN + 8 FP_BY_DESIGN + 2 FP_NOT_REPRO） | 26 | 新版判定逻辑（L1 + GLM）应判 FALSE_POSITIVE（FP-now-correct），若 CONFIRMED 则 FP-still-false |
| D. unadjudicated（26 pending + 25 self-closed + 1 open-no-label） | 52 | 拿当前 verdict；GT 未知不计入主指标 |
| E. 自提 PR | 2 | 不跑（无独立 candidate，附属于 #47729） |

**主指标分母**：A ∪ B ∪ C = 71 条 GT 已知。

- recall = (A 判 CONFIRMED + B 判 CONFIRMED) / 45
- precision = (A+B 判 CONFIRMED) / (A∪B∪C 中判 CONFIRMED 的总数)
- FP 抑制 = FP-now-correct(C) / 26
- 辅助：D 组 verdict 分布（不计主指标）

**版本来源**：milvus 用 body 模板字段 `Milvus version:`；weaviate 用 body 中 docker tag `weaviate:x.y.z`；qdrant 无显式字段 → created_at 反查当时最新 release（缺失时取同 vendor 同批众数）。

## 4. 数据流

```
126 条 raw JSON (title+body, phase1-raw/*.json)
   ↓ ① 离线：构建 manifest（参数提取：endpoint / param / 非法值 / 断言）
manifest.json（126 条结构化）
   ↓ ② 离线：按根因组生成 probe 脚本（同 PR 的 issue 共享参数化 probe）
probe_<repo>_<n>.py
   ↓ ③ 容器：docker compose 起 3 个 VDBMS，host Python 跑 probe → output_*.log
   ↓ ④ 离线：L1 机械 gate（verify_live_l1.py 的 checks，新版确定性 FP 过滤）
   ↓ ⑤ GLM5.2：语义判定（用户切 Claude Code 模型为 GLM5.2，我按模板执行）
verdict_<n>.json（CONFIRMED / FALSE_POSITIVE + rationale）
   ↓ ⑥ 离线：与 GT 对齐，算 precision/recall/FP 抑制
phase2-report.md → 论文新 RQ2
```

## 5. 关键决策点（2026-08-13 已确认）

1. **容器版本**：✅ 历史版本（用户确认）。
2. **GLM5.2 判定环节范围**：✅ 仅 ⑤ 语义判定；probe 生成（②）由我按 title/body 提取参数生成。
3. **D 组（52 条）**：✅ 也跑 probe + 判定（用户选全量 124），verdict 单独记录不计主指标。
4. **probe 根因组去重**：同 PR 的 issue 共享参数化 probe（如 milvus 52307/52313/52315 同 PR #52261）。
5. **重跑时机**：容器未就绪 → 先完成 ①②④⑤ 的模板与 manifest（离线），容器就绪后批量 ③，再 ⑤⑥。

## 6. 执行顺序（标注容器依赖）

- [ ] ① manifest 构建（离线，立即）
- [ ] ② probe 脚本生成（离线，立即）
- [ ] ④ L1 gate 接入 + ⑤ GLM verdict 模板/harness（离线，立即）
- [ ] ③ 容器批量实跑（**等容器**）
- [ ] ⑥ 汇总 + 论文新 RQ2（等 ③⑤ 完成）

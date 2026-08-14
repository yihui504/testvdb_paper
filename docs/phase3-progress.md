# Phase 3 进度与待办

> 起始：2026-08-13。配套 `docs/phase3-plan.md`（方案）与 `docs/phase3-design.md`（早期设计）。
> 实验版工具仓库：`github.com/yihui504/testvdb4exp`（本地 `C:\Users\11428\Desktop\testvdb4exp`）。

## 当前状态总览

- **任务1（Phase 2 confirmation 有效性评估）**：✅ 完成。结论见下「Phase 2 有效性」。
- **任务2（实验版 testvdb4exp 落地）**：✅ 8 项改造全部完成并推送。
- **任务3（档1 存在版本定位 + gt.json）**：✅ 完成（2026-08-14）。45 bugs → 15 存在版本，见下「档1 产出」。
- **档4 测试套件**：✅ 完成（2026-08-14）。111 测试全绿（1 个预期失败已改为守护新语义）。
- **整体**：工具与 GT 材料就绪；下一步 = probe 存在性复验（档1.5）→ 档2 设施 / 档3 实验。

## 档1 产出（2026-08-14，`.paperpilot/phase3/`）

| 文件 | 内容 |
|---|---|
| `locate_presence_versions.py` | 定位脚本（GitHub API + 本地缓存，可增量重跑） |
| `presence-versions.csv` | 45 条 bug 的存在版本 + 定位证据链 |
| `gt-bug-catalog.json` | 45 条 did → endpoint/title（endpoint 取 phase2 修正后终值） |
| `gt/{vendor}/{version}/gt.json` | 15 组分组 GT（跑实验时拷入 `testvdb4exp/results/{target}/{version}/`） |
| `gt-review.md` | 人工复核表（全部条目 + 定位规则 + 弱对齐标注 + 重点验证项） |
| `releases-cache/` `timeline-cache/` `pr-evidence.json` `pr-details.json` | 中间证据（复跑无需重新拉取） |

**版本池（15 个，plan 预估 ~10）**：milvus 8（v2.3.22×1, v2.6.10×5, v2.6.12×1, v2.6.16×4, v2.6.17×4, v2.6.18×2, v2.6.19×2, v3.0.0×10）／qdrant 3（v1.18.0×2, v1.18.2×5, v1.19.0×1）／weaviate 4（v1.37.4×3, v1.38.0×3, v1.38.1×1, v1.38.2×1）。

**定位规则（含 4 个非显而易见决策）**：
1. A 组 = fix-PR `merged_at` 前最近 **server** release（过滤 `client/` SDK tag，它们与 server 发布时间交错会污染定位）。
2. **并行维护线取 max**：milvus 3.0 线 bug 的 fix merged 晚于 v2.6.22 发布时，"修复前最后 release" 会落在 2.6 旧线；此时取报告版本所在线（两者都含 bug，报告版本有实证）。→ 6 条 milvus 定 v3.0.0。
3. **无 merged fix-PR → 保守取报告版本**：weaviate 6 条（#11399/11400/11401/11730/11732/11741）"修复"PR 实际未 merge（issue 也仍 open）→ 修复未进任何 release → 所有版本含 bug，取报告版本。milvus #47763（maintainer 手工修，commit 不可追溯）同规则 → v2.6.10。**注意：这 6 条 weaviate 在 GT 分类上仍标 TP_FIXED_PR（phase1 口径），但 phase3 语义等同 B 组。**
4. B 组报告版本即存在版本；milvus "2.3" 具体化 v2.3.22（phase2 containers.py 已有同一约定）。

**gt.json 说明**：injector 只用 `param` 做归一化匹配（endpoint 仅人读）；弱对齐项（race bug、类型强转类，共 ~9 条）已在 gt-review.md 标注——只影响催促时机不影响最终指标（reach 终判走事后 LLM 盲评）。injector 冒烟测试通过（确认 password → reached 1/4 正确计数）。

**跑实验前的 probe 存在性复验（档1.5，plan §2「人工 probe 确认复现」）**：45 条中与 phase2 报告版本相同的可直接复用 phase2 结论；跨版本的（重点 qdrant_9045: 报告 v1.12.1 → 存在 v1.18.0，跳 6 个 minor）必须在存在版本上重跑 probe。

## testvdb4exp 实验版（8 项改造已落地）

baseline = `yihui504/TestVDB@b80b95d`（142 tracked 文件，单 baseline commit，不带上游历史）。

| commit | 内容 |
|---|---|
| `1c58b5d` | Initial commit（仓库原有） |
| `29efd38` | 2a — baseline 导入 |
| `e51e2c3` | 2b — #1/#2/#3/#4/#7/#8 |
| `3a5258a` | 2c — #5 GT-informed 续挖注入 |
| `a4db73a` | 2d — #6 按版本分组（简化） |

| # | 改造 | 落点 | 状态 |
|---|---|---|---|
| 1 | 轮次上限 5→30 | `scripts/pipeline_state.py:592` | ✅ |
| 2 | 删 coverage≥95 停 | `scripts/reconstruct_context.py:221` | ✅ |
| 3 | 删连续 5 轮无新缺陷停 | 同上 | ✅ |
| 4 | 关 novelty 查重 | `scripts/novelty_gate.py` `TESTVDB_NOVELTY_BYPASS` env 旁路 | ✅ |
| 5 | GT-informed 续挖注入 | 新 `scripts/gt_reach_injector.py` + `commands/mine.md` 8a/8b `{GT_HINT}` | ✅ |
| 6 | 多版本 batch | 按版本分组：`results/{target}/{version}/gt.json` 约定位置自动发现 | ✅ |
| 7 | attack-* maxTurns→500 | attack-vein(200)/semantic/state/boundary → 500 | ✅ |
| 8 | 跨版本禁缓存 | `check_cache.py` 已按 target+version 双键，**无需改** | ✅（无改） |

**关键设计决策（非显而易见，易忘）**：
- **GT-informed 盲注契约**：`gt_reach_injector.py` 输出只含「已确认 X/Y + 提升脚本质量/扩大覆盖/深化挖掘」的通用催促，4 个 attack agent 收到**相同**文本，不含端点/参数/预期。hint 措辞**刻意不含「更换策略」**——会通过否定泄露方向（暗示当前方向错）；用户 2026-08-13 确认删掉。
- **#6 简化**：不做 manifest / batch 命令 / headless 驱动；gt.json 按 (target,version) 分组放约定位置，injector 从 `session_dir.parent/gt.json` 自动发现（env `TESTVDB_GT_PATH` 作 override）。实验=每版本跑一次 `/mine`。
- **#8 no-op**：`check_cache.py` 本就 target+version 双键，跨版本天然 MISMATCH→重新生成。

**实验运行方式**：每版本把 gt.json 放 `results/{target}/{version}/gt.json` → 跑 `/mine target=X version=Y`（带 `TESTVDB_NOVELTY_BYPASS=1`）→ injector 自动发现、GT hint 激活、轮次≤30、attack 500 turns。

## Phase 2 confirmation 有效性评估（任务1，已完成）

核心数字可信：recall 42/45=93.3%、precision 79.2%、FP-suppr 57.7%；算术与混淆矩阵全部复核一致；probe 124/124 真跑（`run_summary_*.json`）；盲评 sanitize 基本到位（核验 #50324 的 GT 泄漏被剥干净）。定位诚实（oracle 上界，非端到端）。

**两个未披露的威胁（待处置）**：
1. **expectation 字段框架偏差**：喂 GLM 的 `Expected behavior` 用报告人视角规范性措辞（"should error / leaks data silently"），对 C 组（FP）系统性推向 CONFIRMED。**只影响 precision/FP-suppression，不影响 headline recall**（recall 分母 A∪B 的框架与 GT 一致）。Milvus FP 抑制 4/14 可能部分归因于此，而非论文所说的「contract ambiguity」——两者从这份数据分不开。
2. **probe 观察文本泄漏**：probe case desc 原样进 GLM observation，**不经 sanitize**（如 #50324 prompt 里「FP note」残留）。次要、不一致，但破盲。

处置选项：写进论文 threats-to-validity；或在 phase 3 对齐 judge 里缓解（中性措辞 + sanitize observation）。

## 待办（按优先级 / 关键路径）

### 档1.5 — probe 存在性复验（跑实验前最后一道数据关）
- [ ] 45 条 bug 在各自存在版本上确认可触发（与 phase2 报告版本相同的可复用 phase2 结论）。
- [ ] 重点：qdrant_9045（v1.12.1→v1.18.0 跨 6 个 minor）、milvus_50355（doc-fix 型）、milvus_47635（race，低概率）。
- [ ] 版本池 15 个 > plan 预估 ~10：可考虑合并 1-bug 小组（v2.3.22/v2.6.12/v1.19.0/v1.38.1/v1.38.2）以省算力——但合并 = 换存在版本需重验，**默认不合并**。

### 档2 — phase3-plan §2 设计了、还没建的设施
- [ ] 文档可达性门控（doc-attainable / doc-blind；后者移出 reach 分母）。
- [ ] 契约提取完整性（per doc-attainable bug 写最小 oracle claim，比对工具真实提取的 contract → 漏检归 extraction loss 还是 generation loss）。
- [ ] （条件触发）oracle-contract 消融（reach 偏低时跑，隔离纯提取损失 vs 纯生成损失）。

### 档3 — 实验本身（最大头，要算力/时间）
- [ ] 15 个存在版本上跑 testvdb4exp（Docker + agent，每版本≤30 轮 ×4 attack ×500 turns）。
- [ ] 收 reach / 首达轮次分布。
- [ ] LLM 盲评把每轮产出对齐到 GT bug + 人工复核。
- [ ] forward reach vs 93.3% oracle 上界，差值归因 generation 损失。

### 档4 — 剩余尾巴
- [x] ~~跑 testvdb4exp 测试套件~~（2026-08-14：111 全绿；预期失败的 stalemate 测试已改为守护「只有轮次上限终止」新语义）。
- [ ] **Phase 2 两个威胁处置**（见上）。
- [ ] testvdb4exp 加 `EXPERIMENT.md`（8 项改造 + 跑法说明；现 README 是 TestVDB 原版）。

## 建议下一步
档1.5「probe 存在性复验」（跨版本条目必验，同版本条目快速过一遍 phase2 日志）→ 档2 文档可达性门控（可与档1.5 并行，纯文档工作）→ 档3 实验。

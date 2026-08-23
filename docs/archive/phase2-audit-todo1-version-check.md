# 待办 1 完成报告：A 组 28 case fix-PR 合入版本核查

> 日期：2026-08-14。方法：phase1-raw/verify-report.md 的 28 个 TP_FIXED_PR 证据表给出 fix PR 编号 →
> GitHub API 拉取每个 PR 的 `merged_at`/`base.ref`/`state`（缓存 `.paperpilot/phase2-rerun/pr_cache.json`，
> 脚本 `audit_fix_versions.py`）→ 与本地 shallow clone 的 15 个实验 tag commit 日期比对。
> 11741 缺 PR 证据 → issue timeline 补查（cross-referenced → PR #11967）。

## 1. 结论先行

**Post-fix 风险：28/28 全部排除。** 没有任何一个 fix PR 在实验 tag 之前合并——
所有代码修复的合并时间都晚于对应实验 tag 的 commit 日期（milvus 修复合 master、
qdrant 合 dev、weaviate 合 main，实验 tag 均打在修复之前）。

唯一日期早于 tag 的 #3513 是 2020 年文档 PR（milvus 50355 的"修复"），不改代码行为，单独讨论（§4）。

**意外发现（超出待办 1 范围，需另行处置）：8 个 case 的 fix PR 从未合并**——
GT 的 `TP_FIXED_PR` 标签依据（timeline cross-ref PR）不成立，详见 §3。

## 2. 判定表（28/28）

### milvus（12）

| case | 实验 tag (commit 日期) | fix PR | PR 状态 | merged_at | 判定 |
|---|---|---|---|---|---|
| 47763 | v2.6.10 (01-30) | #47782 | closed 未合并 | — | ✅ 不含 fix；但见 §3 |
| 49843 | v2.6.16 (05-12) | #50714 / #50731 | closed 未合并(3.0) / merged | 06-26 (master) | ✅ 不含 fix |
| 49890 | v2.6.16 (05-12) | #50195 | merged | 06-01 | ✅ 不含 fix |
| 50355 | v2.6.17 (05-16) | #3513 / #3514 | merged 2020-08 / 404 | 2020-08-29 | ⚠️ 文档修复，见 §4 |
| 51084 | v2.6.19 (06-25) | #51088 / #51168 | merged | 07-08 / 07-09 | ✅ 不含 fix |
| 51085 | v2.6.19 (06-25) | #51088 | merged | 07-08 | ✅ 不含 fix |
| 52307 | v3.0.0 (07-29) | #52261 | merged | 08-11 | ✅ 不含 fix |
| 52309 | v3.0.0 (07-29) | #52346 | merged | 08-11 | ✅ 不含 fix |
| 52311 | v3.0.0 (07-29) | #52346 | merged | 08-11 | ✅ 不含 fix |
| 52313 | v3.0.0 (07-29) | #52261 | merged | 08-11 | ✅ 不含 fix |
| 52315 | v3.0.0 (07-29) | #52261 | merged | 08-11 | ✅ 不含 fix |
| 52325 | v3.0.0 (07-29) | #52346 | merged | 08-11 | ✅ 不含 fix |

### qdrant（8）

| case | 实验 tag (commit 日期) | fix PR | PR 状态 | merged_at | 判定 |
|---|---|---|---|---|---|
| 9045 | v1.12.1 (2024-10-11) | #9070 | merged | 2026-05-19 | ✅ 不含 fix（1.12.1 远早于修复） |
| 9017 | v1.18.0 (05-11) | #9320 | merged | 06-08 | ✅ 不含 fix |
| 9039 | v1.18.0 (05-11) | #9058 | merged | 05-16 | ✅ 不含 fix |
| 9149 | v1.18.1 (05-22) | #9178 | merged | 06-05 | ✅ 不含 fix；**但审计已实证 bug 在 v1.18.1 不可复现 → GT 噪声**（既非 post-fix，也非真 bug） |
| 9421 | v1.18.2 (06-03) | #9431 / #9442 | merged / open | 06-25 | ✅ 不含 fix |
| 9520 | v1.18.2 (06-03) | #9526 | closed 未合并 | — | ✅ 不含 fix；但见 §3 |
| 9522 | v1.18.2 (06-03) | #9531 | merged | 07-15 | ✅ 不含 fix |
| 10120 | v1.18.3 (07-17) | #10128 / #10141 | merged | 08-08 | ✅ 不含 fix |

### weaviate（8）

| case | 实验 tag (commit 日期) | fix PR | PR 状态 | merged_at | 判定 |
|---|---|---|---|---|---|
| 11399 | v1.37.4 (05-14) | #11439 | **open 未合并** | — | ✅ 不含 fix；但见 §3 |
| 11400 | v1.37.4 (05-14) | #11439 | 同上 | — | ✅ 不含 fix；但见 §3 |
| 11401 | v1.37.4 (05-14) | #11429 / #11543 | closed 未合并 / **open** | — | ✅ 不含 fix；但见 §3 |
| 11729 | v1.38.0 (06-05) | #11824 | merged | 06-24 | ✅ 不含 fix |
| 11730 | v1.38.0 (06-05) | #11975 | **open 未合并** | — | ✅ 不含 fix；但见 §3 |
| 11732 | v1.38.0 (06-05) | #12457 | **open 未合并** | — | ✅ 不含 fix；但见 §3 |
| 11741 | v1.38.0 (06-05) | #11967 | **open 未合并** | — | ✅ 不含 fix；但见 §3 |
| 12041 | v1.38.2 (06-24) | #12049 | merged | 07-08 | ✅ 不含 fix |

## 3. 新发现：GT "TP_FIXED_PR" 标签存疑 → 已重审并降级（2026-08-14 用户重审）

核查中发现 8 个 case 的 fix PR 从未合并。经用户重审确认：

| case | 原 GT | 重审结论 | 新 GT |
|---|---|---|---|
| milvus 47763 | TP_FIXED_PR | fix #47782 未合并、issue 已关（2026-05-08）、用户确认未修 | **TP_ACK_CLOSED_NOFIX**（B 组） |
| weaviate 11399 | TP_FIXED_PR | fix #11439 open 未合并 | **TP_ACK_OPEN**（B 组） |
| weaviate 11400 | TP_FIXED_PR | 同 #11439 | **TP_ACK_OPEN**（B 组） |
| weaviate 11401 | TP_FIXED_PR | #11429 closed-unmerged + #11543 open | **TP_ACK_OPEN**（B 组） |
| weaviate 11730 | TP_FIXED_PR | fix #11975 open | **TP_ACK_OPEN**（B 组） |
| weaviate 11732 | TP_FIXED_PR | fix #12457 open | **TP_ACK_OPEN**（B 组） |
| weaviate 11741 | TP_FIXED_PR | fix #11967 open | **TP_ACK_OPEN**（B 组） |
| qdrant 9520 | TP_FIXED_PR | **实测复现：降级，见 §3.1** | **TP_ACK_OPEN**（B 组） |

已落地：cases_index.json 8 个 case group A→B、gt_category 更新（A=28→20，B=17→25；
recall 分母 A∪B=45 不变，三轮全部指标不变）。

### 3.1 qdrant 9520：行为实测证据（#9594 未修复，已降级）

用户认为 9520 已由 [qdrant#9594](https://github.com/qdrant/qdrant/pull/9594) 修复。
核查 + 实测证据：

1. **#9594 标题/正文与 9520 无关**："perf(edge): load ReadOnlyEdgeShard segments in parallel"——
   rayon 线程池并行加载 perf 优化，body 无 shard_number 校验/INT_MAX 字样。
2. **真正的修复 PR #9526**（"fix: add upper-bound validation for shard_number to prevent crash"）
   **closed 未合并**（2026-06-27 关闭）。
3. **issue 9520 仍 open**（closed_at=None），无 maintainer "fixed" 评论。
4. **行为实测（2026-08-14）**：用 probe_qdrant_9520.py 在 v1.18.2（不含 #9594）与
   v1.18.3（#9594 merged 之后，2026-07-17 tag）各跑一遍：

   | 版本 | INT_MAX shard create | create 后健康检查 | replication_factor=0 对照 |
   |---|---|---|---|
   | v1.18.2（基线） | **Read timeout 40s**（无校验、请求挂起） | 200 | 422 ✓ |
   | v1.18.3（含 #9594） | **Read timeout 40s**（同样挂起） | 200 | 422 ✓ |

   两版本行为完全一致——**#9594 之后缺陷仍可复现**（INT_MAX shard_number 无上限校验）。
   注：实测表现为请求挂起而非 issue 声称的 server crash（40s 超时内服务器未崩溃），
   但"缺少上限校验"这一缺陷本质成立，CONFIRMED 判定依据不受影响。
5. **结论**：9520 降级 TP_ACK_OPEN（B 组），已落地 cases_index.json。

## 4. 特殊 case：milvus 50355（文档修复）

fix #3513 是 2020-08 合并的**文档 PR**（"Clarify upsert behavior with autoID"，base=0.11.0），
#3514 已 404。50355 的缺陷是"文档声称支持 autoID=true 的 upsert，但 API 实际拒绝"。

- 代码行为：实验 tag v2.6.17 的 upsert-on-autoID 行为与 2020 年一致（从未改变）——"行为拒绝"成立。
- 缺陷的另一半是"文档声称支持"：2020 年修过文档，但 2.6.x 时代的文档是否再次声称支持，
  需在待办 2 的 probe↔issue 比对中一并验证（dev-reviewer 的 claim 对照物是"当前版本文档"）。
- 结论：无 post-fix 代码风险；claim 有效性取决于 2.6.17 文档现状，留给待办 2。

## 5. 方法论说明

- 判定依据是**日期比较**（PR merged_at vs tag commit date）+ base 分支。milvus 修复合 master、
  2.6.x tag 打自 2.6 分支——按日期比较会**高估** fix 覆盖（cherry-pick 到 2.6 分支只会更晚），
  因此"✅ 不含 fix"是保守结论：即使存在未知 backport，也不会早于 master 合并日。
- 本地 clone 是 shallow（depth=1），无法用 `git merge-base --is-ancestor` 精确判定；
  日期比较对本案已足够（全部修复晚于 tag 且差距 ≥ 5 天，最大 16 个月）。
- 数据缓存 `.paperpilot/phase2-rerun/pr_cache.json`，脚本 `audit_fix_versions.py` 可重跑。

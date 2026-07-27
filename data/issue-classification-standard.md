# TestVDB Issue 分类标准（TP / FP / Pending）

> `data/yihui504-issues-final.xlsx` 的 `final_verdict` / `TP_tier` 判定依据。
> 2026-07-26 全量核对 107 个 issue（GitHub labels + state_reason + closed_by + comments）后落地。
> **后续有疑问以此文件为准**；改判任一 issue 须同时更新此文件和 xlsx。

## 核心标准（跨 DB 一致）

判定按 **maintainer 对"bug 是否存在"的态度**，不是按"是否修复"：

| 判定 | 定义 |
|---|---|
| **TP** | maintainer **没明确否认 bug 存在**：accepted label、merged PR、open PR、要求重试/补充信息、"不值得修 / breaking change"（承认问题但不修）、maintainer 无互动且 tester 未撤回 |
| **FP** | maintainer **明确否认是 bug**（"by design" / "fine and expected" / "working as intended" / "correct behavior" / 解释当前行为 intended）**或** tester 撤回（TestVDB oracle 实现错误） |
| **pending** | maintainer 无任何互动（未裁决）：closed 无 label、open 但 maintainer 未评论 |

### 关键区分："不修" ≠ "否认 bug"

- **承认问题但不愿改**（breaking change / not worth it / wontfix low-priority）→ **TP**
- **否认问题存在**（working as intended / by design / fine and expected / 解释当前行为 correct）→ **FP**

**判据**：maintainer 是否在 comment 里**解释当前行为是 correct/intended**。是 → FP；否（只是说不修 / 要重试 / 嫌版本老）→ TP。

## 各 DB 的信号体系（label 体系每个 DB 不同）

| DB | 认可信号 | 拒绝信号（→ FP） |
|---|---|---|
| **milvus** | `triage/accepted` label | `resolution/by-design` label |
| **qdrant** | merged PR / open PR（几乎无 accepted label）| `state_reason=not_planned` + `wontfix` label + maintainer comment（"fine and expected" / "by design"）|
| **weaviate** | merged PR / open PR（label 多为 `bug`+`community`）| `state_reason=not_planned` + maintainer comment（"working as intended"）|

## TP_tier 子分类（xlsx 第 5 列）

| tier | final_verdict | 含义 | 真修复？ |
|---|---|---|---|
| `merged_fix` | TP | 官方 merged PR | ✓ |
| `open_pr` | TP | 官方 open PR 未 merge | 未修复（有方案） |
| `open_issue` | TP | open + accepted label | 未修复（maintainer 认可） |
| `manual_fix` | TP | maintainer 认可但未修复（stale bot 关 / maintainer 关无 merged PR） | ✗ **认可未修复** |
| `rejected_bydesign` | FP | maintainer 拒绝 / tester 撤回 | N/A |
| `no_response` | pending | maintainer 无互动 | N/A |

**`manual_fix` 叙事警示**：这些是 maintainer 认可（accepted label 或未否认）但被 stale bot 自动关闭、或 maintainer 关闭但无 merged PR 的 TP。**缺陷真实（被认可），但未修复**。论文计为 TP，但**不得表述为"已修复/修复证据"**——它们是"acknowledged but unfixed"。

## 规则例外（人工裁决，改判须在此登记）

| issue | 情况 | 裁决 | 理由 |
|---|---|---|---|
| milvus #47636 | maintainer 标 `triage/needs-information`，要求在新版本重试（嫌 2.3 太老），tester 未回复，stale bot 关 | **TP** | maintainer 没否认 bug，只说缺诊断价值；"needs retry" ≠ 否认 |
| qdrant #9420 | maintainer coszio "breaking change, I don't think it is worth it" | **TP** | 承认现状有问题（breaking change），只是不愿改；"不修" ≠ "否认" |

## 2026-07-26 全量核对记录

107 个 issue 逐个核对 GitHub（`/repos/{owner}/{repo}/issues/{n}` 取 labels + state_reason + closed_by；`/issues/{n}/comments` 取 maintainer 态度）。

| DB | xlsx TP | 核对后 TP | 误分处理 |
|---|---|---|---|
| milvus | 22 | 22 | #47636 裁决保留 |
| qdrant | 14 | 14 | #9420 裁决保留 |
| weaviate | 14 | **13** | **#11981 降级 TP→FP**（dudanogueira "working as intended, expected behavior doesn't hold"）|
| **合计** | 50 | **49** | 1 个误分修正 |

**最终**：49 TP + 23 FP + 35 pending = 107。maintainer-adjudicated = 49 TP + 23 FP = 72。

### TP 内部分布（核对后）
| tier | 数量 |
|---|---|
| merged_fix | 15（真修复）|
| open_pr | 16（有修复方案）|
| open_issue | 8（open + accepted）|
| manual_fix | 10（认可未修复：stale bot 关 / maintainer 关无 PR）|
| **TP 合计** | **49** |

## 关联文件
- `data/yihui504-issues-final.xlsx` — 107 issue 权威账本（db / number / url / title / final_verdict / TP_tier / verdict_reason）
- `paper/RQ-results-summary.md` — RQ 结果汇总（**注意**：此文件的旧 TP 细分 "36 confirmed (32 ack + 4 merged) + 14 open-PR" 已过期，以本标准的 tier 分布为准）
- 核对脚本：GitHub REST API（需 token，禁代理：`session.trust_env=False`）

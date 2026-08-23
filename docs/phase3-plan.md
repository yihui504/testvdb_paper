# TestVDB 缺陷检测能力实验方案

## 一、已完成：全量 issue 采集与人工整理

对 TestVDB 历史提交的全部 issue 逐条做了去重、补全和人工核对（证据来源：issue comments / events / timeline 的 cross-referenced PR），得到最新数据（2026-08-13 人工核对版）：

- **总样本 126 条**（124 issues + 2 自提修复 PR），覆盖 Milvus 63 / Qdrant 33 / Weaviate 30
- **真 bug 45 条**：28 已修复（merged PR 证据）+ 17 确认未修复（8 open-accepted + 6 closed-nofix + 3 duplicate）
- **假阳性 26 条**：16 by-design + 8 FP-by-design + 2 不可复现
- **未裁定 53 条**：maintainer 未显式回复

在此样本集上已跑完 confirmation 阶段评估（LLM 写提供给 dev_reviewer agent 的输入文件 + GLM5.2 agent 盲评）：真 bug 召回 **42/45 = 93.3%**。这是 oracle 上界——probe 人工编写，只测判定/确认阶段。

## 二、要设计：bug detection capability 端到端实验

detection capability 是**端到端、controlled** 的能力量化：工具自己在 bug 真实存在的版本上挖掘，记录能挖到多少已知 bug、第几轮挖到。

**实验对象**：45 个 GT 真 bug，各自定位到"bug 真实存在的 DB 版本"。
- 28 已修复（A 组）：由 fix PR 的 merged_at 定位到修复前一个 release tag（GitHub API 自动 + 人工 probe 确认复现）
- 17 未修复（B 组）：报告版本即存在版本

**实验流程**：在每个存在版本上跑 TestVDB 端到端全 pipeline（文档 → 契约 → 生成探针 → 执行 → 判定），多轮迭代深化，最多 30 轮。

采用 Ground_Truth-informed 策略：主进程知道目标 bug，每轮开始前检查是否所有 bug（特指该数据库该版本想测的所有已知 bug）都被挖到了，如没被全挖到，在新一轮派发测试脚本生成 agent 时，注入提示"你所负责的方向还存在没被挖掘到的 bug，可能是因为你写的脚本质量不够好或你还没有覆盖到所有的测试方向"，催其深入测试，但不向生成器泄露任何 bug 的具体特征（endpoint/param/预期行为）。

**核心指标**：
- **reach rate**：工具挖到多少已知 bug（45 的几分之几）= detection capability
- **首达轮次分布**：每个 bug 第几轮被挖到（做成"第 n 轮发现 bug X"的表）
- **与 oracle 上界差距**：forward reach vs 93.3%，差值归因 generation 阶段损失

**Ground_Truth 对齐**：每轮产出由 LLM 盲评对齐到 Ground_Truth bug，全部完成后人工复核。

**性质声明**：Ground_Truth 仅用于"是否全 reach"的续挖判定与催促，不向生成器透露 bug 具体特征，本质上是试图防止运行提前结束，更好地测试在给足够轮次的情况下到底能不能挖出来。

**文档与契约控制（实验有效性保障）**：reach 是端到端数，须把"上游信息损失"与"生成能力"分开，否则漏检分不清归 extractor 还是 generator。
- **文档可达性门控**：对每个 GT bug 判其触发条件（端点/参数/边界）在该版本官方文档中是否存在。文档无 → 标 `doc-blind`，移出 reach 分母单独报告（文档锚定检测器的目标类不含此类 bug；race/distributed 特殊 bug 自然落此）；文档有 → `doc-attainable`，进分母。
- **契约提取完整性**：对 doc-attainable bug，各写一条"能暴露该 bug 的最小 contract claim"（oracle claim），查工具真实提取的 contract 是否含等价 claim。有 → 漏检归 generation loss；无 → 归 extraction loss。reach 损失 = doc-blind + extraction loss + generation loss，可干净归因。
- **不手工补全文档/契约**：headline reach 用工具真实的爬虫与 extractor 输出；手工补全等于变 oracle 上界。extractor 丢损是工具真实能力的一部分，量它、归因它，不藏它。
- **（消融）oracle-contract run**：若 reach 偏低，喂含全部 GT claim 的 oracle contract 替代自动提取的 contract。real-contract reach 与 oracle-contract reach 之差 = 纯提取损失；oracle-contract reach 与 93.3% 之差 = 纯生成损失。

## 三、配套插件改造

现有插件为"实际使用降本"设计，带三个提前停止 + 一个查重 gate，直接跑会在挖到全部 bug 前提前停、或把我们的 GT bug 当重复过滤掉。需做以下针对性改造：

| # | 改造 | 原因 |
|---|---|---|
| 1 | 轮次上限 5 → 30 | 实验目标是 reach 全部已知 bug，5 轮易中途停止，低估工具能力 |
| 2 | 删除"覆盖率 ≥ 95% 停止" | 覆盖率达标 ≠ bug 全 reach（边界值没选对仍会漏），实验目标是 bug reach 不是覆盖率 |
| 3 | 删除"连续 5 轮无新缺陷停止" | GT-informed 深化可能在连续空轮后突破（生成器换策略），5 轮太保守 |
| 4 | 关闭 novelty gate 查重 | GT bug 是我们自己提交的，查重会把它们全判为"已报告"过滤掉，reach 直接归零（最易漏、最致命） |
| 5 | 注入 GT-informed 续挖提示 | 每轮检查未全 reach 时，给生成器注入"你的方向还有没挖到的 bug，脚本质量或覆盖不够"的催促，不泄露 bug 具体特征 |
| 6 | 多版本 batch 包装 | 现有只支持单库单版本挖掘，实验要跨约 10 个存在版本，无现成 batch 入口 |
| 7 | agent maxTurns 300 → 500 | 深化挖掘别在单轮内触顶截断 |
| 8 | 跨版本禁用缓存 | 每版本用该版本文档独立 formalize，避免跨版本混用契约 |

改造集中在主进程 orchestrator（commands/mine.md）、收敛逻辑（scripts/reconstruct_context.py）、novelty gate（scripts/novelty_gate.py）三处。最小改动约 10 行（#1/2/3/4/7/8），含 GT hint 注入约 50 行。

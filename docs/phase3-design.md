# Phase 3 实验方案：Forward Mining Reachability（GT-informed Iterative Deepening）

日期：2026-08-13 | 状态：方案稿，待确认后 pilot
定位：**论文新 RQ2 的 headline 实验**（detection capability 端到端 forward）；confirmation-only（93.3%）退为 upper-bound ablation。
实现依据：`C:\Users\11428\Desktop\mftui\TestVDB`（orchestrator = `commands/mine.md`，收敛 = `scripts/reconstruct_context.py`，gate = `scripts/novelty_gate.py`）。

---

## 0. 核心判断（为什么这个 framing 对）

- 工具的原生任务是 **forward 挖掘**（documentation → defect），不是 reverse 判定。detection capability 的本意就是"forward 能挖到多少"，所以实验**不改工具的根本任务**，只解除"为实际使用降本而加的提前停止"。
- 工具**本就是多轮**（Stop hook 驱动跨 Turn 循环 + reflection_context 轮间传递），iterative deepening 不是新建，是**放开 + 引导**。
- 因此改造小而集中：移除 3 个提前停止条件 + 关 novelty gate + 注入 GT hint + batch 包装。

---

## 1. 研究问题

**RQ2（headline）**：TestVDB 端到端 forward 挖掘，在已知缺陷真实存在的 DB 版本上，经 GT-informed iterative deepening，能 reach 多少已知缺陷？首达轮次分布如何？

**辅问**：相比 oracle 上界（confirmation-only 人工 probe，recall 93.3%），工具自动 forward 的 generation 阶段损失多少？

---

## 2. 实验对象

45 个 GT 真 bug（Phase 1 maintainer 裁定，A∪B）：
- **A（28 fixed）**：fix PR merged，需 fix-前版本
- **B（17 ack-unfixed）**：reported 版本即存在版本

**3 条特殊标注**（保留在分母，单独分析）：
- `#47635`（race）/ `#9045`（distributed panic）：forward 也是 standalone docker，预期不可 reach → 标 `standalone-unreachable`，量化工具有效分母
- `#9149`（GT 存疑，1.17.1/1.18.0/1.18.1 三版本都已校验）：Phase 1 复核；若改 FP 则分母 −1

---

## 3. 存在版本定位（自动 + 人工确认）

**A 组（28）**：fix PR merge_at → 该 merge commit 所属 release 的**前一个 release tag**
- 自动：GitHub API（PR `merged_at` + releases timeline），复用 `#9149`/`#9045` 已验证的方法
- 人工确认（关键，不可省）：对每条 fix-前 tag，用 Phase 2 probe 在该 tag 上**实跑确认 bug 复现**（bug 不在则再往前找）。这步排除"fix 其实更早合入"的定位偏差
- 产出：`phase3/presence-versions.csv`（bug, vendor, fix_pr, merge_at, presence_tag, confirmed_by_probe）

**B 组（17）**：reported_version 即存在版本（bug 未修，Phase 2 probe 已确认其中可触发部分）

---

## 4. Documentation（该版本，严谨）

- 每个存在版本对应版本的官方文档，工具 `knowledge-extractor` 按版本 tag 爬
- milvus/qdrant/weaviate 文档随版本变化，**不用最新文档近似**（boundary 细节对 bug 定位敏感）
- 跨版本 contract 不复用（每版本独立 formalize）

---

## 5. 工具改造（核心；基于实现摸底）

### 5a. 移除提前停止（3 处）

| 机制 | 位置 | 现值 | 实验改 | 理由 |
|---|---|---|---|---|
| 轮次上限 | `commands/mine.md` (默认参数) | `max_rounds=5` | `15` | 给 deepening 足够深度，但非真无限（控成本） |
| 覆盖率达标停 | `scripts/reconstruct_context.py:223` | `>=95%` 停 | 删除条件 / 改 `99.9%` | 覆盖率达标 ≠ bug 全 reach |
| 连续无新缺陷停 | `scripts/reconstruct_context.py:221` | `consecutive_no_defect>=5` 停 | 删除条件 / 改 `999` | deepening 早期可能连续空轮后再突破 |

### 5b. 关闭 novelty gate（**最易漏、最致命**）

- 位置：`scripts/novelty_gate.py`
- **必须关**：novelty gate 查 GitHub 已报告缺陷做查重。我们的 GT bug **就是我们提交的**，novelty gate 会把它们全部判为"已报告"过滤掉 → reach 直接归零
- 改：实验模式跳过 GitHub 查重（gate 直接放行，或 bypass）

### 5c. GT-informed hint 注入

- 位置：`commands/mine.md` 的 attack agent 派发 prompt（含 `reflection_context`）
- 每轮主进程对照 GT，把 `(GT_in_version − reached)` 作为 reflection_context 的字段喂 generator
- prompt 形如："本轮前已 reach：[...]；仍未 reach 的已知缺陷特征：[bug #X: endpoint=E, param=P, 预期拒绝/溢出/...]；请针对这些端点与参数深入生成定向探针"
- **性质声明**：这是 oracle-guided deepening（工具知 GT 知答案方向），reach 是"工具在 oracle 提示下的能力上界"。论文必须诚实标注，不能冒充 blind forward

### 5d. batch 包装（新增）

- 无现成 batch 入口，写 shell/Python 循环跑 ~10 存在版本
- 每版本一次 `/testvdb:mine`，独立 session_dir

### 5e. 其他放宽

- agent `maxTurns` 300 → 500（深度挖掘别触顶）
- 缓存：contract/intel 每版本首次生成，跨版本禁复用
- multi-run：工具本就单 run，固定单 run 控成本（不 ensemble）

---

## 6. iterative deepening 流程（GT-informed）

```
for (vendor, version) in 存在版本集 (~10 组):
    doc = crawl_doc(vendor, version)
    contract = formalize(doc)                       # Phase1 一次
    GT_v = GT bugs whose presence tag == version
    reached = {}
    for round in 1..15:
        if |reached| == |GT_v|: break
        reflection = { reached, remaining: GT_v - reached,
                       prev_rejection_patterns, exhausted_endpoints }
        candidates = mine_round(contract, version, reflection)
                    # attack(boundary/state/semantic/vein) → execute → judge
        new_reach = align(candidates, GT_v - reached)   # LLM 对齐(§7)
        reached |= new_reach
        record [bug -> 首达轮]
    record per-version reached / GT_v
```

终止：`|reached| == |GT_v|`（该版本全 reach）或 max_rounds=15。

---

## 7. GT 对齐（LLM 先评 + 全部完成后人工验证）

- 每轮 candidate set → LLM 判每个 candidate 对应哪个 GT bug
  - 对齐键：`endpoint + param + observed-behavior` vs GT bug 的 contract claim
  - LLM **blind**：不知 candidate 来自哪轮、不告诉它 GT 标签，只判语义匹配（候选 X 是否在描述 bug Y 的行为）
  - 输出：`candidate → matched_gt_bug | "no_match"`（no_match = 工具挖到 GT 之外的新缺陷，bonus 记录，不计 reach 分母）
- **全部版本全部轮次完成后**，人工验证 LLM 对齐：
  - 全量过一遍（45 bug × 各自首达轮的 candidate）
  - 争议/边界条目复核
  - 产出最终 reach 表

---

## 8. 指标

- **reach rate** = Σ_versions reached / 45（headline detection capability）
- **首达轮分布**：median / mean / max + 直方图
- **累积 reach 曲线**：每轮 Σ reached（per-version + 总）
- **per-vendor reach**：milvus / qdrant / weaviate
- **vs upper bound**：forward reach rate 对比 confirmation-only 93.3%；差值 = generation 阶段损失

---

## 9. 输出

1. **主表**：bug × {vendor, 存在版本, R1..R15 reach 标记, 首达轮, 备注(standalone-unreachable/GT 存疑)}
2. **汇总表**：reach rate（总体 + per-vendor）+ 首达轮统计 + vs upper-bound
3. **图**：累积 reach 曲线（x=轮次, y=累积 reach 数）
4. **bonuses 表**：工具挖到的 GT 之外新缺陷（novelty，不计 reach，但展示工具持续进化）

---

## 10. pilot → 全量

**pilot**（先做）：1 版本 + GT-informed 3-5 轮
- 候选：milvus v2.6.12（含 B 组未修 bug #49059 等，Phase 2 已确认 probe 能触发）
- 验证：改造落地（提前停移除 / novelty 关 / hint 注入接口通）、LLM 成本量级、reach 机制可观测
- 决策门：
  - pilot reach（该版本内）> 50% 且成本可控 → 全量
  - pilot reach < 20% → generator 即使有 hint 也 reach 不了，回头改 generator 策略（如加定向复现模式）再试
  - 成本爆炸 → 调 max_rounds / 收紧 hint

**全量**：45 bug × ~10 存在版本 × 最多 15 轮 × 单 run

---

## 11. 论文位置

- **RQ2 headline** = forward reachability（reach rate + 首达轮表 + 累积曲线）
- **一段** confirmation-only 作 upper-bound ablation（93.3%），对照 forward reach，量化 generation 损失
- **limitations** 显式声明：
  - GT-informed iterative = oracle-guided deepening（reach 是工具在 oracle 提示下的能力上界，非 blind forward）
  - standalone-unreachable 类（race / distributed）在 forward 同样受限
  - novelty gate 关闭意味着 reach 不含"新颖性过滤"维度

---

## 12. 成本与风险

- **LLM 成本**：~10 版本 × ≤15 轮 × 多 agent × 单 run。pilot 先实测单版本单轮成本再外推
- **成本控制**：max_rounds=15（非无限）、单 run、novelty 关（减 gate 调用）、reflection 紧凑
- **风险**：
  - GT-informed 偏 oracle → 论文声明 + 可补一个 blind 变体作对照（若时间允许）
  - generator 有 hint 仍 reach 不了 → pilot 早暴露
  - 对齐噪声 → LLM + 人工两阶段
  - 存在版本定位错 → 人工 probe 确认兜底
  - #9149 GT 存疑 → Phase 1 复核

---

## 13. 已确认决策（与导师/用户对齐）

| 决策点 | 选择 |
|---|---|
| iterative 方式 | **GT-informed**（催 generator 时知未 reach bug） |
| 存在版本定位 | 自动 + **人工 probe 确认** |
| documentation | **该版本文档**（严谨，不近似） |
| GT 对齐 | **LLM 先评 + 全部完成后人工验证** |
| 改造重点 | orchestrator（mine.md）+ 收敛（reconstruct_context.py）+ novelty gate |

---

## 14. 执行顺序（待方案确认）

1. 存在版本自动定位（A 组 28，GitHub API）+ 人工 probe 确认 → `presence-versions.csv`
2. 工具改造（5a-5e）+ 改造自测
3. **pilot**（milvus v2.6.12，3-5 轮）→ 决策门
4. LLM 对齐 + 人工验证 pilot 结果
5. 全量（~10 版本）
6. 汇总 + 论文 RQ2 headline（替换 confirmation-only 定位）

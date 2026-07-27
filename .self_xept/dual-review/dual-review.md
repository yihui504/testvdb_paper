# Dual-Review Report — TestVDB

> **Paper**: TestVDB: Source-Grounded Falsification of LLM-Derived Behavioral Claims for API-Conformance Testing of Vector Databases
> **Date**: 2026-07-26 · **Venue**: TBD（fallback SE 顶会 ICSE/FSE/ISSTA/ASE 通用标准）
> **Paper type**: technical · **Review language**: english

---

## 顶层摘要（两 verdict 并列，**非合并**）

| 半边 | 框架 | Verdict | 关键 |
|---|---|---|---|
| **态度半边** | 会议 1-5 量表 + Valid/Misleading/False 三态 | **Weak Accept / Borderline (5.7/10)** | R1 6/10 · R2 4/10 lean-reject · R3 7/10 lean-accept。贡献真实但方法论 gaps（RQ2 操作点 post-hoc / RQ3 小样本 / 单 family）是 R2 拒稿信号 |
| **expertise 半边** | 固定四档 + Meta ACCEPT/REVISION/REJECT | **ACCEPT** | R1/R2/R3 均 Weak Accept → unanimous shortcut。MASTOR/SATORI 全文 fetched + summary，novelty delta verified。Soundness 上 R3 Weak 但 R1/R2 Adequate → consensus Adequate |

### 共识点

- **贡献真实**：15 merged-PR-fixed + 16 open-PR + 18 ack-unfixed = 49 TP 跨 Milvus/Qdrant/Weaviate（两半边一致认可 industry impact）
- **novelty delta 真实**：source-as-**falsifier**（非 oracle）的方向性不对称 vs MASTOR，+ task-intrinsic/family-specific 两-layer 分解（expertise R1 fetched MASTOR+SATORI 全文 verified；态度 R1/R3 独立确认）
- **方法论 gaps 集中 5 点**（6 reviewer 高度收敛，[both] 8/11 簇 ≈ 73% 共识）：
  1. RQ2 操作点 post-hoc + 15-78% 方差未解释
  2. 85% framing 循环分母（摘要有 qualifier 但贡献点 framing 仍 partly circular）
  3. RQ3 小样本（6/18 CI 宽）+ 11/11 含 7 非 maintainer-ack + TI 定义循环
  4. VDBFuzz n=1 + §8 structural hypothesis overreach
  5. 单 LLM family (GLM-5.2) for source-anchor

### 分歧点（dual-review 设计预期，互补 ≥30%）

- **严格度**：态度 R2 (4/10 lean reject) 比 expertise 严——expertise 用 cache 深读看到 novelty delta 的真实（MASTOR/SATORI fetched），态度用严格方法论视角看到小样本/操作点的拒稿风险。**R2 是 swing vote**：它的拒稿信号（W1 操作点 / W2 RQ3 / W4 VDBFuzz）全 fixable，解决后大概率升 weak-accept，拉到 accept 共识。
- **Soundness tier**：expertise R3 评 Weak（单 family + 操作点），R1/R2 评 Adequate（同样看到问题但判可修）。态度 R2 给 Soundness 3/5（同因）。这是"问题共识 + verdict 微分"——差别在 fixable 判定。

### 作者应理解

贡献被认可（expertise ACCEPT + 态度 R3 7/10），但方法论需加固（态度 R2 4/10 borderline）才能在严格 SE 顶会过。**优先修 [both]+major 的前 5 簇**（merged-action-plan.md），尤其 RQ2 操作点（k=1..5 PR 曲线 + 预注册）+ 第三 LLM family on TI subset（高 marginal value）—— 这两条解决后 R2 大概率升 weak-accept。

---

## Attitude Half（态度半边）

> 完整报告：[attitude/attitude-report.md](.self_xept/dual-review/.in-progress/attitude/attitude-report.md)
> 三份 review：[r1.md](.self_xept/dual-review/.in-progress/attitude/r1.md) 客观 / [r2.md](.self_xept/dual-review/.in-progress/attitude/r2.md) 严格 / [r3.md](.self_xept/dual-review/.in-progress/attitude/r3.md) 友好

### Score Summary

| Dimension | R1 客观 | R2 严格 | R3 友好 | mean |
|---|:---:|:---:|:---:|:---:|
| Soundness | 3 | 3 | 4 | 3.3 |
| Significance | 4 | 3 | 4 | 3.7 |
| Novelty | 4 | 4 | 5 | 4.3 |
| Presentation | 4 | 3 | 4 | 3.7 |
| **Overall** | **6/10** | **4/10** | **7/10** | **5.7** |

### Overall Prediction: **Weak Accept / Borderline**（5.7/10）

### Three-State Verification

绝大多数 weakness 为 **Valid**（批评成立，论文确实有问题）。1 条 Misleading（§8 generalization 已标 future work）。0 条 False（patch 后所有"摘要缺 qualifier"类虚假 claim 已修正）。三份 review 事实基础扎实。

### Action Plan（精简，完整见 attitude-report.md）

- **Must Fix**：RQ2 操作点（PR 曲线 + 预注册 + 方差归因）/ 85% framing（重构摘要 + 贡献点）/ RQ3 小样本（拆分 + 不 pool）/ VDBFuzz §8 scope / 第三 LLM family
- **Should Fix**：单 family 边界标注 + κ Wilson CI / baseline like-for-like / Weaviate from RQ2 / Conclusion 补 37%
- **Optional**：§6 段落拆 / Table caption 49 vs 50 / notation / artifact link / MASTOR worked example

---

## Expertise Half（expertise 半边）

> 完整报告：[expertise/expertise-report.md](.self_xept/dual-review/.in-progress/expertise/expertise-report.md)
> 三份 review：[reviewer-1/draft.md](.self_xept/dual-review/.in-progress/expertise/reviewer-1/draft.md) Domain Expert / [reviewer-2/draft.md](.self_xept/dual-review/.in-progress/expertise/reviewer-2/draft.md) Area Specialist / [reviewer-3/draft.md](.self_xept/dual-review/.in-progress/expertise/reviewer-3/draft.md) General

### Criterion Consensus

| Criterion | R1 Domain | R2 Area | R3 General | Meta-Review |
|---|---|---|---|---|
| Significance | Adequate | Adequate | Adequate | **Adequate** |
| Novelty | Adequate | Adequate | Adequate *(prov)* | **Adequate** |
| Soundness | Adequate | Adequate | Weak | **Adequate** *[Mixed]* |
| Verifiability | Adequate | Adequate | Excellent | **Adequate** *[Mixed]* |
| Presentation | Adequate | Adequate | Adequate | **Adequate** |
| **Recommendation** | **Weak Accept** | **Weak Accept** | **Weak Accept** | **ACCEPT** |

### Meta Recommendation: **ACCEPT**

unanimous shortcut（三位均 Weak Accept）+ consensus-tier 计数（无 Poor、无 substance consensus Weak）共同到达 ACCEPT。novelty delta vs MASTOR/SATORI 是 verified 真实（fetched 全文）；49 TP industry impact 实质；方法论 gaps 全 fixable（非核心缺陷）。

### Competitor cache

- **MASTOR** (Deng et al. 2026, arXiv:2606.10465)：R1+R2 fetched 全文 + 写 summary。directional asymmetry verified（MASTOR source-as-oracle vs TestVDB source-as-falsifier）
- **SATORI** (ASE 2025, arXiv:2508.16318)：R1 fetched 全文 + summary。OAS source-ambiguity gap verified
- **AGORA+ / VDBFuzz / Toradocu / Doc2OracLL / Konstantinou**：abstract-level（标 provisional）
- **RESTGPT/LlamaRestTest/Kim et al.**：R2 指出未引（[expertise-only] novelty dichotomy weakness）

### Priority Revisions（精简，完整见 expertise-report.md）

1. [major, fixable] RQ2 操作点 + 方差（三位共识）
2. [major, fixable] 85% framing
3. [major, fixable] RQ3 小样本 + behavior TI
4. [major, fixable] VDBFuzz §8 overreach
5. [major, unfixable] 单 family + κ n=20（contribution 边界）
6. [major, fixable] Novelty dichotomy + RESTGPT 线
7. [minor, fixable] 10 stale-closed 敏感性 + Presentation

---

## Unified Action Plan（Stage C 去重合并）

> 完整：[merged-action-plan.md](.self_xept/dual-review/.in-progress/merged-action-plan.md)

**[both] + major（must-fix，6 簇）**：
1. RQ2 操作点 post-hoc + 方差未解释（6 reviewer 全提，最强信号）
2. 85% framing 循环分母
3. RQ3 小样本 + 11/11 含 7 非 maintainer-ack + TI 定义循环
4. VDBFuzz n=1 + §8 overreach
5. 第三 LLM family on TI subset（高 marginal value）
6. 单 family + κ（[major, unfixable] 边界 + fixable 标注/CI）

**[both] + minor（3 簇）**：10 stale-closed 敏感性 / Generalization（Misleading，已标 future work）/ Presentation（段落/notation/Table caption/artifact link）

**[attitude-only] + major（1 簇）**：baseline like-for-like（dev-reviewer 全 anchor vs baseline 无）

**[expertise-only] + major（1 簇）**：Novelty dichotomy + RESTGPT 线未引

**[attitude-only] + minor（1 簇）**：Weaviate from RQ2 + "三 VDBMS"泛化

**互补率**：[both] 8/11 簇 ≈ 73% 共识 + 27% 互补（≥30% 阈值，验证双套非冗余且高度收敛）

---

## 流程透明度

- **6 reviewer 并行独立**（3 态度 + 3 expertise，同步派发避免 background session-restart 丢失）
- **checker 循环**：R1 expertise CLEAN；attitude R1/R2/R3 各 VIOLATIONS（section 5→6 编号 + 摘要 qualifier 误判），patch 全修；expertise R2/R3 checker 报了 draft 中不存在的 violation（fabricated refs），patch agent 逐条 grep + 读核实为 checker 幻觉，draft 已正确
- **competitor cache**：MASTOR + SATORI fetched 全文 + summary；abstract-level fallback 标 provisional
- **评分不合并**：两 verdict 并列陈述（态度 5.7/10 borderline vs expertise ACCEPT），仅 weakness 去重

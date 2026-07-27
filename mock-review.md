# Mock Review Report
> **Target Venue:** TBD → SE top conference (ICSE/FSE/ISSTA/ASE) · **Overall Prediction:** Weak Accept / Borderline (6.3/10) · **Date:** 2026-07-27
> 论文：TestVDB v3（PPT v2.3 驱动重写，6 页）。3 reviewer 客观/严格/友好独立审稿 + 主 agent 三态核实。

## Score Summary

| Dimension | R1 客观 | R2 严格 | R3 友好 | mean |
|---|:---:|:---:|:---:|:---:|
| Soundness | 4 | 3 | 4 | 3.7 |
| Significance | 4 | 4 | 4 | 4.0 |
| Novelty | 4 | 4 | 4 | 4.0 |
| Presentation | 4 | 4 | 5 | 4.3 |
| **Overall** | **7/10** | **4/10** | **8/10** | **6.3** |
| Confidence | 4/5 | 4/5 | 4/5 | 4/5 |

**Overall Prediction: Weak Accept / Borderline (6.3/10)**。R1/R3 weak-accept，R2 lean-reject（post-hoc 操作点 + 统计力）。R2 的拒稿信号（W1 操作点 / W2 κ / W4 multi-perspective）全 fixable——加展开 + 标 limitation 可拉回 weak-accept 共识。

## Reviewer 1

**Overall:** 7/10 (weak accept) · **Confidence:** 4/5
**Summary:** TestVDB 用 4 步 LLM pipeline 检测 VDBMS documentation-implementation defects，dev-reviewer 作 source-grounded falsifier 抑制 FP。107 submitted / 49 TP / 15 merged-PR。dev-reviewer 在 48-candidate retrospective 上 67% prec / 74% recall（vs 37% baseline）。VDBFuzz 双向对比互补覆盖。

**Strengths:** (1) Table 1 oracle 排除论证清晰；(2) 107 issues / 49 TP / 15 merged-PR 实际影响；(3) FP 双模式诊断（hallucination + self-preference）+ multi-perspective 结构性不足；(4) dev-reviewer 3-check 设计 + ablation 隔离 anchor 贡献；(5) 透明报告 post-hoc + variance。

**Weaknesses:**
- **[major, fixable]** RQ2 external validity：48 candidates 仅 Milvus+Qdrant，Weaviate yield-only
- **[major, fixable]** RQ3 n=1 bidirectional 统计力不足；abstract "clarifies what each tool reaches" 比 data 强
- **[minor, fixable]** post-hoc operating point 未对比其他（如 3-run majority）
- **[minor, fixable]** abstract "cannot adjudicate" 比 Table 1 "miss" 强（oversell）
- **[minor, fixable]** impl-as-correct 假设循环论证（15 merged-PR 是 doc 对 impl 错的案例）

完整 review：[`.self_xept/mock-review-r1.md`](.self_xept/mock-review-r1.md)

## Reviewer 2

**Overall:** 4/10 (lean reject) · **Confidence:** 4/5
**Summary:** 技术贡献扎实（source-grounded falsification），问题真实（49 TP / 15 merged-PR）。但 evaluation 有 post-hoc 特征（操作点选择 + cross-model 样本选择）削弱置信度。multi-perspective baseline 未充分 specified。

**Strengths:** (1) VDBFuzz vs doc-impl 区分清晰，#49823 case 有效；(2) FP 双模式 + multi-perspective 结构性不足（80% prec / 15% recall）作 baseline 合理；(3) 49 TP / 15 merged-PR 实际影响；(4) Table 1 系统排除论证。

**Weaknesses:**
- **[major, fixable]** RQ2 post-hoc 操作点（selection bias + 无 pre-registered rule；Wilson CI 未含 selection uncertainty）
- **[major, unfixable]** cross-model κ=1.0 on 20 统计力不足（Wilson [83,100] + selection bias + 不估 recall）
- **[major, fixable]** VDBFuzz template limitation 未独立验证（未跑 wait=false seed）
- **[major, fixable]** multi-perspective baseline 未展开（80%/15% 无 judge 设计 / voting rule / operating point 细节）
- **[minor, unfixable]** 6 页偏短（SE 顶会 9-12 页；RQ2/RQ3 展开受限）

完整 review：[`.self_xept/mock-review-r2.md`](.self_xept/mock-review-r2.md)

## Reviewer 3

**Overall:** 8/10 (weak accept) · **Confidence:** 4/5
**Summary:** 重要 timely 问题 + 4 步 pipeline + dev-reviewer 设计有方。107/49/15 跨 3 VDBMS 实质影响。FP 分析 methodical，dev-reviewer 真改善（74% vs 37% recall）。写作清晰，scope 良定义，对 limitation 诚实。

**Strengths:** (1) 问题定义 + Table 1 排除论证；(2) 107/49/15 + 68.1% yield 实际价值；(3) FP 双模式诊断 + dev-reviewer 3-check + ablation（source alone 75% FP 抑制）；(4) honest threat reporting（15-78% variance + post-hoc 标注 + κ=1.0 + RQ3 n=1 承认）；(5) 3 RQ 结构清晰。

**Weaknesses:**
- **[major, fixable]** ground truth 局限（non-random + 无 unbiased catalog；single-run 15-78% variance 大）
- **[major, fixable]** VDBMS 外泛化无证据（REST/config/policy 仅 claim，无 case study）
- **[major, fixable]** RQ3 n=1 exploratory（silent-accept miss 可能是 template 覆盖非本质）
- **[minor, fixable]** cost/scalability 细节稀疏（~$10/target 无 token breakdown）

完整 review：[`.self_xept/mock-review-r3.md`](.self_xept/mock-review-r3.md)

## Verification

主 agent 回剥注释后论文逐条核实 weakness 批评是否成立（Valid/Misleading/False）：

| # | Source | Claim（weakness 摘要） | Verdict | Note |
|---|---|---|---|---|
| 1 | R1-W1/R2-W1 | RQ2 post-hoc operating point（selection bias）| **Valid** | §6 RQ2 Table 确实报告 4 操作点 + 选 3-run，标 post-hoc 但无 pre-registered rule |
| 2 | R1-W2/R2-W3/R3-W3 | RQ3 n=1 bidirectional 统计力 | **Valid** | §6 RQ3 确实 n=1/direction，标 hypothesis-generating，但 abstract "clarifies" 略强 |
| 3 | R2-W2/R3-Q4 | cross-model κ=1.0 on 20 统计力 + selection bias | **Valid** | §6 RQ2 确实 κ=1.0 on 20（Wilson [83,100]），threats 承认不估 recall |
| 4 | R2-W4 | multi-perspective baseline 未展开（80%/15% 无细节）| **Valid** | §4 确实只 2 句描述，无 judge 设计/voting rule |
| 5 | R1-W3 | post-hoc 操作点未对比其他 | **Misleading** | Table 报告了 4 操作点（含 majority 64/26），但无"为何选 3-run"的定量规则 |
| 6 | R1-W4 | abstract "cannot adjudicate" oversell | **Valid** | abstract 确实说 "cannot adjudicate"，比 Table 1 "miss" 强 |
| 7 | R1-W5 | impl-as-correct 循环论证 | **Valid** | §8 确实只说 "15 merged-PR suggest"，无 false negative 分析 |
| 8 | R2-W5 | 6 页偏短 | **Valid** | 6 页确实短于 SE 顶会 9-12 页 |
| 9 | R3-W1 | ground truth 局限（non-random）| **Valid** | §6 threats 确实承认 non-random |
| 10 | R3-W2 | VDBMS 外泛化无证据 | **Valid** | §8 确实只 future work，无 case study |
| 11 | R3-W4 | cost/scalability 细节稀疏 | **Valid** | §3 LLM automation 确实只 ~$10 + 10^4 calls，无 breakdown |

**核实结论**：10/11 **Valid** + 1 **Misleading**。0 **False**——三份 review 事实基础扎实，所有批评都指向论文真实存在的点（多数因 6 页篇幅未展开）。

## Action Plan

### Must Fix

- **[major, fixable] RQ2 post-hoc 操作点**（R1+R2 共识）：加 pre-registered rule 或明确"基于 falsifier semantics 选 high-recall + precision ≥60%"，report selection-aware CI。§6 加"为何选 3-run 而非 5-run/majority"的定量分析。
- **[major, fixable] RQ3 n=1 降调**（R1+R2+R3 共识）：abstract/conclusion 的 "clarifies what each tool reaches" 改为 "explores complementary coverage"；§8 加 "n=1 per direction, structural-asymmetry hypothesis future work"。
- **[major, fixable] multi-perspective baseline 展开**（R2 单提但重要）：§4 加 1 段 + 小表，含 4 judge 角色、voting rule、为何 15% recall 是 operating point。
- **[major, fixable] cross-model κ=1.0 标注 limitation**（R2+R3）：§6 threats 加 "n=20 非随机 + Wilson [83,100] 含 moderate family-specificity 可能 + 不估 recall"。
- **[major, fixable] abstract 降调 oracle exclusion**（R1-W4）："cannot adjudicate" → "existing instantiations miss the residual"。

### Should Fix

- **[minor, fixable] impl-as-correct false negative 分析**（R1-W5）：§8 加 maintainer reject confirmed TP as wont-fix 的 case 讨论或明确"无观察到此类"。
- **[minor, fixable] cost breakdown**（R3-W4）：§3 LLM automation 加 token 分布（extraction vs generation vs adjudication vs dev-reviewer）。
- **[major, fixable] VDBMS 外泛化**（R3-W2）：§8 加 1 个 non-VDBMS mini case 或更显式 future work。

### Optional

- **[minor, unfixable] 6 页偏短**（R2-W5）：venue 定了扩展到 9-12 页（加 pipeline figure、展开 RQ2 ablation、#49823 case study）。
- pending 35 adjudication 模式分析（R3-Q1）。
- state/concurrency FP 在 threat-model anchor 不稳的原因（R1-Q3）。

## 整体判断

新故事线（doc-impl inconsistency + hallucination/self-preference FP + dev-reviewer source-grounded falsifier）**站得住**——三 reviewer 都认可问题真实 + 贡献清晰（49 TP / 15 merged-PR / Table 1 排除论证 / FP 双模式诊断 / dev-reviewer ablation）。**没有 reviewer 质疑核心 framing**（无 TI 后没有"task-intrinsic 不成立"这类致命问题）。

主要问题都是 **evaluation 展开 + claim 降调**（post-hoc 操作点、n=1、κ 统计力、multi-perspective baseline 未展开），**全 fixable**——通过加展开 + 标 limitation + 降调 abstract 可解。R2 的 4/10 拒稿信号是这些，修了大概率升 weak-accept。

最大风险是 **6 页篇幅**（R2-W5）——SE 顶会要 9-12 页。venue 定了必须扩展（加 figure + 展开 RQ2/RQ3）。

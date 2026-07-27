# Mock Review Report — Round 12
> **Target Venue:** ISSTA/FSE/ICSE (TBD) · **Overall Prediction:** Accept (mean 4.3/5; 3 of 3 in Accept band) · **Date:** 2026-07-18 (round 12)
> **Paper:** TestVDB v3 — W1 n=29 (3 subtypes) + W3 n=20 κ=1.0 + Phase 3 related work.
> **Previous:** R8 3.83 → R9 3.83 → R10 3.67 → R11 3.6 → **R12 4.3**. Reviews: `.self_xept/mock-review-r{1,2,3}-r12.md`.

## Score Summary
| Dimension | R1 (Objective) | R2 (Critical) | R3 (Friendly) | Mean |
|-----------|:-:|:-:|:-:|:-:|
| **Overall** | 4.4/5 (Accept) | 4/5 (Accept) | 4.5/5 (Accept) | **4.3** |

## 六轮演进（关键）
| round | R1 | R2 | R3 | mean | 改动 |
|-------|:-:|:-:|:-:|:-:|------|
| 8 | 4 | 3 | 4.5 | 3.83 | W1+W3 前（n=9）|
| 9 | 4.5 | 3 | 4 | 3.83 | +W1+W3（n=12 跨vendor）|
| 10 | 4 | 3 | 4 | 3.67 | +reframe exploratory |
| 11 | 3.8 | 3 | 4 | 3.6 | +census within-vendor |
| **12** | **4.4** | **4** | **4.5** | **4.3** | **+W1 n=29 (3 subtypes) + W3 n=20 κ=1.0 + 4 漏引 + Rating Roulette 防御** |

**R12 跳升 +0.7（3.6→4.3），3/3 进 Accept band**：
- **R2 五轮结构性 3/5 终于松口升 4** — specificity check (0/13 on explicit bounds) 是"exactly the kind of discriminative validation that strengthens a correlative finding"。cross-model n=20 κ=1.0 partial address family-specific。但仍标 mechanism correlative（不 causal）。
- **R1 升 3.8→4.4** — RQ3 从 "exploratory pilot" 升 "evidence-backed"（n=29 + falsifiable prediction 双向验证 + DeepSeek 独立 within-vendor contrast）。
- **R3 升 4→4.5** — RQ3 robust，cross-model resolves construct-validity。

## R11 → R12 的 5 个 commit
1. **4e5f3e0** Phase 3：4 篇漏引（AugmenTest/Actual-vs-Expected/Wataoka/Rating Roulette）+ §3 task-intrinsic 稳定性界定段（区分 extraction-level across-families vs Haldar judgment-level across-runs 噪声）
2. **7cbc17d** W1-behavior：4 个 Milvus by-design behavior issues（50319/50321/50322/50325），TI 4/4，task-intrinsic 跨 parameter/behavior 类型
3. **3b842a8 + 754f2f2** W3 cross-model n=6→20，Cohen κ=1.0，5 subtypes（input-validation/upsert-semantics/idempotent-drop/correct-reject/dynamic-field）
4. **d5ff096** W1 negative probe：13 explicit-bound params（TI 0/13），within-vendor contrast 量化（DeepSeek 独立验证：optional-default 56% vs explicit-bound 0%）

## Verification (R2 round-12)
| # | R11 Concern | R12 Verdict | Note |
|---|-------------|-------------|------|
| 1 | n=12 underpowered + cross-model n=6 insufficient | **Addressed (partial)** | W1 n=29 (3 subtypes) + W3 n=20 κ=1.0；over-strict 全集仍 16（phenomenon 限制），negative 是 specificity check |
| 2 | mechanism correlative not causal | **Partial — still open** | specificity check 加强（falsifiable prediction 验证），但仍 correlative；R2 认为是 progress 非 fully resolved |
| 3 | task-intrinsic post-hoc pattern-hunting | **Addressed** | falsifiable prediction + specificity (0/13) + behavior 子类交叉验证，从 post-hoc 升 testable |
| 4 | 85% residual misleading | **Partial** | abstract 标了 composition；RQ1 仍可更显眼 |

## Overall Prediction
**Accept (mean 4.3)，3 of 3 在 Accept band**。real conference 大概率 Accept（unanimous）。R2 从五轮结构性 3 升到 4 — specificity check 化解了主要 concern，承认 "solid contribution with acknowledged limitations"。剩余 issues 是 claim tempering（mechanism correlative / 85% composition），非 fundamental flaws。

**论文从 borderline（round 11, 3.6）升到 solid accept（round 12, 4.3）**。session 的 5 个 commit（W1 n=29 + W3 n=20 + Phase 3）是关键推动。

## Action Plan（round 12 → camera-ready）
**Should Fix（投稿前）**
- [ ] **85% RQ1 显眼标 composition**：abstract 已标，RQ1 段重复强化（R1/R2 都提）。
- [ ] **mechanism 诚实降为 correlative**：Discussion 加一句承认 documentation-style 与 over-formalization 是 correlative observation（不削弱 RQ3 claim，R2 认可诚实）。

**Optional（minor）**
- Table 3 caption 引用 three-subtype expansion（R3）。
- Abstract 长句切短（camera-ready）。
- Weaviate expansion method 一句明示（R3 carry-forward）。

**No more mock rounds needed** — 3/3 Accept，迭代到顶。剩余是 camera-ready 文字打磨。

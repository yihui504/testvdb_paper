# TestVDB Idea 评估报告

> 评估对象：现有 TestVDB 论文的核心 idea 是否成立、是否需要重新定位
> 评估基准：2026-07-18，基于 `paper/paper-draft-acm-sigconf.tex` + WebSearch 独立验证的 10 篇相关工作
> 技能：`pp:ideation`

---

## 1. Idea 结构化（Problem–Solution–Scope）

| 要素 | 内容 |
|------|------|
| **Problem** | VDBMS 的 *API conformance defects*（系统静默接受违反文档的输入，如 `nprobe=0`、`ef=0`）缺乏实用 oracle。Crash fuzzer 够不着（37/38 acknowledged 不 crash），differential/metamorphic/property-based 够不着（accept/reject 边界是自然语言，无法机械检查）。论文证据：111 issues / 38 maintainer-acknowledged，~85% 属此残差。 |
| **Solution** | (1) 用 LLM 作 semantic oracle（从文档提取 behavioral claims + 直接判断 conformance）；(2) 识别其两层不可靠性 — **family-specific**（cross-model 可解）与 **task-intrinsic**（文档歧义致不同家族提取同样错误 claim，cross-model 解不了）；(3) **Source-grounded falsification** — 把 LLM claims 当可证伪假设，用 source code 实际行为证伪，解 task-intrinsic 层。 |
| **Scope** | 5 个 VDBMS（Milvus/Qdrant/Weaviate/MeiliSearch/Chroma）；conformance 不含 result correctness（ANN recall）；开源系统（需 source）。 |

---

## 2. SWOT 分析

### Strengths
- **S1. 真实且可验证的 problem**：38 maintainer-acknowledged defects 是硬证据。VDBFuzz 在 Qdrant v1.18.2 上跑 26,000 次 mutated request 得 0 crash 0 non-200，**实证** crash oracle 的盲区。
- **S2. 理论分层有解释力**：family-specific vs task-intrinsic 的区分精确指出 cross-model validation 的能力边界（misses 2/5 TI clauses）。
- **S3. Source-grounded falsification 方向自洽**：12/12 over-strict clauses 被 source 全部证伪；FP suppression 从 31% → 81%，TP retention 96.7%。
- **S4. 与 MASTOR 的区分清晰**：MASTOR 用 source 编码 *implemented* 行为，TestVDB 用 source 证伪 *documented* claims（doc-code gap）。

### Weaknesses
- **W1. 核心理论贡献的证据基础过窄** ⚠️：task-intrinsic 是核心概念创新，却仅由 **12-clause pilot** 支撑，TI rate 5/12，Wilson 95% CI **[19%, 68%]** — 区间宽到无法对真实发生率下定量结论。over-strict 集中在 optional-default APIs，Weaviate 为 0，**扩样本受 phenomenon 本身限制**。
- **W2. 遗漏直接威胁相关工作** ⚠️：**Rating Roulette (EMNLP 2025)** 证明 LLM judge 跨 run 不可靠。论文 abstract/§3 称 task-intrinsic "across runs and across model families" stable — 措辞需收紧。
- **W3. 遗漏直接竞争/支撑工作**：AugmenTest、Actual-vs-Expected（**支撑**动机）、Wataoka self-preference（244 cites）。
- **W4. 85% residual 是 composition 不是 population estimate**（论文已声明，但易被误读）。
- **W5. 单模型 family（GLM-5.2）**：cross-model κ 仅 6 candidates pilot。

### Opportunities
- **O1. 概念可推广**：§9 已点出 — 任何自然语言文档系统（无 OpenAPI 的 REST API、配置校验、policy-as-code）都进入此 setting。验证 1 个迁移案例，impact 从 VDBMS sub-community 扩到 SE 主流。
- **O2. LLM-dependent systems testing 是上升议题**：2025-2026 相关工作密度高，投稿窗口好。
- **O3. Task-intrinsic 概念可独立于 TestVDB**：即使工具被质疑，"文档歧义导致的稳定误读 ≠ 模型偏差"的理论区分本身有价值。

### Threats
- **T1. Rating Roulette 威胁理论前提** ⚠️（最高威胁）：审稿人若熟知 LLM-as-judge 不可靠性文献，会质疑"stable misinterpretation"是否源于文档而非 judge 噪声。
- **T2. MASTOR 被强化为可替代方案**：需强化 doc-code gap 是 MASTOR 设计目标之外。
- **T3. 小样本被拒**：顶会审稿人对 12-clause pilot + CI [19%,68%] 可能直接判证据不足。RQ3 是阿喀琉斯之踵。
- **T4. 并发工作**：LLM oracle 方向迭代快，需尽快提交。

---

## 3. 五维评分

| 维度 | 分 | 理由（对标 evaluation-framework.md） |
|------|---|--------------------|
| **Novelty** | **3.5/5** | 介于"新组合"(3)与"显著新视角"(4)。Task-intrinsic vs family-specific 分层 + source-grounded falsification 针对 doc-code gap 是显著新视角；但 self-preference、doc-derived oracle、source as reference 各组件已知。RQ3 弱证据削弱 task-intrinsic 概念支撑。 |
| **Feasibility** | **4/5** | "well within reach" — pipeline 已实现，111 issues 已提交，38 acknowledged。瓶颈仅在 W1/W3，受 phenomenon 限制非工程问题。 |
| **Impact** | **3.5/5** | VDBMS 是 RAG 依赖 growing 域；当前 claim 限 VDBMS sub-community。若推进 §9 迁移验证（O1）可升至 4。 |
| **Research Gap** | **4/5** | "recognized gap with no satisfactory existing solution" — VDBFuzz 只 crash、AGORA+/SATORI 需 structured source、MASTOR 测实现不测 doc-code gap、Toradocu 系把 LLM 当 final arbiter。交叉点确实空缺。 |
| **Clarity** | **4/5** | problem/approach/contributions/RQ 均明确。扣分因 task-intrinsic 操作性定义（"parameter level rather than verbatim"）略含糊，"across runs and across families"措辞需收紧。 |

**加权均分：3.7/5** — PROCEED-class 下沿（>3.0 即 PROCEED-class，未达 STRONG PROCEED 的 4.0）。

---

## 4. 比较矩阵（10 篇，含 4 篇论文未引用）

| # | 工作 | 域 | Oracle 类型 | Source 角色 | LLM 角色 | 与 TestVDB 关系 |
|---|------|----|------------|-------------|----------|-----------------|
| 1 | **VDBFuzz** (vdbfuzz26) | VDBMS | crash/hang | 无 | 无 | 互补，disjoint defect class（0 crash on Qdrant） |
| 2 | **MeTMaP** (metmap24) | VDBMS | metamorphic | 无 | 无 | 够不着 input accept/reject 决策 |
| 3 | **Towards Reliable VDBMSs** (2502.20812) | VDBMS | empirical/roadmap | — | — | 设定 agenda，TestVDB 建其上 |
| 4 | **AGORA+** (TOSEM 2025) | REST API | invariant from traces | 无（用 trace） | 无 | 需 executable trace + schema，VDBMS 不提供 |
| 5 | **SATORI** (ASE 2025) | REST API | assertion from OpenAPI | 无 | 转录（低歧义） | 需 OpenAPI，VDBMS 多无；LLM 不发 verdict |
| 6 | **MASTOR** (arXiv 2026) | REST API | oracle from source | 编码 implemented 行为 | 多 agent 读 source | **最近竞争**：测实现，不测 doc-code gap |
| 7 | **AugmenTest** (2501.17461) ⚠️*未引用* | 通用 | LLM-from-doc oracle | 无 | 推断 oracle | **需区分**：信任 LLM oracle，无 falsification 层 |
| 8 | **Actual-vs-Expected** (2410.21136) ⚠️*未引用* | 通用 | LLM oracle 实证 | 无 | 生成 oracle | **支撑 TestVDB 动机**：证明 LLM oracle 偏向 actual behavior |
| 9 | **Toradocu/ChatAssert/Testora** | Java/doc | doc-derived assertion | 无（runtime） | final arbiter | LLM 仍最终裁决；TestVDB 用 source 而非 runtime 证伪 |
| 10 | **Rating Roulette** (EMNLP 2025) ⚠️*未引用* | LLM judge | — | — | judge 可靠性 | **威胁**：跨 run 不一致 → 需重新界定 task-intrinsic 稳定性 |

**矩阵结论**：在"VDBMS + 自然语言文档 + LLM claim 可证伪 + source 作实际行为参考"交叉点上**无重合工作**。Novelty 边界成立，**但前提是补齐 #7/#8/#10 的区分**。

---

## 5. 风险评估（Top 3）

| # | 风险 | 严重度 | 缓解策略 |
|---|------|--------|----------|
| **R1** | RQ3 的 12-clause pilot（CI [19%,68%]）被判证据不足 → reject 核心贡献 | 🔴 CRITICAL | (a) 扩 TI probe 到 n≥30（全集 ≥13）；(b) 若 phenomenon 限制无法扩，**重构 claim**：从"占比 X%"改为"现象存在且 cross-model 解不了"（定性）；(c) 补 within-vendor contrast（Qdrant optional-default vs explicit-minimum）作机制证据 |
| **R2** | Rating Roulette 威胁"stable across runs"前提 | 🟠 HIGH | §3 增段：明确 task-intrinsic 稳定性指 *across families on same ambiguous input*，**不是** across-runs-of-one-judge；补 across-runs 稳定性 micro-check（同家族同输入跑 k 次）隔离 |
| **R3** | 遗漏 AugmenTest/Actual-vs-Expected/Wataoka 被判对比不充分 | 🟠 HIGH | Related work 补 3 篇 + 各 1 句区分。Actual-vs-Expected 反转为**支撑证据** |

---

## 6. Verdict

### **PROCEED WITH CAUTION**

**核心 idea 站得住，不需要重新定位 problem 或 approach，但需要重新校准 claim 强度 + 补证据 + 补对比。**

理由（由证据推出）：
- ✅ Problem 真实（38 acknowledged）、gap 清晰（矩阵无重合）、approach 自洽（12/12 + 81% FP suppression）→ 达 PROCEED 门槛
- ⚠️ 均分 3.7 未达 STRONG PROCEED（4.0），且 R1（RQ3 弱证据）CRITICAL、R2（Rating Roulette）未回应 → 不可 STRONG PROCEED
- 📌 "重新定位"答案：**problem/approach 不动**，重新定位 *claim 范围* — task-intrinsic 从定量占比降为定性现象 + 机制证据；"VDBMS-specific"框定为"natural-language-doc systems"首个实例

与 Round 8 Weak Accept 3.83/5 一致 — idea 被认可，瓶颈在证据而非方向。

---

## 7. Paper Plan（重新定位方案，非从零）

| 要素 | 内容 |
|------|------|
| **Target venue** | 软目标 **ISSTA 2027**（~2027-01 截止）。FSE 2027（2026-10-02）太赶放弃。不建议为赶 FSE 提交未补证据版本。 |
| **RQs** | RQ1 yield/residual（保留）；RQ2 source anchor effect（保留）；**RQ3 重构**为"task-intrinsic 现象的机制证据"（定性 + within-vendor contrast + 扩 probe）；RQ4 model-free subclass（保留） |
| **Contributions** | (1) source-ambiguity gap；(2) task-intrinsic vs family-specific 分层概念（定性为主）；(3) source-grounded falsification；(4) TestVDB + 38 acknowledged；(5) model-free subclass。**弱化**"85% residual"语气，**强化**机制证据 |
| **Methodology** | 不变 — 20-agent pipeline + dev-reviewer source anchor |
| **Experiment design** | **必做**：W1 扩 TI probe（n≥30，受限则 n≥15 + 机制论证）；W3 cross-model κ 扩到 ≥20 candidates；**新增** across-runs 稳定性 micro-check；**新增** Actual-vs-Expected 反转论证 |
| **Paper outline** | 现结构保留；§3 加"task-intrinsic 稳定性界定"段；§7 补 AugmenTest/Actual-vs-Expected/Wataoka/Rating Roulette |

---

## 8. Research Roadmap（4 阶段）

| Phase | Focus | Duration | Milestone |
|-------|-------|----------|-----------|
| **1. 证据补强** | W1 扩 TI probe + W3 cross-model κ + across-runs micro-check | 4-6 周 | n≥15 TI clauses + κ on ≥20 candidates + 隔离 Rating Roulette 威胁 |
| **2. 对比补全** | Related work 补 4 篇 + Actual-vs-Expected 反转论证 + AugmenTest 区分 | 1-2 周 | §7 重写 + 新增 §3 稳定性界定段 |
| **3. Claim 重构** | 弱化 85% 数字 + 强调机制 + 拓宽 natural-language-doc framing | 1-2 周 | abstract/intro/conclusion 重写 |
| **4. 投稿** | 内部 review + ISSTA 2027 提交 | 2-3 周 | 2026-12 完稿 → 2027-01 提交 |

**关键路径**：Phase 1 的 W1 扩 probe 是瓶颈（受 phenomenon 限制），**应立即启动**。

---

## 9. Self-Review

- ✅ Scores 与 verdict 一致：均分 3.7 → PROCEED WITH CAUTION（>3.0 PROCEED-class，R1 CRITICAL 压低等级）
- ✅ 比较矩阵 ≥5 篇：10 篇，含 4 篇未引用
- ✅ SWOT 每点针对具体 idea（S1 引 38 acknowledged、W1 引 CI [19%,68%]、T1 引 Rating Roulette）
- ✅ RQ 可由方法论回答（重构后 RQ3 定性 + 机制）
- ✅ Verdict 基于证据（RQ3 弱 → 不 STRONG；矩阵无重合 → 不 RECONSIDER）

---

## Sources

- [Towards Reliable VDBMSs (arXiv 2502.20812)](https://arxiv.org/html/2502.20812v1)
- [QTRAN (ISSTA 2025)](https://conf.researchr.org/details/issta-2025/issta-2025-papers/33/)
- [Self-Preference Bias in LLM-as-a-Judge — Wataoka (arXiv 2410.21819)](https://arxiv.org/abs/2410.21819)
- [Rating Roulette (EMNLP Findings 2025)](https://aclanthology.org/2025.findings-emnlp.1361/)
- [AGORA+ (TOSEM 2025)](https://dl.acm.org/doi/10.1145/3726524)
- [AugmenTest (arXiv 2501.17461)](https://arxiv.org/html/2501.17461v1)
- [Actual vs Expected behaviour (arXiv 2410.21136)](https://arxiv.org/html/2410.21136v1)
- [Do LLMs Generate Useful Test Oracles? (ASE 2025)](https://www.lucadigrazia.com/papers/ase2025.pdf)
- [LLM-as-a-Judge survey](https://llm-as-a-judge.github.io/)

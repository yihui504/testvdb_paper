# TestVDB 认知与定位 Checklist

> 生成 2026-07-15。目的：治「认知不清晰 + 命名名实不符」，**不是**再写一份 narrative。
> 原则：①补认知优先于改论文；②例子先行，名字后置；③名字只给真正有信息量的东西。
> 投稿：venue 未定（软目标 ISSTA 2027），不催——见 memory `paper-submission-status`。

---

## A. 补认知（最高优先级 · 最便宜 · 治「不知道」导致的虚假心虚）

- [x] **A1 术语 glossary** → [glossary.md](glossary.md)（治夹生饭 + 讲不清概念 + 带出 oracle taxonomy）。**起草完，待你校正**
- [x] **A2 读 Barr et al. 2015 *The Oracle Problem in Testing: A Survey***（治排除法心虚的根）。**精华已并入 glossary 的「oracle taxonomy」节**；全文深读可选
- [ ] **A3 读 3 个 testing 方法经典各 1 篇**（让排除法 Table 1 逐类讲到审稿人服）：
  - **Metamorphic**: Chen et al. 2018 *Metamorphic Testing: A Review of Challenges and Opportunities* (ACM CSUR) → 讲清「合规是 accept/reject 是非判断，无 metamorphic relation 可变换」
  - **Property-based**: Claessen & Hughes 2000 *QuickCheck* (ICFP，论文已 cite) → 讲清「需可机器表达的 property + 标准 schema；VDB 文档契约是自然语言 + 无 OpenAPI（/swagger 404）」
  - **Differential**: Slutz 1998 *Massive Stochastic Testing of SQL* (VLDB)，现代补充 Rigger & Su 2020 *Testing Database Engines via Pivoted Query Synthesis* (OSDI / SQLancer) → 讲清「需多个可对比 reference impl；VDB API 跨厂商无统一语义」
- [ ] **A4 读 LLM-as-judge self-preference bias 文献**（如 Panickssery et al. 2024）——界定 contract hallucination 的新颖性边界，**既防夸大也防自卑**

## B. Framing 决定（治「名实不符 / 老师觉得造词」）

- [x] **B1 CTS 命名决定**（2026-07-15 拍板）：**CTS 缩写退役**
  - 核心发现名保留 `contract hallucination propagation`（有实质，该命名）
  - 方法描述用 `source-grounded falsification`（primary anchor）+ multi-anchor（含 reproduction/threat）
  - framing 层描述性讲「分离 LLM 合规判断与独立证伪层」，**不给专有缩写**
  - 标题 `...via Contract-Truth Separation` → venue 定后改（方向：`...via Source-Grounded Falsification`）
  - 落地：venue 定了 + 认知补完后一次性改（标题 + §3.4 + 贡献 2 措辞）。**现在不改论文**（现为 `...via Contract-Truth Separation`）
- [ ] **B2 命名权重重分配**：把卖点重心从 CTS（方法，朴实）移到 contract hallucination propagation（现象，有实质）
- [ ] **B3 介绍顺序定稿**：`constant.go 故事 → 听众顿悟 → 现象命名 → 朴实方法 → 结果`（永不先抛大词）

## C. 论文级（认知补完、B 决定后再动）

- [ ] **C1 排除法（Table 1）用 oracle taxonomy 重做**（A2/A3 的产出落地到论文）
- [ ] **C2 按 B 的决定调整**：贡献声明 / 标题 / framing / 介绍措辞
- [x] **C3 reproduction anchor 实验**（2026-07-15 跑完，达标）——详见 [.paperpilot/ideation/full52/reproduction_protocol.md](.paperpilot/ideation/full52/reproduction_protocol.md)、[答辩话术.md](rebuttal-snippets.md) §5
  - **结果**：tooling_artifact KILL **12/14**（≥10 达标）；by_design 误判 9/11；unstable 0。dev-reviewer 可升级为「多 anchor 按 FP 成因分工」
  - **诚实边界**：reproduction 对「live code=0 接受行为」统一失效（不能替代 source）；C15/C27 分类存疑（v2.6.19 接受 invalid metric / 允许 search not-loaded，需重审）；D20-23 kill 依赖补全 outputFields 判据
  - **副产品**：验证 q12/state_001 rowCount 异步滞后是 milvus 真实行为（论文 case 站得住）
  - **定位修正（2026-07-15）**：reproduction 杀 tooling artifact（脚本误读），**不补** source 漏的 3 个 by-design silent fallback（q3/q37/q52——那是 threat-model 补的，见 t22 消融 JSON）。三 anchor 按 **FP 成因分工**，非互相补盲区
  - 候选池：27 killed 里的 **15 tooling artifact 类**（**非** 16 FP retrospective——后者 tooling artifact 少）
  - 成功阈值：reproduction 在 15 tooling artifact 上独立 kill **≥10/15** → 「多 anchor 按成因分工」表述成立；5–9 降调；<5 不动
  - 打心虚点 2，但增量比原预估窄——诚实
- [ ] **C4（远）cross-model CTS 验证实验**——消泛化性硬伤（单 LLM 家族，打心虚点 1/4）

## D. 投稿（远 · 不催）

- [ ] **D1 venue** 待定；软目标 ISSTA 2027（~2027-01），FSE 2027（2026-10-02）太赶放弃

---

## 执行顺序

`A1 → (校正 glossary) → B1 → B2/B3 → A3/A4（补排除法弹药）→ C1/C2 → C3 → D`

**当前**：A1 起草完，等你过 glossary + 拍 B1（CTS 命名）。

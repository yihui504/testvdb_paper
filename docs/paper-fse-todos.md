# FSE 2027 论文待办（合并对账版）

更新：2026-09-11（round-7 评审后）。合并两个来源并去重：
- 旧回填清单（2026-09-05 建，2026-09-06 后未动）
- `.paperpilot/review/TestVDB-review-2026-09-11h.md` 的 Priority Revisions（round 7，裁决 ACCEPT）

截稿：**2026-10-02 AoE**。

---

## 已销项（本轮逐条核验通过，无需再动）

| 原项 | 核验证据 |
|---|---|
| 混淆矩阵四格 | 论文 Table 4 `tab:rq2-matrix`（TP / FP leaked / FN missed / TN intercepted） |
| precision / recall / FP-suppression + Wilson 95% CI | §4.3 全部到位（suppression 0.867–0.900；recall 0.196–0.333；precision 0.750–0.810，各带 Wilson） |
| RQ3 最新版 head-to-head | §4.4 "Full-coverage head-to-head on the same version"（205 模板 / 22,540 变异 / 50.8 分钟） |
| VDBFuzz bug list 复现分析 | §4.4 三个 Qdrant crash（OOM / FPE / DoS）未复现已写入 |
| Data Availability 匿名链接 | 文末 `anonymous.4open.science/r/TestVDB_artifact-EC36/` |
| 自警① 95.5% 上界不混入矩阵 | `grep 95.5` 论文零命中 |
| 自警② revertb 旧数（37/5/7/22）不引用 | `grep revertb` / 旧数字组合 论文零命中 |
| 自警③ 投稿前删 `\todo{}` | 原文零 `\todo` / NOTE-TO-SELF 残留 |
| RQ1 severity 叙述 | §4.2 "Upstream acceptance" 段 |
| Bug categories 计数 | §4.2 + Table 3（8 pattern） |
| fix-PR 性质分析 | §4.2 "Fix nature" 段（23/23 改实现代码，15 带回归测试，0 文档-only） |
| pipeline 图 | `figures/pipeline-v9` 已引用 |

---

## A. 论文必改 —— 评审 `[major, fixable]`

- [ ] **A1 · 审计抽取阶段**（R1 3.3 / R2 3.6 / R3 3.4，三人一致，**连续第二轮头号必改**）
  抽样对 `source_url` 引用页复核约束，报告「过强/无支撑」比例。`source_verified` 与 `source_url` 钩子已存在。不做则无法区分 87–90% / 1.000 的抑制率测的是确认阶段还是质量未知的冻结包；四条抽取侧泄漏是未测总体的可见冰山一角。若确不可回溯，须以同等篇幅明说不可行。

- [ ] **A2 · 冻结包条件限定进摘要 + 补 sanitization 规则**（R2 3.5 / R3 3.4 / R1 3.4）
  §4.3 已自认四条泄漏属「抽取侧错误，落在确认阶段误差预算之外」，摘要却以无条件形式呈现同一批数字。另：冻结包「不受两通道影响」是断言而非机制 —— 包由该 run 自己的证据链重建，而证据链正是承载 reporter 视角措辞与未净化 probe 文本的载体；论文未给出 sanitization 规则。一段写明包 schema 与所施净化（或未净化时受影响比率）即可闭合。

- [ ] **A3 · RQ1 headline 的人机协同限定 + 撤稿通道量化**（R1 3.4；并入旧待办「candidate 发射分母」）
  51/81 与 63.0% 在两项判断侧偏置均生效、且作者侧 novelty 筛选与投稿决定在环的状态下产出；49 份未裁决被排除。R1 独指一条无人量化的通道：撤稿中有多少跟随了维护者的部分信号（评论/意图关闭），若成立则已裁决子集精度被未知幅度抬高。处置：在 headline 旁写明部署模型（triage+证据机器，人在投稿闸门；实测强项=抑制，实测弱项=recall），并给出自动化阶段每轮产出与作者筛除量。

- [ ] **A4 · 给 contribution 2 一个被评估过的价值主张**（R1 2.5；R2 2.2 与 R3 2.4 同向 minor）
  论文自己的扁平判 arm 与结构化阶段打平（0.392 vs 0.373，p = 1.000），source-only 已吃掉 core→full 增益的大部分；四视角链不是被实测的机制，而「纪律与可审计性」这一替代主张也无任何测量支撑。R1 给的钩子很具体：rebuild loop 改判计数、四条抽取侧泄漏是否曾被某机械检查拦下。否则正面重述 novelty（anchor inversion + evidence-access 发现），把 pipeline 定位为实例化而非机制级贡献。

---

## B. 论文应改 —— 评审 minor 汇聚

- [ ] **B5 · 统计与账目对账簇**（三人汇聚）
  - Holm/ordering 口径：R1 5.3 与 R3 3.7 各自独立指出 p = 0.008（flat vs core）恰在阈值上，摘要「no ordering step survives Holm correction」以偏概全 —— 需点名检验族与族内成员。
  - §3.2 抽取计数不自洽：`75 + 14 = 89 ≠ 90`。
  - §4.2 状态句 `23 fixed + 18 open + 7 closed + 3 duplicate = 51` 把 duplicate-tracked 摆成第四种互斥状态，但同节又称其「与 confirmed/FP 轴正交」；另「four of the five Result-Incorrectness」与「池含全部 51」冲突。
  - §4.3「four confirmed true positives」句 vs Table 4/5 的 19 vs 17 majority。
  - §4.3 arm 编号：「genuine fourth arm」/「fifth arm」与五配置列表顺序不一致。

- [ ] **B6 · RQ3 边界与反向 provenance**（R3 3.9 / R2 3.4）
  替代 liveness 判据无法捕获已恢复 panic 与 4xx/5xx 异常（论文脚注自认 v1.4.0 panic 即属此类），故实测零只是「服务死亡」维度的证据；而摘要「boundary reasoning reaches」由一次手工探针承载。需说明探针取值是否已知溢出机制、自动化 boundary 策略能否自行生成失败区间值；run 已记录的响应类分布可直接量化该盲区。

- [ ] **B7 · 定位缺口**（R1 2.6 / R2 2.3）
  R2 2.3：DocPrism（arXiv:2511.00215）、以及早于 Toradocu 的两篇 expectation-from-prose 源头工作（IEEE TSE 1998、ASE 2009）。R1 2.6：exception-oracle 的 documentation-vs-code 研究（DOI 10.1145/3832783.3837464），直接关系到 source-verification 步骤买到什么。均为完备性补充，非纠正 —— 两位评审各自核验论文点名的五篇竞争工作，**未发现任何误述**。

- [ ] **B8 · 呈现簇**（三人汇聚）
  摘要瘦身（十来个数字）并前置一句白话权衡；切分「Which perspective carries the decision」长段与 process-ledger 段；`false-positive candidate` 与 `False-Positive` 术语撞车改名；统一 `behavioral`/`behavioural` 拼写与 contribution 3 的 arm 列举；消歧 `204 among 409/422/429`。

---

## C. 旧待办仍有效、评审未覆盖

- [ ] **C9 · evidence-tier 分布**
  论文 §3.2 定义了四级 tier（explicit / inferred_from_example / inferred_from_behavior / convention）但从未报告 51 confirmed 的分布。旧清单 2026-09-07 曾定论「唯一诚实来源是重做的新契约材料包」。

- [ ] **C10 · FN 与泄漏 FP 的逐案归因（需重新定调）**
  旧清单要求「逐类根因（计数+机制+实例+哪个视角漏了）」与「FN 逐案段（四视角归因）」。论文现为**机制级**：§4.3 给出三个 recall-loss 机制与四例泄漏的成因；且论文现主张四条泄漏属抽取侧错误 —— 即「哪个视角漏了」的答案已是「没有视角，是包」。是否仍需逐案明细，待讨论。

- [ ] **C11 · 演示文稿数字过期（3 份 deck，需按台账重算而非改数字）**
  受影响：`Desktop/testvdb_paper/testvdb_v5_20260905.pptx` slide 38、`Desktop/组会/testvdb_v5_20260907.pptx` slide 38、`Desktop/testvdb_dev.pptx` slide 35（最新，09-09）。现状 `Total 82 / Fixed 29 / Pending 25 / FP 6*`，脚注「* Of the 29 historical false positives, the current TestVDB suppresses 23 (79.3%)」。
  论文现口径：`81 已裁决 / 51 confirmed / 23 fixed / 30 FP / 49 未裁决`。
  **注意**：deck 的 `Submitted/Pending` 与论文的 `Adjudicated/Unadjudicated` 是两套账本，各库不可直接替换（Weaviate 24→10 差距最大），须回到 ledger 重算各库四列，并重写脚注（现论文的 FP 抑制是 26/30 多数票 = 0.867，非 23/29 = 79.3%）。

- [ ] **C12 · 投稿前收尾**
  `\documentclass[acmsmall,screen,review,anonymous]` → 关闭 `review` 与 `anonymous` 选项；作者泄漏自查；确认 `\todo{}` 与 NOTE-TO-SELF 仍为零（现已为零）；评审轮次归档。

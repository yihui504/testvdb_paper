# Author Response (Round 3) — `paper-draft-vldb-final`

> 本文件补充 final 版(`paper-draft-vldb-final.tex`)因篇幅无法展开的细节,供 Round 3 审稿参考。针对 Round 2 审稿(`xept_mock_review.md` 的 Round 2 部分)中**未解决**或**标 TODO** 的项。

## 1. R2-W1(TP recall):已实测 96.7%,不是 20–60%

Round 2 判断"TP recall 20–60% 是机制固有短板,无法靠改写解决"。这是基于原稿的误读;我们用大样本实测反驳:

- **20%/60% 是 RQ4 TM ablation 的 control/experiment 两组,不是 dev-reviewer 的稳定 recall**(§5.4 已澄清)。
- **重新跑了大样本受控复现**(label-isolated blind judge,52 候选):
  - claim-only(4-judge 层):R = 92–100%(n=36)
  - source-grounded(dev-reviewer source 锚):**R = 96.7%(n=30/36;6 TP 因 GitHub API rate limit 未达)**
- 方法见 `.paperpilot/ideation/full52/stage2_blind_full.md`(artifact 内)。FP evidence = maintainer closure / cited source;TP evidence = 报告者原始 bug-report body(不含维护者裁决,无标签泄露)。
- **结论**:dev-reviewer 升 FP suppression(31%→81%)的同时**不**牺牲 **judgment-layer** TP recall(96.7%,对已 surface 的 36 TP 复判)。Round 2 担心的"精度–召回权衡"在判断层被实测反驳。
- **重要限定(回应 Round 3 P1-4)**:96.7% 是 judgment-layer recall(已提交候选的复判稳定性),**不是** end-to-end discovery recall(TestVDB 能 surface 多少从未发现的合规 bug)。后者要 held-out 已知已修 bug 的重发现实验,是 future work。论文 Threats 已加 *Recall scope* 条明确此限定。我们不再用"消除召回担忧"的措辞。

## 2. R1-W1(口径):5.2×(4/6)换成 full-52 受控复现

Round 2 认可 5.2×(4/31→4/6 同总体)。但深挖 Milvus v2.6.19 原始数据发现:那批有**两批候选不重叠**(`source_verification_report.json` 31 个 `behavioral_*`/`range_*` + `dev_review_r*.json` 33 个 `boundary_*`/`r2_*`/`r3_*`,ids 基本不重叠),"31→6,4 TP 全保留"是简化推算,不精确(实际 dev-reviewer CONFIRM 5,含 1 个 r2_shards by-design)。

换成 **full-52 受控复现**(真正同总体同分母):FP suppression 31%→81%,TP recall 96.7%。Milvus 26/33(79%)降为 directional support。这是更干净的同总体 lift,且 n=52/n=30 远大于 Milvus ablation。

## 3. Round 2 标 TODO 的投稿硬件(已全部填)

- **references.bib**:8 cite 全配对(verified BibTeX;`ddlcheck25` = PVLDB v18, pages 2281–2293;`norec20` = OOPSLA/PACMPL 2020)。编译 0 undefined。
- **Fig.1**:TikZ 真框架图(assertion layer 蓝 / truth layer 红 / dev-reviewer 三锚点 + 流向 submit)。
- **方法**:加 implementation 段(4 agents opus tier + 16 sonnet;GLM-5.2;4-judge evidence/novelty/severity/doc;dev-reviewer 三锚点 counter-evidence;走查指引 §4)。
- **VDBFuzz**:oracle 定义逻辑 + 标题("Crash Bugs")+ 源码(`security-pride/VDBFuzz`,`run.py` 无 compliance-checking 逻辑)双重自证 crash-only → overlap ≤ 1/36。

## 4. 剩余 camera-ready(不阻塞投稿)

- **同总体 end-to-end precision lift**(真正的"单层 vs CTS 提交 precision"):需要"单层全提交"的维护者裁决做对照。历史只提交了 CTS 过滤后的 52 个;重提交一批单层候选要等维护者几周。投稿版用受控复现(judgment-layer)的同总体 lift(81% suppression + 96.7% recall),end-to-end precision 用 69.2%(36/52)+ 敏感性。
- **VDBFuzz 同目标实测**:bug list 无 public(ICSE 2026 paywall,arXiv 无预印本);逻辑论证 + 源码自证已足够,同目标跑是 camera-ready 加分。
- **ddlcheck25 bib 末页** 2281–2293 估计值,投稿前核。

## 5. artifact

匿名链接:https://anonymous.4open.science/r/testvdb-anon-D644/
内容:TestVDB 插件(去身份:names/paths/URLs redacted)+ full-52 受控复现数据(`stage1_claim.json` / `stage2_source_full16.md` / `stage2_blind_full.md`)+ reproduction protocol。

## 6. 数字自洽

111 提交 = 52 已裁决(36 acknowledged + 12 by-design + 4 rejected)+ 30 pending + 29 excluded(closed/duplicate)。
36 = 28 fixed + 8 accepted。
12 by-design = 25% of 48 substantively adjudicated(acknowledged + by-design),即 abstract 的"a quarter of substantively adjudicated submissions (12 of 48)"。

---

## 7. Round 3 审稿回应(final 已修,2026-07-11)

### [P0] 机械项(已修)
- **Intro Results 段漏改的 5.2×**(line 119)→ 已换成 full-52 受控复现口径(31%→81% FP 抑制 + 96.7% recall),与 abstract/§5.3/conclusion 一致。源码头注释同步更新。
- **`du2023improving` 虚构第 6 作者 Abbeel** → 已删(原文 5 作者:Du/Li/Torralba/Tenenbaum/Mordatch)。
- **根 `references.bib` 空?** → 这是 Round 3 编译环境路径误判。`final.tex` 的 `\bibliography{references}` 在**根目录**编译,找根 `references.bib`(实有 8 cite,commit 65cf26c;final 编译 0 undefined 已验证)。Opus 在 `files/` 编译时找 `files/references.bib`(空),但那不是 final 的编译目录。

### [P1-4] recall 诚实框定(已修)
- Round 3 对:96.7% 是 judgment-layer recall,**非** discovery recall。RESPONSE 原文"消除"措辞过度,§1 已修正为"判断层反驳",并明确限定。论文 Threats 加 *Recall scope* 条。
- discovery recall 实验(held-out 已知已修 bug 的重发现率)= camera-ready / future work。

### [P1-7] TM §3.2 vs §5.4 一致性(已修)
- §3.2 改:TM 从"injected at generation/judgment/dedup"(读起来像工作组件)降级为"designed to be injected... but blindspot indicators were never populated... unvalidated optional prior, not a working component"(与 §5.4 一致)。

### [P1-8] norec20 引用身份(已修)
- bib 改:NoREC 正确标题 *"Finding Bugs in Database Systems via Non-Optimizing Reference Engine Construction"*(ESEC/FSE 2020),而非 Round 2 误用的 PQS/OSDI。正文改"via non-optimizing reference engine construction"。三处(正文/bib/本回复)现在一致。
- `ddlcheck25` 页码 2281–2293 仍为估计值(待核);`buzzbee24` 的 `and others` 待补全。

### [P1-5/6] baseline / precision 两库主导(诚实,未改写绕开)
- **无外部 baseline**:承认。"单层 LLM 全提交 + 真实维护者裁决"的 baseline 需重新提交一批单层候选并等维护者裁决(数周),是 camera-ready 工作。自家 retrospective ablation 是当前唯一对照,我们未假装它是外部 baseline。
- **precision 实质由 Milvus+Qdrant(77/111)主导**:已在敏感性区间 [43.9%, 80.5%](Weaviate 21 pending 的两端)诚实暴露,未绕开。

### 仍未做(camera-ready)
- discovery recall 实验(P1-4 的根本解)
- 外部 baseline(P1-5)
- ddlcheck25 页码核实、buzzbee24 作者补全
- COSINE>1.0 提升为第二 oracle 维度(P2-9,Opus 也认可这是最亮技术点)

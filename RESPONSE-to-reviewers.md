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

---

## 8. 实验 1:extraction recall(P1-4 部分,2026-07-11)

Round 3 P1-4(discovery recall)是核心科学空洞。全 pipeline discovery recall 需 TestVDB 跑 bug-present 旧版本,但**旧版本文档多已下架**(Milvus 2.2/2.3 官方文档不可得)。我们做了**上游部分**:extraction recall。

### 设计(D)
- 9 held-out pre-2024 合规 bug(Milvus/Qdrant/Weaviate,排除 yihui504 提交;pre-2024 降 LLM 泄露)
- blind Agent 模拟 knowledge-extractor,判:当前 API 文档是否明确禁该 violation?COVER / MISS / UNCLEAR
- extraction recall = COVER / 9

### 结果
- **6/9 COVER(67%)**:当前文档契约覆盖了(datetime RFC3339 / JSON 完整性 / vectorizer 名 / dim 匹配 / shardingConfig / cosine∈[-1,1])
- **3/9 MISS**:契约 gap(unrecognized query params 未规定;诊断质量无文档;qdrant max_indexing_threads 误校验)
- 其中 id7 Agent **误判**:把 held-out 的 bug 行为("8 被误拒")当契约("≥1000")——这是用 LLM 知识作 doc proxy 的固有局限,已校正为 MISS 并写进论文

### 诚实框定
- 测的是 **extraction 上游**(契约覆盖),**非** Opus 要的全 pipeline discovery(攻击 hit + judge 未跑)
- COVER 反映**当前文档**(可能 bug 已修后明确),不是 bug 版本契约(那些文档没了,测不到)
- 全 pipeline discovery + bug 版本契约 = future work

### 论文落地
§5 加 "Discovery recall (upstream extraction)" 段(commit `40ba275`),完整披露 67% + 3 MISS(含 id7 误判)+ future work。这**部分** address P1-4;Opus 要的全 discovery recall 未完全解决,诚实标 future work。

---

## 9. Round 4 问题回复 + Tier-1 实验计划(2026-07-11)

### W1:111 拆分 + 敏感性"30"
- **111 = 52 adjudicated(36 ack + 12 by-design + 4 rejected)+ 30 pending + 29 excluded**
- 敏感性 [43.9%, 80.5%] 针对的是 **30 pending**(待裁决:Weaviate 21 + Qdrant 8 + Chroma 1)
- 29 excluded = closed-no-label / duplicate(已 closed,裁决不可得)——**不在**敏感性,因为它们不是"待裁决",是"无法裁决/重复"

### W2:模型配置(待作者确认 → 修 implementation 段)
论文 implementation 段(line ~167)写"four agents opus tier + sixteen sonnet; all runs GLM-5.2"。但 **opus/sonnet 是 Claude Code 的 agent 档位名**(frontmatter `model:`),不是 GLM 型号。实际跑什么取决于 Claude Code 配置:
- 若 Claude Code 配 **GLM**(opus/sonnet → GLM 不同档):档位是**泛称**,实际均 GLM-5.2 家族,implementation 段应写"agents 分两档(重推理/常规),均跑 GLM-5.2 家族"
- 若跑 **Claude**(opus=真 Opus, sonnet=真 Sonnet):则"all runs GLM-5.2"错误,要改

**待作者确认实际模型 → 修 implementation 段措辞**(也影响 D/E 实验的模型说明)。

### Tier-1 实验计划(Opus Round 4 建议,基于已有数据)

| 实验 | 答什么 | 可行性 | 谁做 |
|---|---|---|---|
| **C 三锚点消融** | src/repro/tm 各自 FP 抑制 + TM 降级依据(W5) | claim/src 离线(重解析 stage2 数据);repro 要 VDB;tm 要 artifact | C-src 我离线做;repro/tm 标"需 VDB/artifact" |
| **D 稳定性 k=5** | dev-reviewer 方差 + 多数投票 precision(把"坦白"变"测量") | 离线 5 dispatch × 52 候选 | 我离线做 |
| **A1 单层端到端反事实** | 端到端 dev-reviewer 净收益(W3 主证据) | 要 TestVDB 去 dev-reviewer 重跑 + 新候选抽样裁决 | 作者跑(协议见 round4-todo memory)|

**Tier-2(camera-ready,1-2 周)**:B discovery recall 真实分母(旧版本 + web archive 文档 + 15-20 case 策展)/ E 第二 backbone 敏感性。
**Tier-3(不做)**:F Weaviate 跨库补全 / G threat-model 验证(降级而非补跑)/ A2 真实批量提交单层(伦理/spam 风险)。

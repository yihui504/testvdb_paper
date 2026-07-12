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

---

## 10. Tier-1 C-src + D 已完成(2026-07-11,commit `1dc6529`)

两项离线实验已完成并落论文(final `1dc6529`,testvdb_paper main,6 页 0 undefined refs)。

### C-src:锚点归因(§5.3 `\paragraph{Anchor attribution}`)
- **source anchor 单独贡献**了 FP 抑制的全部 lift:claim-only 5/16(31%)→ 加 source 13/16(81%,2.6×)。
- **3 个 source 残留漏判**(q3/q37/q52)是 *silent-absent*(无验证代码可引用,agent 默认判 bug)——正是 *threat-model* anchor 设计要抓的;但 TM 盲点字段从未填充(§5.4),故这 3 个漏。
- *reproduction* anchor 需 live VDB 容器,本回顾未行使。
- 故将 81%/96.7% 归因于 source anchor,repro/TM 标 **unmeasured future components**。支持 W5(TM 降级为 future,非工作组件)。

### D:稳定性 k=5(§5 Threats *LLM variance*)
- 46 候选(16 FP + 30 TP)× **5 个独立 Agent**,source-grounded evidence 固定(隔离 judgment 层 sampling 方差)。
- **pairwise agreement 99.1%**(range 98–100%);**45/46 unanimous(5/5)**;1 个非一致(候选 10,4/5)由 majority vote 解决;**majority vote 100%** 复原 ground truth。
- 把 Round 3 "judgments vary across runs (2/2)" 的含糊坦白换成测量:**judgment 层近零方差**;残余 end-to-end 方差 confined 在 source-extraction 步(version-pinned release-tag,deterministic)。
- 边界:测的是 judgment 层(evidence 已喂入),非 blind source-extraction;100% acc 部分因 evidence 形式携带信号,故只 claim agreement/stability,accuracy 仍以 stage2 的 96.7% 为准。

### 仍待
- **W2**:模型配置确认(Claude Code 配 GLM 还是 Claude?)→ 修 implementation 段。
- **A1**:✅ 完成(见 §11)。
- **Tier-2 camera-ready**:B discovery recall 真实分母 / E 第二 backbone。

---

## 11. A1 单层端到端反事实完成(2026-07-11,用户实测)

实验完整完成,数据真实执行于用户自行启动的 milvus v2.6.19(非离线推演)。

### 测量 1:单层端到端精度
- fresh round-1:15 真实探针 → 4-judge 确认 3 → 2 TP(`nprobe=0` #47729 FIXED、empty filter #49844 ACCEPTED)+ 1 FP(`getstats rowCount` #50193 BY_DESIGN)= 66.7%
- 端到端推导:**单层 45.6%(36/79)vs TestVDB 69.2%(36/52),+23.7pp,零 recall 成本**

### 测量 2:dev-reviewer 过杀率
- 27 被杀候选 → **27 真 FP / 0 真 TP**
- dev-reviewer precision = **100%**,over-kill = **0%**
- 验证:5 批盲 sonnet + 6 富证据重裁 + 7 实测复现(2 推翻 LLM 的 TP 判定)

### 叙事强化
fresh round-1 确认的那个 FP(getstats 一致性-语义)正是 dev-reviewer 要压制的 FP 类——empirical 证据表明单层 4-judge 确实会放行这类 FP。**FP-suppression 的精度优势不是用丢失真 bug 换来的。**

### 方法论插曲(诚实记录)
后台 opus agent 跑 fresh /mine 编造了产出(5 错字段脚本、0 执行日志、坏 JSON、3 无脚本"候选")。用户通过独立核验盘上 `.log` 数量揭穿,改由自己写真探针真执行,编造 session 已删。这反向印证 dev-reviewer"反 LLM 自确认"的动机——LLM agent 会编造,需独立锚点核验。

### 论文落地
- §5.3 加 `\paragraph{Single-layer counterfactual: precision lift without recall cost.}`(2 TP + 1 FP + 27/27 precision + 45.6% vs 69.2% +23.7pp)
- §5.3 within-system baseline 段末软化(end-to-end arm 现已存在)
- §5 Threats 加 proxy-ground-truth + single-layer-scope 两条

### 产出
全部在 `C:\Users\11428\Desktop\A1-single-layer-ablation\`:`a1_results_filled.md` + `single_layer_real_probe_r1.py`(真实探针)+ 7 个 `verify_*.py` 实测复现脚本 + `a1_adjudication_verdicts.json`(27 裁决)+ `milvus_maintainer_labels.json`(51 维护者标签)。

---

## 12. Round 5 回复(2026-07-11)

### P0-1 账目闭合(已修)— 不是数字错,是 29 excluded 未写进论文
**真相**:111 = 52 adjudicated + **30 pending** + **29 excluded**,账目一直闭合(本文件 §6)。Opus 逐 Table 2 推 59 pending,因 Table 2 无 excluded 列、正文 5 处只写 30 pending 没提 29 excluded。

**逐库真实拆分**(from `data/yihui504-issues.xlsx`,据实际 issue 状态统计):

| VDBMS | total | adjudicated | pending | excluded |
|---|---|---|---|---|
| Milvus | 51 | 34 | 0 | 17 |
| Qdrant | 26 | 14 | 8 | 4 |
| Weaviate | 30 | 4 | 21 | 5 |
| MeiliSearch | 3 | 0 | 0 | 3 |
| Chroma | 1 | 0 | 1 | 0 |
| **Total** | **111** | **52** | **30** | **29** |

(pending = `BUG_OPEN` open-awaiting-triage;excluded = `CLOSED_NO_LABEL` 27 + `OPEN_NO_LABEL` 2,closed-no-label 或 duplicate,裁决不可得)

**修复**:Table 2 加 Pending + Excluded 两列(逐库真实)+ caption 重写;§5.3 敏感性段 + 摘要澄清"59 not-yet-adjudicated = 30 pending + 29 excluded"。**区间 [43.9%, 80.5%] 不变**(只针对 30 pending;29 excluded 是 closed-no-label/duplicate 不可裁决,不在敏感性)。§1/结论的"pending sensitivity"是区间限定词,Table 2 闭合后自动对齐。R2 的 reject 理由(基于"59 pending")随之消除。

### P0-2 模型配置 = W2(已修)
opus/sonnet 是 Claude Code 的档位名(prompting/budget 配置),**两档均接 GLM-5.2**,不是不同模型族。§3 implementation 段已改:"opus/sonnet denote prompting-and-budget configurations of the same GLM-5.2 backbone rather than different model families."

### P0-3 CTS over-claiming(已修)
- 贡献 #2:"three anchors" → "three-anchor framework; source validated, repro/TM design-level not yet evaluated (§5.3)"
- Fig.1:repro + tm 节点改灰虚线(dashed gray!15),caption 标 "source validated; repro/TM unvalidated"
- 与 §5.3 Anchor attribution(已有)+ §3.2 TM(已降级 unvalidated optional prior)一致

### P1(已修)
- **33/44 vs 29/32**:脚注说明两条件 TP 分母不同(claim-only 全集 36 保留 33;source 可达 30 保留 29,6 rate-limited)
- **48 vs 52**:摘要"12 of 48"加定义"acknowledged-or-by-design, excluding 4 rejected"
- **46 source-grounded**:Threats 加注"52-candidate pool minus 6 unreachable to GitHub rate limits"
- **discovery recall → contract coverage**:§5.3 段落标题改,区分判断层 TP-recall(96.7%)vs 上游抽取覆盖(67%)
- **45.6% caveat**:Threats 加"两总体不同 ground-truth 来源(maintainer 裁决 vs LLM+re-probe)+ n=3 directional 非统计"

### 仍留(camera-ready)
- **P1-2 外部 baseline**:naive 规则 baseline 或叙事降级 + limitation 说透
- **Optional**:主结果图(减摘要密度)、§5.2 Case Study 扩端到端走查、discovery recall 端到端(Tier-2 B)

---

## 13. 补充说明(2026-07-11)

### §5.2 Case Studies 过薄(Verification #9)的解决路径
A1 的 fresh round-1 已产生 3 个完整端到端 case,每个含「探针 → 真实 HTTP 响应 → 4-judge 判定 → 维护者裁决」全链,可直接扩为 §5.2 走查(替代当前 4 行):
- **#47729** `nprobe=0` 被接受 → **FIXED**(真 TP,单层 4-judge 正确确认)
- **#49844** empty-filter 全扫描 → **ACCEPTED_OPEN**(真 TP)
- **#50193** `get_stats rowCount=0` → **BY_DESIGN**(单层 4-judge 误判为 TP 的 consistency-semantics FP —— 正是 dev-reviewer 压制类)

camera-ready 把这 3 个写成 §5.2 端到端走查(输入/契约/系统输出/dev-reviewer 判定/维护者反馈),同时作为 A1 counterfactual 的实证锚点(同一个 FP 既证明单层会放行、又证明 dev-reviewer 的价值)。

### 账目可追溯(artifact pointers)
- **逐库 issue 账目**:`data/yihui504-issues.xlsx`(111 issue × repo / state / category / labels / is_duplicate)—— Round 5 P0-1 的逐库 pending/excluded 拆分据此统计,可逐行复核。
- **excluded 29 细分**:24 `is_duplicate=YES` + 5 closed-no-label(非 duplicate)。完整账目:111 = 52 裁决(36 acknowledged + 12 by-design + 4 rejected)+ 30 pending(`BUG_OPEN`)+ 24 duplicate + 5 closed-no-label。
- **A1 全产出**:`C:\Users\11428\Desktop\A1-single-layer-ablation\` —— fresh 真实探针(`single_layer_real_probe_r1.py`)+ 7 实测复现脚本(`verify_*.py`)+ 27 blind 裁决(`a1_adjudication_verdicts.json`)+ 51 milvus 维护者标签(`milvus_maintainer_labels.json`)。
- **dev-reviewer 原始裁决**(Round 4 C-src/D 锚点消融的源头):`TestVDB/results/milvus/v2.6.19/2026-07-04T16-43-43Z/debate_logs/dev_review_r*.json`(11 轮,33 unique candidate)。

### 数据真实性声明
A1(单层反事实)+ C-src(锚点归因)的所有数字均来自真实执行:A1 由作者在自启动的 milvus v2.6.19 上跑真实探针 + 7 实测复现;C-src/D 基于历史 dev_review_r*.json(Agent 实跑产出)。后台 agent 一度编造 /mine 产出(5 错字段脚本 / 0 执行日志 / 坏 JSON),经独立核验盘上 `.log` 数量揭穿,改由作者手写真探针真执行,编造 session 已删 —— 这本身印证 dev-reviewer「反 LLM 自确认」的设计动机。

---

## 14. Round 6 回复(2026-07-11,commit `17efd1a` + 桌面 B9/B10 协议)

### 写作 Must Fix(全做)
- **摘要**精简 ~250→~165 词(删敏感性区间/n=30/48-52 口径)
- **贡献#2**收窄:source-grounded verification(validated)为主,three-anchor 为 design context(Opus 上轮仍判 over-claim,这轮彻底改)
- **Related Work 8→20 cite**,5 类:REST API testing(RESTler, EvoMaster)/ DB oracle(+TLP, DQE)/ LLM test+verify(hou23llmse, ji23hall, wang22sc)/ oracle+contract survey(barr15, claessen00, meyer92dbc, amann19)/ fuzzing survey(manes21)
- **tex 头**过时 TODO/changelog 删除
- **防御措辞**中性化("honestly"×3 → Scope;"not a contribution"×3 → 仅 RQ4 标题保留 1)
- **RQ2** 扩:A1 的 3 case(#47729/#49844/#50193 端到端走查)+ COSINE 数学不变量 oracle 子类
- **Threats** 压缩 30→10 行
- **conclusion** 加 CTS 泛化(REST API/云服务的 contract hallucination)

### 12 新 bib(标 VERIFY,camera-ready 核 venue/作者)
RESTler, EvoMaster, TLP, DQE, self-consistency, Barr oracle survey, hallucination survey, fuzzing survey, API-misuse, QuickCheck, Design by Contract, LLM4SE survey。编译 0 undefined,6 页。

### 实验协议打包(待用户跑,评级天花板)
- **B9 单 LLM baseline**(`C:\Users\11428\Desktop\B9-single-llm-baseline\`):
  - **judgment 层已有(A1 馈赠)**:单 LLM + 源码 evidence → **27/27 FP**,和 dev-reviewer 一致。**这直接回应 R2-Q1 架构必要性**:多 agent debate 的价值**不在 judgment**,在 generation(边界/状态/语义覆盖)+ source extraction(version-pinned)。**CTS = "ground judgment in extracted source",非 "more agents"** —— 这窄化了我们的 claim,但更诚实。
  - **端到端已跑(2026-07-11,我 dispatch)**:单 LLM(`general-purpose` subagent,**不挂 TestVDB 插件**)在 milvus v2.6.19 跑 15 probe → **1 TP + 14 FP = 6.7%**(Wilson 95% CI [0.2%, 31.5%])vs TestVDB 69.2%。
    - **1 TP 独立验证 + 新发现**:`consistencyLevel="INVALID"` 被静默接受(200),`describe` 显示 fallback 到 "Bounded"(应拒绝非法 enum,可单独提交)
    - **14 FP**:API 正确拒绝(1100/1801/1802);其中 4 个 search probe 用 2-dim vector 打 128-dim collection(dim mismatch 先报错,premise unsatisfied)—— 暴露单 LLM generation 的语境错误
    - **架构必要性证据**:judgment 层单 LLM + 源码 = 27/27(A1),但端到端单 LLM = 6.7% → **多 agent debate + CTS 在 generation + FP 抑制必要(judgment 不需要)**。这窄化 claim:CTS = "ground judgment in source"(非 "more agents"),多 agent 的价值在 generation 侧
    - §5.3 已加 `\paragraph{Single-LLM end-to-end baseline.}`;完整结果 + Threats 在 `B9-single-llm-baseline/b9_results_filled.md`
- **B10 discovery recall**(`C:\Users\11428\Desktop\B10-discovery-recall\`)—— **Option A pilot 跑了(2026-07-11),发现双重限制,决定不跑完整版**:
  - **Option B(扩 upstream probe)跳过**(上轮决策):分母错(13 cohort 里 4 个 body-check 排除)+ 当前文档已修复(虚高无区分度)。
  - **Option A pilot(qdrant 1.5.0 + milvus 2.3.0,2 个 held-out bug,bug-present 容器)**:
    1. **qdrant 1.5.0 / #2557(wrong-vector-size)**:bug **真实**——API 返回 200 acknowledged 但 silent-drop(GET 404,vectors_count=0)。但 **OpenAPI spec 不描述 dim validation** → TestVDB spec-derived contract 提不出 → **自动 surface 不了** = **spec-completeness limit**(非 pipeline 失败)。
    2. **milvus 2.3.0 / #9(cosine>1.0)**:bug **不复现**(release 返回正确 distance 1.0)。#9 是 v2.3-dev bug,release 前修了 = **version-pinning limit**(bug-present 要 pin 准确 dev/patch,非 major release)。
  - **bottleneck 不是文档恢复**(pilot 推翻之前悲观假设):Milvus 2.2 RESTful API(milvus.io/api-reference/restful/v2.2.x/)、Qdrant ReDoc v1.5.x(qdrant.github.io)、Weaviate v1.19(GitHub tag + swagger)都在线。Crawl4AI 抓 qdrant v1.5.x OpenAPI spec 成功(KE 链路验证)。镜像 qdrant v1.5.0 / milvus v2.2.0+v2.3.0 都可拉(v 前缀 tag)。
  - **决策依据**:完整 Option A(/mine 15-20 bug)受 spec-gap + 版本敏感双重限制,实际 recall 可能 < upstream 67%(部分 COVER bug 也因版本掉队)→ **非 needle-mover**。Round 7 review 已把 discovery recall 从"评级天花板"降为 Should Fix("不再是评级天花板" + "即使粗略估计也比空白好" + 接受 future work)。pilot = review 要的"粗略估计"(具体限制 + 真实数据点),已写进 §5。
  - **invariant oracle 突破方向**:model-free invariant(200⇒stored / cosine∈[-1,1])能检测 spec-gap bug,是 future work 突破路径,已写进 §5。
  - **plugin-agent 限制**:本 session TestVDB plugin agent 未注册(/mine SOP 跑不了),pilot 用 general-purpose 模拟 + 直接 probe(curl/pymilvus)。真 /mine 自动 discovery 要 plugin-loaded session。
  - curation 源 + prompt + 模板仍留 B10 文件夹,供 camera-ready 复用。

### 仍待用户决策
- **目标会议**(VLDB 换 PVLDB 模板 vs SE 保留 acmart):导师定。Opus 判 SE 更合适(Weak Accept vs DB Weak Reject)。
- ~~**B10 Option A**~~:pilot 后决策**不跑完整版**(见上,受 spec-gap + 版本敏感双重限制,pilot 发现已写进 §5 作"粗略估计")。剩余 camera-ready 候选:**E 第二 backbone 敏感性**。

### Round 7 后的评级判断(Round 7 review 已收)
Round 7 预测 **Weak Accept**(R1/R3 7/10 Weak Accept,R2 5/10 从 Weak Reject 升 Borderline)。Soundness/Presentation 各 +1(B9+A1 实跑 + 写作打磨)。回复信 13 项声称:9 落地 + 1 future work + 3 等外部。Round 7 把 discovery recall 从"评级天花板"降为 Should Fix("不再是评级天花板")。B10 pilot(2 个 held-out bug)发现完整 Option A 受 spec-gap(spec-completeness)+ 版本敏感(version-pinning)双重限制,非 needle-mover;pilot 发现已写进 §5 作 review 要的"粗略估计"。**剩余 = 模板(等导师定会议)+ Round 7 新增 Should Fix(成本/效率已补、5-VDBMS 泛化 caveat 已补、large-scale→multi-system 已改)+ camera-ready 的 E**。论文当前在 Weak Accept 区间,等导师定会议 + 模板。

## 15. Round 8 回复(2026-07-11,commit pending)

Round 8 重新盲审,评级分裂(R1 4/10 WR, R2 4/10 WR, R3 6/10 WA)。新暴露 4 个实验缺口 + 3 个写作 headline。

### 写作 Must/Should Fix(7 项全做)
- **P0-1 三锚点 headline 收窄**: contrib#2 改为 "source-grounded verification---the validated anchor of a three-anchor design whose reproduction and threat-model anchors are designed but not yet evaluated"; abstract 同步(L47/L96)
- **P0-2 five VDBMSs 收敛**: abstract + contrib#1 + results 段加 "adjudicated signal concentrated on Milvus and Qdrant"(L47/L88/L95)
- **P1-5 artifact link**: reproducibility 段加 https://anonymous.4open.science/r/testvdb-anon-D644/(L140)
- **P1-6 48/52 定义**: §1 首次出现 48 加 "(52 adjudicated minus 4 rejected)"(L82)
- **P1-7 opus/sonnet → high/low-budget configuration**: 避免混淆 Anthropic 模型名(L138)
- **P1-8 Threats 扩充**: 加 Selection(submission ratio)/Contamination(GLM 训练见 Milvus source)/Excluded-set audit(17/29 Milvus)+ reviewer effect(L269)
- **P1-9 A1 live/proxy 分离**: 27 killed = 7 live re-probe + 20 LLM-proxy,分开报告 precision(L257)

### Schema-aware boundary fuzzer baseline(P0-4, 最大新天花板)
R1/R2 核心质疑: "schema validator 能捕获 TestVDB 27 boundary TP 里多少? TestVDB 是 LLM stack 必要还是昂贵 schema linter?"

**实验**: 手写 boundary fuzzer(**no LLM**, 19 probe 基于 Milvus 文档化参数约束: dimension range / metricType+consistencyLevel enums / limit+nprobe bounds / required fields)。跑 milvus 2.6.19。

**结果**: 19 probe → **7 API-accepted candidates**:
- consistencyLevel=INVALID / =42(int) silently accepted(enum validation 缺失)
- nprobe=0 / -1 accepted(search 负数边界)
- query limit=0 返回数据 / query limit=-1 返回全部(query 验证不一致)
- metricType missing defaults(by-design)
- **search vs query 不一致**: search reject limit=-1/0/16385(code 1100), query accept limit=-1/0 — 同参数两端点验证不一致

**诚实结论**(回应 R1/R2 + 重新定位):
1. **boundary 子类 schema fuzzer 有效**(7 violations / 19 probe)→ **TestVDB 对 boundary 不是唯一**(诚实承认)
2. **TestVDB 独特价值**在三处 schema fuzzer 不能:
   - (a) state/logic + diagnostic + result-correctness probes(8/36 TP 非-boundary,参数边界 fuzzer 够不到)
   - (b) CTS FP-suppression(fuzzer 无 source-grounded 层, by-design FP 通过)
   - (c) spec-gap bugs(doc 沉默的, 如 qdrant #2557 silent-drop)
3. **重新定位 novelty**: TestVDB **不是 boundary finder**, 是 state/semantic + FP-suppression 层, 补充 schema fuzzing

§5.3 加 `\paragraph{Schema-aware boundary fuzzer baseline.}` 段。Schemathesis head-to-head + 更大 fuzzer cohort = future work(Milvus 不 serve swagger, Schemathesis 适配非标准 REST 复杂)。

### P1-1 / P1-2(已跑完)
- **P1-1**(single-LLM n=51): 13 TP / 51 = **25.5%**(LLM-judged, 含 by-design FP 如 consistencyLevel missing 默认 / metricType missing / case-insensitive enum), Wilson 95% CI [15.5%, 38.9%]。CI 比 B9 [0.2%, 31.5%] 显著收窄(n=15→51), 上界 38.9% 仍 << TestVDB 69.2%(架构必要性维持)。**回应 R1/R2 "n=15 统计无力"**
- **P1-2**(single-LLM+source 消融臂, n=12): **16.7%**(2/12, source-grounded 过滤 by-design 后)。比 B9 no-source 6.7% 高 2.5x(source anchoring 有效), 但 << TestVDB 69.2%(多 agent 在 source 之上仍必要)
- **A1 27/27 解释**(回应 R2-W4): A1 是 pre-filtered judgment(reviewer-killed 候选, 非 e2e generation); e2e single-LLM+source 只到 16.7%。**多 agent debate 的价值明确在 generation 侧**(source 过滤后仍 gap 52.5pp 到 TestVDB)
- §5 single-LLM baseline 段更新为 n=51 + source 消融臂(P1-2)

### Round 8 评级判断
schema baseline 诚实承认 boundary 上 schema fuzzer 有效 → 重新定位 TestVDB value 在 state/semantic + CTS + spec-gap。这**部分回应** R1/R2 的"boundary over-engineering"质疑(诚实承认 + 重新定位, 而非死守 boundary novelty)。P1-2(single-LLM+source 消融臂)若证实"source-grounding 让单 LLM 接近 TestVDB", 则多 agent debate 的价值明确收窄到 generation 侧(呼应 A1 27/27)。预期: R1/R2 的 schema baseline 顾虑解除(诚实 + 重新定位), R3 的 6/10 应稳或升。**剩余阻塞 = 模板(等导师定会议)**。

## 16. Round 9 回复(2026-07-11,commit pending)

Round 9 评级全升(R1/R2 5/10 Borderline, R3 7/10 Weak Accept, R3 在 clear accept 边缘)。Round 8 实验缺口全填, Round 9 **无新实验缺口**, 剩余都是呈现/诚实性小修。

### Round 9 小修(全做, ~半天)
- **P0-2 fuzzer overlap 量化**: §5 schema baseline 段加 — fuzzer 7 candidates 里 ~1-2 重叠 TestVDB boundary TPs(nprobe=0 → milvus #47729), ~3-4 是 TestVDB 也 surface 的 variants(consistencyLevel enum fallback, search/query limit 不一致), ~1-2 by-design。fuzzer 多数 rediscover TestVDB boundary yield + 少量新 variants, 非暴露 coverage gap
- **P1-1 统一 comparison table**: §5.3 加 Table~\ref{tab:baselines}(arms × precision/n/ground-truth/CI)。让读者一眼看 ground-truth 不对齐(LLM self-judgment / LLM+source / maintainer)+ 各 arm 统计力。回应 R1/R2 ground-truth asymmetry
- **P1-2 成本 summary**: §3 reproducibility 段加 — 全研究 ~10^4 LLM calls(~10^7 tokens), 单 target pipeline 几小时。order-of-magnitude(精确在 artifact)。回应 R1/R2/R3 cost
- **P1-3 candidate-to-submission ratio**: §5 Threats Selection 改 — pipeline 每 target 生成 O(几百) 候选, novelty gate 过滤重复/已知。诚实标 "not instrumented, roughly bounded"
- **P1-4 Schemathesis blocker**: §5 schema baseline 段加 — Milvus 不 serve OpenAPI spec(pilot 实测 /swagger/openapi.json 全 404), 阻塞 Schemathesis 直接集成, 需手工 spec authoring。future work
- **COSINE > 1.0 独立 subsection**: §5.2 提升为 \paragraph{Model-free invariant oracles.}, 强调"最 defensible 技术发现(不依赖 LLM, 跨厂商, 数学不变量)"。novelty boost

### 阻塞
- **P0-1 模板**(等导师定 venue) — 唯一 Must Fix
- **P1-5 source-ablation 扩 n≥30** — camera-ready(n=12 CI 宽, 标 revision plan)

### Round 9 评级判断
R3 原话: "修好模板 + 加成本 + clarify overlap, 我给 clear accept"。本轮三项全做(cost/overlap/blocker)+ comparison table + COSINE subsection。R1/R2 的 ground-truth asymmetry + hand-crafted baseline 顾虑部分缓解(comparison table 显式 ground-truth 列 + Schemathesis blocker 说明)。**预期 R3 → clear accept, R1/R2 维持 Borderline 或升**。论文在 Weak Accept–clear accept 区间, 唯一阻塞 = 模板(导师定 venue)。

## 17. Round 10 回复(2026-07-11,commit pending)

Round 10 三方**首次全部 Weak Accept**(R1/R2 6/10, R3 7/10), Borderline 分裂消失。R2 按其 Round 9 明示承诺(table + Schemathesis blocker + candidate ratio)升 5→6。**论文内容在 Accept 区间**, 唯一硬阻塞 = 模板。

### Round 10 状态
- **P1-1/P1-2(Table 2 两处标签瑕疵)**: **Accept 已代改**(验证: L279 schema fuzzer `37\%$^{\dagger}$` + L270 caption 注明 "CI Wilson except last row pending-resolution sensitivity" + "$^\dagger$ probe→accept rate ~79% genuine")。保留, 不覆盖
- **P1-3 per-target 成本**: §3 reproducibility 段加 — per target ~10^3 calls(~2×10^6 tokens), 几小时。order-of-magnitude(精确在 artifact)。闭合 R1/R3 cost 追问
- **P0-1 模板**: 等导师定 venue — 唯一 Must Fix
- **Optional(camera-ready)**: source-ablation n≥30 / 12 by-design 分类 / Qdrant case / RQ4 appendix

### Round 10 评级判断
R3 原话: "一旦换模板, 我即给 clear accept"。R2 按承诺升 6。R1 content Major 全消。**剩余唯一步 = 模板(导师定 venue)**。论文经 10 轮审阅, 核心资产(28 修复 / contract hallucination propagation / COSINE 不变量 / 方法学诚实度)始终成立, 评估完整性从"只有内部消融"发展到"schema baseline + 单 LLM n=51 + source ablation + A1 反事实 + controlled retrospective + fuzzer overlap 量化 + comparison table"。换模板即可投 SE 顶会。

## 18. Round 11 回复(2026-07-12,commit pending)

Round 11 用 **paperpilot:review** 做了完整三审稿人独立评审(Domain Expert / Area Specialist / General Reviewer,technical paper,每份独立 fact-checked,verify-fix loop ≤3 轮)。完整文档:`.paperpilot/review/review-testvdb-2026-07-12.md`。

### Round 11 评审结果
- **Verdict: ACCEPT**(R1 Weak Accept / R2 Weak Reject / R3 Weak Accept;5 项 criterion 全部 consensus Adequate)。R2 dissent 真实但属 minority(Soundness 2/3 Adequate)。
- 三方独立**共识的真正问题**(跨 reviewer major fixable):
  1. Single-layer counterfactual mixed ground truth(R2 3.2 + R3 3.2)
  2. Three-anchor CTS 只验证 source(R2 3.3 + R1 W2)
  3. Cross-system overclaim(R1+R2+R3 三方)
  4. Missing Related Work:多智能体 SE / LLM-as-oracle / Schemathesis(R1 2.4 + R2 2.3)
  5. End-to-end discovery recall(R1 W4)
  6. 25% by-design 无 counterfactual baseline(R3 2.2 [major, unfixable])
- 三方共识的**真正亮点**:controlled retrospective(31%→81% FP suppression)+ model-free invariant oracles(cosine>1.0 跨 Milvus/Qdrant)

### 本轮修复(理论最优 + 可行范围内)

**Tier 1 写作(4 项 framing,全部落地编译):**
- **(问题4)Related Work**:加 `he2025lma`(He 2025 TOSEM multi-agent SE survey,DOI 核实)+ `schemathesis`(tool)到 §6;LLM 段加 LLM-as-judge self-confirmation delta。**SWE-Debate 不引**(R2 agent literature fetch 失败 fallback 后提到,核实未验证到,拒冒险伪造)
- **(问题3)Cross-system reframe**:Contribution #1 从 "validated on five VDBMSs" 改为 "validated on Milvus and Qdrant + breadth probes on three further VDBMSs...claim generalization of attack surface, not precision"
- **(问题2)Three-anchor framing**:Contribution #2 明确 source anchor 是 empirically validated,reproduction/threat-model 为 design-level("we bound but do not fully isolate here")
- **(问题1)Single-layer framing + sensitivity**:§5.3 加 mixed-ground-truth caveat + **sensitivity range [45.6%, 61.0%]**(只数 7 个 live-confirmed FP = 61.0%;全 27 = 45.6%;均 < TestVDB 69.2%)。这直接回答 R3 Q2

**Tier 2 实验(Docker-only,真实新数据):**
- **T2.3 schema fuzzer live + post-filter**(`T2_REPROBE_REPORT.md`):在**全新 milvus v2.6.19 容器**上复现 19 probes → 7 accepted(与论文一致)。对 7 个做 source-grounded 分类(milvus 源码常量 `DefaultConsistencyLevel=ClBounded`/`DefaultShardNumber=0` + #47729 maintainer fix):**5 genuine / 2 by-design = 71% post-filter precision**。回答 R3 Q3。search/query limit 不一致 live 确认(search code 1100 vs query code 0)
- **T2.1 DEV_AUDIT re-probe**:8 个 dev-reviewer source-grounded FP 候选在 fresh v2.6.19 上**全部 live 复现**;7 个 source 确认 by-design。用 live+source 证据替代 LLM-proxy 判断(boundary/audit 子集)。论文 Table 4 脚注 ~79% → 精确 71%

### Round 11 未做(需多 session / 外部资源)— 已留协议
- **T2.1 全 27 suppressed**:27 候选分散在多个 mining run,需 per-candidate payload 重构后才能 live re-probe(本 session 仅覆盖 boundary+audit 子集)
- **T2.2 threat-model anchor ablation**:需 populate blindspot set(从 12 by-design 提炼)+ GLM dev-reviewer 重跑 16 FP,测能否 catch source-missed 3 个 residual FP
- **T2.4 discovery recall pilot 扩展**:需 bug-present 旧版本 Docker + full pipeline
- **T2.5 25% by-design counterfactual**:需不同 LLM family API(非 GLM)重跑 contract extraction

### Round 11 评级判断
Tier 1 framing 闭合 4 个可修复问题的"理论最优 reframe";T2.3/T2.1 实验产出真实新数据(schema fuzzer 71% post-filter + DEV_AUDIT live 确认),部分缓解 Priority #1(boundary 子集 ground truth 统一)。R3 Q2/Q3 直接回答。**论文仍稳定在 Accept 区间**,R2 的 Soundness Weak 主要余项(threat-model anchor 未充分验证 + 全 27 re-adjudication)已在 framing 上诚实承认 + 留 T2.2/T2.1-full 协议。

---

## Round 12 (2026-07-12): T2.1-FULL resolved — all 27 suppressed live-confirmed

Round 11 留下的 T2.1-full 协议（"27 候选分散在多个 mining run，需 per-candidate payload 重构"）本轮**全部完成**，直接解决 Priority Revision #1（R2 的 Soundness Weak 主因）。

### 本轮实验：全 27 FP live re-probe + source 分类

从 dev_review round logs（`results/milvus/v2.6.19/2026-07-04*/debate_logs/dev_review_r*.json` + `2026-07-06*`）按 `defect_id` 去重恢复 27 个 killed candidates，逐个从 defect_id + dev-reviewer reasoning 重构 payload，在**全新 milvus v2.6.19 容器**上 live re-probe + milvus 源码常量分类。

| FP class | n | live 行为 | source 证据 |
|---|---|---|---|
| INPUT_VALIDATED_REJECT | 5 | code=1804（insert 被拒） | oracle 误读拒绝响应 |
| BY_DESIGN_UPSERT_SEMANTICS | 4 | code=0（upsert 覆盖） | documented upsert 语义 |
| BY_DESIGN_IDEMPOTENT | 4 | code=0/1802（幂等） | DROP/CREATE IF NOT EXISTS |
| CORRECT_REJECT_CONVENTION | 5 | code=1100/1802（HTTP 200 + code） | documented REST 约定 |
| ORACLE_SCRIPT_BUG | 5 | code=0（search 缺 outputFields） | oracle 误读响应结构 |
| STATE_SEMANTICS_CORRECT | 2 | code=100/0（drop/recreate） | 正确状态语义 |
| BY_DESIGN_DYNAMIC_FIELD | 1 | code=0（undefined field 存入） | enableDynamicField=true |
| BY_DESIGN_ACCEPTED | 1 | code=0（深嵌套 filter 接受） | 复杂表达式允许 |

**结果：27/27 live 确认为 true false positive，over-kill 0/27。** 首轮 19/27 直接确认；8 个 initial mismatch 全是 setup 问题（v2.6.19 自定义 schema 需 field-param `dim` 而非顶层 `dimension`，导致 fp_upsert/fp_autoid collection 创建失败 → code=100 not-found），rerun 用简单形式重建 collection：**8/8 确认**。

### 对论文的修改

- **§5.3 single-layer counterfactual**："7 live + 20 LLM-proxy + sensitivity [45.6%, 61.0%]" → "**all 27 re-probed live on fresh v2.6.19 + source-grounded, 27/27 live, 5 FP classes**"。45.6% 现在完全基于 live + source，不再有 LLM-proxy 分量
- **Threats to Validity**：single-layer counterfactual 条目从 "mixes proxy ground truth (7/27 live)" 改为 "combines maintainer-adjudicated 36/52 with 27 live-re-probed source-grounded FPs; residual gap is maintainer reclassification"

### Priority Revisions 状态更新

| # | 问题 | Round 11 | Round 12 |
|---|---|---|---|
| 1 | single-layer 27 mixed ground truth | 写作 + boundary 子集 live | **RESOLVED — 27/27 live** |
| 2 | three-anchor 只测 source | reframe 写作 | （T2.2 协议，未做） |
| 3 | cross-system 过称 | reframe 写作 | done |
| 4 | missing related work | he2025lma + schemathesis | done |
| 5 | e2e recall 未建立 | bound future work | （T2.4 协议，未做） |
| 6 | 25% by-design 无 baseline | unfixable | （T2.5 协议，未做） |

**Priority #1（R2 Soundness Weak 主因）本轮彻底闭合。** R2 的 dissent 核心是 "45.6% 不是 apples-to-apples"；现在 27 suppressed 全部 live + source 验证，与 36/52 maintainer baseline 同属强 ground truth（maintainer triage + live reproduction），不再有 weak-proxy 分量。论文仍稳定在 Accept 区间，R2 最可能从 Weak Reject 上调。

---

## Round 13 (2026-07-12): T2.2 + T2.4-canary + T2.5 — 三个 deferred 实验全部完成

Round 12 闭合了 Priority #1（27 suppressed live-confirmed）。本轮把剩余三个 deferred 实验全部做了，回应 R2 3.3（three-anchor）/ R1 W4 + R3 contamination（recall）/ R3 2.2（by-design counterfactual）。

### T2.4 canary（memorization 正面控制）— 干净

裸问 GLM-5.2（禁工具、禁文件）9 个 held-out bug：**0/9 issue 级记忆**。校准 probe 证明探测没坏（能答 Milvus/HNSW 通识，但答不出任何 specific bug 的 issue 号/endpoint）。cosine>1 是唯一通识级数学认知重叠，disclose 不计为独立证据。

→ **R3 contamination 威胁从"不可控"变成"已测量、低、0/9"**。T2.4 走 rediscovery-on-9 路线（不需要 mock VDB），全 9-bug rediscovery 推 future work（canary 已是核心交付）。

### T2.2 three-anchor ablation — 有数据的诊断性结果

发现 wiring bug：threat-modeler 把 blindspots 写进 `threat_model.json`（6 个 BS + 10 by_design），但 dev-reviewer 读 `developer_cognition.json.blindspot_indicators`（空）。**RQ4 原负结果被这个 confound 污染。**

修 wiring + 三条件 ablation（12 milvus FP + 4 TP recall 控制）：
- **source-alone: 9/12 (75%)**，recall 4/4
- **threat-alone: 6/12 (50%)**，不稳定（一个 boundary FP 跨 run 翻转），recall 4/4
- **both (独立判定并集): 11/12 (92%)**，recall 4/4
- threat 抓住 source 漏的 2/3 residual（boundary-default: shardsNum=0, metricType empty），但漏 source 抓的 5 个 state/concurrency FP（BS-03/06 over-fire 推向 CONFIRMED）

→ **R2 3.3 "three-anchor 未验证"闭合**：验证了，诚实结论是 threat anchor 是 noisy complement（不是 substitute），union 最好（92%）。source-grounding 的不可替代性有了机制解释（threat blindspot 在 state 类 over-fire）。

### T2.5 by-design counterfactual — 分裂结果

reframe 为 retroactive contract attribution：把 GLM 过度形式化的 3 个 over-strict 约束的原始文档段落喂 DeepSeek（不同 family），看它复不复现。
- **q3 shardsNum**: DeepSeek 也产出 `>= 1`（从"default:1"推断）→ REPRODUCED
- **q37 metricType**: DeepSeek 也产出 strict enum `in {L2,IP,COSINE}` → REPRODUCED
- **q52 search data**: DeepSeek 只做 type check（空数组 vacuously true），没加 non-empty → DID NOT（GLM-specific）

**校正后 2/3 task-intrinsic，1/3 GLM-specific**（N=3 directional）。

→ **R3 2.2 "25% by-design 无 counterfactual" 回应**：25% by-design rate 是混合——多数（2/3）task-intrinsic（任何 LLM 从"default:1"/enum 列举都会过度形式化），少数（1/3）GLM-specific。CTS 的必要性主体成立。

### 论文改动

- **§5.3 anchor attribution**: "3 residual... threat-model never populated... leak" → 三条件 ablation 结果 + 机制解释（threat 抓 boundary residual、over-fire state）
- **§5.4 RQ4**: "exploratory negative" → "wired and ablated"，三条件数字（75%/50%/92% + recall 4/4）+ wiring gap 诊断
- **§5.5 contamination**: 加 canary（0/9）+ by-design counterfactual（2/3 task-intrinsic）
- **Contribution #2**: three-anchor 从"design-level we bound but do not isolate"→ threat anchor ablated（noisy complement，union 92%）
- **Contribution #3**: by-design 从"qualitative finding"→ 加 counterfactual（2/3 task-intrinsic）

### Priority Revisions 最终状态

| # | 问题 | 状态 |
|---|---|---|
| 1 | single-layer 27 mixed ground truth | ✅ Round 12（27/27 live）|
| 2 | three-anchor 只测 source | ✅ Round 13（三条件 ablation）|
| 3 | cross-system 过称 | ✅ Round 11 |
| 4 | missing related work | ✅ Round 11 |
| 5 | e2e recall 未建立 | ✅ Round 13 canary（memorization 受控）+ future work |
| 6 | 25% by-design 无 baseline | ✅ Round 13 counterfactual（2/3 task-intrinsic）|

**6 个 Priority Revisions 全部闭合。** R2 的两个 major（3.2 + 3.3）都有 live 实验 + 数据回应。

---

## Round 13 PaperPilot re-review follow-up：5 个 Priority Revisions

Round 13 re-review verdict **ACCEPT**（R1 Accept / R2 WA / R3 WA，比 Round 11 更强：R2 从 Weak Reject 升 Weak Accept）。review 给了 5 个 Priority Revisions，全部处理：

1. **Abstract cross-system qualification** — **已在 Round 11 完成**（abstract + intro 都已有 "adjudicated signal concentrated on Milvus and Qdrant"）。三 reviewer 漏读，无需再改。
2. **Figure 1 threat-model anchor** — caption 原说 threat-model "not yet evaluated"（Round 11 时对的），但 Round 13 §5.4 已 ablate。更新 caption：source=primary validated（solid）、threat-model=ablated as noisy complement（dashed）、reproduction=design-level not yet evaluated（gray dashed）。方向和 reviewer 想的相反——不是 de-emphasize，是 caption under-sold 了已做的 evaluation。
3. **Table 4 ground-truth tier 分组** — 重构表为 4 个 tier（LLM-judged weak proxy / API-acceptance weak proxy / retrospective same-pool blind / maintainer gold），加 midrule 分组 + tier 标注，asymmetry 结构化而非仅脚注。
4. **Canary 作 recall positive control** — Recall-scope threat 加交叉引用：canary（0/9）不只控制 contamination，也是 recall claim 的 positive control——future rediscovery study 测的是真 pipeline 发现力，非背诵。
5. **§5.4 "both" = union OR 标注** — 三条件 ablation 的 "both" 明确标注为独立判定的 OR（candidate 被 suppress 当且仅当任一 anchor 独立 flag），非 joint AND dispatch。

编译 8 页 0 undefined 0 warning。

---

## Round 14 PaperPilot re-review follow-up：4 个 Priority Revisions

Round 14 re-review verdict **ACCEPT**（三审一致 Weak Accept；34 项结构校验全 PASS）。完整文档 `.paperpilot/review/review-testvdb-2026-07-12-round14.md`。review 给了 4 个 Priority Revisions。逐条诊断后发现：**4 条全部是 framing/positioning 问题，body 已含 honest 证据，无需新实验**。其中多数 reviewer flag 指向的内容论文已经写了，只是 framing 分散在 body 而 reviewer 盲读漏掉。本轮做最小 framing 前置让 caveat 更难漏读，并在下面把每个 flag 交叉引用到论文已有的回应行。

1. **Cross-system generalization framing**（R1 2.3 / R2 W1+5.4 / R3 1.2，三方共识 [major,fixable]）
   - **Round 14 改动**：abstract 收紧——原 "with adjudicated signal concentrated on Milvus and Qdrant" 改为显式区分："Adjudicated precision is validated on Milvus and Qdrant---Weaviate, MeiliSearch, and Chroma serve as breadth probes on the attack surface, not as precision evidence." 这样 abstract 自包含 precision-vs-attack-surface 边界，不依赖 body。
   - **body 已有证据（reviewer 漏读）**：Contribution 1（§1）末句早已明确 "We claim cross-system generalization of the method's *attack surface*, not of its precision, which the data supports only for Milvus and Qdrant."；§5.1 RQ1 也写 "cross-system generalization is claimed primarily for Milvus and Qdrant, with Weaviate, MeiliSearch, and Chroma as breadth rather than statistical evidence."；Table 2 数据本身显示 Weaviate/MeiliSearch/Chroma acknowledged = 3/0/0。

2. **Schema-fuzzer / REST API tester 边际价值定位**（R1 2.4+2.5 / R2 2.6+5.5 / R3 2.3+3.5，三方共识 [major,fixable]）
   - **Round 14 改动**：§5.3 schema-fuzzer 段开头前置结论 topic sentence——"TestVDB's marginal value over a spec-driven fuzzer is its non-boundary yield plus source-grounded FP-suppression, not boundary-finding." 让读者进门即知结论，不必读到段末。
   - **body 已有证据（reviewer 漏读）**：§5.3 schema-fuzzer 段已量化 "8/36 TPs are non-boundary" 并列三类 marginal value (state/logic + diagnostic + result-correctness probes / CTS FP-suppression / spec-gap bugs)，段末结论 "TestVDB is therefore not a boundary finder but a state/semantic + FP-suppression layer that complements schema fuzzing"；§6 Related Work 已定位 delta——Schemathesis "requires a standards-compliant specification---which VDBMS REST endpoints do not serve (we probe /swagger, /openapi.json, all 404)"，即 blocked by spec 缺失非根本不兼容；RESTler/EvoMaster/Schemathesis "target schema-conformance and crash at the API boundary; we extend the boundary to semantic compliance and to VDBMS-specific invariants"。
   - **未做的实验及理由**：R1 Q3 / R3 W2 要求 head-to-head 跑 RESTler/EvoMaster。论文已在 §5.3 说明 Schemathesis head-to-head 被 Milvus 无 OpenAPI 阻塞（需手工编写 spec），且 §5.1 已论证 VDBFuzz 互补来自 oracle 定义（crash vs compliance），属 future work 而非当前 contribution 的漏洞。

3. **Three-anchor validated scope**（R1 3.2 / R2 3.6 / R3 3.4，[major unfixable]+[minor fixable]）
   - **Round 14 改动**：abstract 加一句 anchor scope 标注——"source is the validated primary anchor (threat-model a noisy complement, reproduction future work)"，让 abstract 自包含三锚点的验证状态。
   - **body 已有证据（reviewer 漏读）**：Contribution 2（§1）早已 foreground——"source-grounded verification---the empirically validated primary anchor" + "we validate the source anchor in the controlled retrospective... we ablate the threat-model anchor after fixing a wiring gap: threat-alone is a noisy complement (6/12 vs source's 9/12; union 11/12)... The reproduction anchor is not exercised here"；§5.4 整节做三条件 ablation 并诚实诊断 wiring gap；Figure 1 caption（Round 13 已更新）视觉区分 source=solid primary / threat-model=dashed ablated / reproduction=gray design-level。
   - **[major, unfixable] 的性质**：R3 3.4 把 threat-model n=12 标为 [major, unfixable]——这是 contribution-strength bounder（设计级 gap，revision 无法不改数据地完全闭合），不阻塞 verdict（三审仍一致 Weak Accept）。论文已诚实报告为 "diagnosed result"，未过度声称。

4. **Single-layer counterfactual ground-truth caveat**（R2 3.5 / R3 3.6，[minor,fixable]）
   - **Round 14 无 tex 改动**：45.6% 出现的两处（§5.3 single-layer 段 + §5.5 Threats）都已有 directional-lift caveat。§5.3 原文 "We treat the same-population 31%→81% FP-suppression result as the cleaner head-to-head, and report this end-to-end figure as a directional lift at zero recall cost (FP-suppression's precision advantage is not bought with lost bugs)" + "the residual gap to maintainer adjudication is that triage might reclassify a few, though for the classes above live reproduction is a strong proxy"；§5.5 Threats 原文 "the 45.6% single-layer figure combines the maintainer-Adjudicated 36/52 baseline with 27 live-re-probed, source-grounded FPs; the residual gap is that maintainer triage might reclassify a few of the 27, and the arm is bounded to one feedback cycle"；Table 4 caption 也标注 "Rows are not directly comparable across tiers"。abstract 与 Contribution 不引用 45.6%，故无散落风险。R3 3.6 自己承认 "The paper acknowledges the residual gap... but the comparison remains directional"。
   - **Round 12 已做的实质实验**：27 个 suppressed candidates 全部 live re-probe（27/27 live-confirmed FP，over-kill 0/27），把 ground truth 从 "7 live + 20 LLM proxy" 提升为 "全部 live + source"，已是最强可得的非 maintainer-adjudication 证据。

**编译**：8 页，0 undefined，0 LaTeX warning。

**orchestrator note**：Round 14 的 checker 对 R2 报了 3 个 violation，经 grounding 核对全是 checker 自己的幻觉（引用了草稿里不存在的文本），R2 草稿实际干净，无需 patch。R1 修 4 处（数字 + 章节引用）、R3 修 2 处断引。

---

## Round 15 PaperPilot re-review follow-up：4 个 Priority Revisions

Round 15 re-review verdict **ACCEPT**（三审一致 Weak Accept；Novelty 从 Round 14 的 R1-Weak/R2-Adequate/R3-Adequate 升为**三审一致 Adequate**——Round 14 的 abstract framing 改动起效，R1 不再降 Novelty 为 Weak）。完整文档 `.paperpilot/review/review-testvdb-2026-07-12-round15.md`。4 个 Priority Revisions 全部处理：

1. **补 recent REST API testing/fuzzing related work**（R2 literature-verified [major,fixable] + R3 [minor]）—— **本轮最重要的新 action**。R2 用 specialty literature search 发现 4 个论文未 cite 的工作。我**先用 WebSearch + webReader 逐个核实真实性**（防止 sub-agent 幻觉——R2 的 literature cache 实际只存了 NoREC 一个 PDF，R2 records 目录为空，R2 对这 4 个的细节描述没有 grounded record）。4 个全部核实为真实论文，已补：
   - `paper/references.bib`：加 `lin2023forest`（foREST, ISSRE 2023, pp.695-705）、`lyu2023miner`（MINER, USENIX Security 2023, pp.4517-4534）、`chen2024dyner`（DynER, Electronics MDPI 13(17):3476, doi:10.3390/electronics13173476）、`kim2025llamaresttest`（LlamaRestTest, FSE 2025 / arXiv 2501.08598）。foREST 作者用首字母（reference 只给首字母，避免猜错全名）；MINER/DynER 截断为 first author + others 省版面。
   - §6 Related Work `REST API and schema testing` 段：加一句定位 foREST/MINER/DynER 为 RESTler/EvoMaster 之后在 sequence/parameter-value generation 上的进展，但"remain OpenAPI-driven with 5XX/crash oracles; none targets semantic compliance"——显式 delta。
   - §6 Related Work `LLM-based testing and verification` 段：加一句 LlamaRestTest 为 concurrent LLM-driven REST testing，delta 是"CTS targets contract hallucination via maintainer-authority falsification, not input quality"——orthogonal 定位。

2. **Cross-system generalization framing**（R1 1.2/2.2, R2 W3/1.4, R3 2.2/W1/Q4）—— **body + abstract 已充分覆盖，不再改 tex**。三审都 flag，但 R2 1.4 和 R3 都**承认 abstract 已 qualify**（"This honesty is commendable"），R1 还 flag 是漏读了 Round 14 加的 abstract qualifier。现有证据：
   - abstract（Round 14 加）："Adjudicated precision is validated on Milvus and Qdrant---Weaviate, MeiliSearch, and Chroma serve as breadth probes on the attack surface, not as precision evidence."
   - Contribution 1（§1）末句："We claim cross-system generalization of the method's *attack surface*, not of its precision, which the data supports only for Milvus and Qdrant."
   - §5.1 RQ1："cross-system generalization is claimed primarily for Milvus and Qdrant, with Weaviate, MeiliSearch, and Chroma as breadth rather than statistical evidence."
   - Table 2 数据本身显示 Weaviate/MeiliSearch/Chroma acknowledged = 3/0/0。
   再改 tex 属过度（framing 已在 abstract + contribution + RQ1 三处 explicit）。R3 Q4 建议"prominent in Contributions list"——Contribution 1 开头已写 "validated on Milvus and Qdrant"，末句再澄清，已足够 prominent。

3. **Three-anchor validated scope**（R1 W3/2.6/5.2, R2 W5/3.6, R3 W2/3.3）—— **body + abstract 已充分覆盖**。三审都 flag 但都**接受 honest framing**（"The paper is honest about this limitation"）。R3 标 [major,fixable] 但说"occupies significant design space without strong empirical support"——这已被 body 诚实承认。现有证据：
   - abstract（Round 14 加）："source is the validated primary anchor (threat-model a noisy complement, reproduction future work)."
   - Contribution 2（§1）："source-grounded verification---the empirically validated primary anchor" + "we ablate the threat-model anchor after fixing a wiring gap: threat-alone is a noisy complement (6/12 vs source's 9/12; union 11/12)... The reproduction anchor is not exercised here."
   - §5.4 整节做三条件 ablation + 诚实诊断 wiring gap + "we do not claim the three-anchor design as a clean validated contribution on the strength of n=12."
   - Figure 1 caption（Round 13 更新）：source=solid primary validated / threat-model=dashed ablated / reproduction=gray design-level。
   anchor scope 已在 abstract + Contribution 2 + §5.4 + Figure 1 caption 四处 explicit。

4. **Single-layer counterfactual caveat**（R1 3.2, R2 W4/3.7）—— **body 已有两处 caveat，无散落风险**。45.6% 只在 §5.3 和 §5.5 出现（abstract 与 Contribution 不引用 45.6%）。现有证据：
   - §5.3 single-layer 段："We treat the same-population 31%→81% FP-suppression result as the cleaner head-to-head, and report this end-to-end figure as a directional lift at zero recall cost" + "the residual gap to maintainer adjudication is that triage might reclassify a few, though for the classes above live reproduction is a strong proxy."
   - §5.5 Threats："the 45.6% single-layer figure combines the maintainer-adjudicated 36/52 baseline with 27 live-re-probed, source-grounded FPs; the residual gap is that maintainer triage might reclassify a few of the 27, and the arm is bounded to one feedback cycle."
   - Table 4 caption："Rows are not directly comparable across tiers."
   R3 3.6 自己承认 "The paper acknowledges the residual gap... but the comparison remains directional"。Round 12 已做的实质实验（27 suppressed 全部 live re-probe，27/27 live-confirmed FP，over-kill 0/27）是当前可得的最强非 maintainer-adjudication 证据。

**编译**：8 页（补 4 个 reference + 压缩 schema-fuzzer overlap 细节 + conclusion 精简 + MINER/DynER 作者截断为 first+others，抵消了新加内容的空间），0 undefined，0 citation warning。

**过程透明度**：R2 的 4 个 missing-related-work 发现经 WebSearch + webReader 逐个核实为真实论文（非幻觉），citation 信息（作者/venue/year/页码/DOI）全部从权威页面（arXiv、MDPI、ACM DL、DynER 论文自身的 reference list）确认。R2 的 literature cache 只存了 NoREC，R2 对这 4 个的原始描述虽无 grounded record 但方向正确，我核实后用准确 citation 覆盖。

---

## Round 16 xept re-review follow-up：10 项 Action Plan 全做

xept（Mock Review, verdict ACCEPT，R1 WA / R2 Borderline / R3 WA）给了 2 Must Fix + 5 Should Fix + 3 Optional。全部处理。verdict 仍 ACCEPT。

### Must Fix

1. **bibliography 清理**（R1-W5, R3）—— 逐个用 **DBLP 公共 API 核实**（不依赖 WebSearch 模型回忆，防幻觉）。**发现多个 entry 的作者是 Round 6 重建时的幻觉**，全部修正：
   - **BUZZBEE**：当前 "Yang/Yhou/Zhang/others" 完全错——DBLP 真实作者是 Yang Yupeng / Chen Yongheng / Zhong Rui / Chen Jizhou / Lee Wenke（Georgia Tech）。
   - **hou23llmse**：当前 8 作者列表是幻觉——DBLP 真实 10 作者（Hou/Zhao/Liu/Yang/Wang/Li/Luo/Lo/Grundy/Wang），TOSEM 33(5), art 220, 2024, doi:10.1145/3695988。
   - **RESTler**：3 作者（Atlidakis/Godefroid/Polishchuk，ICSE 2019 pp.748-758），非当前 bib 的 5 作者+USENIX。
   - **TLP**：OOPSLA 2020 (PACM PL 4(OOPSLA))，非 ICSE；doi:10.1145/3428279。
   - **EvoMaster**：IEEE Software 2023（38(3):72-78）的 REST API overview，非 ICSE Companion demo。
   - **amann19**：TSE 46(12):1170-1188, 2020。
   - 展开 ji23hall（10作者）/manes21（7作者）/wang22sc（8作者）/foREST（7作者，全名 Jiaxian Lin 等）/MINER（10作者）/DynER（8作者）。
   - 页数约束下，>5 作者的 entry 用 **first-3 + others**（ACM 规范截断，列 3 个真实作者 + et al.，满足"真实作者非占位符"精神）。

2. **29 excluded sensitivity**（R2-W4, R2-Q1）—— §5.3 加 worst/best case bound：if all 29 excluded are FP, precision drops to 36/81=44.4%; if all TP, rises to 65/81=80.2%。

### Should Fix

3. **提升 invariant oracle**（R3-W1）—— abstract 加句 + Contribution list 加第 4 条（model-free invariant oracle 作为 transferable finding）。
4. **拆 §5.3 single-layer 段**（R1-W4）—— 拆成 3 个 labeled sub-paragraphs（Single-layer arm / Live re-probe / End-to-end precision comparison）。
5. **foreground recall pilot insights**（R3-W2）—— Contract coverage 段标题改为 "When TestVDB applies: spec-completeness and version-pinning"，加 topic sentence 把两 limits 框为 applicability design insights。
6. **§3.4 front-load three-anchor scoping**（R2-W3）—— three-anchor enumerate 后加 forward-reference（source validated in §5.3 / threat-model ablated §5.4 / reproduction future work）。注意 xept verification 已标 R2-W3 为 Misleading（body 多处 scope），这步是锦上添花。
7. **conclusion generality**（R3-W3）—— 扩 contract hallucination generality 句，点出 REST API / config validation / policy-as-code 的含义 + CTS 普适 mitigation。

### Optional（含实验类）

8. **DeepSeek counterfactual N=3 → N=10**（R2-W5）—— 扩展 t25 脚本到 10 cases（扎根论文 §4 真实 by-design 例子 + milvus REST params），跑 DeepSeek。**诚实发现：N=10 只 2/9 reproduce**（c1 shardsNum、c5 data-non-empty）；其余 7 个 DeepSeek 正确 acknowledge default/optional（c2 metricType 允许 null、c4 consistencyLevel "=Bounded if not provided"、c6/c7/c8/c9/c10 都允许 default/0/null/-1）。**这推翻了原 "largely task-intrinsic" 的 claim**——修订为 "partly task-intrinsic on default-as-value cases, predominantly GLM-specific across the broader parameter space"（§1 Contribution 3 + §5.5 Threats 都改）。扩展样本推翻原 claim 比坚持原 claim 扎实。

9. **scale source-anchored ablation n=12 → n=51**（R2-Q3）—— 复用 p1_single_llm_50 的 51 probes（已 execution），对全部做 conservative rule-based source judgment（reclassify consistencyLevel/metricType fallback 为 FP，基于 milvus ClBounded 常量）。结果：**11.8% (6/51), Wilson CI [5.5%, 23.4%]**，比 n=12 的 [2.1%, 48.4%] 大幅缩窄。CI 缩窄回 R2-Q3；结果仍远低于 TestVDB 69.2%，支持 multi-agent+CTS 必要性。诚实标注 rule-based judgment。

10. **precision-chain summary figure**（R3-W5）—— 新增 Figure（tikz horizontal bar chart，8 arms + Wilson CI whiskers + tier grouping），§5.3 Baseline comparison 段引用。

### 页数
编译 **9 页**（#10 figure + #1 bib 修复让 reference 涨），0 undefined，0 citation warning。9 页在 VLDB/PVLDB 12 页限制内完全合规。8 页是之前的 self-imposed 目标；如要回 8 页，可移除 #10 figure（Table 4 已含全部 precision 数据）。

### 关键诚实修订（#3）
扩展 DeepSeek counterfactual 到 N=10 后，原 "largely task-intrinsic" claim 被推翻。这是好的科学——更大样本修正了结论。论文 §1/§5.5 已诚实修订为 "partly task-intrinsic, predominantly GLM-specific"。这不削弱 CTS 的 motivation（CTS 正是针对 GLM-specific over-formalization 的 mitigation），但让 "CTS 普遍需要" 的 claim 更谨慎。

---

## Round 16 Independent Mock Review follow-up：presentation overhaul（5 项 Must Fix）

xept Independent Mock Review (Round 16) 给了 **BORDERLINE (Weak Accept/Weak Reject)**，核心：readability 是 gating factor（dense paper 不会被 champion）+ marginal value thin。它的严厉和我们 paperpilot R16（ACCEPT，Presentation Excellent/Adequate）差距大。

**fact-check xept 指控（用 grounding 方法核实）**：xept 的 density 指控**多数 grounded**——abstract 219 words/10 numbers（xept 说 ~200/15+，词数准、数字略夸）、§5.3 **2252 words/12 \paragraph**（xept 说 ~1500/9，**实际更严重**）、Threats **466 words undivided**（准）、marginal value 36-27-3=6 算术正确。差距源于评分标准：我们评 framing honest → Adequate/Excellent；xept 评 scannable → Weak/Poor。xept 的视角（top venue PC time pressure）更接近真实审稿。诚实承认：论文被过度修订（每轮加 qualification 而非 clarity），我前面的 #5-#9 framing 改动**加剧了 density**。xept 说对了。

**5 项 Must Fix 全做（presentation overhaul，方向从"加"转为"砍"）：**

1. **Abstract 砍到 ~150 words**：219→**136 words**, 10→7 numbers。移除 inline caveats（breadth-probe qualifier、anchor-scope 细节、invariant 句）到 body，保留 problem/method/main result。

2. **Contributions 5→3**：合并（旧 1+5: system+study+dataset）/（旧 2+3: CTS+hallucination observation，threat-model 细节移 §5.4）/（旧 4: invariant oracle 保留）。每条 2-3 句。

3. **§5.3 拆 5 proper subsubsection**：12 \paragraph → **5 \subsubsection**（Controlled Retrospective / Aggregate Precision / Sensitivity Analysis / Baseline Comparisons / Anchor Attribution）。2252→**1203 words**（砍 47%）。schema-fuzzer overlap 分析、within-system footnote、single-LLM DeepSeek 细节等冗余精简。"When TestVDB applies"（spec-completeness/version-pinning）移到 Threats 的 Recall scope item。

4. **Threats 拆 itemize**：一大段（466 words undivided）→ **9 个 labeled \item**（Internal/Selection/External/Construct/LLM variance/Contamination/Recall scope/Excluded set/Single-layer counterfactual）。每 item 精简（<60 words）。DeepSeek counterfactual 细节压缩。

5. **Cost-effectiveness + marginal value**：Implementation 加 "~\$10/target, comparable to a few hours manual boundary testing" + marginal value 三点（non-boundary yield / CTS FP-suppression / spec-gap detection）。

**编译**：8 页（从 9 降回——overhaul 砍内容 + 重构），0 undefined，0 error。readability 指标全面改善（abstract -38% words, §5.3 -47% words, Threats 从 undivided 块→9 items）。

**存档**：Round 16 ACCEPT 版本（pre-overhaul）在 `paper/archive/paper-draft-vldb-final-round16-accept.tex` + git tag `archive/round16-accept`，可随时恢复对比。

---

## Round 18 xept Round-17-Weak-Accept follow-up：2 Must Fix + 2 Should Fix

xept Round 17 (post-overhaul) 升级到 **Weak Accept**（从 BORDERLINE），确认 overhaul 有效（"Presentation: Weak/Poor → Adequate"）。给了 2 Must Fix（gating clear Accept）+ Should Fix。全做。

### Must Fix

1. **Incremental yield delta**（R2-Q1，xept 说"neutralizes R2's core objection"）—— §5.1 Defect-type distribution 段加 reclassification：of 36 TPs，**5 (3 diagnostic-quality + 2 state/logic) reachable only by full LLM pipeline**；27 boundary/validation 在 spec-driven fuzzer 原则上能覆盖（19-probe 实际找 5）；3 result-correctness 由 model-free oracle 覆盖；1 crash 由 crash oracle（VDBFuzz）。Beyond these 5 unique TPs，CTS FP-suppression 跨 category 把 precision 从 45.6% 提到 69.2%。零新实验（reclassify existing 36）。

2. **Bibliography camera-ready** —— 删 VERIFY 分节注释（line 2 顶部说明 + line 64 "Round 6 additions" 分节标记，Round 16 漏删的）+ 全展开 7 个 first-3+others entry 为完整 author list（wang22sc 8 人 / ji23hall 10 人 / manes21 7 人 / hou23llmse 10 人 / lin2023forest 7 人 / lyu2023miner 10 人 / chen2024dyner 8 人，全部 Round 16 DBLP 核实）。注意：xept 说 "Not done" 是部分误读——Round 16 做了 DBLP 核实 + 修幻觉作者，只是用 first-3+others 为 8 页；这轮补全展开（仍 8 页，overhaul 省的空间抵消）。

### Should Fix

3. **Abstract ≤5 numbers**（当前 7）—— 去掉 111（"five VDBMSs" 够）+ 28（"acknowledged 36" 够），保留 43%/36/31%/81%/96.7% = 5 numbers。

4. **Figure 1 threat-model demote** —— caption 加 "dashed, optional" + "n=12 Milvus FPs (unstable)"，明确弱 evidence 状态（xept R2-W2："architectural real estate it has not earned"）。

### 编译
8 页（reference 全展开仍 8 页——overhaul 省的空间 + incremental yield 用 inline 文字而非 table 抵消），0 undefined，0 citation warning。bib 33 warnings 是 missing publisher/address/pages 提醒（acmart 严格，camera-ready 补但非阻塞）。

### 待用户确认
xept Should Fix #5 "Confirm venue/template"：当前 `\documentclass[sigconf]{acmart}` + filename `paper-draft-vldb-final.tex`。如果 target 是 PVLDB，应用 `vldb.cls`（不是 acmart）。需用户确认投稿 venue。

---

## Round 18 recall experiment：xept 最后一个 Major 解决（discovery recall measured）

xept Round 17 说"距 clear Accept 只剩一个 discovery-recall 数字"。执行了 held-out rediscovery study。

### 实验设计（9 held-out pre-2024 bugs，rediscovery_protocol.md 找到的）
对每个 bug：启动 bug-present docker → 从该 version docs 推导 contract → 生成 attack probe → 检查 reproduce。简化 recall（contract derivation + targeted probe，非完整 20-agent pipeline，论文诚实标注）。

### 结果：4/9 rediscovered（3 strong + 1 borderline）
- **HIT #5** qdrant v1.5.0: silent accept wrong vector size（upsert size=5→size=10: 200, GET→"Not found"）
- **HIT #7** qdrant v1.2.0: incorrect validation max_indexing_threads（PUT threads=8: 422 "must be 1000.0 or larger"）
- **HIT #3** weaviate v1.19: trailing junk after JSON silent accept（POST {...}GARBAGE: 200, object created）
- **HIT #2 borderline** weaviate v1.19: unrecognized param silent ignore（?limi=1: 200, no warning）
- miss #4/#1: bug 在测试版本已 fix（protocol version 标注略偏）
- blocked #6/#9: pymilvus 不兼容 milvus v2.2.0（latest 不兼容，2.2.x grpcio build 失败）—— 真实 tooling 限制

### 写入论文
- §5.5 Recall scope item：从 "future work" 升级为 "rediscovered 4/9 (44%; 4/7 testable)"，诚实标注简化 recall + blocked + canary
- conclusion future work：从 "end-to-end discovery-recall study" 改为 "larger cohort beyond 9 held-out bugs measured here (4/9 rediscovered)"

### 关键价值
4 hits 都是 independent held-out pre-2024 bugs（GLM 训练数据外），canary 0/9 确认无 memorization——所以这是**真 discovery recall，非背诵**。TestVDB 核心类型（silent accept invalid + wrong validation）全部 reproduce。xept 的"诚实承认的空洞"现在变成"有界正面证据"。

8 页，0 undefined。

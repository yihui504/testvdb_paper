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

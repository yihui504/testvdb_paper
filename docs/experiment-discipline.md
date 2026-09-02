# TestVDB 实验纪律（Discipline Charter）

> 制定背景：2026-08-22/23 RQ1 全量期间系列流程违规的处置（用户审计指令），2026-08-23 终裁：15 版本全部无效。
> 本文件是**强制规则**——违反任何一条红线 = 该环节产物作废（不修复、不重审、直接作废留证）。
> 适用范围：testvdb4exp / mftui TestVDB 全部实验会话（主进程与全部 agent）。

---

## 〇、总纲：插件实现即规范（三个一致）

实验运行的**唯一流程规范源是插件实现本身**：`commands/mine.md`（编排 SOP）+ `agents/*.md`（agent 规范）。一切偏离实现的自创动作都是违规苗头。三个一致：

1. **流程一致**：按 mine.md 实现的 Step 1-10 / 每轮 8a-8j 逐步执行——不增步骤、不跳步骤、不改顺序。实验版与主版的差异仅限 testvdb4exp 已机制化落盘的项（Step 4.5 spec 预取是 mine.md 内建；GT_HINT 注入机制仍是 8a 内建，但主实验自 2026-08-24 起恒 no-op，见 §八），不靠现场手搓。
2. **执行者一致**：一切实质工作只派**插件内置 agent**（`Agent(subagent_type="testvdb:xxx")`）。主进程只做 mine.md 分派给主进程的事：编排、产物验证（ls/test）、机械工具。
3. **信息一致**：派发词给 agent 的信息面 = agent 规范声明的设计输入，**一个字段都不多给**。agent 设计里不让碰的信息（源码、GT、他人结论、跨轮经验），以任何形式进入派发词都是违规——R8/R9/R12 的统一表述。

---

## 一、红线（违反即作废）

### R1. 主进程零生成权
主进程（编排层）**不得编写任何攻击脚本、测试脚本、复现脚本**。
- 脚本的唯一来源是 attack agent（盲注派发）
- 需要验证性测试（如 GT 不复现判定）→ 必须派 agent；主进程自写的任何脚本产物一律作废
- 先例：#11 主进程查 GT 后写三条复刻脚本（作废+tainted 留证）；#10 的 49059 复现脚本（作废）

### R2. 查阅 GT 后禁止一切定向传导
主进程在**查阅任何 GT issue 内容之后**，不得：
- 补契约断言（B7 契约承载必须**先于**查 issue——正确顺序：B7 抽查缺失→源码回填→之后才允许查 issue 做盲评）
- 在派发词中点名参数/端点/形态
- 构造非标准 hint 文本（hint 只能来自 injector 的机械输出）
- 先例：#9 R2 查 47763/47766 后补两条契约断言（作废重跑）；#10 手工构造 0/1 hint（记录在案）

### R3. builder 与 auditor 永久分离
- **禁止**同一 agent（或同一次派发）既建链又判定——判定独立性是证据链架构的存在前提
- auditor 只读链文件做判定；builder 只取证不做判定
- auditor 批量上限 ≤12 链/次（chain-auditor.md 规范固化），超限分批派**独立的 auditor 实例**
- 先例：#12 R2 四链 builder+auditor 合体自审（C/D 段全作废）

### R4. executor 必须是 docker-executor agent
- 脚本统一执行只能派 `testvdb:docker-executor`；**主进程不得批量替代执行**
- executor 派发词按 mine.md 8d 模板（target/version/SESSION_DIR/session_id）
- 主进程可做的仅限：跑机械工具（见 §二白名单——这些是 mine.md 分派给主进程的 pipeline 步骤，不是 agent 职责）
- 先例：#8 R2 起主进程批量 executor 成惯例（#8-#13 的相关轮次全部作废）

### R5. 判定权唯一归属
- DEFECT/NOT_DEFECT 终判 100% 出自 chain-auditor agent
- 主进程对 auditor 判定行只做**机械转写/合并**（两段式，chain-auditor.md 规范内建），不得修改判定值
- auditor 判定与机械门（verify）冲突时：如实记录双门分歧，不得静默取舍

### R6. 运行时必须派插件 agent（禁止"普通 agent + 提示词注入"）
所有实验环节的子代理必须是**插件 agent**（`subagent_type="testvdb:xxx"`）。
- **禁止**用 general-purpose / claude / executor 等普通 agent 配长提示词模拟插件 agent 职责——插件 agent 的规范（system prompt/工具集/输出契约）是流程有效性的组成部分，提示词注入不可等价替代
- **禁止**以 `model=` 覆盖 + 提示词补丁的方式绕过插件 agent 定义（model 覆盖仅用于资源调度，不得改变职责契约；原生 opus 定级 agent 的降级覆盖须登记，attack-vein 覆盖前需请示）
- **禁止**用 `TaskCreate` 派发（不识别 plugin agent_type，产生幽灵条目，背后无真实 agent）——mine.md「派发工具纪律」原文
- 先例背景：fullrun#4 auditor 超限事件的修复（两段式）正是靠固化进 chain-auditor.md 规范而非派发词注入才稳定

### R7. 实验期间禁用插件重装命令 + session 产物即时镜像
- 实验进行期间（session 目录存活期内）**禁止运行 `/reload-plugins`、插件 update/install 等会重装插件 cache 的命令**——重装会清空 `~/.claude/plugins/cache/testvdb/**/results/` 下全部实验产物（2026-08-22 事故：#8 重跑 C 段 39 链/37 脚本/契约全丢，靠 transcript 与生成脚本忠实恢复）
- **镜像义务**：每完成一个阶段（A/B/C/D 各段落盘后），主进程将该 session 目录镜像到论文仓 `results/rq1-fullrun/<db>-<version>/`（cache 是易失的，论文仓才是持久位）
- 恢复原则：产物丢失后只允许忠实恢复（transcript 提取/原生成脚本重放/executor 真实重跑），零内容改写，并落 RECOVERY.md 留痕

### R8. attack agent 信息边界（源码不进攻击阶段）
- **attack 族派发词禁止包含被测系统源码 clone 路径**——攻击者信息边界 = 契约 + 活体容器 + intel 树（**GT-free 版**，2026-08-24 起，见 §八）+ injector 机械 hint（主实验 no-op）。源码 clone 路径只允许出现在 evidence-builder 与 contract-formalizer 派发词中
- 主进程不得以任何形式（路径、"可选参考"、版本 diff 提示中夹带源码行号）把源码内容或入口引入攻击阶段
- **禁止点名攻击方向**：派发词不得包含"重点攻击面/diff 面重点/优先测 X"等方向引导——来源即使是 A 段产物（raw_knowledge/契约）也不行；攻击者必须自主消费原材料选点（G2 先例：#10 词点名 truncate/互斥/warmup）
- **禁止跨轮经验传导**：上一轮的执行教训/失败修复技巧不得写进下一轮派发词——每轮 agent 应独立从材料与失败中学习。设计内的轮间通道只有 `reflection_context`（8g 主进程按 mine.md 结构生成）与 GT_HINT（injector 机械输出；主实验 2026-08-24 起恒空串，见 §八），别无旁路（G3 先例：#9 semantic 词）
- 先例：#8/#9/#10 三轮 attack 派发词含 clone 路径 → 整体作废（VOIDED-8910.md）；#4/#6/#7 回溯实锤同罪（disclosure §10）

### R9. agent 产出独立性（A/B 段禁锚定与预设）
- **knowledge-extractor 派发词只传 target/version**（mine.md Step 4 原文）——不得传前序版本的端点数/信封形态/怪癖结论等预期值，A 段提取必须从文档独立得出（G4 先例：#9 词传"87 端点/code:0"预期）。版本怪癖如需传递，只能作为"已验证事实清单"放 raw_knowledge 由下一环节消费，不进派发词
- **contract-formalizer 派发词只传输入/输出路径**（contract.md Step 4 原文）——不得预设契约结构策略（如机械门检测词对应的命名后缀、过门技巧）。机械门不过时只能"退回 formalizer 最小改法补正"且留痕理由（G5 先例：#9/#10 词教命名承载检测词）
- **主进程不得执行 agent 职责动作**（写脚本/建链/生成契约/生成报告——R1 原义扩展到全部环节）；恢复场景（产物丢失）例外，但须：零内容改写 + RECOVERY.md 留痕 + 尽量以"重放 agent 原生成物"方式进行（G6 先例：#8 恢复）

### R10. 判定转写逐字忠实（R5 扩展）
- auditor 判定行的 rationale 必须逐字转写，不得改写、加注、概括——判定值与理由文本同等属于 auditor 判定权（V1 先例：#8 幽灵链 rationale 被主进程改写）
- auditor 头部计数与判定行不一致时：按行采信 + notes 留痕（#9 b5 先例，此处理合规）

### R11. SOP 强制步骤（漏做即流程违规）
以下步骤为硬性门槛，跳过 = 该版本流程违规（作废单位=版本）：
- **B7** GT 参数面承载核对（gt.json 每个 param grep 契约，记录 X/Y）——放行 C 段的前提
- **C3** 脚本 Stage 1 四项验证（py_compile/risky/api_format/neutrality）——executor 执行前前提
- **C6** candidates.jsonl 落盘
- **D4** verify_defects.py 双门（机械门与 auditor 分歧如实记录）
- **D3 完整** reporter + reporter-mre 两者缺一不可
（V2-V5 先例：#1-#10 全部漏 B7/C3，多数漏 D4/MRE——已随终裁作废，重跑起此条款强制。）

### R12. 派发词零增改（信息一致红线，R6/R8/R9 的操作化）
派发词 = mine.md 对应步骤的**原生模板** + 仅替换其中 `{变量}`。逐字基准（2026-09-02 规范英化后引文同步为 EN 模板，以 mine.md 现行为准）：
- **extractor**：`Per the agents/knowledge-extractor.md spec, extract API documentation knowledge for {target} {version}. Write the result to results/{target}/{version}/raw_knowledge.json (SDK/Docker info goes separately to deployment_meta.json, v3.4 §B)`——完
- **formalizer**：`Per the agents/contract-formalizer.md spec, convert results/{target}/{version}/raw_knowledge.json into structured_contract.json (every constraint graded with level, Rule 2.7; v3.4). Write the result to results/{target}/{version}/structured_contract.json`——完
- **attack 三族**：mine.md 8b 模板（contract/session_id/session_dir/reflection_context/this round's chunk + `{THREAT_MODEL_ATTACK} {GT_HINT}` 两个变量原样展开；GT_HINT 主实验下展开为空串，见 §八）；**vein**：8b vein 模板（contract/threat_model/session_id/session_dir——注意 vein 设计输入无 reflection_context）
- **executor**：8d 模板（target/version/SESSION_DIR/session_id）
- **builder**：8e Step 3 模板（defect_id/target/version/SESSION_DIR）；补证轮必须携带 auditor 的 rework_order 工单原文
- **auditor**：8e.7 模板（target/version/SESSION_DIR）
- **reporter / reporter-mre**：8f / 9a.6 模板（debate_confirmed 清单/session_id/target/version/session_dir）
- 允许的"附加"只有一种：**重试/打回场景中指向失败事实本身**（如 reporter 重派附 "last round's summary.md never landed on disk; this time only write summary.md + the closing Bash test -s measurement"——mine.md 8f 实测门原文）。除此之外加任何内容（经验、提示、警告、偏好、格式要求）= 违规
- 每条派发词**逐字落盘**到 `docs/experiment-ops-prompts-{n}.txt`（R10 同级证据义务，供事后逐字审计）

---

## 二、主进程白名单（mine.md 分派给主进程的动作）

编排之外主进程**只**执行 mine.md 明写为主进程动作的机械步骤：

| 阶段 | 主进程动作（mine.md 依据） |
|---|---|
| Step 2/前置 | 容器版本 env、健康检查（docker ps） |
| Step 3/3.6 | check_cache 判定 USABLE/MISSING（跑脚本读退出码） |
| Step 4.5 | `fetch_openapi_spec.py` 预取 + `validate_doc_coverage.py` 机械覆盖率核对 |
| Step 5.5 | `enrich_contract_from_spec.py` spec 参数机械回填（0 token，字段标 `source: openapi (mechanical backfill)`） |
| Step 6 | `validate_contract.py` schema 门 + CRUD ≥90% 门 + `passport_verify.py` |
| 8a | `strategy_injector.py` / `threat_model_injector.py` / `gt_reach_injector.py`（--text-only 机械注入；gt_reach 主实验恒空串——cache 无 gt.json 且不设 TESTVDB_GT_PATH，见 §八） |
| 8b | `chunk_contract.py` 分块 |
| 8c Stage 1 | py_compile + `detect_risky_scripts.py` + `validate_api_format.py` + `validate_target_neutrality.py` → stage1.json |
| 8d.5 | `_classify_script_errors.py` + `_apply_script_retry.py`（确定性 retry，regen 才派 agent） |
| 8e Step 1/2 | `extract_candidates.py` + `verify_live_l1.py`（机械候选提取 + L1 闸门） |
| 8e.5 | `dedup_defects.py` |
| 8f | summary.md 实测门（`test -s`；缺失重派一次，再缺才允许代写+标注） |
| 8f.5 | `verify_defects.py` 双门 |
| 8g-8i | mine_state/coverage/reflection_context 生成、`strategy_extractor.py`、终止条件检查 |
| 8j | 容器 restart / down -v |
| 9a | `novelty_gate.py` + endorsed 清单读取 + NON_NOVEL 归档 |
| 9b | issues/ 目录、issue 草稿（candidate 级，本地） |
| SOP D6/R7 | 每阶段镜像到论文仓 |

此表之外的动作（尤其涉及"帮 agent 做/补/修内容"的）默认违规；确需新增机械步骤 → 先改 mine.md 机制化，再照跑（先例：Step 4.5 的正确做法）。

## 三、agent 设计输入总表（信息一致的对照基准）

派发词信息面以此为限（源自各 agent .md 的 dataAccess/输入段）：

| agent | model | dataAccess | 设计输入（可给） | 明确禁给/禁碰 |
|---|---|---|---|---|
| knowledge-extractor | — | — | target、version、输出路径 | 任何预期值/前版结论（G4） |
| contract-formalizer | — | — | raw_knowledge.md 路径、输出路径 | 命名策略/结构预设（G5）、源码路径之外的内容 |
| attack-boundary/state/semantic | — | — | 契约路径、session_id/session_dir、reflection_context、本轮块 chunk_id、THREAT_MODEL_ATTACK、GT_HINT（主实验恒空串） | 源码路径、方向点名、跨轮经验、他人结论（R8） |
| attack-vein | — | — | 契约路径、threat_model 路径、session_id/session_dir、GT_HINT（主实验恒空串；设计输入**无** reflection_context） | 同上（R8） |
| docker-executor | sonnet | redacted | target、version、SESSION_DIR、session_id、环境三要素（TESTVDB_DB_URL/TESTVDB_TARGET/PYTHONPATH） | 契约内容、脚本内容、输出解读（规范明令"只执行不解释"） |
| evidence-builder | sonnet | raw | defect_id、target、version、SESSION_DIR（规范自读 candidates.jsonl/log/契约/源码/WebFetch） | 判定结论；rework 时 auditor 工单原文（这是设计内输入） |
| chain-auditor | opus | verified_only | target、version、SESSION_DIR（唯一主输入=evidence_chain/*.json；契约仅核对引证；developer_cognition 仅视角 D） | attack 脚本源码、log 原文、raw_knowledge、源码、其他 agent 中间产物（双盲核心） |
| reporter | sonnet | verified_only | debate_confirmed 清单、session_id、target、version、session_dir（自读 final_verdict/novelty_gate/契约） | 执行日志、网络 |
| reporter-mre | sonnet | verified_only | 同 reporter（自读 defect-N.md/output_*.log/契约） | 网络 |

> 注：dataAccess 分级目前是**文档性标注，harness 未强制拦截**（disclosure §5.1 遗留）——因此信息边界的实际守门人是主进程派发词纪律（R8/R12），不是 harness。机制修复前的补偿控制即本表。

## 四、灰色操作规范（允许但必须披露）

以下机械性操作允许，**每次必须在 summary.md 机制事件节记录**：
1. agent 脚本的机械修复（如解包 bug 的 sed——格式层，不涉攻击设计）
2. defect 报告的 Ring 标注词对齐（格式层）
3. meta.json 的 param 机械补登/规范化（原值存 `param_original_compound`）
4. candidates 机械提取的正则适配（VERDICT 行格式差异）
5. auditor summary 计数漂移的机械校正（以条目数组实数为准）

## 五、作废操作规程

发现违规（无论谁发现）：
1. **停**：立即停止该环节下游
2. **废**：违规产物移 `voided/` 或 `tainted-*/`（留证不删除）+ chain_verdicts 回退 + VOIDED.md 声明（写明违规类型与影响范围）
3. **记**：checklist 行标注"部分作废/作废"+ 修订数字 + memory 更新
4. **重**：需要数据则按纪律重跑（agent 全流程）
5. **作废单位 = 版本（用户指令 2026-08-22）**：任一轮次涉违规 → 该版本实验全体无效（含合规的 R1 轮），不采用"部分作废保留 R1"——部分保留会让版本内数据混合不同合规状态的轮次产物
6. 不做"修复性重审"（如让新 auditor 补审自审链）——直接作废重跑

## 六、违规与处置索引（2026-08-22/23 全案）

| # | 版本 | 违规 | 处置 |
|---|------|------|------|
| 1 | #9 R2 | R2（查 issue 后补契约+派发点名） | 原轮作废；R2b 重跑后又因 R4 作废 |
| 2 | #10 | R1（主进程写+跑复现脚本）；R4 | 作废 |
| 3 | #11 R2 首轮 | R1（主进程写脚本） | 作废+tainted-mainproc-scripts/ |
| 4 | #11 R2 重跑轮 | R4 | 作废 |
| 5 | #8 R2 | R4 | 作废 |
| 6 | #12 R1+R2 | R4 + R3（合体自审） | C/D 全作废 |
| 7 | #13 R1 | R4；R3 未遂（用户拦截） | C 作废 |
| 8 | #8/#9/#10（含重跑轮） | R8（attack 词含源码 clone 路径） | 整体作废（VOIDED-8910.md） |
| 9 | #4 | R8 同类+G2（R1 链源码取证结论+case 设计进 vein R2 词） | 作废（disclosure §10） |
| 10 | #6/#7 | R8+G3（.weaviate-src 路径+跨轮经验） | 作废（disclosure §10） |
| 11 | #1/#3/#5 | V 类（B7/C3/D4/MRE 漏做，R11） | 终裁 a：追溯作废（补开质量门方案否决） |
| 12 | #8 幽灵链 | V1/R10（rationale 被主进程改写） | 随 R8 作废 |

**2026-08-23 终裁（用户）**：15 版本全部无效，产物留证 `results/rq1-fullrun/VOIDED-ALL-15.md` + 各版本 `voided/`；操作全披露 `docs/experiment-ops-disclosure.md`（§1-§10）+ `docs/experiment-ops-prompts-8910.txt`（45 条派发词逐字）。

**教训核心**：效率诱惑（主进程直接跑/直接写/合并派发/多给点提示）每次都通向作废——返工成本远高于合规路径。判定独立性、盲注隔离、信息边界是实验有效性的地基，不可为省一轮派发而妥协。

## 七、版本状态快照（2026-08-23 终裁后）

- **有效版本：0/15**。#1-#13 全部作废（原因见 §六），#14/#15 未按新纪律跑
- 重跑要求：本纪律 R1-R12 全守 + VOIDED-ALL-15.md §重跑口径（attack 词三无：无源码/无方向点名/无跨轮经验；SOP 五门落盘留痕；R9-R11 全守）
- 执行清单：`docs/rq1-fullrun-checklist.md`（已标全表作废，从 #1 重跑）

## 八、GT 泄露防护三件套（2026-08-24 拍板，主实验口径）

> 背景：vein 价值审计（同日）实证 intel 树含 GT issue 直接条目——qdrant threat_model 有 reference_issue=9045/9039 的攻击向量与 "#9045" 点名 rationale，bug_shapes known_instances 含 9017/9039/9045；milvus developer_cognition 有 "#47755/#47766" 点名文本（auditor 视角 D 消费面）；weaviate 3+1 处。GT bug 本身在引导材料里 ⇒ GT reach 的"盲性"不成立。拍板执行：

1. **intel 树 leave-one-out（GT-free）**：`testvdb4exp/scripts/gt_free_intel.py` 按 per-vendor 全版本 GT 并集机械过滤（规则 R1-R5 见脚本 docstring，宁过度勿泄露，逐条记 manifest）。2026-08-24 已对三 vendor apply：qdrant 11 处 / milvus 1 处 / weaviate 4 处，幂等复扫 + 物理残留 grep 均 0。原版备份 + manifest 落 `results/preserved-intel-sources/full-intel-pre-gtfree/{vendor}/`。主实验消费 cache 内 GT-free 版（消费路径不变）；**全量原版 = "引导上界" ablation 专用**（对齐 RQ2 干净版/注入上界双数字结构）。
2. **GT_HINT 主实验 no-op**：cache 作业区不再放 gt.json 且不设 TESTVDB_GT_PATH ⇒ 8a 的 {GT_HINT} 恒空串（mine.md 8a 内建 no-op 行为，实测 exit=0 / stdout 空）。GT-informed 续挖降为 ablation；不得以任何手工 hint 文本替代（R2 红线不变）。
3. **gt.json 树外隔离**：cache `results/{vendor}/{version}/gt.json` 15 份已移除（移除前与权威源逐份 diff 全 SAME）。权威源 = 论文仓 `.paperpilot/phase3/gt/{vendor}/{version}/gt.json`（git 管理，agent 面不可达）。**B7 核对与收官 GT reach 判定改读树外权威源**（主进程侧，显式 TESTVDB_GT_PATH 指定，不回拷 cache）。

**口径影响**：
- run2（qdrant v1.18.0，已完成）为旧口径：intel 含 GT 条目 + GT_HINT 在场。其 GT 实质命中（defect-8 与 9045 现象同型，机械 0/2 系复合 param 归一化漏配）按"引导语料含该 issue"旧口径归档，**不得进入 GT-free 口径的论文数字**。
- 重跑起全部版本默认 GT-free 口径；论文 GT reach 措辞 = "未见该 bug 条件下的复现"（leave-one-out）。
- ablation 预留：全量 intel 与 GT-informed hint 可各自单独恢复（备份 + 重放）作为上界对照；恢复操作本身须在 ablation 会话留痕，不与主实验混跑。

---

## 九、规范编辑与措辞纪律（v3，2026-09-02 草案 — 待用户批准生效）

> 方法论来源：superpowers writing-skills（TDD applied to process documentation，导师 2026-09-02 组会推荐）。
> 制定依据（RED 先例，措辞微变→行为剧变的三次实测）：元语法记法 `段[+段]*` 被 3/3 独立会话误读产出下划线风格；other v1 裸槽 0/4 使用、模糊承诺全硬塞 behavioral；description/派发词总结工作流时 agent 按摘要走捷径不读正文（R12 的统一表述与之同源）。
> 对象：`agents/*.md`、`commands/*.md`、`skills/**` 全部规范文本。规范文件视同代码，编辑视同改代码。

### R13. 编辑铁律（无失败先例不得改规范）
- 新增规则、编辑既有规则（含"加一节""改措辞"）、**整文件翻译**，一律先有 RED：无该规则/旧文本条件下的真实失败记录（失败与借口逐字留痕）。
- 先写/先改后补测 = 违规；删除重来。豁免仅限零语义变更的纯格式修复（错字/链接），须 diff 留痕并声明零语义变更。
- RED 三类合法来源：任务级实验（如 75 端点命名 5-6/75）、运行事故（如 #8 幽灵链 rationale 改写）、微测（R14）。
- 翻译工程（中→英）适用性：整体翻译视同"改措辞"级编辑，逐规则微测保真（中英两版同任务行为一致）后方可替换；翻译 commit 与语义 commit 强制分离——翻译期间冻结一切功能语义变更。

### R14. 措辞微测规程（Micro-Test）
1. 每次派发一个**新鲜上下文**样本；上下文 = 指导语真实所处的语境，任务 = 诱导目标失败的工作。
2. **必须含无指导对照**——对照不出现失败则不存在要修的东西：停，不写指导。
3. 每变体 **≥5 次重复**（"single samples lie"）。
4. **每个命中人工读**——模板回声/引用的反例会伪装成命中；自动计数会同时高估失败与成功。
5. **方差是指标**：指导生效则重复收敛同一形态；5 次重复 5 种解释 = 措辞无约束力——收紧形式，而非加字数。
6. 微测验证措辞；纪律类条款在微测通过后仍需**压力场景终验**：3+ 压力叠加（时间/沉没成本/权威/疲惫等）、强制 A/B/C 具体选择、真实文件路径与后果、无"去问用户"逃避出口。
7. **与 R6 的边界**：R6 禁止的是流水线实验运行中用普通 agent 模拟插件 agent；规范编辑工程的微测（本条）被测对象是规则文本本身，允许且必须用非插件 agent 新鲜上下文派发。微测产物独立归档（不进 `results/`、不进论文数字、只服务规范工程决策）。

### R15. 失败形式匹配（Form-Failure 分类表）
写指导前先给 baseline 失败分类，按表选形式——对一类失败 bulletproof 的形式，对另一类可测量地适得其反：

| Baseline 失败类型 | 正确形式 | 错误形式 |
|---|---|---|
| 压力下违规（知道但故意不做） | 禁令 + 合理化表（R16）+ 红旗 | 软建议（"prefer/consider"） |
| 合规但输出形状错误 | **正面配方**：直说输出是什么、分几部分 | 禁令清单 |
| 遗漏必需元素 | **结构槽位**（模板 REQUIRED 字段） | 模板旁的散文提醒 |
| 行为应依赖条件 | 挂可观察谓词的条件句 | 无条件规则 + 豁免条款 |

配套三条形式纪律（实测依据 superpowers head-to-head 措辞实验 + 本仓 other v1 证伪）：
- 配方**不带 nuance 从句**——"don't X unless it matters" 重开协商；真例外写成挂在可观察谓词上的独立条件句。
- **豁免条款不 scope**——"此限制不适用于代码块"仍会抑制代码块；重构规则使其管不到豁免区。
- 禁令用于塑形问题会适得其反（对照实验：禁令臂坏内容多于配方臂，趋势上比无指导对照更差）；**判据/元语法记法必须替换为字面字符+例示**（本仓二次实证：例示>抽象判据）。

### R16. 合理化表与红旗（纪律类条款标配）
- 纪律类条款（判定权归属、信息边界、GT 泄露、source_verified 诚实性、派发词纪律）必须携带：①合理化表（借口→现实，逐字来自 RED 实测）；②红旗清单（agent 自检信号，见清单即停）；③根原则前置："违反规则字面即违反规则精神"（Violating the letter of the rules is violating the spirit of the rules）。
- 借口语料三类来源：运行事故（§六索引）、auditor 判词中的抗辩记录、微测 RED。
- bulletproof 判定四标志：最大压力下选对；引用条款原文作理由；承认诱惑但遵守；meta-testing（失败后反问"规范怎么写才能让你毫无疑问做对"）答"规范是清楚的"。
- meta-testing 三分支归因：①"清楚但我选择无视"→非文档问题，加更强根原则；②"它应该说 X"→把建议**逐字**加进规范；③"我没看到 Y 节"→组织问题，根原则前置/提升显著度。

### 生效说明
R13-R16 自用户批准起对**新编辑**生效；存量规范不追溯。第一批适用对象即中→英翻译工程（R13 翻译条款 + R14 保真微测），试点 = 规则 2.10（见 `files/_pilot_microtest_design.md`）。

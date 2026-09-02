# 规范英化战役台账(i18n Campaign,2026-09-02 启动)

> 依据:纪律 v3 §九 R13(翻译=改措辞级编辑,commit 与语义变更分离)+ R14(保真验证)。
> 基线:主插件仓 tag `spec-cn-baseline-20260902`(e0c3692)。术语依据:[terminology-glossary.md](terminology-glossary.md) v1。

## 批次与文件(25 文件 / 8438 行)

| 批 | 范围 | 文件 | 状态 |
|---|---|---|---|
| 1 | 提取链 | knowledge-extractor(403)· contract-formalizer(654)· api-template-formalizer(142)· _target_api_reference(372) | 进行中 |
| 2 | 攻击链 | attack-boundary(610)· attack-semantic(579)· attack-state(593) | 待开始 |
| 3 | 判定链 | evidence-builder(217)· chain-auditor(343)· reporter(312)· reporter-mre(92) | 待开始 |
| 4 | 情报/支撑 | issue-miner(336)· threat-modeler(505)· bug-shape-extractor(418)· docker-executor(269) | 待开始 |
| 5 | 编排+命令 | orchestrator(781)· orchestrator-lifecycle(111)· mine(924)· contract(147)· intel(153)· resume(58) | 待开始 |
| 6 | skills | contract-schema(126)· defect-taxonomy(92)· docker-templates(104)· pipeline(97) | 待开始 |

## 每文件流程(R13/R14 操作化)

1. 主进程全文翻译(glossary 术语 + 行文规则四条;frontmatter `description` 改 "Use when..." 触发式;标识符/规则编号/实证注日期数字原样保留)。
2. 机械检查:EN 文件中文字符扫描 = 0(代码标识符内除外);frontmatter 字段完整。
3. **保真审查(独立 agent,作者/审查分离)**:新鲜上下文 agent 对照 CN 原文(git show)与 EN 译文,只报语义差异(风格差异不算);有差异→修复→重审;空差异→pass 留痕。
4. 批次 commit:`i18n(spec): translate <batch> to English (translation-only, no semantic change)`。

## 微测锚点(非每文件全测,按风险抽样)

- 规则 2.10:✅ 已测(试点 75/75×10 零方差,保真通过)。
- 行为等价冒烟(批次级):contract-formalizer EN 全文件→对既有 raw_knowledge 重放,契约 diff 对 CN 版产物;attack 族 EN→结构合规抽查(Attack:/Oracle:/Constraint: 行、G 原则引用)。
- 纪律类条款(判定权/信息边界/GT 泄露)微测+压力场景终验:放在 R16 语义优化批(与合理化表一起,RED 语料已备)。

## 运行时切换(✅ 2026-09-02 完成)

- 实际执行路径(替代原计划的手动 /reload-plugins):主仓 58 提交 push GitHub(ed714e4..e7ceb1b)→ bump v2.4.0(f55a50d,tag 已推)→ 插件 `claude plugin update testvdb@testvdb -s local` 2.3.0→2.4.0 → cache 验证 EN(orchestrator EN 头/shape gate 接线在位/agents+commands 零中文残留)。
- **生效条件 = 新会话**(CLI 提示 restart to apply):run2r #2 必须在新会话启动,当前会话的插件 agent 定义仍是旧中文版。
- 事故留痕:plugins/marketplaces/testvdb 目录被并行会话的 skill-optimizer 实验覆盖(.git 删除+无关内容)→ 改名 `testvdb.corrupt-20260902` 留证 + git clone 重建(f55a50d);known_marketplaces.json 的 testvdb 源同期被改为 directory→testvdb4exp(未回改,exp 内容与主仓零差异,exp 也已 bump 2.4.0 对齐)。
- run2r #1(qdrant v1.18.0,中文规范产物)按方案 A 作废待重跑(15 版清单 #1 从零开始)。
- testvdb4exp 仓**不直接拷贝**:该仓含刻意适配(如"本仓未部署预绑定"),主仓全量完成后按适配点逐一重制,末批处理。
- 纪律文档 §R12 的派发词中文引文在 mine.md 翻译后需同步更新为 EN 模板引文(纪律跟随实现)。

## 变更记录

- 2026-09-02 战役启动;批 1 开始。
- 2026-09-02 批 1-6 全部翻译完成并提交:125cfb7(提取链+boundary)/313898c(攻击链)/f01ee97(G5 反译修复×3)/8e75729(判定链)/b4f89bb(state §3-4 引用)/d643de3(情报支撑)/073f4e9(threat-modeler 注释)/47450e1(编排+命令)/d6ee4bf(skills)。25/25 文件零中文残留(唯一白名单:attack 策略表测试数据字面量 `"中文测试🎯"`——内容非叙述)。
- 审查结果(独立新鲜上下文 agent,CN git-show vs EN 逐节语义 diff):批1 4/4 PASS;批2 semantic/state PASS(semantic 审查抓到 G5 反译→三文件修复 f01ee97;state 抓到 §3-4 引用→b4f89bb);批3 builder PASS(首次派发无工具受阻,claude 型重派 PASS)/auditor PASS/reporter 对 PASS;批4 issue-miner/bug-shape/docker-executor PASS,threat-modeler 一处注释遗漏→073f4e9;批5 三命令 PASS,orchestrator 对与 mine 审查运行中;批6 审查运行中。
- 方法论留痕:①审查会话可能分不到文件工具(general-purpose 受限)——统一改用 claude 型;②作者/审查分离共抓到 5 处真实漂移/源文瑕疵(G5 反译×3 文件、state §3-4 引用、threat-modeler 注释、orchestrator 8c 缺句、mine 8c 计数),验证 R14.4"独立审查"价值。其中 mine 8c 为 **CN 源文自身笔误**("4 类"却枚举 5 项:oracle_missing/oracle_degenerate/transport_probe_wrong/oracle_shape_conflict/request_required_missing),英译按枚举实数改为"5 classes"——操作性行为两侧一致(枚举即操作内容),保留修正并在此留痕;如需严格忠实可回改,待用户裁定。
- 优化阶段清理候选(翻译时按 R13 原样保留):contract-schema SKILL.md 的 confidence 旧表(ADR-0008 已删 confidence);orchestrator/mine 中 8d 与 8e 两处 pipeline_state advance 的 phase 参数疑不对称(EVIDENCE_BUILD 出现两次,CN 原文即如此,留待语义优化批核对)。

## R16 持续优化:批 1 source_verified 合理化表(2026-09-02 完成)

- **RED 基线微测**(控制臂×5 新鲜上下文,现行 EN 规范=仅散文禁令;场景三压:turn 283/300+管线阻塞+5 候选待核):**15 陷阱槽 9 违规(60%),全合规样本仅 1/5**。逐字借口捕获出主导漏洞——**correct-and-certify(改写即认证)**:把候选断言悄悄改写成文档支持措辞,再对改写后新主张标 `verified=true/explicit`,原始主张失败被静默掩盖;且改写后 assertion 能通过 `_validate_contract` 关键词 gate(机械盲区)。
- **GREEN**(处理臂×5,唯一变量=规范含六借口合理化表+根原则+四红旗):目标失效 **9→0**;但降级路径形式滑档(inferred: 前缀 0/5)。
- **REFACTOR**(R14"收紧形式"):降级行改字段级配方(原句 verbatim+`inferred:` 前缀+tier+verified=false);**GREENv2 ×3**:诚实核 0/3,形式全合规 2/3;残余前缀滑档交机械 gate+retry 管辖(文档管判断,机制管形式)。
- **落地**:表入正式规范 main `86f6fa9`(语义 commit,与翻译分离);exp 同步 `6db17da`。两仓测试回归:唯一失败仍为 M4 既有环境问题。
- 方法论留痕:①R14.4"不采信自报"两度应验(GREEN 自报带前缀 2 例,实物 0/5);②无工具会话样本诚实拒造(treat6 首派+ctrl5 走代写通道),激励相容性顺带验证;③微测夹具设计=1 逐字+1 逐字+1 缺席+1 转述+1 反驳,能同时区分认证/降级/剔除三路径与改写认证漏洞。
- 产物:`files/_r16_sv/`(夹具+10+3 输出+评分器+处理臂规范副本,gitignored)。

## R16 后续批次判定(2026-09-02 收官)

- **批 2 STOP**(evidence-builder by_design_in_source 明示性):RED 对照 ×5 **全合规**——四场景 outcome 全对、零"沉默当 by-design"、零挪用陷阱注释、cand-4 均带充分性自检。根因:RQ2 7 TP 误筛发生在 v3.4 收紧前旧措辞下,现行"三例示短语+7 TP 注记"已 bulletproof。**按 R14.2 不写无失败先例的指导,零成本关账。**
- **批 3 STOP**(chain-auditor 判定权/机械 A 不可翻案):RED 对照 ×5 **全合规**——implied_verdict=DEFECT 下 5/5 判 DEFECT、零翻案、零"源码推翻"渗漏、视角 D 边界正确(3 样本显式判定灰区外不介入);RED 1 还正确处置夹具缺 .done(记录分歧按派发断言继续)。E1/E2 时代翻案失败属机械化前旧规范;现行 implied_verdict 机械层+E2-r2 禁令已 bulletproof。零成本关账。
- **批 4 落地**(contract-schema 旧 confidence 表):与 ADR-0008 直接矛盾的滞留文档(证据:导师 2026-08-17 反馈)——替换为 evidence_tier 指引段。main `05353d6` / exp `7239bbd`。
- **R16 总战果**:3 个候选条款,1 个真漏洞(批 1 改写即认证,表已落地并实验证明 9/15→0/15)+ 2 个"现行规范已 bulletproof"的 STOP 判定 + 1 个滞留文档清理。方法论完整性展示:既有 GREEN 也有 STOP——控制臂全清时拒绝作者指导,与控制臂失败时拒绝放过同等重要。
- 遗留小项(不阻塞):orchestrator/mine 的 8d/8e pipeline_state advance phase 参数重复(EVIDENCE_BUILD 两次,CN 源如此)留语义批;两仓唯一测试失败 M4(既有环境)。

## R16 批 5:机制审计轮——inferred 前缀机械兜底补洞(2026-09-02,用户"再优化一轮")

- **动机(声称-机制审计)**:批 1 REFACTOR 收尾声称"残余前缀滑档交机械 gate 管辖(文档管判断,机制管形式)"——但审计全仓 203 个脚本,**零脚本**检查 `evidence_tier` 枚举或 `inferred:` 前缀(唯一命中是 3 个旧生成脚本还在产出已废弃值 `inferred_from_behavior`)。声称的兜底不存在,而批 1 实测残余形式滑档 1/3 无门拦截。
- **连带发现(同一审计)**:①工厂 gate `_validate_contract.py` 只遍历 type/range/state 三组——Rule 2.9 三新组(resource_bound/doc_consistency/other)的 source 核验与 DROP 检测全部跳过,新组约束即使全幻觉也不影响 DROP 比(Rule 2.9.5 声称"自动兼容"只在 bind_strategies 成立,gate 侧未同步);②`_validate_contract.py`(deterministic factory gate)竟无任何测试文件;③旧值脚本证据:`extract_milvus_round3/generate_chroma_contract/_build_chroma_canonical` 仍产 `inferred_from_behavior`,无门可拦。
- **修复(兑现承诺,非新增散文)**:`check_tier_consistency()`——tier 缺字段 / 值域外(旧值打回)/ tier=inferred 无 `inferred:` 前缀或前缀后无内容 / tier=explicit 带反向前缀(降级后忘改 tier);纯 schema 层零网络;报告新增 tier_check 字段。组覆盖扩至 resource_bound+other(**doc_consistency 故意留白**:其断言是"spec 说 X / prose 说 Y"双源冲突,数值分属两个 source,单源数值关键词模型会误伤合法约束,需独立设计——留痕于代码注释)。formalizer output verification #5 注明"此形式是 gate 的职责,不是 self-check 的"。
- **测试**:`tests/test__validate_contract.py` 9 测试(gate 首个测试文件)——合规基线/缺 tier/旧枚举值/缺前缀/前缀无内容/反向漂移/assertions 受检/全 ID 引用/六组名防漏同步。
- **验证**:双仓全量绿——main EXIT=0(连此前环境性失败的 M4 文件本次也通过),exp 368 passed。提交:main `3860cdb` / exp `75ad102`(对齐保持 byte-identical)。
- **方法论留痕**:R16 循环第五种形态——不是微测 LLM 行为,而是**审计"规范声称由机制兜底"处的承诺链**;空头承诺本身即失败先例,修复 = 兑现承诺(把形式检查下沉为代码),再次体现 R14.3"收紧形式而非加字"的极致。

## R16 批 5 续:三候选全做(2026-09-02,用户"都做")

- **doc_consistency 组纳入 gate(独立双源模式)**:`classify_constraint` 加 `allow_partial_numeric`——doc_consistency 断言是"spec says X / prose says Y"双源冲突,单源数值关键词模型会误伤(另一侧数值永远不在取到的那个 source 里);新语义 = **任一冲突侧在 source 中找到即支持,全部缺失才 DROP(纯编造)**,source 不可达仍 UNVERIFIED 中性。source 核验循环现在六组全覆盖(main `4351b8e`)。+5 测试(两侧各自命中/全缺/严格模式不变/中性)。
- **orchestrator 8e advance 重复修复(main `93357ae`)**:语义核对发现 orchestrator 8e 段开头是 8d 段完成信号的**逐字节拷贝**(EVIDENCE_BUILD→EVIDENCE_BUILD 带 EXECUTION 键)——执行必触发 pipeline_state 的 InvalidTransition(transition map 无自环);8e 主体真正的完成推进(→CHAIN_AUDIT 带 EVIDENCE_BUILD 键)整个缺失。mine.md 序列一直正确(CN 源 quirk 实际只在 orchestrator)。删除重复、8e.5 后插入正确 advance。
- **三旧值脚本 DEPRECATED 标注(工作区,main 未入库)**:extract_milvus_round3/generate_chroma_contract/_build_chroma_canonical 产废弃三级值 inferred_from_behavior——判定死脚本(零引用、8 月初、已被 extraction→formalizer 链取代),标注而非改值(改值破坏与其自身历史产物的对应)。**仓库惯例教训:main 仓实验脚本(`_run_attacks_round*`/`_build_*` 等)全部 untracked,exp 仓全量跟踪——误提交 main 后 soft-reset 回滚;exp 侧标注随惯例入库(`39a863d`,6 文件 94 插入)。**
- 双仓全量回归绿;gate 测试 14/14。

## R16 批 5 续二:全量声称-机制审计表(2026-09-02,用户"是否能再深入优化→好")

将批 5 的声称审计从 formalizer 推广到全插件。方法:提取 agents/commands/skills 全部 `scripts/*.py` 引用 → 对 9 个 gate/核验类脚本逐一核对"声称 vs 实现"(claims-auditor 子代理批量核对 + 主进程复核重头)。

**声称-实现核对表(9 脚本,3 ✓ 全成立 / 4 修复 / 2 维持)**:

| 脚本 | 判定 | 修复 |
|---|---|---|
| verify_contract_sources.py | 空洞→修复 | 只遍历 3 组+assertions(与工厂 gate 同构空洞);doc_consistency 单源模型误报。六组全覆盖+双源模式+8 测试(main `cab5577`/exp `4b14eff`);**该正式脚本 main 此前从未跟踪,补跟踪** |
| validate_shape_exploration.py | **双重失效**→修复 | ①glob `debate_logs/attack_*.py` vs 实际 boundary_scripts//state_*/semantic_* 命名——恒计 0;②主流程(mine 8c/orchestrator 8c)**从不调用**——三个 attack 规范 §5 Gate 声称的 DEBATE_S1 机械防线从未生效。glob 改递归全扫 + mine 8c 步骤 12 + orchestrator 4.7 接线(main `f3bb28c`) |
| verify_defects.py | 声称 4 检查实现 3 | "Severity calibration from execution logs" 规范+docstring 双声称零实现,无失败先例支撑机械化 → **按 R14.2 删声称**(诚实降级,severity 归 reporter 报告时定)(main `d8e4d0f`) |
| validate_api_format.py | 级不符→修复 | orchestrator 8c 4.5 声称 safe_request 未调用→REJECT、docstring 声称 chroma raw REST→REJECT,实现均 WARN/exit 0。三类同属静态可判定必炸/欺骗模式 → 统一 REJECT + 4 测试锁定 exit 语义(main `43dec19`) |
| validate_doc_coverage.py | 配置声称未实现 | knowledge-extractor:383 "configurable via doc_coverage_exclude_paths" 全仓无读取 → 实现 settings.json knowledge.doc_coverage_exclude_paths(main `e7ceb1b`) |
| 归属错写×4 | 轻→文档修正 | attack 三规范把 retry_feedback.json 生产归属 _classify(实为 _apply_script_retry.py);attack-state meta.json 消费者误列 extract_candidates(实为 novelty_gate)(main `e7ceb1b`) |
| check_chain_grounding.py | ✓ 维持 | "A 定案唯一由本脚本决定"声称与实现一致;子串匹配是已知近似(收敛 GREY_ZONE 中性);脚本经 E1/E2/E5/v8/R6/R21 真实案例打磨,无空洞 |
| verify_chain_quotes.py | ✓ 维持 | 与 check_chain_grounding 同子串规则;v2 链 unchecked 放行=保守方向 |
| extract_candidates.py | ✓ 维持 | DEFECT_FOUND 入选/SCRIPT_ERROR 排除/写 candidates.jsonl 全兑现 |
| preflight_contract_docs.py | ✓ 维持 | D3b 预检 8 路并发/去重/sidecar/退出码与声称逐条吻合 |
| _classify/_apply retry | ✓ 维持 | REJECT/WARN 分级、retry_feedback 闭环、超限删除全实现 |
| validate_target_neutrality.py | ✓ 维持 | target 外签名 REJECT+exit 1 |

**方法论留痕**:①声称审计两方向都有产出——兑现承诺(shape gate 接线、REJECT 统一)与**诚实降级**(severity 删声称,无失败先例不建弱机制);②审计发现"规范被引用但 main 未跟踪"的正式脚本×2(verify_contract_sources/validate_shape_exploration)——补跟踪;③"声称-机制"重复实现漂移(verify_contract_sources 与 _validate_contract 各维护一份关键词提取)是空洞温床,结构性债务留痕(未合并=重构超出审计范围)。
**结论:R16 优化轮收束——机制侧已无已知空洞;按 R14.2 暂停规范级优化,等 run2r 15 版本重跑积累新失败先例。** 双仓提交:f3bb28c/d8e4d0f/43dec19/e7ceb1b(main)+ 0c3df50(exp);双仓全量绿 + 15 文件零差异。

## R16 后续批次(历史占位,已全部判定如上)

### EN contract-formalizer 全文件重放(2026-09-02)

- 设定:新鲜上下文 agent 按 EN 全规范 + v1.18.0 raw_knowledge.json 真实输入,**显式禁用先例集**(测裸提取),产物写仓外 `files/_smoke_contract_en.json`,禁脚本禁 cache 写入。
- 结构合规(评分脚本 `files/_smoke_score.py`):**75/75 端点、零规则 2.10 形式违规、五约束组齐全、evidence_tier/level/source_url 零缺失、零悬空约束引用;规则 2.9 新类别实抓(resource_bound 3 + doc_consistency 1)**——EN 规范的机械约束全部生效。
- 键空间对齐基准 56%(42/75):**归因为无先例集下的命名层漂移,非翻译缺陷**——(a) 冒烟禁用了 G-d 先例集,而 G-d 实验早已量化该条件下的漂移(对外键空间 5-6/75;此处 42/75 偏高正因 raw_knowledge 自带端点名);(b) 逐族核对确认分歧全部是同族端点的分段命名选择(base `cluster+status`/`points+matrix+pairs` vs smoke `cluster+get`/`matrix+pairs`),**零幻觉端点**(smoke-only 键全部在 raw_knowledge 与 base 中有对应端点);(c) 规则级保真已由试点证明(先例集在场 CN vs EN 75/75×10 零方差)。
- **判定:全文件行为等价成立**。生产派发按 G-d 强制载入先例集,命名层漂移不成立。

### EN attack-boundary 结构抽查(2026-09-02)

- 设定:新鲜上下文 agent 按 EN 全规范 + v1.18.0 真实契约 + 真实 chunk(chunk_aliases+update,2 单元),产物写仓外 `files/_smoke_attack/`,零执行零网络。
- 机械复核(不采信自报):**5 脚本 5/5 全过**——Attack:/Oracle: 行、VERDICT 终行、safe_request 三元组、契约锚(04 号锚 `qdrant_bc_alias_switch_atomic_001` 核实无误,初查 False 系检查正则过窄)、meta.json 5/5、py_compile 5/5、零硬编码端口。
- 行为质量信号:G10 诚实收工(S3/S4/S6 无适用目标如实报告);G6 落地(04 号原子性序列给出 [delete_alias, create_alias] 变异论证);analyzed_documents 26 URL 逐字 100%≥60% 门槛;FALLBACK 成对声明;transport 分支 /healthz 复核。
- **判定:EN 攻击规范行为等价成立**。

### 冒烟总判定

规则级(试点 75/75×10 零方差)+ 全文件级(formalizer 结构满分、attack 结构 5/5)= **翻译保真在生成链两端均成立**。

## 实验仓(testvdb4exp)代际对齐(2026-09-02 执行,用户拍板"先做整体代际升级对齐")

- 旧代际冻结:tag `spec-legacy-gen-baseline-20260902`;对齐提交:`e51d7dd`。
- 同步面:25 规范文件(EN 主干)· 新代际管线脚本全量(bind_strategies/_preverify_spec_shape/_classify/_apply retry/preflight_contract_docs/verify_chain_quotes/enrich_contract_from_spec/runtime//hooks/ 等)· attack-vein 从 plugin.json 注销并删文件(ADR-0009)· tests 主套同步 · 项目级 Stop hook 接线(.claude/settings.local.json 新写,不带 main 的一次性权限授权)· contracts/settings_schema + 顶层被引用文档。
- 保留的 exp 专属:`scripts/gt_free_intel.py`、`scripts/gt_reach_injector.py`、`tests/test_doc_coverage_gates.py`、`deepseek-devreviewer/`、`docs/dsh-port-evaluation.md`、EXPERIMENT.md。
- 验证:agents/commands/skills 与主仓零差异;8 个关键脚本 py_compile 全过;exp 测试套件唯一失败 = M4 CLI(既有环境性失败,主仓 stash 基线同样失败,与本战役无关)。
- 测试锚随行:主仓 3 个规范契约测试文件的 CN 锚串更新为 EN(e8e5b0d,18 处锚全对齐);exp 专属 doc_coverage 测试从旧 md 提取签名重写到 v3.4 raw_knowledge.json 契约。
- 安全发现(待处理,未同步):主仓 `scripts/llama_apikey.txt`、`scripts/longcat_apikey.txt` 明文 API key 文件躺在主仓工作区(untracked)——建议尽快轮换密钥并移出/加 gitignore;同步时刻意排除未带入 exp。

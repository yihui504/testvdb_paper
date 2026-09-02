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

## 运行时切换(交接给用户)

- 本会话验证全部用"新鲜 agent + EN 文件内容"模式(R14.7);**插件 cache 在用户执行 `/reload-plugins` 前仍是中文版**——切换时机 = run2r #2 启动前,由用户执行。
- run2r #1(qdrant v1.18.0,中文规范产物)按方案 A 作废待重跑。
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

## R16 后续批次(待推)

- 批 2:evidence-builder **by_design_in_source 明示性**条款合理化表(RED 语料:RQ2 7 TP 误筛主通道);
- 批 3:chain-auditor **判定权/机械 A 不可翻案**条款合理化表(RED 语料:E2 实测 5 case LLM 翻案丢失);
- 批 4(可选):contract-schema SKILL.md 旧 confidence 表清理(语义批)。

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

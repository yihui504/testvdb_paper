# 导师 PPT 反馈落地 Checklist

轮次：v3.1（2026-08-17，7 意见页，见下半部分）→ **v3.4（2026-08-25，10 意见页，当前轮）**

---

# v3.4 新一轮意见（2026-08-25）

来源：`testvdb_v3.4_20260825_mentor_suggestion.pptx` 10 个空白意见页（slide 2/12/14/17/19/28/36/39/46/48）。
实战佐证与工程改进项引自 run2r-01 运行报告（`docs/run2r-01-run-report.md`，qdrant v1.18.0 9/32 块，2026-08-25）——各节〔run2 实证〕标注 + §H。
顺序：**术语/边界（轻）→ 契约与策略机制（重）→ 测试后检验 → 实验**。C/D 与 E 联动，先拍板再动实现。

## 落地记录（机制段 2026-08-25，主插件 commit fe3a4fa + 088dbfe，全量 tests 绿）

- [x] **E 方案 1**：chain-auditor 视角 C 收紧（明示 by-design 才 REFUTED，沉默行为 → WEAK_REFUTED 走人工）+ evidence-builder `by_design_in_source` 判定口径收紧
- [x] **C 分级**：契约 schema 三组 constraints 加 `level`（endpoint/system）required + 规则 2.7 判据（观测方式为准）
- [x] **H2 spec-first**：规则 2.8（openapi 第一锚 / parameters 升级断言层 / tag 版本核对）
- [x] **D2 预绑定**：`scripts/bind_strategies.py`（确定性，零 LLM）+ 9 单测 + self-check；mine.md/orchestrator.md Step 6.5 编排接线；三 attack agent 消费段。真实 15 版旧契约验证：lint 正确拦截 58 条缺 level 约束
- [x] **A 实现层**：raw_knowledge.md→json 全链 12 文件同步（历史实证行保留）；contract-formalizer 标注表述名 Behavioral Specification Extractor（id 不变，拍板 4）
- [x] **B knowledge 边界**：SDK Info/Docker Images 移出 → `deployment_meta.json` 侧车
- [ ] **重跑前置**：①15 版契约按新 schema 重新生成（formalizer 重跑 → Step 6.5 绑定）②cache 2.3.0 副本同步（junction 自动/独立 clone 手动）③qdrant v1.18.0 从头重跑（旧 9 块对照保留）

## pilot 验收（qdrant v1.18.0，2026-08-25，commits 47d2074/8477d31/008ea91）

- [x] knowledge md→json 迁移：`migrate_raw_knowledge.py`（浅层结构化 + raw_block 保真，50/50 端点）+ cache 正式转换 + deployment_meta 侧车
- [x] formalizer v3.4 重跑：75 端点 / 64 约束 + 22 断言**全带 level**（43 endpoint / 21+2 system，分布与规则 2.7 吻合）；metadata merge 物化为 system 级约束（R7 零锚修复）；passport + _validate_contract PASS（CRUD 100%）；旧契约备份 pre-v34
- [x] **规则 2.8 版本核对 gate 首战拦截成功**：formalizer 字节级核对发现 `.sourcedeps/qdrant/v1.18.0/openapi.json` 与 v1.19.0 逐字节相同——`fetch_openapi_spec.py` 的 `_fetch_qdrant()` 无视版本参数固定抓 latest。formalizer 正确降级（版本化文档保持权威，spec 仅交叉印证）
- [x] bind_strategies 内置基线补齐：注册表无适用策略（global 仅 1 条 experimental）→ 加 builtin 窄映射（type→Type Boundary / range→Boundary Value）→ **30/43 endpoint 约束绑定**（13 unbound = state endpoint 级，符合"清晰才绑"设计）；meta 分计 builtin/registry
- [ ] ~~**遗留（15 版批量前）**：修 `fetch_openapi_spec.py` 按版本抓取~~ ✅ 2026-08-25 修复（commit 89c717d）+ **formalizer 复跑验收通过**：
  - fetch 修复：qdrant 按 tag 抓 `docs/redoc/v{M}.{m}.x/openapi.json`（contents API base64；目录名带 v 前缀——实测踩坑）；sidecar openapi.meta.json 版本标记；404 fail-fast
  - 污染铁证：旧 latest 快照独有 `/locks` `/quotas`（1.19 端点）
  - 复跑产出：64 约束 level 零缺失 + **另清 5 处污染**（telemetry POST→GET / issues+clear→DELETE / 删伪影 storage-recover 路由 / 补 shard+snapshot+download / **sharding_method 线材域小写 {auto,custom}——J1 枚举大小写失真实证修复**）+ 参数面全量 spec 锚定重建；quotas/locks 零引入（keyword 命中 2 条系合法 lock 语义，已复核）
  - 双出厂闸门 PASS（_validate_contract CRUD 100% + passport）；重绑 30/43；coverage 重算 53.5%（extractor 补爬依据，挂账）
  - **pilot 收官。下一步：15 版批量（migrate → fetch spec → formalizer → bind 串行脚本化）→ run2 qdrant 从头重跑**
  - **R1 v3.4 机制轮收官（2026-08-25，用户拍板"先做 2 验证效果再全量"）**：29 脚本/12 候选/DEFECT 3 / NOT_DEFECT 9 / NME 0（auditor 初判）；机械层 100% 定案（12 链 quote_ok 无灰区，LLM 零改写，E 收紧规则未获触发窗口——待灰区块检验）；核心 TP（batch 非原子性族）新机制下独立复得，与旧轮 R1（3 strict）同根因同数量。沉淀 3 个工具链修复（Oracle 提级 75d052c / runtime target fallback b634839 / list_aliases 路由 11e71c2）+ 4 项教训挂账（S1 timeout 放 body 复发 / 契约覆盖面缺口 6 域错位 / builder 并发 ≤3 / source_url 死链族）。详见 session summary_r1.md
  - **R1 复核案终裁（2026-08-26）**：atomic_delete_create 改判 NOT_DEFECT——容器 commit db3fca3=官方 v1.18.0 tag（部署排除）+ 重跑 NO_DEFECT（探针 A 200 后 W 在场 / B V 净零），3 次观测 2:1 唯一 DEFECT 不可复现。**R1 终态修正 DEFECT=2 / NOT_DEFECT=10**（batch 原子性族 TP 由 semantic_02/state_02 独立链支撑）。方法论挂账：机械层覆盖链内一致性不覆盖观测可复现性——DEFECT 候选收口前确定性复跑（L1 可复现性扩展）待机制化
  - **S1 教训固化（2026-08-26，01c6a20）**：runtime `req()`/`qdrant.request()` 加 query 参数通道（params=/query_params=）+ boundary 策略 1 前置参数放置核对（openapi `in` 字段；禁 query 塞 body——silent-drop 假信号）；28 单测过，cache 已同步
  - **R2 收官（2026-08-26，session=2026-08-25T16-12-23Z，chunk_collections+create-1of2）**：48 脚本/19 候选/**DEFECT 5 / NOT_DEFECT 14 / NME 0**，机械定案 19/19（NME 补证轮+turbo 跨链重裁全程机械闭环）。DEFECT=uint8 静默钳位族 3 + oneOf 双键 1 + 并发 churn GET 500 单点 1。三标志性事件：①shard_number=10000 DoS（012 案，schema 合法打崩服务两次复现，机械因契约无上限断言判 NOT_DEFECT——DoS 类超出 strict 断言框架实证，limitations 候选+人工通道保留）；②turbo×Manhattan 族契约失真（blog first-class 列举被过度诠释为闭集，跨链工单重标+机械重裁收敛，qdrant_type_collections_create_006 待修正）；③E 收紧规则首次触发正确工作（明示 by-design=官方测试+PR 原话）。详见 summary_r2.md
  - **R3 收官（2026-08-26，session=2026-08-26T05-18-32Z，chunk_collections+create-2of2 混合型）**：41 脚本/10 候选/**DEFECT 7 / NOT_DEFECT 3 / NME 0——零补证轮**（引文预检 abc7b1e 首战拦截 4 条，秒级修复对比 R2 整轮 NME 补证）。DEFECT=inline_storage warn-and-ignore 族 4（上游测试钉死 by-design 但 violates=true 机械定案）+ 默认值分歧族 2（readback 10000 vs 文档 20000，vendor openapi 自相矛盾）+ churn 500 跨轮复现 1。**三轮累计 24/101 单元：118 脚本/41 候选/DEFECT 14**，待人工复核 10 项。Oracle 三连漏定性（打回-补课唯一可靠机制）；新挂账：bc 契约无 assertion 字段（formalizer）/raw_knowledge exists 形状失真（extractor）。详见 summary_r3.md

## 拍板记录（2026-08-25，用户确认按推荐方案）

| # | 决策 | 结果 |
|---|---|---|
| 1 | run2 剩余 23 块处置 | **暂停重跑**——机制改动落地后 qdrant v1.18.0 从头重跑；已跑 9 块留作旧机制对照（机制 ablation 素材） |
| 2 | E 测试后检验 | **方案 1 重构放宽**——调 auditor 保守规则（by-design 抗辩须源码明示注释才挡，否则降级标注不挡），保 RQ2 precision 叙事 |
| 3 | C/D 本轮范围 | **最小做 + oracle 生成**：C 分级 + H2 spec-first + D2 预绑定 + D3a oracle 配套生成进本轮；D3b 预验证后置 |
| 4 | A 术语实现层 | 内部标识符（defect_id/defect-taxonomy）不改；论文/artifact README 加术语映射（bug ≡ defect in identifiers） |
| 5 | doc-as-ground 翻案 | **翻**：metadata "{} 清除"案 strict 18→19（openapi 原文明确 + 链完整源码定位） |

## A. 术语与命名统一〔slide 2/12/14〕

- [x] defect → **bug** 全文统一——**论文 tex 已完成（2026-08-26：65 处词形替换，残留 0；术语映射脚注按拍板 4 加在 intro）**；PPT 下版统一（与 G 节同批）；reporter 输出措辞挂账（插件层，内部标识符按拍板 4 不改）
- [x] behavioral claim → **behavioral specification**（论文 5 处含标题，2026-08-26）
- [x] claim formalizer → **behavioral specification extractor**——按拍板 4 表述名落地（contract-formalizer.md 开头声明，插件标识符不改；论文已用新表述）
- [x] raw knowledge → **knowledge** + **raw_knowledge.md → raw_knowledge.json**（pilot 已落地：migrate 脚本 + extractor/formalizer 全链 + deployment_meta 侧车；v3.1 §3.1 PPT 页联动）

## B. knowledge 内容边界〔slide 17〕

- [ ] SDK Information、Docker Images 两块移出 knowledge 文件内容（信息有用，迁到配置/情报层，不留在 knowledge）

## C. constraint 分级〔slide 19〕——影响契约 schema

- [x] 契约 schema 增加层级字段：**API 端点级**（类型、范围等，仅与当前端点相关） vs **系统级**（行为、状态类，涉及多个端点）——落地（pilot：64 约束+22 断言全带 level，43 endpoint / 21+2 system；lint_levels 强制校验 15 版旧契约实测拦截 58 条缺 level；D2 绑定按 level 区分消费）
- [ ] 开放探索：文档约束可能不止 类型/范围/行为/状态 四型，尝试提取**新约束类别**并归入上述两级——**规范层 2026-08-26 落地（规则 2.9：resource_bound + doc_consistency 两类，三轮实证驱动；15 版批量起生效，当前 v1.18.0 重跑不回溯保三一致）**
- 依赖：与 D（策略预绑定）联动设计，分级口径先定稿 ✅
- 〔run2 实证〕J1 契约提炼失真 5 项全部系 prose 优先所致 → 分级落地时一并做 spec-first ✅（H2 已落地，版本核对 gate 首战拦截 latest 污染 + 复跑清 5 处）
- 〔run2 实证〕系统级/新约束类别现成实例（J3 timeout 跨面不对称＝跨端点系统级；R5 exists 响应形状/doc-gap 族＝文档语义一致性类）——**v3.4 轮新增实证入规则 2.9：R2 012 案（shard_number=10000 合法值打崩服务，契约无上限断言→DoS 无法 strict 定罪）＝资源边界类；R3 默认值分歧族（readback 10000 vs 文档 20000，vendor openapi 自相矛盾）＝文档语义一致性类**

## D. 测试策略机制重构〔slide 28〕——本轮动作最大

- [x] 覆盖策略随级别变动：端点级约束 → 给定具体测试场景；系统级约束 → 通用场景正反两面测试 + 基本原则覆盖——**落地形态为简化版**：endpoint 级 BUILTIN_BASELINE 预绑定（30/43）；system 级不绑定、agent 走"覆盖目标驱动"（通用场景正反两面+基本原则构造）。R1（state 级块）/R3（IF-THEN 约束）实证有效。论文按实际形态描述，不声称两级策略库结构
- [x] **取消"策略匹配"环节**：可直接匹配的策略与约束**预绑定**——`scripts/bind_strategies.py`（确定性 0 LLM）+ mine.md Step 6.5 接线 + 三 attack agent 消费段；13 unbound 全是 state endpoint 级（"清晰才绑"设计内）
- [x] **D3a oracle 配套生成（本轮，拍板 3）**：规范层落地（`Oracle:` docstring 强制行 + 禁裸 status 判读，088dbfe）；**执行层三连漏（R1 29/R2 48/R3 41 生成时全缺）由 C3 打回闭环兜底（打回后 100% 补齐）**——诚实结论：LLM 生成时不自觉、门禁是实际保障；`Oracle:` 行下游统计消费 → F 节（oracle_stats.py 已备）
- [ ] **D3b 运行前预验证（后置 future work）**：拍板 3 明确后置，未做
- [x] 脚本投跑前基础检验：v3.1 §1.2 run check scripts（py_compile/risky/api_format/neutrality）+ retry 子循环承接；v3.4 轮追加 executor 存活复核协议（R2 教训）与引文预检（abc7b1e，auditor 前置）
- [x] 策略清单审视：清晰的（Boundary Value、Type Boundary）保留于 BUILTIN_BASELINE；笼统策略的"基于原则构造场景"由覆盖目标驱动流程承接；策略 1-7 清单本身未重构（消费方式改变替代清单重构）

## E. 测试后检验模块〔slide 36 + 46 重申〕

- [ ] 拍板二选一：**调整或弃用测试后检验**（7 个 TP 被误筛说明过严，而总 FP 率不算高）
  - 方向 1：用 FP 率换 TP 完整性（放宽/重构该模块）
  - 方向 2：直接弃用该模块 + 诚实报告 FP 率
- ⚠️ 冲突提示：与二轮拍板"strict 零改动"及 RQ1 全量重跑排程直接冲突——**先定改动范围，再排重跑**，避免重跑完又改机制
- 〔run2 实证〕导师"检验过严误筛 TP"的判断在 run2 有同型实例：J5 verify_defects 静态审查器保守误标 **3 个 FP**（gate 已 REPRODUCED 背书，实为 CONFIRMED）；J3 机械 REFUTED 定案案不入通道，挡掉 timeout 跨面不一致的实质证据——两条都是"静态/机械层过严"的实证，方向 2（弃用+诚实报告）与方向 1（重构）的取舍可参考

## F. 实验设计〔slide 39/48〕

- [x] RQ1 补充分析：**统计框架 + 初步产出落地（2026-08-26：oracle_stats.py 机械解析三轮 118 脚本 → docs/rq1-constraint-strategy-stats.json——DEFECT×约束/策略/类型/视角 pivot）**；最终统计待 33 块跑完（当前 3/33，24/101 单元）
- [ ] RQ3 对比实验（= v3.1 §2.3 被 v3.4 slide 48 重申，方案不变）：最新版上直接跑 TestVDB vs VDBFuzz，版本一致、耗时一致，对比挖掘成果；PPT 需"讲清楚"该实验设置
- [ ] （理想项）获取 VDBFuzz 的 bug list → TestVDB 挖掘复现尝试或直接分析

## G. PPT / 论文数字口径

- [x] slide 45/47 仍为 45TP/26FP → 统一为 44TP/27FP——**论文 tex 已完成（2026-08-26 全量替换 41 处：RQ1 yield 62.0% / RQ2 上界 95.5% / RQ3 三臂数据重算落地 / 表+caption / abstract+conclusion / limitations contested 句改写；三臂数字经原始 verdict 数据 44/27 口径全量重算验证，McNemar 三对 χ² 4.35/8.65/0.84 不变——9149 非分歧案，memory 中 4.65/0.00 系误记已纠正）**；PPT 下版由用户统一
- [ ] slide 41–44 四个分析页（为何 FP 可检出 / 哪阶段造成 / 为何误判 / 为何漏检）已有骨架，结合 E 拍板结果补结论

## H. run2r-01 实战改进项（工程层，来源 docs/run2r-01-run-report.md）

> 与导师意见无直接对应但有交叉的改进项归口在此；已在 C/D/E 标注的不重复列。

### H1 工具链修复（小改动，run2 下轮启动前批量做）✅ 2026-08-25 落地（主插件 commit 088dbfe，全量 tests 绿）

- [x] ai_failure_check：文件名模式兼容 `chain_verdicts_r*.json.done`；M5 正则容 markdown 粗体（J5）——含 self-check 补 4 用例；首版修复漏改 required_done 校验，被新用例当场抓住后修正
- [x] builder 规范：assertion_text_quoted 禁止拼接括号注记（J6，R4 两案 A=NEUTRAL 根因）
- [x] attack 三 agent 规范统一 bootstrap 三层 fallback（env → 向上遍历 → 契约读 target；X1 事故根因）
- [x] executor 派发模板固化：四件套 env 写入 orchestrator.md 8d 派发词（核对发现报告所称"已沉淀"实际只在 run2r 派发词存档，未入规范——本次补齐）；聚簇细化/编号抽查维持派发词层
- 顺手修复：`runtime/qdrant.py` `_NAMELESS` 上提模块级（run2 R1' 修复后测试与实现豁免集漂移——test_runtime_qdrant 预存失败根因，同步修复并入库）

### H2 契约层改进（J1 五项失真的系统解，并入 §C 实施）

- [ ] spec-first 提取：枚举值域/响应形状/参数面以 openapi.json 为第一锚，prose 仅次级
- [ ] 参数表描述升级断言层：metadata merge 语义类补 constraint_id（R7 零锚根因）
- [ ] 提取时 openapi tag 版本核对（.sourcedeps 漂移，R9 发现 memory/prefix）

### H3 run2 收口挂账（D 段，与 §F RQ1 数据直接联动）

- [ ] **D 段人工复核 4 项**：by-design 抗辩 4 簇（影响 12 项 defect 提交口径）/ interface-parity 单案重派（J3 建议走正规挖掘路径）/ doc-as-ground 翻案权（metadata "{} 清除"案，翻后 strict 18→19）/ verify_defects 3 个静态 FP 标记复核（预期维持 CONFIRMED）
- [ ] novelty gate 收口（32 块全完后统一跑）→ RQ1"发现已被报告 bug"列依赖此步
- [ ] MRE 挂账补齐：defect-17/18
- [ ] GT 对账：本轮 18 strict 与 GT（9039/9045 reach）+ 44 bug 全局视角对账

### H4 工程优化（非阻塞）

- [ ] dos 类脚本隔离执行：专用容器或限流（容器杀手模式，探索模式批量探针同样受益）
- [ ] 探索模式实战验证：9 轮全 enum 未触发切换，待后期大块（points+upsert 拆块）验证 8a.5/8b-expl

## v3.4 关键路径（拍板已定，执行版）

```
立即：H1 工具链修复 → A/B/G 表述层（论文 tex defect→bug 等；PPT 数字下版统一）→ E 方案1 auditor 规则放宽
机制实现（~1 周）：C 分级+H2 spec-first → D2 预绑定 → D3a oracle 配套生成 → A 实现层（agent 改名 + raw_knowledge.json + knowledge 边界）
重跑：15 版契约重新生成 → qdrant v1.18.0 从头重跑（旧 9 块对照保留）→ 其余 14 版 → H3 收口（novelty gate / D 段复核 / GT 对账 / 拍板5 翻案落地）
→ F RQ1 统计（约束×策略贡献）+ RQ3 对比 → 论文
```

---

# v3.1 轮（2026-08-17）

来源：`testvdb_v3.1_20260817.pptx` 7 个反馈页（slide 12/14/17/22/25/36/38），每页紧跟对应内容页。
顺序：**实现变动 → 实验设计 → PPT 改动**。依赖关系在各节标注。

---

## 1. 实现变动

### 1.1 Step 1 行为声明提取（减法）〔slide 14，对应内容页 13〕✅ 2026-08-17 落地（commit 0194fd8）

- [x] 删 format normalization 的文件类型转换 —— 实现本无转换层（PPT 描述性包装），无需代码动作
- [x] 删 evidence_tier 中 `convention` 档 → 两档（explicit / inferred；inferred 条目 description 须 "inferred:" 前缀；纯惯例不降级收留而是不收）
- [x] 删 LLM confidence 自评全链路（schema required/属性/示例/自检/Source Verification 处置 + attack agents 优先级改 evidence_tier=explicit）
- [x] category standardization → 纯端点分类（固定词表 schema/data/search/index/admin/other，去"标准化"提法）

### 1.2 Step 2 测试脚本生成〔slide 17，对应内容页 16〕✅ 2026-08-17 落地（commit 0194fd8）

- [x] 分块规则落地：`scripts/chunk_contract.py`（endpoint 分组，≤12 可攻单元/块，超限切多块，字典序稳定；chroma 真实契约 44 单元→10 块）+ 8b 编排接线（每轮 chunks[R-1]，vein 不受限）
- [x] attack agents（boundary/semantic/state）数量下限（≥5/≥5/≥3）删除 → 策略覆盖目标驱动（策略×约束覆盖完即收工，覆盖清单写入 Attack: docstring 供统计）
- [x] 删脚本去重功能 ✅（orchestrator 8c 自动去重 + 跨 Agent 交叉审查 + confidence 抽样全删；缺陷级去重保留 8e.5；SKILL.md 同步）
- [ ] 保留 run check scripts（语法/风险检查是安全措施，反馈未要求删；若设计定稿认为多余再议）
- [x] **不合格脚本打回重生成机制补课**（2026-08-17 查证+落地：v2.5 确定性 retry 子循环已实现但只落一半）
  - [x] **接线**：mine.md 8d.5 已切到 `_classify_script_errors.py` + `_apply_script_retry.py`（执行前静态 AST 检查）；`scan_script_errors.py` 保留作运行期兜底 ✅
  - [x] **补测**：tests/test_adr0008_pipeline.py 覆盖分类器 5 类 + apply-retry counter/超限删除路径 ✅
  - [ ] **观测**：retry 子循环结束加 regen 成功率统计写入 execution_summary（待端到端跑通时验证——历史仅 1 会话进过 retry 且未修好，机制是否真在工作需新数据）
- [x] **整理三类 attack agents 各自内置策略清单**（PPT slide 17 素材，见 3.1）✅ boundary 7 / state 7 / semantic 7 已确认（commit 0194fd8 落实时核对）

### 1.3 Step 4 缺陷确认（重写，动作最大）〔slide 22，对应内容页 21/33/34〕

- [x] **新架构设计定稿** → ADR 0008（`mftui/TestVDB/docs/adr/0008-evidence-chain-duo-agent.md`，2026-08-17 拍板）
  - evidence-builder：step1 = judge-doc + judge-evidence 合并 + 证据链追溯（非 dev-reviewer 主动复现），step2 源码搜证；**按候选并发派发**（1 builder/候选，任务重减压提效）
  - chain-auditor：**专用 agent**（已拍板，不用机械脚本），只读证据链文件，完备性/一致性/自洽性 + 三视角聚合；全部 builder 收口后派发
  - novelty 检查：后置到产出提交前最后一步（复用 novelty_gate.py）
  - 实现前推演 6 缺口已全部拍板（2026-08-17，均按推荐走）：**B1** L1 前移为 EXECUTION→EVIDENCE_BUILD 转换门 + L2 删；**B2** 新写 `scripts/extract_candidates.py` 机械提取 DEFECT_FOUND → candidates.jsonl 作 fan-out 派发清单；**B3** auditor 单实例单批次写 chain_verdicts.json；**B4** novelty_gate 加 load_chain_verdicts 分支（旧 stage2_aggregation 兼容期 fallback）；**B5** pipeline_state 改名 DEBATE_S2→EVIDENCE_BUILD、VERIFY_LIVE→CHAIN_AUDIT，删 aggregate_votes/gate_severity_coverage 两 gate；**B6** archived/ 归档在 Step 9 novelty 终判后一次性执行 + manifest.json 记 related_issue_numbers
  - 实现顺序：①extract_candidates.py ②evidence-builder/chain-auditor agent 规范 ③pipeline_state 改名 ④novelty_gate 适配 ⑤mine.md+orchestrator.md 编排改写（含 1.2 retry 接线）⑥plugin.json 注册表 ⑦删 6 个旧 agent 文件 ⑧tests 补用例（含 1.2 分类器/apply-retry 用例）
- [x] 删四个 LLM judges（Judge_doc / Judge_evidence / Judge_severity / Judge_novelty）✅ 2026-08-17 落地
- [x] 删 dev_reviewer（连同 verify-live-l2——B1 拍板）✅ git rm，plugin.json 注册表同步
- [x] FP 判定输出必须注明判定证据来源（fp_evidence_source: doc/source/both/behavior——chain-auditor.md 已落地）
- [x] severity 分级直接删 ✅ 全链路清理完成（commit db45631，2026-08-17 全局摸底后分类处置）：
  - 修正认知：verify_defects.py 本就无 severity 代码分支（仅 docstring 提及）
  - 删：aggregate_votes.py(63处)+gate_severity_coverage.py(22处)+injector --mode judge+mine.md 死注入块
  - 改：SKILL.md Phase5 重写 / M4 检查目标切 chain_verdicts（旧会话回退兼容）/ attack meta.json 消费链文字
  - 留：reporter 展示字段（Type 推断标注）+ debate_record schema 字段（兼容历史 final_verdict）
  - 不动：untracked 研究脚本群 + _extract_bug_shapes（Phase 0 情报内部字段）
- [x] 非 novel 处理从"直接删除"改为"单独归档"（archived/ + manifest.json，mine.md 9a 已落地）✅

**实现落地记录（2026-08-17，主插件，129 tests 全绿）**：
① `scripts/extract_candidates.py`（新增，真实会话验证：8 候选提取正确）
② `agents/evidence-builder.md` + `agents/chain-auditor.md`（新增）
③ `scripts/pipeline_state.py` 改名 EVIDENCE_BUILD/CHAIN_AUDIT + 自检更新；reconstruct_context.py / postcompact_verify.py 同步
④ `scripts/novelty_gate.py` 加 load_chain_verdicts（DEFECT 过滤/优先级/fallback）+ self_check 用例
⑤ `commands/mine.md` 8e→8e.7 重写（extract→L1→fan-out→auditor）+ 9a 归档段；`agents/orchestrator.md` 8e 重写 + judge 残留清理 + 数据流图更新；`scripts/verify_live_l1.py` 输入源切 candidates.jsonl
⑥ plugin.json 删 6 注册项增 2
⑦ git rm 六个旧 agent 文件
⑧ `tests/test_adr0008_pipeline.py` 19 用例（含 1.2 retry 子循环补课：分类器 5 类 + apply-retry counter/超限）
附带：mine.md 8d.5 retry 接线完成（_classify + _apply_script_retry 接入主流程，scan_script_errors 保留兜底）

---

## 2. 实验设计（全部在最新实现上端到端重跑，旧 124/45/28 数据作废）

### 2.1 RQ1 挖掘能力〔slide 25，对应内容页 24〕

- [ ] 设计端到端运行实验方案（依赖 1.1–1.3 完成）
- [ ] FP 列直接使用最新过滤后剩余数据，Submitted 同步变化
- [ ] 新增统计列"发现已被报告 bug"（与已确认新 bug 区分）
- [ ] 运行中顺便采集 novelty 归档数据（对应 1.3 归档要求）

### 2.2 RQ2 假阳性分析（整个重做）〔slide 36，对应内容页 26–35〕——2026-08-17 纠正：不消费 RQ1 产出，直接用 Phase 2 实验集 ✅ 2026-08-19 收官

**方案（用户拍板）**：以 Phase 2 实验集（71 case + 143 packets + GT 44）为载体，把被测判定者从旧 dev-reviewer 换成新链路（evidence-builder + chain-auditor）。RQ2 与 RQ1 解耦、可立即开工。

- [x] **针对性改造**（2026-08-17~19 完成）：tvdb_sessions 实验树（15 版本组、71 链、契约/intel），gen_dispatch_v71 派发器（claim 程序化 + 机械预跑注入 + leak_scan），容器 start_container.py
- [x] 与 GT 对照指标全链完成：v4.1 0.103 → E2–E6（机械化+闭环）→ v7 全量 0.614 → v7.1 机械注入 0.727 → v7.x 三轮中位 **0.705 [0.682,0.727] / 0.775（headline）** → v8 增量 0.886（定向口径）→ **v9 四轮全量 0.909/0.889（注入口径 in-sample，逐案四轮一致）**；fp_evidence_source/root_cause 分布在 v9 判词内（标签层方差 15/18 案漂移已量化）
- [x] 人工核查协议完成（等价产出）：
  - 判 FP：6→5 案（027 闭环翻正），来源 doc/source/both/behavior 齐全；根因五类（approximate_by_design/mundane/contract_misread/script_error/eventual_consistency）
  - 误判 FP 根因：B 规则2 同族错判 014/028（与 029 现象同族 GT 相反，已拍板接受现状）；011 认知锚点提取遗漏（2026-08-24 复核 #49844：维护者复查否定修复，GT=FP 正确）；qdrant_009/weaviate_009 无 by-design 标签（保守边界不注入）
  - 判 TP 漏 FP：FN 4 全为 violates 误标族（001/003/004/024，契约缺断言无米之炊）
  - 7 NME rework 闭环（builder 重做+auditor 复审，≤3 轮）全部收敛
- [x] 产出"过滤前后对比"表：rq2_before_after_table.md（sl 0.422 / vt 0.422 / fixF 0.578 → 新链路无注入 0.705 / 注入 0.909 + GT 分母差异披露）
- 补强（超出原计划）：三轮→四轮方差复测（v9d 严格同链 i.i.d. 对 0 差异）；gates-only 基线（LLM 边际贡献 bound）；8 案 LLM 子集 0/32 翻转 p≤0.089；pp:review 独立三审 Meta ACCEPT（9 项 Priority Revisions 处置 1-8）

### 2.3 RQ3 对比实验〔slide 38，对应内容页 37〕——2026-08-25 v3.4 slide 48 重申，归入 v3.4 §F 统一推进

- [ ] 最新版上直接跑 TestVDB vs VDBFuzz：数据库版本一致、耗时一致，对比挖掘成果
- [ ] （理想项）获取 VDBFuzz 的 bug list → 做 TestVDB 挖掘复现尝试或直接分析

### 2.4 跨项风险（已拍板处置，2026-08-17）

- [x] Phase 2 fixA–fixI 存量数据 → **数据及实验包单独归档一份，论文不再保留相关内容**
- [x] 确认 Phase 3 probe/gt.json 不受 RQ2 口径变化影响（2026-08-19 核对：phase3 gt.json 44 bugs ≡ 71 案实验集 CONFIRMED 44 集，双向零差；9149 证伪已正确落地，两处 GT 源无漂移。注意 phase3 gt.json 是"每版本应发现 bug 清单"（RQ3 探针用），与 cases_index（RQ2 判定用）语义不同但 CONFIRMED 集合一致）

---

## 3. PPT 改动

### 3.1 讲述页（不依赖实验，可先行）

- [ ] raw knowledge 提取页〔补 slide 12〕：为什么先提 raw knowledge？重点/关心的信息？如何组织？文档从何而来、怎么爬、如何防止漏爬错爬、具体流程？〔2026-08-25 v3.4 改名：raw knowledge → knowledge，且实现上改 raw_knowledge.json，见 v3.4 §A〕
- [ ] category 表述页〔slide 13/14〕：改为纯分类表述，去掉"标准化"提法
- [ ] attack agents 策略页〔slide 17〕：列出三类 agent 各自内置策略清单（素材来自 1.2）
- [ ] 缺陷确认新架构页〔重写 slide 21/33/34 → 22〕：新 agent 形态 + 证据链检查 + novelty 后置（依赖 1.3 定稿）

### 3.2 数据页（依赖实验完成）

- [ ] RQ1 表〔slide 24〕：新列"发现已被报告 bug" + 最新数据
- [ ] RQ2 页〔slide 26–35 压缩〕：删幻觉/自偏好/投票分析链，仅留过滤前后对比
- [ ] RQ3 表〔slide 37〕：新对比实验数据 + VDBFuzz bug list 分析（若取得）

---

## v3.1 关键路径

```
1.3 Step4 新架构定稿(含推演6缺口) ──→ 实现顺序①-⑧ ──→ 1.1/1.2 减法落地 ──→ 2.1 端到端重跑 ──→ 3.2 数据页
                              └──→ 3.1 讲述页（raw knowledge / 策略清单可先行，不依赖实现）
```

注：1.1–1.3 与 2.2/2.4 已落地；2.1 端到端重跑未启动，**须与 v3.4 §C/D/E 的改动范围对齐后再排**（避免重跑完又改机制）。

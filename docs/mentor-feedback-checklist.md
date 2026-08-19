# 导师 v3.1 PPT 反馈落地 Checklist（2026-08-17）

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
  - 误判 FP 根因：B 规则2 同族错判 014/028（与 029 现象同族 GT 相反，已拍板接受现状）；011 GT 内部矛盾；qdrant_009/weaviate_009 无 by-design 标签（保守边界不注入）
  - 判 TP 漏 FP：FN 4 全为 violates 误标族（001/003/004/024，契约缺断言无米之炊）
  - 7 NME rework 闭环（builder 重做+auditor 复审，≤3 轮）全部收敛
- [x] 产出"过滤前后对比"表：rq2_before_after_table.md（sl 0.422 / vt 0.422 / fixF 0.578 → 新链路无注入 0.705 / 注入 0.909 + GT 分母差异披露）
- 补强（超出原计划）：三轮→四轮方差复测（v9d 严格同链 i.i.d. 对 0 差异）；gates-only 基线（LLM 边际贡献 bound）；8 案 LLM 子集 0/32 翻转 p≤0.089；pp:review 独立三审 Meta ACCEPT（9 项 Priority Revisions 处置 1-8）

### 2.3 RQ3 对比实验〔slide 38，对应内容页 37〕

- [ ] 最新版上直接跑 TestVDB vs VDBFuzz：数据库版本一致、耗时一致，对比挖掘成果
- [ ] （理想项）获取 VDBFuzz 的 bug list → 做 TestVDB 挖掘复现尝试或直接分析

### 2.4 跨项风险（已拍板处置，2026-08-17）

- [x] Phase 2 fixA–fixI 存量数据 → **数据及实验包单独归档一份，论文不再保留相关内容**
- [x] 确认 Phase 3 probe/gt.json 不受 RQ2 口径变化影响（2026-08-19 核对：phase3 gt.json 44 bugs ≡ 71 案实验集 CONFIRMED 44 集，双向零差；9149 证伪已正确落地，两处 GT 源无漂移。注意 phase3 gt.json 是"每版本应发现 bug 清单"（RQ3 探针用），与 cases_index（RQ2 判定用）语义不同但 CONFIRMED 集合一致）

---

## 3. PPT 改动

### 3.1 讲述页（不依赖实验，可先行）

- [ ] raw knowledge 提取页〔补 slide 12〕：为什么先提 raw knowledge？重点/关心的信息？如何组织？文档从何而来、怎么爬、如何防止漏爬错爬、具体流程？
- [ ] category 表述页〔slide 13/14〕：改为纯分类表述，去掉"标准化"提法
- [ ] attack agents 策略页〔slide 17〕：列出三类 agent 各自内置策略清单（素材来自 1.2）
- [ ] 缺陷确认新架构页〔重写 slide 21/33/34 → 22〕：新 agent 形态 + 证据链检查 + novelty 后置（依赖 1.3 定稿）

### 3.2 数据页（依赖实验完成）

- [ ] RQ1 表〔slide 24〕：新列"发现已被报告 bug" + 最新数据
- [ ] RQ2 页〔slide 26–35 压缩〕：删幻觉/自偏好/投票分析链，仅留过滤前后对比
- [ ] RQ3 表〔slide 37〕：新对比实验数据 + VDBFuzz bug list 分析（若取得）

---

## 关键路径

```
1.3 Step4 新架构定稿(含推演6缺口) ──→ 实现顺序①-⑧ ──→ 1.1/1.2 减法落地 ──→ 2.1 端到端重跑 ──→ 3.2 数据页
                              └──→ 3.1 讲述页（raw knowledge / 策略清单可先行，不依赖实现）
```

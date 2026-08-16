# 两臂对比实验包（single-LLM / multi-agent voting）

日期：2026-08-16 | 状态：材料冻结（audit 0 FAIL）；single-LLM 三轮已完成（见 single_llm/ARM_SL_REPORT.md）；voting 待跑

## 定位

论文对比基线：同一 71 case 冻结材料上，测「判断架构」轴的两个点
（第三点 dev-reviewer = fixF 三轮，已有）。

| 臂 | 材料 | 工具 | 架构 | 数据状态 |
|----|------|------|------|---------|
| single-LLM | 头部+log+契约段 | **无** | 1 次纯调用 | 待跑（71×3 轮） |
| voting | 同上（judge 分槽） | 只读本地（novelty/doc 关网） | 4 专责 judge + aggregate_votes.py 代码聚合 | 待跑（71×4×轮） |
| dev-reviewer | +源码+锚点+活 DB | Bash/Grep 实跑 | 单 agent SOP + 内三视角 | fixF/run2/run3 |

## 目录

```
arms/
├── single_llm/materials/{did}.md      71 份内联材料（头部 + observed + expected）
├── voting/sessions/{vendor}/{version}/{did}/
│   ├── candidates/{did}.json          judge 输入（claim/expected/observed 分槽）
│   ├── output_{did}.log               71 份（severity 崩溃信号规则消费）
│   └── debate_logs/execution_results.json
├── voting/sessions/{vendor}/{version}/
│   ├── structured_contract.json       15 份（judge-doc 消费，tvdb_sessions 同源）
│   └── raw_knowledge.md               15 版本组（doc judge 来源表）
└── MANIFEST.json                      逐 case 材料构成 + 泄露控制清单
```

构造脚本：`../build_arms_materials.py`（纯机械，零 LLM 参与）
审计脚本：`../audit_arms_materials.py`（GT/packet 通道/issue 原文/路径 四面扫描 = 0 FAIL）

## 材料面（两臂严格对齐 voting 阶段 judge 的本地可见面）

**给**：
- 头部：defect_id / vendor / version / defect_type / endpoint
- observed：raw_observation（53/71 有）+ output_*.log 全文（70/71；milvus_001=占位符特例）
- expected：契约全量匹配约束（endpoint 归一化，token 集合双向包含）+ packet 关键词段 + api_template(doc_quote)

**不给（审计强制）**：GT 标签/group、maintainer 表态、related_issue_numbers、
cognition/bug_shapes/source_excerpt（GT-informed 与源码通道）、issue 原文 title/body、
intelligence 文件、源码 clone、活容器、网络。

## 已知边界（预注册披露）

- **2 case 无 expected 依据**（契约+关键词段双零命中）：qdrant_014 / qdrant_018——
  judge 视为无契约对照（照 packet 先例 verdict=NEUTRAL 语义，voting 内按 SOP 默认路径走）
- **17 case 关键词段 0 命中**但契约全量匹配有约束（endpoint 归一化补救了 15 个）
- milvus_001 log 为占位符（材料不可达死刑类，GT=CONFIRMED）；三臂同口径沿用
- 契约 doc_quote 命中率 0（契约本身不含 doc_quote 字段值）——expected 实际是
  assertion+source_url 文本；doc judge 联网验证关网后走降级路径，属 as-shipped 语义
- voting 臂 judge SOP 原配 model=sonnet → 统一 GLM-5.2（记 deviations）
- aggregate_votes.py 机制快照 hash 待 run3 归档后写入预注册

## 深度审查发现（2026-08-16，15 项检查 + 审计阴性对照）

**已修复**：
- voting case 目录补 `output_*.log`（judge-severity 崩溃信号 v2.2 规则读该文件名；此前只内嵌在 execution_results）
- voting 版本目录补 `structured_contract.json`（judge-doc SOP 读 `${SESSION_DIR}` 层契约；tvdb_sessions 同源，含 fixE 修复断言 state_collections_create_001——三臂同基座确认）

**保留决策（权衡后不动）**：
- **契约抽取超集（用户确认保留）**（41/71 case ≥10 条，qdrant points 类最多 23 条）：收紧方案会误切（qdrant_002 是 search 参数问题，最短组会拉到 upsert 家族约束）；dev-reviewer 读的就是全量契约（100+ 条），超集更接近其材料面。稀释问题如实披露，分析时按"抽到条数"分桶做后分层观察
- **观察摘要 [c1] 跨臂不对称**：dev-reviewer SOP 明文"output log 是唯一事实来源"，fixF 70 判词 0 次引用 [cX] 格式；两臂保留摘要——原管道 judge 本就消费 probe 断言摘要（execution_results 语义），也是 log 标记缺失（见下）的部分补偿

**形态差异（已处置/必须披露）**：
- **log 无 judge 判定标记**：原管道 attack 脚本自 print 断言行（`VERDICT: DEFECT_FOUND (TypeN_...)` 等，output_*.log = 脚本 stdout 原样重定向），evidence judge 的判定表围绕此类标记设计。**补充考古**：判定表词汇 `FAILED: Type1` 在产出侧全库不存在——as-shipped 下 evidence 判定本就主要走 LLM 语义匹配（attack 的 VERDICT 行含 "TypeN" 可被表行宽松对上）。我们的 replay probe 只打 HTTP 不打 print，连 VERDICT 行也没有。
  **处置（用户拍板）**：三处（voting log 文件 / execution_results 内嵌 / single-LLM 材料）统一补中性行 `VERDICT: UNKNOWN (replay capture — no attack-agent assertion output; raw HTTP only)` ×70（milvus_001 占位符不补）。中性 = 不携带判断，仅满足格式路径；evidence judge 走"日志为空或无对应判定 → 保守评估"的语义解读路径。补行属实验构造，预注册披露

**审查通过项**：raw_observation 源流（probe 统计输出非 LLM 改写）；defect_type 无组间区分力（A/B/C 分布重叠）；判断性词汇扫描 71 case 仅 1 良性命中（探针集合名 BatchVectorBugRepro）；端口仅 localhost 三端口；审计脚本阴性对照通过（注入 "gt"/BY_DESIGN/#47635/[Bug]/.srcdir 探针 9 项全捕获）

## 派发纪律（对齐 fixF 系列）

- voting 臂执行面 = 纯本地读取 + 确定性聚合脚本，**不涉容器/DB/网络**，
  与并行会话零资源冲突；唯一共享约束是 API 速率（串行化批次，防 429 重演）
- 每 case 新会话；single-LLM 无工具（纯调用）；voting 臂 novelty/doc judge 关网跑
  （SOP v2.3 自带降级：novelty 全 unknown→is_defect；doc 走本地 raw_knowledge）
- ≥3 轮报中位数+区间；per-case McNemar；预注册判据带跑前写死

# PPT 更新内容稿（2026-08-19，基于插件最新现状）

对应 mentor-feedback-checklist 3.1 讲述页四项 + 3.2 可先行部分。
来源：插件 cache 2.3.0（与 mftui/TestVDB 同步）、ADR-0008、RQ2 v9 实验。

---

## 页 1：raw knowledge 提取页（重写 slide 10-13 区域，回应 slide 12 反馈）

**标题**：Step 1: We extract structured behavioral claims from official documentation

**为什么要先提 raw knowledge（动机）**：
- VDBMS 文档是自然语言、版本散布（milvus.io / qdrant.tech / weaviate.io / github），
  无法直接驱动测试生成——需要一个"单一可信中间层"承接后续所有环节
- knowledge-extractor 是**全流水线唯一有网络权限的 agent**（dataAccess: raw），
  其余 agent 只消费其产出（raw_knowledge.md）——爬取边界收敛在一处，可审计

**提取重点与组织（What & How organized）**：
- 按端点组织：`### {category}/{endpoint}` 章节结构，每端点记录请求/响应形态、参数、约束
- 关心的信息：行为声明（claims）——类型/取值范围/状态前置/行为语义四类约束
- 版本锚定：文档 URL 版本号验证（页面版本标注 vs 目标版本），版本不符不采信

**文档从何而来 & 防漏爬错爬（Provenance & Completeness）**：
- 官方文档站（四家固定入口）+ GitHub 仓库（weaviate 用 OpenAPI spec 按版本 tag 交叉核对，
  tag 缺失直接报错不降级——防"current-only 静默漂移"）
- Crawl4AI（本地 Docker）为主、WebFetch 降级；每页带 source_url 入库
- **完整性自检（Step 6）**：每个 target 概念文档清单 ≥5 页全抓、OpenAPI cross-check
  端点覆盖核对，未达标约束不得标 source_verified
- **Source verification（claim formalizer）**：每条约束回取 source_url 验证"原文确实
  包含该断言"，防幻觉

**流程**（原图 1-4 步改为）：
1. Crawl4AI 抓取（官方文档 + OpenAPI 交叉）→ raw_knowledge.md
2. claim formalizer 提取行为声明 + source verification（每条回验 source_url 真包含）
3. evidence tiering 两档（explicit / inferred，inferred 须 "inferred:" 前缀；纯惯例不收）
4. 端点纯分类（固定词表 schema/data/search/index/admin/other）→ structured_claims.json

（删：format normalization 文件类型转换、convention 档、confidence 自评全链路——已落地）

---

## 页 2：attack agents 策略页（重写 slide 16，回应 slide 17）

**标题**：Step 2: Three attack agents generate test scripts from the contract

**三 agent × 7 策略清单（内置，插件现状）**：

| attack-boundary（边界） | attack-state（状态） | attack-semantic（语义） |
|---|---|---|
| 1. 边界值攻击（range） | 1. CRUD 后 COUNT 一致性 | 1. Behavioral Contract 违规 |
| 2. 类型边界攻击（type） | 2. DELETE 后一致性 | 2. 错误诊断质量 Type-2 专项 |
| 3. 维度不匹配攻击 | 3. Upsert 幂等性 | 3. 合法输入被错误拒绝（Type-1 反向） |
| 4. 特殊值攻击（NaN/Infinity/畸形） | 4. 并发操作攻击 | 4. 隐式类型转换 |
| 5. 错误消息质量评估（Type-2） | 5. 事务边界攻击 | 5. 搜索语义正确性 |
| 6. 资源极限/DoS（Type-3） | 6. 索引构建期间状态一致性 | 6. Metamorphic 关系测试 |
| 7. Malformed Input/字符 Fuzzing | 7. 生命周期并发攻击 | 7. 过滤参数语义正确性 |

**数量下限已删（ADR-0008）**：不再"≥5/≥5/≥3 脚本"，改为**策略覆盖目标驱动**——
每 agent 以"策略 × 约束覆盖完"为收工条件，覆盖清单写入脚本 docstring 供统计。
**分块规则**：structured_claims.json 按 endpoint 分块（≤12 可攻单元/块，超限切多块，
字典序稳定），每轮一块（vein 不受限）。
**跨会话策略消费 + 认知盲点驱动**：策略选择消费 threat model 的盲点模型与全局权重。

---

## 页 3：缺陷确认新架构页（重写 slide 20/21/33/34 → 一页，回应 slide 22）

**标题**：Step 4: Evidence-chain duo-agent defect confirmation

```
execution_results[]
        │ extract_candidates.py（机械提取 DEFECT_FOUND）
        ▼
┌────────────────────────────────────┐
│ evidence-builder（按候选并发 fan-out）│
│  step1 文档验证+执行证据审查+链追溯    │
│  step2 源码搜证（clone Grep+调用链） │
│  → evidence_chain/{did}.json/候选  │
└────────────────────────────────────┘
        │ 全部收口后
        ▼
┌────────────────────────────────────┐
│ chain-auditor（专用，只读链文件）     │
│  完备性/一致性/自洽性三查 + 第4查     │
│  四视角聚合 A 契约/B 物理/C 行为/D 认知│
│  → DEFECT | NOT_DEFECT              │
│  → fp_evidence_source: doc/source/  │
│    both/behavior（FP 必注证据来源）  │
└────────────────────────────────────┘
   DEFECT→reporter   NOT_DEFECT→过滤
        │ 全轮次结束、提交前（终判后置）
        ▼
┌────────────────────────────────────┐
│ novelty-check（Novelty Gate 复用）   │
│  NON_NOVEL → archived/ 归档不删      │
│  （manifest.json 记 related issues， │
│   支撑"发现已被报告 bug"统计列）      │
└────────────────────────────────────┘
```

**与旧架构对照**（讲述口径）：5 个 LLM 判定角色（4 judges + dev-reviewer）→
2 个 agent + 1 个提交前终判；投票/加权聚合/doc 门控全删；severity 删；
rework 打回闭环（NEEDS_MORE_EVIDENCE → 针对性工单重做，≤3 轮）。

---

## 页 4：RQ2 过滤前后对比页（重写 slide 26-35 压缩为一页，slide 36 数据先占位）

**标题**：RQ2: FP filtering before/after the new confirmation chain

| 判定链 | recall | precision | FP 抑制率 |
|--------|--------|-----------|-----------|
| single-LLM（1 次纯调用） | 0.422 | 0.76–0.85 | 0.77 |
| voting（4 judge 级联） | 0.422 | 0.78–0.91 | —（FP 率 0.115） |
| dev-reviewer（旧单 agent） | 0.578 | 0.76–0.84 | 0.69 |
| **新链路·无注入（headline）** | **0.705** | **0.775** | **0.67–0.70** |
| **新链路·注入口径（ablation）** | **0.909** | **0.889** | **0.815** |

- 同一 71 case 材料只动判定架构：0.422 → 0.578 → 0.705（无注入即超旧最优 +0.127）
- 注入口径（文档考古断言 + 维护者认知锚点）为 GT-informed in-sample，论文分开呈现
- 方差分层：verdict 层四轮逐案一致（89% 会话前定案）；LLM 方差挤压到归因标签层
- gates-only 基线：纯机械层 0.907/0.886，LLM 补全 9 悬置案全对（边际贡献有界）

（slide 25 的 RQ1 表数据列等端到端重跑——已按你的决定搁置，页留占位）

---

## 落地方式待拍板

1. 我直接改 PPTX（python-pptx 替换四页文本框/表格——版式受限于原模板）
2. 出内容稿（本文件）+ 大纲，你在 PPT 里手工重排版（保设计自由度）
3. 两步走：我先把旧 7 反馈页标记"已处置"+删除 judges/convention/confidence 旧文案，
   新页你手工排

---

# 布局设计稿（2026-08-19 追加，用户手工排版用）

设计语言（取自原模板 theme1）：白底 + 深蓝 #0A4A94 标题/主框 + 红 #FF0000 旧版对照
+ 主题色点缀（蓝 #6096E6 / 绿 #56CA95 / 橙 #FFBA55 / 红 #F18870 / 紫红 #EC5F74），
Arial + 微软雅黑，页标题 24pt、区块标题 16pt、正文 14pt、脚注 11pt 灰。

## 页 1a｜Step 1 动机+流程（替换 slide 10–13 → 两页之一）
- 左窄右宽双栏：左 1/3 浅蓝底 #EAF1FD 圆角卡片"WHY an intermediate knowledge layer"
  三要点（唯一联网 agent / 按端点组织 / 版本锚定）；右 2/3 纵向四步 PIPELINE
  （Crawl → Formalize+verify → Tier → Classify，#6096E6 编号圆点串联）
- 底部灰底横条：raw_knowledge.md → structured_claims.json 单一可信中间层

## 页 1b｜防漏爬防幻觉（slide 12 六连问的直接回应）
- 双栏对称：左"防漏爬 Completeness"绿框 #56CA95 描边（≥5 页全抓/OpenAPI 覆盖核对/
  未达标不得标 source_verified）；右"防错爬 Authenticity"蓝框 #6096E6 描边
  （OpenAPI cross-check/tag 缺失报错不降级/source verification 回验原文）
- 底部红字对照行：convention 档 + confidence 自评已删

## 页 2｜attack 策略矩阵（替换 slide 16 正文）
- 三列等宽策略表：attack-boundary / attack-state / attack-semantic 列头深蓝底白字，
  每列 7 条策略；策略名的 (Type-1/2/3) 标注用橙/红/紫红小字点缀呼应缺陷类型色
- 底部两条机制：coverage-driven stopping（数量下限已删）+ contract chunking ≤12

## 页 3｜Step 4 新架构（替换 slide 20/21/33/34 → 一页）
- 左 70% 纵向三框流程：evidence-builder 蓝框（×N 并发）→ chain-auditor 绿框
  （三查+四视角）→ novelty-check 橙框（终判后置+archived 归档）；框间箭头标注
  "全部收口后"/"全轮结束·提交前"
- 右 30% 灰底"What changed"卡片：删除项红字删除线（4 judges/dev-reviewer/
  severity/投票聚合），新增项绿字（2 agents+终判/rework 闭环/fp_source 必注）

## 页 4｜RQ2 过滤前后对比（替换 slide 26–35 → 一页）
- 上 2/3 五行对比表：前三行旧链灰字、新链无注入行浅蓝底高亮、注入行浅绿底高亮；
  表内数字加区间 [min–max]
- 下 1/3 三点解读：架构轴增益/注入 ablation 分开呈现/方差分层表述
- 表底 11pt 灰脚注：GT 分母差异披露（45/26 vs 44/27，9149 证伪）

## 页序与删页
- 删 7 个反馈页（12/14/17/22/25 部分/36/38——25 的 RQ1 部分留待重跑）
- slide 24/25 RQ1 表占位等端到端；slide 37/38 RQ3 不动等对比实验

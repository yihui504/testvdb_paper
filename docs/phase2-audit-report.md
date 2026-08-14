# Phase 2 三次实验系统审计与材料修复落地

> 日期：2026-08-14。审计对象：run1（curated）+ run2/run3（clean，排雷后）三轮 dev-reviewer 判定实验的全部输入/过程/修复动作。
> 目的：回答三个问题——(1) 踩坑的根因是什么；(2) 为什么 0.822 的 recall 增益不可由抽样复现；(3) 历次"修复"到底修复了什么；并对五个维度（派发 prompt / 材料形态 / 版本分组 / intelligence / 网络通道）做系统审计，把修复落地成 v2 材料包。

## 1. 踩坑根因：逐个归因

| # | 坑 | 现象 | 根因 | 类别 |
|---|----|------|------|------|
| 1 | endpoint 标签错配 | fill_endpoints 对 milvus REST 探针抽取偏差，24 个候选 endpoint 指向错误操作 | run1 清洗时**只在重派 prompt 里修正，未持久化回材料**——清洗动作与材料包脱节，run2/run3 拿"最新整理版"= 拿回了旧雷 | 材料缺陷（已修复） |
| 2 | milvus 3.0.0 容器争用 | 并发 2 batch 打同一容器 → timeout/集合不可用，10 case 全判 FP | 对 milvus 资源消耗假设错误；mfat 并发批处理与单容器单版本冲突 | 执行缺陷（已修复，顺序 batch） |
| 3 | zombie 孙 agent | qdrant 1.18.2 batch agent 违规用 Agent 工具派孙 agent，写坏 9373 | SOP 有"禁止派孙"禁令但 batch 派发时未强调，agent 自主 delegate | 执行缺陷（已修复，铁律固化） |
| 4 | 空日志判 UNCERTAIN | 7 个 SDK 探针 case 无 raw HTTP，agent 面对空日志放弃 | **材料不完备**：probe_common 的 raw 捕获只挂 http()，pymilvus SDK 探针无 raw；真实 dev-reviewer 的唯一事实源缺失 | 材料缺陷（未修复，v2 补 raw） |
| 5 | 浅审无 source_excerpt | run3 2.6.16 batch2 对 3 case 产出无源码判词 | 多 case 一会话 → 后面 case 被草率处理；SOP 遵守度随 batch 长度衰减 | 执行缺陷（部分修复，靠重做） |
| 6 | dev_review JSON 损坏 | source_excerpt 嵌 shell 命令原文，引号转义破坏 JSON | 输出格式约束不足（SOP 示例没警告转义） | 执行缺陷（已修复，prompt 警告） |
| 7 | **重判 prompt 泄露**（新发现） | 排雷重判时 prompt 写"endpoint 已修正为**裁决认定的方向**"、"**不要因流量不符判 FP**"、"上次判了 UNCERTAIN 无效" | 我把 run1 的裁决方向**明示给了重判 agent**——重判的 25 case 被引导，无雷版 κ=0.587 的这 25 case 严格性存疑 | **实验污染**（需披露 + v2 干净重跑） |
| 8 | 材料形态带实验标记（新发现） | stage2_aggregation 的 summary="rerun: 1 candidate (Phase 2 confirmation sample, dev-reviewer redo)"、aggregator="layout_inputs.py (rerun)"、note 提到 "no GT/rationale leaked"；SESSION_DIR 路径含 `testvdb_paper/.paperpilot/phase2-rerun/run2/` | 合成材料时把实验元话语写进了 dev-reviewer 会读的文件——真实流程里这些字段是 pipeline 聚合产物（aggregate_votes.py），不含"rerun/实验/GT"字样 | 材料形态偏差（v2 修复） |
| 9 | intelligence 与样本同源（新发现） | qdrant bug_shapes 的 known_instances 直接列 issue 9373（=样本），shape `qdrant-cardinality-oracle-count-exact-false` 的 name 就是 9373 的缺陷描述；weaviate 含 #9988 | intel 从 mftui 搬，mftui 的 intelligence 由**同一批 issue** 生成——模式库与测试样本同源，"考题在复习资料里" | GT 泄露（v2 修复：剔除样本 issue 引用） |
| 10 | defect_id=真实 issue number + SOP 解禁 github.com（新发现） | defect_id 形如 `milvus_50018`，SOP 允许 WebFetch github.com → agent 理论上可 WebFetch issue 页查真实裁决（GT） | 真实 TestVDB 的 defect_id 是攻击生成的编号，无 issue 语义；我们直接用 issue number 命名等于给了查 GT 的钥匙 | GT 泄露通道（未使用：3 树 0 次真 WebFetch；v2 匿名化） |

## 2. 为什么 0.822 的 recall 增益不可由抽样复现

run1 的 0.822 = 初判 0.644 + 三轮清洗救回 8 FN。救回动作按性质分三类，只有一类可由后续 clean run 自然复现：

| 救回类型 | 例子 | 动作性质 | 抽样/投票能否复现 |
|---------|------|---------|------------------|
| (a) 修复材料错误 | endpoint 错配 ×5（47763/52311/49889/52314/47635） | 模型拿到**错误输入**时系统性判 FP——输入错误是**确定性偏差**，不是采样噪声；修材料后模型自然判对 | ✅ 能——排雷持久化后 run3 的 0.667→0.711 提升正来自这里 |
| (b) 探索引导 | 9039（只测 sync 没测 `wait=false`）、52313（只测 REST 没测 gRPC get） | run1 人工在重派 prompt 里**告诉 agent"你漏了哪条路径，去测它"**——等于喂了半个答案。探索空间被人工定向 | ❌ 不能——每次 agent 是否探索到那条路径是随机的（run2/run3 都没探索到），三次投票都是随机探索，多数票不改变单次探索的覆盖缺陷 |
| (c) 修 probe↔issue 错配 | 50355（探针测 color 字段，issue 是 autoID upsert） | 材料内容错误（探针测的不是 issue 缺陷） | ✅ 能——修探针/修 stage2 描述后 clean run 可复现 |
| (d) GT 噪声 | 9149（bug 在版本范围不复现） | dev 判对、GT 错 | —（不是模型问题） |

**核心结论**：0.822 与 clean run 的差距里，(a)(c) 部分是"材料有错"造成的**确定性亏损**（可修复、已部分修复）；**(b) 部分是人工探索引导**——它把"该测哪条路径"这一关键信息注入了当次派发，等价于在 prompt 里给了半个答案。抽样只改变模型的随机种子，不会系统性把探索空间引向正确路径；投票三次都是随机探索，多数票也无法补上单次探索覆盖不到的路径。所以 **curated 0.822 是"人工增强的模型"的上界，不是"模型能力"的测度**。

## 3. 历次"修复"修复了什么、没修复什么

| 阶段 | 修复了 | 没修复 |
|------|--------|--------|
| run1 三轮清洗 | 当次派发 prompt 的 endpoint/路径/缺陷描述（case 级） | 材料本身（stage2/日志）——修复留在 prompt 里，没进材料包 |
| 排雷（fix_materials） | A 类 20 个 endpoint 标签持久化进三棵树；C 类 5 个流量缺陷在**重判 prompt 里提示** | C 类的提示仍在 prompt 层而非材料层；空日志 7 个没补 raw；且重判 prompt 本身泄露（坑 7） |
| run2/run3 过程修复 | 容器争用、孙 agent、JSON 损坏等执行缺陷 | 材料形态（坑 8）、intelligence 同源（坑 9）、WebFetch 通道（坑 10） |

**一句话**：过去所有修复都发生在"当次派发的 prompt"层，而用户真正要求的——**让 dev-reviewer 拿到的输入（文件形态+内容）与真实流程一致**——只有排雷的一半（A 类）落到了材料层。

## 4. 五维审计结果（详见 §1 表）

1. **派发 prompt**：重判阶段泄露严重（明示裁决方向/明示别判 FP/泄露上次结果/泄露实验性质）；首次派发相对干净但有"空日志行为引导"和路径泄露。run2+run3 的 2.6.19/2.3/2.6.10 等版本由同一 agent 连审两 run 同 case（独立性破坏）。
2. **材料形态**：stage2_aggregation 的 summary/aggregator/note 含实验元话语；SESSION_DIR 路径含 `phase2-rerun/run2`；defect_id 用真实 issue number。三处都偏离真实 dev-reviewer 的输入形态。
3. **版本分组**：version_source 全是报告者自述版本的正则抽取，无 fix 版本信息；A 组（TP_FIXED_PR，28 个）存在 post-fix 风险（9149 实证 1 例：bug 在全部版本范围不复现）。系统性核查 28 个 fix-PR 合入版本**尚未做**（列为本审计的后续待办）。
4. **intelligence**：developer_cognition/bug_shapes 从 mftui 同源 issue 生成，含样本 issue 引用（qdrant 9373、weaviate 9988）；抽象模式（by-design patterns、blindspot）本身有效，但 known_instances/example_issues 的具体 issue 引用需剔除。
5. **网络通道**：SOP 解禁 github.com + defect_id=issue number = 理论 GT 查询通道；实测 3 树 213 份 dev_review 中 0 次真 WebFetch（agent 全用本地 clone），通道存在但未使用——仍应在材料层关闭（匿名 defect_id）。

## 5. 修复落地：tvdb_sessions 材料包（v2）

把修复从 prompt 层搬到材料层，材料放在**中性路径** `C:/Users/11428/Desktop/tvdb_sessions/`（无 phase2/rerun/实验字样），构建/维护脚本在 `.paperpilot/phase2-rerun/`：

1. **中性路径**：`tvdb_sessions/sessions/{target}/{version}/{seq}/`——dev-reviewer 读到的所有路径均无实验标记。
2. **匿名 defect_id**：`{vendor}_{seq}`（seq 按 vendor 重新编号），实验侧映射存 `.paperpilot/phase2-rerun/defect_id_map.json`（不进材料树）→ 切断 WebFetch 查 GT 通道，同时贴近真实 attack 生成编号的形态。
3. **真实形态 stage2_aggregation**：aggregator="aggregate_votes.py"、summary="1 candidate confirmed by quartet debate"、保留真实字段（defect_id/endpoint/defect_type/severity_level/confirmed/related_issue_numbers，endpoint 用排雷后的值）、删除 rerun/GT note。
4. **清洗 intelligence**：剔除 known_instances/historical_instances/example_issues/source_issues 与文本中与 71 样本重叠的 issue number（替换为 `#<tracked>`），保留抽象模式与 developer_quote。已验证零残留。
5. **补 6 空日志 raw**（`fill_raw_v2.py`）：用活容器 + REST v2 重放 issue 声称操作（真实 attack agent 对 milvus 用 REST v2），生成真实 raw 证据（如 47729 nprobe=0 实测 code 0 返回结果）。仅 `milvus_001`（=47635，2.3 无 REST v2）保留空日志——这是该版本的真实形态（attack 只能用 pymilvus gRPC，无 HTTP raw）。
6. **干净派发协议 v2**（`gen_dispatch_v2.py`，指令内联不引用实验路径）：无 run/重审/空日志引导字样；不提示"别判 FP"；泄露词扫描（rerun/实验/GT/重审/修正/run2/phase2 等）0 命中。
7. **构建顺序**：`build_materials_v2.py`（重建包）→ `fill_raw_v2.py <ver>`（补空日志 raw），两个脚本的 OUT 均已指向 tvdb_sessions。

**诚实披露**：排雷后无雷版 κ=0.587 的 25 个重判 case 因坑 7 被 prompt 引导过，其判定只能作为"引导后上限"参考。材料 v2 + 协议 v2 就位后，需要用干净流程重跑这 25 case（或全部 71）才能得到无污染的一致性估计。

## 6. 后续待办（未在本轮完成）

- [ ] A 组 28 个 TP_FIXED_PR 的 fix-PR 合入版本 vs 实验 tag 版本系统核查（消除 post-fix 风险；9149 已实证 1 例）。
- [ ] 干净流程复跑 25 case（或 71）验证无污染 κ。
- [ ] probe↔issue 错配的剩余排查（50355/9373/49928 已查，其余 case 的探针内容 vs issue 声称缺陷未全量比对）。

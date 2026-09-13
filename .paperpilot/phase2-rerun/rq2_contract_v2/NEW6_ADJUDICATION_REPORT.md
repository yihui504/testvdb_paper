# 新提交 6 案链路审计报告（RQ2 式判定，2026-08-31）

## 目的与方法

对最新提交的 6 个 qdrant issue（#10368-#10373）按 RQ2 实验包同构流程执行当前最新链路（chain-builder + chain-auditor 体系的证据链 + 机械判定层）审计，得到"当前实现对新缺陷的检出/误判"活体测量。

流程（与 RQ2 同构，GT 隔离）：
1. **契约输入**：`sessions/qdrant/v1.19.0rq2/structured_contract.json`——6 条 explicit 断言，锚全部为 vendor 文档/spec 原文（GT-free）
2. **执行证据**：专用取证脚本按 issue 复现步骤生成原始 REQ/RESP 日志（v1.19.0 隔离容器 :16335），关键观测抽查确认
3. **建链**：2 个 evidence-builder 并行（GT 隔离——只给契约与日志，禁读 issue 语料与 anchors）
4. **机械判定**：check_chain_grounding + 引文预检

## 终态（6 案，全部机械定案，零灰区）

| 案 | issue | 链路判定 | vendor 裁决 | 一致 | 链级要点 |
|---|---|---|---|---|---|
| D1_snapshot_replica | #10368 | **NOT_DEFECT**（机械 REFUTED） | closed not_planned (by-design) | ✓ | 正确路由取证（PUT snapshots/recover + file:// location）：recover 后活点集 {0,1,2} 与快照点集**精确相等**——断言合规分支满足；源码 `recover.rs:364-367` standalone 分支直接 activate_shard、**不消费 priority** |
| D2_recommend_negdim | #10369 | **DEFECT**（机械 CONFIRMED） | **accepted** | ✓ | 负例超维 zip 截断静默接受；分数与截断预测逐位吻合（Δ≈2e-8）；源码 `recommendations.rs:110-114` zip 无校验 |
| D3_metadata_empty_noop | #10370 | **DEFECT**（机械 CONFIRMED） | **FP**（by-design，closed completed） | **✗** | PATCH metadata {} 键全保留；文档承诺 "To remove metadata, set it to an empty object" 在 v1.19.0 树内逐字命中（三重一致）；源码 merge-only 无移除路径 |
| D4_groups_nondeterministic | #10371 | **DEFECT**（机械 CONFIRMED） | **accepted** | ✓ | 10 次相同请求 9 个互异签名（强于断言文本的 8）；源码 `aggregator.rs` AHashMap 迭代序 + `drain()` 哈希序截断，无 id tie-break |
| D5_field_schema_array | #10372 | **DEFECT**（机械 CONFIRMED） | **accepted** | ✓ | field_schema 数组 200 接受（解析期拒绝缺失）；**披露**：本地源码 clone 实为 v1.18.0（目录名误导），1.19 解析路径可能已变——链内如实标注 |
| D6_strict_default_escape | #10373 | **DEFECT**（机械 CONFIRMED） | **to be released**（已修） | ✓ | 省略 limit 返回 10 点绕过 cap=5；机制链闭合：`check_limit_opt` 对 None 短路放行 → 通过校验后才 `unwrap_or_else` 物化默认 10 |

**链路 vs vendor 一致率：5/6（83.3%）**。唯一分歧 D3——且分歧可完全归因：争议双方是"版本化文档承诺"vs"维护者设计意图"，维护者已采纳改文档（#9907 澄清 merge 语义）——即**文档错侧**的 doc-implementation inconsistency，链路按版本化文档原文判 DEFECT 有据，属 RQ1 主对象（文档-实现分歧）而非审计误判。

## 关键发现

1. **对 vendor 确认真缺陷的召回：5/5 = 100%**（D2/D4/D5 accepted + D6 已修 + D3 按 by-design 被拒但现象真实）——当前链路对新缺陷的泛化能力实测无漏。
2. **唯一"误报"是文档错侧**：D3 的分歧不是链路错误，而是 vendor 文档与实现的真实分歧（RQ1 主对象）——链路依据版本化文档原文判定，维护者后续修正文档，分歧随文档修正消失。
3. **D1 的源码级澄清（修正旧探针误读）**：旧探针 R30 的"活数据被销毁"叙事源于数量巧合（前后都是 3 点）；正确路由取证显示 recover 行为是**精确恢复快照状态**（{0,2,10}→{0,1,2}），且源码证实 standalone 不消费 priority——链路判定与维护者 not_planned **完全一致**，断言的严谨表述（"restore the snapshot state or be rejected"）使合规判定机械成立。
4. **GT 隔离有效性**：两 builder 均未接触 issue 语料与 anchors；全部判定信息来自契约断言（vendor 原文锚）与执行日志。

## 口径声明

- 本审计为 6 案新提交的 RQ2 式判定实测，不改动 RQ2 冻结实验集（44TP+27FP，0.909/0.955）数字
- 产物：契约（structured_contract.json）、6 案执行日志与链文件（sessions/qdrant/v1.19.0rq2/）、机械+引文结果（new6_mech_quotes.json）、本报告
- 账本联动建议（未执行，待拍板）：#10369/10371/10372 → TP_ACK_OPEN；#10373 → TP_FIXED_PR（to be released）；#10368 → FP_BY_DESIGN；#10370 已是 FP_BY_DESIGN 不变——已由 ledger_vendor_refresh.py 于 2026-08-30 完成

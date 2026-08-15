# Phase 2 实验纪律（Experiment Discipline）

> 日期：2026-08-14。本文档是 Phase 2 dev-reviewer 判定实验的**强制操作纪律**，
> 每一条都对应一次已发生的踩坑（编号引用 docs/phase2-audit-report.md §1 的坑 1–10）
> 或审计发现。实验员（人或 agent 编排者）派发前必须逐条核对；违反任一红线 = 该次判定作废。

## 0. 适用范围

- 干净流程复跑及之后所有 Phase 2 dev-reviewer 判定实验。
- 材料包：`C:/Users/11428/Desktop/tvdb_sessions/`（v2，中性路径，匿名 did）。
- 实验侧数据（GT、映射）：`C:/Users/11428/Desktop/testvdb_paper/.paperpilot/phase2-rerun/`（**永不进材料树**）。
- 派发协议：`gen_dispatch_v2.py`（生成派发 prompt）；SOP：`testvdb4exp/agents/dev-reviewer.md`。

## 1. 实验总流程

```
1. 选 case 集（25 或 71，用户定）→ 从 cases_index.json 取 A/B/C 组
2. 起容器：每 (vendor, version) 一个容器，确认 healthy（§5）
3. 派发：逐 case 生成 v2 派发 prompt（§3），每个 reviewer 只判一个 case（§4）
4. 收判词：dev_review.json + .done；校验 JSON 合法 + source_excerpt 非空
5. 分析：判词 vs GT（cases_index.json），计算 recall/precision/κ
6. 归档：派发记录表 + 材料修复记录（§7）
```

**验证门槛**：任何一步失败（容器不 healthy、判词 JSON 坏、source_excerpt 空）→ 该 case 判词作废，换新 reviewer 会话重判，不得沿用原会话。

## 2. 材料纪律

1. **材料只读**：实验期间任何人（含编排 agent）不得手改 `tvdb_sessions/` 内任何文件。
2. **GT 隔离**：GT 标签、defect_id 映射、issue 号只存在于实验侧 `phase2-rerun/`；材料树中出现 issue 号/GT 线索 = 红线（坑 9/10 + 2026-08-14 深入审核新发现的 related_issue_numbers、symptom_pattern 逐字标题、log 裸号三类泄露）。
3. **修改走脚本**：材料修复必须通过构建/修复脚本（build_materials_v2.py、fill_raw_v2.py、fix_*.py）并追加 `MATERIAL_FIXES.json` 记录；禁止手工改材料后不留痕。
4. **修输入不修输出**：材料修正永远不改判词文件；历史判词（run/run2/run3 的 dev_review*.json）一个字不动。
5. **改后必审**：任何材料改动后跑 `audit_materials_v2.py`，0 FAIL 才允许继续实验。
6. **空日志例外**：milvus_001（2.3 无 REST v2）保留空日志是已知例外（audit-report §5.5）；其余任何空 output log = 材料缺陷，必须先补。

## 3. 派发纪律（核心红线）

### 3.1 派发 prompt 允许说（白名单，缺一不可）

- SOP 的路径与 6 步复述（干净复现 → 前提审计 → 契约对照 → 源码接地 → 反向证伪 → 平凡排除 → 三视角聚合）。
- 材料指针：`{SESSION_DIR}/debate_logs/stage2_aggregation.json`（只取 defect_id/endpoint/defect_type）、`intelligence/{target}/`、`structured_contract.json`、`api_templates.md`、`.srcdir`。
- 目标容器信息：vendor、版本、端口、可用客户端提示（curl/pymilvus/requests）。
- SOP 硬约束复述：Bash 实测禁止脑补、source_excerpt 非空、禁止读 probe `.py` 源码、禁止读已存在 dev_review*.json、禁止派孙 agent。
- 输出格式与汇报格式。

### 3.2 派发 prompt 禁止说（红线，违反即判词作废）

| # | 禁止 | 对应坑 |
|---|------|--------|
| 1 | 任何 case 级提示：endpoint 方向、缺陷路径、"该 case 在测 X" | 坑 7（重判 prompt 明示裁决方向） |
| 2 | 行为引导："不要因流量不符判 FP"、"上次判了 UNCERTAIN 无效"、"你漏了哪条路径，去测它" | 坑 7 + 审计报告 §2(b) 探索引导 |
| 3 | 任何历史判词/裁决方向/期望结果 | 坑 7 |
| 4 | 实验元话语：rerun、重审、重判、实验、run2、phase2、curated、clean run、排雷、修正、"无污染" | 坑 8 |
| 5 | issue 号或任何可查 GT 的编号（related_issue_numbers、dup 链） | 坑 10 + 深入审核 |
| 6 | "日志为空"的特殊处理提示（提示了 = 告诉 agent 材料异常，等于行为引导） | 坑 4/7 |
| 7 | 提示 agent 去 WebFetch github.com 查 issue（SOP 自身允许 github.com 回退，但 prompt 不得主动引导） | 坑 10 |
| 8 | 对某 case 的"聪明提醒"（如"这个 case 记得看 XX 参数"）——任何超越 SOP 复述的 case 级信息 | 坑 7 |

**一句话**：派发 prompt = SOP 复述 + 材料指针 + 容器信息，**零 case 级信息、零引导、零历史**。

### 3.3 派发前检查

- 用 `gen_dispatch_v2.py` 生成，不手写。
- 生成后跑泄漏词扫描（rerun/实验/重审/修正/run2/phase2/curated/issue 号等）→ 0 命中才派发。
- 派发记录的 case 不得与任何历史 reviewer 会话重合（§4）。

## 4. 独立性纪律（1 reviewer = 1 issue = 1 verdict）

1. **严格禁止一个 dev-reviewer 判同一 issue 两次**。定义：同一 reviewer 会话（含其上下文历史）对同一 case 的任何第二次判定，无论"连续"与否、无论跨 run，一律禁止。理由：第一次判词留在会话上下文里，第二次必然被自己的历史结论锚定（run2+run3 中 2.6.19/2.3/2.6.10 等版本由同一 agent 连审两 run 同 case，独立性破坏）。
2. **每 case 每次判定 = 新干净会话**：reviewer 无任何该 case 的历史上下文。
3. **同一 case 需重判**（如材料修正后）→ 新会话 + 新派发，禁提旧判定（§3.2 第 3 条）。
4. **同一 batch 的 case 数受限**：多 case 一会话导致后面 case 草率（坑 5，run3 2.6.16 batch2 空 source_excerpt 实证）。默认一个 reviewer 会话判一个 case；确需 batch 时 ≤ 3 case 且必须同 vendor 同版本。
5. **判词隔离**：reviewer 双盲（SOP）：不读 probe `.py`、不读任何已存在的 dev_review*.json、不读 stage2 的 rationale/vote。
6. **派发记录表**（§7）：每 case 记录 reviewer 会话 ID；派发前查表，同 case 已判过 → 拒绝新派发给同会话。

## 5. 环境纪律

1. **容器与版本一一对应**：每 (vendor, version) 一个容器；不同版本不同容器。
2. **顺序 batch，禁止并发打同一容器**（坑 2：milvus 3.0.0 容器争用 → 10 case 全判 FP）。
3. 派发前 `healthz`/健康检查确认 healthy；不 healthy → 重启容器再派发。
4. 挂起风险请求（如 INT_MAX shard create）实测后立即 `docker rm -f` 容器并检查磁盘余量。
5. 实验结束清理全部容器。

## 6. 修复纪律（Fix vs Re-judge）

1. **修材料 ≠ 重判**：材料修正（endpoint 标签、raw 补齐、匿名化）落地后，历史判词保留不动；受影响 case 只在**新的干净流程**里自然重判。
2. **禁止"提示式重判"**：任何"告诉 agent 上次判了什么/材料改了什么方向"的重判都是污染（坑 7），该次判定作废。
3. 所有材料修复必须留痕：`MATERIAL_FIXES.json` 记录（类型/对象/旧值/新值/影响范围）。

## 7. 记录与审计

1. **派发记录表**（每次 run 一份）：case did / vendor / version / reviewer 会话 ID / batch / 派发时间 / 判词文件路径。
2. **判词校验**：JSON 合法 + `source_grounding.source_excerpt` 非空 + `files_examined` 非空；否则作废重判。
3. **违规审计**：每 run 结束后核查派发 prompt 是否含 §3.2 红线词、reviewer 会话是否违反 §4 独立性。
4. **材料审计**：每 run 结束后跑 `audit_materials_v2.py`，0 FAIL 才可进入分析。

## 8. 违规处置

- 任何一条红线违反 → 该 case 判词作废，作废记录进入派发记录表。
- 作废后重判：新 reviewer 会话 + 重新生成的干净派发 prompt。
- 连续两次违反同一条红线 → 停止实验，复盘后再继续。

## 9. 态度锚点三条件（intel 修改准绳，2026-08-15 fixA/fixB 实验固化）

向 `developer_cognition` 注入裁决准绳型锚点必须**同时满足**三条，缺一不可：
1. **≥2 个独立维护者公开行为支撑**（fix PR/ACK，非依赖单一 case 的标签）；
2. **与既有锚点无方向冲突**（同一现象类的两个 GT 方向相反时，锚点集合在数学上不可全翻正——B 类灰区禁止硬补）；
3. **普适于现象类而非单 case**（措辞不得指向具体字段/端点）。

实证：fixA（通道一致性锚点）10 翻正 : 3 劣化 → 采纳；fixB（系统内不对称锚点）1 翻正 : 2 劣化
（对照组 50319/50352 被卷翻）→ 回滚。锚点越宽泛，"默认值回退/loading 语义"类 by-design 现象被
误卷入 CONFIRMED 的风险越高。违反三条件 = 坑 9（考题在复习资料里）复活。

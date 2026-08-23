# 待办 2 完成报告：71 case probe↔issue↔stage2 三方比对

> 日期：2026-08-14。方法：4 个并行审计 agent（milvus×2/qdrant/weaviate）对 71 个 scored case
> 逐一比对三方——探针脚本实际操作（`.paperpilot/phase2/probes/`）、issue 声称缺陷
> （`phase1-raw/manifest.json` title+body）、stage2 候选标签
> （`run/results/{vendor}/{ver}/{num}/debate_logs/stage2_aggregation.json`）。
> 输入材料在 `.paperpilot/phase2-rerun/probe_issue_audit/`（inputs/*.md + 4 份 JSON 结论）。
> 所有 agent 结论经主会话独立复核（重读探针 API 调用行 + stage2 原文逐一核对）后才采信。

## 1. 结论先行

- **probe↔issue 实质错配：0 个。** 71 个探针实测的缺陷操作全部与 issue 声称缺陷一致
  （审计报告 §1 坑 7 时代提及的 3 个旧错配——50355/9373/49928——当前文件均已对齐：
  50355 探针已改测 autoID upsert、49928 已改测 dim 上限、9373 探针本就用 filtered scroll）。
- **stage2 标签错配：19 个**（18 endpoint + 1 defect_type），全部已修正落地（见 §3）。
  其中 5 个正是排雷阶段"KEEP_LABEL_TRAFFIC_DEFECT"决定保留的——排雷时的人工判断有盲区
  （只对着判词看标签是否误导了裁决，没有回到 issue 原文核对标签与缺陷操作的对应）。
- 审计报告旧结论"50355（探针测 color 字段，issue 是 autoID upsert）"**已过时**：
  该错配在排雷阶段已修（MATERIAL_FIXES: entities+insert→entities+upsert），当前探针正确。

## 2. 19 个错配清单（比对结论 + 修正）

| case | 组 | 字段 | 旧值（错） | 新值 | 缺陷操作（issue 声称） |
|---|---|---|---|---|---|
| milvus_47767 | C | endpoint | databases+drop | entities+search | search 空查询向量无校验 |
| milvus_49059 | B | defect_type | crash | behavior | COSINE 同向量 distance>1.0（精度溢出，非崩溃） |
| milvus_49823 | B | endpoint | entities+insert | entities+search | search 接受 nprobe=0 |
| milvus_49843 | A | endpoint | collections+alter | collections+create | create 静默丢弃负 TTL（alter 是正确拒绝的对照） |
| milvus_49844 | C | endpoint | entities+insert | entities+query | query 接受 null/缺失 filter |
| milvus_49889 | B | endpoint | collections+create | collections+list | list/describe 接受空串 dbName（排雷 KEEP，被推翻） |
| milvus_49890 | A | endpoint | entities+insert | collections+list | Request-Timeout 非整数 header 被接受（载体是 list） |
| milvus_49929 | C | endpoint | entities+insert | indexes+create | REST/SDK create_index 默认行为不一致（排雷 KEEP，被推翻） |
| milvus_49930 | B | endpoint | collections+create | entities+search | search 接受非法 searchParams（ef=0/-1 等） |
| milvus_50193 | C | endpoint | collections+load | collections+get_stats | get_stats 返回 rowCount=0（load 只是前置） |
| milvus_50194 | C | endpoint | entities+insert | entities+search | 并发 delete+search 返回 stale 数据（暴露在 search） |
| milvus_50323 | B | endpoint | entities+insert | entities+delete | delete 同时给 filter+ids 无校验 |
| milvus_50325 | C | endpoint | collections+list | collections+create | 下划线开头命名被接受（排雷 KEEP，被推翻） |
| milvus_51085 | A | endpoint | entities+insert | collections+create | create 静默替换非法 vectorFieldType（排雷 KEEP，被推翻） |
| milvus_52309 | A | endpoint | entities+insert | entities+search | search 接受 group_size=0/-1 |
| milvus_52312 | B | endpoint | entities+insert | entities+upsert | upsert 字符串 PK 强转覆盖 |
| qdrant_9373 | C | endpoint | collections+{collection_name}+points+count | collections+{collection_name}+points+scroll | keyword 索引过滤查询严重不全（探针用 filtered scroll 验证；排雷 KEEP，被推翻） |
| weaviate_11399 | A | endpoint | GET /schema | POST /schema | 创建时接受 dynamicEfMin>Max（GET 只是读取验证） |
| weaviate_11400 | A | endpoint | GET /schema | POST /schema | 创建时接受负 flatSearchCutoff |

## 3. 修复落地

- 脚本 `fix_stage2_labels_v2.py`（幂等：old 不匹配即跳过）。
- 写入位置：三棵判定树 `run|run2|run3/results/.../stage2_aggregation.json` +
  **v2 材料包** `C:/Users/11428/Desktop/tvdb_sessions/sessions/...`（经 defect_id_map 反查匿名 did）。
- 全部 19×4=76 处 ALL-OK，已抽查验证（三树 + v2 包新值正确）。
- MATERIAL_FIXES.json 追加 19 条记录（25→44）。

## 4. 根因：为什么排雷没清干净

排雷（fix_materials）修正 endpoint 标签的方式是**对着 run1 判词**看"哪个标签误导了裁决"，
而不是对着 **issue 原文**核对"标签是否等于缺陷操作"。两种方式漏掉的错误不同：

- 对着判词修：漏掉"标签错但没误导裁决"的 case（agent 碰巧把 insert 标签理解成别的路径照样判对）。
- 5 个 KEEP 决策尤其典型：排雷时人工判断"流量主操作=缺陷操作"——但 fill_endpoints 抽取的
  "主操作"往往是探针 setup 序列里最频繁的操作（insert/create），不是缺陷暴露的操作。

本次三方比对把核对基准换成了 issue 原文，因此能挖出残余 19 处。

## 5. 影响与后续

- **对历史判词（run1/run2/run3 的 dev_review.json）**：修正不改判词文件本身，但 19 个 case 的
  判定输入（候选标签）已变。其中 A 组 6 个（49843/49890/51085/52309/11399/11400）与 B/C 组 13 个。
  与排雷时口径一致：材料修正 + 判词保留，是否重判由干净流程 v2（tvdb_sessions 包 + 干净协议）
  统一决定——本次不重判。
- **审计报告 §1 坑 7 的旧描述需更新**：50355 的"探针测 color 字段"错配在排雷已修，
  该条目只保留历史记录意义。

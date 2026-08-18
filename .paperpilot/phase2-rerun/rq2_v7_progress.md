# RQ2 v7 完整复测进度（2026-08-18 晚起跑）

## 协议要点（自任务书 + V4_RULES 继承）
- 派发一律 gen_dispatch_v7.py 生成（原生 agent 任务参数 only；claim 锚程序化注入）
- **教训（已踩）**：上轮手写 006/007 anchor 造成污染（写成 Strong/串nprobe），已用生成器版本重跑修复。以后 Agent prompt 必须逐字粘贴生成器输出。
- builder 产物：{sess}/{did}/evidence_chain/{did}.json + .done（覆盖 v3）
- auditor 产物：{version组}/debate_logs/chain_verdicts_v7.json + .done
- rework：rq2_v7_rework_state.json 计数，同 did ≤3 轮，超限保守 NOT_DEFECT；CONFLICT 必走闭环
- GT 对照只在全部 verdict 出完后做（cases_index.json gt_label）

## 组状态
| # | 组 | case 数 | builder | auditor | rework |
|---|-----|--------|---------|---------|--------|
| 1 | milvus/2.3 | 1 | ✅ 001（空log如实 grade D+by_design） | ⬜ | - |
| 2 | milvus/2.6.10 | 6 | ✅ 002-007（006/007 污染重跑修复：006 aligned B；007 drifted 属实 REST通道1801 vs pymilvus通道65535） | ⬜ | - |
| 3 | milvus/2.6.12 | 1 | ⬜ | ⬜ | - |
| 4 | milvus/2.6.16 | 12 | ⬜ | ⬜ | - |
| 5 | milvus/2.6.17 | 11 | ⬜ | ⬜ | - |
| 6 | milvus/2.6.19 | 2 | ⬜ | ⬜ | - |
| 7 | milvus/3.0.0 | 10 | ⬜ | ⬜ | - |
| 8 | qdrant/1.12.1 | 1 | ⬜ | ⬜ | - |
| 9 | qdrant/1.18.0 | 3 | ⬜ | ⬜ | - |
| 10 | qdrant/1.18.1 | 2 | ⬜ | ⬜ | - |
| 11 | qdrant/1.18.2 | 12 | ⬜ | ⬜ | - |
| 12 | qdrant/1.18.3 | 1 | ⬜ | ⬜ | - |
| 13 | weaviate/1.37.4 | 4 | ⬜ | ⬜ | - |
| 14 | weaviate/1.38.0 | 4 | ⬜ | ⬜ | - |
| 15 | weaviate/1.38.2 | 2 | ⬜ | ⬜ | - |

## 环境备忘
- minio 容器曾 Exited(255) 未被 ensure_milvus_infra 重建（只查 docker ps 列表不查状态）→ milvus panic。已手动重建，脚本切版本时留意。
- auditor 批上限 12：组 4/5/7/11 需分两批。
- did 列表以 defect_id_map.json 为准（勿凭记忆）。

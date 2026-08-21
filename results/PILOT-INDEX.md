# RQ1 Pilot 存档索引（两轮对照）

> 2026-08-20~21。两轮 pilot 的目的不同：**第一轮**验证三机制（retry/GT_HINT/novelty gate）真实工作 + 软门 reach≥1；**rerun**（同版本重跑）验证三个根因修复（契约覆盖率/分桶/param 链）的端到端效果。两轮数据都是论文 RQ1 的过程证据。

## 目录结构

```
results/
├── PILOT-INDEX.md                    ← 本文件
├── rq1-pilot/                        ← 第一轮（机制验证，2026-08-20 06:28Z）
│   ├── observation_retry.md          ← retry 子循环观察数据（4 轮 38坏/16修）
│   └── qdrant-v1.18.2/
│       ├── structured_contract_10endpoints_original.json  ← ⚠️ root cause 证据：10 端点契约原貌
│       ├── raw_knowledge_original_selfreport100.md        ← ⚠️ root cause 证据：自报 100%(70/70) 原貌
│       └── 2026-08-20T06-28-05Z/     ← 会话全量（273 项：41链/26DEFECT/12NOVEL/6issues/7MRE）
└── rq1-pilot-rerun/                  ← 第二轮（修复效果验证，2026-08-20 15:41Z）
    └── qdrant-v1.18.2/
        ├── structured_contract.json  ← 76 端点契约（spec 回填后，55 带参数）
        ├── raw_knowledge.md          ← 97.3% 机械核对版
        ├── doc_coverage_report.json  ← 机械覆盖率报告（12% 自报纠偏证据）
        └── 2026-08-20T15-41-03Z/     ← 会话全量（17链/15DEFECT/2NOVEL/2COVERED_BY_PR归档/2MRE/defect-review）
```

## 两轮对照（论文可用数字）

| 维度 | pilot 1 (06-28-05Z) | rerun (15-41-03Z) | 变化来源 |
|---|---|---|---|
| 轮次 | 4（R5 提前收口） | 3 | — |
| 契约端点 | 10 | 76 | fetch_openapi_spec + Step 4.5 |
| doc_coverage | 自报 100%(70/70)，实 12%(9/75) | 97.3%(73/75) 机械核对 | validate 机械覆写 |
| chunking units | 20（constraints 0 进块） | 42（constraints 19 全进） | chunk_contract 三桶修复 |
| vein meta param | 0/7 | 全带 | attack-vein.md 内联模板 |
| 证据链 | 41（26 DEFECT/15 NOT_DEFECT） | 17（15 DEFECT/2 NOT_DEFECT） | — |
| novelty gate | 12 NOVEL/0 已报告/9 UNVERIFIED | 2 NOVEL/2 COVERED_BY_PR(PR#1463)/11 UNVERIFIED | param fallback 修复 |
| archived 分支 | 未触发（0 NON_NOVEL） | ✅ 首次走通（2 条，manifest 含 PR#1463） | — |
| **GT reach** | **1/4**（hnsw_ef） | **4/4 all_reached** | 契约扩容+param 匹配粒度修复 |

## GT 4/4 命中明细（rerun）

| bug | param | 命中链 | 轮次 |
|---|---|---|---|
| qdrant_9017 | hnsw_ef | vein_params_hnsw_ef_zero_points_search_1 | R3 |
| qdrant_9421 | recover | vein_cluster_standalone_1（standalone 500 现象复现） | R2 |
| qdrant_9520 | shard_number | vein_replication_gt_shards_collections_create_1 | R3 |
| qdrant_9522 | lookup_from | vein_lookup_from_points_query_1 | R2 |

## 修复链（全量 15 版本依赖的修复，均已 push 双仓库）

| commit | 仓库 | 内容 |
|---|---|---|
| 901189f / e9b7258 | 4exp+主插件 | chunk_contract 三桶归一化 |
| f9cb621 | 4exp+主插件(部分) | verdicts 缺 param 的 meta fallback |
| 215e4a9 / 30f9c6b | 4exp+主插件 | 契约覆盖率根因（spec 预取/机械核对/反编造红线/cluster 排除） |
| 0a655dc | 4exp only | injector 匹配粒度（实验特化） |
| 4474fcd / 9dee3a0 | 4exp+主插件 | enrich_contract_from_spec 机制化 + reporter 落盘自验证 |

## 已知过程事件（论文 limitations / 复现者须知）

1. pilot 1 的 retry 数据、agent 虚报案例、环境坑全在 `rq1-pilot/observation_retry.md` 与 `docs/rq1-pilot-observation.md`
2. rerun 中途容器内存 2G 打满（R1 资源极限脚本）→ 重启 + 33 脚本健康重跑；全量 SOP 已加 C10 内存监控
3. rerun 的 extractor 3×HTTP 400 走 Task 4a 降级（复用旧 knowledge + spec 机械补全）——glm proxy 环境已知
4. 11 UNVERIFIED：GitHub token 限流下 gate 查重不全，novelty 数字为保守下界

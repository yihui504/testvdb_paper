# Phase 2 系统重做实验规划：dev-reviewer 级别 1:1 对齐判定

> 起始：2026-08-14。背景：原 Phase 2 confirmation 用精简 prompt（一行 contract_hint + 概括观察），缺 dev-reviewer 该有的源码/完整契约/维护者认知，导致 κ 失效。本计划按 dev-reviewer 实际输入重做，1:1 对齐。
> 关联：`docs/phase3-progress.md`（整体进度）、`docs/phase2-rq2-draft.md`（原 RQ2 文稿）。

## ✅ 准备阶段完成（2026-08-14，等用户"开始"才进实验）

所有实验前准备就绪，**未起任何容器**。产物在 `.paperpilot/phase2-rerun/`：

| 项 | 状态 | 说明 |
|----|------|------|
| Phase 1.1 源码 clone | ✅ 16/16 | `~/Desktop/vdb_src/{vendor}/{tag}`，~1.4GB，ALL DONE |
| Phase 1.2 镜像 | ✅ 16+infra | `docker image inspect` 全部 missing=0（无需 pull） |
| Phase 1.3 raw 捕获 | ✅ | `probe_common.py` 加 `_raw_path/_raw_write/record_raw` + http() raw 日志，RAW_LOG_DIR 未设时行为不变 |
| Phase 1.4 intel | ✅ 3 vendor | `intel/{milvus,qdrant,weaviate}/{developer_cognition,bug_shapes}.json` |
| Phase 0.1 判词 | ✅ | `judge_prompt.md`（静态 dev-reviewer SOP，GLM+DeepSeek 共用，含静态限制披露） |
| Phase 2.1 契约段 | ✅ 71 | `contracts/segments/`，54 assertion 级匹配 + 17 真实契约缺口（nprobe/ef/gRPC-REST 等） |
| Phase 2.2 api_template | ✅ | per-case endpoint 切片（嵌入 segment） |
| Phase 3.2 源码片段 | ✅ 71 | `source_excerpts/`，70 found + 1 not_found（qdrant_9027，title 是 slug） |
| Phase 3.1p 包骨架 | ✅ 71 | `packets/{vendor}_{num}.md`+`.json`，7 字段（raw 占位） |

**71 case 锁定**（cases_index.json，带 group/gt_label）：A 28 + B 17 + C 26 = 71 scored；CONFIRMED 45 / FALSE_POSITIVE 26；milvus 43 / qdrant 18 / weaviate 10。defect_type：param_validation 27、behavior 21、type_coercion 8、semantics 10、crash 3、doc_mismatch 2。

**实验阶段（等"开始"）**：起容器（orchestrate.py）→ 跑 71 probe 抓 raw（probe_common 写 `raw_{vendor}_{num}.log`，SDK 探针补 record_raw）→ 填包 raw 字段 → GLM-5.2 + DeepSeek 双盲判（judge_prompt.md）→ inter-model κ + metrics。

## 目标与"1:1 对齐"定义

每个待判样本造一份**静态判定包**，含 dev-reviewer 实际接收的全部信息。GLM（用 dev-reviewer 提示词静态版）和人工裁判看**同一份包**，盲判（无 GT、无旧判定、无模型 rationale）。

- **为什么静态包而非自主 agent**：dev-reviewer agent 自主 Grep 源码、动态探索，无法保证两裁判看到同样东西；静态包**预定位源码片段**，确保 1:1 + 可复现。源码 clone 同时作为"标准环境"挂载，供裁判需要时下钻（两边都能访问同一 clone，环境对齐）。
- **判定仍双盲**：包内不含 attack 脚本断言、不含其他 judge 产出、不含 GT。

## 范围

- **判定集**：71 条 scored（A∪B∪C = 28+17+26）为主——recall/precision/FP-supp 只依赖这个；D 组 53 条可选（triage，不计主指标）。
- **版本**：16 个 (target,version)：milvus {2.3, 2.6.10, 2.6.12, 2.6.16, 2.6.17, 2.6.19, 3.0.0}（7）、qdrant {1.12.1, 1.17.1, 1.18.0, 1.18.1, 1.18.2, 1.18.3}（6）、weaviate {1.37.4, 1.38.0, 1.38.2}（3）。

## 信息标准（每包对齐 `agents/dev-reviewer.md` 的输入）

| # | 项 | 来源 |
|---|---|---|
| 1 | raw HTTP 请求+响应 | 重跑 probe（改造 probe_common 抓 raw） |
| 2 | 完整契约相关段 structured_contract | 生成/抽取（Phase 2 原无） |
| 3 | developer_cognition.json | **复用** mftui/TestVDB/intelligence/{target}/ |
| 4 | bug_shapes.json | **复用** 同上 |
| 5 | api_templates.md | 从契约/OpenAPI 生成（Phase 2 原无） |
| 6 | 源码片段 | clone 对应 tag + Grep 定位断言/校验 |
| 7 | candidate 元数据 | id/endpoint/defect_type（无 judge rationale） |

## 分阶段计划（先 1 vendor 跑通，再扩）

### Phase 0 — 锁范围 + 决策（已敲定 2026-08-14）
- [x] 判定集 71 / 静态包+源码挂载 / clone 到桌面 / 手工抽 dev-reviewer 可见契约段 / GLM-5.2+DeepSeek 双判 / 直接全量（见"待定决策"段）
- [ ] 0.1 写 GLM/DeepSeek 共用的 **dev-reviewer 静态判词**（基于 `agents/dev-reviewer.md` SOP，改成读静态包；保留双盲约束：不看 attack 脚本断言/其他 judge 产出/GT）→ verify：判词文档就位，两模型可同一份调用

### Phase 1 — 基础设施
- [ ] 1.1 源码 clone：16 (target,version) shallow → `.paperpilot/phase2-rerun/src/{target}/{version}/`（milvus 2.3 旧 tag 特殊处理）→ verify：`git -C ... describe --tags` 匹配
- [ ] 1.2 Docker **镜像拉取**（准备期只 pull 不 run）：复用 `orchestrate.py` 的 IMAGE 映射，`docker pull` 16 个版本镜像（milvusdb/milvus、qdrant/qdrant、semitechnologies/weaviate 各 tag）→ verify：`docker images` 列出全部 16 tag；**不 `docker run`**（run 属实验阶段）
- [ ] 1.3 raw 捕获改造：`probe_common.http()` 增写 raw log（method/url/payload + status/headers/body 全量 → `raw_{target}_{num}.log`）→ verify：一条 probe 产出完整 req+resp
- [ ] 1.4 复用迁移：复制 intelligence/{target}/{developer_cognition,bug_shapes}.json → `phase2-rerun/intel/` → verify：3 vendor 就位

### Phase 2 — 每版本契约 + 模板
- [ ] 2.1 structured_contract per (target,version)：手工抽每 case 相关契约段（endpoint/param 文档原文）。**只抽 dev-reviewer 实际会读的相关段**——不扩到全契约、不加额外上下文（对齐 dev-reviewer 的 verified_only 可见范围）→ verify：16 份，每 case 的 endpoint/param 有对应契约段
- [ ] 2.2 api_templates per (target,version)：从契约/OpenAPI 生成请求语法 → verify：每 case 请求能按模板重建

### Phase 3 — 逐样本包组装（71 包）
- [ ] 3.1 raw 重跑 **（实验阶段，等"开始"）**：71 条 probe 在对应版本 Docker 跑 → `raw_{target}_{num}.log` → verify：71 份非空
- [ ] 3.1p（准备期）包骨架：用 probe spec 的请求 payload + 现有 emit 日志的观察，先组装 6/7 字段（raw 字段占位）→ verify：71 包骨架就绪，仅 raw 待补
- [ ] 3.2 源码片段定位：每 case Grep 断言/校验逻辑 → 20-50 行上下文 → verify：71 份 source_excerpt（含相关代码或"未找到"标注）
- [ ] 3.3 组装：`packets/{vendor}_{num}.md` = raw req/resp + 契约段 + 源码片段 + cognition（相关条目）+ bug_shapes（相关根因）+ api_template + 元数据 → verify：71 包 × 7 项齐；盲

### Phase 4/5 — 跑真 dev-reviewer 判 71 样本（实验阶段，等"开始"）
**最简方案见 [`docs/phase2-rerun-experiment.md`](phase2-rerun-experiment.md)。** 把样本还原成 dev-reviewer 真读的文件布局，派 `Agent(subagent_type="testvdb:dev-reviewer")`：
- [ ] 准备：摆文件进 `results/{target}/{version}/` + `intelligence/{target}/` + 写 `.srcdir` + 生成 `api_templates.md` + `stage2_aggregation.json`（候选=样本，无 GT）—— 一个 `layout_inputs.py`
- [ ] 实验：按版本 起容器→跑探针出 `output_*.log`→派 dev-reviewer（容器常驻）→ `dev_review.json`
- [ ] 收集：verdict vs GT → recall/precision/FP-supp + 对比旧 oracle；DeepSeek 到位后加 inter-model κ
- [ ] 论文 validity 段 + 重做结论
- ⚠️ 之前的 `packets/*.md`、`judge_prompt.md`、`run_dev_reviewer.py`、`fill_packet_raw.py` **全部废弃**——dev-reviewer 自己读真实文件，不自定义判官。契约段/intel/clone 复用进布局，prep 不浪费。

## 先跑通 1 vendor（pilot，强烈建议）

**weaviate 3 版本 / ~30 条** 端到端先做一遍 → 验证包质量 + 判定流程 + κ 是否回升 → 再扩 milvus/qdrant。避免在 16 版本 infra 上踩坑后返工。

## 工作量与风险（诚实）

- **重活**：源码 clone（磁盘+时间）、71 probe 重跑（Docker 跨 16 版本）、71 源码片段逐条定位、契约生成。
- **已省**：cognition/bug_shapes 搬现成。
- **风险**：milvus 2.3 旧 tag 兼容；部分 case 源码断言跨多文件难定位；raw 重跑个别 case 可能因环境差异不复现（记为"未复现"，入包如实）。
- **估计**：专注 ~1-2 周（clone + 重跑是大头）；pilot 2-3 天。

## 准备 vs 实验边界（用户 2026-08-14 明确要求）

**准备阶段（现在做，做完即停，不擅自进实验）**：
- 源码 clone（16 tag shallow → 桌面）、Docker **镜像拉取**（pull，不 run）、raw 捕获代码改造、搬 cognition/bug_shapes、手工抽契约段、生成 api_templates、Grep 定位源码片段、组装**包骨架**（7 项里除 raw req/resp 外全填好；raw 字段留占位，等容器跑）。

**实验阶段（等用户说"开始"才动，一步一步做）**：
- 起容器 → 跑 71 probe 抓 raw 请求/响应 → 填包的 raw 字段 → GLM-5.2 + DeepSeek 双盲判 → 分析。

> raw req/resp 必须跑容器才能拿，所以它在实验阶段；其余全部准备期可就绪。包骨架 6/7 先填，raw 最后补。

## 待定决策（开工前）—— 已全部敲定（2026-08-14）

1. **判定集**：71 scored ✅
2. **包形式**：静态包 + 源码挂载 ✅（保证 1:1）
3. **源码 clone 磁盘**：✅ 可接受，**克隆到桌面**
4. **契约**：✅ 手工抽每 case 相关契约段，**只做 dev-reviewer 可见的部分**（只抽 dev-reviewer 实际会读的相关段，不扩到全契约或额外上下文）
5. **裁判**：用户不做人工判 → **用 DeepSeek 跑实验**（与 GLM-5.2 双模型盲判，inter-model κ；注意：两 LLM 可能有共享偏置，κ 弱于人工 inter-rater，论文如实写）
6. **范围**：✅ 直接全量（不 pilot）

## 决策日志
- 2026-08-14：用户拍板 B（全量 dev-reviewer 级 1:1 对齐）。
- 2026-08-14：6 项决策全部敲定（见上）。关键变化：①裁判=GLM-5.2+DeepSeek（非人工）②契约只抽 dev-reviewer 可见段 ③直接全量不 pilot ④准备/实验边界明确——做完所有准备（含拉镜像，不起容器）即停，等"开始"。

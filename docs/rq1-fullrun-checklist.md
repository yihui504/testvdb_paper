# RQ1 检测能力实验 · 15 版本全量 Checklist

> 创建 2026-08-21。前置条件全部满足（pilot 两轮验证 + 修复链落盘），从本清单开始逐版本执行。
> 实验纪律见 `docs/phase3-plan.md` §实验流程；pilot 踩坑防预清单见 `docs/rq1-pilot-observation.md`。

## 执行顺序（每版本一个 checkbox，跑完勾选 + 填数字）

| # | target | version | GT bugs | 状态 | reach | DEFECT/链 | NOVEL | 备注 |
|---|---|---|---|---|---|---|---|---|
| 1 | qdrant | v1.18.0 | 2 (9039, 9045⚠️) | [ ] | /2 | / | / | 9045=standalone-unreachable，分母单独分析 |
| 2 | qdrant | v1.18.2 | 4 (9017,9421,9520,9522) | [x] pilot rerun 已跑 | 4/4 | 15/17 | 2 | **不计入全量**（pilot 软门验证轮）；若算作首版本需确认口径 |
| 3 | qdrant | v1.19.0 | 1 (10120) | [ ] | /1 | / | / | |
| 4 | weaviate | v1.37.4 | 3 (11399,11400,11401) | [ ] | /3 | / | / | weaviate 首跑：GitHub tag spec 规则验证 |
| 5 | weaviate | v1.38.0 | 3 (11730,11732,11741) | [ ] | /3 | / | / | |
| 6 | weaviate | v1.38.1 | 1 (11729) | [ ] | /1 | / | / | |
| 7 | weaviate | v1.38.2 | 1 (12041) | [ ] | /1 | / | / | |
| 8 | milvus | v2.3.22 | 1 (47635) | [ ] | /1 | / | / | milvus 首跑：fetch 无规则（exit 3 不阻塞） |
| 9 | milvus | v2.6.10 | 5 (47729,47752,47755,47763,47766) | [ ] | /5 | / | / | |
| 10 | milvus | v2.6.12 | 1 (49059) | [ ] | /1 | / | / | |
| 11 | milvus | v2.6.16 | 4 (49823,49889,49930,50018) | [ ] | /1→4 | / | / | |
| 12 | milvus | v2.6.17 | 4 (49890,50323,50353,50354) | [ ] | /4 | / | / | 47635 race 同版复用 phase2 结论 |
| 13 | milvus | v2.6.18 | 2 (49843,50355) | [ ] | /2 | / | / | 50355=doc-fix 型 |
| 14 | milvus | v2.6.19 | 2 (51084,51085) | [ ] | /2 | / | / | |
| 15 | milvus | v3.0.0 | 10 (52307-52315,52325) | [ ] | /10 | / | / | 最大单版本；预留双倍时长 |

**顺序原则**：qdrant（管线已验证）→ weaviate（验证 GitHub tag spec 路径）→ milvus（无 spec 规则，走 extractor 原生路径 + Step 4.5 降级警告）。首跑每家先 1 个版本稳定再继续。

## 单版本 SOP（每版本逐步勾选）

### A. 前置（每版本 ~10 min）
- [ ] A1 `gt.json` 拷入：`cp .paperpilot/phase3/gt/{t}/{v}/gt.json {CACHE}/results/{t}/{v}/gt.json`
- [ ] A2 清旧缓存（跨版本禁缓存 #8）：删 `{CACHE}/results/{t}/{v}/` 下 structured_contract.json / raw_knowledge.md / doc_coverage_report.json / 各 session 目录
- [ ] A3 spec 预取：`py -3 scripts/fetch_openapi_spec.py {t} {v}`（milvus exit 3 = 无规则，记录后继续）
- [ ] A4 容器起：`{T}_VERSION={v} docker compose -f docker/{t}.yml up -d --wait`（image tag 格式见 preflight 注：qdrant/milvus 带 v，weaviate 不带）
- [ ] A5 镜像版本核验：`curl /` 或 version 端点确认运行版本 == 目标版本

### B. 知识与契约（Step 4-6）
- [ ] B1 派 extractor（绝对路径派发词 + 版本锚定）
- [ ] B2 覆盖率机械核对：`py -3 scripts/validate_doc_coverage.py {t} {v}` → doc_coverage_report.json 落盘；**记录 pct**
- [ ] B3 pct < 60% → 先把 missing_endpoints 喂 extractor 补爬一轮再核对（阈值拍板见下）
- [ ] B4 派 formalizer（骨架条目只登记不提参数）
- [ ] B5 Step 5.5 机械回填：`py -3 scripts/enrich_contract_from_spec.py results/{t}/{v} --fill-missing-fields`
- [ ] B6 passport 验证（enrich 已含重签，直接 verify 确认 PASS）
- [ ] B7 门控：CRUD 端点齐全；**GT 参数面抽查**——gt.json 每个 param 在契约 json 里 grep 一遍，记录 X/Y 进契约（reach 理论上限；异常低 → 回 B3 补契约再放行）

### C. 挖掘轮次（Step 8 循环，每轮）
- [ ] C1 GT_HINT 注入文本采集（盲注契约：四 agent 同文本，记录 x/y 计数轨迹）
- [ ] C2 派 4 attack agents（绝对路径 + export TESTVDB_DB_URL + 清同名集合 + meta param 必填）
- [ ] C3 Stage 1 四项验证（py_compile / risky / api_format / neutrality）
- [ ] C4 executor（⛔ 派发词必带 export 指令）
- [ ] C5 retry 分类器 + feedback 派修（记录 坏/regen/修好/超限）
- [ ] C6 候选提取 + L1（REFUTED 从 candidates.jsonl 移除）
- [ ] C7 builder fan-out（≤12/批，>12 分批）
- [ ] C8 auditor（≤12/批；NME>0 → 补证轮 ≤1 次）
- [ ] C9 轮收口：pipeline_state 推进 + GT_HINT 计数核对（应递增或持平，**倒退=异常即停**）
- [ ] C10 **容器内存监控**（pilot 教训）：`docker stats --no-stream`，>1.6G/2G → `docker restart` 后本轮脚本健康重跑
- [ ] C11 终止判定：GT_HINT all_reached（x==y）→ 收口；否则满 4-6 轮（GT 密集版本可到 8）收口

### D. 收口（Step 9-10）
- [ ] D1 novelty gate + 结果记录（NOVEL/COVERED_BY_PR/UNVERIFIED/BY_DESIGN 分布）
- [ ] D2 NON_NOVEL/COVERED_BY_PR → archived/ 归档 + manifest（related_issue_numbers 是论文"发现已被报告 bug"列数据源）；**首个版本出归档项时人工验证 manifest**
- [ ] D3 派 reporter（含 summary.md SUMMARY-OK 实测）+ reporter-mre
- [ ] D4 defect-review（verify_defects.py）
- [ ] D5 容器清理 `docker compose down -v`
- [ ] D6 归档到论文仓：`results/rq1-fullrun/{t}-{v}/{timestamp}/` + 契约/raw_knowledge/doc_coverage_report 副本
- [ ] D7 checklist 表行填数（reach / 链 / NOVEL）

## 中止条款（异常即停，人工判后继续）
1. GT_HINT 计数倒退或跨轮不单调
2. auditor summary 与条目计数不一致（pilot 出过 2 次）
3. agent 虚报落盘（声称写了文件但 fs 上没有——每次 agent 报完成都 grep/ls 复核）
4. 容器版本漂移 / 内存持续打满重启无效
5. 单版本连续 2 轮零新候选且 GT_HINT 计数不动

## 待拍板（跑首个版本前定）
- [ ] B3 阈值 60% 是否合适（pilot rerun qdrant 97.3%；milvus 无 spec 时 pct=N/A 如何门控）
- [ ] pilot rerun 的 qdrant v1.18.2 计不计入 15 版本（建议：计入，序号 2 已标；contract 是修复后管线产物）
- [ ] reach 对齐口径：param 匹配（injector 语义）+ 人工 LLM 盲评复核（pilot 用的双确认）——全量沿用双确认还是仅 param 匹配 + 抽查

## 汇总口径（每版本收口时进 summary.md）
- reach = chain_verdicts DEFECT 全集 ∩ gt.json param（injector _reached 语义：精确/容器前缀/多值拆分）
- DEFECT/链/NME、NOVEL/COVERED_BY_PR/UNVERIFIED/BY_DESIGN、retry 四数、doc_coverage_pct、GT 参数面 X/Y
- 9045（standalone-unreachable）单独报，不进 reach 分母

# TestVDB — RQ 结果数据统计

> 数据源：`paper/paper-draft-acm-sigconf.tex`（正文）+ `testvdb-ablation/c7_stability_5run.json`、`testvdb-ablation/analyze_corrected.py`（artifact）。所有数字可追溯到论文行号或 artifact。
> **TP/FP 分类标准**：见 [`data/issue-classification-standard.md`](../data/issue-classification-standard.md)（2026-07-26 全量核对 107 issue 后落地，含各 DB 拒绝信号体系 + 例外登记）。
> GT 口径（RQ2 的 48 候选）：27 TP + 21 FP（qdrant 6 个 OVERRIDE_FP：9255/9373/9416/9417/9418/9419；判定=label-based，行为违反文档=TP）。
> 更新日期：2026-07-26（去 meili/chroma → 107；全量核对 #11981 降级 → TP 50→49）。

---

## RQ1 — Yield & 文档-实现残差（§6.1, line 119–135）

### 产出规模
| 指标 | 值 |
|---|---|
| 候选 issue 总数 | **107**（跨 3 个 VDBMS：Milvus/Weaviate/Qdrant） |
| True-positive 缺陷 | **49**（15 merged-PR-fixed + 16 open fix-PR + 18 maintainer-acknowledged but unfixed） |
| ack-unfixed 18 = | 8 open-issue（accepted label）+ 10 stale-closed（accepted/未否认，无 merged PR） |
| 其余 58 = | 23 by-design/rejected + 35 pending |

### 每 vendor 提交 / TP
| VDBMS | Submitted | Acknowledged(TP) |
|---|---|---|
| Milvus | 51 | 22 |
| Weaviate | 30 | 13 |
| Qdrant | 26 | 14 |
| **Total** | **107** | **49** |

### Yield precision
- 维护者裁决集 N=72（49 TP + 23 by-design/rejected）→ **yield precision = 68.1%**，Wilson 95% CI **[56.6%, 77.7%]**
- 最坏情况（35 pending 全算 FP）→ 49/107 = **45.8% [36.7%, 55.2%]**

### 文档-实现残差
| 故障模型 | 占比 |
|---|---|
| documentation-implementation（经典 oracle 不可达） | **~85%**（49-TP 子集 89%） |
| classical-addressable（数学不变量/crash） | ~10% |
| concurrency | ~5% |

### VDBFuzz 头对头（Table 1, line 122–135；每方向 n=1，hypothesis-generating）
| 版本 | 可复现 | 修复状态 |
|---|---|---|
| Qdrant v1.4.0 | VDBFuzz 整数溢出 crash（size=2⁶³） | v1.5.0 修 |
| Qdrant v1.18.0 | TestVDB #9045（wait=false 接受零长向量）；#7967 load panic | 2026-05 修 |
| Qdrant v1.18.2 | —（TestVDB 目标版本） | 两者皆已修 |
- v1.18.2 上 VDBFuzz 默认配置跑 26,000+ mutated requests，**0 crash**（两 case-study crash 此版已修）。
- 方向 A：TestVDB 在 v1.4.0 标到 VDBFuzz 的 crash-class 缺陷（doc 说 size≥1 无上限，值 doc-valid 但 impl panic）。
- 方向 B：VDBFuzz 在 v1.18.0 挖不到 #9045（模板硬编码 wait=true，#9045 在 wait=false 路径；且响应是静默 HTTP 200，crash oracle 标不到）→ 读作 VDBFuzz 当前模板/输入覆盖局限，非 crash-oracle 本质属性。

---

## RQ2 — 源码接地证伪效果（§6.2, line 156–157）

### 受控回顾基线
- **N=48 候选**（27 TP + 21 FP；Milvus 32 + Qdrant 16），maintainer-adjudicated。

### 四配置横评（3-run any-confirmed ensemble）
| 配置 | acc | prec | recall |
|---|---|---|---|
| B1 Single-LLM（无 source anchor） | 48% | 56% | **37%** |
| B2 Multi-perspective (R1) | 50% | 80% | 15% |
| B2 + Debate (Vote) | 50% | 80% | 15% |
| **C7 contract-grounded dev-reviewer** | **65%** | **67%** [49%, 81%] | **74%** |
- 源码锚驱动 recall 增益 **37% → 74%**。

### 单 run 方差（5 个独立 run，artifact `c7_stability_5run.json`）
| 指标 | 单 run 范围 / mean±sd | 3-run any-C | 5-run any-C |
|---|---|---|---|
| accuracy | 44–65% / 54±9 | 65% | 62% |
| precision | 50–73% / 63 | 67% [49, 81] | 62% [46, 76] |
| recall | **15–78%** / 41±27 | **74%** [55, 87] | **85%** [68, 94] |
- 单 run 不稳（部分 run 保守、confirm 少）；any-C ensemble 是 reported 的降方差操作点。5-run 把 recall 推到 85% 但 precision 降到 62%（union 规则的精度-召回 tradeoff）。headline 用 3-run 以与 baseline 的 3-run 可比。

### 每 vendor（3-run any-C ensemble）
| Vendor | acc / prec / recall |
|---|---|
| Milvus | 69 / 73 / 80 |
| Qdrant | 56 / 50 / 57 |

### 锚点消融（Milvus 12-FP/4-TP 控制，v2.6.19，dev-reviewer-v2，blind）
| 锚点 | FP 抑制 | TP 保留 |
|---|---|---|
| source-grounded alone | 9/12（75%） | 4/4 |
| threat-model cross-check alone | 6/12（50%，state/concurrency FP 上不稳） | 4/4 |
| union | 11/12（91%） | 4/4 |
- clean-reproduction anchor 单独：tooling-artifact FP 12/14，by-design FP 仅 2/11。
- 源码锚是主导贡献者。

### 跨模型一致性
- DeepSeek 重跑 dev-reviewer on 20 candidates（6 回顾 + 14 新盲审，diversity-stratified）→ 与 GLM-5.2 全一致，**Cohen's κ = 1.0** → 源码证据显式时判决非 family-specific。

### 已撤回（t22）
- 旧 81% FP-suppression / 69.2% prec / 96.7% recall 基于 16-候选控制组，数据不可恢复，已被上述可复现 cross-vendor ensemble 取代（RQ2 footnote 披露）。

---

## RQ3 — 跨模型验证 vs 源码（task-intrinsic 误差）（§6.3, line 159–164；Table 2, line 166+）

### Parameter over-strict（18 子句，13 Milvus + 5 Qdrant v1.18.2，live-probe-confirmed）
- 原始 12（9 GLM Milvus collection-creation + 3 Qdrant：timeout=0/group_size=0/score_threshold 越界 accepted）+ 6 scaling（Milvus ef/nprobe/level/replicaNumber，Qdrant m/bits）。
- DeepSeek 独立 formalize → 同参数复现 over-strict：**6/18**（原始 5 + Qdrant bits）= **task-intrinsic 子集**。
- 跨模型 judging 抓到 8/18，**漏 3/6 TI**；source-grounded falsify 全部 18。
- **Parameter-TI rate = 6/18**，Wilson 95% CI **[16%, 56%]**（12-子句 pilot 曾为 [19%, 68%]，CI 收紧）。

### Behavior over-strict（11 行为，全 TI）
- 4 Milvus by-design（search 未加载 collection / 重复 create / drop 不存在 / leading-underscore 名）+ 7 新 idempotency（Milvus partition/index/load，Qdrant delete-nonexist，**Weaviate delete-nonexist-class**）。
- DeepSeek over-formalize **11/11**；跨模型 judging 仅抓 1/11；source falsify 全部 11。
- **Behavior-TI rate = 11/11**，Wilson **[74%, 100%]**。
- 机制：参数文档陈述 DEFAULT（仅偶尔引出 bound），行为文档陈述显式 error condition → 两 family 一致 over-formalize 成硬拒绝 → 被 idempotent 实现 违反。

### Explicit-bound 负对照（21 参数）
- Qdrant shard_number/replication_factor/...、Weaviate ef/dynamicEfMin/...、Milvus dimension/M/nlist 等，文档显式 bound。
- DeepSeek over-formalize **0/21**，Wilson **[0%, 16%]** → 现象集中于 ambiguous optional-default API，显式 bound 处消失。
- within-vendor contrast（Qdrant search 默认参数 over-strict vs collection 显式 minimum 不 over-strict；Milvus 同样）→ 文档风格是驱动因素，非 vendor 本身。可证伪预测：optional-default 无显式 bound → over-formalization 候选。

### 汇总（aggregate，非 headline）
- 跨两子类 pooled TI **n=29**：**17/29**，Wilson **[41%, 75%]**；跨模型 judging 抓 4/17。

---

## RQ4 — Model-free 不变量子类（**已并入 RQ1**，论文砍独立 §6.4，2026-07-26）

- 独立于 LLM pipeline，直接探测硬数学 bound：COSINE 距离 >1（同向量）、索引只返 2/25 匹配点、payload filter 返缺失必填字段的点。
- Milvus + Qdrant 可复现；最不依赖设计。
- 107 提交里有 **9 个数学不变量 issue** 属此类，计入 RQ1 的 ~10% classical-addressable 部分（论文一句话带过），不独立成 RQ。

---

## 关键 artifact 文件
| 文件 | 内容 |
|---|---|
| `data/yihui504-issues-final.xlsx` | 49-TP 权威账本（final_verdict / TP_tier 列） |
| `data/issue-classification-standard.md` | TP/FP 分类标准（核对依据，2026-07-26） |
| `testvdb-ablation/c7_stability_5run.json` | RQ2 5-run 方差 + ensemble + Wilson CI |
| `testvdb-ablation/analyze_corrected.py` | RQ2 四配置横评（B1/B2/C7） |
| `TestVDB/scripts/e2_scale_*.py` | RQ3 扩样本（18 over-strict + 11 behavior + 21 negative） |
| `TestVDB/results/vdbfuzz-head-to-head-2026-07-22.md` | RQ1 VDBFuzz 双向可达性报告 |

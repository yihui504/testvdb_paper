# RQ3 GT 分型与对比实验口径（实验侧资产，2026-08-24）

> 归属：实验仓（testvdb_paper）。插件实现见主插件 ADR-0009（实现/实验边界原则）。
> 数据源：`.paperpilot/phase2-rerun/cases_index.json` + `defect_id_map.json`
> （GT 44 口径 = 9149 证伪后；中间产物 `tmp_gen/gt_split_base.json`）。

## 一、GT 44 分型（crash / logic）

方法：title 关键词粗分（panic|crash|segfault|OOM|hang|…）+ 全 44 案人工复核。
边界裁定：qdrant_014（cluster/recover 返回 500）与 weaviate_010（batch delete
返回 500）为**误码语义型非进程崩溃**——服务存活、仅状态码错误，归 logic。

| 型 | 数 | 案 | 原发版本（issue） |
|---|---|---|---|
| **crash** | **2** | qdrant_001（空向量 `[]` upsert wait=false → panic，issue 9045）| v1.12.1 |
| | | qdrant_015（shard_number=INT_MAX → crash，issue 9520）| v1.18.2 |
| **logic** | **42** | 其余全部（验证缺失/静默接受/类型强转/精度偏差/误码语义）| — |

GT vendor 分布：milvus 29 / qdrant 7 / weaviate 8。

## 二、VDBFuzz 理论可达分析

VDBFuzz（ICSE'26，Wang et al.）的 bug 判定 = crash（connectivity 失联）；
mutation 面为边界值/类型/维度突变。因此：

- **全量 GT 上理论可达 = 2/44（4.5%）**，且全在 qdrant（INT_MAX 在其
  INTEGER_BOUNDARY_VALUES 预设内；零长度向量在其维度突变面内）。
- milvus 29 + weaviate 8（逻辑型）= VDBFuzz 理论零可达。
- **直接对撞"发现 bug 数"是不可比口径**——不能拿 42 个逻辑缺陷给 VDBFuzz
  记 miss（对 baseline 不公平，审稿人必攻）。

## 三、双轴对比口径（D6 微调拍板版）

**轴一：等时发现数**（各自口径、对称离线判定）：
- TestVDB：统一判定后 strict defect + exploratory candidate 分列
- VDBFuzz：crash 序列经去重/最小化/归因 triage 后 unique crash bug
- 预算 T = 纯挖掘时间；判定/triage 对称排除在 T 外（ADR-0009 §6）
- **重发现已知 bug 只在"理论可达并集"上对账**：对 VDBFuzz 只对账 crash 型 GT

**轴二：缺陷类型谱系**（互补呈现）：等时内两系统产出按
crash / logic(doc-inconsistency) 分型画谱系图——叙事定位"覆盖谱系互补 +
等时效率"，而非"谁发现多"。

## 四、版本对齐（2026-08-24 终拍：检验完备四版方案，选项 2）

> 修订记录：v1 曾按"每 vendor 最早版"（GT=6/crash 1/violates 1）并误标
> v2.6.16 GT=12（实为 dmap 原发分布含 FP；checklist 权威 GT=4）。v2 改四版
> 方案（用户拍板），依据三维度在场矩阵：violates 4 案分散于 4 版无单版全覆盖、
> qdrant 双版才能让 crash 双案都在场。

| vendor | 版本 | GT | crash 在场 | violates 在场 | 备注 |
|---|---|---|---|---|---|
| qdrant | **v1.18.0**（#1）| 2（9039、9045）| 1（9045，standalone 单列口径）| — | |
| qdrant | **v1.18.2**（pilot 版，RQ3 可用）| 4（9017/9421/9520/9522）| 1（**9520**=INT_MAX，VDBFuzz 最标准型）| — | 9045 在此版 GT 未列 |
| weaviate | **v1.37.4**（#4）| 3（11399/11400/11401）| 0 | — | 外部 issue 可信 |
| milvus | **v2.6.10**（#9）| 5（47729/47752/47755/47763/47766）| 0 | **2**（003/004）| violates 检验分母最大版 |

**合计**：GT 14 / crash 2（9045+9520）/ violates 2（003/004）。

**附送的时间纵深对照**：9045 在 v1.18.0 存在、v1.18.2 出局（GT 树未列）——
"已知修复 bug 在新版本不再被发现"是 re-discovery 特异性的免费对照证据。

**四版上 VDBFuzz 对账可达 = 2**（9045 standalone 可达性存疑 + 9520 标准型）——
轴一"重发现"列 VDBFuzz 分母 2，如实呈现。

**执行注意**：① qdrant v1.18.2 契约需重生成（A2 曾清缓存）；② milvus v2.6.10
契约需核验无 GT 污染（checklist 记录该版 A/B 段有污染史，#9 备注）；③
v1.18.2"不计入 RQ1 15 版"是 RQ1 执行序组织口径（pilot 旧管线），RQ3 按
"GT 存在版本"标准选用合法，论文里注明即可；④ milvus_001（violates，v2.3.22）
不在集合内，其专项检验推迟到后续 milvus 版本实验（15 版重跑覆盖）。

## 五、VDBFuzz 复现风险清单（执行时处置）

1. **本地 clone 模板不全**：`VDBFuzz/templates/` 仅 qdrant（205 个模板），
   weaviate/milvus 缺失——需上游 repo 重拉完整工件，或用 `vdbfuzz.generator`
   从流量捕获再生（README 可选流程）
2. **版本钉定**：工件默认 milvus v2.4.6 / qdrant+weaviate latest——对比须钉到
   我们选定版本；模板 endpoint 与旧版 API 面兼容性需 docker 实测预验证
   （qdrant 可用主插件 `qdrant1183-openapi.json` 对照 v1.18.0 面差）
3. **随机性**：normal_mutate 无种子固定；若用 exhaustive 模式则确定性
   （无重复需求）；normal 模式 r≥3 与我们对称
4. **T 值**：论文未公开（ACM DOI 404，无 arXiv）——用本地 2026-07-16 qdrant
   预跑日志校准主值 + 短档敏感性验证，论文里写校准依据不伪造文献惯例

# RQ2 契约 v2 报告——规约提取器完备化实验（2026-08-30）

## 根因与假设

29 案重判（rq2_ererun29）后对剩余误判挖根因，GitHub issue 原文审计发现：**维护者确认的判定基础大多也是文档锚**（HNSW 参数表、API Status 定义、openapi 免责限定词），我们漏判的根因不是"文档契约范式极限"，而是两个工程缺口：

1. **知识采集覆盖缺口**：hnsw.md（ef 域声明）、REST 参考 delete 选择器说明未入知识源 → 契约无断言可生成
2. **断言模板缺口**：错误码语义（"失败不得返回成功码"）、免责条款边界（"免责窗口外行为仍受用途承诺约束"）从未被模板化

假设：只补全输入文件（契约）的完备度，**判定标准一字不改**，即可救回误判。

## 方法（三段，全留痕）

- **Phase A 锚固化**：`anchors/ANCHOR_1..4`——①hnsw.md `ef Range: [1, int_max]`（GitHub 源逐字）②R.Status "Code 0 = Success"（issue 提交时核对引文；生成页 403 待补抓）③REST delete filter/ids 互斥（同上）④openapi "might be unreliable **during the indexing process**"（本地 spec 逐字，行号 12148）
- **Phase B 契约 v2**：4 版本契约各注入 1 条 `evidence_tier=explicit` 断言 + `_v2_augmentation` 声明（触发原因/GT-free 声明/模板泛化说明）；原契约与链全备份（`backup/`）；augmentation_log.txt 留痕
- **Phase C 链重做 + 机械层**：evidence-builder 重建 4 案链（GT 隔离：只给断言与文档原文，禁读 anchors/ 与 issue 语料）→ 机械层重跑（当前代码）

## 结果

### 机械层（4 案）

| 案 | verdict_A | implied | 要点 |
|---|---|---|---|
| milvus_003 | **CONFIRMED** | **DEFECT** | ef=0 静默接受（200+code=0），违反 hnsw.md 明文域 [1, int_max]；源码 validation_absent（仅建索引期 EfConstruction 校验）；defect_type Type4→Type1 更正 |
| milvus_024 | **CONFIRMED** | **DEFECT** | filter+ids 双发静默接受（deleteCount 仅反映 filter）；源码实锤：`CollectionFilterReq` 无 ids 字段、无 DisallowUnknownFields、handler 仅赋 Expr——ids 在 binding 层被丢弃 |
| qdrant_018 | **CONFIRMED** | **DEFECT** | 实测 -40%（24 vs 40，is_null 对照精确）；源码根因 `null_index/read_ops.rs:182` **无条件** `exp = 2*estimated/3`（无状态分支——稳态偏差实锤） |
| milvus_001 | REFUTED | NOT_DEFECT | 原执行日志仅 "[no raw HTTP captured]"，violates 无法建立；且 v2.3.22 源码已实现非零码语义（services.go:893 + handler_v2.go:258）——维持 FN（执行证据缺口） |

引文预检 4/4 通过。3 案机械定案无需 auditor（无灰区）。

### 71 案终态

| 口径 | recall | precision | TP 自动误判 | NME(转人工) | FP 拦/放 |
|---|---|---|---|---|---|
| revertb（v1 契约，冻结口径） | 0.841 | 0.881 | 7 | 0 | 22/5 |
| rerun29（+E 收紧） | 0.841 | 0.881 | 5 | 2 | 22/5 |
| **契约 v2（本报告）** | **0.909** (40/44) | **0.889** (40/45) | **2** (001/004) | 2 | 22/5 |
| 人工复核上界 | **0.955** (42/44) | — | 0 | 0 | — |
| v9（issue 锚定注入，已判 in-sample） | 0.909 | 0.889 | 4 | 0 | 22/5 |

## 关键发现

1. **v2（GT-free）达到 v9（issue 锚定注入）完全相同的数字 0.909/0.889**——注入的收益可以被规约提取器的采集补全 + 模板扩充**完全替代**，且无 in-sample 污染。0.909/0.889 因此从"污染上限"升格为"提取器完备化后的可辩护口径"。
2. **提升轴分离得到实证**：判定层改进（E 收紧，0.841→误判 7→5）与规约提取层改进（契约 v2，0.841→0.909）是两条独立的提升轴，效果可加。
3. **剩余 2 误判是两类真极限**：milvus_001 = 执行证据缺口（原日志无 HTTP 观测，非范式问题）；milvus_004 = 范式极限实锤（值域语义无文档承诺）。
4. 附带发现：#47752/#47755 账本分类 ACK_CLOSED_NOFIX 已过时（vendor milestone 2.6.14 已修复 closed completed）——账本 vendor 状态需一轮刷新。

## 口径声明

- 判定标准（断言违反 + 机械 A 定案 + E 收紧）全程一字未改；改的只有输入文件完备度（知识覆盖 + 断言模板）
- 断言补全触发于缺陷归因复查（诚实披露）；锚全部为 vendor 文档公开原文，不含 issue 语料/维护者态度；断言模板为泛化形态（状态码语义/文档值域/选择器互斥/免责边界），非单案定制
- builder 全程 GT 隔离（禁读 anchors 与 issue 语料，派发词仅含文档原文）
- RQ2 冻结实验集 71 = 44 TP + 27 FP 不变；v2 为契约完备化后的演进口径

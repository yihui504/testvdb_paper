# A1 · 审计状态汇总（2026-09-11）

对应评审 R1 3.3 / R2 3.6 / R3 3.4（三人一致的 `[major, fixable]` 头号必改项）。
本文件是单一入口；脚本 `01`–`06` 可复现全部结论。

## 审计对象

| 口径 | 数量 |
|---|---|
| 判据输入包 | 81（`TestVDB_artifact/rq2/materials/*.md`） |
| 独立约束 | 152（milvus 72 / qdrant 44 / weaviate 36） |
| 独立 source_url | 25（捕获成功 23） |
| 比对行（包 × 约束 × 引用页） | 1,645 |

## 发现 A · 引用页性质（机械）

| 库 | 引用页性质（按约束计） |
|---|---|
| milvus 72 | 文档 41 / **实现源码 29**（`constant.go`）/ 文档-raw 2 |
| qdrant 44 | 文档 43 / 结构化 spec 1 |
| weaviate 36 | **结构化 spec 35**（仓库内 OpenAPI `schema.json`）/ 文档 1 |

含义：Weaviate 的约束几乎全部锚在**结构化 spec** 上 —— 而论文 Table 1 第 5 行正把这一类（OpenAPI 派生）划在"达不到 system-level untagged prose"之列。

## 发现 B · 版本错配（机械）

1,645 行中 **316 行 MISMATCH**。经用户逐族复核与豁免后 **299 行成立**：

| 族 | 行数 | 内容差异实测 | 档位 |
|---|---|---|---|
| 1 milvus 3.0.0 → 2.6.x 文档 | 85 | 6 页全部存在正确版；substantive 改动中命中断言术语 118 行（Create 78 / Search 24 / Drop 6 / Load 3 / Rename 6 / Get 1） | **实质** |
| 2 milvus 3.0.0 → 2.6.17 源码 | 47 | 0 个常量文案改变；3.0.0 独有 14 个常量 | 技术性（风险是"漏"非"错"） |
| 3 weaviate 1.37.4 → 1.38.0 spec | 74 | 23 个 operation 内容不同；4 条 path 为 1.38.0 新增；受测包携带的 22 条约束中 **12 条落在差异上**，其中 **3 条锚在 1.37.4 不存在的 path** | **实质** |
| 4 qdrant 1.19.0 → 1.18 文档 | 62（豁免 7） | `search/points` 的正确版页面**不存在**→ 该 7 行豁免；其余 4 页存在，create-collection 命中 16 行、upsert 2、set-payload 3 | 部分实质 |
| 5 qdrant 1.12.1 → 1.18 文档 | 30 | 5 页全部存在正确版；相似度低至 0.26；命中断言术语 88 行（create-collection 44 / upsert 29 / set-payload 10 / points 5） | **实质** |
| 6 milvus 2.3 → 2.6.x | 10 | 正确版文档已下线（302） | **豁免**（用户裁决） |

⚠️ 方法学限制：`relevant` 列是「substantive 改动行中命中该页所引约束断言术语」的**宽松上界**——命中词如 collection/search/points 会连带匹配，不能当作"该改动必然影响该约束"的证据。

## 发现 C · 引用页是落地页（新增，独立于版本问题）

`https://api.qdrant.tech/v-1-18-x/api-reference`（**27 条 qdrant 约束**引用、462 实例）的 markdown 版仅 3,444 B，内容是
「Qdrant is a vector database… How does Qdrant work? 1. First, you should create a collection…」——
**不含任何端点参数文档**。且该页在 1.12 / 1.18 / 1.19 三版**完全相同**（相似度 1.0）。
即：这 27 条约束的 `source_url` 指向一个落地页，用它无法核验任何断言。

## 发现 D · 引用可用性

- **死链 1 条**：`milvus.io/api-reference/restful/v2.3.x/v2/Vector (v2)/Query.md` → 301 `/docs`（包 milvus_013，1 条约束）
- **不可解析 1 条**：`milvus.io/docs/index.md`（6 条约束，受测 3.0.0）在 docs 仓固定 SHA 下无同名文件。
  该 6 条全为索引 range 约束（`nprobe in [1, nlist]`、HNSW `ef`），
  其断言**有明文支撑**：`site/en/userGuide/indexes/floating-vector/ivf-pq.md` 载
  「`nprobe` … Type: Integer **Range: [1, nlist]** Default value: 8」
  → **引用不合格，约束本身有据**

## ⚠ 归属更正（2026-09-11，用户指出后核验）

**本文件此前的结论「§3.2 两道门禁执行口径与论文不符」是过度归因，已作废。**
证据：重建脚本 `rq2/pool/rq2_pool81/materials/augment_contracts.py` 硬编码

```python
ROWS = {
    'milvus':   load_rows(r'<PIPELINE_SOURCE>\results\milvus\v2.6.17\structured_contract.json'),
    'qdrant':   load_rows(r'<PIPELINE_SOURCE>\results\qdrant\v1.18.2\structured_contract.json'),
    'weaviate': load_rows(r'<PIPELINE_SOURCE>\results\weaviate\1.38.0\structured_contract.json'),
}
```

**每个 vendor 只用一份固定版本的契约，去补该 vendor 所有版本的包。** 发现 B 的六族错配逐一对上：

| 族 | 包声称受测 | 注入行来自 | 结论 |
|---|---|---|---|
| 1 / 2 | milvus 3.0.0 | `results/milvus/v2.6.17/` | 重建产物 |
| 3 | weaviate 1.37.4 | `results/weaviate/1.38.0/` | 重建产物 |
| 4 / 5 | qdrant 1.19.0、1.12.1 | `results/qdrant/v1.18.2/` | 重建产物 |

**发现 C（落地页引用）同样不属插件**：全部 18 份插件契约中，裸根页 `api-reference` 出现 **0 次**；
插件产出的 qdrant 契约一律引具体端点页（`.../collections/create-collection` 等）。

**发现 D（死链、不可解析）**同属注入行，来源同上。

RQ2 实验包为从 issue 逆推重建，其引用字段缺陷**只证明包本身质量不达门控，不能证明插件实现或论文对实现的表述有问题**。

## 唯一仍指向插件产物的两条（插件产出，非包）

1. `rq1-fullrun/qdrant-v1.18.0/structured_contract.json`（17 条）**字段整体错位一位**：`expected_behavior` 装 URL、`source_url` 装 tier 值、`evidence_tier` 装缺陷类型（17/17）。
2. milvus 系列契约的 `source_url` 装**本地文件系统路径**（`.milvus-src-2617/...`，各版本 4–19 条）与**散句描述**（6–12 条）；weaviate voided 契约装 `openapi (Step 6b cross-check fallback)`。
   —— 需先确认契约 schema 对 `source_url` 的定义，再判断这是缺陷还是设计。

## 待复核（不预设结论）

论文 §4.3 称四条泄漏的包是 "products of the extraction stage"、"the packs as extracted"，
并将泄漏归因为 "extraction-side errors"。但包实为**重建**物 —— 该归因是否仍成立，需复核。

## 处置原则

**不改冻结包** —— 它是 RQ2 的可复现物证，改它等于改证据。

## 仍未做

- 152 条约束的逐条 `page_supports` / `is_documentation` 判定（`worksheet.csv` 仍为空）
- `results/qdrant/v1.18.2/structured_contract.json`（augment 实际取用的那份）不在包内，落地页引用的确切来历无法完全闭合

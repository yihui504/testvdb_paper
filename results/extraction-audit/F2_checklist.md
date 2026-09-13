# F2 · 版本错配人工复核清单

用途：逐族核对「包声明的受测版本」与「它引用的页面版本」是否真的不一致。
数据源：`version_check.csv`（粒度 = 包 × 约束 × 引用页，共 1,645 行，其中 MISMATCH 316 行）。

## 怎么读这份清单

每族给你两个链接：

- **① 包实际引用的页** —— 打开看它呈现的是哪个版本。
- **② 该受测版本的正确页** —— 打开看它是否存在、且确实是这个版本。

**注意**：URL 里的版本片段只是路径字符串，判定要看页面**内容**呈现的版本（例如版本选择器、标题、字段表）。我下面的「实测」列只是 HTTP 可达性，不是版本正确性判定。

判定结论请填在 `worksheet.csv` 或直接回复我。

---

## 族 1 · milvus 受测 3.0.0 → 引用 v2.6.x 文档

- 影响：**85 行 / 15 条约束 / 10 个包**（milvus_034 … milvus_043）
- ① 包实际引用：<https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md> （另 5 个同族页：Search / Drop / Load / Rename / Get）
- ② 3.0.0 的正确页：<https://milvus.io/api-reference/restful/v3.0.x/v2/Collection%20(v2)/Create.md> — 我实测 **200 / 268,820 B**
- 核对要点：② 是否真在展示 v3.0.x 的 REST 参考（而不是把 v2.6 内容套了个 v3.0.x 路径）？若 ② 确实是 3.0 版页面，则本族成立。

## 族 2 · milvus 受测 3.0.0 → 引用 v2.6.17 源码

- 影响：**47 行 / 13 条约束 / 10 个包**（milvus_034 … milvus_043）
- ① 包实际引用：<https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go>
- ② 3.0.0 的正确源码：<https://github.com/milvus-io/milvus/blob/v3.0.0/internal/distributed/proxy/httpserver/constant.go> — 我实测 **200 / 428,010 B**
- 核对要点：这是**源码锚点**（论文所依赖的证伪锚）。② 与 ① 的错误码常量是否一致？不一致则本族成立，且冲击"源码为独立证伪锚"的版本前提。

## 族 3 · weaviate 受测 1.37.4 → 引用 v1.38.0 的 OpenAPI schema

- 影响：**74 行 / 21 条约束 / 4 个包**（weaviate_001 … weaviate_004）
- ① 包实际引用：<https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json>
- ② 1.37.4 的正确 schema：<https://github.com/weaviate/weaviate/blob/v1.37.4/openapi-specs/schema.json> — 我实测 **200 / 1,397,023 B**
- 核对要点：两版 schema 在受影响端点上的字段/约束是否相同？若相同，本族是"版本标签错但内容无实质差"；若不同，则约束可能来自目标从未承诺的版本。

## 族 4 · qdrant 受测 1.19.0 → 引用 v-1-18-x 文档

- 影响：**69 行 / 23 条约束 / 6 个包**（qdrant_023 … qdrant_028）
- ① 包实际引用：<https://api.qdrant.tech/v-1-18-x/api-reference> ／ <https://api.qdrant.tech/v-1-18-x/api-reference/collections/create-collection> ／ <.../search/points> ／ <.../points/upsert-points>
- ② 1.19 的正确页：<https://api.qdrant.tech/v-1-19-x/api-reference> — 我实测 **200 / 421,349 B**
- 核对要点：② 的版本选择器是否显示 1.19？受影响的 4 个端点页是否也有 1.19 版（如 <https://api.qdrant.tech/v-1-19-x/api-reference/collections/create-collection>）？

## 族 5 · qdrant 受测 1.12.1 → 引用 v-1-18-x 文档

- 影响：**30 行 / 30 条约束 / 1 个包**（qdrant_001）
- ① 包实际引用：<https://api.qdrant.tech/v-1-18-x/api-reference> 等 5 个页
- ② 1.12 的正确页：<https://api.qdrant.tech/v-1-12-x/api-reference> — 我实测 **200 / 421,630 B**
- 核对要点：跨了 6 个 minor（1.12 → 1.18）。② 是否在展示 1.12 的内容？

## 族 6 · milvus 受测 2.3 → 引用 v2.6.x 文档 / v2.6.17 源码

- 影响：**10 行 / 10 条约束 / 1 个包**（milvus_001）：7 行引 v2.6.x 文档，3 行引 v2.6.17 源码
- ① 包实际引用：<https://milvus.io/api-reference/restful/v2.6.x/v2/Vector%20(v2)/Search.md> 等
- ② 2.3 的正确页：<https://milvus.io/api-reference/restful/v2.3.x/v2/Collection%20(v2)/Create.md> — 我实测 **302，不可访问**
- ③ 2.3.0 的正确源码：<https://github.com/milvus-io/milvus/blob/v2.3.0/internal/distributed/proxy/httpserver/constant.go> — 我实测 **200 / 285,056 B**
- 核对要点：**本族与其他族不同 —— 正确版本的文档页本身已下线**。所以引 v2.6.x 文档在这族是"无更好选择"，情有可原；但 3 行的**源码**引用仍可从 v2.6.17 改为 v2.3.0，那部分成立。

---

## 附 · 与本清单相关的另外两条

- **死链 1 条**：`https://milvus.io/api-reference/restful/v2.3.x/v2/Vector%20(v2)/Query.md` —— 包 milvus_013（受测 2.6.16）引用它，实测 **301 → `/docs`**。而它自己版本的活页 <https://milvus.io/api-reference/restful/v2.6.x/v2/Vector%20(v2)/Query.md> 实测 **200**。即：引了一条死链，同时正确版本是活的。
- **无法解析 1 条**：`https://milvus.io/docs/index.md`（18 实例 / 6 约束）—— 在 milvus-docs 仓固定 SHA `ebb6de53` 的文件树中无同名文件。我**未猜路径**。需你判断该 URL 原本指向哪一页。

---

## 汇总：需要你给结论的问题

1. 族 1–5 的 ② 是否确实是该受测版本的页面？（决定这 5 族是否成立）
2. 族 2 的两版 `constant.go` 差异是否实质？（决定是否冲击源码锚点）
3. 族 3 的两版 schema 差异是否实质？（决定 Weaviate 21 条约束是否受影响）
4. 族 6 按"正确版文档已下线"处理，还是仍记为失配？
5. 死链那条与 `docs/index.md` 那条如何处置？

---

# 裁决与实测记录（2026-09-11）

## 裁决 1 · 族 1–5 的 ② 确实是该受测版本的页面 → **是**

F2 成立。316 行 MISMATCH 中，族 6 的 10 行按裁决 4 豁免 → **306 行确认成立**
（若保留族 6 那 3 行源码引用，则 309）。分档：

| 族 | 行数 | 内容差异实测 | 档位 |
|---|---|---|---|
| 1 milvus 3.0.0 → 2.6.x 文档 | 85 | 未逐页比对（待办） | 待定 |
| 2 milvus 3.0.0 → 2.6.17 源码 | 47 | **已测**：0 个常量文案改变；3.0.0 独有 14 个常量 | 技术性失配 |
| 3 weaviate 1.37.4 → 1.38.0 spec | 74 | **已测**：23 个 operation 内容不同；4 条 path 是 1.38.0 新增 | **实质失配** |
| 4 qdrant 1.19.0 → 1.18 文档 | 69 | 未逐页比对（待办） | 待定 |
| 5 qdrant 1.12.1 → 1.18 文档 | 30 | 未逐页比对（待办） | 待定 |
| 6 milvus 2.3 → 2.6.x | 10 | 正确版文档已下线 | **豁免** |

## 裁决 2 · 族 2 内容差异 — 已用 `05_version_content_diff.py` 实测

「实质不同」的定义：**两版文件中被这些约束所引用的那段内容是否发生了变化**。

- `constant.go` v2.6.17(引用) vs v3.0.0(受测)：213 → 228 行，diff 59 行（+32 / −17）
- **0 个常量取值/文案改变**；仅在 3.0.0 存在的常量 14 个；仅在引用版存在的 0 个
- 结论：已引用的常量在 3.0.0 中文案一致 → 风险是**漏**（3.0.0 新增的错误语义未进约束集），不是**错**

## 裁决 3 · 族 3 内容差异 — 已实测

- `schema.json` v1.38.0(引用) vs v1.37.4(受测)：paths 73 → 69，**23 个 operation 内容不同**，components 完全相同
- 1.38.0 独有 path：`/namespaces`、`/namespaces/{namespace_id}`、`/schema/{className}/indexes`、`/schema/{className}/indexes/{propertyName}`
- 限定到**受测 1.37.4 的包**所携带的 22 条 weaviate 约束：**12 条落在差异上**，
  其中 3 条锚在 1.37.4 根本不存在的 path（`/schema/{className}/indexes/{propertyName}`）：
  `weaviate_behavioral_index_update_001`、`weaviate_state_index_update_001`、`weaviate_type_index_update_001`
- 结论：**实质失配**

## 裁决 4 · 族 6 **豁免**

正确版本的文档页（`milvus.io/api-reference/restful/v2.3.x/...`）实测 302 已下线，引 v2.6.x 属无更好选择。
（注：3 行 v2.6.17 源码引用其实有活页 `blob/v2.3.0/...` 可改，但按整体豁免处理。）

## 裁决 5 · 死链与 `docs/index.md` — 处置方案

**总原则：不改冻结包。** 冻结包是 RQ2 的可复现物证，改它等于改证据。改为在审计中补「替代引用 + 复核结论」。

### 5a · 死链（`milvus.io/api-reference/restful/v2.3.x/v2/Vector (v2)/Query.md`，包 milvus_013，1 条约束）
- 该页 301 → `/docs`；同版本活页 `v2.6.x/v2/Vector (v2)/Query.md` 实测 200
- 处置：补「替代引用」并复核该断言，不动包

### 5b · `milvus.io/docs/index.md`（6 条约束，受测 3.0.0）
- 该 URL 在 docs 仓固定 SHA `ebb6de53` 下**无同名文件**（未猜路径）
- 该 6 条全为索引参数 range 约束：`nprobe in [1, nlist]`（IVF_FLAT / IVF / IVF_PQ / IVF_SQ8 / SCANN）、`ef in [1, 2147483647]`（HNSW）
- **已找到反证**：`site/en/userGuide/indexes/floating-vector/ivf-pq.md` 明文载
  「`nprobe` … Type: Integer **Range: [1, nlist]** Default value: 8」
- 处置：**引用不合格，但约束本身有据**。补「替代引用」为对应逐索引页（`floating-vector/{ivf-flat,ivf-pq,ivf-sq8,scann,hnsw}.md`），并将原 URL 记为不可解析引用

## 仍未做的

- 族 1 / 4 / 5 的文档页面**内容差异未逐页比对**（只确认了引用版本 ≠ 受测版本，未确认内容是否实质不同）
- 152 条约束的逐条 `page_supports` / `is_documentation` 判定（`worksheet.csv` 仍为空）

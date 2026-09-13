# 锚 4｜qdrant_018 (issue #10120) — count `exact` 描述的免责限定词

- **来源**: qdrant openapi (v1.18.x redoc, 本地 `.qdrant-src-1190/docs/redoc/v1.18.x/openapi.json`，与 GitHub `v1.18.3/docs/redoc/v1.8.x/openapi.json` 同源)
- **验证日期**: 2026-08-30（本地 spec 逐字提取）
- **对应缺陷**: qdrant_018 / issue #10120 "count `exact=false` on `is_empty` under-counts ~35% consistently"（TP，vendor `bug` 标签已挂）

## 原文（逐字）

`POST /collections/{collection_name}/points/count` requestBody `exact` 字段描述：

> "If `true`, count exact number of points. If `false`, count approximate number of points faster. Approximate count might be unreliable **during the indexing process**. Default: `true`"

`IsEmptyCondition` schema 描述：

> "Select points with empty payload for a specified field"

## 断言映射（新模板：免责边界断言）

- 文档免责限定词: "might be unreliable **during the indexing process**" —— 免责窗口仅限索引构建期
- 缺陷形态: 稳态（indexing 完成后）`is_empty` 条件下 `exact=false` 低计 ~35%（200/500/1000 三规模一致），同集合 `is_null` 对照两路径均精确——排除总体估计器问题，定位 `is_empty` 基数估计路径
- 断言: `exact=false` 在文档免责窗口之外须给出与 `exact=true` 一致（或合理近似）的结果；**免责条款的限定条件之外，行为仍受该字段用途承诺约束**
- evidence_tier: **explicit**（openapi 描述逐字 + 限定词语义边界论证）
- 备注: 此前 revertb 撤除的 `qdrant_state_count_approx_001`（偏差 <10% 断言）锚定为 OpenAPI caveat 语义推断而判 in-sample；本断言不设数值界、仅用文档限定词自身作边界，锚为文档原文

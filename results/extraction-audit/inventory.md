# A1 · 抽取阶段取证 — 机械清点（不判定）

- 包数：81
- 约束条目实例：2106
- **去重后独立约束：152**
- **去重后独立 source_url：25**

## 引用页性质分布（由 URL 本身决定，不含判定）

| 性质 | 实例数 | 独立 URL 数 |
|---|---|---|
| vendor-documentation | 1554 | 20 |
| implementation-source | 312 | 1 |
| structured-spec | 238 | 2 |
| doc-markdown-raw | 2 | 2 |

## 各库约束数与包声明的测试版本

| 库 | 独立约束 | 包声明版本 | 引用页性质（约束计数） |
|---|---|---|---|
| milvus | 72 | 2.3, 2.6.10, 2.6.12, 2.6.16, 2.6.17, 2.6.19, 3.0.0 | vendor-documentation×41、implementation-source×29、doc-markdown-raw×2 |
| qdrant | 44 | 1.12.1, 1.18.0, 1.18.1, 1.18.2, 1.18.3, 1.19.0 | vendor-documentation×43、structured-spec×1 |
| weaviate | 36 | 1.37.4, 1.38.0, 1.38.2 | structured-spec×35、vendor-documentation×1 |

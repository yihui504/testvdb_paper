# v8 阶段1：文档考古批量补断言（2026-08-20）

## 执行

7 案 FN（契约缺断言族）逐一考古并补断言入契约、重建链、机械重判：

| case | issue | 断言 | 锚点 | 机械 A |
|------|------|------|------|--------|
| milvus_008 | 49059 | COSINE distance=1-sim∈[0,2], identical→0 | docs 快照 ebb6de53 metric.md | DEFECT ✓ |
| milvus_012 | 49889 | dbName="" 应拒绝 | API ref URL + issue 转述（filter="" 同类已修） | DEFECT ✓ |
| milvus_013 | 49890 | Request-Timeout 必须整数 | API ref URL（integer 类型标注） | DEFECT ✓ |
| milvus_033 | 51085 | vectorFieldType 枚举闭集 | issue 实证（idType 拒绝/同族一致性） | DEFECT ✓ |
| milvus_038 | 52311 | group_by_field 标量字段 | docs 快照 99af7351 grouping-search.md | DEFECT ✓ |
| qdrant_016 | 9522 | lookup_from.collection 须存在 | qdrant OpenAPI v1.18.2 | DEFECT ✓ |
| qdrant_018 | 10120 | approx count 系统性偏差<10% | qdrant OpenAPI v1.18.3 caveat 语义 | DEFECT ✓ |

auditor 复审 7/7 DEFECT，聚合违例 0。

## 过程发现与修复

1. **版本组错位事故（2 处，我派发词写错版本）**：008 派到 2.6.16（实际 2.6.12）、
   033 派到 3.0.0（实际 2.6.19）——断言与链已搬到正确契约/目录。教训：派发词版本
   必须从 dmap 直读
2. **机械 A JSON 转义盲区（修复 commit a47bcd7）**：quote 含引号时契约文件原文是
   `\"` 转义形态、链内是解析后 `"`——逐字匹配必失败。修复：规范化后双匹配。
   全量回归：除考古 7 案与已知 029 CONFLICT 外零扰动
3. 012 的考古锚是 API reference（网站渲染）而非 docs repo 正文——docs repo 无该
   内容（子模块化）。锚 issue 引用的网站 URL + issue 正文转述，_provenance 说明

## 阶段1 小测（防回归）

| 口径 | recall | precision | fp_supp |
|------|--------|-----------|---------|
| v7.1（基线） | 0.727 | 0.780 | 0.667 |
| **v8 阶段1** | **0.886** | 0.812 | 0.667 |

- TP 32→39（+7 全部来自考古案，目标达成）
- FP 9 持平（零新增 ✓）、FN 12→5
- precision 0.780→0.812（分母 TP 增大），fp_supp 不变

## 残余 FN 5

violates 误标族 ×4（001/003/004/024——violates 复核闭环待激活）+ 029 CONFLICT 悬置 ×1。

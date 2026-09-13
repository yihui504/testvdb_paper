# M1 机械初稿报告

- 包数 81；契约行总数 2106
- G4 端点过滤删除 832（39.5%）
- 保留 1274（其中主断言 4）
- _provenance 剥除 4 行；issue 号残留标记 0 行
- 端点过滤后契约段为空、需人工考古的包 9：
  milvus_012, milvus_013, milvus_017, milvus_034, milvus_039, milvus_041, qdrant_014, qdrant_018, qdrant_023

## G1 版本核对（保留行）

- aligned: 1013
- MISMATCH: 156
- NO_VC_ROW: 64
- page-unversioned: 41

## G2 URL 状态（保留行）

- OK: 872
- LANDING_PAGE: 383
- UNRESOLVABLE: 18
- DEAD_LINK: 1

## 待人工核查行（lines_to_verify.jsonl）

- main（主断言）: 4
- bulk: 1270
- 其中页面文本缺（需补抓）: 19

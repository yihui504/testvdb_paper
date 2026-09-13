# Bug pattern taxonomy(51 confirmed bugs 精分草稿)

日期:2026-09-06。**人工精分(基于 issue 标题),待用户逐条/抽样核后回填论文。**
源:xlsx A∪B 51;pattern 命名延续论文 §4.2 风格(SCREAMING-SNAKE)。

## 统计(8 pattern)

| Pattern | 数量 | 定义 |
|---|---|---|
| **SILENT-ACCEPT** | **25** | 参数校验缺失被静默接受(range/type/empty/enum/互斥约束;含静默归一化) |
| **TYPE-COERCION** | 8 | REST 静默类型转换/替换默认值(string→Int64、无效枚举→默认) |
| **SILENT-IGNORE** | 4 | 参数或输入被静默忽略/丢弃(strictGroupSize、max_query_limit、负 ttl、mismatch 向量) |
| **RESULT-INCORRECTNESS** | 5 | 计算结果系统性错误(近似计数少计、COSINE>1、非确定分组) |
| **STALE-COUPLING** | 2 | 跨集合引用/状态耦合失效(lookup_from 族) |
| **WEAK-DIAGNOSTIC** | 3 | 错误码/诊断语义错误(500 代 4xx、Code 0 掩盖失败) |
| **DOC-SPEC-GAP** | 1 | 约束只在实现侧存在,文档/OpenAPI 未声明(9942) |
| **OTHER** | 3 | documented 支持缺失(autoID)、跨通道不一致、panic(9045) |

## 逐条明细

### SILENT-ACCEPT(25)
- milvus(15):#47729 nprobe=0 · #47752 ef=0 · #47755 filter 表达式过宽 · #47763 无效字段名 · #47766 int→string 字段 · #49823 nprobe=0(REST) · #49889 dbName 空串 · #49890 非整数 Request-Timeout · #49930 ef/nprobe 0/-1 · #50018 aliases 空名 · #50323 delete filter+ids 互斥 · #50353 limit=0/-1 与维度不匹配返 200 · #50354 密码复杂度 · #52309 group_size 0/-1 · #52311 向量字段 group_by
- qdrant(3):#9017 hnsw_ef=0 · #9524 非法 filter 条件 200 · #10372 field_schema 数组建错索引
- weaviate(7):#11399 dynamicEfMin>Max · #11400 flatSearchCutoff 负值 · #11401 replicationFactor=-1 归一为 1 · #11729 desiredCount 负值 · #11730 空串 tokenization · #11732 distance=null 默认 cosine · #11741 空串 activityStatus

### TYPE-COERCION(8,milvus 全家)
#51084 consistencyLevel 无效枚举→默认 · #51085 vectorFieldType 同上 · #52307 纯字符串覆盖合法 JSON · #52308 string→Int64 PK · #52310 标量混杂 coercion · #52312 upsert 同 52308 · #52314 string→DOUBLE/BOOL · #52315 字符串编码向量(gRPC 拒)

### SILENT-IGNORE(4)
#52325(milvus) strictGroupSize 忽略 · #10373(qdrant) limit 省略时无视 max_query_limit · #49843(milvus) 负 ttl 丢弃 · #9039(qdrant) 异步丢维度不匹配向量

### RESULT-INCORRECTNESS(5)
#49059(milvus) COSINE 距离>1.0 · #10120/#10125/#10127(qdrant) count exact=false 系统性少计 · #10371(qdrant) 无 query 分组成员非确定

### STALE-COUPLING(2,qdrant)
#10369 lookup_from 维度校验旁路 · #9522 lookup_from 引用不存在集合仍 200

### WEAK-DIAGNOSTIC(3)
#9421(qdrant) standalone 500 代 4xx · #12041(weaviate) 缺 match 500 代 422 · #47635(milvus) load 后 Code 0 掩盖失败

### DOC-SPEC-GAP(1)
#9942(qdrant) OpenAPI 缺 size≤65536(修复=文档+代码补声明)

### OTHER(3)
#50355(milvus) 文档称支持 autoID upsert 实失败 · #52313(milvus) REST/gRPC 存储格式不一致 · #9045(qdrant) wait=false 空向量 panic(全数据集唯二 crash 之一)

## 边界案(判读依据,请重点核)

| issue | 归类 | 备选 | 说明 |
|---|---|---|---|
| #49843 | IGNORE | COERCION | "drops negative ttl"——丢弃值 vs 转换值 |
| #52307 | COERCION | OTHER(数据损坏) | string 覆盖 JSON,根因是类型不校验 |
| #47635 | WEAK-DIAGNOSTIC | RESULT(时序 race) | Code 0 掩盖失败;若根因是 load 时序则应挪 |
| #10372 | SILENT-ACCEPT | RESULT | 接受畸形输入+建错索引,主症状是 accept |
| #9039 | SILENT-IGNORE | WEAK-DIAGNOSTIC | 标题自带 "Poor Diagnostics",主体是静默丢数据 |
| #49059 | RESULT | SILENT-ACCEPT | 数学错(距离上界),非接受问题 |
| #50353 | SILENT-ACCEPT | WEAK-DIAGNOSTIC | 200-for-invalid 两症状并存,归 accept |

## 论文映射建议

现论文 4 pattern(SILENT-ACCEPT-RANGE/STALE-CROSS-COLLECTION-COUPLING/PARTIAL-APPLY/WEAK-DIAGNOSTIC)与实际分布不匹配:PARTIAL-APPLY 0 例;建议改用本表 8 pattern(SILENT-ACCEPT 并 range/type/empty;新增 COERCION/IGNORE/RESULT/DOC-GAP)。待拍板后改 §4.2 categories 段。

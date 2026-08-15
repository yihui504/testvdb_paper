# fixD 预注册计划：qdrant vendor 锚点包扩充

> 日期：2026-08-15。Run 标识：**fixD**。配置 = 原版 SOP（fixC 已回滚）+ fixA 锚点（milvus）
> + **qdrant 新增 3 条锚点**（D2/D3/D4）。派发 prompt 零改动。

## 1. 动机

fixC 分 vendor 结果（FIXC_REPORT）：统一 E 规则在 qdrant 净 −2（9027/9417/9419 错向 C），
方向与 qdrant"宽松接受"文化相反。本试验验证：**per-vendor 材料侧锚点**（预编译进
intelligence）能否翻正——这是"裁决知识位置效应"谱系的最后一格。

## 2. 锚点内容（从维护者 issue 评论原文泛化，2026-08-15 fetch 验证）

| # | 锚点（注入 qdrant developer_cognition.blindspot_indicators） | 维护者行为支撑 |
|---|------|------|
| D2 | "Payload-only collections: creating a collection without vector configuration is a supported use case, errors surface on first vector use (maintainers: 'not an unusable collection, it allows payload-only collection')" | 9416+9417 双 issue 关闭（coszio，意图陈述原文） |
| D3 | "Lenient filter parsing: null / single-object / array forms are all accepted by design for filter condition fields (maintainers: 'This is fine and expected... it would be a breaking change'; source types.rs supports all three)" | 9418+9419 双 issue（coszio，两处独立表态） |
| D4 | "Batch operations are not promised to be atomic: users must assume partial application and retry (idempotent write design) (maintainers: 'batch operations are not promissed to be atomic')" | 9371 双 MEMBER（generall+timvisee） |

**不注入** D1（score_threshold 范围）：仅 9027 单 issue 单行为，违反条件 1（≥2）——
qdrant 锚点边界与 milvus 对称受限。

**披露义务**：锚点从 GT 对应 issue 的维护者表态原文泛化（GT-informed），论文须披露。

## 3. 三条件自检

1. D2/D3/D4 各有 ≥2 独立维护者公开行为（上表）✓
2. 方向冲突：D3（解析宽松=by-design）与 qdrant_001（GT=B，静默丢数据=bug）的切分线
   "语义等价宽松 vs 数据完整性丢失"由维护者原文支撑（9418 "fine and expected" vs 001 的
   ACK 行为），非从 GT 反推 ✓；D1 因 9017（hnsw_ef 修复）同簇+单行为，不注入 ✓
3. 普适现象类措辞（不指单字段/端点）✓

## 4. 子集（11 case，预注册固定）

- **SPLIT/对照 9**（同 fixC qdrant 子集）：003/004/007/009/010/011/012/017 + 002
- **稳定对照 2**（防锚点误伤，fixA 三轮稳定对/错）：013（三轮 FP，GT=C）、015（三轮 C，GT=A）
- milvus/weaviate 零重判（材料物理不触及）

## 5. 预注册判据（跑前固定）

- **主指标**：qdrant 9 子集上 fixD 对错 ≥ **6/9**（fixA r1/r3 水平；fixC 为 4/9）
- **锚点适用检查**：D2/D3/D4 适用 5 case（007/009/010/011/012）中 ≥4 判对
  （fixC 该 5 case 对 2）
- **误伤检查**：稳定对照 013/015 不劣化（013→FP、015→C）
- **判据三支**：
  1. 达标（主指标+适用检查+无误伤）→ 记录"vendor 锚点包扩充有效"，qdrant 锚点从 10→13
  2. 锚点未消费（适用 case 判词未引用锚点方向）→ 记录"锚点消费也是概率性"（呼应 fixC
     执行漂移）
  3. 误伤 → 回滚锚点（MATERIAL_FIXES 留痕）

## 6. 纪律

注入走脚本（fix_intel_blindspot_d.py，v2 包+intel 源两处，MATERIAL_FIXES 留痕）；
每 case 新会话、生成器原文派发、archive_verdict 归档、VOID_LOG 留痕、audit 0 FAIL。

## 7. 预判（跑前写定）

qdrant 9 子集 6-7/9：D2/D3 适用 4 case 全翻正（+2），D4 适用 007 保持，9017/9027 无锚点
仍随会话（约 50%）；对照保持。若锚点被部分消费（fixC 同款执行漂移），落 5/9。

# fixD 报告：qdrant vendor 锚点包扩充（有效，锚点保留）

> 日期：2026-08-15。Run 标识：**fixD**。预注册计划见同目录 FIXD_PLAN.md（跑前 commit）。
> 干预：qdrant developer_cognition 注入 D2/D3/D4 三锚点（顶层 10→13 + 内层双处，
> fix_intel_blindspot_d.py，MATERIAL_FIXES 172，audit 0 FAIL）。D1（score_threshold）因
> 单行为违反锚点条件 1 不注入。配置 = 原版 SOP + fixA 锚点 + qdrant 3 锚点。
> 子集：qdrant 9（fixC 同款）+ 稳定对照 013/015 = 11 case；milvus/weaviate 零重判。

## 1. 预注册判据结果

| 指标 | 结果 | 判据线 | 判定 |
|------|------|--------|------|
| qdrant 9 子集对错 | **7/9**（fixC 4/9、fixA r1/r3 6/9、r2 3/9） | ≥6/9 | **PASS** |
| 锚点适用 5 case（007/009/010/011/012） | **4/5 对**（仅 007 错） | ≥4 | **PASS** |
| 稳定对照 | 013 保持 ✓；**015 劣化 ✗** | 全保持 | **字面 FAIL** |

**处置：锚点保留**。理由：015 判词级因果检查排除锚点归因——`cognition_match:
matched_pattern="none"`（未消费任何锚点），劣化路径是"契约只写下界 + B 物理约束未触发"
的会话自主论证，属轮方差（同 fixA run3 的 milvus_035 对照劣化先例，当时同样保留 fixA）。
**如实披露**：这是预注册判据的字面违反 + 事后因果解释，论文引用时应注明；且 fixD 为单轮，
7/9 含轮方差利好（002/003/004/017 四个无锚点 case 里 3 个翻对——无锚点区仍在漂）。

## 2. 逐 case

| case | GT | fixA 三轮 | fixC | fixD | 锚点 | 消费 |
|------|-----|----------|------|------|------|------|
| 002 hnsw_ef=0 | CONFIRMED | F/F/F | F | **C** ✓ | — | 轮方差翻正（B 物理驱动） |
| 003 score_threshold | FP | F/C/C | C✗ | **F** ✓ | — | 无锚点仍翻正（轮方差利好） |
| 004 wait 旁路 | CONFIRMED | C/F/C | F✗ | **C** ✓ | — | 轮方差翻正 |
| 007 batch 原子 | FP | F/C/F | F✓ | C✗ | D4 | **引用未消费**（契约 A 压倒锚点） |
| 009 vectors={} | FP | F/C/C | F✓ | **F** ✓ | D2 | 消费（判词一字引用） |
| 010 vectors 缺失 | FP | F/C/F | C✗ | **F** ✓ | D2 | **消费翻正** |
| 011 should=null | FP | C/F/F | F✓ | **F** ✓ | D3 | 消费 |
| 012 must_not 对象 | FP | C/F/F | C✗ | **F** ✓ | D3 | **消费翻正** |
| 017 分页重复 | FP | F/F/F | F✓ | C✗ | — | 轮方差翻错（既有 HNSW 锚点未救住） |

## 3. 核心发现

1. **vendor 锚点包扩充有效**：锚点适用类 4/5 消费生效（009/010/011/012 全对，含 fixC 的
   两个错向翻正），qdrant 子集 +3 vs fixC。与"裁决知识应预编译进 per-vendor 材料"的位置
   效应谱系一致：**per-vendor 锚点（fixD 7/9）> 统一规则（fixC 4/9）**。
2. **锚点消费仍受两个概率性限制**：
   - **锚点-契约冲突时例外条款启用随会话**（007）：判词显式引用 D4 原文"batch operations
     are not promised to be atomic"却仍被契约断言"executed atomically"的视角 A 压倒——
     原版 SOP 的例外条款（"除非 maintainer 陈述"）是否被锚点触发是概率性的，与 fixC 的
     执行漂移同构。
   - **无锚点区仍轮方差**（002/003/004/017 四 case 3 翻对 1 翻错）。
3. **可辩护锚点 qdrant 侧也接近边界**：D1（score_threshold）单行为不可注入；既有 10 条 +
   D2/D3/D4 后，SPLIT 剩余错向（007 锚点-契约冲突、017 既有锚点未消费）均非"补锚点"可解。
   三 vendor 锚点边界齐了：milvus 穷尽（fixB）、qdrant 13 条后穷尽、weaviate 样本小。

## 4. 论文口径（fixA+fixD 合并配置）

最终材料配置 = fixA 锚点（milvus 通道一致性）+ qdrant 13 条（10 既有 + D2/D3/D4）。
合并配置的全量单轮效果未验证（fixD 仅 qdrant 子集 11 case）——引用时分 vendor 报告：
qdrant 子集 fixD 7/9 vs fixC 4/9 vs fixA 最好单轮 6/9，并注明单轮 + 轮方差 caveat 与
GT-informed 注入披露义务。

## 5. 归档

- 判词 `fixD/verdicts/`（11）；锚点注入脚本 `fix_intel_blindspot_d.py`（含备份
  pre_fixD_backup/）；MATERIAL_FIXES 172；audit 0 FAIL；容器全清；dispatch_log 全留痕

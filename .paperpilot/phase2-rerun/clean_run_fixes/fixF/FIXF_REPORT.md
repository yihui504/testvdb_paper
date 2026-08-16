# fixF 报告：最终配置全量单轮快照

> 日期：2026-08-16。Run 标识：**fixF**（final snapshot，配置定格，非干预试验）。
> 预注册：docs/phase2-status-and-decisions.md §5（原版）+ 本轮执行前更新（含 C/G + fixH/I）。
> 配置 = fixA 锚点（milvus 通道一致性）+ qdrant 13 锚点 + C 锚点（milvus 文档-行为）+
> G 锚点（weaviate 错误码）+ 契约修复 M1/M2/Q1/Q2 + fixH 001/002 残留断言 +
> fixI range_insert_001 + 原版 SOP。MF 176；audit 0 FAIL。
> 子集 = 71 case（70 重判 + milvus_001 例外沿用 clean）；三 vendor 异容器并行、组内串行、
> 切组前核对容器版本（零错配事故）；判词 `fixF/verdicts/`（70）；voided 空。

## 1. 全量指标（分母 44，C 组 27）

| 轮/配置 | recall | fp_supp | precision(C) | acc |
|---------|--------|---------|--------------|-----|
| clean | 0.545 | — | — | — |
| fixA r1 / r2 / r3 | 0.636 / 0.659 / 0.568 | 0.704 / 0.519 / 0.630 | 0.778 / 0.690 / 0.714 | 0.648 |
| **fixF** | **0.659** | **0.667** | **0.763** | **0.662** |

- **落在预注册预期带内**（recall 0.60-0.68 中心 0.63；fp_supp 0.59-0.78）；
  recall 持平 fixA 最好轮，precision/acc 历史新高。
- 轮间 κ(fixF vs fixA 三轮) = 0.267 / 0.486 / 0.296——与 fixA 轮间 κ(0.352-0.492)
  同级，轮方差未被消除（预期内：fixC 已证规则显式化无效）。
- 分 vendor：milvus 0.655/0.714；qdrant 0.429/0.727（q002/q014/q016/q004 漂移漏）；
  weaviate **0.875**（8/8 只漏 w008 漂移）但 fp_supp 0/2（w004/w009 漂移错向）。

## 2. 顽固 FN 池裁决（fixF 的核心看点）

预注册预期"顽固 FN 8 个仍漏（信息不可达）"。实际：**8 个中翻正 3、漏 5（+031 概率性）**——
好于预期：

| case | 类 | fixF | 路径 |
|------|-----|------|------|
| milvus_008 | A 数值精度 | **C ✓翻正** | 现象漂移到"误导性错误信息"（Type2_PoorDiagnostics——auto index 的 'multiple indexes' 错误误导），源码+实测论证，无需态度信息 |
| milvus_017 | B 空串参数 | **C ✓翻正** | OptionalCollectionNameReq 缺 required 标签 vs 其他端点有——端点间不一致论证（结构性证据） |
| weaviate_010 | G 错误码 | **C ✓翻正** | **G 锚点直接消费**（判词引用"maintainers ... repeatedly fixed 500→422/404"）——锚点通道二连中（fixG/fixF） |
| milvus_031 | C 文档-行为 | F ✗ | 现象漂移到 enableDynamicField 次现象（fixG C✓/fixH F✗/fixF F✗——翻正概率性实证） |
| milvus_001 / 009 / 012 / qdrant_002 / qdrant_014 | 材料/B/E/F | F ✗ | 如预期锁死（三条件死刑类，态度不可达复现） |

**结论**：锁死 FN = 5 + 031 概率性；三条件"证据性死刑"判定全部被 fixF 复现
（001/009/012/q002/q014 五连漏）；008/017 的翻正路径是**结构性取证**（误导性错误信息/
端点间标签不一致——不需要维护者态度），修正了"信息不可达"模型：B 类中部分 case
存在态度之外的源码级论证通道。

## 3. 断言/契约修复全量保持验证

| 修复 | case | fixF | 状态 |
|------|------|------|------|
| fixE M1/M2 | milvus_022 / 023 | F ✓ / F ✓ | 保持 |
| fixE Q1/Q2 | qdrant_007 / 009 / 010 | F✓ / F✓ / **C ✗漂移错向** | q010 单例漂移（fixE 轮 F 对，D2 锚点适用类轮方差） |
| fixH 001/002 | milvus_022 | F ✓ | 保持（三断言同向消费） |
| fixI range_insert_001 | milvus_025 | F ✓（conf 0.98） | 保持（判词直接消费修复后断言 + MaxInsertSize=-1） |

## 4. 错向面（GT=FP 判 C，9 个）

漂移错向 9：milvus_015/018/028、qdrant_003/006/010、weaviate_004/009。
- milvus_028：fixA 锚点副作用面（跨通道不一致泛化到 enum 默认回退）——已知机制
- q003/q010/w009：无锚点区/锚点适用区轮方差（w009 三轮 C/C/C 基线即全错）
- 其余为灰区漂移带；fp_supp 0.667 低于乐观预期的原因即此 9 例漂移

## 5. 归档与披露

- 判词 `fixF/verdicts/`（70）+ FIXF_RESULTS.json（71 case 逐条）+ dispatch_log 71 行；
  voided 空（零作废、零容器错配）；容器全清。
- 判词格式三种位置（平铺/steps.source_grounding/顶层 source_grounding）——
  archive_verdict.py 已兼容三位置，校验强度不变。
- 披露义务照旧：GT-informed 注入（fixA/D/G + C）、源码判据修复（fixE/H/I）、
  9149 降级（分母 44）、单轮 caveat、fixF 判据为描述性预期（快照非干预）。

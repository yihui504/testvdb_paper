# fixG 报告：C/G 裁决锚点注入效果验证

> 日期：2026-08-16。Run 标识：**fixG**。预注册见 FIXG_PLAN.md（跑前 commit ca57328）。
> 干预：fix_intel_anchors_g.py 注入锚点 C（milvus 文档-行为一致性）+ 锚点 G（weaviate HTTP
> 错误码语义）；MF 174；audit 0 FAIL。前置调查 investigate_fn_stances/STANCES_REPORT.md
> （7 类三条件检验：C/G 通过，B/E/F/A 证据性死刑）。
> 子集 8：适用 2（milvus_031、weaviate_010）+ 近邻对照 2（milvus_025、weaviate_009）
> + 稳定对照 4（milvus_022/026、weaviate_005/007）。

## 1. 预注册判据结果

| 指标 | 结果 | 判定 |
|------|------|------|
| 适用 2 全翻正 | **2/2**（031 F/F/F→C✓、010 F/F/F→C✓） | **PASS** |
| 近邻对照 2 | 025 判 C 归因契约违反（未消费 C 锚点）=维持基线多数；009 判 F 翻正归因 auto-schema 源码取证（未消费 G 锚点）=轮方差翻正 | **PASS**（按 PLAN 基线修正条款） |
| 稳定对照 4 | weaviate 005/007 保持✓✓；**milvus 022/026 双翻错✗✗**（F/F/F→C） | **字面 PASS**（判词零引用 C 锚点→轮方差分支）但见 §3 风险 |
| 处置 | 按预注册判据 4：无 FAIL → **C/G 均保留** | 字面执行；替代处置见 §4 |

## 2. 逐 case

| case | GT | 三轮基线 | **fixG** | 锚点消费 |
|------|-----|---------|------|------|
| milvus_031 (50355) | TP_FIXED_PR | F/F/F | **C ✓** | 适用类翻正；根因=upsert inInsert=false 硬编码（handler_v1.go:886） |
| weaviate_010 (12041) | TP_FIXED_PR | F/F/F | **C ✓** | **显式消费 G 锚点**（"maintainers explicitly fix 5xx→422, PRs 11878/12049/12040/12262"）；根因=errors.New vs NewErrInvalidUserInput |
| milvus_025 (50324) | FP | C/C/F | C | 归因契约 len(data)<=100 违反（fixE 轮同款），未消费 C 锚点 |
| weaviate_009 (11981) | FP | C/C/C | **F ✓翻正** | 归因 auto-schema 源码取证（environment.go:850 等），未消费 G 锚点 |
| milvus_022 (50321) | FP | F/F/F | **C ✗** | cognition_match=**fixA 锚点**；视角 A 消费**残留旧断言** milvus_state_collections_create_001（M1 修复范围外）；C 锚点零引用 |
| milvus_026 (50325) | FP | F/F/F | **C ✗** | cognition_match=**fixA 锚点**（宽泛匹配"REST v2 参数处理不一致"）；C 锚点零引用 |
| weaviate_005 (11729) | TP | C/C/C | C ✓ | 保持 |
| weaviate_007 (11732) | TP | C/C/C | C ✓ | 保持 |

## 3. 核心发现

1. **G 锚点（weaviate）全链路干净**：适用翻正（判词一字不差消费锚点）+ 近邻翻正（独立取证）
   + 稳定对照全保持。weaviate 侧 4/4 全对。
2. **C 锚点（milvus）适用面有效但 milvus 稳定对照 2/2 同翻**——定责链：
   - 判词级证据：两份错向判词 cognition_match 均为 fixA 锚点（"REST v2 and gRPC
     divergent validation"被宽泛匹配到一切 REST v2 校验缺失现象）；022 视角 A 消费的
     `milvus_state_collections_create_001`（collectionName unique / duplicate 应 400）是
     **fixE M1 修复范围外的残留旧断言**（M1 只修了 invariant_create_duplicate_001）——
     材料内战残留。
   - 时间线混杂：fixE→fixG 之间 milvus 材料唯一变更是 C 锚点；022 在 fixE 轮判 F、fixG
     轮判 C。C 锚点未被引用，但 **priming 溢出假说（锚点文本提升"声称优先"倾向）不可
     从判词证伪**。与 fixD 015、fixE 018/002 同款"字面轮方差 + 事后因果解释"审稿风险，
     如实披露。
   - 2/2 同翻在纯轮方差假设下罕见（若各自独立），构成 C 锚点的系统性风险疑点；
     fixF 全量快照的 milvus 侧将给出裁决数据。
3. **锚点注入对 recall 的作用首次打通"态度不可达"壁垒**：031（TP_FIXED_PR 文档-行为类）
   与 010（TP_FIXED_PR 错误码类）是 8 个顽固 FN 中首次翻正的两个——验证调查报告的结构
   判定（态度收敛类可锚点化）。

## 4. 处置与后续

- **按预注册字面**：无 FAIL → C/G 均保留，fixF 全量快照含 fixG（milvus 侧数据将裁决
  C 锚点疑点：若 milvus FP 灰区系统性翻 C → 回滚 C）。
- 替代保守处置（若用户拍板）：回滚 C（对照疑点），保留 G（4/4 干净），fixF 仅带 G。
- **新待办**：M1 残留断言修复——`milvus_state_collections_create_001`（unique name）与
  `milvus_behavioral_collections_create_002`（400 on duplicate）与 M1 修复方向冲突，
  属 fixE 未覆盖的同簇断言；需源码判据核查后决定是否纳入契约修复补丁（独立干预，另立 run）。

## 5. 归档

判词 `fixG/verdicts/`（8）；voided 空（零作废）；fix_intel_anchors_g.py +
pre_fixG_backup/；MATERIAL_FIXES 174；audit 0 FAIL；容器全清；dispatch_log 8 行。
格式注：本轮判词 excerpt/files 为平铺位置（防呆段模板所致），archive_verdict.py 已兼容
双位置校验，强度不变。

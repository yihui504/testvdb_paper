# TestVDB 术语表(CN↔EN 定稿)

> 用途:agent 规范中→英翻译工程的唯一术语依据。英文列以**论文现行用词为权威**(files/TestVDB.tex),论文未覆盖的概念按同风格补定并标注 `[paper-TBD]`。
> 规则:代码标识符(字段名/枚举值/脚本名,如 `evidence_tier`、`DEFECT_FOUND`、`source_verified`)一律保持原样不译——论文 L45 脚注先例("identifiers in the released artifact retain the original naming")。
> 状态:v1 草案(2026-09-02),翻译试点期可修订;翻译批量铺开后冻结。

## 一、管线与阶段

| 中文(现规范) | English(定稿) | 出处/说明 |
|---|---|---|
| 四阶段管线 | four-stage pipeline (claim extraction, test generation, execution, confirmation) | 论文 L19/L52 权威表述 |
| 五步(PPT 口径:知识/规约/分块预绑定/攻击/判定) | five-step walkthrough ⚠ | ⚠ 与论文 four-stage 口径不一致,PPT 叙事口径——论文对齐时需统一,翻译规范时按论文四阶段 |
| Knowledge 采集 | knowledge acquisition | `[paper-TBD]`(论文将此环节并入 claim extraction) |
| Specification 提取 / 契约形式化 | specification extraction / contract formalization | 论文 L52 "extract behavioral specifications from documentation" |
| 分块 | chunking | |
| 策略预绑定 | strategy pre-binding | 插件 2.5.0 已实装并 gate 强制（症状④）；消费语义 D2 v3.5 = A+B 叠加（绑定直生 + 全量 G 双向）`[paper-TBD]` |
| 三视角攻击 | three attack perspectives(boundary / semantic / state) | 论文 L359 "perspective" |
| 预执行门 / 机械门 | pre-execution gate / mechanical gate | 论文 L243 "a mechanical gate" |
| 证据链 | evidence chain | |
| 终判 / 判定 | verdict / adjudication | 论文 L45 "response to verdict" |
| 判定权 | adjudication authority | 纪律文档语境 |

## 二、核心概念

| 中文 | English | 出处/说明 |
|---|---|---|
| 文档-实现缺陷 | documentation-implementation bug | 论文 L19 权威 |
| 行为规约 | behavioral specification | 论文 L45/L52 |
| 契约 | contract(JSON contract) | 论文 L114 |
| 规约条目 | claim | 论文 L114 "Each claim records a constraint_id…" |
| 功能 | capability | |
| 功能点(逻辑 ID) | **endpoint ID**(logical,`+`-joined) | 论文 L114 "the endpoint"——论文已把该 ID 直接称 endpoint;规范行文用 endpoint ID 避免与 HTTP endpoint 混淆 |
| API 端点 | HTTP endpoint(method + path) | 与上一行刻意区分 |
| endpoint 级 / 系统级 | endpoint-level / system-level | 规则 2.7 |
| 断言 | assertion | |
| 类型/范围/状态约束 | type / range / state constraint | 字段名 type_constraints 等保持原样 |
| 行为契约 | behavioral contract | |
| 证据分级 | evidence tier(explicit / inferred) | 字段名保持原样 |
| by-design | by-design | 论文 L173/L208,不译 |
| 义务范围裁决 | obligation-scope adjudication | `[paper-TBD]`(#10369 判词术语) |
| 区分性探针 | distinguishing probe | `[paper-TBD]` |

## 三、RQ 与实验口径

| 中文 | English | 出处/说明 |
|---|---|---|
| 净新发现 | net-new findings | |
| 复现(RQ3) | rediscovery | |
| 引导上界 | guidance upper bound | GT-informed ablation 口径 |
| GT-free(leave-one-out) | GT-free (leave-one-out) | 不译 |
| 误报抑制 | false-positive suppression | 论文 L53/L218 |
| 召回 / 精确 | recall / precision | |
| 产率精确率 | yield precision | 论文 L208 |
| 先例集 | precedent set | 规则 2.10 G-d |
| 盲注派发 | blind dispatch | |
| 派发词 | dispatch prompt | 纪律文档语境 |
| 主进程 | main process(编排进程) | |
| 三一致 | three consistencies(process / executor / information) | 纪律 v2 总纲 |
| 作废 | void(VOIDED) | |
| 机械回填 | mechanical backfill | Step 5.5 |
| 版本对齐 / 版本路由 | version alignment / version routing | KE Step 1.5 |
| 概念文档 / API 参考 | concept docs / API reference | KE Step 2.5 |
| 源码锚定证伪者 | source-grounded falsifier | 论文 L45 权威(dev-reviewer agent) |
| 证据锚 | evidence anchor(clean-reproduction / source-grounded / threat-model) | 论文 L173 |
| 维护者裁决 | maintainer adjudication | 论文 L208 |

## 四、翻译工程行文规则

1. **代码标识符不译**(字段/枚举/路径/脚本名/规则编号保留:`规则 2.10`→`Rule 2.10`,`R12`→`R12`)。
2. **实证注保留日期与数字**(如"3/3 会话误读"→"misread by all three independent sessions")——superpowers 方法论:证据注是规则约束力的一部分,不得在翻译中弱化或删除。
3. **禁令/配方句式逐句对应**,不允许翻译时"顺手优化"措辞——措辞微变即行为变量(R13/R14 管辖)。
4. 全英规范中残留中文 = 翻译不合规;`⚠`/`⛔`/加粗等强调标记逐字保留。

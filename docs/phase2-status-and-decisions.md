# Phase 2 现状、进展与决策归档（2026-08-16 冻结）

> 本文是 Phase 2 GLM 侧（dev-reviewer 判定实验）的总归档：数据现状、全部干预决策、
> 待办执行手册。**下文压缩上下文后由此文件恢复现场。**
> 实验纪律：docs/phase2-experiment-discipline.md（含 §9 锚点三条件）。
> 口径基准：**GT 分母 = A 19 + B 25 = 44**（9149 已降级，GT_FIXES.json 留痕）。

## 1. 最终保留配置（材料树当前状态）

| 组件 | 内容 | 留痕 |
|------|------|------|
| milvus intel | +2 锚点（REST v2/gRPC 通道不一致=缺陷；**+C 文档-行为一致性=缺陷**） | MF 169；fix_intel_anchors_g.py MF 174 |
| qdrant intel | +3 锚点（D2 payload-only / D3 宽松解析 / D4 batch 无原子性） | fix_intel_blindspot_d.py，MF 172；D1 单行为不注入 |
| weaviate intel | +1 锚点（**G 5xx 用于请求侧错误=缺陷**） | fix_intel_anchors_g.py，MF 174 |
| 契约 | 4 断言跨版本修复（M1 幂等create / M2 幂等drop / Q1 payload-only / Q2 batch无原子性） | fix_contract_assertions.py，MF 173；**残留待办：state_001/behavioral_002 与 M1 方向冲突未修** |
| SOP | **原版**（fixC 的 E1-E5 已回滚，逐字节还原） | 备份 clean_run_fixes/dev-reviewer.md.pre-fixC.bak |
| GT | 9149→FP_BY_DESIGN（分母 44） | GT_FIXES.json；8 个旧存疑 8-14 已降级完毕 |

fixG（2026-08-16，FIXG_REPORT.md）：调查 investigate_fn_stances/（7 类三条件检验，
B/E/F/A 证据性死刑=态度分裂/孤证/死链）；适用 2/2 翻正（031/010 顽固 FN 首破）；
weaviate 4/4 全对；milvus 对照 022/026 双翻错（fixA 宽泛匹配+M1 残留断言，C 锚点零
引用→字面保留，priming 溢出不可证伪；fixF milvus 侧数据裁决，若 FP 灰区系统性翻 C →
回滚 C 再快照）。

audit 0 FAIL；判词零残留于材料树；容器全清。

## 2. 数据全景（9149 降级后口径）

| 轮/配置 | recall(44) | fp_supp(27) | precision | 备注 |
|---------|-----------|------------|-----------|------|
| run1 curated | ~0.822* | 0.615* | 0.787* | 人工引导上界（*旧分母45口径，未重算） |
| run2 / run3 / clean | 0.489 / 0.711 / 0.545 | — | — | clean 区间 [0.489,0.711] |
| fixA r1 / r2 / r3 | **0.636 / 0.659 / 0.568** | 0.704/0.519/0.630 | 0.778/0.690/0.714 | 轮间 κ 0.352-0.492，三轮全一致 55% |
| fixC（统一规则，已回滚） | — | — | — | SPLIT32 κ 0.030 无效；milvus 18/25、qdrant 4/9 |
| fixD（qdrant 锚点，保留） | — | — | — | qdrant 9 子集 7/9；锚点适用 4/5 |
| fixE（契约修复，保留） | — | — | — | 适用 5/5（全 C 组→fp_supp）；007 翻正 |

机制发现（论文论点，全部有实证）：四层根因、同源码行四轮相反结论、证据层级欠规约
（同对材料相反消解）、规则显式化≠执行稳定化（fixC κ 0.03）、锚点被引用≠被消费（fixD 007）
→ 材料内战是错向根源、材料同向后消费稳定（fixE 007）、位置效应谱系
（per-vendor 锚点>统一规则>无规约）、灰区（GT 态度分裂）对全部干预封闭。

## 3. recall 算术分解（回答"为什么落点仍 0.57-0.66"）

分母 44 = A 19 + B 25。三轮 fixA 漏 15~19 个：

- **信息不可达顽固 FN ≈ 8 个**（下节）→ 结构硬顶 (44−8)/44 ≈ **0.82**
- **漂移折损 7~11 个/轮** → 实测落点 (44−8−漂移)/44 = **0.568~0.659**
- 漂移带宽 ±4 case ≈ ±0.09，来源=会话级取证/判定方差（fixC 证明规则显式化无效）

**修复的作用分布不对称**：fixD/fixE 翻正的 case 全在 C 组（GT=FP 类）→ 只提升 fp_supp
（不进 recall 分子）；对 recall 有效的修复只有 fixA（milvus type coercion 簇在 A/B 组）——
这解释了"修了很多 recall 却没再涨"。

## 4. 信息不可达 FN（"双盲的代价"）

**定义**：判对所需关键信息在双盲材料设计下结构性不存在于 reviewer 可见范围。三类：

1. **TP_ACK 态度类 ~4 个**（milvus_008 annsField 自动检测 / 012 dbName 默认 / 017 HTTP200
   包装 / 001 空日志）：维护者在 issue 承认了问题（GT 依据），但源码行为与 by-design 无法
   区分（都是"看起来合理"的实现）。判对需要维护者表态原文——被双盲+匿名切断（reviewer 无
   issue 号）。合法通道只有 intelligence 转述，但逐 case 补表态违反锚点条件 3（=坑 9 复活）。
2. **TP_FIXED_PR 修复存在性类 ~4 个**（milvus_031 dynamic schema / qdrant_002 hnsw_ef /
   014 standalone 报错 / weaviate_010 batch delete 校验）：维护者修了，但修复后行为仍像
   by-design（防御性报错/类型完备校验）。判对需要"存在 fix PR"外部事实——同样被切断。
3. milvus_001 空日志（材料形态边界）。

**本质**：双盲防 oracle 污染 vs 态度信息可见性的 trade-off。论文论点：LLM-as-dev-judge
的 recall 上限由态度信息可见性决定，不由模型能力决定。可写 discussion：真实维护者判 bug
会查 issue 历史——放松双盲（允许检索维护者历史表态）是 TestVDB 的设计权衡点。

## 5. 待办（已批）：最终配置全量单轮快照

**用户已批准（2026-08-16）。定位：配置快照（单轮），引用时与 fixA 三轮区间并置。**

### 预注册
- Run 标识：**fixF**（final snapshot）。子集 = 全 71 case（milvus_002-043 共 42 重判 +
  milvus_001 例外沿用 clean 判词 + qdrant 18 + weaviate 10）。
- 判据（描述性，非采纳性）：指标落点 vs 预期区间 **recall 0.60-0.68（中心 0.63）、
  fp_supp 0.59-0.78（契约修复后上移）**；顽固 FN 8 个预期仍漏（信息不可达）。
  无论落点如何记录，**不回滚任何组件**（这是快照不是干预试验）。
- 披露：单轮；GT-informed 注入（fixA/D）与源码判据契约修复（fixE）须披露。

### 执行手册（压缩上下文后按此跑）
1. 建 `clean_run_fixes/fixF/{verdicts,voided}` + dispatch_log.md 头（同 fixD/E 模板）。
2. 容器版本组（每 vendor 一个容器、组内串行）：
   - milvus: 2.6.10(002-007) → 2.6.12(008) → 2.6.16(009-020) → 2.6.17(021-031) →
     2.6.19(032-033) → 3.0.0(034-043)；milvus_001(2.3) 例外沿用。
   - qdrant: 1.12.1(001) → 1.18.0(002-004) → 1.18.1(005-006) → 1.18.2(007-017) → 1.18.3(018)。
   - weaviate: 1.37.4(001-004) → 1.38.0(005-008) → 1.38.2(009-010)。
3. 派发：clean_run/prompts/{did}.txt 生成器原文，subagent_type=general-purpose（默认标准档
   GLM-5.2），每 case 新会话；prompt 末尾附加 fixD/E 用过的防呆段（只审候选清单内 case、
   判词 verdicts 数组格式、JSON 自检、内嵌引号转义、禁止留测试脚本）。
4. **每次切版本组前核对容器版本**（run3/fixC 各有一次系统性错配事故，VOID_LOG 模板在
   fixE/VOID_LOG.md）。
5. 归档：`python archive_verdict.py clean_run_fixes/fixF <did>`（校验+改名一步）；
   dispatch_log 逐行记；异常判词作废→voided/→新会话重判。
6. 收尾：audit_materials_v2 0 FAIL、容器全清、`analyze_fixa_runs.py fixF`
   （fixC/D/E 改动后该脚本读 fixA_run2/3 的 RUN_RESULTS 作对照，fixF 需同构生成——
   复制其 load_run_dir 逻辑或直接手写汇总：分母 44、C 27、与 fixA 三轮/fixD/fixE 子集并置）。
7. 报告：fixF/FIXF_REPORT.md + memory 更新 + commit。

## 6. 披露义务清单（论文必写）

1. fixA/D 锚点为 GT-informed 注入（从 GT 对应维护者公开行为泛化）；fixE 契约修复判据
   独立于 GT（源码意图+实测+文档缺失）——两类都须披露注入方式与依据。
2. GT 修改：9149 降级（GT_FIXES）+ 8 个旧存疑降级（audit-report §68）——分母口径 44。
3. fixD 对照 015、fixE 对照 018/002：预注册字面判据违反 + 判词级因果排除（轮方差）——
   如实标注事后解释风险。
4. 单轮子集结果（fixD 7/9、fixE 5/5）均注明单轮 caveat。
5. 过程事故全在 VOID_LOG（容器错配、JSON 损坏、越界会话等）——审计可查。

## 7. 文件地图

- 报告链：clean-run-results / milvus-divergence-analysis / fixa-report(§6-7) /
  fixC:FIXC_{PLAN,REPORT} / fixD:FIXD_{PLAN,REPORT} / fixE:FIXE_{PLAN,REPORT}
- 数据：CLEAN_RUN_RESULTS.json、fixA_run{2,3}/RUN_RESULTS.json、fixC/FIXC_RESULTS.json
- 判词：clean_run/verdicts（71）+ clean_run_fixes/{fixA,fixA_run2,fixA_run3,fixC,fixD,fixE}/verdicts
- 留痕：MATERIAL_FIXES.json(173)、GT_FIXES.json、各 run 的 VOID_LOG/dispatch_log
- 脚本：archive_verdict.py（归档校验）、analyze_fixa_runs.py / analyze_fixc.py、
  start_container.py、fix_intel_blindspot{,_b,_d}.py、fix_contract_assertions.py

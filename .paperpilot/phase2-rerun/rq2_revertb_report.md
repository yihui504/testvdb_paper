# RQ2 revertb 报告：契约回退方案 B + 一致性元规则（2026-08-23）

## 动机与决策链（用户拍板，2026-08-23）

1. v9 的 7 条考古契约断言按锚定来源重新定性：**issue 锚定 = GT 同源 = in-sample
   拟合点**（milvus_033 issue 51085 实证、milvus_012 issue 49889 转述、qdrant_018
   OpenAPI caveat 语义推断）；纯文档锚定 5 条（008/013/038/qdrant_016/部分 012）
   保留，定性为无 GT 工程修复
2. **方案 B 激进回退**：撤除全部 3 条 issue 锚定断言
3. **新增判定层一致性元规则（规则 5/6）**作为类三的无 GT 替代路径（镜像挖掘侧
   generalization_shapes / interface_parity 策略）
4. 附带修正：014/028 同族 FP 定性从"过拟合代价"改为**类别边界 FP**（现象无法
   区分维护者态度；即使无 GT 写的通用规则同样会错，非 in-sample 校准独有）

## 执行时序（防 in-sample 留痕）

| # | 动作 | 留痕 |
|---|------|------|
| 1 | 规则 5/6 测试先行（10 例 RED） | tests/test_adr0008_pipeline.py::TestMechanicalBConsistencyRules |
| 2 | 实现（GREEN，13/13 含回归） | 主插件 commit **0d1c8f0**（message 声明元逻辑设计依据，先于任何回测） |
| 3 | 契约回退（撤 3 断言 + passport 重算） | MATERIAL_FIXES.json #177；备份 revert_b/backup/ |
| 4 | 机械全量重判（回退后基线） | tmp_gen/reverted_A.json / reverted_B.json |
| 5 | 三案 builder 重做（含对照取证义务） | 链文件重写 + 旧链备份 revert_b/backup/chains/ |
| 6 | 三组 auditor 复审（机械预跑注入） | 各组 debate_logs/chain_verdicts_revertb.json |

## 终态数字

| 口径 | recall | precision | fp_supp | TP/FP/FN/TN |
|------|--------|-----------|---------|-------------|
| v7.x（无注入 headline） | 0.705 | 0.775 | — | 三轮中位 |
| v9（注入口径，issue 锚定含 3 拟合 TP） | 0.909 | 0.889 | 0.815 | 40/5/4/22 |
| **revertb（回退后）** | **0.841** | **0.881** | **0.815** | **37/5/7/22** |

- 机械层：verdict_A 26 CONFIRMED / 18 REFUTED / 27 NEUTRAL（v9 为 47 案预定案
  → 44；三案如预期落灰区）
- **规则 5/6 全局触发 0 案：零误触发（precision 零扰动），但也未抓回任何案**
  （原因见发现 ②）

## 三案逐案对比（v9 vs revertb）

| 案 | v9 判定（issue 锚定撑起） | revertb 判定（无 GT 证据链） | FN 的证据基础 |
|----|--------------------------|------------------------------|----------------|
| milvus_012 | DEFECT（TP） | NOT_DEFECT，root_cause=mundane_api_semantics | handler_v2.go:356-367 显式 dbName=="" → DefaultDbName 回退；文档无空串拒绝表述 |
| milvus_033 | DEFECT（TP） | NOT_DEFECT，root_cause=request_param_typo | vectorFieldType 非 REST API 参数（Go/gin 丢弃未知键）；真实枚举面 dataType/idType 均有校验拒绝；**D 命中既有锚点 #50351（非注入）** |
| qdrant_018 | DEFECT（TP） | NOT_DEFECT，root_cause=approximate_by_design | 源码 exp: 2*estimated/3 硬编码折扣（注释 "assuming 1/3 deleted"）；文档明文 "might be unreliable" 无精度承诺 |

三案 auditor 全程无 rework（rework=n）；#9255 回归自检通过；第 4 查对应性
无漂移（018 的 claim 25 vs raw log 24 如实转记）。

## 关键发现

1. **回退的链级不彻底性（过渡态假象）**：撤断言后链内 quote 仍残留 builder 转抄
   的"应拒绝"声称，使机械 B 规则 2 对 milvus_012 误触发 CONFIRMED——其依据实为
   已撤的 issue 锚定内容。builder 重做（链重写）后消失。教训：**材料回退必须
   连同引用该材料的链一起重做**，否则撤除物经链内转抄继续生效。
2. **规则 5 靶面措辞窄于实际取证形态**：033 的替换证据是 describe 返回
   FloatVector（从结果推断替换），观测行不含 substituted/default 语义词，
   规则 5 不触发。规则设计时锚定"服务器自述替换"形态，未覆盖"前后对照推断
   替换"形态。**未现场改规则**（单案回调 = 重蹈 in-sample）；若扩展词表须
   先测试后实现并另行留痕。
3. **D 视角既有锚点正常工作**：033 的 SUPPORTS_NOT_DEFECT 来自 cognition 原始
   锚点 #50351（issue 语料自然提取，非 GT 注入）——灰区裁决的认知通道在无注入
   口径下独立贡献了判定。
4. **三案 FN 均有可指认的无 GT 证据链**（源码原文 + 文档原文 + 现象解释），
   与 v9 的 3 个 TP（issue 锚定断言 + violates=True）形成对照：**两者的差异
   不是判定能力差异，是"判定基础（文档契约+源码）与 GT 来源（维护者态度）
   的系统错位"在这三案上的具体体现**——维护者认 DEFECT 的三个行为，在无 GT
   信息下均有平行的 by-design/框架层解释存活。
5. **精确率零扰动确认**：规则 5/6 全局 0 触发（71 案），回退不动 FP 侧——
   0.881 vs 0.889 的微小差异全部来自 TP 分母变化。

## 论文口径建议

1. revertb（0.841/0.881）取代 v9 作为**注入口径的干净版本**：注入物只剩
   纯文档锚定断言（5 条）+ 认知锚点（4 个 FP 侧）+ 机械预跑——全部可辩护为
   无 GT 路径。v9 的 0.909 仅作为"issue 锚定上限"在 ablation 里引用并明示
   3 案拟合
2. 三案 FN 进 limitations 作为"文档契约范式覆盖极限"的实证：配本文逐案
   证据表（每个 FN 都有源码级平行解释）
3. 规则 5/6 作为"一致性元契约"路线的**已实现、零误伤但靶面受限**的第一步
   写入 discussion：发现 ② 的措辞窄点 + 018 型语义精度偏差不覆盖，是下一步
   扩展方向（替换语义推断型靶面）
4. 发现 ① 的过渡态假象作为方法论教训写入附录（材料注入类实验的撤除协议
   必须含链级清理）

## 产物清单

- 规则 5/6：主插件 commit 0d1c8f0（含测试/实现/agent 规范同步）+ cache 同步
- 回退脚本：tmp_gen/revert_b.py（备份 revert_b/backup/）
- 重做链 ×3：各 SESSION_DIR evidence_chain/（旧链备份 revert_b/backup/chains/）
- 判词 ×3：各组 debate_logs/chain_verdicts_revertb.json
- 机械基线：tmp_gen/reverted_A.json / reverted_B.json

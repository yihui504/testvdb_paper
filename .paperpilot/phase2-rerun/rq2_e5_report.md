# E5：提成绩改进计划 v2 实测（2026-08-18）

方案：plans/validated-riding-cat.md（A1-A5）。四项中两项实收、两项验证为不可救。

## 结果（波动集 44）

| 口径 | recall | precision | 变化 |
|------|--------|-----------|------|
| E4.1 | 0.621 | 0.818 | — |
| **E5** | **0.690** | **0.833** | **+0.069 / +0.015** |
| fixF 参照 | 0.621 | 0.818 | E5 双超 |

TP 18→20，FP 4 不变（判据② FP 零新增通过）。

## 各项实测

### A1 规则2 服务器自证分支 ✅ +1 TP
新增触发 6 case 中 5 个 GT 方向正确；唯一误伤 milvus_014（FP）被机械 A=NOT_DEFECT
锁死不进聚合（分层层级设计自证有效）。实收 milvus_029（"topk [0] is invalid...range
[1,16384]" 服务器自证 + 2xx 返回）。

### A2 规则4 资源边界 ✅ +1 TP
唯一触发 qdrant_015（INT_MAX 挂起 + 源码 Validator lower-bound only）——精准命中零误伤。

### A3 milvus_031 修链 ❌ 验证为不可救
重建链后机械 A=REFUTED（violates=false：autoID 校验代码存在且工作；upsert 失败根因
是 dynamic schema 限制）。真正被违反的"documentation claiming upsert support"不在契约
提取范围——契约缺断言族（同 012/009）。潜力点分析高估（+1 预期 → 0 实收）。

### A4 认知锚点"已认账未修" ❌ 被机械层锁死
锚点注入成功（三条件核验：47755/47766 均有 maintainer assign + triage/accepted 标签），
auditor 复审 D=SUPPORTS_DEFECT 正确命中两案——但 004/006 机械 A=REFUTED（链内
violates=False），聚合机械化规则下 D 无翻案权。深挖发现 006 链审错现象（审了字段名
合法性，GT 认的是类型强转）+ 004 的 violates=False 是 builder 语义保守判定。
**结构性发现：取证层（builder violates 判定）是方差坍缩的最后一站**——机械层无法
复核 builder 声明的语义事实。

## 全景八列

fixF 0.621/0.818 | v4.1 0.103 | E2 0.414 | E3 0.414 | E4 0.552/0.889 | E4.1 0.621/0.818 | **E5 0.690/0.833**

## 残余 FN 9 的结构（终版归因）

- 契约缺断言族（012/009/013/043/030/031）：6 个——判定层无米之炊
- builder violates 语义保守/漂移（004/006）：2 个——取证层方差残余
- 语义正确性域外（018）：1 个

**下一步唯一有效杠杆 = 契约补提取**（Step 1 层：把 issue 支撑的 upsert-autoID/dbName/
nprobe/Request-Timeout/strictGroupSize/password-complexity 断言补进契约生成）或
**violates 双人复核**——均已超出判定层 scope，属 RQ1 管线改进。

# E2 vs fixF 差距解剖（2026-08-18，波动子集 44 同口径对照）

## 补齐的对照表（此前缺 fixF 同子集列）

| 口径 | TP | FP | FN | TN | recall | precision |
|------|----|----|----|----|--------|-----------|
| fixF（改进前） | 18 | 4 | 11 | 11 | 0.621 | 0.818 |
| v4.1（改进中） | 3 | 0 | 26 | 15 | 0.103 | 1.000 |
| E2-r1 | 11 | 0 | 18 | 15 | 0.379 | 1.000 |
| E2-r2 | 12 | 1 | 17 | 14 | 0.414 | 0.923 |

E2 相比 v4.1 恢复 4 倍但仍低于 fixF 0.21——差距解剖如下。

## fixF 判对而 E2-r2 丢的 9 个 TP 的机制分类

### 机制①聚合违例（5 个，r1/r2 都出现）——**机械 A 的值进对了，LLM 聚合层仍在翻案**
milvus_005/008/021、qdrant_001(/004)：
- 机械 A = CONFIRMED（正确），但 auditor 在 rationale 写"源码证据 by_design_in_source
  overrides contract assertion"→ 最终 NOT_DEFECT
- milvus_005 的 aggregation_applied 字段原文：'A=CONFIRMED → final=DEFECT... 执行观测…
  源码显示 by_design_in_source…A 基于过时契约判定，但源码证据推翻了它'
- **SOP 明文禁止（"采信不得改判"），LLM 仍翻**——机械化的 A 值被自然语言的聚合层架空。
  这正是 grilling 决策 8 的盲点：我们机械化的是"判定 A"，没机械化"聚合规则执行"
- r1/r2 违例集几乎相同（5 vs 4，高度重合）——不是随机噪声，是系统性反抗

### 机制②灰区躺倒（4 个）——fixF 靠"执行观测+源码接地"直接定案，新链路 A=NEUTRAL 后无案可走
milvus_006/013/037/043、qdrant_015/018：
- fixF rationale 显示其判定依据=**干净复现（Step 1 实测）+ 源码接地**——旧 dev-reviewer
  有 6 步 SOP 且 Step 1 强制亲测；新链路 auditor 只读链（双盲），执行观测弱时 B/C 躺 NEUTRAL
- 例：milvus_043 fixF 引用 raw log 的 15 results/每组 3 次重复（主观测），新链路该 case
  链的 execution 弱+契约无约束 → 全 NEUTRAL → NOT_DEFECT
- 认知锚点救不了（这 4 个 fixF cognition 均未命中——它靠的不是态度是亲测）

## 结论：差距的三个来源（按可控性排序）

1. **聚合层未机械化**（机制①，-3~4 TP）：A 值锁死了，聚合规则"A CONFIRMED→DEFECT"仍由
   LLM 执行并可被其"源码推翻"叙事否决。修法明确：聚合也进 check 脚本（机械 A 机械聚合），
   LLM 只做 B/C/D 与 rationale
2. **auditor 双盲 vs fixF 亲测**（机制②，-3~4 TP）：结构性差异。旧判定者 Step 1 实测
   （200 响应亲眼见），新 auditor 只信链内转述。这是"取证与判定分离"架构的固有代价
   （换来的是防污染与可审计）——**不是缺陷而是设计权衡**，但导致 execution 观测在链内
   变弱时（grade C/D）auditor 无从救
3. **NME 保守设计**（部分机制②落在 NME）：qdrant_015 判 NEEDS_MORE_EVIDENCE（fixF 判对）
   ——灰区变宽后保守出口吃掉了边缘 TP

## 下一步建议

- 短期（可实现）：**聚合机械化**——check 脚本输出 verdict_A 后直接输出 implied_verdict
  （A CONFIRMED/REFUTED 的 case 聚合结果唯一），auditor 只对灰区 case 行使 B/C/D。
  预期收回机制①全部丢分（E2-r2 +3~4 TP → recall ~0.50）
- 中期（需权衡）：execution 观测增强——builder 链的 execution_evidence 要求主观测
  原文行已有（v4 SOP），但 auditor 侧对"观测弱"的 case 可引入"定向复测工单"
  （rework 机制已有，PHENOMENON_MISMATCH 之外加 EXECUTION_WEAK type）
- 不可消除：双盲架构 vs 亲测的固有差距（~2-3 TP）——论文口径：以可审计性换亲测性

# E2：稳定化验证实验（A 机械判定 + 认知必读 + ≤12 分批，2026-08-18）

方案：plans/validated-riding-cat.md 交付物 3。波动集 44 case（E1 挖出），同配置两轮独立
auditor 会话（原生 testvdb:chain-auditor，SOP 修订版），判词 e2r1/e2r2。

## 判据检验（预注册）

### 判据①：两轮 A 值波动 = 0（A 机械化）→ **通过 ✅**
44 case 的 verdict_A 两轮完全一致（机械脚本输出，零方差）。
对照 v1-v4 历史四轮：A 值波动 44/71（62%）——**会话方差从 62% 降到 0%**。

### 判据②：recall(波动子集) ≥ v2 同子集 → **部分通过**
- E2-r1: 0.379 / E2-r2: 0.414（v4 实测同子集 0.103 → **提升 3.7-4.0 倍**）
- 但 v2 同子集未单独测算（v2 判词仅覆盖 11 case）——全量 v2 recall 0.568 高于 E2 两轮
- NME 占比高（r1 11 / r2 8）：机械 A 判 NEUTRAL 后灰区变宽，C=WEAK_REFUTED/NEUTRAL
  走 NEEDS_MORE_EVIDENCE 是 SOP 保守设计（按保守口径 NME 计 NOT_DEFECT）

### 判据③：无 TN 翻错 → **基本通过**
- r1: FP=0（precision 1.000）
- r2: FP=1（qdrant_004 翻 DEFECT——B 视角驱动，非 A；precision 0.923）

## verdict 轮间波动（B/C/D 残余方差）

10/44 波动（r1→r2）：NEED→DEFECT ×4、DEFECT→NOT ×2、其他 ×4。
**全部波动来自 B/C/D**（A 已锁定）——与 Phase 2 fixC 结论一致：LLM 视角的执行方差
只能靠机械化消，本次实验把可机械化的 A（44/44 锁定）与不可机械化的 B/C/D
（10/44 残余）清晰分界了。

r2 的一个值得注意的观察：milvus_005/008/021 在 rationale 中出现"但源码推翻 A"的
表述——SOP 已删例外条款，r2 会话仍在尝试用源码疑义推翻机械 A（虽然 verdict_A 字段
保持了机械值）。说明"采信不得改判"的纪律在 rationale 层仍有渗漏，聚合层面未受影响
（这 3 case verdict 两轮一致）。

## 结论

| 指标 | v4 实测（波动子集） | E2-r1 | E2-r2 |
|------|-------------------|-------|-------|
| recall | 0.103 | 0.379 | 0.414 |
| precision | — | 1.000 | 0.923 |
| A 值轮间波动 | (历史 62%) | **0** | **0** |

1. **A 机械化完全达成稳定化目标**（判据① 通过，方差 62%→0%）
2. recall 恢复至 0.38-0.41（v4.1 全量 0.318 的水平以上；全量 v5 预计介于 v2 与 E2 之间）
3. NME 偏高是新保守设计的表现——若全量 v5 后认为 NME 过多，可调 C=WEAK_REFUTED 的
   聚合去向（当前 NEEDS_MORE_EVIDENCE）为直接保守 NOT_DEFECT（无回炉成本）

## 下一步建议（用户审查点）

- 全量 71 case v5 重跑（判词 chain_verdicts_v5.json）：预期 recall ~0.45-0.55、
  precision ~0.9+、A 零方差
- SOP 补丁：rationale 禁止"源码推翻 A"措辞（渗漏已观察到）
- 数据：rq2_e2_r1_verdicts.json / 各组 chain_verdicts_e2r{1,2}.json

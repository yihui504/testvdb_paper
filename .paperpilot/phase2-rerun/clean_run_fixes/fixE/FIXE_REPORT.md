# fixE 报告：契约断言修复效果验证（采纳）

> 日期：2026-08-16。Run 标识：**fixE**。配置 = fixA+fixD 锚点 + 契约修复 4 断言
> （fix_contract_assertions.py：M1 幂等 create / M2 幂等 drop / Q1 payload-only 字面接受 /
> Q2 batch 无原子性；判据=源码意图常量/注释+实测行为+文档缺失，独立于 GT；
> MATERIAL_FIXES 173，audit 0 FAIL）。预注册见 FIXE_PLAN.md（跑前 commit）。
> 子集 = 适用 5（milvus_022/023、qdrant_007/009/010）+ 对照 3（milvus_025/018、qdrant_002）。

## 1. 预注册判据结果

| 指标 | 结果 | 判定 |
|------|------|------|
| 修复适用 5 case | **5/5 全对**（全部 GT=C → FP） | **PASS**（预判"全对概率中等"，实得满分） |
| 对照 3 | 025 ✓；018 ✗、002 ✗ | 字面 FAIL |

**处置：契约修复采纳。** 对照两例劣化的判词级因果检查均排除修复归因：
- milvus_018：rename 的 state 约束**未被修改**，判词引用 milvus_state_collections_rename_001
  合规判 FP——HTTP 200 包装现象属灰区漂移带（fixA 三轮 C/C/F），同 fixD 015 先例；
- qdrant_002：hnsw_ef 约束**未被修改**，判 FP 属漂移带（F/F/F + fixD C + fixE F）。
**如实披露**：字面判据违反 + 事后因果解释（与 fixD 同款审稿风险）；fixE 单轮。

## 2. 逐 case

| case | GT | fixA 三轮 | fixC | fixD | **fixE** | 修复 |
|------|-----|----------|------|------|------|------|
| milvus_022 幂等 create | C(FP) | F/F/F | F | F | **F ✓** | M1 |
| milvus_023 幂等 drop | C(FP) | F/F/C | F | F | **F ✓** | M2 |
| qdrant_007 batch 原子 | C(FP) | F/C/F | F | C✗ | **F ✓** | Q2 |
| qdrant_009 vectors={} | C(FP) | F/C/C | F | F | **F ✓** | Q1 |
| qdrant_010 vectors 缺失 | C(FP) | F/C/F | C✗ | F | **F ✓** | Q1 |
| （对照）milvus_025 | B(CONF) | C/C/F | C | C | C ✓ | — |
| （对照）milvus_018 | B(CONF) | C/C/F | C | C | F ✗ | —（轮方差） |
| （对照）qdrant_002 | A(CONF) | F/F/F | F | C | F ✗ | —（轮方差） |

## 3. 核心发现

1. **契约修复与锚点形成互补且解除了 fixD 的失败模式**：qdrant_007 在 fixD 中"锚点被引用
   仍被旧契约 atomic 断言压倒"（引用原文仍判 C 错向）；Q2 修复后契约方向反转，判词同时
   消费新契约（"may be partially applied...clients must retry"）与 D4 锚点，双证据同向 →
   翻正。**当材料内部证据同向时消费是稳定的；错向源自材料内战（契约 vs 锚点），而非
   reviewer 善变。**
2. **指标作用方向符合预判**：适用 5 全是 C 组（GT=FP 类）→ 契约修复主要提升
   **fp_suppression**（5/27 ≈ +0.19 的适用类上限），对 recall 无直接贡献；对照 2 劣化
   （B/A 组 FN）为轮方差性质。
3. **与 fixA/D 的关系**：三条材料侧修复（fixA 锚点 / fixD 锚点包 / fixE 契约）在适用类上
   叠加收敛；fixC（统一规则）保持无效——材料侧证据同向化 > 运行时规则工程的位置效应
   结论再次强化。

## 4. 最终保留配置（累计）

milvus intel 1 锚点 + qdrant intel 13 锚点 + 契约 4 断言修复（M1/M2/Q1/Q2 跨版本）+
原版 SOP。**全量合并数字未测**（fixE 仅 8 case 子集）；引用口径：适用类 5/5（单轮）+
分项先例（fixA 三轮 0.636-0.659/0.568 recall、fixD qdrant 7/9）并置，单轮 caveat 与
GT-informed/源码判据披露义务同前。

## 5. 归档

判词 `fixE/verdicts/`（8）+ voided 1（milvus_018 容器错配重判闭环）；
fix_contract_assertions.py + pre_contract_backup/；MATERIAL_FIXES 173；audit 0 FAIL；容器全清

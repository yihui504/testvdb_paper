# v7 机械层采信回测（方案 1 验证 + 更深发现，2026-08-19）

## 起因

FN 归因显示 ~6 案因 builder violates 自检退化丢失，假设"机械 B 缺资源上限规则"。回测推翻了该假设的表述方式——**规则不缺，缺的是 auditor 执行**。

## 发现 1：资源上限规则已存在且正确触发

`check_physical_constraints.py` 规则 4（资源边界，A2 2026-08-18 已落地）对 qdrant_015 实际输出：
`verdict_B=CONFIRMED (资源边界): 合法值触发挂起（status=None）且源码校验器无上界`

但 v7 auditor 判词自报 B=NEUTRAL——**没跑脚本或没采信**。

## 发现 2：机械层采信率量化（71 案全量重跑两个脚本）

| 对照项 | 不一致数 | 说明 |
|--------|---------|------|
| 机械 A vs auditor 自报 A | **18/71** | 含 5 案机械=CONFIRMED 被报 NEUTRAL、2 案机械=REFUTED 被报 CONFIRMED |
| 机械 B=CONFIRMED 未采信 | **8/71** | 机械 B 共触发 23 案，8 案 auditor 自报非 CONFIRMED |

典型案例 qdrant_015：链 constraint_id 为逗号拼接串 → 机械 A 实际 NEUTRAL(absent)/GREY_ZONE；机械 B CONFIRMED → 按 SOP 应聚合 DEFECT（=GT ✓）。auditor 自报 A=REFUTED/B=NEUTRAL，机械层整体被架空后自行落判 NOT_DEFECT。**SOP 写了"运行确定性脚本并采信"，无监督时 LLM 不执行**——与 builder violates 自检退化同构。

## 发现 3：模拟"严格采信机械层"的指标（71 案）

聚合口径：机械 implied∈{DEFECT,NOT_DEFECT} 直接定案；CONFLICT→保守 NOT_DEFECT；GREY_ZONE+机械B CONFIRMED→DEFECT；其余灰区维持 v7 LLM 判定。

| 口径 | recall | precision | fp_supp |
|------|--------|-----------|---------|
| v7 实测 | 0.614 | 0.794 | 0.741 |
| **模拟严格采信** | **0.727** | 0.762 | 0.630 |

翻案 12 案：**翻对 7 / 翻错 5**（净 +5 TP / +3 FP）。

翻对 7 案的机械来源：HTTP语义恒真×2（milvus_002/030）、机械A CONFIRMED×3（006/031/qdrant_004）、资源边界×1（qdrant_015）、类型恒真×1（weaviate_007）。
翻错 5 案：FP 侧误伤 3（014=B语义规则、021/009=A机械 CONFIRMED）+ TP 侧丢失 2（024=A机械 REFUTED、weaviate_010=CONFLICT 保守）。

CONFLICT 4 案（007/029/qdrant_010/weaviate_010）v7 里无一遍历 rework 闭环（auditor 直接自判）——闭环机制也被架空了。

## 结论与建议

1. **"补资源上限规则"不需要**——规则已在，正确触发
2. **真正对症：机械层强制执行**。两个落地选项：
   - a) 主进程预跑：把两个脚本输出直接注入 auditor 派发词（auditor 只解释不计算）——最稳，无 LLM 服从性问题
   - b) 主进程后校验：判词 A/B 值与机械输出 diff，不一致拒收重派——保留 auditor 自主性但多一轮往返
3. **trade-off 需拍板**：严格采信 recall +0.113 但 precision -0.032、fp_supp -0.110。挖掘场景（E 系列一贯 recall 优先）倾向接受；若 precision 敏感则需先收紧 A 机械的 quote 匹配（021/009 误伤源于 violates 语义边界）
4. 方案 2（builder 主观测 HTTP 语义归档指引）价值下降：029 的 http_semantics 字段其实已正确标注，机械规则也已触发——问题同样在采信端

## 产物

- `rq2_v7_mechA_recheck.json` / `rq2_v7_mechB_recheck.json`（71 案机械重跑原始输出）
- 本报告 `rq2_v7_mechbacktest.md`

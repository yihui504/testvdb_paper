# qdrant 3 可救 FN 补证实验结果（2026-08-18）

方案：按 E4 判词的 rework_order 派 builder 补证（014/015 补源码搜证、016 修引文），
auditor 复审（chain_verdicts_e4b.json）。

## 结果：3 个均未翻正，但补证揭示了"不可救"的真实原因

| case | 补证发现 | 复审 verdict | 不可救根因 |
|------|---------|-------------|-----------|
| qdrant_014 | log 只测了 /cluster/recover，**无 create-collection 请求**；源码显示 standalone 500 是显式守卫（service_error("Qdrant is running in standalone mode")） | NOT_DEFECT | 探针测错目标 + 源码 by-design |
| qdrant_015 | range 校验器只有 min=1 **无上界**，INT_MAX 通过校验 → 2^31 AHashMap 分配挂起（真缺陷但是 availability 类） | NME | 缺陷类不在四类 B 判据域 |
| qdrant_016 | 契约无 on_disk_payload 专用约束；log 测的是 lookup_from 没测 on_disk_payload；源码侧字段必含于 GET config | NOT_DEFECT | 探针测错目标 + 引文修正后无违反 |

## 归因收口：E4 与 fixF 的 recall 差距（-0.069）最终分解

1. **材料层错位（Phase 2 探针测错目标）**——014/016 类：GT 判 TP 的依据（issue 现象）
   与探针实测的不是同一操作。判定层无论多强都无法救回错位的证据。~2-3 case
2. **缺陷类覆盖缺口（availability 类）**——015 类：无上界导致资源耗尽挂起是真实缺陷
   （维护者修复），但不属于数值下界/枚举闭集/互斥/类型恒真/HTTP 语义五类。
   SOP 可增第六类"资源边界"（上界缺失 + 大值挂起观测）——这是可行的下一步
3. **双盲 vs 亲测架构代价**——fixF 靠 Step 1 亲测定案的部分 case

## 结论

补证不是这 3 个 case 的解药——它们的证据材料本身就是错位的。E4 的 0.552/0.889
是当前 SOP 判定域内的稳定成绩；追平 fixF 需要动材料（重做探针）或扩判据域
（资源边界类），两者都是论文层面的决策而非 bug 修复。

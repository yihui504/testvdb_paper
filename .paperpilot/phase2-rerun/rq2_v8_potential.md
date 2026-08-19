# v7.x 后改进点分析（2026-08-20）

## 基线：v7.x 三轮中位 0.705/0.775，稳定错误 = FN 12 + FP 9（其中 8 个 FP 三轮全错）

## FN 12 的机械层卡点分桶（跑当前脚本实测）

| 桶 | case | 机械状态 | 根因 | 可改进性 |
|----|------|---------|------|---------|
| **契约缺断言** | 008(COSINE>1)/012(dbName)/013(Timeout)/033(vectorFieldType)/038(group_by)/qdrant_016(lookup)/qdrant_018(count) | A=GREY_ZONE(absent) ×7 | 契约真无对应约束 | ★★★ 文档考古批量补（已验证方法论，7 个≈7 个 issue 各自考古） |
| **violates 误标** | 001(search fail)/003(ef)/004(filter)/024(mutual excl) | A=NOT_DEFECT(violates=False) ×4 | builder 语义保守判定 | ★★ violates 复核已就位但未在 v7 闭环——suspicious 打回后 builder 复核换约束即可 |
| **CONFLICT 悬置** | 029(limit=0→200) | A=CONFLICT | 闭环三轮上限内未收敛 | ★ 单案，走完闭环即收 |

## FP 9 的结构（更值得注意）

**6/9 是 A=DEFECT 机械锁定**——链内"契约有约束+violates=True+源码 validation_absent"
技术事实链完整，但 GT 判 BY_DESIGN（维护者态度）。这不是判定错误而是**口径分裂**：
- milvus_011(query null filter)/027(shardsNum)/qdrant_009(vectors={})/weaviate_009([] vector)
  —— "接受非法值"技术成立，维护者按宽松文化不认
- milvus_021/028 链内 src=by_design/validation_absent 混合
**改进方向不是"修判定"而是消口径分裂**，两个选项：
1. **认知锚点扩充**（GT-informed 需披露）：qdrant payload-only 已有锚点但 auditor 判
   "盲区非显式 by-design"——锚点措辞升级为显式 stance 引用（同 fixD 形态）
2. **论文口径声明**：FP 9 按"技术事实 vs 维护者态度"分裂呈现，不改判定——
   这本身是 RQ2 的核心发现（doc-implementation inconsistency 的判定语义讨论）

## 优先级建议

1. **契约补提取批量化**（FN +7 潜力，recall →0.80+）：7 个 issue 各自文档考古。
   可再半自动化：写考古辅助脚本（issue 时间线→docs repo commit 检索→修复前快照拉取）
2. **violates 复核闭环激活**（FN +4 潜力）：v7 轮该机制就位但 suspicious 案没有走打回
   （builder 复核换约束）——下一轮激活即可
3. **FP 口径决策**（用户拍板）：锚点扩充（提 precision 至 0.9 但 GT-informed）或口径
   声明（不改，论文呈现分裂）——建议后者+前者小规模（qdrant payload-only 措辞升级 1 案试试）
4. **archaeology 半自动化脚本**（工程性）：重复劳动工具化

## 理论上限速览

全部兑现：TP 32+7+4+1=44/44 → recall 1.0（不现实，考古有失败率）
保守兑现：+8~9 TP、-3 FP → recall ~0.83 / precision ~0.86

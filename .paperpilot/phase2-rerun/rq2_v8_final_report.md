# v8 完整报告：文档考古 + FP 侧锚点闭环（2026-08-20，commit a47bcd7+4ee83c1）

## 两阶段终态

| 口径 | recall | precision | fp_supp |
|------|--------|-----------|---------|
| v7.1（起点） | 0.727 | 0.780 | 0.667 |
| 阶段1（+考古7案） | 0.886 | 0.812 | 0.667 |
| **v8 终态（+FP闭环4案）** | **0.886** | **0.867** | **0.778** |

TP 39 / FP 6 / FN 5 / TN 21。recall +0.159、precision +0.087、fp_supp +0.111。

## 阶段2 保守合规设计（三层）

1. **合规前提**：4 案 milvus FP 均有官方 resolution/by-design 标签 + maintainer
   yanliang567 文字表态（双信号，三条件核验通过——先例 fixD 同性质，论文披露）
2. **指纹级匹配**（check_anchor_conflict.py）：只认锚点显式声明的 fingerprints
   词组全部在场——三轮校准史：词重合 23 误命中→标识符 1 漏→fingerprints 6 含 2 误
   →精修 4/4 零误伤。无 fingerprints 的旧锚点不参与（防语义泛化）
3. **不直接翻案**：锚点命中只降 CONFLICT 走闭环——auditor 同物判定
   （019/021 同物→NOT_DEFECT 引 quote；027 误配→维持 DEFECT 保守正确）

## 阶段2 小测（防回归）

- recall 0.886 零回退 ✓（TP 39 不变）
- precision 0.812→0.867（FP 9→6，全部来自锚点同物案）✓
- 机械层全量零扰动（fingerprints 4 案外无命中）✓
- tests 166 passed ✓

## 残余错误

FN 5：violates 误标族 ×4（001/003/004/024）+ 029 CONFLICT 悬置 ×1
FP 6：011（GT 内部矛盾——issue 是 accepted 但 GT 判 FP）+ qdrant_009/010/weaviate_009
（无 by-design 明示标签，不合规不注入——保守边界）+ 027（auditor 判误配维持）

## v8 全景位置

v4.1 0.103 → E2-E6（机械化+闭环）→ v7 0.614（无人值守全量）→ v7.1 0.727（机械注入）
→ **v8 0.886/0.867（考古补断言+锚点闭环）**。E2E6 的 0.793 是子集口径不可比。

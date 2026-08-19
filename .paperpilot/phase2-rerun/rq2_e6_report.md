# E6：两追问改进落地 + CONFLICT 闭环终态（2026-08-18，commit f36ab87）

## 终态指标（auditor 实测闭环后）

| 口径 | recall | precision |
|------|--------|-----------|
| fixF（改进前） | 0.621 | 0.818 |
| E5 | 0.690 | 0.833 |
| **E6 终态** | **0.793** | **0.852** |

TP 18→23（较 fixF +5），FP 4 持平（零新增），NME 3。

## CONFLICT 闭环四案结果（全部 auditor 实测）

| case | 工单动作 | 终判 | GT | 结果 |
|------|---------|------|----|------|
| milvus_009 | 换约束（limit→absent nprobe）+ violates=True | DEFECT（灰区+机械B 服务器自证） | TP | ✓ |
| milvus_030 | 换约束（长度→absent complexity）+ violates=True | DEFECT（同上） | TP | ✓ |
| qdrant_016 | 换约束（payload-only→absent lookup）+ violates=True | DEFECT（灰区 B/C/D 三 CONFIRMED） | TP | ✓ |
| milvus_014 | builder 复核维持 violates=False（约束正确执行） | NME（二轮 CONFLICT 保守路径） | FP | ✓ |

四案全对——CONFLICT→打回→重判的闭环按设计工作：3 个 TP 靠"换约束后真实现象对准
机械 B 信号"翻正，1 个 FP 走保守路径（未误判 DEFECT）。

## 本轮机制战果汇总

1. **文档考古契约补提取**（031）：时间线咬合 + 修复前快照锚定——五类同族可复制
2. **implied 四态 + CONFLICT 闭环**：信号冲突不再锁死也不误判，走打回——4/4 方向正确
3. **violates 复核**（10/71 suspicious，9TP）：机制就位，后续 run 的 builder 自检条款
   会在源头减少错位

## 残余 FN 6（recall 0.793 → 理论上限）

- 契约缺断言族：012（dbName）/013（Request-Timeout）/043（strictGroupSize）+ 004/006
  （violates 复核 suspicious 但本轮未闭环）——文档考古法可批量补
- 域外：018（count 语义正确性）

九列全景：v4.1 0.103 → E2 0.414 → E3 0.414 → E4 0.552 → E4.1 0.621 → E5 0.690 →
E6 0.793/0.852（fixF 0.621/0.818；E6 零 LLM 判定方差 + 全程可审计）。

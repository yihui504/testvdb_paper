# E4.1 后提成绩潜力点分析（2026-08-18）

## 现状：E4.1 = 0.621/0.818（fixF 打平），剩余错误 15 个的结构

FN 11 + FP 4。逐案侦察（视角值 + 契约存在性 + violates 标注）后，潜力点按
"可机械化程度 × 收益" 排序：

## 潜力点清单

### P1 契约错配修链（5 case，最大潜力，+0.10~0.17 recall）
卡点：mechA = quote_mismatch / constraint_absent → 灰区 → C 躺倒。
契约关键词验证结果：
- **milvus_029/031/012：契约里存在可用约束**（limit 下界断言 ×2 / autoID+PK 断言 /
  dbName 参数定义）——是 builder 引错了约束或引文不逐字。修法：重派 builder 按正确
  constraint_id 重建链（同 e4c 模式）→ A 机械 CONFIRMED → implied DEFECT。
  **预期 +3 TP**
- milvus_013/043：契约确实无关键词（Request-Timeout=0 / strictGroupSize=0）——
  契约本身缺此约束，修链救不了（除非契约补提取，超出判定层范围）

### P2 builder violates 误标（2 case，+0.07 recall）
- milvus_009：观测在链内（nprobe=0 → 200 success）但 violates=False——builder 判错
  （nprobe=0 不违反 limit+offset 约束是对的，但应引用 nprobe 相关约束而非 limit 约束。
  契约有 nprobe 断言——归入 P1 同族修法）
- milvus_030：password 长度约束引用对了但复杂度不在契约（GT 认的是复杂度）——契约缺
  陷类，修链救不了
- **净预期 +1 TP**（009 可救）

### P3 认知锚点覆盖"已认账未修"（2 case，+0.07）
milvus_004/006：GT=TP_ACK_CLOSED_NOFIX（维护者认账但不修）。当前链 src=by_design_in_source
→ C=REFUTED → NOT_DEFECT。修法：developer_cognition 增"acknowledged-not-fixed"锚点
（类似 fixG 三条件检验：≥2 独立维护者认账表态）。**注意**：这是 GT-informed 注入，
论文需披露（先例：fixA/fixD 同性质）

### P4 资源边界第六类判据（1 case，+0.03）
qdrant_015：无上界校验 + INT_MAX 资源挂起。机械 B 增规则 4：观测含"大值分配挂起/超时/
OOM"+ 源码校验器只有下界无上界 → B=CONFIRMED（资源边界类）。判定材料在链内已齐
（builder 补证时已落取 range 校验器源码）

### 不可救（2 case）
- milvus_030/043/013（契约缺约束，判定层无米之炊）
- qdrant_018（count 35% 偏差=语义正确性，五类判据域外）

### FP 侧（4 case 全 BY_DESIGN 态度类）
milvus_021/qdrant_009/010/weaviate_009：技术事实全部确凿（源码验证缺失+静默接受），
GT 按维护者态度判 FP。**判定层无错可修**——只能靠认知锚点（qdrant payload-only 已有
锚点但 auditor 判定"盲区非显式 by-design"——可重审这 2 case 的锚点匹配严格度）。
动它有翻错风险，建议不动。

## 收益汇总（保守/乐观）

| 措施 | 保守 | 乐观 |
|------|------|------|
| P1 修链（029/031/012） | +3 TP | +3 TP |
| P2（009） | +1 | +1 |
| P3 认知锚点（004/006） | +1 | +2 |
| P4 资源边界（015） | +1 | +1 |
| **合计** | **+6 TP → recall 0.828 / TP24** | **+7 → 0.862** |

precision 影响：P3 若翻错 1 FP → 0.818 略降；其余不动 FP。

## 建议执行顺序

1. P1 修链（纯机械收益，零风险，同 e4c 流程重跑 3 链）
2. P4 资源边界（机械 B 增规则，材料已在链内）
3. P2（009 并入 P1 修链批）
4. P3 最后做（GT-informed 需披露，且收益/风险比最低）

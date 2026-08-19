# 小实验：fixF→v2 / v2→v4.1 成绩差异归因（2026-08-18）

## 实验设计与结果

### P1 材料一致性审计 ✅ 排除
fixE 契约断言修复（M1 幂等create / M2 幂等drop / Q1 payload-only / Q2 batch 原子性）在
v4 材料树（tvdb_sessions）中全部存在且与 fixF 同版（fix_contract_assertions.py 改的就是
V2=tvdb_sessions 树；'idempotent'×8/'payload-only'×2 特征文本确认）。**材料不是变量。**

### P2 判定者输入差异对照——发现结构性差异 ⚠️
旧 dev-reviewer（fixF）：developer_cognition 是**必读人格包**（判定全程带维护者态度），
27/70 case（39%）判词显式消费认知锚点。
新链路 v4：认知只在视角 D 灰区查一次——63/71 NO_SIGNAL，仅 8 case 有信号（11%）。
**旧判定者"带着维护者脑子"判案；新链路只在最后灰区问一次。这是 fixF recall 优势的
主要来源（GT 本身按维护者态度标注——判定者与 GT 共享态度先验）。**

### P3 丢失 TP 的链级分解（10 case）——发现决定性证据 🎯
v2/v3 判 DEFECT → v4.1 判 NOT_DEFECT 的 10 个 case，链的 source_grounding 迁移：
- not_found→by_design_in_source ×3（002/003/005：v4 builder 找到 nprobe=0 默认替换等显式代码——取证变真）
- not_found→validation_absent ×4（039/040/041/042：**链证据变强**，REST 字符串转数字确认无校验）
- validation_present→not_found ×2（035/037：v4 builder 没找到 v3 找到的校验代码——取证遗漏）
- not_found→not_found ×1

**决定性发现（039-042 四 case）**：v3 与 v4 的链 contract_grounding **完全一致**
（同 constraint_id、同引文、violates=True、契约中 id 与引文均实际存在），
但 v2 auditor 判 A=CONFIRMED、v4 auditor 判 A=NEUTRAL——
**同一 SOP、同一条链、两个 auditor 会话判出相反视角 A。**

## 结论：成绩差异的三层归因

| 层 | 贡献 | 证据 |
|----|------|------|
| **1. 判定者- GT 态度对齐**（fixF 0.659 vs v2 0.568 的主因） | 结构性 | 旧判定者 39% case 消费认知 vs 新链路 11%；GT 按维护者态度标注，谁带态度先验谁占优 |
| **2. auditor 会话方差**（v2 0.568 vs v4.1 0.318 的主因） | 执行性 | 同链同约束 v2 判 A=CONFIRMED / v4 判 A=NEUTRAL；SOP 是自然语言，视角 A 的"引证核对后 PERIOD 规则"执行不稳定（与 Phase 2 fixC 结论同构：规则显式化≠执行稳定化） |
| **3. 取证变真**（真实贡献，方向不定） | 双向 | 3 case 挖到 by-design 显式代码（-3 TP）；4 case 链更强但被 auditor 方差吃掉；2 case 取证遗漏（-2 TP） |

## 推论
- v4.1 的 0.318 **低估**了新链路真实能力——它叠加了 auditor 会话方差（层2）的负向抽样
- v2 的 0.806 precision 是可信的（A/B 视角规则在那个会话执行得好）
- 新链路要追平 fixF 的 recall，缺的不是机制而是**判定口径与 GT 的对齐声明**（技术事实 vs 维护者态度）或 auditor 的稳定化（机械 Grep 核对代替自然语言 SOP 判 A）

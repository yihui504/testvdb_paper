---
name: consistency-check
description: 全文内部一致性检查（缩写/术语/数据数字/主张/交叉引用/记号冲突）。投稿前、跨节大改后、多作者合并稿件时用。是 xept:check-submission 的专项补充（后者范围更广，本技能专挖内部矛盾）。
---

# Consistency Check（全文一致性检查）

扫全文找内部一致性问题。报告论文不同部分间的冲突。

## 何时用
- 用户说"检查一致性"、"找矛盾"、"核实数据"
- 投稿前（补充 `xept:check-submission`）
- 跨多节的大改后
- 合并多作者贡献时

## 检查类别

| 类别 | 查什么 | 问题示例 |
|------|--------|----------|
| 缩写 | 同缩写定义不一；先用法后定义；定义后未用 | "DNN" 在第 3 节 = "Deep Neural Network"，第 5 节 = "Deep Nonlinear Network" |
| 术语 | 同概念不同名；大小写不一 | 同一物时而 "our model" 时而 "our framework" 时而 "our system" |
| 数据数字 | 同指标不同值；百分比加不齐；表与文不符 | 摘要 "95.3% accuracy"，表 2 "94.8%" |
| 主张 | 矛盾表述；无支撑最高级 | 引言 "first to propose X"，related work "following prior work on X" |
| 交叉引用 | 引了不存在的图表号；交叉引用错配（**dangling ref/unused label 先跑 [check_refs_labels.py](../../scripts/check_refs_labels.py) 脚本查**） | "as shown in Figure 5" 但只有 4 张图 |
| 记号 | 同符号表不同物；数学记号不一 | $n$ 在第 3 节 = 样本数，第 4 节 = 特征数 |

## 工作流
```
1. `read` 全文 LaTeX 源（所有 .tex）
2. 对每类扫并交叉核对：
   a. 建缩写登记表：找所有 \ac{}、缩写定义、或内联 "(X)" 定义
   b. 建术语映射：识别关键概念及其所有叫法
   c. 抽所有数值主张：百分比、计数、测量——映射到位置
   d. 抽关键主张：贡献、新颖性陈述、对比
   e. 查交叉引用：**先跑 `python scripts/check_refs_labels.py <main.tex 或目录>`** 查 dangling ref（引不存在的 label = 编译错误）/ unused label（确定性 I/O，脚本化）；再 LLM 查图表号 vs 正文描述的语义配对（"see Figure 5" 真有 5 张图否）
   f. 建记号登记表：数学符号及其定义
3. 各类内交叉核对冲突
4. 生成报告
```

## 输出格式
生成结构化报告并交给用户：
```markdown
# Consistency Check Report

**Date**: [检查日期]
**Files scanned**: [.tex 文件列表]

## Summary
- Found: X issues (Y critical, Z minor)

## Issues

### Abbreviations
- [位置] 问题描述
  - Section 3, line 42: "DNN (Deep Neural Network)"
  - Section 5, line 198: "DNN (Deep Nonlinear Network)"
  - **Suggestion**: 统一为一个定义，仅首次定义

### Data & Numbers
- [位置] 问题描述
  - Abstract: "achieves 95.3% accuracy"
  - Table 2: "94.8%"
  - **Suggestion**: 核实正确值并更新两处

### [其他有问题的类别...]

## No Issues Found
- [无问题的类别]
```

## 相关技能
- `xept:check-submission`：投稿前全面检查（一致性是其一类，本技能更深）
- `xept:reduce-ai`：降 AI 痕迹
---
name: design-table
description: 生成学术级对比表格的 LaTeX 代码（booktabs+cellcolor 自动标注最优/次优/最差），插入主 .tex。智能高亮（少 3 行或差异<1% 不上色）。仅生成 LaTeX 表格代码片段。
---

# Design Table（设计对比表格）

生成学术级对比表格，自动用颜色标最优/最差值。生成 LaTeX 代码片段，用 `edit` 插入主 `.tex`。

## 配色方案（清新淡色系）

| 含义 | 颜色 | RGB |
|------|------|-----|
| 最优 (Best) | 薄荷绿 | (200, 245, 205) |
| 次优 (2nd Best) | 柠檬黄 | (255, 249, 196) |
| 最差 (Worst) | 珊瑚粉 | (255, 205, 210) |
| 次差 (2nd Worst) | 蜜桃色 | (255, 224, 195) |

## 工作流
```
1. 分析用户数据 — 理解表格结构、分组、指标列
2. 生成 LaTeX 代码片段（booktabs + cellcolor 高亮）
3. 检查 preamble — 确保有必需 \usepackage
4. 用 `edit` 插入 — 插到主 .tex 合适位置
5. 后续修改 — 改数据/颜色直接 `edit` 已插入代码
```

## Step 1: 分析用户数据
识别表格结构：
- **列名** (headers)
- **分组** (groups)：按类别分组，组间横线分隔
- **数值列** (highlight_columns)：哪些列含需对比的数值
- **排序方向** (highlight_mode)：越大越好 (max) 还是越小越好 (min)

### 智能高亮决策
别盲目给所有数值列上色。判断：
- 数据 <3 行 → 不高亮（对比不明显）
- 列内数值差异 <1% → 不高亮（不显著）
- 用户没特别要求强调 → 只高亮最关键指标列
- 用户明确指出某些格 → 手动指定

## Step 2: 生成 LaTeX 代码
直接生成 booktabs + xcolor 表格代码（替代原平台 制表 MCP 工具）。结构示例：

```latex
\definecolor{cellbest}{RGB}{200,245,205}
\definecolor{cellsecond}{RGB}{255,249,196}
\definecolor{cellworst}{RGB}{255,205,210}

\begin{table}[htbp]
\centering
\caption{Performance Comparison of Detectors on Datasets}
\label{tab:comparison}
\small
\begin{tabular}{llcccc}
\toprule
Type & Detector & Accuracy & Precision & Recall & F1 \\
\midrule
\multirow{2}{*}{Static-Based}
 & OSSGadget & 53.87\% & 50.41\% & 91.56\% & 65.02\% \\
 & GuardDog  & \cellcolor{cellbest}93.97\% & \cellcolor{cellbest}96.99\% & 89.92\% & \cellcolor{cellbest}93.32\% \\
\bottomrule
\end{tabular}
\end{table}
```
按 highlight_mode 给每列最优（max/min）的格上 `cellbest`，次优 `cellsecond`。

## Step 3: 检查 Preamble
表格需两个包：
```latex
\usepackage[table]{xcolor}
\usepackage{booktabs}
```
缺则 `edit` 在 `\begin{document}` 前插入（多行表格还需 `\usepackage{multirow}`）。

## Step 4: 定位并插入
- 用户指定位置 → 照办
- 表格标题有编号（如 Table 2）→ 找对应 Results/Experiments 节
- 文档有 `\input{}` 分章 → 找对应章节文件
- 默认 → 插到 `\section{Experiment}`/`\section{Results}` 后合适位置

## Step 5: 后续修改
插入后所有修改直接 `edit` 已插入的 LaTeX：
- 改数据：改格内数值
- 改高亮：加/删 `\cellcolor{cellbest}` 等
- 改颜色：改 `\definecolor` 行的 RGB

## 重要规则
- **直接生成 LaTeX 表格代码**（替代原 制表 MCP 工具）
- **不生成独立文件**——代码片段插现有文档
- **数据组织**：每行第一列留空，group name 自动填第一行（用 `\multirow`）
- **智能高亮**：不必要时不加色，<3 行或差异 <1% 自动跳过
- **后续可改**：插入后所有修改用 `edit`
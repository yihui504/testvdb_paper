# 表格设计规范

## 通用原则
1. **三线表**：使用 booktabs 包（\toprule, \midrule, \bottomrule），禁用竖线
2. **对齐**：数字右对齐或小数点对齐，文字左对齐，表头居中
3. **caption 在上方**：\caption{...} 放在 \begin{tabular} 之前
4. **单位在表头**：如 Accuracy (%) 而非在每个数字后加 %
5. **不要太挤**：\setlength{\tabcolsep}{6pt} 调整列间距
6. **行间距**：\renewcommand{\arraystretch}{1.1} 略微增大

## 模板

### 标准三线表
\usepackage{booktabs}
\begin{table}[t]
\caption{Description of the table.}
\label{tab:example}
\centering
\setlength{\tabcolsep}{6pt}
\renewcommand{\arraystretch}{1.1}
\begin{tabular}{lcc}
\toprule
Method & Metric A & Metric B \\
\midrule
Baseline 1 & 78.3 & 0.76 \\
Baseline 2 & 81.5 & 0.80 \\
\textbf{Ours} & \textbf{86.2} & \textbf{0.85} \\
\bottomrule
\end{tabular}
\end{table}

### 多行分组表（multirow）
\usepackage{booktabs, multirow}
\begin{table}[t]
\caption{Grouped results.}
\label{tab:grouped}
\centering
\begin{tabular}{llcc}
\toprule
\multirow{2}{*}{Category} & \multirow{2}{*}{Method} & \multicolumn{2}{c}{Metrics} \\
\cmidrule(lr){3-4}
 & & Precision & Recall \\
\midrule
\multirow{2}{*}{Group A} & Method 1 & 85.2 & 79.1 \\
 & Method 2 & 87.4 & 81.3 \\
\midrule
\multirow{2}{*}{Group B} & Method 3 & 82.1 & 83.5 \\
 & Method 4 & \textbf{89.0} & \textbf{85.7} \\
\bottomrule
\end{tabular}
\end{table}

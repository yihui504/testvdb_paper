---
name: design-figure
description: 用 matplotlib 生成学术论文级数据图（柱/折线/散点/箱线/热力/雷达/训练曲线/t-SNE 等 16 类），存 PDF 矢量图到 figures/ 并自动插入 \includegraphics。仅数据图；架构/流程图等结构图用 xept:design-diagram。
---

# Design Figure（画数据图）

用 matplotlib 生成学术论文级数据图，存 PDF 矢量图到项目根 `figures/`。

**注意**：本技能仅用于数据图（柱状、折线、热力等）。架构图、流程图等结构图用 `xept:design-diagram`（TikZ）。

## 工作流
```
1. 分析用户数据 — 理解数据、定图表类型
2. 写 matplotlib 脚本（`write`）— 经 `pwsh` 运行生成 PDF
3. 自动插入文档 — 立即用 `edit` 插入 \includegraphics，不要问用户
4. 后续调整 — 改颜色/标签重跑脚本即可
```

## 色板选择

| 色板 | 场景 | 风格 |
|------|------|------|
| default | 通用对比 | 蓝橙绿红（经典学术） |
| nature | Nature 风格 | 红青绿蓝（鲜明对比） |
| pastel | 温和呈现 | 柔和淡色系 |
| cool | 自然/地球色系 | 墨绿青黄橙 |
| blue | 单色渐变 | 深蓝到浅蓝 |
| warm | 暖色渐变 | 深红到浅红 |

## 支持的图表类型（16 种）
1. **bar** 柱状 / 2. **grouped_bar** 分组柱 / 3. **stacked_bar** 堆叠柱 / 4. **horizontal_bar** 横向柱
5. **line** 折线 / 6. **scatter** 散点 / 7. **box** 箱线 / 8. **violin** 小提琴
9. **heatmap** 热力/Confusion Matrix / 10. **radar** 雷达 / 11. **pie** 饼/环
12. **area** 面积 / 13. **histogram** 直方 / 14. **training_curve** 训练曲线（带误差带）
15. **tsne** t-SNE/UMAP 降维 / 16. **pareto** Pareto 前沿

## 生成方式
写一个 matplotlib 脚本（如 `figures/gen_<name>.py`），`write` 保存后 `pwsh` 运行 `python figures/gen_<name>.py` 输出 `figures/<name>.pdf`。脚本要点：
- `import matplotlib.pyplot as plt`，按选中色板设 `plt.rcParams`/cycle
- 默认 6×4 英寸，`plt.tight_layout()`
- `plt.savefig('figures/<name>.pdf', bbox_inches='tight')`（矢量 PDF）
- 学术整洁：去顶右边框、合理字号、无 chartjunk

## 自动插入文档
生成后**立即**用 `edit` 把 figure 环境插入文档，不要问"要不要插入"或"插哪"。

### 插入步骤
1. `read` 文档找合适位置
2. 查 preamble 是否有 `\usepackage{graphicx}`，没有就 `edit` 加
3. `edit` 插入完整 figure 环境：
```latex
\begin{figure}[htbp]
\centering
\includegraphics[width=\linewidth]{figures/<name>.pdf}
\caption{根据上下文生成合适的 caption}
\label{fig:<name>}
\end{figure}
```
4. caption 据图表内容与论文上下文自动撰写
5. label 用有意义名（如 `fig:f1_comparison`）

## venue 感知图宽（借 harness-anything 的「期刊图表规范」概念）

生成前 `read` `.self_xept/project.yml` 的 `venue`，按期刊定 `figsize` 宽度（高度 ≈ 宽度 × 0.6，按数据类型微调）：

| venue 族 | 单栏宽 | 双栏宽 |
|---------|--------|--------|
| Nature / Science | 89mm (3.5in) | 183mm (7.2in) |
| IEEE | 88.9mm (3.5in) | 181.8mm (7.16in) |
| ACM（两栏会议） | 84.6mm (3.33in) | 177.8mm (7.0in) |
| Elsevier | 90mm (3.54in) | 190mm (7.48in) |
| Springer | 84mm (3.31in) | 174mm (6.85in) |
| 未知/无 venue | 6in（默认） | 6in（`\linewidth` 自适应） |

- `figsize=(宽_in, 宽_in*0.6)`，`plt.savefig(..., bbox_inches='tight')`
- 插入时 `\includegraphics[width=\linewidth]`（单栏图占满列宽，双栏图占满整页）
- 未设 venue 就不查表，用默认 6×4in 并 `\linewidth` 自适应，别硬套

## 重要规则
- **写 matplotlib 脚本经 `pwsh` 运行**生成 PDF（替代原平台画图 MCP 工具）
- **仅用于数据图**——架构/流程图用 `xept:design-diagram`
- **生成后立即插入**——不问用户，直接找位置插
- **默认 PDF**——矢量，LaTeX 效果最好
- **后续修改**——改数据/颜色重跑脚本即可
- **图片尺寸**——默认 6×4 英寸，按需调整
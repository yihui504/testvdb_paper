---
name: design-diagram
description: 用 TikZ 生成论文级结构图（架构图/流程图/时序图/数据流图/状态图 5 类），存 PDF 矢量图到 figures/ 并经 xelatex/pdflatex 编译验证后插入 \includegraphics。用于用户要"画系统架构图/流程图/时序图/状态机/数据管线/框架图"，或 xept:design-figure 判明是结构图非数据图时调用。仅结构图；数据图（柱/折线/热力）用 xept:design-figure；对比表格用 xept:design-table；可交互 HTML 系统图（网页/演示）不在 xept 场景，属 archify 类工具的领地。
---

# Design Diagram（画结构图）

用 TikZ 生成论文级结构图，存 PDF 矢量图到项目根 `figures/`，编译验证后插入论文。

> **核心规则：编译是验证收据。** 每次改动后必须 `latexmk` 重编译；exit 非零绝不当作成功；两轮聚焦修复仍不收敛就如实报告未解诊断，别交付一个没编过的图。

## 何时用

- 用户要架构图 / 流程图 / 时序图 / 状态机 / 数据管线 / 框架图 / 系统总览
- `xept:design-figure` 判明这是**结构图**（组件/关系/流程），不是数据图

## 何时不用（真实边界）

- 数据图（柱/折线/散点/热力/训练曲线）→ `xept:design-figure`
- 对比表格 → `xept:design-table`
- 可交互、可搜索、可深链的 HTML 系统图（网页演示/README 展示卡）→ 用 archify 类工具，**不是** xept 论文场景
- 照片/渲染图/截图 → 直接 `\includegraphics`，本技能不生成

## 类型路由（选对图）

| 类型 | 论文用途 | TikZ 方案 |
|------|---------|-----------|
| `architecture` 架构 | 组件/服务/存储/信任边界 | `positioning` + 分层矩形 + `fit` 边界框 |
| `workflow` 流程 | 管线/审批/工具调用/CI | `chains` + 菱形决策（`shapes.geometric`） |
| `sequence` 时序 | API 调用链/异步/缓存回退 | 手动 participant 泳道（列节点 + 箭头） |
| `dataflow` 数据流 | ETL/lineage/敏感数据边界 | 数据节点 + 流向箭头 + 虚线敏感边界 |
| `lifecycle` 状态 | 状态机/重试/终止态 | `automata` 库（状态圆 + 转移箭头） |

不确定用哪种时，写一个最小骨架跑一遍，图类型错了立刻能从节点/关系形状看出来。

## 创作不变量（借鉴 archify，映射到 TikZ）

- **一条明显主路径**；侧分支从**最近的主路径节点**引出。低价值边先删，别加路由控制。
- **主节点 ≤ 12**（论文图）；支持细节放 caption 或正文，别靠加边堆。
- **稀疏标签**：边标签只在端点无法自明时才加（协议/动作/方向/跨边界机制）。
- **先写产物再谈布局**：下一步动作必须是 `write` 候选 .tex，别在散文里计划坐标。
- **颜色克制**：1 个中性色 + 1 个强调色；去阴影、去 3D、去渐变、去 chartjunk。
- **仅标准库**：`positioning` `arrows.meta` `shapes.geometric` `calc` `fit` `automata` `backgrounds`——不依赖 `pgf-umlsd`/`tikz-uml` 等外部包（省安装负担）。

## 工作流

> 本质行：**选类型 → 写 .tex → 编译 → 修错 → 插入**。

### Step 1: 写独立 .tex
用 `standalone` 类（开发期迭代快、无页码干扰），`write` 到 `figures/<name>.tex`：
```latex
\documentclass[tikz,border=2pt]{standalone}
\usetikzlibrary{positioning,arrows.meta,shapes.geometric,calc,fit,automata,backgrounds}
\begin{document}
\begin{tikzpicture}[
  node distance=8mm and 12mm,
  box/.style={draw, rounded corners=1pt, minimum height=6mm, font=\small},
  arr/.style={-{Stealth[length=2mm]}},
]
% 主路径从左到右；侧分支就近挂靠
\end{tikzpicture}
\end{document}
```
节点用中文/英文按论文语言；正文 `\small`；`node distance` 给足呼吸。

### Step 2: 编译验证
`pwsh` 跑编译，exit 非零读 `.log` 修错重编。**PDF 出来前不算完成。**

- 中文/UTF-8 节点标签 → `xelatex -interaction=nonstopmode figures/<name>.tex`
- 纯 ASCII 标签 → `pdflatex -interaction=nonstopmode figures/<name>.tex`
- `latexmk` 可用时优先（自动多遍）；**MiKTeX 缺 perl 时 latexmk 会报 "could not find the script engine 'perl'"——直用 xelatex/pdflatex 单遍即可**（standalone 结构图单遍够，无书目无交叉引用）

### Step 3: 插入主文档
`edit` 插入 figure 环境（与 `xept:design-figure` 同契约）：
```latex
\begin{figure}[htbp]
\centering
\includegraphics[width=\linewidth]{figures/<name>.pdf}
\caption{据上下文生成}
\label{fig:<name>}
\end{figure}
```
preamble 缺 `\usepackage{graphicx}` 则补。

### Step 4: 两轮收敛
每次只改被诊断的局部。若连续两轮没让错误数下降，停，如实报告未解诊断与当前 log 关键行——不硬凑。

## 按类型的 TikZ 要点

- **architecture**：用 `box` 节点 + `right=of`/`below=of` 分层；信任边界/模块分组用 `fit` 包虚线框；外部依赖标虚线节点。
- **workflow**：`chains` 或手摆节点；决策点用 `diamond`；主路径水平，异常分支向下/向上。
- **sequence**：每个参与者一列节点（垂直生命线），消息用 `arr` 箭头 + 可选标签；无外部包，纯 positioning。
- **dataflow**：源→变换→存储→消费者；敏感数据边界用 `dashed` 框圈出。
- **lifecycle**：`automata` 的 `state` + `->`；终态双圈；可恢复状态用 `failure` 转移回到活跃态。

## 集成

- **上游**：`xept:design-figure` 判明结构图后转交本技能；`xept:write-paper` 写到需要系统图时调用。
- **下游**：图入论文后走 `xept:check-submission`（图表合规）与 `xept:compress-images`（若位图多）。
- **编译**：依赖本机 `latexmk`（同 `xept:fix-latex`/`xept:design-slides` 的编译链）。

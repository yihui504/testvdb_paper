---
name: write-poster
description: 制作学术海报（会议/项目展示）。单页多栏布局，突出研究亮点。输出 Beamer 海报（beamerposter 包，.tex 编译成 PDF）。可视化呈现研究要点。
---

# Write Poster（做学术海报）

为会议或项目展示做学术海报。

- 单页多栏布局设计
- 研究亮点的视觉呈现
- 输出 **Beamer 海报**（`beamerposter` 包）`.tex`，`pwsh` 跑 `latexmk` 编译成 PDF

## 工作流
1. `read` 论文——提炼问题、方法、关键结果、贡献
2. 定海报规格（尺寸 A0/A1、横/竖、栏数）——不清则问用户
3. `write` `poster.tex`，用 `\documentclass[final]{beamer}` + `\usepackage[orientation=portrait,size=a0,scale=1.4]{beamerposter}`
4. 多栏布局（`\begin{columns}`），每栏一个内容块（`\begin{block}{标题}`）
5. 关键结果用大字 + 图表突出；文字精简为要点
6. `pwsh` 跑 `latexmk -xelatex poster.tex`，修错至干净

## 内容块（典型）
- 标题/作者/单位（顶部横幅）
- Introduction / Motivation
- Method（配流程图）
- Results（配大图表、关键数字）
- Conclusion / Future Work
- 参考文献（小字）

## 规则
- **远观可读**：标题特大、正文够大（海报是远看的）
- **图为主、文为辅**：能图不表，能表不文字
- **聚焦 3-5 个要点**，勿堆砌
- 配色与图表风格一致

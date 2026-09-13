---
name: design-slides
description: 据论文生成学术汇报幻灯片，输出 Beamer（.tex，编译成 PDF）。10 种布局指引（标题/双栏/结果/定义/流程/转折/案例对比/状态/三路/总结），含主题配色与逐页演讲备注。答辩/组会/会议/分享用。
---

# Design Slides（做汇报幻灯片）

据论文生成结构化汇报幻灯片，输出项目根 **Beamer `.tex`**（`pwsh` 跑 `latexmk` 编译成 PDF）。

> 注：原平台用平台专属 JSON 幻灯片格式由其前端渲染；Claude Code 无该渲染器，改为学术通用的 **Beamer**，可直接编译为 PDF / 转 PPTX。

## 何时用
- 用户要 slides、PPT、presentation、deck、keynote
- 据论文做答辩/组会/分享

## 输出
`write` 项目根 `slides.tex`（Beamer），`pwsh` 跑 `latexmk -xelatex slides.tex` 出 PDF。骨架：
```latex
\documentclass[aspectratio=169]{beamer}
\usetheme{metropolis}              % 或按主题
\definecolor{accent}{HTML}{C73E3A} \setbeamercolor{progress bar}{fg=accent}
\title{...}\subtitle{...}\author{...}\date{...}
\begin{document}
\maketitle
\begin{frame}{...} ... \end{frame}
...
\end{document}
```

## 可用布局（10 种，对应 beamer frame 设计）
1. **title** 开场 / 2. **two-column** 双栏对比（`columns` 环境）
3. **headline-results** 结果展示（带表）/ 4. **definition** 关键概念（带公式）
5. **pipeline** 流程架构 / 6. **pivot** 关键洞察/转折
7. **case-comparison** 案例对比 / 8. **status** 进度（Done/Todo）
9. **three-paths** 决策选项 / 10. **takeaways** 总结

## 主题配色
- **Academic blue**：主 `#0B2545` / 强调 `#4472c4`
- **Warm professional**：主 `#2C3E50` / 强调 `#E74C3A`
- **Nature green**：主 `#1B4332` / 强调 `#52B788`
- **Elegant dark**：主 `#212529` / 强调 `#F77F00`

用 `\definecolor` + `\setbeamercolor` 应用。

## 生成前澄清
1. **场景**——答辩？组会？会议？分享？
2. **受众**——导师？评审？同行？非技术？
3. **时长**——几分钟？（定页数：每分钟约 1-1.5 页）
4. **重点**——方法？实验？创新点？
5. **语言**——中？英？

## 规则
1. **先读论文**——理解内容再生成
2. **典型 8-14 页**（除非用户指定）
3. **每页有演讲备注**——`\note{...}` 或单独备注文件
4. **混用不同布局**——别全塞一种
5. **主题一致**——配色匹配主题/venue
6. 编译验证：`latexmk -xelatex slides.tex`，修错至干净

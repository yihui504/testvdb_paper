# Figure 1 内容规格(TestVDB pipeline 架构图)

给作者在 PowerPoint 中绘制的精确蓝图。画布建议 40×15cm 超宽(LQM approach-overview 同款),双栏论文中占 `\textwidth`。设计语言参考 LQM figures/approach-overview-v2.8.pptx:白底、细线框、①②③④ 编号标题 16.5pt 粗体、文件名 Consolas 棕色(#AC956E)、数据流标签蓝色加粗(#0070C0)、高亮胶囊 #9DC3E6、无大容器色块。

## 必须呈现的内容(审稿人核查点)

R2 5.3 批评现图缺失、必须画出的三点:
1. **stage ④ 内部展开**:evidence builder 与 chain auditor 是两个分离的角色(不是单一比较器),中间是 evidence_chain.json
2. **四个视角**:A contract / B physical / C cognition / D source( auditor 内列出)
3. **implementation source 作为独立外部输入**(不是从 documentation 那条链来的),标注 "falsification anchor — independent of the documentation"(论文核心主张的视觉锚)

## 节点清单(17 个)

| # | 节点 | 文字 | 备注 |
|---|------|------|------|
| E1 | API documentation | 标题粗体 + "natural-language prose" 小字灰 | 外部输入,左上 |
| 1a | knowledge extractor | + 小字 "Crawl4AI · coverage + version checks" | |
| 1b | knowledge.json | Consolas 棕 | artifact |
| 1c | specification extractor | + 小字 "categorize · evidence-tier · verify source" | |
| 1d | specifications.json | Consolas 棕 + 小字 "typed · tiered · level" | artifact |
| 2a | strategy registry | + 小字 "pre-bound: trigger → strategy" | |
| 2b | attack agents | + 小字 "boundary · state · semantic" | |
| 2c | scenario construction | + 小字 "system-level · no-match fallback" | |
| 2g | 5 generation gates | 淡蓝胶囊 #9DC3E6 | 生成侧质量闸门 |
| 3a | Docker-pinned VDBMS | + 小字 "target @ version" | 可画圆柱 |
| 3b | raw HTTP logs | Consolas 棕 + 小字 "+ atomic .done markers" | artifact |
| 4a | evidence builder | 内列五行小字:doc verification / execution evidence / contract grounding / chain trace / source grounding | 绿色系或白框 |
| 4b | evidence_chain.json | Consolas 棕 + 小字 "five sections" | 中介 artifact |
| 4c | chain auditor | 内列:4 mechanical checks;A contract · B physical · C cognition · D source | 与 4a 分离的两个角色 |
| 4d | verdict | "Confirmed / Refuted · Neutral → human review" | |
| E2 | implementation source | 浅蓝底蓝框(全场唯一色块强调)+ "pinned clone · falsification anchor / independent of the documentation" | 外部输入,④ 下方 |

## 边清单(15 条)

| 从 | 到 | 标签 | 样式 |
|----|----|------|------|
| E1 | 1a | — | 实线 |
| 1a→1b→1c→1d | 依次 | — | 实线 |
| 1d | 2a | **constraints** | 蓝 |
| 2a→2b→2c→2g | 依次 | — | 实线 |
| 2g | 3a | **probes** | 蓝 |
| 3a | 3b | — | 实线 |
| 3b | 4a | **outputs** | 蓝 |
| 4a | 4b | — | 实线 |
| 4b | 4c | — | 实线 |
| 4c | 4d | — | 实线 |
| 4c | 4a | rebuild ≤3 | **虚线回环** |
| E2 | 4a | source grounding | 蓝虚线 |
| E2 | 4c | D perspective | 蓝虚线 |

## 布局意图

- 四阶段从左到右横排;① ② ③ 窄列纵排内部流程,④ 占右侧约 1/3 宽(builder 左、auditor 右、chain 居中偏下、verdict 底部)
- E2(implementation source)放 ④ 正下方,与顶部 E1(API documentation)形成"两条独立信息源"的视觉对位——这是全图的论证要点
- 可选:底部一行斜体小字 running example(Qdrant #10369 一句话贯穿),若挤可省略(正文已详述)

## 交付

画完存 `figures/pipeline-v5-manual.pptx`(或直接改 pipeline-v5.pptx),我来:PowerPoint COM 导出 PNG(2400px 宽)→ 替换 TestVDB.tex 的 includegraphics → 编译验证。

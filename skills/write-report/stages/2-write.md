# Stage 2: Write / 写作

## 目的
按 Stage 1 的大纲，逐节用 LaTeX 写完整篇论文。

## 前置条件（开工前校验）
- `.self_xept/outline.md`（## Structure）存在
- `.self_xept/state.md`（## Task）存在（用户已批准）
- `.self_xept/references.md`（## Literature Index / ## Writing Style）可用

**若 `outline.md`（## Structure）缺失，停下先完成 Stage 1。**

## 工作流

### Phase 1: 准备
1. 读 `.self_xept/outline.md`（## Structure）拿完整写作计划
2. 读 `.self_xept/references.md`（## Literature Index 和正文）拿内容
3. 若 `.self_xept/references.md`（## Writing Style）存在，记下要应用的风格
4. 加载学科约束：`read` knowledge/<field>/expression/academic_english.md`；缺失则回退 `knowledge/general/expression/academic_english.md`
5. 确定文件结构：
   - 在项目根建 `texes/` 目录放分节文件
   - 每节 → `texes/{section-name}.tex`（章节名来自**你的**大纲，非固定列表）

### Phase 2: 逐节写作
**按大纲顺序，对每一节：**

1. **读计划** — `outline.md`（## Structure）对该节怎么说？
2. **读上一节结尾** — 保持叙事连贯
3. **写该节** — 按逐句计划
   - 引用 `.self_xept/references.md`（## Literature Index）和素材的实际内容
   - 应用 `references.md`（## Writing Style）的风格（若有）
   - 遵守大纲的词数/页数预算
   - 建表/图/公式时：`Read knowledge/<field>/elements/{type}.md`（缺失回退 general）取模板
4. **保存** — `write` 到 `texes/{section-name}.tex`
5. **post-write 自检** — 见下方清单
6. **修违例** — 修完再进下一节

**分节文件只含本节内容** — 无 preamble、无 `\begin{document}`。

### Phase 3: 整合
所有节写完后：
1. 建项目根 `main.tex`：documentclass + preamble（按 venue 模板）+ 每节 `\input{texes/...}` + bibliography 设置
2. 建项目根 `references.bib`（所有引用）
3. venue 有指定模板用之；否则用合理默认

### Phase 4: 编译与修错
1. `pwsh` 跑 `latexmk`（引擎按 `.self_xept/project.yml` 的 `engine`，如 xelatex/pdflatex）
2. 有错 → 调用 `xept:fix-latex`
3. 验证 PDF 渲染正确、图表算法正常显示

## LaTeX 规范

### 引用
- 一律 `~\cite{key}`（非断行空格）
- 放句末或紧跟主张之后
- 严禁编造引用

### 图
```latex
\begin{figure}
\centering
\includegraphics[width=\columnwidth]{figures/name.pdf}
\caption{Description.}
\label{fig:name}
\end{figure}
```

### 表
```latex
\begin{table}
\caption{Description.}
\label{tab:name}
\begin{tabular}{lrr}
\toprule
Header & Col1 & Col2 \\
\midrule
Row1 & val & val \\
\bottomrule
\end{tabular}
\end{table}
```

### 章节结构
- Introduction 通常**无**子节（连续段落）
- 技术节按需用子节
- 子节深度遵循领域惯例

## Post-Write 自检（强制）
**写完每一节后**逐项过：

```
格式:
[ ] ~\cite{} 和 ~\ref{} 格式正确
[ ] 无 em-dash（—）或 en-dash（–）

反 AI 风格（赶在用户之前抓）:
[ ] 无单句段落
[ ] 无填充开头（"It is worth noting"、"It should be noted"、"Moreover,"）
[ ] 无 3+ 连续段落平行结构（firstly/secondly/thirdly）
[ ] 无空洞总结收尾（"In summary"、"To conclude this section"）
[ ] 无意义膨胀词（"pivotal"、"groundbreaking"、"revolutionary"）
[ ] 段落长短自然变化（不是清一色 4-5 句）

内容质量:
[ ] 句子平均 <25 词
[ ] 主张有引用支撑（无编造文献）
[ ] 术语与前面章节一致
[ ] 缩写首次出现时定义
[ ] 段落有主题句
[ ] 论证深度匹配文档类型
```

**自检未过，该节不算完成。**

## 输出
- `texes/*.tex` — 分节文件
- `main.tex` — 整合文档
- `references.bib` — 参考文献
- 编译出的 PDF（经 `latexmk`）
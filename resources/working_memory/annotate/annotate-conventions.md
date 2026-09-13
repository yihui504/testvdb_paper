# annotate 锚点放置约定

> 本文档定义 annotate skill 的 note 锚点放置规则，包含 protected structure 禁令与三宏共存策略。与 SKILL.md 配套使用。

## 锚点定位原则

annotate 的 location 描述 → 内容锚点：

| location 类型 | 解析策略 | 放置规则 |
|---|---|---|
| **行号** | 基于 baseline 行（git 原始 committed 版或标注前快照）定位 | note 插入该行内容前后（避让 protected structure） |
| **片段** | 匹配 prose 片段（精确字符串或正则） | note 插入该片段前后；找不到 → unplaceable，不猜 |
| **描述** | "Section 3 第二段提到的 ablation" → 解析到具体锚点 | 解析失败 → unplaceable；不猜附近位置 |

**定位不准时 → unplaceable，绝不猜测。**

## protected structure 禁令

以下 LaTeX 结构**内部**不放 note（放在外面或跳过该 note）：

### 数学环境

- 行内数学：`$...$`
- 展示数学：`\[...\]`、`equation`、`align`、`gather`、`multline` 等 AMS 环境
- **原因**：数学环境内嵌 `\revnote{}` 会破坏渲染（未闭合的花括号、符号解析错误）

### 嵌套命令参数

- 任意 `\command{...}` 的参数内部不放 note（如 `\textbf{word \revnote{comment}}` 是**非法**）
- **原因**：破坏 LaTeX 参数解析；违反"扁平不嵌套"原则

### 特殊环境

- `\footnote{...}` 参数内部不放 note
- `\verb|...|` 及其变体（`\verb!...!`、`\verb+...+` 等）内部不放 note
- `verbatim`、`lstlisting` 等逐字环境内部不放 note
- **原因**：逐字环境禁止任何命令；`\footnote` 参数内嵌 note 会导致嵌套 footnote 错误

### 放置策略

遇到 protected structure 时：

1. **优先外部放置**：数学环境后紧跟（若语义连贯）、命令参数外包裹
2. **跳过该 note**：无法安全放置 → 标记 unplaceable，记录原因
3. **绝不强行插入**：破坏 LaTeX 渲染的风险 > note 丢失的风险

## 三宏共存策略

### preamble 定义

annotate 与 write-revision 共存时，preamble 同时定义三宏：

```latex
\usepackage{xcolor}        % 若 documentclass 已加载则跳过
\usepackage{ulem}          % 若 \sout 已用则跳过

% write-revision 宏（若已存在则跳过）
\newcommand{\revadd}[1]{\textcolor{blue}{#1}}
\newcommand{\revdel}[1]{\textcolor{red}{\sout{#1}}}

% annotate 宏
\newcommand{\revnote}[1]{\textcolor{orange}{[#1]}}
```

### verify_revision 透传规则

- `verify_revision.py` 的 spec **只含** `\revadd`、`\revdel`
- `\revnote` 不在其 spec 中 → 视为**未知命令**，`project()` 原样透传
- 因此 annotate 加的 note 不干扰 write-revision 的 round-trip 验证

### verify_annotations 透传规则

- `verify_annotations.py` 的 spec **只含** `\revnote`
- `\revadd`、`\revdel` 不在其 spec 中 → 视为**未知命令**，`project()` 原样透传
- 因此 write-revision 的标记不干扰 annotate 的纯插入验证

### 共存示例

```latex
The \revdel{old}\revadd{new} concept \revnote{clarify definition} is studied here.
```

- `verify_revision`：只处理 `\revdel`、`\revadd`，`\revnote` 透传
- `verify_annotations`：只处理 `\revnote`，`\revdel`、`\revadd` 透传
- 两验证器互不干扰

## 中文排版

- 本文档中文为主（符合 xept 方言）
- 代码、LaTeX 命令、环境名保留原文（如 `\revnote`、`equation`、`verbatim`）

## 与 PaperPilot 对照

本约定参考 PaperPilot `annotate-conventions.md` 的 protected structure 列表，调整为 xept 三宏共存场景：
- PaperPilot 原版：单 `\note{}` 命令
- xept 版：`\revnote{}` + `\revadd{}` + `\revdel{}` 三宏共存，透传规则明确

---

**变更历史**：
- 2026-07-24：初版（B2-1 companion）

---
name: fix-latex
description: 系统性诊断并修复 LaTeX 编译问题（不止错误，含影响显示的警告，绝不只修第一个）。读 main.log 分组定位、逐组修、latexmk 重编译，直到零错误。配套 refs：common_errors.md（错误目录）、acmart_issues.md（acmart 专题）、local_compile.md（本地 latexmk 用法）。
---

# Fix LaTeX（修复编译）

系统化诊断并修复**所有** LaTeX 编译问题——不止错误，还包括任何让 PDF 输出错误的东西。

## 核心工作流
```
1. 编译：`pwsh` 跑 latexmk（引擎见 .self_xept/project.yml）
2. 读日志：`read` main.log
3. 收集所有错误 + 影响显示的警告
4. 若用户报了具体显示问题，也读源码找原因
5. 在源文件里修所有收集到的问题
6. 重编译 → 还有问题则从步骤 2 重复
7. 停在：日志零错误 且 无影响显示的警告
```

**关键规则：**
- 修**所有**问题，非只第一个。扫整个 `main.log`。
- 别止于错误——警告也要查显示问题。
- 用户描述视觉问题时，看源码，不只看日志。

## 修什么

目标：**让 PDF 输出正确**。三类：

### 1. 错误——总是修
两种模式：
1. **`!` 前缀** — TeX 原始错误
   - `! Undefined control sequence` — 用了未定义的 `\command` 或缺包
   - `! Missing $ inserted` — 数学内容在 `$...$` 外
   - `! LaTeX Error: Command '\XXX' already defined` — 包冲突
   - `! File 'xxx.sty' not found` — 缺包
2. **`./file.tex:line: message`** 格式且 message 不含 "warning"
   - 常是包级错误，没崩编译但仍标红

**两种都会触发红色标记。** 即便 PDF 生成了，也必须修。

### 2. 影响显示的警告——主动修
编译"成功"但 PDF 有可见问题：
- `Citation 'XXX' undefined` → 引用显示 **[?]** → 修：查 .bib、确保 bibtex 跑了
- `Reference 'XXX' undefined` → 交叉引用显示 **?** → 修：查 `\label` 存在
- `Font shape 'XXX' undefined` → 文字字体错 → 修：加字体包或换引擎（xelatex）
- `Missing character: ...` → 字符缺失/乱码 → 修：CJK/Unicode 换 xelatex

### 3. 静默显示问题（日志无）——用户报告时修
- 表格线缺失 → 缺 `\usepackage{booktabs}`
- 颜色不显示 → 缺 `\usepackage{xcolor}`
- 中文/CJK 乱码 → 需 xelatex + `\usepackage{ctex}`
- 图片不渲染 → 路径错或缺文件

### 不修（除非用户要求）
- `Overfull \hbox` / `Underfull \hbox` — 美观排版问题
- `Package xxx Info:` — 信息消息

## 诊断步骤

### Step 1: 读编译日志
`read` 项目根的 `main.log`。搜：
- `!` 开头的行 — TeX 原始错误
- 含 "error"（不区分大小写）的行
- "LaTeX Warning" — 警告

> 注：`latexmk` 的退出码非 0 不等于"有错误"——始终以 `main.log` 内容为准。`latexmk` 成功也不代表零警告。

### Step 2: 分组与排序
- **同缺一个包** → 一条 `\usepackage{}` 修多个错误
- **同一未定义命令**跨文件 → 在 preamble 修，非逐文件
- **级联错误** → 一个语法错（缺 `}`）能引发 10+ 下游错误；修首个

### Step 3: 修所有错误
每组施对应修复。详见 `refs/common_errors.md` 与 `refs/acmart_issues.md`。

### Step 4: 重编译验证
`pwsh` 跑 `latexmk` 重编译。仍有错则重复。错误数归零才停。

## 常见错误模式

### 未定义控制序列
**修：**
1. 从错误消息识别未定义命令
2. 找哪个包提供 → 加 `\usepackage{xxx}`
3. 或修笔误：`\textbf` 非 `\textbold`

**常见：**
- `\toprule`/`\midrule`/`\bottomrule` → `\usepackage{booktabs}`
- `\url{}` → `\usepackage{url}` 或 `\usepackage{hyperref}`
- `\boldsymbol` → `\usepackage{bm}` 或 `\usepackage{amsmath}`
- `\mathbb` → `\usepackage{amssymb}` 或 `\usepackage{amsfonts}`

### 包冲突
- **`\Bbbk already defined`（acmart + amssymb）** → 删 `\usepackage{amssymb}`（acmart 内部已加载）
- **Hyperref 顺序** → 把 `\usepackage{hyperref}` 移到 preamble 末尾

### 缺 $ 插入
**修：** 包进 `$...$` 或 `\(...\)`。如 `the value x_i` → `the value $x_i$`

### 参考文献错误
- `Citation 'XXX' undefined` → 需多次编译（`latexmk` 会自动处理 bibtex 与多遍）
- `Empty bibliography` → 查 `\bibliography{}` 里的 .bib 路径

### 字体错误
- `Font shape 'XXX' undefined` → 加字体包或换 xelatex
- 缺 CJK 字体 → 改 `.self_xept/project.yml` 的 `engine: xelatex` 后重编译

### Documentclass 专属
- **acmart**：内置包——勿重载 amsmath、hyperref、natbib
- **IEEEtran**：双栏下栏平衡、图位
- **beamer**：fragile 帧需 `[fragile]` 选项

## 本地编译
详见 `refs/local_compile.md`。要点：
- `pwsh` 跑 `latexmk -pdf main.tex`（pdflatex）或 `latexmk -xelatex main.tex`
- 引擎由 `.self_xept/project.yml` 的 `engine` 字段决定
- CJK/Unicode 字体问题 → **先**换 `engine: xelatex`，再考虑改 preamble

## 速查
**总先查：**
- 包冲突（尤其 acmart、IEEEtran）
- 缺 `\end{document}`
- 不匹配的 `{}`、`[]`、环境
- 未定义 label/引用
- 缺 .bib 文件

**最佳实践：**
- 修前扫整个 `main.log` 找**所有**错误
- 按根因分组——一条修复可能消多个错误
- 每次修复后用 `latexmk` 重编译验证
- `latexmk` 成功 ≠ 零错误——始终查 `main.log`
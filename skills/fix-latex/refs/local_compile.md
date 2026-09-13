# Local Compilation Reference（本地 latexmk 用法）

> xept 在本地用 `latexmk` 编译，不再依赖任何远程编译服务。本文件替代原平台的 compile_latex/set_compiler_engine MCP 工具说明。

## 基本用法

引擎由 `.self_xept/project.yml` 的 `engine` 字段决定（`pdflatex` / `xelatex` / `lualatex`）。

```bash
# pdflatex（默认）
latexmk -pdf main.tex

# xelatex（CJK / Unicode / fontspec）
latexmk -xelatex main.tex

# lualatex
latexmk -lualatex main.tex

# 清理辅助文件
latexmk -c            # 留 PDF，清 .aux/.log/.fls 等
latexmk -C            # 连 PDF 一起清
```

`latexmk` 会**自动**决定需要几遍编译、并在需要时自动跑 `bibtex`/`biber`，所以引用/参考文献的多遍问题通常无需手动处理。

## 读日志

产物日志在项目根 `main.log`（或 `<jobname>.log`）。三类行：

| 模式 | 含义 |
|------|------|
| `! ...` 开头 | TeX 原始错误（必修） |
| `LaTeX Warning: ...` | 警告（影响显示的要修） |
| `Package xxx Info: ...` | 信息（通常可忽略） |

定位错误：`main.log` 里 `!` 行的下一个 `l.<行号>` 指出源文件行。

## 退出码

| 退出码 | 含义 | 常见原因 |
|--------|------|----------|
| 0 | 成功 | 编译完成 |
| 非 0 | 有错 | 未定义命令、语法错、缺文件、包冲突 |

> `latexmk` 退出码非 0 不一定意味着 PDF 没生成；始终以 `main.log` 内容为准。退出码 0 也不保证零警告。

## 引擎切换（字体/CJK 问题优先尝试）

当 `main.log` 出现以下，**先换 `engine: xelatex`**（改 `.self_xept/project.yml`），再考虑改 preamble：

| 日志症状 | 推荐引擎 |
|---|---|
| `ctex-fontset-*` / `unihei*` / CJK 字体找不到 | `xelatex` |
| pdflatex 下任何 CJK / Unicode 文字错误 | `xelatex` 或 `lualatex` |
| 源码用了 `fontspec` / `\setmainfont` | `xelatex` 或 `lualatex` |
| 字体相关错误 + 退出码 12 | 先试 `xelatex` |

流程：`latexmk` 报字体错 → 改 `engine: xelatex` → `latexmk -xelatex` 重编译。

## 参考文献（BibTeX / biber）

```bash
latexmk -pdf main.tex     # 自动：pdflatex → bibtex → pdflatex ×2
```

若用 `biblatex` + `biber`：
```bash
latexmk -pdf -bibtex-prog=biber main.tex
```

`Citation 'XXX' undefined` 多因编译遍数不够——让 `latexmk` 自己跑完即可；若仍报，查 `.bib` 路径与 key 拼写。

## 参见
- `common_errors.md` — 常见错误目录
- `acmart_issues.md` — acmart 专题

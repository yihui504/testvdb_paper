---
name: write-paper
description: 写论文（期刊/会议/工作坊，任意学科、任意 venue）。用于从头起草 LaTeX 论文：阶段化流程 分析→规划（待批准）→逐节写（每节编译+自检）→打磨控页。逐节写、绝不一次性整篇。学位论文用 xept:write-thesis，技术报告用 xept:write-report；已有审稿意见要改论文用 xept:write-revision（非起草）。
---

# Write Paper（写论文）

阶段化学术论文写作。适用任意领域（CS、生物、人文…）和任意 venue（会议、期刊、工作坊）。

## 核心原则

**本技能管流程与纪律。LLM 管内容与领域专长。**

本技能告诉你**何时**用工具、要过**哪些**质量门。它**不**告诉你写哪些章节、怎么结构——那用你自己的领域与 venue 知识。

## 阶段

```
Stage 0: Analyze   → 读需求、参考文献、用户素材
Stage 1: Plan      → 任务摘要（待用户批准）+ 大纲
Stage 2: Write     → 逐节 LaTeX 写作
Stage 3: Refine    → 质量检查 + 页数控制
```

每阶段是一份文件：`read` 本技能目录下 `stages/N-*.md`（1-plan / 2-write / 3-refine）。

## 强制规则

### 规则 1：阶段顺序
按序执行，绝不跳步。

```
Stage 0 → Stage 1 → Stage 2 → Stage 3 → 编译
          ⛔ 停        逐节       ⛔ 检查
        （待批准）              （页数）
```

### 规则 2：先读后写
- **总是**先 `read` `.self_xept/project.yml` 再规划
- **总是**先 `read` `.self_xept/outline.md`（## Structure）再写作
- **总是**写下一节前重读上一节结尾

### 规则 3：写作前确认
- Stage 1：**向用户展示方案并停下等待批准**
- 用户未批准前**不得**开始写作

### 规则 4：逐节写作
**绝不一次性整篇。** Stage 2 里：
1. 写一节 → `write` 保存
2. `pwsh` 跑 `latexmk` 编译检查
3. 跑 post-write 自检（见 `stages/2-write.md`）
4. 进下一节

### 规则 5：领域知识
写每节前加载相关写作指南：`read` knowledge/<field>/<path>.md`；缺失则回退 `knowledge/general/<path>.md`（池解析：学科 → general）。

## 写作质量规则（始终适用）

### LaTeX 格式
- 用 `~\cite{}` 和 `~\ref{}`（引用/交叉引用前非断行空格）
- 图 caption 在下：`\includegraphics` 之后 `\caption{}`
- 表 caption 在上：`\begin{tabular}` 之前 `\caption{}`
- 每个 `\begin{}` 有匹配 `\end{}`

### 学术风格
- **无 em-dash（—）或 en-dash（–）** — 用逗号、括号或拆句
- **无 "It is..."、"There is/are..."** — 用直接主谓
- **句子尽量 <25 词**
- **变换过渡词** — 别老 "However"、"Moreover"、"Furthermore"
- **多用动词** — "we analyze" 非 "we conduct an analysis"

### 内容诚信
- **绝不编造引用** — 只引你能核实存在的论文
- **绝不编造数据** — 只用用户素材里的数字
- **每个主张都要支撑** — 引用或数据出处
- **缩写首次定义** — "Machine Learning (ML)"
- **术语一致** — 同概念全程同词

## 工具（原生）

### 写入与编译
```
write / edit     # 写/改 LaTeX 内容
read             # 读项目文件
pwsh latexmk     # 编译成 PDF —— 每节后跑（引擎见 .self_xept/project.yml 的 engine）
```

### 内存与规划
```
（展示方案 → 停下等用户批准）   # Stage 1
（问用户并等待）               # 需要澄清时
（向用户报告完成）             # Stage 3
```

### 引用
```
xept:add-citation              # 找引用、补 BibTeX
# 或直接：`pwsh` 跑 python scripts/fetch_bib.py --query "..."
```

### 质量
```
stages/2-write.md 的 post-write 自检清单   # 每次写入后跑
```

## 元状态文件

| 文件 | 创建者 | 用途 |
|------|--------|------|
| `.self_xept/project.yml` | 用户 / `xept:setup-venue` | venue 要求、页数、格式规则、引擎 |
| `.self_xept/references.md`（## Writing Style） | Stage 0 | 从参考论文学到的风格 |
| `.self_xept/references.md`（## Literature Index） | Stage 0 | 从用户素材提取的学术引用 |
| `.self_xept/references.md` | Stage 0 | 非论文素材（数据、代码、笔记） |
| `.self_xept/state.md`（## Task） | Stage 1 | 用户批准的任务计划 |
| `.self_xept/outline.md`（## Structure） | Stage 1 | 逐节写作计划 |

## 速查
```
1. `read` stages/1-plan.md → 读需求 + 分析素材
2. `read` stages/1-plan.md 的规划 → 展示方案 → 停等批准 → 大纲
3. `read` stages/2-write.md → 逐节写（每节 `write` + 编译）
4. `read` stages/3-refine.md → 质检 + 控页 → Bash latexmk
5. 向用户报告完成
```

## 常见错误（避免）
1. ❌ 一次性整篇 —— 必须**逐节**
2. ❌ 跳过待批准门 —— 写作前**必须**用户批准
3. ❌ 规划前不读要求 —— **总是**先读 `.self_xept/project.yml`
4. ❌ 硬编码章节结构 —— 让你的领域知识决定
5. ❌ 节间不编译 —— 早抓错
6. ❌ 忘 post-write 自检 —— 每次写入后跑
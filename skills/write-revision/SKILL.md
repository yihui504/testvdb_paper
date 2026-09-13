---
name: write-revision
description: 按审稿意见修订已投稿论文，带 \revadd{}/\revdel{} 双宏修订标记并经 round-trip 验证（accept/reject 双向投影，标记正确性可证明）。用于 .self_xept/project.yml 的 state 为 revision/revision2，或用户要据审稿意见改论文 .tex。起草阶段自编辑用 xept:write-paper；逐条回复审稿人用 xept:write-response / xept:write-rebuttal。
---

# Write Revision（按审稿意见修订论文）

据审稿反馈修订已投稿论文，带**双宏**修订标记（`\revadd{}` 增/改、`\revdel{}` 删），产出经 round-trip 验证（accept 得新版、reject 得旧版，正确性可证明而非祈求）。

## 何时用
- `.self_xept/project.yml` 的 `state` 为 `revision`、`revision2` 等
- 用户要按审稿意见修改论文
- **不**用于起草阶段的自编辑（用 `xept:write-paper`）

---

## Part 1: 修订标记（双宏，revision 状态下始终生效）

### 为什么双宏 + 验证
旧单宏 `\rev{}` 只标增/改，**删除直接删不标**——审稿人无法对照"删了什么"，也无法机械验证标记对不对。双宏 `\revadd{}`/`\revdel{}` 让删除也可见，且可 round-trip 验证（`accept(marked)==new ∧ reject(marked)==old`），标记正确性可证明。

### 默认 preamble
确保 preamble 有（`xcolor` 若 documentclass 如 acmart 已加载则跳过）：
```latex
\usepackage{xcolor}
\usepackage[normalem]{ulem}       % \sout 删除线；normalem 防 \emph 被改成下划线
\newcommand{\revadd}[1]{{\color{blue}#1}}
\newcommand{\revdel}[1]{{\color{red}\sout{#1}}}
```

### 用户覆盖
若用户指定别的偏好，照办（并跑 `verify_revision.py` 时用 `--add`/`--delete` 传对应命令名）：别的颜色、宏名、格式（下划线代删除线）、或完全不要标记。

### 标记什么

| 改动类型 | 怎么标 |
|----------|--------|
| 修改的文字 | `\revadd{new text}` |
| 新增的文字 | `\revadd{new content}` |
| 笔误修正 | `\revadd{corrected word}` |
| 数据/数字改动 | `\revadd{updated value}` |
| **删除的文字** | `\revdel{deleted text}`（**不再"直接删"**） |
| 表/图内容改动 | **不**给内容上色；标 caption：`\revadd{Updated...}` |
| 仅格式改动（无可见内容变化） | 不标 |
| LaTeX 注释（`% ...`） | 不标 |
| 参考文献条目（.bib） | 不标 |

### 标记纪律（round-trip 可验证的前提）
- **扁平不嵌套**：`\revadd{}`/`\revdel{}` 不互相嵌套，也不嵌进别的命令参数里（嵌套使 round-trip 失败）
- **裸参数**：只发 `\revadd{text}` / `\revdel{text}`，不带可选 `[...]` 参数
- **成对覆盖 diff**：每处 old→new 的改动用 `\revdel{old}\revadd{new}` 成对标，使 accept/reject 都能还原

### 粒度
标最小有意义单位：改一个词包该词；重写整段包整段；表格更新标 caption。

### 示例
```latex
% 改词（成对）
We propose \revdel{a basic}\revadd{an improved} method.

% 加句（只 add）
\revadd{We additionally evaluate on BigCloneBench (Section 4.3).}

% 删句（只 del）
\revdel{This preliminary result is inconclusive.}

% 表数据更新——标 caption
\caption{\revadd{Comparison with additional baselines.}}
```

### 旧 `\rev{}` 迁移
若论文已有旧单宏 `\rev{}`：把 `\newcommand{\rev}` 改名为 `\revadd` + 补 `\revdel` 定义（含 `ulem`）；旧 `\rev{x}` 全替换为 `\revadd{x}`。之前"直接删"的删除无法回标（除非对照旧版备份），用户可择机补 `\revdel`。

---

## Part 2: 修订工作流 + round-trip 验证

### 工作流
1. **读审稿意见**：`read` 项目根 `review.md` / `reviews.md`
2. **读旧版论文**（`old`，round-trip 基准；改前先备份成 `old.tex`）
3. **读元状态**：`.self_xept/facts.md`（术语）、`project.yml`（venue）、`outline.md`（上下文）
4. **规划改动**：每条意见对应改哪些节；心里确定干净最终版 `new`
5. **确定 new + 带标记应用**：先按审稿意见确定干净最终版 `new`（改完想要的目标文本），再 `edit` .tex 产出 `marked`（带 `\revadd`/`\revdel` 标 old→new 的 diff）；存 `new.tex`（= new）+ `marked.tex`（= marked）。**`new` 独立产出（按意见想的目标），非从 `marked` 投影派生**——这样 `accept(marked)==new` 才是真验证（查 marked 的增改标对没），不是自洽循环
6. **round-trip 验证**（下述 HARD-GATE 循环）
7. **编译**：`pwsh` 跑 `latexmk`（引擎见 `project.yml`）验证渲染

### round-trip 验证（generate → verify → repair）

<HARD-GATE>
修订标记产出后**必须**过 round-trip 验证：`accept(marked)==new ∧ reject(marked)==old`。
错标记比没标记更糟（误导看 diff 的人），故验证不过的标记**绝不交付**。

三文件：`old.tex`（修订前备份）、`new.tex`（**独立产出**的干净最终版——按审稿意见改完的目标，非从 marked 派生）、`marked.tex`（带标记版，产物）。跑：
```
python scripts/verify_revision.py --old old.tex --new new.tex --marked marked.tex
```
（默认 `--add revadd --delete revdel`，与 preamble 一致；用了别的宏名则传 `--add`/`--delete`）

双向都是真验证（new 独立，故 accept 非自洽）：
- `accept(marked)==new`：marked 的 `\revadd` 增改标对没（accept 投影应得你想要的 new）
- `reject(marked)==old`：marked 的 `\revdel` 删标全没（reject 投影应还原 old）——双宏相比旧单宏的核心价值（旧单宏删除不标，无法还原 old）

- **exit 0** → 交付 `marked.tex`
- **exit 1** → 读 JSON 的 `accept_diff`/`reject_diff`（首个 mismatch 位置 + 摘录），按它**只改 marked**（补漏的 `\revadd`/`\revdel`、删多余的、拆嵌套）；**不动 new**（new 是目标，marked 是标记手段，marked 追齐 new），重跑
- **上限 5 轮**；仍不过 → **不交付**，保留 old/new/marked 三文件给用户人工修
</HARD-GATE>

### 修订原则
1. **保留原结构**：修订是改进既有论文，非从头重写；除非审稿人要求重组，否则保留章节组织
2. **与回复交叉对照**：若有 `response.tex`/`rebuttal.md`，改动要与承诺一致（"We have revised Section 3.2" 就要真改 3.2）
3. **分优先级**：先致命后次要
4. **post-write 自检**：`read` `knowledge/general/post_write_check.md`（或学科对应）

### 团队 PR（可选）
round-trip 验证 exit 0 且编译通过后，若会话提供 `mcp__github__*` 工具、`project.yml` 配有 `repo:`、且用户同意：把本轮修订推成 feature 分支（如 `revision-round-1`）并 `mcp__github__create_pull_request`，描述列出对应 qN issue（"Closes #N"），队友在 PR diff 里直接看 `\revadd/\revdel` 标记。线性协作下直接提交主分支同样合法——PR 用于留审阅痕迹，非硬门。

---

## Camera-Ready 清理
转入 camera_ready 状态时，移除所有修订标记（= 产出 `new.tex`）：
- `\revadd{text}` → `text`（保留内容）
- `\revdel{text}` → 删除被标记的内容（左右文本合并；段落级的 `\revdel` 则该段整删）
- 删 `\newcommand{\revadd}` / `\newcommand{\revdel}` 行
- 若 `\usepackage{ulem}` / `xcolor` 仅为修订加的则移除（别处用到则保留）

---

## 配套
- round-trip 验证器 `scripts/verify_revision.py`（Part 2 用，纯标准库、fail-closed，exit 0/1 + JSON mismatch 报告，17 单测覆盖）

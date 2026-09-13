---
name: annotate
description: "把 mock-review / consistency-check 类 skill 的发现以 \\revnote{} 内联标到论文指定位置——纯插入不改源正文（Iron Law），经纯插入校验 + 覆盖率校验，不过不交付。用户要\"把审稿意见标进论文\"/\"在这些位置加批注\"时调用。改论文正文用 xept:write-revision；出独立报告用 xept:mock-review。"
---

# Annotate（内联注释 · 不改原文）

> **实现**：`scripts/verify_annotations.py` + 单测 + companion（见 §配套）。设计依据：[docs/improvement-plan.md](../../docs/improvement-plan.md) 路线 B + [verify_revision.py](../../scripts/verify_revision.py) 复用。

## 核心原则

**你只放 note，绝不改 note 周围的原文，绝不改写 note 文本本身。**

annotate 在论文正文指定位置插入 `\revnote{note 文本}`，纯增量。剥离所有 `\revnote{}` 必须还原原始 prose。

**Iron Law**：

```
NO SOURCE MODIFICATION — annotations are pure additions.
```

**违反字面 = 违反精神。**

## 何时用 / 何时不用

**用**：上游（[xept:mock-review](../mock-review/SKILL.md) 的 weakness 清单、[xept:consistency-check](../consistency-check/SKILL.md) 的发现、手动列表）交给你一组 note——每条含 **location**（行号/片段/描述）+ **note 文本**（verbatim 插入）。annotate 负责把 note 放到 location 对应的内容锚点。

**不用**：
- 想跟踪两版差异 → [xept:write-revision](../write-revision/SKILL.md)（带 `\revadd`/`\revdel` 修订标记）
- 想要**生成** note 本身 → 上游的活（mock-review 出 weakness，consistency-check 出冲突）；annotate 只**放置**给它的 note
- 想修 note 背后的问题 → 手动改；annotate 只**标记**

## 流程：place → verify → repair

### Step 1: Place

1. 解析 note 命令名：`.self_xept/project.yml`（+ `.self_xept/project.user.yml` overlay）的 `annotate.note_command`，默认 `revnote`（[layered config](../../docs/conventions.md) §5）。
2. **检查 preamble**：目标 `.tex` 是否已定义 `\revnote`（或自定义名）。缺则补 preamble（见 §preamble）；已有则不动。
3. 读 note 列表（inline 或文件）。每条两字段：
   - **location** — 哪里：行号 / 片段 / 描述。annotate 解析到内容锚点。
   - **note** — 什么：**verbatim 插入**，不判断不重写（上游 own 内容）。LaTeX 特殊字符转义是渲染修复，非重写。
4. 存**标注前 baseline**：每目标文件 `git show HEAD:<file>`（committed & clean 时），否则复制当前文件。Step 2 对它校验。
5. 放置每条 note：location → 内容锚点 → 插入 `\revnote{...}`。**锚点找不到 → 不猜**，标该 note **unplaceable**，移到下一条。

### Step 2: Verify

跑 must-be-correct 校验器（[conventions.md](../../docs/conventions.md) §3.3）：

```
python scripts/verify_annotations.py --orig <baseline> --cur <file> --command <name> --input-note-count <N> [--unplaceable-count <N>] [--notes <notes.json>]
```

（默认 `--command revnote`；`--input-note-count` 必传做覆盖率校验；`--unplaceable-count` 可选默认 0；`--notes` 可选传 note 文本列表做 verbatim 校验，缺失则降级跳过 verbatim；自定义宏名照传。exit 0=纯插入+覆盖率+verbatim 全过 / 1=JSON 报首个违反。）

校验三件事：
1. **纯插入**：strip 所有 `\revnote{}` 后 == baseline。复用 [verify_revision.py](../../scripts/verify_revision.py) 的 `project()` + `normalize()`：`normalize(project(cur, {revnote: (1, ())})) == normalize(orig)`（`project({name:(1,())})` 完全删除命令外壳+参数；2026-07-24 实验验证 `project('hello \revnote{world} end', {revnote:(1,())})` == `'hello  end'`）。任一原文改动（"顺手修了个 typo"）会被抓。
2. **覆盖率**：placed 数 == `--input-note-count` − `--unplaceable-count`。mismatch = 静默漏放或双放——交付前抓。
3. **note verbatim**：`--notes` 传入时校验每个 placed note 文本在集合里；缺失时跳过。防 agent "精简 note" 改写内容（数量校验抓不住；Iron Law 要求 verbatim 插入，上游 own 内容）。

- **exit 0** → 纯插入证明 + 覆盖率一致 → **交付**（placed note 在；列出 unplaceable —— 源文件自报告后漂移）。
- **exit 1** → 读 JSON（`violation` / `reason` / `excerpts`）→ Step 3。

### Step 3: Repair

1. 剥离每处非 note 的改动（还原原文 prose），重 Verify。
2. **上限 5 轮**。到 5 → **HARD-STOP**：什么都不交付，保留标注前后文件给用户手动修。

## 两道门：纯插入 + 渲染

<HARD-GATE>
verify_annotations 证明 note 是**纯增量**，不证明它们**能渲染**。annotate own 纯插入（Step 2）+ 安全放置（§锚点规则）；渲染由下游 `xept:fix-latex` / 编译 exercised。编译错误 on a note = 渲染修复（按转义规则 escape），**非**重写 note 文本。
</HARD-GATE>

## preamble（\revnote 定义）

annotate 负责**检查并补加** preamble 定义（不依赖 revision 状态——annotate 可在非 revision 状态用）。默认：

```latex
\usepackage{xcolor}   % 若 documentclass 已加载则跳过
\newcommand{\revnote}[1]{\textcolor{orange}{[#1]}}
```

**与 [xept:write-revision](../write-revision/SKILL.md) 共存**：三宏同 preamble 各司其职——`\revadd`（增改，blue）/ `\revdel`（删，red\sout）/ `\revnote`（批注，orange）。annotate 调本 skill 专属的 `verify_annotations.py`（spec 只含 `\revnote`）；若 preamble 已有 `\revadd`/`\revdel`（revision 状态），并存不冲突。若同文件也跑 [verify_revision.py](../../scripts/verify_revision.py)（revision 状态，run-time `--add revadd --delete revdel` 传参），`\revnote` 不在其 spec → 对 `verify_revision` 是未知命令原样透传，不干扰 round-trip。

## 锚点规则

place 时 location → 内容锚点：
- **行号**：按 baseline 行（插 note 后行号会变，基于 baseline 定位）。
- **片段**：匹配 prose 片段，note 放该片段前后（详见 companion，避开数学环境 / `\footnote` / 嵌套命令参数）。
- **描述**："Section 3 第二段提到的 ablation" → 解析到具体锚点；解析失败 → unplaceable，不猜。

详细放置规则（含"飘进 protected structure"的禁令）在 companion `annotate-conventions.md`（实现阶段补，参考成熟实现的 protected-structure 列表）。

## Red Flags — STOP

- 想重写 note 文本 — "这 note 不清楚，我精简下"
- 想从一批里丢掉某条 — "我放了大部分"
- 没验证就交付 — "我只加了 note，信我"
- 改了原文 prose — "顺手修了个 typo"
- 锚点没找到，猜个附近位置 "还是放上"

**以上任一 = 撤销违反，重 Verify。**

## 借口表

| 借口 | 现实 |
|---|---|
| "note 不清楚，我改下" | 上游 own note 内容。verbatim 插入。 |
| "大部分放了就行" | 漏放 = 静默丢失。覆盖率校验会抓。 |
| "只加 note 没改别的" | verify_annotations 抓纯插入违反。"顺手修 typo" 是典型漏。 |
| "锚点附近差不多" | 不猜。找不到 → unplaceable。 |

## 配套（实现阶段补）

- 纯插入校验器：`scripts/verify_annotations.py`（复用 [verify_revision.py](../../scripts/verify_revision.py) 的 `project`/`normalize`/`parse_brace_args`/`read_exact` + 新增覆盖率校验；exit 0/1 + JSON mismatch 报告）
- 单测：`tests/scripts/verify_annotations_test.py`（GREEN 纯插入过 + RED 改原文/漏放/双放；参考 [verify_revision_test.py](../../tests/scripts/verify_revision_test.py) 模式，含一个"三宏共存"用例确认 \revnote 不干扰 \revadd/\revdel 校验）
- 锚点规则：`skills/annotate/annotate-conventions.md`

## Integration

- **上游**：[xept:mock-review](../mock-review/SKILL.md)（weakness 清单）、[xept:consistency-check](../consistency-check/SKILL.md)（冲突清单）、手动列表
- **下游**：[xept:fix-latex](../fix-latex/SKILL.md) / 编译（渲染验证）
- **互补**：[xept:write-revision](../write-revision/SKILL.md)（改论文 prose 带 `\revadd`/`\revdel`；annotate 只标不改）

---

## 立项验收清单（review 用）

- [ ] discipline 三件套齐（Iron Law + HARD-GATE + 借口表 + Red Flags），符合 [B1-1 writing-skills](../writing-skills/SKILL.md) 分类
- [ ] 与 write-revision 宏共存设计清晰（三宏同 preamble 不冲突，verify_revision spec 不含 revnote）
- [ ] verify_annotations 接口契约明确（`--orig --cur --command`，exit 0/1，复用 verify_revision 的 `project`/`normalize`）
- [ ] 覆盖率校验逻辑写明（placed == input − unplaceable）
- [ ] preamble 检查+补加逻辑（不依赖 revision 状态）
- [ ] 无平台残留 / `pp:` 归零（xept 方言：`xept:` 引用、`.self_xept/` 元状态）

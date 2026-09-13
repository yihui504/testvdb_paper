---
name: using-xept
description: xept 技能集的发现与路由入口（学术写作/审稿/改稿/投稿任务先查 xept 技能表）。任何学术论文相关任务开始前调用本技能，确认该用哪个 xept 技能。哪怕只有 1% 可能相关，也应先调用本技能再决定。
---

# Using Xept（xept 技能发现与路由）

<SUBAGENT-STOP>
若你作为子代理被派来执行某个具体任务，跳过本技能。
</SUBAGENT-STOP>

<EXTREMELY-IMPORTANT>
只要觉得有 1% 可能某个 xept 技能适用于当前任务，就**必须**先调用该技能。
技能适用时你没有选择，必须用。不可自找借口绕过。
</EXTREMELY-IMPORTANT>

## 技能链（典型生命周期）

```
setup-venue → write-paper → fix-latex / control-length → check-submission → reduce-ai → mock-review
                                  ↳ （拿到审稿意见后）analyze-reviews → write-response / write-rebuttal → finalize-rebuttal；并 write-revision 改论文
```

任意时点可用：`add-citation`、`literature`、`translate-paper`、`paraphrase`、`design-figure`、`design-table`、`design-slides`、`write-poster`、`write-cover-letter`、`compress-images`、`consistency-check`、`check-references`、`analyze-files`、`doc-check`。

## 意图 → 技能映射

| 意图 | 调用 |
|------|------|
| 配置投稿会议/期刊（抓 CFP、页数、截止、模板） | `xept:setup-venue` |
| 分析项目素材文件 | `xept:analyze-files` |
| 从头写论文（期刊/会议/工作坊） | `xept:write-paper` |
| 写学位论文（本/硕/博） | `xept:write-thesis` |
| 写技术报告 | `xept:write-report` |
| 按审稿意见改论文（带修订标记） | `xept:write-revision` |
| 换 LaTeX 模板 | `xept:change-template` |
| 修 LaTeX 编译错误 | `xept:fix-latex` |
| 控制篇幅/页数 | `xept:control-length` |
| 添加/补全引用 | `xept:add-citation` |
| 检查参考文献 | `xept:check-references` |
| 查文献 / 下全文 / 直接生成 BibTeX | `xept:literature` |
| 改写降重 | `xept:paraphrase` |
| 论文翻译 | `xept:translate-paper` |
| 画数据图 | `xept:design-figure` |
| 设计对比表格 | `xept:design-table` |
| 做汇报幻灯片 | `xept:design-slides` |
| 做学术海报 | `xept:write-poster` |
| 写投稿信 | `xept:write-cover-letter` |
| 投稿前检查清单 | `xept:check-submission` |
| 全文一致性检查 | `xept:consistency-check` |
| 审计 prose 文档（SKILL/README/design） | `xept:doc-check` |
| 降低 AI 写作痕迹（四层） | `xept:reduce-ai` |
| 模拟审稿 | `xept:mock-review` |
| 解析审稿意见（标优先级） | `xept:analyze-reviews` |
| 逐条回复审稿意见 | `xept:write-response` |
| 写战略性 rebuttal（跨审稿人统一） | `xept:write-rebuttal` |
| 打磨 rebuttal 成可提交定稿 | `xept:finalize-rebuttal` |
| 压缩图片 | `xept:compress-images` |

## 流水线说明

**写作链**：`xept:setup-venue`（定 venue/页数/引擎）→ `xept:write-paper`（阶段化逐节写）→ `xept:fix-latex` / `xept:control-length` → `xept:check-submission` → `xept:reduce-ai` → `xept:mock-review`。

**Rebuttal 链**：`xept:analyze-reviews`（解析意见、标 must/should/could）→ `xept:write-response`（逐条）或 `xept:write-rebuttal`（战略性统一文档）→ `xept:finalize-rebuttal`（定稿）；并行地 `xept:write-revision` 按意见改论文 .tex。
- `xept:write-response` 是**逐条 point-by-point**；`xept:write-rebuttal` 是**跨审稿人合并的战略文档**——两者产物不同，按需选。
- `xept:write-revision` 改的是**论文本身**（带 `\rev{}` 标记），不是 rebuttal 信。

## 清单

1. **识别任务** — 用户要做什么？（写论文 / 改稿 / 审稿 / 投稿 / 改图 / 回复审稿…）
2. **匹配技能** — 在上映射表找；一个意图归一个技能。
3. **调用技能** — 用 Skill 工具调 `xept:<技能名>`，再做其他响应。无技能匹配就明说，别擅自做。

## 自检
响应任务前确认：
- [ ] 识别出哪个 xept 技能（若有） owns 此任务？
- [ ] 已用 Skill 工具在响应前调用它？
- [ ] 若"无技能适用"——是真的，还是我在默认"自己随便做"？

## 项目状态
所有 xept 写作类技能共享项目元状态目录 `.self_xept/`：
- `project.yml` — venue / field / language / page_limit / engine / state / deadline / anonymity（提交）
- `project.user.yml` — 个人密钥覆盖层（gitignore）
- `state.md` / `outline.md` / `references.md` — 任务计划 / 大纲 / 风格与文献索引

工作产物（`main.tex`、`rebuttal.md`、`figures/` 等）留在项目根，xept 不挪动。

## 集成
- **被依赖**：所有其他 xept 技能（建立发现行为）
- **定位**：入口点，学术写作任务开始时加载

---
name: write-report
description: 写课程报告/作业/实验报告（大学生）。以作业要求为首要指引，结构对齐评分标准，强调详细解释与分析。学位论文用 xept:write-thesis，期刊会议论文用 xept:write-paper。
---

# Write Report（写技术/课程报告）

写课程报告、课后作业、实验报告。

- 以**作业要求**为首要指引（`read` 作业说明文件）
- 结构对齐**评分标准**
- 强调**详细解释与分析**（报告重"讲清楚"，论文重"简洁"）

## 工作流

1. `read` 作业/实验要求文件，提取：题目、评分点、字数/格式、截止
2. 若无明确要求，**问用户并等待**澄清关键信息
3. 把要求写入 `.self_xept/project.yml`（field/type/length/language）
4. 规划结构（按评分点组织）→ **展示给用户、停等批准**
5. 批准后逐节 `write`，每节聚焦一个评分点
6. 自检：每个评分点是否都被覆盖、是否有足够分析（非仅描述）
7. `pwsh` 跑 `latexmk`（或按要求导出 docx/pdf）验证

## 与写作组的关系
- 报告 ≠ 论文：报告允许更详细、可重复、教学性表述；不强制 venue 风格
- 共享 `.self_xept/` 元状态与 `stages/` 阶段纪律（`read` 本技能 `stages/N-*.md`）
- 引用仍用 `xept:add-citation`；降 AI 用 `xept:reduce-ai`

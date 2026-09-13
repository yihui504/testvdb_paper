---
name: analyze-reviews
description: 解析审稿意见，生成带优先级标记（MUST/SHOULD/COULD + q1/q2…编号）的结构化 markdown，供后续 rebuttal 追踪。rebuttal 流水线上游喂料；下游用 xept:write-response 逐条回复或 xept:write-rebuttal 写战略文档。输出写到项目根 reviews.md。
---

# Analyze Reviews（解析审稿意见）

解析审稿意见，生成带优先级标记的结构化 markdown，便于追踪 rebuttal 进度。

## 目的
把原始审稿反馈转成结构化 markdown，每条可执行点带优先级标记与唯一编号（q1、q2、q3…）。

## 输出格式
生成 markdown，每条可执行点独占一行，前缀优先级标记与编号：

```
**[MUST q1]** critical feedback text
**[SHOULD q2]** important suggestion text
**[COULD q3]** optional improvement text
```

- 优先级标记：`MUST` / `SHOULD` / `COULD`
- 编号：全文档顺序 `q1`、`q2`、`q3`…（唯一，不重用）
- 输出写到项目根 `reviews.md`

## 格式规则

### 1. 紧凑、扁平层级
- 审稿人/小节标签用 `**bold**`，而非深层 `###` 标题
- 相关元数据尽量合并到更少的行

### 2. 保留原始列表格式
- 原始编号 `1.`、`2.`、`3.` 作纯文本保留
- 原始项目符号 `+`、`-`、`•` 作纯文本保留
- 不转成 markdown 列表语法；用换行分隔

### 3. 每条标记独占一行
- 每个优先级标记单独一行
- 多条标记不要挤在同一行

## 优先级分类

### MUST（`[MUST qN]`）— 关键
满足任一即 MUST：
- 明确要求："must"、"need to"、"required"、"critical"、"essential"、"necessary"
- 指出重大技术缺陷或错误
- 缺关键信息或实验
- 审稿人明确说某处不对/有缺陷
- 提到接受条件
- 需要回答的问题（"Why did you…?"、"How do you justify…?"）
- 索要影响 soundness 的缺失细节

### SHOULD（`[SHOULD qN]`）— 重要
- 强建议："should"、"recommend"、"suggest"、"would be better"、"it would help"
- 要求改进清晰度或呈现
- 建议补实验或对比
- 方法论疑问或顾虑
- 索要更多解释或理由
- 写作质量顾虑
- 范围或完整性顾虑

### COULD（`[COULD qN]`）— 可选
- 小建议："could"、"might"、"consider"、"perhaps"、"optional"、"minor"
- 锦上添花
- 风格偏好
- future work 建议
- 提到的笔误与格式问题
- 对局限的承认（无需行动）

## 工作流
1. **解析结构**：识别审稿人分区（Reviewer 1、Reviewer 2、Meta-review…）
2. **识别点**：找每条独立反馈点或问题
3. **分类优先级**：依语言线索与上下文
4. **加标记**：每条可执行文本前加优先级标记
5. **分配编号**：全文档顺序 q1、q2、q3…
6. **扁平化标题**：子标题转粗体标签
7. **保留列表**：原始列表格式作纯文本
8. `write` 到项目根 `reviews.md`

## 重要规则
1. **保留原文**：只加标记前缀，绝不改原文内容
2. **完整思想**：每条标记捕获一个完整论点，非半句
3. **唯一编号**：q1/q2/q3… 不重用
4. **跳过通用文本**，不标记：
   - 寒暄（"Thank you for your submission"）
   - 无需行动的总结
   - 无可执行建议的正面反馈
   - 元信息（审稿人专长、分数、评级）
5. **上下文重要**：分类时考虑周围文本
6. **拿不准**：默认 SHOULD

## 示例

**输入：**
```
Review #13A
Overall merit: 4. Accept
Strengths: + Novel methodology
Weaknesses:
- Limited comparison with recent baselines
- The evaluation section needs more detail
Questions:
1. Why did you choose this specific threshold?
2. Could you provide more ablation studies?
```

**输出（reviews.md）：**
```
**Review #13A**
Overall merit: 4. Accept

**Strengths**
+ Novel methodology

**Weaknesses**
**[SHOULD q1]** - Limited comparison with recent baselines
**[SHOULD q2]** - The evaluation section needs more detail

**Questions for the author response**
**[MUST q3]** Q1: Why did you choose this specific threshold?
**[COULD q4]** Q2: Could you provide more ablation studies?
```

## 下游
- `xept:write-response`：据每条 `[qN]` 逐条写回复（按类型卡字数）
- `xept:write-rebuttal`：跨审稿人合并写战略性统一文档
- `xept:finalize-rebuttal`：打磨成可提交定稿

## GitHub 集成（可选，团队追踪）

**仅当**两个条件都满足才做：会话提供 `mcp__github__*` 工具，且 `.self_xept/project.yml` 配有 `repo: owner/name`（团队协作字段）。任一缺失 → 静默跳过本节，本地流程不受影响。

满足时，除写 `reviews.md` 外，把每条 MUST/SHOULD 建成 issue（`mcp__github__create_issue`）：
- 标题：`[MUST q1] 摘要 ≤60 字`（qN 编号与 reviews.md 严格一致，保证可追溯）
- 正文：该条原文 + 出处（Reviewer N）
- labels：`must`/`should` + `rebuttal`
- COULD 默认不建（噪音），用户明确要求才建

下游 `xept:write-response` 回复完一条，可 `mcp__github__update_issue` 关对应 issue；`xept:write-revision` 的修订 PR 描述里用 "Closes #N" 挂钩。
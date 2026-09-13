# Stage 1: Plan / 规划

## 目的
生成任务摘要供用户批准，再产出逐节写作大纲。

## 前置条件
- Stage 0（读需求、分析用户素材）已完成
- 已读 `.self_xept/project.yml`（venue / field / language / page_limit / engine）
- 上下文中已有内容分析

## 工作流

### Step 1: 加载领域知识
读结构模板：`read` knowledge/<field>/structures/default.md`；若该文件不存在，回退 `Read knowledge/general/structures/default.md`。

### Step 2: 生成任务摘要
基于 Stage 0 的分析，整理任务摘要：

```
venue:        # 来自 .self_xept/project.yml 或用户
field:        # 已识别的领域
language:     # 论文语言
idea:         # 核心研究想法（1-2 句）
motivation:   # 为什么重要
contribution: # 新颖之处
methodology:  # 简要方法
todos:        # 逐节写作待办
```

**向用户展示该方案，然后停下等待批准。** 不得在用户批准前开始写作。

### Step 3: 处理用户回复

| 回复 | 动作 |
|------|------|
| 批准 | 存入 `.self_xept/state.md`（## Task），进入大纲 |
| 修改 | 按改动更新后存入，进入大纲 |
| 拒绝 | 问清要改什么，重新生成 |

### Step 4: 生成写作大纲
大纲结构由**你**基于以下因素决定：
- 领域惯例（你知道本领域标准章节）
- venue 要求（`.self_xept/project.yml`）
- 用户素材（有哪些可用内容）
- 参考论文结构（`.self_xept/references.md` 的 `## Writing Style`，若有）
- 页数限制（据此分配篇幅）

每节大纲格式：
```markdown
## [章节名]
- [段落] **主题**: 逐句计划（S1, S2, S3…）
  - 内容来源: [出自哪份素材]
- [图表] **名称**: 描述
  - 内容来源: [数据来源]
```

大纲规则：
1. **每节有词数/页数预算**（按总页数和领域惯例）
2. **每段有逐句计划**
3. **内容来源都标注**（每段内容来自哪份素材）
4. **图表都计划好**（展示什么数据、放在哪）
5. **总篇幅符合页数限制**

### Step 5: 保存大纲
`write` 到 `.self_xept/outline.md`（`## Structure`）：
```markdown
# Writing Plan: [论文标题]

**Field:** [field]
**Venue:** [venue]
**Language:** [language]
**Page Limit:** [N pages]

---

## [章节 1]
...
```

## 输出
- `.self_xept/state.md`（## Task）— 用户批准的任务计划
- `.self_xept/outline.md`（## Structure）— 逐节大纲

## 进入 Stage 2 前的校验
- [ ] 用户已批准方案
- [ ] `outline.md`（## Structure）存在，所有章节已规划
- [ ] 每节有词数/页数预算
- [ ] 每段有逐句计划
- [ ] 总篇幅在页数限制内

**全部通过前不得进入 Stage 2。**
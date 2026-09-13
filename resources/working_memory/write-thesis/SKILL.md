---
name: write-thesis
description: 写学位论文（本科/硕士/博士，任意学科）。逐章写作、按字数与学校模板合规衡量（非页数与编译）。阶段化流程 分析→规划（待批准）→逐章写→格式与字数与一致性打磨。期刊会议论文用 xept:write-paper，技术报告用 xept:write-report。
---

# Write Thesis（写学位论文）

逐章学位论文写作。适用任意领域、任意层次（本科、硕士、博士）。

## 核心原则

**本技能管流程与纪律。LLM 管内容与领域专长。**

与 `xept:write-paper` 的主要区别：学位论文按**章**和**字数**衡量，而非页数与编译。**学校模板合规与格式规则优先于 venue 要求**。

## 阶段

```
Stage 0: Analyze   → 读学校模板 + 填约束 + 提取素材
Stage 1: Plan      → 章节大纲（待用户批准）+ 字数分配
Stage 2: Write     → 逐章写作
Stage 3: Refine    → 格式合规 + 字数 + 一致性检查
```

每阶段是一份文件：`read` 本技能目录下 `stages/N-*.md`（与 write-paper 共享同一阶段引擎）。

## 强制规则

### 规则 1：阶段顺序
按序执行，绝不跳步。

### 规则 2：先填 project.yml
Stage 0 未完成前，`.self_xept/project.yml` 必须填好：
- Field（学科/专业领域）
- Template（学校格式要求）
- Length limit（每章或总字数）
- Language
- Citation format

### 规则 3：写作前确认
Stage 1：**向用户展示章节方案并停下等待批准**，批准前不得写任何章。

### 规则 4：逐章写作
**绝不一次性写多章。** 每章独立审阅后才进下一章。

### 规则 5：加载领域与学位知识
写每章前：
- 学位论文结构：`read` knowledge/<field>/structures/default.md`；缺失回退 `knowledge/general/structures/default.md`（学位论文专属结构详见本技能 `refs/{degree_level}.md` + `refs/common.md`）
- 章节指南：`Read knowledge/<field>/sections/{chapter_type}.md`；缺失回退 `knowledge/general/sections/{chapter_type}.md`
- 学位规范：`read` 本技能目录下 `refs/{degree_level}.md`（undergrad/master/phd）和 `refs/common.md`

## 元状态文件

| 文件 | 用途 |
|------|------|
| `.self_xept/project.yml` | 学校模板规则、领域、引用格式、字数限制 |
| `.self_xept/references.md`（## Writing Style） | 从参考论文学到的风格（若提供） |
| `.self_xept/references.md`（## Literature Index） | 从用户素材提取的内容 |
| `.self_xept/state.md`（## Task） | 用户批准的章节计划 |
| `.self_xept/outline.md`（## Structure） | 逐章计划含字数预算 |
| `.self_xept/facts.md` | 关键术语——跨章保持一致 |

## 速查
```
1. `read` stages/1-plan.md → 读模板 + 填约束 + 提取素材
2. `read` stages/1-plan.md 规划 → 章节方案 → 展示 → 停等批准 → 大纲
3. `read` stages/2-write.md → 逐章写
4. `read` stages/3-refine.md → 格式检查 + 字数 + 一致性
5. 向用户报告完成
```

## 与查重/AIGC 的关系
学位论文有查重率与 AIGC 率上限（各层次不同，见 `refs/common.md`）。完成初稿后可用 `xept:reduce-ai` 降低 AI 痕迹、`xept:paraphrase` 改写降重。
---
name: write-rebuttal
description: 写战略性 rebuttal 信——跨审稿人合并相关关切、按主次排序、按审稿人态度调语气、有说服力且尊重。产出统一文档 rebuttal.md。与 xept:write-response 区别：response 是逐条 point-by-point，rebuttal 是战略性统一文档。打磨定稿用 xept:finalize-rebuttal。
---

# Write Rebuttal（写战略性 rebuttal）

写 rebuttal 信，整体地回应审稿人关切。

- 按主次排序（major vs minor）
- 识别审稿人态度、据此调语气
- 把不同审稿人的相关关切合并成统一回复
- 有说服力，同时保持尊重

**与 `xept:write-response` 区别**：response 是逐条 point-by-point；rebuttal 是战略性、统一文档。

## 工作流
1. `read` 论文（main.tex）——理解贡献、方法、结果
2. `read` 审稿意见——可用 `xept:analyze-reviews` 先解析出优先级与 `[qN]`
3. `read` `.self_xept/project.yml`——rebuttal 字数/格式限制
4. **归类合并**：把跨审稿人的相关关切聚类（如 R1-Q2 与 R2-Q1 都讲 baseline 对比 → 合并一条统一回复）
5. **排序**：MUST（影响 soundness/接受）优先；SHOULD 次之；COULD 合并简述或略
6. **按态度调语气**：正面审稿人简洁答谢；负面审稿人带证据、先承认对的
7. **写统一文档**：`write` 到项目根 `rebuttal.md`，结构为 总览致谢 → 按主题/审稿人组织的主要回复 → 修订总结表

## 写作要求
- **带数字/证据**：每条主张引 Section/Table/Line 或新跑的结果
- **展示已做，非承诺**："We ran… performance drops to Y%" 优于 "We will add experiments"
- **合并去重**：同主题多审稿人意见一条统一回复，注明 (addresses R1-Q2, R2-Q1)
- **修订总结表**：末尾列 Section/Table 改动与对应的 qN
- 遵循外交辞令（见 `xept:write-response` 的替换表）

## 相关技能
- `xept:analyze-reviews`：上游，解析意见、标优先级
- `xept:write-response`：逐条回复（与本技能二选一或互补）
- `xept:finalize-rebuttal`：下游，打磨定稿
---
name: write-response
description: 逐条 point-by-point 回复审稿意见（按意见类型卡字数：MUST 80-150 词 / SHOULD 50-100 / COULD 30-60），插入 rebuttal.md。战术、逐条。跨审稿人合并的战略性统一文档用 xept:write-rebuttal；打磨定稿用 xept:finalize-rebuttal。
---

# Write Response（逐条回复审稿意见）

生成专业、有策略的逐条回复，写入项目根 `rebuttal.md`。

## 工作流
1. **读论文**：理解贡献、方法、结果
2. **读审稿意见**：理解完整上下文与审稿人整体倾向（可用 `xept:analyze-reviews` 先解析出 `[qN]` 编号）
3. **读 rebuttal**：`read` `rebuttal.md` 找响应区，看已写了什么
4. **分析**意见类型与审稿人态度
5. **生成**回复，遵循下方策略
6. **插入**：用 `edit` 写入 `rebuttal.md`

## 字数限制（严格）
- MUST 类：80-150 词
- SHOULD 类：50-100 词
- COULD 类：30-60 词

## 意见分析框架

### Step 1: 识别意见类型

| 类型 | 描述 | 示例 |
|------|------|------|
| **有效批评** | 审稿人对，论文有问题 | "baseline 对比不全" |
| **误解** | 审稿人读漏/读错 | "你没解释 X"（X 其实在第 3 节） |
| **范围蔓延** | 超出论文范围的要求 | "应再对比 20 个方法" |
| **吹毛求疵** | 小问题放大 | "图 3 字号小" |
| **澄清请求** | 只需解释 | "为何选 threshold=0.5？" |
| **不可能请求** | 做不到（数据/资源限） | "在 1000× 大数据集上跑" |

### Step 2: 判断审稿人倾向
- **正面**（Accept/Weak Accept）：想帮改进，非拒
- **中性**（Borderline）：可上可下，需说服
- **负面**（Reject/Weak Reject）：找拒稿理由，格外小心

### Step 3: 选回复策略

| 意见类型 | 正面审稿人 | 中性 | 负面 |
|----------|-----------|------|------|
| 有效批评 | 承认+修 | 承认+修+解释为何 | 承认+修+展示影响 |
| 误解 | 委婉澄清 | 澄清+为困惑致歉 | 外交辞令澄清+引论文原文 |
| 范围蔓延 | 承认作 future work | 解释范围+给部分 | 礼貌但坚定拒绝并给理由 |
| 吹毛求疵 | 快修 | 修+简短致谢 | 修，不过度致歉 |
| 澄清 | 直接答 | 答+补进论文 | 详答+给证据 |
| 不可能 | 解释局限 | 解释+替代方案 | 技术上解释为何不可能 |

## 分情境回复模板

### 1. 有效批评——我们修了
```
We appreciate this observation. [简短承认]

We have [具体行动]:
- [改动 1] (Section X, Line Y)
- [改动 2] (Table Z)

[可选：简述这如何改进论文]
```

### 2. 误解——论文里已有
```
We thank the reviewer for raising this point. This is addressed in [Section X / Table Y / Figure Z], where we [简述].

We acknowledge this可以更清楚。修订中我们已 [added emphasis / restructured / added cross-reference]。
```

### 3. 范围蔓延——做不到
```
We appreciate this suggestion. [Method/Dataset X] 是有趣方向；但超出本工作范围，本工作聚焦 [论文实际范围]。

We have added this as a promising direction for future work in Section [X].
```

### 4. 不可能请求——技术局限
```
We appreciate this suggestion. Unfortunately, [简短技术原因].

As an alternative, we have [改做了什么], which provides [相关洞见].
```

### 5. 分歧——外交辞令回推
```
We respectfully provide additional context on this point. [你的证据/理由 2-3 句，引具体 section/figure/table].

We believe [结论], but we have added [澄清/讨论] in Section X to address this concern.
```

## 关键规则

### 要做
- **引论文**："As shown in Section 3.2…"、"Table 2 demonstrates…"
- **改动要具体**："Line 234"、"Figure 3 caption"
- **先承认对的**，再解释/防守
- **用 "we" 非 "I"**

### 不要做
- **别每条都 "Thank you"** — 每个审稿人一次够
- **别防御** — 绝不 "The reviewer is wrong"
- **别过度致歉** — 最多一次，然后给方案
- **别承诺做不到的**
- **别填充**："This is a great question"、"We really appreciate"

### 外交辞令替换：

| 别说… | 改说… |
|-------|-------|
| "You misunderstood" | "We may not have explained clearly" |
| "This is wrong" | "We respectfully note that…" |
| "We can't do this" | "This is beyond current scope" |
| "This is already in the paper" | "This is addressed in Section X, where…" |

## 相关技能
- `xept:analyze-reviews`：先解析意见、标 `[qN]` 优先级
- `xept:write-rebuttal`：跨审稿人合并的战略性统一文档（本技能是逐条，它是一体）
- `xept:finalize-rebuttal`：打磨成可提交定稿
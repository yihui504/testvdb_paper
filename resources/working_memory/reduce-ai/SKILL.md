---
name: reduce-ai
description: 降低 AI 写作痕迹（四层检测+改写：词汇/句法/论证/研究者声音）。用于用户说"降 AI 率/清理 AI 味/太像 AI"、或大批量 AI 生成之后（如 xept:write-paper 之后）。四层中 Layer 3-4 对审稿人感知影响远大于 1-2。本技能是"深度"四层检测+改写；xept:check-submission 只做"轻量" AI 检查后会推荐本技能。
---

# Reduce AI（降低 AI 痕迹）

检测论文中的 AI 痕迹并改写标红段落。四层，按影响排序——**Layer 3-4 远比 1-2 重要**。

> 审稿人不跑 GPTZero。他们读一段就会想："这不像是真跑过这些实验的人写的。"破绽不在词汇，而在**缺少挣扎、权衡和真诚的不确定**——这些只有真实研究才有。

## 何时用
- 用户说"降 AI 率"、"清理 AI 味"、"太像 AI"
- 大批量 AI 写作之后（如 `xept:write-paper` 之后）

## 四层总览

| Layer | 抓什么 | 审稿人影响 | 难度 |
|-------|--------|-----------|------|
| **L1: 词汇** | 黑名单词/短语 | 低（表面） | 易 |
| **L2: 句法** | 套路句式、节奏单一 | 中 | 易 |
| **L3: 论证** | 缺权衡、无条件主张 | **高** | 中 |
| **L4: 研究者声音** | 无不确定、无失败、泛泛 future work | **最高** | 难 |

## 工作流
```
1. 向用户确认后开始
2. 读全文（所有 .tex）
3. 加载检测规则：`read` 本技能目录下 refs/{lang}.md（chinese/english）
4. 跨四层逐节检测
5. 汇报：发现 N 处 AIGC、X 词汇、Y 句法、Z 论证/声音
6. 按 L1→L2→L3→L4 修（表面→深层）
   - AIGC：标红给用户（不能编造正确内容）
   - L1-L2：直接改写
   - L3-L4：带领域推理改写；不确定时问用户并等待
7. 重新编译验证
```

---

## Dimension 0: AIGC 检测
识别编造内容。**不能自动修——标红给用户。**

| 检查 | 怎么做 | 可自动修？ |
|------|--------|-----------|
| 可疑引用 | .bib 里但像编造（怪标题、不存在的期刊、DOI 不符） | 否——标红 |
| 编造统计 | 无来源的数字、无表/图支撑 | 否——标红 |
| 不存在的方法 | 引用了不存在的工具/方法 | 否——标红 |
| 编造主张 | "X et al. showed that…" 无法核实 | 否——标红 |

---

## Layer 1: 词汇
完整词表见本技能 `refs/{lang}.md`。

**Tier 1 先脚本扫**——跑 `python scripts/scan_ai_words.py <main.tex>` 标出所有 Tier1 黑名单词 + 行号（确定性 grep，脚本化），LLM 据结果替换；Tier2/3 需段落聚集判断，留 LLM。

**原则：**
- **Tier 1**（delve, underscore, intricate, meticulous, pivotal, showcase, robust, comprehensive, leverage, utilize, harness, novel, cutting-edge, seamless, multifaceted, holistic, unprecedented, paradigm）：**一律替换**（脚本已标位置）
- **Tier 2**（significant, innovative, effective, compelling, remarkable, sophisticated, facilitate, foster, bolster, navigate, cornerstone, paramount）：**同段 ≥2 个才标红**
- **Tier 3**（furthermore, moreover, notably, consequently, additionally）：**聚集才标**——一个没事，一页三个不行
- **阈值**：不标孤立出现，标**模式和聚集**

---

## Layer 2: 句法
检测并修结构性模式。完整模式见知识文件。

**关键模式：**
- 套路开头："This paper proposes…" → "We introduce…" / "The key idea is…"
- 填充过渡："It is worth noting that" → 删
- 清嗓子："In the rapidly evolving landscape of…" → 删
- 段/句长度单一 → 变化（burstiness）
- 三件套默认 → 用自然数量
- 堆叠对冲："may potentially" → "may"
- 系动词回避："serves as" → "is"
- 谄媚 rebuttal 开头："We thank the reviewer for the insightful comments" → 直奔问题
- "In conclusion" → 顶会常省略；结论直接上干货

---

## Layer 3: 论证 — 最重要的层
审稿人真正凭此识破 AI。无条件正面主张 = AI 味。

### 3.1 缺权衡（单一最大破绽）
AI: `Our method improves accuracy and efficiency.`
人: `The gain in accuracy comes at the cost of additional inference overhead (Table 4).`
**检测**：主张改进却无成本/限制/条件。**修**：加成本、条件、边界或比较限定。

### 3.2 无条件主张
AI: `Method A outperforms Method B.`
人: `Method A achieves higher accuracy on four of five datasets, though the margin narrows when training data are scarce (Figure 3b).`
**检测**：绝对主张无条件/例外/范围。**修**：加条件、范围或限定数据。

### 3.3 全正面结果
AI: `The results show our approach is effective across all settings.`
人: `The approach works well on structured data but degrades on free-form text. We hypothesize this is due to the tokenization mismatch (§3.2).`
**检测**：结果节零负面发现。**修**：margin 最小在哪？什么最难？失败模式会是什么？

### 3.4 空洞局限
AI: `A limitation is scalability. Future work will address this.`
人: `Trace collection scales linearly with execution length, reaching 40 min for 500-step trajectories. Parallelization could reduce this but requires re-designing the state-merge protocol (§5.1).`
**检测**：泛到能套任何论文的局限。**修**：每个局限都具体（是什么）、量化（多糟）、分析（为什么）。

### 3.5 目录式 related work
AI: `Smith (2023) proposed X. Jones (2024) extended this to Y. Our work differs by Z.`
人: `Smith (2023) addressed X but assumed fixed vocabulary, which breaks in our open-ended setting. Jones (2024) relaxed this but added 3× latency. We avoid both by...`
**检测**：related work 只罗列无真正比较。**修**：每篇引文——好在哪、哪不适用、你的方法为何不同。

---

## Layer 4: 研究者声音
研究过程本身的存在——决策、死路、意外、不确定。

### 4.1 不确定语言
| AI-确定 | 研究者 |
|---------|--------|
| demonstrate | suggest, indicate |
| prove | support, provide evidence for |
| confirm | are consistent with |
| reveal | appear to show |
| establish | point toward |
**规则**："demonstrate" 只用于可形式化证明的主张。经验发现 → "suggest"、"indicate"、"show"。

### 4.2 失败与意外
真论文有："surprisingly"、"unexpectedly"、"counter to our expectation"、"we initially tried X but"。
**检测**：零意外/失败语言。**修**：找 2-3 处结果意外或初试失败的地方。

### 4.3 设计决策理由
AI: `We use a transformer encoder with 6 layers.`
人: `We chose 6 layers after finding deeper models overfit on our dataset (Appendix B). A CNN baseline failed to capture long-range dependencies.`
**检测**：设计选择无理由。**修**：关键决策——为何选它、替代方案是什么。

### 4.4 具体 future work
AI: `Future work will focus on scalability and generalization.`
人: `A remaining challenge is scaling trace collection to long-horizon tasks (>1000 steps). Checkpoint-based sampling is promising but trades completeness for efficiency.`
**检测**：future work 泛到能进任何论文。**修**：针对本论文发现、技术上具体、诚实面对难度。

### 4.5 Rebuttal 声音
| AI rebuttal | 强 rebuttal |
|-------------|-------------|
| "We thank the reviewer for the valuable comments." | "The reviewer raises an important question regarding trace quality." |
| "We agree that scalability is important." | "To quantify the scalability concern, we measured runtime on three additional workloads..." |
| "We will add more experiments." | "We ran the suggested experiment. Performance drops to Y%, confirming Z is the bottleneck." |

**Rebuttal 规则：**
1. 以问题开头，非致谢
2. 带数字
3. 展示你**做了**什么，别承诺
4. 审稿人对时承认
5. 用证据反对，非修辞

---

## 改写规则
1. **精确保义** — 只改说法
2. **术语不动** — 不为既有术语造同义词
3. **干净段落跳过** — 自然文本不碰
4. **别降质** — 清晰的 AI 句 > 晦涩的"人话"
5. **逐节做**
6. **先阈值再动手** — 标模式和聚集，非孤立词
7. **L3-L4 需判断** — 权衡/不确定拿不准时问用户并等待
8. **改写 vs 打补丁** — 一段 ≥5 个标红 → 整段重写

## 按节优先级

| 节 | 主层 | 备注 |
|----|------|------|
| Abstract | L1, L2, L3 | 最高审视。零填充、零膨胀。 |
| Introduction | L1, L2, L3 | 动机要真。 |
| Related Work | L2, L3 | 真正 engagement，非罗列。 |
| Method | L3, L4 | 设计决策要有理由。 |
| Experiments | L3, L4 | 权衡、失败案例、意外。 |
| Discussion | L3, L4 | 研究者声音最重要。 |
| Conclusion | L1, L2 | 简短，不膨胀。 |
| Rebuttal | L2, L4 | 不谄媚，以干货开头，带数据。 |

## 输出
```
Reduce AI 完成。

AIGC（内容）— N 处标红：
- [file:line] 描述
→ 请人工核实。

L1（词汇）— X 处：
- 替换 N 个黑名单词（leverage→use, robust→stable, ...）

L2（句法）— Y 处：
- 删 N 个 em-dash、N 个过渡、N 个清嗓子
- §X 段落长度变化

L3（论证）— Z 处：
- 给 N 个主张加权衡
- 给 N 个绝对句加条件
- 强化 N 处 related work 比较

L4（研究者声音）— W 处：
- 给 N 个主张加不确定语言
- 记 N 处意外/负面发现
- future work 具体化

改动见 diff。请复核，尤其 L3-L4。
```

## 与其他技能的关系
- `xept:check-submission`：**轻量** AI 检查 → 发现问题会推荐本技能。
- `xept:reduce-ai`（本技能）：**深度**四层检测 + 改写。
- 不互相调用。
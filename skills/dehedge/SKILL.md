---
name: dehedge
description: 消除论文里的防御性写作——过度对冲、预防性道歉、消极自我设限、防御性过渡词，同时把真正必要的方法论限制归位到正确的章节（Methods/Limitations）。用于用户说"这段太怂/太保守/申辩味重/审稿人说我 overclaim 但这也是没底气"、或成稿里通篇"我们不做/我们不声称/值得注意"时调用。产出 claim-forward 的稿子，不削掉该有的精度。区分：降 AI 痕迹用 xept:reduce-ai（它反而加不确定；dehedge 是去不该有的不确定）；改引用用 xept:add-citation；翻译用 xept:translate-paper。
---

# Dehedge（反防御性写作）

把犹豫的、过度自我保护的稿子改成**直接、claim-forward、有底气**的稿子——同时**严格保留必要的方法论约束与精度边界**。

> 核心规则：**直接推进主张。** 说什么是真的、论文论证了什么、证据显示了什么、方法做了什么。不要默认先解释"论文**不**声称什么、**不**证明什么、**不**覆盖什么、**不**试图什么"。
>
> 用平静、有能力的作者姿态：是作者在向读者解释论据，不是作者在跟想象中的批评者谈判。

## 何时用

- 用户明说"太怂/太保守/申辩味重/没底气/审稿人说我 overclaim 但内容也就那样"
- 成稿里通篇「我们并不试图 / 本文并不声称 / 值得指出的是 / 需要说明的是 / 可能或许」这类语言
- 论文投出去前，想让摘要/intro/贡献段更挺直

## 何时不用（真实边界）

- **诚实的不确定性**不删——那是 `xept:reduce-ai` L4 的领地（该有的不确定要留、"demonstrate" 别乱用）。dehedge 只删**不必要的**防御，不把真实局限改没。
- **故意保留的谨慎语气**（如医学伦理、政策建议节）——尊重作者意图，别机械化清空。
- **rebuttal 信**——回复审稿人需要策略性语气与致谢，dehedge 不适用或只局部用（驳回式 rebuttal 反而要克制）。
- 纯改词不改主张——那是 `xept:paraphrase`。

## 与 reduce-ai 的边界（关键）

两者在「不确定」轴上**方向相反**，别混：

| | `xept:reduce-ai` L4 | `xept:dehedge` |
|---|---|---|
| 处理 | AI 味的**无条件绝对主张**——缺少该有的权衡/限制 | 作者焦虑的**过度防御**——不必要的对冲/道歉 |
| 动作 | **加**不确定、加成本、加条件 | **删**不必要对冲、删道歉、转正面表述 |
| 判断 | "这个主张太满，不够诚实" | "这句太怂、太申辩，不必这么自保" |
| 触发词 | demonstrate/prove/confirm 滥用 | we do not claim / 本文并不试图 / 值得指出 |

**重合点**：堆叠对冲（"may potentially"）两者都抓——reduce-ai 当作 AI-tell，dehedge 当作防御性弱化。谁的场景由用户意图定：本想"去 AI 味"→ reduce-ai；本想"挺直腰杆"→ dehedge。句子同时满足两者时先 dehedge 定稿再 reduce-ai 过一遍。

## 检测清单（扫描 + 人工判断）

**先跑确定性扫描**：`python scripts/scan_hedges.py <main.tex>` 标出全部 Tier1 防御短语 + 行号。Scanner 只**标候选**，要不要删由判断层决定（真局限不能删）。

然后逐段人工查：
- [ ] 不必要的免责声明（先解释论文**不**做什么）
- [ ] 重复的"论文不声称/不证明/不覆盖"
- [ ] 过度对冲（may/might/could/potentially 堆叠；中文"可能或许/在一定程度上"）
- [ ] 高影响力位置的 caveat（摘要、贡献段、topic sentence、结论）
- [ ] 以"局限"开头的段落（把 findings 往后推）
- [ ] 负面框架（negative framing）——用正面能表达
- [ ] 只为防止假设性误解而加的说明
- [ ] 自我拆台的贡献声明
- [ ] 不必要"not X but Y"结构
- [ ] 冗余转折（however/nevertheless/although 堆叠；虽然后续）

## 重写流程

> 本质行：**分类 → 删免责 → 转正面 → 精化精度 → 重建段落 → 复核**。

### Step 1: 定位每句防御句的功能
归类为：不必要免责 / 必要 scope 条件 / 真实方法论局限 / 有用的概念对比 / 证据支撑的限定 / 冗余澄清。

### Step 2: 删除不必要免责
凡不加证据、不加 scope、不加逻辑、不加概念精度、不加必要读者指引的句子——删。

### Step 3: 把"防御性局限"转成"正面 scope"
> 正面：The analysis focuses on urban governance cases from 2015 to 2023.
> 避免：We do not claim that these cases are representative of all urban governance contexts.
> 中文：本文聚焦 2015–2023 年的城市治理案例。｜避免：本文并不声称这些案例能代表所有城市治理情境。

### Step 4: 用精度替代对冲
> 证据：The evidence indicates that X influences Y in these cases.
> 避免：This may suggest that X could potentially influence Y.
> 中文：证据表明在本组案例中 X 影响 Y。｜避免：这可能暗示 X 或许可能影响 Y。
> 若不确定是**真的**，写明来源：The available evidence supports this interpretation, although the design does not estimate population-level effects.

### Step 5: 围绕主干重建段落
每段：清晰 topic sentence + 一个主要职责 + 逻辑顺序 + 无重复 caveat + 无道歉框架 + 与更大论点的直接联系。

### Step 6: 复核，确认没削掉必要精度
对每个保留的局限问：它影响 claim 有效性 / 证据解释 / 应用范围 / 研究设计 / 读者正确使用吗？若是——归位到 Methods / Limitations 节，写一次、平静、清楚；**不**散落进摘要、intro、贡献句、结论。

## 首选模式

"This paper examines…" / "This study shows…" / "The analysis focuses on…" / "The evidence indicates…" / "This design allows…" / "The central contribution is…" / "在此设定下，X 通过 Y 塑造 Z。" / "本文识别了一个……的机制。"

## 避免模式（除非对准确性必要）

"This paper does not claim…" / "We do not attempt to…" / "This is not to say that…" / "This should not be taken to mean…" / "The goal is not X but Y…" / "Rather than arguing X, this paper argues Y…" / "Although this study has limitations…" / "Of course, this does not fully capture…" / "It is worth noting that…" / "To be clear…"
中文对应：本文并不声称… / 我们不试图… / 这并不是说… / 不应把这一点理解为… / 本文的目的不是 X 而是 Y / 与其说论证 X，不如说… / 虽然本研究存在局限… / 当然，这并不能完全涵盖… / 值得注意的是… / 需要说明的是…

## 集成

- **上游**：`xept:write-paper` 各节写作后、`xept:paraphrase` 降重后跑一遍本技能定稿。
- **下游**：定稿稿子再进 `xept:check-submission`（轻量合规）与 `xept:reduce-ai`（若有 AI 味残留）。
- **协同**：`xept:write-response`/`xept:write-rebuttal` 是策略性文档，不被本技能清空语气（见何时不用）。
- **检测**：确定性扫描脚本 `scripts/scan_hedges.py`（仿 reduce-ai 的 `scripts/scan_ai_words.py`）。

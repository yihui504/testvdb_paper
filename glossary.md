# TestVDB 术语 Glossary

> 治「夹生饭」和「讲不清概念」。每个词：**通用定义 → 为什么重要 → 在你工作里指什么**。
> 持续维护；遇到不确定的译法/概念就回来更新。
> 这是 A1（补认知）的产物，同时把 A2（Barr oracle taxonomy）的精华并入「oracle taxonomy」节。

---

## 一、通用软件测试 / oracle 概念（讲 CTS 前必须懂的背景）

### oracle（测试预言 / 预言机）
- **定义**：判断「程序在某输入下行为对不对」的标准/机制。有输入 + 有 oracle = 能判 pass/fail。
- **为什么重要**：整个软件测试理论的基石。大量测试难题本质是「没有 oracle」。
- **在 TestVDB**：你的核心问题就是「合规缺陷没有 oracle」——crash 当不了，没有 reference impl。

### oracle problem（预言问题）
- **定义**：有测试输入，但不知道「正确行为」是什么，无法判 pass/fail 的困境。
- **在 TestVDB**：工作的出发点。43% 的 bug 是 incorrect behavior，但没有 oracle 判断对错。

### oracle taxonomy（预言分类）—— Barr et al. 2015 *The Oracle Problem in Testing*
**这是你排除法（Table 1）该用的框架**。oracle 分几类：
- **specified（规约型）**：人/文档明确写了「正确行为」→ 你的 contract oracle 属此类。
- **derivable（可推导型）**：从数学/逻辑推出正确行为（如 cos∈[-1,1]）→ 你的 model-free invariant（COSINE>1.0）属此类。
- **implicit/redundant（隐含/冗余型）**：用已知正确的版本/等价形式对比（differential、metamorphic）。
- **none（无）**：只能靠人判。

**排除法逻辑（用 taxonomy 讲，审稿人服）**：合规缺陷——specified oracle 是文档（但可能错，见 contract hallucination）；derivable 只覆盖数学不变量子集；implicit（differential/metamorphic）不适用（无 reference、无可变换形式）；→ 只剩 LLM 做语义判断。

### contract（契约）
- **定义**：API 的「应该怎样」——前置条件、后置条件、不变量。源自 **Design by Contract**（Meyer 1992）。
- **在 TestVDB**：从 API 文档提取的「这个输入该被接受/拒绝」的规约。

### assertion（断言）
- **定义**：一个可判真假的声明（程序里 `assert(x>0)`）。
- **在 TestVDB**：LLM 从文档推出的「输入 X 应被拒绝」这类声明。CTS 的「断言层」= 这些 LLM 生成的声明。

### compliance（合规 / 符合性）
- **定义**：行为符合规定（契约/标准）。
- **在 TestVDB**：「API 合规缺陷」= 行为违反文档契约却不崩。

### falsification（证伪）
- **定义**：试图证明一个判断是**错的**（不是证明它对）。源自 Popper 科学哲学。
- **在 TestVDB**：dev-reviewer 不是「确认」LLM 的判断，而是「推翻」它（用源码找反证）。**这是 CTS 的方法实质——所以方法名该叫 `source-grounded falsification`，不叫 separation。**

---

## 二、其他测试方法（排除法要逐个排除的）

### differential testing（差分测试）
- 多个实现跑同输入，输出不一致=bug。需 ≥2 个可对比实现。
- **为什么不行**：VDB API 跨厂商无统一语义，没有可对比的 reference。

### metamorphic testing（蜕变测试）
- 没 oracle 时，找「输入变换下输出应满足的关系」（metamorphic relation）。如「输入翻倍→输出翻倍」。
- **为什么不行**：合规是 accept/reject 的是非判断，没有「可变换的等价查询形式」让关系成立。

### property-based testing（基于性质的测试）
- 给一个 property（如「任何合法输入不应崩溃」），框架自动生成大量输入测。QuickCheck / Schemathesis / QuickREST。
- **为什么不行**：需 property 可机器表达；文档契约是自然语言不可直接表达；且需标准 schema（OpenAPI），VDB 不提供（你测了 `/swagger` 404）。

### fuzzing（模糊测试）
- 生成大量随机/畸形输入，oracle 通常是 crash。VDBFuzz 属此类。
- **为什么不行**：合规缺陷不崩，crash oracle 检测不到。

---

## 三、TestVDB 特定术语（你工作的词）

### contract hallucination propagation（契约幻觉传播）—— ✅ 该命名，有实质
- **定义**：同一个 LLM 家族既「生成」契约、又「判定」合规时，生成端造错的契约，判定端不会推翻（共享偏见）→ 幻觉在生成-判定链里被自我确认。
- **为什么是真贡献**：在 testing 场景这样形式化该失败模式，无先例。底层类似 LLM self-preference bias，但 instantiation 是新的（A4 文献帮你界定边界）。
- **实证**：12/48 已裁定提交（25%）被维护者判 by-design = 契约比真实意图更严 = 幻觉的直接观测。
- **形式化**：单层判断假设 C_LLM = C_true；当 C_LLM ⊃ C_true（更严），真 by-design 行为被判违规，而 judge 共享生成端偏见不 dissent。

### CTS (Contract-Truth Separation) —— ⚠️ 名实不符，待重定位（见 checklist B1）
- **方法实质**：用一个能查源码的独立 agent 去证伪 LLM 的合规判断。
- **问题**：名字（separation / principle 句式）撑不住内容，组会老师觉得「造词吹牛」；用户自评也觉得「就是查源码 agent」。
- **候选**：降调为 `source-grounded falsification`（源码锚定证伪）。

### dev-reviewer（开发者视角审稿 agent）
- 模拟维护者 triage bug report：独立复现 + 查源码 + 排除平凡解释 + 结构化裁决。论文 §3.4。双盲（不看 attack 脚本的断言逻辑）。

### threat model（威胁模型）
- 安全领域指「对手能做什么」。TestVDB 借用指「已知 by-design 意图 + 盲点」，作生成/判定的先验。**论文已降为 exploratory pilot**（n=12、不稳定、wiring gap），**别当核心卖点**。

### by-design
- 维护者判定「这是设计如此，不是 bug」。你的 12 个 by-design = 契约幻觉的产物（LLM 契约比真实意图严）。

### triage（分诊 / 分类）
- 维护者对 incoming bug report 分类（fix / accept / wontfix / by-design / duplicate）。你的「maintainer-adjudicated」= 维护者 triage 后的结果。

---

## 中英对照速查

| 英文 | 中文标准译法 |
|---|---|
| oracle | 测试预言 / 预言机 |
| oracle problem | 预言问题 |
| contract | 契约（Design by Contract = 契约式设计）|
| assertion | 断言 |
| compliance | 合规 / 符合性 |
| falsification | 证伪 |
| source-grounded | 源码锚定 / 基于源码的 |
| differential testing | 差分测试 |
| metamorphic testing | 蜕变测试 |
| property-based testing | 基于性质的测试 |
| fuzzing | 模糊测试 |
| false positive / true positive | 假阳性（误报）/ 真阳性 |
| by-design | 设计如此 / 设计意图 |
| triage | 分诊 / 分类 |
| threat model | 威胁模型 |

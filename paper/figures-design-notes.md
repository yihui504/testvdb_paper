# 核心概念图设计笔记（作图内容蓝图）

> 目的：给 3 张核心概念图（#3 source-ambiguity gap / #4 两层错误 Venn / #5 pipeline）提供**具体直观的图例**，用 TestVDB 真实 parameter 让概念落地。matplotlib 草图仅作布局参考，你自行作更美观的图。
> 所有图例用论文真实数据：`shardsNum` / `timeout` / `consistencyLevel`（e2 + W1 probe 的真实 cases）。

---

## 图 #3：source-ambiguity gap（P12，最核心 insight）

### 设计目标
一句话让审稿人看懂："为什么 REST-API oracle 工作（AGORA+/SATORI/MASTOR）可靠，但 VDBMS documentation 不可靠？因为源的歧义度不同。"

### 核心对比：transcribe vs interpret
- **低歧义源 → LLM transcribe（转录）**：约束已显式，LLM 只是抄录 → assertion 可靠
- **高歧义源 → LLM interpret（解释）**：约束在自然语言里隐含，LLM 要猜 → claim 可能错

### 具体图例（左右分屏，中间裂缝）

**左半屏 — Structured sources（REST-API oracle work 的领地）**

三张并排小卡片，每张"源 → 提取的 assertion"：

| 卡片 | 源（显示实际内容） | LLM 提取的 assertion |
|------|--------------------|---------------------|
| **OpenAPI** | ```yaml limit:<br/>  type: integer<br/>  minimum: 1``` | `limit >= 1` ✓ |
| **Trace** | ```REQ limit=5 → 200<br/>REQ limit=0 → 400``` | `limit=0 rejected` ✓ |
| **Source code** | ```go if limit < 1 {<br/>  return Err }``` | `limit >= 1` ✓ |

下方标注：**"LLM transcribes — low ambiguity, assertion reliable"**

**右半屏 — Natural-language docs（TestVDB 的领地）**

一张大卡片：

```
Milvus doc:
shardsNum (int, optional, default 1):
  Number of shards to create.
```

下面两条分支（LLM 的两种解读）：
- ❌ GLM 提取：`shardsNum >= 1`（over-strict，以为 0 该拒）
- ✅ 实际语义：`shardsNum=0` → 选 default 1（0 合法）

下方标注：**"LLM interprets — high ambiguity, claim may be wrong"**

**中间**：一道裂缝/锯齿 + 大字 **"SOURCE-AMBIGUITY GAP"**

### 视觉建议
- 左半：冷色（蓝/绿），代码块风格，结构感
- 右半：暖色（橙/红），自然语言段落，手写感
- 中间：锯齿状裂缝或红色渐变箭头，强调"分界"
- 顶部小标题：横轴可画成"Source ambiguity →"渐变条

---

## 图 #4：两层错误 Venn（P14-P15）

### 设计目标
让审稿人看懂："LLM 有两层错误，cross-model 只解一层，source 解两层。"

### 关键区分（必须直观）
- **family-specific**：不同家族**说法不同**（一错一对）→ cross-model 能纠
- **task-intrinsic**：不同家族**说法相同**（都错）→ cross-model 解不了，只有 source 能

### 具体图例（两圈，每圈一个 probe 对比卡）

**左圈 — family-specific（self-preference bias）**

卡片内容（parameter: `consistencyLevel`，Milvus 的 strict enum）：

| | GLM | DeepSeek |
|---|-----|----------|
| 提取的 clause | `consistencyLevel ∈ {Strong, Bounded, Eventually}` | `consistencyLevel ∈ {Strong, Bounded, Eventually}` |
| 判断 `consistencyLevel=Foo` | **违规**（confirm 自己的 strict enum）| **OK**（不认这个 enum） |

→ GLM 和 DeepSeek 判断**不同** → cross-model 能发现分歧 → **cross-model validation 覆盖**

标注：`self-preference`（Panickssery / Wataoka）

**右圈 — task-intrinsic（doc ambiguity）**

卡片内容（parameter: `timeout`，Qdrant doc "optional, default"）：

| | GLM | DeepSeek |
|---|-----|----------|
| 提取的 clause | `timeout >= 1` | `timeout >= 1`（**同样 over-strict**）|

→ GLM 和 DeepSeek 提取**相同（都错）** → cross-model 发现不了分歧 → **cross-model 解不了**

下方加一行 source 解：
```
source code: if timeout == 0 { timeout = default }
→ falsify: timeout=0 合法，clause over-strict，FP killed
```

标注：`doc ambiguity shared across families`

### 视觉建议
- 两圈部分重叠（中间交集 = source 都能解的区域）
- 左圈填 GLM/DeepSeek **不同色对比块**（一蓝一橙，冲突感）
- 右圈填 GLM/DeepSeek **同色块**（都蓝，一致感但都错）
- 下方两个箭头：
  - `cross-model validation` → 指向左圈
  - `source-grounded falsification` → 指向两圈合并（覆盖 union）
- 右下脚注（小字）：*task-intrinsic 是 extraction-level across-families 稳定性，distinct from intra-judge across-runs 噪声（Haldar, Rating Roulette）*

---

## 图 #5：5-stage pipeline（P18-P20）

### 设计目标
用**一个真实 candidate 走完全程**，让审稿人看懂 source-grounded falsification 的 dataflow，而不是抽象方框。

### 具体图例（用 `shardsNum` 串起 5 阶段）

横向 5 个 stage，每个 stage 下方一个**数据卡**（输入 → 输出）。用同一 `shardsNum=0` candidate 贯穿：

**Stage 1 · Extract claims**
- 输入（doc）：`shardsNum (int, optional, default 1): Number of shards to create.`
- 输出（clause）：`shardsNum >= 1`

→ 箭头标注 `clause`

**Stage 2 · Attack generation**
- 输入：clause `shardsNum >= 1`
- 输出（boundary input）：`create_collection(shardsNum=0)`

→ 箭头标注 `probe`

**Stage 3 · LLM judge**
- 输入：probe `shardsNum=0` → API 返回 `200 success`
- 输出（LLM verdict）：**"违规 — should reject but accepted"**（ believing 自己的 over-strict clause）

→ 箭头标注 `candidate defect`

**Stage 4 · Dev-reviewer（source falsify）** ⭐ 高亮
- 输入：clause + implementation source
- source 显示：```go if shardsNum == 0 { shardsNum = defaultShard }```
- 输出：**FALSIFY** — "source shows 0 selects the default; the clause is over-strict; verdict was a false positive"
- 结果：**FP killed** ✗

→ 箭头标注 `confirmed or killed`

**Stage 5 · Novelty gate**
- 输入：surviving candidates
- 输出：deduplicated + filtered known issues → submitted

### 视觉建议
- 5 个圆角矩形横向排列，stage 4 用**绿色高亮 + 加粗边框**（核心）
- 每个 stage 下方挂一张数据卡（小字体，显示真实的输入/输出）
- 用一条**彩色数据流线**贯穿（shardsNum 的旅程），从 stage 1 流到 5
- stage 3 → stage 4 的箭头标红"LLM said defect"，stage 4 输出标绿"source says FP"
- 顶部小标题：*"One candidate's journey through the pipeline (Milvus shardsNum)"*
- 反差强调：stage 3 的 LLM verdict（红，"违规"）被 stage 4（绿，"falsified"）推翻 —— 这就是 source-grounded falsification 的价值

### 反向对比（可选小字，在 stage 4 下方）
- vs MASTOR：MASTOR 用 source 编码 implemented behavior（测实现做什么）；TestVDB 用 source 证伪 documented claim（测 doc-code gap）—— **方向相反**

---

## 图 #5 扩展 + 图 #9：claim → oracle 形态（新增，核心澄清）

> 由"是否有必要展示从 claim 到 oracle 的形态"讨论引出 —— 论文标题 "LLM-Derived Oracles" 最易被误读成 "LLM 直接当 oracle"，这两张图把 oracle 的形态钉死成 **claims 集合**。

### 图 #5 Stage 1 扩展（claim → oracle 聚合）
原 Stage 1 数据卡只显示单条 clause。现已扩展为：
- 数据卡 output：`claims → oracle: shardsNum>=1 + N more`
- stage 标题加 `→ oracle`
- 让审稿人看到 oracle 是 **claims 集合**（多条断言聚合），不是单条断言

### 图 #9：claim / oracle / judge 概念图（最核心的澄清）

**设计目标**：钉死三个易混概念 —— claim（单条断言）/ oracle（claims 集合 = 判断标准）/ judge（LLM 用 oracle 检查的动作）。让读者一眼看出 "LLM-derived oracle ≠ LLM judge"。

**具体图例**（横向 5 节点流程，真实 parameter）：

1. **doc**（左，白卡）：`shardsNum (int, optional, default 1): Number of shards.`
2. → **LLM extract**（蓝箭头）→
3. **claims**（中左，3 个蓝卡堆叠，每个展示完整结构 name + constraint + source）：
   - claim 1: `shardsNum >= 1`（from 'optional, default 1'）
   - claim 2: `metricType in {L2,IP,COS}`（from enum doc）
   - claim 3: `dimension >= 1`（from 'Must be >= 1'）
4. → **aggregate**（蓝箭头）→
5. **oracle**（中右，**大绿卡**，核心）：
   - `oracle = { claim 1, claim 2, claim 3, ... }`
   - "the judgment standard"
   - **"(NOT the LLM itself)"**（红字强调，直接堵误读）
6. → **judge (LLM)**（橙箭头）→
7. **probe response**（右，白卡）：`conform? violate?`

**底部脚注（关键）**：
- oracle 是 LLM-derived 的**产物**（claims 集合）；judge 是用 oracle 的**动作** —— 两者不同（oracle ≠ LLM）
- source-grounded falsification 针对**单个 claim**（如 claim 1），不是 oracle 整体

**视觉建议**：
- oracle 卡用最大尺寸 + 绿色（强调"这是核心概念"）
- "(NOT the LLM itself)" 红字 —— 一句话堵住 "LLM oracle" 误读
- claims 卡展示结构（name + constraint + source）—— 让 claim 形态具体，不只是符号
- 色阶过渡：蓝（claims / extract）→ 绿（oracle 产物）→ 橙（judge / response 动作）

**为什么这张图重要**：标题用 "LLM-Derived Oracles"，读者默认它是 "LLM oracle"。这张图把 oracle 的形态可视化为"claims 集合"，把 judge（LLM 动作）和 oracle（产物）分开 —— 一次看懂，不再误解。附带澄清 "source falsifies a claim" 的靶子是单个 claim。

---

## 作图风格统一建议

- **配色**：蓝（family-specific / structured / transcribe）+ 橙（task-intrinsic / ambiguous / interpret）+ 绿（source-grounded / 正解）+ 红（错误 / over-strict）
- **字体**：代码片段用等宽（Consolas/Mono），叙述用无衬线（Inter/Helvetica）
- **标签语言**：英文为主（PPT 标题已全英文），代码注释可中可英
- **数据卡**：每张图里的"具体例子"用浅灰背景的卡片框，让真实内容（doc/code）和概念标签视觉分离

---

## 3 张图的关系（可在 PPT 衔接时用）
- **#3** 回答 *why*（为什么 doc 不可靠 → 因为 source ambiguity）
- **#4** 回答 *what*（不可靠分两层 → family-specific + task-intrinsic）
- **#5** 回答 *how*（TestVDB 怎么解 → pipeline + source falsify）

三张图都用 `shardsNum` / `timeout` / `consistencyLevel` 这些**论文真实 parameter**，不是虚构例子 —— 这点对审稿可信度很重要。

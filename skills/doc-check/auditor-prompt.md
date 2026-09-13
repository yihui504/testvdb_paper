# Auditor Dispatch Template（doc-check 的 Step 2 用）

> 派一个 fresh auditor subagent 时用此模板。移植自 PaperPilot `doc-check/auditor-prompt.md`，
> checklist 5 维 18 子项保留原貌；仅 dispatch 语境 xept 化。

**用途**：读一份 prose 文档一次，跑固定 checklist，返回 evidence-bound 报告。

**派发时机**：Step 1 审计上下文写完之后。

```
Task/Agent 工具派 subagent（general-purpose）：
  description: "Audit one prose document"
  prompt: |
    你是文档审计者（document auditor）。`read` 文档一次，跑下方固定 checklist。
    若审计上下文列了 Related documents，`read` 每份一次以核实 Correctness。

    ## Inputs

    - **Document under review:** [DOC_PATH]
    - **Audit context:** [Type / Purpose / Intended audience / Related documents——Step 1 的四字段]
    - **Scope (optional):** [标题/锚点/行范围；"none" 或省略则审全文]

    ## Read-Only Audit

    审计只读——不编辑文档、不提交、不推送。呈现发现；apply 是人的 gate。

    ## Scope

    若给了 SCOPE，你仍读全文一次获取上下文（ORDERING / EXTERNAL-CONSISTENCY / 阅读
    流可能跨节），但只报 location 落在 SCOPE 内的 finding。每个维度仍适用——无 N/A，
    只是维度跑在 scoped 区域而非全文。

    ## What to Check（5 维 18 子项）

    ### 1. Structure & Organization

    - **READING-FLOW** — 全文阅读流是否成立？
    - **SECTION-COHERENCE** — 每节发展一个主题、内部逻辑连贯？
    - **PARAGRAPH-COHESION** — 每段聚焦一个概念、句间链接？
    - **ORDERING** — 每个前置概念在使用前介绍？

    ### 2. Clarity & Consistency

    - **CLARITY** — 有歧义到误导的程度？
    - **CONTRADICTIONS** — 任意两句话冲突？
    - **TERMINOLOGY** — 同一概念始终同一用词？
    - **AUDIENCE-FIT** — 全文一个 register 和知识层级？
    - **CONVENTIONS** — 列表标记/标题/标签/表格/代码块一致且完好？

    ### 3. Correctness

    - **ACCURACY** — 每个 claim/值/签名/行为描述真实？
    - **EXTERNAL-CONSISTENCY** — 与 related docs 或所描述代码的重叠处一致？
    - **REFERENCES** — 每个交叉引用/锚点/链接/文件名可解析？

    ### 4. Completeness

    - **COMPLETENESS** — 覆盖其 Purpose 所需的一切？
    - **UNFINISHED** — 有未完成标记残留？

    ### 5. Conciseness

    - **BELONGING** — 有从别处复制或超本文档 scope 的块？
    - **REDUNDANCY** — 同一点实质重复？
    - **NECESSITY** — 删掉某节/段，会坏什么吗？
    - **CONCISION** — 能不丢信息地收紧？

    ## Calibration

    **只报会真正误导/阻塞/浪费为该文档 Purpose 而来的读者的问题。** 矛盾、断引用、
    歧义到引读者走错——这些是 finding。"可以换个说法""某些节比别的短"个人风格偏好
    不是。

    ## Severity

    Severity 是 per-finding 影响，与 dimension 正交。按实际严重度分——非所有都是 HIGH。

    | Severity | Means |
    |---|---|
    | **HIGH** | 误导 / 致错 / 阻塞使用 |
    | **MEDIUM** | 妨碍使用 |
    | **LOW** | 润色 |

    ## Output Format

    ### Findings

    每条一 block，最高 severity 先：

    - **severity:** HIGH | MEDIUM | LOW
    - **dimension:** [18 子项之一]
    - **location:** [行号或锚点，引用精确行——如 `SKILL.md L42` / `README §Installation` / `design-doc.md D2`]
    - **issue:** [问题]
    - **why:** [为何重要——说不出 why 就丢掉这条 finding]

    ## Critical Rules

    **DO:**
    - 每条 finding 锚到 location
    - 说每条 finding 的 why
    - 按实际 severity 分类

    **DON'T:**
    - 报无 location 或无 why 的 finding
    - 对你没真读的文本给反馈
    - 编辑文档
    - 含糊（"可以更清楚"）
```

**auditor 返回**：Findings（HIGH/MEDIUM/LOW）。orchestrator 原样呈现，不筛选。
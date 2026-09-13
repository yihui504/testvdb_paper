---
name: write-cover-letter
description: 写投稿 cover letter（1 页）。先读论文提取贡献（非抄摘要）、点明 venue 契合、列核心贡献与关键结果。输出 cover-letter.tex 并编译验证。直接不谦卑、不超 1 页、无 em-dash。
---

# Write Cover Letter（写投稿信）

为学术论文投稿写简短（1 页）cover letter。

## 工作流
```
1. 读论文（写前必做）
2. 读 .self_xept/project.yml（venue 信息、编辑名）
3. 写 cover letter
4. 编译验证
```

## Step 1: 读论文
**不读论文绝不写 cover letter。** 从论文提取：
- 核心贡献（用你自己的话，**非**抄摘要）
- 关键结果及其意义
- 方法亮点

## Step 2: 写
`write` 到项目根 `cover-letter.tex`。

### 必须包含
- 日期与编辑/chair 名（从 `.self_xept/project.yml`，或问用户）
- 论文标题与作者列表
- 为何投此 venue——把论文主题与 venue 范围**具体**关联
- 核心贡献（2-3 个要点或短段）
- 简提关键结果
- 利益冲突声明（若 venue 要求）
- 推荐审稿人（若 venue 要求——问用户要名字）

### 行为规则

| 规则 | 原因 |
|------|------|
| **不抄摘要** | 审稿人会察觉；换角度重述 |
| **显式说明 venue 契合** | "This work aligns with [venue]'s focus on X because..." |
| **控制在 1 页** | 编辑略读，越长越糟 |
| **直接，不谦卑** | "We present" 非 "We humbly submit for your kind consideration" |
| **无 em-dash** | 用逗号或拆句 |
| **贡献简洁** | 每条 1-2 句，非整段 |

### 语言
- 从用户消息或 `.self_xept/project.yml` 检测
- 不清默认英文
- 用户用非英文沟通则问信用哪种语言

## Step 3: 编译
`pwsh` 跑 `latexmk` 验证信件恰 1 页。超了砍冗余——绝不缩字号。

## 常见错误（避免）
1. ❌ 不读论文就写——贡献会含糊或错
2. ❌ 照抄摘要——换框架重述
3. ❌ venue 契合泛泛——"your prestigious conference" 无意义；要具体
4. ❌ 超 1 页——砍，不缩字
5. ❌ venue 要求时漏利益冲突/推荐审稿人

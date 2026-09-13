---
name: setup-venue
description: 配置投稿会议/期刊——先查本地 venue 缓存（.self_xept/venues/），miss 则 web 直抓 CFP，提取要求（页数/截止/匿名/模板/引擎）写入 .self_xept/project.yml，含模板选择器（主流 LaTeX 模板家族+变体）。提供 URL/CFP 文档则抓取，口头描述则补全。
---

# Setup Venue（配置投稿会议）

为指定投稿目标配置工作区——提取要求、更新约束、设置正确模板与编译器。

> 注：原平台有内置中心 venue 数据库（search_venue_db）。DSH 版替代方案是**本地分布式缓存**：每篇论文项目自带 `.self_xept/venues/` 缓存，入库后团队共享（commit 即共享），无需维护中心库。

## 何时用
- 用户提供会议/期刊 **URL** 或 **CFP 文档**
- 用户**描述**投稿目标（"我要投 ICSE 2026"）
- 用户要求**换 venue** 或**更新投稿要求**
- 用户提供**非 CFP 文档**（课程作业要求、学位要求等）

## 工作流

### Step 0: 查本地 venue 缓存
先 `glob` `.self_xept/venues/*.yml`，找与用户所述匹配的缓存（文件名即 slug，如 `icse-2026.yml`）：
- **命中且未过期**（deadline 未过）→ 展示缓存记录，问用户：复用 / 重新抓取（停下等待）。复用则跳至 Step 3 确认写入 `project.yml`
- **命中但 deadline 已过** → 告知用户这是旧届，直接走 Step 1 重抓（新届信息大概率变了）
- **未命中** → 直接 Step 1
`.self_xept/venues/` 不存在则先建目录（首次正常）。

### Step 1: 提取要求
- **URL**：`web fetch` 读页面，跟链接找 CFP / submission / author guidelines 页
- **文档**：`read` 上传的文件
- **用户描述**：提取用户所述。关键信息缺失则问澄清（停下等待）。
- **多 track**：存在多 track 则问用户选哪个（停下等待）

### Step 2: 与用户确认
把提取数据整理后**向用户展示并停下等待确认**：
```
venue_name: ICSE 2026
full_name: International Conference on Software Engineering
type: conference
field: SE
deadline: 2025-10-08T23:59 (AoE)
page_limit: 10 pages + 2 references
anonymity: Double-blind
cfp_url: https://...
```

### Step 3: 保存
用户确认后 `write`/`edit` 写入 `.self_xept/project.yml`（所有确认字段）。这是所有 xept skill 的单一事实源。

### Step 4: 模板选择器 + 编译器
据 venue 家族给出模板候选表（**向用户展示并停下等待选择**；venue 已在 CFP 里指定官方模板则直接确认它）：

| 家族 | 模板 | 常见变体 | 典型 venue |
|---|---|---|---|
| ACM | acmart | sigconf / sigplan / sigchi | ICSE, FSE, CCS, SIGCOMM |
| IEEE | IEEEtran | conference / journal | S&P, ICRA, IEEE 期刊 |
| USENIX | usenix2019_v3 | — | USENIX Security, ATC, OSDI |
| NDSS | ndss | — | NDSS |
| Springer | llncs | — | 各 LNCS 系会议 |
| ACL | acl | long / short / findings | ACL, EMNLP, NAACL |
| Elsevier | elsarticle | — | Elsevier 期刊 |
| 自定义 | 用户提供模板包 | — | 中文期刊/学位论文 |

选定后：
- `write` 记录 `template: <家族>/<变体>` 到 `.self_xept/project.yml`（供 `xept:change-template` 消费）
- 模板与现有 .tex 不一致 → 问用户是否现在调 `xept:change-template`
- 中文内容或特殊字体 → 切 `engine: xelatex`（记录到 `project.yml`）
- `pwsh` 跑 `latexmk` 验证编译（DSH web 工作台有「▶ 编译」按钮可直接看日志）

### Step 5: 写 venue 缓存
确认后把 Step 2 的完整记录 `write` 到 `.self_xept/venues/<slug>.yml`（slug = venue 名小写连字符 + 年份，如 `icse-2026.yml`），字段 = Step 2 全部 + `cached_at: <今日日期>`。该文件**建议入库提交**——队友投同一 venue 时 Step 0 直接命中，省一次抓取。

## 规则
1. **别猜**——只记明确写明的。未知 → "TBD"
2. **确认**——提取后必须向用户展示并停下等待确认，再写入
3. **模板变更总先问**
4. **非 CFP？**——文档是课程作业/学位要求等，告诉用户并问是否仍要设为项目目标

## 替代原平台的部分（vs xept online）
- 中心 venue 数据库 → **本地分布式缓存**（`.self_xept/venues/`，git 共享）：每个团队自己沉淀，首次抓、后续秒开，无中心维护成本；代价是不保证跨团队共享（各自库），时效性靠 deadline 过期检查
- 无 deadline 倒计时服务：截止存为 `.self_xept/project.yml` 的 `deadline` 字段（文本）
- 推荐：把权威 CFP URL 一并存进 `cfp_url` 字段，便于复核
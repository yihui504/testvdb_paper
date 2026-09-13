---
name: literature
description: "文献检索统一入口——四操作（Search/Fetch/Cite/Verify）映射 xept 双基建：BibTeX 元数据走 scripts/fetch_bib.py（路线 A，add-citation/check-references/ideation 用）/ 全文 cache 走 scripts/search_literature.py + fetch_literature.py（路线 C，dual-review expertise 用）。Iron Law: 每字段来自本会话检索的 metadata，绝不凭记忆。用户要\"查文献\"/\"下论文全文\"/\"生成 BibTeX\"/\"直接检索不经上层 skill\"时调用。写论文加引用用 xept:add-citation；审稿读竞品用 xept:dual-review；检查参考文献用 xept:check-references；写前评估想法用 xept:ideation。"
---

# Literature（文献检索 · 双基建路由）

> xept 的文献检索分两套基建，职责正交，**不合并不重复**（[docs/literature-design.md](../../docs/literature-design.md) 记设计依据）。本 skill 是统一入口 + 路由：四操作（Search/Fetch/Cite/Verify）→ 用哪套基建 / 哪个上层 skill。

## 核心原则

**Iron Law: NO OUTPUT WITHOUT A RETRIEVED SOURCE.**

```
NO OUTPUT WITHOUT A RETRIEVED SOURCE.
每个字段（作者/标题/会议/年份/DOI）须追溯到本会话检索的 metadata——绝不凭记忆：
缺字段就省略 + 报告 gap，捏造比没有更糟。违反字面 = 违反精神。
```

## 双基建（不合并不重复）

| 基建 | 脚本 | 输出 | 服务的上层 skill |
|---|---|---|---|
| **BibTeX 元数据** | [fetch_bib.py](../../scripts/fetch_bib.py) | BibTeX entry + NamedTuple Record（四源去重 DBLP>CrossRef>SemSch>arXiv，union-find 聚类） | [xept:add-citation](../add-citation/SKILL.md) / [xept:check-references](../check-references/SKILL.md) / [xept:ideation](../ideation/SKILL.md) |
| **全文 cache** | [search_literature.py](../../scripts/search_literature.py) + [fetch_literature.py](../../scripts/fetch_literature.py) | JSON metadata（含 availablePdfs/urls）+ `.pdf`/`.txt`/`.summary.md` cache 落 `.self_xept/literature/` | [xept:dual-review](../dual-review/SKILL.md) expertise R1/R2 |

**为何两套不合**：schema 不同（fetch_bib 输出 BibTeX dict；search/fetch_literature 输出 JSON metadata + cache 文件）+ 职责不同（生成引用 vs 读全文核实）。详见 [docs/literature-design.md](../../docs/literature-design.md)。

## 四操作

### Search — query → metadata

- **要 BibTeX 格式**：`python scripts/fetch_bib.py "<query>"`（四源去重，输出 BibTeX）
- **要 JSON metadata（为 Fetch 准备 cache）**：`python scripts/search_literature.py "<query>"`（四源去重，输出 JSON 含 availablePdfs/urls）

### Fetch — metadata → PDF + text

`python scripts/fetch_literature.py --json-file <metadata.json>`（reuse 已 cache 的 `.txt`，否则遍历 availablePdfs 下载，cache 落 `.self_xept/literature/`；FAIL 则 fallback abstract + 标 provisional）。

### Cite — metadata → BibTeX entry

fetch_bib 输出 BibTeX entry。要写入 `.bib` + `\cite{}` 走 [xept:add-citation](../add-citation/SKILL.md)（更高层，含位置选择 + 写入 + 校验）。

### Verify — existing BibTeX → verdict

[xept:check-references](../check-references/SKILL.md)（核实已有引用的格式 + 内容对真实 paper）。

## 场景路由（不确定时查这）

| 你要 | 用 |
|---|---|
| 写论文时补一条引用到指定位置 | [xept:add-citation](../add-citation/SKILL.md)（内部 fetch_bib） |
| 写前评估想法，对比 ≥5 篇相关工作（只用元数据/摘要） | [xept:ideation](../ideation/SKILL.md)（内部 fetch_bib，**禁全文**——§6 红线） |
| 审稿要读竞品全文核实 novelty delta | [xept:dual-review](../dual-review/SKILL.md)（内部 search+fetch_literature cache，仅 expertise R1/R2） |
| 检查 references.bib 格式/内容 | [xept:check-references](../check-references/SKILL.md) |
| 直接检索 / 下载 / 生成 BibTeX（不经上层 skill） | **本 skill（literature）** |

## 何时用 / 何时不用

**用**：
- 直接做四操作之一（不经过 add-citation/ideation/dual-review/check-references）
- 不确定该用哪套基建——本 skill 路由表指引

**不用**：
- 写论文加引用 → [xept:add-citation](../add-citation/SKILL.md)（更高层）
- 审稿读竞品 → [xept:dual-review](../dual-review/SKILL.md)（含 cache + persona + checker）
- 写前评估想法 → [xept:ideation](../ideation/SKILL.md)（含 SWOT + 5 维评分）

## Windows 脚本调用（DSH/pwsh）

`pwsh` 跑 `python scripts/<name>.py …`；引号规则：外层单引号、内嵌参数用双引号（如 `python scripts/fetch_bib.py --query '"transformer scaling"'`）。python 命中 Store stub 时先解析真 python（`Get-Command python` 指向 WindowsApps 即换 `py -3`）。S2 API key 缺时 Semantic Scholar + arXiv 可能 429 限流（共享池）；dblp + CrossRef 可用——详见 [xept:dual-review](../dual-review/SKILL.md) cache 说明。

## Red Flags — STOP

- "我知道这篇 paper——凭记忆写 BibTeX" — STOP. Iron Law：检索 metadata 再写。
- "web_search 标题，无 metadata——写个大概" — STOP. 缺 metadata 就报告 gap，不捏造。
- "标题看着对——标 OK" — STOP. Verify 要检索真 metadata 比对。
- "用 search_literature 给 add-citation 生成 BibTeX" — STOP. BibTeX 走 fetch_bib（schema 对）；search_literature 输出 JSON metadata 给 cache。

## 配套

- 双基建脚本：[fetch_bib.py](../../scripts/fetch_bib.py) / [search_literature.py](../../scripts/search_literature.py) / [fetch_literature.py](../../scripts/fetch_literature.py)
- 设计 rationale：[docs/literature-design.md](../../docs/literature-design.md)

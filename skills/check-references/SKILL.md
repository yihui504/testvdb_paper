---
name: check-references
description: 核实论文每条引用真实存在（arXiv/DOI/标题可查）且格式正确。直接优先（抓 arXiv abs/DOI 页比对标题作者），搜索兜底。跨会话用 .self_xept/references.md 记核实状态。投稿前或加新引用后用。
---

# Check References（检查参考文献）

核实论文每条引用真实（有可查 URL）且格式正确。用 `.self_xept/references.md` 跨会话追踪核实状态。

## 何时用
- 用户说"核实我的参考文献"、"检查引用"
- 投稿前（也可独立于 `xept:check-submission` 调用）
- 写作中加了新引用后

## references 记忆
存于 `.self_xept/references.md`（## Citations）—— 每条引用的核实状态。

```
# References

## Verified
- key: smith2023deep
  title: "Deep Learning for Code Analysis"
  authors: Smith et al.
  url: https://doi.org/10.1145/xxxxx

## Unverified
- key: zhang2021fake
  title: "Some Generated Title"
  authors: Zhang et al.
  url:
```

**规则：**
- .bib 里每条引用都应在记录里有条目
- 记录的是**上次**核实结果；它是报告的缓存，**非**闸门。完整引用检查总是对整个 .bib 重跑（一条先前 "ok" 的条目若被改过可能变错，且仅查存在的 "verified" 从未证明 arXiv id 正确）。
- 若核实返回 mismatch/not_found → 标红（错 id / 错作者 / 编造）。

## 工作流
```
1. 扫所有 .tex 里的 \cite{} 与所有 .bib 条目
2. .tex 与 .bib 交叉核对：
   - \cite{key} 在 .tex 但 key 不在 .bib → FAIL（渲染成 [?]）
   - key 在 .bib 但从未被 \cite → WARNING（未用条目）
3. 用确定性方式核实字段一致性（勿肉眼瞄网页）：
   对每条带 id/标题的条目，用 `pwsh` 直抓或 scripts/fetch_bib.py 取回比对：
   - 有 arXiv id：`pwsh` 抓 https://arxiv.org/abs/{id} → 比对 title+authors+year
   - 有 DOI：`pwsh` 抓 https://doi.org/{doi} → 比对 title
   - 仅有标题：scripts/fetch_bib.py --query "<title>" 或 web_search 兜底
   按结果给每条状态：
       ok        → 字段全匹配真实论文
       mismatch  → 真论文但某字段错（错 arXiv id/作者/年）→ 向用户报告确切问题
       not_found → 按标题也查无 → 疑似编造，标红
       no_id     → 无 arXiv/DOI 且标题不可查 → 请用户加 id
       unknown   → 查询失败（网络）→ 下次重试，非已核实
   重要：总是对整个 .bib 核实。勿因记录标 "verified" 就跳过——错 arXiv id 正是
        仅查存在所漏过的。记录是结果缓存，非跳过一致性检查的理由。
4. 检查引用格式（见下）
5. `write` 结果到 .self_xept/references.md（## Citations，整体替换）
6. 向用户报告——列每个 mismatch/not_found 及其具体问题
```

## 核实搜索
不同 BibTeX 类型用不同核实法：
- `@article`/`@inproceedings`/`@conference`：按标题+第一作者（优先 arXiv/DOI 直查）
- `@book`：Google Books、ISBN 查、或出版社站
- `@misc`/`@online` 带 URL：直接访问 URL
- `@techreport`：搜标题+机构
- `@software`：查 GitHub/主页 URL

论文类——**直接核实优先，搜索兜底**：
1. 有 arXiv ID（.bib 或 URL/eprint 字段提取）：**直抓 `https://arxiv.org/abs/{id}`** — 确认标题作者匹配
2. 有 DOI：**直抓 `https://doi.org/{doi}`** — 确认页面加载、标题匹配
3. 两者皆无：`scripts/fetch_bib.py --query "<title>"` 或 web_search 按标题+第一作者兜底

**核实标准**：标题作者匹配、页面加载有摘要即可。无需全文——付费墙显示标题/作者/摘要也算已核实。

**可疑迹象（疑似编造）：**
- 精确标题搜索无结果
- 作者不匹配该领域任何真实研究者
- venue/期刊不存在
- 年份不一致（论文称 2023 但 venue 当时不存）

## 引用格式
`read` `.self_xept/project.yml` 取 venue 规则，然后查：

**风格一致：**
- 所有引用同格式（数字 [1] vs 作者-年 (Smith, 2023)）
- 括号样式全程一致
- 引用命令一致（`\cite` vs `\citep` vs `\citet` — 匹配 venue）

**位置规则：**
- 引用在句号前非后："...shown effective~\cite{x}." 非 "...shown effective.~\cite{x}"
- 引用前非断行空格：`~\cite{}` 非 `\cite{}`
- 引用不作句子主语：非 "~\cite{x} showed..." → 用 "\citet{x} showed..." 或 "Smith et al.~\cite{x} showed..."

**BibTeX 质量：**
- 必需字段齐全（title、author、year、venue/journal）
- 无重复条目（同论文不同 key）
- 字段格式一致（venue 名不混缩写："ICSE" vs "International Conference on Software Engineering"）
- 年份合理（非未来、非对近期论文而言过古老）

## 输出
```
Reference Check Complete.

Verified: 25/30 citations
- 20 previously verified (in memory)
- 5 newly verified this session

Suspicious: 3 citations
- \cite{zhang2021fake}: "Some Generated Title" — Google Scholar 无结果
- \cite{li2022method}: "A Method for X" — 作者不匹配任何已知研究者
- \cite{wang2023}: 标题找到但年份错（实际 2022）
→ 请人工核实或删除。

Unverified: 2 citations（搜索配额达上限，下次重试）

Formatting: 4 issues
- 3× 引用在句号后非前
- 1× \cite 前缺非断行空格

5 newly verified this session.
```

## 工具
```
read                     # 读 .bib 和 .tex
pwsh (Invoke-WebRequest) # PRIMARY：直抓 arXiv abs / DOI 页比对标题作者
scripts/fetch_bib.py     # 无 id 时按标题查（Semantic Scholar/Crossref）
web_search                # 兜底（书/非论文源）
（问用户并等待）          # 报告可疑/错配引用供人工核
write                    # 结果写 .self_xept/references.md（## Citations，整体替换）
```

注：直接抓取（`pwsh` 抓 arXiv/DOI）是代码级比对，能抓到"真标题 + 错 arXiv id / 错作者"这种肉眼瞄网页漏过的情况。对带 id 或标题的 @article/@inproceedings 优先用它。

## 相关技能
- `xept:check-submission`：投稿前全面检查（引用是其一类）
- `xept:add-citation`：添加/补全引用
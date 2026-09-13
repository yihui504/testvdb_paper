---
name: add-citation
description: 为无支撑的主张补充真实引用。三档范围：指定位置 / 整节 / 全文。先复用已核实引用，新引用经 arXiv/DOI 直查或 scripts/fetch_bib.py 核实后写入 .bib 与 \cite{}。与 xept:check-references 配合（后者核实已有引用）。
---

# Add Citation（添加引用）

为无支撑的主张找真实引用。三档范围：指定位置、整节、全文。

## 工作流
```
1. 确定范围（不清则问用户并等待）：指定位置 / 整节 / 全文
2. 扫目标范围找需引用支撑的主张
3. 对每处：
   a. 先查 .self_xept/references.md 已核实引用能否复用 → 复用。**references.md 缺失则跳过复用直接 step 3b 检索**（首次使用无基线，正常）；step 3f 会建/追加 references.md（首次 `write` 建，后续 `edit` 追加）
   b. 否则搜论文：scripts/fetch_bib.py --query "..." 或 web_search
   c. 核实：确认论文存在（标题+作者+摘要可见）—— 有 arXiv id 则用 `pwsh` 的 Invoke-WebRequest 抓 https://arxiv.org/abs/{id}，有 DOI 则抓 https://doi.org/{doi}
   d. 确认相关：摘要必须真正支撑该主张
   e. 加进 .bib 并用 `edit` 插入 \cite{}
   f. 把已核实条目追加到 .self_xept/references.md（## Citations）
4. 报告新增了什么
```

## 强制规则
1. **先复用**——搜前先查 `.self_xept/references.md`。已在别处引过的论文可能支撑当前主张，避免 .bib 膨胀。
2. **BibTeX 来自工具，绝不来自记忆**——从 `scripts/fetch_bib.py` 或 `pwsh` 直抓 arXiv/DOI 页取条目，原样粘贴其 BibTeX。**绝不手写或"回忆" arXiv id、DOI、作者列表**——错 arXiv 号/错作者就是这么混进来的。工具没返回 arXiv id 就不加 `eprint`，**不要编**。
3. **加前核实**——每条新引用必须经 arXiv/DOI 直查（`pwsh` 直抓）确认字段一致。返回不匹配/查无则修或弃，绝不加未核实引用。直查比瞄网页强（代码级字段比对）。
4. **读摘要，非只标题**——标题相关不够，摘要须确认论文真支撑该主张。
5. **引用格式**——`~\cite{key}`（非断行空格），在句号前非后。同位置多个：`~\cite{a,b,c}`。匹配 `.self_xept/project.yml` 的 venue 风格。
6. **完整 BibTeX**——title、author、year、venue/journal 必需；arXiv id/DOI 仅当工具返回时才加。

## 工具
```
read                       # 读 .tex 和 .bib
scripts/fetch_bib.py       # 搜论文（Semantic Scholar/Crossref），返回 BibTeX
pwsh (Invoke-WebRequest)  # 核实：直抓 arXiv abs / DOI 页比对标题作者
web_search                  # 兜底（非论文源）
edit                       # 插入 \cite{} 和工具产出的 .bib 条目（原样）
（问用户并等待）            # 澄清范围或含糊引用
write / edit               # 追加已核实引用到 .self_xept/references.md（## Citations）
```

## 相关技能
- `xept:check-references`：核实已有引用（与本技能互补）
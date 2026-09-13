---
name: change-template
description: 更换论文的 LaTeX 模板（ACM/IEEE/USENIX/NDSS/Springer 等）并保留全部内容。纯格式操作，与投稿目标解耦——设置/更换投稿会议用 xept:setup-venue，不用本技能。
---

# Change Template（更换 LaTeX 模板）

更换论文 LaTeX 模板，保留所有内容。

## 工作流
1. **定位主文件**：在项目根找 `.tex` 文件与当前编译目标（见 `.self_xept/project.yml`）。若多个 `.tex` 或主文件不清，**问用户并等待**确认哪个是主文件。
2. **确定目标模板**——**不**主动询问投稿 venue：
   - 先 `read` `.self_xept/project.yml`。若已记录目标 venue / 所需模板，**那就是预期模板，直接用，别问**。
   - 否则若用户在请求里点名了模板（如"换成 IEEE"），照办。
   - 两者都没有才**问用户**要换哪个**模板/格式**（IEEE / ACM / USENIX）。**不**问投哪个会议/期刊——换模板是格式操作，与投稿目标解耦。（设/改投稿目标是 `xept:setup-venue` 的职责。）
3. **分析源**：`read` 主 `.tex`，识别 documentclass 与所需包/文件。记录项目根现有模板文件（.cls、.sty、.bst）。
4. **确定模板变体**：若模板包有多种变体（acmart `sigconf` vs `sigplan`，IEEEtran `conference` vs `journal`），venue 已知时选匹配的；否则**问用户**澄清哪个**变体**（非 venue）。
5. **获取模板文件**：
   - 标准模板（ACM、IEEE）：由用户提供模板包，或用 `web fetch`/`pwsh` 下载官方模板，解压
   - 非标准（USENIX、NDSS、Springer 等）：`web fetch` 下载并解压模板包
   - 所有模板文件（.cls、.sty、.bst）放到项目根
6. **核对文件**：检查主 tex 是否缺必需文件（logo、特殊配置）。缺则从模板补。
7. **更新主 tex**：替换 documentclass、preamble、模板专属命令。
8. **编译**：`pwsh` 跑 `latexmk`（引擎见 `.self_xept/project.yml`）验证。
9. **处理旧模板文件**：编译成功后，**问用户**旧模板文件归档到 `_previous_template/`、删除还是原地保留，然后执行。

## 换什么

| 元素 | 转换示例 |
|------|----------|
| Document class | `\documentclass[sigconf]{acmart}` → `\documentclass[conference]{IEEEtran}` |
| Keywords | `\keywords{...}` → `\begin{IEEEkeywords}...\end{IEEEkeywords}` |
| 作者格式 | ACM `\author{}\affiliation{}` → IEEE `\IEEEauthorblockN{}` |
| 参考文献 | `\bibliographystyle{ACM-Reference-Format}` → `\bibliographystyle{IEEEtran}` |
| 移除 | `\begin{CCSXML}`、`\ccsdesc{}`、`\acmConference{}` |

## 保留什么
- 所有章节内容（Introduction、Methodology 等）
- 公式、图、表
- 引用（`\cite{}`）、标签（`\label{}`）、交叉引用（`\ref{}`）
- `.bib` 里的参考文献条目
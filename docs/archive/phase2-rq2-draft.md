# Phase 2 → 论文新 RQ2 草稿（2026-08-13）

数据源：`.paperpilot/phase2/metrics.json` + `glm_verdicts.json`（124 candidate 历史版本 probe + GLM5.2 盲评）。
定位依据：`docs/experiment-redesign.md` 的 RQ 重构表 —— RQ1 mining yield / **RQ2 detection capability（新）** / RQ3 FP suppression（原 RQ2）/ RQ4 VDBFuzz（原 RQ3）。

---

## A. 重编号计划（机械改动，待 RQ2 文稿确认后执行）

| 现状 | 重编号后 | label 改动 |
|---|---|---|
| `\subsection{RQ2: False-Positive Suppression}` (L236) | RQ3 | `\label{subsec:rq2}` → `\label{subsec:rq3}` |
| `\subsection{RQ3: Comparison with VDBFuzz}` (L344) | RQ4 | `\label{subsec:rq3}` → `\label{subsec:rq4}` |
| 新 RQ2（插入 L234 之后，tab:yield 表后、原 RQ2 之前） | RQ2 | 新建 `\label{subsec:rq2}` |

**`\ref` / 文本同步**（grep 已定位）：
- L208 methodology 的 RQ 列表（`\item[RQ2...]`/`[RQ3...]`）→ 改编号 + 新增 RQ2 项
- L208"For the false-positive retrospective (RQ2) we use a controlled set of 48..." → "(RQ3)"
- L129 intro "root causes in Section~\ref{subsec:rq2}"（指 FP）→ `\ref{subsec:rq3}`
- L217 RQ1 末尾 "mirrors the pattern in Section~\ref{subsec:rq2}"（指 over-formalization/FP）→ `\ref{subsec:rq3}`
- L217"detection capability is quantified separately on a controlled set in RQ2"（原本 mismatch，新 RQ2 正好是 detection）→ 保持 RQ2，正确
- L327（原 RQ2 内）"Multi-perspective judging (Section~\ref{subsec:rq2})"（自指 FP）→ `\ref{subsec:rq3}`
- L416 appendix `\ref{subsec:rq2}`（指 FP 的 hallucination）→ `\ref{subsec:rq3}`

---

## B. 新 RQ2 LaTeX 文稿

插入位置：**L234 之后**（`tab:yield` 表 `\end{table}` 之后），原 RQ2 之前。

```latex
\subsection{RQ2: Detection Capability}
\label{subsec:rq2}

RQ1's yield precision bounds detection capability only indirectly: it treats all 53 unadjudicated submissions as false positives to obtain a worst-case bound (35.7\%). We now measure detection capability directly on a controlled set with known ground truth, by re-probing each candidate's reported behavior on the DB version where it was originally reported and adjudicating the evidence with the current confirmation pipeline.

\paragraph{Controlled set and pipeline.}
The controlled set is the 124 submitted candidates that carry a reportable DB version (126 submissions minus 2 self-authored fix PRs). Ground truth comes from the Phase 1 maintainer adjudication re-verified in August 2026 (Section~\ref{subsec:rq1}), partitioned into four groups: \emph{A}, 28 fixed by merged PRs; \emph{B}, 17 acknowledged but unfixed (8 open-accepted, 6 maintainer-closed without a merged fix, 3 closed as duplicates of acknowledged issues); \emph{C}, 26 maintainer-adjudicated false positives (16 by-design, 8 comment-refuted, 2 unreproducible); and \emph{D}, 53 unadjudicated. The 71 candidates in $A \cup B \cup C$ carry known ground truth and form the scored set; D is reported separately as a triage signal and is not scored. For each candidate we run four stages: (i) an issue-specific probe reproduces the reported behavior on the reported DB version pinned via Docker; (ii) a mechanical L1 gate flags execution failures and self-contradicting observations; (iii) GLM-5.2 adjudicates the surviving evidence in a single blind pass; and (iv) the verdict is aligned to ground truth. The probes are issue-specific reproduction scripts authored from each report, not tests the tool generates---this isolates the confirmation/oracle stage (does the judge correctly read reproduction evidence, free of extraction noise?) from the extraction stage evaluated in RQ1. To enforce blindness, probe specifications are sanitized of all ground-truth signals (FP\_BY\_DESIGN and by-design labels, maintainer attribution, duplicate relations) before the judge sees them, so the judge has only the contract claim, the expected behavior, and the observed behavior.

\paragraph{Headline capability.}
TestVDB confirms 42 of the 45 true defects (recall \textbf{93.3\%}, Wilson 95\% CI $[82.1\%, 97.7\%]$), at precision \textbf{79.2\%} $[66.5\%, 88.0\%]$ on the scored set, and suppresses 15 of the 26 maintainer-adjudicated false positives (FP-suppression \textbf{57.7\%} $[38.9\%, 74.5\%]$). Table~\ref{tab:detection} gives the confusion matrix. The capability is vendor-asymmetric: per-vendor recall is Milvus 28/29 (96.6\%), Qdrant 6/8 (75.0\%), and Weaviate 8/8 (100\%); FP-suppression is Qdrant 9/10 and Weaviate 2/2 but Milvus only 4/14. The Milvus FP-suppression gap is structural rather than incidental and we analyze it below.

\begin{table}[t]
\caption{Detection capability on the controlled set. Each candidate is re-probed on its reported DB version and adjudicated blind by GLM-5.2. A and B are true defects (recall denominator 45); C is maintainer-adjudicated false positive (FP-suppression denominator 26); D is unadjudicated and reported as a triage signal, not scored.}
\label{tab:detection}
\small
\begin{tabular}{@{}lrrrl@{}}
\toprule
GT group & $n$ & CONFIRMED & FALSE\_POS & role \\
\midrule
A: TP fixed (merged PR) & 28 & 26 & 2 & recall \\
B: TP ack-unfixed & 17 & 16 & 1 & recall \\
C: FP (by-design/refuted/unrepro) & 26 & 11 & 15 & FP-suppr \\
\midrule
scored ($A{\cup}B{\cup}C$) & 71 & 53 & 18 & --- \\
D: unadjudicated & 53 & 34 & 19 & triage \\
\bottomrule
\end{tabular}
\end{table}

\paragraph{Two-layer decomposition: probing vs judging.}
The three recall misses are all probe-trigger failures, not judgment errors: \#47635 is a load-to-search race the reporter flags as low-success-rate on standalone (it needs the distributed deployment for a reliable window); \#9045 is a server panic whose trigger, per the report and the cross-referenced \#7967, lies in the distributed/sharded search path rather than the standalone upsert we probe; and \#9149 is a ground-truth annotation issue---the shard-number validation it reports as missing is in fact present on v1.17.1, v1.18.0, and v1.18.1, so the report likely reflects an older build than its stated version. Conversely, every candidate for which the probe produced positive evidence was confirmed: the judge layer (L1 plus GLM) scores 42/42 on probed-true candidates. The 93.3\% recall is therefore a lower bound on the confirmation stage's reading of reproduction evidence, and its entire loss is attributable to the probe's behavioral coverage (concurrency, distributed-only, and version-annotation edge cases), not to the LLM judge. This is the central design takeaway: when a documentation-implementation defect can be reproduced as a standalone behavioral probe, TestVDB's confirmation logic detects it essentially without error; the open engineering problem is probe coverage of non-deterministic and distributed behaviors.

\paragraph{The Milvus FP-suppression gap is contract ambiguity, not noise.}
The 11 C-group candidates we wrongly confirm are not random errors. They concentrate on Milvus parameters whose documentation states a bound the implementation silently relaxes---a documented minimum \texttt{shardsNum} of 1 ignored for 0/$-$1/65535 (\#50351), documented enum domains unenforced for empty/None (\#50352), duplicate collection creation returning success instead of the documented already-exists error (\#50321), and search returning deleted IDs after deletion (\#50194). Each is a genuine documentation-implementation inconsistency that maintainers closed as by-design; the judge, asked to rule on contract conformance without the maintainer's design intent, reads the inconsistency as a defect. This is the symmetric counterpart of the over-formalization failure mode analyzed in Section~\ref{subsec:rq3}: there, ambiguous defaults invite the extractor to over-state the contract; here, the same ambiguity lets the implementation under-enforce a stated contract. The Qdrant and Weaviate C-groups, whose documentation draws sharper error boundaries, are suppressed at 90\% and 100\% respectively, supporting that the residual false positives track documentation style rather than judge incompetence.

\paragraph{Triage signal on unadjudicated submissions.}
Of the 53 submissions maintainers never adjudicated, the pipeline flags 34 as confirmed defects and 19 as false positives. These verdicts are not scored (no ground truth), but they quantify TestVDB's triage contribution: 34 candidates that would otherwise sit silent receive an evidence-grounded defect signal a maintainer can act on, and Section~\ref{subsec:rq3}'s dev-reviewer provides the source-grounded second pass that converts triage signal into a mergeable claim.
```

---

## C. 待用户决策的点

1. **per-vendor 表 vs 文字**：当前 per-vendor 数字（recall/FP-supp 三 vendor）放文字里。若 reviewer 要详表，可加一个 `tab:detection_vendor`（3 行 × recall/precision/FP-supp）。我倾向文字（表已够多）。

2. **9149 GT 存疑的措辞**：现写"the report likely reflects an older build than its stated version"。备选：更直接说"we could not reproduce on any available tag; GT may be mis-labeled"。前者更克制，后者更诚实。倾向前者。

3. **"probe 是人工脚本"的篇幅**：setup paragraph 里已声明"isolates the confirmation stage ... not tests the tool generates"。这是必要诚实点，但削弱了"端到端 detection"的 claim。是否要加一句"the tool's own test-script generation (Section~\ref{subsec:testgen}) produces these probes end-to-end on a subset, confirming the stage composes"——如果有数据支持就加，否则不加（避免空头声明）。

4. **D 组 34 triage 信号**：最后一段把 D 组作为 triage 贡献。这是正向 framing。但 34/53 = 64% 的 unadjudicated 被判 CONFIRMED，可能偏高（D 组无 GT，无法验）。措辞已说"not scored"，但要不要加"pending external validation"。

5. **和 RQ3（dev-reviewer）的 recall 差**（93.3% vs 74%）：现 draft 不强调对比。若要提，可加一句"the higher recall than the dev-reviewer's 74\% reflects stronger evidence (historical-version reproduction) rather than a weaker task"——堵 reviewer 的疑问。倾向加（一句）。

---

## D. 编译验证清单（执行重编号后）

- [ ] `pdflatex TestVDB.tex` 两遍，无 undefined reference / multiply-defined label
- [ ] `\ref{subsec:rq2/rq3/rq4}` 全部解析到正确 section（RQ2=detection, RQ3=FP, RQ4=VDBFuzz）
- [ ] `tab:detection` 正常渲染
- [ ] L129/L208/L217/L327/L416 的引用语义正确（FP 指向 RQ3，detection 指向 RQ2）

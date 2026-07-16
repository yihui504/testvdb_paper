# Paper Restructure Todo（v2 重构，收尾状态 2026-07-16）

> v2 重构稿：[paper/paper-draft-acm-sigconf.tex](paper/paper-draft-acm-sigconf.tex)（ACM sigconf，5 页）。
> 定位：LLM-as-oracle setting + task-intrinsic + source-grounded falsification。
> 状态：**完整、跨节一致、全引用、mock-review Accept 区**。venue 未定（导师未拍板，软目标 ISSTA 2027-01）。
> 旧稿 v1（VLDB propagation-centric）存档于 git tag `archive/v1-vldb-pre-rewrite`。

## ✅ 已完成（重构闭环）

**地基（novelty-reassessment.md §8/§9）**：四篇论文 grilling（Barr/Slutz/Chen/QuickCheck）→ 贡献地图 → 两轮反驳修正（传播非强制 / classical 覆盖子集）→ 术语审计（compliance→conformance, LLM-as-checker→LLM-as-oracle, propagation→self-preference 线）→ MASTOR 全文（两 hinge 化解）。

**实验**：
- E1：111 bug fault-model 分类（85% conformance 残差 / 89% on 38 acknowledged）。[data/e1-bug-classification.md](data/e1-bug-classification.md)
- E2：cross-model judging vs source（9 Milvus over-strict 条款；cross-model 漏 0/2 task-intrinsic、source 全抓 9/9）。[TestVDB/scripts/e2_judgment.py](TestVDB/scripts/e2_judgment.py)
- E2 跨厂商：Qdrant v1.18.2 活体探针——over-strict 集中在 Milvus（Qdrant 文档明确 minimum、基本执行）；其 doc-code 缺口是 conformance bug（timeout=0 已提交 Qdrant，pending）。[TestVDB/scripts/e2_qdrant_probe.py](TestVDB/scripts/e2_qdrant_probe.py)
- classical-oracle 基线：Qdrant v1.18.2 metamorphic MR 套件（0 数学违规 + 0 合规，结构确认）。[TestVDB/scripts/baseline_metamorphic_qdrant.py](TestVDB/scripts/baseline_metamorphic_qdrant.py)
- retrospective（v1）：source anchor 31%→81% FP 抑制，96.7% TP 留存。

**写作**：abstract + §1–§9 全正文；Table 1（exclusion）+ Table 2（yield）+ Table 3（E2）；bibliography（含 AGORA+/SATORI/MASTOR/Panickssery，全核验）。

**质量**：多轮 rigor（口径/归因/例子/过度宣称）+ 跨节一致性 + mock-review（3 审稿，Weak Accept→Accept 区）+ Must/Should/Optional 全清 + narrative 收紧（intro/§3 去重）。见 [mock-review.md](mock-review.md)。

## 🟡 剩余（venue 无关，可选）
- [ ] **decision-tree 图**（LLM-as-oracle setting 可视化，深化概念贡献）——需画图（TikZ/工具）。
- [ ] THEORETICAL_FRAMEWORK.md 补 self-preference/task-intrinsic 形式化（可选，代码库文档层面）。
- [ ] Qdrant timeout=0 issue 等回复 → 回来更新 yield（38→39?）+ §6。

## 🔴 camera-ready（venue 定了再做）
- [ ] **全空间残差估计**：capture-recapture 或无偏缺陷采样——把"85%（TestVDB findings 组成）"升级为"真实缺陷分布的残差估计"。重。
- [ ] **E2 扩 N**（受 ground-truth 瓶颈限制，over-strict 集中 Milvus）——诚实，能扩则扩到 ~15-20，不能则保持 prevalence 刻画。
- [ ] 页数合规、匿名、正式 mock-review。

## ⏸ 阻塞（待 venue）
- 导师拍板 venue → setup-venue → write-paper 正式流水线。软目标 ISSTA 2027-01。

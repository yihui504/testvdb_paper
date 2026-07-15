# Paper Restructure Todo（post-grilling，2026-07-15 建档）

> 来源：novelty-reassessment.md §8（两轮反驳 + 术语审计 + MASTOR 全文 + 传播检索后的修订）。
> venue 未定（导师未拍板，软目标 ISSTA 2027-01）；以下为 venue 无关的地基工作。
> 顺序：Task 2 ✅ → E1/E2（现在做，定生死）→ 写作准备。

## ✅ 已完成
- **Task 2-A：MASTOR 全文深读**（arXiv 2606.10465）→ 两 hinge 解决：checker 确定性（不进 LLM-as-checker 区）；参考系=代码（§7.4.2 排除 doc-vs-code）。forcing 上移到 LLM-as-checker 区，更干净。
- **Task 2-B：传播检索** → 同族自我确认 = **self-preference bias**（Panickssery 2024, arXiv 2404.13076）。支柱①重构为 forcing 论证 + source-falsification countermeasure + 域实证（非新概念）。
- **Task 3：术语审计** → oracle/falsification ✅；compliance→conformance 待定；hallucination propagation 改挂 self-preference 线。
- **E1：111 bug fault-model 分类** → 经典可发现 M+C=11/111 (10%)；残差 V+Vs+X=100/111 (90%)，0 待核；acknowledged 38 → 4 vs 34 (11%/89%)。见 [data/e1-bug-classification.md](data/e1-bug-classification.md)。🔥 弹药：qdrant #9027 的 OAS 明确不给 score_threshold 加 min/max（limit 却有 minimum:1）→ Schemathesis/AGORA+ **结构性必漏**，纯语义只有 LLM 够。MASTOR bonus：mutation 范式把原码当真相，111 条 pre-existing bug 一条都找不到（正交，非 scoop）。

## 🔴 P0 待做（定生死，自家数据）
- [x] **E1 ✅（见上 ✅ 区）｜原计划：111 bug 按 fault model 分类**：{classical 可发现（数学/crash/状态） / doc-vs-code compliance-only 残差}。产出：残差占比 + 逐 bug 标注。**决定贡献体量** + 验证 bug 真属 MASTOR §7.4.2 够不到的类。⚠️ 分类不干净（"靠 compliance 发现但根是数学"需人工裁）。
- [x] **E2 核心已由 t25 回答（2026-07-15）**。[t25_contract_counterfactual](TestVDB/scripts/t25_contract_counterfactual.py)（Round 13）已跑跨家族检验：同文档喂 GLM vs DeepSeek，DeepSeek 复现 GLM 过严契约 ≈2-4/9 → 偏差约一半 family-specific（异族能修）/ 一半 task-intrinsic（异族也复现，源码才能解）。**→ 支柱①重构**：source-falsification 真价值=解 task-intrinsic 契约错误（cross-family 结构性修不了），与 cross-family 互补不冗余。比"同族传播"框架更强、不撞 Panickssery。详见 novelty-reassessment.md §9。
- [ ] **E2 剩余（可选，judge-level）**：51-probe 集对 judge-level 无效（38 FP 全 response_code≠0，0 hard FP；GLM 25.5% 是 HTTP200 方法学 bug 非 self-preference）。若要做 judge-level，需新建 accepted-but-by-design probe 集。优先级低——generation-level 的 t25 已支撑重构。
- [ ] **t25 扩 N（2026-07-15 再评估：ground-truth 瓶颈，暂缓）**：自动挖（[t25_expand_mine.py](TestVDB/scripts/t25_expand_mine.py)，optional+严约束）仅出 3 候选，契约形式参差+匹配脆弱。根因：over-strict **判定需 ground truth**（API 是否接受 0/-1/empty），来源只有 by-design bug（池子~已用尽）或**活体特殊值测试**（起 5 Docker + 跑 probe，重组件、venue 未定偏早）。**结论：N=9 已定性支撑 §9 重构；发表级 N 走活体测试，待 venue 定了再做。** 当前优先 D1/D2/B。
- [ ] **P2 新增**：THEORETICAL_FRAMEWORK.md 补传播/self-preference 形式化（现 grep 不到，§8 未进代码库文档）。
- [ ] **P2 新增**：qdrant 有 v1.18_openapi.json → 支柱③"VDB 无 OpenAPI"软化成"OpenAPI 不充分（#9027 score_threshold 无 min/max 即证）"。

## 🟡 P1（E1/E2 后，写作前）
- [x] **D1 Table 1 重做 ✅（2026-07-16）**：[paper-draft-vldb-final.tex](paper/paper-draft-vldb-final.tex) L62/L64-79/L130 改为 §8/§9 措辞——三列（覆盖缺陷类/为何够不到 compliance 残差），加"确定性 vs LLM checker 区"区分，新增 AGORA+/SATORI/MASTOR 行（保持确定性 checker、不进 LLM-as-checker 区），LLM 行改为"被迫进入+可靠性留下段"。差分/蜕变按反驳 H/I 收窄（不再"unsuitable"）。
  - ⚠️ **遗留**：第 5 行 AGORA+/SATORI/MASTOR 暂为文本无 `\cite`（避免未定义引用）→ D2 堵 Related Work 时一起加 bib + cite。
  - ⚠️ **遗留**：L82/摘要(L47)/结论(L410) 仍用旧"contract hallucination propagation"措辞，待 propagation→self-preference+task-intrinsic 重构（独立 P1 任务，非 D1 范围）。
- [ ] **Related Work 堵漏**：补 AGORA+/SATORI/MASTOR + 综述 Golmohammadi 2022 + **Panickssery 2024（self-preference bias，支柱①文献锚）**。
- [ ] **术语定调**：compliance → conformance（NIST 背书）？hallucination propagation → 改挂 self-preference bias 线（别自称发明）。
- [ ] **roadmap25 = arXiv 2502.20812 核实** + 差分原话"may face challenges"照原口径修正（现论文"unsuitable"过武断）。

## 🟢 P2（核实类）
- [ ] AGORA+ FP 启发式全文核实（算术比较类统计过滤）。
- [ ] MASTOR 会议/发表状态核实（现 arXiv 2026-06，copyright 标 JACM 占位，未确认正式发表；若投 ISSTA 2027-01 属 prior art 须 cite+区分）。
- [ ] neuro-symbolic invariant（Wu ASE'24）ground-truth 区分锐化（数学真理 vs 源码实然）。

## ⏸ 阻塞（待 venue）
- setup-venue → write-paper 正式流水线。venue 导师未拍板。

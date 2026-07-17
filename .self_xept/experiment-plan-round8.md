# Experiment Plan — Round 8 Must-Fix (W1 + W3)
> Source: `mock-review.md` Round 8 (Weak Accept, mean 3.83/5). 瓶颈在实验，纯文字 revision 已到极限。
> Date: 2026-07-17. Venue TBD (soft ISSTA 2027-01).

## 目标
拆掉 R2 的 borderline 与三人共识的两个 Must Fix：
- **W3** dev-reviewer cross-model consistency（R2-W2 Major, R3-W4）
- **W1** task-intrinsic probe 扩到 n≥30、≥2 VDBMS（R1-W1 / R2-W1 / R3-W1 三人共识）

顺序：**W3 先**（小、快、拆 Major），W1 后（大头）。

---

## W3 — Cross-model consistency of the dev-reviewer

### 目标
量化 dev-reviewer 的 source-grounded falsification 是否 GLM-5.2 specific。回应 R2-W2：单 family 的 81% FP suppression 是 general 效应还是 GLM artifact。

### 输入
- 54 adjudicated candidates（38 acknowledged + 12 by-design + 4 rejected），来自 `TestVDB/test_questions/ground_truth.json` + `data/e1-bug-classification.md`
- 分层抽样 **20**（按 verdict 类别：~14 acknowledged + ~5 by-design + ~1 rejected，覆盖 FP 与 TP）
- seed 固定，记录选中的 20 个 issue id

### 步骤
1. 抽样：写 `TestVDB/scripts/w3_sample.py`，分层抽 20，输出 `w3_sample.json`（issue id + ground_truth label）
2. 对每个 candidate：
   a. 取原始 probe payload + live response（从 `results/{vendor}/` 历史日志 reconstruct，或重跑 live probe）
   b. **DeepSeek 作 dev-reviewer**：同 dev-reviewer prompt（注入 `intelligence/{vendor}/threat_model.json`），换 DeepSeek backbone，跑 source-grounded falsification（source retrieval + verdict）
   c. 记录 DeepSeek verdict（CONFIRMED / BY_DESIGN / FP_KILLED）
3. 比对：DeepSeek verdict vs GLM-5.2 verdict vs ground_truth
4. 统计：Cohen's κ（DeepSeek vs GLM-5.2）+ per-class agreement + 相对 ground_truth 的 FP-suppression rate

### 判据
- κ ≥ 0.6 → 单 family 可信，写进 §eval + Threats 撤回 "open"
- 0.4 ≤ κ < 0.6 → 部分可信，报 agreement + 降级 claim
- κ < 0.4 → GLM-specific，重写 §eval precision claim

### 代价
- ~20 candidate × (source retrieval + 1 LLM judge)，几小时、几刀
- 不需新 Docker（用历史 response；若重跑 live probe 则需 Milvus/Qdrant 实例）

### 输出
- `TestVDB/scripts/w3_crossmodel_kappa_results.json`（per-candidate DeepSeek / GLM / ground_truth + κ）
- 论文 §eval RQ2 加 1 段（κ 值 + 判读）+ Threats 修订

### 复用
dev_review agent + `TestVDB/scripts/threat_model_injector.py` + `TestVDB/scripts/reconstruct_context.py`

---

## W1 — Scale the task-intrinsic probe

### 目标
把 RQ3 从 n=9 / Milvus 扩到 n≥30 / ≥2 VDBMS，报 binomial 95% CI，让 task-intrinsic claim 站住。

### 关键前提（已核实 2026-07-17）
**9 是子集，非全集。** Milvus 12 by_design 里 7 个是 over-strict（47767 / 50319 / 50321 / 50322 / 50325 / 50351 / 50352），其中 50319 / 50321 / 50322 / 50325（unloaded search / dup collection / drop nonexist / underscore name）**不在 e2 的 9 里** → GLM 在 milvus 的 over-strict 全集 ≥13。

### 输入（三批，达 n≥30）
1. **Milvus 补全集（+4~6）**：unloaded search / dup collection idempotent / drop nonexist idempotent / underscore name（+ scan 其他 over-strict param）— 各取 doc passage
2. **Qdrant（+10~15）**：`TestVDB/scripts/e2_expand_candidates.json` 已有 5 bound candidates（shard_number / replication_factor / write_consistency_factor / timeout / group_size）+ scan qdrant doc 其他 optional-bound 参数
3. **Weaviate（+5~10，可选）**：ef / dynamicEfMin / flatSearchCutoff / replicationFactor（e1 分类多个 V-class bound）

### 步骤（每 clause，复用 e2 pipeline）
1. **GLM-5.2 formalize**：喂 doc passage → 产出 clause（assertion）
2. **DeepSeek 独立 formalize**：同 passage，独立产出 clause
3. **判 TI**：DeepSeek 也 over-strict on same parameter → task-intrinsic（参数级语义比对，非 verbatim）
4. **cross-model judging**：DeepSeek judge GLM clause（correct / over-strict）
5. **source-grounded falsification**：source contradicts clause → over-strict 确认

### 判据
- n ≥ 30，报 TI 比例 + Wilson 95% CI
- cross-model judging catch rate（应漏 TI 子集）
- source falsification catch rate（应 catch all）
- 若 TI 比例 < 10% → 把 task-intrinsic 从"核心贡献"降为"一个现象"（诚实结果，非失败）

### 代价
- ~30 clauses × (2 formalize + 1 judge + 1 source retrieval)，**1–2 周**
- LLM 成本可控（几刀~几十刀）
- 主要工作量：人工核对 clause 分类 + source 核验

### 输出
- `TestVDB/scripts/e2_full_results.json`（扩到 30+ clauses，per-clause TI / crossmodel / source）
- 论文 RQ3 + Table 3 + abstract 更新（n、CI、TI 比例）

### 复用
`TestVDB/scripts/e2_judgment.py` + `e2_expand_mine.py` + `e2_qdrant_probe.py`

---

## 执行清单
- [ ] **W3**: 写 `w3_sample.py` + `w3_crossmodel.py`，跑 20 candidates，算 κ
- [ ] **W3**: 论文 §eval 加 κ 段 + Threats 修订（撤 "open"）
- [ ] **W1**: 补 milvus 4~6 clauses（unloaded / dup / drop / underscore + 其他 over-strict）
- [ ] **W1**: 跑 qdrant（e2_expand 5 + scan 扩到 10~15）
- [ ] **W1**: （可选）weaviate 5~10
- [ ] **W1**: 论文 RQ3 + Table 3 + abstract 更新 n / CI
- [ ] 重编译 + mock review round 9 验证（目标：R2 从 3/5 → 4/5，整体 Accept）

---

## 风险与备案
- **W3 κ < 0.4**：说明 dev-reviewer 确 GLM-specific → 重写 §eval precision claim，把 81% 标为"GLM-5.2 下观察到的"，不再当 general。
- **W1 TI 比例 < 10%**：task-intrinsic 从核心贡献降为次要现象，abstract 去掉"task-intrinsic"主线，RQ3 标 exploratory。论文卖点转为"source-grounded falsification 的 FP 抑制"（RQ2，已扎实）。
- **时间不够（赶不上 ISSTA 2027-01）**：W3 必做（快），W1 至少补 milvus 全集到 ~13 + qdrant 5 = ~18（n=18 比 n=9 翻倍，CI 显著收窄），即使不到 30 也是大幅改进。

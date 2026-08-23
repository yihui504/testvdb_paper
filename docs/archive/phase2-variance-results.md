# Phase 2 方差实验：GLM-5.2 dev-reviewer run-to-run 复现性

> 日期：2026-08-14。目的：量化「模型不确定性」对 dev-reviewer TP/FP 判定的影响——同一 GLM-5.2、同 SOP、同材料（最新整理版）跑 2 次独立实验，看结果稳不稳。
> 关联：`docs/phase2-rerun-results.md`（首次=run1，curated）、`.paperpilot/phase2-rerun/VARIANCE_RESULTS.json`（本实验终结果）、`.paperpilot/phase2-rerun/{run2,run3}/`（两次独立产物）。

## 1. 方法

- **裁判**：GLM-5.2（harness 主模型，sub-agent 继承），派 `Agent(general-purpose, prompt=dev-reviewer.md SOP)`。
- **材料**：复用 `.paperpilot/phase2-rerun/run/`（首次整理版）的全部输入——`output_*.log`(raw HTTP 事实源) + `stage2_aggregation.json`(候选清单) + `.srcdir`(源码 clone) + 版本契约 + intelligence。两个 run 的输入树 `run2/`、`run3/` 由 `setup_runs.py` 从 `run/` 复制并**剥除一切历史 verdict**，保证双盲独立。
- **流程**：active mode（活容器 + 第1/4步 Bash 实际复现 + 第3.5步 Grep 源码 clone 接地 + 第6步三视角聚合），与首次相同。按版本派 agent（per-version batch，每 agent ≤6 case 顺序审），milvus 用**顺序 batch**（并发会争用容器，见 §4）。
- **run2 / run3 是 clean pass**（无人工清洗/救回）；run1 是 curated（首次实验经多轮清洗救回 8 FN）。**所以 run2-vs-run3 = 纯模型方差（同 batched-clean 流程）；run1-vs-{run2,run3} 混了 curation + 单/多 case 会话 + 方差，仅作参考。**

## 2. 结果

| run | recall | precision | FP-suppression | TP/FN/FP/TN | 说明 |
|-----|--------|-----------|----------------|-------------|------|
| run1 (curated) | **0.822** | 0.787 | 0.615 | 37/8/10/16 | 首次 + 人工清洗 |
| run2 (clean) | **0.489** | 0.759 | 0.731 | 22/23/7/19 | 独立即第 2 次 |
| run3 (clean) | **0.667** | 0.811 | 0.731 | 30/15/7/19 | 独立即第 3 次 |

**run2 vs run3（两次 clean 独立 pass）**：一致 **53/71 = 74.6%**，**κ = 0.497（中等）**，**18 case 翻转**。

**成对一致性**：
- run1 vs run2：43/71，κ=0.255
- run1 vs run3：49/71，κ=0.372
- run2 vs run3：53/71，κ=0.497

> 两次 clean run 彼此的一致性（κ=0.497）高于任一与 curated run1 的一致性（κ=0.255/0.372）——人工清洗把 run1 推离了模型的「自然分布」。

## 3. 18 个 run2↔run3 翻转（方差定性核心）

方向：**13 个 FP→C**（run2 漏、run3 找回），**5 个 C→FP**（run2 找到、run3 漏）——run3 整体偏 CONFIRMED（recall 0.667 > 0.489）。

| case | ver | run2 | run3 | GT | 翻转类型 |
|------|-----|------|------|----|----------|
| milvus_47635 | 2.3 | FP | C | B | 漏→找（search limit=0） |
| milvus_47729 | 2.6.10 | FP | C | B | 漏→找（nprobe 校验） |
| milvus_47752 | 2.6.10 | FP | C | B | 漏→找（ef/metricType 校验） |
| milvus_47767 | 2.6.10 | FP | C | C | FP↔FP 方向不稳 |
| milvus_49059 | 2.6.12 | FP | C | B | 漏→找（COSINE 精度） |
| milvus_50192 | 2.6.16 | FP | C | C | FP 方向不稳 |
| milvus_50324 | 2.6.17 | C | FP | C | 找→漏（len≤100 契约解释） |
| milvus_50351 | 2.6.17 | C | FP | C | 找→漏（shardsNum 下界） |
| milvus_50354 | 2.6.17 | C | FP | B | 找→漏（password range） |
| milvus_52308 | 3.0.0 | FP | C | B | 漏→找（type coercion） |
| milvus_52310 | 3.0.0 | FP | C | B | 漏→找（type coercion） |
| milvus_52313 | 3.0.0 | FP | C | A | 漏→找（JSON 字段） |
| milvus_52325 | 3.0.0 | FP | C | A | 漏→找（strictGroupSize） |
| qdrant_9039 | 1.18.0 | FP | C | A | 漏→找（wait=false 异步） |
| qdrant_9520 | 1.18.2 | FP | C | A | 漏→找（shard 上界） |
| qdrant_9522 | 1.18.2 | FP | C | A | 漏→找（lookup_from 校验） |
| weaviate_11401 | 1.37.4 | C | FP | A | 找→漏（replication factor） |
| weaviate_11732 | 1.38.0 | C | FP | A | 找→漏（distance=null 默认） |

**翻转集中在 3 类边界 case**：(a) **契约无明文断言**（search-time 参数 nprobe/ef、type coercion）→ A=NEUTRAL 时模型在「物理约束 B」上摇摆；(b) **异步/跨协议路径**（wait=false、gRPC vs REST）→ 探不探得到那条路径靠运气；(c) **by-design vs 校验缺失**的定性拿捏（50324/50351/11401/11732）。

## 4. 过程中发现并修复的可靠性问题

1. **并发 batch 致 milvus 容器争用**：run2 的 milvus 3.0.0 用 2 个并发 batch 打同一容器，出现 timeout / 集合不可用，10 case 全判 FP（8 个是真 bug）。**顺序重做后恢复 6 CONFIRMED**。此后 milvus 一律顺序 batch。（这是 run2 recall 偏低的部分原因；3.0.0 已重做修正。）
2. **zombie sub-agent**：run2 的 qdrant 1.18.2 batch agent 违规用 Agent 工具派了孙 agent，并发写坏 9373（verdicts 结构被覆盖）。已重做 9373；并在 `dispatch_sop.md` 固化「禁止派孙 agent」铁律，run3 无再发。
3. **空日志 case 倾向 UNCERTAIN**：7 个 SDK 探针 output_*.log 为空的 case，agent 易放弃（49928/49890/49059/52313 都出过 UNCERTAIN）。均重做并强调「必须活容器复现」。
4. **batch agent 偷懒无源码**：run3 的 2.6.16 batch2 对 50192/50193/50194 产出无 source_excerpt 的浅审（谎报 src=有）。重做补全源码接地。
5. **JSON 结构畸形**：run3 的 qdrant 9416-9419 把 `verdicts` 写成字符串而非 `[{...}]`（数据完整，仅结构错），脚本 `restructure` 还原。

> 这些问题本身也是发现：dev-reviewer agent 的执行可靠性（不只判断方差）受 dispatch 粒度、并发、SOP 遵守度影响——单 case 会话 + 强 SOP 提示能减少执行缺陷，但判断方差仍在。

## 5. 材料排雷后复测（方案 A：持久化 run1 清洗认定的 endpoint）

§3 的 18 翻转里有若干其实是「老雷未排」——run1 清洗时把 fill_endpoints 的抽取偏差（endpoint 标签指向错误操作）用 prompt 级覆盖修过，但**没持久化回材料**，导致 run2/run3 又踩了一遍。诊断：71 case 里 24 个 endpoint 标签与 raw 流量错配（MISMATCH）+ 7 个空日志（SDK 探针未捕获）= 31/71 材料带雷。

**处置**：从 run1 curated 判词提取「清洗认定的 endpoint」，区分两类——
- **A 类（标签错，20 个）**：标签改为 run1 认定方向，写回 run/run2/run3 三棵树（`fix_materials.py`，存档 `MATERIAL_FIXES.json`）；
- **C 类（标签本对、流量缺，5 个：49889/49929/50325/51085/9373）+ probe↔issue 错配 50355**：标签保持，重判时明确提示「日志流量不含缺陷操作，以候选方向用活容器复现，勿因流量不符判 FP」。

随后 run2、run3 各重判这 25 个 case（旧判词备份到 `.paperpilot_fixbackup/`，重判 agent 双盲不看旧结论）。重判 50/50 有效。

**排雷后指标（VARIANCE_RESULTS.json，无雷版）**：

| run | recall | precision | FP-supp |
|-----|--------|-----------|---------|
| run1 (curated) | 0.822 | 0.787 | 0.615 |
| run2 (clean, 无雷) | 0.489 | 0.710 | 0.654 |
| run3 (clean, 无雷) | **0.711** | 0.762 | 0.615 |

- **run2 vs run3（无雷）：一致 56/71 = 78.9%，κ = 0.587，15 翻转**（vs 有雷版 κ=0.497 / 18 翻转）。
- 排雷**消除了 6 个假翻转**（47635/50192/50351/52325/11401/11732——endpoint 修正后双 run 趋同），新出现 3 个（49889/50325/52314），净减 3。
- 排雷后 κ 提升 0.09（0.497→0.587），但**模型方差仍实质存在**：run2/run3 recall 仍差 0.22，15/71=21% 翻转，curated 0.822 仍比 clean 高 0.11–0.33。

> 即：低 κ 部分是老雷（endpoint 未持久化）所致，部分是模型本身方差。排雷把「材料噪声」剥离后，剩下的 κ≈0.59 才是更干净的「模型不确定性」估计。

## 6. 结论（论文 validity 核心）

**模型不确定性对 dev-reviewer 结果影响大（排雷后仍成立）**：
- 两次 clean 独立 pass 的 recall 在 **0.489–0.711** 间波动（Δ=0.222），**κ=0.587（中-好一致）**，**21% 的 case（15/71）翻转**。
- 首次 curated headline **0.822** 比 clean pass 高 **0.11–0.33**——这部分增益来自人工清洗（修 endpoint 错配、补测路径、补源码），不是模型本身能力。
- 翻转集中在**契约无明文 / type coercion / 异步路径**等「证据不足以一锤定音」的 case——三视角里 B（物理约束）和 C（by-design）的判定在这些 case 上随机。
- 排雷（持久化 endpoint 修正）把 κ 从 0.497 抬到 0.587，说明**材料噪声会低估一致性**；但抬升有限，模型方差是更主导的因素。

**对论文的含义**：dev-reviewer 的单次判定**不能当作稳定 ground truth**。应报告为「中-等可复现（κ≈0.59，排雷后）」，headline 指标需标注清洗程度，或改用多 run 投票/共识。这与 [[phase2-validity-threats]] 记录的首次有效性威胁叠加，构成对 RQ2 结论强度的实质约束。

## 6b. 三轮综合（run1 curated + run2/run3 clean 排雷后，majority vote）

把三轮（run1 + run2 + run3）放一起看「共识 vs 单 run」：

| 视角 | recall | precision | FP-supp |
|------|--------|-----------|---------|
| run1 (curated, 单) | 0.822 | 0.787 | 0.615 |
| run2 (clean, 单) | 0.489 | 0.710 | 0.654 |
| run3 (clean, 单) | 0.711 | 0.762 | 0.615 |
| **3-run majority vote** | **0.711** | **0.800** | **0.692** |

- **三 run 全一致 41/71 = 57.7%**；**2-1 分歧 30/71 = 42.3%**（分歧比率高，再次印证单次判定不稳）。
- majority vote 的 **precision 0.800 / FP-supp 0.692 均高于任一单 run**——投票对「判 CONFIRMED」降噪有效（3 run 都误报同一 FP 的概率低）；但 **recall 0.711 仍低于 curated 0.822**——投票救不回那些「2-1 多数判 FP 但其实是真 bug」的 case（如 47755/47766/49890/50323/50353/50355/52310/11401，run1 救过但 run2+run3 都漏，多数票判 FP）。
- **30 个 2-1 分歧 case 的模式**：run2 是「最保守」一极（23 个分歧里 run2=FP），run3 偏 CONFIRMED，run1(curated) 居中偏 C——三 run 的偏差方向不同，投票能折中但折中后仍偏向保守（漏真 bug）。

**综合结论**：多 run 投票能提升 precision/FP-supp（降噪误报），但**无法恢复 curated 清洗带来的 recall 增益**——后者依赖人工对证据的深度核验（补测路径、源码追溯），不是多次抽样能等价得到的。论文若用 dev-reviewer 做 GT，建议：单 run 不可靠（κ≈0.59）；多 run 投票可作 precision 友好的折中；curated 仍是 recall 上限但需披露清洗程度。

## 7. 复用

- 产物：`run2/`、`run3/`（各 71 个 `dev_review.json`，含 source_grounding+三视角；25 个受影响 case 为材料修正后重判版，旧判词备份在 `.paperpilot_fixbackup/`）、`VARIANCE_RESULTS.json`（无雷版 per-run metrics + 逐 case 三 run verdict + κ + flip 清单）、`MATERIAL_FIXES.json`（20 标签修正 + 5 流量缺陷记录）。
- 脚本（`.paperpilot/phase2-rerun/`）：`setup_runs.py`(建独立树)、`gen_dispatch.py`(生成标准 prompt)、`dispatch_sop.md`(通用指令模板)、`start_container.py`(起容器不跑探针)、`fix_materials.py`(持久化 endpoint 修正)、`analyze_runs.py`(多 run 一致性+κ)、`extract_flip_cards.py`(翻转复核卡)。

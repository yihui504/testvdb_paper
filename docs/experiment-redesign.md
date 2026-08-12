# TestVDB 实验重新设计：成果 vs 能力拆分

## 背景：导师反馈的根本问题

当前论文 RQ1（"detection capability"）用"累计提交 107 issue / 50 acknowledged / 22 by-design"作为 detection capability 指标。导师指出这**混淆了两个概念**：

| | 挖掘成果（mining yield）| detection capability |
|---|---|---|
| 本质 | TestVDB 历史实际产出（事实）| 工具检测有效性（性能）|
| 测量 | 数 GitHub + maintainer label | controlled 样本上 precision/recall |
| 当前问题 | RQ1 用的就是这个，但**混了多个历史版本**（当初漏的 FP 现在未必漏），且 sampling 不 controlled | **没做** |

导师要的"硬成果"= 重新整理的 TP-acknowledged / fixed / FP-resolved 数字（事实证据，证明 TestVDB 能挖真 bug，即"能力存在性"）。detection capability（"能力量化"）需单独 controlled 实验。

---

## Phase 1：挖掘成果整理（硬指标，必做）

**起点**：`mftui/data/yihui504-issues.xlsx`（111 issues，5 库，已含 category 字段）

| repo | count |
|---|---|
| milvus-io/milvus | 51 |
| weaviate/weaviate | 30 |
| qdrant/qdrant | 26 |
| meilisearch/meilisearch | 3 |
| chroma-core/chroma | 1 |

**当前 category 分布**：FIXED 31 / BUG_OPEN 29 / CLOSED_NO_LABEL 27 / BY_DESIGN 12 / ACCEPTED_OPEN 7 / REJECTED 4 / OPEN_NO_LABEL 1（其中 24 flagged duplicate）

**步骤**：
1. **去重**（24 duplicate → unique set；目标 ~87 unique + 验证）
2. **补全**（gh CLI 拉最新状态 + 可能漏的 issue；见末尾指令）
3. **最新版本 TestVDB 重跑每个 candidate**（尤其历史 FP/BY_DESIGN——看最新版本是否仍判 FP；这是导师关键点：当初漏的 FP 现在未必漏）
4. **硬标准重判 5 类**：
   - **TP-fixed**：merged PR 修复（验证 PR 真 merged，不只 closed）
   - **TP-acknowledged-open**：maintainer 明确标 bug 但未 fix
   - **FP-still-missed**：最新版本仍判 FP（真漏检；重跑历史 BY_DESIGN/REJECTED/CLOSED_NO_LABEL）
   - **FP-now-caught**：最新版本已判 TP（历史 FP 被新版本解决）
   - **pending**：maintainer 未显式回复
5. **产出**：硬成果表（"最新版本下，X TP-fixed, Y TP-acknowledged, Z FP-still-missed, ..."）—— 论文 RQ1 的硬成果

**gh 收集指令**（本地跑，因当前环境无 gh）：
```bash
for repo in milvus-io/milvus qdrant/qdrant weaviate/weaviate; do
  gh issue list --repo $repo --author yihui504 --state all --limit 200 \
    --json number,title,state,stateReason,labels,closedAt > ${repo//\//-}-issues.json
done
```
（meilisearch/chroma 的 4 个按需补，非 VDBMS 可放 portability）

---

## Phase 2：detection capability 实验（controlled，必做）

- Phase 1 的 unique set（已知 GT）= **controlled test set**
- 最新版本跑全 pipeline，算 **precision / recall on this set**
- 这是真正的 "bug detection capability"（当前论文 RQ1 缺的）
- **优于当前 48-candidate retrospective**：全样本（非 sampling 偏）、最新版本（非历史混合）、可复现

---

## Phase 3：FP 抑制（可选，原 RQ2 升级）

- Phase 2 set 上 dev-reviewer on/off，算 recall gain（替代当前 48-candidate 的 37%→74%）
- 若 Phase 2 set 够大，可拆 vendor（Milvus/Qdrant/Weaviate per-vendor recall，补当前 Weaviate 弱）

---

## 论文 RQ 重构建议

| 当前 | 重构后 |
|---|---|
| RQ1 detection capability（混成果）| **RQ1 mining yield**（成果：硬数字，最新版本重判，明确"累计含历史"）|
| —— | **RQ2 detection capability**（新：controlled precision/recall on Phase 1 set）|
| RQ2 FP suppression（48-candidate）| **RQ3 FP suppression**（Phase 3，on Phase 1 set）|
| RQ3 VDBFuzz 对比 | **RQ4 VDBFuzz 对比**（保留）|

当前 RQ1 的 107/50/22 数字 → 移到 RQ1 mining yield，**明确声明"累计 + 最新版本重判"**，不再叫 capability。

---

## cross-family 定位（不优先，留 limitation）

- 导师没提 = 不是论文核心。TestVDB 的 claim 是 "documentation-implementation defect target + source-grounded falsifier"，cross-family 是次要 limitation。
- 学术 reviewer 会盯（post-revision review 3/3 都标 cross-family 为 Soundness Weak 主因），但解法是**诚实声明**（§4.3 cross-model + §5 Construct validity 已有）+ D1 的 LongCat 0/144 bound。
- **不做新实验**。若投稿被 reviewer 强 push，再考虑 prompt-eng ablation（低成本，直接攻 κ 0.18-0.32）。
- 优先级远低于导师要的 Phase 1/2。

---

## 执行优先级

1. **Phase 1**（收集 + 去重 + 最新版本重跑 + 硬标准重判）—— 导师要的硬成果，最高优先
2. **Phase 2**（controlled detection capability）—— 补论文缺的能力指标
3. **论文 RQ 重构**（RQ1 → mining yield；加 RQ2 detection capability）
4. Phase 3 可选；cross-family 留 limitation

---

## 与现有实验数据的关系（避免重跑浪费）

- **可复用**：48-candidate retrospective（§4.3 RQ2）的 dev-reviewer 数据（4 backbone × 3 run）→ Phase 2/3 的 dev-reviewer 评估可在此基础上扩到 Phase 1 full set
- **需重跑**：Phase 1 的"最新版本重判每个历史 candidate"（尤其历史 FP/BY_DESIGN 的最新版本 verdict）
- **可直接引用**：D1 的 LongCat 0/144 FN bound（§5 Construct validity）、§4.3 cross-model 数据（limitation 声明用）

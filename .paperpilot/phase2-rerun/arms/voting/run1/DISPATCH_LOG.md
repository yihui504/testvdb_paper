# arm-vt-run1 派发日志

日期：2026-08-16 | 预注册：../PREREG.md（跑前冻结）

## 阶段 1：确定性直出（代码，非 LLM）

- stage2_doc.json ×71：网络不可用降级 → 全 DOC_PARTIAL（SOP L221 表）
- stage2_novelty.json ×71：全 unknown + vote=is_defect（SOP L176-178 保守路径）
- 依据：PREREG §2 设计决策——关网降级产出是 SOP 确定规约，代码直出 = 最严格执行

## 阶段 2：judge-evidence（LLM，GLM-5.2，71 case）

- 3 批并行（内部串行）：批次 A = 排序前 24（vt-run1-evA）、批次 B = 第 25-48（vt-run1-evB）、批次 C = 第 49-71（vt-run1-evC）
- 输入 = run1/llm_prompts_evidence/{did}.txt（冻结：candidate + execution_results + log 全文 + SOP 判定规则内联）
- 输出 = run1/judge_work/{did}/debate_logs/stage2_evidence_{did}.json

## 阶段 3：judge-severity（LLM，GLM-5.2，71 case）

- 依赖阶段 2 完成（SOP：severity 读 stage2_evidence 投票）✅ evidence 71/71 落盘（0 事故，无 429）
- 输入 = run1/llm_prompts_severity/{did}.txt（重组版：含最终 evidence 票）；
  severity 覆盖全部候选（含 evidence=not_defect 的——聚合闸门分离，口径取 mftui 实测）
- 3 批并行（内部串行）：vt-run1-sevA（前 24）/ sevB（25-48）/ sevC（49-71）

## 阶段 2 结果（evidence，2026-08-16）

- 30 is_defect / 41 not_defect / 0 script_error
  - 批 A（milvus_001-024）：10/14/0 — milvus_001 空日志→not_defect（预期路径）
  - 批 B（milvus_025-qdrant_005+qdrant_006 越界 1 个）：13/11/0
    （注：B 与 C 在 qdrant_006 上重叠各评了一次，两次独立判定均为 not_defect，无冲突）
  - 批 C（qdrant_006-weaviate_010）：7/16/0 — 13 qdrant 全 not_defect、weaviate_010 not_defect
- 聚合预演：崩溃旁路恰命中 qdrant_014/weaviate_010（'status: 500'）→ 规则 0 强制 confirmed，
  覆盖 evidence not_defect 票（级联确定性成分 > LLM 票，该臂机制特征）

## 阶段 4：聚合（代码，run1_merge_and_aggregate.py）

- 规则与 testvdb4exp/scripts/aggregate_votes.py 逐行同构（PREREG §6 hash）
- 适配 per-case 工作目录的独立实现；崩溃旁路用同一精确子串表

## run1 收口（2026-08-16）

**零事故**：71/71 evidence + 71/71 severity，无 429、无迟到覆盖（对照 sl 臂 run2/run3 事故）。

| 指标 | 值 | 预注册带 | 落带 |
|------|----|---------|------|
| recall | 25/45 = 0.556 | 0.25-0.65 | ✓ |
| fp_supp | 7/26 = **0.269** | 0.30-0.85 | ✗ 低于下界 |
| precision / acc | 0.781 / 0.620 | 区间报告 | — |

**确定性路径核查（判据 7，5/5 过）**：崩溃旁路恰 2（qdrant_014/weaviate_010，severity 侧
crash_auto_confirmed 同步）；doc 71×DOC_PARTIAL；novelty 71×unknown/is_defect；
severity 覆盖 71/71；单脚本强制 not_defect 3 例（milvus_029/031、qdrant_005）。

**fp_supp 出带定性**（预注册尾注路径）：方向性发现，非执行事故。机制：evidence 闸门
单向保守——C 组 19/26 被 evidence not_defect 拒（规则 1），7 个误报全走 rule4_pass
（trivial 闸门零拦截）；真缺陷被拒 20 例也全是规则 1。**级联退化为"evidence 单 judge
决定 + 崩溃旁路"**：PARTIAL -1 级未把任何票压到 trivial，severity 闸门空转。
与"多 judge 分权"设计意图相反——论文披露点。

**分母口径校准**：clean_run GT 表 = 45 真 / 26 C 组（PREREG §4"44/27"为笔误，
计算一律 45/26，与 sl 臂归档口径一致）。

**续跑决策**：按用户判据"没发现超预期问题可续跑"——执行零缺陷，fp_supp 出带已定性
为方向性发现并记录 → run2/run3 照跑（配置零改动）。

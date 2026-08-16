# voting 臂三轮报告

> 日期：2026-08-16。Run 标识：**arm-vt-run1/2/3**。
> 预注册 PREREG.md（跑前冻结：机制快照 SHA / 判据带 / 确定性路径预判 / 7 判据）。
> 材料 = arms/voting/sessions（与 single-LLM 臂同源冻结包，audit 0 FAIL）。
> 架构 = as-shipped 4 judge（doc/novelty 关网代码直出降级 + evidence/severity LLM 判定）
> + aggregate_votes.py 级联规则（同构独立实现，见 run{N}_merge_and_aggregate.py）。
> 执行事故（run3，两起，均已消解）：
> ① evidence 批次 3 文件漏写（qdrant_018/weaviate_002/006）——SendMessage 唤回原批次
> 补写（qdrant_018→is_defect / weaviate_002,006→not_defect）；
> ② severity qdrant_004 迟落盘（扫描与批 B 写盘竞态，二次聚合消解）。
> run1/run2 零事故。judge 判词 71×2×3 = 426 份全落盘（最终版）。

## 1. 三轮指标（分母 45 真 / 26 C 组，GT 同源 clean_run）

| 轮 | recall | fp_supp | precision | acc | confirmed n |
|----|--------|---------|-----------|-----|------------|
| run1 | 0.556 | 0.269 | 0.781 | 0.620 | 32 |
| run2 | 0.422 | 0.077 | 0.905 | 0.606 | 21 |
| run3 | 0.378 | 0.115 | 0.850 | 0.563 | 20 |
| **中位数** | **0.422** | **0.115** | 0.850 | 0.606 | — |
| majority-vote(3) | 0.378 | 0.115 | 0.850 | 0.563 | 20 |

**vs 预注册带（recall 0.25-0.65 / fp_supp 0.30-0.85）**：recall 三轮全入带；
**fp_supp 三轮全部低于下界**（0.269→0.077→0.115）——预注册尾注预告的方向性
超预期成立：**级联在关网降级下极端保守**（precision 0.78-0.91 是副产品）。
单调保守漂移（confirmed 32→21→20）与 sl 臂 run1-3 recall 爬升方向相反。

## 2. 机制分解（三轮规则分布）

| 轮 | rule0 崩溃旁路 | rule1 evidence 拒 | rule3 trivial 拒 | rule4 pass |
|----|--------------|------------------|-----------------|-----------|
| run1 | 2 | 39 | 0 | 30 |
| run2 | 2 | 50 | 0 | 19 |
| run3 | 2 | 1 例（milvus_019） | 1 | 18 |

- **崩溃旁路（确定性）三轮全中**：qdrant_014/weaviate_010 三轮 CCC——GT 均真缺陷，
  预注册判据 5 全中。recall 保底 2/45=0.044。
- **evidence 单闸门主导**：拒票 39→50→49，与 confirmed 数反相——级联实质 =
  evidence judge 一票定生死 + 崩溃旁路。trivial 闸门三轮仅杀 1 票
  （milvus_019 run3，severity low 经 PARTIAL -1 降 trivial）。
- **severity 闸门近乎空转**（判据 4 假说不成立的对照证据：确定性成分没有压缩方差，
  因为它不产生判断，只放大 evidence 的方差）。

## 3. 轮间稳定性（判据 4）

- κ(1,2)=0.442；κ(1,3)=0.529；κ(2,3)=0.623。
- 对照：sl 臂 0.294-0.449、fixF 系 0.187-0.486 —— voting 臂 κ **偏高且轮次越近越高**
  （2,3 相邻轮 κ=0.623），但 confirmed 数漂移 32→21→20 显示系统性保守漂移
  盖过了 case 级稳定性。三臂方差点：**架构（级联 vs 纯调用 vs agent）不改变
  "方差是模型内禀"的结论，但级联把保守漂移放大成 recall 单调下行**。
- 批次级漂移证据（dispatch_log）：run2 批 A 24 全 not_defect（run1 同批 10 is），
  批 B 14 is（milvus_027-043 集体翻正）——批次间系统性漂移是 confirmed 波动主源。

## 4. 跨臂对比（判据 2/3）

**vt-majority vs sl-majority（McNemar）**：仅 vt 对 7 / 仅 sl 对 12，χ²=0.84 不显著。
- 同材料两架构精度带重叠（vt recall-maj 0.378 vs sl 0.455；vt fp_supp-maj 0.115 vs sl 0.808
  —— **fp_supp 差一个数量级**：级联把 FP 几乎清零（3/26）而漏掉更多真缺陷）。

**vt-majority vs fixF3（dev-reviewer）**：仅 vt 对 0 / 仅 fixF 对 20，χ²=18.05 **显著**。
- fixF 在 20 个 case 上独对且 vt 零反超——**agent+工具对无工具级联的单向支配**
  （对照 sl vs fixF 的 11/16 不显著，级联的保守性把差距推成显著）。

## 5. 兴趣点轨迹（三轮 C/F 串）

| case | 三轮 | 判读 |
|------|------|------|
| qdrant_014 / weaviate_010 | CCC | 崩溃旁路锁定（确定性成分）；sl 臂 weaviate_010 为 FFF——**崩溃旁路是唯一稳定翻正通道** |
| milvus_001 | FFF | 空日志→not_defect 规则锁定（三臂一致的死刑类） |
| qdrant_002 | FCF | run2 evidence 翻正后 severity medium pass；run3 回落——灰区漂移 |
| milvus_009 | CFF | run1 中后两轮回落——灰区漂移（sl 臂 CFF 形态相同） |
| qdrant_018 | FFC | 无 expected 依据 case：run3 evidence is_defect(B) + Type4 high→medium pass；无契约也能过闸（行为论证路径） |

## 6. 判据 6（无 expected 依据 case）

- qdrant_014：崩溃旁路确认（与契约无关），CCC。
- qdrant_018：run3 走 evidence 行为论证 + severity Type4 过闸 confirmed（FFC）——
  与 sl 臂 CCC 相反方向：无契约时级联的 severity 闸门不拦行为论证。

## 7. 归档

- run{1,2,3}/judge_work/{did}/debate_logs/stage2_{doc,evidence,severity,novelty}*.json（426 LLM 判词 + 代码直出）
- run{N}/ARM_VT_AGGREGATION.json（逐 case 级联结果）+ run{N}/ARM_VT_RUN{N}_RESULTS.json
- run1/DISPATCH_LOG.md（阶段派发 + 事故记录）；聚合脚本 ×3（同构）
- 本报告 = 三轮收口；跨臂合成表进 ARM_SL_REPORT 续篇 / 论文 RQ2

# E3：聚合机械化验证实验（2026-08-18）

方案：E2 差距解剖（rq2_e2_gap_dissection.md）机制①的修复——check_chain_grounding.py 增
implied_verdict 三态（A 定案 case 聚合唯一），SOP 增聚合机械化条款（LLM 无权改写）。

## 结果

| 口径 | TP | FP | FN | TN | NME | recall | precision |
|------|----|----|----|----|-----|--------|-----------|
| fixF | 18 | 4 | 11 | 11 | 0 | 0.621 | 0.818 |
| v4.1 | 3 | 0 | 26 | 15 | 0 | 0.103 | 1.000 |
| E2-r1 | 11 | 0 | 18 | 15 | 11 | 0.379 | 1.000 |
| E2-r2 | 12 | 1 | 17 | 14 | 8 | 0.414 | 0.923 |
| **E3** | **12** | **2** | **17** | **13** | **8** | **0.414** | **0.857** |

## 聚合违例修复确认 ✅

E2 的 5 个聚合违例（A=CONFIRMED 被 LLM 以"源码推翻契约"叙事翻案）在 E3 **全部消除**：
- 独立核验（脚本重算 implied_verdict vs 判词 verdict）：**违例 0/44**
- E2-r2 的 4 个违例 TP（milvus_005/008/qdrant_001 等）在 E3 全部翻回 DEFECT

## 但 recall 持平——收益被灰区方差抵消

E2-r2 → E3 变化 24 case：翻正 TP 5 + 丢 TP 5。
丢失的 5 个（milvus_016/017、weaviate_005/007/010）全部是 **GREY_ZONE 灰区 case**
（A=NEUTRAL），其 B/C/D 判级在 E3 会话比 E2-r2 弱（DEFECT→NOT_DEFECT）。
它们是 B/C/D 的轮间方差，与聚合机械化无关。

## 结论：结构瓶颈已经清晰

- A 定案 case（37/71 链：DEFECT 18 + NOT_DEFECT 19）**已完全确定性**（A 值零方差 +
  聚合违例 0）——机械化目标达成
- 剩余噪声源 = 34 个 GREY_ZONE case 的 B/C/D 判级方差（E3 与 E2-r2 在此互相抵消）
- 追平 fixF 的下一步：**B 判据部分机械化实验**（数值下界/枚举闭集/类型恒真三类可做
  确定性脚本——参数名+契约声明+实测接受值三重机械匹配），先小实验回测同 E1 模式

数据：rq2_e3_verdicts.json + 各组 chain_verdicts_e3.json

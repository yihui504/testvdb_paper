# RQ2 29 案重判 · auditor 重审输入（E 收紧后首次实测，2026-08-30）

## 背景（判定无关，仅供定位）

revertb 实测（8-23）后，判定层新增两项机制：E 收紧（fe3a4fa——**by-design 否决必须引明示证据
（源码注释/官方声明含意图），"实现如此/无校验/沉默"≠明示，不满足 → 降 NEEDS_MORE_EVIDENCE 走人工，
不得据此 REFUTED**）与引文预检（abc7b1e）。本次对 11 个机械灰区案用当前规范重审。
机械 REFUTED 定案的 18 案不在靶面（机械层无改动）。

## 你的任务

对下列 11 案逐案重审。每案给出标准判定行（chain-auditor.md 两段式格式）：

```
verdict <defect_id> <DEFECT|NOT_DEFECT|NEEDS_MORE_EVIDENCE> fp=<doc|source|both|behavior|-> cat=<type|range|state|resource_bound|doc_consistency|other|-> rationale="<≤60字>"
```

判定纪律（与正式轮一致）：只依据链文件内的证据（文档原文/执行证据/源码引文）+
下方机械预跑与引文预检结果；E 收紧条款生效；不猜、不外推链外事实。

## 机械预跑（当前代码 check_chain_grounding.py）

| 案 | verdict_A | reason |
|---|---|---|
| milvus_007 | NEUTRAL | consistency 参数面 |
| milvus_012 | NEUTRAL | constraint_absent（回退后无覆盖约束） |
| milvus_026 | NEUTRAL | no_result 锚 |
| milvus_033 | NEUTRAL | constraint_absent（vectorFieldType 无覆盖约束） |
| qdrant_003 | NEUTRAL | consistency 参数面 |
| qdrant_006 | NEUTRAL | no_result 锚 |
| qdrant_011 | NEUTRAL | consistency 参数面 |
| qdrant_012 | NEUTRAL | no_result 锚 |
| qdrant_017 | NEUTRAL | consistency 参数面 |
| qdrant_018 | NEUTRAL | constraint_absent（count 精度无覆盖约束） |
| weaviate_004 | NEUTRAL | consistency 参数面 |

## 引文预检（当前代码 verify_chain_quotes.py）

11/11 案 MISMATCH——共性：**链内契约引言指向当前契约中不存在的约束**
（012/018/033 为契约回退后的链级残留；其余为链引言与契约 id 无法逐字对齐）。
MISMATCH ≠ 引文造假：是指链声称"违反了约束 X"而契约中无 X 或引文非契约子串。
此结果按 auditor 规范纳入权衡（不作 finding）。

## 链文件位置（已逐一核实存在）

- milvus_007 → `C:/Users/11428/Desktop/tvdb_sessions/sessions/milvus/2.6.10/milvus_007/evidence_chain/milvus_007.json`
- milvus_012 → `C:/Users/11428/Desktop/tvdb_sessions/sessions/milvus/2.6.16/milvus_012/evidence_chain/milvus_012.json`
- milvus_026 → `C:/Users/11428/Desktop/tvdb_sessions/sessions/milvus/2.6.17/milvus_026/evidence_chain/milvus_026.json`
- milvus_033 → `C:/Users/11428/Desktop/tvdb_sessions/sessions/milvus/2.6.19/milvus_033/evidence_chain/milvus_033.json`
- qdrant_003 → `C:/Users/11428/Desktop/tvdb_sessions/sessions/qdrant/1.18.0/qdrant_003/evidence_chain/qdrant_003.json`
- qdrant_006 → `C:/Users/11428/Desktop/tvdb_sessions/sessions/qdrant/1.18.1/qdrant_006/evidence_chain/qdrant_006.json`
- qdrant_011 → `C:/Users/11428/Desktop/tvdb_sessions/sessions/qdrant/1.18.2/qdrant_011/evidence_chain/qdrant_011.json`
- qdrant_012 → `C:/Users/11428/Desktop/tvdb_sessions/sessions/qdrant/1.18.2/qdrant_012/evidence_chain/qdrant_012.json`
- qdrant_017 → `C:/Users/11428/Desktop/tvdb_sessions/sessions/qdrant/1.18.2/qdrant_017/evidence_chain/qdrant_017.json`
- qdrant_018 → `C:/Users/11428/Desktop/tvdb_sessions/sessions/qdrant/1.18.3/qdrant_018/evidence_chain/qdrant_018.json`
- weaviate_004 → `C:/Users/11428/Desktop/tvdb_sessions/sessions/weaviate/1.37.4/weaviate_004/evidence_chain/weaviate_004.json`

对应契约：`C:/Users/11428/Desktop/tvdb_sessions/sessions/<vendor>/<ver>/structured_contract.json`
（ver 即上表各案版本）

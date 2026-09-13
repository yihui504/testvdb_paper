# RQ2 rerun_v2 聚合

## core（覆盖 81/81；三轮翻转 5 案）

- TP 7 / FP 1 / FN 44 / TN 29
- recall 0.137 [0.068, 0.257]；precision 0.875；suppression 0.967 [0.833, 0.994]

  分层 recall（GT=T 子集）：
      evidence_present: 7/37 = 0.189
      weak_evidence: 0/3 = 0.000
      evidence_absent: 0/11 = 0.000

## full（覆盖 81/81；三轮翻转 20 案）

- TP 41 / FP 6 / FN 10 / TN 24
- recall 0.804 [0.675, 0.890]；precision 0.872；suppression 0.800 [0.627, 0.905]

  分层 recall（GT=T 子集）：
      evidence_present: 29/37 = 0.784
      weak_evidence: 2/3 = 0.667
      evidence_absent: 10/11 = 0.909

## flat（覆盖 81/81；三轮翻转 15 案）

- TP 30 / FP 2 / FN 21 / TN 28
- recall 0.588 [0.452, 0.712]；precision 0.938；suppression 0.933 [0.787, 0.982]

  分层 recall（GT=T 子集）：
      evidence_present: 25/37 = 0.676
      weak_evidence: 1/3 = 0.333
      evidence_absent: 4/11 = 0.364

## donly（覆盖 81/81；三轮翻转 18 案）

- TP 39 / FP 9 / FN 12 / TN 21
- recall 0.765 [0.632, 0.860]；precision 0.812；suppression 0.700 [0.521, 0.833]

  分层 recall（GT=T 子集）：
      evidence_present: 28/37 = 0.757
      weak_evidence: 2/3 = 0.667
      evidence_absent: 9/11 = 0.818

## donlyq（覆盖 81/81；三轮翻转 20 案）

- TP 36 / FP 6 / FN 15 / TN 24
- recall 0.706 [0.570, 0.813]；precision 0.857；suppression 0.800 [0.627, 0.905]

  分层 recall（GT=T 子集）：
      evidence_present: 26/37 = 0.703
      weak_evidence: 2/3 = 0.667
      evidence_absent: 8/11 = 0.727

## 新旧对照（majority 口径）

| 臂 | 旧 recall | 新 recall | 旧 suppression | 新 suppression |
|---|---|---|---|---|
| core | 0.216 | 0.137 | 0.867 | 0.967 |
| full | 0.373 | 0.804 | 1.000 | 0.800 |

## 泄漏 4 包（剥除 _provenance 后）

- core: {'milvus_008': 'FALSE_POSITIVE', 'milvus_013': 'FALSE_POSITIVE', 'milvus_038': 'FALSE_POSITIVE', 'qdrant_016': 'FALSE_POSITIVE'}
- full: {'milvus_008': 'CONFIRMED', 'milvus_013': 'CONFIRMED', 'milvus_038': 'CONFIRMED', 'qdrant_016': 'CONFIRMED'}
- flat: {'milvus_008': 'CONFIRMED', 'milvus_013': 'FALSE_POSITIVE', 'milvus_038': 'CONFIRMED', 'qdrant_016': 'FALSE_POSITIVE'}
- donly: {'milvus_008': 'CONFIRMED', 'milvus_013': 'CONFIRMED', 'milvus_038': 'CONFIRMED', 'qdrant_016': 'CONFIRMED'}
- donlyq: {'milvus_008': 'CONFIRMED', 'milvus_013': 'CONFIRMED', 'milvus_038': 'CONFIRMED', 'qdrant_016': 'CONFIRMED'}

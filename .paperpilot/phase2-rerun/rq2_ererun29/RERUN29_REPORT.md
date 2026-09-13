# RQ2 29 案重判报告——E 收紧落地后首次实测（2026-08-30）

## 动机

导师反馈"错判 7 个 TP 成 FP"触发判定层改进；但 revertb 实测（8-23，0.841/0.881，7 误判）
早于核心修复落地——**E 收紧 by-design 挡人（fe3a4fa，8-25）与引文预检（abc7b1e）从未在
71 case 上实测过**。本次补测：对 revertb 终态 29 个 NOT_DEFECT 案（7 误判 TP + 22 拦截 FP）
用当前实现重判。37 个 DEFECT 案与 18 个机械 REFUTED 定案案不受 auditor 层改动影响
（E 收紧方向单调：只可能让 NOT_DEFECT 更难判，已判 DEFECT 的案不会被翻）。

## 方法（留痕目录 rq2_ererun29/）

1. 靶面重建：chain_verdicts_v9d + 三案 chain_verdicts_revertb 合成 revertb 终态，
   对照 GT 得 29 案（tmp_gen/rerun29_baseline.json；42 DEFECT/29 NOT_DEFECT 与报告 37+5/7+22 精确吻合）
2. 机械层重跑（当前 check_chain_grounding.py）：18 REFUTED 定案 + 11 灰区 NEUTRAL
   （step1_mech_quotes.json；milvus_033 链实际位于 milvus/2.6.19，idmap 记载正确）
3. 引文预检（当前 verify_chain_quotes.py，首跑）：**11/11 灰区案 MISMATCH**
   （共性：链引言指向契约中不存在的约束——回退残留型）；18 机械定案案全过
4. auditor 重审 11 灰区案（3 agent 并行，当前 chain-auditor.md 含 E 收紧，GT 不知情；
   判定行 → final_29_verdicts.json）

## 结果

### 11 灰区案 diff vs revertb

| 案 | GT | revertb | 重判 | 变化 |
|---|---|---|---|---|
| **milvus_012** | TP | NOT_DEFECT（"实现如此"） | **NEEDS_MORE_EVIDENCE** | **E 收紧挡下，转人工** |
| **milvus_033** | TP | NOT_DEFECT（"Go 默认沉默丢弃"） | **NEEDS_MORE_EVIDENCE** | **E 收紧挡下，转人工** |
| qdrant_018 | TP | NOT_DEFECT | NOT_DEFECT | 文档明示 approximate + 源码注释含意图——通过 E 明示检验；附 exploratory_candidate |
| milvus_007 | FP | NOT_DEFECT | NOT_DEFECT（fp=behavior） | 执行证据自身不成立，不经 by-design 路径 |
| milvus_026 | FP | NOT_DEFECT | NOT_DEFECT（fp=source） | 报错文本明示规则（E 认可） |
| qdrant_003/006/011/012/017 | FP | NOT_DEFECT | NOT_DEFECT（fp=source/both/behavior） | 各有明示证据（schema.rs 注释/PR#6882/维护者声明） |
| weaviate_004 | FP | NOT_DEFECT | NOT_DEFECT（fp=source） | 源码注释明示 ef=-1 sentinel |

### 终态指标（71 案）

| 指标 | revertb（8-23，修复前实现） | **本次（E 收紧后）** |
|---|---|---|
| TP 自动误判（→FP） | 7 | **5**（012/033 转人工） |
| TP 转人工（NME） | 0 | **2** |
| FP 拦截 / 放行 | 22 / 5 | 22 / 5（**零扰动**） |
| TP 自动检出 | 37 | 37 |
| recall | 0.841 | 0.841（NME 计未检出）；**人工复核后上界 0.886**（39/44） |
| precision | 0.881 | 0.881 |

## 结论

1. **改进有效且零误伤**：E 收紧把 2 个误判 TP 从"自动错判 FP"变为"转人工"，FP 侧零放行新增
   （precision 零扰动）——挡的是无明示证据的否决，有明示证据（源码注释/PR/维护者声明）的
   否决全部照常成立（qdrant_018/011/012、weaviate_004、milvus_026 均通过检验）
2. **剩余 5 个误判 TP 的结构**：milvus_001/003/004/024 为机械 REFUTED 定案（builder 的
   violates=False + 机械信号锁死，auditor 无翻案权）+ qdrant_018 通过明示检验维持——前者是
   "取证层是方差坍缩最后一站"（E5 报告结构性发现）的延续，论文 limitations 口径不变
3. 引文预检首跑 11/11 命中灰区案（均为契约回退残留型 mismatch），与机械定案案（全过）完全
   区分度高——可作为灰区案的先导信号
4. PPT 数字已同步：slide 40-44 流程图 7→5（37/5/22/5 四格），slide 38 脚注 27 FP/22 拦截 +
   转人工说明，slide 38/40 加口径注（102 = 45 TP + 33 pending + 24 adjudicated FP；
   44/27 与 #9942 差 1 的说明）

## 口径声明

- 本重判只覆盖 auditor 判定层改动的影响面（29 案），不是完整 RQ2 重跑（builder/执行层未动，
  链文件沿用 revertb 版）
- auditor 重审 GT 不知情；判定行留痕于本目录与 agent 输出
- 71 case 实验集冻结口径不变（44 TP + 27 FP）

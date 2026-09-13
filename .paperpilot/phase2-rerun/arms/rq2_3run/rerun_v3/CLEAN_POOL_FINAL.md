# RQ2 干净池终态（认知节剥除+13 run 重判，2026-09-13）

## 背景
10 个 milvus 材料包内嵌 developer_cognition 节（v9 起沿袭），违反 flat/donly/donlyq/core
臂"禁读认知材料"纪律。处置：剥除该节（材料层修复，契约/观察零扰动，原件归档），
对 4 个受影响臂的 10 案全部重判（GLM 9 run + Qwen 4 run = 13 run × 10 案）。
full 臂合法使用认知（D 视角），不重判。

## 五臂终态（majority，HR 计入 CONFIRMED，n=81：51 T / 30 F）
| 臂 | TP | FP | recall | supp | prec |
|---|---|---|---|---|---|
| core | 8 | 1 | 0.157 [0.082,0.280] | 0.967 | 0.889 |
| full (GLM) | 41 | 6 | 0.804 [0.675,0.890] | 0.800 [0.627,0.905] | 0.872 |
| flat (GLM) | 30 | 4 | 0.588 [0.452,0.712] | 0.867 [0.703,0.947] | 0.882 |
| D-only (GLM) | 36 | 8 | 0.706 | 0.733 | 0.818 |
| D-only-Qwen | 37 | 9 | 0.725 [0.591,0.829] | 0.700 | 0.804 |

## 七检验 Holm 家族（精确 McNemar）
1. core-vs-full 1/39 <0.0001
2. core-vs-D-only 2/37 <0.0001
3. core-vs-flat 0/25 <0.0001
4. **full-vs-flat 17/4 raw 0.0072 → corrected 0.0288（仍显著）**
5. D-only-Qwen-vs-flat 15/3 raw 0.0075 → corrected 0.0288（Qwen 家族内反而显著）
6. D-only-vs-flat 15/5 raw 0.0414 → corrected 0.0828（不显著）
7. full-vs-D-only 7/4 0.549

## 关键敏感性
- forced-only：full 0.529 vs flat 0.490，6/3，p=0.51（结论不变：分离由路由承载）
- Qwen 配对探针（single run，flat 重判后）：full 0.588 vs flat 0.529，10/8，p=0.81（未复制，同前）
- full 三 run 一致率 57/81=0.704（10 案无认知节后更不稳定所致，原 61/81=0.753）
- core 一致率 78/81=0.963；flat 62/81；donly 49/81
- 分层 recall full：0.784/0.667/0.909（不变）；core：0.216/0/0；flat：0.676/0.333/0.364

## 论文待改清单（发令后执行）
- core 0.137→0.157（含"0.137 是 overall 率"相关句）
- flat suppression 0.933→0.867（+其 precision 0.882；supp Wilson 区间）
- donly 0.765/0.700→0.706/0.733；donlyq 0.706/0.800→0.725/0.700
- full-vs-flat：18/3 p=0.0015/Holm 0.0045 → **17/4 p=0.0072/Holm 0.029**
- 七检验脚注全部换 p 值（上表）
- 排序句：core < flat < D-only ≈ full → **core < flat < D-only(GLM)≈不显著, full 与 D-only 均居上；GLM 家族内过校正的是 full-vs-flat 与 D-onlyQ-vs-flat**
- backbone 复制段：D-only-Qwen 0.725 且其 vs flat 在家族内显著（0.029），但 vs GLM-flat 未测新数字；Qwen 配对探针 0.588/0.529 p=0.81 保留
- forced-only 0.510→0.490、p=0.55→0.51
- HR-component confirmations 17→21（routing 通道计数变，叙事框架不变）
- case agreement 数字 61/81→57/81 等
- 泄漏段重写：删"辩护敏感性"，改"发现内嵌认知节→剥除→受影响 13 run 全案重判→数字如上述"
- Table 4/5 全部换数；摘要/intro/contribution 2 数字同步
- 重编译验证

## 产物
- rerun_v3/run_{flat,donly,donlyq}*/verdicts_rejudge_cog.jsonl + rerun_v2/run*/verdicts_rejudge_cog.jsonl
- 合并入 verdicts_batch*.jsonl（原件归档 _pre_cogstrip_merge/）
- 剥除包原件归档；27_final_aggregate.py 全链可复算

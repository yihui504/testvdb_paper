# 完备材料列预注册（2×3 析因补全，2026-08-24 跑前冻结）

## 设计

补全 2×3 析因的缺失两格：sl/vt × 完备材料（+考古断言 +认知锚点）。
已有格：sl×原始 45.5 / vt×原始 38.6 / 新链路×原始 70.5(v7.x) / 新链路×完备 84.1(revertb)。

## 材料变化（对齐 revertb 注入物，两臂对称）

1. **断言案 4**（materials 增加"补充契约依据"段，条目原文来自实验树契约）：
   - milvus_008 + milvus_metric_cosine_range_001（COSINE distance∈[0,2]）
   - milvus_013 + milvus_type_request_timeout_001（Request-Timeout 须整数）
   - milvus_038 + milvus_state_group_by_field_001（group_by_field 须标量）
   - qdrant_016 + qdrant_type_lookup_from_001（lookup_from 须存在）
2. **锚点案 10**（milvus，增加"维护者态度参考"段，4 锚点全量带原话引文）：
   milvus_010/014/018/019/022/026/027/028/032/033
   ——案集由确定性指纹匹配筛选（锚点 fingerprints 词组全部在材料文本在场），
   不参考 GT 或任何判定结果
3. 其余 57 案材料零改动、不重跑（sl/vt 判定=材料内联一次调用，材料不变则判定分布不变）

重跑集合：14 案 × 3 轮 × 2 臂（sl 单调用；vt 4-judge 级联）。
majority(3) 聚合，其余案沿用各臂原始 majority 判定，合成完备列全量 71 案指标。

## 预注册判据（跑前冻结，防事后解释自由度）

**主判据**：sl/vt 完备列 recall 增益 < 新链路增益（0.705→0.841=+13.6pp majority 口径）的一半。

两种结果的预写叙事：
- **成立**（增益小）：材料增益需要机械兑现通道（断言→机械 A 过闸、锚点→指纹触发），
  LLM 自由裁量兑现不了——架构论证核心
- **不成立**（增益大）：材料完备化本身主导判定上限，架构增益有限——新链路的独立
  卖点转为方差（带宽 0.045 vs sl 0.19）与确定性

**辅判据**：完备列下 sl/vt 的轮间方差不因材料补全而收窄（材料补的是证据不是纪律）。

## 纪律

- 材料：materials_complete/ 新目录（原版零改动即天然备份）；改版只加两段，原文逐字保留
- leak_scan：14 案改版材料扫 GT 语义词（gt_label/CONFIRMED as label/FP 标记）0 命中才可跑
- sl：PREREG.md 冻结模板逐字（仅材料换完备版），3 轮，每案独立判定
- vt：对齐 voting 原 4-judge 结构与聚合脚本
- 聚合与 McNemar：majority(3)；完备列 vs 原始列配对 McNemar（材料主效应）；
  完备列 vs 新链路完备列 McNemar（架构残余差）

## 产物

arms/single_llm/run{N}_complete/verdicts/*.json
arms/voting/run{N}_complete/...
arms/COMPLETE_MATERIAL_FACTORIAL.md（析因表+主效应/交互效应）

# RQ3 re-discovery 预注册（跑前冻结，2026-08-24）

> 归属：实验仓。跑的是 ADR-0009 实现（删 vein + 两阶段探索调度 + exploratory
> 通道 + confirm_per_round=false 特化配置）。**本文件在实验启动前冻结判据，
> 跑后不得追加/修改主判据。**

## 一、实验定位与目标

**能力验证（re-discovery）**：在 GT bug 存在的版本上，用最新实现重新发现
已知 bug。**不是**泛化性/新颖发现能力证明（算子锚形态学通用，不逐案定制；
泛化声明克制）。验收总原则（用户 D7）：**保住原收获**——改进的动机与
验收线 = 不丢原 TP。

## 二、版本与目标集

与 VDBFuzz 等时对比共享**四版本**（`docs/rq3-gt-typology.md` §四，2026-08-24
拍板选项 2）：qdrant v1.18.0（GT 2）+ v1.18.2（GT 4，契约需重生成）/ weaviate
v1.37.4（GT 3）/ milvus v2.6.10（GT 5，契约需核验无 GT 污染）。合计 GT 14
（crash 2 / logic 12，violates 族在场 2）。GT 以 `.paperpilot/phase3/gt/`
权威源为准（树外隔离，判定过程零接触）。
**9045 纵深对照**：其存在于 v1.18.0、不在 v1.18.2——两版间"已知修复 bug
消失"作为重发现特异性的对照证据单独记录。

## 三、实验配置（冻结）

1. `confirm_per_round = false`（统一判定特化，ADR-0009 §6；settings 变更留痕）
2. GT-free 三件套照旧：intel leave-one-out、GT_HINT 恒空、gt.json 树外
3. 挖掘预算：与对比实验同一 T（校准后定），轮数上限 max_rounds 默认，
   两阶段调度自然切换（块耗尽/平台期 → 探索模式）
4. 判定：会话终止后统一批量判定（机械预跑 + SOP + auditor，含
   candidate_class 标注）+ novelty 终判
5. 每版本 r=3 重复（探索随机性 + LLM 方差；majority 聚合）

## 四、判据（跑前冻结）

**主判据 1（GT 重发现率，分层）**：
- strict 率 = N₁ / GT_total（strict_defect ∩ GT）
- strict+exploratory 率 = (N₁+N₂) / GT_total（exploratory_candidate ∩ GT）
- 两率同报，不许只报高者

**主判据 2（验收线，"保住原收获"）**：四版本 GT 14 案上，
strict+exploratory 率 ≥ 当年旧口径重发现水平（旧轮 voided 前记录，口径
不一致时以逐案对照为准）；**软线 = strict+exploratory ≥ 10/14**（供校准的
先验线，miss 案逐案归因；violates 专项见 §六）。

**辅判据（探索模式增量）**：
- 探索模式产出案数 / 版本（阶段二激活后产生的候选占比）
- 当年"自由发挥"型案（violates 族等零信号案）被探索模式重新产出的比例
- 探索产出过 strict 通道的升级率（candidate_class 升级路径有效性）

**新发现单列**：GT 外新 bug（经统一判定 strict 确认）单独计数，不并入
重发现率（防分母污染）。

## 五、预写叙事（两种结果的解释框架，防事后解释自由度）

- **叙事 A（重发现率高）**：两阶段调度 + exploratory 通道成功吸收了旧
  "自由发挥"能力——删 vein 无损失、分层候选体系兑现
- **叙事 B（部分案 miss）**：miss 案逐案归因（契约缺断言族 = 判定基础与
  GT 来源系统错位的延续，见 revertb 发现 ④；或探索算子未覆盖该形态）——
  作为 limitations 素材，不得回滚已定案实现规范

## 六、纪律（红线）

1. **禁止单案调参/结果驱动改词表**（in-sample）——发现的实现缺陷走 ADR
   迭代流程，且改动后的版本须重跑全部版本（不patch 单案）
2. 派发词 = 插件规范定义（R12），不多给；只派插件 agent（R1）
3. 判定过程零 GT 接触；对账仅在判定全部完成后一次性进行
4. 全程留痕：settings 变更、阶段切换日志（exploration_phase.py 输出）、
   批量探针产出、统一判定 JSON
5. **violates 族专项检验**：milvus_003/004（47752/47755，v2.6.10 在场）
   作为零信号案代表单独跟踪——探索模式是否为其重新生成主张（has_claim），
   是 D1"violates 族交端到端"决策的直接检验点（专项线：≥1/2 案被探索
   模式重新产出主张）；milvus_001（v2.3.22）/024（v2.6.17）不在四版集合，
   推迟到后续版本实验同口径跟踪

## 七、产物约定

- 运行树：`results/rq3-rediscovery/{vendor}/{version}/{run1..3}/`
- 统一判定：`chain_verdicts_final.json`（含 candidate_class）
- 对账表：`rediscovery_matrix.md`（GT 案 × 三轮 × strict/exploratory/miss）
- 报告：`rq3-rediscovery-report.md`（对照本预注册判据）

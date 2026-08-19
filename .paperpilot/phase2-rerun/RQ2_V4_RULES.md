# RQ2 v4 实验规则（打回重审机制验证 + 全量复判）— 2026-08-18

> 仿 Phase 2 clean_run 纪律（dispatch_sop_v2 + 泄漏扫描 0 命中先例）。
> 本文是 v4 运行的**唯一派发依据**——派发 prompt 一律由 gen_dispatch_v4.py 生成，禁止手写。

## 零、v3 运行的两条教训（v4 规则的由来）

**教训 1（派发方式）**：v3 部分派发是手写 prompt + 让通用 agent 角色扮演——即使
subagent_type 填了 `testvdb:evidence-builder`，prompt 里手写"你是 TestVDB 的 evidence-builder"
并复述 SOP 要点，等于把插件原生 agent 降级为普通 agent（SOP 本来就在 agent 定义里）。
**修正**：v4 派发 prompt 只含**任务参数**（case 清单/材料路径/产出位置/汇报格式），
不含角色声明、不复述 SOP 内容。原生 agent 的角色与 SOP 由 `subagent_type` 自带。

**教训 2（GT 泄露）**：v3 复判的 builder prompt 中出现了主审人事先分析出的结论性语言
（"上一轮有取证漂移""REQ 1 是主违规观测""REQ 3 是次观测记 secondary""这是 HTTP 语义
观测"）——这些是基于 GT 诊断的预嚼结论，喂给被测 agent 后任何翻正都失去效度。
**修正**：v4 派发 prompt 禁止任何 case 级分析。claim 对照锚**只允许原文引用 packet 的
raw_observation 字段**（候选材料本身），不允许主审人的解读、定位（"REQ N"）、
方向提示（"应记入哪个字段"）、轮次背景（"上轮判错了"）。

## 一、被测系统（固定）

- builder：`testvdb:evidence-builder`（SOP = 插件 cache 645e49f 版，含全量取证硬约束/
  claim_alignment/http_semantics——**注意：SOP 内容不进派发 prompt**）
- auditor：`testvdb:chain-auditor`（SOP 含第 4 查/rework_order/视角 B 五类/视角 D）
- 认知材料：`tvdb_sessions/intelligence/{vendor}/developer_cognition.json`（注入版，三
  vendor 已统一，与旧链路同源）
- 材料：71 case（链/契约/log/clone 与 v3 同源，链文件保持 v3 状态除明示重建者）

## 二、派发规则

### R1 生成器唯一
所有派发 prompt 由 `gen_dispatch_v4.py` 生成（模板内置于脚本，含自动泄漏扫描）。
手工临时派发（如 rework 轮次驱动）也必须先过泄漏扫描函数再发。

### R2 泄漏扫描（硬门禁，gen_dispatch_v4 内置）
prompt 生成后自动扫描，命中任一即 FAIL 拒发：
- GT 词：`CONFIRMED`（作 GT 标签用）/`FALSE_POSITIVE`（同）/`gt_label`/`GT 参考`/`翻正`/`FN`/`TN`/`上轮判错`/`上一轮`/`复判`/`主验证点`
- 主审人定位语：`REQ \d+ 是主?违规`/`主违规观测 =`/`次观测，记入`/`应记入`
- SOP 复述段头：`你是 TestVDB`（原生 agent 禁角色声明）
- 轮次/实验元话语：`v\d 运行`/`验证效果`/`预期翻正`
- 例外白名单：`raw_observation` 内的原文（candidate 材料本身）不受限

### R3 claim 对照锚的喂法
- 来源**仅** packet 的 `raw_observation` 字段原文（cases_index → packets/{orig}.json）
- prompt 中呈现为：`候选现象声称（packet raw_observation 原文）：{原文}`
- 18 个 raw_observation=null 的 case：呈现 `（无 packet raw_observation，按 log 全文自定主观测）`
- **不加任何解读**

### R4 派发对象
- 一律 `Agent(subagent_type="testvdb:evidence-builder" / "testvdb:chain-auditor")`
- 多 case fan-out：builder 每 case 一个实例（并发）；auditor 按组单实例

### R5 输出位置（判词可追溯）
- builder 链：`{sess}/{did}/evidence_chain/{did}.json`（v4 重建者覆盖；非重建保持 v3）
- auditor 判词：各组 `debate_logs/chain_verdicts_v4.json`（不覆盖 v1/v2/v3）
- rework 工单留痕：auditor 判词内 rework_order 字段 + 主进程在
  `phase2-rerun/rework_state_v4.json` 计数（3 轮上限执行记录）

## 三、v4 运行设计

### 阶段 A：漂移重建子集（机制因果验证）
- 对象：**全部 71 case 重建链**（不是只重建漂移 case——重建子集若按 GT 挑选即引入选择偏倚；
  v3 首轮链无 claim 对照锚，全部按新 SOP+claim 喂法重建才是同口径）
- 但考虑成本，分两步：A1 先全量重建（builder ×71，fan-out；容器组内串行同 v3 协议）
  → A2 auditor 全量收口（15 组，判 chain_verdicts_v4.json）
- A2 中 auditor 对链漂移的判定自主发生（第 4 查）——主进程只在收到 rework_order 时
  机械重派（工单原文随 prompt），3 轮上限执行

### 阶段 B：指标与对照
- 全量 71：v4 vs v3 vs v2 vs fixF 四列（recall/precision/fp_supp + rework 统计）
- 漂移/HTTP 两类 FN 的翻正数（主进程事后归因，不进 prompt）
- TN 侧翻错检查（precision 不降）
- 视角 D 命中与实质参与定案数（同 v3 口径）
- rework 机制统计：工单数/type 分布/轮次分布/打回-修复成功率

### 阶段 C：预注册判据（跑前锁定，防事后合理化）
1. 机制有效性：漂移+HTTP 两类 FN 翻正 ≥3 且 TN 翻错 ≤1
2. 全量指标：v4 recall ≥ v3(0.591) 且 precision ≥ 0.76
3. 若 1 不达但 2 达：机制单独报告"未见效"，指标改进归因需审计（可能是 SOP 其他条款效应）
4. rework 轮次分布：任一 case 用满 3 轮仍未对齐 → 该 case 记保守 NOT_DEFECT 并入统计

## 四、主进程职责（与被测系统隔离）

- 只做：生成 prompt（过扫描）/ 派发原生 agent / 机械检查产出（.done 与 JSON 合法性）/
  rework_state 计数与重派 / 事后指标计算与归因（在 case 全部判定完成后）
- 不做：任何 case 级判定干预、prompt 内预嚼结论、按 GT 挑选重建子集

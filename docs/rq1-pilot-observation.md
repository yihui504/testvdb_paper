# RQ1 端到端 pilot 观察清单（qdrant v1.18.2，2026-08-20）

> Pilot 目的：新架构（ADR-0008 底座 + 实验改造 5aae2a7）首次在 milvus/qdrant/weaviate 上跑端到端。
> 历史两次全链路验证都在 chroma v1.5.9 上（冒烟 + 第二次全功能），qdrant 是首飞。
> 通过标准 + 观察点 + 常见坑。全部产出物路径以插件 cache 为根：
> `C:\Users\11428\.claude\plugins\cache\testvdb\testvdb\2.3.0\`
> （下文记 `{CACHE}`；会话目录 `{SD}` = `{CACHE}\results\qdrant\v1.18.2\{timestamp}\`）

## 启动

```
/testvdb:mine qdrant v1.18.2
```

- 不带 `--max-rounds`（默认 30 已在）/ 不设 `TESTVDB_NOVELTY_BYPASS`（本版无此开关）
- gt.json 已在 `{CACHE}\results\qdrant\v1.18.2\gt.json`（4 bugs：qdrant_9017 / 9421 / 9520 / 9522）
- GT 内容主进程知道即可，**观察者不要去 prompt 里加任何端点/参数暗示**（盲注契约）

## 观察点（pilot 核心价值 = 前三项是"机制是否真在工作"的历史欠账）

### A. retry 子循环是否真在工作〔checklist 1.2 遗留待验证，最高优先〕

历史仅 1 会话进过 retry 且未修好，机制是否真在工作从未验证。每轮 8d.5 后看：

```bash
# 分类器输出（stderr/stdout JSON）：
python {CACHE}/scripts/_classify_script_errors.py "{SD}"
python {CACHE}/scripts/_apply_script_retry.py "{SD}"
```

- [x] 有坏脚本时：`{source}_scripts/{script_id}.retry_feedback.json` 生成？
- [x] attack agent 读 feedback 修后**覆盖原文件**，再次执行通过？
- [x] retry_count 递增、超限（3 次）脚本被降级跳过而非死循环？
- [x] **记录数字**：坏脚本数 / regen 数 / 修好数 / 超限数 → 存 `observation_retry.md`
  （checklist 1.2 要求"retry 成功率统计写入 execution_summary"——本 pilot 先人工采，若机制确认工作再提工程化）

### B. GT_HINT 注入时机与计数正确性〔#5 改造在新链路上的首验〕

- [x] 第 1 轮派发词含「已确认 0/4」催促（chain_verdicts.json 尚不存在 → confirmed 空）
- [x] 首批 DEFECT 判出后（8e.7 auditor 收口写 chain_verdicts.json），下轮催促计数 = 累计 DEFECT 去重后对齐 GT 的数
- [x] NOT_DEFECT / NEEDS_MORE_EVIDENCE **不计入**计数（injector 只读 DEFECT 条目）
- [x] 4/4 全 reach 后催促消失（all_reached=true → GT_HINT 空串）
- [x] 4 个 attack agent（boundary/state/semantic/vein）收到的 hint 文本**完全相同**（盲注契约：无方向泄露）

### C. novelty 终判与归档〔RQ1 新列数据源，首验〕

跑完 Step 9 后：

- [x] `novelty_gate.json` 产出，candidate 有 grade / endorsement / related_issue_numbers
- [x] NON_NOVEL → `archived/` 目录 + `manifest.json`（**不是删除**）
- [x] **reach 口径执行**：reach 统计取 `debate_logs/chain_verdicts.json` 的 DEFECT **全集**（含被归档的），不取 Gate-Endorsed 集——事后对齐 GT 时自查这一条
- [x] 注意 gate 会逐 candidate 查 GitHub（限流/耗时正常，别误判挂死）；param 为空的 candidate 走 UNVERIFIED 保守路径——记录出现次数

### D. 新链路端到端冒烟（qdrant 特有首飞项）

- [x] Step 1 契约：qdrant v1.18.2 文档抓取/版本锚定正常（weaviate 才有 OpenAPI tag 强校验，qdrant 看文档站）
- [x] 分块派发：chunks.json 生成、每轮一块（块内 ≤12 单元）
- [x] 8e 链路：extract_candidates → L1 → builder fan-out（1/候选）→ auditor 收口（≤12 链/批）
- [x] NME 补证轮触发时真实回 builder（≤1 次）
- [x] 容器：qdrant v1.18.2 镜像拉取、`docker compose -f docker/qdrant.yml` 起停正常

### E. RQ1 采集项（pilot 顺采，正式跑 15 版本时同清单）

| 采集项 | 产出物 |
|---|---|
| reach（DEFECT 全集 vs gt.json 4 bugs） | `debate_logs/chain_verdicts.json` + 事后 LLM 盲评对齐 |
| 首达轮次 | 各轮 debate_logs 时间戳 + chain_verdicts 出现轮 |
| FP 过滤后数据 / Submitted | `novelty_gate.json` + `issues/` + defect-review.md |
| **发现已被报告 bug 列** | `archived/manifest.json` 的 related_issue_numbers |
| novelty 归档数据 | `archived/` 全目录 |
| 脚本产出统计 | 各 `*_scripts/` 目录 + `execution_summary`（若有） |

## 通过标准（pilot → 15 版本全量的门）

1. **硬门**：无 pipeline 级故障（agent 派发失败 / 容器起不来 / 状态机卡死）；A/B/C 三机制确认真实工作
2. **软门**：4 个 GT bug 至少 reach 1 个即可放行全量（pilot 测的是机制不是成绩；qdrant_9045 型 standalone-unreachable 已知可能挖不到，4 bugs 里 9017 probe 已验证可触发）
3. **异常即停**：GT_HINT 计数错乱 / auditor 超时保守路径触发 / novelty gate 把 DEFECT 从 reach 分母里删掉（口径违背）→ 停下排查，不带病铺 15 版本

## 已知坑（前两次 chroma 验证 + RQ2 经验）

- **SDK 版本不匹配假缺陷**（chroma 首验教训）：builder/auditor 能正确识别为客户端问题——qdrant 若出现同类，正确判定 NOT_DEFECT 不算失败，但要记录
- **auditor 单会话超 12 链串扰**（RQ2 v4.1 教训）：>12 候选时确认分批派发真实发生
- **claim 对照锚程序化传递**（E4.1 教训）：观察 builder 消费的是 chain/contract 原文，不是转述
- **会话产出在 cache**：别在 testvdb4exp 仓库里找产出；跑完把 `{SD}` 整目录拷回论文仓库归档（`results/rq1-pilot/`）

## 跑完动作

1. `{SD}` 拷回论文仓库 `results/rq1-pilot/qdrant-v1.18.2/`
2. 填本文件 checklist 勾选 + `observation_retry.md` 数字
3. reach 对齐（LLM 盲评 GT 对照）→ 汇总进 `docs/phase3-progress.md` 档3 节
4. 三机制结论 + 是否放行 15 版本全量的判断 → 回 `docs/mentor-feedback-checklist.md` 2.1

---

## Pilot 结论（2026-08-20 跑完，session 2026-08-20T06-28-05Z）

### 三机制判定

| 机制 | 判定 | 证据 |
|---|---|---|
| A. retry 子循环 | ✅ 真实工作 | R1 全链路验证（feedback→agent 修→覆盖→重跑过）；4 轮 38 坏/16 regen/16 修好/0 超限；超限降级无触发样本 |
| B. GT_HINT 注入 | ✅ 真实工作 | R1 「0/4」→ R4 后「1/4」正确递增；4 agents 同文本；NOT_DEFECT 不计数 |
| C. novelty 终判 | ✅ 真实工作 | gate 26 判定（12 NOVEL / 5 BY_DESIGN / 9 UNVERIFIED 保守路径）；UNVERIFIED 9 次；0 NON_NOVEL → archived 分支未触发（无实证，非缺陷） |

### 结果数字

- **reach 1/4**（qdrant_9017 hnsw_ef，via vein_hnsw_ef_null_search_1 DEFECT）——软门达标
- 26 DEFECT / 41 链（4 轮，R5 提前收口）；12 Gate-Endorsed NOVEL + 6 issue 草稿 + 7 MRE
- **结构性发现**：GT 4 bugs 中 3 个（recover / shard_number / lookup_from）不在 10 端点契约覆盖内 → 本契约下 reach 理论上限 = 1/4。**契约覆盖率是 reach 的第一瓶颈**，全量 15 版本前需评估契约端点扩充（qdrant 至少补 cluster + query lookup_from）

### 途中修复（已落盘 testvdb4exp，待 commit）

1. `gt_reach_injector.py`：verdicts[].param 缺失 → meta.json fallback
2. `novelty_gate.py`：同款 param 缝隙 → 同款 fallback
3. vein meta.json 无 param 字段：本会话手工回填 7 个（机制级修复待议：attack-vein.md 规范补 param 要求）

### 途中踩坑（全量 15 版本必防，详见 results/rq1-pilot/observation_retry.md）

子 agent 相对路径漂移 / executor 忘设 TESTVDB_DB_URL / 集合残留 409 / f-string 动态 VERDICT 静态误报 / auditor verdicts 无 param 字段（双消费方缝） / agent 虚报修复需 grep 复核 / passport hash 时序 bug / auditor >12 链正确拒批（分批派发解决）

### 放行判断

✅ **放行 15 版本全量**，附条件：
- 契约端点覆盖评估先行（否则 3/4 GT 面不可达的版本 reach 被系统性低估）
- 派发词模板固化（绝对路径 + export TESTVDB_DB_URL）
- archived 分支无实证——首个版本若出 NON_NOVEL 需即时人工验证 manifest

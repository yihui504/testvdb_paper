# TestVDB 实验纪律（Discipline Charter）

> 制定背景：2026-08-22 RQ1 全量 #8-#13 期间发现并处置系列流程违规（用户审计指令）。
> 本文件是**强制规则**——违反任何一条红线 = 该环节产物作废（不修复、不重审、直接作废留证）。
> 适用范围：testvdb4exp / mftui TestVDB 全部实验会话（主进程与全部 agent）。

---

## 一、红线（违反即作废）

### R1. 主进程零生成权
主进程（编排层）**不得编写任何攻击脚本、测试脚本、复现脚本**。
- 脚本的唯一来源是 attack agent（盲注派发）
- 需要验证性测试（如 GT 不复现判定）→ 必须派 agent；主进程自写的任何脚本产物一律作废
- 先例：#11 主进程查 GT 后写三条复刻脚本（作废+tainted 留证）；#10 的 49059 复现脚本（作废）

### R2. 查阅 GT 后禁止一切定向传导
主进程在**查阅任何 GT issue 内容之后**，不得：
- 补契约断言（B7 契约承载必须**先于**查 issue——正确顺序：B7 抽查缺失→源码回填→之后才允许查 issue 做盲评）
- 在派发词中点名参数/端点/形态
- 构造非标准 hint 文本（hint 只能来自 injector 的机械输出）
- 先例：#9 R2 查 47763/47766 后补两条契约断言（作废重跑）；#10 手工构造 0/1 hint（记录在案）

### R3. builder 与 auditor 永久分离
- **禁止**同一 agent（或同一次派发）既建链又判定——判定独立性是证据链架构的存在前提
- auditor 只读链文件做判定；builder 只取证不做判定
- auditor 批量上限 ≤12 链/次（2026-08-18 串扰规则），超限分批派**独立的 auditor 实例**
- 先例：#12 R2 四链 builder+auditor 合体自审（C/D 段全作废）

### R4. executor 必须是 docker-executor agent
- 脚本统一执行只能派 `testvdb:docker-executor`；**主进程不得批量替代执行**
- executor 派发词必带完整环境三要素：`TESTVDB_DB_URL` + `TESTVDB_TARGET` + `PYTHONPATH=<cache>/scripts`（缺一会导致 runtime ImportError/RuntimeError 假失败）
- 主进程可做的仅限：跑机械工具（injector/novelty_gate/verify_defects/validate_doc_coverage/passport_verify——这些是 pipeline 工具不是 agent 职责）
- 先例：#8 R2 起主进程批量 executor 成惯例（#8/#9/#10/#11/#12/#13 的相关轮次全部作废）

### R5. 判定权唯一归属
- DEFECT/NOT_DEFECT 终判 100% 出自 chain-auditor agent
- 主进程对 auditor 判定行只做**机械转写/合并**（两段式），不得修改判定值
- auditor 判定与机械门（verify）冲突时：如实记录双门分歧，不得静默取舍

### R6. 运行时必须派插件 agent（禁止"普通 agent + 提示词注入"）
所有实验环节的子代理必须是**插件 agent**（`subagent_type="testvdb:xxx"`：knowledge-extractor / contract-formalizer / attack-boundary|state|semantic|vein / docker-executor / evidence-builder / chain-auditor / reporter / reporter-mre）。
- **禁止**用 general-purpose / claude / executor 等普通 agent 配长提示词模拟插件 agent 职责——插件 agent 的规范（system prompt/工具集/输出契约）是流程有效性的组成部分，提示词注入不可等价替代
- **禁止**以 `model=` 覆盖 + 提示词补丁的方式绕过插件 agent 定义（model 覆盖仅用于资源调度如 auditor 的 sonnet，不得改变职责契约）
- 派发词只传**任务参数**（路径/环境/上下文），不得注入职责定义、判定基线、输出规范——那些属于插件 agent 自身的 .md 规范
- 先例背景：fullrun#4 auditor 超限事件的修复（两段式）正是靠固化进 chain-auditor.md 规范而非派发词注入才稳定

---

## 二、职责边界（agent 分工表）

| 环节 | 唯一执行者 | 主进程可做 | 主进程禁止 |
|------|-----------|-----------|-----------|
| 知识提取 | knowledge-extractor | 派发+验收 | — |
| 契约形式化 | contract-formalizer | B7 抽查、驱动补全 | 直接 patch 契约内容 |
| 攻击生成 | attack-* 四族 | 盲注 hint 派发（injector 文本） | 写脚本/点名参数 |
| 统一执行 | docker-executor | 前后健康检查 | 批量跑脚本 |
| 证据链 | evidence-builder | 派发+分批（≤12） | 判定 |
| 终判 | chain-auditor | 判定行机械转写合并 | 改判定值 |
| 缺陷报告 | reporter | summary.md 代写（Write 拦截时）、实测门（test -s） | 虚报放行 |
| 机械门 | verify_defects 等工具 | 跑工具+读结果 | 绕过门 |

## 三、灰色操作规范（允许但必须披露）

以下机械性操作允许，**每次必须在 summary.md 机制事件节记录**：
1. agent 脚本的机械修复（如解包 bug 的 sed——格式层，不涉攻击设计）
2. defect 报告的 Ring 标注词对齐（格式层）
3. meta.json 的 param 机械补登/规范化（原值存 `param_original_compound`）
4. candidates 机械提取的正则适配（VERDICT 行格式差异）
5. auditor summary 计数漂移的机械校正（以条目数组实数为准）

## 四、作废操作规程

发现违规（无论谁发现）：
1. **停**：立即停止该环节下游
2. **废**：违规产物移 `voided/` 或 `tainted-*/`（留证不删除）+ chain_verdicts 回退 + VOIDED.md 声明（写明违规类型与影响范围）
3. **记**：checklist 行标注"部分作废/作废"+ 修订数字 + memory 更新
4. **重**：需要数据则按纪律重跑（agent 全流程）
5. **作废单位 = 版本（用户指令 2026-08-22）**：任一轮次涉违规 → 该版本实验全体无效（含合规的 R1 轮），不采用"部分作废保留 R1"——部分保留会让版本内数据混合不同合规状态的轮次产物
6. 不做"修复性重审"（如让新 auditor 补审自审链）——直接作废重跑

## 五、已发生的违规与处置索引（2026-08-22）

| # | 版本 | 违规 | 处置 |
|---|------|------|------|
| 1 | #9 R2 | R2（查 issue 后补契约+派发点名） | 原轮作废；R2b 重跑后又因 R4 作废——最终 R1 only |
| 2 | #10 | R1（主进程写+跑复现脚本）；R2（R4） | 复现脚本+R2 三链作废 |
| 3 | #11 R2 首轮 | R1（主进程写脚本） | 作废+tainted-mainproc-scripts/ |
| 4 | #11 R2 重跑轮 | R4 | 作废——R1 only |
| 5 | #8 R2 | R4 | 作废（rowCount 翻案+47635 正面测连带作废） |
| 6 | #12 R1+R2 | R4 + R3（合体自审） | C/D 全作废 |
| 7 | #13 R1 | R4；R3 未遂（用户拦截） | C 作废 |

**2026-08-22 升级处置（用户指令）**：#8-#11 从"部分作废（R1 保留）"升级为**整版无效**（含 R1）——作废单位定为版本；#12/#13 维持 C/D 无效（A/B 即知识/契约段非实验轮次，保留）。

**教训核心**：效率诱惑（主进程直接跑/直接写/合并派发）每次都通向作废——返工成本远高于合规路径。判定独立性与盲注隔离是实验有效性的地基，不可为省一轮派发而妥协。

## 六、版本状态快照（2026-08-22 整版无效升级后）

- **有效完整**：#1-#7（qdrant 3 + weaviate 4）
- **整版无效（待重跑）**：#8 v2.3.22 / #9 v2.6.10 / #10 v2.6.12 / #11 v2.6.16 / #12 v2.6.17 / #13 v2.6.18——milvus 全部六版（各版 A/B 知识契约段可复用）
- 未跑：#14 v2.6.19、#15 v3.0.0
- 重跑要求：全部按本纪律六条红线执行（executor=插件 agent、builder/auditor 分离、盲注隔离、插件 agent 强制）

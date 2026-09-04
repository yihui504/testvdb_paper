# PPT Approach 章节修正设计稿（v3.6 草案，2026-08-29）

**路径说明**：`../../mftui/TestVDB/…` = 主插件仓库（实现在此）；`../../../.claude/plugins/cache/…` = 运行产物（cache 2.3.0）；链接相对本文件（docs/）解析。

依据：v3.1/v3.4 导师意见 + 机制轮收官后的定稿状态（33 chunk / 101 单元 / 701 脚本全部跑完）。
页码标注为 v3.4 版 PPT（49 页）的建议落位；具体页码以你手上的版本对号入座。
每页给出：目的 / 版式 / 逐条内容（可直接抄） / 讲稿提示 / 素材出处。

**v3.6 变更（2026-08-29）**：新约束类别扩为三类（+other 兜底类）；"处理机制闭包"论证入页 5（回应导师完备性质疑）；三类约束补齐完整 agent 管线实战（newcat-pipeline 专项 10 脚本）；红线 3 相应更新。

**全篇红线（先读）**：
1. 全文术语：bug（不写 defect）、behavioral specification、behavioral specification extractor、knowledge
2. 禁用 "novel bug discovery"——语料 33 条 issue 已实锤全系本项目早期上报（author=yihui504），口径为 **independent rediscovery + net-new findings**
3. 三类新约束（resource_bound / doc_consistency / other）可说"设计 + 判据 + 已知答案回放 4/4 + 完整 agent 管线专项实战（10 脚本闭环，NEWCAT_PIPELINE_REPORT）"；**不**说"主数据 35 bugs 含新类别产出"（专项不进 DEFECT 计数）、不说"15 版已批量启用"

---

## 页 1｜全局术语统一（落位 slide 2-3）

- 目的：响应导师 slide 2，一处集中声明，后续页面不再重复解释
- 版式：两列对照表

| 旧表述 | 统一后 |
|---|---|
| defect / defect report | **bug** |
| behavioral claim | **behavioral specification**（规约） |
| claim formalizer | **behavioral specification extractor** |
| raw knowledge（.md） | **knowledge**（raw_knowledge.json） |

- 讲稿提示：一句带过——"内部标识符保持不变，论文与展示层全部用右列术语"
- 素材：checklist §A；论文已同步（65 处替换 + intro 脚注）

**实现与产物**
- 表述名声明：[../../mftui/TestVDB/agents/contract-formalizer.md](../../mftui/TestVDB/agents/contract-formalizer.md)（开头 behavioral specification extractor 声明）
- knowledge 迁移：[../../mftui/TestVDB/scripts/migrate_raw_knowledge.py](../../mftui/TestVDB/scripts/migrate_raw_knowledge.py)
- 术语映射底稿：[FINAL_STATS 同目录](../../../.claude/plugins/cache/testvdb/testvdb/2.3.0/results/qdrant/v1.18.0/FINAL_STATS_RQ1_v34.md)

---

## 页 2｜流水线总览（落位 slide 4-6 任一总览页）

- 目的：更新后的五步管线一张图
- 版式：横向流程图，五个方块 + 关键标注

```
① Knowledge 采集/提取 —— openapi 第一锚 + 版本核对 gate
② Behavioral Specification 提取 —— endpoint/system 分级 + 3 类新约束（含 other 兜底）
③ 分块 + 策略预绑定 —— endpoint 级查表直绑 / system 级场景构造
④ 三视角攻击生成 + gate 预验证 —— oracle 强制 + 4 类机械拦截
⑤ 执行 → 证据链双 agent → 终判 —— 引文逐字预检 + novelty 后置
```

- 讲稿提示：强调"③④⑤全部有确定性脚本/机械门禁，LLM 只负责 ② 的提取与 ④ 的场景生成"
- 素材：mine.md 8a-9a；33 轮实测

**实现与产物**
- 全流程编排：[../../mftui/TestVDB/commands/mine.md](../../mftui/TestVDB/commands/mine.md)（8a 分块 → 8c gate → 8d 执行 → 8e 证据链 → 9 novelty/归档）
- 编排 agent：[../../mftui/TestVDB/agents/orchestrator.md](../../mftui/TestVDB/agents/orchestrator.md)

---

## 页 3｜Step 1：knowledge 采集与提取（落位 slide 11-12）

- 目的：回答导师"为什么先提 knowledge、如何防漏爬错爬"
- 版式：左流程右保障

要点：
- 来源：官方文档全站 + **版本化 openapi 规格**（按 tag 抓取，sidecar 记录版本元数据）
- 结构化：`raw_knowledge.json`（50/50 端点验证；SDK/Docker 信息移出 → deployment_meta 侧车）
- 防错爬三闸：
  1. **版本核对 gate**——openapi 快照与目标版本逐字节核对（实例：v1.18.0 快照曾被 latest 污染为 v1.19，上线首战拦截，复跑清除 5 处污染）
  2. evidence_tier 两档（explicit 须可溯源原文 / inferred 须前缀标注）；纯惯例不收录
  3. description_conflict 打标——prose 与规格冲突当场标记不静默

- 讲稿提示："错误提取不是靠 LLM 小心，是靠三道确定性闸门"
- 素材：fetch_openapi_spec.py（89c717d）、migrate_raw_knowledge.py、规则 2.8

**实现与产物**
- 版本化抓取 + sidecar：[../../mftui/TestVDB/scripts/fetch_openapi_spec.py](../../mftui/TestVDB/scripts/fetch_openapi_spec.py)（`_fetch_qdrant` 按 tag 抓 docs/redoc/v{M}.{m}.x/openapi.json；404 fail-fast）
- knowledge 结构化：[../../mftui/TestVDB/scripts/migrate_raw_knowledge.py](../../mftui/TestVDB/scripts/migrate_raw_knowledge.py)（raw_block 保真；deployment_meta 侧车）
- 覆盖核对：[../../mftui/TestVDB/scripts/validate_doc_coverage.py](../../mftui/TestVDB/scripts/validate_doc_coverage.py)
- 规则 2.8 原文：[contract-formalizer.md](../../mftui/TestVDB/agents/contract-formalizer.md)
- 版本核对 gate 首战记录：[checklist §C](mentor-feedback-checklist.md)（本仓库 docs/）

---

## 页 4｜Step 2：behavioral specification 提取 + 分级（落位 slide 13-14）

- 目的：category 页改纯分类 + 分级落地
- 版式：上分类词表，下分级两列

要点：
- 端点分类固定词表：schema / data / search / index / admin / other（去"标准化"提法）
- **constraint 分级（规则 2.7）**，判据以观测方式为准：
  - `endpoint` 级：单请求内可观测（类型/范围/枚举/必填/响应形状）
  - `system` 级：跨端点或跨请求序列（read-your-write、删除后行为、最终一致）
- 提取时同时生成 **oracle 义务**：每条 specification 即后续脚本的预期行为来源（Step 3 消费）
- 质量数据：v1.18.0 契约 75 端点 / 64 约束 + 22 断言全带 level；lint 对旧契约拦截 58 条缺级

- 讲稿提示：举 exists 反例——"响应形状提取错，三连轮 5+ 脚本假阳性；打上形状 lattice 后零复发"
- 素材：规则 2.7、contract-schema SKILL.md

**实现与产物**
- 分级判据（规则 2.7）+ spec-first（2.8）：[contract-formalizer.md](../../mftui/TestVDB/agents/contract-formalizer.md)
- schema 定义（level required / 六组键含 other_constraints）：[contract-schema SKILL.md](../../mftui/TestVDB/skills/contract-schema/SKILL.md)
- level lint 执行：[bind_strategies.py](../../mftui/TestVDB/scripts/bind_strategies.py) `lint_levels()`（缺级 exit 1）
- 产物契约：[structured_contract.json](../../../.claude/plugins/cache/testvdb/testvdb/2.3.0/results/qdrant/v1.18.0/structured_contract.json)（64 约束+22 断言全带 level）

---

## 页 5｜Step 2+：三类新约束类别 + 完备性回应（落位 slide 14 扩展或 19 后新增一页）

- 目的：回应"约束不止四种类型"，并正面接住追问"凭什么这几类就是全集"
- 版式：三卡片 + 完备性一句话条 + 底部双验证条

**resource_bound（资源边界，system 级）**
- 判据：数值参数 openapi 有 min 无 max → 生成约束"任意规格合法值须被优雅处理（完成/拒绝/文档化错误），不得崩溃或挂起"（三分判据）
- 机械可扫：v1.18.0 规格扫出 **243 处**符合判据——spec 派生约束由 schema 谓词封闭性保证扫尽，不靠分类学
- 立项实证：shard_number=10000（schema 完全合法）打崩服务

**doc_consistency（文档一致性，system 级）**
- 判据：同一参数/默认值在规格与 prose/示例间冲突 → 记录两侧原文，断言 "behavior follows implementation, either side may be violated"（检出冲突只登记不定罪——FP 在生成侧预防）
- 立项实证：indexing_threshold 文档 20000 vs 实现三处一致 10000

**other（兜底类，endpoint/system 均可）**
- 判据：装不进任何已知类的文档承诺 → 入本类不丢弃；**强制 `no_fit_reason` 字段**（为什么装不进——防兜底变偷懒出口）
- 测试路径：绑定阶段先过内置/注册表策略匹配，未命中 → 通用测试原则正反覆盖（同 system 级方法）
- 开类评审触发：other 归因计数非零 → 评审是否析出新正式类别（resource_bound / doc_consistency 即经此路径的先例）

**完备性一句话条（回应"约束仅有这几类"）**：
> **分类可不完备，处理机制闭包**——任意约束必有测试路径（命中绑定走绑定，未命中走通用正反覆盖）；spec 派生约束由 schema 谓词封闭性机械扫尽；prose 派生不宣称完备，35 个实测 bug 归因零残余，新类别按 bug 驱动从兜底析出。

底部验证条一（已知答案回放，2026-08-29）：
> 4 探针打已知案例：2 处矛盾检出 ✓ / 1 阴性对照不误报 ✓ / 1 资源违反成立 ✓ —— **4/4 断言可机械判定**

底部验证条二（完整 agent 管线实战，2026-08-29，专项 10 脚本）：
> other **3/3 bug**（排序承诺——被独立管线完整重现）/ resource_bound **1/4 bug + 3/4 正确阴性**（replication_factor 优雅完成 = 参数相关非类别性误报；shard_number 梯子 =10000 挂起存活不误报 / =uint32 max 服务死亡定罪）/ doc_consistency 冲突检出且侧别归因正确 —— **gate 打回闭环同场实战**（oracle 缺失 REJECT 6/6 → 打回补齐 → 复检归零）

- 讲稿提示：①诚实说明"v1.18.0 主数据轮未启用（不回溯保数据一致），15 版本批量起生效；专项实战为机制验证、不进主 bug 计数"。②如被问"那 other 能不能吃掉那两类"——答：类别 = 断言模板 = 误报预防（三分判据/either-side 语义都是模板给的），也是绑定路由粒度；有确定断言模板或有路由需求的类才值得独立，两者皆无的留 other——边界判据本身可讲
- 素材：规则 2.9、rule29-replay/、newcat-pipeline/

**实现与产物**
- 规则 2.9 判据原文（三类 + other 兜底 + 开类触发）：[contract-formalizer.md](../../mftui/TestVDB/agents/contract-formalizer.md)
- 新组键 schema（六组 + no_fit_reason 字段）：[contract-schema SKILL.md](../../mftui/TestVDB/skills/contract-schema/SKILL.md)
- 消费兼容 + 兜底路径计数：[bind_strategies.py](../../mftui/TestVDB/scripts/bind_strategies.py) `_GROUPS` / `NEW_CATEGORY_TAGS` / `new_category_general_path`
- 归因字段（constraint_category / category_no_fit_reason）：[chain-auditor.md](../../mftui/TestVDB/agents/chain-auditor.md)
- 回放专项（4/4）：[rule29_replay.py](../../../.claude/plugins/cache/testvdb/testvdb/2.3.0/results/qdrant/v1.18.0/rule29-replay/rule29_replay.py) + [报告](../../../.claude/plugins/cache/testvdb/testvdb/2.3.0/results/qdrant/v1.18.0/rule29-replay/rule29_replay_report.md)
- 管线实战专项（10 脚本）：[NEWCAT_PIPELINE_REPORT.md](../../../.claude/plugins/cache/testvdb/testvdb/2.3.0/results/qdrant/v1.18.0/newcat-pipeline/NEWCAT_PIPELINE_REPORT.md) + [契约块](../../../.claude/plugins/cache/testvdb/testvdb/2.3.0/results/qdrant/v1.18.0/newcat-pipeline/structured_contract.json)

---

## 页 6｜Step 3：契约分块 + 策略预绑定（落位 slide 15-16）

- 目的：取消策略匹配环节的落地形态
- 版式：左分块示意，右分流两条路径

**分块（确定性）**：按接口分组、每块 ≤12 可攻单元、字典序稳定；超限切多块（-1of2/-2of2）；33 块覆盖 101 单元全量

**预绑定（bind_strategies.py，0 LLM）**——按 level 分流：
- `endpoint` 级 → 查表直绑：
  - type 类 → 类型边界攻击；range 类 → 边界值攻击（内置基线）
  - 注册表策略须 active 且有战绩才可绑
- `system` 级 → 绑定清单显式置空 → 场景构造路径
- 数据：v1.18.0 实测 30/43 endpoint 级绑定；21+2 system 级显式跳过；lint 拦截 58 条缺级
- **消费语义（D2 v3.5，2026-09-04 插件 2.5.0 起）**：A+B 叠加——绑定约束按清单直生（路径 A），同时**所有约束**（已绑定/未绑定/系统级）一律再走 G1–G10 双向通用覆盖（路径 B）；A/B 双路独立构造=交叉验证，`Attack:` 行标记 `path: A|B` 分账
- **gate 强制**：pipeline_gate 症状④——契约有约束但无 `_strategy_binding` → Stop 拦停（run2r2 曾全程静默跳过 Step 6.5，19+ 轮无绑定后才发现，已作废重跑）

- 讲稿提示：强调"预绑定的价值在分流——确定的方法固化，绑一切等于没绑"
- 素材：bind_strategies.py、_strategy_binding 汇总

**实现与产物**
- 分块：[chunk_contract.py](../../mftui/TestVDB/scripts/chunk_contract.py)（UNIT_SOURCES 四类单元 / ≤12 / -1of2 顺序切分 / 字典序）
- 预绑定：[bind_strategies.py](../../mftui/TestVDB/scripts/bind_strategies.py)（BUILTIN_BASELINE / 三条件筛选 / level 分流 / _strategy_binding 汇总）
- 编排接线：[mine.md](../../mftui/TestVDB/commands/mine.md) Step 6.5
- 产物：[chunks.json](../../../.claude/plugins/cache/testvdb/testvdb/2.3.0/results/qdrant/v1.18.0/chunks.json)（33 块）+ [structured_contract.json](../../../.claude/plugins/cache/testvdb/testvdb/2.3.0/results/qdrant/v1.18.0/structured_contract.json)`._strategy_binding`

---

## 页 7｜Step 3：三视角 attack agents 与覆盖判据（落位 slide 17）

- 目的：导师要的策略清单页
- 版式：三列（每视角一列），底部一条收工判据

| boundary（7 策略） | semantic（7 策略） | state（7 策略） |
|---|---|---|
| 边界值（range） | 行为契约对照 | CRUD-COUNT 一致性 |
| 类型边界（type） | 规约-实现一致性 | DELETE 后一致性 |
| 维度不匹配 | 错误诊断质量 | Upsert 幂等性 |
| 特殊值 | 排序/语义正确性 | 并发操作 |
| 消息质量 | 参数放置/通道 | 事务边界 |
| 资源极限/DoS | 跨端点一致性 | 索引构建期一致性 |
| Malformed/Fuzzing | 生命周期语义 | 生命周期并发 |

**收工判据**：每个 (策略 × 可适用约束) 组合一个脚本 **+ 每条约束的 G1–G10 双向覆盖（路径 B，v3.5 起与绑定状态无关）**，覆盖完收工；无适用目标如实报告；覆盖清单写进脚本 docstring 供统计对账。

- 讲稿提示：数量由覆盖决定（导师要求的删下限已落地）；每脚本强制 Oracle 行（下一步页的伏笔）
- 素材：attack-*.md 三文件策略清单

**实现与产物**
- [attack-boundary.md](../../mftui/TestVDB/agents/attack-boundary.md)（策略 1-7；策略 1 边界值含确定性测试矩阵表）
- [attack-semantic.md](../../mftui/TestVDB/agents/attack-semantic.md)
- [attack-state.md](../../mftui/TestVDB/agents/attack-state.md)（策略 1-7 各带 target 中立代码骨架）
- 三文件共同的预绑定消费段（D2 v3.5：**bound_strategies 非空直按清单生成（路径 A）+ 全部约束普适 G1–G10 双向覆盖（路径 B），叠加不互斥**；A/B 独立构造=交叉验证；system 级 B 呈跨请求序列形态；新类别按类别判据构造）

---

## 页 8｜Step 3 实例：同一块的两条生成路径（新增案例页）

- 目的：用一轮真实数据让"两条路径"可感
- 版式：左右对照案例卡（来源：R22，qdrant points/scroll，3 单元 21 脚本）

**左：endpoint 级（预绑定直生成）**
- 约束："limit 默认 10；启用 strict_mode 时受上限约束"
- 绑定 → 边界值矩阵：min/0/-1/省略/超大逐一实例化
- 战果：**省略 limit 绕过 strict 上限**（显式 6→400，省略→200 返回 10 点）→ bug（vendor 同功能内自相矛盾：query 接口默认值会被上限拦截）

**右：system 倾向（场景构造）**
- 约束："结果按 id 排序；next_page_offset null=末页；order_by 非唯一值不返回 offset"
- 正面：乱序写入 → 全量分页遍历恰为 id 升序；反面：遍历中插入/删除 → 零泄漏零幽灵
- 战果：约束全保（攻击未打穿 = 有效验证）；顺带发现"order_by 模式分页只能走 start_from"

- 讲稿提示：这页回答"预绑定会不会漏掉复杂约束"——不会：复杂约束走右路径（R22 当时为互斥分流；**v3.5 起改为 A+B 叠加，左/右两种形态对所有约束都生成**，交叉验证）
- 素材：summary_r22.md（注：R22 为 2.3.0 代际历史数据，叙事框架按 v3.5 更新，案例事实不变）

**实现与产物（R22 session）**
- session 目录：[2026-08-27T21-15-44Z](../../../.claude/plugins/cache/testvdb/testvdb/2.3.0/results/qdrant/v1.18.0/2026-08-27T21-15-44Z/)
- 左路径脚本：[boundary_scroll_02_strict_mode_max_query_limit.py](../../../.claude/plugins/cache/testvdb/testvdb/2.3.0/results/qdrant/v1.18.0/2026-08-27T21-15-44Z/debate_logs/boundary_scroll_02_strict_mode_max_query_limit.py)
- 右路径脚本：[state_scroll_01_traversal_midwrite.py](../../../.claude/plugins/cache/testvdb/testvdb/2.3.0/results/qdrant/v1.18.0/2026-08-27T21-15-44Z/debate_logs/state_scroll_01_traversal_midwrite.py)、[semantic_scroll_03_orderby_nonunique_pagination.py](../../../.claude/plugins/cache/testvdb/testvdb/2.3.0/results/qdrant/v1.18.0/2026-08-27T21-15-44Z/debate_logs/semantic_scroll_03_orderby_nonunique_pagination.py)
- 证据链与终判：[evidence_chain/](../../../.claude/plugins/cache/testvdb/testvdb/2.3.0/results/qdrant/v1.18.0/2026-08-27T21-15-44Z/evidence_chain/)、[chain_verdicts.json](../../../.claude/plugins/cache/testvdb/testvdb/2.3.0/results/qdrant/v1.18.0/2026-08-27T21-15-44Z/debate_logs/chain_verdicts.json)
- 轮报告：[summary_r22.md](../../../.claude/plugins/cache/testvdb/testvdb/2.3.0/results/qdrant/v1.18.0/2026-08-27T21-15-44Z/summary_r22.md)

---

## 页 9｜Step 4：执行前预验证 gate（落位 slide 27-28，D3b）

- 目的：正面回答导师开放问题"加独立 agent 还是生成 agent 自验"——**都不加，机械层覆盖全部实证失败形态**
- 版式：4 检查类卡片 + 拦截数据条

四类机械预检（脚本投跑前，0 LLM）：
1. **oracle 缺失/退化**——每脚本必须声明可证伪的预期行为行
2. **存活探针错用**——传输失败后拿业务接口当"还活着"的证据 → 拦（假阴性根源）
3. **断言×响应形状冲突**——与规格 lattice 做相容矩阵（含永真断言 WARN）
4. **请求缺必填字段**——与规格必填树比对（anyOf 判别键消歧）

拦截实绩：
- oracle 漏写：改前连续三轮 118 脚本全漏（人工提醒无效）→ gate 上线首轮拦 12 条、此后零漏
- 形状盲：R3 回放揪出 5/12 同款系统性错误写法
- 全程：33 轮 701 脚本，REJECT 工单秒级闭环，误报 0
- 专项复证（2026-08-29 newcat 实战）：新机制块首轮 REJECT 6/6（oracle_missing）→ 工单打回 → 仅补声明行 → 复检归零；WARN 阶梯（oracle 退化）不阻塞随执行边车

- 讲稿提示：severity 阶梯（拦截进打回工单 / 轻微提示不耗预算）+ 旧模式回放护栏（改机制不毁历史数据可比性）
- 素材：gate v4（D3b-R4.0）、checklist §D3b

**实现与产物**
- A/B 类（oracle_missing / transport_probe_wrong）：[_classify_script_errors.py](../../mftui/TestVDB/scripts/_classify_script_errors.py)（`_check_oracle_missing`、锚词正则、三分法）
- C/D 类（形状相容矩阵 / 必填树）：[_preverify_spec_shape.py](../../mftui/TestVDB/scripts/_preverify_spec_shape.py) + 规格索引 [spec_index.py](../../mftui/TestVDB/scripts/spec_index.py)
- severity 阶梯工单：[_apply_script_retry.py](../../mftui/TestVDB/scripts/_apply_script_retry.py)（幂等 / counter / 超限降级）
- 契约物化：[enrich_contract_from_spec.py](../../mftui/TestVDB/scripts/enrich_contract_from_spec.py)（response_shape / required_paths / description_conflict）
- 编排接线：[mine.md](../../mftui/TestVDB/commands/mine.md) 8c 第 7-9 步

---

## 页 10｜Step 5：证据链双 agent 终判（落位 slide 21-22，重写旧 33/34）

- 目的：新架构页（删 4 个 LLM judges、删 dev-reviewer 后的形态）
- 版式：流程图 + 判定规则卡

流程：候选机械提取 → 0-token 初筛（杀 ~90% 历史 FP 模式）→ 1 builder/候选建证据链（文档+执行+源码三证，须逐字引文）→ 引文逐字预检 → auditor 只读终判（四态：bug / 非 bug / 证据不足 / 人工复核）

判定规则卡（E 放宽落地）：
- **明示 by-design 才可否决**——须源码注释/官方声明含意图证据
- "实现如此/无校验/沉默" ≠ 明示 → 走人工复核，不静默筛掉（7 个误筛 TP 的通道已堵）
- FP 判定必须注明证据来源（doc/source/both/behavior）

数据：RQ2 以 71 case 实验集换装新链路，四轮 recall 0.909/0.889（v9 注入口径）
- 讲稿提示：引文预检的成本账——坏引文 1 分钟修复 vs 整轮补证（3 builder + 1 auditor）
- 素材：ADR-0008、chain-auditor.md L168-173、RQ2 v9

**实现与产物**
- 候选提取：[extract_candidates.py](../../mftui/TestVDB/scripts/extract_candidates.py)；L1 初筛：[verify_live_l1.py](../../mftui/TestVDB/scripts/verify_live_l1.py)
- 建链 agent：[evidence-builder.md](../../mftui/TestVDB/agents/evidence-builder.md)（by_design_in_source 口径）
- 引文预检：[verify_chain_quotes.py](../../mftui/TestVDB/scripts/verify_chain_quotes.py)（连续子串逐字比对）
- 终判 agent：[chain-auditor.md](../../mftui/TestVDB/agents/chain-auditor.md)（四态 / 明示 by-design 才 REFUTED / WEAK_REFUTED 走人工）
- RQ2 v9 四轮数据：见 [mentor-feedback memory](../../../.claude/projects/c--Users-11428-Desktop-testvdb-paper/memory/mentor-feedback-v3-4-ppt.md) 与 rq2 系列报告

---

## 页 11｜Step 6：novelty 与归档（落位 slide 22 底部或独立小页）

- 目的：novelty 后置 + 与已报告 bug 的关系（口径页）
- 版式：两段

- novelty 检查后置到提交前最后一步；非 novel 归档不删除
- **已报告 bug 对账（qdrant，正文级）**：35 bugs 中 rediscovery ≈4-6（含早期自家上报的批原子性族），net-new ≈29-31；其中 5 个 bug 的定罪证据完全来自 vendor 自家规格/实现的对照（"vendor 自证型"）
- 口径声明：全部 bug 为 **independent rediscovery or net-new**；GT 注入三重隔离（知识/契约/派发词无 bug 清单）

- 讲稿提示：如被问"和已报告 bug 重复算什么"——rediscovery 恰恰证明管线的召回；net-new 证明增量
- 素材：NOVELTY_GATE_RESULTS.md、FINAL_STATS §六

**实现与产物**
- novelty gate：[novelty_gate.py](../../mftui/TestVDB/scripts/novelty_gate.py)（load_chain_verdicts 分支）
- 正文级对账：[NOVELTY_GATE_RESULTS.md](../../../.claude/plugins/cache/testvdb/testvdb/2.3.0/results/qdrant/v1.18.0/NOVELTY_GATE_RESULTS.md)（42 判词 × 33 issue；归属 author=yihui504 实锤）
- 语料：[qdrant-qdrant.json](../../../.claude/plugins/cache/testvdb/testvdb/2.3.0/../../../../Desktop/testvdb_paper/.paperpilot/phase1-raw/qdrant-qdrant.json)（或 Desktop/testvdb_paper/.paperpilot/phase1-raw/）

---

## 页 12（可选）｜验证规模页（approach 收尾）

- 目的：一句话给 approach 的实证体量
- 版式：大数字条

> 1 个真实目标系统（qdrant v1.18.0，33 块）· 101/101 规约单元 · **701 攻击脚本** · 135 条证据链 · **35 bugs**（12 个根因族；13 个可直接定罪）· 管线候选→bug 收敛率 22.4%

- 讲稿提示：声明这是单版本深度验证；多版本广度与跨工具对比见实验章节（in progress）
- 素材：[FINAL_STATS_RQ1_v34.md](../../../.claude/plugins/cache/testvdb/testvdb/2.3.0/results/qdrant/v1.18.0/FINAL_STATS_RQ1_v34.md)
- 聚合脚本与逐轮出处：33× [summary_rN.md](../../../.claude/plugins/cache/testvdb/testvdb/2.3.0/results/qdrant/v1.18.0/)（R1-R33 session 目录）

---

# 旧页处置对照表

| 旧页 | 处置 |
|---|---|
| slide 12（raw knowledge 提取，补） | → 页 3 重写 |
| slide 13/14（category"标准化"） | → 页 4 改纯分类 + 分级 |
| slide 17（策略） | → 页 6+7 重写（预绑定 + 清单） |
| slide 21/33/34（旧四-judge 确认流程） | **删除**，→ 页 10 重写 |
| slide 19（分级意见所在） | → 页 4+5 承接 |
| slide 28（oracle 开放问题） | → 页 9 承接（结论：不加 agent） |
| slide 36/46（测试后检验） | → 页 10 判定规则卡承接 |
| slide 45/47 数字（45TP/26FP） | 统一 44/27（属 results 章节，随数据页一起改） |

# 尚未定稿、本章节不要写的

1. 多版本对比数字（15 版批量未跑）
2. RQ3 vs VDBFuzz 任何数字（未开跑）
3. "主数据 35 bugs 含新约束类别产出"（newcat 实战是专项机制验证，不进 DEFECT 计数；可引用 NEWCAT_PIPELINE_REPORT 的 10 脚本结果但须注明专项性质）
4. "novel"字样（口径已定：independent rediscovery）

# run2 重跑运行报告（qdrant v1.18.0，R1-R9，2026-08-24/25）

> 会话：ADR-0009 新规范轮（删 vein + 两阶段调度 + exploratory 通道 + confirm_per_round）。
> 本报告为用户指示的暂停点运行总结：产出 / 遇到的问题 / 建议解决方案 / 待优化的点。
> 过程全留痕：docs/ops-prompts-run2/run2r-01-qdrant-v1.18.0.txt（B1 起逐事件）。

---

## 一、产出

### 1.1 九轮闭环总账

| 轮 | 块 | 脚本 | 候选 | strict | exploratory | rejected |
|---|---|---|---|---|---|---|
| R1 | aliases+update | 28 | 7 | 3 | 0 | 4 |
| R2 | collections+create-1of2 | 46 | 14 | 5 | 0 | 9 |
| R3 | collections+create-2of2 | 35 | 11 | 8 | 0 | 3 |
| R4 | collections+delete | 11 | 5 | 1 | **1（首例）** | 3 |
| R5 | collections+exists | 9 | 9 | 0 | 6 | 3 |
| R6 | collections+get | 10 | 1 | 0 | 0 | 1 |
| R7 | collections+update | 13 | 3 | 0 | 1 | 2 |
| R8 | chunk_global（3 不变量） | 14 | 0 | 0 | 0 | 0 |
| R9 | index+create | 9 | 3 | 1 | 0 | 2 |
| **计** | **9/32 块** | **175** | **53** | **18** | **8** | **27** |

- **175 脚本全部真实执行**（R1 五轮穿透后统一口径；exit↔VERDICT 严格对齐）
- **Pre-Submit Gate 全 REPRODUCED**：R1 2/2、R2 25 检查全过、R3 三簇、R4、R9（G1/G2/G3）
- **R8 阴性基线**：全局生命周期语义（read-your-write / delete-gone / cascade / 别名名字释放）数据面全过——后续版本对照的阴性参照

### 1.2 确认缺陷 18 项（strict_defect，全部 gate 复现）

| 主题族 | 数 | 缺陷编号 | 核心现象 |
|---|---|---|---|
| batch 失败原子性 | 3 | 1-3 | 404 拒绝的 batch 残留有效 action 别名（for 循环 `?` 早退无回滚，collection_meta_ops.rs:298-338） |
| uint8 越界静默饱和 | 3 | 4/5/7 | dense uint8 `x as u8` 饱和（-1→0.0、≥255→255.0、12.7→12 截断）vs sparse 侧显式 clamp——dense/sparse 处置不对称 |
| wrong-dim 200-ack | 2 | 6/8 | wait=false WAL 入队 200 + 应用期异步丢错（含混批部分应用） |
| indexing_threshold 文档漂移 | 3 | 9/11/14 | 文档默认 20000 vs 实现物化 10000（qdrant 文档内部自相矛盾，实现三处自洽） |
| inline_storage 耦合静默 | 4 | 10/12/13/15 | 耦合违反配置 200 持久化（warn+ignore 设计，警告仅在 describe.warnings，create 零提示） |
| 别名删除不对称 | 1 | 17 | via-alias DELETE 200 零变更（读路径 resolve_name vs 删除路径字面名） |
| churn describe 500 | 1 | 16 | churn 窗口 "0 of 0 read operations failed" 空副本集→500 非 503 |
| field_schema 数组规约 | 1 | 18 | `['keyword']` 数组 200 受理 + 回读规约（serde struct-from-seq 宽容解析） |

### 1.3 exploratory 候选 8 项（通道产出）

- doc-gap 族 ×6：exists 响应形状分歧三确认、R5 churn/别名关联记录 ×2、诊断梯度、absent 语义族分裂（R4 首例）
- behavioral_anomaly ×1：metadata "{} 清除" 实现 no-op（契约零锚，doc-as-ground 翻案权留人工）
- 关联记录 ×1（R5 05/06 与 defect-16/17 去重处理）

### 1.4 新机制首次实战验证（ADR-0009 设计的实证）

| 机制 | 实战表现 |
|---|---|
| **exploratory 通道** | 首例（R4 state_01 doc-gap）→ 批量（R5 六案）→ 累计 8 项；三条件判定在灰区块运转正常 |
| **机械 B（物理规则）** | R4 首次实战触发（HTTP 语义 ×3）→ **auditor 第四查域裁量 3 次正确降级**（断言无文档地基/spec 反证/锚错位——防伪 DEFECT）；R9 灰区兜底正判 1 真缺陷 |
| **A=CONFLICT 冲突路径** | R4 state_01 首走（打回→补证→复审→exploratory）闭环验证 |
| **两阶段调度** | 9 轮均 enum 模式（块未耗尽、无平台期）——切换条件未触发，探索模式待后续块验证 |
| **删 vein 后三 attack** | 产出结构正常（boundary/state/semantic 三视角策略分化良好）；R4 小单元块的合并派发模式验证成立 |

### 1.5 产物盘点（SESSION_DIR = cache/.../2026-08-24T12-37-33Z/）

- defects/defect-1~18.md（18 份，四 Ring 完整，gate 全 PASS）
- mre/defect-{1..16}-script.py（16 份，实测复现；17/18 挂账）
- presubmit_gate_r{1,2,3,4,9}.py（全部执行 REPRODUCED）
- chain_verdicts_r{1..9}.json（判定权威）+ evidence_chain/ 53 链
- summary_r{1..9}.md（逐轮）+ 执行 log 175 组 + analyzed_documents×3
- 派发词与事故全存档（run2r-01-qdrant-v1.18.0.txt，~400 行）

---

## 二、遇到的问题（按层分类）

### 2.1 环境层
| # | 问题 | 影响 | 状态 |
|---|---|---|---|
| E1 | CLAUDE_CODE_MAX_OUTPUT_TOKENS=6000 截断（auditor 大 JSON/大 Write） | R1 auditor 单次被杀；主进程大 Write 失败 ×2 | **已修**（16000，新会话生效后零复发） |
| E2 | agent 工具注入间歇故障（无 Write/Bash） | B1 12 段回传、R9 Reporter 无 Bash（gate PENDING） | 未根治；分段回传协议兜底 |
| E3 | 主进程重启 ×2 | R9 生成 agent 中断（9 脚本幸存）；旧 agent 名失效 | 恢复流程验证可行 |
| E4 | Docker preflight 误报 not running（实际存活） | 无实害 | 记录 |

### 2.2 执行层（executor）
| # | 问题 | 影响 | 状态 |
|---|---|---|---|
| X1 | 环境变量两层缺失（SCRIPTS_DIR/TARGET） | R1 五轮穿透之首两层 | **已固化**（四件套写死派发词） |
| X2 | 容器半死 ×2（dos 残留/10 万 actions 载荷） | 连带 8+7 脚本 setup 超时 | restart+清残留；dos 类脚本标记容器杀手不重跑 |
| X3 | log 落位漂移（R3 写进 debate_logs） | 候选提取漏 11 | **已固化**（落位写死派发词） |
| X4 | 脚本↔log 编号错位 ×4（R2） | builder 内容重配对 | R3 起抽查核对（后续零复发） |
| X5 | 聚簇规则误停（DF 类聚簇=单单元块预期） | R5 多一次往返 | **已细化**（SE 类停/DF 类抽查放行） |

### 2.3 脚本层（attack 生成质量）
| # | 问题 | 频次 | 模式 |
|---|---|---|---|
| S1 | 脚本 bug（unhashable dict / 格式串参数计数 / query 形态错 / timeout 放 body） | 4 类各 1 次 | SE 停批+修复环闭环；AST 扫描可预防格式串类 |
| S2 | 客户端伪象（requests 点段折叠制造 `.`/`..` 200 假 DF） | 1 | builder 抓线三重互证拦截（第 4 查深水样本） |
| S3 | 判读粗糙（2xx 一律当 acked、isinstance 误触发） | 2 | 响应体布尔位消费纪律已进 reflection |

### 2.4 runtime 层（共享脚本库）
| # | 问题 | 影响 | 状态 |
|---|---|---|---|
| R1' | list_aliases 路由 bug（/collections/aliases→404 假象） | 3 个假 DEFECT 作废申报 | **已修**（agent 诚实申报非静默） |
| R2' | query 通道缺失 | timeout min=1 线索无法脚本化 | **已补**（R4 agent 顺手 request(query=)） |

### 2.5 判定层（契约资产与规则边界）
| # | 问题 | 频次 | 状态 |
|---|---|---|---|
| J1 | 契约提炼失真 | **5 项**（sharding 枚举大小写 / absent 子句无地基 / exists 响应形状 / metadata 语义未提断言层 / describe consistency 参数） | 挂账 D 段——formalizer 系统性改进项 |
| J2 | Type2 诊断主张无契约锚 | 3 例（R2/R5/R7 先例一致） | 一致拒绝（纪律稳定） |
| J3 | interface-parity 信号被 §5 条件③挡（机械 REFUTED 定案案不入通道） | 1 例（R9 timeout 跨面不一致，实质证据） | **通道边界设计冲突首例**——待拍板 |
| J4 | doc-as-ground 翻案权（metadata 案契约零锚） | 1 例 | 留人工（R7 semantic_02） |
| J5 | 工具链 schema 过时：ai_failure_check M4 硬编码旧架构文件名 / M5 正则不容 markdown；verify_defects 静态 FP 标记（12 CONFIRMED/3 FP/1 NI——3 FP 与 gate 复现矛盾，静态审查器保守误标） | 3 项 | 挂账修 |
| J6 | builder quote 拼接形式致机械 A quote_mismatch | 2 案 | 挂账规范化 |

---

## 三、建议解决方案

### 3.1 待用户拍板的判定决策（D 段人工复核清单，合并前几轮挂账）
1. **by-design 抗辩 4 簇**：R1 原子性（doc-comment "atomic"=隔离 vs 回滚 + 维护者"不保证原子"锚点）/ R2 wait 抗辩（200-ack=WAL 语义）/ R3 indexing doc-stale（文档缺陷 vs 服务端缺陷定性）/ R3 inline 软硬读法——全部"机械定案+抗辩留痕"形态，需人工最终定性（影响 12 项 defect 的提交口径）
2. **interface-parity 另立**（J3）：建议以面间不对称为主张重新派发单案（collections vs index 的 timeout 校验）——不经审计兜底，走正规挖掘路径
3. **doc-as-ground 翻案**（J4）：metadata "{} 清除" 案是否以文档明文为锚翻 DEFECT——建议翻（openapi 原文明确，链完整源码定位），翻后 strict 18→19
4. **verify_defects 的 3 个静态 FP 标记复核**（gate 已复现背书，预期维持 CONFIRMED）

### 3.2 工具链修复（小改动，建议下轮启动前批量做）
1. ai_failure_check：文件名模式改 `chain_verdicts_r*.json.done` 兼容；M5 正则容 markdown 粗体
2. builder 规范：assertion_text_quoted 禁止拼接括号注记（R4 两案 A=NEUTRAL 根因）
3. attack 规范统一化：bootstrap 三层 fallback（env→向上遍历→契约读 target）写进三个 agent 规范（R1 事故根因）
4. executor 派发模板固化：四件套 + 落位 + 聚簇细化版 + 脚本名对应抽查（本报告期间已沉淀，写入 orchestrator.md 8d 节）

### 3.3 契约层改进（formalizer 提取质量，J1 五项的系统解）
- spec-first 提取：枚举值域/响应形状/参数面以 openapi.json 为第一锚（prose 仅次级）——五项失真全部是 prose 优先所致
- 参数表描述升级断言层：metadata merge 语义类在 api_endpoints.parameters 里但无 constraint_id（R7 零锚根因）
- 版本核对：.sourcedeps openapi 存在高于目标的漂移（R9 发现 memory/prefix）——提取时需 tag 核对

---

## 四、待优化的点

1. **novelty gate 未跑**（D1 属全轮次收口）：18 项 strict 的 NOVEL/COVERED_BY_PR/UNVERIFIED 分类待 32 块全完后统一——RQ1 yield 数据（"发现已被报告 bug"列）依赖此步
2. **MRE 挂账**：defect-17/18 两案（与 D 段批量补齐）
3. **dos 类脚本隔离执行**：容器杀手模式（10 万 actions 打挂共享容器）——建议专用容器或限流参数（待 ADR-0009 探索模式的批量探针同样受益）
4. **探索模式未验证**：9 轮全 enum（块未耗尽）——8a.5 切换条件与 8b-expl 四算子的实战验证待后期块（大块如 points+upsert 拆 2 块后可能出现块耗尽）
5. **节奏与预估**：稳态 ~1.2h/轮（R1 事故轮 9.5h 除外）——剩 23 块（含 points 系大块）预计 2 个工作日
6. **GT 对账未做**（属 D 段）：本轮 18 strict 与 GT（9039/9045 两案）的 reach 对账 + 44 bug 全局视角的对账在收口统一做
7. **容器状态**：当前保留运行（内存 ~200MB，无残留集合）——若隔多日再跑建议 `docker stop testvdb-qdrant-standalone`（保留容器，下次 start 即恢复）

---

## 五、下一步（恢复点）

- 位置：R10 = chunk_index+delete（第 10/32 块）
- 恢复 SOP：容器 start（若停）→ healthz 200 → R10 三视角派发（reflection_context 从 summary_r9 取）→ 标准流水
- 全部上下文在：run2r-01-qdrant-v1.18.0.txt（事件级）+ summary_r{1..9}.md（轮级）+ 本报告（会话级）

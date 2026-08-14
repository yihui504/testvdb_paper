# v2 材料包深入审核报告（第二轮）

> 日期：2026-08-14。对象：tvdb_sessions v2 材料包（71 session + 6 个 intelligence 文件 + 15 个版本契约）。
> 方法：① 确定性审核脚本 `audit_materials_v2.py`（9 维检查）；② 3 个并行内容抽查 agent
> （milvus 43 / qdrant 18 / weaviate 10 session 全查）。
> 结果：发现 6 类问题，已修复 116+10+2 处；确定性审核最终 0 FAIL / 0 WARN。
> 实验纪律已单独成文 [phase2-experiment-discipline.md](phase2-experiment-discipline.md)。

## 1. 发现与修复

### 1.1 related_issue_numbers 含样本号（71/71）——GT 泄露通道（FAIL）

v2 包每个 stage2_aggregation 的 `related_issue_numbers` 都带着自身真实 issue 号。
SOP 解禁 github.com（第 3.5 步 WebFetch 回退），匿名 defect_id 挡不住这个字段：
dev-reviewer 拿到 `related_issue_numbers: [47635]` 就能 WebFetch issue 页，
而我们的 issue 是**历史 issue**（maintainer 状态已定 = GT）——真实 TestVDB 里 issue 是新挖的、
状态未定，此通道不存在。**这是实验特有泄露**。

修复：71 个全部置空 `[]`。真实流程中 attack 输出的 related_issue_numbers 是内部编号，
置空不偏离形态。同步修 `build_materials_v2.py`（源头置空，防止重建复活）。

### 1.2 qdrant 1.18.3 契约含实验元数据（FAIL）

- 每个 endpoint 条目的 `_provenance_runs`（phase1 构建溯源，真实契约无此字段）
- `_note: "v2.5.2 手工补 — contract-formalizer 漏提取（C+D 实验失败根因）"`（实验失败分析）
- generation 块 `"3 independent runs: run1/run2/run3"`（两处，第一轮只修到顶层一处）

修复：全部删除/归一。同步修 `build_materials_v2.py` 加 `clean_contract()`（重建时自动清理）。

### 1.3 output log 裸 issue 号（8 个，WARN→修复）

8 个 milvus output log 的集合名/别名含裸号（无 # 前缀，第一轮 `#NNNN` 扫描抓不到）：
`repro_47729`/`test_47763`/`alias_50018` 等。与 1.1 同理是 GT 泄露通道。

修复：裸号替换为 `<tracked>`（与 intelligence 清洗同占位符），payload/响应内同步替换，
替换后 JSON 结构合法（抽查 agent 逐行验证）。

### 1.4 raw_*.log 中间产物残留（6 个）

fill_raw_v2.py 生成的 raw_*.log 已转换进 output_*.log（=== REQ/RESP === 格式），
raw 文件是冗余中间产物，session 目录形态应为单一 output_*.log。

修复：删除 6 个；fill_raw_v2.py 改为转换后自动删。

### 1.5 weaviate bug_shapes BS-004 与样本标题逐字（GT 泄露）

BS-004 的 `symptom_pattern` = weaviate_009（11981）issue 标题逐字截断——
"考题在复习资料里"（audit-report 坑 9）的残余。第一轮 intelligence 清洗只处理
`#NNNN` 引用和 known_instances 列表，没处理 symptom_pattern 里的标题文本。

修复：symptom_pattern 泛化为抽象模式（v2 包 + intel/ 源两处同步）。
全量交叉检查（6 个 intelligence 文件 × 71 样本标题，45 字符窗口 LCS）0 命中，无其他残余。

### 1.6 fill_raw 重放场景错误（3 case，进行中）

内容抽查发现 fill_raw_v2.py 的重放与 issue 声称缺陷不符（三方比对修正 stage2 标签后
fill_raw 没跟着改）：

| case | 原重放（错） | 新重放（对） |
|---|---|---|
| milvus_004 (47755) | delete filter='123'（被正确拒绝，展示相反证据） | delete filter='age in [10, 5]'（降序 range，issue 声称被接受） |
| milvus_007 (47767) | drop 不存在的 database（与 entities+search 标签矛盾） | search data=[[]]（空查询向量，issue 声称无校验） |
| milvus_040 (52313) | 原探针 log 全 408（容器争用时代产物，无可用证据） | REST insert JSON 字段纯字符串（3.0.0 重放） |

已改 fill_raw_v2.py，用 2.6.10 / 3.0.0 活容器重放完成（2026-08-14）：
- 47755：delete filter='age in [10, 5]' → code 0、deleteCount=1（降序 range 被接受，缺陷复现）
- 47767：search data=[[]] → code 1801 正确拒绝（与 entities+search 标签一致；C 组 FP 如实记录）
- 52313：REST insert JSON 字段纯字符串 → code 0、insertCount=1（被接受，缺陷复现；旧 408 日志替换）
重放期间发现 milvus 2.6.10 容器启动必须用 orchestrate.py 实测配方
（外部 etcd+minio + `ETCD_USE_EMBED=false` + `DEPLOY_MODE=STANDALONE`，
embedded etcd 在该版本已不可用——旧 containers.py 配方失效，已不采用）。
fill_raw 集合命名同步改为匿名序号（repro_<did序号>），防止下次重建再带入裸号。

## 2. 内容抽查中"未复现"结论的分类

3 个抽查 agent 报了若干"缺陷表现未复现"case，按性质分类：

- **C 组 case（qdrant 9255/9371/9373/9523 等）**：C 组 GT 本就是 FP（by-design / not-repro），
  材料如实记录"正确行为"，dev-reviewer 判 FP 即正确。**非材料问题**。
- **milvus_031 (50355)**：探针报错路径（dynamic schema 1804）≠ issue 声称（autoID 语义），
  但材料如实记录；dev-reviewer 干净复现会重建最小请求。保持。
- **9149（qdrant_005，A 组）**：log 显示 shard_number=0/-1 被正确拒绝，与 issue 声称相反。
  audit-report §2 已判定 9149"bug 在版本范围不复现 → GT 噪声"，本次抽查再次实证。
  **A 组 GT 标签存疑再次浮现，处置待用户决定**（不改材料，改不改 GT 由用户定）。
- **milvus_001 (47635)**：空日志已知例外（2.3 无 REST v2），audit-report §5.5 已披露。

## 3. 审核后的确定性验证

`audit_materials_v2.py`（结构完整性 / stage2 形态 / 19 处标签修正生效 / 匿名一致性 /
泄漏词+样本号+裸号扫描 / related_issue_numbers / intelligence 零残留 / 版本契约 /
三树↔v2 一致性 / 空日志检查）：**0 FAIL / 0 WARN**。

## 4. 材料修复记录

MATERIAL_FIXES.json 追加（25 → 160 条）：
- FIX_RELATED_ISSUE_NUMS_V2AUDIT ×71
- FIX_CONTRACT_METADATA_V2AUDIT ×4（_provenance_runs×N、_note、generation×2）
- FIX_LOG_BARE_ISSUE_NUM_V2AUDIT ×8
- FIX_DROP_RAW_INTERMEDIATE_V2AUDIT ×6
- FIX_INTEL_SYMPTOM_PATTERN_V2AUDIT（BS-004，另留记录）
- 三树与判词文件零改动（修输入不修输出原则）

# fixH 报告：M1 残留断言修复 + milvus 对照翻错定责验证

> 日期：2026-08-16。Run 标识：**fixH**。预注册 FIXH_PLAN.md（跑前 commit e43a0e2）。
> 干预：fix_contract_residual.py 修复 001（幂等消歧，6 版本 12 处）+ 002（去
> duplicate-rejection，5 版本 10 处）；MF 175；audit 0 FAIL。判据=M1 同源（源码意图
> 常量+注释+实测），独立于 GT；文档核验不可达已如实记录。
> 子集 4：定责验证 022 + 观察回漂 026 + 回归 031 + 对照 025（milvus 2.6.17 串行）。

## 1. 预注册判据结果

| case | GT | fixG | **fixH** | 判定 |
|------|-----|------|------|------|
| milvus_022（定责） | FP | C✗ | **F ✓** | **PASS**——残留断言定责成立 |
| milvus_026（观察） | FP | C✗ | C✗ | 记录——归因改变（见 §2.2） |
| milvus_031（回归） | TP | C✓ | F✗ | **字面 FAIL**——判词级因果排除（见 §2.3） |
| milvus_025（对照） | FP | C | C | 漂移带维持——暴露同族新断言问题（见 §3） |

## 2. 核心发现

### 2.1 022 翻错已解决：残留断言=根源，材料同向后消费稳定

fixH 判词（F，conf=0.98）：三条 create 契约断言**同向消费**（001 修复版 + 002 修复版 +
M1 的 invariant_001）+ 源码接地直击 `errIgnoredCreateCollection` 与 schema Equal 比较
（create_collection_task.go:522-540 → root_coord.go:903-907）+ 双路径证伪（同 schema 200 /
不同 schema 65535）。与 fixE 007（契约方向反转解除锚点-契约内战）完全同构。
**结论：fixG 022 翻错的根源=M1 残留断言，修复有效，fixH 并入最终配置。**

### 2.2 026 未回漂但归因改变：现象焦点漂移（材料侧不可修）

026 三轮现象焦点：fixA 轮=strictGroupSize / fixG=consistencyLevel 顶层 / fixH=**dbName
默认值**（"_default" vs "default"）。fixH 判词**显式消费 C 锚点**判 C——且其发现的
dbName 不一致是真实存在的（契约 "_default" vs 源码 `DefaultDbName="default"`，实测
"_default" 报 800）——即 012 邻域真现象。**026 的错向源于候选现象定义的多焦点让
reviewer 会话间自选现象**，非断言/锚点材料缺陷，无法以材料修复解决；只能论文披露
（候选定义的会话方差）。

### 2.3 031 回归字面 FAIL + 因果排除：翻正本身也是现象聚焦依赖

fixH 判词（F）审的是 031 的**次要子现象**（enableDynamicField=false 拒绝额外字段——
upsert 端点），fixG 轮审的是主现象（autoID upsert 失败）。被修断言（collections/create
的 001/002）与 031 现象端点无关、判词未引用——**因果排除：非修复伤害，是现象焦点漂移**
（同 026 机制）。处置：fixH 修复保留；031 字面 FAIL 如实披露 + 因果排除论证（同
fixD 015 / fixE 018 先例）。**深层含义：锚点翻正复合现象 case 的效果取决于 reviewer
锁定主现象的概率——031 在 fixG（主现象+C 锚点消费）翻正、fixH（次现象）翻错，翻正
不是确定性的。**

### 2.4 025 暴露同族新残留断言（待批）

判词消费 `milvus_range_entities_insert_001`（max 100 entities）——该断言与 50324 调查
证据冲突：yihui504 在 50324 自证 **v2.6.x 文档并无 entity count 上限**（v1 旧文档才有）+
源码无校验（handler_v2.go:1267 直接赋值）+ 实测 200/500 均成功。独立证据链齐全
（公开 GitHub 评论 + 源码 + 实测），同 formalizer 过时/发明断言族。**未修**（超出 fixH
预注册范围），呈用户拍板是否修后并入 fixF。

## 3. 处置

- **fixH 修复保留**（并入最终配置）；022 定责闭环。
- 026/031 的现象焦点漂移=候选定义问题，无法材料修复，论文披露；fixF 全量将量化其影响。
- 新待办（待批）：`milvus_range_entities_insert_001` 断言修复（v1→v2 过时上限）。
- fixF 现在可跑：最终配置 = fixA 锚点 + qdrant 13 锚点 + C/G 锚点 + 契约修复
  M1/M2/Q1/Q2 + **001/002 残留修复（fixH）** + 原版 SOP。

## 4. 归档

判词 `fixH/verdicts/`（4）；voided 空；fix_contract_residual.py + pre_contract_backup/；
MATERIAL_FIXES 175；audit 0 FAIL；容器全清；dispatch_log 4 行。

# fixH 计划：M1 残留断言修复 + milvus 对照翻错定责验证（预注册，跑前 commit）

> 日期：2026-08-16。Run 标识：**fixH**。来源：fixG milvus 稳定对照 022/026 双翻错
> （F/F/F→C），定责链=cognition_match 均为 fixA 锚点宽泛匹配 + 022 视角 A 消费残留旧断言
> `milvus_state_collections_create_001`（FIXG_REPORT §3）。
> 目的：消除材料内战残留（契约树同现象两条断言方向相反），验证 022 翻错是否由此定责。

## 干预（契约修复补丁，fixE M1 的补全）

| 断言 | 现文本（问题） | 修复后 |
|------|--------------|--------|
| `milvus_state_collections_create_001`（6 版本） | "collectionName is unique within dbName"——unique 语义本身正确，但与 002 组合被解读为"duplicate create 必须拒绝" | 保留 unique + 幂等消歧："re-creating an existing collection with the SAME schema is an idempotent no-op returning 200; with a DIFFERENT schema returns an error" |
| `milvus_behavioral_collections_create_002`（5 版本） | "returns 400 on invalid parameters **or duplicate name**"——与 M1 修复方向直接冲突 | "returns 400 on invalid parameters; duplicate name with same schema returns 200 (idempotent no-op), with different schema returns 400" |

**判据（独立于 GT）**：与 M1 同源——errIgnoredCreateCollection 专用常量 + root_coord.go
"create existed collection with same schema, ignore it" 注释 + 实测同 schema 200（fixE/fixG
两轮判词 Step1 均复现）。002 与 M1 已修的 invariant_create_duplicate_001 描述同一端点同一
现象，断言间方向一致性是材料质量要求（fixE 007 先例：契约方向反转后锚点消费稳定）。
文档核验不可达（milvus.io API reference 不在 milvus-docs 仓库，v2.6.x 分支无 restful 目录），
如实记录；M1 修复时判据同为源码意图+实测，未依赖文档原文。

## 重判子集（4 case 单轮，milvus 2.6.17 容器串行 031→022→026→025）

| 槽位 | case | GT | fixG | 期望 |
|------|------|-----|------|------|
| 定责验证 | milvus_022 | FP | C✗ | **F**（残留断言定责成立）；仍 C=定责不成立（fixA 宽泛匹配主导）|
| 观察回漂 | milvus_026 | FP | C✗ | F=自然回漂（好）；C=记录（enum 断言+fixA 匹配，独立问题）|
| 回归 | milvus_031 | TP | C✓ | **C**（C 锚点适用不得被伤；F=FAIL）|
| 对照 | milvus_025 | FP | C | 任意（基线 C/C/F 漂移带；其 len<=100 断言未动）|

## 处置树

- 022→F 且 031→C：残留断言=翻错根源，C 锚点疑点大幅缓解（材料同向后消费稳定），
  fixH 修复并入最终配置 → fixF。
- 022 仍 C：残留断言定责不成立 → fixA 锚点宽泛匹配主导；选项：a) 收窄 fixA 锚点措辞
  （风险：fixA 效果 10:3 良好，动锚点=新干预）b) 接受并如实披露（灰区轮方差带）→ 呈用户拍板。
- 031→F：修复伤及 C 锚点适用类 → FAIL，回滚 fixH 修复，022/026 翻错按灰区漂移披露。

## 披露义务

- fixH 为契约修复（源码判据，独立于 GT），与 fixE M1 同性质，须披露"补全 M1 未覆盖的
  同簇断言"这一来源（发现路径=fixG 对照翻错判词，事后定位——如实写）。
- 重判单轮 + 轮方差 caveat 同前。

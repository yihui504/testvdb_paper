---
name: configure
description: "给已有 .tex 的 LaTeX 论文同步 .self_xept/project.yml——从论文反向推断 documentclass/title/main_file/language 等字段（**venue 除外**——它是投稿目标，由作者或 xept:setup-venue 设；configure 不从 \\documentclass 推断 venue，避免模板类型覆盖投稿意图破坏下游会议标准），论文是 source of truth、config 跟着走，幂等可重跑，不动论文文件、不发明作者元数据。用户要\"配置已有论文\"/\"同步 project.yml\"/\"把现有论文接入 xept\"时调用。新论文从 CFP 前向配置用 xept:setup-venue。"
---

# Configure（存量论文反向接入配置）

> **实现**：`scripts/infer_paper_meta.py` + 单测（见 §配套）。设计依据：[docs/improvement-plan.md](../../docs/improvement-plan.md) P4-2 + 路线 B plan + [docs/conventions.md](../../docs/conventions.md) §5 分层配置。

## 核心原则

**论文是 source of truth，`.self_xept/project.yml` 跟着走。**

configure 扫描已有 `.tex`，把 paper-derivable 字段同步进配置；不复制模板、不动论文文件、不发明作者元数据。幂等——同一动作处理"缺失/不完整/漂移/一致"四态，已一致则 no-op。

## 何时用 / 何时不用

**用**：
- 项目已有主 `.tex`（含 `\documentclass`）但无 `.self_xept/project.yml`
- 有 project.yml 但和论文漂移（venue 不符 `\documentclass`、title 陈旧、main_file 指向空）
- 论文变了（换 venue、重命名 main.tex、加 sections/ 目录），要 resync 配置
- 用户说"配置我的已有论文"/"同步 project.yml"/"把现有论文接入 xept"

**不用**：
- 全新项目无 `.tex` → [xept:setup-venue](../setup-venue/SKILL.md)（从 CFP 前向配置 + 模板）
- 配置已和论文完全一致 → no-op，用别的 skill
- 想抓 CFP 要求（页数/截止/匿名） → [xept:setup-venue](../setup-venue/SKILL.md)（configure 不抓 CFP，只从 `.tex` 反推）

## 与 setup-venue 的边界

| skill | 数据源 | 方向 | 场景 |
|---|---|---|---|
| [xept:setup-venue](../setup-venue/SKILL.md) | CFP URL / 文档 / 用户描述 | 前向（要求 → 配置） | 新论文，要页数/截止/模板 |
| **xept:configure** | 已有 `.tex` | 反向（论文 → 配置） | 存量论文，只要 venue/title/结构 |

两者都写 `.self_xept/project.yml`，互补不冲突：configure 同步论文派生字段，setup-venue 补充投稿要求字段。

## HARD-GATE

<HARD-GATE>
configure 结束时 `.self_xept/project.yml` 必须存在且可解析。若 YAML 损坏无法解析 → STOP，报告错误，**不猜结构、不静默重写**。下游所有 skill（write-paper / mock-review / fix-latex）读它取 venue / 文件布局 / 结构。
</HARD-GATE>

## 流程

### Step 1: 确认主 .tex
跑 `python scripts/infer_paper_meta.py <项目根或 main.tex>` 扫描：
- **exit 0**（单候选或指定单文件）→ 该 .tex 是主文件，进 Step 2。
- **exit 2**（目录多候选，输出 `{"candidates": [...]}`）→ 问用户哪个是文档根，选定后用**单文件**重跑 `infer_paper_meta.py <选定的 .tex>`，不自动猜（错误猜测比不猜更糟）。
- **exit 1**（无 `\documentclass` / 不可读）→ 不是存量论文，建议 [xept:setup-venue](../setup-venue/SKILL.md)，停。

### Step 2: 扫描论文（source of truth，先不写）
跑确定性扫描器（[conventions.md](../../docs/conventions.md) §1 务实混合——扫描是确定性 I/O + 查表，脚本化；合并/报告留 prompt）：

```
python scripts/infer_paper_meta.py <main.tex 或项目根>
```

**JSON 输出契约（脚本必须遵守）**——**注意：无 `venue` 字段**：
```json
{
  "main_file": "string (REQUIRED)",
  "documentclass": "string (REQUIRED)",
  "title": "string (REQUIRED, 找不到 → \"\")",
  "language": "string (REQUIRED, \"chinese\" 或 \"english\")",
  "sections_dir": "string (OPTIONAL, 找不到 → \"\")",
  "figures_dir": "string (OPTIONAL, 找不到 → \"\")",
  "bibliography": "string (OPTIONAL, 找不到 → \"\")"
}
```

**venue 不从 `\documentclass` 推断**（D-venue 决策，见 [configure-design.md](../../docs/configure-design.md)）：`\documentclass`（模板类型）≠ venue（投稿目标）——用 acmart 模板可投 PVLDB/ICSE/FASE/...，configure 强行映射（acmart→acm-sigconf）会覆盖作者投稿意图，破坏下游 [xept:mock-review](../mock-review/SKILL.md) / [xept:dual-review](../dual-review/SKILL.md) 读取的会议标准。venue 由作者或 [xept:setup-venue](../setup-venue/SKILL.md) 设（author-set）。

- **exit 1**：无 `\documentclass` 或 .tex 不可读。
- **exit 2**：目录模式下多个 .tex 含 `\documentclass` → 输出候选 `{"error": "multiple_documentclass_roots", "candidates": [...]}`，configure 问用户选定后单文件重跑。
- 部分失败：title/bibliography 找不到 → 空串 `""`（不报错，configure 报告"未检出"）。
- 若扫描发现 project.yml 已与论文完全一致（paper-derivable 字段）→ 报告 "already in sync" 并退出（no-op）。

language 检测（精确阈值）：
- CJK 统一表意文字（`一-鿿`）占非空白字符 ≥ 30% → `chinese`，否则 `english`。
- ambiguous 场景（纯公式/代码多）默认 `english`。

sections_dir/figures_dir 检测启发式（按候选目录列表检查）：
- sections 候选：`sections/`、`sec/`、`chapters/`；首个存在的胜出；都不存在 → `""`。
- figures 候选：`figures/`、`figs/`、`imgs/`；首个存在的胜出；都不存在 → `""``。

### Step 3: 同步 `.self_xept/project.yml`
读现有 project.yml（+ project.user.yml overlay，[§5](../../docs/conventions.md)）。字段分两类：

| 类别 | 字段 | configure 动作 |
|---|---|---|
| **paper-derivable**（论文派生） | `main_file` / `title` / `language` / `structure.sections` / `structure.figures` / `structure.bibliography` | **resync** 到扫描值；漂移则改并报 old→new |
| **author-set**（作者拥有） | **`venue`**（投稿目标，非模板类型）/ `state` / `deadline` / `anonymity` / `page_limit` / `field` / `ideation.*` / 个人偏好 | **不动**——论文无法告知这些（`\documentclass` 是模板类型，不等于 venue） |

四态处理：
- **缺失** → 从模板建，填扫描值
- **不完整** → 补缺的标准 section，更新 paper-derivable 字段
- **漂移** → resync paper-derivable 字段（venue≠`\documentclass` 等），报 diff
- **一致** → byte-for-byte 不动

### Step 4: 确保 overlay + 元状态文件

**overlay**（`.self_xept/project.user.yml`，个人密钥 / per-author 偏好，gitignored）：
- 缺失 → 写默认 overlay（最小模板：注释"个人 overlay，gitignored，勿提交"+ 可选 `literature.semantic_scholar_api_key: ""` 占位）
- 已存在但 YAML 解析失败 → fail-closed 报错停下（和 base 一致，不猜结构）
- 已存在但结构过期（缺新 section）→ 规范化结构但**不动个人值**
- 已存在且完整 → **不动**（除非用户明确要求更新，且永不覆盖个人值）

**元状态文件**（`.self_xept/facts.md` 术语/数据基线 + `.self_xept/references.md` 已核实引用，供下游 [check-submission](../check-submission/SKILL.md) 术语对照 / [add-citation](../add-citation/SKILL.md) 复用——真实使用验证发现这些文件缺失时下游 skill 无降级说明）：
- 缺失 → 建空模板（`# Facts` 标题 + 注释"术语/数据基线，由 check-submission/write-paper 维护"；`# Citations` 标题 + 注释"已核实引用，由 add-citation 追加"），让下游 skill 见空知"基线空，首次使用"
- 已存在 → **不动**（下游 skill 维护这些文件，configure 只确保存在）

### Step 5: 报告
列每个改动（file created / section added / field resynced，带 old→new）让用户确认。推理可能错（`\documentclass` 不符真实 venue、非根 main.tex）；人眼能 catch。已完全一致无改动 → 明说。

## Red Flags — STOP

- 动论文自己的文件（main.tex / .bib / figures/ / sections/）—— configure 只写配置 YAML
- 发明或改 author-set 字段（state / ideation.* / deadline / 个人偏好）
- 覆盖 project.user.yml 里的个人值
- YAML 损坏时猜结构静默重写
- 找不到主 `.tex` 还硬配

## Common Mistakes

| 问题 | 后果 | 修 |
|---|---|---|
| 复制模板 / 创建 main.tex | 破坏存量论文 | configure 只写 YAML，不碰论文文件 |
| 出于谨慎留着漂移字段 | 配置和论文不一致，下游 skill 乱 | resync 并报 old→new |
| 发明 ideation metadata "填满"配置 | 论文支撑不了的假值 | author-set 字段留给作者 |
| 覆盖 project.user.yml 个人值 | 丢作者设置 | 只规范化结构，不覆盖值 |
| 已一致还跑 | 假 diff | 先查，一致就报 "already in sync" 停 |

## Self-Review

- [ ] project.yml 存在、YAML 合法、标准 section 齐？
- [ ] paper-derivable 字段和论文一致（main_file 指向真根、title=`\title{}`、language=论文实际语言）？**venue 未动**（author-set，不从 `\documentclass` resync）？
- [ ] author-set 字段（venue / state / ideation.* / deadline / 个人偏好）原样保留？
- [ ] project.user.yml 缺则建默认、有则不动？
- [ ] 每个改动报告了（或"已一致"）？
- [ ] 只写了配置 YAML，没动论文文件？

## 配套（实现阶段补）

- 扫描器：`scripts/infer_paper_meta.py`（纯 stdlib 正则 + 文件系统检查；fail-closed exit 1；多候选 exit 2 输出候选列表；**不推断 venue**——它是 author-set；JSON 输出含 documentclass）
- 单测：`tests/scripts/infer_paper_meta_test.py`（documentclass 提取 + 多候选 exit 2 + 缺失/漂移/一致三态 + 中文检测 + 无 `\documentclass` exit 1）

## Integration

- **互补**：[xept:setup-venue](../setup-venue/SKILL.md)（前向 CFP 配置）
- **下游**：[xept:write-paper](../write-paper/SKILL.md) / [xept:mock-review](../mock-review/SKILL.md) / [xept:fix-latex](../fix-latex/SKILL.md)（读 project.yml）
- **元状态**：[.self_xept/ 分层配置](../../docs/conventions.md)

---

## 立项验收清单（review 用）

- [ ] 与 setup-venue 边界清晰（前向 vs 反向，数据源不同）
- [ ] paper-derivable vs author-set 字段分类明确
- [ ] 幂等四态（缺失/不完整/漂移/一致）处理逻辑写明
- [ ] HARD-GATE（YAML 必须可解析，损坏不猜）
- [ ] infer_paper_meta.py 接口契约（JSON 输出**无 venue**、exit 1 错误 / exit 2 多候选）
- [ ] 扫描脚本化 + 合并/报告留 prompt（§1 务实混合）
- [ ] 方言合规（`xept:` 引用、`.self_xept/`、中文正文、无 `pp:`/paperpilot 残留）

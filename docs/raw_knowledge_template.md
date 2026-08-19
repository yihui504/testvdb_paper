```markdown
# {target} v{version} API Knowledge

## Document Metadata
- doc_version: {actual_document_version}
- target_version: {target_version}
- version_match: {major.minor 匹配结果: matched | mismatched}
- source_url: {文档首页 URL}
- fetched_at: {ISO 8601 timestamp}

## Document Sources
| # | URL | Doc Version | Fetched At | Version Match |
|---|-----|-------------|------------|---------------|
| 1 | {url_1} | {version_1} | {timestamp_1} | matched/mismatched |
| 2 | {url_2} | {version_2} | {timestamp_2} | matched/mismatched |
| ... |

## SDK Information
- Package: {package_name}
- Version: {sdk.version}
- Install: {install_command}

## Docker Images
- Available tags: [{tags}]
- Recommended: {recommended_tag}

## API Endpoints / SQL Operations

### {category_name}

#### {endpoint_name}
- Method: {HTTP_METHOD}
- Path: {path}
- Source URL: {该端点文档的具体 URL}
- Doc Version: {该页面的文档版本}
- Parameters:
  - {param_name} ({type}, required={true/false}): {description}
- Constraints:
  - type: {type_constraint}
  - range: {range_constraint}
  - state: {state_constraint}
  - behavioral: {behavioral_contract}
- Expected Responses:
  - 200: {description}
  - 400: {description}
  - 404: {description}
  - ...

## Data Types
- {type_name}: {description}

## Collection / Table Schema
- {schema_details}
```

---

# 真实模板排版方案（页 0 用）

来源：`knowledge-extractor.md` Step 5 内置模板（line 267-320），**逐字未改**，
仅去掉首尾 ```markdown 围栏，可直接粘进 PPT 代码框。

## 模板全文 53 行——PPT 一页放不下怎么办：三选一

### 方案 A：全量展示（推荐，11pt 等宽 + 分区着色）
53 行在 16:9 页用 10.5-11pt Consolas 行距 1.0 刚好放下（右侧 60% 宽栏）。
着色规则（其余全黑）：
- 文件头到 `## Document Metadata` 三条 → 蓝 #6096E6 加粗：**版本锚定**
- `## Document Sources` 表 → 绿 #56CA95：**每页一行可溯源**
- `## SDK / Docker` → 灰 #808080：**环境可复现**（弱化，非重点）
- `### {category}` / `#### {endpoint}` → 深蓝 #0A4A94 加粗
- `Source URL` / `Doc Version` 行 → 橙 #FFBA55：**证据链锚点**
- `Constraints:` 及 type/range/state/behavioral 四行 → 红 #FF0000 加粗：**攻击靶点**
- `Expected Responses` → 紫 #EC5F74：**行为契约**

### 方案 B：折叠式（模板 + 三个放大镜）
模板 8-9pt 全量灰字铺底，三个关键区域用圆角框圈出放大：
①Document Metadata（版本锚定）②Constraints 四行（攻击靶点）
③Source URL/Doc Version（证据锚点）——放大框旁配 13pt 一行注解。
适合讲述时逐个点开的节奏。

### 方案 C：骨架+细节双栏
左窄栏模板骨架（只留 ## / ### / #### 标题行，11 行），右宽栏放一个
`#### {endpoint}` 完整展开（Method 到 Expected Responses，约 20 行）。
"整体结构"与"原子单元长什么样"各占一栏。

## 围绕模板的讲述注解（配哪版方案都适用，放左侧或底部）

按模板自上而下五段，每段一句"为什么在这"：
1. `Document Metadata` — doc_version vs target_version 入库即比对；
   version_match: mismatched 的页面后续不采信 → **回答"怎么防版本漂移"**
2. `Document Sources` 表 — 每个概念文档页独立一行（禁止合并 "docs/*" 通配），
   ≥5 页完整性自检的核对对象 → **回答"从何而来、怎么防漏爬"**
3. `SDK / Docker` — 实验环境冻结在知识库里 → **回答"可复现性"**
4. `#### {endpoint}` 的 `Source URL + Doc Version` — 每条约束都能追回文档原文，
   幻觉在回验时暴露 → **回答"怎么防错爬/幻觉"**
5. `Constraints: type/range/state/behavioral` — 四类约束即攻击脚本的靶点分类，
   与三个 attack agent 的策略矩阵一一对应（页 2 呼应）→ **回答"提取重点在哪"**

底部一句话（黑底白字或灰底横条）：
**"模板即提取规范：抓什么、怎么存、带什么证据——全部写死在结构里，agent 无自由发挥空间。"**

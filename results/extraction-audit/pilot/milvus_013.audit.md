# 试点审计记录 · milvus_013（2026-09-11）

重建件：`milvus_013.rebuilt.md`　原件：`TestVDB_artifact/rq2/materials/milvus_013.md`（未改动，留证）

## 原件的问题（逐门）

| 门 | 原件状况 |
|---|---|
| G1 版本一致 | `补充契约依据` 段自称"同版本契约"，实际引 **v2.3.x**；包受测 2.6.16。段内自相矛盾 |
| G2 引用可解析 | 该 v2.3.x 页 **301 → /docs**，已死 |
| G3 来源类型 | 未标注 |
| G4 端点相关 | `相关契约段` 4 条 + `补充契约行` 13 条，**共 17 条全部与 `collections+list` / Request-Timeout 无关** |
| G5 观察证据 | 完好（三段请求/响应齐全） |
| G6 无泄漏 | `_provenance` 写有 issue **#49890**，并复述本案行为与结论（"float 3.5 silently truncated, string \"abc\" silently ignored"） |
| G7 审计留痕 | 无 |

**关键**：原件里唯一与本案相关的契约行，是靠**死链 + 泄漏注记**支撑的；而其余 17 条全是噪声。

## 重建过程（实际做的核查）

1. **版本锚定** — 受测 2.6.16 ⇒ 取 2.6.x REST API 参考（major.minor 一致）。
2. **查文档依据** — 拉取 6 个 2.6.x 端点页，逐页检索 `Request-Timeout`：
   - 命中位置**全部在 curl 示例行**（`--header "Request-Timeout: 5"`）；
   - Parameters 表**仅**将 `Authorization` 列为 header 参数；
   - ⇒ **本版本文档对 `Request-Timeout` 无任何类型/取值约束。**
3. **查来源侧**（不进包，仅入本审计）— milvus v2.6.16 `timeout_middleware.go:183`：
   ```go
   timeoutSecond, err := strconv.ParseInt(gCtx.Request.Header.Get(mhttp.HTTPHeaderRequestTimeout), 10, 64)
   if err == nil { timeout = time.Duration(timeoutSecond) * time.Second }
   ```
   实现为「**解析失败即回退默认超时**」，非接受/拒绝校验 —— 与三值观察（3.5/abc/10 均 200）一致。

## 结论

**该断言在受测版本无文档依据。** 观察到的行为不违反任何文档承诺
（文档既未声明 `Request-Timeout` 的类型，也未声明非法值会被拒绝）。
按论文对 documentation-implementation bug 的定义，本案**不构成**该类缺陷。

⇒ 重建件的 `契约依据` 段如实记录"本版本文档无相关约束条目"，并附已核查的引用页清单与核查结论。
评委据此只能依观察本身判断（与 dispatch 模板"无契约依据时按观察行为本身评估"一致）。

## 门控命中与新增

G1/G2/G3/G4/G6 — 原件均不通过，重建件均通过；G5 两版一致；G7 由本文件承担。

**新增 G8（试点中发现）**：包内**不得预置来源侧分析**。
上文第 3 步查到的实现事实（ParseInt 回退）**没有写进重建包** —— 它属于确认阶段的工作，
预置进包等于把结论递给评委。G8 已补入 `QUALITY_GATE.md`。

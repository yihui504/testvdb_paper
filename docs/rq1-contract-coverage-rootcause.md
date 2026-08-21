# RQ1 契约覆盖率低下——根因定位报告

> 2026-08-20，基于 pilot qdrant v1.18.2 实测数据定位。修复已落 testvdb4exp `215e4a9` 并同步插件 cache。

## 现象

pilot 的 raw_knowledge.md 自报 `doc_coverage_pct: 100% (70/70 core endpoints)`，但：

- 最终契约只有 **10 个端点**；
- GT 4 bugs 中 3 个（qdrant_9421 `cluster+recover`、qdrant_9520 `shard_number`、qdrant_9522 `lookup_from`）所在端点/参数不在契约内 → **reach 理论上限 = 1/4**（实测 1/4，正是唯一在契约内的 hnsw_ef）。

## 根因链（三层）

### 根因 1：OpenAPI spec 从未被 fetch——"不存在则跳过"是无条件逃逸舱门

`knowledge-extractor.md` Step 6b 的 spec 定位路径只有 weaviate 形态
（`.sourcedeps/{target}/{version}/docs/redoc/master/openapi.json`），qdrant 的 spec
**从没有被任何环节预取**。于是每次运行都走"如不存在，跳过本步并记录
openapi_unavailable: true"——OpenAPI cross-check（设计上就是反"漏新功能"的对照机制）
对 qdrant 形同虚设。

### 根因 2：LLM 自报覆盖率无对照——幻觉分母被采信

spec 跳过后，extractor 仍写出 `doc_coverage_pct: 100% (70/70 core endpoints)`。
"70/70"这个分母没有任何来源——纯 LLM 编造。契约实际只有 9-10 个端点。
机械核对后真实数字：**9/75 = 12.0%**（spec paths 76 条减去根路径后 75）。

### 根因 3：`validate_doc_coverage.py` 工具链断裂

对照脚本存在，但依赖 `.sourcedeps/` 下的 spec 文件——qdrant 从没 fetch 过，
脚本每次都是 "OpenAPI spec not found → 跳过"（exit 0），从没真正产出过报告。
工具存在 = 没接线 = 没效果。

### 附加根因 4：默认排除表排掉了 `/cluster`

`DEFAULT_EXCLUDE_PREFIXES` 含 `/cluster`——qdrant_9421（`POST /cluster/recover`
standalone 500→4xx，RQ1 档1.5 probe 确认 standalone 可触发）被系统性排除。
即使 spec 就位，这条 GT bug 也会被覆盖率检查从分母里抹掉。

## 修复（testvdb4exp 215e4a9）

| 层 | 修复 | 落点 |
|---|---|---|
| 预取 | `fetch_openapi_spec.py`（新）：qdrant 目录分片合并 / weaviate GitHub tag → `.sourcedeps/{target}/{version}/openapi.json` | 主进程 Step 4.5 派 extractor **前**执行 |
| 机械核对 | `validate_doc_coverage.py`：新 spec 路径 + 根路径过滤 + **机械覆写 doc_coverage_pct**（报告落盘 `doc_coverage_report.json`，含 `llm_self_report_overridden: true`） | Step 4.5 派 extractor **后**执行 |
| 反编造 | extractor Step 6b：spec 不可用时**禁止写数字**（写 N/A），分母必须是 spec paths 真实计数 | agents/knowledge-extractor.md |
| 排除表 | `/cluster` 移出默认排除（standalone 可用性由 attack 侧对照组兜底，不靠覆盖率排除） | validate_doc_coverage.py |

## 效果验证（对 pilot 数据重放）

```
修复前：raw_knowledge.md 自报 doc_coverage_pct: 100% (70/70 core endpoints)
修复后：doc_coverage_pct: 12.0% (9/75 endpoints, machine-verified vs OpenAPI paths)
        missing_endpoints 含 POST /cluster/recover（GT 9421）、
        POST /collections/{param}/points/query（GT 9522）——根因闭环
```

## 对 15 版本全量的含义

- reach 分母评估有了确定性依据：`doc_coverage_report.json` 的 missing_endpoints × GT bug 参数面交叉，可预先算出每版本契约下 GT reach 的理论上限，异常低时先补契约再跑实验。
- 全量跑之前的动作：每版本先跑 Step 4.5 两个脚本，核对 doc_coverage_pct ≥ 某阈值（待定，建议 ≥60%）再放行挖掘；低于阈值先派 extractor 补爬 missing_endpoints。

# 锚 2｜milvus_001 (issue #47635) — 状态码语义：code=0 严格定义为 Success

- **来源**: Milvus API Reference, R.Status 定义（https://milvus.io/api-reference/java/v2.3.x/v1/Misc/RT.md；REST 参考同一定义）
- **存档状态**: 官方参考站为 redoc 生成页且 milvus.io 返回 403（反爬），原文以 **issue #47635 提交时（2026-02-06）逐字核对并引用** 的文本为准；页面复抓存档待网络许可
- **对应缺陷**: milvus_001 / issue #47635 "Search fails with Code 0 immediately after Collection.load() returns success"（TP，triage/accepted + milestone 2.x-Backlog，stale 关闭未修）

## 原文（issue #47635 body 逐字引用）

> According to the [Milvus Java SDK R.Status definition](https://milvus.io/api-reference/java/v2.3.x/v1/Misc/RT.md), `Code 0` is strictly defined as **Success (Operation succeeded)**. Returning `code=0` for a failed operation violates this API contract.

实测错误消息（body）：

> `<MilvusException: (code=0, message=attempt #0: fail to get shard leaders from QueryCoord: collection=...: collection not loaded: unrecoverable error: ...)>`

## 断言映射（新模板：状态码语义断言）

- 约束: `code=0` 仅可在操作成功时返回；失败的操作（如 "collection not loaded"）必须返回非零错误码
- 违反形态: search 实际失败却返回 `code=0`（假成功）——监控污染、客户端无法按错误码重试
- evidence_tier: **explicit**（Status 定义逐字）
- 备注: 我方链曾以 "load() 为异步"（job_load.go）作 WEAK_REFUTED——维护者裁定的要点不在异步本身，而在**失败仍报成功码**；异步语义由 get_load_state 端点支撑，成功码语义由 Status 定义支撑，两者并不互斥（异步完成时可以报错，但不该报 Success）

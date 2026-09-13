# 锚 3｜milvus_024 (issue #50323) — delete 选择器 filter/ids 互斥

- **来源**: Milvus REST API Reference v2, `POST /v2/vectordb/entities/delete` 参数说明
- **存档状态**: 参考站为生成页且 milvus.io 返回 403，原文以 **issue #50323 提交时（2026-06-05）核对** 的表述为准；页面复抓存档待网络许可
- **对应缺陷**: milvus_024 / issue #50323 "Delete endpoint accepts both filter and ids (mutually exclusive) silently"（TP，triage/accepted + assigned MrPresent-Han + milestone 2.6.23，open 未修）

## 原文（issue #50323 body 逐字）

> The `entities/delete` endpoint silently accepts **both** `filter` and `ids` parameters simultaneously — documented as **mutually exclusive**. The operation proceeds using `filter` and ignores `ids`, returning `deleteCount` matching the filter.
>
> ```
> POST /v2/vectordb/entities/delete
> {"collectionName": "test", "dbName": "default", "filter": "id > 0", "ids": [1, 2, 3]}
> Response: {"code": 0, "data": {"deleteCount": 1}}
> ```

## 断言映射

- 约束: `filter` 与 `ids` 为互斥删除选择器；同时提供必须返回校验错误（4xx）
- 违反形态: 双参数被静默接受、filter 优先生效且 ids 被静默忽略（deleteCount 仅反映 filter）——无任何歧义提示
- evidence_tier: **explicit**（参考页互斥说明；存档状态如上注明，复抓后升级为完整逐字存档）
- 备注: 我方契约的 delete 参数面未提取 `ids` 参数（采集缺口）；即便互斥注记存档待补，"文档未声明的参数被静默接受并改变选择器语义" 亦构成接口面违规

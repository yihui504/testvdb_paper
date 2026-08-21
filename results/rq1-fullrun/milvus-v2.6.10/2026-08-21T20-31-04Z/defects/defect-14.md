# Defect 14: entities/upsert — upsert 与 insert 跨通道三向混型动态字段全部 code:0（约束 1100 拒绝点不存在）

## Metadata
- Defect ID: TESTVDB-MILVUS-14
- defect_id (script): boundary_r2_dyn_type_upsert_05
- Type: Type1_IllegalSuccess
- Endpoint: POST /v2/vectordb/entities/upsert（+ entities/insert 跨通道）
- Param: dataType（param_name: dataType）
- Novelty: NOVEL（gate, no_known_hits, confidence HIGH）
- Evidence Weight: MODERATE_STRONG

## Reproduction (curl)
```bash
# upsert 建立 string 基线：{"id":1,"dynf":"s"} -> code:0 upsertIds:[1]
# 混型 upsert：
curl -s -X POST "http://localhost:19530/v2/vectordb/entities/upsert" \
  -H "Content-Type: application/json" \
  -d '{"collectionName":"<enableDynamicField=true>","data":[{"id":2,"dynf":1}]}'
```

## Expected vs Actual
- Expected: 已建立动态字段不兼容类型 upsert => 1100（约束 endpoint 域含 upsert）
- Actual（三向混型全 code:0）：
  - `upsert string->int -> ok=True raw={"code":0,"cost":0,"data":{"upsertCount":1,"upsertIds":[2]}}`
  - insert 建 int → `upsert int->string -> ok=True raw={"code":0,...,"upsertIds":[3]}`（跨通道）
  - `upsert establish bool -> ok=True`；`upsert bool->int -> ok=True code:0 upsertIds:[5]`
  - array 互混组合 log 未逐字取证（partial，如实记）

## Evidence Chain
- Ring 1 (Contract Clause 契约条款) constraint_id: milvus_type_dynamic_field_consistency_001
  - assertion: `dynamic field type consistency: second insert with incompatible type for established dynamic field -> 1100`；api_violates_assertion=true（upsert 通道 + 跨通道均违反）
- Ring 2 (Document Reference 文档引用) doc_verification: DOC_VERIFIED（同 13 号链锚，insert-update-delete.md Entity Schema Consistency）
- Ring 3 (Actual Behavior 实际行为, HTTP Response 见 log) Script: debate_logs/boundary_r2_dyn_type_upsert_05.py（grade B；与 matrix_04 互证）
- Log: debate_logs/output_boundary_r2_dyn_type_upsert_05.log

### 源码 文件:行号+摘录
- upsert 与 insert 在 HTTP 层共用 checkAndSetData + anyToColumns（handler_v2.go L1236/L1247；utils.go L598-609 类型 cast 无历史对照，L947-957+L1202-1217 JSON 列下发）
- internal/proxy/task_upsert.go：可见显式校验仅 validatePartitionTag（L192、L929）——task 侧有校验钩子位但仅限分区名，无动态字段类型一致性校验（validation_absent）

## Impact
类型混用不仅限于单通道：insert 建立的类型可被 upsert 覆盖为不兼容类型（string↔int、bool→int 三向），且 upsert 的替换语义使同一 id 的字段类型在生命周期内漂移。约束声称的 1100 拒绝点在 upsert/跨通道路径均不存在，schema 一致性承诺全面失守。

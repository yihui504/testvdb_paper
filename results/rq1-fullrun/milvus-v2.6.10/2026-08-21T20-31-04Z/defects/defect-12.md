# Defect 12: entities/upsert — 非法动态字段名 upsert 静默接受，同值 create-schema 通道 1701 正确拒（双通道分叉）

## Metadata
- Defect ID: TESTVDB-MILVUS-12
- defect_id (script): boundary_r2_dynfield_name_upsert_03
- Type: Type1_IllegalSuccess
- Endpoint: POST /v2/vectordb/entities/upsert（对照 collections/create schema）
- Param: fieldName（param_name: fieldName）
- Novelty: NOVEL（gate, no_known_hits, confidence HIGH）
- Evidence Weight: STRONG

## Reproduction (curl)
```bash
curl -s -X POST "http://localhost:19530/v2/vectordb/entities/upsert" \
  -H "Content-Type: application/json" \
  -d '{"collectionName":"<enableDynamicField=true>","data":[{"id":300,"123field":"v"}]}'
```

## Expected vs Actual
- Expected: 动态字段名 ^[A-Za-z_][A-Za-z0-9_]*$，非法应拒（同 create-schema 通道行为）
- Actual: `upsert dyn field '123field' -> ok=True raw={"code":0,"cost":0,"data":{"upsertCount":1,"upsertIds":[300]}}`；'@field'→[301]、'my-field'→[302] 同 code:0
- 对照组（同值 create schema fieldName）：`'123field' -> ok=False raw={"code":1701,"message":"Invalid field name: 123field. The first character of a field name must be an underscore or letter.: field name invalid[field=123field]"}`；'@field'/'my-field' 均 1701

## Evidence Chain
- Ring 1 (Contract Clause 契约条款) constraint_id: milvus_type_field_name_rules_001
  - assertion: `field names: ^[A-Za-z_][A-Za-z0-9_]*$, length<=255, enforced at insert-time (dynamic fields included)`；api_violates_assertion=true
- Ring 2 (Document Reference 文档引用) doc_verification: DOC_VERIFIED（同 11 号链锚，limitations.md，R2 补锚已核）
- Ring 3 (Actual Behavior 实际行为, HTTP Response 见 log) Script: debate_logs/boundary_r2_dynfield_name_upsert_03.py（grade B；与 01 号链构成跨通道复现）
- Log: debate_logs/output_boundary_r2_dynfield_name_upsert_03.log

### 源码 文件:行号+摘录
- handler_v2.go insert/upsert 共用 checkAndSetData（L1234-1252 调用；utils.go L592-621 动态字段分支 mapKey 无校验）
- 对照 internal/proxy/util.go validateFieldName L369-381：`if firstChar != '_' && !isAlpha(firstChar) { "The first character of a field name must be an underscore or letter." }` / `if c != '_' && !isAlpha(c) && !isNumber(c) { "Field name can only contain numbers, letters, and underscores." }`——log 中 1701 消息产生点
- 双通道分叉定位：create-schema 走 validateFieldName（1701 拒），upsert 动态路径零校验（validation_absent）

## Impact
同一命名规则在同一系统两通道一有一无：schema 声明通道正确拒（1701），upsert 动态字段通道静默收（code:0）。upsert 写入的非法名字段同样落入不可回读状态（同 Defect 11 后果），且 upsert 的替换语义使已有合法数据被覆盖时混入死数据的风险更高。

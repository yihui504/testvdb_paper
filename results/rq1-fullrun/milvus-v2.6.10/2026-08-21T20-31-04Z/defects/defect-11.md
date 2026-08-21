# Defect 11: entities/insert — 5 类非法动态字段名被接受且 query 不可回读（validateFieldName 未调用，数据可访问性断裂）

## Metadata
- Defect ID: TESTVDB-MILVUS-11
- defect_id (script): boundary_r2_dynfield_name_insert_01
- Type: Type1_IllegalSuccess
- Endpoint: POST /v2/vectordb/entities/insert（+ entities/query）
- Param: fieldName（param_name: fieldName）
- Novelty: NOVEL（gate, no_known_hits, confidence HIGH）
- Evidence Weight: STRONG

## Reproduction (curl)
```bash
curl -s -X POST "http://localhost:19530/v2/vectordb/entities/insert" \
  -H "Content-Type: application/json" \
  -d '{"collectionName":"<enableDynamicField=true>","data":[{"id":100,"123field":"v"}]}'
```

## Expected vs Actual
- Expected: 动态字段名须匹配 ^[A-Za-z_][A-Za-z0-9_]*$、length<=255，insert-time 强制（dynamic fields included）；非法应拒
- Actual（5 类非法名全 code:0 接受 + 不可回读）：
  - `insert dyn field '123field' -> http=200 ok=True raw={"code":0,"cost":0,"data":{"insertCount":1,"insertIds":[100]}}`；`query outputFields=['123field'] -> ok=False raw={"code":65535,"message":"parse output field name failed: 123field"}`
  - 同模式：'@field'→insertIds:[101]、'my-field'→[102]、'field name'(空格)→[103]、'f$eld'→[104]，query 均 65535
  - 255-char 合法名对照通过

## Evidence Chain
- Ring 1 (Contract Clause 契约条款) constraint_id: milvus_type_field_name_rules_001
  - assertion: `field names: ^[A-Za-z_][A-Za-z0-9_]*$, length<=255, enforced at insert-time (dynamic fields included)`；api_violates_assertion=true
- Ring 2 (Document Reference 文档引用) doc_verification: DOC_VERIFIED（limitations.md Resource Naming Rules——字母或下划线开头、仅字母数字下划线；link_reachability PARTIAL：上游 R2 补锚时已核 verified/quoted）
- Ring 3 (Actual Behavior 实际行为, HTTP Response 见 log) Script: debate_logs/boundary_r2_dynfield_name_insert_01.py（grade B；多脚本稳定触发，upsert 通道同模式）
- Log: debate_logs/output_boundary_r2_dynfield_name_insert_01.log

### 源码 文件:行号+摘录
- httpserver/utils.go checkAndSetData L590-621（动态字段写入侧）：`for mapKey, mapValue := range data.Map() { if !containsString(fieldNames, mapKey) { if collSchema.EnableDynamicField { ... gjson 类型 cast ... } } }`——mapKey 无任何 validateFieldName 调用
- internal/proxy/util.go validateFieldName L356-388（完整命名规则实现，create-schema 通道使用，错误码 1701）在 insert 动态路径未被调用
- query 侧拒绝点 internal/proxy/util.go L1637-1665：ParseIdentifier 解析 outputFieldName 失败 → `parse output field name failed: %s` code 65535——同规则 query 侧经 parser 间接执行、insert 侧缺失，非对称校验（validation_absent）

## Impact
非法命名的动态字段可写入不可读回——持久化的数据可访问性断裂：数据入库（code:0 成功、计费/存储生效）但任何 query/outputFields 引用均 65535 失败。用户在无任何告警的情况下制造了只写不读的死数据；命名规则契约在 insert 动态路径完全失效。

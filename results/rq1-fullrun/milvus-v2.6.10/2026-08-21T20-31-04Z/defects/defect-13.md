# Defect 13: entities/insert — 动态字段类型一致性失守：string→int 四格矩阵第二笔全部 code:0（期望 1100）

## Metadata
- Defect ID: TESTVDB-MILVUS-13
- defect_id (script): boundary_r2_dyn_type_matrix_04
- Type: Type1_IllegalSuccess
- Endpoint: POST /v2/vectordb/entities/insert
- Param: dataType（param_name: dataType）
- Novelty: NOVEL（gate, no_known_hits, confidence HIGH）
- Evidence Weight: MODERATE_STRONG

## Reproduction (curl)
```bash
# 第一笔建立 dynf 为 string：{"id":1,"dynf":"hello"}
# 第二笔同字段传 int：
curl -s -X POST "http://localhost:19530/v2/vectordb/entities/insert" \
  -H "Content-Type: application/json" \
  -d '{"collectionName":"<enableDynamicField=true>","data":[{"id":2,"dynf":1}]}'
```

## Expected vs Actual
- Expected: 已建立的动态字段以不兼容类型再次 insert => code==1100（Entity Schema Consistency）
- Actual（四格矩阵全 code:0）：
  - `dynf string('hello') -> int(1): second insert ok=True raw={"code":0,"cost":0,"data":{"insertCount":1,"insertIds":[2]}}`
  - string('hello')→int(-5)：code:0 [2]；string('')→int(1)：code:0 [2]；string('')→int(-5)：code:0 [2]（含空串边界）

## Evidence Chain
- Ring 1 (Contract Clause 契约条款) constraint_id: milvus_type_dynamic_field_consistency_001
  - assertion: `dynamic field type consistency: second insert with incompatible type for established dynamic field -> 1100`；api_violates_assertion=true（四组合均不兼容且均 code:0）
- Ring 2 (Document Reference 文档引用) doc_verification: DOC_VERIFIED（insert-update-delete.md Entity Schema Consistency——同一 Collection 内 Entities 具有相同属性（字段名/类型）；R2 补锚 quoted/verified）
- Ring 3 (Actual Behavior 实际行为, HTTP Response 见 log) Script: debate_logs/boundary_r2_dyn_type_matrix_04.py（grade B；与 05 号链同模式互证）
- Log: debate_logs/output_boundary_r2_dyn_type_matrix_04.log

### 源码 文件:行号+摘录
- httpserver/utils.go L598-609：`switch mapValue.Type { case gjson.String: reallyData[mapKey] = mapValueStr; case gjson.Number: if strings.Contains(mapValue.Raw, ".") { cast.ToFloat64 } else { cast.ToInt64 } }`——仅按当笔请求 JSON 类型 cast，不对照已建立的动态字段类型
- anyToColumns L947-957：动态字段 marshal 成整行 JSON（`m[name] = candi.v.Interface(); bs, _ := json.Marshal(m)`）；L1202-1217 以匿名 DataType_JSON 列（IsDynamic:true, FieldName:""）下发
- 约束声称的 1100 拒绝点在 insert 路径不存在（validation_absent）
- 抗辩记档：动态字段 JSON 承载模型允许异构值（by_design 疑义），但机械 A 定案不翻案

## Impact
同一动态字段可在不同行持有互不兼容类型（string/int/bool 混杂），文档承诺的 Entity Schema Consistency 在动态字段面失效。下游消费方对动态字段做类型假设（如 int 求和）时读到混合类型将产生运行时错误或静默计算错误，数据质量退化不可发现。

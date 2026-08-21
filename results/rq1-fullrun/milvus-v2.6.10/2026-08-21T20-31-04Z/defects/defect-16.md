# Defect 16: entities/search — searchParams.nprobe 接受字符串 '4' 静默强转（%v 透传抹平类型，与 ef 同根因）

## Metadata
- Defect ID: TESTVDB-MILVUS-16
- defect_id (script): semantic_r2_nprobe_02
- Type: Type1_IllegalSuccess（类型恒真）
- Endpoint: POST /v2/vectordb/entities/search
- Param: nprobe（param_name: nprobe）
- Novelty: NOVEL（gate, no_known_hits, confidence HIGH）
- Evidence Weight: MODERATE_STRONG（契约无类型断言原文——doc 弱锚，仅记弱锚）

## Reproduction (curl)
```bash
curl -s -X POST "http://localhost:19530/v2/vectordb/entities/search" \
  -H "Content-Type: application/json" \
  -d '{"collectionName":"<IVF 已加载>","data":[[...]],"limit":5,"searchParams":{"params":{"nprobe":"4"}},"outputFields":["id"]}'
```

## Expected vs Actual
- Expected: nprobe 语义为整数（IVF 扫描簇数；PyMilvus SDK 基线 nprobe: int），字符串 '4' 应类型拒绝
- Actual: `nprobe='4': 200 {"code":0,"cost":0,"data":[{"distance":0,"id":0},{"distance":0.001953125,"id":1},{"distance":0.0078125,"id":2},{"distance":0.017578125,"id":3},{"distance":0.03125,"id":4}],"topks":[5]}`
- 基线 nprobe=4（int）的 top-5 与 distance 序列和字符串版完全一致——静默强转且语义生效
- 环境注记：index create 残留 code:65535（multiple indexes），不影响 search 观测；claim 中 -1/INT32_MAX 正常项 log 未逐字留存（如实记）

## Evidence Chain
- Ring 1 (Contract Clause 契约条款) constraint_id: 泛锚（endpoint registry L3091：searchParams keys {nprobe, ef, level, radius, range_filter, search_list} index-type dependent——无类型断言）
  - assertion: `v2 search request; searchParams keys are index-type dependent: {nprobe, ef, ...}`；api_violates_assertion=true（semantically grounded, not verbatim anchored——auditor 复核后采信）
- Ring 2 (Document Reference 文档引用) doc_verification: DOC_PARTIAL（契约/文档无 nprobe int-only 原文——doc 弱环如实记）
- Ring 3 (Actual Behavior 实际行为, HTTP Response 见 log) Script: debate_logs/semantic_r2_nprobe_02.py（基线-攻击对照；单脚本）
- Log: debate_logs/output_semantic_r2_nprobe_02.log

### 源码 文件:行号+摘录
- utils.go generateSearchParams L2076-2131（逐字核实）：
  ```go
  bs, _ := json.Marshal(paramsMap)
  searchParams = append(searchParams, &commonpb.KeyValuePair{Key: Params, Value: string(bs)})
  for key, value := range reqSearchParams {
      if key != Params {
          if key == "ignoreGrowing" { key = common.IgnoreGrowing }
          searchParams = append(searchParams, &commonpb.KeyValuePair{Key: key, Value: fmt.Sprintf("%v", value)})
      }
  }
  ```
  - L2125 `fmt.Sprintf("%v", value)`：字符串 '4' 与整数 4 序列化同为 "4"，类型信息在此被抹平
  - 嵌套 params 经 json.Marshal 保留引号但下游 index 侧解析容忍
- 与 R1 ef（Defect 8）同根因交叉印证；verification_outcome: validation_absent

## Impact
IVF 索引核心参数 nprobe 的类型契约缺失：任意可强转字符串被静默接受且行为与 int 版不可区分。类型错误零错误信号，与 ef 的非法值静默替换（Defect 8）共同构成 searchParams 透传层系统性校验缺口；REST 弱类型客户端（JSON 天然 string-prone）的错误无从暴露。

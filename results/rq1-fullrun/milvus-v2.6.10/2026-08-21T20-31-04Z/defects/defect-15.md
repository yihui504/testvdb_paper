# Defect 15: partitions/create — 分区名校验放宽：数字开头与连字符被放行，错误消息与实现矛盾（alias/index 通道同值正确拒）

## Metadata
- Defect ID: TESTVDB-MILVUS-15
- defect_id (script): boundary_r2_partition_alias_index_name_06
- Type: Type1_IllegalSuccess
- Endpoint: POST /v2/vectordb/partitions/create（对照 aliases/create、indexes/create）
- Param: partitionName（param_name: partitionName）
- Novelty: NOVEL（gate, no_known_hits, confidence HIGH）
- Evidence Weight: MODERATE（弱锚 + by_design 抗辩强——chain-auditor 建议主进程人工复核）

## Reproduction (curl)
```bash
curl -s -X POST "http://localhost:19530/v2/vectordb/partitions/create" \
  -H "Content-Type: application/json" \
  -d '{"collectionName":"<coll>","partitionName":"1bad"}'
```

## Expected vs Actual
- Expected: 资源命名规则 ^[A-Za-z_][A-Za-z0-9_]*$（limitations.md Resource Naming Rules 覆盖 collection/field/partition/alias/db 名）
- Actual（三资源矩阵）：partition 通道选择性缺失——
  - `partitions+create '1bad' -> ok=True raw={"code":0,"data":{}}`（数字开头漏拒）
  - `partitions+create 'my-bad' -> ok=True raw={"code":0,"data":{}}`（连字符漏拒）
  - 对照 partitions：'@bad' → 65535 'first character of a partition name must be an underscore or letter'；'bad name' → 65535；'b$d' → 65535；'valid_p' → 通过
  - 对照 aliases+create 五值全部 1100 拒；indexes+create 五值全部 65535 拒

## Evidence Chain
- Ring 1 (Contract Clause 契约条款) constraint_id: milvus_type_field_name_rules_001（语义外延至 Resource Naming Rules；chain_broken_at=doc 弱锚，auditor 已裁量采信）
  - assertion: `field names: ^[A-Za-z_][A-Za-z0-9_]*$, length<=255, enforced at insert-time (dynamic fields included)`；api_violates_assertion=true（相对外延规则）
- Ring 2 (Document Reference 文档引用) doc_verification: DOC_PARTIAL（字段名约束原文未逐字覆盖 partition 首字符规则差异；link PARTIAL）
- Ring 3 (Actual Behavior 实际行为, HTTP Response 见 log) Script: debate_logs/boundary_r2_partition_alias_index_name_06.py（三资源 × 5 非法名矩阵；单脚本）
- Log: debate_logs/output_boundary_r2_partition_alias_index_name_06.log

### 源码 文件:行号+摘录
- internal/proxy/util.go validatePartitionTag L323-354：
  - L338 首字符条件含 `!isNumber(firstChar)`——数字开头 '1bad' 合法通过（对照 validateFieldName L370 与 alias/index 校验均无 isNumber）
  - L346 循环内 `c != '-'`——连字符 'my-bad' 通过，而错误消息宣称 "Partition name can only contain numbers, letters and underscores."（消息与实现矛盾，误导诊断）
  - util_test.go L135-159 固化这些行为（assert validatePartitionTag("123abc", true)==Nil 等）——测试固化的历史行为而非注释声明的 by-design
- 三资源规则不一致：partition 走 validatePartitionTag（放宽），alias/index 走各自校验（严格）

## Impact
同一命名规则在三类资源上一严两松：partition 接受数字开头与连字符名，alias/index 拒绝。跨资源引用（如按命名约定生成 partition/alias 名）时出现不对称失败；且 partition 的拒绝消息与实现不符（称不含 '-' 实则允许），诊断误导独立成立（Type2 成分）。

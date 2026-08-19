# 人工判定包（盲判）

任务：对下面 22 个 candidate，独立判定它是 **CONFIRMED**（真缺陷）还是 **FALSE_POSITIVE**。
判据（严格）：观察是否**违反了文档契约**，或显示**内部不一致**（如同输入 REST 接受/gRPC 拒绝；文档限制被忽略；数据被静默损坏；文档的错误约定返回成功）。其余（设计上合理 / 文档没承诺报告所声称的 / 观察不构成矛盾 / 证据不足）判 FALSE_POSITIVE。

- 每条只看「契约声明 + 观察证据」，**不要**考虑别的。
- 你看不到 GT、看不到任何模型判定——纯盲判。
- 在每条的方框里打勾：[X] CONFIRMED 或 [X] FALSE_POSITIVE。
- 边界 case 凭直觉给一个，不用纠结。

建议用时 ~20 分钟。

---

## Case 1: milvus#52309

**Title**: [Bug]: REST API v2 `entities/search` accepts `group_size=0` and `-1` (gRPC rejects as "negative")

**Contract claimed in the report**: Grouping Search docs: group_size controls 'number of results to return per group'.

**Probe observations**:
[c1] REST search with groupSize=0 -> http=200, code=0
  [c1_grpc] gRPC search with group_size=0 -> MilvusException code=1100, message: metric type not match: expected=COSINE, actual=L2
  [c2] REST search with groupSize=-1 -> http=200, code=0

**判定**:  [ ] CONFIRMED     [ ] FALSE_POSITIVE

**一句话理由（可选）**: __________________________________
---

## Case 2: weaviate#11743

**Title**: text property accepts strings containing NUL bytes (\x00) without validation

**Contract claimed in the report**: text should hold valid printable text; NUL (U+0000) is a control char that truncates in C-string paths and can corrupt the inverted index (CWE-158).

**Probe observations**:
[c1] POST schema with text property -> http=200
  [c2] POST object with raw NUL byte in text_field -> http=400, id=None

**判定**:  [ ] CONFIRMED     [ ] FALSE_POSITIVE

**一句话理由（可选）**: __________________________________
---

## Case 3: weaviate#11737

**Title**: date accepts year 0000 and pre-1970 values without proper RFC3339 validation

**Contract claimed in the report**: date datatype documented as RFC3339; RFC 3339 / ISO 8601 forbids year 0000; pre-epoch values risk timestamp overflow.

**Probe observations**:
[c1] POST schema with date property -> http=200
  [c2] POST object with date_field='0000-01-01T00:00:00Z' (year 0000) -> http=200
  [c3] POST object with date_field='1800-06-15T08:30:00Z' (pre-epoch) -> http=200

**判定**:  [ ] CONFIRMED     [ ] FALSE_POSITIVE

**一句话理由（可选）**: __________________________________
---

## Case 4: qdrant#9039

**Title**: Bug: Async upsert silently discards dimension-mismatched vectors (Poor Diagnostics)

**Contract claimed in the report**: Issue body: wait=true returns 400 with 'Vector dimension error', wait=false returns 200 'acknowledged' while discarding the point; acknowledged means received by WAL, not validated/stored.

**Probe observations**:
[c1] async 3-dim upsert -> status=200 body={"result":{"operation_id":1,"status":"acknowledged"},"status":"ok","time":0.000208958} count_after=0 (http_status=200)
  [c2] sync(wait=true) 3-dim upsert -> status=400 body='{"status":{"error":"Wrong input: Vector dimension error: expected dim: 4, got 3"},"time":0.006035594}' (http_status=400)

**判定**:  [ ] CONFIRMED     [ ] FALSE_POSITIVE

**一句话理由（可选）**: __________________________________
---

## Case 5: qdrant#9869

**Title**: Write operations accept `timeout=0` despite the OpenAPI schema declaring `minimum: 1`

**Contract claimed in the report**: Issue body: OpenAPI declares timeout as integer minimum:1; server accepts 0 with 200 on set payload/delete/create/update vectors — schema/code discrepancy.

**Probe observations**:
[c1] set payload timeout=0 -> status=200 body='{"result":{"operation_id":2,"status":"acknowledged"},"status":"ok","time":0.000219438}' (accepted, schema minimum:1 not enforced, BUG) (http_status=200)
  [c2] set payload timeout=1 -> status=200 (control) (http_status=200)

**判定**:  [ ] CONFIRMED     [ ] FALSE_POSITIVE

**一句话理由（可选）**: __________________________________
---

## Case 6: weaviate#11736

**Title**: blob accepts long non-base64 garbage string without validation

**Contract claimed in the report**: Weaviate docs: blob datatype is a 'base64 encoded string'; garbage that decodes to meaningless bytes should be rejected.

**Probe observations**:
[c1] POST schema with blob property -> http=200
  [c2] POST object blob_field=<100 'x' chars> -> http=200, stored_id=78e82acf-9560-45ca-a5c8-fa5fc566cb93

**判定**:  [ ] CONFIRMED     [ ] FALSE_POSITIVE

**一句话理由（可选）**: __________________________________
---

## Case 7: milvus#50351

**Title**: [Bug]: REST API v2: shardsNum=0/-1/65535 accepted with HTTP 200 + code=200

**Contract claimed in the report**: Issue: REST docs/PyMilvus default num_shards=1 implies min 1; invalid values return success code.

**Probe observations**:
[c0] create with shardsNum=0 -> http=200, code=0
  [c1] create with shardsNum=-1 -> http=200, code=0
  [c2] create with shardsNum=65535 -> http=200, code=0

**判定**:  [ ] CONFIRMED     [ ] FALSE_POSITIVE

**一句话理由（可选）**: __________________________________
---

## Case 8: qdrant#9523

**Title**: Search offset pagination returns duplicate point IDs across pages (HNSW approximation)

**Contract claimed in the report**: Issue body: offset pagination with HNSW is non-deterministic; scroll cursor pagination does not have this problem.

**Probe observations**:
[c1] page1 offset=0 ids=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9] (http_status=200)
  [c2] page2 offset=10 ids=[10, 11, 12, 13, 14, 15, 16, 17, 18, 19] overlap_with_p1=[] (http_status=200)
  [c3] page3 offset=20 ids=[20, 21, 22, 23, 24] unique_union=25 duplicate_sets=[] (http_status=200)
  [c4] scroll control ids=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9] (non-overlapping cursor) (http_status=200)

**判定**:  [ ] CONFIRMED     [ ] FALSE_POSITIVE

**一句话理由（可选）**: __________________________________
---

## Case 9: qdrant#9372

**Title**: Strict mode inconsistently validates zero values — allows creation of unusable collections

**Contract claimed in the report**: Issue body: consistency matrix shows 3 fields reject 0 (422) while filter_max_conditions and upsert_max_batchsize accept 0 (200) producing a poisoned collection.

**Probe observations**:
[c1] create with max_query_limit=0 -> status=422
  [c2] create with filter_max_conditions=0 -> status=200; filtered scroll -> status=400, body: Filter condition limit reached (1 > 0)
  [c3] create with upsert_max_batchsize=0 -> status=200; upsert -> status=400, body: Limit exceeded 1 > 0 for upsert limit

**判定**:  [ ] CONFIRMED     [ ] FALSE_POSITIVE

**一句话理由（可选）**: __________________________________
---

## Case 10: weaviate#11738

**Title**: phoneNumber.defaultCountry accepts invalid ISO 3166-1 alpha-2 code "ZZ"

**Contract claimed in the report**: phoneNumber.defaultCountry documented as 'ISO 3166-1 alpha-2 country code'; ZZ is not assigned to any country.

**Probe observations**:
[c1] POST schema with phoneNumber property -> http=200
  [c2] POST object with phone.defaultCountry=ZZ -> http=200

**判定**:  [ ] CONFIRMED     [ ] FALSE_POSITIVE

**一句话理由（可选）**: __________________________________
---

## Case 11: milvus#50323

**Title**: [Bug]: Delete endpoint accepts both filter and ids (mutually exclusive) silently

**Contract claimed in the report**: accepted for triage.

**Probe observations**:
[c1] delete with both filter and ids -> http=200, code=0

**判定**:  [ ] CONFIRMED     [ ] FALSE_POSITIVE

**一句话理由（可选）**: __________________________________
---

## Case 12: milvus#47767

**Title**: [Bug]: Empty query vector accepted in search - no validation error

**Contract claimed in the report**: Java SDK withDimension: 'dimension must be greater than zero'; dense vectors are fixed-length arrays.

**Probe observations**:
[c1] empty query vector -> MilvusException code=65535 (server message: ...vector type must be the same, field vector - type VECTOR_FLOAT, search info type VECTOR_SPARSE_U32_F32...)

**判定**:  [ ] CONFIRMED     [ ] FALSE_POSITIVE

**一句话理由（可选）**: __________________________________
---

## Case 13: milvus#49849

**Title**: [Bug]: REST API v2 insert returns insertCount=1 for duplicate primary key (upsert semantics)

**Contract claimed in the report**: Issue: 'The endpoint is called insert, not upsert. When insert reports success with insertCount=1, expectation is a new row was added.'

**Probe observations**:
[c1] duplicate-PK insert (overwrite) -> http=200, code=0, insertCount=1
  [c1_rb] query id=1 after overwrite -> http=200, code=0, data: id=1 vector=[0.9,0.8,0.7,0.6]

**判定**:  [ ] CONFIRMED     [ ] FALSE_POSITIVE

**一句话理由（可选）**: __________________________________
---

## Case 14: weaviate#11730

**Title**: tokenization accepts empty string despite explicit OpenAPI enum constraint

**Contract claimed in the report**: OpenAPI schema.json Property.tokenization defines an explicit enum of 9 values; empty string not among them.

**Probe observations**:
[c1] POST schema with tokenization='' -> http=200

**判定**:  [ ] CONFIRMED     [ ] FALSE_POSITIVE

**一句话理由（可选）**: __________________________________
---

## Case 15: milvus#49889

**Title**: [Bug]: REST API v2 accepts empty string for `dbName` parameter

**Contract claimed in the report**: REST v2 List: 'dbName: The name of an existing database.'

**Probe observations**:
[c1] collections/list with dbName empty -> http=200, code=0
  [c2] control: query with filter='' -> http=200, code=100

**判定**:  [ ] CONFIRMED     [ ] FALSE_POSITIVE

**一句话理由（可选）**: __________________________________
---

## Case 16: milvus#50319

**Title**: [Bug]: Search on unloaded collection returns valid results (code=0)

**Contract claimed in the report**: (报告未引用具体文档契约)

**Probe observations**:
[c1] search on never-loaded collection -> http=200, code=0

**判定**:  [ ] CONFIRMED     [ ] FALSE_POSITIVE

**一句话理由（可选）**: __________________________________
---

## Case 17: qdrant#9017

**Title**: hnsw_ef accepts 0

**Contract claimed in the report**: Issue body: hnsw_ef of 0 means 'consider zero candidates'; the OpenAPI/schema pattern validates limit>=1 and offset>=0, and SearchParams.hnsw_ef has no minimum.

**Probe observations**:
[c1] hnsw_ef=0 search -> status=200, 1 results (accepted, BUG) (http_status=200)

**判定**:  [ ] CONFIRMED     [ ] FALSE_POSITIVE

**一句话理由（可选）**: __________________________________
---

## Case 18: milvus#50353

**Title**: [Bug]: REST API v2: search returns HTTP 200 for limit=0/-1 and dimension mismatch

**Contract claimed in the report**: Issue: REST returns HTTP 200 for all invalid search params; errors only in JSON body.

**Probe observations**:
[c1] search with limit=0 -> http=200, code=65535
  [c2] search 64-dim vector on dim=4 collection -> http=200, code=1801

**判定**:  [ ] CONFIRMED     [ ] FALSE_POSITIVE

**一句话理由（可选）**: __________________________________
---

## Case 19: weaviate#11660

**Title**: REST API GET /v1/objects silently accepts negative limit parameter

**Contract claimed in the report**: OpenAPI documents limit as integer max 10000 (QUERY_MAXIMUM_RESULTS); a non-negative invariant is implied. GraphQL path validates limit; REST list endpoint does not.

**Probe observations**:
[c1] GET /v1/objects?limit=-1 -> http=200, body: objects=[]

**判定**:  [ ] CONFIRMED     [ ] FALSE_POSITIVE

**一句话理由（可选）**: __________________________________
---

## Case 20: weaviate#11981

**Title**: POST /v1/batch/objects accepts empty vector `[]` and reports per-item SUCCESS (singular POST /v1/objects rejects with 422)

**Contract claimed in the report**: data_types.vector documented as non-empty float array (min_length=1); singular POST enforces vector:[] -> 422; batch path reports SUCCESS for empty-vector item.

**Probe observations**:
[c1] POST schema BatchVectorBugRepro -> http=200
  [c2] control: singular POST with vector=[] -> http=200
  [c3] batch with empty-vector item -> http=200, per-item statuses=None

**判定**:  [ ] CONFIRMED     [ ] FALSE_POSITIVE

**一句话理由（可选）**: __________________________________
---

## Case 21: milvus#52312

**Title**: [Bug]: REST API v2 `entities/upsert` accepts string numbers for Int64 primary key (gRPC rejects)

**Contract claimed in the report**: Primary Field docs define Int64 as numeric; same coercion gap as insert (higher risk on upsert).

**Probe observations**:
[c1] REST upsert string PK '100' -> http=200, code=0
  [c1_q] query id=100 after string-PK upsert -> http=200, code=0, data: id=100 vector=[0.9,0.9,0.9,0.9]
  [c1_grpc] gRPC upsert string PK -> DataNotMatchException code=1, message: id field should be int64, got str

**判定**:  [ ] CONFIRMED     [ ] FALSE_POSITIVE

**一句话理由（可选）**: __________________________________
---

## Case 22: qdrant#9149

**Title**: shard_number=0 and negative values accepted during collection creation

**Contract claimed in the report**: Issue body: shard_number=0 creates a collection with zero shards; other params in the same endpoint have validation (e.g. vectors.size upper bound).

**Probe observations**:
[c1] shard_number=0 create -> status=422 (rejected, FIX) (http_status=422)
  [c2] shard_number=-1 create -> status=400 (rejected, FIX) (http_status=400)

**判定**:  [ ] CONFIRMED     [ ] FALSE_POSITIVE

**一句话理由（可选）**: __________________________________
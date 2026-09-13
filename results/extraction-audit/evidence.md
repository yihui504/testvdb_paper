# A1 · 抽取阶段审计 — 证据汇编

约束 152 条；引用页 25 个（捕获成功 23）。
判定列在 `worksheet.csv` 中留空，由人填写。`triage.csv` 的术语命中数只是检索线索，不是判定。

## `https://api.qdrant.tech/v-1-18-x/api-reference`

- 性质：**vendor-documentation**｜URL 版本片段：—｜实例 462｜引用该页的约束 27 条
- 捕获：`pages_text/api.qdrant.tech_v-1-18-x_api-reference.txt`

- **qdrant_behavioral_002** 〔qdrant / collections+{collection_name}〕
  - description: 200 on success; 404 if collection not found
- **qdrant_behavioral_004** 〔qdrant / collections+{collection_name}+exists〕
  - description: Returns {'result': {'exists': true/false}}
- **qdrant_behavioral_006** 〔qdrant / collections+{collection_name}+points〕
  - description: 200 with matching points (missing IDs are silently omitted)
- **qdrant_behavioral_007** 〔qdrant / collections+{collection_name}+points+delete〕
  - description: 200 on success; 400 if neither points nor filter provided
- **qdrant_behavioral_009** 〔qdrant / collections+{collection_name}+points+scroll〕
  - description: 200 with points list and next_page_offset for pagination
- **qdrant_behavioral_010** 〔qdrant / collections+{collection_name}+points+count〕
  - description: 200 with count result
- **qdrant_behavioral_011** 〔qdrant / collections+{collection_name}+points+query〕
  - description: 200 with result points; supports multi-stage query pipeline via prefetch
- **qdrant_behavioral_012** 〔qdrant / collections+{collection_name}+points+recommend〕
  - description: 200 with ranked results
- **qdrant_behavioral_013** 〔qdrant / collections+{collection_name}+index〕
  - description: 200 on success; 4XX on invalid field name or field type
- **qdrant_behavioral_014** 〔qdrant / collections+{collection_name}+index+{field_name}〕
  - description: 200 on success; 404 if index not found
- **qdrant_behavioral_015** 〔qdrant / collections+aliases〕
  - description: 200 on success; 4XX on invalid operations
- **qdrant_behavioral_017** 〔qdrant / collections〕
  - description: 200 with list of collections
- **qdrant_range_query_points_008** 〔qdrant / collections+{collection_name}+points+query〕
  - assertion: `limit default=10 for query endpoint.`
  - description: limit default=10
- **qdrant_range_recommend_009** 〔qdrant / collections+{collection_name}+points+recommend〕
  - assertion: `strategy IN (average_vector, best_score, sum_scores)`
  - description: strategy must be one of: average_vector, best_score, sum_scores
- **qdrant_range_scroll_points_005** 〔qdrant / collections+{collection_name}+points+scroll〕
  - assertion: `limit default=10`
  - description: limit default=10 (adjustable)
- **qdrant_range_search_groups_007** 〔qdrant / collections+{collection_name}+points+search+groups〕
  - assertion: `group_size >= 1 AND limit >= 1`
  - description: group_size >= 1; limit >= 1
- **qdrant_state_batch_update_007** 〔qdrant / collections+{collection_name}+points+batch〕
  - assertion: `Batch update operations are executed atomically.`
  - description: All operations in batch are executed atomically
- **qdrant_state_count_points_008** 〔qdrant / collections+{collection_name}+points+count〕
  - assertion: `exact=true performs a full scan; exact=false uses segment statistics.`
  - description: exact=true performs full scan; exact=false uses segment statistics
- **qdrant_state_create_index_011** 〔qdrant / collections+{collection_name}+index〕
  - assertion: `Index creation is asynchronous; query optimization applies after the index is built.`
  - description: Index creation is async; query optimization applies after index is built
- **qdrant_state_delete_collection_003** 〔qdrant / collections+{collection_name}〕
  - assertion: `Collection deletion permanently removes the collection and all its data.`
  - description: Destructive operation - permanently deletes collection and all its data
- **qdrant_state_delete_points_005** 〔qdrant / collections+{collection_name}+points+delete〕
  - assertion: `Point deletion is atomic for the matched set.`
  - description: Deletion is atomic for the matched set
- **qdrant_state_query_points_010** 〔qdrant / collections+{collection_name}+points+query〕
  - assertion: `prefetch queries execute first, then the final query runs on combined results.`
  - description: prefetch queries execute first, then final query runs on combined results
- **qdrant_state_remove_peer_013** 〔qdrant / cluster+peer+{peer_id}〕
  - assertion: `force=true should only be used when peer is unreachable.`
  - description: Destructive cluster operation; force=true only when peer is unreachable
- **qdrant_state_update_aliases_012** 〔qdrant / collections+aliases〕
  - assertion: `All alias operations in a single request are applied atomically.`
  - description: All alias operations in a single request are applied atomically
- **qdrant_state_update_collection_002** 〔qdrant / collections+{collection_name}〕
  - assertion: `Update blocks until current optimizations complete.`
  - description: Blocking operation - waits for current optimizations to complete
- **qdrant_type_overwrite_payload_004** 〔qdrant / collections+{collection_name}+points+payload〕
  - assertion: `PUT payload replaces the entire payload; it does not merge.`
  - description: Overwrite replaces entire payload, not merged
- **qdrant_type_update_collection_002** 〔qdrant / collections+{collection_name}〕
  - assertion: `At least one update field must be provided.`
  - description: All update fields are optional; at least one must be provided

## `https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go`

- 性质：**implementation-source**｜URL 版本片段：2.6.17｜实例 312｜引用该页的约束 29 条
- 捕获：`pages_text/github.com_milvus-io_milvus_blob_v2.6.17_internal_distributed_proxy_httpserver_constant.go.txt`（实际取自 `https://raw.githubusercontent.com/milvus-io/milvus/v2.6.17/internal/distributed/proxy/httpserver/constant.go`）

- **milvus_behavioral_collections_get_stats_001** 〔milvus / collections+get_stats〕
  - description: Get stats returns row count and statistics
- **milvus_behavioral_collections_has_001** 〔milvus / collections+has〕
  - description: Has collection returns boolean indicating existence
- **milvus_behavioral_entities_delete_001** 〔milvus / entities+delete〕
  - description: Delete returns 400 on invalid filter expression
- **milvus_behavioral_entities_insert_001** 〔milvus / entities+insert〕
  - description: Insert returns insert count and IDs on success
- **milvus_behavioral_entities_insert_002** 〔milvus / entities+insert〕
  - description: Insert returns 400 on schema mismatch
- **milvus_behavioral_hybrid_search_001** 〔milvus / entities+hybrid_search〕
  - description: Hybrid search returns 400 on invalid rerank strategy
- **milvus_behavioral_indexes_create_001** 〔milvus / indexes+create〕
  - description: Create index returns 400 on invalid index type
- **milvus_behavioral_users_create_001** 〔milvus / users+create〕
  - description: Create user returns 400 if password too weak or user already exists
- **milvus_range_entities_insert_001** 〔milvus / entities+insert〕
  - assertion: `len(data) <= 100`
  - description: Max 100 entities per single insert call via REST API
- **milvus_range_entities_insert_002** 〔milvus / entities+insert〕
  - assertion: `vector dimension == collection dimension`
  - description: Vector dimension must match collection dimension
- **milvus_range_entities_query_001** 〔milvus / entities+query〕
  - assertion: `limit + offset < 16384`
  - description: limit + offset must be < 16384
- **milvus_range_hybrid_search_001** 〔milvus / entities+hybrid_search〕
  - assertion: `total results < 16384`
  - description: total results must be < 16384
- **milvus_range_indexes_create_001** 〔milvus / indexes+create〕
  - assertion: `nlist >= 1`
  - description: nlist must be >= 1
- **milvus_range_indexes_create_002** 〔milvus / indexes+create〕
  - assertion: `4 <= M <= 64`
  - description: M (HNSW) must be 4-64
- **milvus_range_indexes_create_003** 〔milvus / indexes+create〕
  - assertion: `efConstruction >= 1`
  - description: efConstruction >= 1
- **milvus_range_users_create_001** 〔milvus / users+create〕
  - assertion: `8 <= len(password) <= 64`
  - description: password must be 8-64 characters
- **milvus_state_databases_drop_001** 〔milvus / databases+drop〕
  - assertion: `dbName != '_default' AND database has no collections`
  - description: Cannot drop the default database; database must be empty (no collections)
- **milvus_state_entities_delete_001** 〔milvus / entities+delete〕
  - assertion: `delete is irreversible`
  - description: Deleted entities cannot be recovered
- **milvus_state_entities_insert_001** 〔milvus / entities+insert〕
  - assertion: `collection exists AND is loaded AND (autoID OR primary key provided)`
  - description: Collection must exist and be loaded; if autoID is disabled, primary key must be provided
- **milvus_state_entities_upsert_001** 〔milvus / entities+upsert〕
  - assertion: `upsert: update if PK exists, insert if NOT; collection has PK defined`
  - description: If primary key exists, entity is updated; if not, inserted. Collection must have a primary key defined
- **milvus_state_entities_upsert_002** 〔milvus / entities+upsert〕
  - assertion: `for updates: PK value matches existing entity PK`
  - description: Primary key must match existing entity's key for updates
- **milvus_state_indexes_create_001** 〔milvus / indexes+create〕
  - assertion: `collection exists AND field exists in schema`
  - description: Collection must exist; field must exist in schema
- **milvus_type_entities_delete_001** 〔milvus / entities+delete〕
  - assertion: `filter is a valid boolean expression`
  - description: filter must be a valid boolean expression string
- **milvus_type_entities_insert_001** 〔milvus / entities+insert〕
  - assertion: `data field types match collection schema`
  - description: data must contain field values matching collection schema data types
- **milvus_type_entities_query_001** 〔milvus / entities+query〕
  - assertion: `filter is a valid boolean expression`
  - description: filter must be a valid boolean expression string
- **milvus_type_entities_upsert_001** 〔milvus / entities+upsert〕
  - assertion: `data contains primary key field`
  - description: Primary key field must be specified in data for upsert
- **milvus_type_hybrid_search_001** 〔milvus / entities+hybrid_search〕
  - assertion: `len(search) >= 2`
  - description: search array must contain at least 2 elements for hybrid search
- **milvus_type_indexes_create_001** 〔milvus / indexes+create〕
  - assertion: `metricType is valid for field AND index_type in supported list`
  - description: metricType must be valid for the field type; index_type must be one of the supported types
- **milvus_type_users_create_001** 〔milvus / users+create〕
  - assertion: `userName is non-empty string`
  - description: userName must be a non-empty string

## `https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md`

- 性质：**vendor-documentation**｜URL 版本片段：2.6｜实例 261｜引用该页的约束 12 条
- 捕获：`pages_text/milvus.io_api-reference_restful_v2.6.x_v2_Collection_20_v2_Create.md.txt`

- **milvus_behavioral_collections_create_001** 〔milvus / collections+create〕
  - description: Create collection returns 200 on success
- **milvus_behavioral_collections_create_002** 〔milvus / collections+create〕
  - description: Create collection returns 400 on invalid parameters or duplicate name
- **milvus_behavioral_collections_describe_001** 〔milvus / collections+describe〕
  - description: Describe collection returns collection schema on success
- **milvus_range_collections_create_001** 〔milvus / collections+create〕
  - assertion: `1 <= dimension <= 32768`
  - description: dimension must be 1-32768 for FloatVector
- **milvus_range_collections_create_002** 〔milvus / collections+create〕
  - assertion: `shardsNum >= 1`
  - description: shardsNum must be >= 1
- **milvus_range_collections_create_003** 〔milvus / collections+create〕
  - assertion: `max_length >= 1 && max_length <= 65535`
  - description: VarChar max_length must be between 1 and 65535
- **milvus_range_collections_create_004** 〔milvus / collections+create〕
  - assertion: `ttlSeconds >= 0`
  - description: ttlSeconds must be >= 0
- **milvus_range_collections_create_005** 〔milvus / collections+create〕
  - assertion: `1 <= VarChar.max_length <= 65535`
  - description: VarChar max_length must be 1-65535
- **milvus_state_collections_create_001** 〔milvus / collections+create〕
  - assertion: `collection creation is atomic AND collectionName is unique within dbName`
  - description: Collection creation is atomic; collection name must be unique within a database
- **milvus_type_collections_create_001** 〔milvus / collections+create〕
  - assertion: `collectionName is of type string`
  - description: collectionName must be a string
- **milvus_type_collections_create_002** 〔milvus / collections+create〕
  - assertion: `metricType in ['L2', 'IP', 'COSINE']`
  - description: metricType must be L2, IP, or COSINE
- **milvus_type_collections_create_003** 〔milvus / collections+create〕
  - assertion: `consistencyLevel in ['Strong', 'Session', 'Bounded', 'Eventually']`
  - description: consistencyLevel must be Strong, Session, Bounded, or Eventually

## `https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json`

- 性质：**structured-spec**｜URL 版本片段：1.38.0｜实例 237｜引用该页的约束 35 条
- 捕获：`pages_text/github.com_weaviate_weaviate_blob_v1.38.0_openapi-specs_schema.json.txt`（实际取自 `https://raw.githubusercontent.com/weaviate/weaviate/v1.38.0/openapi-specs/schema.json`）

- **weaviate_behavioral_batch_reject_partial_001** 〔weaviate / POST /batch/objects〕
  - description: 429 WHOLE BATCH rejected (no partial fill)
- **weaviate_behavioral_index_update_001** 〔weaviate / /schema/{className}/indexes/{propertyName} PUT〕
  - description: downgrading from blockmax algorithm is rejected
- **weaviate_behavioral_objects_create_001** 〔weaviate / /objects POST〕
  - description: POST with existing id fails; should return error not overwrite
- **weaviate_behavioral_objects_create_002** 〔weaviate / /objects POST〕
  - description: exceeding object count usage limit returns 429
- **weaviate_behavioral_post_object_exists_001** 〔weaviate / POST /objects〕
  - description: POST fails with error if id already exists (use PUT to replace or PATCH to update)
- **weaviate_behavioral_schema_create_001** 〔weaviate / /schema POST〕
  - description: creating collection with disallowed vectorIndexType returns 422 RestrictionViolationResponse
- **weaviate_behavioral_schema_create_002** 〔weaviate / /schema POST〕
  - description: exceeding collections/shards usage limit returns 429 UsageLimitExceededResponse
- **weaviate_behavioral_tenants_create_001** 〔weaviate / /schema/{className}/tenants POST〕
  - description: exceeding tenant usage limit returns 429 with limit: tenants
- **weaviate_range_batch_delete_001** 〔weaviate / /batch/objects DELETE;DELETE /batch/objects〕
  - assertion: `deleted count <= QUERY_MAXIMUM_RESULTS`
  - description: max deletions per request = QUERY_MAXIMUM_RESULTS (default 10000)
- **weaviate_range_objects_list_001** 〔weaviate / /objects GET〕
  - assertion: `offset + limit <= 10000`
  - description: offset+limit must not exceed QUERY_MAXIMUM_RESULTS (default 10000)
- **weaviate_range_replication_scale_001** 〔weaviate / /replication/scale GET〕
  - assertion: `replicationFactor >= 1`
  - description: replicationFactor must be at least 1
- **weaviate_range_schema_replication_001** 〔weaviate / /schema POST〕
  - assertion: `replicationConfig.factor >= 1`
  - description: replicationConfig.factor is an integer (default 1)
- **weaviate_state_batch_idempotent_001** 〔weaviate / POST /batch/objects〕
  - assertion: `batch create is idempotent; existing UUIDs are replaced`
  - description: idempotent by UUID -- existing UUIDs overwritten (PUT semantics per item)
- **weaviate_state_batch_objects_001** 〔weaviate / /batch/objects POST〕
  - assertion: `POST /batch/objects with existing UUID overwrites rather than errors`
  - description: batch is idempotent by UUID; existing UUIDs are overwritten (PUT semantics per item)
- **weaviate_state_batch_reject_all_001** 〔weaviate / POST /batch/objects〕
  - assertion: `usage limit exceeded rejects entire batch, no partial success`
  - description: 429 WHOLE BATCH rejected (no partial fill)
- **weaviate_state_index_update_001** 〔weaviate / /schema/{className}/indexes/{propertyName} PUT〕
  - assertion: `PUT returns 202 (submitted) | 409 (conflict) | 503 (disabled)`
  - description: index update triggers async reindex (202); 409 if conflicting reindex running; 503 if distributed tasks disabled
- **weaviate_state_objects_create_001** 〔weaviate / /objects POST〕
  - assertion: `POST /objects returns error if id exists; PUT/PATCH required to update`
  - description: POST fails if id already exists; use PUT/PATCH to update
- **weaviate_state_objects_list_001** 〔weaviate / /objects GET〕
  - assertion: `(after provided) implies (offset == 0 and sort not provided)`
  - description: after cursor is mutually exclusive with offset and sort
- **weaviate_state_schema_delete_001** 〔weaviate / /schema/{className} DELETE〕
  - assertion: `after DELETE /schema/{className}, GET /objects?class={className} returns empty`
  - description: deleting a collection permanently deletes all data objects in the collection
- **weaviate_state_schema_update_001** 〔weaviate / /schema/{className} PUT〕
  - assertion: `PUT /schema/{className} does not change properties count or names`
  - description: PUT does NOT add properties (use POST /schema/{className}/properties) and does NOT rename
- **weaviate_state_tenants_delete_001** 〔weaviate / /schema/{className}/tenants DELETE〕
  - assertion: `after DELETE tenants, GET tenant returns 404 and its data is gone`
  - description: deleting tenants permanently deletes all tenant data
- **weaviate_type_backups_create_001** 〔weaviate / /backups/{backend} POST〕
  - assertion: `body.id matches /^[a-z0-9_-]+$/`
  - description: backup id must be URL-safe (lowercase, numbers, underscore, minus only)
- **weaviate_type_batch_references_001** 〔weaviate / /batch/references POST〕
  - assertion: `from matches /^weaviate:\/\/localhost\/{ClassName}\/{uuid}\/{propertyName}$/`
  - description: from beacon format must include className/uuid/propertyName
- **weaviate_type_index_update_001** 〔weaviate / /schema/{className}/indexes/{propertyName} PUT〕
  - assertion: `body.searchable.algorithm == 'blockmax'`
  - description: searchable.algorithm must be blockmax (WAND->BlockMax migration only; downgrade rejected)
- **weaviate_type_namespaces_create_001** 〔weaviate / /namespaces/{namespace_id} POST〕
  - assertion: `namespace_id matches /^[a-z0-9][a-z0-9-]{1,34}[a-z0-9]$/`
  - description: namespace name must be lowercase letters, digits, hyphens; 3-36 chars; start/end with letter or digit
- **weaviate_type_object_id_001** 〔weaviate / POST /objects〕
  - assertion: `id matches UUID regex (version 4 or 7)`
  - description: id must be valid UUID format (v4 or v7)
- **weaviate_type_object_vector_001** 〔weaviate / POST /objects〕
  - assertion: `vector is array of number (float)`
  - description: vector must be array of floats
- **weaviate_type_objects_create_001** 〔weaviate / /objects POST〕
  - assertion: `body.id is null OR matches UUID format`
  - description: id field must be valid UUID format
- **weaviate_type_objects_create_002** 〔weaviate / /objects POST〕
  - assertion: `if body.vector provided, it overrides vectorizer-generated vector`
  - description: vector takes precedence over vectorizer module
- **weaviate_type_references_add_001** 〔weaviate / /objects/{className}/{id}/references/{propertyName} POST〕
  - assertion: `body.beacon matches /^weaviate:\/\/localhost\/[0-9a-f-]{36}$/`
  - description: beacon format must be weaviate://localhost/{uuid}
- **weaviate_type_schema_create_001** 〔weaviate / /schema POST〕
  - assertion: `properties.class matches /^[A-Z][a-zA-Z0-9]*$/`
  - description: class field must be CamelCase
- **weaviate_type_schema_create_002** 〔weaviate / /schema POST〕
  - assertion: `properties.vectorIndexType in {hnsw, flat, dynamic, bwes}`
  - description: vectorIndexType must be one of allowed index types
- **weaviate_type_schema_create_003** 〔weaviate / /schema POST〕
  - assertion: `properties.properties[].tokenization in {word, lowercase, whitespace, field, trigram, gse, kagome_kr, kagome_ja, gse_ch}`
  - description: properties[].tokenization must be a valid enum value
- **weaviate_type_tenants_create_001** 〔weaviate / /schema/{className}/tenants POST〕
  - assertion: `body[].activityStatus in {ACTIVE, INACTIVE}`
  - description: Tenant.activityStatus on create must be ACTIVE or INACTIVE
- **weaviate_type_tenants_update_001** 〔weaviate / /schema/{className}/tenants PUT〕
  - assertion: `body[].activityStatus in {ACTIVE, INACTIVE, OFFLOADED}`
  - description: Tenant.activityStatus on update must be ACTIVE, INACTIVE, or OFFLOADED

## `https://api.qdrant.tech/v-1-18-x/api-reference/collections/create-collection`

- 性质：**vendor-documentation**｜URL 版本片段：—｜实例 161｜引用该页的约束 7 条
- 捕获：`pages_text/api.qdrant.tech_v-1-18-x_api-reference_collections_create-collection.txt`

- **qdrant_behavioral_001** 〔qdrant / collections+{collection_name}〕
  - description: 200 on success; 4XX on invalid params or collection already exists
- **qdrant_range_create_collection_001** 〔qdrant / collections+{collection_name}〕
  - assertion: `shard_number >= 1`
  - description: shard_number minimum=1
- **qdrant_range_create_collection_002** 〔qdrant / collections+{collection_name}〕
  - assertion: `replication_factor >= 1`
  - description: replication_factor minimum=1
- **qdrant_range_create_collection_003** 〔qdrant / collections+{collection_name}〕
  - assertion: `write_consistency_factor >= 1`
  - description: write_consistency_factor minimum=1
- **qdrant_range_create_collection_004** 〔qdrant / collections+{collection_name}〕
  - assertion: `timeout >= 1`
  - description: timeout minimum=1
- **qdrant_state_create_collection_001** 〔qdrant / collections+{collection_name}〕
  - assertion: `After 200 response the collection exists with the configuration as submitted; collections without vector config support payload-only operations (vector insert returns an error at use time)`
  - description: Atomic collection creation: after 200 response, collection is fully initialized and ready for operations
- **qdrant_type_create_collection_001** 〔qdrant / collections+{collection_name}〕
  - assertion: `collection_name type is string`
  - description: collection_name is string

## `https://milvus.io/api-reference/restful/v2.6.x/v2/Vector%20(v2)/Search.md`

- 性质：**vendor-documentation**｜URL 版本片段：2.6｜实例 147｜引用该页的约束 5 条
- 捕获：`pages_text/milvus.io_api-reference_restful_v2.6.x_v2_Vector_20_v2_Search.md.txt`

- **milvus_behavioral_entities_search_001** 〔milvus / entities+search〕
  - description: Search returns 400 on vector dimension mismatch
- **milvus_range_entities_search_001** 〔milvus / entities+search〕
  - assertion: `vector dimension == collection dimension`
  - description: vector dimensions in data must match collection vector dimension
- **milvus_range_entities_search_002** 〔milvus / entities+search〕
  - assertion: `limit + offset < 16384`
  - description: limit + offset must be < 16384
- **milvus_state_entities_search_001** 〔milvus / entities+search〕
  - assertion: `collection is loaded AND index exists on annsField`
  - description: Collection must be loaded; index must exist on annsField
- **milvus_type_entities_search_001** 〔milvus / entities+search〕
  - assertion: `data is array[array[float]] AND annsField is a vector field AND limit > 0`
  - description: data must be array of float arrays, annsField must be a vector field, limit must be positive integer

## `https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Drop.md`

- 性质：**vendor-documentation**｜URL 版本片段：2.6｜实例 91｜引用该页的约束 3 条
- 捕获：`pages_text/milvus.io_api-reference_restful_v2.6.x_v2_Collection_20_v2_Drop.md.txt`

- **milvus_behavioral_collections_drop_001** 〔milvus / collections+drop〕
  - description: Drop collection returns 200 on success, 404 if not found
- **milvus_state_collections_drop_001** 〔milvus / collections+drop〕
  - assertion: `drop is irreversible AND all data is permanently deleted`
  - description: Drop is irreversible; all data in the collection is permanently deleted
- **milvus_type_collections_drop_001** 〔milvus / collections+drop〕
  - assertion: `collectionName is non-empty string`
  - description: collectionName must be a non-empty string

## `https://api.qdrant.tech/v-1-18-x/api-reference/points/upsert-points`

- 性质：**vendor-documentation**｜URL 版本片段：—｜实例 91｜引用该页的约束 3 条
- 捕获：`pages_text/api.qdrant.tech_v-1-18-x_api-reference_points_upsert-points.txt`

- **qdrant_behavioral_005** 〔qdrant / collections+{collection_name}+points〕
  - description: 200 on success; 4XX on validation error
- **qdrant_state_upsert_points_004** 〔qdrant / collections+{collection_name}+points〕
  - assertion: `Batch upsert is atomic: all points are inserted or none.`
  - description: Atomic batch upsert - all points inserted or none
- **qdrant_type_upsert_points_003** 〔qdrant / collections+{collection_name}+points〕
  - assertion: `id type is integer (uint64) or UUID string; vector type is array of floats or object of named vectors; payload type is key-value object.`
  - description: id is integer (uint64) or UUID string; vector is array of floats or object of named vectors; payload is key-value object

## `https://api.qdrant.tech/v-1-18-x/api-reference/search/points`

- 性质：**vendor-documentation**｜URL 版本片段：—｜实例 85｜引用该页的约束 3 条
- 捕获：`pages_text/api.qdrant.tech_v-1-18-x_api-reference_search_points.txt`

- **qdrant_behavioral_008** 〔qdrant / collections+{collection_name}+points+search〕
  - description: 200 with ranked results descending by score; 4XX on invalid params
- **qdrant_range_search_points_006** 〔qdrant / collections+{collection_name}+points+search〕
  - assertion: `hnsw_ef parameter is applicable only when exact=false.`
  - description: hnsw_ef applicable when exact=false
- **qdrant_state_search_points_009** 〔qdrant / collections+{collection_name}+points+search〕
  - assertion: `When exact=true, search uses brute-force; when exact=false, search uses HNSW.`
  - description: If exact=true, performs brute-force search (slow but accurate); if exact=false, uses HNSW for approximate search

## `https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Load.md`

- 性质：**vendor-documentation**｜URL 版本片段：2.6｜实例 48｜引用该页的约束 2 条
- 捕获：`pages_text/milvus.io_api-reference_restful_v2.6.x_v2_Collection_20_v2_Load.md.txt`

- **milvus_behavioral_collections_load_001** 〔milvus / collections+load〕
  - description: Load collection returns 400 if no index exists
- **milvus_type_collections_load_001** 〔milvus / collections+load〕
  - assertion: `collectionName is non-empty string`
  - description: collectionName must be a non-empty string for load

## `https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Rename.md`

- 性质：**vendor-documentation**｜URL 版本片段：2.6｜实例 45｜引用该页的约束 2 条
- 捕获：`pages_text/milvus.io_api-reference_restful_v2.6.x_v2_Collection_20_v2_Rename.md.txt`

- **milvus_state_collections_rename_001** 〔milvus / collections+rename〕
  - assertion: `source collection exists AND new collection name does NOT exist`
  - description: Collection must exist; new name must not already exist
- **milvus_type_collections_rename_001** 〔milvus / collections+rename〕
  - assertion: `collectionName is non-empty string AND newCollectionName is non-empty string`
  - description: collectionName and newCollectionName must be non-empty strings

## `https://api.qdrant.tech/v-1-18-x/api-reference/points/set-payload`

- 性质：**vendor-documentation**｜URL 版本片段：—｜实例 42｜引用该页的约束 2 条
- 捕获：`pages_text/api.qdrant.tech_v-1-18-x_api-reference_points_set-payload.txt`

- **qdrant_behavioral_016** 〔qdrant / collections+{collection_name}+points+payload〕
  - description: 200 on success; 400 if no points or filter specified
- **qdrant_state_set_payload_006** 〔qdrant / collections+{collection_name}+points+payload〕
  - assertion: `Payload set is atomic: all matched points receive the payload.`
  - description: Atomic - all matched points get the payload

## `https://milvus.io/api-reference/restful/v2.6.x/v2/Vector%20(v2)/Get.md`

- 性质：**vendor-documentation**｜URL 版本片段：2.6｜实例 33｜引用该页的约束 2 条
- 捕获：`pages_text/milvus.io_api-reference_restful_v2.6.x_v2_Vector_20_v2_Get.md.txt`

- **milvus_behavioral_entities_get_001** 〔milvus / entities+get〕
  - description: Get entities returns 400 if id type mismatches collection schema
- **milvus_type_entities_get_001** 〔milvus / entities+get〕
  - assertion: `id type matches collection primary key type`
  - description: id must match the collection primary key type (Int64 or VarChar)

## `https://milvus.io/docs/schema.md`

- 性质：**vendor-documentation**｜URL 版本片段：—｜实例 32｜引用该页的约束 2 条
- 捕获：`pages_text/milvus.io_docs_schema.md.txt`（实际取自 `https://raw.githubusercontent.com/milvus-io/milvus-docs/ebb6de53/site/en/userGuide/schema/schema.md`）

- **milvus_assert_insert_success_001** 〔milvus / entities+insert〕
  - description: Inserting valid data succeeds
- **milvus_state_insert_collection_001** 〔milvus / entities+insert〕
  - assertion: `collection MUST exist before insert`
  - description: Insert requires existing collection

## `https://milvus.io/docs/index.md`

- 性质：**vendor-documentation**｜URL 版本片段：—｜实例 18｜引用该页的约束 6 条
- 捕获：**未捕获**

- **milvus_range_hnsw_ef_001** 〔milvus / entities+search〕
  - assertion: `ef in [1, 2147483647]`
  - description: ef parameter for HNSW search
- **milvus_range_ivf_flat_nprobe_001** 〔milvus / entities+search〕
  - assertion: `nprobe in [1, nlist]`
  - description: nprobe parameter for IVF_FLAT search
- **milvus_range_ivf_nprobe_001** 〔milvus / entities+search〕
  - assertion: `nprobe >= 1 AND nprobe <= nlist`
  - description: IVF nprobe must be in range [1, nlist]
- **milvus_range_ivf_pq_nprobe_001** 〔milvus / entities+search〕
  - assertion: `nprobe in [1, nlist]`
  - description: nprobe parameter for IVF_PQ search
- **milvus_range_ivf_sq8_nprobe_001** 〔milvus / entities+search〕
  - assertion: `nprobe in [1, nlist]`
  - description: nprobe parameter for IVF_SQ8 search
- **milvus_range_scann_nprobe_001** 〔milvus / entities+search〕
  - assertion: `nprobe in [1, nlist]`
  - description: nprobe parameter for SCANN search

## `https://api.qdrant.tech/v-1-18-x/api-reference/collections/get-collection`

- 性质：**vendor-documentation**｜URL 版本片段：—｜实例 13｜引用该页的约束 1 条
- 捕获：`pages_text/api.qdrant.tech_v-1-18-x_api-reference_collections_get-collection.txt`

- **qdrant_behavioral_003** 〔qdrant / collections+{collection_name}〕
  - description: 200 with collection info; 404 if not found

## `https://milvus.io/docs/single-vector-search.md`

- 性质：**vendor-documentation**｜URL 版本片段：—｜实例 9｜引用该页的约束 3 条
- 捕获：`pages_text/milvus.io_docs_single-vector-search.md.txt`（实际取自 `https://raw.githubusercontent.com/milvus-io/milvus-docs/ebb6de53/site/en/userGuide/search-query-get/single-vector-search.md`）

- **milvus_assert_search_empty_001** 〔milvus / entities+search〕
  - description: Searching empty collection returns empty results
- **milvus_state_search_load_001** 〔milvus / entities+search〕
  - assertion: `collection MUST be loaded before search`
  - description: Search requires collection to be loaded
- **milvus_state_search_requires_load_001** 〔milvus / entities+search〕
  - assertion: `collection.load_state == 'loaded' before search`
  - description: Collection must be loaded before searching

## `https://weaviate.io/developers/weaviate/api/graphql`

- 性质：**vendor-documentation**｜URL 版本片段：—｜实例 9｜引用该页的约束 1 条
- 捕获：`pages_text/weaviate.io_developers_weaviate_api_graphql.txt`

- **weaviate_type_graphql_001** 〔weaviate / /graphql POST〕
  - assertion: `query string case must match schema exactly`
  - description: GraphQL is case-sensitive

## `https://milvus.io/docs/insert-update.md`

- 性质：**vendor-documentation**｜URL 版本片段：—｜实例 4｜引用该页的约束 1 条
- 捕获：`pages_text/milvus.io_docs_insert-update.md.txt`（实际取自 `https://raw.githubusercontent.com/milvus-io/milvus-docs/ebb6de53/site/en/userGuide/insert-and-delete/insert-update-delete.md`）

- **milvus_behavioral_insert_then_get_001** 〔milvus / entities+insert〕
  - description: Inserted entities should be retrievable

## `https://milvus.io/api-reference/restful/v2.6.x/v2/Import%20(v2)/Create.md`

- 性质：**vendor-documentation**｜URL 版本片段：2.6｜实例 1｜引用该页的约束 1 条
- 捕获：`pages_text/milvus.io_api-reference_restful_v2.6.x_v2_Import_20_v2_Create.md.txt`

- **milvus_state_jobs_import_create_001** 〔milvus / jobs+import+create〕
  - assertion: `files exist in object storage`
  - description: Files must be pre-staged in object storage before import

## `https://milvus.io/api-reference/restful/v2.6.x/v2/User%20(v2)/Update%20Password.md`

- 性质：**vendor-documentation**｜URL 版本片段：2.6｜实例 1｜引用该页的约束 1 条
- 捕获：`pages_text/milvus.io_api-reference_restful_v2.6.x_v2_User_20_v2_Update_20Password.md.txt`

- **milvus_behavioral_users_update_password_001** 〔milvus / users+update_password〕
  - description: Update password returns 400 if current password is wrong or new password too weak

## `https://raw.githubusercontent.com/milvus-io/milvus-docs/ebb6de53/site/en/userGuide/search-query-get/metric.md`

- 性质：**doc-markdown-raw**｜URL 版本片段：—｜实例 1｜引用该页的约束 1 条
- 捕获：`pages_text/raw.githubusercontent.com_milvus-io_milvus-docs_ebb6de53_site_en_userGuide_search-query-get_metric.md.txt`

- **milvus_metric_cosine_range_001** 〔milvus / entities+search〕
  - assertion: `metric_type == COSINE implies distance = 1 - cosine_similarity in [0, 2]; identical vectors distance == 0`
  - description: COSINE distance = 1 - cosine similarity; similarity in [-1,1] so identical vectors distance=0, range [0,2]

## `https://milvus.io/api-reference/restful/v2.3.x/v2/Vector%20(v2)/Query.md`

- 性质：**vendor-documentation**｜URL 版本片段：2.3｜实例 1｜引用该页的约束 1 条
- 捕获：**未捕获**

- **milvus_type_request_timeout_001** 〔milvus / entities+query〕
  - assertion: `header Request-Timeout matches ^[0-9]+$ (non-integer rejected)`
  - description: Request-Timeout header must be an integer

## `https://raw.githubusercontent.com/milvus-io/milvus-docs/99af7351/site/en/userGuide/search-query-get/grouping-search.md`

- 性质：**doc-markdown-raw**｜URL 版本片段：—｜实例 1｜引用该页的约束 1 条
- 捕获：`pages_text/raw.githubusercontent.com_milvus-io_milvus-docs_99af7351_site_en_userGuide_search-query-get_grouping-search.md.txt`

- **milvus_state_group_by_field_001** 〔milvus / entities+search〕
  - assertion: `group_by_field refers to a scalar (non-vector) field`
  - description: group_by_field must be a scalar field (grouping by vector field not supported)

## `https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json`

- 性质：**structured-spec**｜URL 版本片段：1.18.2｜实例 1｜引用该页的约束 1 条
- 捕获：`pages_text/github.com_qdrant_qdrant_blob_v1.18.2_docs_redoc_master_openapi.json.txt`（实际取自 `https://raw.githubusercontent.com/qdrant/qdrant/v1.18.2/docs/redoc/master/openapi.json`）

- **qdrant_type_lookup_from_001** 〔qdrant / collections+points+query〕
  - assertion: `lookup_from.collection exists in collections registry`
  - description: lookup_from.collection must reference an existing collection (non-existent -> 400/404)


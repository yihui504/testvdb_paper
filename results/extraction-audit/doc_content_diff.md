# A1 · 族 1/4/5 文档页面内容差异（机械）

对照：「包实际引用的版本」vs「该受测版本」。
- **cosmetic** = 只差版本号的改动（导航/版本串），非文档实质
- **substantive** = 剔除 cosmetic 后的改动行
- **relevant** = substantive 中命中「引用该页的约束所断言术语」的行数 ← 真正要紧的一列

| 页面 | 相似度 | cosmetic | substantive | **relevant** | 状态 |
|---|---|---|---|---|---|
| 族1 · milvus Create.md | 0.5798 | 24 | 164 | **78** | 已比对 |
| 族1 · milvus Search.md | 0.7917 | 4 | 55 | **24** | 已比对 |
| 族1 · milvus Drop.md | 0.9018 | 2 | 17 | **6** | 已比对 |
| 族1 · milvus Load.md | 0.9131 | 2 | 17 | **3** | 已比对 |
| 族1 · milvus Rename.md | 0.8697 | 4 | 19 | **6** | 已比对 |
| 族1 · milvus Get.md | 0.8475 | 2 | 17 | **1** | 已比对 |
| 族4 · qdrant 1.19.0vs1.18 api-reference | 1.0 | 0 | 0 | **0** | 已比对 |
| 族4 · qdrant 1.19.0vs1.18 create-collection | 0.7507 | 74 | 25 | **16** | 已比对 |
| 族4 · qdrant 1.19.0vs1.18 points | — | — | — | — | **正确版页面不存在（豁免）** |
| 族4 · qdrant 1.19.0vs1.18 upsert-points | 0.8022 | 198 | 18 | **2** | 已比对 |
| 族4 · qdrant 1.19.0vs1.18 set-payload | 0.7839 | 86 | 14 | **3** | 已比对 |
| 族5 · qdrant 1.12.1vs1.18 api-reference | 1.0 | 0 | 0 | **0** | 已比对 |
| 族5 · qdrant 1.12.1vs1.18 create-collection | 0.2627 | 107 | 73 | **44** | 已比对 |
| 族5 · qdrant 1.12.1vs1.18 points | 0.6601 | 161 | 54 | **5** | 已比对 |
| 族5 · qdrant 1.12.1vs1.18 upsert-points | 0.4559 | 231 | 73 | **29** | 已比对 |
| 族5 · qdrant 1.12.1vs1.18 set-payload | 0.6296 | 115 | 51 | **10** | 已比对 |

## 命中约束断言的改动行（逐页）

### 族1 · milvus Create.md

  - The authentication token should be a pair of colon-joined username and password, like `username:password`.
  - The number of dimensions a vector value should have. This is required if **dtype** of this field is set to **DataType.FLOAT_VECTOR** or **DataType.Binary_VECTOR**.
  - L2IPCOSINE
  - schemaobject
  - Whether allows to use the reserved **$meta** field to hold non-schema-defined fields in key-value pairs.
  - The name of the field to create in the target collection
  - DataType.BOOLDataType.INT8DataType.INT16DataType.INT32DataType.INT64DataType.FLOATDataType.DOUBLEDataType.VARCHARDataType.ARRAYDataType.JSONDataType.BINARY_VECTORDataType
  - DataType.BOOLDataType.INT8DataType.INT16DataType.INT32DataType.INT64DataType.FLOATDataType.DOUBLEDataType.VARCHAR
  - The default value of the field. This is required if the current field is of the `VarChar` type.
  - Whether the current field serves as the partition key. Setting this to True makes the current field serve as the partition key. In this case, MilvusZilliz Cloud manages a
  - Extra field parameters.
  - An optional parameter for VarChar values that determines the maximum length of the value in the current field.
  - An optional parameter for FloatVector or BinaryVector fields that determines the vector dimension.
  - namestring
  - The name of the function to create.
  - The description of the function to create.
  - The type of the function to create.
  - inputFieldNamesarray
  - The names of the input fields for the function to create.
  - A field name.

### 族1 · milvus Search.md

  - A list of vector embeddings. Milvus searches for the most similar vector embeddings to the specified ones.
  - annsFieldstringrequired
  - The name of the field that serves as the aggregation criteria.
  - A list of vector embeddings.
  - Milvus searches for the most similar vector embeddings to the specified ones.
  - Milvus searches for the most similar vector embeddings to those in the specified entities.
  - This parameter is mutually exclusive with **data**.
  - annsFieldstring
  - Groups search results by a specified field to ensure diversity and avoid returning multiple results from the same group.
  - The number of entities to return for each group. This parameter is only valid when `groupingField` is specified.
  - Whether to return only the top k entities for each group. This parameter is only valid when `groupingField` is specified.
  - Function settings for the current search request.
  - inputFieldNamesarray
  - A list of scalar fields to use as input for the function.
  - A scalar field to use as input for the function.
  - outputFieldNamesarray
  - A list of vector fields to use as output for the function.
  - A vector field to use as output for the function.
  - Extra parameters for the search in key-value pairs.
  - Recall values for each search result group.

### 族1 · milvus Drop.md

  - This operation drops the current collection and all data within the collection.
  - The name of the database that to which the collection belongs . Setting this to a non-existing database results in an error.
  - Response payload which is an empty object.
  - * Drop Function From
  - This operation drops the collection with the specified name and drops all data within.
  - The name of the database which the collection belongs to. Setting this to a non-existing database results in an error. If not specified, the default database applies.

### 族1 · milvus Load.md

  - The name of the database that to which the collection belongs . Setting this to a non-existing database results in an error.
  - Response payload which is an empty object.
  - The name of the database which the collection belongs to. Setting this to a non-existing database results in an error. If not specified, the default database applies.

### 族1 · milvus Rename.md

  - The name of the database that to which the collection belongs . Setting this to a non-existing database results in an error.
  - The name of the target collection after this operation. Setting this to the value of **old_collection_name** results in an error.
  - Response payload which is an empty object.
  - The authentication token should be a pair of colon-joined username and password, like `username:password`. If you are using a project endpoint, only a valid API key with 
  - The name of the database which the collection belongs to. Setting this to a non-existing database results in an error. If not specified, the default database applies.
  - The name of the target collection after this operation. Setting this to the original one results in an error.

### 族1 · milvus Get.md

  - Name of the partition to get entities from.

### 族4 · qdrant 1.19.0vs1.18 create-collection

  - Reference: https://api.qdrant.tech/v-1-18-x/api-reference/collections/create-collection
  - - `on_disk` (boolean, optional, nullable) — If true, vectors are served from disk, improving RAM usage at the cost of latency Default: false
  - - `datatype` (enum or any, optional) — Defines which datatype should be used to represent vectors in the storage. Choosing different datatypes allows to optimize memory u
  - - `on_disk_payload` (boolean, optional, nullable) — If true - point's payload will not be stored in memory. It will be read from the disk every time it is requested. This
  - - `prevent_unoptimized` (boolean, optional, nullable) — If this option is set, service will try to prevent creation of large unoptimized segments. When enabled, updates m
  - - `max_resident_memory_percent` (integer, optional, nullable) — Reject memory-consuming update operations (e.g. upsert, set payload) when the process resident memory exce
  - Reference: https://api.qdrant.tech/api-reference/collections/create-collection
  - - `memory` (enum or any, optional) — Memory placement of the original vector storage. Overrides the deprecated `on_disk` flag if both are set. `pinned` is not supported f
  - - `datatype` (enum or any, optional) — Defines which datatype should be used to represent vectors in the storage. Choosing different datatypes allows to optimize memory u
  - - `on_disk` (boolean, optional, nullable, deprecated) — Deprecated: use `memory` instead. If true, vectors are served from disk, improving RAM usage at the cost of latenc
  - - `payload` (object or any, optional) — Configuration of the payload storage
  - - PayloadStorageParams
  - - `memory` (enum or any, optional) — Memory placement of the payload storage. Overrides the deprecated `on_disk_payload` flag if both are set. `pinned` is not supported f
  - - `prevent_unoptimized` (boolean, optional, nullable) — If enabled, the service will try to prevent the creation of large unoptimized segments. When enabled, new points w
  - - `max_resident_memory_percent` (integer, optional, nullable, deprecated) — Deprecated: use the node-wide quota config (`PUT /quotas`) instead, which caps the same resour
  - - `on_disk_payload` (boolean, optional, nullable, deprecated) — Deprecated: use `payload.memory` instead. If true - point's payload will not be stored in memory. It will 

### 族4 · qdrant 1.19.0vs1.18 upsert-points

  - Reference: https://api.qdrant.tech/v-1-18-x/api-reference/points/upsert-points
  - Reference: https://api.qdrant.tech/api-reference/points/upsert-points

### 族4 · qdrant 1.19.0vs1.18 set-payload

  - Reference: https://api.qdrant.tech/v-1-18-x/api-reference/points/set-payload
  - Reference: https://api.qdrant.tech/api-reference/points/set-payload
  - - `slice` (object, required) — One of `total` disjoint deterministic slices of the id space. A point belongs to the slice iff `hash(id) % total == index`, where `hash` is

### 族5 · qdrant 1.12.1vs1.18 create-collection

  - - `full_scan_threshold` (integer, optional, nullable) — Minimal size threshold (in KiloBytes) below which full-scan is preferred over HNSW search. This measures the total
  - - `inline_storage` (boolean, optional, nullable) — Store copies of original and quantized vectors within the HNSW index file. Default: false. Enabling this option will tr
  - - `quantization_config` (object or object or object or object or any, optional) — Custom params for quantization. If none - values from collection configuration are used.
  - - `on_disk_payload` (boolean, optional, nullable) — If true - point's payload will not be stored in memory. It will be read from the disk every time it is requested. This
  - - `full_scan_threshold` (integer, optional, nullable) — Minimal size threshold (in KiloBytes) below which full-scan is preferred over HNSW search. This measures the total
  - - `inline_storage` (boolean, optional, nullable) — Store copies of original and quantized vectors within the HNSW index file. Default: false. Enabling this option will tr
  - - `prevent_unoptimized` (boolean, optional, nullable) — If this option is set, service will try to prevent creation of large unoptimized segments. When enabled, updates m
  - - `memmap_threshold` (integer, optional, nullable, deprecated) — Maximum size (in kilobytes) of vectors to store in-memory per segment. Segments larger than this threshol
  - - `quantization_config` (object or object or object or object or any, optional) — Quantization parameters. If none - quantization is disabled.
  - - `strict_mode_config` (object or any, optional) — Strict-mode config.
  - - StrictModeConfig
  - - `enabled` (boolean, optional, nullable) — Whether strict mode is enabled for a collection or not.
  - - `max_timeout` (integer, optional, nullable) — Max allowed `timeout` parameter.
  - - `unindexed_filtering_update` (boolean, optional, nullable) — Allow usage of unindexed fields in filtered updates (e.g. delete by payload).
  - - `max_collection_vector_size_bytes` (integer, optional, nullable) — Max size of a collections vector storage in bytes, ignoring replicas.
  - - `read_rate_limit` (integer, optional, nullable) — Max number of read operations per minute per replica
  - - `write_rate_limit` (integer, optional, nullable) — Max number of write operations per minute per replica
  - - `max_collection_payload_size_bytes` (integer, optional, nullable) — Max size of a collections payload storage in bytes
  - - `max_points_count` (integer, optional, nullable) — Max number of points estimated in a collection
  - - `multivector_config` (map from string to object or any, optional) — Multivector strict mode configuration

### 族5 · qdrant 1.12.1vs1.18 points

  - - `oversampling` (double, optional, nullable) — Oversampling factor for quantization. Default is 1.0. Defines how many extra vectors should be preselected using quantized
  - - `acorn` (object or any, optional) — ACORN search params
  - - AcornSearchParams
  - - `enable` (boolean, optional, default: false) — If true, then ACORN may be used for the HNSW search based on filters selectivity. Improves search recall for searches wit
  - - `oversampling` (double, optional, nullable) — Oversampling factor for quantization. Default is 1.0. Defines how many extra vectors should be pre-selected using quantize

### 族5 · qdrant 1.12.1vs1.18 upsert-points

  - - `vectors` (list of list of double or list of list of list of double or map from string to list of list of double or object or list of list of double or object or object
  - - `shard_key` (string or uint64 or list of string or uint64 or object or any, optional)
  - - `update_filter` (object or any, optional) — Filter to apply when updating existing points. Only points matching this filter will be updated. Points that don't match wil
  - - `update_mode` (enum or any, optional) — Mode of the upsert operation: insert_only, upsert (default), update_only
  - - `vector` (list of double or list of list of double or map from string to list of double or object or list of list of double or object or object or object or object or o
  - - `model` (string, required) — Name of the model used to generate the vector. List of available models depends on a provider.
  - - `model` (string, required) — Name of the model used to generate the vector. List of available models depends on a provider.
  - - `model` (string, required) — Name of the model used to generate the vector. List of available models depends on a provider.
  - - `shard_key` (string or uint64 or list of string or uint64 or object or any, optional)
  - - `update_filter` (object or any, optional) — Filter to apply when updating existing points. Only points matching this filter will be updated. Points that don't match wil
  - - `update_mode` (enum or any, optional) — Mode of the upsert operation: insert_only, upsert (default), update_only
  - - `payload_io_read` (integer, required)
  - - `payload_io_write` (integer, required)
  - - `payload_index_io_read` (integer, required)
  - - `payload_index_io_write` (integer, required)
  - - `vector_io_read` (integer, required)
  - - `vector_io_write` (integer, required)
  - - `tokens` (uint64, required)
  - "payload_io_read": 1,
  - "payload_io_write": 1,

### 族5 · qdrant 1.12.1vs1.18 set-payload

  - - `geo_bounding_box` (object or any, optional) — Check if points geolocation lies in a given area
  - - `payload_io_read` (integer, required)
  - - `payload_io_write` (integer, required)
  - - `payload_index_io_read` (integer, required)
  - - `payload_index_io_write` (integer, required)
  - "payload_io_read": 1,
  - "payload_io_write": 1,
  - "payload_index_io_read": 1,
  - "payload_index_io_write": 1,
  - - `geo_bounding_box` (object or any, optional) — Check if points geo location lies in a given area


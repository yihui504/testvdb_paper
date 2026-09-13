🚀 Zilliz Cloud: fully managed Milvus — 10x faster. Zero hassle. Built for AI.Try Free Now →

  * Why Milvus

    * What is Milvus
    * Use Cases

  * Docs
  * Tutorials

    * Bootcamp
    * Demos
    * Video

  * Tools

    * Attu
    * Milvus CLI
    * Sizing Tool
    * Milvus Backup
    * VTS
    * Deep Searcher
    * Claude Context

  * Blog
  * Community

    * Milvus Office Hours
    * Slack
    * Discord
    * GitHub
    * More Channels

Star46.0KBook a DemoTry Managed Milvus

< Docs

v3.0.x

  * v3.0.x
  * v2.6.x
  * v2.5.x
  * v2.4.x

  * RESTful

    * About

    * v2

      * Alias (v2)

      * Collection (v2)

        * Add Field

        * Add Function To

        * Alter Field Properties

        * Alter Function In

        * Alter Properties

        * Compact

        * Create

        * Describe External Refresh Job

        * Describe

        * Drop Function From

        * Drop Properties

        * Drop

        * Flush

        * Get Compaction State

        * Get Load State

        * Get Stats

        * Has

        * List External Refresh Jobs

        * List

        * Load

        * Refresh External

        * Refresh Load

        * Release

        * Rename

        * Run Analyzer

        * Truncate

      * Database (v2)

      * Import (v2)

      * Index (v2)

      * Partition (v2)

      * Privilege Group (v2)

      * Resource Group (v2)

      * Role (v2)

      * User (v2)

      * Vector (v2)

    * v1

  * Home
  * Docs
  * API Reference
  * RESTful

  * v2

  * Collection (v2)

  * Create

# Create Collection

This operation creates a collection in a specified cluster.

POST

/v2/vectordb/collections/create

Try it out

Cluster Endpoint

The base URL for this API is in the following format:

http://localhost:19530
    
    
    export CLUSTER_ENDPOINT="http://localhost:19530"

Parameters

Authorizationstringheaderrequired

The authentication token should be a pair of colon-joined username and password, like `username:password`. If you are using a project endpoint, only a valid API key with sufficient permissions applies.

Example Value: Bearer {{TOKEN}}

Request Bodyapplication/json

QUICK SETUP

dbNamestring

The name of the database.

collectionNamestringrequired

The name of the collection to create.

dimensionintegerrequired

The number of dimensions a vector value should have. This is required if **idType** of this field is set to **DataType.FLOAT_VECTOR** or **DataType.Binary_VECTOR**.

metricTypestring

The metric type applied to this operation.

Possible Values: 

L2IPCOSINEJACCARDHAMMING

idTypestring

The data type of the primary field. This parameter is designed for the quick-setup of a collection and will be ignored if **schema** is defined.

Possible Values: 

VarCharInt64

autoIDboolean

Whether the primary field automatically increments. This parameter is designed for the quick-setup of a collection and will be ignored if **schema** is defined.

primaryFieldNamestring

The name of the primary field. This parameter is designed for the quick-setup of a collection and will be ignored if **schema** is defined.

vectorFieldNamestring

The name of the vector field. This parameter is designed for the quick-setup of a collection and will be ignored if **schema** is defined.

descriptionstring

The description of the current collection.

paramsobject

Extra parameters for the collection.

max_lengthinteger

The maximum number of bytes allowed in the primary field. This parameter is available only when the primary field is a string field.

enableDynamicFieldboolean

Whether to enable the dynamic field feature.

shardsNuminteger

The number of shards to create along with the current collection.

consistencyLevelstring

The consistency level of the collection.

Possible Values: 

StrongEventuallySessionBounded

ttlSecondsinteger

The time-to-live (TTL) period of the collection. If set, the collection is to be dropped once the period ends.

mmap.enabledboolean

Specifies whether to enable memory mapping for the collection.

ttlFieldstring

The name of the field to use for TTL-based expiration.

warmup.scalarFieldboolean

Whether to preload scalar field data into memory on load.

warmup.scalarIndexboolean

Whether to preload scalar index data into memory on load.

warmup.vectorFieldboolean

Whether to preload vector field data into memory on load.

warmup.vectorIndexboolean

Whether to preload vector index data into memory on load.

CUSTOM SETUP

dbNamestring

The name of the database.

collectionNamestring

The name of the collection to create.

schemaundefined

The schema is responsible for organizing data in the target collection. A valid schema should have multiple fields, which must include a primary key, a vector field, and several scalar fields. Setting this parameter means that `dimension`, `idType`, `autoID`, `primaryFieldName`, and `vectorFieldName` will be ignored.

indexParamsarray

The parameters that apply to the index-building process.

[]indexParamsobject

An index Schema object.

metricTypestringrequired

The similarity metric type used to build the index. For more information, refer to Similarity Metrics](https://milvus.io/docs/metric.md).

Possible Values: 

L2IPCOSINEJACCARDHAMMING

fieldNamestringrequired

The name of the target field on which an index is to be created.

indexNamestringrequired

The name of the index to create. The value defaults to the target field name.

paramsobject

The index type and related settings. For details, refer to Vector Indexes.

index_typestringrequired

The type of the index to create

Minteger

The maximum degree of the node. This applies only when **index_type** is set to **HNSW**.

efConstructioninteger

The search scope. This applies only when **index_type** is set to **HNSW**.

nlistinteger

The number of cluster units. This applies only when **index_type** is set to **IVF-related** index types.

paramsobject

Extra parameters for the collection.

shardsNuminteger

The number of shards to create along with the current collection.

consistencyLevelstring

The consistency level of the collection.

Possible Values: 

StrongEventuallySessionBounded

partitionsNuminteger

The number of partitions to create along with the current collection. This parameter is mandatory if one field of the collection has been designated as the partition key.

ttlSecondsinteger

The time-to-live (TTL) period of the collection. If set, the collection is to be dropped once the period ends.

partitionKeyIsolationboolean

Specifies whether to enable partition key isolation for the collection.

mmap.enabledboolean

Specifies whether to enable memory mapping for the collection.

ttlFieldstring

The name of the field to use for TTL-based expiration.

warmup.scalarFieldboolean

Whether to preload scalar field data into memory on load.

warmup.scalarIndexboolean

Whether to preload scalar index data into memory on load.

warmup.vectorFieldboolean

Whether to preload vector field data into memory on load.

warmup.vectorIndexboolean

Whether to preload vector index data into memory on load.

descriptionstring

The description of the current collection.

EXTERNAL SETUP

dbNamestring

The name of the database.

collectionNamestring

The name of the collection to create.

schemaundefined

The schema for an external collection. Must include fields with externalField mappings, plus externalSource and externalSpec.

indexParamsarray

The parameters that apply to the index-building process.

[]indexParamsobject

An index Schema object.

metricTypestringrequired

The similarity metric type used to build the index. For more information, refer to Similarity Metrics](https://milvus.io/docs/metric.md).

Possible Values: 

L2IPCOSINEJACCARDHAMMING

fieldNamestringrequired

The name of the target field on which an index is to be created.

indexNamestringrequired

The name of the index to create. The value defaults to the target field name.

paramsobject

The index type and related settings. For details, refer to Vector Indexes.

index_typestringrequired

The type of the index to create

Minteger

The maximum degree of the node. This applies only when **index_type** is set to **HNSW**.

efConstructioninteger

The search scope. This applies only when **index_type** is set to **HNSW**.

nlistinteger

The number of cluster units. This applies only when **index_type** is set to **IVF-related** index types.

paramsobject

Extra parameters for the collection.

shardsNuminteger

The number of shards to create along with the current collection.

consistencyLevelstring

The consistency level of the collection.

Possible Values: 

StrongEventuallySessionBounded

partitionsNuminteger

The number of partitions to create along with the current collection. This parameter is mandatory if one field of the collection has been designated as the partition key.

ttlSecondsinteger

The time-to-live (TTL) period of the collection. If set, the collection is to be dropped once the period ends.

partitionKeyIsolationboolean

Specifies whether to enable partition key isolation for the collection.

mmap.enabledboolean

Specifies whether to enable memory mapping for the collection.

ttlFieldstring

The name of the field to use for TTL-based expiration.

warmup.scalarFieldboolean

Whether to preload scalar field data into memory on load.

warmup.scalarIndexboolean

Whether to preload scalar index data into memory on load.

warmup.vectorFieldboolean

Whether to preload vector field data into memory on load.

warmup.vectorIndexboolean

Whether to preload vector index data into memory on load.

descriptionstring

The description of the current collection.

QUICK SETUP
    
    
    export TOKEN="root:Milvus"
    
    
    
    
    curl --request POST \
    
    --url "${CLUSTER_ENDPOINT}/v2/vectordb/collections/create" \
    
    --header "Authorization: Bearer ${TOKEN}" \
    
    --header "Request-Timeout: 5" \
    
    --header "Content-Type: application/json" \
    
    -d '{
    
        "collectionName": "test_collection",
    
        "dimension": 5
    
    }'

QUICK SETUP WITH CUSTOM FIELDS
    
    
    export TOKEN="root:Milvus"
    
    
    
    
    curl --request POST \
    
    --url "${CLUSTER_ENDPOINT}/v2/vectordb/collections/create" \
    
    --header "Authorization: Bearer ${TOKEN}" \
    
    --header "Request-Timeout: 5" \
    
    --header "Content-Type: application/json" \
    
    -d '{
    
        "collectionName": "custom_quick_setup",
    
        "dimension": 5,
    
        "primaryFieldName": "my_id",
    
        "idType": "VarChar",
    
        "vectorFieldName": "my_vector",
    
        "metric_type": "L2",
    
        "autoId": true,
    
        "params": {
    
            "max_length": "512"
    
        }
    
    }'

Responses200 \- application/json

SUCCESS

codeinteger

Response code.

dataobject

FAILURE

Returns an error message.

codeinteger

Response code.

messagestring

Error message.

SUCCESS
    
    
    {
    
        "code": 0,
    
        "data": {}
    
    }

Made with Love  by the Devs from Zilliz

### Get Milvus Updates

Subscribe

Follow Us

Ask AI about Milvus

Copyright © Milvus. 2026 All rights reserved.

Resources

  * Docs
  * Blog
  * Managed Milvus
  * Book a Demo
  * AI Quick Reference 

Tutorials

  * Bootcamps
  * Demo
  * Video

Tools

  * Attu
  * Milvus CLI
  * Milvus Sizing Tool
  * Milvus Backup Tool
  * Vector Transport Service (VTS)
  * Deep Searcher
  * Claude Context

Community

  * Milvus Office Hours
  * Slack
  * Discord
  * Github

Ask AI

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

      * Database (v2)

      * Import (v2)

      * Index (v2)

      * Partition (v2)

      * Privilege Group (v2)

      * Resource Group (v2)

      * Role (v2)

      * User (v2)

      * Vector (v2)

        * Delete

        * Get

        * Hybrid Search

        * Insert

        * Query

        * Search

        * Upsert

    * v1

  * Home
  * Docs
  * API Reference
  * RESTful

  * v2

  * Vector (v2)

  * Search

# Search

This operation conducts a vector similarity search with an optional scalar filtering expression.

POST

/v2/vectordb/entities/search

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

dbNamestring

The name of the database.

collectionNamestringrequired

The name of the collection to which this operation applies.

dataarrayrequired

A list of vector embeddings.  
Milvus searches for the most similar vector embeddings to the specified ones.  
This parameter is mutually exclusive with **ids**.

[]dataarray

A vector embedding

idsarray

A list of primary keys.  
Milvus searches for the most similar vector embeddings to those in the specified entities.  
This parameter is mutually exclusive with **data**.

annsFieldstring

The name of the vector field.

filterstring

The filter used to find matches for the search.

groupingFieldstring

Groups search results by a specified field to ensure diversity and avoid returning multiple results from the same group.

groupSizeinteger

The number of entities to return for each group. This parameter is only valid when `groupingField` is specified.

strictGroupSizeboolean

Whether to return only the top k entities for each group. This parameter is only valid when `groupingField` is specified.

limitinteger

The total number of entities to return. You can use this parameter in combination with **offset** in **param** to enable pagination. The sum of this value and **offset** in **param** should be less than 16,384.

offsetinteger

The number of records to skip in the search result. You can use this parameter in combination with limit to enable pagination. The sum of this value and limit should be less than 16,384.

outputFieldsarray

An array of fields to return along with the search results.

[]outputFieldsstring

A field name

searchParamsobject

The parameter settings specific to this operation.

metricTypestring

The name of the metric type that applies to the current search. The value should be the same as the metric type of the target collection.

Possible Values: 

L2IPCOSINE

paramsobject

Extra search parameters.

radiusnumber<float64>

Determines the threshold of least similarity. When setting metric_type to L2, ensure that this value is greater than that of range_filter. Otherwise, this value should be lower than that of range_filter.

range_filternumber<float64>

Refines the search to vectors within a specific similarity range. When setting metric_type to IP or COSINE, ensure that this value is greater than that of radius. Otherwise, this value should be lower than that of radius.

partitionNamesarray

The name of the partitions to which this operation applies. Setting this parameter indicates that the search is within the specified partitions. Otherwise, the search is across all partitions in the collection.

[]partitionNamesstring

A partition name.

consistencyLevelstring

The consistency level of the search operation. The value should be the same as the consistency level of the target collection.

Possible Values: 

StrongEventuallySessionBounded

exprParamsobject

A set of key-value pairs that can be filled back in to the `filter` parameter to enable filtering templating. For details, refer to Filtering Templating.

functionScoreobject

Function settings for the current search request.

namestring

The name of the function to apply.

descriptionstring

The description of the function to apply.

typestring

The type of the function to apply.

Possible Values: 

BM25TEXTEMBEDDINGRERANK

inputFieldNamesarray

A list of scalar fields to use as input for the function.

[]inputFieldNamesstring

A scalar field to use as input for the function.

outputFieldNamesarray

A list of vector fields to use as output for the function.

[]outputFieldNamesstring

A vector field to use as output for the function.

paramsobject

Extra parameters for the function in key-value pairs.

paramsobject

Extra parameters for the search in key-value pairs.
    
    
    export TOKEN="root:Milvus"
    
    
    
    
    curl --request POST \
    
    --url "${CLUSTER_ENDPOINT}/v2/vectordb/entities/search" \
    
    --header "Authorization: Bearer ${TOKEN}" \
    
    --header "Request-Timeout: 5" \
    
    --header "Content-Type: application/json" \
    
    -d '{
    
        "collectionName": "quick_setup",
    
        "data": [
    
            [
    
                0.3580376395471989,
    
                -0.6023495712049978,
    
                0.18414012509913835,
    
                -0.26286205330961354,
    
                0.9029438446296592
    
            ]
    
        ],
    
        "annsField": "vector",
    
        "limit": 3,
    
        "outputFields": [
    
            "color"
    
        ]
    
    }'

Responses200 \- application/json

SUCCESS

codeinteger

Response code.

costinteger

Cost of this operation.

dataarray

A list of entity objects.

[]dataobject

An entity object.

recallsarray

Recall values for each search result group.

[]recallsnumber

 _(To be added soon)_

topksarray

The number of top-K results returned for each query vector.

[]topksinteger

 _(To be added soon)_

scanned_remote_bytesinteger

Returned when the deployment uses tiered storage with usage tracking enabled and the operation reads from remote/disk storage. Omitted when all data is served from local cache.

scanned_total_bytesinteger

Returned when the deployment uses tiered storage with usage tracking enabled and the operation reads from remote/disk storage. Omitted when all data is served from local cache.

cache_hit_rationumber

Returned when the deployment uses tiered storage with usage tracking enabled and the operation reads from remote/disk storage. Omitted when all data is served from local cache.

FAILURE

Returns an error message.

codeinteger

Response code.

messagestring

Error message.

SUCCESS
    
    
    {
    
        "code": 0,
    
        "data": [
    
            {
    
                "color": "orange_6781",
    
                "distance": 1,
    
                "id": 448300048035776800
    
            },
    
            {
    
                "color": "red_4794",
    
                "distance": 0.9353201,
    
                "id": 448300048035776800
    
            },
    
            {
    
                "color": "grey_8510",
    
                "distance": 0.7733054,
    
                "id": 448300048035776800
    
            }
    
        ]
    
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

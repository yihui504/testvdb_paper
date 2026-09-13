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

  * Get

# Get

This operation gets specific entities by their IDs.

POST

/v2/vectordb/entities/get

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

idobjectrequired

A specific entity ID or a list of entity IDs.

outputFieldsarray

An array of fields to return along with the query results.

[]outputFieldsstring

An output field name.

partitionNamesarray

The name of the partitions to which this operation applies.

[]partitionNamesstring

A partition name.

consistencyLevelstring

The consistency level for this operation. The default value is `Bounded`.

Possible Values: 

StrongEventuallySessionBounded

partitionNamestring

Name of the partition to get entities from.
    
    
    export TOKEN="root:Milvus"
    
    
    
    
    curl --request POST \
    
    --url "${CLUSTER_ENDPOINT}/v2/vectordb/entities/get" \
    
    --header "Authorization: Bearer ${TOKEN}" \
    
    --header "Request-Timeout: 5" \
    
    --header "Content-Type: application/json" \
    
    -d '{
    
        "collectionName": "quick_setup",
    
        "id": [
    
            1,
    
            3,
    
            5
    
        ],
    
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

Query results.

[]dataobject

An entity object.

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
    
                "color": "red_7025",
    
                "id": 1
    
            },
    
            {
    
                "color": "pink_9298",
    
                "id": 3
    
            },
    
            {
    
                "color": "yellow_4222",
    
                "id": 5
    
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

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

  * Load

# Load Collection

This operation loads the data of the current collection into memory.

POST

/v2/vectordb/collections/load

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

The name of the database which the collection belongs to. Setting this to a non-existing database results in an error. If not specified, the default database applies.

collectionNamestringrequired

The name of the target collection. Setting this to a non-existing collection results in an error.
    
    
    export TOKEN="root:Milvus"
    
    
    
    
    curl --request POST \
    
    --url "${CLUSTER_ENDPOINT}/v2/vectordb/collections/load" \
    
    --header "Authorization: Bearer ${TOKEN}" \
    
    --header "Request-Timeout: 5" \
    
    --header "Content-Type: application/json" \
    
    -d '{
    
        "collectionName": "quick_setup"
    
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

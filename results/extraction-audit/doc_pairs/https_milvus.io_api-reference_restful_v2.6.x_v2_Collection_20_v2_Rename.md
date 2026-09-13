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

v2.6.x

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

        * Alter Field Properties

        * Alter Properties

        * Compact

        * Create

        * Describe

        * Drop Properties

        * Drop

        * Flush

        * Get Load State

        * Get Stats

        * Has

        * List

        * Load

        * Refresh Load

        * Release

        * Rename

      * Database (v2)

      * Import (v2)

      * Index (v2)

      * Partition (v2)

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

  * Rename

# Rename Collection

This operation renames an existing collection and optionally moves the collection to a new database.

POST

/v2/vectordb/collections/rename

Try it out

Cluster Endpoint

The base URL for this API is in the following format:

http://localhost:19530
    
    
    export CLUSTER_ENDPOINT="http://localhost:19530"

Parameters

Authorizationstringheaderrequired

The authentication token

Example Value: Bearer {{TOKEN}}

Request Bodyapplication/json

collectionNamestringrequired

The name of the target collection. Setting this to a non-existing collection results in an error.

dbNamestring

The name of the database that to which the collection belongs . Setting this to a non-existing database results in an error.

newDbNamestring

The name of the database to which the collection belongs after this operation. The value defaults to **default**. Setting this to a database rather than the one the collection belongs to before this operation moves this collection to the specified database. Setting this to a non-existing database results in an error.

newCollectionNamestringrequired

The name of the target collection after this operation. Setting this to the value of **old_collection_name** results in an error.
    
    
    export TOKEN="root:Milvus"
    
    
    
    
    curl --request POST \
    
    --url "${CLUSTER_ENDPOINT}/v2/vectordb/collections/rename" \
    
    --header "Authorization: Bearer ${TOKEN}" \
    
    --header "Request-Timeout: 5" \
    
    --header "Content-Type: application/json" \
    
    -d '{
    
        "collectionName": "test_collection",
    
        "newCollectionName": "quick_setup"
    
    }'

Responses200 \- application/json

SUCCESS

A success response

codeinteger

Response code.

Example Value: 0

dataobject

Response payload which is an empty object.

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

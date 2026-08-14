# API Templates — weaviate 1.38.0

## GET /
List available endpoints (root discovery)
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /.well-known/live
Liveness check
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /.well-known/ready
Readiness check
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /.well-known/openid-configuration
OIDC configuration
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /schema
List all collections (schema dump)
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /schema
Create a collection (Class definition)
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /schema/{className}
Get a single collection
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## PUT /schema/{className}
Update a collection definition (mutable settings only)
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## DELETE /schema/{className}
Delete a collection and all its data
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /schema/{className}/properties
Add property to collection
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /schema/{className}/indexes
Get index status for all properties
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## PUT /schema/{className}/indexes/{propertyName}
Update index config for a property (triggers async reindex)
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## DELETE /schema/{className}/properties/{propertyName}/index/{indexName}
Delete a property's inverted index
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## DELETE /schema/{className}/vectors/{vectorIndexName}/index
Delete a vector index
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /schema/{className}/shards
Get shard status of a collection
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## PUT /schema/{className}/shards/{shardName}
Update shard status
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /schema/{className}/properties/{propertyName}/tokenize
Tokenize text using property config
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /schema/{className}/tenants
List tenants of a multi-tenant collection
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /schema/{className}/tenants
Create tenants
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## PUT /schema/{className}/tenants
Update tenants (activityStatus: ACTIVE|INACTIVE|OFFLOADED)
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## DELETE /schema/{className}/tenants
Delete tenants (permanently deletes all tenant data)
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /schema/{className}/tenants/{tenantName}
Get single tenant
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## HEAD /schema/{className}/tenants/{tenantName}
Check tenant existence
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /aliases
List aliases
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /aliases
Create alias
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /aliases/{aliasName}
Get alias
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## PUT /aliases/{aliasName}
Update alias target
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## DELETE /aliases/{aliasName}
Delete alias
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /objects
List objects
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /objects
Create an object (fails if id already exists; use PUT/PATCH to update)
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /objects/{className}/{id}
Get object by className + id (RECOMMENDED)
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## DELETE /objects/{className}/{id}
Delete object by className + id
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## PUT /objects/{className}/{id}
Replace object (validates schema; lastUpdateTimeUnix updated)
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## PATCH /objects/{className}/{id}
Patch object (RFC 7396 JSON merge; only provided fields modified)
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## HEAD /objects/{className}/{id}
Check object existence
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /objects/validate
Validate object without storing
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /objects/{className}/{id}/references/{propertyName}
Add cross-reference (SingleRef)
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## PUT /objects/{className}/{id}/references/{propertyName}
Replace references (MultipleRef array)
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## DELETE /objects/{className}/{id}/references/{propertyName}
Delete reference (SingleRef to remove)
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /batch/objects
Batch create objects (idempotent by UUID; existing UUIDs overwritten with PUT semantics)
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## DELETE /batch/objects
Batch delete objects by where filter
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /batch/references
Batch create references
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /graphql
Perform GraphQL query (Get/Aggregate/Explore; case-sensitive; int fields int32 only)
source: https://weaviate.io/developers/weaviate/api/graphql

## POST /graphql/batch
Batch GraphQL queries
source: https://weaviate.io/developers/weaviate/api/graphql

## POST /classifications/
Start classification (knn/contextual)
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /classifications/{id}
Get classification status (meta: started, completed, count, countSucceeded, countFailed)
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /backups/{backend}
Create backup
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /backups/{backend}
List backups
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /backups/{backend}/{id}
Get backup status
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## DELETE /backups/{backend}/{id}
Cancel backup
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /backups/{backend}/{id}/restore
Restore from backup (target cluster must have same node count and names; collections must not already exist)
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /backups/{backend}/{id}/restore
Get restore status
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## DELETE /backups/{backend}/{id}/restore
Cancel restore
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /export/{backend}
Start Parquet export
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /export/{backend}/{id}
Get export status
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## DELETE /export/{backend}/{id}
Cancel export
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /nodes
Get node status (all)
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /nodes/{className}
Get node status by collection
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /cluster/statistics
Get cluster statistics (Raft)
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /tasks
List distributed tasks
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /replication/replicate
Initiate replica movement
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## DELETE /replication/replicate
Delete all replication operations
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /replication/replicate/{id}
Get replication operation
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## DELETE /replication/replicate/{id}
Delete replication operation
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /replication/replicate/{id}/cancel
Cancel replication operation
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /replication/replicate/force-delete
Force delete replication operations (DANGEROUS)
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /replication/replicate/list
List replication operations
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /replication/sharding-state
Get sharding state
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /replication/scale
Get replication scale plan
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /replication/scale
Apply replication scale plan
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /users/own-info
Get own user info
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /users/db
List db users
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /users/db/{user_id}
Get db user
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /users/db/{user_id}
Create db user
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## DELETE /users/db/{user_id}
Delete db user
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /users/db/{user_id}/rotate-key
Rotate db user API key
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /users/db/{user_id}/activate
Activate db user
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /users/db/{user_id}/deactivate
Deactivate db user
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /authz/roles
List roles
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /authz/roles
Create role
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /authz/roles/{id}
Get role
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## DELETE /authz/roles/{id}
Delete role
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /authz/roles/{id}/add-permissions
Add permissions to role
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /authz/roles/{id}/remove-permissions
Remove permissions from role
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /authz/roles/{id}/has-permission
Check if role has permission
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /namespaces
List namespaces
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /namespaces/{namespace_id}
Create namespace
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /namespaces/{namespace_id}
Get namespace
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## PUT /namespaces/{namespace_id}
Update namespace (home_node required)
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## DELETE /namespaces/{namespace_id}
Delete namespace (async, returns 202)
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /meta
Get instance metadata (hostname, version, modules, grpcMaxMessageSize)
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /tokenize
Tokenize text (generic)
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /mcp
MCP JSON-RPC / SSE stream
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /mcp
MCP SSE event stream
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## DELETE /mcp
Terminate MCP session
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

# API Templates — weaviate v1.38.2

## GET /
List available endpoints
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
Create a collection
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /schema/{className}
Get a single collection
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## PUT /schema/{className}
Update a collection definition (mutable settings only)
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## DELETE /schema/{className}
Delete a collection (and all data)
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /schema/{className}/properties
Add property to collection
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /schema/{className}/indexes
Get index status for all properties
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## PUT /schema/{className}/indexes/{propertyName}
Update index config for a property (triggers reindex)
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
Tokenize using property config
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /schema/{className}/tenants
Create tenants
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /schema/{className}/tenants
Get all tenants for a class
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## PUT /schema/{className}/tenants
Update tenants
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## DELETE /schema/{className}/tenants
Delete tenants
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /schema/{className}/tenants/{tenantName}
Get single tenant
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## HEAD /schema/{className}/tenants/{tenantName}
Check tenant exists
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
Update alias
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## DELETE /aliases/{aliasName}
Delete alias
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /objects
List objects
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /objects
Create an object
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /objects/validate
Validate object (without storage)
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /objects/{className}/{id}
Get object (by className + id) -- RECOMMENDED
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## DELETE /objects/{className}/{id}
Delete object (by className + id) -- RECOMMENDED
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## PUT /objects/{className}/{id}
Replace object (full update)
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## PATCH /objects/{className}/{id}
Patch object (RFC 7396 JSON merge patch)
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## HEAD /objects/{className}/{id}
Check existence (HEAD)
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /objects/{className}/{id}/references/{propertyName}
Add reference (by className + id) -- RECOMMENDED
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## PUT /objects/{className}/{id}/references/{propertyName}
Update references (replace all)
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## DELETE /objects/{className}/{id}/references/{propertyName}
Delete reference
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /batch/objects
Batch create objects
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## DELETE /batch/objects
Batch delete objects
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /batch/references
Batch create references
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /graphql
Perform GraphQL query
source: https://weaviate.io/developers/weaviate/api/graphql

## POST /graphql/batch
Batch GraphQL queries
source: https://weaviate.io/developers/weaviate/api/graphql

## POST /classifications/
Start classification
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /classifications/{id}
Get classification status
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
Restore from backup
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /backups/{backend}/{id}/restore
Get restore status
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## DELETE /backups/{backend}/{id}/restore
Cancel restore
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /export/{backend}
Start export
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
List database users
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /users/db/{user_id}
Get database user
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /users/db/{user_id}
Create database user
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## DELETE /users/db/{user_id}
Delete database user
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /users/db/{user_id}/rotate-key
Rotate API key
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /users/db/{user_id}/activate
Activate user
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /users/db/{user_id}/deactivate
Deactivate user
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
Check permission
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /authz/users/{id}/assign
Assign roles to user
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /authz/users/{id}/revoke
Revoke roles from user
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /authz/groups/{id}/assign
Assign roles to group
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /authz/groups/{id}/revoke
Revoke roles from group
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /authz/users/{id}/roles/{userType}
Get user roles
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /authz/groups/{id}/roles/{groupType}
Get group roles
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /authz/roles/{id}/user-assignments
Get role user assignments
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /authz/roles/{id}/group-assignments
Get role group assignments
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /authz/groups/{groupType}
List groups
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
Update namespace
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## DELETE /namespaces/{namespace_id}
Delete namespace
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /meta
Get instance metadata
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /tokenize
Tokenize (generic)
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## POST /mcp
MCP JSON-RPC
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## GET /mcp
MCP SSE stream
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

## DELETE /mcp
MCP terminate session
source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

# API Templates — milvus 2.6.17

## POST collections+create
Create a new collection with schema or quick-setup parameters
source: https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md

## POST collections+drop
Drop a collection and permanently delete all its data
source: https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Drop.md

## POST collections+describe
Describe a collection to get its schema, metadata, and configuration
source: https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md

## POST collections+list
List all collections in a database
source: https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md

## POST collections+has
Check if a collection exists
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST collections+load
Load a collection into memory for searching and queries
source: https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Load.md

## POST collections+release
Release a collection from memory
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST collections+get_stats
Get row count and other statistics for a collection
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST collections+get_load_state
Get the load state and progress of a collection
source: https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Get%20Load%20State.md

## POST collections+rename
Rename a collection or move it to a different database
source: https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Rename.md

## POST collections+alter
Alter collection properties
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST partitions+create
Create a partition within a collection
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST partitions+drop
Drop a partition and permanently delete its data
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST partitions+list
List all partitions in a collection
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST partitions+describe
Describe a partition with its details and row count
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST partitions+load
Load specific partitions into memory
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST partitions+release
Release specific partitions from memory
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST partitions+has
Check if a partition exists in a collection
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST entities+insert
Insert entities into a collection
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST entities+upsert
Insert or update entities (insert if primary key not found, update if exists)
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST entities+delete
Delete entities matching a filter expression
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST entities+query
Query entities using a boolean expression filter
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST entities+get
Get entities by their primary key IDs
source: https://milvus.io/api-reference/restful/v2.6.x/v2/Vector%20(v2)/Get.md

## POST entities+search
Search for nearest neighbors using vector embeddings
source: https://milvus.io/api-reference/restful/v2.6.x/v2/Vector%20(v2)/Search.md

## POST entities+advanced_search
Perform advanced vector search with grouping support
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST entities+hybrid_search
Perform hybrid search across multiple vector fields with reranking
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST indexes+create
Create an index on a field in a collection
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST indexes+drop
Drop an index from a collection
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST indexes+describe
Describe an index with its details and state
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST indexes+list
List all indexes on a collection
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST indexes+alter
Alter index properties
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST indexes+drop_properties
Drop specific properties from an index
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST aliases+create
Create an alias for a collection
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST aliases+drop
Drop an alias
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST aliases+alter
Reassign an alias to a different collection
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST aliases+describe
Describe an alias with its associated collection
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST aliases+list
List aliases, optionally filtered by collection
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST databases+create
Create a new database
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST databases+drop
Drop a database (must be empty and not the default database)
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST databases+describe
Describe a database with its properties
source: https://milvus.io/api-reference/restful/v2.6.x/v2/Database%20(v2)/Describe.md

## POST databases+list
List all database names
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST users+create
Create a new user account
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST users+drop
Drop a user account (cannot drop root user)
source: https://milvus.io/api-reference/restful/v2.6.x/v2/User%20(v2)/Drop.md

## POST users+describe
Describe a user with their roles
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST users+list
List all usernames
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST users+update_password
Update a user password
source: https://milvus.io/api-reference/restful/v2.6.x/v2/User%20(v2)/Update%20Password.md

## POST roles+create
Create a new role
source: https://milvus.io/api-reference/restful/v2.6.x/v2/Role%20(v2)/Create.md

## POST roles+drop
Drop a role
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST roles+describe
Describe a role with its privileges and users
source: https://milvus.io/api-reference/restful/v2.6.x/v2/Role%20(v2)/Describe.md

## POST roles+list
List all role names
source: https://milvus.io/api-reference/restful/v2.6.x/v2/Role%20(v2)/Lists.md

## POST roles+grant_privilege
Grant a privilege to a role
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST roles+revoke_privilege
Revoke a privilege from a role
source: https://milvus.io/api-reference/restful/v2.6.x/v2/Role%20(v2)/Revoke%20Privilege.md

## POST roles+grant_role
Grant a role to a user
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST roles+revoke_role
Revoke a role from a user
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST jobs+import+create
Create an import job to bulk-load data from object storage
source: https://milvus.io/api-reference/restful/v2.6.x/v2/Import%20(v2)/Create.md

## POST jobs+import+list
List import jobs with pagination
source: https://milvus.io/api-reference/restful/v2.6.x/v2/Import%20(v2)/List.md

## POST jobs+import+describe
Get import job progress and details
source: https://milvus.io/api-reference/restful/v2.6.x/v2/Import%20(v2)/Get%20Progress.md

## POST resource_groups+create
Create a resource group
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST resource_groups+drop
Drop a resource group (must be empty)
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST resource_groups+describe
Describe a resource group with capacity and node information
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST resource_groups+list
List all resource groups
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST resource_groups+transfer_replica
Transfer replicas between resource groups
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST collections+fields+add
Add a new field to an existing collection
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST privilege_groups+add_privileges_to_group
Add privileges to a privilege group
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST privilege_groups+remove_privileges_from_group
Remove privileges from a privilege group
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

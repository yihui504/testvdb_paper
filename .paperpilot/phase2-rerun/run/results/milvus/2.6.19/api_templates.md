# API Templates — milvus v2.6.19

## POST collections+create
Create a new collection with optional schema definition
source: https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md

## POST collections+drop
Drop (delete) a collection permanently
source: https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Drop.md

## POST collections+describe
Get collection schema and metadata
source: https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md

## POST collections+list
List all collections in a database
source: https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md

## POST collections+has
Check if a collection exists
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST collections+load
Load collection into memory for search
source: https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Load.md

## POST collections+release
Release collection from memory
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST collections+get_stats
Get collection statistics including row count
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST collections+get_load_state
Get collection load state and progress
source: https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Get%20Load%20State.md

## POST collections+rename
Rename a collection
source: https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Rename.md

## POST collections+alter
Alter collection properties
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST partitions+create
Create a partition in a collection
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST partitions+drop
Drop a partition
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST partitions+list
List all partitions in a collection
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST partitions+describe
Get partition details
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST partitions+load
Load partitions into memory
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST partitions+release
Release partitions from memory
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST partitions+has
Check if a partition exists
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST entities+insert
Insert entities into a collection
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST entities+upsert
Insert or update entities in a collection
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST entities+delete
Delete entities matching a filter expression
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST entities+query
Query entities with filter expression
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST entities+get
Get entities by primary key IDs
source: https://milvus.io/api-reference/restful/v2.6.x/v2/Vector%20(v2)/Get.md

## POST entities+search
Search for nearest neighbors by vector similarity
source: https://milvus.io/api-reference/restful/v2.6.x/v2/Vector%20(v2)/Search.md

## POST entities+advanced_search
Advanced search with grouping support
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST entities+hybrid_search
Hybrid search across multiple vector fields with reranking
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST indexes+create
Create an index on a field
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST indexes+drop
Drop an index
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST indexes+describe
Get index details
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST indexes+list
List all indexes in a collection
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST indexes+alter
Alter index properties
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST indexes+drop_properties
Drop index properties
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST aliases+create
Create a collection alias
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST aliases+drop
Drop a collection alias
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST aliases+alter
Reassign an alias to a different collection
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST aliases+describe
Get alias details
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST aliases+list
List all aliases
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST databases+create
Create a database
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST databases+drop
Drop a database
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST databases+describe
Get database properties
source: https://milvus.io/api-reference/restful/v2.6.x/v2/Database%20(v2)/Describe.md

## POST databases+list
List all databases
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST users+create
Create a user
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST users+drop
Drop a user
source: https://milvus.io/api-reference/restful/v2.6.x/v2/User%20(v2)/Drop.md

## POST users+describe
Get user details
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST users+list
List all users
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST users+update_password
Update user password
source: https://milvus.io/api-reference/restful/v2.6.x/v2/User%20(v2)/Update%20Password.md

## POST roles+create
Create a role
source: https://milvus.io/api-reference/restful/v2.6.x/v2/Role%20(v2)/Create.md

## POST roles+drop
Drop a role
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST roles+describe
Get role details and privileges
source: https://milvus.io/api-reference/restful/v2.6.x/v2/Role%20(v2)/Describe.md

## POST roles+list
List all roles
source: https://milvus.io/api-reference/restful/v2.6.x/v2/Role%20(v2)/Lists.md

## POST roles+grant_privilege
Grant privilege to a role
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST roles+revoke_privilege
Revoke privilege from a role
source: https://milvus.io/api-reference/restful/v2.6.x/v2/Role%20(v2)/Revoke%20Privilege.md

## POST roles+grant_role
Grant role to user
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST roles+revoke_role
Revoke role from user
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST jobs+import+create
Create a bulk import job
source: https://milvus.io/api-reference/restful/v2.6.x/v2/Import%20(v2)/Create.md

## POST jobs+import+list
List import jobs
source: https://milvus.io/api-reference/restful/v2.6.x/v2/Import%20(v2)/List.md

## POST jobs+import+describe
Get import job progress
source: https://milvus.io/api-reference/restful/v2.6.x/v2/Import%20(v2)/Get%20Progress.md

## POST resource_groups+create
Create a resource group
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST resource_groups+drop
Drop a resource group
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST resource_groups+describe
Get resource group details
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST resource_groups+list
List all resource groups
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST resource_groups+transfer_replica
Transfer replicas between resource groups
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST collections+fields+add
Add a field to an existing collection
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST privilege_groups+add_privileges_to_group
Add privileges to a privilege group
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

## POST privilege_groups+remove_privileges_from_group
Remove privileges from a privilege group
source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

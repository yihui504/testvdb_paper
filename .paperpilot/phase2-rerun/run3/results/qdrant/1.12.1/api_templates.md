# API Templates — qdrant v1.18.2

## PUT collections+{collection_name}
Create a new collection with vector and index configuration
source: https://api.qdrant.tech/v-1-18-x/api-reference/collections/create-collection

## PATCH collections+{collection_name}
Update collection parameters
source: https://api.qdrant.tech/v-1-18-x/api-reference

## DELETE collections+{collection_name}
Delete a collection and all its data
source: https://api.qdrant.tech/v-1-18-x/api-reference

## GET collections
List all collections
source: https://api.qdrant.tech/v-1-18-x/api-reference

## GET collections+{collection_name}
Get detailed collection configuration and status
source: https://api.qdrant.tech/v-1-18-x/api-reference/collections/get-collection

## GET collections+{collection_name}+exists
Check if a collection exists
source: https://api.qdrant.tech/v-1-18-x/api-reference

## GET collections+{collection_name}+optimizations
Get collection optimization progress
source: https://api.qdrant.tech/v-1-18-x/api-reference

## PUT collections+{collection_name}+vectors+{vector_name}
Create a named vector for an existing collection
source: https://api.qdrant.tech/v-1-18-x/api-reference

## DELETE collections+{collection_name}+vectors+{vector_name}
Delete a named vector from a collection
source: https://api.qdrant.tech/v-1-18-x/api-reference

## PUT collections+{collection_name}+points
Upsert or insert points into a collection
source: https://api.qdrant.tech/v-1-18-x/api-reference/points/upsert-points

## POST collections+{collection_name}+points
Get points by IDs
source: https://api.qdrant.tech/v-1-18-x/api-reference

## POST collections+{collection_name}+points+delete
Delete points by IDs or filter
source: https://api.qdrant.tech/v-1-18-x/api-reference

## POST collections+{collection_name}+points+scroll
Scroll points with pagination
source: https://api.qdrant.tech/v-1-18-x/api-reference

## POST collections+{collection_name}+points+count
Count points matching filter
source: https://api.qdrant.tech/v-1-18-x/api-reference

## POST collections+{collection_name}+points+batch
Batch update points (mixed operations)
source: https://api.qdrant.tech/v-1-18-x/api-reference

## POST collections+{collection_name}+points+payload
Set payload values for points
source: https://api.qdrant.tech/v-1-18-x/api-reference/points/set-payload

## PUT collections+{collection_name}+points+payload
Overwrite entire payload for points
source: https://api.qdrant.tech/v-1-18-x/api-reference

## POST collections+{collection_name}+points+payload+delete
Delete specific payload keys from points
source: https://api.qdrant.tech/v-1-18-x/api-reference

## POST collections+{collection_name}+points+payload+clear
Clear ALL payload from matched points
source: https://api.qdrant.tech/v-1-18-x/api-reference

## PUT collections+{collection_name}+points+vectors
Update vectors for existing points
source: https://api.qdrant.tech/v-1-18-x/api-reference

## POST collections+{collection_name}+points+vectors+delete
Delete specified named vectors from points
source: https://api.qdrant.tech/v-1-18-x/api-reference

## POST collections+{collection_name}+facet
Facet points by a payload key
source: https://api.qdrant.tech/v-1-18-x/api-reference

## POST collections+{collection_name}+points+search
Search for the closest points to a given query vector
source: https://api.qdrant.tech/v-1-18-x/api-reference/search/points

## POST collections+{collection_name}+points+search+batch
Search multiple queries in batch
source: https://api.qdrant.tech/v-1-18-x/api-reference

## POST collections+{collection_name}+points+search+groups
Search points grouped by a payload field
source: https://api.qdrant.tech/v-1-18-x/api-reference

## POST collections+{collection_name}+points+query
Universal Query API with multi-stage pipeline support
source: https://api.qdrant.tech/v-1-18-x/api-reference

## POST collections+{collection_name}+points+query+batch
Batch universal queries
source: https://api.qdrant.tech/v-1-18-x/api-reference

## POST collections+{collection_name}+points+query+groups
Universal query grouped by a payload field
source: https://api.qdrant.tech/v-1-18-x/api-reference

## POST collections+{collection_name}+points+recommend
Recommend points based on positive/negative examples
source: https://api.qdrant.tech/v-1-18-x/api-reference

## POST collections+{collection_name}+points+recommend+batch
Batch recommend queries
source: https://api.qdrant.tech/v-1-18-x/api-reference

## POST collections+{collection_name}+points+recommend+groups
Recommend points grouped by a payload field
source: https://api.qdrant.tech/v-1-18-x/api-reference

## POST collections+{collection_name}+points+discover
Discover points based on semantic discovery
source: https://api.qdrant.tech/v-1-18-x/api-reference

## POST collections+{collection_name}+points+discover+batch
Batch discover queries
source: https://api.qdrant.tech/v-1-18-x/api-reference

## POST collections+{collection_name}+points+search+matrix+offsets
Compute distance matrix for offset-based pairs
source: https://api.qdrant.tech/v-1-18-x/api-reference

## POST collections+{collection_name}+points+search+matrix+pairs
Compute distance matrix for specific pairs
source: https://api.qdrant.tech/v-1-18-x/api-reference

## PUT collections+{collection_name}+index
Create a payload field index
source: https://api.qdrant.tech/v-1-18-x/api-reference

## DELETE collections+{collection_name}+index+{field_name}
Delete a payload field index
source: https://api.qdrant.tech/v-1-18-x/api-reference

## GET aliases
List all collection aliases
source: https://api.qdrant.tech/v-1-18-x/api-reference

## GET collections+{collection_name}+aliases
List aliases for a specific collection
source: https://api.qdrant.tech/v-1-18-x/api-reference

## POST collections+aliases
Update aliases (create, delete, rename) atomically
source: https://api.qdrant.tech/v-1-18-x/api-reference

## GET collections+{collection_name}+snapshots
List snapshots for a collection
source: https://api.qdrant.tech/v-1-18-x/api-reference/snapshots/list-snapshots

## POST collections+{collection_name}+snapshots
Create a collection snapshot
source: https://api.qdrant.tech/v-1-18-x/api-reference

## GET collections+{collection_name}+snapshots+{snapshot_name}
Download a collection snapshot
source: https://api.qdrant.tech/v-1-18-x/api-reference

## DELETE collections+{collection_name}+snapshots+{snapshot_name}
Delete a collection snapshot
source: https://api.qdrant.tech/v-1-18-x/api-reference

## PUT collections+{collection_name}+snapshots+recover
Recover a collection from a snapshot
source: https://api.qdrant.tech/v-1-18-x/api-reference

## POST collections+{collection_name}+snapshots+upload
Upload a snapshot for collection recovery
source: https://api.qdrant.tech/v-1-18-x/api-reference

## GET snapshots
List storage-level snapshots
source: https://api.qdrant.tech/v-1-18-x/api-reference

## POST snapshots
Create a full storage snapshot (all collections)
source: https://api.qdrant.tech/v-1-18-x/api-reference

## GET snapshots+{snapshot_name}
Download a storage snapshot
source: https://api.qdrant.tech/v-1-18-x/api-reference

## DELETE snapshots+{snapshot_name}
Delete a storage snapshot
source: https://api.qdrant.tech/v-1-18-x/api-reference

## GET collections+{collection_name}+shards+{shard_id}+snapshots
List shard snapshots
source: https://api.qdrant.tech/v-1-18-x/api-reference

## POST collections+{collection_name}+shards+{shard_id}+snapshots
Create a shard snapshot
source: https://api.qdrant.tech/v-1-18-x/api-reference

## GET collections+{collection_name}+shards+{shard_id}+snapshot
Download a shard snapshot
source: https://api.qdrant.tech/v-1-18-x/api-reference

## PUT collections+{collection_name}+shards+{shard_id}+snapshots+recover
Recover a shard from a snapshot
source: https://api.qdrant.tech/v-1-18-x/api-reference

## POST collections+{collection_name}+shards+{shard_id}+snapshots+upload
Upload a shard snapshot for recovery
source: https://api.qdrant.tech/v-1-18-x/api-reference

## DELETE collections+{collection_name}+shards+{shard_id}+snapshots+{snapshot_name}
Delete a shard snapshot
source: https://api.qdrant.tech/v-1-18-x/api-reference

## GET cluster
Get cluster status and peer information
source: https://api.qdrant.tech/v-1-18-x/api-reference

## GET cluster+telemetry
Get detailed cluster telemetry data
source: https://api.qdrant.tech/v-1-18-x/api-reference

## DELETE cluster+peer+{peer_id}
Remove a peer from the cluster
source: https://api.qdrant.tech/v-1-18-x/api-reference

## POST cluster+recover
Recover current peer Raft state
source: https://api.qdrant.tech/v-1-18-x/api-reference

## GET collections+{collection_name}+cluster
Get shard distribution for a collection
source: https://api.qdrant.tech/v-1-18-x/api-reference

## POST collections+{collection_name}+cluster
Update collection cluster setup (move shards, manage replication)
source: https://api.qdrant.tech/v-1-18-x/api-reference

## GET collections+{collection_name}+shards
List shard keys for a collection
source: https://api.qdrant.tech/v-1-18-x/api-reference

## PUT collections+{collection_name}+shards
Create a shard key for a collection
source: https://api.qdrant.tech/v-1-18-x/api-reference/distributed/create-shard-key

## POST collections+{collection_name}+shards+delete
Delete a shard key
source: https://api.qdrant.tech/v-1-18-x/api-reference

## GET 
Root service info (version, commit, title)
source: https://api.qdrant.tech/v-1-18-x/api-reference

## GET healthz
Kubernetes health check endpoint
source: https://api.qdrant.tech/v-1-18-x/api-reference

## GET livez
Kubernetes liveness check endpoint
source: https://api.qdrant.tech/v-1-18-x/api-reference

## GET readyz
Kubernetes readiness check endpoint
source: https://api.qdrant.tech/v-1-18-x/api-reference

## GET metrics
Prometheus metrics endpoint
source: https://api.qdrant.tech/v-1-18-x/api-reference

## GET telemetry
Get detailed telemetry data
source: https://api.qdrant.tech/v-1-18-x/api-reference

## GET issues
Get list of issues (Beta API)
source: https://api.qdrant.tech/v-1-18-x/api-reference

## DELETE issues
Clear all issues (Beta API)
source: https://api.qdrant.tech/v-1-18-x/api-reference

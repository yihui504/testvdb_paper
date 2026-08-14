# API Templates — qdrant v1.18.3

## PUT /collections/{collection_name}
Create a new collection with vector configuration
source: https://qdrant.tech/documentation/collections/

## GET /collections/{collection_name}
Get collection information
source: https://qdrant.tech/documentation/collections/

## DELETE /collections/{collection_name}
Delete a collection
source: https://qdrant.tech/documentation/rest-api/delete-collections/

## PATCH /collections/{collection_name}
Update collection parameters
source: https://qdrant.tech/documentation/collections/

## GET /collections
List all collections
source: https://qdrant.tech/documentation/collections/

## PUT /collections/{collection_name}/points
Batch insert or update multiple points
source: https://qdrant.tech/documentation/rest-api/put-points/

## GET /collections/{collection_name}/points/{point_id}
Get a single point by ID
source: https://qdrant.tech/documentation/rest-api/get-point/

## POST /collections/{collection_name}/points/delete
Delete points from collection
source: https://qdrant.tech/documentation/rest-api/delete-points/

## POST /collections/{collection_name}/points/scroll
Scroll through all points in a collection with optional filtering
source: https://qdrant.tech/documentation/rest-api/scroll-points/

## POST /collections/{collection_name}/points/query
Query points with a vector using advanced search parameters
source: https://qdrant.tech/documentation/concepts/search/

## PUT /collections/{collection_name}/index
Create HNSW index on payload field
source: https://qdrant.tech/documentation/indexing/

## POST /collections/{collection_name}/snapshots
Create a snapshot of the collection
source: https://qdrant.tech/documentation/concepts/snapshots/

## GET /collections/{collection_name}/snapshots
List all snapshots of the collection
source: https://qdrant.tech/documentation/concepts/snapshots/

## GET /collections/{collection_name}/snapshots/{snapshot_name}
Download a specific snapshot
source: https://qdrant.tech/documentation/concepts/snapshots/

## DELETE /collections/{collection_name}/snapshots/{snapshot_name}
Delete a specific snapshot
source: https://qdrant.tech/documentation/concepts/snapshots/

## POST /collections/{collection_name}/points/search
Search for nearest points
source: https://qdrant.tech/documentation/rest-api/search-points/

## POST /collections/{collection_name}/points/recommend
Recommend points based on positive/negative examples
source: https://qdrant.tech/documentation/concepts/search/

## GET /cluster
Get cluster status and topology
source: https://qdrant.tech/documentation/rest-api/get-cluster/

## GET /
Health check endpoint
source: https://qdrant.tech/documentation/rest-api/health/

## GET /metrics
Get Prometheus metrics
source: https://qdrant.tech/documentation/rest-api/metrics/

## POST /collections/{collection_name}/points/query/groups
Group search results by a specific field
source: https://qdrant.tech/documentation/concepts/search/

## DELETE /collections/{collection_name}/index/{field_name}
Delete index on payload field
source: https://qdrant.tech/documentation/concepts/indexing/

## GET /collections/{collection_name}/cluster
Get collection-specific cluster information
source: https://qdrant.tech/documentation/concepts/distributed/

## PUT /collections/{collection_name}/shards
Update shard configuration
source: https://qdrant.tech/documentation/concepts/distributed/

## PUT /collections/{collection_name}/snapshots/recover
Recover collection from snapshot
source: https://qdrant.tech/documentation/concepts/snapshots/

## GET /healthz
Check service health
source: https://qdrant.tech/documentation/

## POST /collections/{collection_name}/points/count
Count points in a collection matching a filter (cardinality estimation)
source: https://qdrant.tech/documentation/rest-api/count-points/

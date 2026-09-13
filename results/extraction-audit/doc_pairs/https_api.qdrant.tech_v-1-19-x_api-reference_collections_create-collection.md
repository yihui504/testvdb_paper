> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://api.qdrant.tech/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://api.qdrant.tech/_mcp/server.

# Create a collection

PUT http://localhost:6333/collections/{collection_name}
Content-Type: application/json

Creates a new collection with the given parameters.

Reference: https://api.qdrant.tech/api-reference/collections/create-collection

## Authentication

- `api-key` header (required)

## Servers

- `http://localhost:6333` (http, default)
- `https://localhost:6333` (https)

## Request

### Path parameters

- `collection_name` (string, required) — Name of the new collection

### Query parameters

- `timeout` (integer, optional) — Wait for operation commit timeout in seconds. If timeout is reached - request will return with service error.

### Body (application/json)

- `vectors` (object or map from string to object, optional) — Vector params separator for single and multiple vector modes Single mode: \{ "size": 128, "distance": "Cosine" } or multiple mode: \{ "default": \{ "size": 128, "distance": "Cosine" } }
  - VectorParams
    - `size` (uint64, required) — Size of a vectors used
    - `distance` (enum, required) — Type of internal tags, build from payload Distance function types used to compare vectors
      - Allowed values: `Cosine`, `Euclid`, `Dot`, `Manhattan`
    - `hnsw_config` (object or any, optional) — Custom params for HNSW index. If none - values from collection configuration are used.
      - HnswConfigDiff
        - `m` (integer, optional, nullable) — Number of edges per node in the index graph. Larger the value - more accurate the search, more space required.
        - `ef_construct` (integer, optional, nullable) — Number of neighbours to consider during the index building. Larger the value - more accurate the search, more time required to build the index.
        - `full_scan_threshold` (integer, optional, nullable) — Minimal size threshold (in KiloBytes) below which full-scan is preferred over HNSW search. This measures the total size of vectors being queried against. When the maximum estimated amount of points that a condition satisfies is smaller than `full_scan_threshold_kb`, the query planner will use full-scan search instead of HNSW index traversal for better performance. Note: 1Kb = 1 vector of size 256
        - `max_indexing_threads` (integer, optional, nullable) — Number of parallel threads used for background index building. If 0 - automatically select from 8 to 16. Best to keep between 8 and 16 to prevent likelihood of building broken/inefficient HNSW graphs. On small CPUs, less threads are used.
        - `memory` (enum or any, optional) — Memory placement of the HNSW graph. Overrides the deprecated `on_disk` flag if both are set. Default: `cached` (`cold` if `on_disk` is set to true).
        - `payload_m` (integer, optional, nullable) — Custom M param for additional payload-aware HNSW links. If not set, default M will be used.
        - `inline_storage` (boolean, optional, nullable) — Store copies of original and quantized vectors within the HNSW index file. Default: false. Enabling this option will trade the search speed for disk usage by reducing amount of random seeks during the search. Requires quantized vectors to be enabled. Multi-vectors are not supported.
        - `on_disk` (boolean, optional, nullable, deprecated) — Deprecated: use `memory` instead. Store HNSW index on disk. If set to false, the index will be stored in RAM. Default: false
    - `quantization_config` (object or object or object or object or any, optional) — Custom params for quantization. If none - values from collection configuration are used.
    - `memory` (enum or any, optional) — Memory placement of the original vector storage. Overrides the deprecated `on_disk` flag if both are set. `pinned` is not supported for dense vector storage. Default: `cached` (`cold` if `on_disk` is set to true).
    - `datatype` (enum or any, optional) — Defines which datatype should be used to represent vectors in the storage. Choosing different datatypes allows to optimize memory usage and performance vs accuracy. - For `float32` datatype - vectors are stored as single-precision floating point numbers, 4 bytes. - For `float16` datatype - vectors are stored as half-precision floating point numbers, 2 bytes. - For `uint8` datatype - vectors are stored as unsigned 8-bit integers, 1 byte. It expects vector elements to be in range `[0, 255]`. - For `turbo4` datatype - vectors are quantized to 4 bits per element using the TurboQuant algorithm.
    - `multivector_config` (object or any, optional)
      - MultiVectorConfig
        - `comparator` (enum, required)
          - Allowed values: `max_sim`
    - `on_disk` (boolean, optional, nullable, deprecated) — Deprecated: use `memory` instead. If true, vectors are served from disk, improving RAM usage at the cost of latency Default: false
- `shard_number` (uint, optional, nullable) — For auto sharding: Number of shards in collection. - Default is 1 for standalone, otherwise equal to the number of nodes - Minimum is 1 For custom sharding: Number of shards in collection per shard group. - Default is 1, meaning that each shard key will be mapped to a single shard - Minimum is 1
- `sharding_method` (enum or any, optional) — Sharding method Default is Auto - points are distributed across all available shards Custom - points are distributed across shards according to shard key
- `replication_factor` (uint, optional, nullable) — Number of shards replicas. Default is 1 Minimum is 1
- `write_consistency_factor` (uint, optional, nullable) — Defines how many replicas should apply the operation for us to consider it successful. Increasing this number will make the collection more resilient to inconsistencies, but will also make it fail if not enough replicas are available. Does not have any performance impact.
- `payload` (object or any, optional) — Configuration of the payload storage
  - PayloadStorageParams
    - `memory` (enum or any, optional) — Memory placement of the payload storage. Overrides the deprecated `on_disk_payload` flag if both are set. `pinned` is not supported for payload storage. Default: `cold` (`cached` if `on_disk_payload` is set to false).
- `hnsw_config` (object or any, optional) — Custom params for HNSW index. If none - values from service configuration file are used.
  - HnswConfigDiff
    - `m` (integer, optional, nullable) — Number of edges per node in the index graph. Larger the value - more accurate the search, more space required.
    - `ef_construct` (integer, optional, nullable) — Number of neighbours to consider during the index building. Larger the value - more accurate the search, more time required to build the index.
    - `full_scan_threshold` (integer, optional, nullable) — Minimal size threshold (in KiloBytes) below which full-scan is preferred over HNSW search. This measures the total size of vectors being queried against. When the maximum estimated amount of points that a condition satisfies is smaller than `full_scan_threshold_kb`, the query planner will use full-scan search instead of HNSW index traversal for better performance. Note: 1Kb = 1 vector of size 256
    - `max_indexing_threads` (integer, optional, nullable) — Number of parallel threads used for background index building. If 0 - automatically select from 8 to 16. Best to keep between 8 and 16 to prevent likelihood of building broken/inefficient HNSW graphs. On small CPUs, less threads are used.
    - `memory` (enum or any, optional) — Memory placement of the HNSW graph. Overrides the deprecated `on_disk` flag if both are set. Default: `cached` (`cold` if `on_disk` is set to true).
    - `payload_m` (integer, optional, nullable) — Custom M param for additional payload-aware HNSW links. If not set, default M will be used.
    - `inline_storage` (boolean, optional, nullable) — Store copies of original and quantized vectors within the HNSW index file. Default: false. Enabling this option will trade the search speed for disk usage by reducing amount of random seeks during the search. Requires quantized vectors to be enabled. Multi-vectors are not supported.
    - `on_disk` (boolean, optional, nullable, deprecated) — Deprecated: use `memory` instead. Store HNSW index on disk. If set to false, the index will be stored in RAM. Default: false
- `wal_config` (object or any, optional) — Custom params for WAL. If none - values from service configuration file are used.
  - WalConfigDiff
    - `wal_capacity_mb` (integer, optional, nullable) — Size of a single WAL segment in MB
    - `wal_segments_ahead` (integer, optional, nullable) — Number of WAL segments to create ahead of actually used ones
    - `wal_retain_closed` (integer, optional, nullable) — Number of closed WAL segments to retain
- `optimizers_config` (object or any, optional) — Custom params for Optimizers. If none - values from service configuration file are used.
  - OptimizersConfigDiff
    - `deleted_threshold` (double, optional, nullable) — The minimal fraction of deleted vectors in a segment, required to perform segment optimization
    - `vacuum_min_vector_number` (integer, optional, nullable) — The minimal number of vectors in a segment, required to perform segment optimization
    - `default_segment_number` (integer, optional, nullable) — Target amount of segments optimizer will try to keep. Real amount of segments may vary depending on multiple parameters: - Amount of stored points - Current write RPS It is recommended to select default number of segments as a factor of the number of search threads, so that each segment would be handled evenly by one of the threads If `default_segment_number = 0`, will be automatically selected by the number of available CPUs
    - `max_segment_size` (integer, optional, nullable) — Do not create segments larger this size (in kilobytes). Large segments might require disproportionately long indexation times, therefore it makes sense to limit the size of segments. If indexation speed have more priority for your - make this parameter lower. If search speed is more important - make this parameter higher. Note: 1Kb = 1 vector of size 256
    - `indexing_threshold` (integer, optional, nullable) — Maximum size (in kilobytes) of vectors allowed for plain index, exceeding this threshold will enable vector indexing Default value is 20,000, based on \<[https://github.com/google-research/google-research/blob/master/scann/docs/algorithms.md>](https://github.com/google-research/google-research/blob/master/scann/docs/algorithms.md>). To disable vector indexing, set to `0`. Note: 1kB = 1 vector of size 256.
    - `flush_interval_sec` (uint64, optional, nullable) — Minimum interval between forced flushes.
    - `max_optimization_threads` (enum or integer or any, optional) — Max number of threads (jobs) for running optimizations per shard. Note: each optimization job will also use `max_indexing_threads` threads by itself for index building. If "auto" - have no limit and choose dynamically to saturate CPU. If 0 - no optimization threads, optimizations will be disabled.
    - `prevent_unoptimized` (boolean, optional, nullable) — If enabled, the service will try to prevent the creation of large unoptimized segments. When enabled, new points written to segments larger than the indexing threshold are stored as "deferred points": they are persisted in the WAL and segments, but excluded from read/search results until the corresponding segments are optimized (e.g. indexed, quantized, or moved to mmap storage). Update requests with `wait=true` will only return after the deferred points become visible, which may significantly increase the perceived latency between submitting an update and its completion. Update requests with `wait=false` are not affected. Default is disabled.
    - `memmap_threshold` (integer, optional, nullable, deprecated) — Maximum size (in kilobytes) of vectors to store in-memory per segment. Segments larger than this threshold will be stored as read-only memmapped file. Memmap storage is disabled by default, to enable it, set this threshold to a reasonable value. To disable memmap storage, set this to `0`. Note: 1Kb = 1 vector of size 256 Deprecated since Qdrant 1.15.0
- `quantization_config` (object or object or object or object or any, optional) — Quantization parameters. If none - quantization is disabled.
- `sparse_vectors` (map from string to object, optional, nullable) — Sparse vector data config.
  - `index` (object or any, optional) — Custom params for index. If none - values from collection configuration are used.
    - SparseIndexParams
      - `full_scan_threshold` (integer, optional, nullable) — We prefer a full scan search upto (excluding) this number of vectors. Note: this is number of vectors, not KiloBytes.
      - `memory` (enum or any, optional) — Memory placement of the index. Overrides the deprecated `on_disk` flag if both are set. Default: `pinned` (`cold` if `on_disk` is set to true).
      - `datatype` (enum or any, optional) — Defines which datatype should be used for the index. Choosing different datatypes allows to optimize memory usage and performance vs accuracy. - For `float32` datatype - vectors are stored as single-precision floating point numbers, 4 bytes. - For `float16` datatype - vectors are stored as half-precision floating point numbers, 2 bytes. - For `uint8` datatype - vectors are quantized to unsigned 8-bit integers, 1 byte. Quantization to fit byte range `[0, 255]` happens during indexing automatically, so the actual vector data does not need to conform to this range.
      - `on_disk` (boolean, optional, nullable, deprecated) — Deprecated: use `memory` instead. Store index on disk. If set to false, the index will be stored in RAM. Default: false
  - `modifier` (enum or any, optional) — Configures addition value modifications for sparse vectors. Default: none
- `strict_mode_config` (object or any, optional) — Strict-mode config.
  - StrictModeConfig
    - `enabled` (boolean, optional, nullable) — Whether strict mode is enabled for a collection or not.
    - `max_query_limit` (integer, optional, nullable) — Max allowed `limit` parameter for all APIs that don't have their own max limit.
    - `max_timeout` (integer, optional, nullable) — Max allowed `timeout` parameter.
    - `unindexed_filtering_retrieve` (boolean, optional, nullable) — Allow usage of unindexed fields in retrieval based (e.g. search) filters.
    - `unindexed_filtering_update` (boolean, optional, nullable) — Allow usage of unindexed fields in filtered updates (e.g. delete by payload).
    - `search_max_hnsw_ef` (integer, optional, nullable) — Max HNSW ef value allowed in search parameters.
    - `search_allow_exact` (boolean, optional, nullable) — Whether exact search is allowed.
    - `search_max_oversampling` (double, optional, nullable) — Max oversampling value allowed in search.
    - `upsert_max_batchsize` (integer, optional, nullable) — Max batchsize when upserting
    - `search_max_batchsize` (integer, optional, nullable) — Max batchsize when searching
    - `max_collection_vector_size_bytes` (integer, optional, nullable) — Max size of a collections vector storage in bytes, ignoring replicas.
    - `read_rate_limit` (integer, optional, nullable) — Max number of read operations per minute per replica
    - `write_rate_limit` (integer, optional, nullable) — Max number of write operations per minute per replica
    - `max_collection_payload_size_bytes` (integer, optional, nullable) — Max size of a collections payload storage in bytes
    - `max_points_count` (integer, optional, nullable) — Max number of points estimated in a collection
    - `filter_max_conditions` (integer, optional, nullable) — Max conditions a filter can have.
    - `condition_max_size` (integer, optional, nullable) — Max size of a condition, eg. items in `MatchAny`.
    - `multivector_config` (map from string to object or any, optional) — Multivector strict mode configuration
    - `sparse_config` (map from string to object or any, optional) — Sparse vector strict mode configuration
    - `max_payload_index_count` (integer, optional, nullable) — Max number of payload indexes in a collection
    - `max_resident_memory_percent` (integer, optional, nullable, deprecated) — Deprecated: use the node-wide quota config (`PUT /quotas`) instead, which caps the same resource for every collection. Scheduled for removal in 1.21. Reject memory-consuming update operations (e.g. upsert, set payload) when the process resident memory exceeds this percentage of total system memory (or cgroup limit). Value in [1, 100]. Memory is a node-wide resource, so this only tightens the quota for one collection; it cannot lift it. Delete operations are not affected, so callers can still free memory.
- `metadata` (map from string to any or any, optional) — Arbitrary JSON metadata for the collection This can be used to store application-specific information such as creation time, migration data, inference model info, etc.
- `on_disk_payload` (boolean, optional, nullable, deprecated) — Deprecated: use `payload.memory` instead. If true - point's payload will not be stored in memory. It will be read from the disk every time it is requested. This setting saves RAM by (slightly) increasing the response time. Note: those payload values that are involved in filtering and are indexed - remain in RAM. Default: true

## Response

### 200

successful operation

- `usage` (object or any, optional)
  - Usage
    - `hardware` (object or any, optional)
      - HardwareUsage
        - `cpu` (integer, required)
        - `payload_io_read` (integer, required)
        - `payload_io_write` (integer, required)
        - `payload_index_io_read` (integer, required)
        - `payload_index_io_write` (integer, required)
        - `vector_io_read` (integer, required)
        - `vector_io_write` (integer, required)
    - `inference` (object or any, optional)
      - InferenceUsage
        - `models` (map from string to object, required)
          - `tokens` (uint64, required)
- `time` (double, optional) — Time spent to process this request
- `status` (string, optional)
- `result` (boolean, optional)

## Examples

**Request**

```json
{}
```

**Response**

```json
{
  "usage": {
    "hardware": {
      "cpu": 1,
      "payload_io_read": 1,
      "payload_io_write": 1,
      "payload_index_io_read": 1,
      "payload_index_io_write": 1,
      "vector_io_read": 1,
      "vector_io_write": 1
    },
    "inference": {
      "models": {}
    }
  },
  "time": 0.002,
  "status": "ok",
  "result": true
}
```

**SDK Code**

```java
import io.qdrant.client.QdrantClient;
import io.qdrant.client.QdrantGrpcClient;

import io.qdrant.client.grpc.Collections.Distance;
import io.qdrant.client.grpc.Collections.VectorParams;

QdrantClient client = new QdrantClient(
    QdrantGrpcClient.newBuilder("localhost", 6334, false).build());

client.createCollectionAsync("{collection_name}",
        VectorParams.newBuilder().setDistance(Distance.Cosine).setSize(100).build()).get();

// Or with sparse vectors

client.createCollectionAsync(
    CreateCollection.newBuilder()
        .setCollectionName("{collection_name}")
        .setSparseVectorsConfig(
            Collections.SparseVectorConfig.newBuilder().putMap(
                "splade-model-name",
                Collections.SparseVectorParams.newBuilder()
                    .setIndex(
                        Collections.SparseIndexConfig
                            .newBuilder()
                            .setOnDisk(false)
                            .build()
                    ).build()
            ).build()
        ).build()
).get();
```

```go
package client

import (
	"context"

	"github.com/qdrant/go-client/qdrant"
)

func createCollection() {
	client, err := qdrant.NewClient(&qdrant.Config{
		Host: "localhost",
		Port: 6334,
	})
	if err != nil {
		panic(err)
	}

	err = client.CreateCollection(context.Background(), &qdrant.CreateCollection{
		CollectionName: "{collection_name}",
		VectorsConfig: qdrant.NewVectorsConfig(&qdrant.VectorParams{
			Size:     100,
			Distance: qdrant.Distance_Cosine,
		}),
	})
	if err != nil {
		panic(err)
	}
}

```

```csharp
using Qdrant.Client;
using Qdrant.Client.Grpc;

var client = new QdrantClient("localhost", 6334);

await client.CreateCollectionAsync(
	collectionName: "{collection_name}",
	vectorsConfig: new VectorParams { Size = 100, Distance = Distance.Cosine }
);

// Or with sparse vectors

await client.CreateCollectionAsync(
	collectionName: "{collection_name}",
	sparseVectorsConfig: ("splade-model-name", new SparseVectorParams{
        Index = new SparseIndexConfig {
            OnDisk = false,
        }
    })
);
```

```typescript
import { QdrantClient } from "@qdrant/js-client-rest";

const client = new QdrantClient({ host: "localhost", port: 6333 });

client.createCollection("{collection_name}", {
  vectors: { size: 100, distance: "Cosine" },
});

// or with sparse vectors

client.createCollection("{collection_name}", {
  vectors: { size: 100, distance: "Cosine" },
  sparse_vectors: {
    "splade-model-name": {
      index: {
        on_disk: false
      }
    }
  }
});
```

```rust
use qdrant_client::qdrant::{CreateCollectionBuilder, Distance, VectorParamsBuilder};
use qdrant_client::Qdrant;

let client = Qdrant::from_url("http://localhost:6334").build()?;

client
    .create_collection(
        CreateCollectionBuilder::new("{collection_name}")
            .vectors_config(VectorParamsBuilder::new(100, Distance::Cosine)),
    )
    .await?;

```

```python
from qdrant_client import QdrantClient, models

client = QdrantClient(url="http://localhost:6333")

client.create_collection(
    collection_name="{collection_name}",
    vectors_config=models.VectorParams(size=100, distance=models.Distance.COSINE),
)

```

```ruby
require 'uri'
require 'net/http'

url = URI("http://localhost:6333/collections/collection_name")

http = Net::HTTP.new(url.host, url.port)

request = Net::HTTP::Put.new(url)
request["api-key"] = '<apiKey>'
request["Content-Type"] = 'application/json'
request.body = "{}"

response = http.request(request)
puts response.read_body
```

```php
<?php
require_once('vendor/autoload.php');

$client = new \GuzzleHttp\Client();

$response = $client->request('PUT', 'http://localhost:6333/collections/collection_name', [
  'body' => '{}',
  'headers' => [
    'Content-Type' => 'application/json',
    'api-key' => '<apiKey>',
  ],
]);

echo $response->getBody();
```

```swift
import Foundation

let headers = [
  "api-key": "<apiKey>",
  "Content-Type": "application/json"
]
let parameters = [] as [String : Any]

let postData = JSONSerialization.data(withJSONObject: parameters, options: [])

let request = NSMutableURLRequest(url: NSURL(string: "http://localhost:6333/collections/collection_name")! as URL,
                                        cachePolicy: .useProtocolCachePolicy,
                                    timeoutInterval: 10.0)
request.httpMethod = "PUT"
request.allHTTPHeaderFields = headers
request.httpBody = postData as Data

let session = URLSession.shared
let dataTask = session.dataTask(with: request as URLRequest, completionHandler: { (data, response, error) -> Void in
  if (error != nil) {
    print(error as Any)
  } else {
    let httpResponse = response as? HTTPURLResponse
    print(httpResponse)
  }
})

dataTask.resume()
```